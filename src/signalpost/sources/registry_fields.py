"""Reported official attributes shared by JSON and CSV identity extractors."""
EXTRA = {
    'employees_reported':('harRegistrertAntallAnsatte','bool'),
    'employee_count_registration_date':('registreringsdatoAntallAnsatteEnhetsregisteret','text'),
    'employee_count_nav_registration_date':('registreringsdatoantallansatteNAVAaregisteret','text'),
    'registered_email':('epostadresse','text'),'registered_phone':('telefon','text'),
    'registered_mobile':('mobil','text'),'language_form':('maalform','text'),
    'registered_in_vat':('registrertIMvaRegisteret','bool'),
    'registered_in_business_register':('registrertIForetaksregisteret','bool'),
    'registered_in_voluntary_register':('registrertIFrivillighetsregisteret','bool'),
    'registered_in_foundations_register':('registrertIStiftelsesregisteret','bool'),
    'registered_in_party_register':('registrertIPartiregisteret','bool'),
    'vat_registry_record_date':('registreringsdatoMerverdiavgiftsregisteretEnhetsregisteret','text'),
    'voluntary_vat_registration_date':('registreringsdatoFrivilligMerverdiavgiftsregisteret','text'),
    'voluntary_register_registration_date':('registreringsdatoFrivillighetsregisteret','text'),
    'business_register_registration_date':('registreringsdatoForetaksregisteret','text'),
    'party_register_registration_date':('registreringsdatoPartiregisteret','text'),
    'articles_date':('vedtektsdato','text'),'bankruptcy_date':('konkursdato','text'),
    'liquidation_date':('underAvviklingDato','text'),
    'forced_dissolution':('underTvangsavviklingEllerTvangsopplosning','bool'),
    'forced_dissolution_missing_ceo_date':('tvangsopplostPgaManglendeDagligLederDato','text'),
    'forced_dissolution_missing_auditor_date':('tvangsopplostPgaManglendeRevisorDato','text'),
    'forced_dissolution_missing_accounts_date':('tvangsopplostPgaManglendeRegnskapDato','text'),
    'forced_dissolution_board_date':('tvangsopplostPgaMangelfulltStyreDato','text'),
    'foreign_insolvency_date':('underUtenlandskInsolvensbehandlingDato','text'),
    'reconstruction_date':('underRekonstruksjonsforhandlingDato','text'),
    'audit_opt_out_date':('fravalgRevisjonDato','text'),
    'audit_opt_out_decision_date':('fravalgRevisjonBeslutningsDato','text'),
    'part_of_group':('erIKonsern','bool'),'parent_organisation_number':('overordnetEnhet','text'),
}
GROUPS = {'institutional_sector':('institusjonellSektorkode',('kode','beskrivelse')),
          'support_unit_code':('hjelpeenhetskode',('kode','beskrivelse')),
          'registered_capital':('kapital',('belop','antallAksjer','type','bundet','valuta','innbetalt','fulltInnbetalt','innfortDato'))}


def boolean(value):
    from ..budget import SourceFailure
    if value is None:return None
    if isinstance(value,bool):return value
    if isinstance(value,str) and value.casefold() in {'true','false'}:return value.casefold()=='true'
    raise SourceFailure('malformed_flag')
