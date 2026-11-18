import copy,json
import httpx,pytest
from tests.test_websites import OUR,execute_web,html
from signalpost.sources.text import decode_body
from scripts.verify_output import verify
from scripts.verify_owner_social import verify as verify_social
URL='https://facebook.com/publicstorebrand'
def new_claim(row):return next(c for c in row['claims'] if c['field'].startswith('social_profile.'))
def checked(row,cfg):
    evidence={e['id']:e for e in row['evidence']}
    return verify_social(OUR,row,evidence,lambda sha:decode_body((cfg.state_dir/'blobs'/sha).read_bytes()))
def test_exact_owner_jsonld_full_evidence_and_independent_replay(tmp_path,monkeypatch):
    node={'@type':'Organization','name':'Public Store Brand','vatID':'NO'+OUR+'MVA','sameAs':[URL]}
    body=html(extra='<script type="application/ld+json">'+json.dumps(node)+'</script>'
                    '<main><a href="'+URL+'">Facebook</a></main>')
    report,row,requests,cfg=execute_web(tmp_path,monkeypatch,body=body)
    claim=new_claim(row)
    assert claim['value']['proof_tier']=='owner_jsonld_sameas_v1' and checked(row,cfg)==1
    assert not any('facebook.com' in u for u in requests)
    assert verify(cfg.output,cfg.state_dir,1)['briefing_unverified_values']==0
    forged=copy.deepcopy(row);new_claim(forged)['value']['owner_declaration']['owner_name']='Another AS'
    with pytest.raises(AssertionError,match='Unsupported owner social declaration'):checked(forged,cfg)
def test_owner_declaration_cannot_survive_missing_or_group_website(tmp_path,monkeypatch):
    node={'@type':'Organization','identifier':OUR,'sameAs':URL}
    _,row,_,cfg=execute_web(tmp_path,monkeypatch,body=html(extra=
        '<script type="application/ld+json">'+json.dumps(node)+'</script>'
        '<main><a href="'+URL+'">Facebook</a></main>'))
    forged=copy.deepcopy(row);forged['claims']=[c for c in forged['claims'] if c['field']!='official_website']
    with pytest.raises(AssertionError,match='requires a verified/HIGH website'):checked(forged,cfg)
    forged=copy.deepcopy(row);next(c for c in forged['claims'] if c['field']=='official_website')['value']['relationship_note']='group_site'
    with pytest.raises(AssertionError,match='Unsupported social site scope'):checked(forged,cfg)
def test_linked_contact_follow_us_is_social_only_and_budgeted(tmp_path,monkeypatch):
    def response(request):
        if request.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        if request.url.path=='/kontakt':return httpx.Response(200,text=html(extra='<div class="contact">post@example.no F?lg oss <a href="'+URL+'">Facebook</a></div>'))
        return httpx.Response(200,text=html(extra='<nav><a href="/kontakt">Kontakt</a></nav>'))
    report,row,requests,cfg=execute_web(tmp_path,monkeypatch,response=response)
    claim=new_claim(row)
    assert claim['value']['proof_tier']=='own_contact_follow_us_v1' and checked(row,cfg)==1
    assert sum(u=='https://example.no/kontakt' for u in requests)==1
    assert row['run']['refresh']['owner_social']['state']=='available'
    assert not any(c['field'].startswith('contact.') and c['value']=='post@example.no' for c in row['claims'])
    assert report['requests']<=report['limits']['max_requests']
    assert verify(cfg.output,cfg.state_dir,1)['briefing_unverified_values']==0
