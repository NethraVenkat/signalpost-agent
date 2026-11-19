"""Confirm a sustained identity-host outage before abandoning a live batch."""
import asyncio
import time

from ..budget import SourceFailure
from . import brreg_enhet
from .official_resilience import DNS_FAILURES

SAMPLE_SIZE = 25
RETRY_SIZE = 3
RECOVERY_WAIT_SECONDS = 15.0
NETWORK_ERRORS = DNS_FAILURES | {'network_error', 'timeout'}


async def _wait(seconds):
    await asyncio.sleep(seconds)


async def check(orgs, http):
    sample = list(orgs)[:SAMPLE_SIZE]
    result = {'state': 'not_applicable', 'host': 'data.brreg.no',
              'sample_size': len(sample), 'initial': [], 'retries': [], 'wait_seconds': 0}
    identities = {}
    if len(sample) < SAMPLE_SIZE:
        result['reason'] = 'Fewer than 25 live identity lookups required'
        return result, identities

    async def lookup(org, phase):
        item = {'organisation_number': org}
        try:
            response = await http._get(brreg_enhet.BASE + org, org, attempts=1)
            item.update(state='reachable', status=response.status)
            # Use the normal exact-company extractor; a response is not identity proof.
            from .extract import decode, response_source
            data, error = decode(response, 'identity')
            if error is None:
                from ..workers import offload
                identities[org] = await offload(brreg_enhet.extract, org, data, response_source(response))
        except SourceFailure as exc:
            item.update(state='network_error' if exc.code in NETWORK_ERRORS else 'failed', reason=exc.code)
        except Exception as exc:
            item.update(state='failed', reason=type(exc).__name__)
        result[phase].append(item)

    await asyncio.gather(*(lookup(org, 'initial') for org in sample))
    result['state'] = 'continue'
    if not all(item['state'] == 'network_error' for item in result['initial']):
        return result, identities
    if time.monotonic() + RECOVERY_WAIT_SECONDS >= http.budget.deadline:
        result.update(state='budget_exhausted', reason='Insufficient budget to confirm outage; no unreachable-host conclusion')
        return result, identities
    result['wait_seconds'] = RECOVERY_WAIT_SECONDS
    await _wait(RECOVERY_WAIT_SECONDS)
    await asyncio.gather(*(lookup(org, 'retries') for org in sample[:RETRY_SIZE]))
    if all(item['state'] == 'network_error' for item in result['retries']):
        result.update(state='aborted', reason='First 25 live identity lookups and all three recovery checks failed with network errors')
    return result, identities
