# Robots transient recovery

Official-source robots requests now use the same bounded retry path on every origin: an initial attempt and at most two transient retries, with 5/20-second backoff, host politeness and existing request/deadline limits. Robots 2xx is parsed; robots 4xx allows access without rules; persistent 5xx or transport failure blocks the origin for this run. Data-endpoint refusals remain unchanged. Access-result policy: [RFC 9309 section 2.3.1](https://www.rfc-editor.org/rfc/rfc9309.html#section-2.3.1).

Targeted state-aid, official-resilience and exact-public tests: **56 passed**. Tests cover reset then 200, repeated resets with cached blocking, 204, 404 and 403.

The single small live source check for organisation 923609016 did not reach the Støtteregisteret data endpoint: robots remained unreachable (`httpx.ReadError` / `public_connect`), and the bounded retry path ended in `public_robots_unavailable`. Resumed state-aid requests are therefore **not confirmed**. No robots failure was bypassed, and no second small live check was made. The following 500-company check records this source's actual requests and available claims separately.
