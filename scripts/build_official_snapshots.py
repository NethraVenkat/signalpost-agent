"""Build Stage S bundled exact-orgnr snapshots from downloaded official files.

  research     Research Council of Norway `soknader2` (NLOD) + SkatteFUNN
               application lists (NLOD) -> src/signalpost/data/research_projects.json.gz
  inspections  Mattilsynet Smilefjes `tilsyn.csv` (CC BY 4.0)
               -> src/signalpost/data/food_inspections.json.gz

Only rows whose own organisation-number field holds a mod-11-valid number are
kept, with a fixed list of non-personal columns copied verbatim (no person
names, genders or free-text summaries). Each kept row is stored as one
canonical JSON record string; at runtime those exact bytes are the evidence
body, so verification can match them byte-for-byte against this bundle.
Downloads are inputs given on the command line (see docs/SOURCES.md); this
script performs no network requests.
"""
import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import sys
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from signalpost.identity.orgnr import valid  # noqa: E402

WINDOW_YEARS = 3
RCN_URL = 'https://raw.githubusercontent.com/Forskningsradet/open-data/main/datasets/soknader2/dataset.csv'
SF_NEW_URL = 'https://www.forskningsradet.no/siteassets/skattefunn/tall/260902-webliste-skattefunn.xlsx'
SF_OLD_URL = 'https://www.forskningsradet.no/siteassets/skattefunn/tall/skattefunn-innsendte-soknader-2002-2024.xlsx'
SMILE_URL = 'https://smilefjes.mattilsynet.no/api/tilsyn.csv'
RCN_COLUMNS = ('prosjektnummer', 'prosjekttittel', 'prosjektfase', 'prosjektstart', 'prosjektslutt', 'prosjektansvarlig_type',
               'prosjektansvarlig_navn', 'organisasjonsnummer', 'aktivitet', 'virkemiddel', 'tildelt_belop')
SF_NEW_COLUMNS = ('Søknadsnummer', 'Prosjektnummer', 'Prosjektansvarlig', 'Prosjekttittel', 'Organisasjonsnr', 'Godkjent',
                  'Fra-år', 'Til-år', 'Vedtaksdato')
SF_OLD_COLUMNS = ('Prosjektnummer', 'Bedriftsnavn', 'Prosjekttittel', 'Organisasjonsnummer', 'Søknad godkjent', 'Søknad avslått',
                  'Prosjektets fra-år', 'Prosjektets til-år', 'Vedtaksdato')
