"""Execute the shipped theme handler with denied browser storage."""
import shutil
import subprocess
from pathlib import Path
import pytest


def test_theme_storage_denied_keeps_initialization_and_toggle_working():
    node = shutil.which('node')
    if not node:
        pytest.skip('Node unavailable: JavaScript execution requires Node')
    source = Path('src/signalpost/site_assets/site.js').read_text(encoding='utf-8')
    theme = source.split('// Theme toggle',1)[1].split('// Pre-process indexed records',1)[0]
    script = '''
const assert = require('node:assert/strict');
let clicked;
const button = {textContent:'', addEventListener:(_, fn)=>clicked=fn};
const document = {getElementById:()=>button, documentElement:{dataset:{}}};
const window = {matchMedia:()=>({matches:true})};
const localStorage = {getItem(){throw Error('SecurityError')},setItem(){throw Error('QuotaExceededError')}};
''' + theme + '''
assert.equal(document.documentElement.dataset.theme, 'dark');
clicked();
assert.equal(document.documentElement.dataset.theme, 'light');
assert.ok(button.textContent.includes('Dark'));
'''
    subprocess.run([node,'-e',script],check=True,capture_output=True,text=True)
