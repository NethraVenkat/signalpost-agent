# Measured Coverage Gaps and Improvement Plan

**Project**: Signalpost  
**Baseline Dataset**: 1,000-company evaluated cohort (`out/w5-opt1000-rev4-envelopes.jsonl`)  
**Audit Date**: 2026-10-14  
**Evaluator Environment**: Python 3.12+, `uv`, Windows / Linux (Ubuntu)

---

## 1. Executive Summary: Measured Coverage Baseline

An empirical diagnosis was conducted on the saved 1,000-company evaluation cohort (`out/w5-opt1000-rev4-envelopes.jsonl`) without issuing new external requests:

| Coverage Family | Count (out of 1,000) | Proportion (%) | Verification Standard |
|---|---:|---:|---|
| **Verified Websites** | 47 | 4.70% | Strict identity proof: exact 9-digit orgnr in page text, JSON-LD VAT ID, or multi-signal matching on declared site. |
| **Social Profile Links** | 31 | 3.10% | Owned social URLs (LinkedIn, Facebook, Instagram, YouTube, X) linked directly from verified company pages. |
| **Hiring (NAV Arbeidsplassen)** | 8 | 0.80% | Exact orgnr or registered subunit orgnr match on official active NAV job feed detail. |
| **Dated Public Web Activity** | 4 | 0.40% | Dated articles/news/press entries from feeds/sitemaps on verified websites within bounds [2000..now+2d]. |

---

## 2. Separation of Real Production Results vs. Mock-Assisted Discovery

In the 1,000-company cohort, the 47 verified websites break down by candidate nomination origin as follows:

- **Official Registry Declared (`registry_website`)**: 26 companies (55.3%)
- **Derived Name Slug (`legal_name_slug`)**: 16 companies (34.0%)
- **Corroborated External Search (`search_brave`)**: 4 companies (8.5%)
- **Registry Email Domain (`registry_email`)**: 1 company (2.1%)

### Critical Integrity Classification:
The 4 search-nominated companies (**853097012** NYDALS AS, **979703384** STIG OG STEIN AS, **987634308** CONDIS AS, and **994109464** DIGERNESET NÆRINGSOMRÅDE AS) were discovered using `MockBraveProvider`, **not a live Brave Web Search API key**. 
Although their destination evidence pages are genuine live website responses verified cryptographically against the exact organisation numbers, **they must never be reported as live Brave Search discovery performance**. In a standard production environment without `BRAVE_SEARCH_API_KEY`, search remains unconfigured (0 queries, \$0 cost).

---

## 3. Failure Funnel and Bottleneck Analysis

### 3.1 Website Verification Funnel
Out of 1,000 evaluated companies, 953 companies (95.3%) have no published official website. Analysis of recorded error states reveals:
- **`website_candidates` (999 occurrences)**: Companies where generated candidate domains failed verification.
- **`website_source_unavailable` (282 occurrences)**: Remote hosts timed out, connection failed, or returned HTTP 5xx.
- **`website_budget_exhausted` (166 occurrences)**: Per-company request cap (default 6 requests) or global request limit reached before verification was finalized.
- **`robots` / `robots_unavailable` (45 occurrences)**: Domain disallowed crawling in `robots.txt` or robots endpoint timed out/failed.
- **`block_page` (19 occurrences)**: Cloudflare/human challenge/interstitial detected and refused.
- **`http_blocked` (6 occurrences)**: Explicit HTTP 401/403/429 response.
- **`no_localized_proof` (1 occurrence)**: Matched token could not be localized to a valid verbatim span under 300 characters.

### 3.2 Subunit Website Opportunities
- **57 companies** without a verified parent website have registered subunits in Enhetsregisteret with a declared `registered_website`.
- However, 55 of these 57 share the exact same root domain as the parent's attempted candidates (which failed due to timeout, connection refusal, or robots).
- Exactly **2 companies** have distinct subunit websites that were fetched but failed because the subunit proof only achieved `MEDIUM` signal confidence (`familiebarnehage.no` and `s12.no`), and the parent required exact organisation number proof.

### 3.3 Social Profile Link Funnel
- Exactly **16 verified company websites** published no social profile claims.
- The failure mode is primarily:
  1. Social links are present on secondary pages (e.g., `/kontakt`, `/om-oss`) but only the home page was scraped for social links.
  2. Non-standard social link formats or share widgets (which are properly excluded by safety policy).

