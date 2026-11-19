# G1 retry: canonical robots still unreachable

Baseline `ac88ab0`; retry recorded on 2026-11-20 (Asia/Calcutta). No application change.

| Probe | Attempts | HTTP status / content | Result |
|---|---:|---|---|
| Python httpx, restricted sandbox | 3 | none / none | RemoteProtocolError: disconnected without response |
| Python httpx, normal network | 3 | none / none | Same failure; 5/20-second backoff |
| Windows curl, independent TLS stack, normal network | 1 | none / none | Exit 56: connection reset |
| Web lookup, canonical robots URL | 1 | unavailable / unavailable | Tool reported URL not accessible |

Canonical URL: `https://data.brreg.no/robots.txt`. Production user agent used. Null status/content in receipts means no HTTP response arrived; it is not a 404, empty successful response, Allow rule or Disallow rule. No robots body exists to save. The native header capture is empty.

First-party docs were reachable and confirm the public signature/prokura paths and the group-tree path:
- [Fullmakt docs](https://data.brreg.no/fullmakt/docs/index.html): `/fullmakt/enheter/{orgnr}/signatur` and `/fullmakt/enheter/{orgnr}/prokura`.
- [Enhetsregisteret docs](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html): `/enhetsregisteret/api/konsernstruktur/{orgnr}`.

Planned three-number probe: `923609016`, `984851006`, `914778271`; all nine company endpoint requests remain **not sent** because the required robots allow decision was not obtained. No endpoint status, real-response fixture or new claim is asserted. Existing access to other paths on the same host is not evidence of a successful canonical robots fetch in this retry. This is temporary unavailability, not a conclusion that Brreg prohibits these endpoints.

Fail-closed after retries remains unchanged. Implementation and the subsequent standard-100 comparison are blocked at the access prerequisite. No live 100 or 500 run was performed. No new count or size improvement is claimed against `ac88ab0`. Full pytest was not rerun for this documentation-only attempt; the baseline fix has 1,444 passing tests. A fresh privacy guard checks these receipts before commit. No tags or push.

[Normal-network preflight](preflight.json) | [Sandbox preflight](preflight-sandbox.json) | [Native client](native-preflight.json) | [Reproducible Python probe](preflight.py).

Subsequent policy correction: these official API endpoints follow the existing registry client policy, not the website-crawler robots gate. The failure receipts above remain accurate; their API-gating conclusion is superseded. [Current API implementation](../g1-api/SUMMARY.md).
