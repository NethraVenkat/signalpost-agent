"""Summarize accepted F1/C evidence; no network or source mutation."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
R=ROOT/'reports/r5'

def main():
    data={(s,c):json.loads((R/('stage'+s)/c/'counts.json').read_text(encoding='utf8')) for s in ('I','F1','C') for c in ('frozen','daily')}
    financial={s:json.loads((R/('stage'+s)/'financial_metrics.json').read_text(encoding='utf8')) for s in ('F1','C')}
    audit=json.loads((R/'stageC/audit.json').read_text(encoding='utf8'))
    diagnosis=json.loads((R/'stageC/diagnosis.json').read_text(encoding='utf8'))
    after=json.loads((R/'stageC/diagnosis_after.json').read_text(encoding='utf8'))
    changes=json.loads((R/'stageC/url_inventory.json').read_text(encoding='utf8'))['comparisons']
    text='''# Stage C - bounded proof-page discovery

Implementation commit: this commit; the exact hash is recorded in SUMMARY.md after the stage commit. No push or publication.

## Diagnosis and action

diagnosis.md/diagnosis.json use the actual F1 final runs. Every missing company is listed with state, exclusive primary cause, overlapping signals and saved attempt/request receipts. Primary buckets prioritize ambiguity/cutoff so the separate signal counts expose DNS/no-proof work hidden by a later cutoff. Robots includes access challenges; timeout includes connect/5xx. No candidate means no recorded nomination attempts; it does not assert no website exists.

| Cause | F1 frozen primary | F1 daily primary | C frozen primary | C daily primary |
|---|---:|---:|---:|---:|
'''
    for cause in ('no candidate','DNS fail','timeout','robots','fetched-no-proof','veto','budget','ambiguous'):
        text+='| '+cause+' | '+' | '.join(str(d[s]['primary'].get(cause,0)) for d,s in [(diagnosis,'frozen'),(diagnosis,'daily'),(after,'frozen'),(after,'daily')])+' |\n'
    text+='''
The largest cause is external DNS failure, followed by budget outcomes. No NXDOMAIN, timeout, robots refusal, foreign/group veto or ambiguous proof is bypassed. The two actionable issues addressed are budget ordering and fetched-no-proof discovery: own linked proof pages precede sitemap nominations, then blind fixed paths; known privacy aliases precede redundant bare /om guesses. A map request uses one existing slot, so a late blind alias can remain unchecked; tests require explicit cutoff instead of raising the cap. Existing strong registry/email/subunit/NAV candidate ranking is retained.

Own sitemaps only nominate contact/about/privacy/impressum pages. Per candidate, one map and at most one non-news page-map child are inspected; at most two sitemap-nominated HTML pages per company across both passes. Discovered proof-page URLs reject cross-domain/query-dependent/news targets and binary file suffixes. XML supplies no website proof: the fetched HTML must pass the unchanged identity scorer, exact number/corroboration, group/foreign veto and localized receipt rules. No HTTP/DNS/time allowance is added. Sitemap attempts/targets/cutoffs appear in run.refresh.proof_sitemaps.

Cloudflare active challenge markers, branded access-security gates and challenge titles are detected before identity scoring and before HTTP status retry/fallback, including text/plain challenge bodies and HTTP 403/503 gates. Blocked exceptions on own proof pages stop the candidate instead of continuing blind guesses. Ordinary recaptcha contact forms and passive Cloudflare scripts/jsd/main.js on a usable page are not access gates; a visible gate still blocks when JSD is present. Robots, public-IP pinning/TLS, terms, politeness, cumulative company/global budgets and once-only candidate veto/cache rules remain intact.

The instruction never to use sitemaps for news is applied to public activity as well as the new discovery path. Public updates now use explicitly linked RSS/Atom and bounded dated own-site HTML. Sitemaps cannot nominate news or supply lastmod claims. The corresponding activity/fact reduction is intentional; registry activity is retained and the measured difference is shown below.

## Accepted seven-flag measurements

Exactly --organisations, --bulk, --output, --profiles-output, --report, --run-id, --expected-count; original hash-checked seed 20261017/20261113 inputs; fresh state and new IDs. Both final C runs are sequential and use final source manifests. No enrichment/cap flags or paid services.

| Metric | I frozen | F1 frozen | C frozen | I daily | F1 daily | C daily |
|---|---:|---:|---:|---:|---:|---:|
'''
    for key in ('verified_websites','social_profile_companies','contacts','job_ad_companies','activity_companies','activity_claims','total_facts','http_requests','runtime_seconds','process_wall_seconds'):
        vals=[data[s,c]['metrics'][key] for c in ('frozen','daily') for s in ('I','F1','C')]
        text+='| '+key+' | '+' | '.join(f'{v:.3f}' if isinstance(v,float) else str(v) for v in vals)+' |\n'
    for key,label in [('derived_ratios','Derived ratios'),('yoy_metrics','Comparable revenue YoY metrics'),('yoy_cited_sentence_instances','Distinct cited YoY sentence instances within profiles')]:
        vals=[0,financial['F1']['frozen'][key],financial['C']['frozen'][key],0,financial['F1']['daily'][key],financial['C']['daily'][key]]
        text+='| '+label+' | '+' | '.join(map(str,vals))+' |\n'
    text+='\nF1 restores dimensionless arithmetic without assigning absolute scale: matching exact-company statement, period, declared currency and unit field for ratios; matching unit fields (or both absent from the same approved entity schema), consecutive comparable annual periods and positive prior revenue for YoY. Every metric cites both inputs. Raw absolute amounts remain labelled unscaled where appropriate, and whole-currency sentence frames require declared matching units. Independent verification rechecks raw amounts/periods/currency/unit and statement/schema scope.\n\n'
    text+='## Sitemap and access audit\n\n'
    for sample in ('frozen','daily'):
        a=audit[sample]
        text+=f'- {sample}: map attempt states `{json.dumps(a["sitemap_attempt_states"],sort_keys=True)}`; companies by nominated-page count `{json.dumps(a["companies_by_nominated_page_count"],sort_keys=True)}`; new exact sites proved via map targets: {len(a["sitemap_proof_successes"])}; challenge companies: '+(', '.join(a['challenge_companies']) or 'none')+'.\n'
    text+='\nNo recall gain is claimed when the strict proof does not support one. Source variation and access/cap failures are not proof of website closure. new_websites.md lists every added/removed site/social URL with organisation number, company, proof tier, exact excerpt, retrieval time, source URL and hash; unchanged URLs remain in url_inventory.json.\n\n'
    for label,delta in changes.items():text+='- '+label+': '+str(len(delta['added']))+' added, '+str(len(delta['removed']))+' removed website/social URLs.\n'
    text+='''
## Gates, trials and hand checks

Full F1 pytest: 899 green. Final C pytest: 912 green (pytest-release.txt); final focused suite: 96 green. Tests include positive hidden-map exact proof, two-page quota across candidates, one-child depth, cross-domain/news/binary/query rejection, malformed/DTD refusal, hard budgets/robots, veto stops, ordinary contact forms, passive JSD versus real gates, 200/403/503 challenges, own-link careers, financial scope/scale and all existing contracts. Earlier tests are retained; stale legacy assertions were updated to the new explicit sitemap policy, never by raising a resource/proof gate.

Each final run exits 0 with 100 ordered terminal envelopes, an available 100-company site, all five cited briefing topics, zero unsupported values, HTTP <=1850, completion within 2100 seconds and $0. audit.json rechecks the seven flags, final source hashes, <=13 cumulative website HTTP, two nominated-page quota, no sitemap news, and the unchanged <250000-byte profile gate. Review exact section states rather than treating exit 0 as source success. Financial metrics are dimensionless; no future performance or commercial suitability is inferred.

Headless Chromium 156.0.8078.4 passes 20 checks at 1280/360 px on the final recovered frozen site: search by name/org number, profiles, complete retained registry timeline/source receipts, restored financial briefings, filed-year source jumps, largest history profile, all evidence and comparison. Eighteen screenshots are in browser-release/, including mobile-financial-row showing unknown absolute unit. Targets >=44px, no horizontal scroll/JavaScript errors; external browser requests blocked. All QA/application code is authored within this repository; only an installed Playwright dependency is used, with no application code copied from another repository.

Retained trials: pre_transport/ includes initial proof-scoring-only runs and browser evidence; html_only_transport/ preserves the later incomplete implementation run, its complete output reverified independently, and the report-postprocessor collision failure. passive_jsd_false_block/ retains both audited trial samples and the historical URL receipt for a false DIGITALIQ removal: a broad challenge-platform matcher mistook passive JSD for an interactive gate. The final rule excludes passive JSD on usable pages and still blocks active/visible gates; both samples were remeasured. A host no-progress interval inflated trial runtimes. One superseded wrapper read the newer run's fixed report directory; its own report/counts were reconstructed and independently reverified in the trial folder, not accepted as final metrics. Final measurements are sequential, have their own fresh state, and pass the final audit. Further tests caught text/plain gates and swallowed blocked exceptions; final source handles both. An automatic approval-review timeout delayed the final test launch; the authorized single retry succeeded. No trial output is substituted for an accepted run.

The unchanged-code dns_outage/ pair is retained separately: the frozen run had 15 role, 16 figure and 19 filing-year checks reporting OS name-not-found failures; the daily run had seven incomplete subunit/hiring scopes. These were not converted to success or replaced with historical proofs. One fresh recovery run per sample followed; accepted comparison rows use those later runs and the source-failure pair remains inspectable. The daily reporting wrapper also exposed a counting bug when a state was absent from the baseline: the helper now includes newly observed states and regenerated its table from saved output without a crawl. All retained outputs independently verify zero unsupported values. Passive JSD behavior was checked against the vendor's official documentation; passive_jsd_review.json replays DIGITALIQ's saved body and exact number without a live fetch or publication carry-forward.

Hand checks: compare F1 and C proof URL inventories; inspect any removed URL's current failure plus historical proof, never promote the historical receipt. Check the map-nominated candidate pages in audit.json/diagnosis_after.json: a nomination is not identity proof. Inspect challenge receipts for the org numbers in audit.json and the complete request ledgers, and verify no follow-up guess or alternate host bypassed a blocked candidate. For F1, inspect a matching-missing-unit ratio and a comparable YoY example alongside the raw amount's unknown-unit label; both input citations are retained. SPEDIFY and INNLANDET REVISJON IKS profiles exercise the restored arithmetic and source panels. Registry-only activity remains available even where public website checks fail.

Cost/models/licences: $0 provider fees; model calls=0, paid search=0. Code and Playwright retain MIT, Brreg NLOD 2.0 attribution, NAV official reuse terms and SSB CC BY 4.0; company content retains its own terms. Compute/storage/network excluded as in prior reports. No push, publication or next stage. Commit C, commit the combined SUMMARY.md, then stop.
'''
    (R/'stageC/C_REPORT.md').write_text(portable_text(text),encoding='utf8')

if __name__=='__main__':main()
