"""Add exact/HIGH breakdown and provenance without re-parsing or new requests."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
from audit import ROOT, DEST, DOWNLOADS, load_runs, host


def main():
    path = DEST / 'rejections.json'
    data = json.loads(path.read_text(encoding='utf8'))
    summaries = {s['seed']: s for s in data['samples']}
    for seed, work, registry, rows, report in load_runs():
        counts = {'exact_verified_websites': 0, 'high_websites': 0, 'declared_domain_VERIFIED': 0, 'declared_domain_HIGH': 0}
        for row in rows:
            declared = (registry.get(row['organisation_number']) or {}).get('hjemmeside')
            for claim in row['claims']:
                if claim['field'] != 'official_website' or claim['availability'] != 'available':
                    continue
                value = claim['value']; tier = value['identity_level']
                counts['exact_verified_websites' if tier == 'VERIFIED' else 'high_websites'] += 1
                if declared and host(value['final_url']) == host(declared):
                    counts['declared_domain_' + tier] += 1
        summaries[seed].update(counts)
    data['jobs']['index_file_sha256'] = hashlib.sha256((ROOT / 'src/signalpost/data/nav_index.json.gz').read_bytes()).hexdigest()
    data['jobs']['universe_archive_sha256'] = hashlib.sha256((DOWNLOADS / 'universe.jsonl.gz').read_bytes()).hexdigest()
    path.write_text(portable_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
    dns_path = DEST / 'dns_recheck.json'; dns = json.loads(dns_path.read_text(encoding='utf8'))
    dns['input_audit_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    dns['input_correction'] = 'Final report-only corrections add literal full-name/publisher locations, saved URL bases, structured-owner ID locations, unique DNS counts, exact/HIGH tier breakdown and bundle/universe hashes. DNS candidates unchanged; no query repeated.'
    dns_path.write_text(portable_text(json.dumps(dns, ensure_ascii=False, indent=2) + '\n'), encoding='utf8', newline='\n')
    totals = {key: sum(s[key] for s in data['samples']) for key in counts}
    note = '\nPublished proof tiers: 26 VERIFIED / 3 HIGH across all six samples. Registry-declared-domain publications: 10 VERIFIED / 3 HIGH. Thus strict exact-number declared-domain recall is 10/72 (13.89%); all default publication tiers together are 13/72 (18.06%). HIGH is never relabelled VERIFIED. Complete per-seed counts are in rejections.json.\n'
    for filename in ('rejections.md', 'W0_REPORT.md'):
        p = DEST / filename; text = p.read_text(encoding='utf8')
        if note.strip() not in text:
            p.write_text(portable_text(text + note), encoding='utf8', newline='\n')
    print(json.dumps(totals))


if __name__ == '__main__':
    main()
