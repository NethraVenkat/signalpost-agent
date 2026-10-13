import json
import re
from urllib.parse import urlsplit, urlunsplit
from ..budget import SourceFailure
from ..models.envelope import Error
from ..models.evidence import digest
from ..sources.extract import Section, Source, add, missing, response_source
from .candidates import generate, context_from_bulk, legal_name
from .html import Page
from .policy import domain, normalize_url
from .proof import score, phone
from .social import discover, profile_url


def registry_context(envelope, bulk, blobs):
    if bulk is not None:
        row, source = bulk
        return context_from_bulk(row), source, "row:" + envelope.organisation_number + "/column:hjemmeside"
    reference = next((e for e in envelope.evidence if e.locator == "/navn"), None)
    if reference is None:
        return {}, None, ""
    body = (blobs.directory / reference.content_sha256).read_bytes()
    data = json.loads(body)
    address = data.get("forretningsadresse") or {}
    context = {"name": data.get("navn"), "website": data.get("hjemmeside"), "email": data.get("epostadresse"),
               "phone": data.get("telefon"), "municipality": address.get("kommune"), "street": address.get("adresse"),
               "postcode": address.get("postnummer"), "city": address.get("poststed")}
    return context, Source(reference.source_url, body, reference.content_sha256, reference.retrieved_at), "/hjemmeside"


def publish(section, response, org, field, value, locator, span):
    if not span or span not in response.body.decode("utf8", errors="replace") or len(span) > 300:
        raise SourceFailure("invalid_span")
    add(section, response_source(response), org, "website", field, value, locator, span=span,
        source_class="company_owned", method="signalpost.website.v1")


def followup_links(page):
    patterns = [r'kontakt|contact',r'om[- ]oss|about',r'personvern|privacy|vilk[åa]r|terms|impressum']
    ranked=[]
    for link in page.links:
        text=urlsplit(link.href).path+' '+link.text
        priority=next((i for i,p in enumerate(patterns) if re.search(p,text,re.I)),None)
        if priority is not None: ranked.append((priority,link.href))
    return list(dict.fromkeys(url for _,url in sorted(ranked,key=lambda x:x[0])))


