# CI live-20 repair and human review

Fresh local clone at 1e93023, uv sync --frozen, then the original workflow run and verifier reproduced the failure: run exit 0, 20 envelopes, 140 HTTP / 101.217s process wall; site failed the 250000-byte profile gate and require-clean rejected its warning. The current seven-flag command initially reproduced a 266116-byte profile for 823884362. Logs and reports are retained; this is local Windows evidence, not a GitHub Linux dispatch.

Workflow now runs exactly the seven evaluator flags from a new working directory, default time budget (420 seconds scaled for 20), fresh state and a 10-minute job timeout. It always uploads report/process/verification artifacts. The verifier rejects invalid evidence/schema/order/unsupported values, unfinished placeholders, missing actual site pages, budget violations, output reductions and unhandled application exceptions. It permits legitimate failed/blocked live-source sections instead of equating source availability with evidence validity.

Presentation regression fix: halve only the duplicate audit table's initial row count as necessary to fit the unchanged 250000-byte HTML gate. Every primary fact/anchor and evidence row remains in local data, exports and Show remaining; no proof rule changed. The saved failing 20 output now generates a site (largest profile 248053 bytes). A new live seven-flag run passes all checks: 147 requests, 107.698 seconds process wall / 106.468 seconds report wall, 20 ordered terminal envelopes, generated site, all five topics, zero unsupported values, $0. Receipts: sitefix/.

Validation: 33 focused site/gate tests, final full pytest 952 passed. Tests distinguish legitimate source timeouts from corrupted bytes/schema/order/value and absent index/profile pages; site regression verifies no input rewrite and all fact anchors/rows retained. No Linux execution or remote CI success is claimed until a later user-authorized push/run; nothing pushed here.

Four human verdicts are recorded separately for the exact original Stage T sample/field/value: GLAMDAl MASKIN 995194163 website, CONCEDO 988217867 website and LinkedIn, BONES BONES 922718059 LEI (exact Norwegian names retained in the ledger). All user-confirmed correct. Automated doubtful verdicts and original proof tiers remain unchanged; no general precision inference. human_reviews.json preserves scope, reviewer and date.

Next authorized work: Stage H new seeds 20261115/16/17 from a clean clone of the CI-fix HEAD. No push.
