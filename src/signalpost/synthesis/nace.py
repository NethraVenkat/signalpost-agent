"""Offline SSB KLASS titles; versioned source snapshots: data/ and docs/SOURCES.md."""
import json
from pathlib import Path

TABLE = json.loads((Path(__file__).parent / 'data' / 'nace-klass-2026-10-13.json').read_text(encoding='utf8'))


def unspecified(value):
    return isinstance(value, dict) and (value.get('kode') == '00.000' or
        str(value.get('beskrivelse', '')).strip().casefold() == 'uoppgitt')


def english_title(value, version_id=None):
    if not isinstance(value, dict) or unspecified(value):
        return None
    code = str(value.get('kode', ''))
    description = ' '.join(str(value.get('beskrivelse', '')).split()).casefold()
    candidates = []
    matched = []
    for version in TABLE['versions']:
        if version_id is not None and version['version_id'] != version_id:
            continue
        subclass = version['subclasses'].get(code)
        title = version['titles'].get(code)
        if title:
            candidates.append(title)
            if subclass and description == ' '.join(subclass['registered_title'].split()).casefold():
                matched.append(title)
    # Conflicting versions need an exact registered-label match. No guessing.
    titles = set(matched or candidates)
    return next(iter(titles)) if len(titles) == 1 else None
