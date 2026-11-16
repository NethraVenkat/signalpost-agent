# Sources, licensing and access policy

The MIT licence covers this repository's code and documentation. Third-party data, website content and dependency licences retain their own terms.

## Registry

Stage B registry activity uses the existing shared official `/api/oppdateringer/enheter` and `/api/oppdateringer/underenheter` calls bounded to 36 months, with no additional request for event completeness. One claim represents one update event (new, changed, deleted, or generic), with all supplied changed-field paths/operations and an honest label. Known name/address/capital fields retain their directly supported values; other paths do not acquire invented interpretations. The newest 50 events per company are retained; coverage metadata reports truncation. Date is registry publication time, not effective date. Exact-current-parent proof is required for all subunit events, including removals; unproven historical subunits and formal announcement text remain outside coverage. Pagination errors/duplicate IDs fail affected coverage while preserving verified partial events. Source pointers/labels/values are independently rechecked from saved bodies.

Official HTTPS `data.brreg.no:443` endpoints:

- `/enhetsregisteret/api/enheter/{orgnr}` and `/roller`.
- `/enhetsregisteret/api/underenheter?overordnetEnhet={orgnr}&size=1000&page=N`.
- `/regnskapsregisteret/regnskap/{orgnr}`.
- `/regnskapsregisteret/regnskap/aarsregnskap/kopi/{orgnr}/aar` (available-copy years only).
- Bulk `/enhetsregisteret/api/enheter/lastned/csv`; responses can be gzip even with a CSV filename.

Redirects, URL credentials, unapproved hosts and ports are refused. Registry requests share a bounded async client, host semaphore and global budgets. Accounts allow two retries; other registry requests allow one on eligible failures, respecting Retry-After and remaining deadline. Bodies are hashed and stored.

