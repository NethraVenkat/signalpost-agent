# Saved-run defects and fixes

The original single live run at `f740933` is retained unchanged. No new live run is planned unless the requested offline 500 check fails.

## Workplace HTML overflow

Organisation `968360302` produced a 262,692-byte page. Its 42 workplace claims were all rendered into HTML; the old Show remaining workplaces control merely hid the later rows. It did not reduce file bytes. The local-data loader already handled official-record overflow and registry attributes.

Workplace facts now use that loader too: first 10 by default, the remainder in the company's data file with their complete values and original evidence references. If the page is still too large after existing fallbacks, the workplace allowance halves down to zero. All exports, fact identifiers and referenced evidence remain intact. The rendering-only fixture preserves all 826 original claims and reproduces the original byte count; 21 birth-date values in evidence spans are masked with equal-width X strings for repository privacy. The fixture is not used for original-source verification.

## Adaptive pass-2 OSError

The last incomplete request was organisation `890136532`, `https://goldencolombia.org/kjopsbetingelser`, at 1369.614 seconds: status 404, no body hash and no runtime_ms. A prior 404 response completed normally. Thus 404 itself is not the failure. The runner retained only the exception type, discarding the original errno, message and traceback; a disk-full, permissions or network diagnosis cannot be established from that log alone.

The code defect is the batch-wide propagation: adaptive.run had no company-local OSError boundary. The HTTP finalizer also wrote its partial receipt before setting runtime_ms; a failed blob write could suppress that completion marker and replace the original exception. An injected receipt-write failure reproduces this propagation path. [Original request boundary](original-io-boundary.json).

OSError is now isolated during nomination, discovery and post-proof activity/careers work. Each affected company records failed state, phase, URL, exception type, errno/winerror, sanitized message and traceback. Other companies continue; later candidates for the failed company are skipped. A post-proof failure keeps the proven website and marks the failed downstream section. Request finalization records storage errors and runtime even when writing the receipt fails. A summary warning and per-company metrics make partial results explicit. No request counters, deadlines, robots decisions, identity rules or seven-flag defaults change.

## Fix verification before commit

Full pytest: **1,444 passed in 906.97 seconds** ([receipt](pytest.txt)); privacy guard: **5 passed in 2.98 seconds** ([receipt](privacy.txt)). JavaScript syntax check passed. Six new tests cover the saved workplace overflow, zero-inline retention, nomination/discovery/activity failures, and a real fetcher receipt-storage fault. No live research run was performed. The offline rebuild driver blocks network and preserves original outputs by SHA-256; its execution receipts are recorded separately after the fix commit.
