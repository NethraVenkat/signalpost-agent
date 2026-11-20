# S1: dated registry/status events

S1 uses only existing exact-company responses from `data.brreg.no/enhetsregisteret/api/oppdateringer/enheter`; no new host or production HTTP request. No announcement-site access and no legal-announcement text or dissolution inference. First-party documentation: [Enhetsregisteret API](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html), NLOD.

## Existing integration

Change feeds are fetched once per run in bounded company/subunit batches and merged with role updates. Original response bytes are stored by SHA-256. Exact orgnr and proven parent scope control attribution. Existing timeline claims carry URL, UTC retrieval time, hash, locator and verbatim spans. The newest 50 events per company are retained by the pre-existing scope; S1 reuses those receipts and does not widen acquisition or time budgets.

## Real fields and meanings

| Response field | Used meaning |
|---|---|
| `organisasjonsnummer` | Exact entity identifier |
| `oppdateringsid` | Event identifier, not a status |
| `dato` | API publication timestamp; not legal effective date |
| `endringstype` | Documented change-type code |
| `endringer[].op` | Patch operation |
| `endringer[].path` | Changed entity-field path |
| `endringer[].value` | Explicit new value, when supplied |

The documented `endringstype` values are Ny (added to Enhetsregisteret), Endring (changed), Sletting (deleted from Enhetsregisteret), Fjernet (removed from Open Data; copies must remove entity), and Ukjent (unknown type). Unknown codes retain their raw code/date and neutral label. There is no documented top-level dissolution/liquidation announcement code or legal-effective-date field in the update response. S1 does not invent one.

The entity schema's documented status fields may appear as patch paths: `konkurs`, `konkursdato`, `underAvvikling`, `underAvviklingDato`, `underTvangsavviklingEllerTvangsopplosning`, `slettedato`, `tvangsavvikletPgaManglendeSlettingDato`. Only explicit boolean/date/remove patch values publish, with neutral Registered status field changed labels. No name or arbitrary free-text value is copied. Saved-real header/status fixtures exclude other fields, clearly identify their projection scope and preserve original response hash/locator metadata; they are not represented as original byte-identical responses.

## Offline final500e measurement

Original application/run `40813fe`; seed 20261126. Original envelope SHA-256 `217314e5ec17ff29b13905ac264ee3a9fe2a8ff0051975670f825cfc61a27da9` remains unchanged. The original live run is not repeated or relabelled as an S1 live measurement.

| Metric | Result |
|---|---:|
| Cohort companies / companies gaining dated events | 500 / 500 |
| New dated event claims / independently source-verified | 4,156 / 4,156 |
| Companies with specific deletion/status-field events | 6 |
| Specific deletion/status-field events | 8 |
| Types: Endring / Ukjent / Ny / Sletting | 3,568 / 499 / 87 / 2 |
| Explicit changed status paths | underAvvikling: 6; underAvviklingDato: 6 |
| Added production HTTP requests | 0 |
| Local projection wall | 1.2993 s |
| New-claim source replay wall | 1.3438 s |
| Full offline site render wall | 20.5034 s |
| Largest profile HTML | 249,279 bytes (<250,000) |
| Original envelopes changed | No |

The measured runtime delta is only the additional local projection step, not an end-to-end network/live-run comparison. No change to the fixed 2,100-second budget, finalisation reserve or seven flags. Every S1 row is deferred to company-local data through the existing loader/overflow path; 500 HTML profiles rebuilt under the cap. A company gaining a generic dated registry event does not mean it gained a formal announcement or a specific legal-status transition. The six-company/eight-event subset is reported separately to avoid that overstatement.

## Failure handling and verification

Normal operation does no live S1 acquisition; source bodies come from the existing run-local blob cache. Upstream feed failure/incomplete state propagates to S1 even when earlier verified facts survive. The explicit direct-acquisition path is unused by runner, but requires a counted robots/network exchange before company data, restricted to data.brreg.no. RFC9309: 2xx parse; 4xx allow; 5xx/reset retry twice within shared politeness/budget, then fail closed. Unit tests cover reset-then-200, repeated resets, 404, repeated 503, Disallow, evidence completeness, undocumented-code fallback, tampering, wrong company, upstream outage, no additional runner requests, real saved header projections and 100 local deferred rows.

[Measured counts/timing scope](measurement.json) | [Offline measurement driver](measure.py). The driver requires the saved original final500e run, blocks network and does not modify original outputs. Full-suite and privacy receipts follow below after completion. No tags or push.

Full pytest: **1,489 passed in 959.55 seconds** ([receipt](pytest.txt)). Initial full run had one equivalent-timezone refresh observation failure, preserved in [pytest-first.txt](pytest-first.txt). The correction uses the existing registry-event instant normalization for S1 comparison only, retaining original date/evidence text; its focused refresh and S1 checks passed 19/19. Final privacy receipt follows in [privacy.txt](privacy.txt).

Final privacy guard: **5 passed in 38.68 seconds**. No additional person names or local home paths were added to S1 source, fixtures, claims or reports. No live company-data request, tag or push was made.
