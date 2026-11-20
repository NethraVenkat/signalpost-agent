# Enhetsregisteret field coverage audit

Schema basis: Brønnøysundregistrene's official [open data API documentation](https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html), section response examples for `/api/enheter/{orgnr}` and `/api/underenheter?overordnetEnhet=...` (NLOD 2.0). Nested attributes count as published when they are preserved verbatim in an evidenced compound claim; they need not be duplicated as scalar claims. Null and absent values do not create claims. `_links` are navigation metadata; `respons_klasse` is a transport discriminator.

## Enhet response fields

| Field | Published as claim? | If no, why |
|---|---|---|
| `respons_klasse` | no | Transport discriminator, not a company attribute. |
| `organisasjonsnummer` | yes | New `identity.organisation_number`, exact identity evidence. |
| `navn` | yes | `identity.legal_name`. |
| `organisasjonsform` (`kode`, `beskrivelse`, `utgaatt`) | yes | `identity.organisation_form`; nested values retained. |
| `historiskeNavn[]` (`navn`, `fraDato`, `tilDato`) | yes | `identity.historical_names`; record members retained. |
| `postadresse` (`kommune`, `landkode`, `postnummer`, `adresse[]`, `land`, `kommunenummer`, `poststed`) | yes | Postal address and location claims. |
| `forretningsadresse` (`kommune`, `landkode`, `postnummer`, `adresse[]`, `land`, `kommunenummer`, `poststed`) | yes | Business address and location claims. |
| `registrertIMvaregisteret` | yes | `identity.registered_in_vat`. |
| `maalform` | yes | `identity.language_form`. |
| `naeringskode1` (`kode`, `beskrivelse`) | yes | `identity.nace1`; nested values retained. |
| `naeringskode2` (`kode`, `beskrivelse`) | yes | `identity.nace2`; nested values retained. |
| `naeringskode3` (`kode`, `beskrivelse`) | yes | `identity.nace3`; nested values retained. |
| `hjelpeenhetskode` (`kode`, `beskrivelse`) | yes | `identity.support_unit_code`; nested values retained. |
| `underAvvikling` | yes | `identity.under_liquidation`. |
| `underAvviklingDato` | yes | `identity.liquidation_date`. |
| `registrertIStiftelsesregisteret` | yes | `identity.registered_in_foundations_register`. |
| `konkurs` | yes | `identity.bankrupt`. |
| `konkursdato` | yes | `identity.bankruptcy_date`. |
| `tvangsavvikletPgaManglendeSlettingDato` | yes | `identity.forced_closure_missing_deletion_date`. |
| `tvangsopplostPgaManglendeDagligLederDato` | yes | `identity.forced_dissolution_missing_ceo_date`. |
| `tvangsopplostPgaManglendeRevisorDato` | yes | `identity.forced_dissolution_missing_auditor_date`. |
| `tvangsopplostPgaManglendeRegnskapDato` | yes | `identity.forced_dissolution_missing_accounts_date`. |
| `tvangsopplostPgaMangelfulltStyreDato` | yes | `identity.forced_dissolution_board_date`. |
| `vedtektsdato` | yes | `identity.articles_date`. |
| `vedtektsfestetFormaal` | yes | `identity.statutory_purpose`. |
| `aktivitet` | yes | `identity.registered_activity`. |
| `paategninger[]` (`infotype`, `tekst`, `innfoertDato`) | yes | `identity.registry_annotations`; records retained. |
| `registrertIFrivillighetsregisteret` | yes | `identity.registered_in_voluntary_register`. |
| `stiftelsesdato` | yes | `identity.founding_date`. |
| `institusjonellSektorkode` (`kode`, `beskrivelse`) | yes | `identity.institutional_sector`; undocumented codes remain raw. |
| `registrertIForetaksregisteret` | yes | `identity.registered_in_business_register`. |
| `registreringsdatoEnhetsregisteret` | yes | `identity.registration_date`. |
| `hjemmeside` | yes | `identity.registered_website`. |
| `sisteInnsendteAarsregnskap` | yes | `identity.latest_submitted_accounts`. |
| `frivilligMvaRegistrertBeskrivelser[]` | yes | `identity.voluntary_vat_descriptions`. |
| `underTvangsavviklingEllerTvangsopplosning` | yes | `identity.forced_dissolution`. |
| `antallAnsatte` | yes | `identity.employees`, gated by reported-count flag. |
| `harRegistrertAntallAnsatte` | yes | `identity.employees_reported`. |
| `overordnetEnhet` | yes | `identity.parent_organisation_number`. |
| `registreringsnummerIHjemlandet` | yes | `identity.home_country_registration_number`. |
| `registreringsdatoAntallAnsatteNAVAaregisteret` | yes | `identity.employee_count_nav_registration_date`. |
| `registreringsdatoAntallAnsatteEnhetsregisteret` | yes | `identity.employee_count_registration_date`. |
| `registreringsdatoMerverdiavgiftsregisteret` | yes | `identity.vat_registration_date`. |
| `registreringsdatoMerverdiavgiftsregisteretEnhetsregisteret` | yes | `identity.vat_registry_record_date`. |
| `registreringsdatoFrivilligMerverdiavgiftsregisteret` | yes | `identity.voluntary_vat_registration_date`. |
| `registreringsdatoForetaksregisteret` | yes | `identity.business_register_registration_date`. |
| `registreringsdatoFrivillighetsregisteret` | yes | `identity.voluntary_register_registration_date`. |
| `registrertIPartiregisteret` | yes | `identity.registered_in_party_register`. |
| `registreringsdatoPartiregisteret` | yes | `identity.party_register_registration_date`. |
| `epostadresse` | yes | `identity.registered_email`. |
| `telefon` | yes | `identity.registered_phone`. |
| `mobil` | yes | `identity.registered_mobile`. |
| `erIKonsern` | yes | `identity.part_of_group`. |
| `fravalgRevisjonDato` | yes | `identity.audit_opt_out_date`. |
| `fravalgRevisjonBeslutningsDato` | yes | `identity.audit_opt_out_decision_date`. |
| `underRekonstruksjonsforhandlingDato` | yes | `identity.reconstruction_date`. |
| `underUtenlandskInsolvensbehandlingDato` | yes | `identity.foreign_insolvency_date`. |
| `kapital` (`belop`, `antallAksjer`, `type`, `bundet`, `valuta`, `innbetalt`, `fulltInnbetalt`, `innfortDato`) | yes | `identity.registered_capital`; nested values retained. |
| `foretaksformIHjemlandet` (`kode`, `beskrivelse`, `beskrivelseBokmaal`) | yes | `identity.home_country_organisation_form`; nested values retained. |
| `utenlandskRegisterNavn` | yes | `identity.foreign_register_name`. |
| `utenlandskRegisterAdresse` (`adresse`, `land`, `poststed`) | yes | `identity.foreign_register_address`; nested values retained. |
| `underlagtLovgivningLand` | yes | `identity.legislation_country`. |
| `underlagtLovgivningLandKode` | yes | `identity.legislation_country_code`. |
| `slettedato` | yes | `identity.deletion_date` plus existing `identity.deleted` status. |
| `_links.*` | no | HAL navigation links are transport metadata, not business facts. |

