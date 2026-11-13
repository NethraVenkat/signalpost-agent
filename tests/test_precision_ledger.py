import copy
from scripts.precision_ledger import recheck,kind
from tests.test_websites import execute_web,html


def website(row):return next(c for c in row['claims'] if c['field']=='official_website' and c['availability']=='available')


def test_ledger_correct_then_wrong_bytes_and_wrong_url_are_retained(tmp_path,monkeypatch):
    _,row,_,cfg=execute_web(tmp_path,monkeypatch)
    claim=website(row);body=lambda sha:(cfg.state_dir/'blobs'/sha).read_bytes()
    verdict,reasons,checks=recheck(row,claim,body)
    assert verdict=='correct' and not reasons and checks['name_match']
    broken=recheck(row,claim,lambda sha:b'not the stored response')
    assert broken[0]=='wrong' and 'hash' in broken[1][0]
    changed=copy.deepcopy(claim);changed['value']['final_url']='https://foreign.test/'
    assert recheck(row,changed,body)[0]=='wrong'
    assert claim['value']['final_url']=='https://example.no'
    _,high_row,_,high_cfg=execute_web(tmp_path/'high',monkeypatch,html('Example gate 1, 0001 OSLO <a href="tel:12345678">Phone</a>'))
    high=website(high_row)
    assert high['value']['identity_level']=='HIGH'
    verdict,reasons,checks=recheck(high_row,high,lambda sha:(high_cfg.state_dir/'blobs'/sha).read_bytes())
    assert verdict=='doubtful' and not checks['exact_company_number']
    assert any('signal-only' in reason for reason in reasons)


def test_ledger_flags_group_without_silently_removing_the_published_item(tmp_path,monkeypatch):
    _,row,_,cfg=execute_web(tmp_path,monkeypatch,html('Org.nr 923609016; parent org.nr 993578843'))
    claim=website(row);original=copy.deepcopy(row)
    verdict,reasons,checks=recheck(row,claim,lambda sha:(cfg.state_dir/'blobs'/sha).read_bytes())
    assert verdict=='doubtful' and any('Group' in r or 'Other valid' in r for r in reasons)
    assert row==original and checks['other_owner_orgnrs']==['993578843']


def test_ledger_social_rechecks_exact_owned_header_footer_context(tmp_path,monkeypatch):
    _,row,_,cfg=execute_web(tmp_path,monkeypatch,html('Org.nr 923609016 <a href="https://www.linkedin.com/company/123456">LinkedIn</a>'))
    social=next(c for c in row['claims'] if c['field'].startswith('social_profile.'))
    verdict,reasons,checks=recheck(row,social,lambda sha:(cfg.state_dir/'blobs'/sha).read_bytes())
    assert verdict=='correct' and checks['own_header_footer_and_no_founder_agency_context']
    assert kind(social)=='social'
