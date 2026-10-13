import json
from pathlib import Path
import pytest
from tests.test_registry import config,execute,handler
from signalpost.models.envelope import Envelope
from signalpost.models.synthesis import Sentence
from signalpost.synthesis.validate import sentence_error,validate_synthesis
from signalpost.synthesis.template import generate


def envelope(tmp_path):
    cfg=config(tmp_path,['923609016'])
    _,rows=execute(cfg)
    return Envelope.model_validate(rows[0]),cfg


def test_template_citations_unknowns_and_all_shapes(tmp_path):
    from signalpost.models.shapes import serialize,validate
    row,cfg=envelope(tmp_path)
    summary=row.run.synthesis
    assert summary.checks.sentences==summary.checks.cited>0 and summary.checks.values_verified
    assert 'First observation' in summary.summary
    assert any(item.family=='accounts' for item in summary.sections.unknowns)
    for shape in ('union','contract','reference'):
        result=serialize(row,shape);validate(result,shape)
        synthesis=result['profile']['synthesis'] if shape=='reference' else result['run']['synthesis']
        assert synthesis==summary.model_dump(mode='json')


@pytest.mark.parametrize('kind',['number','name','url','quote','missing','unavailable'])
def test_unverified_sentence_is_dropped(tmp_path,kind):
    row,_=envelope(tmp_path)
    name=next(c for c in row.claims if c.field=='identity.legal_name')
    examples={'number':'Employees: 99999999.','name':'CEO: Invented Person.','url':'Official website: https://invented.example.',
              'quote':'Registered activity: «Invented business».','missing':'CEO: Example.','unavailable':'Employees: 0.'}
    key='f'*64 if kind=='missing' else next(c.id for c in row.claims if c.availability!='available') if kind=='unavailable' else name.id
    bad=Sentence(text=examples[kind],claim_ids=[key])
    assert sentence_error(bad,row)
    summary=generate(row);summary.sections.what_it_does=[bad]
    checked=validate_synthesis(summary,row)
    assert checked.sections.what_it_does==[] and checked.checks.dropped_sentences>=1
    assert any(item.family=='what_it_does' for item in checked.sections.unknowns)


def test_counts_cite_distinct_records_and_never_create_claims(tmp_path):
    from tests.test_websites import OTHER
    import httpx
    cfg=config(tmp_path,['923609016'])
    def response(request):
        if '/underenheter' in request.url.path:
            return httpx.Response(200,json={'_embedded':{'underenheter':[{'organisasjonsnummer':'993578843','overordnetEnhet':'923609016','navn':'Branch One'},
                {'organisasjonsnummer':'988258229','overordnetEnhet':'923609016','navn':'Branch Two'}]},'page':{'totalPages':1}})
        return handler()(request)
    _,rows=execute(cfg,response)
    row=Envelope.model_validate(rows[0]);units=[c for c in row.claims if c.family=='subunits' and c.availability=='available']
    count=next(s for s in row.run.synthesis.sections.scale if s.value_kind=='derived')
    assert count.count==2 and set(count.claim_ids)=={c.id for c in units}
    assert not any(c.field.startswith('synthesis_support') for c in row.claims)
    assert not sentence_error(count,row)
    assert sentence_error(count.model_copy(update={'count':3,'text':'Registered workplaces: 3.'}),row)=='unverified_derived_count'
    assert sentence_error(count.model_copy(update={'claim_ids':[units[0].id,units[0].id]}),row)=='unverified_derived_count'
    assert sentence_error(count.model_copy(update={'record_type':'board_members'}),row)=='unverified_derived_count'
    assert sentence_error(count.model_copy(update={'text':'Registered workplaces: 3.'}),row)=='unverified_derived_count'


def test_low_identity_level_cannot_support_summary(tmp_path,monkeypatch):
    from tests.test_websites import execute_web
    _,body,_,_=execute_web(tmp_path,monkeypatch)
    row=Envelope.model_validate(body)
    website=next(c for c in row.claims if c.field=='official_website')
    website.value['identity_level']='LOW'
    assert sentence_error(Sentence(text='Official website: '+website.value['final_url']+'.',claim_ids=[website.id]),row)=='identity_below_threshold'


