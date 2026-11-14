"""Evidence-linked public names, never legal identity or standalone site proof."""
import hashlib
import json
import re

from .models.evidence import digest
from .sources.extract import Section,Source,add,response_source
from .web.publisher import extract_publisher
from .web.publisher_identity import normalize_name
from .web.publisher_veto import conflict
from .web.policy import domain

METHOD='signalpost.public_names.v1'
GENERIC={'home','hjem','forside','velkommen','welcome','frontpage','min nettside','website','wix','wordpress','squarespace',
         'contact','kontakt','kontakt oss','personvern','privacy','about','about us','om oss','tjenester','services','nettbutikk','shop',
         'just another wordpress site','site title','my website','my site','untitled'}


def different(name,legal):
    return isinstance(name,str) and bool(name.strip()) and normalize_name(name)!=normalize_name(legal)


def site_name(page,legal):
    publisher=extract_publisher(page)
    def usable(value):
        return value if (different(value,legal) and normalize_name(value) not in GENERIC and len(value)<=120
            and len(re.findall(r'[^\W\d_]',value))>=2 and not value.lower().startswith(('http://','https://'))) else None
    og=next((f.text for f in publisher.fragments if f.location=='og:site_name'),None)
    if og:return usable(og)
    title=next((f.text for f in publisher.fragments if f.location=='title'),None)
    if not title:return None
    parts=[p.strip() for p in re.split(r'\s*(?:\||\s[-–—]\s)\s*',title) if p.strip()]
    # If a title part is already the legal name, the other part is commonly
    # a page/service headline, not an additional trading name.
    if any(normalize_name(p)==normalize_name(legal) for p in parts):return None
    branding=' '.join(f.text for f in publisher.fragments if f.location in {'header','logo','footer','copyright'})
    for part in reversed(parts):
        if usable(part) and re.search(r'(?<!\w)'+re.escape(normalize_name(part))+r'(?!\w)',normalize_name(branding)):
            return part
    return None


def pointer(document,path):
    for token in path.strip('/').split('/'):
        if not token:continue
        token=token.replace('~1','/').replace('~0','~')
        document=document[int(token)] if isinstance(document,list) else document[token]
    return document


def enrich(envelopes,blobs,accepted_pages):
    for org,envelope in envelopes.items():
        legal_claim=next((c for c in envelope.claims if c.field=='identity.legal_name' and c.availability=='available' and not c.carried_forward),None)
        legal=legal_claim.value if legal_claim else None
        if not legal:continue
        records={e.id:e for e in envelope.evidence};sources={};new=Section();seen=set()
        units=sorted((c for c in envelope.claims if c.field.startswith('subunits.unit.') and c.availability=='available' and not c.carried_forward),key=lambda c:c.field)
        for unit in units:
            name=unit.value.get('name');number=unit.value.get('organisation_number')
            if not different(name,legal) or normalize_name(name) in seen:continue
            for eid in unit.evidence_ids:
                e=records[eid]
                if not e.source_url.startswith('https://data.brreg.no/enhetsregisteret/api/underenheter?'):continue
                if e.content_sha256 not in sources:
                    body=blobs.read(e.content_sha256)
                    if body is None or hashlib.sha256(body).hexdigest()!=e.content_sha256:continue
                    sources[e.content_sha256]=(Source(e.source_url,body,e.content_sha256,e.retrieved_at),json.loads(body))
                source,document=sources[e.content_sha256]
                try:raw=pointer(document,e.locator)
                except (KeyError,IndexError,ValueError,TypeError):continue
                if raw.get('overordnetEnhet')!=org or raw.get('organisasjonsnummer')!=number or raw.get('navn')!=name:continue
                value={'name':name,'origin':'registered_subunit','subunit_orgnr':number}
                add(new,source,org,'subunits','brand.registered_subunit.'+digest(normalize_name(name))[:20],value,e.locator+'/navn',method=METHOD)
                new.evidence.append(e);new.claims[-1].evidence_ids.append(e.id);seen.add(normalize_name(name));break
        # Replace the earlier heuristic's optional brand with a strict publisher
        # name. Withdrawals remain visible in output comparisons/identity ledger.
        envelope.claims=[c for c in envelope.claims if c.field!='public_brand' and not c.field.startswith('brand.registered_subunit.')]
        site=next((c for c in envelope.claims if c.field=='official_website' and c.availability=='available' and not c.carried_forward),None)
        if site and site.value.get('identity_level') in {'VERIFIED','HIGH'} and not site.value.get('other_orgnrs') and site.value.get('relationship_note')!='group_site':
            context={'name':legal,'subunits':[{'orgnr':u.value['organisation_number']} for u in units]}
            for response,page in accepted_pages.get(org,[]):
                if response.url!=site.value['proof_page_url'] or domain(response.url)!=domain(site.value['final_url']):continue
                if conflict(page,org,context)[0]:continue
                name=site_name(page,legal)
                if not name:continue
                span=page.name_span(name)
                if not span or span not in page.raw:continue
                add(new,response_source(response),org,'website','public_brand',name,'publisher-public-name',span=span,source_class='company_owned',method=METHOD)
                refs=set(site.evidence_ids);new.evidence.extend(records[eid] for eid in refs);new.claims[-1].evidence_ids.extend(sorted(refs))
                new.claims[-1].reasons['public_name']='Site-declared name, not a trademark or legal-name inference'
                break
        envelope.claims.extend(new.claims)
        new.evidence.extend(records[eid] for eid in legal_claim.evidence_ids)
        for claim in new.claims:claim.evidence_ids.extend(legal_claim.evidence_ids)
        envelope.evidence=list({e.id:e for e in [*envelope.evidence,*new.evidence]}.values())


