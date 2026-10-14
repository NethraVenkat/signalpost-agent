import asyncio
from ..budget import SourceFailure
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
}


async def fetch(org, http):
    response = await http.get(URL + org, org)
    return await asyncio.to_thread(extract,org,response,http.blobs)


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
    period = record.get("regnskapsperiode") or {}
    end = period.get("tilDato")
    reporting = {"fiscal_year": str(end)[:4] if end else None, "period_start": period.get("fraDato"), "period_end": end,
                 "currency": record.get("valuta"), "unit": record.get("enhet"), "account_type": record.get("regnskapstype")}
    reported_identity=dict(reporting)
    confirmed=reporting['unit'] is None and reporting['currency']=='NOK'
    calibration=[]
    if confirmed:
        reporting.update({'unit':'NOK','source_unit':None,'unit_basis':'four_exact_parent_2025_ratios_within_0.995_1.005'})
        calibration=financial_units.evidence(blobs)
        section.evidence.extend(calibration)
    for name, path in PATHS.items():
        value = get(record, path)
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
            raise SourceFailure("malformed_financial_value", name)
        add(section, response_source(response), org, "accounts", "accounts." + name, value,
            f"/{index}/" + "/".join(path), reporting=reporting, effective=end,id_reporting=reported_identity)
        if confirmed:
            section.claims[-1].evidence_ids.extend(e.id for e in calibration)
            section.claims[-1].reasons['unit']='whole_NOK_confirmed_by_four_ratio_calibration_no_multiplier'
        if reporting["unit"] is None:
            section.claims[-1].reasons["unit"] = "scale_not_declared_by_source_or_reviewed_openapi"
            section.claims[-1].reasons["unit_crosscheck"] = "NOK_calibration_not_applied_to_other_or_missing_currencies"
    return finish(section)
