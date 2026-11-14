"""Explicit dated official observations; never turn retrieval/period dates into events."""
import json
import re
from datetime import datetime,timezone

from ..models.evidence import digest
from .extract import Section,add,response_source
from .http import Response
from .registry_changes import cutoff,timestamp
from .exact_public import lei_record,GLEIF

METHOD='signalpost.dated_official.v1'


def frames(document,org,url):
    if url.startswith(GLEIF+'lei-records?'):
        for index,item in enumerate(document.get('data',[])):
            record=lei_record(item,org)
            if not record:continue
            registration=item['attributes'].get('registration',{})
            for key,label in [('initialRegistrationDate','LEI initial registration'),('lastRenewalDate','LEI last renewal')]:
                value=registration.get(key)
                if not isinstance(value,str):continue
                try:timestamp(value)
                except (ValueError,TypeError,AttributeError):continue
                yield {'company_orgnr':org,'title':label,'date':value,'date_source':'GLEIF '+key+' (explicit source date)',
                    'lei':record['lei'],'url':GLEIF+'lei-records/'+record['lei']},f'/data/{index}/attributes/registration/{key}',key
    # Copy-year arrays and statement period ends have no availability timestamp.
    # They deliberately produce no dated filing fact here.


def enrich(envelopes,blobs):
    for org,env in envelopes.items():
        now=timestamp(env.run.started_at);since=cutoff(now);new=Section();seen=set()
        evidence={e.id:e for e in env.evidence}
        claims=[c for c in env.claims if c.field=='gleif.record' and c.availability=='available' and not c.carried_forward]
        for parent in claims:
            for eid in parent.evidence_ids:
                e=evidence[eid]
                if not e.source_url.startswith(GLEIF+'lei-records?') or e.content_sha256 in seen:continue
                seen.add(e.content_sha256);body=blobs.read(e.content_sha256)
                if body is None:continue
                document=json.loads(body);response=Response(body,200,e.source_url,e.retrieved_at,e.content_sha256)
                for value,locator,kind in frames(document,org,e.source_url):
                    if not since<=timestamp(value['date'])<=now:continue
                    field='official_dated.gleif.'+digest([value['lei'],kind,value['date']])[:24]
                    add(new,response_source(response),org,'activity',field,value,locator,source_class='official_gleif',method=METHOD)
                    new.claims[-1].evidence_ids.extend(parent.evidence_ids)
                    new.evidence.extend(evidence[eid] for eid in parent.evidence_ids)
        present={c.field for c in env.claims}
        env.claims.extend(c for c in new.claims if c.field not in present)
        env.evidence=list({e.id:e for e in [*env.evidence,*new.evidence]}.values())
        env.run.refresh['official_dated']={'events':len(new.claims),'lookback_months':36,
            'accounts_availability_date':'not_supplied_by_checked_accounts_sources',
            'lei_last_renewal_date':'only_explicit_lastRenewalDate; lastUpdateDate/nextRenewalDate never substituted'}
        if new.claims and env.run.sections.get('activity') in {'not_available','not_applicable'}:env.run.sections['activity']='available'


def verify(org,data,evidence,stored_body):
    for claim in data['claims']:
        if claim['availability']!='available' or not claim['field'].startswith('official_dated.'):continue
        parents=[c for c in data['claims'] if c['field']=='gleif.record' and c['availability']=='available' and c['value']['lei']==claim['value']['lei']]
        assert any(set(c['evidence_ids'])<=set(claim['evidence_ids']) for c in parents),'Missing exact LEI identity dependency'
        receipts=[evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']==METHOD]
        assert any(any(value==claim['value'] and locator==e['locator'] for value,locator,_ in frames(json.loads(stored_body(e['content_sha256'])),org,e['source_url'])) for e in receipts),'Unsupported official dated fact'


def sentence(value):
    return value['title']+': '+value['lei']+'; '+value['date']+' ('+value['date_source']+').'
