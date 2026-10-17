from ..workers import offload
import html
import json
import asyncio
import re
from urllib.parse import urlsplit, urlunsplit
from ..budget import SourceFailure
from ..models.envelope import Error
from ..models.evidence import digest
import xml.etree.ElementTree as ET
from ..sources.extract import Section, Source, add, missing, response_source
from .candidates import generate, context_from_bulk, legal_name, Candidate, GENERIC
from .html import Page
from .policy import domain, normalize_url, SOCIAL, DIRECTORIES, FREE_MAIL
from .proof import score, phone, extract_entity_cards, find_containing_card
from .social import discover, profile_url


def extract_sitemap_domains(xml_body, legal_nm, brand_nm):
    raw = xml_body.decode('utf-8', errors='replace')
    if re.search(r'<!\s*(?:DOCTYPE|ENTITY)', raw, re.I): return []
    try: root = ET.fromstring(raw)
    except Exception: return []
    tokens = [t.lower() for t in legal_name(legal_nm).split() if t not in GENERIC and len(t) >= 4]
    if brand_nm: tokens.append(brand_nm.lower())
    urls = []
    for elem in root.iter():
        tag = elem.tag.rsplit('}', 1)[-1]
        if tag == 'loc' and elem.text:
            urls.append(elem.text.strip())
    discovered = []
    seen = set()
    for u in urls:
        norm = normalize_url(u)
        d = domain(norm) if norm else ''
        if not d or d in seen or d in SOCIAL | DIRECTORIES | FREE_MAIL: continue
        d_clean = re.sub(r'[^a-z0-9]', '', d.lower().split('.')[0])
        if any(tok in d_clean for tok in tokens):
            seen.add(d)
            discovered.append((norm, d))
            if len(discovered) >= 5: break
    return discovered


def extract_rss_domains(xml_body, legal_nm, brand_nm):
    raw = xml_body.decode('utf-8', errors='replace')
    if re.search(r'<!\s*(?:DOCTYPE|ENTITY)', raw, re.I): return []
    try: root = ET.fromstring(raw)
    except Exception: return []
    tokens = [t.lower() for t in legal_name(legal_nm).split() if t not in GENERIC and len(t) >= 3]
    if brand_nm: tokens.append(brand_nm.lower())
    discovered = []
    seen = set()
    for item in root.iter():
        tag = item.tag.rsplit('}', 1)[-1]
        if tag in ('item', 'entry'):
            link = next((e.text for e in item if e.tag.rsplit('}', 1)[-1] == 'link' and e.text), None)
            if not link:
                link = next((e.get('href') for e in item if e.tag.rsplit('}', 1)[-1] == 'link' and e.get('href')), None)
            title = next((e.text for e in item if e.tag.rsplit('}', 1)[-1] == 'title' and e.text), '') or ''
            desc = next((e.text for e in item if e.tag.rsplit('}', 1)[-1] in ('description', 'summary') and e.text), '') or ''
            text = f'{title} {desc}'.lower()
            if any(tok in text for tok in tokens) and link:
                norm = normalize_url(link)
                d = domain(norm) if norm else ''
                if d and d not in seen and d not in SOCIAL | DIRECTORIES | FREE_MAIL:
                    seen.add(d)
                    discovered.append((norm, d))
                    if len(discovered) >= 5: break
    return discovered


