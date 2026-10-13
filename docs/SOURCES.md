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

## Static English industry titles (SSB KLASS)

Official SSB KLASS classification 6 was downloaded during development on **2026-10-13**. Runtime synthesis reads bundled files only; it never calls KLASS. The English version responses are saved, without replacing titles or truncating classification items, in `src/signalpost/synthesis/data/`:

| Standard | KLASS version | Underlying NACE | English source URL | Saved file |
|---|---|---|---|---|
| SN2025 | 3218; valid from 2025-01-01; last modified 2026-06-17T08:02:16.000+0000 | Rev. 2.1 | https://data.ssb.no/api/klass/v1/versions/3218?language=en | `ssb-sn2025-en-2026-10-13.json` |
| SN2007 | 30; valid from 2009-01-01 | Rev. 2 | https://data.ssb.no/api/klass/v1/versions/30?language=en | `ssb-sn2007-en-2026-10-13.json` |

`nace-klass-2026-10-13.json` records source URLs, download date and version metadata, all English four- and five-digit titles present in each saved response, and all 738/820 five-digit Norwegian subclasses with their official metadata. English lookup uses only the exact code's `name` in the selected version. There is no subclass-to-parent title fallback; missing exact English titles retain the Norwegian registry description. The original four-digit classes and parent metadata remain archival metadata only. Norwegian registered labels were downloaded on the same date from `https://data.ssb.no/api/klass/v1/versions/3218?language=nb` and `https://data.ssb.no/api/klass/v1/versions/30?language=nb` and retained in the normalized table to resolve version collisions. The English originals remain the title authority; tests compare every derived title against them. Part 4A.2 derives this exact-code index from the already saved English responses without another download.

For example, SN2025 `46.640` has the exact English title **Wholesale of other machinery and equipment**, while the same code in SN2007 denotes textile machinery. SN2025 `97.001` has the exact title **Activities of housing cooperatives**; its parent's domestic-personnel title is never substituted. An exact normalized Norwegian label chooses between conflicting versions; if the version cannot be established, synthesis retains only the Norwegian description. Unknown codes never receive a guessed English title. `00.000` / `Uoppgitt` is omitted as an activity and shown as an explicit unknown. No English titles were sourced from model memory. `scripts/download_nace.py` reproduces the development-only download and table build; runtime versions are pinned until a deliberate code/data update.

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

No language model or paid API is called. Template synthesis costs $0 per run, per 100 companies and per configured 1,100-company batch; this excludes compute/storage/network costs. A provider-agnostic interface is tested with a fake provider only. No live adapter or model host is enabled. Reserved provider/model/key environment names contain no values in `.env.example`; setting a key alone does not enable a call.

An injected provider receives claim identifiers/labels and at most two bounded untrusted description quotes. It can only order approved English frames with placeholders; exact values are substituted locally and validated. One call/company, 15 seconds, 2,000 input tokens, 500 output tokens, global call/cost caps and cache prevent unbounded work. Both the dedicated model cap and global cost cap apply. Synthetic offline price entries must be replaced with verified rates before enabling an adapter. Invalid output/errors/caps use template fallback. The cache contains accepted placeholder JSON or sanitized fallback reasons, never credentials.

Runtime: httpx (BSD-3-Clause), Pydantic (MIT), tldextract (BSD-3-Clause); development: pytest (MIT), respx (BSD-3-Clause); build: Hatchling (MIT). Locked transitive dependencies retain their licences. The public company-universe download is an input-sampling resource, not claim evidence or part of the published dataset.
