"""Audit each measured URL transition against retained, hash-verified bodies."""
import hashlib
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
from signalpost.web.html import Page
from signalpost.web.social import discover_strict

ROOT = Path('reports/r5/stage4_7')


def ancestor_tags(raw, base, target):
    class Context(HTMLParser):
        def __init__(self):
            super().__init__(); self.stack=[]; self.found=[]
        def handle_starttag(self, tag, attrs):
            attrs=dict(attrs)
            if tag=='a' and urljoin(base, attrs.get('href','')).rstrip('/')==target.rstrip('/'):
                self.found.append([literal for _,literal in self.stack])
            if tag not in {'meta','link','img','br','hr','input','source','area','base','embed','wbr'}:
                self.stack.append((tag,self.get_starttag_text()))
        def handle_endtag(self, tag):
            for i in range(len(self.stack)-1,-1,-1):
                if self.stack[i][0]==tag:
                    self.stack=self.stack[:i]; break
    parser=Context(); parser.feed(raw)
    return parser.found


def rows(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf8').splitlines()]


def urls(row):
    result = {}
    for c in row['claims']:
        if c['availability'] != 'available': continue
        if c['field'] == 'official_website': result[c['value']['final_url']] = c
        if c['field'].startswith('social_profile.'): result[c['value']['url']] = c
    return result


def main():
    settings = json.loads(Path('reports/r5/stage4/step4_6/settings.json').read_text())['resolved_config']
    stages = [('Stage 3', '.data/r5/stage3-run/envelopes.jsonl', '.data/r5/stage3-run/state'),
              ('4.6', settings['output'], settings['state_dir'])]
    for step in ('budget', 'caps', 'order', 'singlehost', 'social', 'reuse'):
        path = ROOT / ('step' + step) / 'settings.json'
        if path.exists():
            cfg = json.loads(path.read_text(encoding='utf-8-sig'))['resolved_config']
            if Path(cfg['output']).exists(): stages.append((step, cfg['output'], cfg['state_dir']))
    transitions = []
    for (old_label, old_path, old_state), (label, path, state) in zip(stages, stages[1:]):
        for old, new in zip(rows(old_path), rows(path)):
            assert old['organisation_number'] == new['organisation_number']
            for action, source, target, store in [('added', new, old, state), ('removed', old, new, old_state)]:
                for url in sorted(urls(source).keys() - urls(target).keys()):
                    c = urls(source)[url]
                    evidence = [e for e in source['evidence'] if e['id'] in c['evidence_ids']]
                    for e in evidence:
                        blob = Path(store) / 'blobs' / e['content_sha256']
                        assert hashlib.sha256(blob.read_bytes()).hexdigest() == e['content_sha256']
                        assert e['claim_span'] in blob.read_bytes().decode('utf8', errors='replace')
                    name = next(c['value'] for c in source['claims'] if c['field'] == 'identity.legal_name')
                    transitions.append(dict(step=label, comparison=old_label, action=action,
                        organisation_number=source['organisation_number'], name=name, url=url,
                        proof_tier=c['value'].get('identity_level', c['value'].get('proof_tier', 'legacy_site_link')),
                        evidence=evidence))
    contexts = []
    label, path, state = stages[-1]
    for row in rows(path):
        org = row['organisation_number']
        if org not in {'991853995', '964398003'}: continue
        name = next(c['value'] for c in row['claims'] if c['field'] == 'identity.legal_name')
        web = next((c for c in row['claims'] if c['field'] == 'official_website' and c['availability'] == 'available'), None)
        checked = row['run'].get('refresh', {}).get('website', {}).get('checked_urls', [])
        report = json.loads(Path(state).parent.joinpath('report.json').read_text())
        events = report.get('request_log', report.get('requests_log', []))
        # Evidence bodies include the accepted homepage even if no social fact survives.
        bodies = {(e['source_url'], e['content_sha256']) for e in row['evidence'] if e['source_class'] == 'company_owned'}
        for event in events:
            if event.get('url') in checked and event.get('content_sha256'):
                bodies.add((event['url'], event['content_sha256']))
        for url, sha in sorted(bodies):
            raw = Path(state).joinpath('blobs', sha).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == sha
            page = Page(raw, url)
            for link in page.links:
                if 'linkedin.com/company/' not in link.href: continue
                pos = page.raw.find(link.span)
                contexts.append(dict(organisation_number=org, name=name, source_url=url,
                    content_sha256=sha, url=link.href, anchor=link.span, anchor_text=link.text,
                    header_footer_context=link.header_footer_context,
                    group_site=bool(web and web['value'].get('other_orgnrs')),
                    accepted=link.href.rstrip('/') in discover_strict(page, name) and bool(web) and not web['value'].get('other_orgnrs'),
                    ancestor_opening_tags=ancestor_tags(page.raw,url,link.href),
                    exact_context=page.raw[max(0, pos-350):pos+len(link.span)+350]))
    (ROOT/'url_audit.json').write_text(json.dumps({'transitions':transitions,'withheld_recheck':contexts}, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    text = '# Stage 4.7 website and social URL audit\n\nEvery transition is shown, including Stage 3 to 4.6 for the two previously withheld URLs. Evidence excerpts below are verbatim; complete evidence and context are in `url_audit.json`.\n\n'
    for item in transitions:
        text += f"## {item['comparison']} to {item['step']}: {item['action']}\n\n{item['organisation_number']} — {item['name']} — {item['url']}\n\nProof tier: `{item['proof_tier']}`\n\n"
        for e in item['evidence']:
            text += f"Source: {e['source_url']} · SHA-256 `{e['content_sha256']}` · locator `{e['locator']}`\n\n```html\n{e.get('claim_span', e.get('verbatim_span', ''))}\n```\n\n"
    if not transitions: text += 'No added or removed URLs.\n\n'
    text += '## Recheck of withheld numeric LinkedIn URLs\n\n'
    for item in contexts:
        text += f"### {item['organisation_number']} — {item['name']}\n\nURL: {item['url']}\n\nSource: {item['source_url']} · SHA-256 `{item['content_sha256']}`\n\nOwn header/footer: {item['header_footer_context']}; group site: {item['group_site']}; accepted: {item['accepted']}.\n\nExact link text: `{item['anchor_text']}`\n\n```html\n{item['exact_context']}\n```\n\n"
        for ancestors in item['ancestor_opening_tags']:
            text += 'Enclosing ancestor opening tags, each verbatim from this body:\n\n```html\n'+'\n'.join(ancestors)+'\n```\n\n'
    (ROOT/'new_websites.md').write_text(text, encoding='utf8')
    print(json.dumps({'transitions':len(transitions),'contexts':len(contexts)}))


if __name__ == '__main__': main()