def extract_public_brand(page: Page, legal_name_val: str | None) -> str | None:
    """
    Extracts verified public brand from page, withholding generic storefront taglines,
    legal/store suffixes, and exact duplicates of the registered legal name.
    """
    candidate_brand = page.meta.get("og:site_name") or page.meta.get("og:sitename")
    if candidate_brand:
        candidate_brand = html.unescape(candidate_brand).strip()
    else:
        parts = [html.unescape(p).strip() for p in re.split(r"\s+[|–-]\s+", page.title) if p.strip()]
        if parts:
            generic_store_words = {"nettbutikk", "fiskeutstyr", "båtutstyr", "butikk", "webshop", "forside", "hjem", "velkommen", "home", "shop", "online"}
            p0_lower = parts[0].lower()
            if any(w in p0_lower for w in generic_store_words) and len(parts) > 1:
                candidate_brand = parts[-1]
            else:
                candidate_brand = parts[0]

    if not candidate_brand:
        return None

    cleaned_brand = re.sub(r"\s*[-–|:]?\s*(?:org(?:anisasjons)?\.?\s*nr\.?|organisasjonsnummer)\s*[:.]?\s*\d{9}\b.*$", "", candidate_brand, flags=re.I).strip(" .,-")
    cleaned_brand = re.sub(r"\s*[-–|:]\s*(?:nettbutikk|butikk|webshop|forside|hjem|velkommen|home|shop|store)\b.*$", "", cleaned_brand, flags=re.I).strip(" .,-")
    norm_b = legal_name(cleaned_brand)
    generic_brands = {
        "home", "hjem", "welcome", "velkommen", "kontakt", "contact",
        "kontakt oss", "contact us", "privacy policy", "personvern",
        "vilkar", "vilkar og betingelser", "terms", "terms of service",
        "forside", "hjemmeside"
    }
    is_generic_tagline = (
        re.search(r"\b(?:din|ditt)\s+\w+", cleaned_brand, re.I) is not None
        or re.search(r"\b(?:kontakt|contact)\b", cleaned_brand, re.I) is not None
        or re.search(r"\b(?:vilk[aå]r|betingelser|privacy|personvern)\b", cleaned_brand, re.I) is not None
        or (re.search(r"\bi\s+[A-ZÆØÅa-zæøå]{3,}\b", cleaned_brand) is not None and len(cleaned_brand.split()) > 3)
    )
    if (cleaned_brand and len(cleaned_brand) <= 100 and "\ufffd" not in cleaned_brand
            and norm_b not in generic_brands
            and not is_generic_tagline
            and norm_b != legal_name(legal_name_val)):
        return cleaned_brand
    return None


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


# Pages where Norwegian companies state their organisation number. They are tried
# after the links found on the home page; proof rules apply to them unchanged.
FALLBACK_PROOF_PATHS = ('/kontakt', '/kontakt-oss', '/om-oss', '/om', '/personvern', '/personvernerklaering')
FOLLOWUP_PAGES = len(FALLBACK_PROOF_PATHS)


def proof_page_targets(page, base_url, limit=FOLLOWUP_PAGES):
    base = urlsplit(base_url)
    fixed = [urlunsplit((base.scheme, base.netloc, path, '', '')) for path in FALLBACK_PROOF_PATHS]
    targets = []
    for target in followup_links(page) + fixed:
        target = normalize_url(target)
        if target and target not in targets:
            targets.append(target)
    def priority(target):
        path=urlsplit(target).path
        return next((i for i,p in enumerate((r'kontakt|contact',r'om[-_/]?oss|about|^/om/?$',r'personvern|privacy|vilk|terms|impressum')) if re.search(p,path,re.I)),3)
    return sorted(targets,key=priority)[:limit]


