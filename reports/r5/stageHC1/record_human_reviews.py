"""Pin the reviewer's supplied verdicts to the saved P2 and P3g social claims."""

import hashlib
import json
from pathlib import Path

from signalpost.portable_paths import expand, portable
from signalpost.sources.text import decode_body

DEST = Path(__file__).resolve().parent
ROOT = DEST.parents[2]
SAMPLES = {'P2': ('scale500', 20261118), 'P3g': ('stageP3/P3g', 20261120)}
REVIEWER = 'Nethra Venkat'
DATE = '2026-11-18'
METHOD = 'Independent web hand-check supplied by the reviewer in conversation'

CORRECT = {
    ('918811370', 'https://www.facebook.com/totenforsikring'),
    ('933831922', 'http://www.youtube.com/@ShiftSecurityAS'),
    ('933831922', 'https://www.youtube.com/@ShiftSecurityAS'),
    ('971050756', 'https://www.linkedin.com/company/petroonline-as'),
    ('912503259', 'https://www.facebook.com/officeaid.no'),
    ('966261218', 'https://www.facebook.com/bomlofhs'),
    ('966261218', 'https://www.youtube.com/channel/UCKY6h9lnepk7TGa-pvYSDdw'),
    ('970991786', 'https://www.facebook.com/vitec.agrando'),
    ('985256055', 'https://www.facebook.com/FrameworksArendal'),
    ('985256055', 'https://www.linkedin.com/company/frameworks-as'),
    ('986902651', 'https://www.facebook.com/tinnheiabil'),
    ('991323848', 'https://twitter.com/TrollheimAS'),
    ('994479865', 'https://twitter.com/IAM_Identum'),
    ('994479865', 'https://www.facebook.com/identum.no'),
}
WRONG = {
    ('927525399', 'https://www.facebook.com/arenaskog'): (
        'The profile belongs to the Swedish Arena Skog project. WoodWorks visibly links facebook.com/woodworkscluster.',
        ['https://arenaskog.se/om-oss/', 'https://woodworkscluster.no/'],
    ),
    ('991323848', 'https://facebook.com/TrollheimAS'): (
        'The profile belongs to Trollheim Kurs og Kompetanse AS (924191627), which shares trollheim.no.',
        ['https://virksomhet.brreg.no/nb/oppslag/enheter/924191627', 'https://trollheim.no/kontakt/'],
    ),
}
UNSURE = {
    ('922569738', 'https://www.instagram.com/snuompsykiskhelse'),
    ('927361426', 'https://www.facebook.com/Lterrasseno-101890795424991'),
    ('912503259', 'https://www.instagram.com/officeaid.no'),
    ('916364806', 'https://www.facebook.com/ttexpressas'),
    ('966261218', 'https://www.instagram.com/bomlofhs'),
    ('966261218', 'https://www.tiktok.com/@bomlofhs'),
    ('985256055', 'https://www.instagram.com/frameworks.no'),
    ('990825076', 'https://www.instagram.com/peculium_as'),
    ('991323848', 'https://www.instagram.com/trollheimas'),
    ('994479865', 'https://www.instagram.com/iam_identum'),
}


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def value_sha256(value):
    # Same canonical value encoding as scripts/precision_ledger.py.
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(portable(value), indent=2, ensure_ascii=False) + '\n',
                    encoding='utf8', newline='\n')


def read(path):
    return json.loads(path.read_text(encoding='utf8'))


def samples(kind='social'):
    included = (lambda field: field == 'official_website') if kind == 'website' else (
        lambda field: field.startswith('social_profile.'))
    for label, (location, seed) in SAMPLES.items():
        folder = ROOT / 'reports/r5' / location
        inventory = read(folder / 'urls.json')
        work = Path(expand(read(folder / 'run.json')['cwd']))
        envelopes = work / 'envelopes.jsonl'
        output_hash = sha256(envelopes)
        assert output_hash == inventory['output_sha256'], label
        pins = {
            'seed': seed,
            'input_sha256': sha256(folder / 'companies500.jsonl'),
            'envelopes_sha256': output_hash,
            'url_inventory_sha256': sha256(folder / 'urls.json'),
            'url_inventory': (folder / 'urls.json').relative_to(ROOT).as_posix(),
        }
        with envelopes.open(encoding='utf8') as stream:
            rows = {}
            for line in stream:
                row = json.loads(line)
                claims = {c['id']: c for c in row['claims']
                          if included(c['field']) and c['availability'] == 'available'}
                if claims:
                    rows[row['organisation_number']] = (row, claims)
        yield label, folder, work, pins, inventory, rows


def main():
    inputs, reviews, matched = {}, [], set()
    for label, _, work, pins, inventory, rows in samples():
        inputs[label] = pins
        for item in inventory['records']:
            if item['kind'] != 'social' or item['automated_verdict'] == 'correct':
                continue
            org, url = item['organisation_number'], item['url']
            key = org, url
            assert key not in matched, (label, key)
            matched.add(key)
            source_urls = []
            if key in WRONG:
                verdict = 'wrong'
                note, source_urls = WRONG[key]
            elif key in CORRECT:
                verdict = 'correct'
                note = 'Confirmed by the reviewer.'
                if org == '971050756':
                    note = 'PETRO ONLINE AS is a Brønnøysund-recorded former name of this exact organisation.'
                    source_urls = ['https://virksomhet.brreg.no/nb/oppslag/enheter/971050756']
            elif key in UNSURE:
                verdict, note = 'unsure', 'No definitive human verdict. Keep the original automated label.'
            else:
                raise ValueError(f'Flagged social claim has no supplied hand-check: {label} {key}')
            _, claims = rows[org]
            claim = claims[item['claim_id']]
            assert claim['field'] == item['field'] and claim['value']['url'] == url
            assert claim['value']['proof_tier'] == item['proof_tier']
            for receipt in item['receipts']:
                digest = receipt['content_sha256']
                raw = (work / 'state/blobs' / digest).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == digest
                assert receipt['claim_span'] in decode_body(raw)
            reviews.append({
                'sample': label, 'seed': pins['seed'], 'sample_sha256': pins['input_sha256'],
                'envelopes_sha256': pins['envelopes_sha256'], 'organisation_number': org,
                'company': item['company'], 'kind': 'social', 'url': url, 'field': claim['field'],
                'claim_id': claim['id'], 'value_sha256': value_sha256(claim['value']),
                'verdict': verdict, 'human_verified': verdict != 'unsure',
                'reviewer': REVIEWER, 'review_date': DATE, 'method': METHOD,
                'automated_verdict': item['automated_verdict'], 'automated_reasons': item['reasons'],
                'proof_tier': item['proof_tier'], 'note': note, 'review_source_urls': source_urls,
                'receipts': item['receipts'],
            })
    assert matched == CORRECT | WRONG.keys() | UNSURE
    counts = {verdict: sum(r['verdict'] == verdict for r in reviews)
              for verdict in ('correct', 'wrong', 'unsure')}
    result = {'reviewer': REVIEWER, 'review_date': DATE, 'method': METHOD, 'inputs': inputs,
              'counts': counts, 'reviews': reviews}
    save(DEST / 'human_reviews.json', result)
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
