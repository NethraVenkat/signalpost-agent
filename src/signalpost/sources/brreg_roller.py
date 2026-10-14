from ..workers import offload
from ..budget import SourceFailure
import asyncio
from .brreg_enhet import BASE
from .extract import Section, add, finish, decode, response_source
from ..models.evidence import digest, canonical


async def fetch(org, http):
    response = await http.get(BASE + org + "/roller", org)
    return await offload(extract,org,response)


def extract(org,response):
    data, error = decode(response, "roles")
    if error:
        return error
    linked_entity = data.get("_links", {}).get("enhet", {}).get("href") if isinstance(data, dict) else None
    explicit_org = data.get("organisasjonsnummer") if isinstance(data, dict) else None
    if not isinstance(data, dict) or (str(explicit_org) != org and linked_entity != BASE + org):
        raise SourceFailure("wrong_company", "Roles parent does not match requested company")
    section = Section()
    seen = {}
    for group_index, group in enumerate(data.get("rollegrupper", [])):
        for role_index, item in enumerate(group.get("roller", [])):
            person = item.get("person") or {}
            entity = item.get("enhet") or {}
            name = person.get("navn") or {}
            if isinstance(name, dict):
                display = " ".join(str(name[k]) for k in ("fornavn", "mellomnavn", "etternavn") if name.get(k))
            else:
                display = str(name)
            entry = {"role_type": item.get("type"), "name": display or entity.get("navn") or None,
                     "entity_organisation_number": entity.get("organisasjonsnummer"), "inactive": item.get("avregistrert"),
                     "group_type": group.get("type"), "last_changed": group.get("sistEndret"), "from_date": item.get("fraDato")}
            key = digest(canonical([entry["group_type"], entry["role_type"], entry["name"], entry["entity_organisation_number"]]))[:24]
            slot = seen.get(key, 0)
            seen[key] = slot + 1
            add(section, response_source(response), org, "roles", f"roles.role.{key}.{slot}", entry,
                f"/rollegrupper/{group_index}/roller/{role_index}", effective=entry["from_date"] or entry["last_changed"])
            for name,path in {'responsibility_share':('ansvarsandel',),'order':('rekkefolge',),
                              'elected_by':('valgtAv',),'entity_deleted':('enhet','erSlettet'),
                              'entity_approval_status':('enhet','godkjenningsstatus'),
                              'entity_form':('enhet','organisasjonsform')}.items():
                value=item
                for part in path:value=value.get(part) if isinstance(value,dict) else None
                if isinstance(value,dict):value={k:v for k,v in value.items() if k!='_links'}
                if value is not None:
                    add(section,response_source(response),org,'roles',f'roles.detail.{key}.{slot}.{name}',value,
                        f'/rollegrupper/{group_index}/roller/{role_index}/'+ '/'.join(path))
    if not section.claims:
        add(section, response_source(response), org, "roles", "roles.roles", None, "/rollegrupper")
    return finish(section)
