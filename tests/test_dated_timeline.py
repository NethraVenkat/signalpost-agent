import copy,json,socket
from pathlib import Path
from types import SimpleNamespace
import pytest
from signalpost.synthesis import timeline as tl


def claim(field,value,index='a',refs=None):
 return {'id':index*64,'field':field,'family':field.split('.')[0],'value':value,'availability':'available','evidence_ids':refs or [index+'e']}


def receipt(index='a'):
 return {'id':index+'e','source_url':'https://data.brreg.no/example','retrieved_at':'2026-11-20T00:00:00Z','content_sha256':'0'*64,'locator':'/date','claim_span':'"2020"','extraction_method':'saved.test'}


def test_year_day_timestamp_labels_stable_order_and_inherited_evidence():
 claims=[claim('accounts.filed_year.2020','2020','a'),claim('identity.founding_date','2020-01-02','b'),claim('status_events.event.1',{'date':'2020-01-02T00:00:00Z','change_type':'Endring'},'c')]
 evidence=[receipt(x) for x in 'abc'];before=copy.deepcopy((claims,evidence))
 result=tl.build(list(reversed(claims)),evidence)
 assert [x.date for x in result]==['2020','2020-01-02','2020-01-02T00:00:00Z']
 assert [x.precision for x in result]==['year','day','timestamp']
 assert tl.build(claims,list(reversed(evidence)))==result
 assert [(x.claim_ids,x.evidence_ids) for x in result]==[([c['id']],c['evidence_ids']) for c in claims]
 assert (claims,evidence)==before
 assert not any(w in x.text.lower() for x in result for w in ('because','following','after which'))


@pytest.mark.parametrize('key',['source_url','retrieved_at','content_sha256','locator','claim_span','extraction_method'])
def test_incomplete_own_evidence_abstains_and_under_two_omits(key):
 claims=[claim('identity.founding_date','2020-01-01'),claim('identity.registration_date','2020-02-01','b')]
 evidence=[receipt(),receipt('b')];evidence[0][key]=''
 assert tl.build(claims,evidence)==[]
 assert tl.build(claims,evidence[1:])==[]


def test_one_claim_with_two_dates_does_not_make_two_facts():
 c=claim('roles.role.1',{'from_date':'2020-01-01','last_changed':'2021-01-01'})
 assert tl.build([c],[receipt()])==[]


@pytest.mark.parametrize('value',['2020-02-30','not a date','2020-01-01T12:00:00','2020-13','0000'])
def test_invalid_or_unzoned_dates_rejected(value):
 assert tl.precision(value) is None


def test_no_retrieval_date_or_signature_date_inferred_and_no_names():
 claims=[claim('signature.rule','SOURCE TEXT'),claim('prokura.combination.1',{'date':'2020-01-01','people':['SOURCE TEXT']},'b'),claim('identity.registration_date','2020-01-01','c')]
 assert tl.build(claims,[receipt(x) for x in 'abc'])==[]
 claims.append(claim('roles.role.1',{'name':'SOURCE TEXT','last_changed':'2021-01-01'},'d'))
 out=tl.build(claims,[receipt(x) for x in 'abcd'])
 assert len(out)==2 and 'SOURCE TEXT' not in json.dumps([x.model_dump() for x in out])


def test_filed_list_dedup_and_safe_evidence_omission():
 claims=[claim('accounts.filed_years',['2020','2021']),claim('accounts.filed_year.2020','2020','b'),claim('identity.founding_date','1999-01-01','c')]
 result=tl.build(claims,[receipt(x) for x in 'abc'])
 assert [(x.date,x.source_field) for x in result]==[('1999-01-01','identity.founding_date'),('2020','accounts.filed_year.2020'),('2021','accounts.filed_years')]


def test_projection_cannot_open_network(monkeypatch):
 def fail(*a,**k):raise AssertionError('Timeline attempted HTTP/network')
 monkeypatch.setattr(socket.socket,'connect',fail)
 import httpx
 monkeypatch.setattr(httpx.Client,'get',fail);monkeypatch.setattr(httpx.AsyncClient,'get',fail)
 assert len(tl.build([claim('identity.founding_date','2000'),claim('identity.registration_date','2001','b')],[receipt(),receipt('b')]))==2


def test_synthesis_section_and_overflow_remain_local(tmp_path):
 from signalpost.site import generate_site,company_payload
 from signalpost.runner import placeholder,update
 from signalpost.sources.extract import Section,Source,add
 from signalpost.models.evidence import utc_now
 from signalpost.synthesis.template import generate
 envelope=placeholder('923609016','timeline-test',utc_now(),families=('identity',))
 s=Section();source=Source('https://data.brreg.no/example',b'{"year":"2020"}','0'*64,utc_now())
 for i in range(200):
  add(s,source,'923609016','accounts','accounts.filed_year.'+str(1800+i),str(1800+i),'/year')
 update(envelope,'identity',s)
 synthesis=generate(envelope)
 assert len(synthesis.sections.timeline)==200
 envelope.run.synthesis=synthesis
 row=envelope.model_dump(mode='json');payload=company_payload(row)
 assert payload['timeline']==tl.for_row(row) and len(payload['timeline'])==200
 path=tmp_path/'input.jsonl';path.write_text(envelope.model_dump_json()+'\n',encoding='utf8')
 stats=generate_site(path,tmp_path/'site');assert stats['largest_profile_bytes']<250000
 html=(tmp_path/'site/c/923609016.html').read_text(encoding='utf8')
 assert 'data-dated-timeline' in html and 'Accounting year with a filed copy recorded' not in html
 data=(tmp_path/'site/c/923609016.data.js').read_text(encoding='utf8');assert 'Accounting year with a filed copy recorded' in data
 # Derived view adds neither source evidence nor claims.
 assert len(envelope.claims)==200 and len(envelope.evidence)==1
 tampered=copy.deepcopy(row);tampered['run']['synthesis']['sections']['timeline'][0]['date']='2099'
 with pytest.raises(AssertionError):tl.verify(tampered)
