"""Exact registered recipients in Brreg's licensed, publisher-advertised CSV.

Only non-personal columns copied from our own download are bundled. No lookup
is sent to the unavailable API origin, and no names widen recipient scope.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

URL = 'https://stotte.brreg.no/nb/oppslag/stoettetildeling/totalbestand/csv'
BUNDLE = Path(__file__).resolve().parents[1] / 'data' / 'state_aid.json.gz'
KEY = 'brreg_state_aid_csv'
COLUMNS = (
    'Støttetiltaksnummer', 'Status', 'Støttetiltakstype',
    'Organisasjonsnummer støttemottaker', 'Organisasjonsnummer spesifisert støttemottaker',
    'Organisasjonsnummer støttegiver', 'Navn støttegiver', 'Tildelingsdato',
    'Tildelt beløp', 'Tildelt beløp valuta', 'Beløpsintervall fra beløp',
    'Beløpsintervall til beløp', 'Beløpsintervall valuta', 'Tilknyttet støtteordning', 'Støtteinstrument',
)


def amount(raw):
    """Publisher's decimal-comma CSV, without guessing thousands separators."""
    if not isinstance(raw, str) or not re.fullmatch(r'\d+(?:,\d+)?', raw):
        return None
    try:
        number = Decimal(raw.replace(',', '.'))
        value = int(number) if number == number.to_integral_value() else float(number)
        if not number.is_finite() or Decimal(str(value)) != number:
            return None
        return value
    except (InvalidOperation, ValueError, OverflowError):
        return None


def derive(record, org, now):
    from .exact_official import org_id, window_start
    from ..identity.orgnr import valid
    if record.get('source') != KEY:
        return None
    f = record.get('fields') or {}
    if org_id(f.get('Organisasjonsnummer støttemottaker')) != org or not valid(org):
        return None
    if f.get('Status') != 'Registrert' or f.get('Støttetiltakstype') != 'Støttetildeling med statsstøtte':
        return None
    award = f.get('Støttetiltaksnummer', '')
    giver = org_id(f.get('Organisasjonsnummer støttegiver'))
    giver_name = f.get('Navn støttegiver', '')
    if (not isinstance(award, str) or not re.fullmatch(r'\d+', award) or not giver or not valid(giver)
            or not isinstance(giver_name, str) or not giver_name.strip()):
        return None
    try:
        day = datetime.strptime(f.get('Tildelingsdato', ''), '%d.%m.%Y').date()
    except (ValueError, TypeError):
        return None
    if not window_start(now) <= day <= now.date():
        return None
    value = {'company_orgnr': org, 'award_id': award, 'date': day.isoformat(),
             'date_source': 'award date (Tildelingsdato) as registered in Brreg CSV',
             'granting_authority': giver_name, 'granting_authority_orgnr': giver,
             'label': 'State aid award', 'recipient_scope': 'registered recipient; amount applies to the registered award'}
    used = ['Organisasjonsnummer støttemottaker', 'Støttetiltaksnummer', 'Status', 'Støttetiltakstype',
            'Tildelingsdato', 'Organisasjonsnummer støttegiver', 'Navn støttegiver']
    specified = f.get('Organisasjonsnummer spesifisert støttemottaker', '')
    if specified:
        specified = org_id(specified)
        if not specified or not valid(specified):
            return None
        value['specified_recipient_orgnr'] = specified
        used.append('Organisasjonsnummer spesifisert støttemottaker')
    exact = amount(f.get('Tildelt beløp'))
    currency = f.get('Tildelt beløp valuta', '')
    if exact is not None and re.fullmatch(r'[A-Z]{3}', currency):
        value.update(amount=exact, currency=currency)
        used += ['Tildelt beløp', 'Tildelt beløp valuta']
    else:
        low, high = amount(f.get('Beløpsintervall fra beløp')), amount(f.get('Beløpsintervall til beløp'))
        currency = f.get('Beløpsintervall valuta', '')
        if low is not None and high is not None and low <= high and re.fullmatch(r'[A-Z]{3}', currency):
            value.update(amount_range={'from': low, 'to': high}, currency=currency)
            used += ['Beløpsintervall fra beløp', 'Beløpsintervall til beløp', 'Beløpsintervall valuta']
    for key, name in [('Tilknyttet støtteordning', 'scheme_id'), ('Støtteinstrument', 'instrument')]:
        if f.get(key):
            value[name] = f[key]
            used.append(key)
    return value, ['/fields/' + key for key in used]


def section(org, now, blobs):
    from .exact_official import load_bundle, record_section
    return record_section('state_aid', 'state_aid.award.', load_bundle(BUNDLE), org, now,
                          derive, blobs, 'official_state_aid', 'award_id')
