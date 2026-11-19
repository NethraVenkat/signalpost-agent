from scripts.check_documented_defaults import check
from pathlib import Path


def test_current_judge_instructions_match_code_and_shipped_nav_index():
    result = check()
    assert result['current_defaults_verified']
    assert result['markdown_files_scanned'] > 100


def test_shipped_osm_database_has_explicit_licence_attribution_and_size():
    root = Path(__file__).resolve().parents[1]
    sources = (root / 'docs/SOURCES.md').read_text(encoding='utf8')
    section = sources.split('## Shipped OpenStreetMap candidate database', 1)[1]
    assert '© OpenStreetMap contributors' in section
    assert 'ODbL) 1.0' in section and 'share-alike' in section
    bundle = root / 'src/signalpost/data/website_seeds/openstreetmap.json.gz'
    assert f'{bundle.stat().st_size:,} compressed bytes' in section
