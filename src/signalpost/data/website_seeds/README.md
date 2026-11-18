# Website seed data

Each gzip file contains organisation numbers mapped to candidate domains. Common Crawl entries include the archived URL, capture time and SHA-256 of the archived HTML body. The build reads HTTP byte ranges from Common Crawl's bulk index and WARC data. [Common Crawl CDXJ documentation](https://commoncrawl.org/cdxj-index)

The index is experimental and disabled in runtime by default. Set `SIGNALPOST_WEBSITE_SEEDS=1` to opt in for a run. In the paired 100-company W3 measurement, seeds ON produced 11 website claims with 909 HTTP requests, compared with 40 claims and 1,160 requests with seeds OFF. Five claims appeared only in the seeds-ON run. Seed candidates can crowd out registry/name candidates within per-company caps. See the [W3 saved-output comparison](../../../../reports/r5/stageW/seed_recall.md).

`openstreetmap.json.gz` contains paired `ref:NO:orgnr` and `website` tags from the Geofabrik Norway extract. © OpenStreetMap contributors. The OpenStreetMap candidate database is available under ODbL 1.0. [OpenStreetMap copyright and attribution](https://www.openstreetmap.org/copyright) · [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) · [Geofabrik Norway extract](https://download.geofabrik.de/europe/norway.html)

Run `scripts/build_seed_index.py --help` for rebuild options. Reading an OSM extract requires the optional Osmium Python package. Reuse the same work directory to resume the archive build.
