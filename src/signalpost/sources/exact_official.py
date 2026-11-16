"""Stage S exact-ID official sources: the source's own record must carry our orgnr.

S2 Støtteregisteret (Brønnøysundregistrene, NLOD 2.0): dated state-aid awards
whose single registered beneficiary role holds our exact organisation number.

No names, domains or fuzzy matching widen company scope. Failures and partial
coverage stay explicit; dates and amounts are copied only when the record
supplies them, never inferred.
"""
import json
import math
import re
from datetime import date, datetime, timezone

from ..budget import SourceFailure
from .extract import Section, add, missing, response_source

METHOD = 'signalpost.exact_official.v1'
FAMILIES = ('state_aid',)
# Site grouping and labels for each family.
SITE_GROUP = {'state_aid': 'activity'}
LABELS = {'state_aid.award.': 'State aid award'}
STOTTE_HOST = 'stottetiltak-registerinfo-api.app.brreg.no'
STOTTE = 'https://' + STOTTE_HOST + '/api/v1/soek/stoettetildeling'
STOTTE_PAGE_SIZE = 100
STOTTE_MAX_PAGES = 5
HOSTS = {STOTTE_HOST}
SECTION_BY_HOST = {STOTTE_HOST: 'state_aid'}
# The Støtteregisteret API host resets connections on /robots.txt instead of
# serving a file (receipts in reports/r5/stageS/access). That is recorded as
# "no robots file served", the same as 404 — never as an allow-list override
# for a host that does serve rules.
ROBOTS_UNSERVED = {STOTTE_HOST}
POLITENESS_SECONDS = 1  # per host, between request completion and next start
REFUSALS = {'public_robots_blocked', 'public_http_401', 'public_http_403', 'public_http_429'}
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


FETCHERS = {'state_aid': lambda org, http, now: state_aid(org, http, now)}


def enabled_families(config):
    return [f for f in FAMILIES if getattr(config, f, False)]


async def enrich(envelopes, client, config, budget, blobs, update):
    from .exact_public import PublicHttp
    eligible = sorted(o for o, e in envelopes.items() if e.run.sections.get('identity') == 'available')
    http = PublicHttp(client, config, budget, blobs, hosts=HOSTS, sections=SECTION_BY_HOST,
                      robots_unserved=ROBOTS_UNSERVED, politeness=POLITENESS_SECONDS)
    now = datetime.now(timezone.utc)
    for family in enabled_families(config):
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


def number(value):
    """Exact source number as text: no rounding, scaling or scientific notation."""
    return str(int(value)) if float(value).is_integer() else repr(float(value))


def briefing_sentences(envelope):
    from ..models.synthesis import Sentence
    claims = [c for c in envelope.claims if c.availability == 'available' and not c.carried_forward]
    result = []
    awards = sorted((c for c in claims if c.field.startswith('state_aid.award.')),
                    key=lambda c: (c.value['date'], c.id), reverse=True)[:3]
    for claim in awards:
        v = claim.value
        amount = (f"{number(v['amount'])} {v['currency']}" if 'amount' in v else
                  f"{number(v['amount_range']['from'])}–{number(v['amount_range']['to'])} (registered range)" if 'amount_range' in v else
                  'amount not registered')
        result.append(Sentence(text=f"State aid award: {amount} from {v['granting_authority']}; {v['date']}.", claim_ids=[claim.id]))
    return result
