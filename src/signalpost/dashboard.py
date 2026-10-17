"""Dataset-wide analytics from verified envelope data."""

from collections import defaultdict
from pathlib import Path
import json
from typing import Any, Dict, List, Optional


def analyze_envelopes(envelopes_path: Path) -> Dict[str, Any]:
    """
    Analyze all envelopes and compute dataset-wide statistics.

    Returns analytics dict with:
    - total_companies: count of input envelopes
    - complete_count: envelopes with status='complete'
    - error_count: envelopes with status='submission_error'
    - by_industry: count by NACE industry code
    - coverage: source coverage percentages
    - subunit_footprint: distribution of subunit counts
    """

    if not envelopes_path.exists():
        return {}

    total = 0
    complete = 0
    error = 0
    industries = defaultdict(int)
    coverage = {
        'identity': 0,
        'accounts': 0,
        'roles': 0,
        'subunits': 0,
        'websites': 0,
        'hiring': 0,
        'activity': 0,
    }
    subunit_counts = defaultdict(int)

    with open(envelopes_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                envelope = json.loads(line)
            except json.JSONDecodeError:
                continue

            total += 1
            status = envelope.get('status', '')

            if status == 'complete':
                complete += 1
            elif status == 'submission_error':
                error += 1

            # Track by industry
            if 'company' in envelope:
                company = envelope['company']
                if company.get('industry', {}).get('code'):
                    industries[company['industry']['code']] += 1

            # Track source coverage
            sources = envelope.get('sources', {})
            if sources.get('identity', {}).get('state') in ['complete', 'partial']:
                coverage['identity'] += 1
            if sources.get('accounts', {}).get('state') in ['complete', 'partial']:
                coverage['accounts'] += 1
            if sources.get('roles', {}).get('state') in ['complete', 'partial']:
                coverage['roles'] += 1
            if sources.get('subunits', {}).get('state') in ['complete', 'partial']:
                coverage['subunits'] += 1
            if sources.get('websites', {}).get('state') in ['complete', 'partial']:
                coverage['websites'] += 1
            if sources.get('hiring', {}).get('state') in ['complete', 'partial']:
                coverage['hiring'] += 1
            if sources.get('public_activity', {}).get('state') in ['complete', 'partial']:
                coverage['activity'] += 1

            # Track subunit footprint (explicit empty-collection claim, not employee count)
            if 'subunits' in sources:
                subunit_source = sources['subunits']
                if subunit_source.get('state') == 'complete':
                    # Count explicit subunit records
                    subunit_records = subunit_source.get('subunits', [])
                    subunit_count = len(subunit_records) if subunit_records else 0
                    subunit_counts[subunit_count] += 1
                elif subunit_source.get('state') == 'not_available':
                    # Not available = unknown, not zero
                    subunit_counts['unknown'] += 1

    # Convert percentages
    if total > 0:
        coverage = {k: round(100 * v / total, 1) for k, v in coverage.items()}

    # Convert subunit counts to percentages
    subunit_pct = {}
    if total > 0:
        for k, v in subunit_counts.items():
            subunit_pct[str(k)] = round(100 * v / total, 1)

    return {
        'total_companies': total,
        'complete': complete,
        'errors': error,
        'coverage_percent': coverage,
        'industries_top': dict(sorted(industries.items(), key=lambda x: x[1], reverse=True)[:20]),
        'subunit_footprint': subunit_pct,
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        envelopes = Path(sys.argv[1])
        stats = analyze_envelopes(envelopes)
        print(json.dumps(stats, indent=2))
