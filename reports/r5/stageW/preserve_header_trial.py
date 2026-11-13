"""Retain all six superseded runs before measuring the corrected extractor."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from audit import ROOT, DEST, SAMPLES
from signalpost.web.html import Page
from signalpost.web.publisher_veto import conflict


def main():
    trial = DEST / 'trials/overbroad_header'
    trial.mkdir(parents=True, exist_ok=False)
    # Verify both ends stay inside the exact stage report folder before any move.
    paths = [(DEST / ('seed' + str(seed)), trial / ('seed' + str(seed))) for seed, _ in SAMPLES]
    paths += [(DEST / name, trial / name) for name in ('measure-log.txt', 'r4_source_manifest.json', 'r4_manifest_check.json')]
    for source, target in paths:
        assert source.resolve().is_relative_to(DEST.resolve()) and target.resolve().is_relative_to(trial.resolve())
        assert source.exists() and not target.exists()
    original = json.loads((DEST / 'r4_source_manifest.json').read_text(encoding='utf8'))
    old = subprocess.check_output(['git', 'show', '81a76b8d:src/signalpost/web/publisher.py'], cwd=ROOT)
    assert hashlib.sha256(old).hexdigest() == original['src/signalpost/web/publisher.py']
    (trial / 'publisher_before_header_fix.py').write_bytes(old)
    for source, target in paths:
        shutil.move(str(source), str(target))
    work = ROOT / '.data/r5/stageR4-20261116-final'
    sha = '3d7d01d8fb55e32be5685d30f458e2894829c08de225993269dd15d401173d7c'
    body = (work / 'state/blobs' / sha).read_bytes()
    assert hashlib.sha256(body).hexdigest() == sha
    page = Page(body, 'https://www.sissener.no/om-oss')
    rule, _ = conflict(page, '991658807', {'name': 'SISSENER AS'})
    assert rule is None
    excerpt = page.span_for('Franklin Financial Group')
    assert excerpt and excerpt in page.raw
    evidence = {'orgnr': '991658807', 'name': 'SISSENER AS', 'source_url': page.url, 'content_sha256': sha,
                'exact_excerpt': excerpt, 'old_rule': 'publisher_group_without_exact_orgnr', 'corrected_rule': rule,
                'false_header_wrapper_classes': 'header-over-content dmPageBody',
                'reason': 'Whole-page layout modifiers were mistaken for a header region. The Group words belong to employee biographies about former employers, not publisher/group branding.',
                'trial_raw_outputs_preserved': str(work), 'changes_to_proof_thresholds': False}
    (trial / 'false_veto.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    (trial / 'README.md').write_text('# Rejected header-wrapper trial\n\nAll six runs are retained, independently schema/evidence/site verified, but are not the accepted R4 comparison. Seed 20261116 falsely lost SISSENER HIGH website because a whole-page header-over-content class exposed biographies as publisher branding. The corrected extractor recognizes region components and excludes layout modifier traits. Exact source excerpt/hash in false_veto.json; old publisher source and complete original source manifest retained. Raw output directories remain in place. No historical proof was carried forward and no proof threshold was relaxed.\n', encoding='utf8', newline='\n')
    print('Preserved six trials; corrected SISSENER about-page guard passes.')


if __name__ == '__main__':
    main()
