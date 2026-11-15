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
from .candidates import generate, context_from_bulk, legal_name, Candidate, GENERIC, candidate_key
from .html import Page
from .policy import domain, normalize_url, SOCIAL, DIRECTORIES, FREE_MAIL
from .proof import score, phone, extract_entity_cards, find_containing_card, registry_contacts
from .social import discover, discover_strict, profile_url, numeric_linkedin
from .fetcher import TRANSIENT


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
               "phone": data.get("telefon"), "mobile":data.get('mobil'), "municipality": address.get("kommune"), "street": address.get("adresse"),
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
    from .legal_pages import legal_links
    return list(dict.fromkeys(legal_links(page)+[url for _,url in sorted(ranked,key=lambda x:x[0])]))


# Pages where Norwegian companies state their organisation number. They are tried
# after the links found on the home page; proof rules apply to them unchanged.
from .legal_pages import FIXED as LEGAL_PROOF_PATHS
FALLBACK_PROOF_PATHS = tuple(dict.fromkeys(('/personvern','/personvernerklaering','/kontakt','/om-oss','/kontakt-oss','/om')+LEGAL_PROOF_PATHS))
FOLLOWUP_PAGES = len(FALLBACK_PROOF_PATHS)  # nominations only; HTTP ceilings are unchanged


def proof_page_targets(page, base_url, limit=FOLLOWUP_PAGES):
    base = urlsplit(base_url)
    fixed = [urlunsplit((base.scheme, base.netloc, path, '', '')) for path in FALLBACK_PROOF_PATHS]
    targets = []
    for target in followup_links(page) + fixed:
        target = normalize_url(target)
        if target and not re.search(r'\.(?:pdf|docx?|xlsx?|zip|jpe?g|png)(?:$|/)', urlsplit(target).path, re.I) and target not in targets:
            targets.append(target)
    return targets[:limit]


async def ordered_proof_targets(org,http,page,seen,legal_only=False):
    """Real own links, then bounded sitemap nominations, then legacy guesses."""
    linked=[url for url in proof_page_targets(page,page.url,limit=100)
            if url in {normalize_url(link) for link in followup_links(page)} and domain(url)==domain(page.url)]
    from .legal_pages import legal_links,is_legal
    if legal_only:linked=[url for url in linked if url in legal_links(page)]
    yielded=set()
    async def queued_pdfs():
        for pdf_url in list(getattr(http,'legal_pdf_links',{}).get(org,{})):
            if pdf_url not in yielded and pdf_url not in seen:
                yielded.add(pdf_url);yield pdf_url
    for url in linked:
        yielded.add(url);yield url
        async for pdf_url in queued_pdfs():yield pdf_url
    async for pdf_url in queued_pdfs():yield pdf_url
    from .proof_sitemaps import discover
    # Leave capacity for at least the map and one proof page. No allowance is
    # added and all robots/redirect requests still consume the shared counters.
    if http.company_cap(org)-http.counts.get(org,0)>=2:
        for url in await discover(org,http,page.url,seen):
            yielded.add(url);yield url
            async for pdf_url in queued_pdfs():yield pdf_url
    fixed=proof_page_targets(page,page.url)
    if legal_only:
        base=urlsplit(page.url)
        fixed=[url for url in getattr(http,'proof_sitemap_targets',{}).get(org,set()) if is_legal(url)]
        fixed += [urlunsplit((base.scheme,base.netloc,path,'','')) for path in LEGAL_PROOF_PATHS]
    for url in fixed:
        if url not in yielded:
            yielded.add(url);yield url
            async for pdf_url in queued_pdfs():yield pdf_url


def previous_nomination(previous, context, units):
    if not previous:
        return None, None
    row = previous if 'claims' in previous else previous.get('profile', {})
    claims = row.get('claims', [])
    old_registry = next((c['value'] for c in claims if c['field'] == 'identity.registered_website' and c['availability'] == 'available'), None)
    if normalize_url(old_registry) != normalize_url(context.get('website')):
        return None, None  # A new registry declaration takes precedence.
    claim = next((c for c in claims if c['field'] == 'official_website' and c['availability'] == 'available'), None)
    value = claim.get('value', {}) if claim else {}
    if value.get('identity_level') != 'VERIFIED' or not value.get('candidate_origin'):
        return None, None
    branch = value.get('matched_via_subunit')
    if branch and branch not in units:
        return None, None  # Historical scope cannot authorize a branch today.
    url = normalize_url(value.get('final_url'))
    proof_url = normalize_url(value.get('proof_page_url'))
    if not url:
        return None, None
    return Candidate(url, domain(url), value['candidate_origin'], branch), proof_url


