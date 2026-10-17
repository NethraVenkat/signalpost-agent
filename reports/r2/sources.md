# Sources and operating limits

Checked 18 October 2026 (IST).

- [BRREG](https://www.brreg.no/bruke-data-fra-bronnoysundregistrene/datasett-og-api/) declares NLOD reuse for its datasets without registration. Source URLs, retrieval times, hashes and selected frozen CSV records remain evidence.
- [NAV documentation](https://navikt.github.io/pam-stilling-feed/) describes a free authenticated feed, a rotating experimental public token, and registered-consumer tokens. The runtime uses the documented public-token path; no personal consumer credential is shipped. The nomination index cannot establish that an ad remains active.
- [NAV terms](https://arbeidsplassen.nav.no/vilkar-api) require updates and prompt removal of inactive/deleted ads, with personal-data obligations. The exact employer/subunit and current live-detail publication checks remain. A static exported site needs a new run to reflect later closures; it is not a continuously synchronized service.
- Company-site access retains robots, public-IP/DNS pinning, domain bounds, request caps and spacing. Site-specific terms have not been independently cleared for every contacted domain. Robots permission alone is not complete contractual clearance.
- Social platforms are linked from accepted company-site evidence; the collector does not fetch them. Search and LLM generation remain disabled by default. Provider fees in that configuration are $0; hardware and hosting are excluded.
