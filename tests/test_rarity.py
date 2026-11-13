import csv
import gzip
import importlib.util
import json
from pathlib import Path
import pytest
from signalpost.web.rarity import count, domain_key, keys, load, name_key, phone_key


def test_key_normalization_and_free_mail():
    assert phone_key('+47 12 34 56 78') == phone_key('0047 12345678') == '12345678'
    assert phone_key('+46 12345678') is None
    assert name_key('BÅT & ØY AS') == name_key('ØY og BÅT ASA') == 'bat oy'
    assert domain_key('owner@GMAIL.COM') is None
    assert domain_key('Name@EXAMPLE.NO') == 'example.no'
    assert keys({'telefon': '12345678', 'mobil': '+47 12345678'})['phone'] == {'12345678'}


def test_builder_counts_entities_once_across_snapshots(tmp_path):
    spec = importlib.util.spec_from_file_location('build_rarity', Path(__file__).resolve().parents[1] / 'scripts/build_rarity_table.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    path = tmp_path / 'registry.csv'
    fields = ['organisasjonsnummer', 'navn', 'telefon', 'mobil', 'epostadresse']
    with path.open('w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
        writer.writerows([dict(zip(fields, r)) for r in [('923609016', 'Example AS', '12345678', '+47 12345678', 'one@example.no'),
                                                       ('993578843', 'Example ASA', '12345678', '', 'two@example.no')]])
    data = module.build([('enheter', path), ('underenheter', path)])
    assert data['entity_count'] == 2
    assert data['counts']['phone']['12345678'] == 2
    assert data['counts']['domain']['example.no'] == 2
    assert data['counts']['name']['example'] == 2
    output = tmp_path / 'table.gz'; output.write_bytes(gzip.compress(json.dumps(data).encode()))
    assert count('phone', '+47 12345678', output) == 2
    assert count('phone', '87654321', output) == 0
    assert count('domain', 'free@gmail.com', output) == 0
    assert count('domain', 'example.no', output) == 2


def test_missing_or_corrupt_local_data_never_fetches(tmp_path):
    with pytest.raises(FileNotFoundError):
        load(tmp_path / 'missing')
    path = tmp_path / 'bad.gz'; path.write_bytes(gzip.compress(b'{"schema_version":2}'))
    with pytest.raises(ValueError, match='schema'):
        load(path)
