"""Reconstruct new publisher tiers from hashed page + exact registry receipts."""
import csv
import io
import json
from urllib.parse import urlsplit, urlunsplit

from signalpost.web.html import Page
from signalpost.web.publisher_identity import DECLARED, RARE, REDIRECT, declared_receipt, rare_receipt,redirect_receipt
from signalpost.web.publisher_veto import conflict
# Historical receipts remain replayable after nomination tooling removal.
SEED_ORIGINS = {'seed_commoncrawl', 'seed_openstreetmap'}

def publisher_has_number(page, organisation_number):
    from signalpost.web.proof import orgnrs
    from signalpost.web.publisher import extract_publisher

    fragments = extract_publisher(page).fragments
    return any(organisation_number in orgnrs(fragment.text) for fragment in fragments)



def registry_context(org,data,evidence,stored_body,allow_carried=False):
    fields={'name':('legal_name','navn'),'website':('registered_website','hjemmeside'),
            'phone':('registered_phone','telefon'),'mobile':('registered_mobile','mobil'),
            'email':('registered_email','epostadresse')}
    context={}
    refs=set()
    for key,(field,column) in fields.items():
        claim=next((c for c in data['claims'] if c['field']=='identity.'+field and c['availability']=='available' and (allow_carried or not c.get('carried_forward'))),None)
        if not claim:continue
        valid=False
        for ref in claim['evidence_ids']:
            e=evidence[ref]
            if e['source_class']!='official_registry':continue
            body=stored_body(e['content_sha256'])
            if e['locator'].startswith('row:'+org+'/column:'):
                from signalpost.sources.bulk_registry import column as read_column
                records=list(csv.DictReader(io.StringIO(body)))
                match=any(read_column(r,'organisasjonsnummer')[0]==org and read_column(r,column)[0]==claim['value'] for r in records)
            elif e['locator']=='/'+column:
                doc=json.loads(body)
                match=str(doc.get('organisasjonsnummer'))==org and doc.get(column)==claim['value']
            else:match=False
            if match:valid=True;refs.add(ref)
        assert valid,'Publisher identity registry input not supported by exact source field: '+key
        context[key]=claim['value']
    address=next((c for c in data['claims'] if c['field']=='identity.registered_address' and c['availability']=='available' and (allow_carried or not c.get('carried_forward'))),None)
    if address:
        valid=False
        for ref in address['evidence_ids']:
            e=evidence[ref]
            if e['source_class']!='official_registry':continue
            body=stored_body(e['content_sha256'])
            if e['locator']=='row:'+org+'/columns:forretningsadresse.*':
                from signalpost.sources.bulk_registry import column as read_column
                match=any(read_column(r,'organisasjonsnummer')[0]==org and all(read_column(r,'forretningsadresse.'+k)[0]==v for k,v in address['value'].items()) for r in csv.DictReader(io.StringIO(body)))
            elif e['locator']=='/forretningsadresse':
                doc=json.loads(body);match=str(doc.get('organisasjonsnummer'))==org and doc.get('forretningsadresse')==address['value']
            else:match=False
            if match:valid=True;refs.add(ref)
        assert valid,'Unsupported registry publisher address'
        context.update(street=address['value'].get('adresse'),postcode=address['value'].get('postnummer'),city=address['value'].get('poststed'))
    context['subunits']=[{'orgnr':c['value']['organisation_number']} for c in data['claims'] if c['field'].startswith('subunits.unit.') and c['availability']=='available']
    return context,refs


def verify(org,data,evidence,stored_body):
    from signalpost.web.reach_identity import RULES
    total=0
    for claim in data['claims']:
        if claim['field']!='official_website' or claim['availability']!='available':continue
        value=claim['value']
        tier=value.get('proof_type')
        if value.get('candidate_origin') in SEED_ORIGINS:
            from signalpost.web.proof import score

            context, _ = registry_context(org, data, evidence, stored_body,
                                          allow_carried=bool(claim.get('carried_forward')))
            assert value['identity_level'] == 'VERIFIED' and not value.get('matched_via_subunit')
            verified = False
            for ref in claim['evidence_ids']:
                receipt = evidence[ref]
                if (receipt['source_class'] != 'company_owned'
                        or receipt['source_url'] != value['proof_page_url']
                        or receipt['locator'] != 'identity-proof:' + org):
                    continue
                text = stored_body(receipt['content_sha256'])
                page = Page(text.encode('utf8'), receipt['source_url'], text=text)
                parts = urlsplit(page.url)
                assert value['final_url'] == urlunsplit((parts.scheme, parts.netloc, '', '', ''))
                result = score(page, org, context, value['candidate_origin'], [])
                verified |= (publisher_has_number(page, org) and result.level == 'VERIFIED'
                             and result.token == org and result.proof_type == tier)
            assert verified, 'Seed website lacks live exact publisher evidence'
            total += 1
            continue
        if tier not in {DECLARED,RARE,REDIRECT}|RULES.keys():continue
        context,refs=registry_context(org,data,evidence,stored_body,allow_carried=bool(claim.get('carried_forward')))
        assert refs<=set(claim['evidence_ids']),'Missing registry proof dependencies'
        receipt=value['publisher_identity'];context['candidate_url']=receipt['candidate_url']
        own=[evidence[e] for e in claim['evidence_ids'] if evidence[e]['source_class']=='company_owned' and evidence[e]['source_url']==value['proof_page_url']]
        assert own,'Missing publisher response evidence'
        matched=False
        for e in own:
            text=stored_body(e['content_sha256'])
            page=Page(text.encode('utf8'),e['source_url'],text=text)
            parts=urlsplit(page.url)
            assert value['final_url']==urlunsplit((parts.scheme,parts.netloc,'','','')),'Published URL differs from proven publisher authority'
            assert not conflict(page,org,context)[0],'Publisher conflict'
            expected={DECLARED:declared_receipt,RARE:rare_receipt,REDIRECT:redirect_receipt,**RULES}[tier](page,org,context)
            from signalpost.web.proof import score
            checked=score(page,org,context,value.get('candidate_origin'),[])
            matched |= bool(expected and expected==receipt and checked.level=='HIGH')
        assert matched and value['identity_level']=='HIGH','Unsupported publisher identity receipt'
        total+=1
    return total
