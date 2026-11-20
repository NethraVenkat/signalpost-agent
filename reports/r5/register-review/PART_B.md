# Regulatory-register access review

**Scope and cutoff:** review of uncovered Norwegian public registers relevant to legal-entity identity, authorization or regulated operations, against the sources already listed in [`docs/SOURCES.md`](../../../docs/SOURCES.md). Live robots responses below were fetched 2026-11-20 04:26 UTC. `404` is treated as no published robots rules under RFC 9309; `403` is a 4xx response and therefore also permits access under that rule. This records robots permission only, not a licence or authentication grant.

## Candidate inventory

| Candidate / publisher | Documented API or distribution | Licence / access classification | Live robots result and relevant lines | Decision |
|---|---|---|---|---|
| Official Aquaculture Register / Norwegian Directorate of Fisheries | [`https://api.fiskeridir.no/pub-aqua/`](https://api.fiskeridir.no/catalog/) (listed in the official API catalog as public/allment) | NLOD 2.0; DataNorge marks it public. Catalog has no required-authentication entry. | `api.fiskeridir.no/robots.txt`: **404**, empty body; no `User-agent` or `Disallow` lines. | **Survives.** Best-fit candidate: documented public register API, reuse-friendly licence, no robots restriction or credential requirement found. Recommend this one if the next step authorizes an integration. |
| Operational Aquaculture Rights / Norwegian Directorate of Fisheries | [`https://api.fiskeridir.no/aqua-operations-public`](https://data.norge.no/nb/data-services/3ad8c19c-6591-3217-be54-77b616d77f3e/offentlig-api-for-operasjonelle-akvakulturrettigheter) | NLOD 2.0; official catalog lists public/allment and no required-authentication entry. | Same host: **404**, empty body; no rules. | **Survives the access gate**, but it is an adjacent operational-rights dataset, not the register itself; not selected over the explicit register above. |
| Buyer Register / Norwegian Directorate of Fisheries | [`https://api.fiskeridir.no/buyer-api/`](https://api.fiskeridir.no/catalog/) (catalog; [Swagger UI](https://api.fiskeridir.no/buyer-api/swagger-ui/index.html)) | NLOD 2.0; catalog lists public/allment and no required-authentication entry. | Same host: **404**, empty body; no rules. | **Survives access gate.** Register concerns registered fish buyers/landing sites; lower fit for general company regulatory status, so not selected. |
| Authorization Register / Norwegian Directorate of Fisheries | [`https://api.fiskeridir.no/authreg-api/swagger-ui/`](https://api.fiskeridir.no/catalog/) | NLOD 2.0; catalog lists public/allment and no required-authentication entry. | Same host: **404**, empty body; no rules. | **Survives access gate**, but covers vessel authorizations rather than company-level approvals; not selected. |
| Aquaculture application service / Norwegian Directorate of Fisheries | [`https://api.fiskeridir.no/aqua-portal-api-public`](https://api.fiskeridir.no/catalog/) | NLOD 2.0; public/allment, no required-authentication entry in the catalog. | Same host: **404**, empty body; no rules. | Access gate passes, but it is an applications service rather than an established register; not selected. |
| Central Approval Register (Sentral godkjenning) / DiBK | [`https://sgregister.dibk.no/api`](https://data.norge.no/en/data-services/c443ab25-ae23-3b67-b6b3-3782c08f4d46/sgregister-register-over-foretak-med-sentral-godkjenning) | DataNorge says no licence is provided. | **200**; matching lines are quoted in the robots excerpt section. | **Eliminated:** intended API path is disallowed; licence absent. |
| Registered staffing enterprises / Labour Inspection Authority | [Public register page](https://www.arbeidstilsynet.no/tema/ansettelse/innleie/registrerte-bemanningsforetak/) | No documented API/bulk distribution or reuse licence found for this register. | `www.arbeidstilsynet.no/robots.txt`: **200**; relevant lines quoted below. | **Eliminated:** no documented licensed API/bulk route. |
| Car-care register (Bilpleieregisteret) / Labour Inspection Authority | [Open API portal](https://openapi.arbeidstilsynet.no/) | Portal describes open access, but no reuse licence found. | `openapi.arbeidstilsynet.no/robots.txt`: **403** with XML `AccessDenied`; no robots lines. RFC 9309 4xx treatment applies. | **Eliminated:** licence absent/unclear. |
| National Kindergarten Register (NBR) / Directorate for Education | [`https://data-nbr.udir.no/swagger/v4/swagger.json`](https://data.norge.no/en/data-services/5700e3a2-8fe0-3363-8419-965f70c4d216/national-kindergarten-register-nbr-api) | NLOD 2.0 and metadata says public, but Swagger declares global Basic authentication. | `data-nbr.udir.no/robots.txt`: **404**, empty body; no rules. | **Eliminated:** API calls require credentials. |
| National Kindergarten Register, National School Register, National Register of Education, National Occupation Register, National Pupil Register (NBR, NSR, NFR, NOR, NPR) / Directorate for Education | Documented API specs: `https://data-nbr.udir.no/swagger/v4/swagger.json`, `https://data-nsr.udir.no/swagger/v4/swagger.json`, `https://data-nfr.udir.no/swagger/v4/swagger.json`, `https://data-nor.udir.no/swagger/v4/swagger.json`, `https://data-npr.udir.no/swagger/v4/swagger.json` | NLOD 2.0 metadata; each inspected v4 spec declares global Basic authentication. | Each corresponding host's `/robots.txt`: **404**, empty body; no rules. | **Eliminated:** credentials required despite the catalogue access label. NBR is detailed above; the same gate result applies to the four related registers. |
| Patent, trademark and design register / Norwegian Industrial Property Office | [API service metadata](https://data.norge.no/en/data-services/4fa0433f-2fa8-3235-8c8b-f0a577e25c48/api-for-the-trademark-patent-and-designregister-in-norway); [access instructions](https://developer.patentstyret.no/docs-get-access) | DataNorge lists NLOD 2.0, but the official developer portal requires account creation, sign-in, product subscription and an API key. | `developer.patentstyret.no/robots.txt`: **404** (HTML 404 page); no robots rules. | **Eliminated:** account/subscription/API key required. |
| Konkursregisteret / Norwegian Register Centre | DataNorge lists **zero registered APIs**. The XML subscription is documented [here](https://www.brreg.no/bruke-data-fra-bronnoysundregistrene/abonnement/abonnement-pa-kunngjoringer-i-xml-format/). | DataNorge classifies the dataset **Non-public access**; XML distribution has no catalogue licence and requires a signed agreement. The separate free daily/weekly service sends email links, not XML. | `w2.brreg.no/robots.txt`: **200**; exact relevant lines quoted below. | **Eliminated:** publisher classifies it non-public; announcement path disallowed; XML requires agreement and has no stated licence. |

## Result

Several Fisheries Directorate APIs pass the access checks. Recommend exactly one for a possible follow-up: **Official Aquaculture Register** (`pub-aqua`). It has the strongest register fit among the passing candidates and its official service metadata identifies NLOD 2.0 and public access. No integration code, fixture, data request or new host was added in this review. The other Fisheries Directorate APIs are documented above so the selection is auditable; they are not bundled into a proposed integration.

## Exact live robots excerpts

Fetched 2026-11-20 04:26 UTC. Hosts returning an empty `404` body (Fisheries Directorate API; Udir NBR/NSR/NFR/NOR/NPR; Patentstyret developer portal) publish no lines to quote. `openapi.arbeidstilsynet.no` returned `403` and an XML access-denied body, not a robots file. The following matching lines were returned by 200 responses:

`https://sgregister.dibk.no/robots.txt`:

```text
User-agent: *
Disallow: /api/
```

`https://www.arbeidstilsynet.no/robots.txt`:

```text
User-agent: *
Sitemap: https://www.arbeidstilsynet.no/sitemap.xml
```

`https://w2.brreg.no/robots.txt`:

```text
User-agent: *
Disallow: /kunngjoring/
```

## Evidence references

- [Official Fisheries Directorate API catalog](https://api.fiskeridir.no/catalog/)
- [DataNorge: Official Aquaculture Register dataset](https://data.norge.no/en/datasets/76ac1294-3732-35bc-8732-0b6584ac8970/offentlig-api-for-akvakulturregister)
- [DataNorge: Operational Aquaculture Rights service](https://data.norge.no/nb/data-services/3ad8c19c-6591-3217-be54-77b616d77f3e/offentlig-api-for-operasjonelle-akvakulturrettigheter)
- [DataNorge: Konkursregisteret access and distributions](https://data.norge.no/en/datasets/eb8773a6-5b76-3af6-b747-6145d55f6b95/konkursregisteret)
- [Brreg XML subscription terms](https://www.brreg.no/bruke-data-fra-bronnoysundregistrene/abonnement/abonnement-pa-kunngjoringer-i-xml-format/)
- [Brreg free announcement subscription](https://www.brreg.no/bruke-data-fra-bronnoysundregistrene/abonnement/abonnement-pa-kunngjoringer/)
- [Patentstyret API access instructions](https://developer.patentstyret.no/docs-get-access)
