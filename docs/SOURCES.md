# Sources, licensing and access policy

The MIT licence covers this repository's code and documentation. Third-party data, website content and dependency licences retain their own terms.

## Registry

Official HTTPS `data.brreg.no:443` endpoints:

- `/enhetsregisteret/api/enheter/{orgnr}` and `/roller`.
- `/enhetsregisteret/api/underenheter?overordnetEnhet={orgnr}&size=1000&page=N`.
- `/regnskapsregisteret/regnskap/{orgnr}`.
- Bulk `/enhetsregisteret/api/enheter/lastned/csv`; responses can be gzip even with a CSV filename.

Redirects, URL credentials, unapproved hosts and ports are refused. Registry requests share a bounded async client, host semaphore and global budgets. Accounts allow two retries; other registry requests allow one on eligible failures, respecting Retry-After and remaining deadline. Bodies are hashed and stored.

Enhetsregisteret data uses NLOD 2.0: attribute Bronnoysundregistrene. Primary references: [dataset licensing](https://www.brreg.no/en/use-of-data-from-the-bronnoysund-register-centre/datasets-and-api/), [registry API](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/en/index.html), [accounts schema](https://raw.githubusercontent.com/brreg/regnskapsregister-api/master/src/main/resources/specification/regnskapsregister.json). Restricted authenticated role data is not requested.

## Websites

Candidates use registry website/email and legal-name slugs only. Public Suffix List boundaries come from the installed tldextract snapshot without network updates. Social/directory/search hosts are refused. Only HTML/XHTML/plain responses are used; scripts, images and third-party resources are not fetched. There is no browser renderer.

Every DNS answer and redirect must pass public-unicast and company-domain rules. Connection-time DNS pinning preserves TLS hostname checks and blocks rebinding to private, loopback, link-local, CGNAT, multicast or reserved addresses. HTTPS certificates remain verified; plaintext fallback is permitted only after TLS/connect failure.

Robots are checked per scheme/authority, including redirected hosts. Robots 404/410 permits access; disallow/errors refuse it. At least one second between starts and at most two concurrent requests per registrable domain. Defaults: six website requests/company including robots/redirects, nine overall company slots for website eligibility, eight-second DNS/response bounds, two-MiB body cap. The user agent identifies this repository.

Website facts have company-owned provenance. Publication of short factual spans does not assert an open-data licence for website content. Social-profile URLs are extracted from accepted sites but social platforms are never requested.

## NAV job ads and credentials

[Official feed documentation](https://navikt.github.io/pam-stilling-feed/) and [reuse terms](https://arbeidsplassen.nav.no/vilkar-api). HTTPS `pam-stilling-feed.nav.no:443` only, paths `/api/publicToken`, `/api/v1/feed`, `/api/v1/feed/{UUID}`, `/api/v1/feedentry/{UUID}`. Redirects and arbitrary query/path values are refused. The same public-IP pinned transport is used. Public ad URLs on arbeidsplassen.nav.no are derived, never fetched.

`NAV_API_TOKEN` is optional and read from the process environment. Otherwise retrieve the public credential at run start. Environment credentials can fall back once on rejected access. Credential bodies and Authorization headers are never stored or logged; credential-echo responses are refused. `.env.example` contains only a variable name; no .env loader runs.

A 185-day window accounts for the documented maximum ad lifetime. Resolve repeated UUIDs by latest modification before checking active entries. ETag 304 responses require exact locally stored bodies. Header employer names are discovery only; detail identifiers, status and dates authorize publication. Default detail cap: 300 HTTP attempts including retries.

Terms require updates and removal of inactive/deleted ads. Known inactive/expired jobs are removed even on partial refresh. Unconfirmed historical support is explicitly stale. Emit factual title, dates, location/categories and identifiers; exclude descriptions and contact-person data.

## Financial unit calibration

The accounts schema does not give a normative scaling statement. Four exact-parent 2025 comparisons support whole NOK within tolerance 0.995 to 1.005:

| Publication | Revenue ratio API / published NOK | Annual-result ratio |
|---|---:|---:|
| [TOMRA annual report](https://www.tomra.com/-/media/project/tomra/tomra/investor-relations/annual-reports/2025/tomra-annual-report-2025.pdf), parent p145, org 927124238 |0.999915405|0.999216301|
| [Aker Solutions annual report](https://www.akersolutions.com/globalassets/investors/agm/2026/aker-solutions-annual-report-2025.pdf), parent p176, org 913748174 |1.000000000|1.000246124|

For explicit NOK currency and absent source unit, annotate whole NOK without multiplying any reported amount. Other/missing currencies stay unknown unless reported. Short factual calibration records are stored separately; source identifiers carry the original PDF SHA-256 and page locator. These records are extracted facts, not the original PDF body. This is empirical calibration, not universal API documentation.

## Models, dependencies and cost

No language model or paid API is called. Third-party provider cost is currently $0 per run, per 100 companies and per configured 1,100-company batch; this excludes compute/storage/network costs. Optional evidence-constrained LLM synthesis is planned and unimplemented.

Runtime: httpx (BSD-3-Clause), Pydantic (MIT), tldextract (BSD-3-Clause); development: pytest (MIT), respx (BSD-3-Clause); build: Hatchling (MIT). Locked transitive dependencies retain their licences. The public company-universe download is an input-sampling resource, not claim evidence or part of the published dataset.
