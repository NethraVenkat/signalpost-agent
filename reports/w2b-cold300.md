# Declared NAV index: cold 300 gate

Seed 20261015, 300 input records, fresh empty state directory, 2,400-second budget. The shipped discovery index is explicitly supplied; no runtime response cache was copied. This is a cold indexed run, not a cold full-history download.

| Measurement | Result |
|---|---:|
| Index compressed bytes / age | 403,768 / 0.048664 days |
| Active index ads / distinct employers | 9,015 / 5,769 |
| Disk-seeded / freshly fetched index entries | 6,791 / 2,224 |
| Failed index details | 0 |
| Forward feed pages / seconds | 2 / 10.843 |
| Decoded feed MB / seconds per page | 0.016817 / 5.4215 |
| Feed complete | true |
| Candidates / live detail responses | 2 / 2 |
| Published ads / companies with ads | 2 / 1 |
| Hiring failed | 0 / 300 (0%) |
| NAV total / cap | 137.922 / 900 seconds |
| Batch runtime | 250.359 seconds |
| HTTP requests | 1,522 |
| Handled / unhandled exceptions / deadline hits | 0 / 0 / 0 |
| Site bytes / largest HTML | 16,422,320 / 82,260 |

Index version `nav-20261014T042640.758720Z-v1`, built 2026-10-14T04:26:40.758720Z. Both published ads were independently checked against their live stored detail responses: exact UUID, employer parent/listed-subunit membership, active status, dates, title, source URL, hash, verbatim span and declared-index provenance. Two supported matches, zero doubtful matches; the audit CSV is retained privately. Stored index entries cannot themselves support a published fact.

The first detail started at 135.422 seconds after verified subunit scopes became ready. No qualifying detail started during the short forward read. Website work was occupying registry company slots; separate registry and website worker semaphores now have a regression test proving a slow website cannot hold the next company's registry slot. This run predates that scheduling fix. Its measured 137.922 seconds is retained; it does not establish the later cold 1,000-company target of NAV at most 120 seconds or batch at most 1,200 seconds.

Fourteen companies have unusable fallback names. The declared baseline is orgnr-keyed; name matching only nominates new forward-feed items lacking employer orgnr. Unknown trading names remain a discovery risk. Absence requires a loaded index, completed forward feed, completed company/subunit scope and every discovered candidate checked. Partial coverage never becomes `not_available`. No field projection is documented by NAV; projection savings are zero MB. MB denotes decoded decimal response-body size, not compressed wire bytes.
