"""Preserve the stopped intermediate driver and its completed CLI outputs."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from audit import ROOT, DEST, SAMPLES


def main():
    trial = DEST / 'trials/short_contact_wrapper'
    trial.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((DEST / 'r4_source_manifest.json').read_text(encoding='utf8'))
    current = (ROOT / 'src/signalpost/web/publisher.py').read_bytes()
    old = current.replace(b"{'div', 'p', 'address', 'header', 'footer', 'main', 'section', 'aside', 'ul', 'li', 'table'}", b"{'div', 'p', 'address'}")
    assert hashlib.sha256(old).hexdigest() == manifest['src/signalpost/web/publisher.py']
    (trial / 'publisher_before_contact_fix.py').write_bytes(old)
    paths = []
    for seed, _ in SAMPLES:
        folder = DEST / ('seed' + str(seed))
        if not folder.exists():
            continue
        settings = json.loads((folder / 'settings.json').read_text(encoding='utf8')); work = Path(expand(settings['working_directory']))
        assert (work / 'report.json').is_file() and (work / 'envelopes.jsonl').is_file(), 'Do not archive unfinished CLI outputs as complete'
        if not (folder / 'execution.json').exists():
            argv = settings['command_argv']; organisations = argv[argv.index('--organisations') + 1]
            check = [sys.executable, str(ROOT / 'scripts/check_live_run.py'), '--output', str(work / 'envelopes.jsonl'), '--organisations', organisations,
                     '--state', str(work / 'state'), '--report', str(work / 'report.json'), '--site', str(work / 'site'), '--count', '100']
            result = subprocess.run(check, cwd=ROOT, capture_output=True, text=True, encoding='utf8')
            (folder / 'verification.txt').write_text(portable_text(result.stdout + result.stderr), encoding='utf8', newline='\n')
            assert result.returncode == 0, result.stderr
            (folder / 'verification.json').write_text(portable_text(json.dumps(json.loads(result.stdout), indent=2) + '\n'), encoding='utf8', newline='\n')
            shutil.copyfile(work / 'report.json', folder / 'report.json')
            (folder / 'driver_interruption.json').write_text(portable_text(json.dumps({'driver_intentionally_stopped': True, 'driver_pid': 563524,
                'reason': 'Avoid further superseded live runs after focused test exposed contact-container aggregation bug.',
                'cli_child_allowed_to_finish': True, 'cli_exit_code': None,
                'exit_code_note': 'Not captured after driver stop; never reported as exit 0. All 100 mandatory envelopes and site independently verified.',
                'accepted_measurement': False}, indent=2) + '\n'), encoding='utf8', newline='\n')
        paths.append((folder, trial / folder.name))
    paths += [(DEST / name, trial / name) for name in ('measure-log.txt', 'r4_source_manifest.json')]
    for source, target in paths:
        assert source.resolve().is_relative_to(DEST.resolve()) and target.resolve().is_relative_to(trial.resolve())
        assert source.exists() and not target.exists()
    for source, target in paths:
        shutil.move(str(source), str(target))
    (trial / 'README.md').write_text(portable_text('# Superseded short-contact-wrapper trial\n\nThe header-class correction was measured on four samples. A stronger no-orgnr HIGH regression exposed a separate issue: a short page wrapper could aggregate its footer contacts and biography into an imprint block. Contact containers now defer to descendant footer/main/section blocks rather than absorbing their content. The synthetic fixture also supplies a proper HTML head/title, matching the real page and exercising the existing HIGH path. No positive proof threshold changed.\n\nThe driver was intentionally stopped before more superseded batches; its current CLI child completed all mandatory outputs and site. That child exit code was not captured and is not invented. Its outputs independently verify 100 terminal envelopes, five cited topics and zero unsupported values. Other completed execution receipts retain their original exit codes. All raw output directories remain intact. No file from these runs is substituted for an accepted measurement. Before-contact-fix source bytes and the original source manifest are preserved.\n'), encoding='utf8', newline='\n')
    print('Preserved intermediate measurements and independently checked final child outputs.')


if __name__ == '__main__':
    main()