def test_registered_activity_and_self_description_sources(tmp_path,monkeypatch):
    from tests.test_websites import execute_web,html
    _,body,_,cfg=execute_web(tmp_path,monkeypatch,body=html(extra='') .replace('<title>','<meta name="description" content="We make useful software for customers."><title>'))
    descriptions=[c for c in body['claims'] if c['field'].startswith('website_description.')]
    assert len(descriptions)==1 and descriptions[0]['value']['self_description']
    evidence={e['id']:e for e in body['evidence']}
    for key in descriptions[0]['evidence_ids']:
        item=evidence[key]
        assert item['claim_span'] in (cfg.state_dir/'blobs'/item['content_sha256']).read_text()
    assert 'Website self-description' in body['run']['synthesis']['summary']


def test_same_prior_snapshot_is_byte_identical_and_derived_text_not_a_change(tmp_path):
    baseline=config(tmp_path/'prior',['923609016']);execute(baseline)
    report,a=execute(config(tmp_path/'a',['923609016'],previous=baseline.output))
    rerun,b=execute(config(tmp_path/'b',['923609016'],previous=baseline.output))
    assert json.dumps(a[0]['run']['synthesis'],sort_keys=True)==json.dumps(b[0]['run']['synthesis'],sort_keys=True)
    assert report['changes']==rerun['changes']==0
    assert 'First observation' not in a[0]['run']['synthesis']['summary']


def test_registry_descriptions_have_exact_source_locators(tmp_path):
    import httpx
    from tests.test_registry import entity
    cfg=config(tmp_path,['923609016'])
    def response(request):
        if request.url.path.endswith('/923609016') and '/enhetsregisteret/' in request.url.path:
            data=entity('923609016')
            data.update(aktivitet=['Utvikling av programvare.'],vedtektsfestetFormaal='Drive programvareutvikling.')
            return httpx.Response(200,json=data)
        return handler()(request)
    _,rows=execute(cfg,response)
    row=Envelope.model_validate(rows[0]);evidence={e.id:e for e in row.evidence}
    for field,pointer,quote in [('identity.registered_activity','/aktivitet','Utvikling av programvare.'),
                              ('identity.statutory_purpose','/vedtektsfestetFormaal','Drive programvareutvikling.')]:
        claim=next(c for c in row.claims if c.field==field)
        assert claim.availability=='available'
        assert evidence[claim.evidence_ids[0]].locator==pointer
        assert '«'+quote+'»' in row.run.synthesis.summary


def test_changed_role_summary_links_both_original_evidence_sides(tmp_path):
    baseline=config(tmp_path/'prior',['923609016']);execute(baseline,handler(role_name='Person One'))
    _,rows=execute(config(tmp_path/'changed',['923609016'],previous=baseline.output),handler(role_name='Person Two'))
    row=Envelope.model_validate(rows[0]);s=row.run.synthesis
    assert len(row.changes)==1 and len(s.sections.changes)==1
    sentence=s.sections.changes[0]
    assert 'Person One' in sentence.text and 'Person Two' in sentence.text
    records={c.id:c for c in s.change_claims}
    assert len(sentence.claim_ids)==2
    assert {eid for cid in sentence.claim_ids for eid in records[cid].evidence_ids}==set(row.changes[0].old_evidence_ids+row.changes[0].new_evidence_ids)
    assert not sentence_error(sentence,row)


def test_about_paragraph_skips_hidden_text_and_uses_stored_page_only():
    from signalpost.web.html import Page
    body=b'<html><body><p hidden>Invented hidden company text.</p><p>Visible <strong>company</strong> description.</p></body></html>'
    page=Page(body,'https://example.no/om-oss')
    assert page.paragraphs[0][0]=='Visible company description.'
    assert page.paragraphs[0][1] in body.decode()


def test_output_verifier_rejects_unchecked_synthesis(tmp_path):
    from scripts.verify_output import verify_synthesis
    row,_=envelope(tmp_path)
    raw=row.model_dump(mode='json')
    assert verify_synthesis(raw)[0]==1
    raw['run']['synthesis']['sections']['what_it_does'][0]['text']='Employees as registered: 99999999.'
    with pytest.raises(AssertionError,match='Unverified synthesis'):
        verify_synthesis(raw)
