"""S4 Finanstilsynet registry: exact organisationNumber; own licences vs agent registrations kept distinct."""
import asyncio
import copy
import json
from datetime import datetime, timezone

import pytest

from signalpost.sources import exact_official as eo
from signalpost.sources.http import Response

ORG = '991853995'
NOW = datetime(2026, 11, 16, tzinfo=timezone.utc)
ENTITY = {'legalEntityId': 106427, 'legalEntityType': 'Company', 'organisationNumber': ORG, 'name': 'EXAMPLE SPAREBANK ASA',
          'licences': [
              {'licensedEntity': {'legalEntityId': 106427, 'legalEntityName': 'EXAMPLE SPAREBANK ASA'}, 'serviceProviderType': 'Licensed',
               'licenceType': {'code': 'BANK', 'name': {'norwegian': 'Bank', 'english': 'Bank'}}, 'registeredDate': '2010-01-04T00:00:00'},
              {'licensedEntity': {'legalEntityId': 99172, 'legalEntityName': 'FREMTIND FORSIKRING AS'}, 'serviceProviderType': 'Agent',
               'licenceType': {'code': 'SKADEFORSI', 'name': {'norwegian': 'Skadeforsikringsforetak', 'english': 'Non-life insurance company'}},
               'registeredDate': '2024-12-02T00:00:00'},
              {'licensedEntity': {'legalEntityId': 106427, 'legalEntityName': 'EXAMPLE SPAREBANK ASA'}, 'serviceProviderType': 'Branch',
               'licenceType': {'code': 'BANK', 'name': {'english': 'Bank'}}},  # unsupported provider type abstains
          ]}


def test_own_licence_and_agent_registration_are_distinct_and_exact():
    values = {key: value for key, value, _ in eo.licence_values(ENTITY, ORG)}
    assert values['BANK.self'] == {'company_orgnr': ORG, 'role': 'licensed', 'licence_code': 'BANK', 'licence_name': 'Bank',
                                   'registered_date': '2010-01-04', 'registered_date_source': 'registeredDate as published by Finanstilsynet',
                                   'registry_entity_id': 106427, 'label': 'Finanstilsynet licence/registration'}
    agent = values['SKADEFORSI.agent.99172']
    assert agent['role'] == 'agent' and agent['principal'] == 'FREMTIND FORSIKRING AS' and agent['licence_code'] == 'SKADEFORSI'
    assert len(values) == 2


@pytest.mark.parametrize('change', [{'organisationNumber': '974760673'}, {'legalEntityType': 'Person'}, {'legalEntityId': None}])
def test_wrong_entity_or_person_records_abstain(change):
    assert eo.licence_values({**ENTITY, **change}, ORG) == []


def test_unparseable_registered_date_is_omitted_not_invented():
    entity = copy.deepcopy(ENTITY)
    entity['licences'][0]['registeredDate'] = 'unknown'
    value = next(v for k, v, _ in eo.licence_values(entity, ORG) if k == 'BANK.self')
    assert 'registered_date' not in value


class FakeHttp:
    def __init__(self, search, entity=None):
        self.search, self.entity, self.calls = search, entity, []

    async def request(self, url, org, payload=None, headers=None):
        self.calls.append(url)
        body = self.search if 'search' in url else self.entity
        return Response(json.dumps(body).encode(), 200, url, '2026-11-16T09:00:00Z', 'b' * 64)


def hit(org=ORG, entity_id=106427, kind='Company'):
    return {'legalEntityId': entity_id, 'legalEntityType': kind, 'organisationNumber': org, 'name': 'X'}


def test_exact_search_then_record_fetch():
    http = FakeHttp({'total': 1, 'legalEntities': [hit()]}, {'legalEntities': [ENTITY]})
    section = asyncio.run(eo.licences(ORG, http, NOW))
    assert http.calls == [eo.ft_search_url(ORG), eo.ft_entity_url(106427)]
    assert sorted(c.field for c in section.claims) == ['licences.BANK.self', 'licences.SKADEFORSI.agent.99172']


def test_no_exact_hit_is_explicit_none_and_ambiguous_ids_abstain():
    none = asyncio.run(eo.licences(ORG, FakeHttp({'total': 1, 'legalEntities': [hit(org='974760673')]}), NOW))
    assert none.state == 'not_available' and none.claims[0].field == 'licences.registrations'
    amb = asyncio.run(eo.licences(ORG, FakeHttp({'total': 2, 'legalEntities': [hit(), hit(entity_id=5)]}), NOW))
    assert amb.state == 'ambiguous' and not amb.claims


def test_truncated_search_fails_explicitly():
    from signalpost.budget import SourceFailure
    with pytest.raises(SourceFailure, match='licences_search_incomplete'):
        asyncio.run(eo.licences(ORG, FakeHttp({'total': 60, 'legalEntities': [hit()] * 50}), NOW))


def test_verifier_rejects_forged_licence():
    from scripts.verify_output import verify_exact_official
    http = FakeHttp({'total': 1, 'legalEntities': [hit()]}, {'legalEntities': [ENTITY]})
    section = asyncio.run(eo.licences(ORG, http, NOW))
    body = json.dumps({'legalEntities': [ENTITY]})
    claims = [c.model_dump(mode='json') for c in section.claims]
    evidence = {e.id: {**e.model_dump(mode='json'), 'source_url': eo.ft_entity_url(106427)} for e in section.evidence}
    row = {'organisation_number': ORG}
    assert verify_exact_official(row, {'claims': claims}, evidence, lambda sha: body) == 2
    claims[0]['value']['role'] = 'licensed' if claims[0]['value']['role'] == 'agent' else 'agent'
    with pytest.raises(AssertionError):
        verify_exact_official(row, {'claims': claims}, evidence, lambda sha: body)