async def fetch(org, envelope, bulk, http):
    context, registry_source, registry_locator = registry_context(envelope, bulk, http.blobs)
    section = Section(state="not_available")
    if registry_source and (social := profile_url(normalize_url(context.get("website")) or "")):
        add(section, registry_source, org, "website", "registry_social." + digest(social)[:20],
            {"url": social, "platform": domain(social), "verification": "registry_asserted"}, registry_locator)
    candidates = generate(context)
    leaders = [c.value.get("name") for c in envelope.claims if c.family == "roles" and isinstance(c.value, dict) and (c.value.get("role_type") or {}).get("kode") in {"DAGL", "LEDE"} and c.value.get("name")]
    proved = set()
    successes = []
    attempts = []
    blocked = False
    ambiguous = False
    budget_hit = None
    source_unavailable = False
    registry_failed = False
    fetchable_failures = set()
    checked = set()
    for candidate in candidates:
        pages = []
        best = None
        try:
            response = await http.candidate(candidate, org, proved)
            if response.status in (401, 403, 429):
                raise SourceFailure("http_blocked", f"HTTP {response.status}")
            if not 200 <= response.status < 300:
                if response.status >= 500:
                    source_unavailable = True
                attempts.append({"domain": candidate.domain, "level": "LOW", "reason": f"http_{response.status}"})
                continue
            page = Page(response.body, response.url)
            checked.add(candidate.domain)
            proof = score(page, org, context, candidate.origin, leaders)
            pages.append((response, page))
            best = (proof, response, page)
            if proof.level == "BLOCKED":
                raise SourceFailure("block_page")
            if proof.level not in {"VERIFIED", "REJECT"}:
                seen = {response.url}
                links = followup_links(page)
                for target in links[:2]:
                    target = normalize_url(target)
                    if not target or target in seen or domain(target) != domain(response.url):
                        continue
                    seen.add(target)
                    try:
                        extra = await http.get(target, org, candidate.domain, proved)
                    except SourceFailure as exc:
                        attempts.append({"domain": candidate.domain, "level": "LOW", "reason": exc.code, "page": target})
                        if exc.code in {"website_budget_exhausted", "budget_exhausted", "deadline"}:
                            budget_hit = exc.code
                            break
                        continue
                    if extra.status != 200:
                        continue
                    extra_page = Page(extra.body, extra.url)
                    extra_proof = score(extra_page, org, context, candidate.origin, leaders)
                    if extra_proof.level == 'BLOCKED':
                        attempts.append({'domain':candidate.domain,'origin':candidate.origin,'reason':'block_page','page':target})
                        continue
                    pages.append((extra, extra_page))
                    if extra_proof.level == "REJECT" and extra_proof.reason == "foreign_orgnr":
                        best = (extra_proof, extra, extra_page)
                        break
                    ranks = {"REJECT": -1, "BLOCKED": -1, "LOW": 0, "MEDIUM": 1,'REGISTRY_DECLARED':2, "HIGH": 3, "VERIFIED": 4}
                    if ranks[extra_proof.level] > ranks[best[0].level]:
                        best = (extra_proof, extra, extra_page)
                    if extra_proof.level == "VERIFIED":
                        break
            proof, response, page = best
            attempts.append({"domain": candidate.domain, "level": proof.level, "points": proof.points, "signals": proof.signals, "origin": candidate.origin, "reason": proof.reason})
            if proof.level in {"VERIFIED", "HIGH"} or (proof.level=='REGISTRY_DECLARED' and http.config.registry_declared):
                final_domain = domain(response.url)
                successes.append((candidate, proof, response, page, pages))
                if proof.level == "VERIFIED":
                    proved.add(final_domain)
                    if http.config.website_stop_after_verified:
                        break
            elif proof.level in {"MEDIUM", 'REGISTRY_DECLARED'}:
                ambiguous = True
        except SourceFailure as exc:
            if exc.code in {'website_timeout','website_connect_error','website_http_5xx','dns_timeout','dns_error','dns_unavailable'}:
                source_unavailable = True
                fetchable_failures.add(candidate.domain)
                if candidate.origin == 'registry_website': registry_failed=True
            attempts.append({"domain": candidate.domain,'origin':candidate.origin, "level": "BLOCKED" if exc.code in {"robots", "robots_unavailable", "http_blocked", "block_page"} else "LOW", "reason": exc.code})
            if exc.code in {"robots", "robots_unavailable", "http_blocked", "block_page"}:
                blocked = blocked or candidate.origin == 'registry_website'
                section.errors.append(Error(section="website", code=exc.code, message=f"{candidate.domain}: access refused"))
            if exc.code in {"website_budget_exhausted", "budget_exhausted", "deadline"}:
                budget_hit = exc.code
                break
    unique = {}
    for result in successes:
        root = domain(result[2].url)
        if root not in unique or result[1].level == "VERIFIED":
            unique[root] = result
    choices = list(unique.values())
    if len(choices) > 1:
        verified = [x for x in choices if x[1].level == "VERIFIED"]
        if verified:
            choices = verified
    if len(choices) != 1:
        section.state = 'ambiguous' if len(choices)>1 or ambiguous else 'blocked' if blocked else 'failed' if registry_failed or (fetchable_failures and not checked) or budget_hit else 'not_available'
        if source_unavailable:
            section.errors.append(Error(section="website", code="website_source_unavailable", message="A candidate source could not be checked"))
        if budget_hit:
            section.errors.append(Error(section="website", code=budget_hit, message="Website work ended at configured budget"))
        section.errors.append(Error(section="website", code="website_candidates", message=json.dumps(attempts+http.attempts.get(org,[]), ensure_ascii=False)))
        return section
    candidate, proof, response, page, pages = choices[0]
    p = urlsplit(response.url)
    root_url = urlunsplit((p.scheme, p.netloc, "", "", ""))
    span = page.proof_span(org) if proof.level == "VERIFIED" else page.name_span(proof.token)
    if not span:
        return missing("website", "no_localized_proof", state="ambiguous")
    value = {"final_url": root_url, "identity_level": proof.level, "proof_type": proof.proof_type,
             "proof_page_url": response.url, "signals": proof.signals, "points": proof.points,
             "candidate_origin": candidate.origin, "relationship_note": "group_site" if proof.other_orgnrs else None,
             "other_orgnrs": proof.other_orgnrs}
    publish(section, response, org, "official_website", value, "identity-proof:" + org, span)
    # HIGH combines page signals with authoritative registry/roles facts.
    if proof.level in {"HIGH",'REGISTRY_DECLARED'}:
        registry_refs = [e for e in envelope.evidence if e.source_class == "official_registry"]
        section.evidence.extend(registry_refs)
        section.claims[-1].evidence_ids.extend(e.id for e in registry_refs)
    from .descriptions import extract as descriptions
    descriptions(section,org,section.claims[-1],[(r,p) for r,p in pages if domain(r.url)==domain(response.url)])
    social_seen, contact_seen = set(), set()
    for source_response, source_page in pages:
        if domain(source_response.url) != domain(response.url):
            continue
        for url, source_span in discover(source_page).items():
            if url not in social_seen:
                publish(section, source_response, org, "social_profile." + digest(url)[:20], {"url": url, "platform": domain(url)}, "company-link:" + url, source_span)
                social_seen.add(url)
        contacts = []
        for link in source_page.links:
            if link.href.startswith("tel:") and (number := phone(link.href[4:])):
                contacts.append(("phone", number, link.span))
            if link.href.startswith("mailto:"):
                address = link.href[7:].split("?", 1)[0].strip()
                if address.rsplit("@", 1)[-1].lower() == domain(response.url):
                    contacts.append(("email", address, link.span))
        for match in re.finditer(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", source_page.visible):
            address = match.group()
            if address.rsplit("@", 1)[-1].lower() == domain(response.url):
                contacts.append(("email", address, source_page.span_for(address)[:150]))
        for match in re.finditer(r"(?:telefon|tlf|phone)\s*:?\s*((?:\+47|0047)?[ .()0-9-]{8,20})", source_page.visible, re.I):
            if number := phone(match.group(1)):
                contacts.append(("phone", number, source_page.span_for(match.group(1))[:150]))
        for kind, contact, source_span in contacts:
            if (kind, contact.casefold()) not in contact_seen:
                publish(section, source_response, org, "contact." + kind + "." + digest(contact.casefold())[:20], contact, "contact:" + contact, source_span)
                contact_seen.add((kind, contact.casefold()))
    brand = page.meta.get("og:site_name") or re.split(r"\s+[|–-]\s+", page.title)[0].strip()
    if brand and len(brand) <= 100 and "\ufffd" not in brand and legal_name(brand) != legal_name(context.get("name")) and legal_name(brand) not in {"home", "hjem", "welcome", "velkommen", "kontakt", "contact"}:
        publish(section, response, org, "public_brand", brand, "meta:brand", page.span_for(brand)[:150])
    section.state = "available"
    http.accepted_pages[org] = [(r, p) for r, p in pages if domain(r.url) == domain(response.url)]
    envelope.run.refresh['website'] = {'checked_urls': sorted({r.url for r, _ in http.accepted_pages[org]})}
    section.errors.append(Error(section='website',code='website_candidates',message=json.dumps(attempts+http.attempts.get(org,[]),ensure_ascii=False)))
    return section
