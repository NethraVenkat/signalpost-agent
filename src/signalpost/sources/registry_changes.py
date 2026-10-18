"""Run-local, bounded BRREG change feeds; only explicitly named changes publish."""
import asyncio
import hashlib
import json
from datetime import datetime, timezone
from urllib.parse import urlencode

from ..budget import SourceFailure
from ..models.evidence import digest
from ..workers import offload
from .extract import Section, add, missing, response_source

BASE = 'https://data.brreg.no/enhetsregisteret/api/'
METHOD = 'registry change feed'
PREFIX = 'registry_change.'
DATE_LABEL = 'registry publication time (not effective date)'
CHUNK = 200
PAGE_SIZE = 1000


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamp lacks timezone')
    return parsed.astimezone(timezone.utc)


def field_label(path):
    if path == '/navn': return 'Registered name changed'
    if path == '/kapital/belop': return 'Registered share capital changed'
    if path == '/forretningsadresse' or path.startswith('/forretningsadresse/'):
        return 'Registered business address changed'
    if path == '/postadresse' or path.startswith('/postadresse/'):
        return 'Registered postal address changed'
    return None


def sentence(value):
    detail = value['title']
    if 'changed_field' in value:
        detail += ' (' + value['changed_field'] + ')'
        if 'new_value' in value:
            detail += ': ' + json.dumps(value['new_value'], ensure_ascii=False, sort_keys=True)
        else:
            detail += ': field removed'
    else:
        detail += ': ' + value['subunit_orgnr']
        if value.get('start_date'):
            detail += '; registered start date ' + value['start_date']
    return detail + '. Registry publication time: ' + value['date'] + ' (not effective date).'


def permitted(claim, envelope):
    value = claim.value
    if not isinstance(value, dict) or value.get('company_orgnr') != envelope.organisation_number:
        return False
    evidence = {e.id: e for e in envelope.evidence}
    return bool(claim.evidence_ids and all(eid in evidence for eid in claim.evidence_ids)
                and any(evidence[eid].extraction_method == METHOD
                        and evidence[eid].source_url.startswith(BASE + 'oppdateringer/')
                        for eid in claim.evidence_ids))


def subunit_scope(envelope, blobs):
    """Only current, exact-parent records with retained, hash-checked source bytes.

    Historical or deleted units absent from this verified scope are abstentions.
    A parent number is never passed off as a subunit number.
    """
    result = {}
    records = {e.id: e for e in envelope.evidence}
    bodies = {}
    for claim in envelope.claims:
        if not claim.field.startswith('subunits.unit.') or claim.availability != 'available' or claim.carried_forward:
            continue
        unit = claim.value['organisation_number']
        for eid in claim.evidence_ids:
            evidence = records[eid]
            if not evidence.source_url.startswith(BASE + 'underenheter?'):
                continue
            sha = evidence.content_sha256
            if sha not in bodies:
                body = blobs.read(sha)
                if body is None or hashlib.sha256(body).hexdigest() != sha:
                    raise SourceFailure('registry_change_scope_unavailable')
                bodies[sha] = json.loads(body).get('_embedded', {}).get('underenheter', [])
            for item in bodies[sha]:
                if item.get('organisasjonsnummer') == unit:
                    if item.get('overordnetEnhet') != envelope.organisation_number:
                        raise SourceFailure('registry_change_wrong_parent')
                    result[unit] = (item, evidence)
    return result


def extract(event, response, locator, org, endpoint, scope=None):
    section = Section(state='not_available')
    source = response_source(response)
    event_id = event['oppdateringsid']
    common = {'company_orgnr': org, 'event_id': event_id, 'date': event['dato'],
              'date_source': DATE_LABEL,
              'url': BASE + 'oppdateringer/' + endpoint + '?' + urlencode(
                  {'oppdateringsid': event_id, 'size': 1, 'includeChanges': 'true'})}
    if endpoint == 'enheter':
        if event.get('organisasjonsnummer') != org:
            raise SourceFailure('registry_change_wrong_company')
        if event.get('endringstype') != 'Endring': return section
        changes = event.get('endringer', [])
        if not isinstance(changes, list): raise SourceFailure('registry_change_invalid_payload')
        for index, change in enumerate(changes):
            path = change.get('path', '')
            label = field_label(path)
            if not label or change.get('op') not in {'add', 'replace', 'remove'}: continue
            if change['op'] != 'remove' and 'value' not in change:
                raise SourceFailure('registry_change_missing_value')
            value = {**common, 'title': label, 'changed_field': path, 'operation': change['op']}
            if change['op'] != 'remove': value['new_value'] = change['value']
            add(section, source, org, 'activity', PREFIX + digest(['entity', event_id, index])[:24],
                value, locator + '/endringer/' + str(index), method=METHOD)
    elif event.get('endringstype') in {'Ny', 'Sletting'}:
        unit = event['organisasjonsnummer']
        item, proof = scope[unit]
        if item.get('overordnetEnhet') != org:
            raise SourceFailure('registry_change_wrong_parent')
        value = {**common, 'title': 'New registered workplace' if event['endringstype'] == 'Ny' else 'Workplace removed',
                 'subunit_orgnr': unit, 'event_type': event['endringstype']}
        if event['endringstype'] == 'Ny' and item.get('oppstartsdato'):
            # This is the separately reported start date, never the event date.
            datetime.strptime(item['oppstartsdato'], '%Y-%m-%d')
            value['start_date'] = item['oppstartsdato']
        add(section, source, org, 'activity', PREFIX + digest(['subunit', event_id])[:24],
            value, locator, method=METHOD)
        section.evidence.append(proof)
        section.claims[-1].evidence_ids.append(proof.id)
    if section.claims: section.state = 'available'
    return section


