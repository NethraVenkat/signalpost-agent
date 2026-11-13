# Release v4 check - Revision 5 / v1.2.0

**PASS for the requested technical release checks.** No new application features, push or publication. The package version is 1.2.0; the local annotated release tag is v1.2.0. All release changes are authored by Nethra Venkat <nethravenkat510@gmail.com>.

## Exact tested revision and clean installation

Exact clean-clone source commit: **`3168e29b7224270ff1b3829ddad4fc596d1d6705`**, revision/r5 HEAD at clone time. Git application source tree: `3edf64c9f569b5ff6dfaf90a6f52ec0305af818b`.

Clone: `C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo`. It was created with `git clone --no-local --single-branch --branch revision/r5` from the local repository, with no shared/hardlinked Git objects and no copied runtime state. The initial checkout was clean. `uv sync --frozen` created its own .venv; the recorded successful frozen-sync exit is 0. `clean_clone.json` records the interpreter, prefix, loaded signalpost module path and lock fingerprint, proving tests loaded the clone rather than the original workspace. All sampling, extraction, smoke/verification commands, version updates and pytest ran from this clone.

The two requested smoke runs tested that exact source commit with its then-installed metadata version 1.1.1. After the smokes, pyproject/README and the editable package entry in uv.lock were bumped to 1.2.0. A second frozen sync succeeds and reports installed version 1.2.0. **Application source bytes and every third-party dependency version are unchanged**, verified by the complete source manifest and installed-distribution comparison. The full 1.2.0 test gate is **838 passed in 149.49s**. The release commit contains metadata/docs/evidence changes only; the annotated local tag identifies that commit and records its exact SHA in its annotation. No source behavior was changed between the measured revision and the tagged release.

## New daily-test draw

The existing 411,160-company universe archive and bulk snapshot are hash-checked before use. The sample is a new uniform random draw of 100 using seed **20261113**, with **zero overlap** with the earlier frozen 100. Identity uses the supplied frozen registry snapshot; live source retrieval dates remain separate in receipts. This is not presented as a newly downloaded universe. All 100 sampled identifiers are valid/unique and all 100 have extracted bulk rows.

- Universe archive SHA-256: `1c89710e5b01f8617e86d09fbdff4a52f2f8dbbba297e74f7164b5984f5a0384`.
- Full registry snapshot SHA-256: `5b0df27c5567a655320b8dfb8975049b76c46ba93d748a8a763f8db7050b7862`.
- New sample SHA-256: `34d436c3bec6b5677bd2c8bab11a178192965c828c56722b571d0ba84547903c`.
- Extracted 100-row CSV SHA-256: `5b92dd3a9015a2f6a8ad9eaf6d5796f779669a382effdb59bbb9260d803dbd90`.

## Smoke results

Both commands use exactly the seven evaluator flags, with default enrichment/site/caps, fresh independent working directories and default state/. No cap, feature, synthesis or state-dir flag was added. Paid search is explicitly disabled through the recorded environment; template synthesis is the default.

| Check | Daily new 100 | Edge 10 rows |
|---|---:|---:|
| Terminal envelopes | 100 | 10 |
| Unique input identifiers | 100 | 9 |
| Invalid identifiers | 0 | 2 |
| Duplicate rows | 0 | 1 |
| CLI exit | 0 | 0 |
| HTTP requests | 961 | 166 |
| Resolved HTTP ceiling | 1850 | 166 |
| Wall seconds | 302.996 | 104.455 |
| Runner seconds | 276.812 | 102.140 |
| Accepted company websites | 4 | 0 |
| Owned social URLs | 2 | 0 |
| Contacts | 8 | 0 |
| Jobs | 1 | 0 |
| Activity claims | 97 | 0 |
| Available source facts | 9677 | 728 |
| Runtime provider cost USD | 0.000 | 0.000 |
| Input order verified | yes | yes |
| Output verifier exit | 0 | 0 |
| Unsupported synthesis/briefing values | 0 | 0 |
| All five briefing topics | 100/100 | 10/10 |
| Site generated | 100 profiles / 102 pages | 9 profiles / 11 pages |

The daily wall time is **302.996s (about 5.05 minutes)**, well under 45 minutes and inside the stricter default 35-minute ceiling. It uses 961/1850 HTTP requests and completes outputs/site inside the effective budget. Its four accepted company websites comprise **three VERIFIED exact-number sites and one HIGH corroborated site**; the existing HIGH rule is unchanged and remains labelled. The two social URLs belong to one company; no social platform was fetched. One exact-company/subunit job is verified. Receipts and financial/synthesis checks pass independently for all 100 envelopes (4,361 financial values, 169 derived metrics, 389 source blobs).

The edge input is seven distinct valid companies, invalid `123456789` and `923609017`, plus one repeated valid identifier, interleaved as saved in companies10.jsonl. All ten envelopes retain the exact input order; the repeated envelopes are identical. Both invalid IDs terminate failed, have no available facts and cause zero HTTP requests. Their nine-digit filename-safe identifiers retain explicitly failed placeholder pages; the site therefore has nine unique profiles (seven valid plus two failed placeholders). The scaled unique-input request ceiling is 166 and is hit without exceeding it; partial source coverage remains explicit. Exit 0 and verifier success do not claim every section is complete.

