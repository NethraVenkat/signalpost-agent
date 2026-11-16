# Stage S (exact-ID official sources): identity items vs P0 re-baseline

Identity items = official websites, social profiles and public brand names (stage X definitions). Compared per seed with `reports/r5/stageP0rb/seed<seed>/counts.json`. Stage S sources publish official-record facts (state aid, research projects, licences, food inspections), not identity items, so no identity item is expected to change from Stage S itself.

## Added

None in any of the six samples.

## Removed

- seed 20261017: 814635562 BELLAS AS - brand `Bellas Burrito`
- seed 20261017: 814635562 BELLAS AS - website `https://www.bellasburrito.com`

Cause: live variation, not Stage S. In this run the company's website section is `not_available` with reason code `robots` (run observation in the saved envelope), so the registry-declared site was not fetched and the site-declared brand that depends on it was not published. The re-baseline fetched it. Stage S code does not touch website discovery.

## New official-record items (not identity items)

| seed | state aid | research | licences | inspections | companies (sa/r/l/i) |
|---|---|---|---|---|---|
| 20261017 | 51 | 0 | 11 | 4 | 8/0/3/2 |
| 20261113 | 71 | 1 | 1 | 3 | 10/1/1/2 |
| 20261114 | 62 | 1 | 1 | 1 | 7/1/1/1 |
| 20261115 | 31 | 0 | 10 | 0 | 6/0/2/0 |
| 20261116 | 76 | 7 | 3 | 7 | 10/3/2/4 |
| 20261117 | 46 | 1 | 0 | 27 | 7/1/0/1 |