def verify(org,data,evidence,stored_body):
    legal=next((c['value'] for c in data['claims'] if c['field']=='identity.legal_name' and c['availability']=='available'),None)
    legal_refs={eid for c in data['claims'] if c['field']=='identity.legal_name' and c['availability']=='available' for eid in c['evidence_ids']}
    checked=[]
    for claim in data['claims']:
        if claim['availability']!='available' or not(claim['field']=='public_brand' or claim['field'].startswith('brand.')):continue
        receipts=[evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']==METHOD]
        if not receipts:continue  # legacy saved outputs retain their own policy
        assert legal and not claim.get('carried_forward')
        assert legal_refs<=set(claim['evidence_ids'])
        supported=False
        for e in receipts:
            text=stored_body(e['content_sha256'])
            if claim['field'].startswith('brand.registered_subunit.'):
                assert e['source_url'].startswith('https://data.brreg.no/enhetsregisteret/api/underenheter?')
                unit=pointer(json.loads(text),e['locator'].rsplit('/',1)[0])
                expected={'name':unit['navn'],'origin':'registered_subunit','subunit_orgnr':unit['organisasjonsnummer']}
                supported|=unit.get('overordnetEnhet')==org and expected==claim['value'] and different(unit['navn'],legal)
            else:
                site=next(c for c in data['claims'] if c['field']=='official_website' and c['availability']=='available' and not c.get('carried_forward'))
                assert site['value']['identity_level'] in {'VERIFIED','HIGH'} and not site['value'].get('other_orgnrs')
                assert set(site['evidence_ids'])<=set(claim['evidence_ids'])
                page=Page(text.encode('utf8'),e['source_url'])
                units=[{'orgnr':c['value']['organisation_number']} for c in data['claims'] if c['field'].startswith('subunits.unit.') and c['availability']=='available']
                assert not conflict(page,org,{'name':legal,'subunits':units})[0]
                supported|=(e['source_url']==site['value']['proof_page_url'] and domain(e['source_url'])==domain(site['value']['final_url']) and site_name(page,legal)==claim['value'])
        assert supported,'Unsupported public-name claim'
        checked.append(claim['id'])
    return checked


from .web.html import Page