async def fetch(org, envelope, bulk, http):
    context, registry_source, registry_locator = await offload(registry_context,envelope,bulk,http.blobs)
    units={c.value['organisation_number']:{} for c in envelope.claims
           if c.field.startswith('subunits.unit.') and c.availability=='available' and isinstance(c.value,dict)}
    for c in envelope.claims:
        if c.availability!='available' or not c.field.startswith('subunits.detail.'):continue
        _,_,unit,field=c.field.split('.',3)
        if unit in units and field in {'registered_website','registered_email'}:
            units[unit]['website' if field=='registered_website' else 'email']=c.value
    context['subunits']=[{'orgnr':unit,**data} for unit,data in units.items()]
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
    async def nominations():
        for candidate in candidates:yield candidate
        search=getattr(http,'search',None)
        if not successes and search:
            existing={c.domain for c in candidates}
            for candidate in await search.nominate(org,context,http):
                if candidate.domain not in existing:yield candidate
    async for candidate in nominations():
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
            page = await offload(Page,response.body,response.url)
            checked.add(candidate.domain)
            proof = await offload(candidate_proof,page,org,context,candidate,leaders)
            pages.append((response, page))
            best = (proof, response, page)
            if proof.level == "BLOCKED":
                raise SourceFailure("block_page")
            if proof.level in {"VERIFIED", "HIGH"} and len(pages) == 1 and http.counts.get(org, 0) + 1 <= http.config.website_request_cap:
                links = followup_links(page)
                for target in links[:1]:
                    target = normalize_url(target)
                    if target and domain(target) == domain(response.url):
                        try:
                            extra = await http.get(target, org, candidate.domain, proved)
                            if extra.status == 200:
                                extra_page = await offload(Page, extra.body, extra.url)
                                extra_proof = await offload(candidate_proof, extra_page, org, context, candidate, leaders)
                                if extra_proof.level != 'BLOCKED' and not (extra_proof.level == 'REJECT' and extra_proof.reason == 'foreign_orgnr'):
                                    pages.append((extra, extra_page))
                        except SourceFailure:
                            pass
            elif proof.level not in {"VERIFIED", "REJECT"} or (proof.reason == 'foreign_orgnr' and candidate.origin in {'registry_website', 'subunit_registry_website'}):
                seen = {response.url}
                for target in proof_page_targets(page, response.url):
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
                    extra_page = await offload(Page,extra.body,extra.url)
                    extra_proof = await offload(candidate_proof,extra_page,org,context,candidate,leaders)
                    if extra_proof.level == 'BLOCKED':
                        attempts.append({'domain':candidate.domain,'origin':candidate.origin,'reason':'block_page','page':target})
                        continue
                    pages.append((extra, extra_page))
                    if extra_proof.level == "REJECT" and extra_proof.reason == "foreign_orgnr":
                        best = (extra_proof, extra, extra_page)
                        continue
                    ranks = {"REJECT": -1, "BLOCKED": -1, "LOW": 0, "MEDIUM": 1,'REGISTRY_DECLARED':2, "HIGH": 3, "VERIFIED": 4}
                    if ranks[extra_proof.level] > ranks[best[0].level] and (extra_proof.level == 'VERIFIED' or best[0].reason != 'foreign_orgnr'):
                        best = (extra_proof, extra, extra_page)
                    if extra_proof.level == "VERIFIED":
                        # A foreign footer is not evidence for this entity's
                        # contacts or profiles. Retain only its exact proof page.
                        if any(candidate_proof(p, org, context, candidate, leaders).reason == 'foreign_orgnr' for _, p in pages):
                            pages = [(extra, extra_page)]
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
            if not successes and http.counts.get(org, 0) + 2 <= http.discovery_cap(org):
                legal_nm = context.get('name')
                brand_nm = context.get('brand')
                metrics = getattr(http, 'discovery_metrics', None)
                if metrics is None:
                    http.discovery_metrics = {'sitemaps_found': 0, 'sitemap_candidates': 0, 'rss_feeds_found': 0, 'rss_candidates': 0}
                    metrics = http.discovery_metrics
                try:
                    sm_resp = await http.get(f'https://{candidate.domain}/sitemap.xml', org, candidate.domain, xml=True)
                    if sm_resp.status == 200:
                        metrics['sitemaps_found'] += 1
                        for u, d in extract_sitemap_domains(sm_resp.body, legal_nm, brand_nm):
                            if d not in checked and d not in {c.domain for c in candidates}:
                                metrics['sitemap_candidates'] += 1
                                candidates.append(Candidate(u, d, 'sitemap'))
                except SourceFailure: pass
                for feed_path in ('/feed.xml', '/rss.xml', '/feed/', '/blog/feed.xml'):
                    if successes or http.counts.get(org, 0) >= http.discovery_cap(org): break
                    try:
                        rss_resp = await http.get(f'https://{candidate.domain}{feed_path}', org, candidate.domain, xml=True)
                        if rss_resp.status == 200:
                            metrics['rss_feeds_found'] += 1
                            for u, d in extract_rss_domains(rss_resp.body, legal_nm, brand_nm):
                                if d not in checked and d not in {c.domain for c in candidates}:
                                    metrics['rss_candidates'] += 1
                                    candidates.append(Candidate(u, d, 'rss'))
                            break
                    except SourceFailure: pass
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
    return await offload(publish_result,org,envelope,http,section,choices,attempts,context)


