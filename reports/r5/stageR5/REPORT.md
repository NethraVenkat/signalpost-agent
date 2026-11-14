# R5 — Registry-declared domain and exact publisher legal name

Branch revision/r5; parent 23838192. Author/committer Nethra Venkat. No push. No paid models, search or APIs. R3 is not implemented in this stage.

## Gap diagnosis

Before R5: 13/72 declared-homepage companies publish a website; 59 gaps. Primary causes: {"conflict": 6, "redirect_refused": 9, "fetched_without_proof": 29, "connect_timeout": 6, "robots": 6, "DNS": 2, "HTTP": 1}. Full per-company chains, publisher fragments, R4 conflicts and registry receipts are in declared_gap.md/json. Diagnosis used only accepted R4 saved responses (zero extra HTTP). Refused redirects retain unknown target/final-host states when historical Location headers were not saved.

## Proof decision

`registry_declared_publisher_name` is an explicit HIGH proof type. It requires the complete registered legal name, including its suffix, in a permitted R1 publisher fragment and a candidate matching the registered homepage hostname (www/apex and HTTP(S) variants). Only case/whitespace and æ→ae, ø→o, å→a spelling normalization apply. No suffix removal, punctuation removal, fuzzy names or body-only mentions. All R4/previous vetoes remain ahead of acceptance. The old exact-number VERIFIED and corroborated HIGH routes remain distinct.

A declared redirect nominates a destination under the same HTTP/time/hop/SSRF/TLS/politeness limits, with robots checked at each authority. Cross-registrable-domain publication requires another explicit registry domain (registered email domain) or the exact company number in the destination publisher block. The redirect alone is never proof. Once-only candidate reuse is unchanged; the page cache additionally distinguishes redirect permission. N3/public DNS fallback is dropped; hiring is unchanged.

Every new-tier claim retains the publisher fragment/location, nomination/proof URL and registry homepage plus the authoritative registry evidence dependencies. Independent saved-evidence verification checks exact registry source fields, R4, the publisher name/domain rule, hashes/verbatim spans and published URL authority. The old registry-contact gate cannot override a successful new R5 rule. Social extraction/rules are unchanged.

## Fresh seven-flag results

Declared-homepage recall means companies with a registry homepage and a published VERIFIED/HIGH website; it is a declaration-based recall metric, not a human ownership precision verdict. Denominator is 72 across the six fixed samples.

| Seed | Total sites R4 → R5 | Declared recall R4 → R5 | Declared N | HTTP R4 → R5 | Wall seconds R5 |
|---|---:|---:|---:|---:|---:|
| 20261017 | 5 → 5 | 4 → 4 | 11 | 696 → 695 | 403.469 |
| 20261113 | 4 → 6 | 3 → 5 | 11 | 777 → 785 | 423.578 |
| 20261114 | 3 → 4 | 3 → 4 | 8 | 723 → 726 | 336.047 |
| 20261115 | 6 → 8 | 1 → 3 | 14 | 748 → 755 | 411.625 |
| 20261116 | 5 → 6 | 2 → 3 | 17 | 787 → 787 | 500.672 |
| 20261117 | 7 → 7 | 0 → 0 | 11 | 734 → 749 | 368.421 |

Total sites 30 → 36; declared recall 13/72 → 19/72 (26.39%). Added: {'website': 8}; removed: {'website': 2, 'social': 2}. New website proof types: {'registry_declared_publisher_name': 6, 'orgnr_on_page': 2}. Live changes under older tiers are reported separately from gains attributable to R5.

Each final sample: exit 0, 100 ordered terminal envelopes, generated site, all five cited briefing topics, zero unsupported values, HTTP ≤1,850, completion under 35 minutes, provider cost $0. Exact argv/new run IDs/fresh working directories, input/bulk hashes, source manifest and validation receipts are in seed*/. Final source remained unchanged throughout all six measurements.

Test gate: 1016 passed in 370.92s (0:06:10). Positive and negative tests cover publisher regions, hidden/body/client/article/credit exclusions, suffix/punctuation mismatches, R4 precedence, cross-domain redirects, destination robots, exact publisher number, source receipt/URL tampering, and legacy cache/DNS/retry behavior.

## Hand check and resource disclosure

Every added or removed website/social URL, orgnr, legal name, tier, complete publisher text, exact raw excerpt, source URL/date/hash and registry receipt is listed in new_websites.md and items.json. Saved-evidence rechecks of every new item returned correct; this does not replace independent human ownership review. No doubtful item was silently removed.

Unaccepted pre-contact-gate trial: 699 HTTP, 369.266 reported completion seconds, 5 websites, declared recall 4/11, $0; retained under trials/pre_contact_gate/. Driver was stopped before another sample began; its current CLI child finished mandatory outputs and independently passed validation, but its exit code was not captured. It is not used as an accepted final measurement.

A second unaccepted suite found a pre-existing HIGH localization problem: stripping punctuation from the proof token prevented localization of DICA PROFIL & YRKESKLÆR AS even though its exact full publisher name satisfied R5. Candidate proof now falls back to the authorized R5 receipt when the older HIGH token cannot be localized; it does not invent or weaken an excerpt. The regression and full suite are green. The four superseded runs, source manifest and resource totals are retained under trials/pre_localization_fix/. Their last child was allowed to finish outputs after only the driver was stopped; its exit code is unknown. None is substituted for a final-source sample.

A later agency-credit recheck reproduced an R1 bug: removing a credit marker before joining a footer could leave the agency name in a sibling node. Extraction now preserves the marker while joining children and excludes traversal of credit siblings, including nested logos/copyright. Six split-node credit fixtures protect the new positive tier. trials/pre_split_credit_fix retains two completed runs (697 + 778 HTTP, $0), and a third incomplete run with no report/empty execution receipt after disk exhaustion. Its final exit/request totals are unknown; no output is invented.

Lossless workspace-only disk recovery: byte-identical saved blobs were SHA-256 checked and atomically replaced with hard links to identical local blobs. Every evidence path and byte remains available. blob_deduplication.json records reclaimed space/method. No other repository code/data was read, copied or modified.

Conservative withholding: PROFINOVA AS 899177932 has a matching title but its saved owner body is only a 49-character frame fallback; embedded publisher content is not fetched/proven and standard proof pages return 404. The existing short/script-shell guard remains. No title-only acceptance of that unverified frame is added. Saved-page eligibility/localization preflight found six eligible gap companies and zero remaining localization failures; this offline preflight is not a fresh measurement.

The previous completed R4 measurement has 30 total sites (including the documented LOOPYTY live-source recovery); W0 had 29. The declared-homepage baseline remains 13/72 in both. No proof-label relabelling is counted as a newly gained URL.
