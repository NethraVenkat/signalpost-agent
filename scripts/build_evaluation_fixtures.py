"""Generate synthetic HTTP fixtures; never factual accuracy evidence."""
import base64
import hashlib
import json
from pathlib import Path


def main():
    root = Path('tests/fixtures/external_integration')
    blobs = root / 'blobs'
    blobs.mkdir(parents=True, exist_ok=True)
    fixtures = []
    def add(url, body, status=200, kind='application/json'):
        raw = (json.dumps(body, ensure_ascii=False) if isinstance(body, (dict, list)) else body).encode()
        sha = hashlib.sha256(raw).hexdigest()
        (blobs / sha).write_bytes(raw)
        fixtures.append(dict(url=url, method='GET', status_code=status,
            headers={'content-type': kind}, content_sha256=sha, blob_file=sha,
            metadata_complete=True, repeatable=True))
    companies = [('923609016', 'Zephyrsynthetic AS', 'zephyrsynthetic.no'),
                 ('988258229', 'Quartzsynthetic AS', 'quartzsynthetic.no'),
                 ('999592236', 'Ambersynthetic AS', 'ambersynthetic.no')]
    base = 'https://data.brreg.no'
    for org, name, host in companies:
        add(f'{base}/enhetsregisteret/api/enheter/{org}', {
            'organisasjonsnummer': org, 'navn': name,
            'organisasjonsform': {'kode': 'AS', 'beskrivelse': 'Aksjeselskap'},
            'hjemmeside': f'https://{host}', 'registreringsdatoEnhetsregisteret': '2020-01-01',
            'forretningsadresse': {'adresse': ['Example gate 1'], 'postnummer': '0001', 'kommune': 'OSLO'}})
        add(f'{base}/enhetsregisteret/api/enheter/{org}/roller', {'organisasjonsnummer':org, 'rollegrupper':[]})
        units = [{'organisasjonsnummer':'993578843','overordnetEnhet':org,'navn':'Zephyrsynthetic Branch'}] if org == '923609016' else []
        add(f'{base}/enhetsregisteret/api/underenheter?overordnetEnhet={org}&size=1000&page=0',
            {'_embedded':{'underenheter':units},'page':{'totalPages':1}})
        add(f'{base}/regnskapsregisteret/regnskap/{org}', [], 503 if org == '999592236' else 200)
        add(f'https://{host}/robots.txt', 'User-agent: *\nAllow: /', kind='text/plain')
        if org == '923609016':
            html = f'''<html><head><title>{name}</title><meta name="description" content="We develop synthetic research software for fixture testing."><link rel="alternate" type="application/rss+xml" href="/feed.xml"></head><body><h1>{name}</h1><p>Org.nr. {org}</p><a href="mailto:hello@{host}">Email</a><a href="https://www.linkedin.com/company/zephyrsynthetic">LinkedIn</a></body></html>'''
        elif org == '988258229':
            html = '<html><title>Unrelated directory</title><body><h1>Our partners</h1><p>Quartzsynthetic AS Org.nr. 988258229</p><p>Other AS Org.nr. 999592236</p></body></html>'
        else:
            html = 'Source unavailable'
        if org == '923609016':
            html = html.replace('<body>', '<body><section class="company">').replace('</body>',
                '</section><section class="company"><h2>Sibling AS</h2><p>Org.nr. 988258229</p>'
                '<a href="mailto:sibling@zephyrsynthetic.no">Sibling email</a>'
                '<a href="https://www.linkedin.com/company/sibling-synthetic">Sibling LinkedIn</a>'
                '</section><section class="company"><h2>Other AS</h2><p>Org.nr. 999592236</p></section></body>')
        html = html.replace('<body>', '<body><footer>').replace('</body>', '<p>' + 'Synthetic fixture content for testing company attribution and source extraction. ' * 8 + '</p></footer></body>')
        add(f'https://{host}/', html, 503 if org == '999592236' else 200, 'text/html')
        add(f'https://{host}/sitemap.xml', '', 404, 'application/xml')
        for path in ['/feed.xml', '/rss.xml']:
            if host != 'zephyrsynthetic.no':
                add(f'https://{host}{path}', '', 404, 'application/xml')
    add('https://zephyrsynthetic.no/feed.xml', '<rss><channel><item><title>Synthetic launch</title><link>https://zephyrsynthetic.no/news/launch</link><pubDate>Wed, 14 Oct 2026 12:00:00 GMT</pubDate></item></channel></rss>', kind='application/rss+xml')
    nav = 'https://pam-stilling-feed.nav.no'
    token = '.'.join(base64.urlsafe_b64encode(x).decode().rstrip('=') for x in [b'{"alg":"HS256"}', b'{"sub":"synthetic-fixture"}', b'synthetic-signature'])
    add(nav+'/api/publicToken', token, kind='text/plain')
    items=[]
    for i, employer in enumerate(['923609016', '993578843', None], 1):
        uuid=f'00000000-0000-4000-8000-{i:012d}'
        items.append({'id':uuid,'url':'/api/v1/feedentry/'+uuid,'date_modified':'2026-10-14T12:00:00Z','_feed_entry':{'uuid':uuid,'status':'ACTIVE','businessName':'Zephyrsynthetic AS'}})
        add(nav+'/api/v1/feedentry/'+uuid, {'uuid':uuid,'status':'ACTIVE','ad_content':{'uuid':uuid,'title':'Synthetic vacancy','published':'2026-10-13T12:00:00Z','expires':'2026-11-13T12:00:00Z','employer':{'name':'Zephyrsynthetic AS',**({'orgnr':employer} if employer else {})}}})
    add(nav+'/api/v1/feed', {'items':items,'next_url':None,'next_id':None})
    (root/'manifest.json').write_text(json.dumps({'description':'SYNTHETIC: no real company facts; fixed observation 2026-10-15T10:00:00Z','fixtures':fixtures}, indent=2), encoding='utf-8')
    (root/'batch.txt').write_text('923609016\n988258229\n999592236\n923609016\n123456789\n', encoding='utf-8')


if __name__ == '__main__':
    main()
