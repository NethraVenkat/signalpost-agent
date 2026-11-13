"""Summarize qualification receipts without touching published outputs."""
import hashlib,json,subprocess
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/stageH'


def summarize():
    metadata=json.loads((DEST/'clean_clone.json').read_text(encoding='utf8'))
    ledger=json.loads((DEST/'precision/ledger.json').read_text(encoding='utf8'))
    samples={};all_rows=[]
    for seed in (20261115,20261116,20261117):
        sample='seed'+str(seed);folder=DEST/sample
        settings=json.loads((folder/'settings.json').read_text(encoding='utf8'))
        counts=json.loads((folder/'counts.json').read_text(encoding='utf8'))
        verification=json.loads((folder/'verification.json').read_text(encoding='utf8'))
        execution=json.loads((folder/'execution.json').read_text(encoding='utf8'))
        assert execution['exit_code']==0 and execution['wall_seconds']<=2100
        assert verification['lines']==verification['complete_briefing_contracts']==100 and verification['site_verified']
        assert verification['synthesis_unverified_values']==verification['briefing_unverified_values']==0
        assert counts['metrics']['http_requests']<=1850 and counts['metrics']['cost_usd']==0
        work=Path(settings['working_directory'])
        for name,expected in counts['artifacts'].items():assert hashlib.sha256((work/name).read_bytes()).hexdigest()==expected
        assert hashlib.sha256((folder/'report.json').read_bytes()).hexdigest()==counts['artifacts']['report.json']
        rows=[json.loads(x) for x in (work/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        assert [r['organisation_number'] for r in rows]==metadata['samples'][sample]['input_order']
        all_rows+=rows
        metrics=ledger['measurements'][sample]
        samples[sample]={'seed':seed,'metrics':metrics,'verification':verification,'source_commit':metadata['tested_commit'],
            'output_sha256':counts['artifacts']['envelopes.jsonl'],'site':json.loads((folder/'report.json').read_text(encoding='utf8'))['site']}
    assert len({r['organisation_number'] for r in all_rows})==300
    for scope in metadata['samples'].values():assert not any(scope['overlap_with_prior_samples'].values()) and scope['overlap_with_all_preceding_inputs']==0
    counts=ledger['counts'];flagged=[i for i in ledger['items'] if i['verdict']!='correct']
    summary={'tested_commit':metadata['tested_commit'],'samples':samples,'terminal_envelopes':300,'unique_companies':300,
        'http_total':sum(s['metrics']['http_requests'] for s in samples.values()),
        'process_wall_seconds_total':sum(s['metrics']['process_wall_seconds'] for s in samples.values()),
        'published_facts':sum(s['metrics']['total_facts'] for s in samples.values()),'cost_usd':0,
        'precision_counts':counts,'flagged_items':len(flagged),'wrong_items':sum(i['verdict']=='wrong' for i in flagged)}
    save=DEST/'results.json';save.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    text='# Stage H - three clean-clone mock daily tests\n\n'
    text+='Tested `revision/r5` HEAD `'+metadata['tested_commit']+'` (CI repair and four human verdicts), cloned locally with --no-hardlinks; uv sync --frozen succeeded. Interpreter/module paths and lock/source hashes are retained. No push, publication, tag or version change. Author/committer Nethra Venkat. No external implementation code copied; provider cost $0.\n\n'
    text+='## Per-batch results\n\n'
    text+='| Seed | Terminal / ordered | Websites | Social companies | Jobs / job companies | LEI companies | Parent companies | Awards | Activity claims | Facts | HTTP | Wall s | Site | Unsupported |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|\n'
    for sample,s in samples.items():
        m=s['metrics'];text+=f"| {s['seed']} | 100 / yes | {m['verified_websites']} | {m['social_profile_companies']} | {m['job_claims']} / {m['job_ad_companies']} | {m['lei_companies']} | {m['parent_companies']} | {m['award_claims']} | {m['activity_claims']} | {m['total_facts']} | {m['http_requests']} | {m['process_wall_seconds']:.3f} | generated | 0 |\n"
    text+=f"\nTotals: 300 ordered terminal envelopes, 300 unique companies, {summary['published_facts']} published facts, {summary['http_total']} HTTP across three independently bounded runs; {summary['process_wall_seconds_total']:.3f}s combined sequential process wall, $0. Each run exited 0, used <=1850 HTTP and <=2100s wall, generated the site and all five cited briefing topics, and independently verified zero unsupported values. The totals do not replace per-batch safety checks.\n\n"
    text+='Exactly seven evaluator flags per command: --organisations, --bulk, --output, --profiles-output, --report, --run-id, --expected-count. Default feature/cap/time settings; no cap/enable flags. Each run starts in a different empty working directory inside the clone; no state/cache copied. Search provider disabled explicitly in the environment, no model calls or paid API. Exact argv, cwd, runtime, report, output/source/input hashes and verifier receipts are in each seed folder.\n\n'
    text+=f"Sampling: universe {metadata['universe_count']} rows, archive/content/snapshot hashes verified. Exclude {metadata['original_excluded_unique']} unique earlier retained named sample/batch/CI inputs, explicitly including seeds 20261017/20261113/20261114; draw Random(seed).sample from remaining corpus order and exclude each preceding H batch before the next draw. Zero overlap with every recorded prior input and between the three H samples. Registry rows are extracted from the supplied snapshot without changing the seeded draws; absent rows are listed below and use the existing strict live identity fallback. No row is invented and no company is resampled. Full sampling inputs/exclusion manifests/order/hashes: clean_clone.json.\n\n"
    text+='Snapshot extraction by batch:\n\n'
    for sample,scope in metadata['samples'].items():
        text+='- '+sample+': '+str(scope['registry_rows_found'])+' CSV rows; missing snapshot IDs: '+(', '.join(scope['missing_snapshot_rows']) or 'none')+'.\n'
    text+='\n'
    text+='## Failures and fixes\n\n'
    text+='Before H, old pushed 1e93023 workflow was reproduced with original flags and failed its strict verifier on a site-size warning. Current code also reproduced the fixture size regression. CI-fix commit '+metadata['tested_commit']+' changes workflow to seven flags/default scaled budget/fresh cwd and always-uploaded artifacts; its verifier rejects corrupt schema/evidence/order/unsupported values/missing actual site while permitting honest live-source outages. Renderer defers only duplicate audit rows through the existing local loader under the unchanged 250000-byte gate; no proof rule or fact removed. Fresh corrected CI20: 147 HTTP, 107.698s process wall, 20 ordered terminal envelopes/site, zero unsupported values. [Full CI reproduction](../ci-fix/SUMMARY.md).\n\n'
    failures=list((DEST/'trials').glob('*')) if (DEST/'trials').exists() else []
    text+='All three initial Stage H daily batches passed the qualification checks; no daily batch rerun or production correction was needed. The first clean-clone test gate failed two fake-search tests because the measurement wrapper inherited its live search-disabled environment. Fix only the wrapper: offline tests clear provider/mock/key overrides while live runs keep paid search disabled. A focused regression test passes, followed by a fully green unchanged clone suite. Additional preparation-only issues were an invalid UTF-8 alias and an incorrect assumption that every universe draw exists in the older bulk snapshot. Both wrapper checks were corrected without editing clone production code, resampling or inventing rows. Missing bulk rows go through existing live identity checks. Regression tests verify environment isolation and found-plus-missing extraction counts. Original receipts are in trials/preparation-env, preparation-encoding and preparation-missing-snapshot; historical CI site failures are in trials/ci-site-regression. Legitimate source errors stay explicit; terminal does not mean every source succeeded.\n\n'
    text+='## Precision and hand checks\n\n'
    text+='All published websites, social profiles, jobs, LEIs/parents and awards were rechecked from saved hashes/excerpts and source-bound identity/link/role rules. Every item is retained, including flags. No live re-fetch or output modification. The four user-confirmed original T items remain confirmed in the old precision ledger; those sample/value-scoped verdicts are not transferred to new H companies. This is an automated evidence audit, not independently human-labelled real-world precision.\n\n'
    text+='| Type | Checked | Automated correct | Doubtful | Wrong |\n|---|---:|---:|---:|---:|\n'
    for typ,c in counts.items():text+=f"| {typ} | {sum(c.values())} | {c['correct']} | {c['doubtful']} | {c['wrong']} |\n"
    text+='\nFull per-item value/proof tier/exact excerpts/source URL/retrieval/hash/verdict: [precision/LEDGER.md](precision/LEDGER.md) and ledger.json. [Every flagged item with excerpts](doubtful_items.md), doubtful_items.json.\n\n'
    for item in flagged:
        text+='- **'+str(item['seed'])+' / '+item['organisation_number']+' / '+item['company']+' / '+item['kind']+' ('+item['verdict']+')**: '+'; '.join(item['reasons'])+'.\n'
    if not flagged:text+='No doubtful/wrong items were identified under the saved-evidence rules; this is not a guarantee of live correctness.\n'
    text+='\n## Validation and limits\n\nClean-clone full pytest: 952 passed (pytest.txt/pytest.json). Parent checkout final full pytest including both wrapper environment/extraction regression tests: 954 passed (pytest-parent-commit.txt). CI source gates: 952 passing tests and 33 focused site/gate tests before commit; all proof/access/robots/politeness/global/time rules unchanged. Stage H clone package remains version 1.3.0; lockfile frozen, no new dependency. GLEIF CC0, TED EU reuse policy, official registry/NAV and verified site terms remain in docs/SOURCES.md. Some live APIs may block cloud runners; current published claims must still pass the same saved-evidence validation. Local Windows qualification is not a GitHub Linux execution or official score.\n\n'
    text+='Decisions: [DECISIONS.md](../DECISIONS.md), CI and H entries. Historical reports remain historical. Stopped after H summary commit; nothing pushed.\n'
    (DEST/'SUMMARY.md').write_text(text,encoding='utf8')
    print(json.dumps({k:v for k,v in summary.items() if k!='samples'}))
    return summary


if __name__=='__main__':summarize()
