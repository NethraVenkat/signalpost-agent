from ..workers import offload
from ..budget import SourceFailure
import asyncio
from .extract import Section, Source, add, finish, get, decode, response_source
from .registry_fields import EXTRA,GROUPS,boolean

BASE = "https://data.brreg.no/enhetsregisteret/api/enheter/"
FIELDS = {
    "legal_name": ("navn",), "organisation_form": ("organisasjonsform",),
    "registration_date": ("registreringsdatoEnhetsregisteret",),
    "registered_address": ("forretningsadresse",), "postal_address": ("postadresse",),
    "municipality": ("forretningsadresse", "kommune"), "employees": ("antallAnsatte",),
    "registered_website": ("hjemmeside",), "bankrupt": ("konkurs",),
    "under_liquidation": ("underAvvikling",), "deleted": ("slettedato",),
    "latest_submitted_accounts": ("sisteInnsendteAarsregnskap",),
    "registered_activity": ("aktivitet",), "statutory_purpose": ("vedtektsfestetFormaal",),
}


def extract(org, data, source):
    if str(data.get("organisasjonsnummer")) != org:
        raise SourceFailure("wrong_company", "Registry identity differs from requested orgnr")
    section = Section()
    for field, key in [('founding_date', 'stiftelsesdato'), ('vat_registration_date', 'registreringsdatoMerverdiavgiftsregisteret')]:
        if data.get(key):
            add(section, source, org, 'identity', 'identity.' + field, data[key], '/' + key, effective=data[key])
    for field, path in FIELDS.items():
        value = get(data, path)
        if field == "employees" and data.get("harRegistrertAntallAnsatte") is False:
            value = None
        if field == "deleted" and value is not None:
            deleted_date, value = value, True
        else:
            deleted_date = None
        # Publish no fabricated false value when slettedato is missing.
        add(section, source, org, "identity", "identity." + field, value, "/" + "/".join(path), effective=value if field == "registration_date" else deleted_date)
    for i in range(1, 4):
        field = f"naeringskode{i}"
        add(section, source, org, "identity", f"identity.nace{i}", data.get(field), "/" + field)
    for field,(key,kind) in EXTRA.items():
        actual=next((k for k in data if k.casefold()==key.casefold()),key)
        value=data.get(actual)
        if value is None:continue
        if kind=='bool':value=boolean(value)
        add(section,source,org,'identity','identity.'+field,value,'/'+actual,
            effective=value if field.endswith('_date') else None)
    for field,(key,keys) in GROUPS.items():
        value=data.get(key)
        if isinstance(value,dict):value={k:value[k] for k in keys if k in value}
        if value in (None,{}):continue
        add(section,source,org,'identity','identity.'+field,value,'/'+key)
    return finish(section)


async def fetch(org, http):
    response = await http.get(BASE + org, org)
    return await offload(extract_response,org,response)


def extract_response(org,response):
    data, error = decode(response, "identity")
    return error or extract(org, data, response_source(response))
