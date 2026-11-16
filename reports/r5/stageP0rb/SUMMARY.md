# P0 re-baseline on new machine

New local reference for later stages, measured on 2026-11-16 on a new laptop after a fresh clone of `revision/r5`. The runtime is the P0 commit plus the path-only privacy commit `d54f9db`. Earlier run folders (`.data/`) were not transferred, so **no before/after comparison** is made against them; these numbers are a new starting point, not a delta. No paid models or search; cost $0.

## Inputs (rebuilt and verified)

| Input | Result |
|---|---|
| Six frozen cohorts committed in `reports/` (companies + registry CSV per seed 20261017/1113/1114/1115/1116/1117) | All 12 files match the SHA-256 recorded in the X2 settings; used as-is |
| Universe archive, re-downloaded 2026-11-16 from `https://builderr.ai/signalpost-company-universe-2025.jsonl.gz` | **Unchanged**: archive `1c89710e…0a5f0384`, content `b82d6a3e…cd01bc838`, 411,160 rows; seed 20261017 reproduces `baseline/companies.jsonl` byte-for-byte (`7d59169d…`) |
| Brreg enheter bulk | **New snapshot**, not the 13 Oct 2026 file: `https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv`, requested 2026-11-16T06:07:51Z, server file `enheter_2026-11-16T04-25-21.340365166.csv.gz`, 155,307,711 bytes, SHA-256 `56922f51839e7ed3f3c9adde50dbcfa375202d7bc5aa998d9572158e228693e1`, 1,181,260 entities. Kept locally for future full-snapshot extraction (P2); not used by these runs |
| Shipped rarity bundle / NAV index | Match the P0 source manifest (rarity `900882536a57…`, NAV `ba4d5df8a8fa…`); not rebuilt |
| Environment | `uv sync --frozen --dry-run`: no changes; Python 3.12.15 |

## Smoke test — 20 companies, exact seven flags

`tests/fixtures/ci20.jsonl` / `ci20.csv` (the CI fixtures), fresh working directory, then `scripts/check_live_run.py --count 20`: exit 0, 20/20 `complete`, 176 / 370 HTTP, 118 s wall (scaled limit 420 s), $0. Checker: schema valid, 0 unsupported synthesis/briefing values, five briefing topics for 20/20 companies, site verified, largest page 241,827 bytes. Receipts: `smoke20/`.

## Six-sample measurement — exact seven flags, fresh state, one sample at a time

| Seed | Sites | Declared recall | Social cos/claims | Activity claims | Brands | Facts | HTTP | Process s | Largest page | Gates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 20261017 | 8 | 5/11 | 4/10 | 1,392 | 10 | 13,560 | 973 | 733.5 | 239,845 | pass |
| 20261113 | 6 | 5/11 | 1/2 | 1,341 | 10 | 13,993 | 927 | 666.0 | 224,442 | pass |
| 20261114 | 6 | 4/8 | 4/4 | 1,256 | 10 | 13,464 | 950 | 605.8 | 222,891 | pass |
| 20261115 | 9 | 4/14 | 4/4 | 1,153 | 8 | 13,287 | 951 | 561.1 | 222,052 | pass |
| 20261116 | 8 | 4/17 | 0/0 | 1,472 | 15 | 13,787 | 1,007 | 653.4 | 229,166 | pass |
| 20261117 | 9 | 1/11 | 4/7 | 1,243 | 25 | 14,068 | 907 | 575.1 | 249,037 | pass |
| **Total** | **46** | **23/72** | **17/27** | **7,857** | **78** | **82,159** | **5,715** | **3,794.9** | — | **all pass** |

Gates checked per sample (`totals.json`): exit 0; exactly seven flags; 100 ordered terminal envelopes; schema valid; 0 unsupported synthesis/briefing values; all five briefing topics and complete briefing contracts for 100/100; site available with every profile page below 250,000 bytes; HTTP ≤ 1,850 and process time ≤ 2,100 s (the scaled hard limits recorded in each report); $0. All four official-source health probes were reachable in every sample. The runtime source manifest (`source_manifest.json`, working-tree and LF hashes) was identical before and after every sample.

The R7 items human-reviewed as correct reappear with unchanged proof tiers: PEAK LANDSCAPES website (`publisher_name_registered_place`) and Instagram (`own_header_footer_exact_name_v1`) in 20261017; CRAFTING HOUSE (`registry_declared_live`) and MELDAL MILJØANLEGG (`orgnr_on_page`) in 20261116. Every published website/social/brand item for each seed is listed in `seed*/counts.json` → `identity_items`. Because nothing is compared, these are not reviewed as "new" additions; later stages compare against this reference.

Exact command per seed (`seed*/settings.json`): `python -m signalpost.cli run --organisations … --bulk … --output … --profiles-output … --report … --run-id r5-stageP0rb-seed<seed>-final --expected-count 100`, run from a fresh `.data/r5/stageP0rb-<seed>-final` directory. Envelopes, profiles, state and sites remain local under those directories (hashes in `counts.json`). Each wait was a harness-tracked sequential command; no sample was detached, stopped or retried.