async def fetch(org, envelope, bulk, http, previous=None, *, resume=False, candidates_override=None, nav_homepages=(), legal_resume=False):
    context, registry_source, registry_locator = await offload(registry_context,envelope,bulk,http.blobs)
    units={c.value['organisation_number']:{'name': c.value.get('name')} for c in envelope.claims
           if c.field.startswith('subunits.unit.') and c.availability=='available' and isinstance(c.value,dict)}
    for c in envelope.claims:
        if c.availability!='available' or not c.field.startswith('subunits.detail.'):continue
        _,_,unit,field=c.field.split('.',3)
        if unit in units and field in {'registered_website','registered_email'}:
            units[unit]['website' if field=='registered_website' else 'email']=c.value
    context['subunits']=[{'orgnr':unit,**data} for unit,data in units.items()]
    context['former_names']=list(dict.fromkeys(record['navn'] for c in envelope.claims
        if c.field=='identity.historical_names' and c.availability=='available' and not c.carried_forward
        and isinstance(c.value,list) for record in c.value
        if isinstance(record,dict) and isinstance(record.get('navn'),str) and record['navn'].strip()))
    if previous:
        old = previous if 'claims' in previous else previous.get('profile', {})
        context['brands'] = [c['value'] for c in old.get('claims', []) if c.get('field') == 'public_brand'
                             and c.get('availability') == 'available' and isinstance(c.get('value'), str)]
    http.legal_resumable=getattr(http,'legal_resumable',{})
    http.legal_resumable.setdefault(org,{})
    http.proof_checked_urls=getattr(http,'proof_checked_urls',{})
    http.proof_checked_urls.setdefault(org,set())
    section = Section(state="not_available")
    if registry_source and (social := profile_url(normalize_url(context.get("website")) or "")):
        add(section, registry_source, org, "website", "registry_social." + digest(social)[:20],
            {"url": social, "platform": domain(social), "verification": "registry_asserted"}, registry_locator)
    context['nav_homepages'] = list(nav_homepages)
    candidates = list(candidates_override) if candidates_override is not None else generate(context)
    refresh_candidate, refresh_proof = previous_nomination(previous, context, units)
    if refresh_candidate:
        candidates = [refresh_candidate] + [c for c in candidates if c.url != refresh_candidate.url]
    leaders = [c.value.get("name") for c in envelope.claims if c.family == "roles" and isinstance(c.value, dict) and (c.value.get("role_type") or {}).get("kode") in {"DAGL", "LEDE"} and c.value.get("name")]
    saved = http.discovery_sessions.get(org) if resume else None
    proved = saved['proved'] if saved else set()
    successes = saved['successes'] if saved else []
    attempts = saved['attempts'] if saved else []
    blocked = saved['blocked'] if saved else False
    ambiguous = saved['ambiguous'] if saved else False
    budget_hit = None
    source_unavailable = saved['source_unavailable'] if saved else False
    registry_failed = saved['registry_failed'] if saved else False
    fetchable_failures = saved['fetchable_failures'] if saved else set()
    checked = saved['checked'] if saved else set()
    attempted = saved['attempted'] if saved else set()
    vetoed = saved['vetoed'] if saved else set()
    failures = saved.get('transient_failures',{}) if saved else {}
    if saved:section.errors.extend(saved['access_errors'])
    async def nominations():
        for candidate in candidates:yield candidate
        search=getattr(http,'search',None)
        if not resume and not successes and search:
            existing={c.domain for c in candidates}
            for candidate in await search.nominate(org,context,http):
                if candidate.domain not in existing:yield candidate
    async for candidate in nominations():
        key = candidate_key(candidate)
        can_resume=legal_resume and key in http.legal_resumable[org]
        if (key in attempted and not can_resume) or candidate.domain in vetoed:continue
        attempted.add(key)
        pages = []
        best = None
        try:
            response = await http.candidate(candidate, org, proved)
            if response.status in (401, 403, 429):
                raise SourceFailure("http_blocked", f"HTTP {response.status}")
            if not 200 <= response.status < 300:
                if response.status >= 500:
                    source_unavailable = True
                    failures[key]={'candidate':candidate,'reason':'website_http_5xx'}
                attempts.append({"domain": candidate.domain, "level": "LOW", "reason": f"http_{response.status}"})
                continue
            page = await offload(Page,response.body,response.url)
            checked.add(candidate.domain)
            proof = await offload(candidate_proof,page,org,context,candidate,leaders)
            if proof.level not in {'REJECT','BLOCKED','VERIFIED'}:
                http.legal_resumable[org][key]=candidate
            pages.append((response, page))
            best = (proof, response, page)
            if proof.level == "BLOCKED":
                raise SourceFailure("block_page")
            if (candidate is refresh_candidate and refresh_proof and refresh_proof != response.url
                    and domain(refresh_proof) == candidate.domain and proof.level != 'REJECT'):
                try:
                    checked_response = await http.get(refresh_proof, org, candidate.domain, proved)
                    if checked_response.status == 200:
                        checked_page = await offload(Page, checked_response.body, checked_response.url)
                        checked_proof = await offload(candidate_proof, checked_page, org, context, candidate, leaders)
                        if checked_proof.level=='BLOCKED':raise SourceFailure('block_page')
                        if checked_proof.level == 'VERIFIED':
                            pages.append((checked_response, checked_page))
                            best = (checked_proof, checked_response, checked_page)
                            proof, response, page = best
                except SourceFailure as exc:
                    if exc.code in {'block_page','http_blocked','robots','robots_unavailable'}:raise
                    if exc.code in TRANSIENT:failures[key]={'candidate':candidate,'reason':exc.code}
                    attempts.append({'domain': candidate.domain, 'origin': candidate.origin,
                                     'reason': exc.code, 'page': refresh_proof})
            if proof.level not in {"VERIFIED", "REJECT"}:
                seen = {response.url}|http.proof_checked_urls[org]
                from .legal_pages import pdf_receipts
                http.legal_pdf_links=getattr(http,'legal_pdf_links',{})
                http.legal_pdf_links.setdefault(org,{}).update(pdf_receipts(response,page))
                async for target in ordered_proof_targets(org,http,page,seen,legal_only=legal_resume):
                    if not target or target in seen or domain(target) != domain(response.url):
                        continue
                    seen.add(target)
                    try:
                        is_pdf_target=target in http.legal_pdf_links.get(org,{})
                        extra = await http.get(target, org, candidate.domain, proved,**({'pdf':True} if is_pdf_target else {}))
                    except SourceFailure as exc:
                        if exc.code in {'block_page','http_blocked','robots','robots_unavailable'}:raise
                        if exc.code in TRANSIENT:failures[key]={'candidate':candidate,'reason':exc.code}
                        attempts.append({"domain": candidate.domain, "level": "LOW", "reason": exc.code, "page": target})
                        if exc.code in {"website_budget_exhausted", "budget_exhausted", "deadline"}:
                            budget_hit = exc.code
                            break
                        continue
                    http.proof_checked_urls[org].add(target)
                    if extra.status != 200:
                        if extra.status in {401,403,429}:raise SourceFailure('http_blocked')
                        if extra.status>=500:failures[key]={'candidate':candidate,'reason':'website_http_5xx'}
                        continue
                    if is_pdf_target:
                        if extra.url!=target:
                            attempts.append({'domain':candidate.domain,'page':target,'reason':'pdf_redirect_unproven'});continue
                        from .legal_pdf import prove as prove_pdf
                        try:
                            remaining=max(.001,http.budget.deadline-__import__('time').monotonic())
                            result=await asyncio.wait_for(offload(prove_pdf,extra,org,context,candidate,leaders,http.legal_pdf_links[org][target]),timeout=min(5,remaining))
                        except (SourceFailure,TimeoutError) as exc:
                            if getattr(exc,'code',None)=='pdf_publisher_conflict':
                                from .proof import Proof
                                best=(Proof('REJECT',reason='pdf_publisher_conflict'),extra,Page(b'',extra.url))
                                break
                            attempts.append({'domain':candidate.domain,'page':target,'reason':getattr(exc,'code','pdf_parse_timeout')});continue
                        if not result:continue
                        extra,extra_page,extra_proof=result
                        await offload(http.blobs.put,extra.body)
                    else:
                        extra_page = await offload(Page,extra.body,extra.url)
                        http.legal_pdf_links[org].update(pdf_receipts(extra,extra_page))
                        extra_proof = await offload(candidate_proof,extra_page,org,context,candidate,leaders)
                    from .legal_pages import is_legal
                    if is_legal(urlsplit(extra.url).path) and extra_proof.level in {'HIGH','REGISTRY_DECLARED'}:
                        from .proof import Proof
                        extra_proof=Proof('LOW',reason='legal_page_exact_number_missing')
                    if extra_proof.level == 'BLOCKED':
                        attempts.append({'domain':candidate.domain,'origin':candidate.origin,'reason':'block_page','page':target})
                        raise SourceFailure('block_page')
                    pages.append((extra, extra_page))
                    if extra_proof.level == "REJECT":
                        best = (extra_proof, extra, extra_page)
                        break
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
            if proof.level in {'REJECT','BLOCKED'}:
                vetoed.add(candidate.domain);failures.pop(key,None)
                http.legal_resumable[org].pop(key,None)
            attempts.append({"domain": candidate.domain, "level": proof.level, "points": proof.points, "signals": proof.signals, "origin": candidate.origin, "reason": proof.reason})
            if candidate is refresh_candidate and proof.level != 'VERIFIED':
                continue  # Previous metadata nominates; only fresh exact proof publishes.
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
            if exc.code in TRANSIENT:failures[key]={'candidate':candidate,'reason':exc.code}
            if exc.code in {'robots','robots_unavailable','http_blocked','block_page','ssrf','url_refused'}:vetoed.add(candidate.domain)
            if exc.code in {'website_timeout','website_connect_error','website_http_5xx','dns_timeout','dns_error','dns_unavailable'}:
                source_unavailable = True
                fetchable_failures.add(candidate.domain)
                if candidate.origin == 'registry_website': registry_failed=True
            attempts.append({"domain": candidate.domain,'origin':candidate.origin, "level": "BLOCKED" if exc.code in {"robots", "robots_unavailable", "http_blocked", "block_page"} else "LOW", "reason": exc.code})
            if exc.code in {"robots", "robots_unavailable", "http_blocked", "block_page"}:
                blocked = blocked or candidate.origin == 'registry_website' or exc.code=='block_page'
                section.errors.append(Error(section="website", code=exc.code, message=f"{candidate.domain}: access refused"))
            if exc.code in {"website_budget_exhausted", "budget_exhausted", "deadline"}:
                budget_hit = exc.code
                attempted.discard(key)  # Not a completed candidate check.
                break
    http.discovery_sessions[org] = dict(context=context, proved=proved, successes=successes,
        attempts=attempts, blocked=blocked, ambiguous=ambiguous, source_unavailable=source_unavailable,
        registry_failed=registry_failed, fetchable_failures=fetchable_failures, checked=checked,
        attempted=attempted, vetoed=vetoed, transient_failures=failures, access_errors=list(section.errors))
    envelope.run.refresh['proof_sitemaps']={'attempts':getattr(http,'proof_sitemap_attempts',{}).get(org,[]),
        'scope':'same-site proof-page nomination only; max two sitemap-nominated pages; no news; unchanged cumulative limits'}
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
    from .owner_social_contact import collect as owner_contact
    owner_pages,owner_state=await owner_contact(org,choices[0],http,proved,context)
    http.owner_social_pages=getattr(http,'owner_social_pages',{})
    http.owner_social_pages[org]=owner_pages
    envelope.run.refresh['owner_social']=owner_state
    return await offload(publish_result,org,envelope,http,section,choices,attempts,context)


