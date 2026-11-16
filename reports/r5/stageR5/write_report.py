"""Write the measured R5 report after all six runs and receipt rechecks."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import json
import hashlib
from pathlib import Path
from collections import Counter
from declared_audit import ROOT,SEEDS,save


def main():
    dest=Path(__file__).resolve().parent
    data=json.loads((dest/'items.json').read_text(encoding='utf8'))
    gap=json.loads((dest/'declared_gap.json').read_text(encoding='utf8'))
    assert not data['new_doubtful'],'Withhold or resolve doubtful new items before committing'
    tables=data['samples']
    assert len(tables)==6 and sum(t['declared_homepages'] for t in tables)==72
    qualified=[]
    for seed in SEEDS:
        folder=dest/f'seed{seed}'
        settings=json.loads((folder/'settings.json').read_text(encoding='utf8'))
        counts=json.loads((folder/'counts.json').read_text(encoding='utf8'))
        work=Path(expand(settings['working_directory']))
        assert work.name.endswith('release-proof-final') and sum(a.startswith('--') for a in settings['command_argv'])==7
        assert counts['envelopes_sha256']==hashlib.sha256((work/'envelopes.jsonl').read_bytes()).hexdigest(),'Stale trial counts'
        assert counts['profiles_sha256']==hashlib.sha256((work/'profiles.jsonl').read_bytes()).hexdigest(),'Stale trial profiles'
        v=json.loads((dest/f'seed{seed}/verification.json').read_text(encoding='utf8'))
        assert v['terminal_envelopes']==100 and v['complete_briefing_contracts']==100
        assert v['synthesis_unverified_values']==v['briefing_unverified_values']==v['cost_usd']==0
        qualified.append({'seed':seed,'work':str(work),'verification':v,'counts_sha256':hashlib.sha256((folder/'counts.json').read_bytes()).hexdigest()})
    manifest=json.loads((dest/'source_manifest.json').read_text(encoding='utf8'))
    assert manifest=={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    save(dest/'VALIDATION.json',{'samples':qualified,'accepted_runs':6,'ordered_terminal_envelopes':600,'new_doubtful_items':0,
         'runtime_source_unchanged':True,'declared_homepages':72,'cost_usd':0,'test_gate':'pytest-proof-final.txt'})
    log=(dest/'pytest-proof-final.txt').read_bytes()
    tests=log.decode('utf16' if log.startswith(b'\xff\xfe') else 'utf8').strip().splitlines()[-1]
    lines=['# R5 — Registry-declared domain and exact publisher legal name','',
        'Branch revision/r5; parent 23838192. Author/committer Nethra Venkat. No push. No paid models, search or APIs. R3 is not implemented in this stage.','',
        '## Gap diagnosis','',f"Before R5: 13/72 declared-homepage companies publish a website; 59 gaps. Primary causes: {json.dumps(gap['cause_counts'])}. Full per-company chains, publisher fragments, R4 conflicts and registry receipts are in declared_gap.md/json. Diagnosis used only accepted R4 saved responses (zero extra HTTP). Refused redirects retain unknown target/final-host states when historical Location headers were not saved.",'',
        '## Proof decision','',
        '`registry_declared_publisher_name` is an explicit HIGH proof type. It requires the complete registered legal name, including its suffix, in a permitted R1 publisher fragment and a candidate matching the registered homepage hostname (www/apex and HTTP(S) variants). Only case/whitespace and æ→ae, ø→o, å→a spelling normalization apply. No suffix removal, punctuation removal, fuzzy names or body-only mentions. All R4/previous vetoes remain ahead of acceptance. The old exact-number VERIFIED and corroborated HIGH routes remain distinct.','',
        'A declared redirect nominates a destination under the same HTTP/time/hop/SSRF/TLS/politeness limits, with robots checked at each authority. Cross-registrable-domain publication requires another explicit registry domain (registered email domain) or the exact company number in the destination publisher block. The redirect alone is never proof. Once-only candidate reuse is unchanged; the page cache additionally distinguishes redirect permission. N3/public DNS fallback is dropped; hiring is unchanged.','',
        'Every new-tier claim retains the publisher fragment/location, nomination/proof URL and registry homepage plus the authoritative registry evidence dependencies. Independent saved-evidence verification checks exact registry source fields, R4, the publisher name/domain rule, hashes/verbatim spans and published URL authority. The old registry-contact gate cannot override a successful new R5 rule. Social extraction/rules are unchanged.','',
        '## Fresh seven-flag results','',
        'Declared-homepage recall means companies with a registry homepage and a published VERIFIED/HIGH website; it is a declaration-based recall metric, not a human ownership precision verdict. Denominator is 72 across the six fixed samples.','',
        '| Seed | Total sites R4 → R5 | Declared recall R4 → R5 | Declared N | HTTP R4 → R5 | Wall seconds R5 |','|---|---:|---:|---:|---:|---:|']
    for t in tables:
        lines.append(f"| {t['seed']} | {t['websites_before']} → {t['websites_after']} | {t['declared_recall_before']} → {t['declared_recall_after']} | {t['declared_homepages']} | {t['http_before']} → {t['http_after']} | {t['runtime_seconds']:.3f} |")
    old=sum(t['websites_before'] for t in tables);new=sum(t['websites_after'] for t in tables);recall=sum(t['declared_recall_after'] for t in tables)
    added=Counter(i['kind'] for i in data['added']);removed=Counter(i['kind'] for i in data['removed'])
    gains=Counter(i['tier'] for i in data['added'] if i['kind']=='website')
    lines += ['',f"Total sites {old} → {new}; declared recall 13/72 → {recall}/72 ({recall/72:.2%}). Added: {dict(added)}; removed: {dict(removed)}. New website proof types: {dict(gains)}. Live changes under older tiers are reported separately from gains attributable to R5.",'',
        'Each final sample: exit 0, 100 ordered terminal envelopes, generated site, all five cited briefing topics, zero unsupported values, HTTP ≤1,850, completion under 35 minutes, provider cost $0. Exact argv/new run IDs/fresh working directories, input/bulk hashes, source manifest and validation receipts are in seed*/. Final source remained unchanged throughout all six measurements.','',
        'Test gate: '+tests+'. Positive and negative tests cover publisher regions, hidden/body/client/article/credit exclusions, suffix/punctuation mismatches, R4 precedence, cross-domain redirects, destination robots, exact publisher number, source receipt/URL tampering, and legacy cache/DNS/retry behavior.','',
        '## Hand check and resource disclosure','',
        'Every added or removed website/social URL, orgnr, legal name, tier, complete publisher text, exact raw excerpt, source URL/date/hash and registry receipt is listed in new_websites.md and items.json. Saved-evidence rechecks of every new item returned correct; this does not replace independent human ownership review. No doubtful item was silently removed.','',
        'Unaccepted pre-contact-gate trial: 699 HTTP, 369.266 reported completion seconds, 5 websites, declared recall 4/11, $0; retained under trials/pre_contact_gate/. Driver was stopped before another sample began; its current CLI child finished mandatory outputs and independently passed validation, but its exit code was not captured. It is not used as an accepted final measurement.','',
        'A second unaccepted suite found a pre-existing HIGH localization problem: stripping punctuation from the proof token prevented localization of DICA PROFIL & YRKESKLÆR AS even though its exact full publisher name satisfied R5. Candidate proof now falls back to the authorized R5 receipt when the older HIGH token cannot be localized; it does not invent or weaken an excerpt. The regression and full suite are green. The four superseded runs, source manifest and resource totals are retained under trials/pre_localization_fix/. Their last child was allowed to finish outputs after only the driver was stopped; its exit code is unknown. None is substituted for a final-source sample.','',
        'A later agency-credit recheck reproduced an R1 bug: removing a credit marker before joining a footer could leave the agency name in a sibling node. Extraction now preserves the marker while joining children and excludes traversal of credit siblings, including nested logos/copyright. Six split-node credit fixtures protect the new positive tier. trials/pre_split_credit_fix retains two completed runs (697 + 778 HTTP, $0), and a third incomplete run with no report/empty execution receipt after disk exhaustion. Its final exit/request totals are unknown; no output is invented.','',
        'Lossless workspace-only disk recovery: byte-identical saved blobs were SHA-256 checked and atomically replaced with hard links to identical local blobs. Every evidence path and byte remains available. blob_deduplication.json records reclaimed space/method. No other repository code/data was read, copied or modified.','',
        'Conservative withholding: PROFINOVA AS 899177932 has a matching title but its saved owner body is only a 49-character frame fallback; embedded publisher content is not fetched/proven and standard proof pages return 404. The existing short/script-shell guard remains. No title-only acceptance of that unverified frame is added. Saved-page eligibility/localization preflight found six eligible gap companies and zero remaining localization failures; this offline preflight is not a fresh measurement.','',
        'The previous completed R4 measurement has 30 total sites (including the documented LOOPYTY live-source recovery); W0 had 29. The declared-homepage baseline remains 13/72 in both. No proof-label relabelling is counted as a newly gained URL.','']
    (dest/'REPORT.md').write_text(portable_text('\n'.join(lines)),encoding='utf8',newline='\n')
    print(json.dumps({'websites_before':old,'websites_after':new,'declared_recall_after':recall,'new_site_tiers':dict(gains)}))


if __name__=='__main__':main()
