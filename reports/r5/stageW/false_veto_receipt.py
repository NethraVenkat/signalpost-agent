"""Retain the saved SISSENER excerpt behind the discarded broad group match."""
import hashlib
import json
from pathlib import Path
from signalpost.web.html import Page
from signalpost.web.publisher_veto import conflict
from audit import ROOT, DEST


def main():
    settings = json.loads((ROOT / 'reports/r5/stageH/seed20261116/settings.json').read_text(encoding='utf8'))
    work = Path(settings['working_directory'])
    sha = '1fef9e92174a78bf6c105c6b7f14b8e488a231a8b0833d2f72325efcfdaf2702'
    body = (work / 'state/blobs' / sha).read_bytes()
    assert hashlib.sha256(body).hexdigest() == sha
    page = Page(body, 'https://www.sissener.no/')
    span = page.span_for('en del av')
    assert span and span in page.raw
    rule, _ = conflict(page, '991658807', {'name': 'SISSENER AS'})
    assert rule is None
    data = {'orgnr': '991658807', 'name': 'SISSENER AS', 'source_url': page.url, 'content_sha256': sha,
            'exact_excerpt': span, 'obsolete_match': 'en del av',
            'initial_trial_rule': 'publisher_group_without_exact_orgnr', 'current_conflict_rule': rule,
            'reason': 'The phrase concerns the fund selection process, not parent/group ownership. Bare part-of phrases were removed; explicit group/parent markers remain.',
            'method': 'Retrospective reproduction of discarded broad matcher on the original saved proof; not an accepted live result or new identity evidence.'}
    (DEST / 'r4_false_veto.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print('Saved exact SISSENER false-veto receipt; corrected conflict guard passes.')


if __name__ == '__main__':
    main()