def extract_contacts_and_social(section, org, web_claim, pages, context=None, envelope=None, owner_pages=()):
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
    original_pages={(id(r),id(p)) for r,p in pages}
    for source_response, source_page in list(pages)+list(owner_pages):
        if domain(source_response.url) != target_domain:
            continue
        cards = extract_entity_cards(source_page.raw) if is_group else []
        from .owner_social import declared_profiles
        profiles={url:{'span':span,'tier':'own_header_footer_numeric_linkedin_v1' if numeric_linkedin(url) else 'own_header_footer_exact_name_v1'}
                  for url,span in discover_strict(source_page,context.get('name')).items()}
        if context.get('name') and not is_group and web_val.get('identity_level') in {'HIGH','VERIFIED'}:
            for url,receipt in declared_profiles(source_page,context.get('name'),org,context).items():profiles.setdefault(url,receipt)
        for url,receipt in profiles.items():
            if is_group:continue
            if url not in social_seen:
                value={'url':url,'platform':domain(url),'proof_tier':receipt['tier'],'company_name':context.get('name')}
                if receipt['tier'] in {'owner_jsonld_sameas_v1','own_contact_follow_us_v1'}:value['owner_declaration']=receipt
                publish(section,source_response,org,'social_profile.'+digest(url)[:20],value,'company-link:'+url,receipt['span'])
                refs={eid for c in envelope.claims if c.field=='identity.legal_name' and c.availability=='available' for eid in c.evidence_ids} if envelope else set()
                section.evidence.extend(e for e in envelope.evidence if e.id in refs) if envelope else None
                section.claims[-1].evidence_ids.extend(sorted(refs))
                section.claims[-1].evidence_ids.extend(web_claim.evidence_ids)
                section.claims[-1].reasons['relationship'] = 'Company-owned profile linked from verified website'
                social_seen.add(url)
        if (id(source_response),id(source_page)) not in original_pages:continue
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
    context = {**context, 'publisher_company_orgnr': org, 'candidate_url': candidate.url}
    proof=score(page,org,context,candidate.origin,leaders)
    # A guessed parent candidate may actually be its proven registered branch.
    # Only an exact number in R1 publisher context authorizes this fallback;
    # each branch is rescored with every existing conflict/proof rule intact.
    if proof.level not in {'VERIFIED','BLOCKED'} and (not proof.reason.startswith('publisher_') or proof.reason=='publisher_group_without_exact_orgnr'):
        from .publisher import extract_publisher
        from .proof import orgnrs
        publisher_ids=orgnrs(extract_publisher(page).text)
        proven={str(u['orgnr']) for u in context.get('subunits',[]) if u.get('orgnr')}
        for branch in sorted(publisher_ids & proven):
            unit=score(page,branch,context,candidate.origin,leaders)
            if unit.level=='VERIFIED':
                unit.signals.append('proven_subunit_publisher_number')
                return unit
    if proof.reason.startswith('publisher_'):
        return proof
    if candidate.origin=='registry_website' and domain(page.url)!=candidate.domain:
        from .publisher_identity import declared_match,redirect_receipt
        if not declared_match(page,org,context) and not redirect_receipt(page,org,context):
            from .proof import Proof
            return Proof('REJECT',reason='registry_redirect_identity_missing')
    if candidate.subunit_orgnr and proof.level not in {'VERIFIED','BLOCKED'}:
        unit=score(page,candidate.subunit_orgnr,context,candidate.origin,leaders)
        if unit.level=='VERIFIED':return unit
    matches = registry_contacts(page, context)
    if proof.level in {'HIGH','REGISTRY_DECLARED'} and not proof.publisher_receipt and (not matches or not page.name_span(proof.token)):
        from .proof import Proof
        from .publisher_identity import declared_receipt, DECLARED
        if receipt := declared_receipt(page,org,context):
            return Proof('HIGH',DECLARED,['publisher_full_legal_name','registry_declared_domain'],
                         reason=DECLARED,token=context['name'],publisher_receipt=receipt)
        from .publisher_identity import rare_receipt, RARE
        if receipt := rare_receipt(page,org,context):
            return Proof('HIGH',RARE,['publisher_full_legal_name','rare_registry_contact'],
                         reason=RARE,token=context['name'],publisher_receipt=receipt)
        if not matches:
            from .publisher_identity import redirect_receipt,REDIRECT
            if receipt := redirect_receipt(page,org,context):
                return Proof('HIGH',REDIRECT,['registry_declared_redirect','publisher_full_legal_name'],
                             reason=REDIRECT,token=context['name'],publisher_receipt=receipt)
            return Proof('MEDIUM', signals=proof.signals, points=proof.points, reason='registry_contact_missing')
    # A shared registry phone/domain is corroboration, never a replacement for
    # exact-entity proof or an override of parked/foreign/group/source vetoes.
    return proof


