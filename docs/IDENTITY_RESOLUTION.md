# Identity resolution

The identity firewall prevents name similarity from authorizing another company's facts.

## Registry and accounts

Organisation numbers remain strings. Input normalization strips BOM, whitespace and embedded spaces, then checks nine ASCII digits and the mod-11 checksum. Invalid numbers make no requests.

Live identity and accounts must explicitly identify the requested company. Roles can identify their parent through the exact registry entity link. Subunits must report the requested `overordnetEnhet`. Accounts publish only exact-company `SELSKAP` records; consolidated `KONSERN` values are excluded.

## Websites

Candidates come from registry homepages/emails, proven subunits, NAV employer homepages and bounded legal-name variants, within the README's cumulative website/DNS and global limits. Registry website claims remain registry assertions until website identity is independently established. Social/directory domains are excluded from candidate fetching.

| Level | Publication rule |
|---|---|
| VERIFIED | A checksum-valid exact organisation number appears in owner/footer content, appropriate metadata, or explicit non-person JSON-LD identifiers, after every conflict veto. Under R4, another publisher identifier requires proven subunit membership; an unrelated group company's number vetoes even an exact target mention. Historical `group_site` claims remain inspectable but do not authorize new publication. |
| HIGH | Registry-origin domain, full legal-name match, matching site title/brand, strong address/phone/leader corroboration and at least five proof points. Navigation-only matches do not qualify. |
| REGISTRY_DECLARED | Registry-origin domain stays on its registrable domain; live content is neither parked, blocked nor a shell; no foreign owner number appears; two independent signal types among distinctive legal-name branding, registered address and registry phone support it. |
| MEDIUM / LOW | Abstain. Several qualifying domains remain ambiguous unless the policy selects a unique exact-verified domain. |

Guessed slug and email domains require exact organisation-number proof. Hidden text, arbitrary scripts, foreign numbers and page instructions cannot establish ownership. A matching phone alone cannot qualify a registry-declared website.

R4 checks publisher conflicts before positive scoring. Its local publisher block includes title, og:site_name, header/logo, footer/copyright and bounded contact/imprint blocks; customer/partner/reference lists, news/articles, hidden/scripts and agency credits are excluded from this block. A foreign valid publisher orgnr without proven subunit membership, the same name stem with an incompatible legal form (AS/ASA excepted), explicit group branding without the target number, default/parked/placeholder hosting, or a different service-provider publisher vetoes the candidate. An accountant's own correctly branded site is not rejected merely for being an accountant. Subunit fallback cannot override a publisher veto. All older independent vetoes remain active.

The bundled R2 frequency table counts distinct registry entities per phone/full email/corporate email domain/name key. It has source hashes, dates and NLOD 2.0 attribution and loads locally only. These foundation stages do not use rarity as positive proof, change a threshold, or add a tier.

Contacts and social-profile links are extracted only from accepted company sites. Social platforms are never fetched. Company profile links are restricted to accepted-site navigation/footer/header or non-person `sameAs`; sharing, article, platform-root and personal links are excluded.

R5 Stage 4 tightens publication: social links must occur in the site's own header/footer (including equivalent banner/contentinfo roles), outside hidden/article/agency-credit/founder contexts, and their literal profile handle must match the full registered company name with bounded spelling/format normalization. Generic navigation and JSON-LD `sameAs` alone remain discovery only. Shared group-site profiles abstain. The source link span, registry legal-name evidence and accepted website identity evidence are retained. Platforms are not fetched, so no platform display-name verification is claimed. Legacy loose social facts are not carried forward; policy transitions are observations, not invented company changes.

## Job advertisements

NAV header employer names are discovery only. Normalize legal, known brand and subunit names, strip legal suffixes, and require a distinctive token of at least four letters. Distinctive-token overlap ranks candidate details by inverse header-token frequency; Norwegian and ASCII spelling variants converge. Names never authorize publication. The optional unranked reproduction mode uses full-phrase matching. Nameless headers fall back to unfiltered detail discovery within the same cap.

Publication requires detail `employer.orgnr` to equal the company organisation number or a verified subunit number. Record `matched_via` explicitly. A same-name employer with a different identifier is rejected. Only active, non-expired ads with valid dates and matching UUIDs qualify. Unknown trading names and names without distinctive tokens can leave coverage incomplete.
# Explicit publisher identity tiers (R5)

`registry_declared_publisher_name` is HIGH, not exact-number VERIFIED. It requires the complete legal name including legal suffix in an R1 publisher fragment and a candidate hostname matching the registry homepage (www/apex and HTTP(S) variants). Name comparison preserves punctuation, order and suffix; only case, whitespace and æ/ø/å spelling normalization are allowed. Body-only mentions, client lists, articles and agency credits do not qualify. R4 and existing conflict/parked/challenge guards run first.

A registry redirect only nominates a public destination. Its own robots, TLS, SSRF, hop, politeness and HTTP/time budgets still apply. A cross-registrable-domain destination requires that domain also be explicitly named by the company's registered email, or the exact company orgnr in the destination publisher block. Neither a redirect nor a registry declaration alone proves ownership. Full publisher fragments and exact registry evidence dependencies are saved and reconstructed by `verify_output.py`.

`publisher_name_rare_contact` (R3, implemented after R5 commit 153465ff) is also HIGH. It requires the same exact full publisher legal-name group plus one exact registered phone/mobile, full email, or corporate email domain in a publisher footer/contact/imprint block. Two occurrences of the name never count as two groups. Domain-only matching requires the registered email domain to equal the site's own registrable domain. Free-mail domains do not qualify as domain evidence; an exact full free-mail address can qualify if rare. Each contact must have a positive frequency of 1 or 2 distinct entities in the bundled R2 snapshot; absent keys, common contacts and unavailable tables abstain. This frequency is snapshot-specific, not a claim of current worldwide uniqueness. No runtime network lookup is made.

Staff/employee/team blocks, articles, client/partner lists, hidden content and split-node agency credits are excluded before extracting either name or contact. R4 and earlier vetoes still precede acceptance. Claims retain full name/contact fragments, exact registry contact value, normalized key/count and R2 bundle/source hashes/date/licence attribution. The verifier reconstructs these facts from saved page bytes, exact registry receipts and the local table. Existing social rules remain unchanged.
