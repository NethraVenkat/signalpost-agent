"""Development-only SSB snapshot builder; never imported by the runtime.

Usage: python scripts/download_nace.py --date YYYY-MM-DD
"""
import argparse
import json
from pathlib import Path
import httpx


def build_table(english, norwegian, year, version_id, download_date):
    names = {item['code']: item['name'] for item in norwegian['classificationItems']}
    base = f'https://data.ssb.no/api/klass/v1/versions/{version_id}'
    return {
        'standard': f'SN{year}', 'version_id': version_id, 'download_date': download_date,
        'source_url': base + '?language=en', 'norwegian_source_url': base + '?language=nb',
        'valid_from': english['validFrom'], 'last_modified': english['lastModified'],
        'derived_from': english.get('derivedFrom'),
        'classes': {item['code']: item['name'] for item in english['classificationItems'] if item['level'] == '4'},
        'titles': {item['code']: item['name'] for item in english['classificationItems'] if item['level'] in ('4', '5')},
        'subclasses': {item['code']: {'parent': item['parentCode'], 'registered_title': names.get(item['code'], '')}
                       for item in english['classificationItems'] if item['level'] == '5'},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', required=True, help='Actual development download date, YYYY-MM-DD')
    args = parser.parse_args()
    from datetime import date
    date.fromisoformat(args.date)
    target = Path(__file__).resolve().parents[1] / 'src/signalpost/synthesis/data'
    pending = {}
    versions = []
    with httpx.Client(timeout=30, follow_redirects=False) as client:
        for year, version_id in ((2025, 3218), (2007, 30)):
            responses = {}
            for language in ('en', 'nb'):
                url = f'https://data.ssb.no/api/klass/v1/versions/{version_id}?language={language}'
                response = client.get(url)
                response.raise_for_status()
                responses[language] = response.json()
                assert responses[language]['id'] == version_id
            pending[f'ssb-sn{year}-en-{args.date}.json'] = responses['en']
            versions.append(build_table(responses['en'], responses['nb'], year, version_id, args.date))
    # Publish only after both official versions succeed. No partial fallback table.
    pending[f'nace-klass-{args.date}.json'] = {'versions': versions}
    target.mkdir(exist_ok=True)
    for filename, data in pending.items():
        (target / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


if __name__ == '__main__':
    main()
