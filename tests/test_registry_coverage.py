import json
import httpx
from signalpost.sources import brreg_enhet,brreg_roller,brreg_underenheter,regnskap
from signalpost.sources.http import Response
from signalpost.sources.extract import Source,Section
from signalpost.sources.blobstore import BlobStore
from signalpost.models.evidence import utc_now
from tests.test_nav import ORG,SUB


def response(tmp_path,value):
    body=json.dumps(value).encode();blobs=BlobStore(tmp_path)
    return Response(body,200,'https://data.brreg.no/example',utc_now(),blobs.put(body)),blobs


def test_reported_false_zero_and_absent_identity_fields(tmp_path):
    r,b=response(tmp_path,{'organisasjonsnummer':ORG,'navn':'Example AS','registrertIMvaRegisteret':False,
                         'kapital':{'belop':0,'valuta':'NOK'}})
    s=brreg_enhet.extract_response(ORG,r);claims={c.field:c for c in s.claims}
    assert claims['identity.registered_in_vat'].value is False
    assert claims['identity.registered_capital'].value=={'belop':0,'valuta':'NOK'}
    assert 'identity.articles_date' not in claims
    assert next(e for e in s.evidence if e.id in claims['identity.registered_in_vat'].evidence_ids).locator=='/registrertIMvaRegisteret'


def test_subunit_and_role_details_preserve_core_records_and_locators(tmp_path):
    r,_=response(tmp_path,{'_embedded':{'underenheter':[{'organisasjonsnummer':SUB,'overordnetEnhet':ORG,
                'oppstartsdato':'2020-01-01','harRegistrertAntallAnsatte':False,'antallAnsatte':0}]}})
    s=Section();brreg_underenheter.extract_page(ORG,r,s,0)
    assert next(c for c in s.claims if c.field=='subunits.unit.'+SUB).value['employees'] is None
    detail=next(c for c in s.claims if c.field.endswith('.employees_reported'))
    assert detail.value is False
    assert next(e for e in s.evidence if e.id in detail.evidence_ids).locator.endswith('/0/harRegistrertAntallAnsatte')
    r,_=response(tmp_path,{'organisasjonsnummer':ORG,'rollegrupper':[{'roller':[{'ansvarsandel':0,'rekkefolge':0,
         'person':{'navn':{'fornavn':'Example'},'fodselsdato':'2000-01-01'},'avregistrert':False}]}]})
    s=brreg_roller.extract(ORG,r)
    assert sum(c.field.startswith('roles.role.') for c in s.claims)==1
    assert all(c.value==0 for c in s.claims if c.field.startswith('roles.detail.'))
    assert not any('fodselsdato' in e.locator for e in s.evidence)


def test_extra_accounts_are_reported_not_computed_and_keep_period(tmp_path):
    r,b=response(tmp_path,[{'regnskapstype':'SELSKAP','virksomhet':{'organisasjonsnummer':ORG},
        'regnskapsperiode':{'fraDato':'2025-01-01','tilDato':'2025-12-31'},'valuta':'EUR','enhet':'EUR',
        'eiendeler':{'sumBankinnskuddOgKontanter':0}}])
    s=regnskap.extract(ORG,r,b);claims={c.field:c for c in s.claims}
    c=claims['accounts.cash_and_bank'];assert c.value==0 and c.reporting_period['currency']=='EUR'
    assert 'accounts.current_assets' not in claims
    assert next(e for e in s.evidence if e.id in c.evidence_ids).locator=='/0/eiendeler/sumBankinnskuddOgKontanter'
