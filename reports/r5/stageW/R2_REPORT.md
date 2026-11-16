# R2 local identity rarity table

Build input: the existing official enheter snapshot, SHA-256 5b0df27c5567a655320b8dfb8975049b76c46ba93d748a8a763f8db7050b7862. It contains 1,177,860 distinct valid entity identifiers; the evaluation universe is a smaller 411,160-company subset. No data from another repository or entry is used. Brønnøysundregistrene / Enhetsregisteret, NLOD 2.0 attribution and source URL/hash, local file modification date and actual UTC build time are embedded in the bundle and rarity.json. File modification time is not claimed to be the registry's effective date.

The gzip bundle (wrapper mtime fixed at zero) is 10,853,314 bytes; SHA-256 900882536a574656025214e5163174812d4d4234e4922b9e452e86882b530d07. The builder accepts an optional official underenheter snapshot. None is available locally; the failed robots checks and explicit missing-parent limitation are documented in W0_REPORT.md. Counts do not pretend to include missing subunit data.

| Key | Shared by 1 entity | 2 | 3–4 | ≥5 |
|---|---:|---:|---:|---:|
| Phone/mobile | 363,794 | 33,024 | 8,123 | 2,135 |
| Full email | 277,476 | 11,472 | 2,337 | 836 |
| Corporate email domain | 76,131 | 9,334 | 3,771 | 2,589 |
| Normalized name key | 1,095,275 | 34,983 | 2,717 | 577 |

Phone/mobile collapse to eight Norwegian digits, with +47/0047 normalization and foreign-prefix rejection. The same phone in both fields counts once per entity. Full emails are case folded and validated as full addresses; domain counts exclude the project's free-mail/ISP providers and their subdomains. Name keys fold accents/æ/ø, remove enumerated legal forms and filler words, then sort tokens. Duplicate input rows and repeated entity/key pairs across snapshots count once. Empty/invalid keys do not acquire counts. A unique key is a measured frequency, never ownership proof.

Rebuild: `.venv/Scripts/python.exe scripts/build_rarity_table.py --enheter <HOME>/Downloads/Signalpost/state/downloads/registry.csv --report reports/r5/stageW/rarity.json`. Use `--underenheter PATH` only for an available official snapshot. Runtime `signalpost.web.rarity.count` lazily loads the local bundled table; it never fetches, performs DNS, calls a model, or supplies a fallback on missing/corrupt data. No runtime proof rule consumes the counts in these foundation stages. This preserves the instruction not to add a proof tier.

Tests cover normalization, free-mail exclusion, phone/mobile and cross-snapshot entity deduplication, shared-domain/name counts, missing keys, local reload and corrupt/missing bundle failure. Full-suite gates and trial failures are retained separately; only a green full gate authorizes the stage commit. Paid cost $0; no push.

Exact committed-tree verification: isolated local worktree at 81a76b8d, application import proven to use that worktree, full pytest 964 passed in 162.05 seconds. Main working-tree full 979-test gate also passed before commit; its extra tests covered pending R4. Receipt: r2_committed_tree_check.json; log: pytest-R2-committed-tree.txt. No network dependency install.
