# W0 rejection audit

Saved receipts only. Categories overlap. All fetched pages and identity locations are retained in rejections.json. A candidate-level rule cannot be attributed to one particular fetched page when the old output did not save that association.

| Seed | Companies | Published sites | Declared homepage | Declared with a published site | Declared domain published | Veto | Ambiguous | Fetched without proof |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 20261017 | 100 | 5 | 11 | 4 | 4 | 3 | 6 | 22 |
| 20261113 | 100 | 4 | 11 | 3 | 3 | 4 | 10 | 27 |
| 20261114 | 100 | 3 | 8 | 3 | 3 | 2 | 8 | 27 |
| 20261115 | 100 | 5 | 14 | 1 | 1 | 3 | 5 | 25 |
| 20261116 | 100 | 5 | 17 | 2 | 2 | 6 | 9 | 25 |
| 20261117 | 100 | 7 | 11 | 0 | 0 | 6 | 6 | 24 |

## DNS history

{"NXDOMAIN/name-not-found": 2511, "unknown (resolver error or DNS nomination budget)": 7}

Generic dns_unavailable cannot retrospectively distinguish SERVFAIL, timeout or another resolver error. no_such_domain is the OS name-not-found category; it is not a saved authoritative DNS RCODE. Fresh public-resolver checks are separately recorded.

## NAV/universe overlap

```json
{
  "index_built_at": "2026-11-13T08:23:53.796625Z",
  "ads": 9511,
  "index_employers": 6012,
  "universe_size": 411160,
  "direct_employers_in_universe": 0,
  "proven_parent_employers_in_universe": 3,
  "unique_represented_companies": 3,
  "expected_per_1000_lower_bound": 0.007296429613775659,
  "measured_job_companies": 3,
  "measured_inputs": 600,
  "measured_per_1000": 5.0,
  "limitation": "No full underenheter snapshot is available locally. Parent coverage is a lower bound from saved exact-parent proofs; index entries are discovery metadata, not current posting proof. Not a complete expected-rate estimate."
}
```

## 20261017 / 925181536 / SESTANTE AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://sestante.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: sestante.no; recorded rule: `corroboration`; level: LOW.
- Candidate: sestante.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://sestante.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: sestante.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://sestante.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.sestante.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://sestante.no/; recorded rule: `None`; level: not saved.
- Candidate: https://sestante.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://sestante.com/; recorded rule: `None`; level: not saved.

Page: http://sestante.no/ — title: sestante.no is parked

SHA-256: `1b6653faadc091fcefa95c1ba569cb3f2b4178cc91c3b2dd5fb8b136fd7b0808`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://sestante.no/kontakt — title: sestante.no is parked

SHA-256: `5cea00e85f5fa871be413f374e00f67ab6a32055b605c6eea8ecd3a639e4f8ff`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://sestante.no/om-oss — title: sestante.no is parked

SHA-256: `d7bf1c17fd87df270bf9b32a4ec8ffea708a409e8de65943ebc20c0d66854f82`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://sestante.no/personvern — title: sestante.no is parked

SHA-256: `6ff6ece6d4741040af07169634e18a1d6031ce4ce92ba5b78349664bc0878587`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://sestante.com/ — title: Sestante Family Office | Stewards of Your Wealth and Lifestyle

SHA-256: `8e1e27a3b5ce54e7594b42d81d9da070e67cb677f7b736bbf36cbbcb24f626b0`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://sestante.com/contact/ — title: Contact | Sestante Family Office

SHA-256: `3ce63b72a99905b32a1d59efb4ab9090439b6393a82e2b46904f83ae95f138c2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 932525070 / AS ELVELY

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://svill.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: svill.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: aselvely.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: as-elvely.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: aselvely.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: as-elvely.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://svill.no/; recorded rule: `None`; level: not saved.

Page: https://svill.no/ — title: Svill Eiendom

SHA-256: `74127d774996775f2c9df5840e27f331e4eea387acb3442a8fe4497b2416631b`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://svill.no/kontakt — title: Kontakt

SHA-256: `2b6159f9efaa3f13133d2b392eb52afe49ba1eba62e442177cfc3d999e71588f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://svill.no/om-oss — title: Not Found

SHA-256: `2bf5f0aebaea858c5b57265b0dbb15fa3b176c67c11b36381a5a1e56bedf2e9f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://svill.no/personvern — title: Not Found

SHA-256: `2bf5f0aebaea858c5b57265b0dbb15fa3b176c67c11b36381a5a1e56bedf2e9f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://svill.no/personvernerklaering — title: Not Found

SHA-256: `2bf5f0aebaea858c5b57265b0dbb15fa3b176c67c11b36381a5a1e56bedf2e9f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://svill.no/kontakt-oss — title: Not Found

SHA-256: `2bf5f0aebaea858c5b57265b0dbb15fa3b176c67c11b36381a5a1e56bedf2e9f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 915188389 / HAUGESUND INTERNATIONAL SCHOOL STI

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: hischool.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: haugesundinternationalschool.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: haugesund-international-school.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: haugesundinternationalschool.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: haugesund-international-school.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://hischool.no/; recorded rule: `None`; level: not saved.

Page: https://hischool.no/ — title: Home — Haugesund International School

SHA-256: `7028d4ce3b8f516a82429fcad488aae2cef1e8d3b41c5bae0dfaaa0a95acd0e2`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hischool.no/contact — title: Contact — Haugesund International School

SHA-256: `16df687950438b823472dfc173ba2e7aea4378ffe732cdc0118960acd716999b`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hischool.no/kontakt — title: Haugesund International School

SHA-256: `48647f296084cbeb5db532d4720945614c2fe4b33ab5678bda50a819d005bb53`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hischool.no/om-oss — title: Haugesund International School

SHA-256: `5e0e71959b430719f6dd52989115772164e489a385c5e2e06ca477ffa69e2f0e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hischool.no/personvern — title: Haugesund International School

SHA-256: `7d3b619355d43d23f35a2be3b9ef4bb47251232a6f590ecdb01a946eeef5ccd6`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hischool.no/personvernerklaering — title: Haugesund International School

SHA-256: `a6b469786d793c82a240efd3798bf67d737ceb1d8094853df9c8f787cc3817ab`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 936035523 / RETT RØRSERVICE AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: rettroerservice.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rett-roerservice.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rettroerservice.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rett-roerservice.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://rettrorservice.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: rettrorservice.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: rettrorservice.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rett-rorservice.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rett-rorservice.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--rett-rrservice-vqb.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--rettrrservice-fnb.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--rett-rrservice-vqb.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--rettrrservice-fnb.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://rettrorservice.no/; recorded rule: `None`; level: not saved.

Page: https://rettrorservice.no/ — title: www.rettrorservice.no

SHA-256: `a61ee8b3f06b9b53643a1a28eb2f7d5c97e77977b36cfab10eec302d877248e9`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rettrorservice.no/kontakt — title: 404 Not Found

SHA-256: `e149b5f6935f334dc4d0b8292dfd2db88d96f5b76189be5092bd23030c5990c8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rettrorservice.no/om-oss — title: 404 Not Found

SHA-256: `e149b5f6935f334dc4d0b8292dfd2db88d96f5b76189be5092bd23030c5990c8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rettrorservice.no/personvern — title: 404 Not Found

SHA-256: `e149b5f6935f334dc4d0b8292dfd2db88d96f5b76189be5092bd23030c5990c8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rettrorservice.no/personvernerklaering — title: 404 Not Found

SHA-256: `e149b5f6935f334dc4d0b8292dfd2db88d96f5b76189be5092bd23030c5990c8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rettrorservice.no/kontakt-oss — title: 404 Not Found

SHA-256: `e149b5f6935f334dc4d0b8292dfd2db88d96f5b76189be5092bd23030c5990c8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 948639416 / SVERSTAD BORETTSLAG

Categories: veto; terminal website state: not_available.

- Candidate: nbbo.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: sverstadborettslag.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sverstad-borettslag.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sverstadborettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sverstad-borettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.nbbo.no/; recorded rule: `None`; level: not saved.

Page: https://nbbo.no/ — title: NBBO - Nedre Buskerud Boligbyggelag - Gode hjem siden 1946

SHA-256: `4d78e147eee097a7a4dd20e65239dad6b988d7cad79ba19f05c5c8543886e259`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "952527827"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 927439794 / FJERSTAD AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://fjerstad.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: fjerstad.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: fjerstad.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: http://fjerstad.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: fjerstad.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://fjerstad.no/; recorded rule: `None`; level: not saved.
- Candidate: https://fjerstad.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://fjerstad.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.fjerstad.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://fjerstad.com/; recorded rule: `None`; level: not saved.

Page: https://fjerstad.no/ — title: Siden er nÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¥ nede for vedlikehold/oppdatering

SHA-256: `656be9606c71e2e9a58664b446c0d5b3d5c7e81967056c00f9ad7f2b840b2abe`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjerstad.no/kontakt — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjerstad.no/om-oss — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjerstad.no/personvern — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjerstad.no/personvernerklaering — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjerstad.no/kontakt-oss — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://fjerstad.com/ — title: Fjerstad Home Page

SHA-256: `65d5547bac37c8307c4730a455b93ba594e2d6d58aa0dccad364d165eda49096`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://fjerstad.com/kontakt — title: 

SHA-256: `c1b9046b1d6258ce6c1640a29c552816d721c00c48e462d418a1ea5f15191897`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 930621927 / DENTAL HOLDING AS

Categories: fetched-without-proof, veto; terminal website state: not_available.

- Candidate: dentalholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: dental-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://dentalholding.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: dentalholding.com; recorded rule: `corroboration`; level: LOW.
- Candidate: dental-holding.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: dental-holding.com; recorded rule: `group_without_exact_orgnr`; level: REJECT.
- Candidate: https://dentalholding.com/; recorded rule: `None`; level: not saved.
- Candidate: https://dental-holding.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://dental-holding.com/; recorded rule: `None`; level: not saved.

Page: https://dentalholding.com/ — title: DentalHolding – sprzęt, materiały i szkolenia dla stomatologii

SHA-256: `d75b741cbb41fe625aca9de1904226fc0b219d7d9da7ee0596be3e6d7c28cfe5`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dentalholding.com/kontakt.html — title: Kontakt – DentalHolding | telefon, e-mail, formularz kontaktowy

SHA-256: `88371cbb9b0e618d3f66330f43944422b9379969d575c27d85ebe11e9e3962c8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dentalholding.com/kontakt — title: 404 Not Found

SHA-256: `e2731769fe4a7858d77c8d86679c7a9fcfe0866b882b311aa163934152bff201`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dentalholding.com/om-oss — title: 404 Not Found

SHA-256: `e2731769fe4a7858d77c8d86679c7a9fcfe0866b882b311aa163934152bff201`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dentalholding.com/personvern — title: 404 Not Found

SHA-256: `e2731769fe4a7858d77c8d86679c7a9fcfe0866b882b311aa163934152bff201`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dental-holding.com/ — title: Dental Holding | Dental Distribution Group in CEE

SHA-256: `79310c65ff1e98d6489e79e28f325cec78953aecc4e394ac4701da56ac673238`; candidate rules: group_without_exact_orgnr, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Holding",
    "Group",
    "Holding",
    "Holding",
    "Our Companies",
    "Our Companies",
    "Holding"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 912579433 / KAMPEN HOTEL AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://lmc.as/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: lmc.as; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: kampenhotel.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kampen-hotel.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kampenhotel.no; recorded rule: `url_refused`; level: LOW.
- Candidate: kampen-hotel.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kampenhotel.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://lmc.as/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.lmc.as/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://lmc.as/; recorded rule: `None`; level: not saved.
- Candidate: https://kampenhotel.no/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://kampenhotel.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.kampenhotel.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://kampenhotel.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://kampenhotel.com/; recorded rule: `website_budget_exhausted`; level: not saved.

Page: http://lmc.as/ — title: lmc.as

SHA-256: `00bfba3eb691644b2835a1ec936bd77c3c7b96f25bc5861b4382999e5d12f1d4`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://lmc.as/kontakt — title: lmc.as

SHA-256: `5e6bf71e5f148b1c67845bab3a81e6f232deb18ad3945990a845396347a87e3e`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://lmc.as/om-oss — title: lmc.as

SHA-256: `dff6a89ceb172b128b0c9d8a4e481c11d453e36db7be833c9f25a308af01e0eb`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://lmc.as/personvern — title: lmc.as

SHA-256: `66fbf7aa700d82c4dcac9f451216e7cec9d1a0d334353860949858db4705f086`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://kampenhotel.no/ — title: Document Moved

SHA-256: `3d3d601611485982d923526ce089a172a6d28e709f59e5affd247042150b88c9`; candidate rules: url_refused, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 991835423 / H-2 EIENDOM AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://ragde.no/om-ragde/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ragde.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: h2eiendom.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: h-2-eiendom.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: h2eiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: h-2-eiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.ragde.no/; recorded rule: `None`; level: not saved.

Page: https://ragde.no/ — title: 
                            Velkommen til Ragde Eiendom | Ragde.no
                    

SHA-256: `c9140206239c0bdf2f4ead550750d9c5b39767e212184a3da6cf0fdaf628f63d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hovedmeny Eiendommer Dette er Ragde Eiendom Ragde Charge Team Ragde Charge Ledige stillinger Kontakt oss Søk Eiendomsselskap i sterk vekst Utleie og forvaltning, kjøp og salg av bolig- og næringseiendom. Alle eiendommer Raske fakta om Ragde Næringseiendom 1.8 millioner m² Parkeringerplasser 16000 Ansatte 53 Omsetning 2025 2.4 milliarder Kort fortalt Varierte prosjekter siden 1995 Visste du at Ragde Eiendom i dag består av alt fra lager, kontor, kjøpesenter, industri, hoteller og private utleieleiligheter? Gode resultater gir stabilitet Konsernets eiendomsportefølje er godt diversifisert og har i alle år levert svært gode resultater. Langvarige samarbeid Vi er opptatt av at du er fornøyd med lokalene du leier eller drifter sammen med oss. Derfor strekker vi oss den ekstra mila for at du skal bli fornøyd. God hjelp fra våre ansatte 53 ansatte fordelt på administrasjon, senterledere, vaktmestere og bygningsarbeidere står klare til å gi deg god og rask hjelp når du trenger det. Eiendommer Varierte eiendommer med moderne infrastruktur Eiendomene er geografisk godt spredt, med hovedvekt i Oslo og Bergen. Selskapet eier også eiendom i Belgia, Nederland, Sverige, Danmark og Finland. Se alle eiendommer Velkommen til Sannergata 2 Bygget er totalrenovert og utformet med fokus på kvalitet, funksjon og opplevelse. Ingenting er overlatt til tilfeldighetene – hver detalj er gjennomtenkt, fra materialvalg og belysning til møblering. Veggene prydes av flott kunst, og interiøret skaper en inspirerende og luksuriøs atmosfære som både ansatte og besøkende legger merke til. Samtidig holder eiendommen et av de høyeste nivåene innen bærekraft, miljø og energieffektivitet, sertifisert som BREEAM Excellent . Det er lagt vekt på energieffektive løsninger, smart styring av lys og ventilasjon, samt bruk av miljøvennlige materialer med lang levetid. Les mer The Box – Coworking på sitt mest inspirerende The Box er nå åpent i Sannergata 2, Løkkas nye signalbygg. Her finner du mer enn bare kontorplasser. Vi har skapt et pulserende coworking-miljø fylt med gründere, kreative sjeler og ambisiøse selskaper. Les mer Splitter nye lagre sentralt på Sinsen KUBIKK gir deg lagring med superenkel tilgang sentralt på Sinsen i Oslo. Vi har over 60 lagerplasser av ulik størrelse, og finner et lager som passer deg. Fortell oss hva du ønsker, så fikser vi resten. Les mer Kiellands Hus Smilende gode resultater På Alexander Kiellands plass tok Ragde Eiendom over nærsenteret Kiellands Hus. Med restaurering, en spennende grafisk profil og markedsføring har vi klart å løfte omsetningen 29 % siste året for våre leietakere, og fått mer fornøyde kunder. Les mer Ragde Kontakt oss Dette er Ragde Eiendom Angrerettskjema Personvernerklæring Åpenhetsloven Kameraovervåking © 2026 Ragde. All Rights Reserved. Drift av nettside levert av Mementor AS"
  ]
}
```

Page: https://ragde.no/kontakt-oss/ — title: 
                            Kontakt oss | Ragde Eiendom
                    

SHA-256: `7bbdc46c97eeb12dc9679dd3695ca0b31952a29a11e6d4dce0ba53bbff11a555`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ragde.no/personvernerklaering/ — title: 
                            Personvernerklæring - Ragde
                    

SHA-256: `641e5e41165afffc246e318a9cde0d6bd67ea800ee3a0703ea88dc266c6ec4a9`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "974227037"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 997995414 / PEAK LANDSCAPES AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.peaklandscapes.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: peaklandscapes.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: peak-landscapes.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: peaklandscapes.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: peak-landscapes.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: peaklandscapes.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://peaklandscapes.no/; recorded rule: `None`; level: not saved.
- Candidate: https://peaklandscapes.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://peaklandscapes.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.peaklandscapes.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://peaklandscapes.com/; recorded rule: `url_refused`; level: not saved.

Page: https://www.peaklandscapes.no/ — title: Peak Landscapes | Anleggsgartner i Oslo og Akershus

SHA-256: `3a6eb3ef5be3ffbfe51e837088b8bf0560744cc1f37395d5b4bc2488499c9450`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "top of page HJEM TJENESTER PROSJEKTER OM OSS Menu Back to site FÅ DITT TILBUD Forvandler rom, forbedrer hjem Pålitelig designere og anleggsgartnere med erfaring siden 2000 FÅ DITT TILBUD Kontakt oss Navn Telefonnummer E-post Fortell oss om prosjektet ditt Send inn Der visjon møter virkelighet Peak Landscapes AS ble opprinnelig opprettet som et engelsk anleggsgartnerfirma i den sørlige delen av England. Firmaet spesialiserer seg på planlegging og bygging av private hager; nye så vel som etablerte hageanlegg. Vi kombinerer engelsk hagetradisjon og design med norske byggeteknikker. Peak Landscapes hjelper deg med planlegging og design av utemiljøet, enten det gjelder hagerom, bakgårder, bygårder eller andre fellesarealer. Arbeidet utføres av fagutannede Fokus på god dialog med kunden hele veien Kreativitet og nøyaktighet FÅ DITT TILBUD Vi skaper uterom du vil elske ALLE PROSJEKTER VÅR 3-TRINNS PROSESS DESIGN Alt starter med design. Dette er den viktigste delen av prosessen – her lytter vi, planlegger og former visjonen din til et gjennomtenkt konsept. Et godt design sikrer at alle elementer spiller sammen, og gir det beste mulige resultatet for ditt uteområde. UTFØRELSE Når designet er klart, setter vårt erfarne team i gang. Vi bruker profesjonelle metoder og materialer av høy kvalitet for å gjennomføre prosjektet trygt, effektivt og med presisjon. ​ ​ ​ NYT – DITT NYE UTEOMRÅDE Det siste steget er det mest givende – å nyte resultatet. Enten du slapper av med familien, inviterer venner eller bare nyter utsikten, er dette øyeblikket hvor alt arbeidet virkelig lønner seg. ​ ​ ​ ALLE PROSJEKTER Våre partnere Samarbeidspartner Peak Landscapes AS HJEM TJENESTER PROSJEKTER OM OSS Menu Close HOVEDKONTOR Alunsjøveien 65, 0957 Oslo +47 45 68 54 99 david@peaklandscapes.no SOCIALS Facebook Instagram FORESPØRSLER FÅ DITT TILBUD © 2025 by SGNXT HJEM TJENESTER PROSJEKTER OM OSS bottom of page"
  ]
}
```

Page: https://www.peaklandscapes.no/about-us — title: OM OSS | Peak Landscapes

SHA-256: `ee8ece818b865017ce536d310998ad0df90518a0b6a78fa588d05b7fe0d08139`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.peaklandscapes.no/kontakt — title: 404 Error: Page Not Found

SHA-256: `e6d51ba5f14d21c806ac67f0de1bdded337e18e2070c6cb245df6a52ff61d3ff`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 957687504 / DECIBELPRODUKTER AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.desibelprodukter.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: desibelprodukter.no; recorded rule: `corroboration`; level: LOW.
- Candidate: decibelprodukter.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: decibelprodukter.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.desibelprodukter.no/; recorded rule: `None`; level: not saved.

Page: https://www.desibelprodukter.no/ — title: DesibelProdukter

SHA-256: `d2c7961886b4b8f45ecaff7d9a4e555296c49e15050a215c121777f18f5cd8d6`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.desibelprodukter.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.desibelprodukter.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.desibelprodukter.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.desibelprodukter.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.desibelprodukter.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 916249985 / KALDVELLFJORDEN EIENDOM AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.olsenbygg.com/om-kaldvellfjorden/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: olsenbygg.com; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: kaldvellfjordeneiendom.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kaldvellfjorden-eiendom.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kaldvellfjordeneiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kaldvellfjorden-eiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://olsenbygg.com/; recorded rule: `None`; level: not saved.

Page: https://www.olsenbygg.com/ — title: Hjem - Olsenbygg

SHA-256: `e425855aecf8c71a2a1fc32a2b46c4edadb0e4c6846e8a3170708f2718111675`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.olsenbygg.com/kontakt-olsenbygg/ — title: Kontakt oss - Olsenbygg

SHA-256: `d6edd8d855a9725c36fa4cc8e6ecb1b83c1651eda5cce7bc0cd5219e6518fba4`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.olsenbygg.com/om-olsenbygg/ — title: Om oss - Olsenbygg

SHA-256: `9a227248520b3c355f0836939d4fad1774acf45da42028f3e49a0d2165f97a32`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 999504116 / MLC INVEST AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: mlcinvest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: mlc-invest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: mlcinvest.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: mlc-invest.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: mlc-invest.com; recorded rule: `robots`; level: BLOCKED.
- Candidate: https://mlcinvest.com/; recorded rule: `None`; level: not saved.
- Candidate: https://mlc-invest.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://mlc-invest.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.mlc-invest.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://mlc-invest.com/; recorded rule: `robots`; level: not saved.

Page: https://mlcinvest.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mlcinvest.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mlcinvest.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mlcinvest.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mlcinvest.com/personvernerklaering — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mlcinvest.com/kontakt-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mlcinvest.com/om — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 998320143 / CAELI SYSTEM AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://caelisystem.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: caelisystem.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: caeli-system.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: caelisystem.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: caeli-system.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://caelisystem.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.caelisystem.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://caelisystem.no/; recorded rule: `None`; level: not saved.

Page: http://caelisystem.no/ — title: caelisystem.no

SHA-256: `fc89267facf827c06d63e9a750e01446d3e1f44d3c04151ebc6c1abd90194afc`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://caelisystem.no/kontakt — title: caelisystem.no

SHA-256: `ee5cea386826faecef6a636fcb9bca292c7799e981633df5afbcb7578184d290`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://caelisystem.no/om-oss — title: caelisystem.no

SHA-256: `5dfc49482707fce048cfd6ea546d3e37422b694c3c91e49351af65a47e7ab454`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://caelisystem.no/personvern — title: caelisystem.no

SHA-256: `64d510bdaa69a2fab310c656413abf4127a674ba1917923e9aef19e434a14d39`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 918109099 / STIFTELSEN DOK-FESTIVALEN

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.dokfestivalen.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: dokfestivalen.no; recorded rule: `corroboration`; level: LOW.
- Candidate: stiftelsendokfestivalen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: stiftelsen-dok-festivalen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: stiftelsendokfestivalen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: stiftelsen-dok-festivalen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.dokfestivalen.no/; recorded rule: `None`; level: not saved.

Page: https://www.dokfestivalen.no/ — title: DOK26

SHA-256: `5c2c155c35d1ffa4f771e2211b2abde58dcc91a4d5ab4ff1ef4e71ce768f5ff2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dokfestivalen.no/about — title: OM FESTIVALEN — DOK26

SHA-256: `2c1c7360793f5d9cee72e2df09e6571ad7d43d89af49af2d72c68e135d6e6aeb`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dokfestivalen.no/contact — title: Contact — DOK26

SHA-256: `854cfdc2afa359de67b0550559bd8078dde13641f590099d07b0096d4e6079c2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dokfestivalen.no/kontakt — title: DOK26

SHA-256: `1ff3d7c64ff467b3ee68989e873ed310abe397a24c71a7e5184d76d5b72a1e60`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dokfestivalen.no/om-oss — title: DOK26

SHA-256: `1ff3d7c64ff467b3ee68989e873ed310abe397a24c71a7e5184d76d5b72a1e60`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dokfestivalen.no/personvern — title: DOK26

SHA-256: `1ff3d7c64ff467b3ee68989e873ed310abe397a24c71a7e5184d76d5b72a1e60`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 932112183 / PURE CAPITAL AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: purecapital.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: pure-capital.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://purecapital.com/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: purecapital.com; recorded rule: `corroboration`; level: LOW.
- Candidate: pure-capital.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: pure-capital.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://purecapital.com/; recorded rule: `None`; level: not saved.
- Candidate: https://pure-capital.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://pure-capital.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.pure-capital.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://pure-capital.com/; recorded rule: `url_refused`; level: not saved.

Page: https://purecapital.com/ — title: Pure Capital

SHA-256: `cf0d5f193f4df5a90059fc583b3e7167184e442ff9c699827bbd5b2f160decb4`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://purecapital.com/contact-us/ — title: Pure Capital

SHA-256: `a29d343c4a8255a019d8cbeb30137c0202bc2fd7e5c5a9ff5b0b8decb7a04f8d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://purecapital.com/kontakt — title: The page you're looking for could not be found (404)

SHA-256: `cea75b0a503a77e1c60a39c02d8849c285aed5d983b1e96c6e7c90b735982d32`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://purecapital.com/om-oss — title: The page you're looking for could not be found (404)

SHA-256: `cea75b0a503a77e1c60a39c02d8849c285aed5d983b1e96c6e7c90b735982d32`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://purecapital.com/personvern — title: The page you're looking for could not be found (404)

SHA-256: `cea75b0a503a77e1c60a39c02d8849c285aed5d983b1e96c6e7c90b735982d32`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://purecapital.com/personvernerklaering — title: The page you're looking for could not be found (404)

SHA-256: `cea75b0a503a77e1c60a39c02d8849c285aed5d983b1e96c6e7c90b735982d32`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 899174682 / FANTOFT UTVIKLING AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://paretosec.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: paretosec.com; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: fantoftutvikling.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fantoft-utvikling.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fantoftutvikling.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fantoft-utvikling.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://paretosec.com/; recorded rule: `None`; level: not saved.

Page: https://paretosec.com/ — title: Pareto Securities - The Nordic Gateway : Pareto Securities

SHA-256: `9e87b52203b95233e1bfb6eb8565857b3ad5a9e2260bc79a0d8a98d240e08172`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://paretosec.com/contact — title: Contact : Pareto Securities

SHA-256: `1e5261907e1641e28ab2f419dff0a1d9a5b1c92b28cf99a1ff16bed283fbd82a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "741510391"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://paretosec.com/energy-conference — title: Energy Conference : Pareto Securities

SHA-256: `18a1c51a77da955ce1676a15846ce5e42c2654999f8a2bdd3e63028822eda724`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://paretosec.com/updates/events-and-conferences — title: Events & Conferences | Pareto Securities : Pareto Securities

SHA-256: `b838e062fb5983b04ef3e3cfdd6ba387dbdf3791c7a0a682a0332e33d06db152`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://paretosec.com/terms-of-use — title: Terms of use : Pareto Securities

SHA-256: `b5456e57af81bb881c50487e5783e4247f66d066044128443810da8d0a758910`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://paretosec.com/kontakt — title: Pareto Securities - The Nordic Gateway : Pareto Securities

SHA-256: `8fecae60b1110c25a069d209053fa886051b8efbba5a9b59b126e37fd93dd454`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 933581411 / PAW BYGG AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://pawbygg.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: pawbygg.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: paw-bygg.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: pawbygg.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: paw-bygg.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://pawbygg.no/; recorded rule: `None`; level: not saved.

Page: https://pawbygg.no/ — title: www.pawbygg.no

SHA-256: `e6650452947240047f1ec934d0d20be939c4de7d5081d8af466bda99749ca09a`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pawbygg.no/kontakt — title: 404 Not Found

SHA-256: `83b669e566e408f0eca82a159a559ea1bce7bf4eea5f7b6f24f48bac72628161`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pawbygg.no/om-oss — title: 404 Not Found

SHA-256: `83b669e566e408f0eca82a159a559ea1bce7bf4eea5f7b6f24f48bac72628161`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pawbygg.no/personvern — title: 404 Not Found

SHA-256: `83b669e566e408f0eca82a159a559ea1bce7bf4eea5f7b6f24f48bac72628161`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pawbygg.no/personvernerklaering — title: 404 Not Found

SHA-256: `83b669e566e408f0eca82a159a559ea1bce7bf4eea5f7b6f24f48bac72628161`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pawbygg.no/kontakt-oss — title: 404 Not Found

SHA-256: `83b669e566e408f0eca82a159a559ea1bce7bf4eea5f7b6f24f48bac72628161`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 912238504 / TERMINALEN BYSCENE AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.terminalenbyscene.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: terminalenbyscene.no; recorded rule: `corroboration`; level: LOW.
- Candidate: terminalen-byscene.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: terminalenbyscene.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: terminalen-byscene.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://terminalenbyscene.no/; recorded rule: `None`; level: not saved.

Page: https://www.terminalenbyscene.no/ — title: Terminalen Byscene

SHA-256: `e64d1096a76e9a68facb4b8f9ed1782d0089fe003257c221d0d1e5f24f4e2504`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.terminalenbyscene.no/kontakt — title: Kontakt — Terminalen Byscene

SHA-256: `6245edf08b0c2c771da4e8858d2c5370719aea3bc62564c9da1a7ad825d3eb26`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.terminalenbyscene.no/om-oss — title: Terminalen Byscene

SHA-256: `2515893c985089c2c66b872a9bfd74e7f77d2df190a65020b1cefe35f343b4ea`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.terminalenbyscene.no/personvern — title: Terminalen Byscene

SHA-256: `2515893c985089c2c66b872a9bfd74e7f77d2df190a65020b1cefe35f343b4ea`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 925622605 / PERHO AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://perho.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: perho.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: perho.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://perho.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: perho.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://perho.no/; recorded rule: `None`; level: not saved.
- Candidate: https://perho.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://perho.com/; recorded rule: `None`; level: not saved.

Page: https://perho.no/ — title: PERHOSIDEN kommer snart

SHA-256: `0c7a9169f0c04b7d4152c78ec65ca55b58e356e982a994b63219c38e9ab62d63`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://perho.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://perho.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://perho.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://perho.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://perho.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://perho.com/ — title: Koti ja työ Perhossa - Perhon kunta

SHA-256: `480f2b038567643e68f436fbd5f89193f2a0c1a8604bbc05996faf459ebc79db`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://perho.com/kontakt — title: Page not found - Perhon kunta

SHA-256: `66e0f55fb626bbf0e9e82c18c65b8451aa436b7ba9a611b1ec8d0d5ade00a1c2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 998309530 / HÅRFOKUS AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: haarfokus.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: harfokus.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: haarfokus.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: harfokus.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://xn--hrfokus-exa.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: xn--hrfokus-exa.no; recorded rule: `corroboration`; level: LOW.
- Candidate: xn--hrfokus-exa.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://xn--hrfokus-exa.no/; recorded rule: `None`; level: not saved.

Page: https://xn--hrfokus-exa.no/ — title: hårfokus.no — Alt om hår i Norge

SHA-256: `8589771265553d99982750c1f9f6a891b582f8016870c7126d48c89bb9aea751`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://xn--hrfokus-exa.no/kontakt/ — title: Kontakt | hårfokus.no

SHA-256: `0bd78f86ed99099a9b06cb75f5b6cd4bf7362d05bd5d534e473401f9916eea8a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://xn--hrfokus-exa.no/om-oss/ — title: Om oss | hårfokus.no

SHA-256: `d8a009015343bfa9676be4f929b0b1d017cb4e02a2d51e3e9b4980a829f73c8b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://xn--hrfokus-exa.no/personvern/ — title: Personvern | hårfokus.no

SHA-256: `f740a6a0fc6b3a781a99bb38665f304bac33d51f528a08dced9824d57844f152`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 915412262 / MOHEIA BORETTSLAG

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://helgelandbbl.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: helgelandbbl.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: moheiaborettslag.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: moheia-borettslag.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: moheiaborettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: moheia-borettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.helgelandbbl.no/; recorded rule: `None`; level: not saved.

Page: https://helgelandbbl.no/ — title: Helgeland BBL

SHA-256: `5b285d2a9fd1af73ad6e7f07e2364a05decbe503c8242b718d6af9f051b1feb3`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hopp rett til innholdet MELD SKADE FORKJØPSRETT MIN SIDE LEDIG STILLING BLI MEDLEM MENY Forkjøpsrett Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev For deg Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie For beboere Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog For styret Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal Tjenester Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester Om HELBO Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser boligselskap Eiendomsmegling For deg Alt om å være medlem i Helgeland BBL Se boliger med forkjøpsrett Medlemsskap Medlemsfordeler Hva er forkjøpsrett? Medlemsinfo til din mobil Leie til eie For styret Tjenester skreddersydd for borettslag og sameier Styreseminar Portal Basistjenester Renovering og vedlikehold Boligservice Ny i styret Om HELBO Totalleverandør av tjenester for boligselskap på Helgeland Styreseminar Portal Basistjenester Renovering og vedlikehold Boligservice Ny i styret Gi et medlemskap i gave og send dine nærmeste foran i boligkøen på sikt. Gi medlemsskap Nyttig lesestoff 7 oktober 2026 Styreseminar 2026 Det er med stor glede vi inviterer til årets styreseminar, som denne gangen blir på Meyergården hotell, Mo i Rana. 21 mai 2026 Satser sammen for å styrke boligmarkedet: – Kundene skal merke forskjellen Samarbeidet mellom Helgeland Boligbyggelag, Grong Sparebank og Aktiv Eiendomsmegling Helgeland er blitt stadig tettere de siste årene. Nå tar de et nytt steg, med felles eierskap i eiendomsmeglerkjeden Aktiv Helgeland.... 19 mai 2025 Først i køen for bærekraftsrapportering: Ormenget borettslag går foran Hvordan står det egentlig til med bomiljø, energiforbruk og plastsortering i borettslaget ditt? I Ormenget i Mo i Rana har styret begynt å systematisere svarene. Nå tester de ut et... 6 mai 2025 – Det handler ikke bare om å bo her, det handler om å være en del av noe Borettslaget Hagen 2 i Mosjøen er ikke som alle andre borettslag. Her er det ingen vaktmester, og beboerne er ikke tilskuere, de er deltakere. Det var tanken da de 24... 28 mars 2025 Mye har skjedd i løpet av de 43 årene Heidi har bodd i borettslaget Stormyra borettslag har vært Heidi Valviks hjem i 43 år, og i 20 av dem har hun hatt ansvaret som styreleder. Men i februar i år ga hun stafettpinnen videre.... 20 mars 2025 Grete takker av etter 30 år som styreleder Siden 1954 har de 136 leilighetene i kvartal 48 vært et viktig landemerke for ranværingene. De fleste har et forhold til Sentrum borettslag, enten de har bodd der selv, hatt... Vis flere artikler FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Search for: Hurtigvalg Helgeland BBL Forside Helgeland BBL Forside MIN SIDE MIN SIDE BLI MEDLEM BLI MEDLEM BO & LEV BO & LEV EIENDOMSMEGLING EIENDOMSMEGLING LEDIG STILLING LEDIG STILLING FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Kontakt Tlf: 75 13 70 00 E-Post: post@helgelandbbl.no Følg oss på facebook https://www.facebook.com/helgelandbbl Åpningstider Mandag - Fredag 08:00 - 15:00 Besøksadresse O.T. Olsens gt. 7, 8622 Mo i Rana Strandgata 10, 8656 Mosjøen Torolv Kveldulvsonsgate 25, Sandnesssjøen Nyttig Lesestoff helgelandbbl.no/bolev Designet av Spiren Design AS . Utviklet av Awati AS | Personvernerklæring Begynn å skrive og trykk enter for å søke Søk … Administrer samtykke For å gi de beste opplevelsene bruker vi teknologier som informasjonskapsler for å lagre og/eller få tilgang til enhetsinformasjon. Å samtykke til disse teknologiene vil tillate oss å behandle data som nettleseratferd eller unike ID-er på dette nettstedet. Å ikke samtykke eller trekke tilbake samtykke kan ha negativ innvirkning på visse egenskaper og funksjoner. Funksjonell Funksjonell Alltid aktiv Preferanser Preferanser Statistikk Statistikk Markedsføring Markedsføring Administrer alternativer Administrer tjenester Administrer {vendor_count} leverandører Les mer om disse formålene Aksepter Benekte Se preferanser Lagre preferanser Se preferanser {title} {title} {title} Administrer samtykke Skroll til toppen"
  ]
}
```

Page: https://helgelandbbl.no/kontakt/ — title: Kontakt - Helgeland BBL

SHA-256: `21975b4a4d8c1514af17d78ccec022f1244a144b96ad930b52c866dd3bab56d2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "948205149"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hopp rett til innholdet MELD SKADE FORKJØPSRETT MIN SIDE LEDIG STILLING BLI MEDLEM MENY Forkjøpsrett Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev For deg Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie For beboere Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog For styret Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal Tjenester Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester Om HELBO Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser boligselskap Eiendomsmegling Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser Eiendomsmegling Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser Eiendomsmegling Åpningstider Mandag - Fredag 08:00 - 15:00 Kontakt oss E-post: post@helgelandbbl.no Telefon: 75 13 70 00 Org.nr.: 948 205 149 Besøksadresse O.T. Olsens gt. 7, 8622 Mo i Rana Strandgata 10, 8656 Mosjøen Torolv Kveldulvsonsgate 25, 8800 Sandnessjøen Postadresse Postboks 1013, Sentrum 8602 Mo i Rana Fakturaadresse Helgeland Boligbyggelag 948205149 Postboks 2726, 7439 Trondheim Faktura kan også sendes på email: 948205149@senddocuments.io EHF: org.nr. 948 205 149 Kontaktskjema Bruk kontaktskjemaet nedenfor for å komme i dialog med oss. Du vil bli kontaktet så fort din henvendelse har vært inne til behandling. FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Search for: Hurtigvalg Helgeland BBL Forside Helgeland BBL Forside MIN SIDE MIN SIDE BLI MEDLEM BLI MEDLEM BO & LEV BO & LEV EIENDOMSMEGLING EIENDOMSMEGLING LEDIG STILLING LEDIG STILLING FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Kontakt Tlf: 75 13 70 00 E-Post: post@helgelandbbl.no Følg oss på facebook https://www.facebook.com/helgelandbbl Åpningstider Mandag - Fredag 08:00 - 15:00 Besøksadresse O.T. Olsens gt. 7, 8622 Mo i Rana Strandgata 10, 8656 Mosjøen Torolv Kveldulvsonsgate 25, Sandnesssjøen Nyttig Lesestoff helgelandbbl.no/bolev Designet av Spiren Design AS . Utviklet av Awati AS | Personvernerklæring Begynn å skrive og trykk enter for å søke Søk … Administrer samtykke For å gi de beste opplevelsene bruker vi teknologier som informasjonskapsler for å lagre og/eller få tilgang til enhetsinformasjon. Å samtykke til disse teknologiene vil tillate oss å behandle data som nettleseratferd eller unike ID-er på dette nettstedet. Å ikke samtykke eller trekke tilbake samtykke kan ha negativ innvirkning på visse egenskaper og funksjoner. Funksjonell Funksjonell Alltid aktiv Preferanser Preferanser Statistikk Statistikk Markedsføring Markedsføring Administrer alternativer Administrer tjenester Administrer {vendor_count} leverandører Les mer om disse formålene Aksepter Benekte Se preferanser Lagre preferanser Se preferanser {title} {title} {title} Administrer samtykke Skroll til toppen"
  ]
}
```

Page: https://helgelandbbl.no/kort-om-oss/ — title: Kort om oss - Helgeland BBL

SHA-256: `01617e6525e4b13ab760f28255115442e351453eac931deae1ed5bfeae43244d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "regnskap",
    "regnskap"
  ],
  "agency_credit_lines": [
    "Hopp rett til innholdet MELD SKADE FORKJØPSRETT MIN SIDE LEDIG STILLING BLI MEDLEM MENY Forkjøpsrett Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev For deg Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie For beboere Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog For styret Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal Tjenester Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester Om HELBO Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser boligselskap Eiendomsmegling Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser Eiendomsmegling Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser Eiendomsmegling Om oss HELBO er totalleverandør av forvaltningstjenester til over 270 boligselskap med i overkant av 5.500 boliger fordelt på de fleste kommuner på Helgeland. Vi har kontor i Brønnøysund, Sandnessjøen, Mosjøen og Mo i Rana. Vår kompetanse - din trygghet Primærtjenestene er regnskap og rådgivning for boligselskap. Våre tjenester holder faglig høy standard med krav til sertifiseringer og autorisasjoner. Tekniske tjenester Vår tekniske avdeling tilbyr et bredt spekter av tjenester, som boligtakst og prosjekt- og byggeledelse ved vedlikehold og renovering. Vi utarbeider tilstandsrapporter, vedlikeholdsplaner, håndterer skadesaker samt gir byggeteknisk rådgivning. Forutsigbarhet Vedlikeholdsplaner som sikrer et godt planlagt vedlikehold, gir god driftsøkonomi for boligselskapet. Det gir forutsigbarhet i vedlikeholdskostnadene, samtidig som det bidrar til å øke verdien på boligene. Boligservice Gressklipping og hagearbeid, rydding og bortkjøring, utvendig renhold og snørydding rundt inngangsparti. Dette er noe av det som utføres gjennom vår vaktmestertjeneste. Dette sikrer deg profesjonelt utførte tjenester - og mer fritid til deg selv. FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Search for: Hurtigvalg Helgeland BBL Forside Helgeland BBL Forside MIN SIDE MIN SIDE BLI MEDLEM BLI MEDLEM BO & LEV BO & LEV EIENDOMSMEGLING EIENDOMSMEGLING LEDIG STILLING LEDIG STILLING FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Kontakt Tlf: 75 13 70 00 E-Post: post@helgelandbbl.no Følg oss på facebook https://www.facebook.com/helgelandbbl Åpningstider Mandag - Fredag 08:00 - 15:00 Besøksadresse O.T. Olsens gt. 7, 8622 Mo i Rana Strandgata 10, 8656 Mosjøen Torolv Kveldulvsonsgate 25, Sandnesssjøen Nyttig Lesestoff helgelandbbl.no/bolev Designet av Spiren Design AS . Utviklet av Awati AS | Personvernerklæring Begynn å skrive og trykk enter for å søke Søk … Administrer samtykke For å gi de beste opplevelsene bruker vi teknologier som informasjonskapsler for å lagre og/eller få tilgang til enhetsinformasjon. Å samtykke til disse teknologiene vil tillate oss å behandle data som nettleseratferd eller unike ID-er på dette nettstedet. Å ikke samtykke eller trekke tilbake samtykke kan ha negativ innvirkning på visse egenskaper og funksjoner. Funksjonell Funksjonell Alltid aktiv Preferanser Preferanser Statistikk Statistikk Markedsføring Markedsføring Administrer alternativer Administrer tjenester Administrer {vendor_count} leverandører Les mer om disse formålene Aksepter Benekte Se preferanser Lagre preferanser Se preferanser {title} {title} {title} Administrer samtykke Skroll til toppen"
  ]
}
```

Page: https://helgelandbbl.no/personvernerklaering-eu/ — title: Personvernerklæring (EU) - Helgeland BBL

SHA-256: `5962ee2b54e2ee5e7c01cabba403ef41a96ab22b1f9dc3a73007f16efa8bafe5`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hopp rett til innholdet MELD SKADE FORKJØPSRETT MIN SIDE LEDIG STILLING BLI MEDLEM MENY Forkjøpsrett Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev For deg Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie For beboere Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog For styret Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal Tjenester Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester Om HELBO Kort om oss Kontakt Styret Åpenhetsloven Vedtekter HELBO Våre ansatte Adresser boligselskap Eiendomsmegling Personvernerklæring (EU) Denne personvernerklæringen ble sist oppdatert 30. juni 2026 og gjelder statsborgere og lovlige fastboende i Det europeiske økonomiske samarbeidsområdet og Sveits. I denne personvernerklæringen forklarer vi hva vi gjør med opplysningene vi innhenter om deg via https://helgelandbbl.no . Vi anbefaler deg å lese denne erklæringen nøye. I vår behandling overholder vi kravene i personvernlovgivningen. Det betyr blant annet at: vi oppgir tydelig om hvilke formål vi behandler personopplysninger for. Vi gjør dette ved hjelp av denne personvernerklæringen; vi tar sikte på å begrense vår innsamling av personopplysninger til bare de personopplysningene som er nødvendige for legitime formål; vi ber først om ditt eksplisitte samtykke til å behandle dine personopplysninger i tilfeller som krever ditt samtykke; vi tar nødvendige sikkerhetstiltak for å beskytte dine personopplysninger og krever også dette fra parter som behandler personopplysninger på våre vegne; vi respekterer din rett til å få tilgang til dine personopplysningene eller få opplysningene korrigert eller slettet, på forespørsel. Hvis du har spørsmål, eller ønsker å vite nøyaktig hvilke data vi oppbevarer om deg, kan du kontakte oss. 1. Formål, data og oppbevaringsperiode Vi samler eller mottar personlig informasjon av ulike årsaker knyttet til tjenestene våre. Dette kan inkludere følgende: (klikk for å utvide) 1.1 Kontakt - via telefon, e-post, og/eller nett-skjema For dette formålet bruker vi følgende data: Et fornavn og etternavn En hjemmeadresse eller annen fysisk adresse, inkludert navn på gate og navn på by eller sted En e-post adresse Et telefonnummer Fødselsdato Grunnlaget for at vi kan behandle disse dataene er: Det er nødvendig for gjennomføring av en kontrakt eller foreløpige prosedyrer knyttet til en kontrakt som den registrerte er part i. Oppbevaringsperiode Ved avslutning av tjenesten beholder vi disse dataene for følgende periode: 5 år. 2. Cookies Nettstedet vårt bruker cookies. For mer informasjon om cookies, se vår Cookieerklæring . 3. Formidlingspraksis Vi utleverer personopplysninger hvis vi er pålagt det ved lov eller ved rettskjennelse, som svar til et rettshåndhevende organ, i den grad det er tillatt i henhold til andre lovbestemmelser, for å gi informasjon, eller for en etterforskning av en sak knyttet til offentlig sikkerhet. Hvis nettstedet eller organisasjonen vår blir overdratt, solgt eller fusjonert, kan opplysningene dine bli utlevert til våre rådgivere og eventuelle potensielle kjøpere og vil bli gitt videre til de nye eierne. Vi har inngått en databehandlingsavtale med Google. Google kan ikke bruke dataene til andre Google-tjenester. 4. Sikkerhet Vi er forpliktet til å ivareta sikkerheten for personopplysninger. Vi gjør nødvendige sikkerhetstiltak for å begrense misbruk av og uautorisert tilgang til personopplysninger. Dette sikrer at kun de nødvendige personene har tilgang til dine data, at tilgangen til dataene er beskyttet, og at våre sikkerhetstiltak regelmessig blir gjennomgått. 5. Tredjeparts nettsteder Denne personvernerklæringen gjelder ikke for tredjeparts-nettsteder som kobles til via lenker på nettstedet vårt. Vi kan ikke garantere at disse tredjepartene behandler dine personopplysninger på en pålitelig eller sikker måte. Vi anbefaler at du leser personvernerklæringene til disse nettstedene før du bruker disse nettstedene. 6. Endringer i denne personvernerklæringen Vi forbeholder oss retten til å gjøre endringer i denne personvernerklæringen. Det anbefales at du konsulterer denne personvernerklæringen regelmessig for å være oppmerksom på eventuelle endringer. I tillegg vil vi aktivt informere deg der det er mulig. 7. Få tilgang til og endre dataene dine Hvis du har spørsmål eller ønsker å vite hvilke personopplysninger vi har om deg, kan du kontakte oss. Du kan kontakte oss ved å bruke informasjonen nedenfor. Du har følgende rettigheter: Du har krav på å få vite hvorfor dine personopplysninger trengs, hva som vil skje med dem, og hvor lenge de vil bli oppbevart. Rett til innsyn: Du har rett til innsyn i dine personopplysninger som er kjent for oss. Rett til retting: Du har rett til å tilføye, korrigere, og å ha dine personlige data slettet eller blokkert når du måtte ønske det.. Hvis du gir oss ditt samtykke til å behandle dataene dine, har du rett til å tilbakekalle det samtykket og å få dine personlige data slettet. Rett til å overføre dine data: du har rett til å be om alle dine personopplysninger fra behandlingsansvarlig og overføre dem i sin helhet til en annen behandlingsansvarlig. Rett til å nekte: Du kan nekte at dine data blir behandlet. Vi etterkommer dette med mindre det er berettige grunner for behandling. Vennligst sørg for å alltid oppgi tydelig hvem du er, slik at vi kan være sikre på at vi ikke modifiserer eller sletter data fra feil person. 8. Innsending av klage Hvis du ikke er fornøyd med måten vi håndterer (en klage på) behandlingen av dine personopplysninger, har du rett til å sende inn en klage til Datatilsynet. 9. Kontaktdetaljer Helgeland Boligbyggelag Postboks 1013 Sentrum, 8602 Mo i Rana Norge Nettsted: https://helgelandbbl.no E-post: post@ ex.com helgelandbbl.no Telefonnummer: +4775137000 10. Dataforespørsler For de oftest innsendte forespørslene tilbyr vi deg også muligheten til å bruke vårt dataforespørselsskjema × Navn Navn E-post Send inn en forespørsel om tilgang til dataene vi behandler om deg. Send inn en forespørsel om sletting av dataene dersom det ikke lenger er aktuelt. Send inn en forespørsel om å motta en eksportfil med dataene vi behandler om deg. FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Search for: Hurtigvalg Helgeland BBL Forside Helgeland BBL Forside MIN SIDE MIN SIDE BLI MEDLEM BLI MEDLEM BO & LEV BO & LEV EIENDOMSMEGLING EIENDOMSMEGLING LEDIG STILLING LEDIG STILLING FORKJØPSRETT Om forkjøpsrett Boliger med forkjøpsrett Felles forkjøpsrett Eiendomsmegling Bo&Lev FOR DEG Bli medlem Gavemedlemskap Overfør medlemsskap Endre adresse Medlemsfordeler Medlemsrettigheter Medlemsinfo til din mobil Strandgata leie til eie FOR BEBOERE Registrer eller slett medeier Overføring av bolig Utleie av egen bolig Fellesgjeld i borettslag Skjemakatalog FOR STYRET Styreseminar Ny i styret Basistjenester Boligservice Individuell nedbetaling Portal TJENESTER Tekniske tjenester Renovering og vedlikehold Vedlikeholdsplan Vannsjekken Taksering Forsikringer Vaktmestertjenester OM HELGELAND BBL Kort om oss Kontakt Styret Vedtekter Helgeland BBL Våre ansatte Adresser boligselskap Eiendomsmegling MELD SKADE Kontakt Tlf: 75 13 70 00 E-Post: post@helgelandbbl.no Følg oss på facebook https://www.facebook.com/helgelandbbl Åpningstider Mandag - Fredag 08:00 - 15:00 Besøksadresse O.T. Olsens gt. 7, 8622 Mo i Rana Strandgata 10, 8656 Mosjøen Torolv Kveldulvsonsgate 25, Sandnesssjøen Nyttig Lesestoff helgelandbbl.no/bolev Designet av Spiren Design AS . Utviklet av Awati AS | Personvernerklæring Begynn å skrive og trykk enter for å søke Søk … Administrer samtykke For å gi de beste opplevelsene bruker vi teknologier som informasjonskapsler for å lagre og/eller få tilgang til enhetsinformasjon. Å samtykke til disse teknologiene vil tillate oss å behandle data som nettleseratferd eller unike ID-er på dette nettstedet. Å ikke samtykke eller trekke tilbake samtykke kan ha negativ innvirkning på visse egenskaper og funksjoner. Funksjonell Funksjonell Alltid aktiv Preferanser Preferanser Statistikk Statistikk Markedsføring Markedsføring Administrer alternativer Administrer tjenester Administrer {vendor_count} leverandører Les mer om disse formålene Aksepter Benekte Se preferanser Lagre preferanser Se preferanser {title} {title} {title} Administrer samtykke Skroll til toppen"
  ]
}
```
## 20261017 / 930012130 / AWI HOLDING AS

Categories: veto; terminal website state: not_available.

- Candidate: awiholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: awi-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: awiholding.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: awi-holding.com; recorded rule: `group_without_exact_orgnr`; level: REJECT.
- Candidate: https://awi-holding.com/; recorded rule: `None`; level: not saved.

Page: https://awi-holding.com/ — title: awi-holding.com

SHA-256: `d6b67f2c7f14ff00c9c554a3a46d7cf80f3d1f44212f8952ff45a530b9783c4e`; candidate rules: group_without_exact_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "holding",
    "holding",
    "holding",
    "holding",
    "holding",
    "holding"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261017 / 934616081 / DICKSON NAPRAPATI AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.naprapatgruppen.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: naprapatgruppen.no; recorded rule: `corroboration`; level: LOW.
- Candidate: dicksonnaprapati.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: dickson-naprapati.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: dicksonnaprapati.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: dickson-naprapati.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://naprapatgruppen.no/; recorded rule: `None`; level: not saved.

Page: https://www.naprapatgruppen.no/ — title: Muskel -og leddbehandling | naprapatgruppen

SHA-256: `c6eddf2ebe8c3aea2ce4de588bd9204a3baa68c794f90408b22c3640dbdc9a5d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.naprapatgruppen.no/kontakt-oss — title: Kontakt oss | naprapatgruppen

SHA-256: `bee6afccb0ea7ff7dc5f54b35dc8653bc7b60007c3f9d59cda1d958fdc9e428d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.naprapatgruppen.no/kontakt — title: 404 Error: Page Not Found

SHA-256: `e0b60c6a699c9adae2292950cbaa850b3990eb7b5cd6902345e7479a1162b35a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 823569262 / MAGNA PROSJEKT SØR AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: magnaprosjektsoer.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: magna-prosjekt-soer.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: magnaprosjektsoer.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: magna-prosjekt-soer.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://magnaprosjektsor.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: magnaprosjektsor.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: magnaprosjektsor.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: magna-prosjekt-sor.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: magna-prosjekt-sor.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--magna-prosjekt-sr-g1b.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--magnaprosjektsr-jub.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--magna-prosjekt-sr-g1b.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--magnaprosjektsr-jub.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://magnaprosjektsor.no/; recorded rule: `None`; level: not saved.

Page: https://magnaprosjektsor.no/ — title: Prosjektledelse og rådgivning | Magna Prosjekt Sør

SHA-256: `ac36255b26e97c23d6c917a7670039174b1dda33063b9eed6c916c8e67beedbb`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Tjenester Om oss Prosjekter Karriere Kontakt En samarbeidspartner i utfordrende prosjekter PROSJEKTLEDELSE OG RÅDGIVNING Kompetanse og erfaring betyr noe Vi består av personell med årelang erfaring som bidragsyter på mange store og små prosjekter. Selskapet er ungt, men de ansatte kjenner hverandre fra mange år tilbake. I Magna Prosjekt Sør vil vi vise at kompetanse og erfaring betyr noe. våre prosjekter Vi bistår i alle sentrale roller i et prosjekt  Prosjektledelse Prosjektledelse er et fag. Ingen prosjekter er like, men strukturen i gjennomføringen er den samme. I samarbeid med våre kolleger i øst har vi utviklet en prosjekthåndbok som danner grunnlag for gjennomføringen. Den bruker vi som mal og oppslagsbok for vårt arbeid og deler gjerne erfaringen med våre oppdragsgivere.  Byggherreombud Vi kan påta oss rollen som byggherreombud i totalentrepriser, som vil si at vi stiller som arbeidsgivers «profesjonelle hjelper». Ved å engasjere oss som byggherreombud får du som byggherre en ekstra trygghet i prosjektet ditt. Vi bidrar blant annet med kontraktsinngåelser, økonomisk kontroll og ivaretagelse av kravet om sikkerhet, helse og arbeidsmiljø (SHA).  Anskaffelser og kontrakter Anskaffelsesstrategien må være en integrert del av prosjektets prosjektmandat. Hensikten med å beskrive anskaffelsesstrategien er å sikre at anskaffelsesaktivitetene understøtter prosjektets hovedmål og gjennomføringstid. Anskaffelsesstrategien skal være en del av prosjektgjennomføringsplanen.  Prosjekteringsledelse Ethvert bygg- og anleggsarbeid må planlegges nøye for å lykkes. Arbeidet må beskrives i detalj, tegninger må produseres og beregninger må gjøres slik at resultatet blir trygt og innenfor gjeldende lover og forskrifter. Vi produseres gode løsninger og tegninger slik at alle som jobber på byggeprosjektet kan jobbe effektivt.  Planlegging Hovedtidsplanen skal være en overordnet plan som viser alle faser i prosjektet, samt hoved­aktivitetene/kontrakter og viktige avhengigheter i hver fase. Prosjektets hovedmilepæler skal fremgå av planen. Normalt vil en hovedtidsplan være dokumentert på en side. Under denne etableres det to nivåer, som skal sikre fremdriften i prosjekteringen Nivå 2, samt detaljplaner (Nivå 3) som skal gi de utførende tilstrekkelig informasjon til at de kan samhandle med alle på byggeplassen.  Byggledelse Vi gir oppdragsgiver all nødvendige bistand med å styre og følge opp både små og store prosjektet i utførelsesfasen. Vi benytter personell med lang og bred erfaring fra bygge- og anleggsledelse. I tillegg tilbyr vi også teknisk byggeledelse innenfor elektro og VVS-fag.  SHA Byggherreforskriften stiller krav til at alle byggeprosjekt av en viss størrelse skal ha en oppfølging i forhold til sikkerhet, helse og arbeidsmiljø. Som uavhengig rådgiver kan flere av våre medarbeidere bistå alle byggherrer med å ivareta de forpliktelser byggherreforskriften krever.  Ansvarlig søk Det skal være et firma som står som ansvarlig søker for de aller fleste bygge og anleggsprosjekt i Norge. Med sentral godkjenning i tiltaksklasse 3 kan våre ansatte bistå byggherre / entreprenør med alle typer byggesøknader uavhengig av størrelse og kompleksitet.  Prosessledelse Som uavhengig rådgiver kan våre kompetente medarbeidere bistå med å utvikle eiendom igjennom gode planprosesser ved å hente gode ressurser fra ulike fagmiljø. Vi bistår i alle sentrale roller i et prosjekt Prosjektledelse Prosjektledelse er et fag. Ingen prosjekter er like, men strukturen i gjennomføringen er den samme. I samarbeid med våre kolleger i øst har vi utviklet en prosjekthåndbok som danner grunnlag for gjennomføringen. Den bruker vi som mal og oppslagsbok for vårt arbeid og deler gjerne erfaringen med våre oppdragsgivere. Byggeherreombud Vi kan påta oss rollen som byggherreombud i totalentrepriser, som vil si at vi stiller som arbeidsgivers “profesjonelle hjelper”. Ved å engasjere oss som byggherreombud får du som byggherre en ekstra trygghet i prosjektet ditt. Vi bidrar blant annet med kontraktsinngåelser, økonomisk kontroll og ivaretagelse av kravet om sikkerhet, helse og arbeidsmiljø (SHA). Anskaffelser og kontrakter Anskaffelsesstrategien må være en integrert del av prosjektets prosjektmandat. Hensikten med å beskrive anskaffelsesstrategien er å sikre at anskaffelsesaktivitetene understøtter prosjektets hovedmål og gjennomføringstid. Anskaffelsesstrategien skal være en del av prosjektgjennomføringsplanen. Prosjekteringsledelse Ethvert bygg- og anleggsarbeid må planlegges nøye for å lykkes. Arbeidet må beskrives i detalj, tegninger må produseres og beregninger må gjøres slik at resultatet blir trygt og innenfor gjeldende lover og forskrifter. Vi produseres gode løsninger og tegninger slik at alle som jobber på byggeprosjektet kan jobbe effektivt. Planlegging Hovedtidsplanen skal være en overordnet plan som viser alle faser i prosjektet, samt hoved­aktivitetene/kontrakter og viktige avhengigheter i hver fase. Prosjektets hovedmilepæler skal fremgå av planen. Normalt vil en hovedtidsplan være dokumentert på en side. Under denne etableres det to nivåer, som skal sikre fremdriften i prosjekteringen Nivå 2, samt detaljplaner (Nivå 3) som skal gi de utførende tilstrekkelig informasjon til at de kan samhandle med alle på byggeplassen. Byggledelse Vi gir oppdragsgiver all nødvendige bistand med å styre og følge opp både små og store prosjektet i utførelsesfasen. Vi benytter personell med lang og bred erfaring fra bygge- og anleggsledelse. I tillegg tilbyr vi også teknisk byggeledelse innenfor elektro og VVS-fag. SHA Byggherreforskriften stiller krav til at alle byggeprosjekt av en viss størrelse skal ha en oppfølging i forhold til sikkerhet, helse og arbeidsmiljø. Som uavhengig rådgiver kan flere av våre medarbeidere bistå alle byggherrer med å ivareta de forpliktelser byggherreforskriften krever. Ansvarlig søk Det skal være et firma som står som ansvarlig søker for de aller fleste bygge og anleggsprosjekt i Norge. Med sentral godkjenning i tiltaksklasse 3 kan våre ansatte bistå byggherre / entreprenør med alle typer byggesøknader uavhengig av størrelse og kompleksitet. Prosessledelse Som uavhengig rådgiver kan våre kompetente medarbeidere bistå med å utvikle eiendom igjennom gode planprosesser ved å hente gode ressurser fra ulike fagmiljø. Agderbygg Eiendom Ulike roller Sørlandsparken ØST AS Infrastruktur anlegg og tomteopparbeidelser Elkem Northern Recharge Kontrakt og anskaffelser Entra ASA Kontorbygg Spørsmål og henvendelser Finn riktig kontaktperson TA KONTAKT bli med på laget Karriere som prosjektleder? Karriere som prosjekteringsleder? Karriere som byggeleder? Karriere som anleggsleder? Vi søker stadig flere engasjerte og dyktige medarbeidere. Kanskje er det nettopp deg? LES MER HER Tjenester Om oss Prosjekter Karriere Kontakt Kontor Kristiansand Gyldenløves gate 2, 4611 Kristiansand Kontor Mandal Kastellgata 34, 4514 Mandal Postadresse Postboks 216, 4503 Mandal Les om vår bruk av Cookies Utviklet av Warp Media 2026 © Magna Prosjekt Sør Vi bruker cookies (informasjonskapsler) for at nettsiden skal fungere som planlagt og for å analysere og forstå våre brukere. Det hjelper oss å optimalisere nettsiden. Les om vår bruk av cookies Innstillinger Godta"
  ]
}
```

Page: https://magnaprosjektsor.no/kontakt-oss/ — title: Vil du vite mer om hva vi kan tilby deg? | Kontakt oss - Magna Prosjekt Sør

SHA-256: `492f82b40881759541b6a4dc40dc712e84806c22c9ecb05b6aa5f66cfcd4b455`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Tjenester Om oss Prosjekter Karriere Kontakt Mona Mortensen tlf: 911 64 897 Daglig leder Send mail Aleksandar Petrovic tlf: 979 01 591 Prosjektleder Send mail Thorstein Dyrstad tlf: 952 37 668 Senior rådgiver Send mail Jan Hauge Nilsen tlf: 975 43 390 Senior Rådgiver Send mail Hilde Gulbrandsen tlf: 953 00 137 Prosjektleder Send mail Jens Birger Kristensen tlf: 959 86 305 Senior Rådgiver Send mail Espen Hille tlf: 909 85 403 Prosjektleder Send mail Frank Ole Rødal tlf: 915 89 838 Senior Rådgiver Send mail Øystein Salthaug tlf: 905 58 849 Senior rådgiver Send mail Tjenester Om oss Prosjekter Karriere Kontakt Kontor Kristiansand Gyldenløves gate 2, 4611 Kristiansand Kontor Mandal Kastellgata 34, 4514 Mandal Postadresse Postboks 216, 4503 Mandal Les om vår bruk av Cookies Utviklet av Warp Media 2026 © Magna Prosjekt Sør Vi bruker cookies (informasjonskapsler) for at nettsiden skal fungere som planlagt og for å analysere og forstå våre brukere. Det hjelper oss å optimalisere nettsiden. Les om vår bruk av cookies Innstillinger Godta"
  ]
}
```

Page: https://magnaprosjektsor.no/om-oss/ — title: Om oss - Prosjektledelse og rådgivning | Magna Prosjekt Sør

SHA-256: `a6d265c84245528b4b8b464f2f2656fcb4d2f2c24a33b8dba711b821254c8c92`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Tjenester Om oss Prosjekter Karriere Kontakt hvem er vi? Magna Prosjekt Sør I alle våre roller arbeider vi for byggherren med prosjektadministrasjon, helt uavhengig av de prosjekterende, enten som et samlet team eller som enkeltpersoner kundene våre engasjerer. Magna Prosjekt Sør holder til på Sørlandet, og har kontorer i Mandal og Kristiansand. Vi kjenner Sørlandet og aktørene her godt, og har korte kontaktlinjer mellom oss. Skulle vi ha behov for ytterlig kompetanse, så er veien kort til våre kolleger i øst. vårt arbeid Vi ønsker å ta ansvar for at våre kunder skal kunne stole på oss og de råd og oppgaver vi utfører på deres vegne. Møt teamet Magna Prosjekt Sør er sammensatt av et team med svært lang erfaring fra ledelse av komplekse prosjekter. Mona er utdannet sivilingeniør fra Newcastle, England, og har snart 40 års erfaring med prosjektledelse, hvorav de siste 20 årene som daglig leder for grunn- og byggentreprenører. send mail Mona Mortensen tlf: 911 64 897 Daglig leder send mail Aleksandar Petrovic tlf: 979 01 591 Prosjektleder Jens Birger er utdannet sivilingeniør og har lang erfaring med prosjekledelse, prosjekteringsledelse, byggeledelse og mer. Nå er Jens Birger senior rådgiver i Magna Prosjekt Sør. send mail Jens Birger Kristensen tlf: 959 86 305 Senior Rådgiver Jens Birger er utdannet sivilingeniør og har lang erfaring med prosjekledelse, prosjekteringsledelse, byggeledelse og mer. Nå er Jens Birger senior rådgiver i Magna Prosjekt Sør. send mail Øystein Salthaug tlf: 905 58 849 Senior Rådgiver Hilde er utdannet sivilingeniør og har lang erfaring med tverrfaglig prosess-, prosjekt- og prosjekteringsledelse. Hilde er prosjektleder i Magna. send mail Hilde Gulbrandsen tlf: 953 00 137 Prosjektleder send mail Espen Hille tlf: 909 85 403 Prosjektleder Jan er utdannet bygg- og anleggsingeniør med over 30 års erfaring fra bygg og anleggsbransjen. Han har fokus på prosjekt-, prosjekterings- og byggeledelse. send mail Jan Hauge Nilsen tlf: 975 43 390 Senior Rådgiver Thorstein er utdannet ingeniør og har over 40 års erfaring med blant annet kontrakter, innkjøp og prosjektledelse på mange ulike prosjekter. Thorstein har tidligere vært daglig leder i Magna Prosjekt Sør. send mail Thorstein Dyrstad tlf: 952 37 668 Senior Rådgiver Frank Ole er utdannet sivilingeniør og har lang erfaring med blant annet prosjekt-, prosjekterings- og byggeledelse/teknisk byggeledelse. send mail Frank Ole Rødal tlf: 915 89 838 Senior Rådgiver bli med på laget Karriere som prosjektleder? Karriere som prosjekteringsleder? Karriere som byggeleder? Karriere som anleggsleder? Vi søker stadig flere engasjerte og dyktige medarbeidere. Kanskje er det nettopp deg? LES MER HER Mona Mortensen Daglig leder Tlf: 911 64 897 Mona er utdannet sivilingeniør fra Newcastle, England, og har snart 40 års erfaring med prosjektledelse, hvorav de siste 20 årene som daglig leder for grunn- og byggentreprenører. Send mail Thorstein Dyrstad Senior rådgiver Tlf: 952 37 668 Thorstein er utdannet ingeniør og har over 40 års erfaring med blant annet kontrakter, innkjøp og prosjektledelse på mange ulike prosjekter. Thorstein har tidligere vært daglig leder i Magna Prosjekt Sør. Send mail Aleksandar Petrovic Prosjektleder tlf: 979 01 591 Aleksandar er masterutdannet sivilingeniør innen bygg- og anleggsteknikk. Prosjektleder med over 18 års erfaring fra byggebransjen. Han er VDC-sertifisert og har solid kompetanse innen prosjektledelse, kontrahering, HMS, økonomi, fremdrift og kvalitet. Send mail Hilde Gulbrandsen Prosjektleder tlf: 953 00 137 Hilde er utdannet sivilingeniør og har lang erfaring med tverrfaglig prosess-, prosjekt- og prosjekteringsledelse. Hilde er prosjektleder i Magna. Send mail Jan Hauge Nilsen Senior rådgiver tlf: 975 43 390 Jan er utdannet bygg- og anleggsingeniør med over 30 års erfaring fra bygg og anleggsbransjen. Han har fokus på prosjekt-, prosjekterings- og byggeledelse. Send mail Jens Birger Kristensen Senior rådgiver tlf: 959 86 305 Jens Birger er utdannet sivilingeniør og har lang erfaring med prosjekledelse, prosjekteringsledelse, byggeledelse og mer. Nå er Jens Birger senior rådgiver i Magna Prosjekt Sør. Send mail Espen Hille Prosjektleder tlf: 909 85 403 Espen er utdannet maskiningeniør og bedriftsøkonom, og har lang erfaring som prosjektleder fra bygge- og anleggsbransjen både på byggherre- og entreprenørsiden. Meget god teknisk og praktisk erfaring fra datasenterutbygging. Send mail Frank Ole Rødal Senior rådgiver tlf: 915 89 838 Frank Ole er utdannet sivilingeniør og har lang erfaring med blant annet prosjekt-, prosjekterings- og byggeledelse/teknisk byggeledelse. Send mail Øystein Salthaug Senior rådgiver tlf: 905 58 849 Øystein har solid erfaring fra rådgiverbransjen og har vært prosjektleder i en rekke store, sammensatte prosjekter. Øystein har også spisskompetanse innen Construction management og prosjekteringsledelse. Send mail Tjenester Om oss Prosjekter Karriere Kontakt Kontor Kristiansand Gyldenløves gate 2, 4611 Kristiansand Kontor Mandal Kastellgata 34, 4514 Mandal Postadresse Postboks 216, 4503 Mandal Les om vår bruk av Cookies Utviklet av Warp Media 2026 © Magna Prosjekt Sør Vi bruker cookies (informasjonskapsler) for at nettsiden skal fungere som planlagt og for å analysere og forstå våre brukere. Det hjelper oss å optimalisere nettsiden. Les om vår bruk av cookies Innstillinger Godta"
  ]
}
```

Page: https://magnaprosjektsor.no/ — title: Prosjektledelse og rådgivning | Magna Prosjekt Sør

SHA-256: `ac36255b26e97c23d6c917a7670039174b1dda33063b9eed6c916c8e67beedbb`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Tjenester Om oss Prosjekter Karriere Kontakt En samarbeidspartner i utfordrende prosjekter PROSJEKTLEDELSE OG RÅDGIVNING Kompetanse og erfaring betyr noe Vi består av personell med årelang erfaring som bidragsyter på mange store og små prosjekter. Selskapet er ungt, men de ansatte kjenner hverandre fra mange år tilbake. I Magna Prosjekt Sør vil vi vise at kompetanse og erfaring betyr noe. våre prosjekter Vi bistår i alle sentrale roller i et prosjekt  Prosjektledelse Prosjektledelse er et fag. Ingen prosjekter er like, men strukturen i gjennomføringen er den samme. I samarbeid med våre kolleger i øst har vi utviklet en prosjekthåndbok som danner grunnlag for gjennomføringen. Den bruker vi som mal og oppslagsbok for vårt arbeid og deler gjerne erfaringen med våre oppdragsgivere.  Byggherreombud Vi kan påta oss rollen som byggherreombud i totalentrepriser, som vil si at vi stiller som arbeidsgivers «profesjonelle hjelper». Ved å engasjere oss som byggherreombud får du som byggherre en ekstra trygghet i prosjektet ditt. Vi bidrar blant annet med kontraktsinngåelser, økonomisk kontroll og ivaretagelse av kravet om sikkerhet, helse og arbeidsmiljø (SHA).  Anskaffelser og kontrakter Anskaffelsesstrategien må være en integrert del av prosjektets prosjektmandat. Hensikten med å beskrive anskaffelsesstrategien er å sikre at anskaffelsesaktivitetene understøtter prosjektets hovedmål og gjennomføringstid. Anskaffelsesstrategien skal være en del av prosjektgjennomføringsplanen.  Prosjekteringsledelse Ethvert bygg- og anleggsarbeid må planlegges nøye for å lykkes. Arbeidet må beskrives i detalj, tegninger må produseres og beregninger må gjøres slik at resultatet blir trygt og innenfor gjeldende lover og forskrifter. Vi produseres gode løsninger og tegninger slik at alle som jobber på byggeprosjektet kan jobbe effektivt.  Planlegging Hovedtidsplanen skal være en overordnet plan som viser alle faser i prosjektet, samt hoved­aktivitetene/kontrakter og viktige avhengigheter i hver fase. Prosjektets hovedmilepæler skal fremgå av planen. Normalt vil en hovedtidsplan være dokumentert på en side. Under denne etableres det to nivåer, som skal sikre fremdriften i prosjekteringen Nivå 2, samt detaljplaner (Nivå 3) som skal gi de utførende tilstrekkelig informasjon til at de kan samhandle med alle på byggeplassen.  Byggledelse Vi gir oppdragsgiver all nødvendige bistand med å styre og følge opp både små og store prosjektet i utførelsesfasen. Vi benytter personell med lang og bred erfaring fra bygge- og anleggsledelse. I tillegg tilbyr vi også teknisk byggeledelse innenfor elektro og VVS-fag.  SHA Byggherreforskriften stiller krav til at alle byggeprosjekt av en viss størrelse skal ha en oppfølging i forhold til sikkerhet, helse og arbeidsmiljø. Som uavhengig rådgiver kan flere av våre medarbeidere bistå alle byggherrer med å ivareta de forpliktelser byggherreforskriften krever.  Ansvarlig søk Det skal være et firma som står som ansvarlig søker for de aller fleste bygge og anleggsprosjekt i Norge. Med sentral godkjenning i tiltaksklasse 3 kan våre ansatte bistå byggherre / entreprenør med alle typer byggesøknader uavhengig av størrelse og kompleksitet.  Prosessledelse Som uavhengig rådgiver kan våre kompetente medarbeidere bistå med å utvikle eiendom igjennom gode planprosesser ved å hente gode ressurser fra ulike fagmiljø. Vi bistår i alle sentrale roller i et prosjekt Prosjektledelse Prosjektledelse er et fag. Ingen prosjekter er like, men strukturen i gjennomføringen er den samme. I samarbeid med våre kolleger i øst har vi utviklet en prosjekthåndbok som danner grunnlag for gjennomføringen. Den bruker vi som mal og oppslagsbok for vårt arbeid og deler gjerne erfaringen med våre oppdragsgivere. Byggeherreombud Vi kan påta oss rollen som byggherreombud i totalentrepriser, som vil si at vi stiller som arbeidsgivers “profesjonelle hjelper”. Ved å engasjere oss som byggherreombud får du som byggherre en ekstra trygghet i prosjektet ditt. Vi bidrar blant annet med kontraktsinngåelser, økonomisk kontroll og ivaretagelse av kravet om sikkerhet, helse og arbeidsmiljø (SHA). Anskaffelser og kontrakter Anskaffelsesstrategien må være en integrert del av prosjektets prosjektmandat. Hensikten med å beskrive anskaffelsesstrategien er å sikre at anskaffelsesaktivitetene understøtter prosjektets hovedmål og gjennomføringstid. Anskaffelsesstrategien skal være en del av prosjektgjennomføringsplanen. Prosjekteringsledelse Ethvert bygg- og anleggsarbeid må planlegges nøye for å lykkes. Arbeidet må beskrives i detalj, tegninger må produseres og beregninger må gjøres slik at resultatet blir trygt og innenfor gjeldende lover og forskrifter. Vi produseres gode løsninger og tegninger slik at alle som jobber på byggeprosjektet kan jobbe effektivt. Planlegging Hovedtidsplanen skal være en overordnet plan som viser alle faser i prosjektet, samt hoved­aktivitetene/kontrakter og viktige avhengigheter i hver fase. Prosjektets hovedmilepæler skal fremgå av planen. Normalt vil en hovedtidsplan være dokumentert på en side. Under denne etableres det to nivåer, som skal sikre fremdriften i prosjekteringen Nivå 2, samt detaljplaner (Nivå 3) som skal gi de utførende tilstrekkelig informasjon til at de kan samhandle med alle på byggeplassen. Byggledelse Vi gir oppdragsgiver all nødvendige bistand med å styre og følge opp både små og store prosjektet i utførelsesfasen. Vi benytter personell med lang og bred erfaring fra bygge- og anleggsledelse. I tillegg tilbyr vi også teknisk byggeledelse innenfor elektro og VVS-fag. SHA Byggherreforskriften stiller krav til at alle byggeprosjekt av en viss størrelse skal ha en oppfølging i forhold til sikkerhet, helse og arbeidsmiljø. Som uavhengig rådgiver kan flere av våre medarbeidere bistå alle byggherrer med å ivareta de forpliktelser byggherreforskriften krever. Ansvarlig søk Det skal være et firma som står som ansvarlig søker for de aller fleste bygge og anleggsprosjekt i Norge. Med sentral godkjenning i tiltaksklasse 3 kan våre ansatte bistå byggherre / entreprenør med alle typer byggesøknader uavhengig av størrelse og kompleksitet. Prosessledelse Som uavhengig rådgiver kan våre kompetente medarbeidere bistå med å utvikle eiendom igjennom gode planprosesser ved å hente gode ressurser fra ulike fagmiljø. Agderbygg Eiendom Ulike roller Sørlandsparken ØST AS Infrastruktur anlegg og tomteopparbeidelser Elkem Northern Recharge Kontrakt og anskaffelser Entra ASA Kontorbygg Spørsmål og henvendelser Finn riktig kontaktperson TA KONTAKT bli med på laget Karriere som prosjektleder? Karriere som prosjekteringsleder? Karriere som byggeleder? Karriere som anleggsleder? Vi søker stadig flere engasjerte og dyktige medarbeidere. Kanskje er det nettopp deg? LES MER HER Tjenester Om oss Prosjekter Karriere Kontakt Kontor Kristiansand Gyldenløves gate 2, 4611 Kristiansand Kontor Mandal Kastellgata 34, 4514 Mandal Postadresse Postboks 216, 4503 Mandal Les om vår bruk av Cookies Utviklet av Warp Media 2026 © Magna Prosjekt Sør Vi bruker cookies (informasjonskapsler) for at nettsiden skal fungere som planlagt og for å analysere og forstå våre brukere. Det hjelper oss å optimalisere nettsiden. Les om vår bruk av cookies Innstillinger Godta"
  ]
}
```
## 20261113 / 818330952 / B2 EIENDOMSUTVIKLING AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://vikengartneri.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: vikengartneri.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: b2eiendomsutvikling.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: b2-eiendomsutvikling.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: b2eiendomsutvikling.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: b2-eiendomsutvikling.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://vikengartneri.no/; recorded rule: `None`; level: not saved.

Page: https://vikengartneri.no/ — title: Krydderurter og salater, naturlig dyrket uten sprøytemidler

SHA-256: `2e6d10ec6e5b4a1c5b9c8641db4a625f7ab728ad279e6778e319207c8df87e4c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://vikengartneri.no/kontakt/ — title: Kontakt oss | Viken Gartneri Frosta

SHA-256: `f4e4c5ba4e9e59132d141a62b205ab19e8a07341b72e7b330205dba37a8e496c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://vikengartneri.no/om-oss/ — title: Om oss | Viken Gartneri Frosta

SHA-256: `34b5acb398d47b0d8abd5a14b960a41336f6b2401db2f68ed829fb3d808b0483`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://vikengartneri.no/personvern/ — title: Personvernerklæring | Viken Gartneri Frosta

SHA-256: `a334bba4d650ae81ae71c03cb125b65ddfb592714572507f8dea52c1adbf1a5c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 913244702 / SAMEIESERVICE AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://sameieservice.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: sameieservice.no; recorded rule: `corroboration`; level: LOW.
- Candidate: sameieservice.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://sameieservice.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.sameieservice.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://sameieservice.no/; recorded rule: `None`; level: not saved.

Page: http://sameieservice.no/ — title: sameieservice.no is parked

SHA-256: `62459608b2b2e6a5f81d8a1fbd95cb4ebb80d9609089139dab116f1843bdfd80`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://sameieservice.no/kontakt — title: sameieservice.no is parked

SHA-256: `2782c3ab1060733c379ca41902aa5fd075c239b35c3ef1ee1b8e65f2138e0e94`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://sameieservice.no/om-oss — title: sameieservice.no is parked

SHA-256: `b14fb2d24b885c6f34c14f683f3c4ecbe62305f67a21bf8c956bd250a5e5227e`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://sameieservice.no/personvern — title: sameieservice.no is parked

SHA-256: `3b5b1a4d8bbd3148253c5044c272ec126bb8903da2de50192bb6d58e0aa09c08`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 914324769 / IDEA GROUP AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: ideagroup.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: idea-group.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.ideagroup.com/contact-us; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ideagroup.com; recorded rule: `corroboration`; level: LOW.
- Candidate: idea-group.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: idea-group.com; recorded rule: `robots_unavailable`; level: BLOCKED.
- Candidate: https://ideagroup.com/; recorded rule: `None`; level: not saved.
- Candidate: https://idea-group.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://idea-group.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.idea-group.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://idea-group.com/; recorded rule: `robots_unavailable`; level: not saved.

Page: https://www.ideagroup.com/ — title: IDEA Engineering Services | product design

SHA-256: `9f5f167461a713bd09dd98aa4fe85d2e13efe48daf65cb8181217dd6d4f984b9`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.ideagroup.com/contact-us-1 — title: IDEA Engineering Services - Southfield, MI

SHA-256: `a02bb018c99890335d32f5e87506b6caa40cfd53cc2f7a7ba329582fbe6a1a6e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.ideagroup.com/aboutus — title: IDEA Engineering Services

SHA-256: `f3fba99f3c248e21e1066f4eb717c52911c4cbfe2962d8f19570a8590b92b1de`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 926364715 / GODE RETAIL AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: goderetail.no; recorded rule: `corroboration`; level: LOW.
- Candidate: gode-retail.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: goderetail.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gode-retail.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: st1sogndal.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: st1sogndal.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: st1-sogndal.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: st1-sogndal.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://goderetail.no/; recorded rule: `None`; level: not saved.

Page: https://goderetail.no/ — title: Hosted By One.com | Webhosting made simple

SHA-256: `c33fcc4b8a202e637fa79652e2086de8a50239bdedb920e286ce63c489382deb`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://goderetail.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://goderetail.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://goderetail.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://goderetail.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://goderetail.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 830009612 / VEKSTPARTNER AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.vekstpartner.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: vekstpartner.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: vekstpartner.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: vekstpartner.com; recorded rule: `http_404`; level: LOW.
- Candidate: https://vekstpartner.no/; recorded rule: `None`; level: not saved.
- Candidate: https://vekstpartner.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://vekstpartner.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.vekstpartner.com/; recorded rule: `None`; level: not saved.
- Candidate: https://www.vekstpartner.com/; recorded rule: `http_404`; level: not saved.

Page: https://vekstpartner.no/ — title: 301 Moved Permanently

SHA-256: `87a9323ac85ce28867d5d7ce590c8f29b8d1a999961fca71bb33adef48683691`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.vekstpartner.no/ — title: Vekstpartner – fra idé til investorklar | Bryne og Tau

SHA-256: `aeb4dbc38c09221334397f96ca986299cd542d69abe5d53c555a7a3c42c4c471`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Kontakt Historier Nettverk Vekstpartner Ryfylke Vekstpartner Jæren Kontakt oss Fra idé til investorklar Vi bygger selskap – sammen med deg! Om oss Kontakt Blogg Fra idé til investorklar Les historiene til gründerne vi jobber med – og hva de har lært underveis Se artikler Ryfylke May 13, 2026 Vil bygge verdens beste jaktopplevelse – historien om Jegerhub Les mer Jæren February 24, 2026 MASE Home - historien om Susanne Sekkesæter Les mer Jæren November 25, 2025 Vind i seilene - historien om Sine Delta Les mer Ryfylke November 25, 2025 Innovasjon på tvers av regioner – historien om Ryfylkeprosjektet og RyhubX Les mer Jæren November 25, 2025 På lag med både kunstig og menneskelig intelligens – historien om The Next Level Les mer Rogaland November 25, 2025 Hjelp til hjelperne – historien om Kakadu Les mer Se alle Hos Vekstpartner møter du et team som går inn i tidligfaseselskaper med kompetanse, engasjement og gjennomføringsevne. Enten du står i startgropen med en idé, eller skal løfte selskapet til neste nivå, hjelper vi deg med å bygge struktur, finne riktige partnere og gjøre deg investorklar. Kontakt Mer om nettverk Cofounderrollen Som cofounder bidrar vi operativt i utviklingen av nye selskaper – fra tidlig markedsavklaring, forretnings- og teknologiutvikling til kapitalinnhenting og vekst. Sammen deler vi risikoen, innsatsen og suksessen. Kompetanse når du trenger det Cofounder-modellen passer ikke for alle – noen ønsker kun rådgivning eller sparring. Derfor tilbyr vi også konsulentbistand innen: - Forretningsutvikling - Strategi, investorforberedelse og kapitalinnhenting Nettverk som åpner dører Vi har et nettverk av flinke folk som vi kobler på ved behov. Ofte vil spisskompetanse fra eksperter tilføre en verdi som kan vise seg å være uvurderlig mange år etter oppstartsprosessen. ‍ Lyst på en prat? Kontakt oss Kontakt Våre lokasjoner Vi er tilgjengelig for selskap i hele landet, men har fysiske kontorer på Bryne på Jæren og Tau i Ryfylke Jæren Se kart Ryfylke Se kart Verktøykasse for tidligfaseselskaper Test dem gjerne KTH Innovation Readiness Level™ Med dette verktøyet får du et øyeblikksbilde av selskapets modenhet og et godt grunnlag for planlegging av videre utvikling. ‍ * Dette verktøyet er utviklet av KTH Innovation. Få oversikt Test din verdsettelse Her kan du raskt få en estimert verdi av ditt tidlige oppstartsselskap. * Dette analyseverktøyet er skapt av Keystones. Test verdsettelsen Pre- og post-money verdsettelse Verktøyet gir deg fort innsikt i dine investeringsdetaljer, inkludert eierskap, verdivurdering før og etter kapitalinnhenting. Prøv verktøyet Kapitalutvikling Beregner utvikling i gründerteamets eierandeler og utvikling i selskapsverdi etter en eller flere investorrunder. Se mulighetene Kontakt post@vekstpartner.no Kontakt Jæren Ryfylke Verktøy Nettverk Alle artikler © Vekstpartner AS. Alle rettigheter reservert. Personvern"
  ]
}
```

Page: https://www.vekstpartner.no/kontakt-oss — title: Kontakt Vekstpartner – møt oss på Bryne, Tau eller Teams

SHA-256: `576d8e7c5d52a53e89c8b56e9fe352abb6c91d06bd18d7bb2957550ce2224920`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.vekstpartner.no/personvern — title: Personvern | Vekstpartner

SHA-256: `f69b66236c6e1472fb04512ae5d15bdde2683502b20f5ffc975b8b49cba93302`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.vekstpartner.no/kontakt — title: Siden finnes ikke | Vekstpartner

SHA-256: `4bed4dde8876171ca2733417ef860222a0d9400400a085d5da18330736e1aa92`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.vekstpartner.com/ — title: Domain not connected

SHA-256: `ca80206796ca93b9e186300d949b6aa28c3cf6c5b19baee178878b0e5e763f93`; candidate rules: http_404, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 926073737 / ANATAS AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: anatas.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://anatas.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: anatas.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://anatas.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.anatas.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://anatas.com/; recorded rule: `None`; level: not saved.

Page: http://anatas.com/ — title: 

SHA-256: `9278d16ed2fdcd5dc651615b0b8adc6b55fb667a9d106a9891b861d4561d9a24`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://anatas.com/kontakt — title: 404 Not Found

SHA-256: `05794727f000aa88b2216faccc8ec8e5bea6339d882c177963ea0b3e952e6497`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://anatas.com/om-oss — title: 404 Not Found

SHA-256: `c89f74b5f036b73bc6850239d756cd7fdcb85dd5d1c5ef438f2e9993187c56a2`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://anatas.com/personvern — title: 404 Not Found

SHA-256: `d33eaa66f96c4dcfb9fe75efff46278fa5b92c6d141c00a57b0c94aeed1ff7d4`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 988060933 / KV IKT AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://www.kvikt.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kvikt.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: kv-ikt.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kv-ikt.no; recorded rule: `url_refused`; level: LOW.
- Candidate: kv-ikt.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kvikt.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://kvikt.no/; recorded rule: `None`; level: not saved.
- Candidate: https://kv-ikt.no/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://kv-ikt.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://kvikt.com/; recorded rule: `url_refused`; level: not saved.

Page: https://kvikt.no/ — title: 301 Moved Permanently

SHA-256: `87a9323ac85ce28867d5d7ce590c8f29b8d1a999961fca71bb33adef48683691`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://www.kvikt.no/ — title: 301 Moved Permanently

SHA-256: `c34e3a7ca27f39dc680bdd3b396bb4ea9b68bf13bf546472f32e9ed710c2ed9a`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kvikt.no/ — title: KV IKT AS is under construction

SHA-256: `2ecac348f0c7ed05bcde9e211ad8fa8adaaaea82dff2edc393a841100f58c19e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title"
  ],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 989704516 / GYSTADMYR UTBYGGING AS

Categories: veto; terminal website state: not_available.

- Candidate: kamperhaug.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: gystadmyrutbygging.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gystadmyr-utbygging.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gystadmyrutbygging.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gystadmyr-utbygging.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://kamperhaug.no/; recorded rule: `None`; level: not saved.

Page: https://kamperhaug.no/ — title: Hjem | Kamperhaug

SHA-256: `43a71aec7a85cfce1d795b4d84b4f7c0aa9031737f0bda3d785ba5ee4b5e6e65`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "898130282"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 926317490 / OSINGEN GASTROPUB AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://osingengastropub.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: osingengastropub.no; recorded rule: `corroboration`; level: LOW.
- Candidate: osingen-gastropub.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: osingengastropub.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: osingen-gastropub.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://osingengastropub.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.osingengastropub.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://osingengastropub.no/; recorded rule: `None`; level: not saved.

Page: http://osingengastropub.no/ — title: osingengastropub.no is parked

SHA-256: `429b68c970562194e62c1d30205f9f190055ef7dd6f8df1a54dddb637f6b691b`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://osingengastropub.no/kontakt — title: osingengastropub.no is parked

SHA-256: `9d9095ca661f4b17322524678880e227a19d91fcd512ba6de0d670c8be37d3b1`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://osingengastropub.no/om-oss — title: osingengastropub.no is parked

SHA-256: `948bbc391ee5b83628a93b94a33161f88fe141ec133eba97cb13b23af92f837e`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://osingengastropub.no/personvern — title: osingengastropub.no is parked

SHA-256: `10eafafb22f6552249ba2fc5eafc933c6888f55f8e50d207dc96dca1507f3a5e`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 935294746 / ALOHA HOME AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: alohahome.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: aloha-home.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: alohahome.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://aloha-home.com/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: aloha-home.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://alohahome.com/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://aloha-home.com/; recorded rule: `None`; level: not saved.

Page: https://aloha-home.com/ — title: 名古屋の女性専用グループホーム ALOHA（アロハ）　障害者共同生活援助グループホーム

SHA-256: `e549e7d879e3592f7ed6a4f29c77c977a6c59be5d932c240042cc7868ede1837`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://aloha-home.com/contact/ — title: お問い合わせ｜名古屋の女性専用グループホーム ALOHA（アロハ）　障害者共同生活援助グループホーム

SHA-256: `fed5622438c8179d8bc800edb78addba5e3d3821875d85568580c63cae521d8c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://aloha-home.com/kontakt — title: 名古屋の女性専用グループホーム ALOHA（アロハ）　障害者共同生活援助グループホーム

SHA-256: `239eeab6f943010c1dfb3b49ffaa431b6bbabd407e651a76aaeda6acad3dc7b2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://aloha-home.com/om-oss — title: 名古屋の女性専用グループホーム ALOHA（アロハ）　障害者共同生活援助グループホーム

SHA-256: `239eeab6f943010c1dfb3b49ffaa431b6bbabd407e651a76aaeda6acad3dc7b2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 924004843 / STRØMSNES AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.stroemsnes.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: stroemsnes.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: stromsnes.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: stromsnes.no; recorded rule: `url_refused`; level: LOW.
- Candidate: xn--strmsnes-74a.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://stroemsnes.no/; recorded rule: `None`; level: not saved.
- Candidate: https://stromsnes.no/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://stromsnes.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.stromsnes.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://stromsnes.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://xn--strmsnes-74a.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.xn--strmsnes-74a.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://xn--strmsnes-74a.no/; recorded rule: `website_budget_exhausted`; level: not saved.

Page: https://stroemsnes.no/ — title: 301 Moved Permanently

SHA-256: `eb3e665bf77bf41000641c3d78962440f4b88a04ae74f6f011a9c5c52be930c6`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.stroemsnes.no/ — title: 
		stroemsnes.no
	

SHA-256: `d46e5f171a4a5d4e17d52290d00805b5667fbfc1d792052f4a23693f0dbf2198`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.stroemsnes.no/kontakt — title: 404 Not Found

SHA-256: `771c2a9a2e879b99a2359d0fa56cc93f119ab118bf6a20f90e1b41751303dcd4`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.stroemsnes.no/om-oss — title: 404 Not Found

SHA-256: `007474a4843ac890246a8d59243c6a1c9ce2e9991758b1918d0eadeedb2f1877`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.stroemsnes.no/personvern — title: 404 Not Found

SHA-256: `8a3206e218ce3f016943fbe1e1defc6ec4f91ba9ef9a3d52c863fd3ced341404`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 934626176 / ADVOKATFIRMAET TASHAKORI AS

Categories: ambiguous; terminal website state: ambiguous.

- Candidate: https://tashakori.no/nb/vilkar; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: tashakori.no; recorded rule: `registry_contact_missing`; level: MEDIUM.
- Candidate: advokatfirmaettashakori.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: advokatfirmaet-tashakori.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: advokatfirmaettashakori.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: advokatfirmaet-tashakori.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.tashakori.no/; recorded rule: `None`; level: not saved.

Page: https://www.tashakori.no/ — title: 

SHA-256: `a723620c4637b7a259285deb986e97ff6ce1fb10f08949550b7d0987af405d30`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://tashakori.no/ — title: 

SHA-256: `9e26450008369fb00919ac1e8b82ba4c876177b29944d017dc800d51fed43ffc`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://tashakori.no/nb — title: Forside | Advokatfirmaet Tashakori

SHA-256: `6e249158873fd837e088f6a83afdcc84d6f3baba0972384a500b098426c71375`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Advokatfirmaet",
    "Advokatfirmaet",
    "Advokatfirmaet"
  ],
  "agency_credit_lines": []
}
```

Page: https://tashakori.no/nb/kontakt — title: Advokatfirmaet Tashakori

SHA-256: `9967bd8c561c91cd21565603d1edd06b2c36528ce7d36d325e899db268c1d3f9`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Advokatfirmaet",
    "Advokatfirmaet",
    "advokathjelp",
    "advokat",
    "advokat",
    "Advokatfirmaet",
    "Advokatfirmaet"
  ],
  "agency_credit_lines": []
}
```

Page: https://tashakori.no/nb/vare-tjenester/strafferett — title: 

SHA-256: `75c64da38dd1c01a13970b2be49bb6addbac57cd65c80dbc418d1d63535813a8`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Advokatfirmaet",
    "Advokatfirmaet",
    "Advokatfirmaet"
  ],
  "agency_credit_lines": []
}
```

Page: https://tashakori.no/nb/om-oss — title: Om oss | Advokatfirmaet Tashakori

SHA-256: `72060e6824d8bcc249e0f6f9be4422e365ab458f15ae0c45fdc399406df03d21`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Advokatfirmaet",
    "Advokatfirmaet",
    "Advokatfirmaet",
    "advokatpraksis",
    "Advokatfirmaet",
    "advokathjelp",
    "advokat",
    "advokat",
    "Advokatfirmaet",
    "Advokatfirmaet"
  ],
  "agency_credit_lines": []
}
```
## 20261113 / 927550563 / ZILLA CAPITAL AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: zillacapital.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: zilla-capital.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.zillacapital.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: zillacapital.com; recorded rule: `corroboration`; level: LOW.
- Candidate: zilla-capital.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://zillacapital.com/; recorded rule: `None`; level: not saved.

Page: https://www.zillacapital.com/ — title: 

SHA-256: `b2fbad2d479f15ac05c381cc43ee3b82b5b430df98a465d3cb934284d766d29c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.zillacapital.com/contact-us/ — title: 

SHA-256: `c18fda52ef35a4e5ac9ad6323dfb844d1046c1f5c27ac09680e6afc8b3a5ea8f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.zillacapital.com/about-zilla-capital/ — title: 

SHA-256: `c6832c7cf3ddfed9768eae7ed9ebbe2566d406537a8fa325ee98a5cd9586fef4`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.zillacapital.com/privacy-policy/ — title: 

SHA-256: `c058bc0bcae0c9b08c10f4c70da794c872e8023b0053abd4d8e2041dc6044444`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.zillacapital.com/kontakt — title: 

SHA-256: `1104d32167887b360020011c0d8f827586b9d320502c5fe51231a88fe697dc70`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 993821403 / NEXTHOP AS

Categories: ambiguous, fetched-without-proof, veto; terminal website state: ambiguous.

- Candidate: nexthop.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: nexthop.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: zetta.io; recorded rule: `partner_directory_mention`; level: REJECT.
- Candidate: nexthop.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://nexthop.no/; recorded rule: `None`; level: not saved.
- Candidate: https://nexthop.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://www.zetta.io/; recorded rule: `None`; level: not saved.
- Candidate: https://nexthop.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.nexthop.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://nexthop.com/; recorded rule: `website_budget_exhausted`; level: not saved.

Page: https://nexthop.no/ — title: Nexthop AS

SHA-256: `e0ce4c16ca058d2af8429690fb34b014c99826f589eda7acb14cf571a6e7f1a4`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "footer",
    "imprint-kontakt",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://nexthop.no/kontakt — title: 404 Not Found

SHA-256: `e38e0cee2c2996a92b17cd2a648120c322ea4d33d62adb2823b0a1f9ffe21ab2`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://nexthop.no/om-oss — title: 404 Not Found

SHA-256: `e38e0cee2c2996a92b17cd2a648120c322ea4d33d62adb2823b0a1f9ffe21ab2`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://nexthop.no/personvern — title: 404 Not Found

SHA-256: `e38e0cee2c2996a92b17cd2a648120c322ea4d33d62adb2823b0a1f9ffe21ab2`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://nexthop.no/personvernerklaering — title: 404 Not Found

SHA-256: `e38e0cee2c2996a92b17cd2a648120c322ea4d33d62adb2823b0a1f9ffe21ab2`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://nexthop.no/kontakt-oss — title: 404 Not Found

SHA-256: `e38e0cee2c2996a92b17cd2a648120c322ea4d33d62adb2823b0a1f9ffe21ab2`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.zetta.io/ — title: Zetta.IO - Home

SHA-256: `8211afcbd6abf9a5ac9d809c244d3a8a6489c1bd90c5e4992a927536315aa31d`; candidate rules: partner_directory_mention

```json
{
  "full_legal_name_locations": [
    "body",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.zetta.io/about/contact/ — title: Zetta.IO - Contact Us

SHA-256: `7f00083d9e9d903e72b220b378b9a194e579862b713871cd4322e79a8085b969`; candidate rules: partner_directory_mention

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 925293180 / ONZONZ AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://onzonz.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: onzonz.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: onzonz.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: onzonz.com; recorded rule: `website_timeout`; level: LOW.
- Candidate: https://onzonz.no/; recorded rule: `None`; level: not saved.
- Candidate: https://onzonz.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://onzonz.com/; recorded rule: `website_timeout`; level: not saved.

Page: https://onzonz.no/ — title: ONZONZ - Film & post production

SHA-256: `01d55610d9a88c07340018517ecb409c3f8229e16315b6bd466dcf05d8db93f5`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://onzonz.no/kontakt — title: Page not found

SHA-256: `c07b1d64415ec68628bc208f9acd3118e0554635947ae484244053e20272f404`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://onzonz.no/om-oss — title: Page not found

SHA-256: `c07b1d64415ec68628bc208f9acd3118e0554635947ae484244053e20272f404`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://onzonz.no/personvern — title: Page not found

SHA-256: `c07b1d64415ec68628bc208f9acd3118e0554635947ae484244053e20272f404`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://onzonz.no/personvernerklaering — title: Page not found

SHA-256: `c07b1d64415ec68628bc208f9acd3118e0554635947ae484244053e20272f404`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://onzonz.no/kontakt-oss — title: Page not found

SHA-256: `c07b1d64415ec68628bc208f9acd3118e0554635947ae484244053e20272f404`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 928745813 / MDM CONSULTANCY AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: mdmconsultancy.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: mdm-consultancy.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: mdmconsultancy.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: mdm-consultancy.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://mdmconsultancy.com/; recorded rule: `None`; level: not saved.

Page: https://mdmconsultancy.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mdmconsultancy.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mdmconsultancy.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mdmconsultancy.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mdmconsultancy.com/personvernerklaering — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mdmconsultancy.com/kontakt-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mdmconsultancy.com/om — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 996904490 / SOLLERUD BÅTBYGGERI & SLIPP AS

Categories: ambiguous; terminal website state: ambiguous.


Page: https://www.sollerud.com/ — title: Sollerud Båtbyggeri & Slipp

SHA-256: `685964099d3535e62f04030773bdcfde600bd8519a3006b8236f8680922d50b4`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sollerud.com/kontakt — title: Sollerud Båtbyggeri & Slipp

SHA-256: `5374d0cf0ef91c2d40df84096f069f675c2b0f35be00b6f553c6b3f2a91d53af`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sollerud.com/om-oss — title: Sollerud Båtbyggeri & Slipp

SHA-256: `01de6b1c181d5de48bf5999cc242518a1a1e6d84ecf9c8b1448fbf364c151ceb`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sollerud.com/personvern — title: Sollerud Båtbyggeri & Slipp

SHA-256: `01de6b1c181d5de48bf5999cc242518a1a1e6d84ecf9c8b1448fbf364c151ceb`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sollerud.com/personvernerklaering — title: Sollerud Båtbyggeri & Slipp

SHA-256: `01de6b1c181d5de48bf5999cc242518a1a1e6d84ecf9c8b1448fbf364c151ceb`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sollerud.com/kontakt-oss — title: Sollerud Båtbyggeri & Slipp

SHA-256: `01de6b1c181d5de48bf5999cc242518a1a1e6d84ecf9c8b1448fbf364c151ceb`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 930532223 / SAMEIET SJØKANTEN PARK

Categories: veto; terminal website state: not_available.

- Candidate: agioforvaltning.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: sameietsjoekantenpark.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameiet-sjoekanten-park.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameietsjoekantenpark.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameiet-sjoekanten-park.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameietsjokantenpark.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameietsjokantenpark.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameiet-sjokanten-park.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--sameiet-sjkanten-park-zfc.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--sameietsjkantenpark-37b.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameiet-sjokanten-park.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--sameiet-sjkanten-park-zfc.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--sameietsjkantenpark-37b.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.agioforvaltning.no/; recorded rule: `None`; level: not saved.

Page: https://agioforvaltning.no/ — title: Forretningsfører for sameie og borettslag | Bytt enkelt og trygt

SHA-256: `abf54a5b238bcd8539316f5d09d46ba9b6213f8be0a1b3c3ccb56d17507f4d2f`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "995366517"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskap",
    "regnskapsføring",
    "Regnskapsrapporter",
    "regnskap",
    "regnskap",
    "regnskap",
    "regnskap",
    "Regnskap",
    "regnskapsføring",
    "Regnskapsrapporter",
    "regnskap",
    "regnskap",
    "regnskap",
    "regnskap"
  ],
  "agency_credit_lines": []
}
```
## 20261113 / 936106374 / KO&CO AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: koco.no; recorded rule: `robots`; level: BLOCKED.
- Candidate: ko-co.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.koco.com/contact; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: koco.com; recorded rule: `corroboration`; level: LOW.
- Candidate: ko-co.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://ko-co.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ko-co.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://koco.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.koco.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://koco.no/; recorded rule: `robots`; level: not saved.
- Candidate: https://koco.com/; recorded rule: `None`; level: not saved.
- Candidate: https://ko-co.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://ko-co.com/; recorded rule: `None`; level: not saved.

Page: https://www.koco.com/ — title: Oklahoma City News, Weather and Sports - KOCO 5 News

SHA-256: `d3c12816a7701fcf5dea8abe25452c9fc7860d643b42e0e40c6af504a8b4f833`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.koco.com/article/contact-us/3616874 — title: Contact Us  - KOCO

SHA-256: `d6b3a7af97543e432d8eb800ff7e8d440aa9b7cb48642a82c5942f4643d4c808`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ko-co.com/ — title: KO&CO | ARCHITECTURAL COMPLEMENTS – rvs weefsels – maille inox – metal fabrics

SHA-256: `421a0065b52094c1593f3d51d16f5a59bbea6e0c8f3613b24094d2973438b346`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ko-co.com/contact/ — title: Contact – KO&CO | ARCHITECTURAL COMPLEMENTS

SHA-256: `350472be77bf72bca0ae046de0d10a600f736d684136f1004a2f17c21e23d707`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ko-co.com/privacy/ — title: Privacy – KO&CO | ARCHITECTURAL COMPLEMENTS

SHA-256: `d49beb86f218607b0f5c4644522dc5003eb09aeb66f4cdbb04ac880d0bd9144f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ko-co.com/kontakt — title: Pagina niet gevonden – KO&CO | ARCHITECTURAL COMPLEMENTS

SHA-256: `fb520f74cd7e9dd1af513fd41d9032438cb76a8119b098d2039bd065dcc18d5f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 933741761 / HØYÅSEN AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: hoeyaasen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://hoyasen.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: hoyasen.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: hoeyaasen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: hoyasen.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: hoeyasen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: hoyaasen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://xn--hysen-nra5k.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: xn--hysen-nra5k.no; recorded rule: `corroboration`; level: LOW.
- Candidate: https://hoyasen.no/; recorded rule: `None`; level: not saved.
- Candidate: https://hoyasen.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://xn--hysen-nra5k.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.xn--hysen-nra5k.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://xn--hysen-nra5k.no/; recorded rule: `None`; level: not saved.

Page: https://hoyasen.no/ — title: Index of /

SHA-256: `195661223f9f553405b1bf4478def7eefc3548e575b73b17cf02a77ec9426aac`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hoyasen.no/kontakt — title:  404 Not Found


SHA-256: `4c13d452dd5d49671bd93ca32f2b4f85c78e39b6ab0ad1f38d98ed267f8fd896`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hoyasen.no/om-oss — title:  404 Not Found


SHA-256: `4c13d452dd5d49671bd93ca32f2b4f85c78e39b6ab0ad1f38d98ed267f8fd896`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hoyasen.no/personvern — title:  404 Not Found


SHA-256: `4c13d452dd5d49671bd93ca32f2b4f85c78e39b6ab0ad1f38d98ed267f8fd896`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hoyasen.no/personvernerklaering — title:  404 Not Found


SHA-256: `4c13d452dd5d49671bd93ca32f2b4f85c78e39b6ab0ad1f38d98ed267f8fd896`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hoyasen.no/kontakt-oss — title:  404 Not Found


SHA-256: `4c13d452dd5d49671bd93ca32f2b4f85c78e39b6ab0ad1f38d98ed267f8fd896`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://xn--hysen-nra5k.no/ — title: høyåsen.no

SHA-256: `893a16c648938786aa4fe923574b8bc5f1933e234ae34eb8f4d44879041093f5`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://xn--hysen-nra5k.no/kontakt — title: 404 Not Found

SHA-256: `c1d597f566a3359b4d47b768b54fffb131890911631361f6d6bae2932eac2162`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 995744562 / GRORUD ELEKTRO SERVICE AS

Categories: veto; terminal website state: not_available.

- Candidate: ghs.no; recorded rule: `group_without_exact_orgnr`; level: REJECT.
- Candidate: grorudelektroservice.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: grorud-elektro-service.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: grorudelektroservice.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: grorud-elektro-service.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://ghs.no/; recorded rule: `None`; level: not saved.

Page: https://www.ghs.no/ — title: Håndverker i Oslo & Groruddalen | Grorud-Gruppen

SHA-256: `57c34c7a31af437ad38f73fdaa3b095ae56c1831667ab163b1229207685399c2`; candidate rules: group_without_exact_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hopp rett til innholdet Hjem Tjenester Tømrer Elektriker Rørlegger Maler Prosjekter Prosjekter Tømrer Prosjekter Elektriker Prosjekter Rørlegger Prosjekter Maler Leverandører Om Kontakt Jobb i Grorud-Gruppen Nyheter Nyheter Hjem Tjenester Tømrer Elektriker Rørlegger Maler Prosjekter Prosjekter Tømrer Prosjekter Elektriker Prosjekter Rørlegger Prosjekter Maler Leverandører Om Kontakt Jobb i Grorud-Gruppen 30 år med kvalitet Oppussing. Rehabilitering. Vedlikehold. Grorud-Gruppen er plassert sentralt på Grorud og leverer tømrer, elektro, Rørlegger og maler-tjenester i Oslo og omegn. Vi er i tillegg spesialister på baderom. Enkelt for deg, du forholder deg til én aktør som tar ansvar for fremdrift, kvalitet og oppfølging - støttet av over 30 års erfaring Jobb i Grorud-Gruppen Gratis befaring Service i alle ledd Tømrer, elektro, rør og maler jobber tett sammen i hvert prosjekt, slik at arbeidet er samordnet og prosjekter gjennomføres effektivt 30+ års erfaring Lang erfaring fra både privat- og bedriftsmarkedet gir trygg rådgivning og solide løsninger – i små oppdrag og større prosjekter. Én ansvarlig leverandør Du har én tydelig aktør å forholde deg til, med ansvar for planlegging, gjennomføring og kvalitet hele veien. Nyhetsbrev november Les nyhetsbrev Grorud-Gruppen Totalleverandør av håndverkstjenester Grorud-Gruppen leverer håndverks-tjenester for privatkunder, bedrifter, borettslag og sameier i Oslo og omegn. Med egne fagmiljøer og tydelig ansvar sørger vi for at jobben blir gjort skikkelig – og fulgt opp hele veien. Tømrer, elektro, rør og maler under samme tak Fast kontaktpunkt gjennom prosjektet Kjent for ryddighet, kvalitet og tillit Service i alle ledd Våre Tjenester Tømrer Tømrere som leverer trygge løsninger med ryddig arbeid, tydelig fremdrift og kvalitet i alle ledd. Les mer Elektriker Elektrikere som leverer trygge løsninger med ryddig arbeid, tydelig fremdrift og kvalitet i alle ledd. Les mer Rørlegger Rørleggere som leverer trygge løsninger med ryddig arbeid, tydelig fremdrift og kvalitet i alle ledd. Les mer Maler Malere som leverer trygge løsninger med ryddig arbeid, tydelig fremdrift og kvalitet i alle ledd. les mer Våre prosjekter Skikkelig håndverk. Levert av fagfolk. Et utvalg prosjekter levert for privat- og bedriftsmarkedet – utført av våre dyktige ansatte Se flere prosjekter Vi hjelper deg å realisere ditt neste prosjekt! Uansett om prosjektet er stort eller lite, starter det med en god dialog. Vi lytter, gir faglige råd og hjelper deg videre på en ryddig og forutsigbar måte. Kontakt oss Kundeanmleldelser Dette Sier Våre Kunder Google Review Har samarbeidet med Grorud Håntverk-service AS flere ganger, over flere år i forskjellige anledninger med dører & vinduer. De er profesjonelle, og punktlige. Anbefales! Endre Knutsen Google Review Snekker, elektriker eller rørlegger. Firmaet har alle disse. Har brukt alle 3 flere ganger og er veldig fornøyd. Terje Benjamin Google Review Profesjonelle fagfolk som leverer innenfor alle håndverkertjenester. Kan anbefales på det sterkeste. Fredrik Winger-Solvang Kvalitet i alle ledd! Erfaring du kan stole på Bygget på tillit og solid gjennomføring. Grorud-Gruppen har levert håndverkstjenester i Oslo-området i over 30 år. Vi bygger langsiktige relasjoner gjennom ryddige prosesser, tydelig ansvar og leveranser som holder det vi lover – prosjekt etter prosjekt. 20+ Fagfolk i arbeid Tømrere, elektrikere, rørleggere og malere med fagbrev og erfaring. 30 År Med Fornøyde Kunder Lang erfaring fra både privat- og bedriftsmarkedet. Lokal kunnskap 30+ år i markedet har gitt oss en unik erfaring og sterk lokalkunnskap siden etableringen i 1994 Sterke partnere Vi samarbeider med etablerte merkevarer og leverandører som stiller krav til kvalitet. Flere fagrupper Flere fag samlet i én struktur, med bedre flyt, færre avklaringer og trygg fremdrift. Folk i fokus Trivelige og dyktige fagfolk som tar eierskap til jobben og følger prosjektet hele veien. Hvorfor Grorud- Gruppen Vi gjør det enkelt å velge riktig! Hos Grorud-Gruppen handler det ikke bare om å gjøre jobben, men om å gjøre den skikkelig. Med flere faggrupper samlet og én ansvarlig part å forholde seg til, blir prosessen enklere, ryddigere og mer forutsigbar for deg som kunde. KLAR FOR Å KOMME I GANG? Bestill gratis befaring til ditt neste prosjekt! Med alle fagområdene under samme tak får du en plan som henger sammen, tydelige avklaringer og en leveranse du kan stole på. Kontakt oss Om Grorud-Gruppen I Grorud-Gruppen leverer vi solide tjenester innen bygg, rehabilitering og tekniske fag. Vi kombinerer fagkompetanse med ryddige prosesser – og står for kvalitet som varer. Meny Main Menu Hjem Tjenester Tømrer Elektriker Rørlegger Maler Prosjekter Prosjekter Tømrer Prosjekter Elektriker Prosjekter Rørlegger Prosjekter Maler Leverandører Om Kontakt Jobb i Grorud-Gruppen Ressurser Main Menu Nyheter Jobb i Grorud-Gruppen Referanser Kontakt Oss Ring Oss +47 22 80 38 90 Send E-post post@ghs.no Adresse Pastor Blaauws vei 16 0962 Oslo © 2025 Copyright by Digitalverkstedet.no Main Menu Privacy Policy Vikår & Betingelser Skroll til toppen"
  ]
}
```
## 20261113 / 917664986 / ANTONS EIENDOM AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.drammenbolig.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: drammenbolig.no; recorded rule: `corroboration`; level: LOW.
- Candidate: antonseiendom.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: antons-eiendom.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: antonseiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: antons-eiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://drammenbolig.no/; recorded rule: `None`; level: not saved.

Page: https://www.drammenbolig.no/ — title: Drammen Bolig | drammenbolig

SHA-256: `d3183bb31f5ac302330b7dc5539a14301e42d84faf4193c05b455c3439155dea`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.drammenbolig.no/kontakt-oss — title: KONTAKT OSS | drammenbolig

SHA-256: `9da60b8d0d6224dff7003b25be16fe844d040bb6590d334c0e40bb103f724587`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.drammenbolig.no/kontakt — title: 404 Error: Page Not Found

SHA-256: `643b426e0089dbeef7c1bcee0d3fc7c431b0183fc3402e6b790426aa05f344c0`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 915469132 / ARCHWAY AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.archway.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: archway.no; recorded rule: `corroboration`; level: LOW.
- Candidate: archway.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: archway.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://archway.no/; recorded rule: `None`; level: not saved.
- Candidate: https://archway.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://archway.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.archway.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://archway.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://www.archway.com/; recorded rule: `website_budget_exhausted`; level: not saved.

Page: https://archway.no/ — title: 

SHA-256: `7beb454b40b5a05f33f39d9b11d2478291d700e5bd9e3a8e1552a65347c35e0d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.archway.no/ — title: Archway - AI-drevet arkitektonisk rendering

SHA-256: `62c0dfbc76aedd2e16defb3796d75458118a365574091240b24a1a23904ec7dc`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://app.archway.no/kontakt — title: 

SHA-256: `b3f44832b96b54a2bdd0f6cb3cea63d039312ddda4a9e8ee66467fbdfc8b7ec8`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.app.archway.no/kontakt — title: Kontakt oss

SHA-256: `3f2fadbbbb2e9d0cc7f753711bfb4c9516d6310f4c0af0864d1ea0895d4c2ce2`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 911818191 / VANADIUM AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://vanadium.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: vanadium.no; recorded rule: `corroboration`; level: LOW.
- Candidate: vanadium.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://vanadium.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: vanadium.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://vanadium.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.vanadium.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://vanadium.no/; recorded rule: `None`; level: not saved.
- Candidate: https://vanadium.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://vanadium.com/; recorded rule: `None`; level: not saved.

Page: http://vanadium.no/ — title: vanadium.no is parked

SHA-256: `f99c652cb32c5468a4c4a75364a65f5b097aff12f8b011c503383116c751d43d`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://vanadium.no/kontakt — title: vanadium.no is parked

SHA-256: `fbc2e0239ef0bebed14f3b698b667e8074dc6b763796ad720099447600973417`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://vanadium.no/om-oss — title: vanadium.no is parked

SHA-256: `673c2bc7014e28de907a5a5653626e007c10baa50e92539ae26353ad47f45040`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://vanadium.no/personvern — title: vanadium.no is parked

SHA-256: `a7d4cd1e69b35922b2b80696751b63549d621e590e73e6e8f7589b5084571b0c`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://vanadium.com/ — title: Vanadium Price -

SHA-256: `52cef5df8bc83735535151882fc7f9547a4a10e24fc9206a5e283de197601f24`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group",
    "Group",
    "holding",
    "Group",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://vanadium.com/about/ — title: about - Vanadium Price

SHA-256: `50f47cf89f07f64891a5c2cf02682bdc835ad9cf3133a88a3f463c94cad47976`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 934058577 / FLOVEIEN 1 AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://floveien1.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: floveien1.no; recorded rule: `corroboration`; level: LOW.
- Candidate: floveien-1.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: floveien1.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: floveien-1.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://floveien1.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.floveien1.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://floveien1.no/; recorded rule: `None`; level: not saved.

Page: http://floveien1.no/ — title: floveien1.no is parked

SHA-256: `2360bd36359cf40919c06feff54faaf4fe63880762a520914cf56926e8077227`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://floveien1.no/kontakt — title: floveien1.no is parked

SHA-256: `7ec97f2d5847cf5f20d953d3488c1bc44cf47d0cae6ef28d2e093ff6b1ab87d5`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://floveien1.no/om-oss — title: floveien1.no is parked

SHA-256: `d5d4551c5851f96b851512e77514e9de4109b53372cf98af3eba71f5ab43e9a6`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://floveien1.no/personvern — title: floveien1.no is parked

SHA-256: `665ffc3650b45bd675600b2120ae9799b3c6ff7b824b6962b15ac3a64bcdfd78`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 935656176 / HØG AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: hoeg.no; recorded rule: `website_timeout`; level: LOW.
- Candidate: xn--hg-lka.no; recorded rule: `website_timeout`; level: LOW.
- Candidate: https://hoeg.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: hoeg.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: xn--hg-lka.com; recorded rule: `dns_unavailable`; level: LOW.
- Candidate: https://hoeg.no/; recorded rule: `website_timeout`; level: not saved.
- Candidate: https://xn--hg-lka.no/; recorded rule: `website_timeout`; level: not saved.
- Candidate: https://hoeg.com/; recorded rule: `None`; level: not saved.

Page: https://hoeg.com/ — title: Hoeg

SHA-256: `e9d11779c904bb6d944485799f46e4942bb4779de08884d2d1d06162b6d9eb05`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 930090077 / AS SOLO

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: assolo.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: as-solo.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: assolo.com; recorded rule: `http_410`; level: LOW.
- Candidate: as-solo.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://solo.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: solo.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: solo.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://assolo.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.assolo.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://assolo.com/; recorded rule: `None`; level: not saved.
- Candidate: http://www.assolo.com/; recorded rule: `None`; level: not saved.
- Candidate: https://solo.no/; recorded rule: `None`; level: not saved.

Page: http://assolo.com/ — title: 410 Gone

SHA-256: `ee72a4b38447822a3a5f7a38bcfb2e3fc65f04ad397d013225280cf624cae61d`; candidate rules: http_410, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://www.assolo.com/ — title: 410 Gone

SHA-256: `ee72a4b38447822a3a5f7a38bcfb2e3fc65f04ad397d013225280cf624cae61d`; candidate rules: http_410, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://solo.no/ — title: Solo

SHA-256: `0bd2c7fdf6b4270a49821dde12543ca39b5a40f110772b8132b7b8d3445355a5`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 989221981 / COSTRA AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: dhr.no; recorded rule: `url_refused`; level: LOW.
- Candidate: costra.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://costra.com/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: costra.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://dhr.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://costra.com/; recorded rule: `None`; level: not saved.

Page: https://costra.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://costra.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://costra.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://costra.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://costra.com/personvernerklaering — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://costra.com/kontakt-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 927265222 / TRANSPOLAR AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://transpolar.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: transpolar.no; recorded rule: `corroboration`; level: LOW.
- Candidate: transpolar.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: transpolar.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://transpolar.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.transpolar.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://transpolar.no/; recorded rule: `None`; level: not saved.
- Candidate: https://transpolar.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://transpolar.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.transpolar.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://transpolar.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://www.transpolar.com/; recorded rule: `website_budget_exhausted`; level: not saved.

Page: http://transpolar.no/ — title: Hosted by one.com

SHA-256: `4fee3bfe650b625deb6da561222154f83cfa0d1f8682ce0ed055215abf1f37b1`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://transpolar.no/kontakt — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://transpolar.no/om-oss — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://transpolar.no/personvern — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 997274253 / ELEKTROFIL AS

Categories: ambiguous; terminal website state: ambiguous.

- Candidate: https://www.elektrofil.as/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: elektrofil.as; recorded rule: `registry_contact_missing`; level: MEDIUM.
- Candidate: elektrofil.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: elektrofil.no; recorded rule: `url_refused`; level: LOW.
- Candidate: elektrofil.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://www.elektrofil.as/; recorded rule: `None`; level: not saved.
- Candidate: https://elektrofil.no/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://elektrofil.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://elektrofil.com/; recorded rule: `url_refused`; level: not saved.

Page: https://www.elektrofil.as/ — title: Elektriker i Oslo og Akershus | Elektrofil AS

SHA-256: `c8f1cce55b31955d486bc67415667b23fce8a3144be58fcbd7baaf23fc0544f8`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "header/logo",
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hovedside Tjenester Elsjekk Service Installasjon Belysning Varme El-billader Referanser Om oss Bestill elektriker Personvern Elektriker i Oslo og Viken Vi tar alle elektrikeroppdrag i alt fra bolig til næringsbygg Tjenester Bestill elektriker Elektroentreprenør med bred erfaring Elektrofil AS er en elektroentreprenør sentralt i Oslo. Vi har lang erfaring i bransjen, og utfører alle typer oppdrag innen elektro for private og bedrifter. Kontakt oss gjerne for å avtale en uforpliktende befaring! Våre tjenester Elsjekk Service Installasjon Belysning Varme Brannsikkerhet Visste du at over 40 prosent av branner i norske hjem forårsakes av feil på elektriske anlegg og apparater? Eier og bruker er selv ansvarlig for at apparater og anlegg er i orden. Bestill en elsjekk i dag, så er du på den sikre siden! Vennligst godta markedsføringsinformasjonskapsler for å se dette innholdet. Accept cookies  Hvamsvingen 4 2013 Skjetten  22 09 90 00  post@elektrofil.as Utviklet av Hjemmesidehuset . Personvern"
  ]
}
```

Page: https://www.elektrofil.as/om-oss — title: Elektrikerfirma sentralt i Oslo | Elektrofil AS

SHA-256: `c1cf37c5ef7f6e8e1af2323b058b80e8973f76fdfece8a8035e18ed13e9833e8`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "header/logo",
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hovedside Tjenester Elsjekk Service Installasjon Belysning Varme El-billader Referanser Om oss Bestill elektriker Personvern Elektrikerfirma sentralt i Oslo Med kundens beste i fokus Referanser Erfarne elektrikere og moderne tjenester Elektrofil AS ble etablert i 2011. Siden den gang har vi levert utallige oppdrag for kunder i Oslo og Viken. Vi møter opp på jobb med tre viktige ting i fokus hver eneste dag: Punktlighet Vi vet at et elektrikerbesøk krever planlegging. Derfor gjør vi alltid vårt ytterste for å komme til avtalt tid. Åpenhet Vi gir deg våre beste løsninger basert på hva vi tror vil løse dine behov og være mest økonomisk gunstig for deg. Service Fornøyde kunder er vår viktigste referanse. Det er det vi lever av. Nettopp derfor er vi opptatt av å yte høy grad av service, uansett oppdrag. Våre elektrikere Thomas K. Jansen Montør/daglig leder  48014111 Andreas Sellgren Jørstad Installatør  48014112 Mohamed Aliseyd Lærling Marius Jansen Montør  92661909 Hilde Jansen Kontor Mandag og Onsdag:  90684306 Svein Jansen Styreformann Mathias Sørlie Sollund Montør  45223500  Hvamsvingen 4 2013 Skjetten  22 09 90 00  post@elektrofil.as Utviklet av Hjemmesidehuset . Personvern"
  ]
}
```

Page: https://www.elektrofil.as/personvern — title: Personvern | Elektrofil AS

SHA-256: `a7c0e23aac58b5fe33887163708c304776030af214121ac474f2a8146cff8f22`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "header/logo",
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hovedside Tjenester Elsjekk Service Installasjon Belysning Varme El-billader Referanser Om oss Bestill elektriker Personvern Personvern Våre brukeres tillit er av største viktighet for oss og derfor følger vi en strikt integritetspolicy. Den forklarer hvordan og hvorfor vi samler inn og anvender informasjonskapsler (cookies), og hvordan vi beskytter brukernes integritet. Bruk av informasjonskapsler og andre måleverktøy Vi bruker informasjonskapsler for å gjøre det lettere å bruke våre websider og kan brukes for å personalisere visse deler av innholdet. En informasjonskapsel er en liten tekstfil som sendes fra vår webserver og lagres av din nettleser. Informasjonen som lagres kan være opplysninger om hvordan våre brukere har surfet på og anvendt våre nettsider, og om hvilken nettleser de har brukt. Vi anvender statistikk om brukere og trafikk/trafikkleverandører i aggregert form. Statistikken inneholder aldri noen form for personlig informasjon, alt er anonymt. IP-adresser lagres ikke i vår database der vi lagrer atferd på nettstedet, derfor kan informasjon om deg som bruker aldri kobles sammen med din identitet. Din IP-adresse lagres av sikkerhetsmessige årsaker bare i de tilfeller du selv aktivt registrerer deg på nettstedet. Formål: - Utvikle og forbedre nettstedet gjennom å forstå hvordan det anvendes. - Beregne og rapportere brukerantall og trafikk. - Gjøre det lettere for deg å navigere på nettstedet. - Gjøre det mulig for systemet å kjenne igjen faste brukere for å kunne tilpasse tjenestene. - Iblant anvender vi tredjepartsinformasjonskapsler fra andre firma for å gjøre markedsundersøkelser og trafikkmålinger, og for å forbedre funksjonaliteten på nettstedet. Slik forhindrer du at informasjonskapsler lagres Du kan slette informasjonskapsler fra din harddisk når som helst, men dette gjør at dine personlige innstillinger forsvinner. Du kan også endre innstillingene i din nettleser slik at den ikke tillater at informasjonskapsler lagres på din harddisk. Dette gir imidlertid dårligere funksjonalitet på visse websider, kan forhindre tilgang til medlemssider og gjøre at deler av innhold og enkelte funksjoner ikke blir tilgjengelige. Hvis du ikke ønsker å bli sporet av Google Analytics kan dette deaktiveres på adressen: http://tools.google.com/dlpage/gaoptout . Mer informasjon om hvordan du kan unngå informasjonskapsler kan du lese på: www.allaboutcookies.org . Til Hovedsiden  Hvamsvingen 4 2013 Skjetten  22 09 90 00  post@elektrofil.as Utviklet av Hjemmesidehuset . Personvern"
  ]
}
```

Page: https://www.elektrofil.as/kontakt — title: 404 ikke funnet | Hjemmesidehuset

SHA-256: `59f6c353f6df2a0b1174914b98970dd661045288b4b5e3aacbb41a55f293feb5`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Å nei, her var det tomt! Trykk på knappen nedenfor for å komme tilbake til forrige side. Gå tilbake Utviklet av Hjemmesidehuset"
  ]
}
```

Page: https://www.elektrofil.as/personvernerklaering — title: 404 ikke funnet | Hjemmesidehuset

SHA-256: `59f6c353f6df2a0b1174914b98970dd661045288b4b5e3aacbb41a55f293feb5`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Å nei, her var det tomt! Trykk på knappen nedenfor for å komme tilbake til forrige side. Gå tilbake Utviklet av Hjemmesidehuset"
  ]
}
```

Page: https://www.elektrofil.as/kontakt-oss — title: 404 ikke funnet | Hjemmesidehuset

SHA-256: `59f6c353f6df2a0b1174914b98970dd661045288b4b5e3aacbb41a55f293feb5`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Å nei, her var det tomt! Trykk på knappen nedenfor for å komme tilbake til forrige side. Gå tilbake Utviklet av Hjemmesidehuset"
  ]
}
```
## 20261113 / 982039177 / ETNE INVEST AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: etneinvest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: etne-invest.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: etneinvest.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: etne-invest.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://etne-invest.no/; recorded rule: `None`; level: not saved.

Page: https://etne-invest.no/ — title: Etne Invest AS – Info om Etne Invest AS

SHA-256: `aa9d5d7ac2891977e926d13be608f6b1c108f30cccedfa5a6d3750045c1efb08`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://etne-invest.no/kontakt — title: Fant ikke siden – Etne Invest AS

SHA-256: `0837b113212dc87895279dd90da2cbff5024417761c9e9c5d26b642a57004f44`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://etne-invest.no/om-oss — title: Fant ikke siden – Etne Invest AS

SHA-256: `0837b113212dc87895279dd90da2cbff5024417761c9e9c5d26b642a57004f44`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://etne-invest.no/personvern — title: Fant ikke siden – Etne Invest AS

SHA-256: `0837b113212dc87895279dd90da2cbff5024417761c9e9c5d26b642a57004f44`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://etne-invest.no/personvernerklaering — title: Fant ikke siden – Etne Invest AS

SHA-256: `0837b113212dc87895279dd90da2cbff5024417761c9e9c5d26b642a57004f44`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://etne-invest.no/kontakt-oss — title: Fant ikke siden – Etne Invest AS

SHA-256: `0837b113212dc87895279dd90da2cbff5024417761c9e9c5d26b642a57004f44`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261113 / 994900544 / FORBERG INTERNATIONAL AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: forberg.no; recorded rule: `url_refused`; level: LOW.
- Candidate: forberginternational.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: forberg-international.no; recorded rule: `robots`; level: BLOCKED.
- Candidate: forberginternational.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://forberg-international.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: forberg-international.com; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: forbergmixertechnology.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: forbergmixertechnology.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: forberg-mixer-technology.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: forberg-mixer-technology.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://forberg.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://forberg-international.no/; recorded rule: `robots`; level: not saved.
- Candidate: https://forberg-international.com/; recorded rule: `None`; level: not saved.

Page: https://forberg-international.com/ — title: Home | Forberg

SHA-256: `a7793875818280c2849837dc6e98493905fb1235401badc4118342731a2a3ae4`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://forberg-international.com/contact-us/ — title: Contact us | Forberg

SHA-256: `c66b9ce1d173e3ba7c6fdbeeb3023d2e29d87384f85b64cb32f18ece457fc9e4`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://forberg-international.com/about-us/ — title: About us | Forberg

SHA-256: `9a8be5d5451281b3afb3d32f5b126026973fcfa34738ab8ff799efbafeeb5a35`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 892442762 / SKJESET AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: skjeset.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.skjeset.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: skjeset.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://skjeset.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.skjeset.com/; recorded rule: `None`; level: not saved.

Page: https://www.skjeset.com/ — title: Leif Skjeset

SHA-256: `3e52297cad5d6c0eb541fc6e30b5a7e1a7c836a8bfeae2d9f4e536bfcc62e008`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.skjeset.com/kontakt — title: Page not found – Leif Skjeset

SHA-256: `43181dffdba4b1c6fec7bb2d82b28a7b61f25cb03e7054f5930ec31f0e0a75ae`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.skjeset.com/om-oss — title: Page not found – Leif Skjeset

SHA-256: `43181dffdba4b1c6fec7bb2d82b28a7b61f25cb03e7054f5930ec31f0e0a75ae`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.skjeset.com/personvern — title: Page not found – Leif Skjeset

SHA-256: `43181dffdba4b1c6fec7bb2d82b28a7b61f25cb03e7054f5930ec31f0e0a75ae`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 935352398 / STUDIO LIVING AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.studioliving.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: studioliving.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: studio-living.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: studioliving.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: studio-living.com; recorded rule: `dns_unavailable`; level: LOW.
- Candidate: https://studioliving.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: studioliving.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://studioliving.no/; recorded rule: `None`; level: not saved.
- Candidate: https://studioliving.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://studioliving.com/; recorded rule: `None`; level: not saved.

Page: https://www.studioliving.no/ — title: Hjem | Studio Living

SHA-256: `851ef79379226362c21ee2d7275e6774b343366dfb1ddf6e3d9914bb0c9b3573`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.studioliving.no/kontakt — title: 404 Error: Page Not Found

SHA-256: `449f82a53b872e04f1b05d9854518bd94668ba07dafbb1e558564ccc3d14a7de`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.studioliving.no/om-oss — title: 404 Error: Page Not Found

SHA-256: `db1333aebdd5342b8fe08490ff9228ed53683f098ef05700613eaee137bf6336`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.studioliving.no/personvern — title: 404 Error: Page Not Found

SHA-256: `de7fbb95fbba4ca247b9e8ebe8e8b9f60a5b901c961128873ee81c9265ac40e7`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://studioliving.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://studioliving.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://studioliving.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://studioliving.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 935033381 / PETNOURISH AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://petnourish.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: petnourish.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: petnourish.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: petnourish.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://petnourish.no/; recorded rule: `None`; level: not saved.
- Candidate: https://petnourish.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://petnourish.com/; recorded rule: `url_refused`; level: not saved.

Page: https://petnourish.no/ — title: www.petnourish.no

SHA-256: `60f78c74b9421d11a2ed72abbb91a38b9371d7d8d73f9cbc1c778e54824f438c`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://petnourish.no/kontakt — title: 404 Not Found

SHA-256: `835796df023e6834e53dc5536e468624855af857fb53f3c047ddef96bd0c4d72`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://petnourish.no/om-oss — title: 404 Not Found

SHA-256: `835796df023e6834e53dc5536e468624855af857fb53f3c047ddef96bd0c4d72`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://petnourish.no/personvern — title: 404 Not Found

SHA-256: `835796df023e6834e53dc5536e468624855af857fb53f3c047ddef96bd0c4d72`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://petnourish.no/personvernerklaering — title: 404 Not Found

SHA-256: `835796df023e6834e53dc5536e468624855af857fb53f3c047ddef96bd0c4d72`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://petnourish.no/kontakt-oss — title: 404 Not Found

SHA-256: `835796df023e6834e53dc5536e468624855af857fb53f3c047ddef96bd0c4d72`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://petnourish.com/ — title: 301 Moved Permanently

SHA-256: `446a6087825fa73eadb045e5a2e9e2adf7df241b571228187728191d961dda1f`; candidate rules: url_refused, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 932522209 / YNGVE HOLEN AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://yngveholen.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: yngveholen.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: yngve-holen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: yngveholen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: yngve-holen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://yngveholen.no/; recorded rule: `None`; level: not saved.

Page: https://yngveholen.no/ — title: This domain is hosted by UnoEuro Webhosting

SHA-256: `95959f90a4bb0255b317f2364b63ea6edbde3868fbfbe3471f0bd37f72aca133`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://yngveholen.no/kontakt — title: 404 Not Found

SHA-256: `6aab95c44711f3dcfff0e14dcfc23083a5435aed340268826657a759b5f7d0be`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://yngveholen.no/om-oss — title: 404 Not Found

SHA-256: `6aab95c44711f3dcfff0e14dcfc23083a5435aed340268826657a759b5f7d0be`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://yngveholen.no/personvern — title: 404 Not Found

SHA-256: `6aab95c44711f3dcfff0e14dcfc23083a5435aed340268826657a759b5f7d0be`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://yngveholen.no/personvernerklaering — title: 404 Not Found

SHA-256: `6aab95c44711f3dcfff0e14dcfc23083a5435aed340268826657a759b5f7d0be`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://yngveholen.no/kontakt-oss — title: 404 Not Found

SHA-256: `6aab95c44711f3dcfff0e14dcfc23083a5435aed340268826657a759b5f7d0be`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 999630480 / JI HOLDING AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://jiholding.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: jiholding.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: ji-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: jiholding.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ji-holding.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: jiholding.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://jiholding.no/; recorded rule: `None`; level: not saved.
- Candidate: https://jiholding.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://jiholding.com/; recorded rule: `url_refused`; level: not saved.

Page: https://jiholding.no/ — title: www.jiholding.no

SHA-256: `30fd2acdd5701ba3491f355fdac9abaadc732ab920da55221014d6026d7b63fc`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://jiholding.no/kontakt — title: 404 Not Found

SHA-256: `57e110fe5466a7497e2abdda465c23d41bf608ae63f9d1cf3008ce8622633ba9`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://jiholding.no/om-oss — title: 404 Not Found

SHA-256: `57e110fe5466a7497e2abdda465c23d41bf608ae63f9d1cf3008ce8622633ba9`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://jiholding.no/personvern — title: 404 Not Found

SHA-256: `57e110fe5466a7497e2abdda465c23d41bf608ae63f9d1cf3008ce8622633ba9`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://jiholding.no/personvernerklaering — title: 404 Not Found

SHA-256: `57e110fe5466a7497e2abdda465c23d41bf608ae63f9d1cf3008ce8622633ba9`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://jiholding.no/kontakt-oss — title: 404 Not Found

SHA-256: `57e110fe5466a7497e2abdda465c23d41bf608ae63f9d1cf3008ce8622633ba9`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://jiholding.com/ — title: 

SHA-256: `b9f05d268113e28eb1f0bef2848e33720eae060409b8dd6ea19d57109c14623e`; candidate rules: url_refused, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 995636468 / BIOMENTEK AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: hargassner.no; recorded rule: `url_refused`; level: LOW.
- Candidate: http://biomentek.no/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: biomentek.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: biomentek.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.hargassner.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://biomentek.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.biomentek.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://biomentek.no/; recorded rule: `None`; level: not saved.

Page: http://biomentek.no/ — title: A web page that points a browser to a different page after 1 seconds

SHA-256: `13a3b549812ccae8d5275bb712c67a992e14147121caecb2cfff7657482155e4`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://biomentek.no/kontakt — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://biomentek.no/om-oss — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 917438986 / T SUNDBY AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: tsundby.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: t-sundby.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tsundby.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://t-sundby.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: t-sundby.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://t-sundby.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.t-sundby.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://t-sundby.com/; recorded rule: `None`; level: not saved.

Page: http://t-sundby.com/ — title: Hosted by one.com

SHA-256: `4fee3bfe650b625deb6da561222154f83cfa0d1f8682ce0ed055215abf1f37b1`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://t-sundby.com/kontakt — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://t-sundby.com/om-oss — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://t-sundby.com/personvern — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 981304772 / KVANTEK AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: kvantek.no; recorded rule: `website_timeout`; level: LOW.
- Candidate: http://kvantek.com/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kvantek.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://kvantek.no/; recorded rule: `website_timeout`; level: not saved.
- Candidate: https://kvantek.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.kvantek.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://kvantek.com/; recorded rule: `None`; level: not saved.

Page: http://kvantek.com/ — title: 

SHA-256: `fc17b4356a8614f75ac928c672da6287e79c3649ebcccde421ad8b9785c7659e`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://kvantek.com/kontakt — title: 

SHA-256: `008bc8052e2323d4f892dc397bad94bc4fa61295619923fea932915948939c50`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://kvantek.com/om-oss — title: 

SHA-256: `008bc8052e2323d4f892dc397bad94bc4fa61295619923fea932915948939c50`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 998543118 / BYGGVISUALISERING AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://byggvisualisering.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: byggvisualisering.no; recorded rule: `corroboration`; level: LOW.
- Candidate: byggvisualisering.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://byggvisualisering.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.byggvisualisering.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://byggvisualisering.no/; recorded rule: `None`; level: not saved.

Page: http://byggvisualisering.no/ — title: Hosted by one.com

SHA-256: `4fee3bfe650b625deb6da561222154f83cfa0d1f8682ce0ed055215abf1f37b1`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://byggvisualisering.no/kontakt — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://byggvisualisering.no/om-oss — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://byggvisualisering.no/personvern — title: 404 Not Found

SHA-256: `340c8464c2007ce3f80682e15dfafa4180b641d53c14201b929906b7b0284d87`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 990623376 / H-2 HOTELL KRISTIANSUND AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://ragde.no/om-ragde/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ragde.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: h2hotellkristiansund.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: h-2-hotell-kristiansund.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: h2hotellkristiansund.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: h-2-hotell-kristiansund.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.ragde.no/; recorded rule: `None`; level: not saved.

Page: https://ragde.no/ — title: 
                            Velkommen til Ragde Eiendom | Ragde.no
                    

SHA-256: `c9140206239c0bdf2f4ead550750d9c5b39767e212184a3da6cf0fdaf628f63d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hovedmeny Eiendommer Dette er Ragde Eiendom Ragde Charge Team Ragde Charge Ledige stillinger Kontakt oss Søk Eiendomsselskap i sterk vekst Utleie og forvaltning, kjøp og salg av bolig- og næringseiendom. Alle eiendommer Raske fakta om Ragde Næringseiendom 1.8 millioner m² Parkeringerplasser 16000 Ansatte 53 Omsetning 2025 2.4 milliarder Kort fortalt Varierte prosjekter siden 1995 Visste du at Ragde Eiendom i dag består av alt fra lager, kontor, kjøpesenter, industri, hoteller og private utleieleiligheter? Gode resultater gir stabilitet Konsernets eiendomsportefølje er godt diversifisert og har i alle år levert svært gode resultater. Langvarige samarbeid Vi er opptatt av at du er fornøyd med lokalene du leier eller drifter sammen med oss. Derfor strekker vi oss den ekstra mila for at du skal bli fornøyd. God hjelp fra våre ansatte 53 ansatte fordelt på administrasjon, senterledere, vaktmestere og bygningsarbeidere står klare til å gi deg god og rask hjelp når du trenger det. Eiendommer Varierte eiendommer med moderne infrastruktur Eiendomene er geografisk godt spredt, med hovedvekt i Oslo og Bergen. Selskapet eier også eiendom i Belgia, Nederland, Sverige, Danmark og Finland. Se alle eiendommer Velkommen til Sannergata 2 Bygget er totalrenovert og utformet med fokus på kvalitet, funksjon og opplevelse. Ingenting er overlatt til tilfeldighetene – hver detalj er gjennomtenkt, fra materialvalg og belysning til møblering. Veggene prydes av flott kunst, og interiøret skaper en inspirerende og luksuriøs atmosfære som både ansatte og besøkende legger merke til. Samtidig holder eiendommen et av de høyeste nivåene innen bærekraft, miljø og energieffektivitet, sertifisert som BREEAM Excellent . Det er lagt vekt på energieffektive løsninger, smart styring av lys og ventilasjon, samt bruk av miljøvennlige materialer med lang levetid. Les mer The Box – Coworking på sitt mest inspirerende The Box er nå åpent i Sannergata 2, Løkkas nye signalbygg. Her finner du mer enn bare kontorplasser. Vi har skapt et pulserende coworking-miljø fylt med gründere, kreative sjeler og ambisiøse selskaper. Les mer Splitter nye lagre sentralt på Sinsen KUBIKK gir deg lagring med superenkel tilgang sentralt på Sinsen i Oslo. Vi har over 60 lagerplasser av ulik størrelse, og finner et lager som passer deg. Fortell oss hva du ønsker, så fikser vi resten. Les mer Kiellands Hus Smilende gode resultater På Alexander Kiellands plass tok Ragde Eiendom over nærsenteret Kiellands Hus. Med restaurering, en spennende grafisk profil og markedsføring har vi klart å løfte omsetningen 29 % siste året for våre leietakere, og fått mer fornøyde kunder. Les mer Ragde Kontakt oss Dette er Ragde Eiendom Angrerettskjema Personvernerklæring Åpenhetsloven Kameraovervåking © 2026 Ragde. All Rights Reserved. Drift av nettside levert av Mementor AS"
  ]
}
```

Page: https://ragde.no/kontakt-oss/ — title: 
                            Kontakt oss | Ragde Eiendom
                    

SHA-256: `d222682c27f82977f9b2c695492bf2fb6a3799cb80780493ecc2643e9f3aca0d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ragde.no/personvernerklaering/ — title: 
                            Personvernerklæring - Ragde
                    

SHA-256: `641e5e41165afffc246e318a9cde0d6bd67ea800ee3a0703ea88dc266c6ec4a9`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "974227037"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 917148627 / TRONDHEIM TILKOMSTTEKNIKK AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.trondheimtilkomstteknikk.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: trondheimtilkomstteknikk.no; recorded rule: `corroboration`; level: LOW.
- Candidate: trondheim-tilkomstteknikk.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: trondheimtilkomstteknikk.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: trondheim-tilkomstteknikk.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.trondheimtilkomstteknikk.no/; recorded rule: `None`; level: not saved.

Page: https://www.trondheimtilkomstteknikk.no/ — title: Hacked By Ghost louay

SHA-256: `aa8e633b49383db0e3f81dd9c6613cb23855873e4571f5c4f143c60c3dc4cb3b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.trondheimtilkomstteknikk.no/kontakt — title: Hacked By Ghost louay

SHA-256: `aa8e633b49383db0e3f81dd9c6613cb23855873e4571f5c4f143c60c3dc4cb3b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.trondheimtilkomstteknikk.no/om-oss — title: Hacked By Ghost louay

SHA-256: `aa8e633b49383db0e3f81dd9c6613cb23855873e4571f5c4f143c60c3dc4cb3b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.trondheimtilkomstteknikk.no/personvern — title: Hacked By Ghost louay

SHA-256: `aa8e633b49383db0e3f81dd9c6613cb23855873e4571f5c4f143c60c3dc4cb3b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.trondheimtilkomstteknikk.no/personvernerklaering — title: Hacked By Ghost louay

SHA-256: `aa8e633b49383db0e3f81dd9c6613cb23855873e4571f5c4f143c60c3dc4cb3b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.trondheimtilkomstteknikk.no/kontakt-oss — title: Hacked By Ghost louay

SHA-256: `aa8e633b49383db0e3f81dd9c6613cb23855873e4571f5c4f143c60c3dc4cb3b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 988330116 / KONGEVEIEN 49 KOLBOTN AS

Categories: veto; terminal website state: not_available.

- Candidate: fremtind.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: kongeveien49kolbotn.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kongeveien-49-kolbotn.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kongeveien49kolbotn.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kongeveien-49-kolbotn.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://fremtind.no/; recorded rule: `None`; level: not saved.

Page: https://www.fremtind.no/ — title: Fremtind Forsikring

SHA-256: `b76b8635327f5bc93b619d7e2f34ca04e0fc17ea6245a266bc79fd825491673e`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "915651232"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 929209850 / JØNK FRYSJA AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://www.jonkburger.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: jonkburger.no; recorded rule: `corroboration`; level: LOW.
- Candidate: joenkfrysja.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: joenk-frysja.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: joenkfrysja.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: joenk-frysja.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: jonkfrysja.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: jonkfrysja.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: jonk-frysja.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--jnk-frysja-0cb.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--jnkfrysja-l8a.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: jonk-frysja.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--jnk-frysja-0cb.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--jnkfrysja-l8a.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://jonkburger.no/; recorded rule: `None`; level: not saved.

Page: https://www.jonkburger.no/ — title: Hjem | JØNK SMASHBURGER

SHA-256: `9356113c4c036ef8a507ca2f336d0358baf9637aedd58f29fd5984f39281754e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.jonkburger.no/contact — title: Kontakt | JØNK SMASHBURGER

SHA-256: `8a7c80a2f1390babf97fbcea897a2642f82772096148dc079dd7930e99528d55`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.jonkburger.no/kontakt — title: 404 Error: Page Not Found

SHA-256: `d971680acad4e8f611b5625367108477b548d80d07a050621825f844b768d82d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 934358945 / FJORD HIKES AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://fjordhikes.no/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: fjordhikes.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: fjord-hikes.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fjordhikes.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fjord-hikes.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://fjordhikes.no/; recorded rule: `None`; level: not saved.

Page: https://fjordhikes.no/ — title: Fjordhikes - Authentic Norwegian Fjord Adventures & Hiking Tours

SHA-256: `a2a15fc63bc9bbf0b9cc308a71cb955ff09be890391995b02fc0dbb6e3dc7885`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjordhikes.no/about — title: Fjordhikes - Authentic Norwegian Fjord Adventures & Hiking Tours

SHA-256: `a2a15fc63bc9bbf0b9cc308a71cb955ff09be890391995b02fc0dbb6e3dc7885`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjordhikes.no/kontakt — title: Error

SHA-256: `00922ea6c25b59d5e0dd47969cd4c2412ef160a1256af9329f1c4dcf64095b76`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjordhikes.no/om-oss — title: Error

SHA-256: `e2a92d856261a5fefb96257fde5aa9f8fcc50b55f3f475bcbc3c3eb9c8300260`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjordhikes.no/personvern — title: Error

SHA-256: `563124c13edaf4b1d3a8a6eaa2a40b70c6189feacc4442f6ec7438987701abd6`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://fjordhikes.no/personvernerklaering — title: Error

SHA-256: `fd2a81479058436af5fdca8a583ec9cbfc3af2f42f51293d003e28a8ba1358e0`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 998989493 / XO HELICOPTERS AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: xohelicopters.no; recorded rule: `url_refused`; level: LOW.
- Candidate: xo-helicopters.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.xohelicopters.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: xohelicopters.com; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: xo-helicopters.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://xohelicopters.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://xohelicopters.com/; recorded rule: `None`; level: not saved.

Page: https://www.xohelicopters.com/ — title: Helicopter | XO Helicopters

SHA-256: `2bc6236f86c326afc7dd40acdc5019ce815f91f14a44d3d49321b807d168fb0c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.xohelicopters.com/contact-us — title: Contact Us | XO Helicopters

SHA-256: `96c4a38fe4ebad6ca69a43ea6c67765d6b79eebfd252e802afa854ffb8089b47`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.xohelicopters.com/terms — title: Terms and Conditions | XO Helicopters

SHA-256: `3b27c98afa80f7c754b770640b5950992afdb4c390481bfa1f7610c17e9dbae0`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.xohelicopters.com/kontakt — title: 404 Error: Page Not Found

SHA-256: `7eb69c8992fffc22d5a7e06e48316c805964c524463e5aa959471f8797aa0e57`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 994808540 / SMEDHAGEN SAMEIE

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: bori.no; recorded rule: `website_timeout`; level: LOW.
- Candidate: smedhagensameie.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: smedhagen-sameie.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: smedhagensameie.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: smedhagen-sameie.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.bori.no/om-bori/jobb-i-bori/sebastian-kawala/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bori.no; recorded rule: `corroboration`; level: LOW.
- Candidate: https://bori.no/; recorded rule: `website_timeout`; level: not saved.
- Candidate: https://bori.no/; recorded rule: `None`; level: not saved.

Page: https://bori.no/ — title: 302 Found

SHA-256: `fbf3632b5274808378d65cb72e934734d5ef1d61d33b0840fb0282977e8e8032`; candidate rules: corroboration, website_budget_exhausted, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/ — title: Hjem - BORI BBL

SHA-256: `a7f556fcb3af94c43a8cc5996a3a8ab3505a111c1a28293f154b03006072b724`; candidate rules: corroboration, website_budget_exhausted, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/om-bori/kontakt-oss/ — title: Kontakt oss - BORI BBL

SHA-256: `82279d0c6ec76ffe11c8a16aee378284c20ded90c1e569154ff463097c58c81f`; candidate rules: corroboration, website_budget_exhausted, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "regnskap"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/medlem/aktuelt/vilkarene-for-fordelsprogrammet-oppdateres/ — title: Vilkårene for fordelsprogrammet oppdateres - BORI BBL

SHA-256: `8d71e4584adc017ce25f6de9b1e3766670fd78443f3784a87c81fa9b6ce3a0b8`; candidate rules: corroboration, website_budget_exhausted, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/personvernerklaering/ — title: Personvernerklæring - BORI BBL

SHA-256: `4aea6518339bfb78b89eebd3b27fd4cd1fa7f9d22a0ce75e433e25328bee74dc`; candidate rules: corroboration, website_budget_exhausted, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "konsern"
  ],
  "publisher_role_markers": [
    "regnskapsmateriale",
    "regnskapsavdelingen"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/medlem/vilkar-fordelsprogram/ — title: Vilkår fordelsprogram - BORI BBL

SHA-256: `4f669ba1f6eabe99f7dd68402353cf974b1cf02a7b024a52f8dd7a4aafe56cd8`; candidate rules: corroboration, website_budget_exhausted, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/om-bori/egenerklaering-om-hvitvasking/ — title: Egenerklæring om hvitvasking - BORI BBL

SHA-256: `0ae81a0830266de99b0f18dcf4fa7d3fa610ef5abf35e88a826c1dd2bdc7e61c`; candidate rules: corroboration, website_budget_exhausted, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 918912746 / EB GROUP AS

Categories: fetched-without-proof, veto; terminal website state: not_available.

- Candidate: ebgroup.no; recorded rule: `url_refused`; level: LOW.
- Candidate: eb-group.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.ebgroup.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ebgroup.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: eb-group.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: eb-group.com; recorded rule: `group_without_exact_orgnr`; level: REJECT.
- Candidate: https://ebgroup.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.ebgroup.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://ebgroup.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://ebgroup.com/; recorded rule: `None`; level: not saved.
- Candidate: https://eb-group.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://eb-group.com/; recorded rule: `None`; level: not saved.

Page: https://ebgroup.com/ — title: 

SHA-256: `ca6dda01ca87d338d08a9862c4b0d35eca0edbe70dd2bf7e6ec09c32442b9e46`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.ebgroup.com/ — title: EB Group

SHA-256: `9a557bcff09145ca3a9dd3d5c192d07931ad25629a59660b308696dde6935230`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.ebgroup.com/kontakt — title: 

SHA-256: `07a971372b857970dd09cfa89ebaedd39c4d0ff02b4c025be1c8a39fdde3a934`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://eb-group.com/ — title: EB Group |

SHA-256: `03e194309c189d9733cb328329ebb63bd47d12d4854393bd30d02696dbbbcef8`; candidate rules: group_without_exact_orgnr, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group",
    "Group",
    "Group",
    "Group",
    "Group",
    "Group",
    "group",
    "Group",
    "Group",
    "Group",
    "Group",
    "Group",
    "Group",
    "group",
    "Group",
    "group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 933368947 / BO NEWCO AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://bocoliving.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bocoliving.no; recorded rule: `corroboration`; level: LOW.
- Candidate: bonewco.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: bo-newco.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: bonewco.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: bo-newco.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://bocoliving.no/; recorded rule: `None`; level: not saved.

Page: https://bocoliving.no/ — title: Forside - Bo Coliving

SHA-256: `95456509561748de4f27f949b8ffcf4640e2205eef90569eea694a4a5908b5cc`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://bocoliving.no/kontakt — title: Kontakt oss - Bo Coliving

SHA-256: `55282436d239d506639f8e553cc713ed8793c61467f3d072985850377548706a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://bocoliving.no/om-oss — title: Om oss - Bo Coliving

SHA-256: `5f241fabc93c4edd8863aafbc797400946a85206398ad6933c61f2962abc414c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://bocoliving.no/personvern — title: Hei, hvor vil du bo? - Bo Coliving

SHA-256: `6acc2fd38ef3dbcc3ffa2df006e57ac704fe78c4c198d3e309cb110707edb84a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 986464492 / OPTIMAL REGNSKAP AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.optimal-regnskap.no/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: optimal-regnskap.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: optimalregnskap.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimalregnskap.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimal-regnskap.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimalregnskapasavddrammen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimalregnskapasavddrammen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimal-regnskap-as-avd-drammen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimal-regnskap-as-avd-drammen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimal-regnskap-as-avd-orkanger.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimalregnskapasavdorkanger.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimal-regnskap-as-avd-orkanger.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: optimalregnskapasavdorkanger.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://optimal-regnskap.no/; recorded rule: `None`; level: not saved.

Page: https://optimal-regnskap.no/ — title: 301 Moved Permanently

SHA-256: `87a9323ac85ce28867d5d7ce590c8f29b8d1a999961fca71bb33adef48683691`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.optimal-regnskap.no/ — title: Optimal Regnskap AS -   Hjem

SHA-256: `876a8b707878e0afb23735b2accd765a63b6b5c762731c76ad1f1b66e6923050`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "og:site_name",
    "title"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskap",
    "Regnskap",
    "regnskap"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.optimal-regnskap.no/kontakt/ — title: Optimal Regnskap AS - Kontakt

SHA-256: `6b9b5486891ada7e18a8115e5e2f614a548ac590202e2771bc99daecdf64efc7`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "og:site_name",
    "title"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskap",
    "Regnskap",
    "regnskapsfører",
    "regnskap",
    "regnskapsfører",
    "regnskap",
    "regnskap",
    "regnskap"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.optimal-regnskap.no/kontakt — title: Optimal Regnskap AS - Kontakt

SHA-256: `6b9b5486891ada7e18a8115e5e2f614a548ac590202e2771bc99daecdf64efc7`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "og:site_name",
    "title"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskap",
    "Regnskap",
    "regnskapsfører",
    "regnskap",
    "regnskapsfører",
    "regnskap",
    "regnskap",
    "regnskap"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.optimal-regnskap.no/om-oss/ — title: Optimal Regnskap AS - Om oss

SHA-256: `bd6101c086889c004a1b7b22c9f3d4a72c2db34334cf885817e162efd5b90947`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "og:site_name",
    "title",
    "body",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskap",
    "Regnskap",
    "Regnskap",
    "regnskapsførerselskap",
    "regnskap",
    "regnskap"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.optimal-regnskap.no/om-oss — title: Optimal Regnskap AS - Om oss

SHA-256: `bd6101c086889c004a1b7b22c9f3d4a72c2db34334cf885817e162efd5b90947`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "og:site_name",
    "title",
    "body",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskap",
    "Regnskap",
    "Regnskap",
    "regnskapsførerselskap",
    "regnskap",
    "regnskap"
  ],
  "agency_credit_lines": []
}
```
## 20261114 / 911697688 / GRAM SVENDSEN AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.gramsvendsen.no/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: gramsvendsen.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: gram-svendsen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gramsvendsen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gram-svendsen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://gramsvendsen.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.gramsvendsen.no/; recorded rule: `None`; level: not saved.

Page: https://www.gramsvendsen.no/ — title: GramSvendsen - Hjem

SHA-256: `f948cfc9611c28b5c489b8d24cfe1ae308fae1ade51a82cd3f2323209c82a4b3`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.gramsvendsen.no/kontakt — title: GramSvendsen - Hjem

SHA-256: `77c1eee80620f5354f6b3e32a3e1edf75b4155f396a77ed9cb3f19470eb5a02e`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.gramsvendsen.no/om-oss — title: GramSvendsen - Hjem

SHA-256: `0b7698e911f5e26b8a63d451ee362125d3df3f7e8527a683d8d283d6744069d2`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.gramsvendsen.no/personvern — title: GramSvendsen - Hjem

SHA-256: `04a1548a0c6204b037ab0907f13e1822ed12f0262ff61c18fc324b61b9545c5b`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.gramsvendsen.no/personvernerklaering — title: GramSvendsen - Hjem

SHA-256: `6538768966fd4f4dfc11fa7df71ea13d587627ce7107c2f145a78d719d0d8fed`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 936187854 / WAYMARK AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: waymark.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://waymark.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: waymark.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://waymark.com/; recorded rule: `None`; level: not saved.

Page: https://waymark.com/ — title: Home

SHA-256: `5c6975a0d14fd9360342f73de3d5b69a7d0fe3f52cedfdbe8deae86f6e984fd8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://waymark.com/marketing/contact — title: Contact

SHA-256: `c70ba81fea8e59f6d9e31056f6793ae443e4fa9788abf3ba65794275465dac9b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://waymark.com/about — title: About | Waymark

SHA-256: `5fc9bbb8910b892e8d2a08e2857bee7bd2dcb6afd46c9253bfcbcc4cd17ebb4e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://waymark.com/legal/site-privacy-policy — title: Privacy Policy

SHA-256: `ad2fce8e834802806b316c575e63947bdd6a17f36cdd61cdeb108537ba88d50e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://waymark.com/legal/site-terms-of-use — title: Terms of Service

SHA-256: `908706f135a9d7b66e7f13e4ddc364f0bab9048a4f728569bcf924ffbd56f71d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://waymark.com/kontakt — title: 404 Error

SHA-256: `7b3da540404257ef44e76c277d2d0904d8f8940c61b6e254721d00fb23da090a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 986128662 / MASKINKURS AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: kristoffersenkompe.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: maskinkurs.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: maskinkurs.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: maskinkurs.com; recorded rule: `http_404`; level: LOW.
- Candidate: https://maskinkurs.no/; recorded rule: `None`; level: not saved.
- Candidate: https://maskinkurs.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.maskinkurs.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://maskinkurs.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.maskinkurs.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://maskinkurs.com/; recorded rule: `None`; level: not saved.
- Candidate: http://www.maskinkurs.com/; recorded rule: `None`; level: not saved.

Page: https://maskinkurs.no/ — title: Kurs og Sertifisering i Bergen | Maskinkurs AS

SHA-256: `ab612600fe44500ea955478ca21481559e3848684efb61ad803137e56ddcf9e1`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://maskinkurs.no/kontakt — title: Kontakt Maskinkurs AS | Kurs og Opplæring i BergenFAQ – Maskinkurs AS

SHA-256: `852e45d0162dd8ee890a3bbddf2567e05c622b96584d4a44dfc68d660357b262`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://maskinkurs.no/om-oss — title: Om Maskinkurs AS | Sertifisert Opplæringsbedrift i Bergen

SHA-256: `d3865575a1a17645516d5e8deeb68fbf99b9f17e07de4f0d09e36edf5cc4aa38`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://maskinkurs.no/privacy-policy — title: 

SHA-256: `0161ae7d5c8fefc55f345bec22477fb8f2707fe318d8c84acf9a9860357fe309`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://maskinkurs.no/personvern — title: 404 Not Found

SHA-256: `9584ae906c0f823598d1c8a925945fc42aa4ec68a459b8851d40ef6c4c2c9067`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://maskinkurs.com/ — title: Site Not Configured | 404 Not Found

SHA-256: `bf34adf3dde506c2940ede6367b0a5c72da298fb6cd04243bb0e2d874754d6cb`; candidate rules: http_404, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://www.maskinkurs.com/ — title: Site Not Configured | 404 Not Found

SHA-256: `bf34adf3dde506c2940ede6367b0a5c72da298fb6cd04243bb0e2d874754d6cb`; candidate rules: http_404, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 994882597 / DICA PROFIL & YRKESKLÆR AS

Categories: ambiguous; terminal website state: ambiguous.


Page: https://www.dica.no/ — title: 301 Moved Permanently

SHA-256: `9e17cb15dd75bbbd5dbb984eda674863c3b10ab72613cf8a39a00c3e11a8492a`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://dica.no/ — title: Dica Profil & Yrkesklær AS

SHA-256: `59fad8984afcd0d1d6e4a4e7d43f9199620bb51125df56e9e30ddf427752ccd6`; candidate rules: 

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://dica.no/kontakt/ — title: Kontakt — Dica Profil & Yrkesklær AS

SHA-256: `f5c718e0631f4f695bff7592f47fd9f68b8cc61e487a50fbe78786064cb6a7bd`; candidate rules: 

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://dica.no/ — title: Dica Profil & Yrkesklær AS

SHA-256: `93bcd31b583f7d1f4be480d025d2e44329d3ac92a477b64ef98526097fba56ae`; candidate rules: 

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 919083603 / ELENORD TRANSPORT AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: elenordtransport.no; recorded rule: `corroboration`; level: LOW.
- Candidate: elenord-transport.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: elenordtransport.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: elenord-transport.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://elenordtransport.no/; recorded rule: `None`; level: not saved.

Page: https://elenordtransport.no/ — title: Hosted By One.com | Webhosting made simple

SHA-256: `c33fcc4b8a202e637fa79652e2086de8a50239bdedb920e286ce63c489382deb`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://elenordtransport.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://elenordtransport.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://elenordtransport.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://elenordtransport.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://elenordtransport.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 935341205 / ÅSMUND VVS AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: aasmundvvs.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: aasmund-vvs.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: aasmundvvs.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: aasmund-vvs.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://asmundvvs.no/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: asmundvvs.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: asmundvvs.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: asmund-vvs.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: asmund-vvs.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--smund-vvs-42a.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--smundvvs-8za.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--smund-vvs-42a.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--smundvvs-8za.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://asmundvvs.no/; recorded rule: `None`; level: not saved.

Page: https://asmundvvs.no/ — title: asmundvvs.no

SHA-256: `7d1f63655444eea7426a8ebdea20206c486bb2c90bd8721e536dfdc9d70b1699`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Skip to content Aktuelt - - HÅNDVERK OG HOLDBARHET I HVER ENESTE LØSNING Pålitelig håndverk, god service og fagkunnskap du kan stole på. Velkommen til Åsmund VVS AS – din autoriserte rørlegger for små og store oppdrag! Enten du trenger hjelp til en liten reparasjon, oppussing av badet, installasjon av varmepumpe eller ny vann- og avløpsløsning, leverer vi arbeid med fokus på kvalitet, ryddighet og god oppfølging. Vi holder til på Geilo og tar oppdrag i hele Hallingdal og omegn – for både private, bedrifter og borettslag. Hos oss får du personlig oppfølging og løsninger som er skreddersydd for dine behov, uansett omfang. Som autorisert rørlegger legger vi vekt på: – Fagmessig utførelse etter gjeldende standarder – Punktlighet og tydelig kommunikasjon – Trygge løsninger som varer over tid Ta kontakt i dag for en uforpliktende prat om ditt prosjekt – vi hjelper deg gjerne videre! Kontakt meg på tlf 95 74 73 43 eller send meg en e-post ved å trykke på knappen under. SEND E-POST post@asmundvvs.no Åsmund VVS AS tilbyr: ✅ Service og vedlikehold ✅ Baderomsrenovering ✅ Kjøkken og sanitærinstallasjoner ✅ Rørservice ved lekkasjer og skader ✅ Varmepumper og vannbårne systemer 2026 © Åsmund VVS AS - levert av melombelom Aktuelt - Newsletter Dette nettstedet bruker cookies for å forbedre opplevelsen din. Ved å fortsette å bruke siden, godtar du dette. Accept"
  ]
}
```

Page: https://asmundvvs.no/kontakt — title: Fant ikke siden – asmundvvs.no

SHA-256: `5662d5e53b646ac6e822514328e3c4cc0ec75f56f3130465570f7455abbe9d05`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Skip to content Aktuelt - - 404 Oops! That page can’t be found. It looks like nothing was found at this location. Maybe try one of the links below or a search? 2026 © Åsmund VVS AS - levert av melombelom Aktuelt - Newsletter Dette nettstedet bruker cookies for å forbedre opplevelsen din. Ved å fortsette å bruke siden, godtar du dette. Accept"
  ]
}
```

Page: https://asmundvvs.no/om-oss — title: Fant ikke siden – asmundvvs.no

SHA-256: `5662d5e53b646ac6e822514328e3c4cc0ec75f56f3130465570f7455abbe9d05`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Skip to content Aktuelt - - 404 Oops! That page can’t be found. It looks like nothing was found at this location. Maybe try one of the links below or a search? 2026 © Åsmund VVS AS - levert av melombelom Aktuelt - Newsletter Dette nettstedet bruker cookies for å forbedre opplevelsen din. Ved å fortsette å bruke siden, godtar du dette. Accept"
  ]
}
```

Page: https://asmundvvs.no/personvern — title: Fant ikke siden – asmundvvs.no

SHA-256: `5662d5e53b646ac6e822514328e3c4cc0ec75f56f3130465570f7455abbe9d05`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Skip to content Aktuelt - - 404 Oops! That page can’t be found. It looks like nothing was found at this location. Maybe try one of the links below or a search? 2026 © Åsmund VVS AS - levert av melombelom Aktuelt - Newsletter Dette nettstedet bruker cookies for å forbedre opplevelsen din. Ved å fortsette å bruke siden, godtar du dette. Accept"
  ]
}
```

Page: https://asmundvvs.no/personvernerklaering — title: Fant ikke siden – asmundvvs.no

SHA-256: `5662d5e53b646ac6e822514328e3c4cc0ec75f56f3130465570f7455abbe9d05`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Skip to content Aktuelt - - 404 Oops! That page can’t be found. It looks like nothing was found at this location. Maybe try one of the links below or a search? 2026 © Åsmund VVS AS - levert av melombelom Aktuelt - Newsletter Dette nettstedet bruker cookies for å forbedre opplevelsen din. Ved å fortsette å bruke siden, godtar du dette. Accept"
  ]
}
```
## 20261114 / 928723240 / FINE TRANSPORT AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: finetransport.no; recorded rule: `corroboration`; level: LOW.
- Candidate: fine-transport.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: finetransport.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: fine-transport.com; recorded rule: `robots`; level: BLOCKED.
- Candidate: https://finetransport.com/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: finetransport.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://finetransport.no/; recorded rule: `None`; level: not saved.
- Candidate: https://finetransport.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://fine-transport.com/; recorded rule: `robots`; level: not saved.
- Candidate: https://finetransport.com/; recorded rule: `None`; level: not saved.

Page: https://finetransport.no/ — title: Hosted By One.com | Webhosting made simple

SHA-256: `c33fcc4b8a202e637fa79652e2086de8a50239bdedb920e286ce63c489382deb`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://finetransport.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 917222975 / RØHNE BRYGGERHUS AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://stangevestbygd.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: stangevestbygd.no; recorded rule: `registry_contact_missing`; level: MEDIUM.
- Candidate: roehnebryggerhus.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: roehne-bryggerhus.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: roehnebryggerhus.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: roehne-bryggerhus.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rohnebryggerhus.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rohnebryggerhus.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rohne-bryggerhus.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://xn--rhne-bryggerhus-5tb.no/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: xn--rhne-bryggerhus-5tb.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://www.stangevestbygd.no/firmaer/rohne-bryggerhus/; recorded rule: `None`; level: not saved.
- Candidate: https://xn--rhne-bryggerhus-5tb.no/; recorded rule: `None`; level: not saved.

Page: https://stangevestbygd.no/firmaer/rohne-bryggerhus/ — title: Røhne Bryggerhus - Stange Vestbygd

SHA-256: `f9da62dd6c6e6329b713b5192b42a4a2aacc3bdb8f0c77c21ac476824b316d6c`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://stangevestbygd.no/om-stange-vestbygd-nettverket/kontakt/ — title: Kontakt - Stange Vestbygd

SHA-256: `04db2ded20337112f6f620091612bbc7d484791a1f8c43154fb68c0951560923`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://stangevestbygd.no/om-stange-vestbygd-nettverket/pakker/ — title: Pakketilbud - Stange Vestbygd

SHA-256: `2f00beaf79a0354cca7686ee94780c922867b8679f56475124ab0a2343f5c913`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://xn--rhne-bryggerhus-5tb.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://xn--rhne-bryggerhus-5tb.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 920629148 / MARECO AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: mareco.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://mareco.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: mareco.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://mareco.com/; recorded rule: `None`; level: not saved.

Page: https://mareco.com/ — title: Mareco — Better branded products. Less guesswork.

SHA-256: `ca5f558fc87629281b5a88f6e74df11e2221a6ab90bf2421e090be01b544cfb1`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mareco.com/contact — title: Contact · Mareco

SHA-256: `5c97cd2de9c56ab7b540a2e2c8dcd7384c457bdb4c2e8276efb66bc32e2b4860`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mareco.com/about — title: About Mareco · Mareco

SHA-256: `7385a1d17124e5662fd00693e3131b6f4a6ea7fa813d8631995c55d28faacd35`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mareco.com/kontakt — title: Not found · Mareco

SHA-256: `6868b9644651cffb9897aea5f04e260ec1eae19f46bc8a333adb218474a1a439`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mareco.com/om-oss — title: Not found · Mareco

SHA-256: `c7a4625e3bbbd4b433e85aeb0db58af952d52ea255f9fe458d3d78bcde4ef622`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://mareco.com/personvern — title: Not found · Mareco

SHA-256: `52e8a44a3a81b293aac16c9d3f76baa221294849b41c49c0ecb13a5e09044494`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261114 / 917468788 / SUPERFLY HOLDING AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: superflyholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: superfly-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://superflyholding.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: superflyholding.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: superfly-holding.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://superflyholding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.superflyholding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://superflyholding.com/; recorded rule: `None`; level: not saved.

Page: http://superflyholding.com/ — title: 

SHA-256: `7e1d2fc944800e870605e3d1c838565edd4c91dcdd8f62f8e3108179d8d7ec0d`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://superflyholding.com/kontakt — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://superflyholding.com/om-oss — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://superflyholding.com/personvern — title: 404 Not Found

SHA-256: `cc0b4e42510d49c6decd464123ecf3b14ae9b47f9b4ed2ee64893e2d6520a264`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 926147528 / SEVES HOLDING AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: sevesholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: seves-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sevesholding.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://seves-holding.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: seves-holding.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://seves-holding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.seves-holding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://seves-holding.com/; recorded rule: `None`; level: not saved.

Page: http://seves-holding.com/ — title: 

SHA-256: `680bd12409acf815e9a6ee05b316f0b84ed8acdb6e57c127bb5c240184e774d6`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://seves-holding.com/kontakt — title: 

SHA-256: `5b91dd665bf31140958c0a1a6a3de0e34b41b9ef560eb7cdcb8fd255b5266604`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://seves-holding.com/om-oss — title: 

SHA-256: `5b91dd665bf31140958c0a1a6a3de0e34b41b9ef560eb7cdcb8fd255b5266604`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://seves-holding.com/personvern — title: 

SHA-256: `5b91dd665bf31140958c0a1a6a3de0e34b41b9ef560eb7cdcb8fd255b5266604`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 991248897 / DESIGNWORKS NORWAY LIMITED NUF

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://dworks.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: dworks.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: designworksnorwaylimited.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: designworks-norway-limited.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: designworksnorwaylimited.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: designworks-norway-limited.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://dworks.no/; recorded rule: `None`; level: not saved.

Page: https://dworks.no/ — title: DesignWorks – Vi skaper muligheter

SHA-256: `e1d2f90e06314e42dc9c492dc46b28d788e9fc253abb88082099e887fe064b1f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dworks.no/kontakt-oss/ — title: Kontakt oss – DesignWorks

SHA-256: `1dbf64add25c5d2cd42e1a4e92b2d9843600bd163a8f7053b0d7c90c64bd8cdc`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dworks.no/om-oss/ — title: Om oss – DesignWorks

SHA-256: `4b5636016b56ea5a4ace9d9425091f42fc615954984c4db70b7ab1ce037050e1`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dworks.no/kontakt-oss/ — title: Kontakt oss – DesignWorks

SHA-256: `cd7677e40b1758844830959be6e10611d457c7c0bc46e693bcb15efee2648d59`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 991126627 / ESPIRA DVERGSNES AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://espira.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: espira.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: espiradvergsnes.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: espira-dvergsnes.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: espiradvergsnes.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: espira-dvergsnes.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: espiradvergsnesbarnehage.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: espiradvergsnesbarnehage.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: espira-dvergsnes-barnehage.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: espira-dvergsnes-barnehage.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.espira.no/; recorded rule: `None`; level: not saved.

Page: https://www.espira.no/ — title: 

SHA-256: `8ff29f9c0aba03ecad0d7362092290241f82c3ac82474cf86d998c76506e4f1c`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://espira.no/ — title: Espira | barnehage med høy pedagogisk kvalitet og matpakkefri hverdag

SHA-256: `28cb05c701368d8c28c0d393e3a3053dac90e02fbebefdfda6cb2cfb18e5dc19`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://espira.no/om-espira/kontakt-oss — title: Kontakt Espira

SHA-256: `8a63f78215a01b9e5ed9ca68a9f23325377e3838e9ca0b8629a22f9a51b2ea28`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://espira.no/personvernerklaering — title: Personvernerklæring

SHA-256: `075a931dd003d31dd927eb9719cdda5eaffe50af75edb8d20d64b4afcc19c5aa`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://espira.no/om-espira/for-pressen — title: For pressen

SHA-256: `79d3713a3c317eb195834396d46d3b010328110eacd002a0c8c15d3d1c4e1d26`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 999254926 / KR EIENDOM AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://kreiendom.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kreiendom.no; recorded rule: `corroboration`; level: LOW.
- Candidate: kr-eiendom.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kr-eiendom.no; recorded rule: `website_timeout`; level: LOW.
- Candidate: kr-eiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kreiendom.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://kreiendom.no/; recorded rule: `None`; level: not saved.
- Candidate: https://www.kr-eiendom.no/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://www.kr-eiendom.no/; recorded rule: `website_timeout`; level: not saved.

Page: https://kreiendom.no/ — title: Index of /

SHA-256: `b943b1ff0addb9e91117a721efe5c696906c0c15b54f3b3ed90c5863b0e001be`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kreiendom.no/kontakt — title: 404 Not Found

SHA-256: `d36a026841311da3a8eae56a3ff53246fdddf658585b2d48eb49ec4c9b393243`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kreiendom.no/om-oss — title: 404 Not Found

SHA-256: `f9c551032f25ee44bdd64509d689d4391a824026525f41a82a8f15fad55099ce`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kreiendom.no/personvern — title: 404 Not Found

SHA-256: `2f67fcb0dd73af5af9eb4b263c13e419141fffe258aa5b4dde6bbcf8ea60cc85`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kreiendom.no/personvernerklaering — title: 404 Not Found

SHA-256: `127e1b1bcaa21579033cba12490e06cc04ea8925b167944b8e6204cbf45f8dbb`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kreiendom.no/kontakt-oss — title: 404 Not Found

SHA-256: `8618bd9c289cea0235d071707bd94beec98720ab3c4d6caa95ef2b1d7a0cc8d7`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 933163385 / AMBER AURA AS

Categories: fetched-without-proof, veto; terminal website state: failed.

- Candidate: amberaura.no; recorded rule: `partner_directory_mention`; level: REJECT.
- Candidate: amber-aura.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: amberaura.com; recorded rule: `robots`; level: BLOCKED.
- Candidate: https://amber-aura.com/about-me; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: amber-aura.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://amberaura.no/; recorded rule: `None`; level: not saved.
- Candidate: https://amberaura.com/; recorded rule: `robots`; level: not saved.
- Candidate: https://amber-aura.com/; recorded rule: `None`; level: not saved.

Page: https://www.amberaura.no/ — title: HOME | Amber Aura As

SHA-256: `94b4e7d2ff3f883bf77a6209140578f1f5e718f4b2ddbfb4346c2dbd0449c706`; candidate rules: partner_directory_mention

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://amber-aura.com/ — title: amber-aura.com

SHA-256: `5ca8b56552080c307bc11f9284c7c8ba7451b3e301acc6dc493f505b446898f9`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://amber-aura.com/contact-me — title: Contact Me

SHA-256: `0a9a29953d42b22ab7cd5376b260dd9658db308f80238a95a06b704657a6ed92`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 984204582 / SAMNØY AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: samnoey.no; recorded rule: `website_http_5xx`; level: LOW.
- Candidate: samnoy.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://samnoey.com/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: samnoey.com; recorded rule: `corroboration`; level: LOW.
- Candidate: samnoy.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: xn--samny-yua.no; recorded rule: `url_refused`; level: LOW.
- Candidate: https://samnoy.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: samnoy.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://samnoey.no/; recorded rule: `website_http_5xx`; level: not saved.
- Candidate: https://samnoey.com/; recorded rule: `None`; level: not saved.
- Candidate: https://samnoy.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://xn--samny-yua.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.xn--samny-yua.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://xn--samny-yua.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://samnoy.com/; recorded rule: `None`; level: not saved.

Page: https://samnoey.com/ — title: Hosted By One.com | Webhosting made simple

SHA-256: `c33fcc4b8a202e637fa79652e2086de8a50239bdedb920e286ce63c489382deb`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://samnoey.com/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://samnoey.com/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://samnoey.com/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://samnoey.com/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://samnoy.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 995742764 / SRE INVEST AS

Categories: fetched-without-proof; terminal website state: blocked.

- Candidate: sreinvest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sre-invest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sreinvest.com; recorded rule: `block_page`; level: BLOCKED.
- Candidate: https://www.sre-invest.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: sre-invest.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://sreinvest.com/; recorded rule: `block_page`; level: not saved.
- Candidate: https://sre-invest.com/; recorded rule: `None`; level: not saved.

Page: https://sre-invest.com/ — title: Redirecting to https://www.sre-invest.com/

SHA-256: `e7ba33d771f806d0b2dc356df41aa23b2bb52d62fc7d429789bd6a7fe07a60f0`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sre-invest.com/ — title: Home

SHA-256: `b73299f8992a48f079bd9224d17a368fb3ecb18f4789485e5e36494031a31ae2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sre-invest.com/contact — title: Contact

SHA-256: `488b520f090a690d785d6e9fc05c4d2e307016b133b5c4c11fbc7d0903ae584b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sre-invest.com/about — title: About

SHA-256: `15300576e200797aaa1217d6edd9d18fbc2fc4737479eb460d3575d27a548502`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "holding"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sre-invest.com/kontakt — title: Redirecting to https://www.sre-invest.com

SHA-256: `5b90672a59b738649df928841a9d9f4a3ff9e99842f178d93f7cfd972007dff6`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 919499117 / BT ENERGY AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://btenergy.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: btenergy.no; recorded rule: `corroboration`; level: LOW.
- Candidate: bt-energy.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: btenergy.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bt-energy.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://btenergy.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: btenergy.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://btenergy.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.btenergy.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://btenergy.no/; recorded rule: `None`; level: not saved.
- Candidate: https://btenergy.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://btenergy.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.btenergy.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://btenergy.com/; recorded rule: `None`; level: not saved.

Page: http://btenergy.no/ — title: btenergy.no is parked

SHA-256: `b0836636a849b193e69883ff9752ccf077facca9af9b58e85bb03fbc7f8d39af`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://btenergy.no/kontakt — title: btenergy.no is parked

SHA-256: `0e59af5243fecb85114375603503e288058b7bac5494a13565164079dfdacdd9`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://btenergy.no/om-oss — title: btenergy.no is parked

SHA-256: `fbc2943adc523082749c8ddb1b1d0988a70676f3246d7905d2e41f694f0d662c`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://btenergy.no/personvern — title: btenergy.no is parked

SHA-256: `79743cdc38871d0d7dd9532baa617514d64073225759fe554666d4c28a84788b`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://btenergy.com/ — title: BTEnergy.com - Reserved For Strategic Use

SHA-256: `a8f3d1b531e17458a6488df7f9d937d032dafe01ec85f58eae5f686fac9c58a9`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://btenergy.com/kontakt — title: BTEnergy.com - Reserved For Strategic Use

SHA-256: `52c789acc27a7b68ec7585a4653d21d635dd28fc0bc75de4ce64e5f12a7f5d13`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 934968352 / MAVTEK AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: mavtek.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.mavtek.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: mavtek.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://mavtek.com/; recorded rule: `None`; level: not saved.

Page: https://www.mavtek.com/ — title: Home | Mavtek

SHA-256: `713e1fccec15ae0550733131798c686b101ac749038f234b0bebffe77b2fdefc`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.mavtek.com/copy-of-mavtek-candidate-notice — title: Privacy Policy | Mavtek

SHA-256: `cbd925b4bd3fb9cf275bd8e35dc1ec4f89bebdfc0e6a4db22b5035eadec22adf`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.mavtek.com/kontakt — title: 404 Error: Page Not Found

SHA-256: `ae2b4886c2265a04aedf6a00ac8b9c920a47698265c3b98fbc95c2b40fbf8cb6`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 992104201 / BETTER WINES AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: betterwines.no; recorded rule: `url_refused`; level: LOW.
- Candidate: better-wines.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://betterwines.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: betterwines.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: better-wines.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.betterwines.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://betterwines.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://www.betterwines.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://betterwines.com/; recorded rule: `None`; level: not saved.

Page: https://betterwines.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://betterwines.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://betterwines.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://betterwines.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 998756308 / SAMEIET KRUMGATEN 4

Categories: veto; terminal website state: not_available.

- Candidate: enqvist.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: sameietkrumgaten4.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameiet-krumgaten-4.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameietkrumgaten4.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sameiet-krumgaten-4.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.enqvist.no/; recorded rule: `None`; level: not saved.

Page: https://enqvist.no/ — title: Boligforvaltning og forretningsførsel | Enqvist

SHA-256: `5d932d97d7abe8d8b756f2001e33fadca1272b87a64fe5ec9f18e3ed3b4d63ce`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "991398805"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Gruppen",
    "Gruppen"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 984204663 / A TIL Å PROFILERING AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: atilaa.com; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: atilaaprofilering.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: a-til-aa-profilering.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: atilaaprofilering.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: a-til-aa-profilering.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: atilaprofilering.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: atilaprofilering.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: a-til-a-profilering.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--a-til--profilering-9tb.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--atilprofilering-klb.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: a-til-a-profilering.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--a-til--profilering-9tb.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--atilprofilering-klb.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.atilaa.com/; recorded rule: `None`; level: not saved.

Page: https://www.atilaa.com/ — title: A til Å Profilering AS

SHA-256: `664f1baee243518651936b27e21f9340d6cee629d1882d5c3f857a53638ade50`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [
    "title",
    "header/logo",
    "body",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.atilaa.com/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.atilaa.com/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.atilaa.com/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.atilaa.com/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.atilaa.com/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 926078135 / GRENLANDSPORTEN 1 AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://grenlandsporten1.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: grenlandsporten1.no; recorded rule: `corroboration`; level: LOW.
- Candidate: grenlandsporten-1.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: grenlandsporten1.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: grenlandsporten-1.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://grenlandsporten1.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.grenlandsporten1.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://grenlandsporten1.no/; recorded rule: `None`; level: not saved.

Page: http://grenlandsporten1.no/ — title: grenlandsporten1.no is parked

SHA-256: `eb5933d33ea3b3a55cf1d1fbe2abf2956b819f3eb169f0a8a34bda57b515a9d6`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://grenlandsporten1.no/kontakt — title: grenlandsporten1.no is parked

SHA-256: `7f918ffaed8291602719f18ea52bffc6810df6e64f0c0480a98de88edfb17666`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://grenlandsporten1.no/om-oss — title: grenlandsporten1.no is parked

SHA-256: `39b1727e259196d31e590773d009abfb5ba0b7fcbfe070bde0f3eb64e724dd8b`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://grenlandsporten1.no/personvern — title: grenlandsporten1.no is parked

SHA-256: `3e331a8108b40ce2da3aca4e722ff8c46747b734ba2924c8add5462569a007ce`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 997843517 / AMMERUD FYSIOTERAPI AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://ammerudfysioterapi.no/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ammerudfysioterapi.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: ammerud-fysioterapi.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: ammerudfysioterapi.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: ammerud-fysioterapi.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://ammerudfysioterapi.no/; recorded rule: `None`; level: not saved.

Page: https://ammerudfysioterapi.no/ — title: Ammerud Fysioterapi

SHA-256: `16a6fc0a0f710673f875efcdee03d9d75e793c716fa7e289bea7b21c6e8b30d0`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ammerudfysioterapi.no/kontakt/ — title: Kontakt – Ammerud Fysioterapi

SHA-256: `9c93e06f157aa2b73259eca3e65c7952382315e9b58c2f81110c2b65e06fa3e8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ammerudfysioterapi.no/kontakt/ — title: Kontakt – Ammerud Fysioterapi

SHA-256: `9c93e06f157aa2b73259eca3e65c7952382315e9b58c2f81110c2b65e06fa3e8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://ammerudfysioterapi.no/om-oss — title: Page not found – Ammerud Fysioterapi

SHA-256: `0f045912014d372e83ad720225cad6f5ec0e25caacc490fb7e9523aa1343aeb2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 977141907 / KAMPEN MENIGHETS STIFTELSE

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.kirken.no/nb-NO/fellesrad/kirkeneioslo/toppmeny/kontakt%20oss/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kirken.no; recorded rule: `corroboration`; level: LOW.
- Candidate: kampenmenighetsstiftelse.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kampen-menighets-stiftelse.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kampenmenighetsstiftelse.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kampen-menighets-stiftelse.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://oslo.kirken.no/; recorded rule: `None`; level: not saved.

Page: https://www.kirken.no/kirkeneioslo — title: Kirkelig fellesråd i Oslo - Kirkelig fellesråd i Oslo

SHA-256: `52bc02fa5e36cbef8bc575c2525d2fc15601ca3e595b9c334f414277b35fd979`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kirken.no/kirkeneioslo — title: Kirkelig fellesråd i Oslo - Kirkelig fellesråd i Oslo

SHA-256: `52bc02fa5e36cbef8bc575c2525d2fc15601ca3e595b9c334f414277b35fd979`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kirken.no/kirkeneioslo — title: Kirkelig fellesråd i Oslo - Kirkelig fellesråd i Oslo

SHA-256: `52bc02fa5e36cbef8bc575c2525d2fc15601ca3e595b9c334f414277b35fd979`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 927267527 / SUS OG DUS ODDA AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://sablamoro.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: sablamoro.no; recorded rule: `corroboration`; level: LOW.
- Candidate: susdusodda.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sus-dus-odda.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: susdusodda.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: sus-dus-odda.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://sablamoro.no/; recorded rule: `None`; level: not saved.

Page: https://sablamoro.no/ — title: Sabla Moro

SHA-256: `0785d7eacc537d46a9e678401badf3654093656a6de4944870b2cc09b7e15735`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://sablamoro.no/om-sabla-moro-as/ — title: Om Sabla Moro – Sabla Moro

SHA-256: `f30d5ac9bb9b1cbd0168db6179157e509d8f443bc8327951adf50a16468487ad`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Holding",
    "Holding"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://sablamoro.no/kontakt — title: Fant ikke siden – Sabla Moro

SHA-256: `9136072653b60e23c9675c4f4fac14584426d8f5490006ee0551955e1863d71e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://sablamoro.no/om-oss — title: Fant ikke siden – Sabla Moro

SHA-256: `92d0e4d26008b5467a43fa5446005b5a24e77fc3246fa8cde18cd75c6b597821`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://sablamoro.no/personvern — title: Fant ikke siden – Sabla Moro

SHA-256: `4c3b6f0fd08912168ffa11720cddb6b1604398fb1d87675d95f47d9f70bfea9a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 986116982 / CHUBB EUROPEAN GROUP SE, NORSKREGISTRERT UTENLANDSK FORETAK NUF

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: chubb.com; recorded rule: `website_http_5xx`; level: LOW.
- Candidate: acegroup.co; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://www.chubb.com/nordic-en/contact-us/finland.html; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: chubb.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://www2.chubb.com/nordic-en; recorded rule: `None`; level: not saved.
- Candidate: https://www2.chubb.com/nordic-en; recorded rule: `website_http_5xx`; level: not saved.
- Candidate: https://acegroup.co/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.acegroup.co/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://acegroup.co/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://www2.chubb.com/nordic-en; recorded rule: `None`; level: not saved.

Page: https://www2.chubb.com/nordic-en/ — title: Error

SHA-256: `866718d61b58ebe12db301962c0ca45a0a02798fb3232734a41199b3323272c5`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www2.chubb.com/nordic-en/ — title: 301 Moved Permanently

SHA-256: `3df19be212d819fa3e7626fc225502a4eed7af2929fe59244efb425bf844da2c`; candidate rules: 

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.chubb.com/nordic-en/ — title: Chubb Nordics

SHA-256: `65c33fd68901dc93044206850d2ff8fb58bcf84cdfed1da12e5c032f50780c21`; candidate rules: corroboration, website_budget_exhausted, website_http_5xx

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.chubb.com/nordic-en/contact-us.html — title: Contact us Nordics | Chubb

SHA-256: `cb533bfd8d69caf5fae9a3d23874a1acad6277e4ba3c614fb1f5d3ec74464fc0`; candidate rules: corroboration, website_budget_exhausted, website_http_5xx

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.chubb.com/nordic-en/contact-us/denmark.html — title: Contact Us Denmark | Chubb

SHA-256: `d9f8b8fed2ee1fd31b824a0c77434f51431b0e41bcc10077a5f823ca02a05ba8`; candidate rules: corroboration, website_budget_exhausted, website_http_5xx

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 928280314 / FOSSUM & CO VVS AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://fossumcovvs.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: fossumcovvs.no; recorded rule: `corroboration`; level: LOW.
- Candidate: fossum-co-vvs.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fossumcovvs.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fossum-co-vvs.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://fossumcovvs.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.fossumcovvs.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://fossumcovvs.no/; recorded rule: `None`; level: not saved.

Page: http://fossumcovvs.no/ — title: fossumcovvs.no is parked

SHA-256: `b6cb0887cfec5c636513ed35290398a8b1a47124dc63e15ae82fe279dad1453a`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://fossumcovvs.no/kontakt — title: fossumcovvs.no is parked

SHA-256: `c24089f65c7cf7e2f129fe532b85996e64e2eb3f3c263485b9d2ba30dd381627`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://fossumcovvs.no/om-oss — title: fossumcovvs.no is parked

SHA-256: `75589a1e50066241945d995cdc6da28cce97bc9a3cfc646ecc414d427c2d771e`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://fossumcovvs.no/personvern — title: fossumcovvs.no is parked

SHA-256: `a173878f48fc34d9fd462e78b24c591586e5e479d89704bdc355872804a12dfe`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 915356559 / KG MOTOR AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.kgmotor.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kgmotor.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: kg-motor.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kgmotor.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kg-motor.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://kgmotor.no/; recorded rule: `None`; level: not saved.

Page: https://www.kgmotor.no/ — title: Vi er en forhandler som kan hjelpe kunden med å velge riktig bil - KG Motor

SHA-256: `a59b5d28202c9739dd35f95eb13f8dc4b2ff225881fdc94e214611b743747b09`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kgmotor.no/kontakt-oss/ — title: show

SHA-256: `6e23af529f94614564f17f6c2363243a26416abbc1b8baf43e1eca3b8b5d434b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kgmotor.no/om-oss/ — title: show

SHA-256: `76192dd39c1b4266210c2530c6de243bd30db7ebd7187473cfbfe77c06044dfd`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kgmotor.no/personvern/ — title: show

SHA-256: `d2cf312980c548b9d2aaeb9b536dd10ecf6c96f3e4dd903072adec666d90e2f5`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 922275998 / RYGR AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://rygr.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: rygr.no; recorded rule: `corroboration`; level: LOW.
- Candidate: rygr.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: rygr.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://rygr.no/; recorded rule: `None`; level: not saved.
- Candidate: https://rygr.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://rygr.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.rygr.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://rygr.com/; recorded rule: `url_refused`; level: not saved.

Page: https://rygr.no/ — title: Hjem - RYGR Brygghús

SHA-256: `f0da1d7f0856fa6511d851f38def02d83ab6be7181f1c772d1e3df3e54dc75c6`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rygr.no/olsmaking-omvisning/ — title: Ølsmaking/Omvisning - RYGR Brygghús

SHA-256: `5430de8c3aa0eb6fc7bed14c8b9271c3c0c95d30099e108a2b487450cb35c55f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rygr.no/kontakt/ — title: Kontakt - RYGR Brygghús

SHA-256: `73763871ee70708231229842dee7358877738b8faf144a3ba7593c8bcb3e7741`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rygr.no/kontakt/ — title: Kontakt - RYGR Brygghús

SHA-256: `73763871ee70708231229842dee7358877738b8faf144a3ba7593c8bcb3e7741`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 926561650 / BROCO AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: http://broco.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: broco.no; recorded rule: `corroboration`; level: LOW.
- Candidate: broco.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: broco.com; recorded rule: `website_http_5xx`; level: LOW.
- Candidate: https://broco.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.broco.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://broco.no/; recorded rule: `None`; level: not saved.
- Candidate: https://broco.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://broco.com/; recorded rule: `website_http_5xx`; level: not saved.

Page: http://broco.no/ — title: broco.no is parked

SHA-256: `eff81d57d6441a6bb99bd43ddff875372a1d67008f87650bdc37a70cd4b4f0d1`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://broco.no/kontakt — title: broco.no is parked

SHA-256: `99d5fe22c0d9779a11274c071e2013c744e670d88ca9d954639ee353d1f62f5c`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://broco.no/om-oss — title: broco.no is parked

SHA-256: `9ada778519ea88a875b8b459703ba9051860dd593ca2e8ac80d75e5b1ae9bd6a`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://broco.no/personvern — title: broco.no is parked

SHA-256: `5b290a59710c98da72bea1a622e9986814e164a9d125725353649b6fbddb6ebc`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 928442608 / HARTSTONE AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://hartstone.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: hartstone.no; recorded rule: `corroboration`; level: LOW.
- Candidate: hartstone.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://hartstone.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: hartstone.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://hartstone.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.hartstone.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://hartstone.no/; recorded rule: `None`; level: not saved.
- Candidate: https://hartstone.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://hartstone.com/; recorded rule: `None`; level: not saved.

Page: http://hartstone.no/ — title: hartstone.no is parked

SHA-256: `359a68b3f38525c41a11d290a5eee9e663e6aa74a1cca46633805a88965e870a`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://hartstone.no/kontakt — title: hartstone.no is parked

SHA-256: `c7b86c93d8776bb49fae54a327a8a62035a4e4b20c0d1a6d43f895a1314cfa5c`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://hartstone.no/om-oss — title: hartstone.no is parked

SHA-256: `3a003215a61b6873797b1f0623ccff96c4863cf67a6d598e3c8ecc5d38ecc0b8`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://hartstone.no/personvern — title: hartstone.no is parked

SHA-256: `aab3d2fd4f89cf332116956f2ada98375e9cb4002ec8345818d649c7555ccbce`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hartstone.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hartstone.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hartstone.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://hartstone.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 825754032 / KAB CONSULTING AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: kabconsulting.no; recorded rule: `url_refused`; level: LOW.
- Candidate: kab-consulting.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://kabconsulting.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kabconsulting.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: kab-consulting.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://kab-consulting.com/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kab-consulting.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://kabconsulting.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.kabconsulting.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://kabconsulting.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://kabconsulting.com/; recorded rule: `None`; level: not saved.
- Candidate: https://kab-consulting.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://kab-consulting.com/; recorded rule: `None`; level: not saved.

Page: https://kabconsulting.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kabconsulting.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kabconsulting.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kabconsulting.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kab-consulting.com/ — title: En construction

SHA-256: `6f2e9ab7ec5cf073b32629f789771f65be7cb10594faaf203f2d755cb7da0fea`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kab-consulting.com/kontakt — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://kab-consulting.com/om-oss — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 924276886 / SALTO AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: salto.no; recorded rule: `url_refused`; level: LOW.
- Candidate: https://salto.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: salto.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://salto.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://salto.com/; recorded rule: `None`; level: not saved.

Page: https://salto.no/ — title:  301 Moved Permanently


SHA-256: `e8b101a7c7f64aad528cc734513cbeb02243c0af37930dc0f3239749cff184b6`; candidate rules: url_refused

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://salto.com/ — title: SALTO München | SALTO Kommunikation München 2026 | Kunst / Kultur / Kommerz | Graphic Web Design, Internet Service, Klassische Medien, Print | Beratung || Audiodeskription || ART•SALTO - Hier erfahren Sie mehr zu unserem Kunstengagement, Rolf Kaiser, Muenchen, Bayern, Deutschland

SHA-256: `dde59834b944843f11deafb64c72cdce2d9aedd28c24fd7b011e8e610f8a0bc1`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://salto.com/impressum.html — title: SALTO-Impressum / Kontakt

SHA-256: `b7c4b8ab21ec309e6df74328183765de096cc90c4c8dddd2f3e072dbceef164e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://salto.com/kontakt — title: ERROR 404

SHA-256: `06c2dde0bf5a346bf3a7082394293193d9617e972bb9346a6b955e72f96bc944`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 985780595 / VRÅDAL KRAFT AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: wraa.no; recorded rule: `corroboration`; level: LOW.
- Candidate: vraadalkraft.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: vraadal-kraft.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: vraadalkraft.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: vraadal-kraft.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: vradalkraft.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: vradalkraft.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: vradal-kraft.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--vrdal-kraft-y8a.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--vrdalkraft-25a.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: vradal-kraft.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--vrdal-kraft-y8a.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://wraa.no/; recorded rule: `None`; level: not saved.

Page: https://wraa.no/ — title: Hosted By One.com | Webhosting made simple

SHA-256: `c33fcc4b8a202e637fa79652e2086de8a50239bdedb920e286ce63c489382deb`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wraa.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wraa.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wraa.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wraa.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wraa.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261115 / 988427438 / ARVEN AS

Categories: veto; terminal website state: not_available.

- Candidate: arven.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: arven.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://arven.no/; recorded rule: `None`; level: not saved.
- Candidate: https://arven.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.arven.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://arven.com/; recorded rule: `url_refused`; level: not saved.

Page: https://arven.no/ — title: 
      Arven - Norges eldste gull- og sølvprodusent
    

SHA-256: `47b766c536d6d33126e9997c6d62b2717140037baef831fcd45960875e2daa36`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hopp til innhold Forrige Fri frakt over 1000 kr i Norge Tjen bonus hver gang du handler – bli med i kundeklubben! Neste Arven Meny Arven Vintage Vintage gullsmykker Vintage sølvsmykker Vintage bunadssølv Vintage sølvbestikk Vintage sølvtøy Ingrid Vik Lysne Se alle Private Collection Smykker Nyheter fra By Arven Ringer Allianseringer Diamantringer Forlovelsesringer Gifteringer Gullringer Signetringer Sølvringer Perleringer Ringer med fargesten Ørepynt Diamantørepynt Gullørepynt Sølvørepynt Perleørepynt Ørepynt med fargesten Øreringer Halssmykker Anheng med fargesten Diamantanheng Gullanheng Halssmykker til barn Kjeder Mynt Perlesmykker Sølvsmykker Armbånd Armringer Diamantarmbånd Se alle armbånd Gaver Til henne Til han Til barn Bryllupsgaver Gavekort Kolleksjoner Handmade by Arven Bryggemynt Kvartpenning Unisex Piccolini Mia Perlesmykker Sløyfer Bon Bon Skjerfringer By Arven Nyheter Gold Collection Silver Collection Private Collection Ekenberg Scandinavia Pulpit Rock Flying Birds Fjords Of Norway In Your Hand Bryllup & Forlovelse Arven`s bryllupsunivers Gifteringer Forlovelsesringer Smykker til bruden Til brudgommen Gave til brudeparet Sølvbestikk Sølvbestikk Sølv til barn Serviettring Interiør Sølv til barn Lysestaker Vaser Fat/skåler/krus Salt- og peppersett Vikingskip Pokaler og medaljer Julepynt Tilbehør 17. maisløyfer Silkeskjerf Skjerfringer Pride sløyfer Mansjettknapper Skjorteknapper Smykkeskrin Pussemidler Selg ditt gull/sølv Tjenester Design selv Reparasjon NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English Konto Søk Handlekurv Lukk Arven Vintage Private Collection Smykker Kolleksjoner Bryllup & Forlovelse Sølvbestikk Interiør Tilbehør Selg ditt gull/sølv Tjenester Konto NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English Handlekurv Handlekurven din er tom For øyeblikk som varer evig Norsk håndverk siden 1868 COMING SOON... NESTE VINTAGE DROP Arven har startet nedtellingen til neste vintage drop. Finn favorittene dine, så er du klar 15. november kl. 20:00. Vintage drop Forrige COMING SOON Arven Vintage Vintage glatt ring gult gull str54 Salgspris kr 3 395,- COMING SOON Arven Vintage Vintage ring gult gull str57 Salgspris kr 4 695,- COMING SOON Arven Vintage Vintage ørepynt gult gull Salgspris kr 3 795,- COMING SOON Arven Vintage Vintage ørepynt gult og hvitt gull Salgspris kr 2 195,- COMING SOON Arven Vintage Vintage glatt ring gult gull str53 Salgspris kr 3 595,- COMING SOON Arven Vintage Vintage glatt ring gult gull str54 Salgspris kr 5 595,- COMING SOON Arven Vintage Vintage diamantørepynt hvitt gull Salgspris kr 5 795,- COMING SOON Arven Vintage Vintage glatt ring gult gull str57 Salgspris kr 9 695,- Neste Se alle De beste julegavene kommer i en liten eske... Oppdag våre beste julegavetips! Se alle Skal du fri? Oppdag våre forlovelsesringer Forrige By Arven Aurora Solitairering Salgspris Fra kr 18 250,- Kvalitet Hvitt gull Gult gull By Arven Celine Halo Diamantring Salgspris Fra kr 21 600,- Kvalitet Gult gull Hvitt gull By Arven Diana Diamantring Salgspris Fra kr 26 900,- Kvalitet Hvitt gull Gult gull By Arven Elara Emerald Diamantring Salgspris Fra kr 26 200,- Kvalitet Hvitt gull Gult gull By Arven Elena Diamantring Salgspris Fra kr 13 750,- Kvalitet Gult gull Hvitt gull By Arven Flora Rosettring Salgspris Fra kr 19 400,- Kvalitet Hvitt gull Gult gull By Arven Freya Oval Diamantring Salgspris Fra kr 26 500,- Kvalitet Hvitt gull Gult gull Handmade By Arven Guri Solitairering Salgspris Fra kr 17 850,- Kvalitet Gult gull Hvitt gull Neste Se alle Utforsk kolleksjonene Forrige Handmade by Arven Arven Vintage By Arven Private Collection Neste Tjen bonus hver gang du handler – bli med i kundeklubben! Bli ARVEN-VENN 4.69 ★ ( 42 ) Verified Bli inspirert! Tips og Inspirasjon De fire C-ene | Slik vurderer du en diamant Skal du kjøpe en diamant – til en forlovelsesring, et anheng eller bare til deg selv? Da møter du fort fire ord: carat, cut, clarity og color. Her forklarer vi hva de betyr, og hvordan du kan bruke... Les mer Gavetips Populære julegaver | til han Leter du etter julegave til han? Se fire populære gaveidéer fra Arven: ringer, armbånd, halssmykker, mansjettknapper og personlig gravering, laget av gullsmeder i Bergen. Les mer Gavetips Julegaver | gi en gave som varer Leter du etter en julegave som varer? Se Arvens gaveguide til julen 2026 med smykker i gull og sølv, perler, vintage og personlig gravering. Les mer Alle artikler Unik design & høyeste kvalitet Est. 1868 Egen butikk & verksted Grønn og bærekraftig produksjon 100% resirkulert gull og sølv Gå til element 1 Gå til element 2 Gå til element 3 Gå til element 4 Gå til element 5 Tjenester Salg/kjøp av gull og sølv Bestill time gullsmed Reparasjon/oppussing Taksering Gravering Forsølving og forgylling Omvisning hos Arven Kundeservice Min side - kundeklubb Ofte stilte spørsmål Garanti Bytte og retur Sikker betaling Salgsbetingelser Betingelser service Login forhandler Personvern Våre produkter Arven Vintage Private Collection Smykker Kolleksjoner Bryllup & Forlovelse Sølvbestikk Interiør Tilbehør Selg ditt gull/sølv Tjenester Om Arven Om Arven Kontakt oss Kundeklubb Garanti på smykker Våre grønne reise Vår historie Omvisning hos Arven NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English © 2026 - Arven Utviklet av appsalon{"
  ]
}
```

Page: https://arven.no/pages/contact — title: 
      Kontakt oss
    

SHA-256: `dec32afe3c235558ef0a2334fd3bcb335d2020cd0d3737d00807669884f26ff3`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hopp til innhold Forrige Fri frakt over 1000 kr i Norge Tjen bonus hver gang du handler – bli med i kundeklubben! Neste Arven Meny Arven Vintage Vintage gullsmykker Vintage sølvsmykker Vintage bunadssølv Vintage sølvbestikk Vintage sølvtøy Ingrid Vik Lysne Se alle Private Collection Smykker Nyheter fra By Arven Ringer Allianseringer Diamantringer Forlovelsesringer Gifteringer Gullringer Signetringer Sølvringer Perleringer Ringer med fargesten Ørepynt Diamantørepynt Gullørepynt Sølvørepynt Perleørepynt Ørepynt med fargesten Øreringer Halssmykker Anheng med fargesten Diamantanheng Gullanheng Halssmykker til barn Kjeder Mynt Perlesmykker Sølvsmykker Armbånd Armringer Diamantarmbånd Se alle armbånd Gaver Til henne Til han Til barn Bryllupsgaver Gavekort Kolleksjoner Handmade by Arven Bryggemynt Kvartpenning Unisex Piccolini Mia Perlesmykker Sløyfer Bon Bon Skjerfringer By Arven Nyheter Gold Collection Silver Collection Private Collection Ekenberg Scandinavia Pulpit Rock Flying Birds Fjords Of Norway In Your Hand Bryllup & Forlovelse Arven`s bryllupsunivers Gifteringer Forlovelsesringer Smykker til bruden Til brudgommen Gave til brudeparet Sølvbestikk Sølvbestikk Sølv til barn Serviettring Interiør Sølv til barn Lysestaker Vaser Fat/skåler/krus Salt- og peppersett Vikingskip Pokaler og medaljer Julepynt Tilbehør 17. maisløyfer Silkeskjerf Skjerfringer Pride sløyfer Mansjettknapper Skjorteknapper Smykkeskrin Pussemidler Selg ditt gull/sølv Tjenester Design selv Reparasjon NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English Konto Søk Handlekurv Lukk Arven Vintage Private Collection Smykker Kolleksjoner Bryllup & Forlovelse Sølvbestikk Interiør Tilbehør Selg ditt gull/sølv Tjenester Konto NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English Handlekurv Handlekurven din er tom Vi hjelper deg gjerne! Kontakt oss Trenger du veiledning, eller har du spørsmål om våre produkter og tjenester? Vi tar gjerne en prat og hjelper deg med alt fra inspirasjon og gaveidéer til valg av smykker og sølv som varer i generasjoner. Nedenfor finner du vår kontaktinformasjon – vi ser frem til å høre fra deg. Besøk oss Du finner oss i vår butikk i Sandbrogaten 11, 5006 Bergen. Kom innom for å se våre produkter og få personlig service fra vårt dyktige team. Våre åpningstider er: Mandag-fredag kl.10:00-17:00 Lørdag kl. 10:00-15:00. Åpne kart --> Ring oss Kundesenter: 55 55 14 40 Åpningstider : Mandag - fredag 09:00-15:30 (telefon er stengt mellom kl. 11:30-12:00). Send oss en e-post Kundesenter: hello@arven.no Butikk: shop@arven.no For spørsmål om kjøp og salg av gull og sølv: oppgjor@arven.no For spørsmål om serviceordre du har inne hos oss: service@arven.no Er du forhandler? Ta kontakt med vårt kundesenter: kundesenter@arven.no Vi svarer vanligvis innen 1-4 virkedager. Send oss en melding Ta kontakt med oss der dersom du har spørsmål vedrørende produkt, tjeneste, retur, etc. OBS! Spørsmål knyttet til din bestilling ( hello@arven.no) eller service og pristilbud ( service@arven.no ) må henvendes til oppgitt epostadresse eller pr. telefon 55 55 14 40. Navn E-post Melding Send melding 4.69 ★ ( 42 ) Verified Bli inspirert! Tips og Inspirasjon De fire C-ene | Slik vurderer du en diamant Skal du kjøpe en diamant – til en forlovelsesring, et anheng eller bare til deg selv? Da møter du fort fire ord: carat, cut, clarity og color. Her forklarer vi hva de betyr, og hvordan du kan bruke... Les mer Gavetips Populære julegaver | til han Leter du etter julegave til han? Se fire populære gaveidéer fra Arven: ringer, armbånd, halssmykker, mansjettknapper og personlig gravering, laget av gullsmeder i Bergen. Les mer Gavetips Julegaver | gi en gave som varer Leter du etter en julegave som varer? Se Arvens gaveguide til julen 2026 med smykker i gull og sølv, perler, vintage og personlig gravering. Les mer Alle artikler Unik design & høyeste kvalitet Est. 1868 Egen butikk & verksted Grønn og bærekraftig produksjon 100% resirkulert gull og sølv Gå til element 1 Gå til element 2 Gå til element 3 Gå til element 4 Gå til element 5 Tjenester Salg/kjøp av gull og sølv Bestill time gullsmed Reparasjon/oppussing Taksering Gravering Forsølving og forgylling Omvisning hos Arven Kundeservice Min side - kundeklubb Ofte stilte spørsmål Garanti Bytte og retur Sikker betaling Salgsbetingelser Betingelser service Login forhandler Personvern Våre produkter Arven Vintage Private Collection Smykker Kolleksjoner Bryllup & Forlovelse Sølvbestikk Interiør Tilbehør Selg ditt gull/sølv Tjenester Om Arven Om Arven Kontakt oss Kundeklubb Garanti på smykker Våre grønne reise Vår historie Omvisning hos Arven NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English © 2026 - Arven Utviklet av appsalon{"
  ]
}
```

Page: https://arven.no/policies/terms-of-service — title: 
      Vilkår for bruk
    

SHA-256: `7f2e04bb80662cda7491abc1371c49f07203ba0a97740328e10ab209f5f1fdb7`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [
    "body"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "916839898"
  ],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Hopp til innhold Forrige Fri frakt over 1000 kr i Norge Tjen bonus hver gang du handler – bli med i kundeklubben! Neste Arven Meny Arven Vintage Vintage gullsmykker Vintage sølvsmykker Vintage bunadssølv Vintage sølvbestikk Vintage sølvtøy Ingrid Vik Lysne Se alle Private Collection Smykker Nyheter fra By Arven Ringer Allianseringer Diamantringer Forlovelsesringer Gifteringer Gullringer Signetringer Sølvringer Perleringer Ringer med fargesten Ørepynt Diamantørepynt Gullørepynt Sølvørepynt Perleørepynt Ørepynt med fargesten Øreringer Halssmykker Anheng med fargesten Diamantanheng Gullanheng Halssmykker til barn Kjeder Mynt Perlesmykker Sølvsmykker Armbånd Armringer Diamantarmbånd Se alle armbånd Gaver Til henne Til han Til barn Bryllupsgaver Gavekort Kolleksjoner Handmade by Arven Bryggemynt Kvartpenning Unisex Piccolini Mia Perlesmykker Sløyfer Bon Bon Skjerfringer By Arven Nyheter Gold Collection Silver Collection Private Collection Ekenberg Scandinavia Pulpit Rock Flying Birds Fjords Of Norway In Your Hand Bryllup & Forlovelse Arven`s bryllupsunivers Gifteringer Forlovelsesringer Smykker til bruden Til brudgommen Gave til brudeparet Sølvbestikk Sølvbestikk Sølv til barn Serviettring Interiør Sølv til barn Lysestaker Vaser Fat/skåler/krus Salt- og peppersett Vikingskip Pokaler og medaljer Julepynt Tilbehør 17. maisløyfer Silkeskjerf Skjerfringer Pride sløyfer Mansjettknapper Skjorteknapper Smykkeskrin Pussemidler Selg ditt gull/sølv Tjenester Design selv Reparasjon NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English Konto Søk Handlekurv Lukk Arven Vintage Private Collection Smykker Kolleksjoner Bryllup & Forlovelse Sølvbestikk Interiør Tilbehør Selg ditt gull/sølv Tjenester Konto NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English Handlekurv Handlekurven din er tom Vilkår for bruk Salgsbetingelser Kjøp via arven.no er regulert av standard salgsbetingelser for forbrukerkjøp av varer over Internett. Forbrukerkjøp over internett reguleres hovedsakelig av avtaleloven, forbrukerkjøpsloven, markedsføringsloven, angrerettloven og ehandelsloven, og disse lovene gir forbrukeren ufravikelige rettigheter. Lovene er tilgjengelig på www.lovdata.no . Vilkårene i denne avtalen skal ikke forstås som noen begrensning i de lovbestemte rettighetene, men oppstiller partenes viktigste rettigheter og plikter for handelen. Salgsbetingelsene er laget med utgangspunkt i anbefalinger fra Forbrukerombudet. 1. Avtalen Avtalen består av disse salgsbetingelsene, opplysninger gitt i bestillingsløsningen og eventuelt særskilt avtalte vilkår. Ved eventuell motstrid mellom opplysningene, går det som særskilt er avtalt mellom partene foran, så fremt det ikke strider mot ufravikelig lovgivning. Avtalen vil i tillegg bli utfylt av relevante lovbestemmelser som regulerer kjøp av varer mellom næringsdrivende og forbrukere. 2. Partene Selger er Arven AS, Sandbrogaten 11, 5003 Bergen Org.nr: 916 839 898 Kjøper er den forbrukeren som foretar bestillingen, og betegnes i det følgende som kjøper/kjøperen. 3. Pris Den oppgitte prisen for varen og tjenester er den totale prisen kjøper skal betale. Denne prisen inkluderer alle avgifter og tilleggskostnader. Ytterligere kostnader som selger før kjøpet ikke har informert om, skal kjøper ikke bære. 4. Avtaleinngåelse Avtalen er bindende for begge parter når kjøperen har sendt sin bestilling til selgeren. Avtalen er likevel ikke bindende hvis det har forekommet skrive- eller tastefeil i tilbudet fra selgeren i bestillingsløsningen i nettbutikken eller i kjøperens bestilling, og den annen part innså eller burde ha innsett at det forelå en slik feil. 5. Betaling Selgeren kan kreve betaling for varen fra det tidspunkt den blir sendt fra selgeren til kjøperen. Dersom kjøperen bruker kredittkort eller debetkort ved betaling, kan selgeren reservere kjøpesummen på kortet ved bestilling. Kortet blir belastet samme dag som varen sendes. Ved betaling med faktura, blir fakturaen til kjøperen utstedt ved forsendelse av varen. Betalingsfristen fremgår av fakturaen og er på minimum 14 dager fra mottak. Kjøpere under 18 år kan ikke betale med etterfølgende faktura. 6. Levering Levering er skjedd når kjøperen, eller hans representant, har overtatt tingen. Hvis ikke leveringstidspunkt fremgår av bestillingsløsningen, skal selgeren levere varen til kjøper uten unødig opphold og senest 30 dager etter bestillingen fra kunden. Varen skal leveres hos kjøperen med mindre annet er særskilt avtalt mellom partene. 7. Risikoen for varen Risikoen for varen går over på kjøper når han, eller hans representant, har fått varene levert i tråd med punkt 6. 8. Angrerett Med mindre avtalen er unntatt fra angrerett, kan kjøperen angre kjøpet av varen i henhold til angrerettloven. Kjøperen må gi selger melding om bruk av angreretten innen 14 dager fra fristen begynner å løpe. I fristen inkluderes alle kalenderdager. Dersom fristen ender på en lørdag, helligdag eller høytidsdag forlenges fristen til nærmeste virkedag. Angrefristen anses overholdt dersom melding er sendt før utløpet av fristen. Kjøper har bevisbyrden for at angreretten er blitt gjort gjeldende, og meldingen bør derfor skje skriftlig (angrerettskjema, e-post eller brev).Angrefristen begynner å løpe: • Ved kjøp av enkeltstående varer vil angrefristen løpe fra dagen etter varen(e) er mottatt. • Består kjøpet av flere leveranser, vil angrefristen løpe fra dagen etter siste leveranse er mottatt. Angrefristen utvides til 12 måneder etter utløpet av den opprinnelige fristen dersom selger ikke før avtaleinngåelsen opplyser om at det foreligger angrerett og standardisert angreskjema. Tilsvarende gjelder ved manglende opplysning om vilkår, tidsfrister og fremgangsmåte for å benytte angreretten. Sørger den næringsdrivende for å gi opplysningene i løpet av disse 12 månedene, utløper angrefristen likevel 14 dager etter den dagen kjøperen mottok opplysningene. Ved bruk av angreretten må varen leveres tilbake til selgeren uten unødig opphold og senest 14 dager fra melding om bruk av angreretten er gitt. Kjøper dekker de direkte kostnadene ved å returnere varen (bruk av vedlagt returseddel kr.99), med mindre annet er avtalt eller selger har unnlatt å opplyse om at kjøper skal dekke returkostnadene. Kjøper kan prøve eller teste varen på en forsvarlig måte for å fastslå varens art, egenskaper og funksjon, uten at angreretten faller bort. Dersom prøving eller test av varen går utover hva som er forsvarlig og nødvendig, kan kjøperen bli ansvarlig for eventuell redusert verdi på varen. Selgeren er forpliktet til å tilbakebetale kjøpesummen for varen(e) til kjøperen uten unødig opphold, og senest 14 dager fra selgeren fikk melding om kjøperens beslutning om å benytte angreretten. Selger har rett til å holde tilbake betalingen til han har mottatt varene fra kjøperen, eller til kjøper har lagt frem dokumentasjon for at varene er sendt tilbake. 9. Forsinkelse og manglende levering - kjøpernes rettigheter og frist for å melde krav Dersom selgeren ikke leverer varen eller leverer den for sent i henhold til avtalen mellom partene, og dette ikke skyldes kjøperen eller forhold på kjøperens side, kan kjøperen i henhold til reglene i forbrukerkjøpslovens kapittel 5 etter omstendighetene holde kjøpesummen tilbake, kreve oppfyllelse, heve avtalen og/eller kreve erstatning fra selgeren. Ved krav om misligholdsbeføyelser bør meldingen av bevishensyn være skriftlig (for eksempel e-post). Oppfyllelse Kjøper kan fastholde kjøpet og kreve oppfyllelse fra selger. Kjøper kan imidlertid ikke kreve oppfyllelse dersom det foreligger en hindring som selgeren ikke kan overvinne, eller dersom oppfyllelse vil medføre en så stor ulempe eller kostnad for selger at det står i vesentlig misforhold til kjøperens interesse i at selgeren oppfyller. Skulle vanskene falle bort innen rimelig tid, kan kjøper likevel kreve oppfyllelse. Kjøperen taper sin rett til å kreve oppfyllelse om han eller hun venter urimelig lenge med å fremme kravet. Heving Dersom selgeren ikke leverer varen på leveringstidspunktet, skal kjøperen oppfordre selger til å levere innen en rimelig tilleggsfrist for oppfyllelse. Dersom selger ikke leverer varen innen tilleggsfristen, kan kjøperen heve kjøpet. Kjøper kan imidlertid heve kjøpet umiddelbart hvis selger nekter å levere varen. Tilsvarende gjelder dersom levering til avtalt tid var avgjørende for inngåelsen av avtalen, eller dersom kjøperen har underrettet selger om at leveringstidspunktet er avgjørende. Leveres tingen etter tilleggsfristen forbrukeren har satt eller etter leveringstidspunktet som var avgjørende for inngåelsen av avtalen, må krav om heving gjøres gjeldende innen rimelig tid etter at kjøperen fikk vite om leveringen. Erstatning Kjøperen kan kreve erstatning for lidt tap som følge av forsinkelsen. Dette gjelder imidlertid ikke dersom selgeren godtgjør at forsinkelsen skyldes hindring utenfor selgers kontroll som ikke med rimelighet kunne blitt tatt i betraktning på avtaletiden, unngått, eller overvunnet følgene av. 10. Mangel ved varen - kjøperens rettigheter og reklamasjonsfrist Hvis det foreligger en mangel ved varen må kjøper innen rimelig tid etter at den ble oppdaget eller burde ha blitt oppdaget, gi selger melding om at han eller hun vil påberope seg mangelen. Kjøper har alltid reklamert tidsnok dersom det skjer innen 2 måneder fra mangelen ble oppdaget eller burde blitt oppdaget. Reklamasjon kan skje senest to år etter at kjøper overtok varen. Dersom varen eller deler av den er ment å vare vesentlig lenger enn to år, er reklamasjonsfristen fem år. Dersom varen har en mangel og dette ikke skyldes kjøperen eller forhold på kjøperens side, kan kjøperen i henhold til reglene i forbrukerkjøpsloven kapittel 6 etter omstendighetene holde kjøpesummen tilbake, velge mellom retting og omlevering, kreve prisavslag, kreve avtalen hevet og/eller kreve erstatning fra selgeren. Reklamasjon til selgeren bør skje skriftlig. Retting eller omlevering Kjøperen kan velge mellom å kreve mangelen rettet eller levering av tilsvarende ting. Selger kan likevel motsette seg kjøperens krav dersom gjennomføringen av kravet er umulig eller volder selgeren urimelige kostnader. Retting eller omlevering skal foretas innen rimelig tid. Selger har i utgangspunktet ikke rett til å foreta mer enn to avhjelpsforsøk for samme mangel. Prisavslag Kjøper kan kreve et passende prisavslag dersom varen ikke blir rettet eller omlevert. Dette innebærer at forholdet mellom nedsatt og avtalt pris svarer til forholdet mellom tingens verdi i mangelfull og kontraktsmessig stand. Dersom særlige grunner taler for det, kan prisavslaget i stedet settes lik mangelens betydning for kjøperen. Heving Dersom varen ikke er rettet eller omlevert, kan kjøperen også heve kjøpet når mangelen ikke er uvesentlig. 11. Selgerens rettigheter ved kjøperens mislighold Dersom kjøperen ikke betaler eller oppfyller de øvrige pliktene etter avtalen eller loven, og dette ikke skyldes selgeren eller forhold på selgerens side, kan selgeren i henhold til reglene i forbrukerkjøpsloven kapittel 9 etter omstendighetene holde varen tilbake, kreve oppfyllelse av avtalen, kreve avtalen hevet samt kreve erstatning fra kjøperen. Selgeren vil også etter omstendighetene kunne kreve renter ved forsinket betaling, inkassogebyr og et rimelig gebyr ved uavhentede varer. Oppfyllelse Selger kan fastholde kjøpet og kreve at kjøperen betaler kjøpesummen. Er varen ikke levert, taper selgeren sin rett dersom han venter urimelig lenge med å fremme kravet. Heving Selger kan heve avtalen dersom det foreligger vesentlig betalingsmislighold eller annet vesentlig mislighold fra kjøperens side. Selger kan likevel ikke heve dersom hele kjøpesummen er betalt. Fastsetter selger en rimelig tilleggsfrist for oppfyllelse og kjøperen ikke betaler innen denne fristen, kan selger heve kjøpet. Renter ved forsinket betaling/inkassogebyr Dersom kjøperen ikke betaler kjøpesummen i henhold til avtalen, kan selger kreve renter av kjøpesummen etter forsinkelsesrenteloven. Ved manglende betaling kan kravet, etter forutgående varsel, bli sendt til Kjøper kan da bli holdt ansvarlig for gebyr etter inkassoloven. Gebyr ved uavhentede ikke-forskuddsbetalte varer Dersom kjøperen unnlater å hente ubetalte varer, kan selger belaste kjøper med et gebyr. Gebyret skal maksimalt dekke selgerens faktiske utlegg for å levere varen til kjøperen. Et slikt gebyr kan ikke belastes kjøpere under 18 år. 12. Garanti Garanti som gis av selgeren eller produsenten, gir kjøperen rettigheter i tillegg til de kjøperen allerede har etter ufravikelig lovgivning. En garanti innebærer dermed ingen begrensninger i kjøperens rett til reklamasjon og krav ved forsinkelse eller mangler etter punkt 9 og 10. 13. Personopplysninger Behandlingsansvarlig for innsamlede personopplysninger er selger. Med mindre kjøperen samtykker til noe annet, kan selgeren, i tråd med personopplysningsloven, kun innhente og lagre de personopplysninger som er nødvendig for at selgeren skal kunne gjennomføre forpliktelsene etter avtalen. Kjøperens personopplysninger vil kun bli utlevert til andre hvis det er nødvendig for at selger skal få gjennomført avtalen med kjøperen, eller i lovbestemte tilfelle. 14. Konfliktløsning Klager rettes til selger innen rimelig tid, jf. punkt 9 og 10. Partene skal forsøke å løse eventuelle tvister i minnelighet. Dersom dette ikke lykkes, kan kjøperen ta kontakt med Forbrukerrådet for mekling. Forbrukerrådet er tilgjengelig på telefon 23 400 500 eller www.forbrukerradet.no. 4.69 ★ ( 42 ) Verified Bli inspirert! Tips og Inspirasjon De fire C-ene | Slik vurderer du en diamant Skal du kjøpe en diamant – til en forlovelsesring, et anheng eller bare til deg selv? Da møter du fort fire ord: carat, cut, clarity og color. Her forklarer vi hva de betyr, og hvordan du kan bruke... Les mer Gavetips Populære julegaver | til han Leter du etter julegave til han? Se fire populære gaveidéer fra Arven: ringer, armbånd, halssmykker, mansjettknapper og personlig gravering, laget av gullsmeder i Bergen. Les mer Gavetips Julegaver | gi en gave som varer Leter du etter en julegave som varer? Se Arvens gaveguide til julen 2026 med smykker i gull og sølv, perler, vintage og personlig gravering. Les mer Alle artikler Unik design & høyeste kvalitet Est. 1868 Egen butikk & verksted Grønn og bærekraftig produksjon 100% resirkulert gull og sølv Gå til element 1 Gå til element 2 Gå til element 3 Gå til element 4 Gå til element 5 Tjenester Salg/kjøp av gull og sølv Bestill time gullsmed Reparasjon/oppussing Taksering Gravering Forsølving og forgylling Omvisning hos Arven Kundeservice Min side - kundeklubb Ofte stilte spørsmål Garanti Bytte og retur Sikker betaling Salgsbetingelser Betingelser service Login forhandler Personvern Våre produkter Arven Vintage Private Collection Smykker Kolleksjoner Bryllup & Forlovelse Sølvbestikk Interiør Tilbehør Selg ditt gull/sølv Tjenester Om Arven Om Arven Kontakt oss Kundeklubb Garanti på smykker Våre grønne reise Vår historie Omvisning hos Arven NOK kr Land Afghanistan (NOK kr) Åland Islands (NOK kr) Albania (NOK kr) Algeria (NOK kr) Andorra (NOK kr) Angola (NOK kr) Anguilla (NOK kr) Antigua & Barbuda (NOK kr) Argentina (NOK kr) Armenia (NOK kr) Aruba (NOK kr) Ascension Island (NOK kr) Australia (NOK kr) Austria (NOK kr) Azerbaijan (NOK kr) Bahamas (NOK kr) Bahrain (NOK kr) Bangladesh (NOK kr) Barbados (NOK kr) Belarus (NOK kr) Belgium (NOK kr) Belize (NOK kr) Benin (NOK kr) Bermuda (NOK kr) Bhutan (NOK kr) Bolivia (NOK kr) Bosnia & Herzegovina (NOK kr) Botswana (NOK kr) Brazil (NOK kr) British Indian Ocean Territory (NOK kr) British Virgin Islands (NOK kr) Brunei (NOK kr) Bulgaria (NOK kr) Burkina Faso (NOK kr) Burundi (NOK kr) Cambodia (NOK kr) Cameroon (NOK kr) Canada (NOK kr) Cape Verde (NOK kr) Caribbean Netherlands (NOK kr) Cayman Islands (NOK kr) Central African Republic (NOK kr) Chad (NOK kr) Chile (NOK kr) China (NOK kr) Christmas Island (NOK kr) Cocos (Keeling) Islands (NOK kr) Colombia (NOK kr) Comoros (NOK kr) Congo - Brazzaville (NOK kr) Congo - Kinshasa (NOK kr) Cook Islands (NOK kr) Costa Rica (NOK kr) Côte d’Ivoire (NOK kr) Croatia (NOK kr) Curaçao (NOK kr) Cyprus (NOK kr) Czechia (NOK kr) Denmark (NOK kr) Djibouti (NOK kr) Dominica (NOK kr) Dominican Republic (NOK kr) Ecuador (NOK kr) Egypt (NOK kr) El Salvador (NOK kr) Equatorial Guinea (NOK kr) Eritrea (NOK kr) Estonia (NOK kr) Eswatini (NOK kr) Ethiopia (NOK kr) Falkland Islands (NOK kr) Faroe Islands (NOK kr) Fiji (NOK kr) Finland (NOK kr) France (NOK kr) French Guiana (NOK kr) French Polynesia (NOK kr) French Southern Territories (NOK kr) Gabon (NOK kr) Gambia (NOK kr) Georgia (NOK kr) Germany (NOK kr) Ghana (NOK kr) Gibraltar (NOK kr) Greece (NOK kr) Greenland (NOK kr) Grenada (NOK kr) Guadeloupe (NOK kr) Guatemala (NOK kr) Guernsey (NOK kr) Guinea (NOK kr) Guinea-Bissau (NOK kr) Guyana (NOK kr) Haiti (NOK kr) Honduras (NOK kr) Hong Kong SAR (NOK kr) Hungary (NOK kr) Iceland (NOK kr) India (NOK kr) Indonesia (NOK kr) Iraq (NOK kr) Ireland (NOK kr) Isle of Man (NOK kr) Israel (NOK kr) Italy (NOK kr) Jamaica (NOK kr) Japan (NOK kr) Jersey (NOK kr) Jordan (NOK kr) Kazakhstan (NOK kr) Kenya (NOK kr) Kiribati (NOK kr) Kosovo (NOK kr) Kuwait (NOK kr) Kyrgyzstan (NOK kr) Laos (NOK kr) Latvia (NOK kr) Lebanon (NOK kr) Lesotho (NOK kr) Liberia (NOK kr) Libya (NOK kr) Liechtenstein (NOK kr) Lithuania (NOK kr) Luxembourg (NOK kr) Macao SAR (NOK kr) Madagascar (NOK kr) Malawi (NOK kr) Malaysia (NOK kr) Maldives (NOK kr) Mali (NOK kr) Malta (NOK kr) Martinique (NOK kr) Mauritania (NOK kr) Mauritius (NOK kr) Mayotte (NOK kr) Mexico (NOK kr) Moldova (NOK kr) Monaco (NOK kr) Mongolia (NOK kr) Montenegro (NOK kr) Montserrat (NOK kr) Morocco (NOK kr) Mozambique (NOK kr) Myanmar (Burma) (NOK kr) Namibia (NOK kr) Nauru (NOK kr) Nepal (NOK kr) Netherlands (NOK kr) New Caledonia (NOK kr) New Zealand (NOK kr) Nicaragua (NOK kr) Niger (NOK kr) Nigeria (NOK kr) Niue (NOK kr) Norfolk Island (NOK kr) North Macedonia (NOK kr) Norway (NOK kr) Oman (NOK kr) Pakistan (NOK kr) Palestinian Territories (NOK kr) Panama (NOK kr) Papua New Guinea (NOK kr) Paraguay (NOK kr) Peru (NOK kr) Philippines (NOK kr) Pitcairn Islands (NOK kr) Poland (NOK kr) Portugal (NOK kr) Qatar (NOK kr) Réunion (NOK kr) Romania (NOK kr) Russia (NOK kr) Rwanda (NOK kr) Samoa (NOK kr) San Marino (NOK kr) São Tomé & Príncipe (NOK kr) Saudi Arabia (NOK kr) Senegal (NOK kr) Serbia (NOK kr) Seychelles (NOK kr) Sierra Leone (NOK kr) Singapore (NOK kr) Sint Maarten (NOK kr) Slovakia (NOK kr) Slovenia (NOK kr) Solomon Islands (NOK kr) Somalia (NOK kr) South Africa (NOK kr) South Georgia & South Sandwich Islands (NOK kr) South Korea (NOK kr) South Sudan (NOK kr) Spain (NOK kr) Sri Lanka (NOK kr) St. Barthélemy (NOK kr) St. Helena (NOK kr) St. Kitts & Nevis (NOK kr) St. Lucia (NOK kr) St. Martin (NOK kr) St. Pierre & Miquelon (NOK kr) St. Vincent & Grenadines (NOK kr) Sudan (NOK kr) Suriname (NOK kr) Svalbard & Jan Mayen (NOK kr) Sweden (NOK kr) Switzerland (NOK kr) Taiwan (NOK kr) Tajikistan (NOK kr) Tanzania (NOK kr) Thailand (NOK kr) Timor-Leste (NOK kr) Togo (NOK kr) Tokelau (NOK kr) Tonga (NOK kr) Trinidad & Tobago (NOK kr) Tristan da Cunha (NOK kr) Tunisia (NOK kr) Türkiye (NOK kr) Turkmenistan (NOK kr) Turks & Caicos Islands (NOK kr) Tuvalu (NOK kr) U.S. Outlying Islands (NOK kr) Uganda (NOK kr) Ukraine (NOK kr) United Arab Emirates (NOK kr) United Kingdom (NOK kr) United States (NOK kr) Uruguay (NOK kr) Uzbekistan (NOK kr) Vanuatu (NOK kr) Vatican City (NOK kr) Venezuela (NOK kr) Vietnam (NOK kr) Wallis & Futuna (NOK kr) Western Sahara (NOK kr) Yemen (NOK kr) Zambia (NOK kr) Zimbabwe (NOK kr) Norsk Språk Norsk English © 2026 - Arven Utviklet av appsalon{"
  ]
}
```
## 20261115 / 984406622 / TIDEMANN BIL AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://tidemannbil.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: tidemannbil.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: tidemann-bil.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tidemannbil.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tidemann-bil.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.tidemannbil.no/; recorded rule: `None`; level: not saved.

Page: https://tidemannbil.no/ — title: Tidemann Bil AS – Bensinstasjonen med sjel

SHA-256: `cc7decc936f5ae0efc83d40e125c52185f84733b97544e9a99ebb7644180d362`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "header/logo",
    "body",
    "header",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Tidemann Bil Produkter Bildekk og dekkhotell Felger Tilhengerutleie Service og bilpleie Bilvask Samarbeidspartnere Bilder Kontakt Velg en side Tidemann Bil Tidemann Bil – Bensinstasjon & BilXtra verksted med sjel Tidemann Bil er en bensinstasjon litt utenom det vanlige. En bensinstasjon med sjel. I 1964 ble den overtatt av Ulf-Eirik Tidemanns far, og siden har den gått i arv til Ulf- Erik, som den dag i dag driver Tidemann Bil. Vi tilbyr et bredt utvalg av dekk og felger, eget verksted, bilvask i maskin, belysning, skilter, vindusviskere og forskjellige typer olje. Fom mai 2021 er vi en del av BilXtra. Vi selger også en del mat som er enkel å ta med seg og spise i bilen, som for eksempel. Diverse boller, sjokolade, hamburger, panini, salater, baguetter og andre fristende retter. På underholdningssiden har vi en god del kjøpefilmer og et bredt utvalg av forskjellige blad, magasiner og aviser. Godkjenningsbevis kjøretøyverksted Book time for verksted / service, leie av tilhenger eller leie av barnestol her: Book time Månedens deal Månedens deal er alltid et saftig kupp her hos oss. Finn ut hva som er månedens deal hos Best Sjekk ut månedens deal © 2026 Tidemann Bil AS Vi bruker informasjonskapsler for å gi deg en bedre opplevelse - les mer om personvern Utviklet av Robust Media"
  ]
}
```

Page: https://tidemannbil.no/kontakt/ — title: Kontakt – Tidemann Bil AS

SHA-256: `d5c221c880655e7426e5edae0d1d51ec0a4d72dcc556c1850cc26d6cdfbb6726`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "header/logo",
    "body",
    "header",
    "footer",
    "imprint-kontakt",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Tidemann Bil Produkter Bildekk og dekkhotell Felger Tilhengerutleie Service og bilpleie Bilvask Samarbeidspartnere Bilder Kontakt Velg en side Kontakt Kontakt Ta kontakt med oss i dag Navn E-post Melding Kontaktinformasjon Adresse : Chr. Tidemannsvei 22, 8150 Ørnes, Meløy E-post: ulftidemann@gmail.com Telefon: 75 72 10 80 Mobil : 472 50 555 Åpningstider Sommertider: Søndag – fredag: 08:00 – 20:00 Lørdag: 09.00-16:00 Vintertider: Mandag – fredag: 08.00 – 17:00 Lørdag: 10.00 – 15:00 For mer informasjon om våre tjenester, produkter eller annet, ta kontakt via vårt kontaktskjema eller ring oss på telefon for en hyggelig og uforpliktende samtale. © 2026 Tidemann Bil AS Vi bruker informasjonskapsler for å gi deg en bedre opplevelse - les mer om personvern Utviklet av Robust Media"
  ]
}
```

Page: https://tidemannbil.no/personvern/ — title: Tidemann Bil AS

SHA-256: `3f62f0e02320874d7dd3318ddce3c9733549a2273bcdd45b7f1c0e9dc1cb2492`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "header/logo",
    "body",
    "header",
    "footer",
    "imprint-kontakt",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Tidemann Bil Produkter Bildekk og dekkhotell Felger Tilhengerutleie Service og bilpleie Bilvask Samarbeidspartnere Bilder Kontakt Velg en side Personvern Vi bruker informasjonskapsler (cookies) for å gi deg en så god brukeropplevelse som mulig . Ved videre bruk av nettstedet aksepterer du at slik informasjon benyttes. På dette nettstedet logger vi anonym informasjon om alle besøkende. Vi bruker cookies hovedsakelig for trafikkmåling og optimalisering av innhold og brukeropplevelse. Denne informasjonen er anonymisert og kan ikke spores tilbake til deg som enkeltperson. Informasjonskapsler – hva det er og hvordan det fungerer Informasjonskapsler – eller cookies – er noe de aller fleste nettsider benytter seg av i dag. En informasjonskapsel er en liten tekstfil som legges i din nettlesers internminne og gjør at vi kan se hva du trykker på, hvordan du navigerer på nettsiden samt hvordan innholdet på nettsiden presterer. Videre samler vi blant annet inn informasjon om navigasjon, tid for besøk, hvilken nettleser du bruker og så videre. Dette gjør vi slik at vi best mulig kan tilpasse innholdet på nettstedet til deg som bruker. De fleste nettlesere (Google Chrome, Firefox, Internet Explorer, Safari, osv.) er stilt inn til å akseptere informasjonskapsler automatisk, men du kan selv velge å endre innstillingene slik at informasjonskapslene ikke blir akseptert. Vi gjør oppmerksom på at dette kan medføre at svært mange nettsider ikke lenger vil fungere som de skal. Hva vi bruker informasjonskapsler til Google Analytics Analyseverktøyet Google Analytics benyttes for å studere trafikk, bruksmønstre og trender på nettstedet. Dataene som samles inn brukes for å optimalisere brukeropplevelsen og tilpasse innholdet på nettsiden. I henhold til Googles retningslinjer for bruk av Google Analytics samles det ikke inn personlig identifiserbar informasjon om deg som bruker. Dataene som samles inn lagres på Googles tjenere. Dersom du vil reservere deg mot at Google Analytics samler inn data om deg kan du be om å bli ekskludert . Google Tag Manager Google Tag Manager håndterer sporingskoder og refererer til sporingsoppsett og tracking til tredjepartsløsninger som Universal Analytics (Google Analytics) og brukes til optimalisering av nettsiden og markedsføringstjenester. Alt av sporingskoder kjøres og håndteres via Google Tag Manager. Hva som lagres: Dine bevegelser og visse handlinger på nettstedet (f.eks. om du trykker på «Legg i handlekurven» i en nettbutikk). All data er anonymisert og vi lagrer ingen sensitiv informasjon som: kredittkortopplysninger, telefonnummer, adresse eller annen form for data som kan identifisere deg som person. Facebook Pixel Facebook Pixel er et analyseverktøy som lar oss måle effektiviteten av annonsering fra Facebook ved å spore handlingene brukeren utfører på nettstedet med tanke på optimalisering av Facebook Ads (bygge Audience og remarketing). Man kan bruke denne informasjonen til å: Sørge for at annonser vises til de riktige personene Bygge opp annonsepublikum Låse opp ytterligere annonseringsverktøy på Facebook Hva som lagres: Hvilke annonser brukeren har sett på Facebook, Hvilke sider brukeren har besøkt og hvilke konverteringer (bestilling, kontakt o.l.) brukeren har utført. Hotjar Kartlegger interaksjonen brukeren har med nettstedet. For å hjelpe oss å forstå hvordan besøkende samhandler med nettstedet, registrerer Hotjar besøkendes økter. Hotjar-skriptet er en websocket-tilkobling som sender følgende informasjon til Hotjar sine tjenere: HTML-endringer som skjer under brukerens økt på nettstedet Musebevegelser Museklikk Scrolle-bevegelser Tastetrykk for hvitlistede handlinger Statistikk for om visningsstørrelsen for nettleseren endres Hver hendelse som spores lagres i Hotjars sky-database ved hjelp av et tidsstempel som senere brukes til å spille av hendelsene i sekvensiell rekkefølge. Hotjar-skriptet sporer besøkende når de besøker forskjellige sider ved hjelp av en første-parti informasjonskapsel, slik at man kan spille av hele økten i et enkelt opptak. Ingen sensitiv informasjon eller brukerinformasjon hentes eller lagres. Sporingspiksler Sporingspikslene på nettstedet benyttes til sporing av konverteringer og brukertilpasset markedsføring. De er ikke containerkoder, og sender ikke tilbake personlige opplysninger. Innhenting av informasjon Vi samler inn opplysninger gjennom skjemaer på våre nettsider. Det er frivillig å oppgi denne informasjonen. Hvis du velger å ikke oppgi personopplysningene, kan vi være forhindret fra å gi deg tilgang til produktet eller tjenesten. Eksempel på skjema: Kontaktskjema Når man ønsker å prøve et produkt eller tjeneste Ved kjøp av produkter eller tjenester på en nettside Ved påmelding til webinar, kurs og konferanser Når man laster ned dokumenter som e-bøker eller annet Ved påmelding til å motta nyhetsbrev eller blogg på e-post Formålet med informasjonen som innhentes: Å gi brukeren tilgang til våre produkter og tjenester Å sende sende relevant informasjon til brukeren Å kunne ta kontakt for å tilby produkter eller tjenester Hvordan slette informasjonskapsler Normalt sett er de fleste nettlesere stilt inn til å godta informasjonskapsler. Vi gjør oppmerksom på at du kan slette disse ved å følge instruksjonene for sletting av informasjonskapsler i din nettleser. Du finner informasjonen om dette i “Hjelp”-funksjonen i nettleseren din. Vær oppmerksom på at å begrense tilgangen til informasjonskapsler kan påvirke funksjonaliteten på nettstedet. Hvis du vil fjerne informasjonskapsler ( cookies ) fra datamaskinen , kan du bruke disse veiledningene: Internet Explorer Chrome Safari Firefox © 2026 Tidemann Bil AS Vi bruker informasjonskapsler for å gi deg en bedre opplevelse - les mer om personvern Utviklet av Robust Media"
  ]
}
```
## 20261116 / 921136714 / BLACKHEART INVEST AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: blackheartinvest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: blackheart-invest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: blackheartinvest.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://blackheart-invest.com/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: blackheart-invest.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://blackheart-invest.com/; recorded rule: `None`; level: not saved.

Page: https://blackheart-invest.com/ — title: Blackheart Invest, LLC

SHA-256: `d2409bf514ca0194f2110fb21de32cd98c850519fbcfbeb32cd3c2a5cacfb445`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://blackheart-invest.com/kontakt — title: 404 Not Found

SHA-256: `b9347f234dc3c8d56e015e86d88a1400415db8f7a5ad91f02b6a2323c10a4187`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://blackheart-invest.com/om-oss — title: 404 Not Found

SHA-256: `b9347f234dc3c8d56e015e86d88a1400415db8f7a5ad91f02b6a2323c10a4187`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://blackheart-invest.com/personvern — title: 404 Not Found

SHA-256: `b9347f234dc3c8d56e015e86d88a1400415db8f7a5ad91f02b6a2323c10a4187`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://blackheart-invest.com/personvernerklaering — title: 404 Not Found

SHA-256: `b9347f234dc3c8d56e015e86d88a1400415db8f7a5ad91f02b6a2323c10a4187`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://blackheart-invest.com/kontakt-oss — title: 404 Not Found

SHA-256: `b9347f234dc3c8d56e015e86d88a1400415db8f7a5ad91f02b6a2323c10a4187`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 927835304 / PIRE AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: pire.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://pire.com/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: pire.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://pire.com/; recorded rule: `None`; level: not saved.

Page: https://pire.com/ — title: 

SHA-256: `aacb9af1ef411058dc683642e14acbba0e5cf88c4c78ade4933b34d07535b603`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pire.com/kontakt — title: 

SHA-256: `cb2e98c3794c5ea4c7a121acb0b396eb86ee3fd41261dd2e3e3bdd2fb697a0fc`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pire.com/om-oss — title: 

SHA-256: `844719027b617c2e99ba4e5b29a649398576ceef00d1c6a5cff147e92ef5844d`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pire.com/personvern — title: 

SHA-256: `e96883e437ba105b350be76febaccccbf249949bda21e5ecc0d393e92377a493`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pire.com/personvernerklaering — title: 

SHA-256: `dbfabd33884b52aa90954c8f339d9815b4877fd286891aa6ab6a38262fd17358`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pire.com/kontakt-oss — title: 

SHA-256: `2fd50fae35e1ce4183c5f3f92c3a8a5cc14d31e830c4a8ac1d015a4d2d66de5a`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 927138581 / TITANGATA 11 AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://andmork.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: andmork.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: titangata11.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: titangata-11.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: titangata11.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: titangata-11.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://andmork.no/; recorded rule: `None`; level: not saved.

Page: https://andmork.no/ — title: Transport, Frakt, Lager og Fortolling i Norge og Europa - Andersen & Mørck AS

SHA-256: `c385c0cc350e1c4fc5ad642dc33fc2b2284186905ded05a4974e2993c351af5f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://andmork.no/kontakt-oss/ — title: Kontakt oss - Andersen & Mørck AS

SHA-256: `9a8a68a7ada8a7c32936c5deb995164eb1ab9803a666b8cbbf63c025aa87d91d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "914370094"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://andmork.no/om-oss/ — title: Andersen & Mørck AS - Logistikk siden 1859

SHA-256: `c8835d8ef5978fca3b4640814b0e2db7d53608c7e281a3e4f325c81c855bf95a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://andmork.no/privacy-policy/ — title: Personvernerklæring - Andersen & Mørck AS

SHA-256: `f48963220b138c429ac794121f03901612281f63001dad5068e6861ce0417638`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "914370094"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskapsloven",
    "Regnskapsloven"
  ],
  "agency_credit_lines": []
}
```

Page: https://andmork.no/kontakt — title: Page not found - Andersen & Mørck AS

SHA-256: `9a343c084f70dfa0f35ed32855db577d6fac6553e2772620f1f05d7a87623e8b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 820529162 / I SYD AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://isyd.no/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: isyd.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: i-syd.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: isyd.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: i-syd.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: isyd.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://isyd.no/; recorded rule: `None`; level: not saved.
- Candidate: https://isyd.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://isyd.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.isyd.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://isyd.com/; recorded rule: `url_refused`; level: not saved.

Page: https://isyd.no/ — title: 
      Tilhengere og utleie på Sørlandet | iSyd
 – Tilhengere i syd AS

SHA-256: `d4a462a8b447a35f44c4ebf4ca0f396a74e92234570b5aa9fd5a3713281fa32a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "footer",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://isyd.no/pages/contact — title: 
      Contact
 – Tilhengere i syd AS

SHA-256: `40c16c35187a4452d84c8fd2126ea4e0a10bfcbb0d2657dee70337ed8801aa04`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://isyd.no/kontakt — title: 
      404 ikke funnet
 – Tilhengere i syd AS

SHA-256: `ddc406ae0396b53e6ce7ec9f841e0e98f019fe35615b680455dcf7beb9b77709`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://isyd.no/om-oss — title: 
      404 ikke funnet
 – Tilhengere i syd AS

SHA-256: `2f109fbe3c58fd0888bb50cdef0429a5ea8ebbb0deceafe92c46f420ff1aa8a1`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://isyd.no/personvern — title: 
      404 ikke funnet
 – Tilhengere i syd AS

SHA-256: `a784efa66f66d7cb6a3f87d517734263b899bee60b2ee0da64195057bb7faf70`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://isyd.no/personvernerklaering — title: 
      404 ikke funnet
 – Tilhengere i syd AS

SHA-256: `5ec78895e48f105a73d3aa89b6a4736f50450cadf44279ac66a37854dcf0950c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "og:site_name",
    "body",
    "imprint-kontakt",
    "footer",
    "header/logo"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 816273242 / TROMSØ SOSIALE ENTREPRENØRSKAP AS

Categories: veto; terminal website state: not_available.

- Candidate: fontenehuset-tromso.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: tromsoesosialeentreprenoerskap.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tromsoe-sosiale-entreprenoerskap.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tromsoesosialeentreprenoerskap.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tromsoe-sosiale-entreprenoerskap.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tromsososialeentreprenorskap.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tromsososialeentreprenorskap.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tromso-sosiale-entreprenorskap.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--troms-sosiale-entreprenrskap-u3cs.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--tromssosialeentreprenrskap-zwcq.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tromso-sosiale-entreprenorskap.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--troms-sosiale-entreprenrskap-u3cs.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://fontenehuset-tromso.no/; recorded rule: `None`; level: not saved.

Page: https://www.fontenehuset-tromso.no/ — title: Fontenehuset Tromsø

SHA-256: `80724d7fd9f384350ca6155841e0ea38db1889dd5ba973c7b7f70046257185c6`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "890240062"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "0 Hopp til innhold Hva skjer? Animasjonsfilm Helligdager Vårt tilbud Våre arbeidsenheter Vår arbeidsdag Jobb og studie Student på huset Sosialt Standardene Ofte stilte spørsmål Medlemsskap Slik fungerer det Bli medlem Finn Fontenehus Samarbeid AFT Hva er overgangsarbeid? Våre støttespillere Våre samarbeidspartnere Våre prosjekter Støtt oss Overgangsarbeidsgiver Grasrotandel Økonomiske bidrag Datterselskapet Om datterselskapet Kontakt oss Kontaktinformasjon Book introduksjon Hva skjer? Animasjonsfilm Helligdager Vårt tilbud Våre arbeidsenheter Vår arbeidsdag Jobb og studie Student på huset Sosialt Standardene Ofte stilte spørsmål Medlemsskap Slik fungerer det Bli medlem Finn Fontenehus Samarbeid AFT Hva er overgangsarbeid? Våre støttespillere Våre samarbeidspartnere Våre prosjekter Støtt oss Overgangsarbeidsgiver Grasrotandel Økonomiske bidrag Datterselskapet Om datterselskapet Kontakt oss Kontaktinformasjon Book introduksjon Mappe: Hva skjer? Tilbake Animasjonsfilm Helligdager Mappe: Vårt tilbud Tilbake Våre arbeidsenheter Vår arbeidsdag Jobb og studie Student på huset Sosialt Standardene Ofte stilte spørsmål Mappe: Medlemsskap Tilbake Slik fungerer det Bli medlem Finn Fontenehus Mappe: Samarbeid Tilbake AFT Hva er overgangsarbeid? Våre støttespillere Våre samarbeidspartnere Våre prosjekter Mappe: Støtt oss Tilbake Overgangsarbeidsgiver Grasrotandel Økonomiske bidrag Mappe: Datterselskapet Tilbake Om datterselskapet Mappe: Kontakt oss Tilbake Kontaktinformasjon Book introduksjon Arbeid for bedre psykisk helse 14. Oktober kl 10:00 - 15:10 på Det Norske Teatret Les mer Program og påmelding Fontenehuset vårt i Tromsø Fontenehuset Tromsø er et frivillig og inkluderende arbeidsfellesskap for alle som er eller har vært psykisk syk. Vi støtter hverandre ut i jobb, studier eller med andre personlige mål. Verdens nordligste Fontenehus! Fontenehuset Tromsø ligger sentralt i øvre del av sentrum. Hovedinngangen finner du i Skolegata 37. Vi har et lett og trivelig arbeidsmiljø der latter og humor sitter løst. Vi er dyktige på å inkludere, se hverandre og dra nytte av hverandres resurser. På Fontenehuset vårt har vi ingen fokus på sykdom og driver ingen form for behandling. Vis i full størrelse Les mer Hva tilbyr Fontenehuset? Vi drifter tilbudet ved å gjøre små og store oppgaver sammen – arbeid er både metode og mål. Arbeidsorientert dag Det trengs ingen henvisning eller søknad for å begynne hos oss. Det viktigste for oss er å bli kjent med deg – uten fokus på diagnose. Lavterskeltilbud Få hjelp til å finne jobb, skrive søknad, oppdatere CV eller øve til intervjuer. Vi kan også bistå med studiestøtte. Jobb- og studiestøtte Gratis og livslangt medlemskap Å være medlem på Fontenehuset koster ingenting. For medlemmer som begynner i jobb eller studier, er det alltid mulig å fortsette å bruke huset. Slik blir du medlem: 1. Omvisning Første skritt for å bli medlem er å avtale en omvisning. Du trenger ingen henvisning fra lege eller behandler. På omvisning blir du tatt godt imot. Vi forteller deg mer om hva et Fontenehus er og hvordan vi opererer. 2. Test tilbudet Etter omvisning kan du teste om tilbudet passer for deg. Her blir du bedre kjent med oss og hvordan vi jobber. Vi tar godt vare på deg, og du velger selv hvor mye du vil være med å bidra. 3. Medlemsskap Medlemskapet er gratis og uten tidsbegrensning. Fontenehuset kan brukes parallelt med jobb, studier eller andre aktiviteter. Som del av vårt fellesskap bidrar du til å skape et trygt og godt arbeidsmiljø. Bli medlem Hva skjer? Følg oss på Instagram: Fontenehuset Tromsø Følg oss på Facebook: Fontenehuset Tromsø Følg oss på Youtube: Fontenehuset Tromsø Vis full størrelse Vis full størrelse Vis full størrelse Vis full størrelse Vis full størrelse Vis full størrelse Vis full størrelse Vis full størrelse Besøksadresse Fontenehuset Tromsø Skolegata 37, 9008 Tromsø Kontakt Telefon: 947 81 619 E-post: post@fontenehuset-tromso.no Org.nr: 890 240 062 NB ikke send sensitive opplysninger på epost. Personvernerklæring Nettside levert av Gasta"
  ]
}
```
## 20261116 / 966636351 / SKÅRE BORETTSLAG I

Categories: veto; terminal website state: not_available.

- Candidate: vestbo.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: skaareborettslagi.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: skaare-borettslag-i.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: skaareborettslagi.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: skaare-borettslag-i.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: skareborettslagi.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: skareborettslagi.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: skare-borettslag-i.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--skre-borettslag-i-9qb.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--skreborettslagi-ilb.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: skare-borettslag-i.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--skre-borettslag-i-9qb.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--skreborettslagi-ilb.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.vestbo.no/; recorded rule: `None`; level: not saved.

Page: https://www.vestbo.no/ — title: 301 Moved Permanently

SHA-256: `9e17cb15dd75bbbd5dbb984eda674863c3b10ab72613cf8a39a00c3e11a8492a`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://vestbo.no/ — title: Vestbo: ditt lokale boligbyggelag på Vestlandet - Vestbo BBL

SHA-256: `33e34683a7e26c851624b81803c1ed8895d31f058d530ffa77a94505116d1f75`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "946450197"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 954687821 / GRAABEIN BORETTSLAG

Categories: fetched-without-proof, veto; terminal website state: failed.

- Candidate: usbl.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: http://graabeinborettslag.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: graabeinborettslag.no; recorded rule: `corroboration`; level: LOW.
- Candidate: graabein-borettslag.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: graabeinborettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: graabein-borettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.usbl.no/; recorded rule: `None`; level: not saved.
- Candidate: https://graabeinborettslag.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.graabeinborettslag.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://graabeinborettslag.no/; recorded rule: `None`; level: not saved.

Page: https://www.usbl.no/ — title: Boligbyggelag, forretningsfører og boligutvikler | Usbl

SHA-256: `07891fdaffea25281ac4333b2420c2e3fc916d0afdeb651a1df7d89cc5e9e5fe`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "950285680"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://graabeinborettslag.no/ — title: graabeinborettslag.no is parked

SHA-256: `5dbb41a6eb3d0ad1f56a5a9c141b3b0ccaf990bdc71bb0ef00a8cd3c4bb18e40`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://graabeinborettslag.no/kontakt — title: graabeinborettslag.no is parked

SHA-256: `c5f5b0097647deb757820f13f18e0fca7f65e9e22ad3e6739fd86d49615c79a1`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 928737225 / ALTUM HOLDING AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: altumholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: altum-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: altumholding.com; recorded rule: `corroboration`; level: LOW.
- Candidate: altum-holding.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://altumholding.com/; recorded rule: `None`; level: not saved.

Page: https://altumholding.com/ — title: altumholding.com

SHA-256: `881af8c059c4299db17ff6291e4e4df60b88623a765adcdbb0d8b0461e602f08`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://altumholding.com/kontakt — title: altumholding.com

SHA-256: `03976af5f2bb94362c3b7519b9c20ab06ae0924d5c6e65dd3be25e59eeb25616`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://altumholding.com/om-oss — title: altumholding.com

SHA-256: `03976af5f2bb94362c3b7519b9c20ab06ae0924d5c6e65dd3be25e59eeb25616`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://altumholding.com/personvern — title: altumholding.com

SHA-256: `03976af5f2bb94362c3b7519b9c20ab06ae0924d5c6e65dd3be25e59eeb25616`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://altumholding.com/personvernerklaering — title: altumholding.com

SHA-256: `03976af5f2bb94362c3b7519b9c20ab06ae0924d5c6e65dd3be25e59eeb25616`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 923748849 / TERRA HOLDING AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: terraholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: terra-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: terraholding.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: terra-holding.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: terra-holding.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://terraholding.com/; recorded rule: `None`; level: not saved.
- Candidate: https://terra-holding.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://terra-holding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.terra-holding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://terra-holding.com/; recorded rule: `url_refused`; level: not saved.

Page: https://terraholding.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://terraholding.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://terraholding.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://terraholding.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://terraholding.com/personvernerklaering — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://terraholding.com/kontakt-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://terraholding.com/om — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 832602132 / P-H INVEST AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: http://phinvest.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: phinvest.no; recorded rule: `corroboration`; level: LOW.
- Candidate: p-h-invest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: phinvest.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: p-h-invest.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: phinvest.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://phinvest.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.phinvest.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://phinvest.no/; recorded rule: `None`; level: not saved.
- Candidate: https://phinvest.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://phinvest.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.phinvest.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://phinvest.com/; recorded rule: `url_refused`; level: not saved.

Page: http://phinvest.no/ — title: phinvest.no is parked

SHA-256: `488f68aeee822b3245bc01289604bd5ba259d29a56d1e6b85e8a8ce5edb281c3`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://phinvest.no/kontakt — title: phinvest.no is parked

SHA-256: `a81c3e60a1677ab7c3b3ec3d705e4bb2b12290adac0b956d22891eeda3e5399e`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://phinvest.no/om-oss — title: phinvest.no is parked

SHA-256: `24c706c9c8a92fa2ba7d0745b566cdbd0ad7ff6e9acf8bcf871665090146bd08`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://phinvest.no/personvern — title: phinvest.no is parked

SHA-256: `07728b8210a5ad7fcfc734c360d4fcdf98490da17aea623400993b4329575969`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 965441441 / GRAFI-TEC AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://grafitec.no/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: grafitec.no; recorded rule: `corroboration`; level: LOW.
- Candidate: grafi-tec.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: grafitec.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: grafi-tec.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: grafitec.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://grafitec.no/; recorded rule: `None`; level: not saved.
- Candidate: https://grafitec.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://grafitec.com/; recorded rule: `url_refused`; level: not saved.

Page: https://grafitec.no/ — title: Grafitec.no | Grafitec.no

SHA-256: `6304a642cffe58a565efdd526340942c4ce3356f602df6939b747835c2cace4e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://grafitec.no/kontakt — title: 404 Ikke Funnet | Grafitec.no

SHA-256: `ffd0b64941265cde2f34bfeb659bc4bd150a414529b5f9b7d2a25b185406ac28`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://grafitec.no/om-oss — title: 404 Ikke Funnet | Grafitec.no

SHA-256: `ffd0b64941265cde2f34bfeb659bc4bd150a414529b5f9b7d2a25b185406ac28`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://grafitec.no/personvern — title: 404 Ikke Funnet | Grafitec.no

SHA-256: `ffd0b64941265cde2f34bfeb659bc4bd150a414529b5f9b7d2a25b185406ac28`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://grafitec.no/personvernerklaering — title: 404 Ikke Funnet | Grafitec.no

SHA-256: `4f2b2d436967e47b49c567f96368a6043b5b3b5149fb7ec1a0db46d90c9b96e7`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://grafitec.com/ — title: 302 Found

SHA-256: `745173bcc5c57ce9751dd019606e877e0aae13b60372fdb090f3db0470c3a43c`; candidate rules: url_refused, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 932390086 / EMPX AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://empx.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: empx.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: empx.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://empx.com/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: empx.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://empx.no/; recorded rule: `None`; level: not saved.
- Candidate: https://empx.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://empx.com/; recorded rule: `None`; level: not saved.

Page: https://empx.no/ — title: www.empx.no

SHA-256: `34d60636e1b69666168ad9d90320b79f32a5637d1b8ceac43f4319191793c5af`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.no/kontakt — title: 404 Not Found

SHA-256: `7bf6357846fd042fb9b92979d8c335a33e08b1f932b455500ed2f2a529199fe8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.no/om-oss — title: 404 Not Found

SHA-256: `7bf6357846fd042fb9b92979d8c335a33e08b1f932b455500ed2f2a529199fe8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.no/personvern — title: 404 Not Found

SHA-256: `7bf6357846fd042fb9b92979d8c335a33e08b1f932b455500ed2f2a529199fe8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.no/personvernerklaering — title: 404 Not Found

SHA-256: `7bf6357846fd042fb9b92979d8c335a33e08b1f932b455500ed2f2a529199fe8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.no/kontakt-oss — title: 404 Not Found

SHA-256: `7bf6357846fd042fb9b92979d8c335a33e08b1f932b455500ed2f2a529199fe8`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.com/ — title: 

SHA-256: `02e73de680c74971593acee9f8c8ab82f874c703f9eba86af670f137b006e53e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.com/kontakt — title: 

SHA-256: `d296bdb7b08e8ffca575ad2bf7a8287d0a00484e1a2b240e83aaef27365d041d`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://empx.com/om-oss — title: 

SHA-256: `b654d83906598748479fd0e1af9ef7931c646a17bb0ba87f10f25780e9da74db`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 930867306 / NELI1 AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: neli1.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://neli1.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: neli1.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://neli1.com/; recorded rule: `None`; level: not saved.

Page: https://neli1.com/ — title: 
      NELI1
    

SHA-256: `9355476cddf22fbd5496f2c39cc1c63f34111839b34a3f84db04a9ab895e44a3`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://neli1.com/pages/privacy — title: 
      Privacy – NELI1
    

SHA-256: `c0b2f7234e493aaf52b99f1e07c3f55395f256b9a4d71ae784397fe820fd3246`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://neli1.com/pages/terms-of-use — title: 
      Terms of Use – NELI1
    

SHA-256: `ac28acecd2f60ca645b06b451ee893fb6083dd749c074d7c9cbc9b8d221ff5a9`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://neli1.com/kontakt — title: 
      404 Not Found – NELI1
    

SHA-256: `873fff52c5a8dedd3f7a1c40c25cfd02b3c7fbf5b41a47badc95ddbb85309a01`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://neli1.com/om-oss — title: 
      404 Not Found – NELI1
    

SHA-256: `b5f0214de814040845127810312ba70862b001c79ab5482767715bf7cfaeca1d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://neli1.com/personvern — title: 
      404 Not Found – NELI1
    

SHA-256: `601db4f996b5808cba114ed72b53f0a1c717d09e40f6000bd88711ff5e1d408a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 933746097 / CRUST AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://crust.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: crust.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: crust.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: crust.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://crust.no/; recorded rule: `None`; level: not saved.
- Candidate: https://crust.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://crust.com/; recorded rule: `url_refused`; level: not saved.

Page: https://crust.no/ — title: Crust n' Trust

SHA-256: `12f7b8587409ef2f78dfb000c64138cfa7d70174f0ed8b1958adda6a64cc6404`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://crust.no/kontakt — title: Crust n' Trust

SHA-256: `12f7b8587409ef2f78dfb000c64138cfa7d70174f0ed8b1958adda6a64cc6404`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://crust.no/om-oss — title: Crust n' Trust

SHA-256: `12f7b8587409ef2f78dfb000c64138cfa7d70174f0ed8b1958adda6a64cc6404`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://crust.no/personvern — title: Crust n' Trust

SHA-256: `12f7b8587409ef2f78dfb000c64138cfa7d70174f0ed8b1958adda6a64cc6404`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://crust.no/personvernerklaering — title: Crust n' Trust

SHA-256: `12f7b8587409ef2f78dfb000c64138cfa7d70174f0ed8b1958adda6a64cc6404`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://crust.no/kontakt-oss — title: Crust n' Trust

SHA-256: `12f7b8587409ef2f78dfb000c64138cfa7d70174f0ed8b1958adda6a64cc6404`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 920598692 / PRESTKVÆRN NÆRINGSPARK AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: jareneiendomsutvikling.no; recorded rule: `url_refused`; level: LOW.
- Candidate: https://www.2770jaren.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: 2770jaren.no; recorded rule: `corroboration`; level: LOW.
- Candidate: prestkvaernnaeringspark.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: prestkvaern-naeringspark.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: prestkvaernnaeringspark.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: prestkvaern-naeringspark.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: prestkvarnnaringspark.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: prestkvarnnaringspark.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: prestkvarn-naringspark.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--prestkvrn-nringspark-o0be.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--prestkvrnnringspark-rxbd.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: prestkvarn-naringspark.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--prestkvrn-nringspark-o0be.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.jareneiendomsutvikling.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://jareneiendomsutvikling.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://www.jareneiendomsutvikling.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://2770jaren.no/; recorded rule: `None`; level: not saved.

Page: https://2770jaren.no/ — title: Redirecting to https://www.2770jaren.no/

SHA-256: `be09601ebf512eb43d655828d27756d68120b2d81a6f1c2c956d1f8cdb306159`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.2770jaren.no/ — title: Home Page

SHA-256: `4912e0402a7ee9039ccce55973f6a655de5e05eb54b4991f16fb4460f6d786e1`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.2770jaren.no/kontakt — title: Page not found

SHA-256: `91f072ccc2ea8b1bdaa3a7b46f089eebfb4838d6703f995a0623b0e82b3ad2d8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 815714512 / CARDINOR AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: cardinor.com; recorded rule: `registry_contact_missing`; level: MEDIUM.
- Candidate: cardinor.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://cardinor.no/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: cardinor.no; recorded rule: `corroboration`; level: LOW.
- Candidate: https://www.cardinor.com/; recorded rule: `None`; level: not saved.
- Candidate: https://cardinor.no/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://cardinor.no/; recorded rule: `None`; level: not saved.

Page: https://www.cardinor.com/ — title: Cardinor – Advancing cardiovascular risk assessment with secretoneurin

SHA-256: `4ea4433b8370d4b300192ca15fb9e5ac82aa1f4d01dfcd1f7e912d8092924e5c`; candidate rules: registry_contact_missing

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.cardinor.com/contact-us — title: Cardinor – Contact us

SHA-256: `90302b15c8997d204c6ab615438890253d29dc400cbde2566a6d12ac86a482f8`; candidate rules: registry_contact_missing

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.cardinor.com/partners — title: Cardinor – Partners

SHA-256: `4b424e0ff9033f56e638d37730759321e7983de7d7305747cd14f4da0411efed`; candidate rules: registry_contact_missing

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.cardinor.com/distributors — title: Cardinor – Distributors

SHA-256: `380115f70a2e548cb0bf565c5408740e59f5df5d820567527bcdda3a778549a2`; candidate rules: registry_contact_missing

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.cardinor.com/about-us — title: Cardinor – About us

SHA-256: `a278ca76dbd31abaa96cb391bd2ae391ab8f74ebca550ebee8fa589616f5a5ca`; candidate rules: registry_contact_missing

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.cardinor.com/kontakt — title: 

SHA-256: `0eeaa5a2e2ba2fe556b329594a87ac0b88c005a376c01bd24805ae67f66b1509`; candidate rules: registry_contact_missing

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://cardinor.no/ — title: Hosted By One.com | Webhosting made simple

SHA-256: `c33fcc4b8a202e637fa79652e2086de8a50239bdedb920e286ce63c489382deb`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://cardinor.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://cardinor.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 816322812 / HAMMERHEAD AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: hammerhead.no; recorded rule: `url_refused`; level: LOW.
- Candidate: http://hammerhead.com/about.html; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: hammerhead.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://hammerhead.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.hammerhead.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://hammerhead.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://hammerhead.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.hammerhead.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://hammerhead.com/; recorded rule: `None`; level: not saved.

Page: http://hammerhead.com/ — title: Hammerhead Productions, Inc.

SHA-256: `115ae89ab52bbe893309b311416e4db7079e2eb6d2f6a0994d342b4e788240da`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://hammerhead.com/contact.html — title: Contact

SHA-256: `09ca757e8f4f85f4e0ea6d4470bf19ceb4558265dde8e9a8303c50d712fddf1d`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 936552889 / BOXXY AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://boxxy.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: boxxy.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: boxxy.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: boxxy.com; recorded rule: `robots`; level: BLOCKED.
- Candidate: https://boxxy.no/; recorded rule: `None`; level: not saved.
- Candidate: https://boxxy.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://boxxy.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.boxxy.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://boxxy.com/; recorded rule: `robots`; level: not saved.

Page: https://boxxy.no/ — title: Boxxy – Smart containerutleie | Spar penger og miljøet

SHA-256: `49a46c187966b61907633f88fe1a307e720430c0e420200a83af87db3c68ea04`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://boxxy.no/om-oss — title: Om oss | Boxxy – Lagring i Lillestrøm

SHA-256: `11214a1e7ab8a7b1bfd7b074f96c90ebe3ea26c89c73e0c33ec2c178485b1528`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://boxxy.no/personvern — title: Personvernerklæring – Boxxy

SHA-256: `30ce60f11b9c40536f521e270b5176684c045e18d4dc0631299d7a48e611bb4f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://boxxy.no/kontakt — title: Boxxy – Smart containerutleie | Spar penger og miljøet

SHA-256: `93c7dbb7aaa3b6c8894832eda627e1e8034ccef925c7307f0ea6107820edc140`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://boxxy.no/personvernerklaering — title: Boxxy – Smart containerutleie | Spar penger og miljøet

SHA-256: `c546df176ed43a61c69485881410689ae6208458bea1dc21b689d59baaa300b6`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://boxxy.no/kontakt-oss — title: Boxxy – Smart containerutleie | Spar penger og miljøet

SHA-256: `1c1dd4a23ab884cb33a325b6f49771d4287a8712d2fee35e03489ee5065fe82c`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 998784468 / FETSUND BRYGGE FELLESORGAN

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.bori.no/om-bori/egenerklaering-om-hvitvasking/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bori.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: fetsundbryggefellesorgan.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fetsund-brygge-fellesorgan.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fetsundbryggefellesorgan.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: fetsund-brygge-fellesorgan.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.bori.no/; recorded rule: `None`; level: not saved.

Page: https://www.bori.no/ — title: Hjem - BORI BBL

SHA-256: `a7f556fcb3af94c43a8cc5996a3a8ab3505a111c1a28293f154b03006072b724`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/om-bori/kontakt-oss/ — title: Kontakt oss - BORI BBL

SHA-256: `82279d0c6ec76ffe11c8a16aee378284c20ded90c1e569154ff463097c58c81f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "regnskap"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/medlem/aktuelt/vilkarene-for-fordelsprogrammet-oppdateres/ — title: Vilkårene for fordelsprogrammet oppdateres - BORI BBL

SHA-256: `8d71e4584adc017ce25f6de9b1e3766670fd78443f3784a87c81fa9b6ce3a0b8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/personvernerklaering/ — title: Personvernerklæring - BORI BBL

SHA-256: `4aea6518339bfb78b89eebd3b27fd4cd1fa7f9d22a0ce75e433e25328bee74dc`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "konsern"
  ],
  "publisher_role_markers": [
    "regnskapsmateriale",
    "regnskapsavdelingen"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/medlem/vilkar-fordelsprogram/ — title: Vilkår fordelsprogram - BORI BBL

SHA-256: `4f669ba1f6eabe99f7dd68402353cf974b1cf02a7b024a52f8dd7a4aafe56cd8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 912188655 / MTS HOLDING AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: mtsholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: mts-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: mtsholding.com; recorded rule: `url_refused`; level: LOW.
- Candidate: http://mts-holding.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: mts-holding.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://mtsholding.com/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://mts-holding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.mts-holding.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://mts-holding.com/; recorded rule: `None`; level: not saved.

Page: http://mts-holding.com/ — title: 

SHA-256: `d31b4ed65b3ec41988e0db354902d6939b9231ddc141ec8401f02f5901c604ae`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://mts-holding.com/kontakt — title: 
   Error 404 - Not found
  

SHA-256: `e3a1783fe697f2b13807e497d9f91dcf017c479031d9b49bbc47a5ae546974a6`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 920881548 / DALYPE ART INT AS

Categories: veto; terminal website state: not_available.

- Candidate: dalypeartint.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: dalype-art-int.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: dalypeartint.com; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: dalype-art-int.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://dalypeartint.com/; recorded rule: `None`; level: not saved.

Page: https://dalypeartint.com/ — title: EDVARD MUNCH GALLERIET

SHA-256: `7fb8bf04981567cb1a13697562930f1095ba34ee02ce5eff2d6a8a96f70a811e`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dalypeartint.com/kontakt.html — title: EDVARD MUNCH GALLERIET

SHA-256: `38d12e31e1315376f0300be36e4896c9d8a248722fb9d22333b5189abaff4339`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "952490591"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 919543604 / HIGHLAND LODGE AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://highland.no/privacy-policy/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: highland.no; recorded rule: `registry_and_live_corroboration`; level: REGISTRY_DECLARED.
- Candidate: highlandlodge.no; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: highland-lodge.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.highlandlodge.no/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: highlandlodge.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: https://www.highland.no/; recorded rule: `None`; level: not saved.
- Candidate: https://highlandlodge.no/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://highlandlodge.no/; recorded rule: `None`; level: not saved.

Page: https://highland.no/ — title: Forside - Highland

SHA-256: `be72d71e0122830107fbe26817498882d700b8c4c5058d80bfd32fd245e8ae8e`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://highland.no/personvernerklaering/ — title: Personvernerklæring - Highland

SHA-256: `26ad2be4d6086f1f29df25a73bba46075f3e2f8d76d4dc3f1e40f65a2171e3ad`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.highlandlodge.no/ — title: HII

SHA-256: `0e22c8dc0fb15fc5d3b7097f4e1b55695efd537e77c96915f7c0cab72eb0f0dd`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.highlandlodge.no/kontakt — title: Kontakt — HII

SHA-256: `b20482d45665db13263ff9b4f67a29b8dc4cb0bb56f8d47ce4a85dc106b7e3d8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 984177070 / KRAABOL AS

Categories: ambiguous; terminal website state: ambiguous.

- Candidate: https://www.kraabol-as.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kraabol-as.com; recorded rule: `registry_contact_missing`; level: MEDIUM.
- Candidate: kraabol.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: kraabol.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kraabol.com; recorded rule: `website_http_5xx`; level: LOW.
- Candidate: https://www.kraabol-as.com/; recorded rule: `None`; level: not saved.
- Candidate: https://www.kraabol.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://www.kraabol.com/; recorded rule: `website_http_5xx`; level: not saved.

Page: https://www.kraabol-as.com/robots.txt/ — title: Kraabol AS – We provide a professional and global network to support your business needs.

SHA-256: `d0ca226d1aac015d81b45af02ac16f794ecdb487435d750f6b692c5806e91c25`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kraabol-as.com/ — title: Kraabol AS – We provide a professional and global network to support your business needs.

SHA-256: `7e784d32ad9c60476509f58f43d64dbad95113b8856177c223e3a74f81cb36e2`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kraabol-as.com/sitemap.xml/ — title: Kraabol AS – We provide a professional and global network to support your business needs.

SHA-256: `d0ca226d1aac015d81b45af02ac16f794ecdb487435d750f6b692c5806e91c25`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.kraabol-as.com/kontakt/ — title: Kraabol AS – We provide a professional and global network to support your business needs.

SHA-256: `d0ca226d1aac015d81b45af02ac16f794ecdb487435d750f6b692c5806e91c25`; candidate rules: registry_contact_missing, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "header",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 983387675 / CEST AS

Categories: veto; terminal website state: not_available.

- Candidate: cest.no; recorded rule: `url_refused`; level: LOW.
- Candidate: cest.com; recorded rule: `parked`; level: REJECT.
- Candidate: https://cest.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.cest.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://cest.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://cest.com/; recorded rule: `None`; level: not saved.

Page: https://cest.com/ — title: Domain For Sale

SHA-256: `3c4ab4cc8ad4500b744f2c2b6553996b709dd2d1227904532129008255c0a441`; candidate rules: parked

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 926924672 / PURE PERFORMANCE AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://pureperformance.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: pureperformance.no; recorded rule: `corroboration`; level: LOW.
- Candidate: pure-performance.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: pureperformance.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://www.pure-performance.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: pure-performance.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://pureperformance.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.pureperformance.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://pureperformance.no/; recorded rule: `None`; level: not saved.
- Candidate: https://pureperformance.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://pure-performance.com/; recorded rule: `None`; level: not saved.

Page: http://pureperformance.no/ — title: pureperformance.no is parked

SHA-256: `c56bb9e72485f47832d94044e2c51f482c4ff705d6cbd13b2e584a4db94aec73`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://pureperformance.no/kontakt — title: pureperformance.no is parked

SHA-256: `a1a3fffc8584a8afb3044d140bb05ea0390c35267df13e7ec207fb55b6e5f440`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://pureperformance.no/om-oss — title: pureperformance.no is parked

SHA-256: `38d13c6b606446ef2c1a6559a01d2fbcfc3a96ebf530031a3727a63ff17f4a5c`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://pureperformance.no/personvern — title: pureperformance.no is parked

SHA-256: `01b16213c496ab42540ad895e0354b188c2f7f2875e20e3baded1cf0061943e4`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://pure-performance.com/ — title: 301 Moved Permanently

SHA-256: `87a9323ac85ce28867d5d7ce590c8f29b8d1a999961fca71bb33adef48683691`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.pure-performance.com/ — title: Leadership Communication Coaching | Pure Performance Communications

SHA-256: `79667e0d567da170053ca693017c7e6fcadd477fa05362cf86cc0c2ca9caad58`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.pure-performance.com/kontakt — title: 404 - Page not found

SHA-256: `90c032f35272ba1a7aa93027ab635e6610d4f24cf9e53c0624d00f065d7c7e7d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 983803075 / MELTWATER NEWS AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://www.meltwater.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: meltwater.com; recorded rule: `corroboration`; level: LOW.
- Candidate: meltwaternews.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwater-news.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwaternews.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: meltwater-news.com; recorded rule: `robots_unavailable`; level: BLOCKED.
- Candidate: meltwaternews.com; recorded rule: `url_refused`; level: LOW.
- Candidate: meltwater-news-as-avd-oslo-support.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwater-news-as-avd-oslo.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwaternewsasavdoslo.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwaternewsasavdoslosupport.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwater-news-as-avd-oslo-support.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwater-news-as-avd-oslo.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwaternewsasavdoslo.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: meltwaternewsasavdoslosupport.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.meltwater.com/; recorded rule: `None`; level: not saved.
- Candidate: https://meltwaternews.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://meltwater-news.com/; recorded rule: `robots_unavailable`; level: not saved.
- Candidate: https://meltwaternews.com/; recorded rule: `url_refused`; level: not saved.

Page: https://www.meltwater.com/ — title: 

SHA-256: `15befc14b4d6818e36237b6fd5b091a8af78374e8edae42e131f85fbd2a32d10`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.meltwater.com/en — title: Meltwater: Media Intelligence, Social Listening, AI Tracking

SHA-256: `9957b3262162aa342364d485539d989f462db16460dbd74f5ed138b3112771a8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.meltwater.com/en/about/contact-us — title: Contact Meltwater | Global Media Intelligence Experts

SHA-256: `d76b27b49d1d7b4da1c95848ea0cb4acb5b92afd36be5b23404b1a62dd9f39c7`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.meltwater.com/en/resources/own-brand-visibility-ai — title: Free Guide: Own Your Brand’s Visibility in AI

SHA-256: `050ccdf6340a1b46be77da1c7a1094c5c2f9d8edf2dbb404f23afb8591b4cb08`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.meltwater.com/en/privacy — title: Meltwater Privacy

SHA-256: `43af08933cb96b239aefb9465e3ebd273e926649265cdbf1420266080336e5b5`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.meltwater.com/kontakt — title: 

SHA-256: `184887d71aefc6142dd1a2558f1fa870c9c3a5d3d96a145d92571da9671fa984`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 997831977 / LOSBYVEIEN LEGESENTER AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://losbyveienlegesenter.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: losbyveienlegesenter.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: losbyveien-legesenter.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: losbyveienlegesenter.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: losbyveien-legesenter.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://losbyveienlegesenter.no/; recorded rule: `None`; level: not saved.

Page: https://losbyveienlegesenter.no/ — title: LOSBYVEIEN LEGESENTER | HelseRespons

SHA-256: `0df91eb916c1f1cd8347004da2d7f64a47b9e15688618258d666b67e211ddf58`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://losbyveienlegesenter.no/kontakt — title: 302 Found

SHA-256: `11d5aa15bfa78de934ada2379211d0227c2a70d4aeea940a42a9ef8677a7bf39`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://losbyveienlegesenter.no/kontakt/ — title: 301 Moved Permanently

SHA-256: `66a4c37663e2e400eda64990fc3119d2519946201310c7f0acb82784e8b60ef1`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://losbyveienlegesenter.no/kontakt/ — title: LOSBYVEIEN LEGESENTER | HelseRespons

SHA-256: `ceb531d4e4caa3f3bdafbca3536a73d8056751b2813a3a60344a7aaf8f6d0052`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 985615691 / GIGAFIB HOLDING AS

Categories: ambiguous; terminal website state: ambiguous.

- Candidate: https://www.gigafib.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: gigafib.no; recorded rule: `registry_and_live_corroboration`; level: REGISTRY_DECLARED.
- Candidate: gigafibholding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gigafib-holding.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gigafibholding.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: gigafib-holding.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.gigafib.no/; recorded rule: `None`; level: not saved.

Page: https://www.gigafib.no/ — title: Gigafib - Ditt lokale bredbåndselskap

SHA-256: `06ae675e3bd4ed93da6179c742a469c1f69ccb717a122fb1b03d19059af7a3de`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Til innhold Forside Driftsmeldinger Kontakt Om Gigafib MinSide Privat Trådløst bredbånd privat Fiber bredbånd privat Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Meny Privat Trådløst bredbånd privat Fiber bredbånd privat Fiber bredbånd privat Trådløst bredbånd privat Telia Play-førsteklasses underholdning Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Driftsmeldinger Kontakt Om Gigafib MinSide Kortreist og raskt internett Vi leverer et stabilt og raskt internett til bedrifter, offentlige og privatpersoner i Vestfold via vårt radio- og fibernett. Se om du kan få bredbånd fra Gigafib! Privat Bedrift Borettslag Ønsker du lynraskt nett til ditt borettslag, vel eller sameie? Industriområder Vi prosjekterer fiber til nye og eksisterende næringsområder. Næringsbygg Har dine leietakere godt nok nett til å bli værende over tid? Offentlig Vi tilbyr skreddersydde og velprøvde løsninger for det offentlige. Fiberbredbånd Lynraskt fiberbredbånd, hyggelig kundeservice og ansatte som bryr seg er hva du får som kunde hos Gigafib. At vi holder til rett borti gata og er raskt på pletten er jo heller ingen ulempe. Fiber Trådløst bredbånd Vi kan levere bredbånd der andre ikke kan! Der fiber ikke er tilgjengelig, eller for kostbart, kan vi levere et raskt og stabilt trådløst bredbånd fra våre basestasjoner. Vi har over 20 års erfaring med trådløst bredbånd i Vestfold og storfornøyde kunder. Trådløst Telia Play Telia Play er en moderne TV-tjeneste med frihet til å se TV slik du vil. Med Telia Play får du tilgang til populære strømmetjenester og kanaler. Alt samlet i ett abonnement og på ett sted. Telia Play Nytt hos Gigafib Prisjustering på fiber fra 1.april Den 1.april 2026 gjennomfører vi en prisjustering på våre fiberabonnement. Vi fornyer hele vår trådløse infrastruktur I månedene fremover vil utføre en full utskifting av alle basestasjoner og kundeantenner. Dette vil resultere i mulighet for vesentlig raskere hastigheter, og enda bedre oppetid på ditt bredbånd. Vi har blitt sertifisert Miljøfyrtårn Vi fikk storfint besøk av ordføreren i Tønsberg som kunne overrekke det synlige beviset på at vi nå har blitt sertifisert Miløfyrtårn. Flere nyheter Logo Kontakt oss Gigafib Bredbånd AS Wirgenes vei 8B 3157 Barkåker Telefon: 33 05 04 60 E-post: kundeservice@gigafib.no Meny Bredbånd for private Bredbånd for bedrifter Kontakt oss Webmail H-nett Sosiale medier Facebook Personvern og informasjonskapsler Levert av: Consilio Kommunikasjon og CoreTrek AS"
  ]
}
```

Page: https://www.gigafib.no/kontakt-oss/ — title: Kontakt oss - Gigafib

SHA-256: `3d17e17f5e3b270e93e79e7b0a2b17d1c00cfd5e5309caaf99c7fde9a7d070bf`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Til innhold Kontakt oss Driftsmeldinger Kontakt Om Gigafib MinSide Privat Trådløst bredbånd privat Fiber bredbånd privat Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Meny Privat Trådløst bredbånd privat Fiber bredbånd privat Fiber bredbånd privat Trådløst bredbånd privat Telia Play-førsteklasses underholdning Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Driftsmeldinger Kontakt Om Gigafib MinSide Hjem Kontakt oss Kontakt oss Har du spørsmål om oss, våre produkter, fiber eller trådløst, eller kanskje allerede er kunde? Ta kontakt, så hjelper vi deg. Den raskeste måten å kontakte oss på er via vår chat som du finner nederst i høyre hjørnet. Den kan benyttes hele døgnet. Telefontid Kundeservice Hverdager 10.00-16.00 (Fredag 12.00-16.00) Telefon: 33 05 04 60 kundeservice@gigafib.no Her finner du oss Kontaktskjema generelle henvendelser Fornavn (Påkrevd) Etternavn (Påkrevd) E-post (Påkrevd) Mobilnummer Hvilken avdeling? Administrasjon Økonomi Emne (Påkrevd) Melding (Påkrevd) Ønsker du å kontakte våre ansatte? Klikk deg inn på vår ansatt-side . Del på: Logo Kontakt oss Gigafib Bredbånd AS Wirgenes vei 8B 3157 Barkåker Telefon: 33 05 04 60 E-post: kundeservice@gigafib.no Meny Bredbånd for private Bredbånd for bedrifter Kontakt oss Webmail H-nett Sosiale medier Facebook Personvern og informasjonskapsler Levert av: Consilio Kommunikasjon og CoreTrek AS"
  ]
}
```

Page: https://www.gigafib.no/personvern-og-informasjonskapsler/ — title: Personvern og informasjonskapsler - Gigafib

SHA-256: `3d38f4ab3f30af50290298a106840f538723ca7188f7d7f17f364619a0b0970a`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [
    "Holding",
    "Holding",
    "Holding",
    "Holding",
    "Holding",
    "Holding",
    "Holding",
    "Holding",
    "Holding",
    "Holding"
  ],
  "publisher_role_markers": [
    "regnskap"
  ],
  "agency_credit_lines": [
    "Til innhold Personvern og informasjonskapsler Driftsmeldinger Kontakt Om Gigafib MinSide Privat Trådløst bredbånd privat Fiber bredbånd privat Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Meny Privat Trådløst bredbånd privat Fiber bredbånd privat Fiber bredbånd privat Trådløst bredbånd privat Telia Play-førsteklasses underholdning Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Driftsmeldinger Kontakt Om Gigafib MinSide Hjem Personvern og informasjonskapsler Personvern og informasjonskapsler Hos Gigafib Holding AS er vi forpliktet til å beskytte og respektere personvernet ditt. Vi jobber hardt for å følge det regelverk om personvern som til enhver tid er gjeldende. Samtidig er deler av regelverket åpen for tolkninger og «beste måter» å følge regelverket er ikke tydelige nok enda pr oktober 2018. Endringer på denne siden kan m.a.o. komme. Når samler vi inn informasjon om deg? Det meste vi har av data om deg er data du selv gir oss når du bruker nettstedet vårt, f.eks. når du kontakter oss om produkter og tjenester. Hvilken type informasjon samles? Personopplysningene vi samler inn er data du selv oppgir når du kontakter oss per e-post eller telefon. Det kan inkludere navn, adresse, e-postadresse, telefonnummer. Oppgir du annen informasjon til oss når du kommuniserer med oss, kan også disse bli lagret. Hvordan brukes informasjonen din? Vi bruker informasjonen for å ha et forretningsmessig forhold til deg som kunde: Er du eksisterende kunde, så bruker vi informasjonen for å gi deg support eller tilby deg andre relevante produkter og tjenester Er du en mulig kunde, bruker vi informasjon for å kommunisere med deg videre om våre produkter og tjenester Gjelder forespørselen noe annet, bruker vi informasjonen for å besvare din forespørsel Oppbevaring av informasjon Vi er juridisk pålagt å lagre visse typer opplysninger for å oppfylle våre lovbestemte forpliktelser (f.eks. i forhold til regnskap og de arrangører vi holder eventer for). Vi vil holde dine personlige opplysninger i våre systemer så lenge det er nødvendig for den aktuelle aktiviteten, eller så lenge det er angitt i en relevant kontrakt du har med oss. Hvem har tilgang til informasjonen din? Det er ansatte i Gigafib Holding AS som har tilgang til informasjonen. Vi verken selger eller leier informasjonen din til tredjepart. Hvordan du kan få tilgang til og oppdatere informasjonen din Nøyaktigheten av dine opplysninger er viktig for oss. Ønsker du utfyllende informasjon om eventuelle data vi har lagret om deg, vennligst send oss ​​en e-post på post@gigafib.no . Eventuelt send oss post til vår fysiske adresse. Alternativt kan du ringe oss. Du har rett til å be om en kopi av informasjonen Gigafib Holding AS har lagret om deg. Sikkerhetsregler for å beskytte informasjonen din Når du gir oss personlig informasjon, tar vi tiltak for å sikre at den behandles sikkert. All informasjon som sendes via vårt nettsted er beskyttet med SSL. Når vi mottar informasjonen din, sikrer vi den ihht. gjeldende personvernregler. Behandlingsansvarlig og databehandler Gigafib Holding AS er behandlingsansvarlig for personopplysninger som behandles i forbindelse med bruk av våre nettsider. At Gigafib Holding AS er behandlingsansvarlig innebærer at det er Gigafib Holding AS som har ansvar og plikter etter personopplysningsloven. Et selskap som behandler data på vegne av Gigafib Holding AS, kalles en databehandler. Gigafib benytter databehandleravtaler til å regulere hvordan en databehandler kan behandle data som databehandler har tilgang på. Generelt regulerer en slik avtale at databehandleren kun får behandle personopplysningene på Gigafib Holding AS sine vegne og kun til tydelig definerte formål. Tredjepartsverktøy Gigafib Holding AS bruker følgende tredjepartsverktøy på vårt nettsted: WordPress – publiseringssystemet som driver nettstedet Google Analytics – nettstedsmåling, her har vi slått på anonymiseringsfunksjonen I noen tilfeller må vi sende din informasjon til våre tredjepartsverktøy, men kun for å fullføre oppgaver og tilby tjenester til deg på våre vegne – og vi sender kun den informasjonen som er nødvendig. Bruk av «cookies» På samme måte som mange andre nettsteder, bruker også Gigafib Holding AS sitt nettsted cookies. En cookie er en liten tekstfil som lagres på enheten din av nettsteder du besøker. De samler data om dine surfevaner, men identifiserer deg ikke som et individ. Dette hjelper oss med å forbedre nettstedet vårt og vise relevant markedsføring. Dersom du ikke vil akseptere vår bruk av cookies, kan du fjerne cookiene som blir lagret på din PC, via nettleseren din. Dette kan medføre at tjenestene på våre nettsider ikke fungerer optimalt. Vi har laget en egen side med ytterligere informasjon om cookies . Denne siden inneholder også en oppdatert liste over de cookies som brukes på www.gigafib.no, samt hvordan du kan slette cookies. 16 år eller yngre Vi er ekstra opptatt av å beskytte personvernet til barn i alderen 16 eller yngre. Hvis du er 16 år eller yngre, vennligst ta kontakt med foreldre / foresatte på forhånd før du gir oss personlig informasjon. Som opplyst innledningsvis, så kan vi endre disse reglene fra tid til annen. Gjeldende lover og personvern praksis forandres over tid. Hold deg derfor regelmessig oppdatert på våre personvernregler for å sikre at du er fornøyd med eventuelle endringer som har blitt gjort. Ved å bruke nettstedet vårt, godtar du disse reglene. Eventuelle spørsmål kan sendes til post@gigafib.no eller send oss post til vår fysiske adresse. Alternativt kan du ringe oss. Sist oppdatert: mars 2019. Del på: Logo Kontakt oss Gigafib Bredbånd AS Wirgenes vei 8B 3157 Barkåker Telefon: 33 05 04 60 E-post: kundeservice@gigafib.no Meny Bredbånd for private Bredbånd for bedrifter Kontakt oss Webmail H-nett Sosiale medier Facebook Personvern og informasjonskapsler Levert av: Consilio Kommunikasjon og CoreTrek AS"
  ]
}
```

Page: https://www.gigafib.no/kontakt-oss/ — title: Kontakt oss - Gigafib

SHA-256: `3d17e17f5e3b270e93e79e7b0a2b17d1c00cfd5e5309caaf99c7fde9a7d070bf`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": [
    "Til innhold Kontakt oss Driftsmeldinger Kontakt Om Gigafib MinSide Privat Trådløst bredbånd privat Fiber bredbånd privat Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Meny Privat Trådløst bredbånd privat Fiber bredbånd privat Fiber bredbånd privat Trådløst bredbånd privat Telia Play-førsteklasses underholdning Bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Trådløst bredbånd bedrift Fiber bredbånd bedrift Offentlig Nettbutikk Driftsmeldinger Kontakt Om Gigafib MinSide Hjem Kontakt oss Kontakt oss Har du spørsmål om oss, våre produkter, fiber eller trådløst, eller kanskje allerede er kunde? Ta kontakt, så hjelper vi deg. Den raskeste måten å kontakte oss på er via vår chat som du finner nederst i høyre hjørnet. Den kan benyttes hele døgnet. Telefontid Kundeservice Hverdager 10.00-16.00 (Fredag 12.00-16.00) Telefon: 33 05 04 60 kundeservice@gigafib.no Her finner du oss Kontaktskjema generelle henvendelser Fornavn (Påkrevd) Etternavn (Påkrevd) E-post (Påkrevd) Mobilnummer Hvilken avdeling? Administrasjon Økonomi Emne (Påkrevd) Melding (Påkrevd) Ønsker du å kontakte våre ansatte? Klikk deg inn på vår ansatt-side . Del på: Logo Kontakt oss Gigafib Bredbånd AS Wirgenes vei 8B 3157 Barkåker Telefon: 33 05 04 60 E-post: kundeservice@gigafib.no Meny Bredbånd for private Bredbånd for bedrifter Kontakt oss Webmail H-nett Sosiale medier Facebook Personvern og informasjonskapsler Levert av: Consilio Kommunikasjon og CoreTrek AS"
  ]
}
```
## 20261116 / 926312537 / PROPR AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://propr.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: propr.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: propr.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: propr.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://propr.no/; recorded rule: `None`; level: not saved.
- Candidate: https://propr.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://propr.com/; recorded rule: `None`; level: not saved.

Page: https://propr.no/ — title: 

SHA-256: `c2c239f9ca0d1a318434eb4bd373e2f0c93188237ff755dfb8d72b7515040548`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://propr.no/om-oss — title: 

SHA-256: `e96b3b189a75639ea06abb51ab942c380b8822d9eac049499a7d57833fdf296f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://propr.no/vilk%C3%A5r/personvern — title: 

SHA-256: `5ea9f06a8ca3df1d17de53d7abca13ef427a83d44a13f5be5beab1089f6b6e5f`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://propr.no/vilk%C3%A5r — title: Vilkår - Propr

SHA-256: `64c7a85d92e409548571937ec6cbff3c4f3c7ef94fd2a2466dc9b8cd84fcd866`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://propr.no/personvern — title: 

SHA-256: `25d47076c33345a1803271bf07e4f1745e9a986a29877d18b7cea8ee91159798`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://propr.no/kontakt — title: 

SHA-256: `2c58b044bea819a982290e0336bf10523713f87b5b42a7e814a86b027964bb80`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://propr.com/ — title: PropR.com is for sale - Premium  Domain

SHA-256: `8c22828ba83edf98b819c3bf7ab1484b9c1296bd224fec61574ea8348a325a31`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://propr.com/kontakt — title: 404 Not Found

SHA-256: `e38e0cee2c2996a92b17cd2a648120c322ea4d33d62adb2823b0a1f9ffe21ab2`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 930086533 / YUGEN AS

Categories: veto; terminal website state: not_available.

- Candidate: yugen.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: yugen.com; recorded rule: `dns_unavailable`; level: LOW.
- Candidate: https://yugen.no/; recorded rule: `None`; level: not saved.

Page: https://www.yugen.no/ — title: Samlekort, Figurer og Blindbokser | Yugen Collectibles

SHA-256: `bfd9ecae5f31b6c98583e68201c7513a9ededbc33b6712950667f453ec842ded`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "838683932"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 930807206 / AKELEIE AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: akeleie.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://akeleie.com/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: akeleie.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://akeleie.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.akeleie.com/; recorded rule: `no_such_domain`; level: not saved.
- Candidate: http://akeleie.com/; recorded rule: `None`; level: not saved.

Page: http://akeleie.com/ — title: No Index

SHA-256: `cd15fd5fdb73b356a4ee7d879cb387dc543c22edce4c8cb95d5ccf9e0664c86c`; candidate rules: corroboration, no_such_domain, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://akeleie.com/kontakt — title: 404

SHA-256: `4380dccef55f2333d94d3418ab8cf6f3bd33089c1b76b3fab6833984cd515881`; candidate rules: corroboration, no_such_domain, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://akeleie.com/om-oss — title: 404

SHA-256: `4380dccef55f2333d94d3418ab8cf6f3bd33089c1b76b3fab6833984cd515881`; candidate rules: corroboration, no_such_domain, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://akeleie.com/personvern — title: 404

SHA-256: `4380dccef55f2333d94d3418ab8cf6f3bd33089c1b76b3fab6833984cd515881`; candidate rules: corroboration, no_such_domain, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://akeleie.com/personvernerklaering — title: 404

SHA-256: `4380dccef55f2333d94d3418ab8cf6f3bd33089c1b76b3fab6833984cd515881`; candidate rules: corroboration, no_such_domain, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261116 / 995135086 / CRAFTING HOUSE AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://craftinghouse.no/om-oss/hva-vi-gjor/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: craftinghouse.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: crafting-house.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: craftinghouse.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: crafting-house.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: craftinghouse.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://www.craftinghouse.no/; recorded rule: `None`; level: not saved.
- Candidate: https://craftinghouse.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://craftinghouse.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.craftinghouse.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://craftinghouse.com/; recorded rule: `url_refused`; level: not saved.

Page: https://craftinghouse.no/ — title: Crafting House – Samskaper med ledere som beveger samfunn

SHA-256: `5089733488a7869f90bd42c26903e5ecfec5d7e5ffe04032945073fdd590f80f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://craftinghouse.no/kontakt-oss/ — title: Kontakt oss – Crafting House

SHA-256: `cbe292eb7892945b38bada0e30f99acf6d25030a2bc66647564180968723b557`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://craftinghouse.no/om-oss/ — title: Om oss – Crafting House

SHA-256: `d39dea19e157e142d3eb15441fa4c41b4cd39116e425475bac692bfc12785dee`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 920440045 / LAMELLA AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://lamella.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: lamella.no; recorded rule: `corroboration`; level: LOW.
- Candidate: lamella.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: http://lamella.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: lamella.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://lamella.no/; recorded rule: `None`; level: not saved.
- Candidate: https://lamella.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://lamella.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.lamella.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://lamella.com/; recorded rule: `None`; level: not saved.

Page: https://lamella.no/ — title: LAMELLA | Iskrem & Sorbet

SHA-256: `a92ddc071cce6ce0f723ca619e979531f525e7c5be2dfdddc895c5a035948ef8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://lamella.no/kontakt/ — title: KONTAKT | LAMELLA

SHA-256: `8739015a3874cc3e8159c7721620f2c4a1c61173a9ae13fc32b7b3881517e90b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://lamella.no/om-oss/ — title: OM OSS | LAMELLA

SHA-256: `e21e993bf49d964f840e9eb80a7c877b5c416bae8ce114772854fc14a10c259a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://lamella.no/personvern-og-cookies/ — title: PERSONVERN OG COOKIES | LAMELLA

SHA-256: `cac79adeb619cc7046c38e3f8e98ef0aa2c455ca012c64aebc962578aa0bc17f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://lamella.com/ — title: Domain im Kundenauftrag registriert

SHA-256: `50900200d53b6415b014951ed6fbf53a011cb399091291018eed8ad15fa87d05`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://lamella.com/kontakt — title: Domain im Kundenauftrag registriert

SHA-256: `50900200d53b6415b014951ed6fbf53a011cb399091291018eed8ad15fa87d05`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 921187297 / KIZU AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: http://kizu.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kizu.no; recorded rule: `corroboration`; level: LOW.
- Candidate: kizu.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: kizu.com; recorded rule: `robots`; level: BLOCKED.
- Candidate: https://kizu.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.kizu.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://kizu.no/; recorded rule: `None`; level: not saved.
- Candidate: https://kizu.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://kizu.com/; recorded rule: `robots`; level: not saved.

Page: http://kizu.no/ — title: kizu.no is not set up yet

SHA-256: `8edcbdf302e5a22a29759ad674424919e5be68edaf29a2c97cd2af4289b9ee1c`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://kizu.no/kontakt — title: 404 Not Found

SHA-256: `ee1a27178227546d3dcc49e611a6d72e4f1c30080ee4493ae4085b58a49e28e6`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://kizu.no/om-oss — title: 404 Not Found

SHA-256: `ee1a27178227546d3dcc49e611a6d72e4f1c30080ee4493ae4085b58a49e28e6`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://kizu.no/personvern — title: 404 Not Found

SHA-256: `ee1a27178227546d3dcc49e611a6d72e4f1c30080ee4493ae4085b58a49e28e6`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 928106977 / SUBFARM AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: subfarm.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: subfarm.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: subfarm.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://subfarm.no/; recorded rule: `None`; level: not saved.
- Candidate: https://subfarm.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://subfarm.com/; recorded rule: `url_refused`; level: not saved.

Page: https://subfarm.no/ — title: SubFarm – Submersible Aquaculture Cage System

SHA-256: `ecf91c4e4f822cddc76e6a75dd9c586285ff03527e3ee66a767efa7058e8ce57`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://subfarm.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://subfarm.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://subfarm.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://subfarm.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://subfarm.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 928155501 / ARTIST AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: artist.no; recorded rule: `url_refused`; level: LOW.
- Candidate: https://artist.com/terms/; recorded rule: `website_connect_error`; level: LOW.
- Candidate: https://artist.com/kontakt; recorded rule: `website_timeout`; level: LOW.
- Candidate: https://artist.com/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: artist.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://artist.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://artist.com/; recorded rule: `None`; level: not saved.

Page: https://artist.com/ — title: Artist.com -  Buy Fine Art Online, Original / Print Artwork From Trusted Name in Online Art Sales, Featuring Artists Around the World

SHA-256: `a1d42adb5f29e71cd388669e34c2d4e0630653a8e13761e8cec710e7ffa6058b`; candidate rules: corroboration, website_budget_exhausted, website_connect_error, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://artist.com/contact/ — title: Contact | Online Fine Art, Paintings, Photography, Drawings, Sketches, Sculpture, Digital Art, Abstract - Artist.com

SHA-256: `de5a02e99c9a25827122b7e0f44ff35e6aae8f041a29076cb7c01f1d553f15c8`; candidate rules: corroboration, website_budget_exhausted, website_connect_error, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://artist.com/about/ — title: About - Artist.com

SHA-256: `c8ff05dfb75e9023e264c7de9748a152b7bd313596eb005f19fb104608dbfba1`; candidate rules: corroboration, website_budget_exhausted, website_connect_error, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://artist.com/privacy/ — title: Privacy Policy | Artist.com - Online Art Gallery | Find Art Pieces | Paintings for Sale - Artist.com

SHA-256: `2e095500707dbdc4a83ee13931d86255b07af47b6b07d593d34430a5b7a2d3f2`; candidate rules: corroboration, website_budget_exhausted, website_connect_error, website_timeout

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 933709329 / RINO HANSEN AS

Categories: veto; terminal website state: not_available.

- Candidate: rinohansen.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: rino-hansen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rinohansen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: rino-hansen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://rinohansen.no/; recorded rule: `None`; level: not saved.

Page: https://rinohansen.no/ — title: Hjem - Rino Hansen

SHA-256: `5b65eefb57fdbc068720ba16b35ba2eafc40ed72db1d1950cea90750cef9f205`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://rinohansen.no/personvern/ — title: Personvern - Rino Hansen

SHA-256: `1b3755ed4a23d3717cf1ac5671893ad72bcf3f995914ae7fbb90319d148b6c10`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "regnskapsmessige",
    "regnskapsmessige"
  ],
  "agency_credit_lines": [
    "Skip to the content Gratis frakt på ordre over 1500kr Dame Dame Hurtiglenker Siste nytt Populære produkter Alle Dameprodukter Klær Blazer Bluser & Skjorter Bukser & Shorts Genser & Hoodies Jakker & Frakker Jeans Kjoler Skjørt T-Skjorter & Topper Tilbehør Smykker Herre Herre Hurtiglenker Siste nytt Populære produkter Alle Herreprodukter Klær Bukser Dress Genser Jakker Jeans Shorts Skjorter T-Skjorter & Pique Tilbehør Skjerf & Hodeplagg Undertøy & Sokker Bli Medlem Personlig serivce Sporing Rask levering Fredrikstad | Norway Dame Hurtiglenker Siste nytt Populære produkter Alle Dameprodukter Klær Blazer Utforsk vårt utvalg av blazere for dame, perfekte for å legge til et snev av sofistikert eleganse i garderoben din. Velg mellom et mangfold av snitt, farger og mønstre for å finne din signaturstil. Oppdater din look med disse allsidige og stilfulle plaggene som er perfekte for enhver anledning. Bluser & Skjorter Utforsk vårt varierte utvalg av damebluser og skjorter, designet for å bringe tidløs eleganse til enhver garderobe. Velg blant et mangfold av stiler, fra klassiske skjorter til delikate bluser, og skap et sofistikert uttrykk som passer din personlige stil. Oppdater din garderobe hos oss i dag! Bukser & Shorts Utforsk vårt utvalg av damebukser og shorts, perfekte for enhver anledning. Velg mellom et variert utvalg av stiler, fra klassiske bukser til avslappede shorts. Oppdater garderoben din med komfortable og trendy plagg som passer din personlige stil. Genser & Hoodies Utforsk vårt utvalg av damegensere og hoodies, perfekt for enhver anledning. Velg din favorittstil blant vårt mangfold av farger, mønstre og passformer. Oppdater din look med komfortable plagg fra oss i dag! Jakker & Frakker Utforsk vårt varierte utvalg av jakker og frakker for dame, perfekt for å holde deg varm og stilig. Velg blant et mangfold av stiler, fra klassiske frakker til trendy jakker, og finn det perfekte plagget som passer din personlige stil. Oppdater garderoben din med disse elegante og funksjonelle plaggene i dag. Jeans Utforsk vårt utvalg av damejeans, en essensiell del av enhver garderobe. Velg mellom et mangfold av passformer og vasker for å finne din perfekte match. Oppgrader din stil med disse allsidige og komfortable plaggene. Kjoler Utforsk vårt varierte utvalg av damekjoler, fra klassiske til trendy stiler. Velg blant et mangfold av farger, lengder og snitt for å finne din perfekte match. Oppgrader garderoben din i dag med våre elegante kjoler! Skjørt Utforsk vårt utvalg av dame skjørt, designet for å være et tidløs tilskudd til garderoben din. Velg mellom et mangfold av lengder, snitt og stiler, fra klassiske blyantskjørt til luftige maxiskjørt. Oppdater din look med disse allsidige plaggene som passer til enhver anledning. T-Skjorter & Topper Utforsk vårt varierte utvalg av dame t-skjorter og topper, perfekte for enhver anledning. Velg blant et mangfold av farger, mønstre og passformer for å finne din favorittstil. Oppdater din garderobe med komfortable plagg som gir deg både stil og selvtillit. Tilbehør Smykker Utforsk vårt varierte utvalg av smykker for dame, designet for å legge til en touch av tidløs eleganse i ditt antrekk. Velg blant et mangfold av stiler, fra delikate halskjeder til glitrende armbånd, elegante øredobber, ringer og hårklyper, for å finne de perfekte smykkene som passer din unike stil og personlighet. Oppdater din look med disse vakre og allsidige tilbehørene i dag. Herre Hurtiglenker Siste nytt Populære produkter Alle Herreprodukter Klær Bukser Utforsk vårt utvalg av herrebukser, fra klassiske dressbukser til avslappede chinos og trendy jeans. Våre bukser er laget av kvalitetsmaterialer og finnes i ulike passformer og farger. Finn din perfekte stil hos oss! Dress Genser Finn din signaturstil blant vårt utvalg av herregensere og hoodies, designet med fokus på både stil og komfort. Velg blant et variert utvalg av farger, mønstre og passformer for å oppdatere din garderobe med det siste innen mote. Jakker Oppdag vårt utvalg av herrejakker, fra varme vinterjakker til lette vårjakker og stilrene blazere. Våre jakker kombinerer moderne design med høy funksjonalitet og komfort. Finn din perfekte jakke hos oss i dag! Jeans Oppdag vårt utvalg av herrejeans, fra klassiske modeller til moderne stiler. Våre jeans er laget av kvalitetsmaterialer og finnes i ulike passformer og farger. Finn dine perfekte jeans hos oss! Shorts Oppdag vårt varierte utvalg av herreshorts i materialer som lin, bomull og andre naturlige stoffer. Våre shorts tilbyr både stil og komfort, og kommer i ulike farger og passformer. Finn dine favoritt shorts hos oss! Skjorter Utforsk vårt utvalg av herreskjorter, fra klassiske, formelle skjorter til trendy og hverdagslige alternativer. Våre skjorter er laget av høykvalitetsmaterialer og finnes i ulike farger og passformer. Finn din perfekte skjorte hos oss i dag! T-Skjorter & Pique Utforsk vårt utvalg av herre t-skjorter og piquer, fra klassiske basisplagg til trendy design. Våre t-skjorter og piquer er laget av kvalitetsmaterialer og finnes i ulike farger og passformer. Finn dine favoritter hos oss! Tibehør Skjerf & Hodeplagg Undertøy & Sokker Utforsk vårt utvalg av undertøy og sokker, designet med fokus på komfort og funksjonalitet. Velg blant et variert utvalg av boxere, truser, sokker og mer for å finne det perfekte alternativet for dine behov. Oppdater din undertøyskolleksjon med disse komfortable plaggene i dag. Merker Christian AKS Edblad Eton Filippa K Flattered Gabba Hale Bob Hansen & Jacob InWear Les Deux Maanesten Morris Morris Stockholm Munthe Oscar Jacobson Panos Emporio Riccovero Sail Racing Sand Copenhagen Scandinavian Edition Stenströms TGA By Ahler Hvilke personopplysninger vi samler inn og hvorfor vi samler de inn Kontaktskjemaer Når du fyller ut kontaktskjema så sendes all informasjon som du legger inn i skjema til oss som e-post, dette kan inkludere navn, telefonnummer, e-postadresse og beskjed til oss. Denne informasjonen blir lagret i ubegrenset tid, for at vi skal kunne ha oversikt over service- og behandlingshistorikk for våre brukere. Fordi e-postsystemet er ukryptert bør man unngå å sende sensitiv informasjon per e-post. Sendt kontaktskjema blir også arkivert på nettsiden. Informasjonskapsler Hvis du bruker en tjeneste, kan du be oss om å huske navn, e-post og nettsted. Denne informasjonen lagres i en informasjonskapsel og er der for å gjøre ting lettere for deg. Du trenger da ikke å gi inn denne informasjonen på nytt neste gang du skal bruke tjenesten. Disse informasjonskapslene utløper etter ett år. Hvis du har en konto og logger deg inn på dette nettstedet, vil vi opprette en midlertidig informasjonskapsel for å avgjøre om nettleseren din støtter bruk av dette. Denne informasjonskapselen innholder ingen personopplysninger og forsvinner så snart du lukker nettleseren din. Når du logger deg inn, blir det opprettet informasjonskapsler som lagrer innloggingsinformasjonen din og valg du har tatt når det gjelder hvordan innhold skal vises. Informasjonskapsler med innloggingsinformasjon utløper etter to dager, mens de med visningsvalg varer i ett år. Hvis du krysser av for ‘Husk meg’ vil innloggingsinformasjonen din oppbevares i to uker. Hvis du logger deg ut av kontoen din, vil disse informasjonskapslene forsvinne. For mer detaljer om informasjonskapsler og hvordan de blir brukt på denne side, gå til vår oversikt over informasjonskapsler. Nettbutikk Vi samler inn informasjon om deg under kassen på vår butikk. Mens du besøker nettstedet vårt, sporer vi produkter du har sett på. Vi bruker dette til for eksempel å vise deg produkter du nylig har sett. Vi sporer også plassering, IP-adresse og nettlesertype: Vi bruker dette til formål som estimering av skatter og frakt. Vi ber deg om å skrive inn fraktadresse, slik at vi kan estimere frakt før du legger inn en bestilling, og sende deg varene etter bestilling. Vi bruker også informasjonskapsler for å holde oversikt over innholdet i handlekurven mens du surfer på nettstedet vårt. Når du kjøper fra oss, ber vi deg om å gi informasjon, inkludert navn, faktureringsadresse, fraktadresse, e-postadresse, telefonnummer, kredittkort / betalingsinformasjon. Vi bruker denne informasjonen til forskjellige formål, blant annet: Send deg informasjon om din konto og bestilling. Svare på dine henvendelser. Behandle betalinger og forhindre svindel. Sett opp kontoen din for butikken vår. Etterkomme alle juridiske forpliktelser vi har, for eksempel beregning av skatter Forbedre våre tilbud. Send deg markedsføringsmeldinger, hvis du velger å motta dem. Hvis du oppretter en konto, lagrer vi ditt navn, adresse, e-post og telefonnummer, som vil bli brukt til å fylle ut kassen for fremtidige bestillinger. Generelt lagrer vi informasjon om deg så lenge vi trenger den for de formål vi har samlet dem inn for og bruker den. For eksempel lagrer vi ordreinformasjon for skatt og regnskapsmessige formål. Dette inkluderer navn, e-postadresse og faktura- og fraktadresser. Vi vil også lagre kommentarer eller vurderinger, hvis du velger å gjøre det. Medlemmer av vårt team har tilgang til informasjonen du gir oss. For eksempel kan både administratorer og butikkansvarlige få tilgang til bestillings informasjon som hva som ble kjøpt, når ble det kjøpt og hvor det skal sendes. Kundeinformasjon som navn, e-postadresse, faktura og fraktinformasjon er også inkludert. Våre medarbeiderne har tilgang til denne informasjonen for å hjelpe til med å oppfylle bestillinger, behandle refusjoner og hjelpe deg. Innebygd innhold fra andre nettsteder Sider på dette nettstedet kan inkludere innebygd innhold (f.eks. videoer, bilder, artikler osv.). Innebygd innhold fra andre nettsteder oppfører seg på nøyaktig samme måte som om den besøkende hadde besøkt nettstedet som det innebygde innholdet kommer fra. Disse nettstedene kan samle inn opplysninger om deg, bruke informasjonskapsler eller bygge inn sporingssystemer fra en tredjepart og overvåke hva du gjør via dette innebygde innholdet. Dette omfatter også sporing av handlingene dine via det innebygde innholdet dersom du har en konto og er logget inn på nettstedet. Her gjelder de eksterne nettstedenes egne personvernerklæringer. Statistikk Vi bruker Google Analytics for å analysere brukeradferd på våre nettsider. Dette verktøyet lagrer cookies med din brukeradferd, her blir ingen personlig informasjon samlet, da vi har deaktivert innsamling av IP-adresser. Hvis du ikke vil tillate Google å samle brukeradferd, så må du slå på ‘Do Not Track’. Datahjelperne.no har en veiledning i hvordan du slår på ‘Do Not Track’ funksjonen i nettleseren. Hvem vi deler dine opplysninger med Google LLC Google LLC er et amerikansk multinasjonalt teknologiselskap som spesialiserer seg på internettrelaterte tjenester og produkter, som inkluderer online-annonseringsteknologi, søkemotor, cloud computing, programvare og maskinvare. Google Analytics deler brukeradferd med Google LLC, men det er ikke noe personlig data som blir delt, da vi har deaktivert innsamling av IP-adresser. Dintero AS Dintero AS, er en norsk aktør som tilbyr online finansielle tjenester som betalingsløsninger for nettbutikker, innkreving av fordringer, kredittinnbetaling og mer. Ved kassen kan vi samle ditt kredittkortnummer, utløpsdato og sikkerhetskode. Denne informasjonen er dirigert til vår betalingsgateway (Klarna) for å behandle ditt kjøp. Vipps Vipps er en norsk betalingsløsning designet for smarttelefoner utviklet av DNB. Ved kassen kan vi samle ditt telefon-nummer. Denne informasjonen er dirigert til vår betalingsgateway (Vipps) for å behandle ditt kjøp. Hvor lenge vi oppbevarer opplysninger om deg For brukere som registrerer seg på dette nettstedet, lagres det også personopplysninger som de oppgir i brukerprofilen sin. Alle brukere kan se, redigere og slette sine egne personopplysninger når som helst (bortsett fra brukernavn). Nettstedets administratorer kan også se og redigere denne informasjonen. Rettighetene dine når det gjelder opplysninger vi har om deg Hvis du har en konto på dette nettstedet, kan du be om å få en eksport fil som inneholder personopplysningene vi har om deg. Dette omfatter all data du har gitt oss som har blitt lagret. Du kan også be om at vi sletter alle personopplysninger vi har om deg. Dette omfatter ikke opplysninger vi er pålagt å lagre av administrative, juridiske eller sikkerhetsmessige årsaker. Hvordan vi beskytter dine personopplysninger Nettstedet benytter SSL-sertifikat (for HTTPS). Dette sertifikatet har A-klassevurdering, og sikrer blant annet kommunikasjonen mellom nettstedet og besøkende slik at ingen skal kunne lese eller endre på informasjon som utveksles. I tillegg sikrer dette identitet til nettstedet. Servere befinner seg i Tyskland og driftes av Fancy Chap Inc (getflywheels.com), som er en profesjonell og anerkjent hosting leverandør som holder til i USA. De står for nødvendige oppdateringer og sikkerhetstiltak. Passord knyttet til brukerprofilene krypteres i databasen slik at ingen kan se hvilket passord som er knyttet til en brukerkonto, selv ikke teknisk personell. Det er flere nivåer av tilgangskontroll i løsningsarkitekturen. Operatører for ordreadministrasjon har tilgang til ordrer og behandling av disse. Endringer Vi kan endre samtykkevilkår og personvernerklæring for å følge nye rettslige krav, og på grunn av endringer i vår egen praksis for innsamling og behandling av personopplysninger. Ved endringer som krever samtykke vil du bli bedt om å samtykke til nye vilkår. Kontaktinformasjon For spørsmål eller henvendelser til personvern kan dere ta kontakt på nettbutikken@rinohansen.no. Du kan klage på hvordan vi behandler dine opplysninger til Datatilsynet E-post: postkasse@datatilsynet.no Telefon: 22 39 69 00. nettbutikken@rinohansen.no Kontakt Rino Hansen (Jeans Corner AS) Nygaards Gata 46, 1607, Fredrikstad Tlf: 69 31 98 31 E-post: nettbutikken@rinohansen.no Åpningstider Mandag : 10:00 - 18:00 Tirsdag : 10:00 - 18:00 Onsdag : 10:00 - 18:00 Torsdag : 10:00 - 19:00 Fredag : 10:00 - 18:00 Lørdag : 10:00 - 17:00 Følg oss Facebook Instagram Firmainfo Personvern Vilkår og Betingelser Bli medlem av vår kundeklubb Made by Studio G9 Tilbakestill passordet E-Post Tilbakestill Logg inn eller opprett en ny konto Har du en konto? Logg inn med Logg inn med e-post Logg inn med e-post Ønsker du å bli medlem? Registrere deg her Logg inn eller opprett en ny konto E-Post Passord Logg inn Glemt passord? DINE INFORMASJON E-Post Mobilnummer Fornavn Etternavn Adresse Postnummer By Kjønn MANN KVINNE Ønsker du gode tilbud og informassjon på SMS? JA TAKK NEI TAKK Ønssker du gode tilbud og informassjon på E-Post? JA TAKK NEI TAKK Passord Registrer Tilbake"
  ]
}
```

Page: https://rinohansen.no/vilkar-og-betingelser/ — title: Vilkår og Betingelser - Rino Hansen

SHA-256: `9a13512fd918e4001231eecf69e4599a4ab997466e3b2415e1e18aa9e1e3f509`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "965194894"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 934394747 / JAVI-GROUP AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: javigroup.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: javi-group.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: javigroup.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: javi-group.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://www.javi-group.com/contact-2/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: javi-group.com; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: https://javigroup.com/; recorded rule: `None`; level: not saved.
- Candidate: https://javi-group.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://javi-group.com/; recorded rule: `None`; level: not saved.

Page: https://javigroup.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://javigroup.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://javigroup.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://javigroup.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://javigroup.com/personvernerklaering — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://javigroup.com/kontakt-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://javigroup.com/om — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.javi-group.com/ — title: JAVIGROUP

SHA-256: `b1ed6c5c909fd7ac394575a03aa626e475580b75c7a73f53839353dc418b1497`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [
    "group",
    "Group",
    "Group",
    "group",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.javi-group.com/contact/ — title: JAVIGROUP

SHA-256: `e15113db78bdeea88475be56e9a9d23715473f6f015fbccae22234b657a66399`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "header",
    "imprint-kontakt",
    "footer",
    "copyright"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [
    "group",
    "group",
    "Group",
    "Group",
    "group",
    "group",
    "Group",
    "Group",
    "group",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 914975158 / LOE BRUK 13 AS

Categories: veto; terminal website state: not_available.

- Candidate: vevi.no; recorded rule: `group_without_exact_orgnr`; level: REJECT.
- Candidate: loebruk13.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: loe-bruk-13.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: loebruk13.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: loe-bruk-13.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://vevi.no/; recorded rule: `None`; level: not saved.

Page: https://www.vevi.no/ — title: Vestviken Gruppen AS  | Entreprenør

SHA-256: `fb1d41ecfe0643468dc416a9055893a9daeec89274f0cd0807d474cc1eddc164`; candidate rules: group_without_exact_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Gruppen",
    "Gruppen",
    "Gruppen",
    "Gruppen"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 994918540 / GRØTEN AS

Categories: fetched-without-proof, veto; terminal website state: failed.

- Candidate: groeten.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: groten.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: groeten.com; recorded rule: `parked`; level: REJECT.
- Candidate: https://groten.com/kontakt-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: groten.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: xn--grten-wua.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--grten-wua.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://groeten.com/; recorded rule: `None`; level: not saved.
- Candidate: https://groten.com/; recorded rule: `None`; level: not saved.

Page: https://groeten.com/ — title: GROETEN.COM  MAY BE AVAILABLE!

SHA-256: `f537258ac59da4ada833cdeeee83a8274356ff351a990111e215fa7907627443`; candidate rules: parked

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://groten.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://groten.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://groten.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://groten.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://groten.com/personvernerklaering — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 915664830 / BUILDING STYLE AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: buildingstyle.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: building-style.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: buildingstyle.com; recorded rule: `corroboration`; level: LOW.
- Candidate: building-style.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://buildingstyle.com/; recorded rule: `None`; level: not saved.

Page: https://buildingstyle.com/ — title: BuildingStyle.com is for sale - Premium  Domain

SHA-256: `54e81e92de7a14ae5f7822ba9353779ac87c08bc588e2808cde8fa78409b0e10`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://buildingstyle.com/kontakt — title: 404 Not Found

SHA-256: `e38e0cee2c2996a92b17cd2a648120c322ea4d33d62adb2823b0a1f9ffe21ab2`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 916151721 / SPEIL - O - GLASS AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: plateteknikk.no; recorded rule: `corroboration`; level: LOW.
- Candidate: speiloglass.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: speil-o-glass.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: speiloglass.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: speil-o-glass.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://plateteknikk.no/; recorded rule: `None`; level: not saved.

Page: https://plateteknikk.no/ — title: Plateteknikk AS

SHA-256: `eeefb0b244073e005545d90022548139759ddb9a383bffcda1e8bf2cd12350c7`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://plateteknikk.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://plateteknikk.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://plateteknikk.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://plateteknikk.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://plateteknikk.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 980616622 / BAGGES AS

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.bagges.no/om-oss/avdeling-for-innesalg-kundeservice; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bagges.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: bagges.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bagges.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://bagges.no/; recorded rule: `None`; level: not saved.
- Candidate: https://bagges.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://bagges.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.bagges.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://bagges.com/; recorded rule: `url_refused`; level: not saved.

Page: https://bagges.no/ — title: Object moved

SHA-256: `9a247ac4559b0442793a31a075b25ca4d29d98d1cd3bc8bde77d61f9b4796eb6`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bagges.no/ — title: BAGGES AS - Ventiler, pakninger og tekniske løsninger

SHA-256: `c9a5c43c17ac6d471209edc8a3a18f6948219b46e104f5b600119bd3d87c37c8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title",
    "body",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bagges.no/kontakt — title: Kontakt

SHA-256: `0f3cbff6c4008f15b2a3b7b074671a7b3146b08924b946e905ef65a3955fbc12`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bagges.no/om-oss — title: Om oss

SHA-256: `e37d1bee38939714e9c62ef3588fd7e3feb586d346bf2a6d93d195850aa5f28b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bagges.no/om-oss/avdeling-for-ventiler-pakninger-og-pumper — title: AVDELING FOR VENTILER, PAKNINGER OG PUMPER

SHA-256: `cedb27dcdac5d9d6e1958029eebcfb6aa6f68173feed196294b8e6482e16f7a9`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bagges.no/om-oss/avdeling-for-isolasjon-og-filtrering — title: AVDELING FOR ISOLASJON OG FILTRERING

SHA-256: `1c707c4bdd0da2a21c61fc316f638655d5df396bea08a47802565b640f945817`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt",
    "footer"
  ],
  "name_without_suffix": true,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 952473786 / BORETTSLAGET NORDAHL BRUNSGT 4

Categories: veto; terminal website state: not_available.

- Candidate: nbbo.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: borettslagetnordahlbrunsgt4.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: borettslaget-nordahl-brunsgt-4.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: borettslagetnordahlbrunsgt4.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: borettslaget-nordahl-brunsgt-4.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.nbbo.no/; recorded rule: `None`; level: not saved.

Page: https://nbbo.no/ — title: NBBO - Nedre Buskerud Boligbyggelag - Gode hjem siden 1946

SHA-256: `0d0e18d18f16b0b56af68e3708e3759dc155efbc6502897c9db88826a4456e04`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "952527827"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 899177932 / PROFINOVA AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.profinova.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: profinova.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: profinova.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: https://profinova.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: profinova.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: https://www.profinova.no/; recorded rule: `None`; level: not saved.
- Candidate: https://profinova.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://profinova.com/; recorded rule: `None`; level: not saved.

Page: https://www.profinova.no/ — title: Profinova AS

SHA-256: `dcb1500398b56bbf09856575584b50f616d0f9dc44ca75ea027f0087fae11180`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "title"
  ],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.profinova.no/kontakt — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.profinova.no/om-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.profinova.no/personvern — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.profinova.no/personvernerklaering — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.profinova.no/kontakt-oss — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://profinova.com/ — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://profinova.com/kontakt — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://profinova.com/om-oss — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://profinova.com/personvern — title: 

SHA-256: `6dc9c7fc93bb488bb0520a6c780a8d3c0fb5486a4711aca49b4c53fac7393023`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 911920603 / ISOBYGG SOGN AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://www.sogn.no/om-oss; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: sogn.no; recorded rule: `corroboration`; level: LOW.
- Candidate: isobyggsogn.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: isobygg-sogn.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: isobyggsogn.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: isobygg-sogn.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://sogn.no/; recorded rule: `None`; level: not saved.

Page: https://www.sogn.no/ — title: Sogn

SHA-256: `92309b5b4509e918934f50603fd64116710695c386e7cfe6641bbfcfa101699d`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sogn.no/kontakt-oss — title: Kontakt oss — Sogn

SHA-256: `3173bdbcbc2473724543ca8bab05f4ad0d1b3889110d6b57779fe2cb5e228f12`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sogn.no/jobb-for-to — title: Jobb for to? — Sogn

SHA-256: `a377575aa66c6b5e2ed9d4eefadb1f1e51ae02e2ea6104b91e5c87e74690c63c`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sogn.no/personvernerklaering — title: Personvernerklæring — Sogn

SHA-256: `cf583d4fa7dd495ac3350388be607566688bb7531472c36fddc7998f40ff1233`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.sogn.no/kontakt — title: Sogn

SHA-256: `9b69ef1269f1f653954d8e213905c8889dc6f3363ba3802027d5c922bc4ed5aa`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 992568356 / SURVITEC FIRE SOLUTIONS NORWAY AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: https://survitecgroup.com/about-us/our-values; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: survitecgroup.com; recorded rule: `corroboration`; level: LOW.
- Candidate: survitecfiresolutionsnorway.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: survitec-fire-solutions-norway.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: survitecfiresolutionsnorway.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: survitec-fire-solutions-norway.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.survitecgroup.com/; recorded rule: `None`; level: not saved.

Page: https://www.survitecgroup.com/ — title: 301 Moved Permanently

SHA-256: `a76004959bdd8402fe10509e667dd20ad3e7390f6e8097cc44ef935c908e0e36`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://survitecgroup.com/ — title: Trusted survival technology, equipment, and services | Survitec

SHA-256: `7ab7d7f8b6b830faeec83f13d092145bd1105d2e14432e2e74f0416c8c045fa3`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group",
    "holding",
    "Group",
    "holding",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://survitecgroup.com/contact-us — title: Contact our highly qualified Survitec experts

SHA-256: `49188fa82506e267d6b2c9cf9ba087f71bc37100f904a7c901e33a26647ca541`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group",
    "holding",
    "Group",
    "holding",
    "Group",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://survitecgroup.com/contact-us — title: Contact our highly qualified Survitec experts

SHA-256: `62ec7b69e3eec285031015168471b0c98ce32f39567d399bf55dad6cd0c5201a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group",
    "holding",
    "Group",
    "holding",
    "Group",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://survitecgroup.com/about-us/company-overview — title: Company Overview | Survitec

SHA-256: `e3bc583806f56f17b82051952430573ef40f9436df5db1379b4a30b67a90df4b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "Group",
    "Group",
    "holding",
    "Group",
    "holding",
    "Group",
    "Group",
    "Group"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 948866994 / C ANDERSENSGATE BORETTSLAG

Categories: veto; terminal website state: not_available.

- Candidate: usbl.no; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: candersensgateborettslag.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: c-andersensgate-borettslag.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: candersensgateborettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: c-andersensgate-borettslag.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://usbl.no/; recorded rule: `None`; level: not saved.

Page: https://usbl.no/ — title: Document Moved

SHA-256: `eb3295ab518e22f746c806441490808cbe92b77acf0575d1f725893fdf182f35`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.usbl.no/ — title: Boligbyggelag, forretningsfører og boligutvikler | Usbl

SHA-256: `82162aad7abcbb750db8f1c95eada0eb2760cd16192302369296e41c5bc61709`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "950285680"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 926290126 / FALCO INVEST AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: falcoinvest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: falco-invest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: falcoinvest.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://falco-invest.com/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: falco-invest.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://falcoinvest.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.falcoinvest.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://falcoinvest.com/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://falco-invest.com/; recorded rule: `None`; level: not saved.

Page: https://falco-invest.com/ — title: WordPress – Un site utilisant WordPress

SHA-256: `e057b91e5790f6d8cb3764a15ed69c11f83cb6cf397f7ef442f3eb3b750289d1`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://falco-invest.com/kontakt — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://falco-invest.com/om-oss — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 911606321 / IMD FACTORY AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: imdfactory.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: imd-factory.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://imdfactory.com/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: imdfactory.com; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: imd-factory.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://imdfactory.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.imdfactory.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://imdfactory.com/; recorded rule: `None`; level: not saved.

Page: http://imdfactory.com/ — title: imdfactory.com

SHA-256: `293acf1b5043c357b2edc871b96849e96dceafa427b363154991f06f84f63954`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://imdfactory.com/kontakt — title: imdfactory.com

SHA-256: `02e39f356f5d971b7e7fd6f803bfac3e9f7cbf3188716d0c92dd069048233fac`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://imdfactory.com/om-oss — title: imdfactory.com

SHA-256: `61cac6076e85823a114d842a6284d3baf57a21b0512115ba582ce8a8939ec45b`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://imdfactory.com/personvern — title: imdfactory.com

SHA-256: `da5bd883c0b355dc1f42a8eebb38aa767afc2ac435669e066c72b42c8dbea688`; candidate rules: short_or_js_shell, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 928445607 / MERSAN AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: mersan.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://mersan.com/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: mersan.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://mersan.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.mersan.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://mersan.com/; recorded rule: `None`; level: not saved.

Page: http://mersan.com/ — title: GRUPO MERSAN - Inicio

SHA-256: `ab29bbbe2199f85697251095888b924f80382dceaab823676a284f32d3fc38ed`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://mersan.com/page_1124307816150.html — title: GRUPO MERSAN - Contactenos

SHA-256: `910a4aa94a49cef911120673a2f8152efaaa7d5ac580f97d451e796ea10e710f`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://mersan.com/kontakt — title: 404 Not Found

SHA-256: `cbcddb919665572e7caaaf3e9c60e33ce5ae6e7af8bd843307a8f2843582593f`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://mersan.com/om-oss — title: 404 Not Found

SHA-256: `cbcddb919665572e7caaaf3e9c60e33ce5ae6e7af8bd843307a8f2843582593f`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 985196214 / BYGGMESTER JAKOBSEN AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: byggmesterjakobsen.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: http://byggmester-jakobsen.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: byggmester-jakobsen.no; recorded rule: `corroboration`; level: LOW.
- Candidate: byggmesterjakobsen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: byggmester-jakobsen.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://byggmester-jakobsen.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.byggmester-jakobsen.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://byggmester-jakobsen.no/; recorded rule: `None`; level: not saved.

Page: http://byggmester-jakobsen.no/ — title: byggmester-jakobsen.no is parked

SHA-256: `35b19b865df3c0cee66f7f112e0c0a41cbd88fba57bd69ed73b144db62d41878`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://byggmester-jakobsen.no/kontakt — title: byggmester-jakobsen.no is parked

SHA-256: `77ded89c5dedf041f7cd56da6857e368170fe9a5ffaff228a6010f5961c90419`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://byggmester-jakobsen.no/om-oss — title: byggmester-jakobsen.no is parked

SHA-256: `d46d866e292e6a1327827991a660968cbe5fa6a978fa662164f186711dec3887`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://byggmester-jakobsen.no/personvern — title: byggmester-jakobsen.no is parked

SHA-256: `7987cac637863f36fe3caa6383f97c62446effd28e5725f3f24fe9db4a587067`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 923395881 / BRYNEKLINIKKEN AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: http://bryneklinikken.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bryneklinikken.no; recorded rule: `corroboration`; level: LOW.
- Candidate: bryneklinikken.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://bryneklinikken.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.bryneklinikken.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://bryneklinikken.no/; recorded rule: `None`; level: not saved.

Page: http://bryneklinikken.no/ — title: bryneklinikken.no is parked

SHA-256: `6559e472e160b62cf44e42a063e166edce224d051d7fea6a5be73254419a4dad`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://bryneklinikken.no/kontakt — title: bryneklinikken.no is parked

SHA-256: `261563363db42311af1e7c3229ed2604b8b79e706979d8bef5a3989ad8c13bc9`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://bryneklinikken.no/om-oss — title: bryneklinikken.no is parked

SHA-256: `ba2cdb5fd0f21ceb13078c43644503377068c4f6eb5ae0d2ab1d4f679e9d5549`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: http://bryneklinikken.no/personvern — title: bryneklinikken.no is parked

SHA-256: `44b04592e6639e5df74dde938cd379e372c1c473e684363613e7eb486099adc4`; candidate rules: corroboration, website_budget_exhausted, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 934608143 / NORWAY MARINE SUPPLY AS

Categories: ambiguous; terminal website state: ambiguous.

- Candidate: https://www.maritim.no/personvernerklaering; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: maritim.no; recorded rule: `registry_and_live_corroboration`; level: REGISTRY_DECLARED.
- Candidate: norwaymarinesupply.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: norway-marine-supply.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: norwaymarinesupply.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: norway-marine-supply.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: norwaymarinesupply.com; recorded rule: `website_http_5xx`; level: LOW.
- Candidate: https://www.maritim.no/; recorded rule: `None`; level: not saved.
- Candidate: https://norwaymarinesupply.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://norwaymarinesupply.com/; recorded rule: `website_http_5xx`; level: not saved.

Page: https://www.maritim.no/ — title: Båtutstyr - Maritim båtbutikk på nettet - Maritim

SHA-256: `84008b4baa7609e1cb189c96acceceb9cf195f36026e2dd4013f5d858b86116c`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [
    "803948623"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.maritim.no/nettbutikk-kontakt — title: Nettbutikk kontakt Maritim Båtutstyr

SHA-256: `308bdd57bc68b95e20938f487e15aff236f8fa78344ca1427cd37b991bf7623f`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": true,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.maritim.no/personvern-gdpr — title: Personvern - GDPR Maritim Båtutstyr

SHA-256: `e574d87a6034236528a42882d09d4e80cf5e372011dead40abb929f9cfa14d7f`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [
    "body",
    "imprint-kontakt"
  ],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": true,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [
    "as"
  ],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "Regnskapsloven"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.maritim.no/kontakt — title:  Maritim Båtutstyr

SHA-256: `cb6ed95e500f079afad029a7d08b39d1d014164334c0b1b105ee36eb660fa0e9`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.maritim.no/om-oss — title:  Maritim Båtutstyr

SHA-256: `cb6ed95e500f079afad029a7d08b39d1d014164334c0b1b105ee36eb660fa0e9`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.maritim.no/personvern — title:  Maritim Båtutstyr

SHA-256: `cb6ed95e500f079afad029a7d08b39d1d014164334c0b1b105ee36eb660fa0e9`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 914609674 / NYE OSLO HAIR & BEAUTY AS

Categories: ambiguous; terminal website state: ambiguous.

- Candidate: https://www.oslohair.no/personvern; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: oslohair.no; recorded rule: `registry_and_live_corroboration`; level: REGISTRY_DECLARED.
- Candidate: nyeoslohairbeauty.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: nye-oslo-hair-beauty.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: nyeoslohairbeauty.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: nye-oslo-hair-beauty.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.oslohair.no/; recorded rule: `None`; level: not saved.

Page: https://www.oslohair.no/ — title: Frisør Oslo - Kåret til Oslo's beste frisørsalong for 2026

SHA-256: `bdd302ff94564b9faf05ecc3d80ccb5532c12c99b17463c0ae28f4ca92b301a1`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.oslohair.no/kontakt/ — title: Kontakt oss - Oslo Hair & Beauty - Frognerveien 5

SHA-256: `adbbf355421396c1414d02ff2612169ea10f9a12ab25c196ad352d84812b6aed`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.oslohair.no/kontakt/ — title: Kontakt oss - Oslo Hair & Beauty - Frognerveien 5

SHA-256: `adbbf355421396c1414d02ff2612169ea10f9a12ab25c196ad352d84812b6aed`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.oslohair.no/om-oss — title: Side ikke funnet - Oslo Hair & Beauty

SHA-256: `34b122f0d5d0010cba51c82df690ccc3e5e92cc33346debf080d98bae4e9a91f`; candidate rules: registry_and_live_corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 918317848 / DINGO AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: dingo.no; recorded rule: `url_refused`; level: LOW.
- Candidate: https://www.dingo.com/company/; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: dingo.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://dingo.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://dingo.com/; recorded rule: `None`; level: not saved.

Page: https://dingo.com/ — title: 301 Moved Permanently

SHA-256: `0104382f7956f68472745ac75b65e02b89e41eeca05f4911f8332fd8e6f07dee`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dingo.com/ — title: Equipment Maintenance Software | Predictive Maintenance | DINGO

SHA-256: `ee1918a3f944f25ef05adddb20107f4e2b8edb5c622823cd6f4f4fde6272af8a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dingo.com/contact/ — title: Contact DINGO | Predictive Maintenance Experts

SHA-256: `29b9c923f1db2d62d7bce5f30a26f9a3a16171fb6b46e6266f7a3e4f2b31b1f8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://dingo.com/contact/ — title: 301 Moved Permanently

SHA-256: `cd75115ccdf85e5a7b157c372831c249d90067207a624adddb5ab24ca6e18198`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.dingo.com/contact/ — title: Contact DINGO | Predictive Maintenance Experts

SHA-256: `29b9c923f1db2d62d7bce5f30a26f9a3a16171fb6b46e6266f7a3e4f2b31b1f8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 926432826 / TELELYS AS

Categories: veto; terminal website state: not_available.

- Candidate: telelys.no; recorded rule: `url_refused`; level: LOW.
- Candidate: telelys.com; recorded rule: `foreign_orgnr`; level: REJECT.
- Candidate: https://telelys.no/; recorded rule: `url_refused`; level: not saved.
- Candidate: https://telelys.com/; recorded rule: `None`; level: not saved.

Page: https://telelys.com/ — title: Telelys – Data eSIM for reiser

SHA-256: `31d564a7c3c1222362a03bfbe2d2298dcda1c7e61dbacdb093e41036fe6683ce`; candidate rules: foreign_orgnr

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [
    "935080134"
  ],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 934656695 / TVINNA AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: tvinna.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: tvinna.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://tvinna.com/; recorded rule: `None`; level: not saved.

Page: https://tvinna.com/ — title: Tvinna - One in the Dark

SHA-256: `fa28b79cacff54ee3dfe5713ea17a052e27389af0370c0904f0d45ec17498358`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://tvinna.com/kontakt — title: Tvinna - One in the Dark

SHA-256: `a3b01fd006f7e82ab6c73211b1d218893609c8bdc7d42a31d1ca9a3f07ad1595`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://tvinna.com/om-oss — title: Tvinna - One in the Dark

SHA-256: `fc54a20d3517d95d4ca93f37c0809eab613d4a27ccf91e167d6623073bc60c07`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://tvinna.com/personvern — title: Tvinna - One in the Dark

SHA-256: `520c69c70f308c849e746079456b226ebde71d0944bb03e7c1ab1c409e4a8dcf`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://tvinna.com/personvernerklaering — title: Tvinna - One in the Dark

SHA-256: `daafba1f28a794134ee53e0deb004e449e3b450d9c5fad19acf6b238768bfed7`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://tvinna.com/kontakt-oss — title: Tvinna - One in the Dark

SHA-256: `04181f1df688a5f45c8fb0686d41a55cd2e6db16bae1ae25a8cae4a1581be8cb`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 959998027 / MEER AS

Categories: fetched-without-proof; terminal website state: failed.

- Candidate: meer.no; recorded rule: `http_404`; level: LOW.
- Candidate: https://www.meer.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: meer.com; recorded rule: `corroboration`; level: LOW.
- Candidate: https://www.meer.no/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: http://www.meer.no/; recorded rule: `None`; level: not saved.
- Candidate: https://meer.com/; recorded rule: `None`; level: not saved.

Page: http://www.meer.no/ — title: 404 Not Found

SHA-256: `9448f8a1159c9b14e3e1b9d8eab1a6ddf88d26e1f888a34cef430c756e4e6e1e`; candidate rules: http_404, website_connect_error

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://meer.com/ — title: 301 Moved Permanently

SHA-256: `9e17cb15dd75bbbd5dbb984eda674863c3b10ab72613cf8a39a00c3e11a8492a`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.meer.com/ — title: 

SHA-256: `cb67fef7166a6933910ae7dc62bc89f5578ebcf00d331b850d20773d7b50ec0b`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.meer.com/en — title: Meer | English edition

SHA-256: `13ed56b98bd7b0ff495be09a5d9f922d3ba0592d8b80bbbb1df758edb05deb71`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": true,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 932447940 / ØHS INVEST AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: oehsinvest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: oehs-invest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: oehsinvest.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: oehs-invest.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: ohsinvest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://www.ohsinvest.com/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: ohsinvest.com; recorded rule: `corroboration`; level: LOW.
- Candidate: ohs-invest.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: ohs-invest.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--hs-invest-k8a.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--hsinvest-44a.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--hs-invest-k8a.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--hsinvest-44a.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://ohsinvest.com/; recorded rule: `None`; level: not saved.

Page: https://www.ohsinvest.com/ — title: Home | Oak Hills Securities

SHA-256: `75b7213bffcba3a69aebcf01b84f1c95d284ee4d1c750cd68daa044f509e46e0`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.ohsinvest.com/contact-us — title: Contact Us | Oak Hills Securities

SHA-256: `bb6dbfac96f5004e375d5be774dcf298ef8dae1db46ffebd17bc60d3597178e9`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.ohsinvest.com/about — title: About Us | Oak Hills Securities

SHA-256: `554dacaea27f9cd02a6bd406b95a8b37ab61613e38227be4b06280984154abc6`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 928664341 / GREENBALL AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: https://www.greenball.no/om; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: greenball.no; recorded rule: `short_or_js_shell`; level: LOW.
- Candidate: greenball.com; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: greenball.com; recorded rule: `url_refused`; level: LOW.
- Candidate: https://www.greenball.no/; recorded rule: `None`; level: not saved.
- Candidate: https://greenball.com/; recorded rule: `website_budget_exhausted`; level: not saved.
- Candidate: https://greenball.com/; recorded rule: `website_connect_error`; level: not saved.
- Candidate: https://www.greenball.com/; recorded rule: `url_refused`; level: not saved.

Page: https://www.greenball.no/ — title: GreenBall.no

SHA-256: `0f9f2f1cd5708b06fb1962a04792b6fae15cf75553ed32febac0a23d26b06562`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.greenball.no/kontakt — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.greenball.no/om-oss — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.greenball.no/personvern — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.greenball.no/personvernerklaering — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.greenball.no/kontakt-oss — title: 404 Not Found

SHA-256: `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; candidate rules: short_or_js_shell, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 989038583 / LØRENPARKEN BOLIGSAMEIE

Categories: ambiguous, fetched-without-proof; terminal website state: ambiguous.

- Candidate: https://www.bori.no/kontakt; recorded rule: `website_budget_exhausted`; level: LOW.
- Candidate: bori.no; recorded rule: `corroboration`; level: MEDIUM.
- Candidate: loerenparkenboligsameie.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: loerenparken-boligsameie.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: loerenparkenboligsameie.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: loerenparken-boligsameie.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: lorenparkenboligsameie.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: lorenparkenboligsameie.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: lorenparken-boligsameie.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--lrenparken-boligsameie-5ic.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--lrenparkenboligsameie-qfc.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: lorenparken-boligsameie.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--lrenparken-boligsameie-5ic.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: xn--lrenparkenboligsameie-qfc.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://bori.no/; recorded rule: `None`; level: not saved.

Page: https://bori.no/ — title: 302 Found

SHA-256: `fbf3632b5274808378d65cb72e934734d5ef1d61d33b0840fb0282977e8e8032`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/ — title: Hjem - BORI BBL

SHA-256: `a7f556fcb3af94c43a8cc5996a3a8ab3505a111c1a28293f154b03006072b724`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/om-bori/kontakt-oss/ — title: Kontakt oss - BORI BBL

SHA-256: `82279d0c6ec76ffe11c8a16aee378284c20ded90c1e569154ff463097c58c81f`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [
    "regnskap"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/medlem/aktuelt/vilkarene-for-fordelsprogrammet-oppdateres/ — title: Vilkårene for fordelsprogrammet oppdateres - BORI BBL

SHA-256: `8d71e4584adc017ce25f6de9b1e3766670fd78443f3784a87c81fa9b6ce3a0b8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/personvernerklaering/ — title: Personvernerklæring - BORI BBL

SHA-256: `4aea6518339bfb78b89eebd3b27fd4cd1fa7f9d22a0ce75e433e25328bee74dc`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "konsern"
  ],
  "publisher_role_markers": [
    "regnskapsmateriale",
    "regnskapsavdelingen"
  ],
  "agency_credit_lines": []
}
```

Page: https://www.bori.no/medlem/vilkar-fordelsprogram/ — title: Vilkår fordelsprogram - BORI BBL

SHA-256: `4f669ba1f6eabe99f7dd68402353cf974b1cf02a7b024a52f8dd7a4aafe56cd8`; candidate rules: corroboration, website_budget_exhausted

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": true,
  "registry_full_email": false,
  "registry_email_domain": true,
  "exact_street_and_postcode": false,
  "registry_declared_domain": true,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
## 20261117 / 931858483 / WIKNE MOTOR AS

Categories: fetched-without-proof; terminal website state: not_available.

- Candidate: wiknemotor.no; recorded rule: `corroboration`; level: LOW.
- Candidate: wikne-motor.no; recorded rule: `no_such_domain`; level: LOW.
- Candidate: wiknemotor.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: wikne-motor.com; recorded rule: `no_such_domain`; level: LOW.
- Candidate: https://wiknemotor.no/; recorded rule: `None`; level: not saved.

Page: https://wiknemotor.no/ — title: hjem - Wiknemotor

SHA-256: `f26602b0df70be57a86c79748901c8a3809bab141f1de15073864c472bdad91e`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "GROUP",
    "GROUP"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wiknemotor.no/contact/ — title: Contact - Wiknemotor

SHA-256: `8a55d409b42fc0b662f007645c73a067cbb7a627d68e738902329d79516bece5`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "GROUP",
    "GROUP",
    "GROUP"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wiknemotor.no/about-us/ — title: About Us - Wiknemotor

SHA-256: `c9caea8120952722a4b7f5a5322f9c9e287b52536a696374e386b60f00900d9c`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "GROUP",
    "GROUP",
    "GROUP"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wiknemotor.no/kontakt — title: 404: Page not found - Wiknemotor

SHA-256: `6c38a1b18cf471a4b58752cf3687ed459749240c2425856e7c10450d1d320d6c`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "GROUP",
    "GROUP",
    "GROUP"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wiknemotor.no/om-oss — title: 404: Page not found - Wiknemotor

SHA-256: `0ca47c2aface71c615d41e37a8712f0dbc36c9e014244e01c0fa92fb2ecd3395`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "GROUP",
    "GROUP",
    "GROUP"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```

Page: https://wiknemotor.no/personvern — title: 404: Page not found - Wiknemotor

SHA-256: `f4488b36b814327b71f5a8c44ee1fbd24ef038c858044ce660693f7a84549344`; candidate rules: corroboration

```json
{
  "full_legal_name_locations": [],
  "name_without_suffix": false,
  "registry_phone": false,
  "registry_full_email": false,
  "registry_email_domain": false,
  "exact_street_and_postcode": false,
  "registry_declared_domain": false,
  "other_orgnrs": [],
  "same_stem_legal_forms": [],
  "group_parent_markers": [
    "GROUP",
    "GROUP",
    "GROUP"
  ],
  "publisher_role_markers": [],
  "agency_credit_lines": []
}
```
