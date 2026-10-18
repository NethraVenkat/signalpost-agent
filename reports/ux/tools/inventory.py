"""Measure every generated site file and its synchronous file:// dependencies."""
import json
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / 'sample/site'
OUT = Path(__file__).resolve().parents[1] / 'inventory.json'


class Loads(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script' and a.get('src'):
            self.paths.append(('script', a['src']))
        if tag == 'link' and a.get('rel') == 'stylesheet' and a.get('href'):
            self.paths.append(('stylesheet', a['href']))


files = {p.relative_to(SITE).as_posix(): p.stat().st_size for p in SITE.rglob('*') if p.is_file()}
pages = {}
loaded_by = {name: [] for name in files}
for name, size in files.items():
    if not name.endswith('.html'):
        continue
    parser = Loads()
    parser.feed((SITE / name).read_text(encoding='utf8'))
    loads = []
    for mode, ref in parser.paths:
        target = (SITE / name).parent.joinpath(ref).resolve().relative_to(SITE.resolve()).as_posix()
        loads.append({'mode': mode, 'path': target, 'bytes': files[target]})
        loaded_by[target].append(name)
    pages[name] = {'html_bytes': size, 'sync_loads': loads,
                   'initial_load_bytes': size + sum(item['bytes'] for item in loads),
                   'over_html_limit': size > 250_000,
                   'over_initial_limit': size + sum(item['bytes'] for item in loads) > 250_000}


def purpose(path):
    if path == 'index.html': return 'dashboard, directory, invalid-input notice'
    if path == 'compare.html': return 'company comparison selectors and cards'
    if path == 'data/index.json': return 'optional directory export; not loaded on navigation'
    if path == 'data/index.js': return 'directory/search index; synchronously loaded on every page'
    if path.startswith('c/') and path.endswith('.html'): return 'one company profile'
    if path.startswith('c/') and path.endswith('.data.js'): return 'profile evidence/claim payload; synchronously loaded on its profile'
    if path == 'assets/site.js': return 'interactive UI script; synchronously loaded on every page'
    if path == 'assets/site.css': return 'UI stylesheet; synchronously loaded on every page'
    return 'other generated file'


result = {'site': str(SITE), 'file_count': len(files), 'total_bytes': sum(files.values()),
          'files': {name: {'bytes': size, 'purpose': purpose(name), 'loaded_by': loaded_by[name],
                           'lazy': False if loaded_by[name] else None}
                    for name, size in sorted(files.items())},
          'pages': pages, 'largest_html': max(v['html_bytes'] for v in pages.values()),
          'largest_initial': max(v['initial_load_bytes'] for v in pages.values()),
          'html_limit_failures': [name for name, v in pages.items() if v['over_html_limit']],
          'initial_limit_failures': [name for name, v in pages.items() if v['over_initial_limit']],
          'lazy_chunk_limit_failures': []}
OUT.write_text(json.dumps(result, indent=2), encoding='utf8')
print(json.dumps({k: result[k] for k in ('file_count', 'total_bytes', 'largest_html', 'largest_initial',
                                         'html_limit_failures', 'initial_limit_failures')}))
