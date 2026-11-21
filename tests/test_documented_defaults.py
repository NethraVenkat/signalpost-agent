from scripts.check_documented_defaults import check
from pathlib import Path


def test_current_judge_instructions_match_code_and_shipped_nav_index():
    result = check()
    assert result['current_defaults_verified']
    assert result['markdown_files_scanned'] > 100
