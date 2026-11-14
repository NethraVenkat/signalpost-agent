import pytest
from signalpost.sources.dated_official import frames,GLEIF

ORG='923609016';LEI='A'*20


def item(**registration):
    return {'data':[{'id':LEI,'attributes':{'lei':LEI,'entity':{'registeredAs':ORG,'registeredAt':{'id':'RA000472'},
        'jurisdiction':'NO','legalAddress':{'country':'NO'}},'registration':registration}}]}


def test_initial_registration_and_only_explicit_renewal_date():
    document=item(initialRegistrationDate='2025-01-01T00:00:00Z',lastRenewalDate='2026-02-01T00:00:00Z',
        lastUpdateDate='2026-03-01T00:00:00Z',nextRenewalDate='2027-02-01T00:00:00Z')
    result=list(frames(document,ORG,GLEIF+'lei-records?filter=x'))
    assert [r[2] for r in result]==['initialRegistrationDate','lastRenewalDate']
    assert result[0][0]['lei']==LEI and result[1][0]['title']=='LEI last renewal'


def test_update_next_renewal_period_end_and_retrieval_never_supply_event_dates():
    assert not list(frames(item(lastUpdateDate='2026-01-01T00:00:00Z',nextRenewalDate='2027-01-01T00:00:00Z'),ORG,GLEIF+'lei-records?x'))
    assert not list(frames([{'regnskapsperiode':{'tilDato':'2025-12-31'}}],ORG,'https://data.brreg.no/regnskapsregisteret/regnskap/'+ORG))
    assert not list(frames([2024,2025],ORG,'https://data.brreg.no/regnskapsregisteret/regnskap/aarsregnskap/kopi/'+ORG+'/aar'))


@pytest.mark.parametrize('date',['2026','2026-01-01','not a date','2026-01-01T00:00:00'])
def test_invalid_or_naive_dates_abstain(date):
    assert not list(frames(item(initialRegistrationDate=date),ORG,GLEIF+'lei-records?x'))


def test_exact_company_and_registration_authority_still_required():
    document=item(initialRegistrationDate='2026-01-01T00:00:00Z')
    assert not list(frames(document,'993578843',GLEIF+'lei-records?x'))
    document['data'][0]['attributes']['entity']['registeredAt']['id']='OTHER'
    assert not list(frames(document,ORG,GLEIF+'lei-records?x'))
