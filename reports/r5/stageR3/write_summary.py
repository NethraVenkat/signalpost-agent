"""Final R5/R3 summary, exact saved-evidence inventory and validation."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
import sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reports/r5/stageR5'))
from declared_audit import SEEDS,save


def main():
    dest=Path(__file__).resolve().parent
    data=json.loads((dest/'items.json').read_text(encoding='utf8'))
    r5=json.loads((ROOT/'reports/r5/stageR5/items.json').read_text(encoding='utf8'))
    gap=json.loads((ROOT/'reports/r5/stageR5/declared_gap.json').read_text(encoding='utf8'))
    assert not data['new_doubtful'],'Doubtful new items require withholding before commit'
    manifest=json.loads((dest/'source_manifest.json').read_text(encoding='utf8'))
    assert manifest=={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    checked=[];table=[];totals=Counter()
    for seed in SEEDS:
        folder=dest/f'seed{seed}';settings=json.loads((folder/'settings.json').read_text(encoding='utf8'))
        work=Path(expand(settings['working_directory']));args=settings['command_argv']
        assert work.name.endswith('release-proof-final') and sum(a.startswith('--') for a in args)==7
        execution=json.loads((folder/'execution.json').read_text(encoding='utf8'));assert execution['exit_code']==0
        verification=json.loads((folder/'verification.json').read_text(encoding='utf8'))
        assert verification['terminal_envelopes']==verification['complete_briefing_contracts']==100
        assert verification['synthesis_unverified_values']==verification['briefing_unverified_values']==verification['cost_usd']==0
        assert verification['http_requests']<=1850 and verification['wall_seconds']<=2100
        counts=json.loads((folder/'counts.json').read_text(encoding='utf8'))
        for field,name in [('envelopes_sha256','envelopes.jsonl'),('profiles_sha256','profiles.jsonl')]:
            assert counts[field]==hashlib.sha256((work/name).read_bytes()).hexdigest()
        old=json.loads((ROOT/f'reports/r5/stageR5/seed{seed}/counts.json').read_text(encoding='utf8'))
        r4=json.loads((ROOT/f'reports/r5/stageW/seed{seed}/counts.json').read_text(encoding='utf8'))
        r5_gains=sum(i['seed']==seed and i['kind']=='website' and i['tier']=='registry_declared_publisher_name' for i in r5['added'])
        r3_gains=sum(i['seed']==seed and i['kind']=='website' and i['tier']=='publisher_name_rare_contact' for i in data['added'])
        row={'seed':seed,'declared_homepages':counts['declared_homepages'],
             'websites_R4':old['websites_before'],'websites_R5':old['websites_after'],'websites_R3':counts['websites_after'],
             'declared_recall_R4':old['declared_recall_before'],'declared_recall_R5':old['declared_recall_after'],'declared_recall_R3':counts['declared_recall_after'],
             'R5_tier_new_URLs':r5_gains,'R3_tier_new_URLs':r3_gains,
             'HTTP_R4':old['http_before'],'HTTP_R5':old['http_after'],'HTTP_R3':counts['http_after'],
             'wall_R4':r4['runtime_seconds'],'wall_R5':old['runtime_seconds'],'wall_R3':counts['runtime_seconds'],'cost_usd':0}
        table.append(row);checked.append({'seed':seed,'verification':verification,'execution':execution})
        for k,v in row.items():
            if k!='seed' and isinstance(v,(int,float)):totals[k]+=v
    log=(dest/'pytest.txt').read_bytes();test_result=log.decode('utf16' if log.startswith(b'\xff\xfe') else 'utf8').strip().splitlines()[-1]
    assert ' passed' in test_result and 'failed' not in test_result
    save(dest/'VALIDATION.json',{'stageR5_commit':'153465ff','stageR3_commit':'this commit','samples':checked,'table':table,'totals':dict(totals),
        'runtime_source_unchanged':True,'test_result':test_result,'new_doubtful':[],'cost_usd':0})
    lines=['# R5 / R3 — Measured publisher identity tiers','',
        'Branch revision/r5. Author/committer Nethra Venkat. R5 commit `153465ff`; R3 and this summary are in this commit (no self-referential hash). No push. Implemented here from the task descriptions; no other repository/entry code or data. Provider cost $0. N3 dropped; hiring unchanged.','',
        '## Declared-homepage gap','',
        f"Baseline 13/72 declared-homepage companies publish a VERIFIED/HIGH site, leaving 59 gaps. Causes: {json.dumps(gap['cause_counts'])}. [All company-level fetch chains, titles, R1 fragments, R4 conflicts and registry receipts](../stageR5/declared_gap.md). Historical unknown redirect targets are not invented. W0 had 29 total sites; the accepted R4 baseline has 30 after its documented exact-number LOOPYTY timeout recovery. Declared recall remains 13/72 in both.",'',
        '## Proof rules and limits','',
        'R5 `registry_declared_publisher_name`: exact complete legal name including suffix in a publisher fragment, registry-declared candidate hostname, and no R4/earlier veto. www/apex and HTTP(S) variants are accepted; cross-registrable-domain redirects need another registry-declared domain or the target publisher’s exact company number. Redirect destinations still obey per-authority robots, public-IP/TLS checks, hop limits and all budgets. [R5 full report and trials](../stageR5/REPORT.md).','',
        'R3 `publisher_name_rare_contact`: the same full publisher name plus an exact registered phone/mobile/full email in a footer/contact/imprint block; alternatively an exact registered email domain only when it equals the site’s own registrable domain. Contact count must be 1–2 distinct entities in the local R2 bundle. Zero/absent keys, common contacts and unavailable table abstain. Staff/employee/team blocks, customer/partner lists, articles, hidden content and split-node agency credits do not count. A name repeated twice remains one signal group. Both tiers are explicit HIGH proof types, never relabelled exact-number VERIFIED. R4, existing vetoes and strict social rules remain first.','',
        'R3 saves the name/contact excerpts and locations, exact original registry contact, normalized key/count and the R2 bundle/source hash, build date and NLOD attribution. The independent verifier checks exact registry fields and page bytes plus the local table, and rejects forged contact/count/URL receipts. No network lookup for rarity, new model, paid API, DNS fallback or budget increase. The table covers 1,177,860 entities in the saved enheter snapshot; optional nationwide subunit data was unavailable in R2. Snapshot rarity is not current global uniqueness.','',
        '## Six fresh seven-flag measurements','',
        'Recall counts companies with a registry homepage and a published VERIFIED/HIGH site, not merely matching domain strings. It is a declaration-based recall metric, not a human precision verdict. All three stages are shown against the accepted R4 baseline.','',
        '| Seed | Sites R4 / R5 / R3 | Declared recall R4 / R5 / R3 | Declared N | New R5 / R3 tier URLs | HTTP R4 / R5 / R3 | Wall seconds R4 / R5 / R3 |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for r in table:
        lines.append(f"| {r['seed']} | {r['websites_R4']} / {r['websites_R5']} / {r['websites_R3']} | {r['declared_recall_R4']} / {r['declared_recall_R5']} / {r['declared_recall_R3']} | {r['declared_homepages']} | {r['R5_tier_new_URLs']} / {r['R3_tier_new_URLs']} | {r['HTTP_R4']} / {r['HTTP_R5']} / {r['HTTP_R3']} | {r['wall_R4']:.1f} / {r['wall_R5']:.1f} / {r['wall_R3']:.1f} |")
    lines += ['',f"Total websites: {totals['websites_R4']} → {totals['websites_R5']} → {totals['websites_R3']}. Declared-homepage recall: {totals['declared_recall_R4']}/72 → {totals['declared_recall_R5']}/72 → {totals['declared_recall_R3']}/72. HTTP: {totals['HTTP_R4']} / {totals['HTTP_R5']} / {totals['HTTP_R3']}; summed process wall seconds: {totals['wall_R4']:.3f} / {totals['wall_R5']:.3f} / {totals['wall_R3']:.3f}. Each individual run stays below 1,850 requests and 35 minutes. Cost $0.",'',
        'Every R5 and R3 final sample: exactly seven flags, fresh working directory/state and new run ID, exit 0, 100 ordered terminal envelopes, full generated profile site, all five cited briefing topics, zero unsupported values. Settings preserve argv/input/bulk/source hashes; validation checks envelopes/profiles hashes against the actual final-run directory. Final runtime source was unchanged during each six-sample suite.','',
        'R3 test gate: '+test_result+'. R5 test gate: 1,016 passed. Tests cover exact name/suffix/normalization, R4 precedence, declared/cross-domain rules, robots/budgets/cache/retries, all contact kinds, positive count 1–2 versus zero/3+, exact own-domain restriction, staff/article/client/agency exclusions, repeat-name non-acceptance, missing-table abstention and forged evidence/counts/URLs.','',
        '## URL ledger and hand checks','',
        'Every new/removed R5 URL with orgnr, legal name, proof type, exact publisher excerpt and registry receipt: [R5 new_websites.md](../stageR5/new_websites.md). Every new/removed R3 website/social URL, including live-source changes under older rules: [R3 new_websites.md](new_websites.md). Both items.json files retain full response hashes, retrieval times, evidence excerpts and automated recheck reasons. No newly published item is doubtful in the saved-evidence recheck; this is not independent human ownership validation.','',
        'R5: six new company websites. Also two existing-website URL changes (VESTFJORDEN www variant, VALAKER → BRAUD), and removal of VALAKER’s old Facebook/Instagram links. BRAUD’s own footer explicitly states Valaker Bakeri og Konditori AS / 948 039 958; it is an older exact-number route, not an R5 gain. PROFINOVA remains withheld as a short frame fallback. Manager/group/foreign-publisher gaps remain vetoed. R5 trials, disk-full failure and lossless workspace-only 3.40 GB verified blob deduplication are disclosed in its report; no incomplete trial replaces a final sample.','',
        '### Every added website/social URL for manual review','']
    for stage,items in [('R5',r5['added']),('R3',data['added'])]:
        for i in items:
            lines.append(f"- {stage} / {i['seed']} / {i['orgnr']} / {i['legal_name']} / {i['kind']}: {i['url']} — `{i['tier']}`; saved-evidence verdict {i['automated_verdict']}.")
    lines += ['', 'Automated review limitation: exact evidence/rule replay can verify the published support, but cannot guarantee sources remain current or replace a human’s independent ownership check. Rarity only describes its bundled snapshot. No new social profile bypasses the strict own header/footer/name/group-context rule. Stop after this summary/stage commit; no new stage or push.','']
    (dest/'SUMMARY.md').write_text(portable_text('\n'.join(lines)),encoding='utf8',newline='\n')
    print(json.dumps({'totals':dict(totals),'test_result':test_result,'added':dict(Counter(i['kind'] for i in data['added'])),'removed':dict(Counter(i['kind'] for i in data['removed']))}))


if __name__=='__main__':main()