SMILE_COLUMNS = ('tilsynsobjektid', 'orgnummer', 'navn', 'postnr', 'poststed', 'tilsynid', 'status', 'dato', 'total_karakter',
                 'tilsynsbesoektype')
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def record(source, row, fields):
    return json.dumps({'source': source, 'row': row, 'fields': fields}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def excel_day(value):
    """Excel 1900 date system serial -> date (deterministic decoding of the stored cell)."""
    try:
        serial = float(value)
    except (TypeError, ValueError):
        return None
    if not 1 <= serial < 2958466:
        return None
    return date(1899, 12, 30) + timedelta(days=int(serial))


def xlsx_rows(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    shared = []
    if 'xl/sharedStrings.xml' in names:
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
            shared.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    sheets = sorted(n for n in names if re.fullmatch(r'xl/worksheets/sheet\d+\.xml', n))
    if len(sheets) != 1:
        raise SystemExit(f'{path}: expected one worksheet, found {len(sheets)}')
    rows = []
    for r in ET.fromstring(z.read(sheets[0])).findall('.//m:sheetData/m:row', NS):
        cells = {}
        for c in r.findall('m:c', NS):
            column = re.match(r'[A-Z]+', c.get('r', '')).group(0)
            v = c.find('m:v', NS)
            if v is None:
                inline = c.find('m:is/m:t', NS)
                cells[column] = inline.text if inline is not None else None
            else:
                cells[column] = shared[int(v.text)] if c.get('t') == 's' else v.text
        rows.append(cells)
    header = rows[0]
    keys = {col: name for col, name in header.items()}
    return [{keys[col]: val for col, val in row.items() if col in keys} for row in rows[1:]]


def source_meta(key, url, path, licence, total, kept, columns, retrieved_at):
    return {'key': key, 'source_url': url, 'retrieved_at': retrieved_at, 'sha256': sha(path), 'bytes': Path(path).stat().st_size,
            'licence': licence, 'rows_total': total, 'rows_kept': kept, 'columns': list(columns)}


def window(build_day):
    try:
        return build_day.replace(year=build_day.year - WINDOW_YEARS)
    except ValueError:
        return build_day.replace(year=build_day.year - WINDOW_YEARS, day=28)


def build_research(rcn, sf_new, sf_old, retrieved, build_day):
    records, sources = {}, []
    start = window(build_day)
    text = Path(rcn).read_bytes().decode('utf-8-sig')
    rows = list(csv.DictReader(io.StringIO(text, newline='')))
    kept = 0
    for i, row in enumerate(rows):
        org = (row.get('organisasjonsnummer') or '').strip()
        if not (valid(org) and row.get('prosjektansvarlig_type') == 'Organisasjon'
                and row.get('prosjektfase') in {'Bevilgning', 'Avsluttet'}):
            continue
        end = row.get('prosjektslutt') or ''
        if not (re.fullmatch(r'\d{4}', end) and int(end) >= start.year):
            continue
        records.setdefault(org, []).append(record('rcn', i, {k: row.get(k) for k in RCN_COLUMNS}))
        kept += 1
    sources.append(source_meta('rcn', RCN_URL, rcn, 'NLOD 2.0 (Norges forskningsråd, data.norge.no)', len(rows), kept, RCN_COLUMNS, retrieved['rcn']))
    for key, path, url, columns, org_key, approved in (
            ('skattefunn_2024_2026', sf_new, SF_NEW_URL, SF_NEW_COLUMNS, 'Organisasjonsnr', lambda r: r.get('Godkjent') == 'JA'),
            ('skattefunn_2002_2024', sf_old, SF_OLD_URL, SF_OLD_COLUMNS, 'Organisasjonsnummer',
             # This file marks both columns JA/NEI; approved means godkjent=JA and avslått=NEI.
             lambda r: r.get('Søknad godkjent') == 'JA' and r.get('Søknad avslått') == 'NEI')):
        rows = xlsx_rows(path)
        missing = [c for c in columns if c not in (rows[0] if rows else {}) and not any(c in r for r in rows[:50])]
        if missing:
            raise SystemExit(f'{key}: missing columns {missing}')
        kept = 0
        for i, row in enumerate(rows):
            org = (row.get(org_key) or '').strip()
            decided = excel_day(row.get('Vedtaksdato'))
            if not (valid(org) and approved(row) and decided and start <= decided <= build_day):
                continue
            records.setdefault(org, []).append(record(key, i, {k: row.get(k) for k in columns}))
            kept += 1
        sources.append(source_meta(key, url, path, 'NLOD 2.0 (Norges forskningsråd, data.norge.no)', len(rows), kept, columns, retrieved[key]))
    return records, sources


def build_inspections(smile, retrieved, build_day):
    start = window(build_day)
    text = Path(smile).read_bytes().decode('utf-8-sig')
    rows = list(csv.DictReader(io.StringIO(text, newline=''), delimiter=';'))
    records, kept = {}, 0
    for i, row in enumerate(rows):
        org = (row.get('orgnummer') or '').strip()
        raw = row.get('dato') or ''
        if not (valid(org) and re.fullmatch(r'\d{8}', raw)):
            continue
        try:
            day = date(int(raw[4:]), int(raw[2:4]), int(raw[:2]))
        except ValueError:
            continue
        if not start <= day <= build_day:
            continue
        records.setdefault(org, []).append(record('smilefjes', i, {k: row.get(k) for k in SMILE_COLUMNS}))
        kept += 1
    return records, [source_meta('smilefjes', SMILE_URL, smile, 'CC BY 4.0 (Mattilsynet, data.norge.no)', len(rows), kept,
                                 SMILE_COLUMNS, retrieved['smilefjes'])]


def write(path, family, records, sources, build_day):
    payload = {'schema': 1, 'family': family, 'built_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
               'window_start': window(build_day).isoformat(), 'build_day': build_day.isoformat(),
               'method': 'Exact mod-11-valid organisation-number field of the source row; fixed non-personal columns copied verbatim',
               'sources': sources, 'records': {org: sorted(set(v)) for org, v in sorted(records.items())}}
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')
    Path(path).write_bytes(gzip.compress(raw, mtime=0))
    print(json.dumps({'output': str(Path(path).relative_to(ROOT)), 'bytes': Path(path).stat().st_size, 'sha256': sha(path),
                      'companies': len(records), 'records': sum(len(v) for v in records.values()),
                      'sources': [{k: s[k] for k in ('key', 'rows_total', 'rows_kept', 'sha256')} for s in sources]}, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('family', choices=['research', 'inspections'])
    p.add_argument('--rcn'); p.add_argument('--skattefunn-new'); p.add_argument('--skattefunn-old'); p.add_argument('--smilefjes')
    p.add_argument('--retrieved', action='append', default=[], help='key=ISO-UTC download time, per source key')
    p.add_argument('--build-day', required=True, help='YYYY-MM-DD; fixes the 36-month window for reproducible builds')
    a = p.parse_args()
    retrieved = dict(x.split('=', 1) for x in a.retrieved)
    build_day = date.fromisoformat(a.build_day)
    if a.family == 'research':
        records, sources = build_research(a.rcn, a.skattefunn_new, a.skattefunn_old, retrieved, build_day)
        write(ROOT / 'src/signalpost/data/research_projects.json.gz', 'research', records, sources, build_day)
    else:
        records, sources = build_inspections(a.smilefjes, retrieved, build_day)
        write(ROOT / 'src/signalpost/data/food_inspections.json.gz', 'inspections', records, sources, build_day)


if __name__ == '__main__':
    main()
