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

# Useful documented fields omitted before R5. Core identity fields, EXTRA and
# GROUPS above already retain dates, sector, registers, NACE1-3 and capital.
# Transport metadata (_links/respons_klasse) is deliberately not a business fact.
ADDITIONAL = {
    'deletion_date': ('slettedato', 'date'),
    'forced_closure_missing_deletion_date': ('tvangsavvikletPgaManglendeSlettingDato', 'date'),
    'home_country_registration_number': ('registreringsnummerIHjemlandet', 'text'),
    'foreign_register_name': ('utenlandskRegisterNavn', 'text'),
    'foreign_register_address': ('utenlandskRegisterAdresse', 'object'),
    'legislation_country': ('underlagtLovgivningLand', 'text'),
    'legislation_country_code': ('underlagtLovgivningLandKode', 'text'),
    'home_country_organisation_form': ('foretaksformIHjemlandet', 'object'),
    'voluntary_vat_descriptions': ('frivilligMvaRegistrertBeskrivelser', 'texts'),
    'historical_names': ('historiskeNavn', 'records'),
    'registry_annotations': ('paategninger', 'records'),
}

# Separate attributes that were lost or merged into subunits.unit.*. Keep the
# compound core record for backward compatibility, but never infer its address
# type or copy the first NACE code into a missing second/third code.
SUBUNIT_ADDITIONAL = {
    'physical_address': ('beliggenhetsadresse', 'object'),
    'nace1': ('naeringskode1', 'object'),
    'nace2': ('naeringskode2', 'object'),
    'nace3': ('naeringskode3', 'object'),
    'employees': ('antallAnsatte', 'employees'),
    'closure_date': ('nedleggelsesdato', 'date'),
    'deletion_date': ('slettedato', 'date'),
    'vat_registration_date': ('registreringsdatoMerverdiavgiftsregisteret', 'date'),
    'vat_registry_record_date': ('registreringsdatoMerverdiavgiftsregisteretEnhetsregisteret', 'date'),
    'voluntary_vat_registration_date': ('registreringsdatoFrivilligMerverdiavgiftsregisteret', 'date'),
    'voluntary_vat_descriptions': ('frivilligMvaRegistrertBeskrivelser', 'texts'),
    'historical_names': ('historiskeNavn', 'records'),
}

DROPPED_BEFORE_R5 = {
    'entity': tuple(path for path, _ in ADDITIONAL.values()),
    'subunit': tuple(path for path, _ in SUBUNIT_ADDITIONAL.values()),
    'csv_address_components': ('forretningsadresse.landkode', 'postadresse.landkode', 'organisasjonsform.utgaatt'),
    'intentionally_excluded': ('_links', 'respons_klasse', 'unknown/undocumented fields'),
}


def reported(value, kind, *, csv=False):
    """Validate reported values without coercing false/zero into missing data."""
    from datetime import date
    import json
    if value is None or value == '' or value == [] or value == {}: return None
    if kind == 'bool': return boolean(value)
    if kind == 'employees':
        if csv and isinstance(value, str) and value.isascii() and value.isdigit(): value = int(value)
        if type(value) is not int or value < 0: raise ValueError('invalid employee count')
    elif kind == 'date':
        if not isinstance(value, str): raise ValueError('invalid date')
        date.fromisoformat(value)
    elif kind == 'text':
        if not isinstance(value, str): raise ValueError('invalid text')
    elif kind in {'object', 'texts', 'records'}:
        if csv and isinstance(value, str): value = json.loads(value)
        if kind == 'object' and not isinstance(value, dict): raise ValueError('invalid object')
        if kind in {'texts', 'records'}:
            element = str if kind == 'texts' else dict
            if not isinstance(value, list) or not all(isinstance(v, element) for v in value): raise ValueError('invalid list')
        # Drop HAL navigation only; no unknown nested ownership is inferred.
        if isinstance(value, dict): value = {k:v for k,v in value.items() if k != '_links'}
    return value


def publish_additional(section, source, org, family, prefix, data, fields, locator='', *, csv=False):
    from .extract import add
    from ..budget import SourceFailure
    from ..models.envelope import Error
    for name, (key, kind) in fields.items():
        actual = next((k for k in data if isinstance(k, str) and k.casefold() == key.casefold()), None)
        if actual is None: continue  # No optional source field was supplied.
        value = data[actual]
        if name == 'employees' and boolean(data.get('harRegistrertAntallAnsatte')) is False: value = None
        error = False
        try: value = reported(value, kind, csv=csv)
        except (ValueError, TypeError, SourceFailure): value, error = None, True
        pointer = f'row:{org}/column:{actual}' if csv else locator + '/' + actual
        add(section, source, org, family, prefix + name, value, pointer,
            effective=value if kind == 'date' else None,
            availability='failed' if error else None, method='signalpost.registry_fields.v2')
        if error:
            section.claims[-1].reasons['value'] = 'Source field has an unsupported type or invalid value; no value inferred.'
            section.errors.append(Error(section=family, code='invalid_registry_field', message=prefix+name))


def boolean(value):
    from ..budget import SourceFailure
    if value is None:return None
    if isinstance(value,bool):return value
    if isinstance(value,str) and value.casefold() in {'true','false'}:return value.casefold()=='true'
    raise SourceFailure('malformed_flag')
