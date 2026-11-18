# HC1 saved social replay

The replay uses the recorded website proof pages and contact-page receipts from P2 and P3g. It verifies their hashes locally and reapplies the current social publication rules to the saved URLs.

| Sample | Original URLs | Retained | Withheld | Human-correct retained | Human-correct withheld |
|---|---:|---:|---:|---:|---:|
| P2 | 16 | 10 | 6 | 3 | 1 |
| P3g | 40 | 30 | 10 | 8 | 2 |

Both human-confirmed wrong links were withheld. Three human-confirmed correct links were also withheld under the same shared-site rule. The table lists every withheld URL.

| Sample | Organisation | Saved URL | Human verdict | Original automated verdict | Reason |
|---|---|---|---|---|---|
| P3g | 927525399 · WOODWORKS! CLUSTER | `https://www.facebook.com/arenaskog` | wrong | wrong | Different visible profile on the same platform · [https://www.facebook.com/woodworkscluster](<https://woodworkscluster.no/>) |
| P3g | 991323848 · TROLLHEIM AS | `https://facebook.com/TrollheimAS` | wrong | doubtful | Visible registered name at the same registered domain · [trollheim kurs og kompetanse](<https://trollheim.no/kontakt/>) |
| P2 | 827458392 · SMARTE HODER AS | `https://www.instagram.com/smartehoderas` | unreviewed | correct | Another full registered legal name appears on the site · [Control Cutter AS](<https://www.smarte-hoder.no/>) |
| P2 | 827458392 · SMARTE HODER AS | `https://www.linkedin.com/company/smarte-hoder-as` | unreviewed | correct | Another full registered legal name appears on the site · [Control Cutter AS](<https://www.smarte-hoder.no/>) |
| P2 | 927361426 · L TERRASSE AS | `https://www.facebook.com/Lterrasseno-101890795424991` | unsure | wrong | JSON-LD-only handle lacks a distinctive registry-name token |
| P2 | 932296047 · KURVE REGNSKAP AS | `https://instagram.com/kurveregnskap` | unreviewed | correct | Another full registered legal name appears on the site · [Bratås AS](<https://kurveregnskap.no/>) |
| P2 | 932296047 · KURVE REGNSKAP AS | `https://www.facebook.com/kurveregnskap` | unreviewed | correct | Another full registered legal name appears on the site · [Bratås AS](<https://kurveregnskap.no/>) |
| P2 | 971050756 · ACCELLA SOLUTIONS AS | `https://www.linkedin.com/company/petroonline-as` | correct | wrong | Another full registered legal name appears on the site · [Verdi Media Norge AS](<https://accella.no/>) |
| P3g | 912503259 · OFFICEAID AS | `https://www.facebook.com/officeaid.no` | correct | wrong | Another full registered legal name appears on the site · [Falck Norge AS](<https://www.officeaid.no/kontakt-oss>) |
| P3g | 912503259 · OFFICEAID AS | `https://www.instagram.com/officeaid.no` | unsure | wrong | Another full registered legal name appears on the site · [Falck Norge AS](<https://www.officeaid.no/kontakt-oss>) |
| P3g | 912766349 · CUBASTOLEN AS | `https://www.facebook.com/cubastolen` | unreviewed | correct | Another full registered legal name appears on the site · [Staas AS](<https://cubastolen.no/pages/kjops-og-leveringsvilkar>) |
| P3g | 916364806 · TT EXPRESS AS | `https://www.facebook.com/ttexpressas` | unsure | wrong | JSON-LD-only handle lacks a distinctive registry-name token |
| P3g | 975339688 · DIGERNES AS | `https://www.linkedin.com/company/digernes-as` | unreviewed | correct | Another full registered legal name appears on the site · [Oculos AS](<https://www.digernes.no/om-oss/pernsonvernerklaering>) |
| P3g | 990825076 · PECULIUM AS | `https://www.instagram.com/peculium_as` | unsure | doubtful | Another full registered legal name appears on the site · [Texicon AS](<https://peculium.no/>) |
| P3g | 991323848 · TROLLHEIM AS | `https://twitter.com/TrollheimAS` | correct | doubtful | Visible registered name at the same registered domain · [trollheim kurs og kompetanse](<https://trollheim.no/kontakt/>) |
| P3g | 991323848 · TROLLHEIM AS | `https://www.instagram.com/trollheimas` | unsure | doubtful | Visible registered name at the same registered domain · [trollheim kurs og kompetanse](<https://trollheim.no/kontakt/>) |

The three human-confirmed losses are Accella’s LinkedIn (another registered firm in the site credit), OfficeAid’s Facebook (another registered firm named in a product category), and Trollheim’s Twitter (the same site names a second entity registered at that domain). The saved pages do not supply the exact-organisation profile tie required on a shared site.

[Pinned human verdicts](human_reviews.json) · [Every replay decision and proof excerpt](replay.json)
