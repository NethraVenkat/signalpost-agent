# W3 seed index recall hand-check

## Valid paired measurement

The network-enabled reruns completed against the same frozen 100-company cohort and 2026-11-16 registry subset. Each run used a fresh per-run state directory and exactly seven evaluator CLI flags. The default-on run and the `SIGNALPOST_WEBSITE_SEEDS=0` run used separate state directories. The saved execution receipts and verification results are in `seed_recall_on_retry/` and `seed_recall_off_retry/`.

- Cohort SHA-256: `86ad22303145a2efca1980dcc63678cb3192afcbd4dc9e3959e633a1ed02b79a` (100 organizations, CC 54, OSM 46).
- Registry subset SHA-256: `9613083ec10d124ff6f0a009ec210e2a26ca7a9a4ec0ef4890653e11146e2331` (100 rows).
- Seeds on: 332.609 seconds, 11 published website claims, 909 HTTP requests, 100 verified terminal envelopes, 100 complete briefing contracts, site verification passed, largest profile 249,116 bytes.
- Seeds off: 336.688 seconds, 40 published website claims, 1,160 HTTP requests, 100 verified terminal envelopes, 100 complete briefing contracts, site verification passed, largest profile 247,993 bytes.
- Website claims present only in seeds-on: 5. These are listed below with their saved evidence excerpts. The on/off total counts differ because each timed website pass can verify a different set of candidates.

The two earlier sandbox-blocked W3 runs, `seed_recall_on/` and `seed_recall_off/`, are **INVALID** for measuring recall. They ended at the deadline with zero published websites while website requests were blocked by the execution environment. Their results are not used in the comparison below.

The requested three-check network preflight passed before this report was written. Brreg API returned HTTP 200, `https://www.in-bo.no/` returned HTTP 200, and DNS resolved `data.brreg.no` to `195.43.63.68` and `2001:678:f0b:b::46`.

## Seed-only websites for human hand-check

Automated-doubtful entries are first.

1. **833270222 — AS HVERDAG M.M. — https://ashverdag.no**
   - Proof tier: `VERIFIED`; proof type: `orgnr_on_page`.
   - Seed source tag: `seed_commoncrawl`.
   - Relationship note: `group_site`.
   - Saved excerpt from the own-site footer: “Org.nr. 833 270 222”. The same saved page says “Marius er eier og gründer av Poleringskongen AS, som han har drevet i 19 år.”
   - Evidence SHA-256: `03e32d28699b3005de834d22f5a0861d5fa96b7fc75d3a31f3b1c0dc9cdd75c5`.

2. **917219354 — KNUDSEN RØR AS — https://berederekspressen.no**
   - Proof tier: `VERIFIED`; proof type: `orgnr_on_page`.
   - Seed source tag: `seed_commoncrawl`.
   - Saved excerpt from the terms page: “Org.nr: 917 219 354”.
   - Evidence SHA-256: `6b4f1f27b128aa7b02cb88894d4eb8b146e4688ba881c05f1732420e5f6fc29d`.

3. **937170653 — WANGEN SOFTWARE SOLUTIONS AS — https://bryllup.no**
   - Proof tier: `VERIFIED`; proof type: `jsonld_vatid`.
   - Seed source tag: `seed_commoncrawl`.
   - Saved excerpt from the own-site page: “Wangen Software Solutions AS · Org.nr 937 170 653”.
   - Evidence SHA-256: `d2896e09bd905e402405224ce472fedc137c0ba061cf56aa2e4bf12644e31da5`.

4. **989011359 — DEKORLYS Ranveig Eide Langørgen — https://dekorlys.no**
   - Proof tier: `VERIFIED`; proof type: `orgnr_on_page`.
   - Seed source tag: `seed_commoncrawl`.
   - Saved excerpt from the own-site page: “Org.nr: 989011359”.
   - Evidence SHA-256: `0dea997cb3533aa00e8bf52028fd20386c462eb7d60de0dda7ecfab0314dc17`.

5. **990742588 — AT HOME AS — https://athome.as**
   - Proof tier: `VERIFIED`; proof type: `orgnr_on_page`.
   - Seed source tag: `seed_openstreetmap`.
   - Saved excerpt from the own-site page: “Orgnr: 990742588” and “E-post: post@athome.as”.
   - Evidence SHA-256: `da8ca1dd8b7510dd27318aaefbbb29e5c85ba54f6e804b99dcc5270351d19969`.

## Verification

Both completed reruns passed the saved-run checker. They emitted 100 terminal envelopes and 100 complete briefing contracts, verified all source blobs, passed schema and offline site checks, and kept the largest profile below 250,000 bytes. No 500-company run was started.
