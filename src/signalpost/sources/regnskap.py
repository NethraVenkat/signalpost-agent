from ..workers import offload
from ..budget import SourceFailure
import asyncio
import math
from datetime import date
from ..models.envelope import Error
from ..models.claim import Claim
from ..models.evidence import digest,utc_now
from .extract import Section, add, finish, decode, response_source, get
from . import accounts_years

URL = "https://data.brreg.no/regnskapsregisteret/regnskap/"
PATHS = {
    "revenue": ("resultatregnskapResultat", "driftsresultat", "driftsinntekter", "sumDriftsinntekter"),
    "operating_result": ("resultatregnskapResultat", "driftsresultat", "driftsresultat"),
    "result_before_tax": ("resultatregnskapResultat", "ordinaertResultatFoerSkattekostnad"),
    "net_result": ("resultatregnskapResultat", "aarsresultat"),
    "equity": ("egenkapitalGjeld", "egenkapital", "sumEgenkapital"),
    "total_assets": ("eiendeler", "sumEiendeler"),
    "total_liabilities": ("egenkapitalGjeld", "gjeldOversikt", "sumGjeld"),
    'paid_in_equity':('egenkapitalGjeld','egenkapital','innskuttEgenkapital','sumInnskuttEgenkaptial'),
    'retained_equity':('egenkapitalGjeld','egenkapital','opptjentEgenkapital','sumOpptjentEgenkapital'),
    'current_liabilities':('egenkapitalGjeld','gjeldOversikt','kortsiktigGjeld','sumKortsiktigGjeld'),
    'long_term_liabilities':('egenkapitalGjeld','gjeldOversikt','langsiktigGjeld','sumLangsiktigGjeld'),
    'equity_and_liabilities':('egenkapitalGjeld','sumEgenkapitalGjeld'),
    'non_current_assets':('eiendeler','anleggsmidler','sumAnleggsmidler'),
    'current_assets':('eiendeler','omloepsmidler','sumOmloepsmidler'),
    'cash_and_bank':('eiendeler','sumBankinnskuddOgKontanter'),
    'receivables':('eiendeler','sumFordringer'),'investments':('eiendeler','sumInvesteringer'),
    'inventories':('eiendeler','sumVarer'),'goodwill':('eiendeler','goodwill'),
    'sales_income':('resultatregnskapResultat','driftsresultat','driftsinntekter','salgsinntekter'),
    'salary_expenses':('resultatregnskapResultat','driftsresultat','driftskostnad','loennskostnad'),
    'operating_expenses':('resultatregnskapResultat','driftsresultat','driftskostnad','sumDriftskostnad'),
    'financial_income':('resultatregnskapResultat','finansresultat','finansinntekt','sumFinansinntekter'),
    'financial_expenses':('resultatregnskapResultat','finansresultat','finanskostnad','sumFinanskostnad'),
    'other_interest_expense':('resultatregnskapResultat','finansresultat','finanskostnad','annenRentekostnad'),
    'group_interest_expense':('resultatregnskapResultat','finansresultat','finanskostnad','rentekostnadSammeKonsern'),
    'financial_result':('resultatregnskapResultat','finansresultat','nettoFinans'),
    'tax_expense':('resultatregnskapResultat','ordinaertResultatSkattekostnad'),
    'total_comprehensive_result':('resultatregnskapResultat','totalresultat'),
}


async def fetch(org, http):
    response = await http.get(URL + org, org)
    section=await offload(extract,org,response,http.blobs)
    try:
        # Same approved registry host, concurrency limiter, retry policy and
        # global meter. No PDFs, year guessing or requests per listed year.
        await asyncio.sleep(.1)
        response=await http.get(accounts_years.YEARS.format(org=org),org)
        years=await offload(accounts_years.extract,org,response)
        section.claims.extend(years.claims);section.evidence.extend(years.evidence)
        section.errors.extend(Error(section='accounts',code='filing_years_'+e.code,message=e.message) for e in years.errors)
        if section.state=='not_available' and years.state=='available':section.state='available'
    except asyncio.CancelledError:raise
    except Exception as exc:
        code=exc.code if isinstance(exc,SourceFailure) else type(exc).__name__
        section.errors.append(Error(section='accounts',code='filing_years_'+code,message='Filing-year coverage incomplete; supported figures retained'))
        now=utc_now()
        section.claims.append(Claim(field='accounts.filed_years',value=None,availability='failed',family='accounts',
            evidence_ids=[],id=digest([org,'accounts.filed_years',None,'failed',None]),
            first_observed_at=now,last_observed_at=now,reasons={'coverage':code}))
    return section


