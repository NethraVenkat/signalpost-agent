from ..workers import offload
from urllib.parse import urlencode
import asyncio
from ..budget import SourceFailure
from .extract import Section, add, finish, decode, response_source

DETAILS={'start_date':'oppstartsdato','registration_date':'registreringsdatoEnhetsregisteret',
         'ownership_change_date':'datoEierskifte','registered_website':'hjemmeside','registered_email':'epostadresse',
         'registered_phone':'telefon','registered_mobile':'mobil','postal_address':'postadresse',
         'organisation_form':'organisasjonsform','support_unit_code':'hjelpeenhetskode',
         'employees_reported':'harRegistrertAntallAnsatte','registered_in_vat':'registrertIMvaregisteret',
         'employee_registration_date':'registreringsdatoAntallAnsatteEnhetsregisteret',
         'nav_employee_registration_date':'registreringsdatoAntallAnsatteNAVAaregisteret'}


async def fetch(org, http, progress=None):
    section = Section()
    page = 0
    total = 1
    while page < total:
        url = "https://data.brreg.no/enhetsregisteret/api/underenheter?" + urlencode({"overordnetEnhet": org, "size": 1000, "page": page})
        response = await http.get(url, org)
        result=await offload(extract_page,org,response,section,page)
        if isinstance(result,Section):return result
        if progress:progress(section)
        total=result
        page+=1
    return finish(section)


def extract_page(org,response,section,page):
        data,error=decode(response,'subunits')
        if error:return error
        items=data.get('_embedded',{}).get('underenheter',[])
        for item in items:
            if str(item.get('overordnetEnhet'))!=org:raise SourceFailure('wrong_company','Subunit parent differs from requested company')
        normalized = [{"organisation_number": item.get("organisasjonsnummer"), "name": item.get("navn"),
                       "address": item.get("beliggenhetsadresse") or item.get("postadresse"),
                       "nace": item.get("naeringskode1"),
                       "employees": None if item.get("harRegistrertAntallAnsatte") is False else item.get("antallAnsatte")}
                      for item in items]
        # Preserve every page's evidence, including empty search responses.
        for index, item in enumerate(normalized):
            key = item["organisation_number"]
            if not key:
                raise SourceFailure("malformed_subunit", "A subunit lacks its organisation number")
            add(section, response_source(response), org, "subunits", f"subunits.unit.{key}", item, f"/_embedded/underenheter/{index}")
            raw=items[index]
            for name,field in DETAILS.items():
                value=raw.get(field)
                if isinstance(value,dict):value={k:v for k,v in value.items() if k!='_links'}
                if value is not None:
                    add(section,response_source(response),org,'subunits',f'subunits.detail.{key}.{name}',value,
                        f'/_embedded/underenheter/{index}/{field}',effective=value if name.endswith('_date') else None)
        if not normalized and page == 0:
            add(section, response_source(response), org, "subunits", "subunits.units", None, "/_embedded/underenheter")
        return int(data.get('page',{}).get('totalPages',1))
