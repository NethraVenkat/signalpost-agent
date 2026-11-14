import pytest
from signalpost.web.reach_identity import registered_place
from tests.test_r7_declared import page,context,ORG

@pytest.mark.parametrize('address',['0123 Oslo','Eksempelgata 12, 0123'])
def test_exact_legal_publisher_name_and_registered_place(address):
    r=registered_place(page('<header>Unrelated AS</header><footer>'+address+'</footer>'),ORG,context())
    assert r and r['tier']=='publisher_name_registered_place'

@pytest.mark.parametrize('markup',['<header>Unrelated</header><footer>0123 Oslo</footer>','<header>Unrelated AS</header><p>0123 Oslo</p>','<header>Unrelated AS</header><footer>0124 Oslo</footer>','<header>Unrelated AS</header><footer>0123 Bergen</footer>','<header>Unrelated AS</header><footer>Regnskapskontor 0123 Oslo</footer>','<header>Unrelated AS</header><footer>Our companies 0123 Oslo</footer>','<meta property="og:site_name" content="Regional Portal"><header>Unrelated AS</header><footer>0123 Oslo</footer>'])
def test_missing_suffix_wrong_place_body_service_group_portal_reject(markup):
    assert registered_place(page(markup),ORG,context()) is None

def test_other_legal_footer_owner_vetoes_even_when_our_name_in_header():
    p=page('<header>Unrelated AS</header><footer>Other Publisher AS 0123 Oslo post@example.no</footer>')
    assert registered_place(p,ORG,context()) is None

@pytest.mark.parametrize('names',['Other Publisher AS Unrelated AS','Unrelated AS Other Publisher AS'])
def test_multiple_legal_footer_owners_are_not_single_company(names):
    p=page('<header>Unrelated AS</header><footer>'+names+' 0123 Oslo</footer>')
    assert registered_place(p,ORG,context()) is None

def test_registered_place_publication_and_independent_replay(tmp_path,monkeypatch):
    import json
    import tests.test_websites as web
    from signalpost.web import rarity
    from scripts.verify_output import verify
    original=web.entity
    def entity(org):
        value=original(org);value['forretningsadresse']={'adresse':['Eksempelgata 12'],'postnummer':'0123','poststed':'Oslo','kommune':'OSLO'}
        return value
    monkeypatch.setattr(web,'entity',entity)
    data=rarity.load();monkeypatch.setattr(rarity,'load',lambda:{**data,'counts':{**data['counts'],'name':{}}})
    _,row,_,cfg=web.execute_web(tmp_path,monkeypatch,website=None,body=web.html('Example AS 0123 Oslo'))
    claim=next(c for c in row['claims'] if c['field']=='official_website')
    assert claim['value']['proof_type']=='publisher_name_registered_place'
    verify(cfg.output,cfg.state_dir,1)
    claim['value']['publisher_identity']['place']['postcode']='9999'
    cfg.output.write_text(json.dumps(row)+'\n',encoding='utf8')
    with pytest.raises(AssertionError):verify(cfg.output,cfg.state_dir,1)
