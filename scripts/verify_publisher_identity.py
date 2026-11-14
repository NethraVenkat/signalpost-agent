"""Reconstruct new publisher tiers from hashed page + exact registry receipts."""
import csv
import io
import json
from urllib.parse import urlsplit, urlunsplit

from signalpost.web.html import Page
from signalpost.web.publisher_identity import DECLARED, RARE, declared_receipt, rare_receipt
from signalpost.web.publisher_veto import conflict


def registry_context(org,data,evidence,stored_body):
    fields={'name':('legal_name','navn'),'website':('registered_website','hjemmeside'),
            'phone':('registered_phone','telefon'),'mobile':('registered_mobile','mobil'),
            'email':('registered_email','epostadresse')}
    context={}
    refs=set()
    for key,(field,column) in fields.items():
        claim=next((c for c in data['claims'] if c['field']=='identity.'+field and c['availability']=='available' and not c.get('carried_forward')),None)
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
    context['subunits']=[{'orgnr':c['value']['organisation_number']} for c in data['claims'] if c['field'].startswith('subunits.unit.') and c['availability']=='available']
    return context,refs


def verify(org,data,evidence,stored_body):
    total=0
    for claim in data['claims']:
        if claim['field']!='official_website' or claim['availability']!='available':continue
        value=claim['value']
        tier=value.get('proof_type')
        if tier not in {DECLARED,RARE}:continue
        context,refs=registry_context(org,data,evidence,stored_body)
        assert refs<=set(claim['evidence_ids']),'Missing registry proof dependencies'
        receipt=value['publisher_identity'];context['candidate_url']=receipt['candidate_url']
        own=[evidence[e] for e in claim['evidence_ids'] if evidence[e]['source_class']=='company_owned' and evidence[e]['source_url']==value['proof_page_url']]
        assert own,'Missing publisher response evidence'
        matched=False
        for e in own:
            page=Page(stored_body(e['content_sha256']).encode('utf8'),e['source_url'])
            parts=urlsplit(page.url)
            assert value['final_url']==urlunsplit((parts.scheme,parts.netloc,'','','')),'Published URL differs from proven publisher authority'
            assert not conflict(page,org,context)[0],'Publisher conflict'
            expected=(declared_receipt if tier==DECLARED else rare_receipt)(page,org,context)
            from signalpost.web.proof import score
            checked=score(page,org,context,value.get('candidate_origin'),[])
            matched |= bool(expected and expected==receipt and checked.level=='HIGH')
        assert matched and value['identity_level']=='HIGH','Unsupported publisher identity receipt'
        total+=1
    return total
