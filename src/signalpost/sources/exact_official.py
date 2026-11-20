"""Stage S exact-ID official sources: the source's own record must carry our orgnr.

S2 Støtteregisteret (Brønnøysundregistrene, NLOD 2.0): dated state-aid awards
whose single registered beneficiary role holds our exact organisation number.
S3 Research Council of Norway projects and SkatteFUNN approvals (NLOD 2.0),
from a bundled snapshot built by scripts/build_official_snapshots.py.
S4 Finanstilsynet registry (NLOD 2.0): own licences and agent registrations of the
Company entity whose organisationNumber equals ours.
S5 Mattilsynet Smilefjes inspections (CC BY 4.0) at our orgnr or a registry-proven
subunit, from a bundled snapshot.

No names, domains or fuzzy matching widen company scope. Failures and partial
coverage stay explicit; dates and amounts are copied only when the record
supplies them, never inferred.
"""
import asyncio
import json
import math
import re
from datetime import date, datetime, timezone

from ..budget import SourceFailure
from ..workers import offload
from .extract import Section, add, missing, response_source
from . import state_aid_bulk

METHOD = 'signalpost.exact_official.v1'
FAMILIES = ('state_aid', 'research', 'licences', 'inspections')
# Site grouping and labels for each family.
SITE_GROUP = {'status_events': 'activity','signature': 'people', 'prokura': 'people', 'group': 'what-it-does', 'state_aid': 'activity', 'research': 'activity', 'licences': 'what-it-does', 'inspections': 'activity'}
LABELS = {'state_aid.award.': 'State aid award', 'research.project.': 'Research or innovation project',
          'licences.': 'Finanstilsynet licence/registration',
          'inspections.inspection.': 'Food safety inspection (Mattilsynet)'}
STOTTE_HOST = 'stottetiltak-registerinfo-api.app.brreg.no'
STOTTE = 'https://' + STOTTE_HOST + '/api/v1/soek/stoettetildeling'
STOTTE_PAGE_SIZE = 100
STOTTE_MAX_PAGES = 5
HOSTS = {STOTTE_HOST, 'api.finanstilsynet.no'}
SECTION_BY_HOST = {STOTTE_HOST: 'state_aid', 'api.finanstilsynet.no': 'licences'}
# Legacy constructor hint; PublicHttp now retries robots on every origin.
# This never authorizes data access while robots remains unreachable.
ROBOTS_UNSERVED = {STOTTE_HOST}
POLITENESS_SECONDS = 1  # per host, between request completion and next start
REFUSALS = {'public_robots_blocked', 'public_robots_unavailable', 'public_http_401', 'public_http_403', 'public_http_429'}
WINDOW_YEARS = 3
# Only a registered award record counts. Other/unknown statuses abstain.
AWARD_STATUSES = {'stoettetiltaksstatus.registrert'}


def org_id(value):
    if not isinstance(value, str):
        return None
    return value.replace(' ', '') if re.fullmatch(r'[0-9]{9}|[0-9]{3} [0-9]{3} [0-9]{3}', value) else None


def window_start(now):
    try:
        return now.date().replace(year=now.year - WINDOW_YEARS)
    except ValueError:
        return now.date().replace(year=now.year - WINDOW_YEARS, day=28)