def publish_result(org,envelope,http,section,choices,attempts,context):
    candidate, proof, response, page, pages = choices[0]
    p = urlsplit(response.url)
    root_url = urlunsplit((p.scheme, p.netloc, "", "", ""))
    matched=proof.token if proof.level=='VERIFIED' else org
    span = page.proof_span(matched) if proof.level == "VERIFIED" else page.name_span(proof.token)
    if getattr(proof,'publisher_receipt',None):
        from .publisher_identity import localized_span
        span = localized_span(page,proof.publisher_receipt)
    if not span:
        return missing("website", "no_localized_proof", state="ambiguous")
    value = {"final_url": root_url, "identity_level": proof.level, "proof_type": proof.proof_type,
             "proof_page_url": response.url, "signals": proof.signals, "points": proof.points,
             "candidate_origin": candidate.origin, "relationship_note": "group_site" if proof.other_orgnrs else None,
             "other_orgnrs": proof.other_orgnrs}
    if getattr(response,'pdf_receipt',None):value['pdf_proof']=response.pdf_receipt
    if getattr(proof,'publisher_receipt',None):
        value['publisher_identity'] = proof.publisher_receipt
    proven_units={str(u['orgnr']) for u in context.get('subunits',[]) if u.get('orgnr')}
    if (candidate.subunit_orgnr and matched==candidate.subunit_orgnr) or matched in proven_units:
        value['matched_via_subunit']=matched
        from .social import shared_group_context
        if shared_group_context(page):value['relationship_note']='group_site'
    contact_matches = registry_contacts(page, context) if not proof.other_orgnrs else {}
    contact_refs = {}
    for kind in contact_matches:
        field = 'identity.registered_phone' if kind == 'phone' else 'identity.registered_email'
        refs = {ref for c in envelope.claims if c.field == field and c.availability == 'available' and not c.carried_forward for ref in c.evidence_ids}
        if refs: contact_refs[kind] = refs
    if contact_refs:
        value['registry_contact_matches'] = {kind:contact_matches[kind][0] for kind in contact_refs}
    locator=('pdf:page:'+str(response.pdf_receipt['page_number'])+'/' if getattr(response,'pdf_receipt',None) else '')+'identity-proof:'+matched
    publish(section,response,org,'official_website',value,locator,span)
    web_claim = section.claims[-1]
    if getattr(response,'pdf_receipt',None):
        from .legal_pdf import attach
        attach(section,web_claim,response)
    for kind, refs in contact_refs.items():
        contact_value, contact_span = contact_matches[kind]
        if not contact_span or len(contact_span) > 300 or contact_span not in page.raw: continue
        temporary = Section()
        add(temporary, response_source(response), org, 'website', 'registry_contact.'+kind, contact_value,
            'registry-contact:'+kind, span=contact_span, source_class='company_owned', method='signalpost.registry_contact.v1')
        section.evidence.extend(temporary.evidence)
        section.evidence.extend(e for e in envelope.evidence if e.id in refs)
        web_claim.evidence_ids.extend(sorted(refs))
        web_claim.evidence_ids.extend(e.id for e in temporary.evidence)
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
    accepted_domain_pages = [(r, p) for r, p in pages if domain(r.url) == domain(response.url) and not getattr(r,'pdf_receipt',None)]
    identity_claim = section.claims[-1]
    descriptions(section, org, identity_claim, accepted_domain_pages)
    extract_contacts_and_social(section, org, identity_claim, accepted_domain_pages, context=context, envelope=envelope,owner_pages=getattr(http,'owner_social_pages',{}).get(org,()))
    brand = extract_public_brand(page, context.get("name"))
    if brand:
        span = (page.span_for(brand) or "")[:150]
        publish(section, response, org, "public_brand", brand, "meta:brand", span)
    section.state = "available"
    http.accepted_pages[org] = accepted_domain_pages
    envelope.run.refresh['website'] = {'checked_urls': sorted({r.url for r, _ in http.accepted_pages[org]}),
                                       'social_policy':'strict_header_footer_or_exact_owner_declaration_v3'}
    section.errors.append(Error(section='website',code='website_candidates',message=json.dumps(attempts+http.attempts.get(org,[]),ensure_ascii=False)))
    return section
