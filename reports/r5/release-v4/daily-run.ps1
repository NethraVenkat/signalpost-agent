$REPO = (git -C $PSScriptRoot rev-parse --show-toplevel)  # repository root; saved paths are repo-relative
$env:SIGNALPOST_SEARCH_PROVIDER = 'disabled'
$env:SIGNALPOST_SEARCH_MOCK = '0'
$env:PYTHONUTF8 = '1'
Set-Location -LiteralPath "$REPO\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily"
& "$REPO\.data\r5\release-v4-20261113-112818\repo\.venv\Scripts\python.exe" '-m' 'signalpost.cli' 'run' '--organisations' "$REPO\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\companies100.jsonl" '--bulk' "$REPO\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\registry100.csv" '--output' "$REPO\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\envelopes.jsonl" '--profiles-output' "$REPO\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\profiles.jsonl" '--report' "$REPO\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\report.json" '--run-id' 'release-v4-daily-seed20261113' '--expected-count' '100'
exit $LASTEXITCODE
