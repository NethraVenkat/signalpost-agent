$ErrorActionPreference = 'Stop'
# Run from the repository root. Use a fresh output/state directory every time.
if (Test-Path -LiteralPath '.data/r5/stage4_7/stepbudget-run-uninterrupted') {
    throw 'Baseline output already exists; preserve it and use a new path for any later comparison.'
}
$env:SIGNALPOST_SEARCH_PROVIDER = 'disabled'
$env:SIGNALPOST_SEARCH_MOCK = '0'
$env:PYTHONUTF8 = '1'
uv run signalpost run `
    --organisations reports/r5/baseline/companies.jsonl `
    --bulk reports/r5/baseline/registry100.csv `
    --output .data/r5/stage4_7/stepbudget-run-uninterrupted/envelopes.jsonl `
    --profiles-output .data/r5/stage4_7/stepbudget-run-uninterrupted/profiles.jsonl `
    --report .data/r5/stage4_7/stepbudget-run-uninterrupted/report.json `
    --site-dir .data/r5/stage4_7/stepbudget-run-uninterrupted/site `
    --state-dir .data/r5/stage4_7/stepbudget-run-uninterrupted/state `
    --websites --hiring --public-activity --registry-changes `
    --expected-count 100 --run-id r5-stagebudget-seed20261017-uninterrupted `
    --max-requests 2000 --time-budget-seconds 2400 `
    --max-cost-usd 0 --search-max-queries 0 --search-max-cost-usd 0 `
    --synthesis template --llm-max-calls 0 --llm-max-cost-usd 0
exit $LASTEXITCODE
