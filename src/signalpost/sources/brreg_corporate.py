"""Exact-orgnr authority and direct group relationships from Brreg's public APIs."""
import json
from .extract import Section, add, decode, finish, missing, response_source
from ..budget import SourceFailure
from ..workers import offload
from ..identity.orgnr import valid

FAMILIES = ('signature', 'prokura', 'group')
METHOD = 'signalpost.brreg_corporate.v1'
SITE_GROUP = {'signature': 'people', 'prokura': 'people', 'group': 'what-it-does'}


def url(org, family):
    if not valid(org) or family not in FAMILIES:
        raise SourceFailure('wrong_company', 'Invalid exact organisation number or corporate section')
    return ('https://data.brreg.no/enhetsregisteret/api/konsernstruktur/' + org if family == 'group'
            else 'https://data.brreg.no/fullmakt/enheter/' + org + '/' + ('signatur' if family == 'signature' else 'prokura'))


async def fetch(org, family, http):
    response = await http.get(url(org, family), org)
    return await offload(extract, org, family, response)


def clean_text(value):
    return value if isinstance(value, str) and value.strip() else None


def holders(items):
    result = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        name = clean_text(item.get('navn'))
        role = item.get('rolle') or {}
        entry = {k: v for k, v in {'name': name, 'role_code': clean_text(role.get('kode')),
                                  'role': clean_text(role.get('tekstforklaring'))}.items() if v is not None}
        if name:
            result.append(entry)
    return result


def extract(org, family, response):
    if response.url != url(org, family):
        raise SourceFailure('wrong_company', 'Corporate response URL differs from exact request')
    data, error = decode(response, family)
    if error:
        return error
    if not isinstance(data, dict):
        raise SourceFailure('wrong_company', 'Corporate response is not an entity object')
    section = Section()
    source = response_source(response)
    def emit(field, value, pointer, effective=None):
        add(section, source, org, family, family + '.' + field, value, pointer,
            effective=effective, method=METHOD)
    if family != 'group':
        if (data.get('enhet') or {}).get('organisasjonsnummer') != org:
            raise SourceFailure('wrong_company', 'Authority entity differs from requested orgnr')
        status = data.get('status') or {}
        routine = (status.get('rutineStatus') or {}).get('kode')
        if routine != 'OK':
            return missing(family, 'authority_lookup_unavailable',
                           'Publisher routine status: ' + str(routine), state='not_available' if routine == 'NA' else 'failed')
        basis = data.get('signeringsGrunnlag') or {}
        rule = clean_text((basis.get('signaturProkuraRoller') or {}).get('signaturProkuraFritekst'))
        if rule:
            emit('rule', rule, '/signeringsGrunnlag/signaturProkuraRoller/signaturProkuraFritekst')
        # Preserve the publisher's possible-combination scope, not a legal opinion
        # that these people can override a registered free-text restriction.
        if (status.get('kombinasjonStatus') or {}).get('kode') == 'OK':
            for i, combo in enumerate((data.get('signeringsKombinasjon') or {}).get('kombinasjon', [])):
                if not isinstance(combo, dict) or not clean_text(combo.get('tekstforklaring')):
                    continue
                value = {'scope': 'Publisher possible signing combination; registered rule restrictions apply',
                         'description': combo['tekstforklaring'], 'code': combo.get('kode'),
                         'people': holders(combo.get('personRolleKombinasjon')),
                         'rule_status': (status.get('regelStatus') or {}).get('kode')}
                if rule:
                    value['registered_rule'] = rule
                emit('combination.' + str(i), value, f'/signeringsKombinasjon/kombinasjon/{i}/tekstforklaring')
        if not section.claims:
            return missing(family, 'authority_rule_unavailable', state='not_available')
        return finish(section)
    # The API can return an entire hierarchy. Only edges incident to the exact
    # requested node are published; siblings and indirect descendants stay out.
    nodes = []
    def walk(node, pointer='', parent=None):
        if not isinstance(node, dict) or not valid(node.get('organisasjonsnummer', '')):
            raise SourceFailure('wrong_company', 'Group node lacks an exact valid orgnr')
        nodes.append((node, pointer, parent))
        for i, child in enumerate(node.get('children') or []):
            if not isinstance(child, dict) or child.get('parentOrganisasjonsnummer') != node['organisasjonsnummer']:
                raise SourceFailure('wrong_company', 'Group hierarchy contradicts explicit parent orgnr')
            walk(child, pointer + f'/children/{i}', node)
    walk(data)
    if not any(n['organisasjonsnummer'] == org for n, _, _ in nodes):
        raise SourceFailure('wrong_company', 'Requested orgnr absent from returned group hierarchy')
    seen = set()
    for node, pointer, parent in nodes:
        child_id = node['organisasjonsnummer']
        parent_id = node.get('parentOrganisasjonsnummer')
        if parent_id is None or not valid(parent_id) or parent_id == child_id:
            continue
        if org not in {parent_id, child_id}:
            continue
        key = (parent_id, child_id)
        if key in seen:
            continue
        seen.add(key)
        relation = 'parent' if child_id == org else 'subsidiary'
        value = {'relationship': relation, 'parent_organisation_number': parent_id,
                 'subsidiary_organisation_number': child_id,
                 'parent_name': node.get('parentNavn'), 'subsidiary_name': node.get('navn'),
                 'registered_basis': node.get('grunnlag'), 'relationship_type': node.get('knytningsform'),
                 'date': node.get('dato')}
        emit(relation + '.' + (parent_id if relation == 'parent' else child_id), value,
             pointer + '/organisasjonsnummer', effective=node.get('dato'))
    if not section.claims:
        return missing('group', 'no_direct_group_relationships', state='not_available')
    return finish(section)


def verify(org, data, evidence, stored_body):
    """Re-derive every corporate value/locator from its exact saved response."""
    from .http import Response
    from .text import decode_body
    cache = {}
    checked = 0
    for claim in data['claims']:
        if claim['family'] not in FAMILIES or claim['availability'] != 'available':
            continue
        expected_url = url(org, claim['family'])
        receipts = [evidence[eid] for eid in claim['evidence_ids']]
        assert receipts and all(e['extraction_method'] == METHOD and e['source_url'] == expected_url for e in receipts), 'Corporate source identity differs'
        for e in receipts:
            key = (claim['family'], e['content_sha256'])
            if key not in cache:
                body = stored_body(e['content_sha256'])
                raw = body.encode('utf8') if isinstance(body, str) else body
                section = extract(org, claim['family'], Response(raw, 200, expected_url, e['retrieved_at'], e['content_sha256']))
                cache[key] = (section, decode_body(raw))
            section, text = cache[key]
            match = next((c for c in section.claims if c.field == claim['field'] and c.value == claim['value'] and c.reporting_period == claim.get('reporting_period')), None)
            assert match is not None, 'Unsupported corporate authority or group value'
            matched = next(x for x in section.evidence if x.id in match.evidence_ids)
            assert e['locator'] == matched.locator and e['claim_span'] in text, 'Corporate evidence locator differs'
        checked += 1
    return checked
