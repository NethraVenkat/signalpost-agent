"""CI uses only saved fixtures; no network success can mask a refresh defect."""
import json
from scripts.refresh_proof_harness import run_suite,fixture,CASES


def test_saved_source_refresh_precision_recall_and_stale_evidence(tmp_path):
    result=run_suite(tmp_path/'replay')
    assert result['planted_causal_changes']==result['true_positives']==7
    assert result['false_positives']==result['false_negatives']==0
    assert result['precision']==result['recall']==1
    assert result['unchanged_changes']==result['idempotent_changes']==0
    assert result['equivalent_timestamp_changes']==0
    assert not result['equivalent_timestamp_execution']['coverage_observations']
    assert result['false_change_rate_unchanged']==0
    assert not result['unchanged_execution']['coverage_observations']
    assert not result['idempotent_execution']['coverage_observations']
    assert result['transient']['changes']==0 and result['transient']['carried_claims']>0
    assert result['transient']['prior_receipts_and_times_preserved'] and result['transient']['stale_markers_present']
    for case in CASES:
        c=result['cases'][case]
        assert c['detected'] and c['idempotent_changes']==0 and not c['unexpected_changes']
        assert not c['repeat_execution']['coverage_observations']
        assert not c['execution']['unrecorded_urls']
        assert c['execution']['verification']['synthesis_unverified_values']==0
        assert c['execution']['verification']['briefing_unverified_values']==0
        assert sum(a.startswith('--') for a in c['execution']['argv'])==7
    root=tmp_path/'replay'
    base=json.loads((root/'baseline/envelopes.jsonl').read_text(encoding='utf8'))
    closed=json.loads((root/'nav_removed/envelopes.jsonl').read_text(encoding='utf8'))
    assert any(c['field'].startswith('hiring.job.') and c['availability']=='available' for c in base['claims'])
    assert any(c['type']=='closed_job' and c['new_evidence_ids'] for c in closed['changes'])
    assert not any(c['field'].startswith('hiring.job.') and c['availability']=='available' for c in closed['claims'])
    stale=json.loads((root/'transient/envelopes.jsonl').read_text(encoding='utf8'))
    assert any(c['field']=='official_website' and c['carried_forward'] for c in stale['claims'])
    assert any(c['family']=='accounts' and c['carried_forward'] for c in stale['claims'])
    assert 'Previously supported' in (root/'transient/site/c/918266917.html').read_text(encoding='utf8')


def test_fixture_is_exact_saved_seed_20261113_body_collection():
    m,bodies=fixture()
    assert m['source_sample_seed']==20261113 and m['organisation_number']=='918266917'
    assert len(bodies)==len(m['routes'])
    assert m['source_run_id']=='r5-stageC-daily-seed20261113-recovery'


def test_registry_event_comparison_normalizes_only_equivalent_aware_instants():
    from signalpost.refresh.diff import meaning
    from tests.test_r5_stage_b import extract,event
    original=extract(event(dato='2025-06-12T00:15:38.309+02:00')).claims[0]
    equivalent=original.model_copy(deep=True);equivalent.value['date']='2025-06-11T22:15:38.309000Z'
    assert meaning(original)==meaning(equivalent)
    assert original.value['date']=='2025-06-12T00:15:38.309+02:00'
    different=original.model_copy(deep=True);different.value['date']='2025-06-11T22:15:39.309Z'
    assert meaning(original)!=meaning(different)
    naive=original.model_copy(deep=True);naive.value['date']='2025-06-11T22:15:38.309'
    assert meaning(original)!=meaning(naive)
    for key,value in [('title','Different event label'),('changed_fields',[{'path':'/forretningsadresse','operation':'remove'}])]:
        changed=equivalent.model_copy(deep=True);changed.value[key]=value
        assert meaning(original)!=meaning(changed)


def test_refresh_equivalent_publisher_timestamp_has_zero_events_with_exact_receipts(tmp_path):
    import httpx
    from tests.test_registry import config,execute,handler
    from tests.test_registry_changes import event
    from scripts.verify_output import verify
    def source(date):
        def dispatch(request):
            if '/oppdateringer/' in request.url.path:
                sub=request.url.path.endswith('/underenheter')
                records=[] if sub else [event(dato=date)]
                return httpx.Response(200,json={'page':{'number':0,'size':1000,'totalElements':len(records),'totalPages':1 if records else 0},
                    '_embedded':{'oppdaterteUnderenheter' if sub else 'oppdaterteEnheter':records}})
            return handler()(request)
        return dispatch
    first=config(tmp_path/'first',['923609016'],registry_changes=True)
    _,before=execute(first,source('2025-06-12T00:15:38.309+02:00'))
    second=config(tmp_path/'second',['923609016'],registry_changes=True,previous=first.output)
    report,after=execute(second,source('2025-06-11T22:15:38.309000Z'))
    a=next(c for c in before[0]['claims'] if c['field'].startswith('registry_change.'))
    b=next(c for c in after[0]['claims'] if c['field'].startswith('registry_change.'))
    assert a['value']['date']!=b['value']['date'] and a['evidence_ids']!=b['evidence_ids']
    assert report['changes']==report['observation_changes']==0
    assert verify(second.output,second.state_dir,1,second.organisations,second.report)['registry_events_verified']==1