async def pages(http, endpoint, numbers, since, until):
    """Construct every page locally; never follow untrusted next links or truncate."""
    # BRREG accepts exactly millisecond precision in UTC, not Python's default
    # microseconds. Validate events against the same bounds sent to the API.
    since = timestamp(since).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    until = timestamp(until).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    key = 'oppdaterteEnheter' if endpoint == 'enheter' else 'oppdaterteUnderenheter'
    page, total, seen, count = 0, None, set(), 0
    while True:
        params = {'organisasjonsnummer': ','.join(numbers), 'dato': since,
                  'updatedBefore': until, 'includeChanges': 'true', 'size': PAGE_SIZE,
                  'sort': 'id,ASC', 'page': page}
        response = await http.get(BASE + 'oppdateringer/' + endpoint + '?' + urlencode(params), '__registry_changes__')
        if response.status != 200: raise SourceFailure('registry_change_http_' + str(response.status))
        data = json.loads(response.body)
        paging = data['page']
        rows = data.get('_embedded', {}).get(key, [])
        reported = paging['totalElements']
        if (not isinstance(rows, list) or type(reported) is not int or reported < 0
                or paging['number'] != page or paging['size'] != PAGE_SIZE
                or paging['totalPages'] != (reported + PAGE_SIZE - 1) // PAGE_SIZE
                or (total is not None and total != reported)):
            raise SourceFailure('registry_change_pagination_invalid')
        total = reported
        if len(rows) != min(PAGE_SIZE, total - count):
            raise SourceFailure('registry_change_pagination_incomplete')
        for index, event in enumerate(rows):
            ident = event['oppdateringsid']
            if type(ident) is not int or ident in seen or (seen and ident <= max(seen)):
                raise SourceFailure('registry_change_pagination_repeated')
            if event['organisasjonsnummer'] not in numbers:
                raise SourceFailure('registry_change_wrong_company')
            if not timestamp(since) <= timestamp(event['dato']) <= timestamp(until):
                raise SourceFailure('registry_change_date_outside_window')
            seen.add(ident)
            yield event, response, '/_embedded/' + key + '/' + str(index)
        count += len(rows)
        if count == total: return
        page += 1


async def fetch_batch(envelopes, http, blobs, until):
    """One run-local acquisition, shared by the entire batch; errors stay explicit."""
    now = timestamp(until)
    try: since = now.replace(year=now.year - 2)
    except ValueError: since = now.replace(year=now.year - 2, day=28)
    since = since.isoformat().replace('+00:00', 'Z')
    result = {org: Section(state='not_available') for org in envelopes}
    scopes, owners = {}, {}
    for org, envelope in envelopes.items():
        try:
            if envelope.run.sections.get('subunits') not in {'available', 'not_available'}:
                raise SourceFailure('registry_change_scope_incomplete')
            scopes[org] = await offload(subunit_scope, envelope, blobs)
            for unit in scopes[org]:
                if unit in owners and owners[unit] != org:
                    raise SourceFailure('registry_change_conflicting_parent')
                owners[unit] = org
        except (SourceFailure, ValueError, KeyError, TypeError) as exc:
            result[org] = missing('activity', getattr(exc, 'code', 'registry_change_scope_invalid'))
    for endpoint, numbers in [('enheter', sorted(envelopes)), ('underenheter', sorted(owners))]:
        for start in range(0, len(numbers), CHUNK):
            chunk = numbers[start:start + CHUNK]
            affected = set(chunk) if endpoint == 'enheter' else {owners[n] for n in chunk}
            try:
                async for event, response, locator in pages(http, endpoint, chunk, since, until):
                    org = event['organisasjonsnummer'] if endpoint == 'enheter' else owners[event['organisasjonsnummer']]
                    section = await offload(extract, event, response, locator, org, endpoint, scopes.get(org))
                    result[org].claims.extend(section.claims)
                    result[org].evidence.extend(section.evidence)
                    if section.claims and result[org].state != 'failed': result[org].state = 'available'
            except asyncio.CancelledError:
                # Caller marks every unfinished activity failed on cancellation.
                raise
            except Exception as exc:
                code = getattr(exc, 'code', 'registry_change_invalid_payload')
                for org in affected:
                    result[org].state = 'failed'
                    result[org].errors.extend(missing('activity', code).errors)
    return result


def merge(envelope, section, website_enabled):
    """Retain existing source facts; section placeholders reflect combined status."""
    claims = [c for c in envelope.claims if c.family == 'activity' and c.field != 'activity.section']
    evidence = [e for e in envelope.evidence if any(e.id in c.evidence_ids for c in claims)]
    old_state = envelope.run.sections.get('activity')
    errors = [e for e in envelope.errors if e.section == 'activity'] if website_enabled else []
    state = 'failed' if section.state == 'failed' or (website_enabled and old_state in {'failed', 'blocked', 'ambiguous'}) else 'available' if claims or section.claims else 'not_available'
    return Section(state=state, claims=claims + section.claims, evidence=evidence + section.evidence,
                   errors=errors + section.errors)
