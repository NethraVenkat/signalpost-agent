"""Build the final combined A2/B measurement report from saved verified artifacts."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DEST=ROOT/'reports/r5/stageB'

def main():
    datasets={(stage,sample):json.loads((ROOT/'reports/r5'/('stage'+stage)/sample/'counts.json').read_text(encoding='utf8')) for stage in ['A2','B'] for sample in ['frozen','daily']}
    reports={(stage,sample):json.loads((ROOT/'reports/r5'/('stage'+stage)/sample/'report.json').read_text(encoding='utf8')) for stage in ['A2','B'] for sample in ['frozen','daily']}
    audit=json.loads((DEST/'event_comparison.json').read_text(encoding='utf8'))
    s="""# Stages A2 and B - final report

Completed on revision/r5 as Nethra Venkat <nethravenkat510@gmail.com>. Never pushed, published or started Stage D. The initial working tree was clean at 8a907844; prior release inventory/data-ignore commits and the local v1.2.0 tag were preserved.

## Commits and validation

| Stage | Commit | Green full pytest |
|---|---|---|
| A2 - useful bounded second pass | f0786702a4c825213084c946214c3a5d304260f4 | 848 passed in 139.44s |
| B - complete returned registry timeline, site fix, independent verification and this report | This commit, directly after A2 | 865 passed in 135.03s |

Source manifests cover all application files, including new files. Every accepted run uses exactly the seven evaluator flags, fresh state/new run ID, original hash-checked input/registry fixtures, $0, HTTP <=1850 and completion within 2100 seconds with an available 100-company site. Frozen seed is 20261017; the second sample is seed 20261113 from release-v4. Exact argv, resolved settings, source/output hashes, original reports, counts and independent verifications are saved under each stage/cohort directory.

## A2 - bounded capacity and transient retries

Pass 1 keeps 8/13 HTTP and eight DNS nominations. Pass 2 grants unfinished companies up to five additional HTTP slots and four DNS nominations, shared by all candidates/retries and taken only from remaining global capacity. Absolute cumulative maxima are 13 website HTTP / 18 overall company slots / 12 DNS nominations. The shared global meter and original deadline remain hard stops; counters never reset.

Strong registry homepage/email, subunit and NAV candidates may be retried once after timeout/connect/5xx failure. Only transient cached failures are evicted; NXDOMAIN, successes, proof vetoes, robots denials and access refusals are not retried. Shared candidates get at most one fresh retry across companies. Identity proof, corroboration, parent checks, politeness, robots and public-IP/TLS rules are unchanged. --no-adaptive-extra-budget retains the earlier scheduler for comparison.