def extract_contacts_and_social(section, org, web_claim, pages, context=None, envelope=None):
    """
    Extracts contacts and verified social profiles from website pages.
    Enforces corporate entity card attribution and filters sibling/group accounts on multi-entity group sites.
    """
    context = context or {}
    web_val = web_claim.value if hasattr(web_claim, "value") and isinstance(web_claim.value, dict) else (web_claim if isinstance(web_claim, dict) else {})
    other_orgnrs = web_val.get("other_orgnrs") or []
    is_group = bool(other_orgnrs) or web_val.get("relationship_note") == "group_site"

    subunits = set()
    if envelope and hasattr(envelope, "claims"):
        for c in envelope.claims:
            if c.field.startswith("subunits.unit.") and isinstance(c.value, dict) and c.value.get("orgnr"):
                subunits.add(c.value.get("orgnr"))
    if context.get("subunits"):
        subunits.update(unit['orgnr'] for unit in context["subunits"] if unit.get('orgnr'))

    proof_url = web_val.get("final_url") or web_val.get("proof_page_url") or ""
    target_domain = domain(proof_url) if proof_url else (domain(pages[0][0].url) if pages else "")

    social_seen, contact_seen = set(), set()
    for source_response, source_page in pages:
        if domain(source_response.url) != target_domain:
            continue
        cards = extract_entity_cards(source_page.raw) if is_group else []
        for url, source_span in discover(source_page).items():
            if url not in social_seen:
                if is_group:
                    p_path = urlsplit(url).path.rstrip("/").lower()
                    legal_nm = (context.get("name") or "").lower()
                    if any(term in p_path for term in ("group", "holding", "gruppe")) and not any(term in legal_nm for term in ("group", "holding", "gruppe")):
                        continue
                    pos = source_page.raw.find(url)
                    if pos >= 0:
                        c = find_containing_card(cards, pos)
                        if c and c.is_sibling(org, other_orgnrs, subunits):
                            continue
                publish(section, source_response, org, "social_profile." + digest(url)[:20], {"url": url, "platform": domain(url)}, "company-link:" + url, source_span)
                section.claims[-1].reasons['relationship'] = 'Company-owned profile linked from verified website'
                social_seen.add(url)
        contacts = []
        for link in source_page.links:
            if link.href.startswith("tel:") and (number := phone(link.href[4:])):
                contacts.append(("phone", number, link.span))
            if link.href.startswith("mailto:"):
                address = link.href[7:].split("?", 1)[0].strip()
                if address.rsplit("@", 1)[-1].lower() == target_domain:
                    contacts.append(("email", address, link.span))
        for match in re.finditer(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", source_page.visible):
            address = match.group()
            if address.rsplit("@", 1)[-1].lower() == target_domain:
                contacts.append(("email", address, source_page.span_for(address)[:150]))
        for match in re.finditer(r"(?:telefon|tlf|phone)\s*:?\s*((?:\+47|0047)?[ .()0-9-]{8,20})", source_page.visible, re.I):
            if number := phone(match.group(1)):
                contacts.append(("phone", number, source_page.span_for(match.group(1))[:150]))
        for kind, contact, source_span in contacts:
            if (kind, contact.casefold()) not in contact_seen:
                if is_group:
                    pos = source_page.raw.find(contact)
                    if pos >= 0:
                        c = find_containing_card(cards, pos)
                        if c:
                            if c.is_sibling(org, other_orgnrs, subunits) or not c.matches_org(org, context, subunits):
                                continue
                        else:
                            continue
                    else:
                        continue
                publish(section, source_response, org, "contact." + kind + "." + digest(contact.casefold())[:20], contact, "contact:" + contact, source_span)
                contact_seen.add((kind, contact.casefold()))


def candidate_proof(page,org,context,candidate,leaders):
    proof=score(page,org,context,candidate.origin,leaders)
    if candidate.subunit_orgnr and proof.level not in {'VERIFIED','BLOCKED'}:
        unit=score(page,candidate.subunit_orgnr,context,candidate.origin,leaders)
        if unit.level=='VERIFIED':return unit
    return proof


def publish_result(org,envelope,http,section,choices,attempts,context):
    candidate, proof, response, page, pages = choices[0]
    p = urlsplit(response.url)
    root_url = urlunsplit((p.scheme, p.netloc, "", "", ""))
    matched=proof.token if proof.level=='VERIFIED' else org
    span = page.proof_span(matched) if proof.level == "VERIFIED" else page.name_span(proof.token)
    if not span:
        return missing("website", "no_localized_proof", state="ambiguous")
    value = {"final_url": root_url, "identity_level": proof.level, "proof_type": proof.proof_type,
             "proof_page_url": response.url, "signals": proof.signals, "points": proof.points,
             "candidate_origin": candidate.origin, "relationship_note": "group_site" if proof.other_orgnrs else None,
             "other_orgnrs": proof.other_orgnrs}
    if candidate.subunit_orgnr and matched==candidate.subunit_orgnr:
        value['matched_via_subunit']=matched
    publish(section, response, org, "official_website", value, "identity-proof:" + matched, span)
    if candidate.origin in {'registry_email', 'subunit_registry_email'}:
        section.claims[-1].reasons['discovery_method'] = 'registry email domain'
    if value.get('matched_via_subunit'):
        section.claims[-1].reasons['relationship'] = 'Website of registered subunit ' + matched
        refs={ref for c in envelope.claims if c.field=='subunits.unit.'+matched for ref in c.evidence_ids}
        section.evidence.extend(e for e in envelope.evidence if e.id in refs)
        section.claims[-1].evidence_ids.extend(sorted(refs))
    # HIGH combines page signals with authoritative registry/roles facts.
    if proof.level in {"HIGH",'REGISTRY_DECLARED'}:
        registry_refs = [e for e in envelope.evidence if e.source_class == "official_registry"]
        section.evidence.extend(registry_refs)
        section.claims[-1].evidence_ids.extend(e.id for e in registry_refs)
    from .descriptions import extract as descriptions
    accepted_domain_pages = [(r, p) for r, p in pages if domain(r.url) == domain(response.url)]
    identity_claim = section.claims[-1]
    descriptions(section, org, identity_claim, accepted_domain_pages)
    extract_contacts_and_social(section, org, identity_claim, accepted_domain_pages, context=context, envelope=envelope)
    brand = extract_public_brand(page, context.get("name"))
    if brand:
        span = (page.span_for(brand) or "")[:150]
        publish(section, response, org, "public_brand", brand, "meta:brand", span)
    section.state = "available"
    http.accepted_pages[org] = [(r, p) for r, p in pages if domain(r.url) == domain(response.url)]
    envelope.run.refresh['website'] = {'checked_urls': sorted({r.url for r, _ in http.accepted_pages[org]})}
    section.errors.append(Error(section='website',code='website_candidates',message=json.dumps(attempts+http.attempts.get(org,[]),ensure_ascii=False)))
    return section
