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
METHOD = 'signalpost.registry_changes.v3'
MAX_EVENTS = 50
PREFIX = 'registry_change.'
DATE_LABEL = 'registry publication time (not effective date)'
CHUNK = 200
PAGE_SIZE = 1000
LOOKBACK_MONTHS = 36


def cutoff(now):
    """36 calendar months, clamping leap day to the final valid day."""
    try: return now.replace(year=now.year - 3)
    except ValueError: return now.replace(year=now.year - 3, day=28)


def coverage(since, until):
    return {'lookback_months': LOOKBACK_MONTHS, 'since': since, 'until': until,
            'date_label': 'registry publication time, not effective date',
            'unavailable_types': {'formal_announcements': {
                'state': 'not_available',
                'reason': 'The public Enhetsregisteret update APIs do not supply formal announcement text/types; kunngjoringer HTML is not fetched because robots.txt blocks it.'}},
            'scope': 'All returned registry update events for this company and current exact-parent proven subunits, newest 50; not formal announcements or unproven historical subunits.'}


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
    elif value.get('subunit_orgnr'):
        detail += ': ' + value['subunit_orgnr']
        if value.get('start_date'):
            detail += '; registered start date ' + value['start_date']
    if value.get('changed_fields') and 'changed_field' not in value:
        detail += '; changed fields: '+', '.join(item['path'] for item in value['changed_fields'])
    return detail + '. Registry publication time: ' + value['date'] + ' (not effective date).'


