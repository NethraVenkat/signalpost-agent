from ..workers import offload
from ..budget import SourceFailure
import asyncio
import math
from datetime import date
from ..models.envelope import Error
from .extract import Section, add, finish, decode, response_source, get
from . import financial_units

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
    return await offload(extract,org,response,http.blobs)


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
    emit_record(org,response,blobs,section,index,record,'accounts.',True)
    try: latest_end=date.fromisoformat(record['regnskapsperiode']['tilDato'])
    except (KeyError,TypeError,ValueError): latest_end=None
    for old_index,old in indexed[1:] if latest_end else []:
        try:
            old_end=date.fromisoformat(old['regnskapsperiode']['tilDato'])
            old_start=date.fromisoformat(old['regnskapsperiode']['fraDato'])
            if old_end>=latest_end or old_start>old_end: continue
        except (KeyError,TypeError,ValueError): continue
        owner=old.get('virksomhet') or {}
        if not isinstance(owner,dict) or str(owner.get('organisasjonsnummer'))!=org:
            section.errors.append(Error(section='accounts',code='history_wrong_company',message='Historical statement does not match this organisation; withheld'))
            continue
        before_claims,before_evidence=len(section.claims),len(section.evidence)
        try:
            emit_record(org,response,blobs,section,old_index,old,'accounts.history.'+old_end.isoformat()+'.',False)
        except SourceFailure:
            del section.claims[before_claims:]; del section.evidence[before_evidence:]
            section.errors.append(Error(section='accounts',code='history_malformed',message='Malformed historical statement withheld'))
        break  # At most one earlier entity statement; no extra requests.
    return finish(section)


def emit_record(org,response,blobs,section,index,record,prefix,allow_calibration):
    period = record.get("regnskapsperiode") or {}
    end = period.get("tilDato")
    reporting = {"fiscal_year": str(end)[:4] if end else None, "period_start": period.get("fraDato"), "period_end": end,
                 "currency": record.get("valuta"), "unit": record.get("enhet"), "account_type": record.get("regnskapstype")}
    reported_identity=dict(reporting)
    confirmed=allow_calibration and reporting['unit'] is None and reporting['currency']=='NOK'
    calibration=[]
    if confirmed:
        reporting.update({'unit':'NOK','source_unit':None,'unit_basis':'four_exact_parent_2025_ratios_within_0.995_1.005'})
        calibration=financial_units.evidence(blobs)
        section.evidence.extend(calibration)
    for name, path in PATHS.items():
        value = get(record, path)
        if value is None and name not in {'revenue','operating_result','result_before_tax','net_result','equity','total_assets','total_liabilities'}:
            continue
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or (isinstance(value,float) and not math.isfinite(value))):
            raise SourceFailure("malformed_financial_value", name)
        add(section, response_source(response), org, "accounts", prefix + name, value,
            f"/{index}/" + "/".join(path), reporting=reporting, effective=end,id_reporting=reported_identity)
        if confirmed:
            section.claims[-1].evidence_ids.extend(e.id for e in calibration)
            section.claims[-1].reasons['unit']='whole_NOK_confirmed_by_four_ratio_calibration_no_multiplier'
        if reporting["unit"] is None:
            section.claims[-1].reasons["unit"] = "scale_not_declared_by_source_or_reviewed_openapi"
            section.claims[-1].reasons["unit_crosscheck"] = "NOK_calibration_not_applied_to_other_or_missing_currencies"
            if not allow_calibration: section.claims[-1].reasons['unit_crosscheck']='historical_unit_not_inferred_from_latest_calibration'