def iso_day(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def finite_amount(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def state_aid_award(item, org, now):
    """Return (value, pointer suffixes) for an exact-beneficiary award, else None."""
    if not isinstance(item, dict):
        return None
    award_id = item.get('stoettetiltaksnummer')
    if not isinstance(award_id, str) or not re.fullmatch(r'[0-9]{1,20}', award_id):
        return None
    if not str(item.get('type', '')).startswith('stoettetiltakstype.stoettetildeling'):
        return None
    if item.get('status') not in AWARD_STATUSES:
        return None
    roles = item.get('rolle')
    if not isinstance(roles, list):
        return None
    recipients, givers = [], []
    for i, role in enumerate(roles):
        if not isinstance(role, dict) or role.get('rolleinnehavertype') != 'virksomhet':
            continue
        holder = role.get('rolleinnehaverVirksomhet') or {}
        if role.get('type') == 'rolletype.stoettemottaker':
            recipients.append((i, org_id(holder.get('organisasjonsnummer'))))
        elif role.get('type') == 'rolletype.stoettegiver':
            givers.append((i, org_id(holder.get('organisasjonsnummer')), holder.get('navn')))
    # Exactly one beneficiary, and it is us: a shared award cannot be attributed.
    if len(recipients) != 1 or recipients[0][1] != org:
        return None
    if len(givers) != 1 or not givers[0][1] or not isinstance(givers[0][2], str) or not givers[0][2].strip():
        return None
    day = iso_day(item.get('tildelingsdato'))
    if day is None or not window_start(now) <= day <= now.date():
        return None
    value = {'company_orgnr': org, 'award_id': award_id, 'date': day.isoformat(),
             'date_source': 'award date (tildelingsdato) as registered in Støtteregisteret',
             'granting_authority': givers[0][2].strip(), 'granting_authority_orgnr': givers[0][1],
             'label': 'State aid award'}
    paths = [f'/rolle/{recipients[0][0]}/rolleinnehaverVirksomhet/organisasjonsnummer', '/stoettetiltaksnummer', '/tildelingsdato',
             f'/rolle/{givers[0][0]}/rolleinnehaverVirksomhet/organisasjonsnummer', f'/rolle/{givers[0][0]}/rolleinnehaverVirksomhet/navn']
    amount = item.get('tildeltBeloep')
    if isinstance(amount, dict) and finite_amount(amount.get('beloep')) and isinstance(amount.get('valuta'), str) \
            and re.fullmatch(r'[A-Z]{3}', amount['valuta']):
        value.update(amount=amount['beloep'], currency=amount['valuta'])
        paths += ['/tildeltBeloep/beloep', '/tildeltBeloep/valuta']
    else:
        interval = item.get('beloepsintervall')
        if isinstance(interval, dict) and finite_amount(interval.get('fraBeloep')) and finite_amount(interval.get('tilBeloep')) \
                and interval['fraBeloep'] <= interval['tilBeloep']:
            value.update(amount_range={'from': interval['fraBeloep'], 'to': interval['tilBeloep']})
            paths += ['/beloepsintervall/fraBeloep', '/beloepsintervall/tilBeloep']
    for key, name in (('tilknyttetStoetteordning', 'scheme_id'), ('stoetteinstrument', 'instrument')):
        if isinstance(item.get(key), str) and item[key].strip():
            value[name] = item[key].strip()
            paths.append('/' + key)
    return value, paths


def merged_claim(section, response, org, family, field, value, paths, source_class):
    """One verbatim pointer receipt per supporting scalar, merged into one claim."""
    source = response_source(response)
    start = len(section.claims)
    for path in paths:
        add(section, source, org, family, field, value, path, source_class=source_class, method=METHOD)
    created = section.claims[start:]
    if created:
        created[0].evidence_ids = list(dict.fromkeys(c.evidence_ids[0] for c in created))
        section.claims = section.claims[:start] + [created[0]]


def stotte_url(page):
    return f'{STOTTE}?pageSize={STOTTE_PAGE_SIZE}&page={page}&sortBy=STOETTETILTAKSNUMMER&sortDirection=ASC'


def stotte_payload(org):
    return [{'field': 'STOETTEMOTTAKER_ORGNR', 'value': org, 'matchType': 'EXACT_MATCH'}]


async def state_aid(org, http, now):
    section = Section()
    responses = []
    for page in range(1, STOTTE_MAX_PAGES + 1):
        response = await http.request(stotte_url(page), org, stotte_payload(org), headers={'Accept': 'application/json'})
        data = json.loads(response.body)
        items = data.get('stoettetildeling') if isinstance(data, dict) else None
        if not isinstance(items, list):
            raise SourceFailure('state_aid_schema')
        responses.append(response)
        for i, item in enumerate(items):
            award = state_aid_award(item, org, now)
            if award:
                value, paths = award
                merged_claim(section, response, org, 'state_aid', 'state_aid.award.' + value['award_id'], value,
                             [f'/stoettetildeling/{i}' + p for p in paths], 'official_state_aid')
        if len(items) < STOTTE_PAGE_SIZE:
            break
    else:
        section.errors += missing('state_aid', 'state_aid_pagination_limit').errors
    if not any(c.availability == 'available' for c in section.claims):
        # The exact-recipient search ran and returned no attributable award in
        # the window: an explicit, sourced "none found", not a claim of absence
        # beyond the register's own scope.
        add(section, response_source(responses[0]), org, 'state_aid', 'state_aid.awards', None, '/stoettetildeling',
            source_class='official_state_aid', method=METHOD)
        section.state = 'not_available'
    return section


FETCHERS = {'state_aid': lambda org, http, now: state_aid(org, http, now),
            'licences': lambda org, http, now: licences(org, http, now)}
# Local bundled snapshots: no network, evidence body = the exact bundled record.
LOCAL = {'state_aid': lambda org, now, blobs, envelope: state_aid_bulk.section(org, now, blobs),
         'research': lambda org, now, blobs, envelope: record_section('research', 'research.project.', load_bundle(RESEARCH_BUNDLE), org,
                                                                      now, research_value, blobs, 'official_research', 'project_id'),
         'inspections': lambda org, now, blobs, envelope: inspections_section(org, envelope, now, blobs)}


def enabled_families(config):
    return [f for f in FAMILIES if getattr(config, f, False)]


async def enrich(envelopes, client, config, budget, blobs, update):
    from .exact_public import PublicHttp
    eligible = sorted(o for o, e in envelopes.items() if e.run.sections.get('identity') == 'available')
    http = PublicHttp(client, config, budget, blobs, hosts=HOSTS, sections=SECTION_BY_HOST,
                      robots_unserved=ROBOTS_UNSERVED, politeness=POLITENESS_SECONDS)
    now = datetime.now(timezone.utc)
    live = []
    for family in enabled_families(config):
        if family in LOCAL:
            for org in eligible:
                try:
                    # Bundle decompression and matching are CPU work; keep them off
                    # the event loop so concurrent website timeouts are not starved.
                    section = await offload(LOCAL[family], org, now, blobs, envelopes[org])
                except (SourceFailure, ValueError, TypeError, OSError) as exc:
                    section = missing(family, getattr(exc, 'code', type(exc).__name__))
                update(envelopes[org], family, section)
            continue
        live.append(family)

    async def run_live(family):
        fetch = FETCHERS[family]
        stop = None  # (code, state) once the source is refused or limits are reached
        for org in eligible:
            if stop:
                update(envelopes[org], family, missing(family, stop[0], state=stop[1]))
                continue
            try:
                section = await fetch(org, http, now)
            except (SourceFailure, ValueError, TypeError) as exc:
                code = getattr(exc, 'code', type(exc).__name__)
                state = 'blocked' if code in REFUSALS else 'failed'
                if code in REFUSALS or code in {'deadline', 'budget_exhausted'}:
                    stop = (code, state)  # one refusal/limit closes the source for the run; no hammering
                section = missing(family, code, state=state)
            update(envelopes[org], family, section)
    # Live families use different hosts, each paced by its own lock and clock.
    await asyncio.gather(*(run_live(f) for f in live))


# --- S3 research projects (bundled snapshot; appended to exact_official.py) ---
import gzip as _gzip
from functools import lru_cache as _lru_cache
from pathlib import Path as _Path
from types import SimpleNamespace as _NS

RESEARCH_BUNDLE = _Path(__file__).resolve().parents[1] / 'data' / 'research_projects.json.gz'
RESEARCH_LABELS = {'rcn': 'Research Council of Norway project', 'skattefunn_2024_2026': 'SkatteFUNN-approved R&D project',
                   'skattefunn_2002_2024': 'SkatteFUNN-approved R&D project'}


@_lru_cache(maxsize=4)
def load_bundle(path):
    """Local bundled snapshot; schema/size bounded, never a network fallback."""
    raw = _Path(path).read_bytes()
    if len(raw) > 64_000_000:
        raise SourceFailure('bundle_too_large')
    data = json.loads(_gzip.decompress(raw))
    if data.get('schema') != 1 or not isinstance(data.get('records'), dict) or not isinstance(data.get('sources'), list):
        raise SourceFailure('bundle_schema')
    return data


def excel_day(value):
    try:
        serial = float(value)
    except (TypeError, ValueError):
        return None
    if not 1 <= serial < 2958466:
        return None
    from datetime import timedelta
    return date(1899, 12, 30) + timedelta(days=int(serial))


def research_value(record, org, now):
    """(value, pointer paths) for one bundled record whose own orgnr field is ours."""
    source, f = record.get('source'), record.get('fields') or {}
    if source == 'rcn':
        if (f.get('organisasjonsnummer') or '').strip() != org or f.get('prosjektansvarlig_type') != 'Organisasjon':
            return None
        if f.get('prosjektfase') not in {'Bevilgning', 'Avsluttet'}:
            return None
        start, end = f.get('prosjektstart') or '', f.get('prosjektslutt') or ''
        if not (re.fullmatch(r'\d{4}', start) and re.fullmatch(r'\d{4}', end)) or int(start) > now.year or int(end) < window_start(now).year:
            return None
        if not (f.get('prosjektnummer') or '').strip() or not (f.get('prosjekttittel') or '').strip():
            return None
        value = {'company_orgnr': org, 'project_id': f['prosjektnummer'].strip(), 'title': f['prosjekttittel'].strip(),
                 'date': start, 'date_precision': 'year', 'date_source': 'project start year (prosjektstart) as published',
                 'start_year': start, 'end_year': end,
                 'phase': 'granted' if f['prosjektfase'] == 'Bevilgning' else 'completed',
                 'source': 'Research Council of Norway', 'label': RESEARCH_LABELS['rcn']}
        paths = ['/fields/organisasjonsnummer', '/fields/prosjektnummer', '/fields/prosjekttittel', '/fields/prosjektstart',
                 '/fields/prosjektslutt', '/fields/prosjektfase']
        for key, name in (('aktivitet', 'programme'), ('virkemiddel', 'instrument')):
            if (f.get(key) or '').strip():
                value[name] = f[key].strip(); paths.append('/fields/' + key)
        amount = (f.get('tildelt_belop') or '').strip()
        if re.fullmatch(r'\d+(\.\d+)?', amount) and float(amount) > 0:
            # As given for this project over its whole period; the source states no unit.
            value.update(amount=float(amount), amount_note='granted total for the project period as given; unit not stated in source')
            paths.append('/fields/tildelt_belop')
        return value, paths
    if source in {'skattefunn_2024_2026', 'skattefunn_2002_2024'}:
        new = source == 'skattefunn_2024_2026'
        org_key = 'Organisasjonsnr' if new else 'Organisasjonsnummer'
        if (f.get(org_key) or '').strip() != org:
            return None
        approved = f.get('Godkjent') == 'JA' if new else (f.get('Søknad godkjent') == 'JA' and f.get('Søknad avslått') == 'NEI')
        decided = excel_day(f.get('Vedtaksdato'))
        if not approved or decided is None or not window_start(now) <= decided <= now.date():
            return None
        if not (f.get('Prosjektnummer') or '').strip() or not (f.get('Prosjekttittel') or '').strip():
            return None
        value = {'company_orgnr': org, 'project_id': str(f['Prosjektnummer']).strip(), 'title': f['Prosjekttittel'].strip(),
                 'date': decided.isoformat(), 'date_precision': 'day',
                 'date_source': 'SkatteFUNN decision date (Vedtaksdato) as published, decoded from the spreadsheet date serial',
                 'decision_date_serial': f['Vedtaksdato'], 'source': 'SkatteFUNN (Research Council of Norway)',
                 'label': RESEARCH_LABELS[source]}
        paths = ['/fields/' + org_key, '/fields/Prosjektnummer', '/fields/Prosjekttittel', '/fields/Vedtaksdato',
                 '/fields/' + ('Godkjent' if new else 'Søknad godkjent')]
        return value, paths
    return None


def bundled_sources(bundle):
    return {s['key']: s for s in bundle['sources']}


def bundled_records(bundle, org):
    return bundle['records'].get(org, [])


def record_section(family, field_prefix, bundle, org, now, derive, blobs, source_class, id_key):
    """Publish every bundled record of ours; each record's exact bytes are the stored evidence body."""
    from .http import Response
    section = Section()
    sources = bundled_sources(bundle)
    for text in bundled_records(bundle, org):
        record = json.loads(text)
        derived = derive(record, org, now)
        if not derived:
            continue
        value, paths = derived
        field = f"{field_prefix}{record['source']}.{value[id_key]}"
        if any(c.field == field for c in section.claims):
            continue  # the same project/inspection id listed twice publishes once
        meta = sources[record['source']]
        body = text.encode('utf8')
        sha = blobs.put(body)
        response = Response(body, 200, meta['source_url'], meta['retrieved_at'], sha)
        merged_claim(section, response, org, family, field, value, paths, source_class)
    if not any(c.availability == 'available' for c in section.claims):
        section.state = 'not_available'
        section.errors += missing(family, family + '_none_in_bundled_snapshot', state='not_available').errors
    return section


# --- S4 Finanstilsynet registry (live exact-orgnr lookup) ---
FT_HOST = 'api.finanstilsynet.no'
FT = 'https://' + FT_HOST + '/registry/v2'


def ft_search_url(org):
    return f'{FT}/legal-entities/search?query={org}&entityType=Company&pageSize=50&page=1'


def ft_entity_url(entity_id):
    return f'{FT}/legal-entities?ids={entity_id}'


def ft_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}(T[0-9:.]+)?', value):
        return None
    return iso_day(value[:10])


def licence_values(entity, org):
    """(value, paths) per licence row of an entity record whose own organisationNumber is ours."""
    if not isinstance(entity, dict) or org_id(entity.get('organisationNumber')) != org or entity.get('legalEntityType') != 'Company':
        return []
    own_id = entity.get('legalEntityId')
    if not isinstance(own_id, int):
        return []
    result = []
    for i, licence in enumerate(entity.get('licences') or []):
        if not isinstance(licence, dict):
            continue
        holder = licence.get('licensedEntity') or {}
        kind = licence.get('serviceProviderType')
        ltype = licence.get('licenceType') or {}
        code = ltype.get('code')
        names = ltype.get('name') or {}
        name = names.get('english') or names.get('norwegian')
        if not isinstance(code, str) or not re.fullmatch(r'[A-Z0-9_]{2,20}', code) or not isinstance(name, str) or not name.strip():
            continue
        base = f'/legalEntities/0/licences/{i}'
        paths = ['/legalEntities/0/organisationNumber', base + '/licenceType/code',
                 base + '/licenceType/name/' + ('english' if names.get('english') else 'norwegian')]
        if kind == 'Licensed' and holder.get('legalEntityId') == own_id:
            value = {'company_orgnr': org, 'role': 'licensed', 'licence_code': code, 'licence_name': name.strip()}
            key = f'{code}.self'
        elif kind == 'Agent' and isinstance(holder.get('legalEntityId'), int) and holder['legalEntityId'] != own_id \
                and isinstance(holder.get('legalEntityName'), str) and holder['legalEntityName'].strip():
            # Registered as an agent for another licensed company: not our own licence.
            value = {'company_orgnr': org, 'role': 'agent', 'licence_code': code, 'licence_name': name.strip(),
                     'principal': holder['legalEntityName'].strip(), 'principal_registry_id': holder['legalEntityId']}
            paths += [base + '/licensedEntity/legalEntityName', base + '/serviceProviderType']
            key = f"{code}.agent.{holder['legalEntityId']}"
        else:
            continue
        registered = ft_date(licence.get('registeredDate'))
        if registered:
            value['registered_date'] = registered.isoformat()
            value['registered_date_source'] = 'registeredDate as published by Finanstilsynet'
            paths.append(base + '/registeredDate')
        value.update(registry_entity_id=own_id, label='Finanstilsynet licence/registration')
        result.append((key, value, paths))
    return result


async def licences(org, http, now):
    section = Section()
    search = await http.request(ft_search_url(org), org, headers={'Accept': 'application/json'})
    data = json.loads(search.body)
    hits = data.get('legalEntities') if isinstance(data, dict) else None
    if not isinstance(hits, list):
        raise SourceFailure('licences_schema')
    if isinstance(data.get('total'), int) and data['total'] > len(hits):
        raise SourceFailure('licences_search_incomplete')
    exact = [h for h in hits if isinstance(h, dict) and org_id(h.get('organisationNumber')) == org and h.get('legalEntityType') == 'Company']
    if len(exact) > 1:
        return missing('licences', 'licences_ambiguous_id', state='ambiguous')
    if not exact:
        add(section, response_source(search), org, 'licences', 'licences.registrations', None, '/legalEntities',
            source_class='official_financial_registry', method=METHOD)
        section.state = 'not_available'
        return section
    entity_id = exact[0].get('legalEntityId')
    if not isinstance(entity_id, int):
        raise SourceFailure('licences_schema')
    record = await http.request(ft_entity_url(entity_id), org, headers={'Accept': 'application/json'})
    entities = (json.loads(record.body) or {}).get('legalEntities')
    if not isinstance(entities, list) or len(entities) != 1:
        raise SourceFailure('licences_schema')
    for key, value, paths in licence_values(entities[0], org):
        if any(c.field == 'licences.' + key for c in section.claims):
            continue
        merged_claim(section, record, org, 'licences', 'licences.' + key, value, paths, 'official_financial_registry')
    if not section.claims:
        add(section, response_source(record), org, 'licences', 'licences.registrations', None, '/legalEntities/0/licences',
            source_class='official_financial_registry', method=METHOD)
        section.state = 'not_available'
    return section


# --- S5 Mattilsynet Smilefjes inspections (bundled snapshot) ---
INSPECTIONS_BUNDLE = _Path(__file__).resolve().parents[1] / 'data' / 'food_inspections.json.gz'
# Grade meanings as published by Mattilsynet in the dataset's catalogue entry (data.norge.no).
INSPECTION_COLUMNS = ('tilsynsobjektid', 'orgnummer', 'navn', 'postnr', 'poststed', 'tilsynid', 'status', 'dato',
                      'total_karakter', 'tilsynsbesoektype')
GRADES = {'0': 'No breaches of the regulations found (big smile)',
          '1': 'Minor breaches not requiring follow-up (big smile)',
          '2': 'Breaches requiring follow-up (straight mouth)',
          '3': 'Serious breaches of the regulations (sad mouth)'}


def proven_subunits(envelope):
    """Registry-proven subunits of this company: orgnr -> the subunits.unit claim."""
    units = {}
    for c in envelope.claims:
        if (c.field.startswith('subunits.unit.') and c.availability == 'available' and not c.carried_forward
                and isinstance(c.value, dict) and org_id(str(c.value.get('organisation_number') or ''))):
            units[str(c.value['organisation_number'])] = c
    return units


def inspection_value(record, org, now, subunits=()):
    if record.get('source') != 'smilefjes':
        return None
    f = record.get('fields') or {}
    workplace = (f.get('orgnummer') or '').strip()
    if workplace == org:
        matched = 'company'
    elif workplace in subunits:
        matched = 'registered_subunit'
    else:
        return None
    raw = f.get('dato') or ''
    if not re.fullmatch(r'\d{8}', raw):
        return None
    try:
        day = date(int(raw[4:]), int(raw[2:4]), int(raw[:2]))
    except ValueError:
        return None
    if not window_start(now) <= day <= now.date():
        return None
    grade = f.get('total_karakter')
    if grade not in GRADES or not (f.get('tilsynid') or '').strip():
        return None
    value = {'company_orgnr': org, 'workplace_orgnr': workplace, 'matched_as': matched, 'inspection_id': f['tilsynid'].strip(),
             'date': day.isoformat(), 'date_precision': 'day', 'date_source': 'inspection date (dato, ddmmyyyy) as published',
             'grade': int(grade), 'result': GRADES[grade], 'label': 'Food safety inspection (Mattilsynet smilefjes)'}
    paths = ['/fields/orgnummer', '/fields/tilsynid', '/fields/dato', '/fields/total_karakter']
    for key, name in (('navn', 'workplace_name'), ('poststed', 'place'), ('tilsynsbesoektype', 'visit_type_code')):
        if (f.get(key) or '').strip():
            value[name] = f[key].strip(); paths.append('/fields/' + key)
    return value, paths


def inspections_section(org, envelope, now, blobs):
    bundle = load_bundle(INSPECTIONS_BUNDLE)
    units = proven_subunits(envelope)
    section = Section()
    texts = list(bundled_records(bundle, org))
    for unit in sorted(units):
        texts += [t for t in bundled_records(bundle, unit) if t not in texts]
    probe = Section()
    for text in texts:
        derived = inspection_value(json.loads(text), org, now, units)
        if not derived:
            continue
        value, _ = derived
        sub = record_section('inspections', 'inspections.inspection.', {'sources': bundle['sources'], 'records': {org: [text]}},
                             org, now, lambda r, o, n: inspection_value(r, o, n, units), blobs, 'official_food_inspection', 'inspection_id')
        for claim in sub.claims:
            if any(c.field == claim.field for c in section.claims):
                continue
            if value['matched_as'] == 'registered_subunit':
                # The parent link is a dependency: cite the registry subunit claim's own evidence.
                claim.evidence_ids = list(dict.fromkeys(claim.evidence_ids + units[value['workplace_orgnr']].evidence_ids))
            section.claims.append(claim)
        section.evidence += sub.evidence
    if not section.claims:
        section.state = 'not_available'
        section.errors += missing('inspections', 'inspections_none_in_bundled_snapshot', state='not_available').errors
    return section


def number(value):
    """Exact source number as text: no rounding, scaling or scientific notation."""
    return str(int(value)) if float(value).is_integer() else repr(float(value))


def briefing_sentences(envelope):
    from ..models.synthesis import Sentence
    claims = [c for c in envelope.claims if c.availability == 'available' and not c.carried_forward]
    result = []
    awards = sorted((c for c in claims if c.field.startswith('state_aid.award.')),
                    key=lambda c: (c.value['date'], c.id), reverse=True)[:3]
    projects = sorted((c for c in claims if c.field.startswith('research.project.')),
                      key=lambda c: (c.value['date'], c.id), reverse=True)[:3]
    for claim in projects:
        v = claim.value
        when = (f"start year {v['date']}, {v['phase']}" if v['date_precision'] == 'year' else f"decision {v['date']}")
        result.append(Sentence(text=f"{v['label']}: {v['title']}; {when}.", claim_ids=[claim.id]))
    for claim in sorted((c for c in claims if c.field.startswith('licences.')), key=lambda c: c.field)[:4]:
        v = claim.value
        what = (f"licensed: {v['licence_name']} ({v['licence_code']})" if v['role'] == 'licensed' else
                f"registered agent for {v['principal']}: {v['licence_name']} ({v['licence_code']})")
        result.append(Sentence(text=f"Finanstilsynet registry — {what}.", claim_ids=[claim.id]))
    for claim in sorted((c for c in claims if c.field.startswith('inspections.inspection.')),
                        key=lambda c: (c.value['date'], c.id), reverse=True)[:2]:
        v = claim.value
        where = 'at the company' if v['matched_as'] == 'company' else f"at registered workplace {v['workplace_orgnr']}"
        result.append(Sentence(text=f"Food safety inspection {where}: {v['date']}; grade {v['grade']} — {v['result']}.", claim_ids=[claim.id]))
    for claim in awards:
        v = claim.value
        amount = (f"{number(v['amount'])} {v['currency']}" if 'amount' in v else
                  f"{number(v['amount_range']['from'])}–{number(v['amount_range']['to'])} " +
                  (v['currency'] + ' ' if v.get('currency') else '') + '(registered range)' if 'amount_range' in v else
                  'amount unavailable')
        result.append(Sentence(text=f"State aid award: {amount} from {v['granting_authority']}; {v['date']}.", claim_ids=[claim.id]))
    return result
