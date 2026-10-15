"""Destination-only collector replay of archived evidence; never performs network I/O.

Redirect/robots metadata is deliberately not invented from a historical request log.
The supplied destination is replayed after transport, through real collection and
dependent extraction. Unrecorded followups fail explicitly.
"""
import argparse
import asyncio
import csv
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from signalpost.budget import SourceFailure
from signalpost.models.envelope import Envelope
from signalpost.sources.extract import Source
from signalpost.web.collector import fetch


async def verify(archive, bulk, org, url, sha):
    with (archive/'envelopes.jsonl').open(encoding='utf8') as lines:
        old=next(json.loads(line) for line in lines if json.loads(line)['organisation_number']==org)
    envelope=Envelope.model_validate(old)
    envelope.claims=[c for c in envelope.claims if c.family!='website']
    with bulk.open(encoding='utf-8-sig',newline='') as lines:
        row=next(r for r in csv.DictReader(lines) if r['organisasjonsnummer']==org)
    body=(archive/'state/blobs'/sha).read_bytes()
    assert hashlib.sha256(body).hexdigest()==sha
    log=json.loads((archive/'report.json').read_text(encoding='utf8'))['request_log']
    assert any(e['url']==url and e.get('status')==200 and e.get('content_sha256')==sha for e in log)
    source_body=bulk.read_bytes()
    source=Source(str(bulk),source_body,hashlib.sha256(source_body).hexdigest(),old['run']['completed_at'])
    response=SimpleNamespace(body=body,url=url,sha=sha,retrieved_at=old['run']['completed_at'],status=200)
    class RecordedDestination:
        blobs=None
        config=SimpleNamespace(website_request_cap=6,registry_declared=False,website_stop_after_verified=True)
        counts={};attempts={};accepted_pages={}
        followups=[]
        async def candidate(self,candidate,number,proved):
            from signalpost.web.policy import domain
            assert number==org and candidate.domain==domain(url)
            self.counts[org]=1
            return response
        async def get(self,target,*args,**kwargs):
            self.followups.append(target)
            raise SourceFailure('unrecorded_followup')
    http=RecordedDestination()
    result=await fetch(org,envelope,(row,source),http)
    claims=[c.model_dump(mode='json') for c in result.claims]
    assert any(c['field']=='official_website' and c['value']['identity_level']=='VERIFIED' for c in claims)
    assert any(c['field'].startswith('website_description.') for c in claims)
    for e in result.evidence:
        assert e.content_sha256==sha and e.claim_span in body.decode('utf8') and len(e.claim_span)<=300
    return {'scope':'Actual archived registry context and destination bytes through production collector + dependent extraction; transport and new followups not verified',
            'organisation_number':org,'registry_name':row['navn'],'source_sha256':sha,'source_url':url,
            'state':result.state,'claims':claims,'evidence':[e.model_dump(mode='json') for e in result.evidence],
            'published_fields':[c['field'] for c in claims],'unrecorded_followups':http.followups,'network_requests':0}


def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--bulk',type=Path,required=True)
    p.add_argument('--org',required=True);p.add_argument('--url',required=True);p.add_argument('--sha',required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=asyncio.run(verify(a.archive,a.bulk,a.org,a.url,a.sha))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k not in {'claims','evidence'}},ensure_ascii=True))


if __name__=='__main__':main()