A2 added IREV (987769386, https://irev.no) to the frozen result relative to Stage A, and ADVOKATFIRMAET TASHAKORI (934626176, https://tashakori.no) to the new-sample result relative to release-v4; both are VERIFIED. No comparison website/social URL was removed in A2. Exact receipts/excerpts are in ../stageA2/new_websites.md. In the daily run one exact site was gained in pass 2 and one strong retry succeeded; the frozen run gained no additional site in pass 2 after six pass-1 exact sites.

A host/tool no-progress interval inflated A2 wall times and expired shared NAV prefetch coverage: all hiring sections are incomplete. Zero jobs there is not verified absence, and lower HTTP is not a claimed scheduler speedup. Both runs remain within 2100 seconds. The interrupted full test gate is retained; an unchanged rerun passed. A daily comparison-postprocessor metadata error was corrected from the saved output without recrawling.

## Both-cohort comparison

Website counts include the existing accepted HIGH tier; exact pass gains count only VERIFIED sites. Activity companies means companies with published available activity claims, independently of aggregate section state. Live source/retry changes can affect recall, facts, states and HTTP; these tables do not attribute every delta to code.

| Metric | A2 frozen | B frozen | A2 seed-20261113 | B seed-20261113 |
|---|---:|---:|---:|---:|
"""
    keys=['verified_websites','social_profile_companies','contacts','job_ad_companies','activity_companies','activity_claims','total_facts','http_requests','runtime_seconds','process_wall_seconds']
    columns=[('A2','frozen'),('B','frozen'),('A2','daily'),('B','daily')]
    for key in keys:
        values=[datasets[col]['metrics'][key] for col in columns]
        s+='| '+key+' | '+' | '.join(f'{v:.3f}' if isinstance(v,float) else str(v) for v in values)+' |\n'
    s+='| Provider cost USD | 0 | 0 | 0 | 0 |\n'
    for family in ['website','activity','hiring','accounts']:
        s+='| '+family+' failed | '+' | '.join(str(datasets[col]['counts_by_section_state'][family].get('failed',0)) for col in columns)+' |\n'
    s+='\n| Stage / cohort / pass | All HTTP | Website HTTP | Exact sites gained | Strong retry outcomes |\n|---|---:|---:|---:|---|\n'
    for col in columns:
        a=reports[col]['adaptive_websites']
        for phase in ['pass1','pass2']:
            item=a[phase]
            s+='| '+' / '.join((*col,phase))+' | '+str(item['requests'])+' | '+str(item['website_requests'])+' | '+str(item['websites_gained'])+' | '+json.dumps(item.get('retry_outcomes',{}))+' |\n'
    s+="""
## B - registry event completeness within source scope

The existing shared 36-month Enhetsregisteret parent/subunit calls and pagination are unchanged; the extractor now publishes one claim per returned event, not only a few named field changes. It covers new, changed, deleted and generic company records plus proven-subunit changes/additions/removals. Supplied changed-field paths/operations are retained; known supported name/address/capital values retain their exact raw values. A generic event says "Registry record updated" and never invents what changed.

All dates are registry publication time, not effective date. Every event carries source URL, retrieval date, hash, locator and bounded verbatim receipts; subunit events additionally cite current exact-parent source proof. Subunits absent from the current proven scope, including historical removed units without proof, remain outside coverage. Formal announcement text remains unavailable; this is complete returned API coverage, not an exhaustive legal/company history.

Retain at most 50 newest events per company, with chronological ordering, deduplication by event identity and explicit counts/truncation. Partial-response failures stay failed while retaining verified events. The same cap applies after partial-refresh carry-forward; a current complete event supersedes a carried legacy field-frame for the same record/event identity, preventing duplicate events during an upgrade. Duplicate pagination IDs are rejected rather than double-published. Refreshing the same supported events is idempotent. The timeline displays every retained event and links to source evidence. The first-run what-changed topic picks a significant event within the newest 90-day cluster: deletion, name/capital change or new record before generic update, with ties by publication time; its cited date stays exact.

Independent verification reconstructs the complete closed event frame from saved raw JSON and verified parent scope. It rejects altered dates/types/changed fields/labels/values; checks source hashes and exact excerpts, cap/order, complete five-topic briefings and scorer mirrors. Parsed shared bodies/receipt sources are cached during verification only; no extra acquisition or weaker check is introduced.

| Event audit | B frozen | B seed-20261113 |
|---|---:|---:|
"""
    for key in ['companies_with_registry_events','events_published','previous_extractor_claims_on_the_same_retained_events','companies_truncated','shared_registry_http_requests']:
        s+='| '+key+' | '+str(audit['frozen'][key])+' | '+str(audit['daily'][key])+' |\n'
    s+='\nThe prior-extractor count applies the exact A2 extractor to the same retained B event bodies; it separates extraction differences from live sampling, without network calls. It is not an estimate for events omitted by the 50-event cap. events_audit.json contains every event, raw proof receipt, per-company coverage and selected briefing citation. event_comparison.json records event types and summary counts. Native tests demonstrate no request increase (one parent and one proven-subunit shared call even when 66 events are returned). Live request totals can still differ through source retries/pagination and website/NAV outcomes.\n'
    s+='\n| Independent B verification | Frozen | Seed-20261113 |\n|---|---:|---:|\n'
    for key in ['lines','published_claims','registry_events_verified','complete_briefing_contracts','financial_inputs_verified','derived_financial_metrics_verified','synthesis_unverified_values','briefing_unverified_values']:
        values=[json.loads((DEST/sample/'verification.json').read_text())[key] for sample in ['frozen','daily']]
        s+='| '+key+' | '+' | '.join(str(v) for v in values)+' |\n'
    s+="""
## Site regression, trials and URL evidence

The first B measurements passed raw-output verification but failed the existing 250 KB profile-page gate. Fifty event cards repeated long shared-batch URLs. These rejected runs are preserved under each cohort's site_trial/. The gate was not raised and no event/receipt was removed. Cards keep their bounded publisher-event link and Check the evidence button; full original batch URLs, excerpts, dates and hashes remain in the local expandable receipt payload. The browser then found long changed-field JSON-pointer paths overflowing mobile timeline cards. Timeline text now wraps within the card; a shorter badge keeps the full publication-time distinction in the event text. The 360px no-scroll assertion remains unchanged. These runs are retained in mobile_trial/. The final mobile-safe source, including the legacy/current-event refresh deduplication guard, was remeasured from fresh state on both samples. Pre-guard measurements remain under pre_refresh_dedup_trial/. Unit tests verify event links and all evidence IDs remain present.

B's URL changes versus A2 are recorded in new_websites.md and url_inventory.json with exact excerpts, org number, legal name and proof tier; removed receipts are explicitly historical. A2's requested complete delta list is committed in ../stageA2/new_websites.md. No weaker identity tier or inferred social affiliation was introduced.

The existing site remains a local generated run artifact; no publication or demo replacement is implied. Authored Playwright passes 16 checks at 1280/360px, including every retained registry event in the timeline, event-to-receipt links, search, comparison, 44px controls, no horizontal overflow and no JavaScript errors, with external requests blocked. Fourteen screenshots are retained alongside browser_results.json. The final run is checked again after measurement.  Unit tests and the generated-site size gate remain mandatory regardless of optional browser evidence.

## Decisions and hand checks

See ../DECISIONS.md. Hand-check:

- A2's successful late/strong retry and added TASHAKORI/IREV proof; review failed retry outcomes and shared/global capacity states rather than treating failures as absence.
- The newest-50 truncation flags and subunit scope: unproven historical removed workplaces are not silently attributed. Review generic labels against raw update type/changed fields.
- Significant-event selection and publication-time labels; a registry publication timestamp is not an inferred effective business-change date.
- Every added/removed URL's exact source excerpt and proof tier, especially existing HIGH corroboration and own-footer numeric LinkedIn attribution.
- NAV incomplete coverage, missing accounts and live timeout effects; no paid providers, official score, exhaustive history or causally proven runtime speedup is claimed.
- Physical mobile/Safari and large timelines after any separately authorized deployment.

Stopped after Stage B. No Stage D, push or publication.
"""
    (DEST/'SUMMARY.md').write_text(s,encoding='utf8')

if __name__=='__main__':main()