def extract(org,response,blobs):
    data, error = decode(response, "accounts")
    if error:
        return error
    if not isinstance(data, list):
        raise SourceFailure("malformed_accounts")
    section = Section()
    if not data:
        add(section, response_source(response), org, "accounts", "accounts.latest", None, "/")
        return finish(section)
    if any(not isinstance(row,dict) for row in data): raise SourceFailure('malformed_accounts')
    emit_consolidated(org, response, blobs, section, data)
    indexed = [(index, row) for index, row in enumerate(data) if row.get("regnskapstype") == "SELSKAP"]
    if not indexed:
        add(section, response_source(response), org, "accounts", "accounts.latest", None, "/")
        section.errors.append(Error(section="accounts", code="entity_accounts_unavailable", message="Only consolidated or unknown account types returned; entity financials not published"))
        return finish(section)
    indexed.sort(key=lambda pair: str(get(pair[1], ("regnskapsperiode", "tilDato")) or ""), reverse=True)
    index, record = indexed[0]
    entity = record.get("virksomhet", {})
    reported_org = entity.get("organisasjonsnummer") if isinstance(entity, dict) else None
    if str(reported_org) != org:
        raise SourceFailure("wrong_company", "Accounts do not explicitly match the requested orgnr")
    emit_record(org,response,blobs,section,index,record,'accounts.')
    try: latest_end=date.fromisoformat(record['regnskapsperiode']['tilDato'])
    except (KeyError,TypeError,ValueError): latest_end=None
    seen={latest_end}
    for old_index,old in indexed[1:] if latest_end else []:
        try:
            old_end=date.fromisoformat(old['regnskapsperiode']['tilDato'])
            old_start=date.fromisoformat(old['regnskapsperiode']['fraDato'])
            if old_end>=latest_end or old_start>old_end or old_end in seen: continue
        except (KeyError,TypeError,ValueError): continue
        owner=old.get('virksomhet') or {}
        if not isinstance(owner,dict) or str(owner.get('organisasjonsnummer'))!=org:
            section.errors.append(Error(section='accounts',code='history_wrong_company',message='Historical statement does not match this organisation; withheld'))
            continue
        before_claims,before_evidence=len(section.claims),len(section.evidence)
        try:
            emit_record(org,response,blobs,section,old_index,old,'accounts.history.'+old_end.isoformat()+'.')
            seen.add(old_end)
        except SourceFailure:
            del section.claims[before_claims:]; del section.evidence[before_evidence:]
            section.errors.append(Error(section='accounts',code='history_malformed',message='Malformed historical statement withheld'))
    return finish(section)


def emit_consolidated(org, response, blobs, section, data):
    """Statements already in the ordinary response; no additional lookup.

    A group filing is never an entity statement or a shareholder-register claim.
    Filing ID and period keep distinct group filings separate and auditable.
    """
    seen = set()
    for index, record in enumerate(data):
        if record.get('regnskapstype') != 'KONSERN':
            continue
        owner = record.get('virksomhet') or {}
        period = record.get('regnskapsperiode') or {}
        filing = record.get('id')
        try:
            start = date.fromisoformat(period['fraDato'])
            end = date.fromisoformat(period['tilDato'])
            valid = (str(owner.get('organisasjonsnummer')) == org and start <= end
                     and isinstance(filing, int) and not isinstance(filing, bool) and filing > 0)
        except (KeyError, TypeError, ValueError, AttributeError):
            valid = False
        if not valid:
            section.errors.append(Error(section='accounts', code='consolidated_unverifiable',
                                        message='Group statement lacks exact owner, filing ID or valid period; withheld'))
            continue
        if filing in seen:
            continue
        before_claims, before_evidence = len(section.claims), len(section.evidence)
        try:
            emit_record(org, response, blobs, section, index, record,
                        f'accounts.consolidated.{end.isoformat()}.{filing}.')
            seen.add(filing)
        except SourceFailure:
            del section.claims[before_claims:]
            del section.evidence[before_evidence:]
            section.errors.append(Error(section='accounts', code='consolidated_malformed',
                                        message='Malformed group statement withheld; entity statements retained'))


def emit_record(org,response,blobs,section,index,record,prefix):
    period = record.get("regnskapsperiode") or {}
    end = period.get("tilDato")
    reporting = {"fiscal_year": str(end)[:4] if end else None, "period_start": period.get("fraDato"), "period_end": end,
                 "currency": record.get("valuta"), "unit": record.get("enhet"), "account_type": record.get("regnskapstype")}
    if prefix.startswith('accounts.consolidated.'):
        reporting['filing_id'] = record['id']
    reported_identity=dict(reporting)
    for name, path in PATHS.items():
        value = get(record, path)
        if value is None and name not in {'revenue','operating_result','result_before_tax','net_result','equity','total_assets','total_liabilities'}:
            continue
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or (isinstance(value,float) and not math.isfinite(value))):
            raise SourceFailure("malformed_financial_value", name)
        add(section, response_source(response), org, "accounts", prefix + name, value,
            f"/{index}/" + "/".join(path), reporting=reporting, effective=end,id_reporting=reported_identity)
        if reporting["unit"] is None:
            section.claims[-1].reasons["unit"] = "unit_or_scale_not_declared_by_source; no inference applied"