### 3.4 Public Activity Funnel
- Only **4 companies** currently publish web activity items (`dated_item.*`).
- Activity discovery is currently restricted to feed links in `<head>` and `/sitemap.xml`.
- When an accepted company domain does not have a sitemap index or root `/sitemap.xml`, or has dated news pages linked directly on the home page or contact page, those pages are currently not crawled for activity.

### 3.5 NAV Arbeidsplassen Hiring Matching
- Only **8 companies** had active ads matched in this run.
- Arbeidsplassen matching requires exact 9-digit employer or subunit orgnr in the feed detail record.
- Name-only matching is strictly rejected under identity rules to prevent publishing wrong-company job postings.

---

## 4. Authoritative Rules & Permissions Inventory

| Source / Guidance | Permitted Scope | Status | Notes |
|---|---|:---:|---|
| **Brønnøysundregistrene (NLOD 2.0)** | Bulk registry, Enheter, Underenheter, Roller, Regnskap. | **VERIFIED** | Pinned HTTPS port 443 only. |
| **Arbeidsplassen (NAV)** | PAM Stilling feed and details; declared cache metadata permitted with live detail verification. | **VERIFIED** | Exact orgnr matching only; name-only publishing forbidden. |
| **Company-Owned Websites** | Direct HTTP requests within politeness and robots limits. | **VERIFIED** | 1s domain politeness, max 6 req/co, 2 MiB limit, SSRF protection. |
| **Brave Search API** | Web search query for discovery nomination only. | **VERIFIED** | \$0.005/query; results never evidence; requires explicit key. |
| **Social Platforms (LinkedIn, Facebook, etc.)** | Extracting profile links from verified company websites. | **VERIFIED** | Direct crawling/scraping of social platforms is **STRICTLY FORBIDDEN**. |
| **Google / Generic Web Scraping** | Scraping search engine SERPs. | **FORBIDDEN** | Unauthorised and violates provider terms. |
| **Organiser Hackathon Brief** | Missing from repository. | **UNVERIFIED** | Rely on verified proxy tests and rules compliance. |

---

## 5. Improvement Ranking Matrix

| Opportunity | Measured Opportunity | Request Cost | Implementation Effort | Precision Risk | Priority |
|---|:---:|:---:|:---:|:---:|:---:|
| **1. Secondary Page Social Extraction** | +5 to +10 companies | 0 extra reqs (reuses already fetched followup pages) | Low | Low (strict whitelist applies) | **HIGH** |
| **2. Subunit Website Candidate Generation** | +2 to +5 companies | Within existing 6-req cap | Low | Low (requires exact orgnr/subunit proof) | **HIGH** |
| **3. Bounded Followup Page Fallbacks for Contacts/Proof** | +4 to +8 companies | 1-2 reqs within company cap | Medium | Low (requires exact orgnr proof) | **HIGH** |
| **4. Permitted Activity Extraction from HTML Feeds** | +5 to +15 companies | 1 req within budget | Medium | Low (requires strict dated items [2000..now+2d]) | **MEDIUM** |
| **5. Live Brave Search API Key Handling** | Bounded by key availability | \$0.005 / company | Low | Low (discovery only, destination proof required) | **MEDIUM** |
| **6. Scraper for Social Platforms / Google SERP** | N/A | High | High | Extreme (forbidden by organiser rules) | **REJECTED** |
| **7. Name-Only Job Publishing** | High recall | 0 | Low | Extreme (wrong-company claims forbidden) | **REJECTED** |

---

## 6. Actionable Implementation Scope for Stage C

1. **Subunit Candidate Priority**: Ensure distinct subunit website candidates from `subunits.detail.*.registered_website` are prioritized when parent website is absent.
2. **Followup Page Social Profile Extraction**: When followup pages (like `/kontakt` or `/om-oss`) are fetched during proof corroboration, extract social links from those already-downloaded pages as well.
3. **Verified Activity Discovery**: Extract activity items from feed links discovered on verified sites with strict date validation and SHA-256 provenance.
4. **Offline Search Key Safety**: Maintain strict zero-cost offline search behavior when `BRAVE_SEARCH_API_KEY` is not provided.
