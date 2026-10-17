"""JSONL is split on newline only. str.splitlines() also splits on U+2028, U+2029
and other separators that are legal inside JSON strings, and tore valid
envelopes apart."""
import json

from signalpost.io.input_adapter import read
from signalpost.models.shapes import serialize
from signalpost.site import generate_site
from tests.test_synthesis import envelope

LS, PS = chr(0x2028), chr(0x2029)  # Line and paragraph separator.
SEPARATORS = LS + PS + chr(0x85) + chr(0x0b) + chr(0x0c)


def dumps(row):
    return json.dumps(row, ensure_ascii=False)


def test_site_reads_envelopes_with_unicode_line_separators_in_strings(tmp_path):
    row, _ = envelope(tmp_path / 'run')
    row.claims[0].value = 'Alpha' + SEPARATORS + 'Beta'
    line = dumps(serialize(row, 'union'))
    assert LS in line and PS in line  # Raw separators, not JSON escapes.
    source = tmp_path / 'source.jsonl'
    source.write_text(line + chr(10), encoding='utf8')
    assert generate_site(source, tmp_path / 'site')['companies'] == 1


def test_input_adapter_keeps_jsonl_rows_with_unicode_line_separators(tmp_path):
    path = tmp_path / 'input.jsonl'
    rows = [{'organisation_number': '923609016', 'note': 'a' + LS + 'b' + PS + 'c'}, {'organisation_number': '993578843'}]
    path.write_text(chr(10).join(dumps(r) for r in rows) + chr(10), encoding='utf8')
    assert read(path).unique == ['923609016', '993578843']


def test_verify_output_loads_envelopes_with_unicode_line_separators(tmp_path):
    from scripts.verify_output import load
    row, _ = envelope(tmp_path / 'run')
    row.claims[0].value = 'a' + LS + 'b' + PS + 'c'
    path = tmp_path / 'out.jsonl'
    path.write_text(dumps(serialize(row, 'union')) + chr(10), encoding='utf8')
    assert len(load(path)) == 1
