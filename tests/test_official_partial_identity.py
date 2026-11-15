import json
from types import SimpleNamespace
from signalpost.web.html import Page
from signalpost.web.owner_social import declared_profiles
from signalpost.web.collector import extract_contacts_and_social
from signalpost.sources.extract import Section
URL='https://facebook.com/anonymousbrand';ORG='923609016'
def test_missing_names_do_not_equal_exact_legal_identity():
    page=Page(('<script type="application/ld+json">'+json.dumps({'@type':'Organization','sameAs':URL})+'</script>').encode(),'https://example.no')
    assert not declared_profiles(page,None,ORG)
def test_partial_registry_identity_abstains_before_social_publication():
    page=Page(('<script type="application/ld+json">'+json.dumps({'@type':'Organization','identifier':ORG,'sameAs':URL})+'</script>').encode(),'https://example.no')
    section=Section();site=SimpleNamespace(value={'identity_level':'VERIFIED','final_url':'https://example.no'},evidence_ids=[])
    extract_contacts_and_social(section,ORG,site,[(SimpleNamespace(url='https://example.no'),page)],context={'name':None})
    assert not any(c.field.startswith('social_profile.') for c in section.claims)
