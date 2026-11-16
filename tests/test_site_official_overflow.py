"""Older official records defer to the local data file; none are dropped."""
from signalpost import site


def claim(i, family='inspections', date=None):
    return {'id': f'{family}{i:04d}' + '0' * 16, 'family': family, 'availability': 'available',
            'field': f'{family}.x.{i}', 'value': {'date': date or f'2026-01-{i + 1:02d}'}}


def test_newest_inline_rest_deferred_per_family():
    claims = [claim(i) for i in range(12)] + [claim(i, 'state_aid') for i in range(3)]
    out = site.official_overflow(claims, 8)
    assert out == {c['id'] for c in claims[:4]}  # four oldest inspections only
    assert site.official_overflow(claims, 0) == {c['id'] for c in claims}


def test_non_official_families_never_deferred():
    assert not site.official_overflow([claim(i, 'activity') for i in range(30)], 0)
