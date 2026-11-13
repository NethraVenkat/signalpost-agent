"""Retain intermediate measurements before the atomic-copyright correction."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from audit import ROOT, DEST, SAMPLES


def main():
    trial = DEST / 'trials/copyright_wrapper'; trial.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((DEST / 'r4_source_manifest.json').read_text(encoding='utf8'))
    current = (ROOT / 'src/signalpost/web/publisher.py').read_text(encoding='utf8')
    insertion = "        block_children = any(isinstance(c, _Node) and c.tag in {'div', 'p', 'address', 'header', 'footer', 'main', 'section', 'aside', 'article', 'nav', 'ul', 'li', 'table'} for c in node.children)\n"
    old = current.replace(insertion, '').replace("if 'copyright' in marker and not block_children:", "if 'copyright' in marker:").replace('if not block_children and len(text) <= 1200', 'if len(text) <= 1200').encode()
    assert hashlib.sha256(old).hexdigest() == manifest['src/signalpost/web/publisher.py']
    (trial / 'publisher_before_copyright_fix.py').write_bytes(old)
    paths = []
    for seed, _ in SAMPLES:
        folder = DEST / ('seed' + str(seed))
        if not folder.exists():
            continue
        settings = json.loads((folder / 'settings.json').read_text(encoding='utf8')); work = Path(settings['working_directory'])
        assert (work / 'report.json').is_file() and (work / 'envelopes.jsonl').is_file()
        if not (folder / 'execution.json').exists():
            argv = settings['command_argv']; organisations = argv[argv.index('--organisations') + 1]
            command = [sys.executable, str(ROOT / 'scripts/check_live_run.py'), '--output', str(work / 'envelopes.jsonl'), '--organisations', organisations,
                       '--state', str(work / 'state'), '--report', str(work / 'report.json'), '--site', str(work / 'site'), '--count', '100']
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf8')
            (folder / 'verification.txt').write_text(result.stdout + result.stderr, encoding='utf8', newline='\n')
            assert result.returncode == 0, result.stderr
            (folder / 'verification.json').write_text(json.dumps(json.loads(result.stdout), indent=2) + '\n', encoding='utf8', newline='\n')
            shutil.copyfile(work / 'report.json', folder / 'report.json')
            (folder / 'driver_interruption.json').write_text(json.dumps({'driver_intentionally_stopped': True,
                'stop_scope': 'Only processes whose CommandLine matched this repository reports/r5/stageW/measure.py, verified through Cim.',
                'cli_child_allowed_to_finish': True, 'cli_exit_code': None,
                'source_import_window': 'In-flight child import timing is not captured; final source versus pre-fix source is not asserted for this rejected trial.',
                'exit_code_note': 'Not captured after driver stop; never asserted exit 0. All mandatory outputs independently verified.',
                'accepted_measurement': False}, indent=2) + '\n', encoding='utf8', newline='\n')
        paths.append((folder, trial / folder.name))
    paths += [(DEST / name, trial / name) for name in ('measure-log.txt', 'r4_source_manifest.json')]
    for source, target in paths:
        assert source.resolve().is_relative_to(DEST.resolve()) and target.resolve().is_relative_to(trial.resolve())
        assert source.exists() and not target.exists()
    for source, target in paths:
        shutil.move(str(source), str(target))
    (trial / 'README.md').write_text('# Superseded copyright-wrapper trial\n\nA further offline regression added a footer copyright line to the no-number HIGH fixture. Generic compound wrappers could copy the full body into a copyright fragment. Copyright inference now applies only to atomic blocks; semantic footer context and standalone copyright lines remain. No proof threshold changed. All saved output directories remain intact.\n\nThe owned driver was stopped to avoid more superseded requests; the in-flight CLI child completed all mandatory outputs/site and independently verified. Its exit code and precise source-import window were not captured, remain unknown and are not promoted into accepted results. Final measurements repeat all six with a fresh source manifest/state/run ID. No trial replaces an accepted sample.\n', encoding='utf8', newline='\n')
    print('Preserved copyright-wrapper trials and independently verified the completed child.')


if __name__ == '__main__':
    main()
