# Stage U - UX

The seven evaluator flags now produce `<output directory>/site/` by default. `--no-site` disables it; `--site-dir` chooses another destination. The report records available/skipped/failed/disabled state. Mandatory outputs complete before optional rendering; deadline skips remain explicit. Library callers retain explicit Config control.

The real CLI/runner test invokes only those seven flags with mocked sources and verifies index, profile and profiles JSON files. A separate case checks `--no-site`. The fresh frozen run omits `--site-dir` and records an available site for 100 companies / 102 HTML pages.

## Browser verification

Authored Playwright checks use cached Chromium 156 at 1280 and 360 px, with external requests blocked. All 12 checks pass: dashboard, name/number search, profile, source panel, expanded evidence table and two-company comparison. Visible controls measure at least 44 by 44 px; page width stays inside the viewport. Source panels show excerpt, source URL, retrieval time and full hash. No JavaScript errors occurred.

Profiles have a compact expandable verification hint. Main and lazy facts link to publishers and evidence; explorer entries link to the underlying fact. Mobile tables become labelled rows, financial values stay readable, long preformatted content wraps, and comparison states/reasons have separate spacing.

## Evidence and demo

- Full pytest: **771 passed in 131.00s**, without timeout/assertion relaxation.
- Fresh state, frozen input hashes, same 8/13 settings as best 4.7, $0, no paid search/model calls.
- [table.md](table.md) compares all metrics/states; settings, commands, original report, hashes, full tests and verifier are alongside it.
- `docs/demo/` is built from fresh Stage U output. [demo_manifest.json](demo_manifest.json) records every file/hash. It is a Pages artifact root with relative paths tested under `/signalpost-agent/`; README gives the expected URL and publishing instructions. **Nothing was published or pushed.**
- Screenshots: desktop-directory.png, desktop-profile.png, desktop-source.png, desktop-compare.png; mobile-directory.png, mobile-profile.png, mobile-source.png, mobile-compare.png, mobile-financial-row.png, mobile-evidence-row.png.

These checks cover requested behaviors, not an official award of 8/8. Hand-check physical phone/Safari behavior, comparison usefulness, and public-source data before deployment.

Fresh run: 6 websites; website failed 17, activity failed 23; 898 HTTP attempts, 274.016s runner time, $0. Verifier: 100 envelopes / 385 source bodies, zero unsupported values.
