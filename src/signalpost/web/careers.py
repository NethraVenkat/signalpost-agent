"""Vacancies reached through a current exact-number site's own navigation.

No search or employer-name matching. JSON-LD JobPosting is deliberately the
only supported posting layout; unsupported layouts remain explicit abstentions.
"""
import re
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
from ..budget import SourceFailure
from ..models.evidence import digest
from ..sources.extract import Section, add, response_source
from .html import Page
from .policy import domain, normalize_url
from .social import shared_group_context

ATS = frozenset({'webcruiter.com','teamtailor.com','jobylon.com','reachmee.com',
                 'easycruit.com','recman.no','varbi.com'})
CAREER = re.compile(r'\b(?:jobb|karriere|ledige stillinger|careers?|jobs|vacancies)\b', re.I)


def target(url, root):
    # Query-dependent postings cannot be fetched faithfully by the shared
    # query-stripping website transport. Withhold rather than change the URL.
    if urlsplit(url).query: return None
    clean=normalize_url(url)
    return clean if clean and (domain(clean)==root or domain(clean) in ATS) else None


def links(page, root, navigation=True):
    if shared_group_context(page): return []
    return [(link, url) for link in page.links
            if (link.owned_context if navigation else True)
            and (CAREER.search(link.text+' '+urlsplit(link.href).path) or domain(link.href) in ATS)
            and (url:=target(link.href,root))]


def objects(value):
    if isinstance(value,list):
        for item in value: yield from objects(item)
    elif isinstance(value,dict):
        if value.get('@type')=='JobPosting': yield value
        for key,item in value.items():
            if key!='hiringOrganization': yield from objects(item)


def stamp(value):
    try:
        parsed=datetime.fromisoformat(str(value).replace('Z','+00:00'))
        return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).astimezone(timezone.utc)
    except (ValueError,TypeError,OverflowError): return None


def postings(page,org,now):
    if shared_group_context(page): return []
    out=[]
    for body in page.jsonld:
        for item in objects(body):
            title=item.get('title'); posted=item.get('datePosted'); deadline=item.get('validThrough')
            start,end=stamp(posted),stamp(deadline)
            # An explicit expired deadline overrides a recent publication.
            if end and (end.date()<now.date() if re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(deadline)) else end<=now): continue
            if deadline and end is None: continue
            # An open invitation elsewhere in a site's footer is not the
            # vacancy's status: require title and status in the same paragraph.
            opened=None
            if isinstance(title,str):
                for text,span in page.paragraphs:
                    if title in text:
                        opened=re.search(r'\b(?:applications open|stillingen er åpen|søknader mottas fortløpende)\b',text,re.I)
                        if opened:break
            current=(end and end.date()>=now.date()) or (start and now-timedelta(days=60)<=start) or opened
            if not current: continue
            if not isinstance(title,str) or not title.strip() or len(title)>200: continue
            owner=item.get('hiringOrganization') or {}
            identifier=owner.get('identifier') if isinstance(owner,dict) else None
            if isinstance(identifier,dict): identifier=identifier.get('value')
            if identifier is not None and re.sub(r'\D','',str(identifier))!=org: continue
            # A listing's JobPosting for another URL is not a posting page.
            if item.get('url') and normalize_url(item['url'])!=normalize_url(page.url): continue
            tokens=[title]+([posted] if start else [])+([deadline] if end else [])+([opened.group()] if opened else [])
            spans=[page.span_for(str(token)) for token in tokens]
            if not all(span and str(token) in span for span,token in zip(spans,tokens)): continue
            out.append(({'title':title,'url':page.url,'employer_orgnr':org,
                         'published':posted if start else None,'expires':deadline if end else None,
                         'date_basis':'JobPosting.datePosted/validThrough','source':'verified_site_careers'},spans))
    return out


async def fetch(org,envelope,http,pages):
    proof=next((c for c in envelope.claims if c.field=='official_website' and c.availability=='available'
                and not c.carried_forward and c.value.get('identity_level')=='VERIFIED'
                and c.value.get('relationship_note')!='group_site' and not c.value.get('other_orgnrs')),None)
    state={'state':'not_applicable','reason':'no_current_exact_verified_website','checked_urls':[]}
    envelope.run.refresh['careers']=state
    section=Section(state='not_available')
    if not proof:return section
    root=domain(proof.value['final_url']); queue=[]; seen=set()
    for response,page in pages:
        if domain(response.url)!=root:continue
        for link,url in links(page,root):queue.append((url,[(response,link)]))
    state.update(state='not_available',reason='no_supported_current_posting')
    try:
        # Four pages at most, all within the existing cumulative counters.
        while queue and len(seen)<4:
            url,chain=queue.pop(0)
            if url in seen:continue
            seen.add(url)
            response=await http.get(url,org,root,proven={domain(url)})
            state['checked_urls'].append(response.url)
            if response.status!=200:raise SourceFailure('careers_http_'+str(response.status))
            if response.url!=url:
                state['reason']='redirect_chain_not_proven';continue
            page=Page(response.body,response.url)
            if shared_group_context(page):continue
            for value,spans in postings(page,org,datetime.now(timezone.utc)):
                value.update(uuid='career-'+digest(response.url)[:20],identity_claim_id=proof.id)
                start=len(section.evidence)
                add(section,response_source(response),org,'hiring','hiring.job.'+value['uuid'],value,
                    'JobPosting/title',span=spans[0],source_class='company_owned',method='signalpost.careers.v1')
                claim=section.claims[-1]
                for number,span in enumerate(spans[1:]):
                    receipt=Section()
                    add(receipt,response_source(response),org,'hiring','receipt',None,'JobPosting/date/'+str(number),
                        span=span,source_class='company_owned',method='signalpost.careers.v1')
                    section.evidence.extend(receipt.evidence)
                for depth,(parent,link) in enumerate(chain):
                    receipt=Section()
                    add(receipt,response_source(parent),org,'hiring','receipt',None,'careers/link/'+str(depth),
                        span=link.span,source_class='company_owned',method='signalpost.careers.v1')
                    section.evidence.extend(receipt.evidence)
                claim.evidence_ids=[e.id for e in section.evidence[start:]]+proof.evidence_ids
                section.state=state['state']='available'
            # One linked careers index may lead to individual posting pages.
            if len(chain)==1:
                for link in page.links:
                    next_url=target(link.href,root)
                    if next_url and domain(next_url)==domain(response.url) and (
                        CAREER.search(link.href+' '+link.text) or re.search(r'/(?:positions?|vacancies|stillinger)/',link.href,re.I)):
                        queue.append((next_url,chain+[(response,link)]))
        if queue:state.update(reason='careers_page_limit',remaining_candidates=len(queue))
    except SourceFailure as exc:
        state.update(state='failed',reason=exc.code)
    return section


def merge(envelope,section):
    """Preserve NAV coverage/errors; a careers absence never proves NAV absence."""
    current=[c for c in envelope.claims if c.family=='hiring' and c.availability=='available']
    ids={c.id for c in current}
    section.claims=current+[c for c in section.claims if c.id not in ids]
    section.errors=[e for e in envelope.errors if e.section=='hiring']
    section.state=envelope.run.sections.get('hiring','not_available')
    if section.claims and section.state not in {'failed','blocked'}:section.state='available'
    return section