## Underenhet response fields

| Field | Published as claim? | If no, why |
|---|---|---|
| `respons_klasse` | no | Transport discriminator, not a company attribute. |
| `organisasjonsnummer` | yes | `subunits.unit.{orgnr}` exact subunit record. |
| `navn` | yes | `subunits.unit.{orgnr}` exact subunit record. |
| `historiskeNavn[]` (`navn`, `fraDato`, `tilDato`) | yes | `subunits.detail.{orgnr}.historical_names`. |
| `organisasjonsform` (`kode`, `beskrivelse`, `utgaatt`) | yes | `subunits.detail.{orgnr}.organisation_form`. |
| `postadresse` (address members) | yes | `subunits.detail.{orgnr}.location.postal.*` and unit record. |
| `beliggenhetsadresse` (address members) | yes | `subunits.detail.{orgnr}.location.workplace.*` and physical-address claim. |
| `registrertIMvaregisteret` | yes | `subunits.detail.{orgnr}.registered_in_vat`. |
| `naeringskode1` (`kode`, `beskrivelse`) | yes | Unit record and `subunits.detail.{orgnr}.nace1`. |
| `naeringskode2` (`kode`, `beskrivelse`) | yes | `subunits.detail.{orgnr}.nace2`, when supplied. |
| `naeringskode3` (`kode`, `beskrivelse`) | yes | `subunits.detail.{orgnr}.nace3`, when supplied. |
| `hjelpeenhetskode` (`kode`, `beskrivelse`) | yes | `subunits.detail.{orgnr}.support_unit_code`. |
| `registreringsdatoEnhetsregisteret` | yes | `subunits.detail.{orgnr}.registration_date`. |
| `hjemmeside` | yes | `subunits.detail.{orgnr}.registered_website`. |
| `frivilligMvaRegistrertBeskrivelser[]` | yes | `subunits.detail.{orgnr}.voluntary_vat_descriptions`. |
| `antallAnsatte` | yes | Unit record and `subunits.detail.{orgnr}.employees`, gated by reported-count flag. |
| `harRegistrertAntallAnsatte` | yes | Unit record and `subunits.detail.{orgnr}.employees_reported`. |
| `overordnetEnhet` | yes | New `subunits.detail.{orgnr}.parent_organisation_number`; exact requested parent is validated first. |
| `oppstartsdato` | yes | `subunits.detail.{orgnr}.start_date`. |
| `datoEierskifte` | yes | `subunits.detail.{orgnr}.ownership_change_date`. |
| `nedleggelsesdato` | yes | `subunits.detail.{orgnr}.closure_date`. |
| `slettedato` | yes | `subunits.detail.{orgnr}.deletion_date`, when supplied. |
| `registreringsdatoAntallAnsatteNAVAaregisteret` | yes | `subunits.detail.{orgnr}.nav_employee_registration_date`. |
| `registreringsdatoAntallAnsatteEnhetsregisteret` | yes | `subunits.detail.{orgnr}.employee_registration_date`. |
| `registreringsdatoMerverdiavgiftsregisteret` | yes | `subunits.detail.{orgnr}.vat_registration_date`. |
| `registreringsdatoMerverdiavgiftsregisteretEnhetsregisteret` | yes | `subunits.detail.{orgnr}.vat_registry_record_date`. |
| `registreringsdatoFrivilligMerverdiavgiftsregisteret` | yes | `subunits.detail.{orgnr}.voluntary_vat_registration_date`. |
| `epostadresse` | yes | `subunits.detail.{orgnr}.registered_email`. |
| `telefon` | yes | `subunits.detail.{orgnr}.registered_phone`. |
| `mobil` | yes | `subunits.detail.{orgnr}.registered_mobile`. |
| `_links.*` | no | HAL navigation links are transport metadata, not business facts. |

## Changes from this audit

The exact organization number is now explicit evidence-backed identity output for JSON and bulk CSV records. For subunits, `overordnetEnhet` is now emitted as a separate claim after exact parent validation; a missing or mismatched parent rejects the source response. The saved 500-company replay added 924 claims (500 identity numbers and 424 explicit parent links); 401 companies gained at least one parent-link claim. Median added claims is 2 per company across the 500. Replay used 1,000 already-saved response bodies, with network access disabled and zero new HTTP requests. The largest rebuilt profile is 234,179 bytes; the top five are recorded in `measurement.json`.

Validation: full pytest **1,512 passed**; the separate privacy guard **17 passed**. The synthetic profile-overflow test was adjusted for the new explicit identity claim and still exercises the reduced-visible-rows path under the 235,000-byte target.
