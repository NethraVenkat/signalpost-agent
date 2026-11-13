$env:SIGNALPOST_SEARCH_PROVIDER = 'disabled'
$env:SIGNALPOST_SEARCH_MOCK = '0'
$env:PYTHONUTF8 = '1'
Set-Location -LiteralPath 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily'
& 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.venv\Scripts\python.exe' '-m' 'signalpost.cli' 'run' '--organisations' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\companies100.jsonl' '--bulk' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\reports\r5\release-v4\registry100.csv' '--output' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\envelopes.jsonl' '--profiles-output' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\profiles.jsonl' '--report' 'C:\Users\<USER>\signal-nethra\.data\r5\release-v4-20261113-112818\repo\.data\release-v4\daily\report.json' '--run-id' 'release-v4-daily-seed20261113' '--expected-count' '100'
exit $LASTEXITCODE
