"""Audit retained event order/caps/receipts and old-vs-new extraction on identical bodies."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import asyncio,hashlib,json,subprocess,types
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/stageB'
from signalpost.sources import registry_changes as current
from signalpost.sources.http import Response
from signalpost.sources.blobstore import BlobStore
from signalpost.models.envelope import Envelope
oldcode=subprocess.check_output(['git','show','f0786702:src/signalpost/sources/registry_changes.py'],cwd=ROOT,text=True)
old=types.ModuleType('signalpost.sources.previous_registry_changes');old.__package__='signalpost.sources';exec(compile(oldcode,'previous_registry_changes','exec'),old.__dict__)


def main():
    summary={}
    for sample in ['frozen','daily']:
        dest=DEST/sample;settings=json.loads((dest/'settings.json').read_text(encoding='utf8'))
        work=Path(expand(settings['working_directory']));blobs=BlobStore(work/'state')
        rows=[json.loads(line) for line in (work/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        report=json.loads((dest/'report.json').read_text(encoding='utf8'))
        events=[];per=[];prior_count=0;types_count=Counter();claims_count=0
        for row in rows:
            env=Envelope.model_validate(row);scope=current.subunit_scope(env,blobs)
            selected=[c for c in row['claims'] if c['field'].startswith('registry_change.') and c['availability']=='available']
            assert len(selected)<=50
            assert [(current.timestamp(c['value']['date']),c['value']['event_id'],c['field']) for c in selected]==sorted([(current.timestamp(c['value']['date']),c['value']['event_id'],c['field']) for c in selected],reverse=True)
            ev={e['id']:e for e in row['evidence']}
            for c in selected:
                v=c['value'];receipt=next(ev[eid] for eid in c['evidence_ids'] if ev[eid]['extraction_method']==current.METHOD)
                rawbody=blobs.read(receipt['content_sha256']);assert hashlib.sha256(rawbody).hexdigest()==receipt['content_sha256']
                assert receipt['claim_span'] in rawbody.decode('utf8')
                raw=json.loads(rawbody)
                for key in receipt['locator'].strip('/').split('/'):raw=raw[int(key)] if isinstance(raw,list) else raw[key]
                endpoint='underenheter' if '/oppdateringer/underenheter?' in receipt['source_url'] else 'enheter'
                response=Response(rawbody,200,receipt['source_url'],receipt['retrieved_at'],receipt['content_sha256'])
                prior_error=None
                try:previous_count=len(old.extract(raw,response,receipt['locator'],row['organisation_number'],endpoint,scope).claims)
                except Exception as exc:
                    previous_count=0;prior_error=getattr(exc,'code',type(exc).__name__)
                prior_count+=previous_count;claims_count+=1;types_count[(endpoint,v['event_type'])]+=1
                events.append({'organisation_number':row['organisation_number'],'value':v,'exact_excerpt':receipt['claim_span'],
                    'source_url':receipt['source_url'],'retrieved_at':receipt['retrieved_at'],'content_sha256':receipt['content_sha256'],
                    'locator':receipt['locator'],'previous_extractor_claim_count_for_this_event':previous_count,
                    'previous_extractor_error_for_this_event':prior_error})
            per.append({'organisation_number':row['organisation_number'],'events':len(selected),
                'coverage':row['run']['refresh'].get('registry_activity',{}),
                'briefing_change':next(s for s in row['run']['synthesis']['briefing'] if s['topic']=='change')})
        result={'sample':sample,'events_published':claims_count,'companies_with_registry_events':sum(x['events']>0 for x in per),
            'event_types':{str(k):v for k,v in types_count.items()},'previous_extractor_claims_on_the_same_retained_events':prior_count,
            'shared_registry_http_requests':sum('/oppdateringer/' in e['url'] for e in report['request_log']),
            'companies_truncated':sum(x['coverage'].get('truncated',False) for x in per),'per_company':per,'events':events}
        (dest/'events_audit.json').write_text(portable_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
        summary[sample]={k:v for k,v in result.items() if k not in {'events','per_company'}}
    (DEST/'event_comparison.json').write_text(portable_text(json.dumps(summary,indent=2)+'\n'),encoding='utf8')
    print(json.dumps(summary))

if __name__=='__main__':main()
