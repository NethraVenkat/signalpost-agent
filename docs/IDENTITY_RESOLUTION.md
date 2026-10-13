# Identity resolution

The identity firewall prevents name similarity from authorizing another company's facts.

## Registry and accounts

Organisation numbers remain strings. Input normalization strips BOM, whitespace and embedded spaces, then checks nine ASCII digits and the mod-11 checksum. Invalid numbers make no requests.

Live identity and accounts must explicitly identify the requested company. Roles can identify their parent through the exact registry entity link. Subunits must report the requested `overordnetEnhet`. Accounts publish only exact-company `SELSKAP` records; consolidated `KONSERN` values are excluded.

## Websites

At most four registrable-domain candidates come from the registered website, registry email or legal-name slugs. Registry website claims remain registry assertions until website identity is independently established. Social/directory domains are excluded from candidate fetching.

| Level | Publication rule |
|---|---|
| VERIFIED | A checksum-valid exact organisation number appears in owner/footer content, appropriate metadata, or explicit non-person JSON-LD identifiers. A group page listing the company is labeled `group_site`. |
| HIGH | Registry-origin domain, full legal-name match, matching site title/brand, strong address/phone/leader corroboration and at least five proof points. Navigation-only matches do not qualify. |
| REGISTRY_DECLARED | Registry-origin domain stays on its registrable domain; live content is neither parked, blocked nor a shell; no foreign owner number appears; two independent signal types among distinctive legal-name branding, registered address and registry phone support it. |
| MEDIUM / LOW | Abstain. Several qualifying domains remain ambiguous unless the policy selects a unique exact-verified domain. |

Guessed slug and email domains require exact organisation-number proof. Hidden text, arbitrary scripts, foreign numbers and page instructions cannot establish ownership. A matching phone alone cannot qualify a registry-declared website.

Contacts and social-profile links are extracted only from accepted company sites. Social platforms are never fetched. Company profile links are restricted to accepted-site navigation/footer/header or non-person `sameAs`; sharing, article, platform-root and personal links are excluded.

## Job advertisements

NAV header employer names are discovery only. Normalize legal, known brand and subunit names, strip legal suffixes, and require a distinctive token of at least four letters. Distinctive-token overlap ranks candidate details by inverse header-token frequency; Norwegian and ASCII spelling variants converge. Names never authorize publication. The optional unranked reproduction mode uses full-phrase matching. Nameless headers fall back to unfiltered detail discovery within the same cap.

Publication requires detail `employer.orgnr` to equal the company organisation number or a verified subunit number. Record `matched_via` explicitly. A same-name employer with a different identifier is rejected. Only active, non-expired ads with valid dates and matching UUIDs qualify. Unknown trading names and names without distinctive tokens can leave coverage incomplete.