def permitted(claim, envelope):
    value = claim.value
    if not isinstance(value, dict) or value.get('company_orgnr') != envelope.organisation_number:
        return False
    evidence = {e.id: e for e in envelope.evidence}
    return bool(claim.evidence_ids and all(eid in evidence for eid in claim.evidence_ids)
                and any(evidence[eid].extraction_method in {METHOD,'signalpost.registry_changes.v2','signalpost.role_changes.v1'}
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
    if type(event_id) is not int or event_id < 1:
        raise SourceFailure('registry_change_invalid_id')
    try: timestamp(event['dato'])
    except (KeyError, ValueError, TypeError, AttributeError):
        raise SourceFailure('registry_change_missing_or_invalid_date') from None
    common = {'company_orgnr': org, 'event_id': event_id, 'date': event['dato'],
              'date_source': DATE_LABEL,
              'url': BASE + 'oppdateringer/' + endpoint + '?' + urlencode(
                  {'oppdateringsid': event_id, 'size': 1, 'includeChanges': 'true'})}
    kind=event.get('endringstype')
    if not isinstance(kind,str) or not kind:raise SourceFailure('registry_change_invalid_type')
    changes=event.get('endringer',[])
    if changes is None:changes=[]
    if not isinstance(changes,list):raise SourceFailure('registry_change_invalid_payload')
    fields=[]
    for change in changes:
        if not isinstance(change,dict) or not isinstance(change.get('path'),str):
            raise SourceFailure('registry_change_invalid_payload')
        op=change.get('op')
        if not isinstance(op,str):raise SourceFailure('registry_change_invalid_payload')
        if op in {'add','replace'} and 'value' not in change:raise SourceFailure('registry_change_missing_value')
        fields.append({'path':change['path'],'operation':op})
    value={**common,'event_type':kind,'changed_fields':fields,'record_orgnr':event['organisasjonsnummer'],
           'title':{'Ny':'Registry record created','Sletting':'Registry record deleted'}.get(kind,'Registry record updated')}
    proof=None
    if endpoint=='enheter':
        if event.get('organisasjonsnummer')!=org:raise SourceFailure('registry_change_wrong_company')
        if kind=='Endring':
            named=next((c for c in changes if field_label(c['path']) and c.get('op') in {'add','replace','remove'}),None)
            if named:
                value.update(title=field_label(named['path']),changed_field=named['path'],operation=named['op'])
                if named['op']!='remove':value['new_value']=named['value']
    else:
        unit=event['organisasjonsnummer']
        if not scope or unit not in scope:return missing('activity','registry_change_parent_not_proven',state='not_available')
        item,proof=scope[unit]
        if item.get('overordnetEnhet')!=org:raise SourceFailure('registry_change_wrong_parent')
        value.update(subunit_orgnr=unit,title={'Ny':'New registered workplace','Sletting':'Workplace removed'}.get(kind,'Workplace registry record updated'))
        if kind=='Ny' and item.get('oppstartsdato'):
            datetime.strptime(item['oppstartsdato'],'%Y-%m-%d');value['start_date']=item['oppstartsdato']
    # One claim per event, with distinct localized receipts for its header and
    # every supplied changed-field descriptor. No unsupported change is inferred.
    field=PREFIX+digest([endpoint,event_id])[:24]
    add(section,source,org,'activity',field,value,locator,method=METHOD)
    for attr in ['organisasjonsnummer','oppdateringsid','dato','endringstype']:
        receipt=Section();add(receipt,source,org,'activity','receipt',event[attr],locator+'/'+attr,method=METHOD)
        section.evidence.extend(receipt.evidence);section.claims[-1].evidence_ids.extend(e.id for e in receipt.evidence)
    for i,change in enumerate(changes):
        for attr in ['path','op']:
            receipt=Section();add(receipt,source,org,'activity','receipt',change[attr],locator+'/endringer/'+str(i)+'/'+attr,method=METHOD)
            section.evidence.extend(receipt.evidence);section.claims[-1].evidence_ids.extend(e.id for e in receipt.evidence)
    if proof:
        section.evidence.append(proof);section.claims[-1].evidence_ids.append(proof.id)
    if section.claims: section.state = 'available'
    return section


def significant_recent(claims):
    """Prioritize substantive events in the newest 90-day cluster; dates stay honest."""
    if not claims:return None
    newest=max(timestamp(c.value['date']) for c in claims)
    recent=[c for c in claims if (newest-timestamp(c.value['date'])).days<=90]
    def significance(c):
        v=c.value
        return (4 if v.get('event_type')=='Sletting' else
                3 if v.get('changed_field') in {'/navn','/kapital/belop'} else
                2 if v.get('event_type')=='Ny' or v.get('changed_field') else 1)
    return max(recent,key=lambda c:(significance(c),c.value['date'],c.value['event_id']))


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
            try: published = timestamp(event['dato'])
            except (KeyError, ValueError, TypeError, AttributeError):
                raise SourceFailure('registry_change_missing_or_invalid_date') from None
            if not timestamp(since) <= published <= timestamp(until):
                raise SourceFailure('registry_change_date_outside_window')
            seen.add(ident)
            yield event, response, '/_embedded/' + key + '/' + str(index)
        count += len(rows)
        if count == total: return
        page += 1


async def fetch_batch(envelopes, http, blobs, until):
    """One run-local acquisition, shared by the entire batch; errors stay explicit."""
    now = timestamp(until)
    since = cutoff(now)
    since = since.isoformat().replace('+00:00', 'Z')
    result = {org: Section(state='not_available') for org in envelopes}
    for envelope in envelopes.values():
        envelope.run.refresh['registry_activity'] = coverage(since, until)
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
    from .role_changes import collect as collect_roles
    role_sections=await collect_roles(envelopes,http,since,until)
    for org,roles in role_sections.items():
        result[org].claims.extend(roles.claims);result[org].evidence.extend(roles.evidence)
        result[org].errors.extend(roles.errors)
        if roles.state=='failed':result[org].state='failed'
        elif roles.claims and result[org].state!='failed':result[org].state='available'
        envelopes[org].run.refresh['registry_activity']['roles']={'state':roles.state,'events_returned':len(roles.claims),
            'role_type_state':'not_supplied_by_public_feed','person_names_state':'not_supplied_by_public_feed',
            'leadership_change_state':'cannot_infer_from_generic_update','errors':sorted({e.code for e in roles.errors})}
    for org, section in result.items():
        unique={c.field:c for c in section.claims}
        ordered=sorted(unique.values(),key=lambda c:(timestamp(c.value['date']),c.value['event_id'],c.field),reverse=True)
        section.claims=ordered[:MAX_EVENTS]
        refs={eid for c in section.claims for eid in c.evidence_ids}
        section.evidence=list({e.id:e for e in section.evidence if e.id in refs}.values())
        envelopes[org].run.refresh['registry_activity'].update(events_returned=len(ordered),
            events_published=len(section.claims),event_cap=MAX_EVENTS,truncated=len(ordered)>MAX_EVENTS)
        envelopes[org].run.refresh['registry_activity'].update(
            state=section.state, errors=sorted({e.code for e in section.errors}))
    return result


def cap_envelope(envelope):
    """Apply the same presentation cap after partial-refresh carry-forward."""
    claims=[c for c in envelope.claims if c.field.startswith(PREFIX) and c.availability=='available']
    unique={}
    for c in claims:
        v=c.value
        key=(v.get('event_source'),v.get('record_orgnr') or v.get('subunit_orgnr') or v['company_orgnr'],v['event_id'])
        rank=(not c.carried_forward,'changed_fields' in v)
        if key not in unique or rank>unique[key][0]:unique[key]=(rank,c)
    ordered=sorted((pair[1] for pair in unique.values()),key=lambda c:(timestamp(c.value['date']),c.value['event_id'],c.field),reverse=True)
    keep={c.field for c in ordered[:MAX_EVENTS]}
    envelope.claims=[c for c in envelope.claims if not c.field.startswith(PREFIX)]+ordered[:MAX_EVENTS]
    envelope.changes=[c for c in envelope.changes if not c.field.startswith(PREFIX) or c.field in keep]


def merge(envelope, section, website_enabled):
    """Retain existing source facts; section placeholders reflect combined status."""
    claims = [c for c in envelope.claims if c.family == 'activity' and c.field != 'activity.section']
    evidence = [e for e in envelope.evidence if any(e.id in c.evidence_ids for c in claims)]
    old_state = envelope.run.sections.get('activity')
    errors = [e for e in envelope.errors if e.section == 'activity'] if website_enabled else []
    state = 'failed' if section.state == 'failed' or (website_enabled and old_state in {'failed', 'blocked', 'ambiguous'}) else 'available' if claims or section.claims else 'not_available'
    return Section(state=state, claims=claims + section.claims, evidence=evidence + section.evidence,
                   errors=errors + section.errors)
