import pytest
from signalpost.web.candidates import legal_name, legal_name_slugs, generate
from signalpost.web.proof import score
from signalpost.web.html import Page
from tests.test_websites import html, OUR


@pytest.mark.parametrize('suffix',['AS','ASA','DA','ENK'])
def test_suffixes_and_requested_transliterations_are_candidates_only(suffix):
    name=legal_name('ÆØÅ Verksted '+suffix)
    assert name=='æøå verksted'
    slugs=legal_name_slugs(name)
    assert {'aeoeaaverksted.no','aeoeaa-verksted.no','aoaverksted.no','aoa-verksted.no'} <= set(slugs)
    page=Page(html('No company number here',title='ÆØÅ Verksted').encode(),'https://aeoeaaverksted.no/')
    assert score(page,OUR,{'name':'ÆØÅ Verksted '+suffix},'legal_name_slug',[]).level not in {'VERIFIED','HIGH'}


def test_registry_origins_stay_first_and_eight_candidate_cap():
    result=generate({'name':'ÆØÅ Verksted AS','website':'https://declared.no','email':'hi@email.no',
                     'brands':['Reported Brand']})
    assert [c.origin for c in result[:2]]==['registry_website','registry_email']
    assert len(result)<=8 and any(c.origin=='brand_variant' for c in result)


def test_no_leading_as_masthead_or_unique_token_shortcut():
    assert legal_name('AS Elvely')=='as elvely'
    assert 'elvely.no' not in legal_name_slugs(legal_name('AS Elvely'))
    assert 'distinctive.no' not in legal_name_slugs('distinctive industrial systems')


def test_proven_subunit_name_nomination_keeps_subunit_number():
    result=generate({'name':'Holding AS','subunits':[{'orgnr':'993578843','name':'Reported Workshop AS'}]})
    assert any(c.origin=='registry_subunit_name' and c.subunit_orgnr=='993578843' for c in result)
