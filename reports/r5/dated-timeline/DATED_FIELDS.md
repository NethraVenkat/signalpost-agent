# Dated-field inventory from current code

This inventory distinguishes available date-bearing output from the allowlist used by S2. It does not treat retrieval times as events. No new source access was used.

| Published claim field / value path | Precision | S2 treatment |
|---|---|---|
| `identity.founding_date` -> `value` | day or explicit zoned timestamp (as supplied) | Founding date recorded |
| `identity.registration_date` -> `value` | day or explicit zoned timestamp (as supplied) | Enhetsregisteret registration date recorded |
| `identity.vat_registration_date` -> `value` | day or explicit zoned timestamp (as supplied) | VAT registration date recorded |
| `accounts.filed_years` -> `value[]` | year | Accounting year with a filed copy recorded |
| `accounts.filed_year.*` -> `value` | year | Accounting year with a filed copy recorded |
| `roles.role.*` -> `from_date,last_changed` | day or explicit zoned timestamp (as supplied) | Role record start date / last changed date recorded |
| `registry_change.roles.*` -> `date` | day or explicit zoned timestamp (as supplied) | Registry role-update publication recorded |
| `state_aid.award.*` -> `date` | day or explicit zoned timestamp (as supplied) | State-aid award date recorded |
| `procurement.award.*` -> `date` | day or explicit zoned timestamp (as supplied) | Contract award date recorded |
| `status_events.event.*` -> `date` | day or explicit zoned timestamp (as supplied) | Registry event publication recorded |
| `signature.* / prokura.*` -> `none` | none | No published change date; omitted |

Other date-bearing fields already emitted by extractors (excluded from this task's permitted event categories unless listed above):

| Published field / path | Source/code | Precision / distinction |
|---|---|---|
| `identity.employee_count_registration_date` | registry_fields.EXTRA: `registreringsdatoAntallAnsatteEnhetsregisteret` | date-shaped text; day when valid |
| `identity.employee_count_nav_registration_date` | registry_fields.EXTRA: `registreringsdatoantallansatteNAVAaregisteret` | date-shaped text; day when valid |
| `identity.vat_registry_record_date` | registry_fields.EXTRA: `registreringsdatoMerverdiavgiftsregisteretEnhetsregisteret` | date-shaped text; day when valid |
| `identity.voluntary_vat_registration_date` | registry_fields.EXTRA: `registreringsdatoFrivilligMerverdiavgiftsregisteret` | date-shaped text; day when valid |
| `identity.voluntary_register_registration_date` | registry_fields.EXTRA: `registreringsdatoFrivillighetsregisteret` | date-shaped text; day when valid |
| `identity.business_register_registration_date` | registry_fields.EXTRA: `registreringsdatoForetaksregisteret` | date-shaped text; day when valid |
| `identity.party_register_registration_date` | registry_fields.EXTRA: `registreringsdatoPartiregisteret` | date-shaped text; day when valid |
| `identity.articles_date` | registry_fields.EXTRA: `vedtektsdato` | date-shaped text; day when valid |
| `identity.bankruptcy_date` | registry_fields.EXTRA: `konkursdato` | date-shaped text; day when valid |
| `identity.liquidation_date` | registry_fields.EXTRA: `underAvviklingDato` | date-shaped text; day when valid |
| `identity.forced_dissolution_missing_ceo_date` | registry_fields.EXTRA: `tvangsopplostPgaManglendeDagligLederDato` | date-shaped text; day when valid |
| `identity.forced_dissolution_missing_auditor_date` | registry_fields.EXTRA: `tvangsopplostPgaManglendeRevisorDato` | date-shaped text; day when valid |
| `identity.forced_dissolution_missing_accounts_date` | registry_fields.EXTRA: `tvangsopplostPgaManglendeRegnskapDato` | date-shaped text; day when valid |
| `identity.forced_dissolution_board_date` | registry_fields.EXTRA: `tvangsopplostPgaMangelfulltStyreDato` | date-shaped text; day when valid |
| `identity.foreign_insolvency_date` | registry_fields.EXTRA: `underUtenlandskInsolvensbehandlingDato` | date-shaped text; day when valid |
| `identity.reconstruction_date` | registry_fields.EXTRA: `underRekonstruksjonsforhandlingDato` | date-shaped text; day when valid |
| `identity.audit_opt_out_date` | registry_fields.EXTRA: `fravalgRevisjonDato` | date-shaped text; day when valid |
| `identity.audit_opt_out_decision_date` | registry_fields.EXTRA: `fravalgRevisjonBeslutningsDato` | date-shaped text; day when valid |
| `identity.deletion_date` | registry_fields.ADDITIONAL: `slettedato` | day |
| `identity.forced_closure_missing_deletion_date` | registry_fields.ADDITIONAL: `tvangsavvikletPgaManglendeSlettingDato` | day |
| `subunits.detail.{orgnr}.closure_date` | registry_fields.SUBUNIT_ADDITIONAL: `nedleggelsesdato` | day |
| `subunits.detail.{orgnr}.deletion_date` | registry_fields.SUBUNIT_ADDITIONAL: `slettedato` | day |
| `subunits.detail.{orgnr}.vat_registration_date` | registry_fields.SUBUNIT_ADDITIONAL: `registreringsdatoMerverdiavgiftsregisteret` | day |
| `subunits.detail.{orgnr}.vat_registry_record_date` | registry_fields.SUBUNIT_ADDITIONAL: `registreringsdatoMerverdiavgiftsregisteretEnhetsregisteret` | day |
| `subunits.detail.{orgnr}.voluntary_vat_registration_date` | registry_fields.SUBUNIT_ADDITIONAL: `registreringsdatoFrivilligMerverdiavgiftsregisteret` | day |
| `accounts.*.reporting_period.period_start/period_end/fiscal_year` | regnskap.emit | day / year; accounting period, not filing/submission date |
| `identity.latest_submitted_accounts` | brreg_enhet / bulk_registry | year; registry reports accounting year, not actual filing day |
| `group.parent/subsidiary.*.date` | brreg_corporate: `dato` | day; group relationship date outside S2 input scope |
| `gleif.record.initial_registration_date/next_renewal_date` | exact_public | date/time as published; LEI registration/renewal, not company timeline input |
| `research.project.*.date/start_year/end_year` | exact_official | year (RCN) or day (SkatteFUNN decision); excluded by S2 scope |
| `licences.*.registered_date` | exact_official | day; licence registration, excluded by S2 scope |
| `inspections.inspection.*.date` | exact_official | day; inspection date, excluded by S2 scope |
| `hiring.job.*.published/expires` | NAV / careers | explicit timestamp when present; excluded by S2 scope |
| `dated_item.*.date` | company public-activity extraction | published date precision as supplied; excluded by S2 scope |
| `subunits.unit.*` ancillary registered dates / `roles.detail.*.from_date` through source metadata | registry subunit/role fields | only role `from_date/last_changed` consumed; no subunit event date inferred |

S1 retains `status_events.event.*.date` with API-publication semantics. Existing generic `registry_change.*.date` contains entity/subunit or role feed publication; S2 consumes role feed dates and S1 entity dates, not two views of the same entity event. Signature/prokura responses supply rules/combinations without a published change date; no retrieval timestamp is promoted into a change date.

Implementation checks ISO year, exact calendar day and explicitly zoned timestamp, preserves original representation, labels precision, sorts oldest first using a stable date/precision/field/claim-ID/text tie-break. Year-only entries sort before dated entries in the same year by an explicit coarse-date convention; no January 1 is added.