The release checker originally expected checksum-invalid profiles to be omitted. That assertion was corrected to the existing placeholder behavior, then all checks and the verifier were rerun against the same preserved edge output without another crawl or envelope rewrite. The application was not modified to make the checker pass.

## Commands as executed

Run from each cwd in daily.json / edge.json, which were new empty working directories. Use new directories when replaying; saved raw evidence is intentionally retained. Initial setup was `uv sync --frozen` in the clone. Sampling and extraction commands/logs are in sample.json/txt and extract.json/txt. These are the actual seven-flag invocations:

### daily

```powershell
& 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.venv\Scripts\python.exe' '-m' 'signalpost.cli' 'run' '--organisations' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\companies100.jsonl' '--bulk' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\registry100.csv' '--output' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\envelopes.jsonl' '--profiles-output' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\profiles.jsonl' '--report' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\report.json' '--run-id' 'release-v4-daily-seed20261113' '--expected-count' '100'
```

### edge

```powershell
& 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.venv\Scripts\python.exe' '-m' 'signalpost.cli' 'run' '--organisations' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\companies10.jsonl' '--bulk' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\registry100.csv' '--output' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\edge\envelopes.jsonl' '--profiles-output' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\edge\profiles.jsonl' '--report' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\edge\report.json' '--run-id' 'release-v4-edge-seed20261113' '--expected-count' '10'
```

`daily-verify.json/txt` and `edge-verify.json/txt` preserve the independent scripts/verify_output.py commands/results, including membership/order, schemas, stored-body hashes, verbatim spans, financial inputs/arithmetic, complete briefings and scorer mirrors. The fresh runs and original bodies remain in the preserved clone under .data/release-v4/daily and edge. Source/output hashes, exact argv, elapsed times, full original reports, dependency licences, installed-version evidence and pytest output are tracked alongside this report.

## Models, APIs, licences and expected cost

- **Models:** deterministic local template synthesis and explicitly labelled arithmetic only; no external LLM, embeddings or model API. Search queries and model calls are both zero. SSB industry-title mappings and the Public Suffix List are bundled data, not model guesses.
- **Registry APIs/data:** supplied bulk CSV, public Brreg organisation/roles/subunit/accounts APIs and bounded registry update feeds at data.brreg.no. Attribute Bronnoysundregistrene under [NLOD dataset terms](https://www.brreg.no/en/use-of-data-from-the-bronnoysund-register-centre/datasets-and-api/) and [NLOD 2.0](https://data.norge.no/nlod/en/2.0).
- **Hiring:** official pam-stilling-feed.nav.no public token/feed/detail APIs; exact live employer identifiers authorize publication. NAV describes the service as free and requires updates/removal of changed/inactive ads under its [API terms](https://arbeidsplassen.nav.no/vilkar-api). Published fields exclude ad descriptions/contact persons.
- **Websites:** bounded company-owned HTML and same-domain feeds/sitemaps, with robots, per-domain politeness, pinned public-IP/TLS checks and cumulative budgets. Website excerpts retain their owners' terms; MIT/NLOD is not asserted for that content. Social URLs are extracted links, not platform scraping.
- **Bundled classification data:** attribute Statistics Norway/SSB; its [public API policy](https://www.ssb.no/en/api) and [licence page](https://www.ssb.no/en/diverse/lisens) identify CC BY 4.0. Runtime makes no SSB calls.
- **Code/dependencies:** application code/docs use the repository MIT licence (Copyright 2026 Nethra Venkat). Frozen direct dependencies are httpx 0.28.1 (BSD-3-Clause), pydantic 2.14.1 (MIT), tldextract 5.4.0 (BSD-3-Clause). Transitive/dev licences and exact versions come from installed METADATA in dependency_licenses.json; certifi and the bundled PSL retain MPL-2.0 (PSL licence/version/fingerprint in psl_snapshot.json). Installer/build tools are uv 0.13.0 and pinned Hatchling 1.29.0. No application code was copied from another repository.
- **Expected runtime provider/API cost: $0; measured: $0 for both runs.** No paid key/provider, purchased search, external model, deployment or publication was used.

Official source/licence references above were checked on 13 November 2026. Registry field values and company website/social URLs are not promoted beyond their recorded proof tiers.

## Hand-check inventory and release boundary

[urls.md](urls.md) lists every semantic website/social URL claim from the daily run with organisation number, legal name, proof tier, field, exact excerpt, source URL, retrieval time and hash. It separates four ownership-accepted websites/two social URLs from 21 registry homepage field assertions; registry assertions are **not ownership proof**. urls.json retains claim IDs, all evidence IDs, supporting receipts and proof details, including the HIGH site's corroboration chain. Hand-check the HIGH site (995194163) and SUNNCOM's own-footer numeric LinkedIn link (918031502) in particular.

Both the normal and budget-limited invalid/duplicate runs meet the requested technical gates. Source failures and incomplete sections remain recorded in the original reports; no live recall target or official score is claimed. A local v1.2.0 tag is the handoff, not publication. No new features and no push.
