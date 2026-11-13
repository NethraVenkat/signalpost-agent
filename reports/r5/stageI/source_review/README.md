# Official source review (2026-11-13)

The public Brreg OpenAPI 1.1.16 explicitly lists the annual-accounts available-copy years endpoint; the bounded development probe returned 200 without authentication. The official catalogue links the open data distribution to NLOD 2.0. No subscriptions, PDFs, logins or paid calls are used. These are source documentation/access checks, not evaluator company runs.

- OpenAPI: https://data.brreg.no/regnskapsregisteret/regnskap/v3/api-docs (0.body)
- Available-copy probe: https://data.brreg.no/regnskapsregisteret/regnskap/aarsregnskap/kopi/923609016/aar (1.body)
- Catalogue and licence: https://data.norge.no/en/datasets/8132460c-91ab-3950-a54b-a54ee20c62e9/regnskapsregisteret and https://data.norge.no/nlod/no/2.0
- Robots lookup: two attempts disconnected (RemoteProtocolError); no permission inferred from that error. Requests use the existing explicit official machine-API allowlist and host/global limiter. Website robots errors still refuse crawling.

receipts.json records URLs, statuses/errors and hashes. The robots lookup failed before its body could be saved. API body files contain official schema/data only, no application code was copied.