Enhetsregisteret data uses NLOD 2.0: attribute Bronnoysundregistrene. Primary references: [dataset licensing](https://www.brreg.no/en/use-of-data-from-the-bronnoysund-register-centre/datasets-and-api/), [registry API](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/en/index.html), [accounts schema](https://raw.githubusercontent.com/brreg/regnskapsregister-api/master/src/main/resources/specification/regnskapsregister.json). Restricted authenticated role data is not requested.

R2's bundled identity-frequency table is built only from the project's existing official bulk snapshot. `scripts/build_rarity_table.py` embeds source SHA-256, local file timestamp (not an asserted effective date), build UTC, source URLs and Brønnøysundregistrene / NLOD 2.0 attribution. It supports an optional official underenheter CSV but does not claim one is included when unavailable. Runtime lookup reads the local gzip file with schema/size checks and has no network fallback. Frequency never authorizes ownership in R4. Build distributions and exact bundle hash are retained in reports/r5/stageW/rarity.json.

R3 (after R5 commit 153465ff) uses this local table only as contact corroboration alongside the exact full legal name in publisher context and no conflict. A positive frequency of 1–2 is required; missing/common contacts abstain. The full email-domain contact must equal the site's own registrable domain. Every new-tier proof retains the exact registry source fields, page excerpts, rarity count and bundle/source hash/date/attribution. Snapshot frequency is not current global uniqueness; no new HTTP request or source licence is introduced. R5's declaration/name tier and R3's name/contact tier remain HIGH, distinguishable from exact-number VERIFIED proof. Strict social rules and source/robot/budget constraints remain unchanged.

## Websites

### X1 role-registry publication events (checked 2026-11-14)

The existing NLOD public-registry REST policy covers the [documented open role-update endpoint](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html), `/api/oppdateringer/roller`. It supports exact company batches and CloudEvent cursors; no authenticated person endpoint is used. A current 237-event batch supplies only organisation number within event data, so the app publishes generic "Registry roles updated" events with exact event type and publication time, explicitly not effective date. Changed role/person/leadership details are unavailable and never inferred from current roles. Existing shared 50-event cap, evidence, budgets and failures remain. [Saved source review and diagnostic receipts](../reports/r5/stageX/sources/X1_SOURCE_REVIEW.md).

Candidates use parent registry website/email, listed-subunit website/email, then legal-name slugs, within unchanged candidate/request/DNS caps. Optional configured search may nominate further candidates only if there is budget for proof fetching. Public Suffix List boundaries come from the installed tldextract snapshot without network updates. Social/directory/search hosts are refused as company sources. Only HTML/XHTML/plain responses are used; scripts, images and third-party resources are not fetched. There is no browser renderer.

Every DNS answer and redirect must pass public-unicast and company-domain rules. Connection-time DNS pinning preserves TLS hostname checks and blocks rebinding to private, loopback, link-local, CGNAT, multicast or reserved addresses. HTTPS certificates remain verified; plaintext fallback is permitted only after TLS/connect failure.

Robots are checked per scheme/authority, including redirected hosts. Robots 404/410 permits access; disallow/errors refuse it. At least one second between starts and at most two concurrent requests per registrable domain. Defaults: eight website requests/company including robots/redirects, thirteen overall company slots for website eligibility, three-second candidate DNS prechecks, eight-second HTTP bounds and a two-MiB body cap. Both website ceilings are cumulative across passes; shared global safety limits and explicit opt-outs are documented in README. The user agent identifies this repository.

Website facts have company-owned provenance. Publication of short factual spans does not assert an open-data licence for website content. Social-profile URLs are extracted from accepted sites but social platforms are never requested. The weaker REGISTRY_DECLARED path is default-off: a generalisation audit found group branding with shared address data that did not identify the exact legal company. Its address corroboration was tightened to require the actual street rather than postcode/city alone; remaining ambiguity justified disabling it. `--registry-declared` exists only for explicit historical/research reproduction. Default publication retains HIGH own-company branding with corroboration or exact organisation-number proof.

## Static English industry titles (SSB KLASS)

Official SSB KLASS classification 6 was downloaded during development on **2026-10-13**. Runtime synthesis reads bundled files only; it never calls KLASS. The English version responses are saved, without replacing titles or truncating classification items, in `src/signalpost/synthesis/data/`:

| Standard | KLASS version | Underlying NACE | English source URL | Saved file |
|---|---|---|---|---|
| SN2025 | 3218; valid from 2025-01-01; last modified 2026-06-17T08:02:16.000+0000 | Rev. 2.1 | https://data.ssb.no/api/klass/v1/versions/3218?language=en | `ssb-sn2025-en-2026-10-13.json` |
| SN2007 | 30; valid from 2009-01-01 | Rev. 2 | https://data.ssb.no/api/klass/v1/versions/30?language=en | `ssb-sn2007-en-2026-10-13.json` |

`nace-klass-2026-10-13.json` records source URLs, download date and version metadata, all English four- and five-digit titles present in each saved response, and all 738/820 five-digit Norwegian subclasses with their official metadata. English lookup uses only the exact code's `name` in the selected version. There is no subclass-to-parent title fallback; missing exact English titles retain the Norwegian registry description. The original four-digit classes and parent metadata remain archival metadata only. Norwegian registered labels were downloaded on the same date from `https://data.ssb.no/api/klass/v1/versions/3218?language=nb` and `https://data.ssb.no/api/klass/v1/versions/30?language=nb` and retained in the normalized table to resolve version collisions. The English originals remain the title authority; tests compare every derived title against them. The exact-code index is derived from the already saved English responses without another download.

For example, SN2025 `46.640` has the exact English title **Wholesale of other machinery and equipment**, while the same code in SN2007 denotes textile machinery. SN2025 `97.001` has the exact title **Activities of housing cooperatives**; its parent's domestic-personnel title is never substituted. An exact normalized Norwegian label chooses between conflicting versions; if the version cannot be established, synthesis retains only the Norwegian description. Unknown codes never receive a guessed English title. `00.000` / `Uoppgitt` is omitted as an activity and shown as an explicit unknown. No English titles were sourced from model memory. `scripts/download_nace.py` reproduces the development-only download and table build; runtime versions are pinned until a deliberate code/data update.

Bundled SSB classification data retains [SSB's CC BY 4.0 licence](https://www.ssb.no/en/api); it is not relicensed as application code.

## NAV job ads and credentials

Stage D rebuilds the bundled exact-employer discovery index from the official
feed and active detail endpoints only. The bounded maintenance builder is
separate from evaluator budgets; daily runs still require current live detail
proof and exact current parent/subunit membership. Build counts, date, HTTP
attempts and runtime are recorded in `reports/r5/stageD/index_build.json`.
The index exports identifiers/dates only, never job descriptions or credentials.

Careers checks use the same website transport, robots rules and cumulative
counters. A current exact-number VERIFIED site must own the navigation/footer
link. External targets are restricted to the seven ATS registrable domains
listed in `web/careers.py`; no search/name result can authorize a posting. A
supported JobPosting needs a title and a non-expired deadline, a date within 60
days or in the future, or an explicit open status in the title's paragraph.
Group sites, other employer identifiers, unsupported layouts and query-dependent
URLs are withheld. Receipts retain the own-link chain, title and date/status
spans; the verifier replays that chain from saved bodies.

[Official feed documentation](https://navikt.github.io/pam-stilling-feed/) and [reuse terms](https://arbeidsplassen.nav.no/vilkar-api). HTTPS `pam-stilling-feed.nav.no:443` only, paths `/api/publicToken`, `/api/v1/feed`, `/api/v1/feed/{UUID}`, `/api/v1/feedentry/{UUID}`. Redirects and arbitrary query/path values are refused. The same public-IP pinned transport is used. Public ad URLs on arbeidsplassen.nav.no are derived, never fetched.

`NAV_API_TOKEN` is optional and read from the process environment. Otherwise retrieve the public credential at run start. Environment credentials can fall back once on rejected access. Credential bodies and Authorization headers are never stored or logged; credential-echo responses are refused. `.env.example` contains only a variable name; no .env loader runs.

A 185-day window accounts for the documented maximum ad lifetime. Resolve repeated UUIDs by latest modification before checking active entries. ETag 304 responses require exact locally stored bodies. Header employer names are discovery only; detail identifiers, status and dates authorize publication. The default detail cap is min(candidate ads, max(300, 2 × unique companies)), including retries. Distinctive-token overlap ranks candidates by inverse header-token frequency, stripping suffixes/stop words and converging Norwegian/ASCII spelling variants. Names never authorize a claim; unmatched identifiers remain unpublished and cap-hit candidate scopes remain incomplete.

NAV prefetch starts before company crawling and owns a separate pinned connection pool, so website traffic cannot evict its keep-alive connection. Its default time cap is `min(900 seconds, 40% of --time-budget-seconds)`; `--nav-time-cap-seconds` overrides it while the global watchdog still applies. Reports distinguish feed elapsed time/pages/seconds per page from total prefetch time and record `feed_complete` as soon as paging ends. Partial feed indexes never establish company absence or job closure.

The 185-day window remains conservative. The saved official documentation permits six-month ad lifetimes and recommends `If-Modified-Since` for paging. Active headers do not contain publication/expiry dates, and the prior complete header read fetched details for only two name candidates. Those two publication dates cannot prove an exhaustive shorter horizon for all 9,537 active headers. No shortest safe window can therefore be established from that archive; recent-update or last-page scans would risk losing unchanged active ads.

Terms require updates and removal of inactive/deleted ads. Known inactive/expired jobs are removed even on partial refresh. Unconfirmed historical support is explicitly stale. Emit factual title, dates, location/categories and identifiers; exclude descriptions and contact-person data.

## DNS and dated website updates

Email- and name-derived domains use a per-run cached DNS pre-check with a three-second bound and eight candidate checks/company. NXDOMAIN/no addresses produce `no_such_domain` without HTTP; timeout/SERVFAIL produce `dns_unavailable`, preserving incomplete source states. Public-IP preflight and connection-time pinning still apply. Reports count DNS resolver invocations separately, including guessed-domain checks, website preflight and pinned transport resolutions.

Dated website activity is enabled by default; use `--no-public-activity` to opt out. It uses explicitly linked same-domain RSS/Atom feeds and bounded dated own-site HTML. Sitemaps never supply news or update dates. No feed/sitemap publication licence is inferred. Dates, exact excerpts, same-company identity, robots/politeness and cumulative company/global budgets remain mandatory. XML is limited to two MiB and DTD/entity declarations are refused.

## Accounts history and units (Stage I)

The current [official OpenAPI](https://data.brreg.no/regnskapsregisteret/regnskap/v3/api-docs)
lists `/regnskapsregisteret/regnskap/aarsregnskap/kopi/{orgnr}/aar` as the
available-copy years endpoint. It returned HTTP 200 without authentication in
the development access check. The [official dataset catalogue](https://data.norge.no/en/datasets/8132460c-91ab-3950-a54b-a54ee20c62e9/regnskapsregisteret)
identifies the open-data distribution under [NLOD 2.0](https://data.norge.no/nlod/no/2.0).
Attribute Bronnoysundregistrene; no paid subscription, credentials or PDFs are
requested. Review receipts/schema are in `reports/r5/stageI/source_review/`.
The robots lookup disconnected; this is documented direct use of an expressly
published machine API under the existing approved-registry policy, not a
website crawl or a claim that a robots error permits website access.

One additional years lookup per company shares registry concurrency and the hard
global meter. A single shared gate spaces new lookups by at least 2.1 seconds; other transient failures retain bounded registry retries inside that gate. A 429
response is returned as blocked coverage without an immediate retry; all queued
lookups then wait at least 60 seconds or a longer Retry-After. Waiting checks the
original deadline and never grants request/time capacity.
Years mean copies available from this endpoint, not guaranteed complete lifetime
filing history. Each year and the list retain source pointers and hashed bodies.
Failures/denials/budget stops publish explicit unavailable year coverage, preserve
supported figures and never imply a filing deletion in refresh comparisons.

All earlier exact-entity SELSKAP statements already returned in the existing
response are retained with their own period, raw amount, currency and unit;
duplicate period ends are suppressed, wrong-owner and malformed rows withheld.
No year-by-year request probing, PDF extraction or multiplier is performed.
F1 ratios use two values from the same exact-company statement, period, declared
currency and unit-field value; matching absent units cancel. YoY requires
consecutive comparable annual periods, positive prior revenue, declared matching
currency and the same unit field (or both absent from the same approved schema).
Absolute values never acquire scale from that cancellation. Previous
four-ratio whole-NOK calibration is historical evidence only and no longer
supplies metadata for any current or prior statement. Undeclared units stay
unknown; missing comparable inputs produce an explicit unknown, not a trend.
The newer-filing comparison uses the greatest supported year from the registry
identity field or the available-copy years list, citing the selected year claim
and the claim that supplies the period of the figures.

## Models, dependencies and cost

No language model is called. Template synthesis costs $0 per run, per 100 companies and per configured 1,100-company batch; this excludes compute/storage/network costs and optional configured search. The model provider interface is tested with a fake provider only. No live model adapter or model host is enabled. Reserved model provider/model/key environment names contain no values in `.env.example`; setting a model key alone does not enable a call.

Optional Brave Web Search only nominates website candidates and never supplies published evidence. The starter kit's read-only `scripts/run_brave_discovery.py` uses `BRAVE_SEARCH_API_KEY`; the implementation accepts the same variable and `SIGNALPOST_SEARCH_PROVIDER=brave`. Own implementation, no connector code copied. Official [authentication](https://api-dashboard.search.brave.com/documentation/guides/authentication) uses `X-Subscription-Token`; [Web Search reference](https://api-dashboard.search.brave.com/api-reference/web/search/get) specifies the endpoint and result count. [Published pricing](https://brave.com/search/api/), checked 14 October 2026, is $5 per 1,000 Web Search requests. Configured estimate: $0.005 times billable query attempts, including retries, no assumed free credits; **verify before use/submission**. Costs/calls are capped and reported. Results remain in memory, no search bodies are stored as evidence. No development key supplied, so the live search gate is skipped; mock providers cover proof acceptance/rejection, domain filtering, caps, error fallback and costs.

An injected provider receives claim identifiers/labels and at most two bounded untrusted description quotes. It can only order approved English frames with placeholders; exact values are substituted locally and validated. One call/company, 15 seconds, 2,000 input tokens, 500 output tokens, global call/cost caps and cache prevent unbounded work. Both the dedicated model cap and global cost cap apply. Synthetic offline price entries must be replaced with verified rates before enabling an adapter. Invalid output/errors/caps use template fallback. The cache contains accepted placeholder JSON or sanitized fallback reasons, never credentials.

Runtime: httpx (BSD-3-Clause), Pydantic (MIT), tldextract (BSD-3-Clause); development: pytest (MIT), respx (BSD-3-Clause); build: Hatchling (MIT). Locked transitive dependencies retain their licences. The public company-universe download is an input-sampling resource, not claim evidence or part of the published dataset.

SSB KLASS data uses **CC BY 4.0**, confirmed by Statistics Norway's [API policy](https://www.ssb.no/en/api) and [licence](https://www.ssb.no/en/diverse/lisens). Attribute Statistics Norway, link [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and retain source/version URLs and download dates. The bundled table is a normalized exact-code index derived from the original responses; this transformation is disclosed and does not imply SSB endorsement. Confidential/personal data and third-party photographs are outside the licence's stated scope. Repository MIT does not replace these data terms.

Ranked NAV discovery requires a shared distinctive token occurring in at most0.5% of current active ad headers, capped at50 headers (a floor of3 supports tiny feeds). The saved9,741-active-header distribution gives48: barnehage435, helse391, oslo378 and nord198 are excluded; bygg35 is also excluded by the common-business-word rule. The common-only overlap list is bygg/service/eiendom/holding/transport/invest/consult/regnskap/drift/handel/norge/norway/group/gruppen. Tokens absent from headers can still make a legal name usable, but cannot create candidates. Companies with no usable distinctive name remain incomplete; previous active ads whose names cease to match also remain incomplete. These discovery constraints never publish or infer an employer identifier.

The default detail attempt cap is min(distinct candidate ads discovered during paging, max(300, 2 × unique companies)); explicit --nav-max-details overrides it, and retries count toward it and the global HTTP budget. Each arriving page is scored against the precomputed company/subunit name index. A candidate needs both distinctive-token overlap and a complete normalized known-name phrase. Pending candidates are ranked again as the observed header distribution changes; at most four detail workers run while the separate feed connection continues paging. Ads later made inactive may already have consumed an attempt; reports distinguish all discovered candidates from final active candidates. The 900-second adaptive NAV cap and run watchdog still apply. Completed company scopes remain complete after a detail timeout, provided the feed finished. Partial feed indexes never establish absence.

The company-website completion spacing belongs only to `WebsiteHttp`; NAV and Brreg do not enter that gate. NAV has its own isolated pool with one feed connection plus four detail connections, bounded retries and response-directed retry handling. No website delay or additional fixed NAV paging delay is applied. Reports include response-read and blob-store timing to distinguish transport/body work from storage.

Scheduling diagnostics use a100ms heartbeat and per-request httpcore header-send/body-completion timing. A failed request's in-flight duration is reported as request runtime, followed by a separate retry-dispatch gap; it is not counted again as idle after the preceding page. Windows Kernel-Power506/507 events confirm Modern Standby during the third cold100 diagnostic (2026-10-14,10:38:54–10:40:17 Asia/Kolkata). The original76.141-second timed-out attempt and75.493-second maximum loop lag remain in that report. Active Windows batches now use a temporary [SetThreadExecutionState](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate) `ES_SYSTEM_REQUIRED | ES_CONTINUOUS` request, restoring the prior thread state on completion. No display/away-mode request or persistent power setting is changed; `--allow-system-sleep` opts out. Explicit user sleep and system power policies can still take precedence. No sleep time is subtracted from budget or runtime measurements.


### Declared NAV official-feed index

`src/signalpost/data/nav_index.json.gz` is an explicitly declared development-time cache of official NAV discovery metadata. Version `nav-20261014T042640.758720Z-v1`, baseline/build time 2026-10-14T04:26:40.758720Z, 9,015 ads, 5,769 distinct employer orgnr, zero failed details, 403,768 compressed bytes. Exported entries comprise 6,791 `seeded_from_disk` and 2,224 freshly fetched ads (counts only). A saved detail may seed discovery when its UUID occurs as active in the latest feed and it supplies an employer orgnr; no timestamp-order proof is required for seeding. Every published ad still requires a new live detail and exact employer matching. The index schema permits only version/build/cursor/source/count metadata and per-ad UUID, employer orgnr, status, publication/expiry/modification dates and optional ETag. No title, description, ad text, person or contact fields ship.

The [official usage guidance](https://navikt.github.io/pam-stilling-feed/#using-the-feed) documents polling the last returned page and following its `next_url` once new pages appear. The stored cursor is that final page's official `feed_url`, not a guessed chronological offset. Runtime reads it forward to null `next_url`/`next_id`, merges status updates and nominates exact parent/listed-subunit candidates from the index plus the forward feed. Known-name discovery is only a fallback for new UUIDs without header employer identifiers. Cache metadata is attached as discovery provenance; claim evidence comes from the newly fetched live detail, with its SHA-256, bounded verbatim span and retrieval time. A missing/stale (default21 days), invalid or incomplete index falls back to the full 185-day feed and reports the reason. Absence requires a loaded usable index, completed forward feed, checked subunit coverage and all candidates live-checked. Token failure is blocked; missing live proof or an incomplete feed is failed. A positive verified ad can remain available while explicit errors preserve incomplete additional coverage.

Previously published ads are live-checked again. Only a detail showing inactive/expired can establish `closed_job`; a forward-feed status or a missing/unverified detail yields an observation, not a closure. Rebuild with `uv run python scripts/build_nav_index.py --state-dir state/nav-index-build --output src/signalpost/data/nav_index.json.gz --report out/nav-index-build-report.json`. Builder checkpoints every200 ads, resumes safely and never stores new header/detail bodies solely for index construction. It seeds existing official bodies, fetches missing details with at most4 workers, and shares escalating backoff for429/5xx while respecting Retry-After. Live runtime proof, URL/SSRF checks and the unchanged global budgets remain mandatory.

Builderr staff guidance, supplied by the user from Discord `#build-help`, 9 October 2026: search may nominate candidates only; facts must be fetched again from permitted sources and tied to the exact legal entity. Official provider/model/key/limits arrive as documented server-side environment variables; assume a clean run without reused output. Builderr supplies the registry snapshot. A declared cache of the official NAV feed is permitted when access is allowed, every published ad is live-verified and company-matched, and source/refresh metadata is retained. This is the supplied basis for the planned declared index and optional search adapter; it is not an independent verification of final official acceptance.

### Cold-run qualification and response size

All Wednesday gates from the W2 streaming rerun onward use a new, empty `--state-dir` without copied NAV pages, ETags or blobs. Earlier accepted 300-company runs (190.484–194.703 feed seconds, mostly 304 responses) and the previous 1,000-company result (239.968 feed seconds, 378 cached 304 responses) are **warm-cache measurements**, not official cold-run predictions. The diagnostic 300 run downloaded 187.661 MB of decoded feed bodies in 530.203 seconds over 378 pages (1.403 seconds/page). MB means decimal megabytes; decoded response bodies are measured, not compressed wire bytes.

The revised default `min(900 seconds, 40% of the run budget)` is retained after the final cold 1,000-company run finished in 268.875 seconds, below the 1,200-second headroom gate against 2,400 seconds. It read two forward pages in 2.547 seconds (0.279161 decoded MB); total NAV was 141.312 seconds, feed complete and hiring failed 0%. The separate 120-second NAV target was missed and remains an open performance risk. Overrides remain explicit and the global watchdog is unchanged.

The [official feed documentation](https://navikt.github.io/pam-stilling-feed/) and [controller](https://github.com/navikt/pam-stilling-feed/blob/main/src/main/kotlin/no/nav/pam/stilling/feed/FeedController.kt), checked again on 2026-10-14, expose no field-selection or compact-header projection. The controller accepts `pageSize` (default 1,000, ceiling 10,000), which changes batching rather than omitting ad header fields. Reducing it adds page overhead; increasing it does not remove per-ad payload, and the saved 10,000-item probe timed out. Keep the 1,000-item default and relative `next_url`; no undocumented parameters are sent. No payload reduction is claimed (0 MB saved by projection).


## Stage C proof-page sitemap discovery and challenges

Own navigation links precede bounded same-site sitemap nominations, then legacy
fixed proof paths. Read one own sitemap or a non-news page sitemap named by its
index, at most one child level. Accept only contact/about/privacy/impressum paths;
reject cross-domain, query-dependent, news/blog and binary URLs. At most
two sitemap-nominated HTML pages per company across both passes; no extra HTTP,
DNS or time allowance. XML only nominates a URL: the fetched HTML must pass the
same exact-number/identity proof and veto rules. A map/robots failure stays
explicit; no candidate already vetoed is retried. Common privacy aliases precede
redundant bare /om guesses; a late blind alias may remain unchecked at the cap.

Challenge classification checks Cloudflare challenge markers, branded access
security gates (Imperva/DataDome/etc.) and challenge titles. Ordinary recaptcha
contact forms and passive Cloudflare JSD on usable pages are not challenge pages;
visible access gates still block when JSD is present. Challenges on home, proof, historical
proof or sitemap responses stop the walk and record blocked access; they are
never no-proof or an invitation to bypass protections. Source receipts and
attempt/cutoff diagnostics remain available in run.refresh.proof_sitemaps and
website_candidates. The diagnosis distinguishes external DNS/access failures
from actionable discovery/ordering gaps; no proof or robots rule is loosened.

The passive-JSD distinction was checked against [Cloudflare documentation](https://developers.cloudflare.com/cloudflare-challenges/challenge-types/javascript-detections/) on 2026-11-13: JSD is injected into HTML and is separate from an enforced interstitial. We do not execute it, solve challenges, or change access policy; visible/active gates remain blocked.


## Stage T: exact-ID GLEIF and TED (checked 2026-11-13)

GLEIF's [LEI Data Terms of Use](https://www.gleif.org/en/meta/lei-data-terms-of-use) state free access and CC0 1.0 data reuse, with the right to suspend/modify access. [API documentation](https://api.gleif.org/docs) is linked from the official API. `https://api.gleif.org/robots.txt` returned 200: `User-agent: *` and an empty `Disallow`. No key, paid service, search provider or model. RA000472 is Norway's Foretaksregisteret in the [official authority list](https://www.gleif.org/about-lei/code-lists/gleif-registration-authorities-list/registrationauthorities_v1.8.pdf); RA000473 is not silently accepted.

Requests batch 25 company IDs, each in compact and three-group spaced registry form, using comma-separated registeredAs filters plus RA000472, page size 100. Live probes established that compact-only misses BIEN's spaced registration and that comma is OR whereas a pipe is literal. Every returned record is checked again for exact registeredAs, authority, jurisdiction NO and legal-address country NO; no fuzzy/name match. Multiple distinct LEIs for one ID abstain as ambiguous. Entity status, legal-form **code**, initial LEI registration, next renewal and registration status are copied only when supplied; a lapsed LEI is not called active.

Direct/ultimate accounting-consolidation parents publish only from the child's own linked relationship-record endpoint: relationship status ACTIVE, correct relationship type, exact child LEI and typed parent LEI. Reporting exceptions, registration status PUBLISHED alone, and inactive relationships do not prove parents. Parent LEI is a relationship fact, not authorization to crawl or merge parent websites/contacts/jobs. Parent-country or ownership percentages are not inferred.

TED's [official API docs](https://docs.ted.europa.eu/api/latest/search.html) describe unauthenticated public search for reuse. The [API schema](https://api.ted.europa.eu/api-v3.yaml) points to the [legal notice](https://ted.europa.eu/en/legal-notice): procurement notices may be reused commercially or noncommercially unless otherwise noted; editorial documentation is CC BY 4.0. Attribution: European Union / TED, publisher URL, original dates and exact excerpts; no personal contact fields are extracted. The legal notice was readable through the browser search source; direct site requests returned a 202 empty access gate. No bypass. API robots returned 404 (no rules supplied); website robots returned 202 and is treated as **blocked/unknown**, never allow-all. Runtime checks robots afresh before access. Receipt bodies/statuses and hashes are in `reports/r5/stageT/access/`; site terms access limitations are explicit.

[Search field definitions](https://docs.ted.europa.eu/ODS/latest/reuse/field-list.html), [result schema](https://docs.ted.europa.eu/eforms/latest/schema/competition-results.html), and [party references](https://docs.ted.europa.eu/eforms/latest/schema/parties.html) define the extraction. Batch 25 IDs using winner-identifier/buyer-identifier, 36 months of publication dates, contract-award notice types, scope ALL, 100 notices/page; max 10 pages, explicit incomplete state on truncation/cycles/timeouts. Flattened search arrays only nominate XML. Structured eForms must link Norwegian exact national ID to the buyer or selected tenderer through Organization, TenderingParty, LotTender, LotResult (selec-w) and SettledContract; award date must be within 36 months and not future. No name matching, unlinked organization, cancellation or foreign-country match. XML gates/unsupported schemas stay explicit; older TED-schema notices are not guessed into eForms.

Published award facts include title, buyer, reported award date, notice/lot, matched role and notice link, labelled Public procurement award. **No amount is published in this implementation**: notice totals, shared tenders and flattened value arrays cannot establish the matched winner's sole lot amount. This deliberate abstention loses amount coverage, not attribution precision. Publisher XML supplies facts; API search only nominates them.

Both sources are on by default in CLI and library without extra flags. Separate gleif/procurement section states isolate their failures from existing sources. All robots, search, pagination, XML and parent calls consume the same scaled 1850 HTTP / 35-minute hard batch budget and watchdog; per-host serialized starts have at least one second between completions/starts, honoring longer robots Crawl-delay. Request timeouts use remaining budget. 401/403/429 closes that host for the run; no redirects, auth bypass or automatic retry flood. Maximum source bodies 8 MB; current receipt blobs are hashed with retrieval UTC and exact bounded excerpts. Paid cost $0. Development policy/schema probes are retained separately and are not misreported as evaluator-run HTTP.

### Linked legal PDF terms (L2)

The locked `pypdf==7.1.0` dependency is BSD-3-Clause, free local parsing, no model/API charge. Official package and API references checked 2026-11-15: https://pypi.org/project/pypdf/ and https://pypdf.readthedocs.io/en/stable/user/extract-text.html . No library implementation was copied. The official docs note decompression/memory costs; extraction applies context-scoped decoded-stream/work limits in addition to the fetched2MB cap,20pages,200ktext characters and bounded parse wait. No OCR, password bypass or external binary.

Only PDFs actually linked by the candidate site's visible own footer/navigation or fetched legal pages are nominated; same-site robots/TLS/SSRF/politeness and cumulative HTTP limits apply. PDF redirects abstain until their link chain is independently supported. Existing exact-number proof and R4 run on the extracted document; foreign identifiers anywhere in the PDF veto. Original PDF bytes/hash, page index, page-text hash, derived-proof hash, own linking-page hash/anchor and exact excerpt are retained. Derived text is explicitly identified and independently regenerated by verification; it is not presented as original HTML. Image-only/unreadable/encrypted/oversize/unsupported PDFs abstain explicitly.

## X2 owner-declared social profiles

On an already VERIFIED/HIGH single-company website, an Organization/LocalBusiness JSON-LD sameAs node must match the full registry legal name or exact Norwegian orgnr vatID/identifier. Conflicting owner IDs/countries, foreign owner URLs, Person/founder URLs (including separate scripts), hidden/article/client/staff/agency contexts and group/parent contexts abstain. Relative owner URLs resolve on the same site; social profile URLs must be supported platform profile URLs. Numeric LinkedIn remains limited to the existing own semantic header/footer rule.

A contact/imprint page may also declare a profile in its own R1 footer/contact Follow us/F?lg oss block, with R4 first and the same exclusions. At most one visible own navigation/footer linked contact page is fetched after site proof, within existing robots, public-IP/TLS, politeness and per-company/global limits. It feeds social extraction only. No social platform is requested. Each new claim retains the exact raw owner declaration, official legal-name and verified-site proof dependencies, retrieval time and source hash; verify_output replays them independently. Unsupported or cancelled optional work remains explicit. This introduces no new API or licence claim over company-owned content.

## P0 official-source outage handling

Brreg, NAV and GLEIF transient DNS/connect/timeout/protocol/5xx requests may retry twice with5s/20s backoff and longer Retry-After, only while the existing request/deadline budget permits. Existing authentication/robots/URL refusals do not become positive evidence; NAV secret bodies and Authorization headers stay out of storage/logs. The accounts copy-years shared429cooldown and ordinary429retry bound remain. Startup HEAD reachability checks are bounded to45seconds/?5seconds per attempt and count as requests.404/405means reachable, not usable company data. Failed health checks and unresolved requests appear in official_source_outages; section failures stay explicit. Zero valid identifiers means no probes. No proof tier or rate/scope limit is relaxed.

Previously supported HIGH/PDF website claims may verify against their original exact registry/page receipts only when explicitly carried_forward. They retain original times/hashes and stale display; fresh claims cannot use carried identity through this path. Fresh-state refresh verification still needs the immutable historical proof bodies (as in the offline refresh harness); no source/result cache is treated as current proof. Missing official legal-name dependencies cause social abstention, never a match between missing names.

## Stage S: exact-ID official sources (checked 2026-11-16)

Each candidate source was checked for licence/terms and robots before any code. Receipts (robots files, schema/code lists, probes, with status, size and SHA-256) are in `reports/r5/stageS/access/manifest.json`. A fact is published only when the source's own record carries our exact organisation number, or a registry-proven subunit number mapped to the parent. Failures stay explicit states; no date or amount is invented.

### S1 Wikidata — skipped (robots)

Wikidata data is CC0, but both machine routes are disallowed for all user agents. `https://query.wikidata.org/robots.txt` has `User-agent: *` / `Disallow: /sparql`, and `https://www.wikidata.org/robots.txt` has `User-agent: *` / `Disallow: /w/` and `Disallow: /api/` (the Action API is under `/w/api.php`; only a mobile-view action is allowed). This project treats robots rules as binding for automated access, so neither the SPARQL query for P2333 nor the API is used, and no snapshot is built. The full entity dumps (dumps.wikimedia.org) are tens of GB, which is impractical to transfer and filter here. No Wikidata website candidate, social ID or ticker/ISIN is published.

### S2 Støtteregisteret (state-aid awards) — implemented

Brønnøysundregistrene's Støtteregisteret is listed on data.norge.no with the search distribution under **NLOD 2.0** (`https://stotte.brreg.no/`); the API distribution lists no licence of its own and is the machine form of the same register. The published OpenAPI document (`https://stottetiltak-registerinfo-api.app.brreg.no/v3/api-docs`) declares a bearer scheme, but the search endpoint answers unauthenticated requests (receipt `stotte_search_noauth`). No credential is used or bypassed; a 401/403/429 closes the source for the run. The API host serves no robots.txt: two requests to `/robots.txt` were connection-reset (receipts `stotte_api_robots*`). That is treated like a 404 (no rules), one attempt per run, and recorded on the request log as `robots_unserved`. `stotte.brreg.no/robots.txt` redirects into the web app and is not a robots file.

Runtime: `POST /api/v1/soek/stoettetildeling?pageSize=100&page=N` with exactly `[{"field":"STOETTEMOTTAKER_ORGNR","value":<orgnr>,"matchType":"EXACT_MATCH"}]`, at most 5 pages (explicit `state_aid_pagination_limit`), 1 s per-host politeness, inside the shared scaled HTTP/time limits. A record is published only when its type is an award (`stoettetiltakstype.stoettetildeling*`), its status is `stoettetiltaksstatus.registrert` (rejected, unlawful-aid and incorrectly-registered statuses abstain; code list receipt `stotte_status_nested`), it has **exactly one** `rolletype.stoettemottaker` holding our exact orgnr (a shared award is not attributed), exactly one `rolletype.stoettegiver` with orgnr and name, and an ISO `tildelingsdato` that is not in the future and lies within 36 months. The published value carries award id, date (labelled as the registered award date), granting authority and orgnr, and scheme/instrument codes when present. The amount and currency appear only when `tildeltBeloep` supplies both, or as a registered range from `beloepsintervall`; otherwise there is no amount. Every scalar is a JSON-pointer receipt into the saved response, and `verify_output` re-derives the value from it. Family `state_aid`, shown under activity. Attribution: Brønnøysundregistrene, Støtteregisteret, NLOD 2.0.

### S3 Research Council of Norway and SkatteFUNN projects — implemented (bundled snapshot)

Sources, all **NLOD 2.0** per their data.norge.no entries:
- `soknader2` (applications and granted projects), `https://raw.githubusercontent.com/Forskningsradet/open-data/main/datasets/soknader2/dataset.csv`, updated quarterly; field definitions in the repository's `fields.csv`.
- The two SkatteFUNN application lists, May 2024–September 2026 and 2002–2024: `https://www.forskningsradet.no/siteassets/skattefunn/tall/260902-webliste-skattefunn.xlsx` and `.../skattefunn-innsendte-soknader-2002-2024.xlsx`.

`raw.githubusercontent.com/robots.txt` is 404 (no rules). `www.forskningsradet.no/robots.txt` disallows only `/episerver/`, `/EPIserver`, `/utils/` and `*/Download`, so `/siteassets/...` is permitted (receipt `forskningsradet_www_robots`). The repository has no LICENSE file; the licence comes from the national data catalogue. Attribution: Norges forskningsråd.

`scripts/build_official_snapshots.py research --build-day 2026-11-16` builds `src/signalpost/data/research_projects.json.gz` (907,295 bytes, SHA-256 `ab80455b96200e768ae9e97bc327d1610f656a9a754282b0e83ed5e5d858da21`) from the downloaded files, whose URL, UTC download time, SHA-256, size, licence and row counts are embedded:
- **RCN:** 7,491 of 88,268 rows, where the owner type is Organisasjon, the phase is Bevilgning/Avsluttet (rejected and pending applications excluded) and the end year is within the 36-month window.
- **SkatteFUNN 2024–2026:** 4,338 of 7,934 rows, with `Godkjent` = JA and the decision date in the window.
- **SkatteFUNN 2002–2024:** 1,251 of 70,599 rows, with `Søknad godkjent` = JA and `Søknad avslått` = NEI.

Only a fixed list of non-personal columns is copied verbatim; no project-leader name or gender and no free-text summary. Runtime reads the bundle locally, with no network. A claim needs the record's own orgnr column to equal ours. RCN projects publish title, start/end year (date precision **year**, never a guessed day), phase, programme (`aktivitet`), instrument and `tildelt_belop` as given ("granted total for the project period as given; unit not stated in source", with no currency invented). SkatteFUNN approvals publish title and the decision date (`Vedtaksdato`), decoded from the spreadsheet's Excel date serial; the raw serial is kept beside it and SkatteFUNN publishes no amount. Each record's exact bundled bytes are the stored evidence body, with JSON-pointer receipts. `verify_output` requires that body to be byte-identical to a bundled record of that orgnr from the named source, then re-derives the value. Family `research`, shown under activity. The bundle is a dated snapshot; rebuild it with the script on newer downloads.

### S4 Finanstilsynet registry — implemented; DiBK sentral godkjenning — skipped (robots)

Finanstilsynet's open registry API (`https://api.finanstilsynet.no/registry/v2`; OpenAPI `swagger/v2/swagger.json`, receipt `finanstilsynet_swagger_v2`) is listed on data.norge.no under **NLOD 2.0**. It documents rate limits (1,000 requests per 60 s per IP; report endpoints 5/min) and needs no credential. `api.finanstilsynet.no/robots.txt` is 404 (no rules); the web host's robots allows all with `Crawl-delay: 10`, and only the API host is used. Runtime per eligible company:
1. `GET /legal-entities/search?query=<orgnr>&entityType=Company&pageSize=50&page=1`. Exactly one hit must have `organisationNumber` equal to ours; more than one is `ambiguous`, none is an explicit sourced "none", and a truncated result fails explicitly.
2. `GET /legal-entities?ids=<legalEntityId>`. The record's own `organisationNumber` must again equal ours.

Each licence row becomes one of two clearly separated claims. A row with `serviceProviderType` `Licensed` and `licensedEntity` = this entity is **our own licence**. A row with `Agent` and a named other `licensedEntity` is a **registration as agent for that principal**, never presented as our own licence. Other provider types abstain. The licence code and name, and `registeredDate` when parseable (labelled as published), are copied. Person entities are never queried. Family `licences`, shown as company detail. Attribution: Finanstilsynet, NLOD 2.0. The register states it may contain errors and excludes revoked licences, so absence is not proof of no licence history.

DiBK's central approval register (`sgregister.dibk.no/api/enterprises/{orgnr}`) is documented as open, but `https://sgregister.dibk.no/robots.txt` has `User-agent: *` / `Disallow: /api/` (receipt `dibk_sg_robots`). The user's condition was "only if robots allows", so it is not used.

### S5 Mattilsynet Smilefjes inspections — implemented (bundled snapshot)

The dataset "Smilefjestilsyn på serveringssteder" is **CC BY 4.0** per data.norge.no. Its distribution is `https://smilefjes.mattilsynet.no/api/tilsyn.csv` (nightly; downloaded 2026-11-16T11:01:01Z, 15,845,528 bytes, SHA-256 `29adbcf5…`, ETag `"6afa8f13-f1c898"`). `smilefjes.mattilsynet.no/robots.txt` is 404 (no rules). The older hotell.difi.no distribution is marked unpublished/unmaintained and is not used. The catalogue defines `orgnummer` as the key linking the inspected place to its owner in Brønnøysundregistrene, `dato` as the inspection date (ddmmyyyy), and the 0–3 grade scale: "0: Ingen brudd på regelverket funnet. Stort smil. 1: Mindre brudd på regelverket som ikke krever oppfølging. Stort smil. 2: Brudd på regelverket som krever oppfølging. Strekmunn. 3: Alvorlig brudd på regelverket. Sur munn." The visit type is described only as "ordinary or follow-up", with no numeric mapping, so its code is published raw.

`scripts/build_official_snapshots.py inspections --build-day 2026-11-16` builds `src/signalpost/data/food_inspections.json.gz` (749,247 bytes, SHA-256 `0134010f9c2c803e6e4b39b61e8937e71434fd4676a9db5fa70f4ddfd6fcef8f`). It keeps 13,813 of 45,164 rows: a mod-11-valid `orgnummer` and a date within 36 months, with ten fixed columns copied verbatim. A claim is published only when the row's `orgnummer` equals our orgnr, or equals the orgnr of a subunit proven by the current registry `underenheter?overordnetEnhet=<ours>` response (no carried-forward subunit). In the subunit case the claim cites that subunit claim's evidence, and `verify_output` rechecks the parent link in the saved registry body. The date is the published inspection day and the grade is the published value with the catalogue's meaning. Family `inspections`, shown under activity. Attribution: Mattilsynet, CC BY 4.0.

### S6 Brreg signatur/prokura — skipped (not in the open API)

The open Enhetsregisteret role-group code list (`https://data.brreg.no/enhetsregisteret/api/roller/rollegruppetyper`, receipt `brreg_rollegruppetyper`) has 21 types and no SIGN/PROK group. The saved `/roller` responses for all 100 frozen-baseline companies contain only those types, and every returned group is already published. Signature and prokura are served only through Brreg's authorised API (Maskinporten), which this project does not use. Nothing is invented from the role groups that are present.
