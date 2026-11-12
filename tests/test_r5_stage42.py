import pytest
from signalpost.sources import brreg_enhet, brreg_underenheter
from signalpost.sources.extract import Section
from signalpost.budget import SourceFailure
from tests.test_registry_coverage import response
from tests.test_nav import ORG, SUB


def test_business_postal_are_separate_and_evidenced(tmp_path):
    raw={'organisasjonsnummer':ORG,'navn':'Example AS',
         'forretningsadresse':{'adresse':['Business 1']},'postadresse':{'adresse':['PO box 2']}}
    r,_=response(tmp_path,raw);s=brreg_enhet.extract_response(ORG,r)
    typed=[c for c in s.claims if c.field.startswith('identity.location.')]
    assert {c.value['location_type'] for c in typed}=={'business','postal'}
    assert all(c.value['organisation_number']==ORG and c.evidence_ids for c in typed)
    assert {e.locator for e in s.evidence if any(e.id in c.evidence_ids for c in typed)}=={'/forretningsadresse','/postadresse'}


def test_postal_address_never_becomes_physical_workplace(tmp_path):
    r,_=response(tmp_path,{'_embedded':{'underenheter':[{'organisasjonsnummer':SUB,'overordnetEnhet':ORG,
                                                      'postadresse':{'poststed':'Postal'}}]}})
    s=Section();brreg_underenheter.extract_page(ORG,r,s,0)
    typed=[c for c in s.claims if '.location.' in c.field]
    assert len(typed)==1 and typed[0].value['location_type']=='postal'
    assert typed[0].value['parent_organisation_number']==ORG


def test_wrong_parent_never_publishes_location(tmp_path):
    r,_=response(tmp_path,{'_embedded':{'underenheter':[{'organisasjonsnummer':SUB,'overordnetEnhet':SUB,
                                                      'beliggenhetsadresse':{'poststed':'Wrong'}}]}})
    with pytest.raises(SourceFailure):brreg_underenheter.extract_page(ORG,r,Section(),0)


@pytest.mark.parametrize('value',[None,{},'',False,0])
def test_missing_or_odd_location_never_invents_a_site(tmp_path,value):
    r,_=response(tmp_path,{'organisasjonsnummer':ORG,'navn':'Example AS','postadresse':value})
    s=brreg_enhet.extract_response(ORG,r)
    assert not any(c.field.startswith('identity.location.') for c in s.claims)
