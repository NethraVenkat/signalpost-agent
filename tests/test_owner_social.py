import json
import pytest
from signalpost.web.html import Page
from signalpost.web import owner_social as m
URL='https://www.facebook.com/unrelatedbrand'
ORG='986464492'
def page(node,extra='',path='/'):
    return Page(('<html><head><script type="application/ld+json">'+json.dumps(node)+'</script></head><body>'+extra+'</body></html>').encode(),'https://example.no'+path)
def node(**extra):return {'@type':'Organization','name':'EXAMPLE AS','sameAs':[URL],**extra}
def test_own_exact_node():
    assert URL in m.declared_profiles(page(node()),'EXAMPLE AS',ORG)
def test_id_proves_different_public_brand():
    assert URL in m.declared_profiles(page(node(name='Public Brand',vatID='NO '+ORG+' MVA')),'EXAMPLE AS',ORG)
@pytest.mark.parametrize('extra',[{'name':'Example'},{'vatID':'NO 995194163 MVA'},{'vatID':'SE'+ORG},{'@type':'Person'},{'@type':['Person','Organization']},{'url':'https://foreign.no'},{'parentOrganization':{'name':'Parent AS'}},{'name':'Founder Agency'}])
def test_unmatched_owner_rejected(extra):
    assert not m.declared_profiles(page(node(**extra)),'EXAMPLE AS',ORG)
def test_founder_url_not_organisation_social():
    assert not m.declared_profiles(page(node(founder={'@type':'Person','sameAs':URL})),'EXAMPLE AS',ORG)
def test_numeric_linkedin_not_extended():
    assert not m.declared_profiles(page(node(sameAs='https://linkedin.com/company/12345')),'EXAMPLE AS',ORG)
@pytest.mark.parametrize('wrapper',['<div hidden>{}</div>','<article>{}</article>','<div class="agency">{}</div>'])
def test_hidden_agency_script(wrapper):
    script='<script type="application/ld+json">'+json.dumps(node())+'</script>'
    p=Page(wrapper.format(script).encode(),'https://example.no')
    assert not m.declared_profiles(p,'EXAMPLE AS',ORG)
def test_contact_block():
    html='<div class="contact">Telefon 12345678 F?lg oss <a href="'+URL+'">Facebook</a></div>'
    p=Page(html.encode(),'https://example.no/kontakt')
    found=m.declared_profiles(p,'EXAMPLE AS',ORG)
    assert found[URL]['tier']=='own_contact_follow_us_v1'
    assert found[URL]['span'] in p.raw
@pytest.mark.parametrize('wrapper',['<article>{}</article>','<section class="staff">{}</section>','<section class="partners">{}</section>'])
def test_contact_nonpublisher(wrapper):
    html='<div>Telefon 12345678 F?lg oss <a href="'+URL+'">Facebook</a></div>'
    assert not m.declared_profiles(Page(wrapper.format(html).encode(),'https://example.no/kontakt'),'EXAMPLE AS',ORG)

def test_malformed_jsonld_social_abstains():
    malformed='https://[object Object]'
    assert not m.declared_profiles(page(node(sameAs=malformed,founder={'@type':'Person','sameAs':malformed})),'EXAMPLE AS',ORG)

@pytest.mark.parametrize('extra',[{'identifier':995194163},{'identifier':{'value':ORG,'country':'SE'}},{'address':{'addressCountry':'SE'}}])
def test_conflicting_identifier_and_country(extra):
    assert not m.declared_profiles(page(node(**extra)),'EXAMPLE AS',ORG)
@pytest.mark.parametrize('wrapper',['<section class="news">{}</section>','<div class="team">{}</div>'])
def test_jsonld_nonowner_region(wrapper):
    script='<script type="application/ld+json">'+json.dumps(node())+'</script>'
    assert not m.declared_profiles(Page(wrapper.format(script).encode(),'https://example.no'),'EXAMPLE AS',ORG)
def test_unrelated_nested_organisation_is_not_site_owner():
    assert not m.declared_profiles(page({'@type':'WebPage','mentions':node()}),'EXAMPLE AS',ORG)

def test_person_url_in_separate_script_stays_excluded():
    person='<script type="application/ld+json">'+json.dumps({'@type':'Person','sameAs':URL})+'</script>'
    assert not m.declared_profiles(page(node(),extra=person),'EXAMPLE AS',ORG)

def test_relative_own_node_url_resolves_on_verified_site():
    assert URL in m.declared_profiles(page(node(url='/')),'EXAMPLE AS',ORG)
