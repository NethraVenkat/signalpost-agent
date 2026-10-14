import json
import pytest
from signalpost.profiles import project
from signalpost.models.shapes import serialize
from tests.test_synthesis import envelope
from tests.test_registry import config,execute


def test_profile_has_reference_module_types_and_exact_claim_values_and_hashes(tmp_path):
    e,_=envelope(tmp_path/'source')
    p=project(e)
    assert isinstance(p['evidence'],dict)
    assert set(p['evidence'])=={'registry_live','financials','roles','locations','website','hiring','activity'}
    keys={'field','status','source_type','source_class','source_url','retrieved_at','value',
          'as_of','note','content_sha256','source_row_key','effective_at'}
    statuses={'available','not_found','not_applicable','not_fetched','source_error','blocked'}
    for name,record in p['evidence'].items():
        assert set(record)==keys and record['field']==name and record['status'] in statuses
        assert isinstance(record['retrieved_at'],str) and isinstance(record['source_url'],str)
        if record['status'] in {'source_error','not_applicable','blocked'}:
            assert record['value'] is None
    assert p['evidence']['registry_live']['value']['organisation_number']==e.organisation_number
    expected=[{'id':c.id,'field':c.field,'value':c.value,'evidence_ids':c.evidence_ids} for c in e.claims if c.availability=='available']
    assert p['verified_claims']==expected
    records={r.id:r for r in e.evidence}
    for c in p['verified_claims']:
        for eid in c['evidence_ids']:
            assert p['source_records'][eid]['content_sha256']==records[eid].content_sha256
            assert p['source_records'][eid]['claim_span']==records[eid].claim_span
    # Serialization remains unchanged and provenance round-trips as ordinary JSON.
    assert isinstance(serialize(e,'contract')['evidence'],list)
    assert isinstance(serialize(e,'union')['evidence'],list)
    assert json.loads(json.dumps(p))==p


@pytest.mark.parametrize('shape',['union','contract','reference'])
def test_profiles_preserve_input_order_duplicates_invalids_and_all_envelope_shapes(tmp_path,shape):
    cfg=config(tmp_path,['923609016','bad','923609016'],envelope_shape=shape,
               profiles_output=tmp_path/'profiles.jsonl')
    report,rows=execute(cfg)
    p=[json.loads(line) for line in cfg.profiles_output.read_text(encoding='utf8').splitlines()]
    assert [r['organisation_number'] for r in p]==['923609016','bad','923609016']
    assert p[0]==p[2] and p[1]['verified_claims']==[]
    assert all(r['value'] is None and r['status']!='available' for r in p[1]['evidence'].values())
    assert report['profiles_output']['rows']==3
    from scripts.verify_output import verify
    verify(cfg.output,cfg.state_dir,3,cfg.organisations,cfg.report)


def test_profiles_output_failure_is_reported_without_losing_envelopes(tmp_path):
    target=tmp_path/'unwritable';target.mkdir()
    report,rows=execute(config(tmp_path/'run',['923609016'],profiles_output=target))
    assert len(rows)==1 and report['profiles_output']['state']=='failed'
    assert any('profiles output failed' in warning for warning in report['warnings'])


def test_partial_profile_keeps_supported_values_and_incomplete_state(tmp_path):
    e,_=envelope(tmp_path/'source');e.run.sections['identity']='failed'
    p=project(e)
    assert p['evidence']['registry_live']['status']=='source_error'
    assert p['evidence']['registry_live']['value']['name']==next(c.value for c in e.claims if c.field=='identity.legal_name')


def test_cli_accepts_reference_runner_flag_names_and_writes_both_files(tmp_path,monkeypatch):
    import respx
    from signalpost.cli import main
    from tests.test_registry import handler
    cfg=config(tmp_path,['923609016'])
    profiles=tmp_path/'profiles.jsonl'
    monkeypatch.setattr('sys.argv',['signalpost','run','--organisations',str(cfg.organisations),
        '--output',str(cfg.output),'--profiles-output',str(profiles),'--report',str(cfg.report),
        '--state-dir',str(cfg.state_dir),'--run-id','kit-call','--expected-count','1'])
    with respx.mock(assert_all_called=False) as router:
        router.get(url__regex=r'https://data\.brreg\.no/.*').mock(side_effect=handler())
        assert main()==0
    assert json.loads(cfg.output.read_text(encoding='utf8'))['run_id']=='kit-call'
    assert json.loads(profiles.read_text(encoding='utf8'))['organisation_number']=='923609016'
    assert json.loads(cfg.report.read_text(encoding='utf8'))['profiles_output']['rows']==1


def test_profile_temporary_cannot_overwrite_input(tmp_path,monkeypatch):
    from signalpost.cli import main
    inp=tmp_path/'profiles.jsonl.tmp';inp.write_text('923609016',encoding='utf8')
    monkeypatch.setattr('sys.argv',['signalpost','run','--organisations',str(inp),
        '--output',str(tmp_path/'out.jsonl'),'--profiles-output',str(tmp_path/'profiles.jsonl'),
        '--report',str(tmp_path/'report.json')])
    assert main()==1 and inp.read_text(encoding='utf8')=='923609016'
