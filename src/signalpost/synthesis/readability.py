"""Deterministic presentation helpers shared by generation and validation."""
from decimal import Decimal
from .catalog import leaves
from .nace import english_title, unspecified


def money(value):
    # Remove only insignificant fractional zeros; never round or scale.
    fixed = format(Decimal(str(value)), 'f')
    whole, _, fraction = fixed.partition('.')
    fraction = fraction.rstrip('0')
    return format(Decimal(whole + ('.' + fraction if fraction else '')), ',f')


def normalised_description(value):
    return ' '.join(' '.join(leaves(value)).split())


def headline(claims, municipality_display=None):
    fields = {c.field: c for c in claims}
    name = fields.get('identity.legal_name')
    if name is None:
        return None
    used = [name]
    municipality = fields.get('identity.municipality')
    industry = next((c for c in sorted(claims, key=lambda c: c.field)
                     if c.field.startswith('identity.nace') and not unspecified(c.value) and
                     (english_title(c.value) or c.value.get('beskrivelse'))), None)
    text = str(name.value)
    if municipality:
        text += ' is based in ' + (municipality_display if municipality_display is not None else str(municipality.value).title())
        used.append(municipality)
    if industry:
        text += ' and registered under ' if municipality else ' is registered under '
        text += (english_title(industry.value) or industry.value['beskrivelse']) + ' (NACE ' + str(industry.value['kode']) + ')'
        used.append(industry)
    employees = fields.get('identity.employees')
    revenue = fields.get('accounts.revenue')
    period = getattr(revenue, 'reporting_period', None) or {}
    if employees:
        text += (', with ' if municipality or industry else ' has ') + str(employees.value) + ' registered employees'
        used.append(employees)
    if revenue and period.get('currency') == 'NOK' and period.get('fiscal_year'):
        text += (' and ' if employees or municipality or industry else ' has ')
        text += 'NOK ' + money(revenue.value) + ' in revenue in FY' + str(period['fiscal_year'])
        used.append(revenue)
    if len(used) == 1:
        text = 'Registered name: ' + str(name.value)
    if any(getattr(c,'carried_forward',False) for c in used):
        text = 'Previously supported. ' + text
    return text + '.', [c.id for c in used]


def workplace_label(claim):
    value = claim.value
    address = value.get('address') or {}
    name = str(value.get('name') or '')
    city = address.get('kommune') or address.get('poststed')
    return name + ' (' + str(city) + ')' if name and city else name or str(city or '')


def workplaces_sentence(claims):
    records = sorted({c.id: c for c in claims}.values(), key=lambda c: c.field)
    labels = [workplace_label(c) for c in records[:3]]
    examples = labels[0] if len(labels) == 1 else ' and '.join(labels) if len(labels) == 2 else ', '.join(labels[:-1]) + ' and ' + labels[-1]
    prefix = 'Previously supported. ' if any(getattr(c, 'carried_forward', False) for c in records) else ''
    return prefix + str(len(records)) + ' registered workplaces, including ' + examples + '.'


def nace_sentence(claim):
    value = claim.value
    title = english_title(value)
    rendered = str(value.get('kode', '')) + ': '
    rendered += title + ' (' + str(value.get('beskrivelse', '')) + ')' if title else str(value.get('beskrivelse', ''))
    return ('Previously supported. ' if getattr(claim,'carried_forward',False) else '') + 'NACE ' + rendered + '.'


def dual_role(claims):
    ceo = next((c for c in claims if (c.value.get('role_type') or {}).get('kode') == 'DAGL'), None)
    chair = next((c for c in claims if (c.value.get('role_type') or {}).get('kode') == 'LEDE'), None)
    if not ceo or not chair or not isinstance(ceo.value.get('name'),str) or not ceo.value.get('name') or ceo.value.get('name') != chair.value.get('name'):
        return None
    # Names alone cannot establish that two different registered people are one.
    if ceo.value.get('birth_date') != chair.value.get('birth_date') or ceo.value.get('entity_organisation_number')!=chair.value.get('entity_organisation_number'):
        return None
    prefix = 'Previously supported. ' if ceo.carried_forward or chair.carried_forward else ''
    return prefix + str(ceo.value['name']) + ' is both CEO and chair.', [ceo.id, chair.id]


def unknown_text(unknown, envelope):
    if unknown.family == 'refresh':
        return unknown.reason
    if unknown.field == 'employees':
        return 'Employee count not reported.'
    if unknown.field == 'industry':
        return 'Industry code not specified.'
    if unknown.field == 'financial_direction':
        years = sorted({str(c.reporting_period['fiscal_year']) for c in envelope.claims
                        if c.availability == 'available' and c.family == 'accounts' and
                        c.reporting_period and c.reporting_period.get('fiscal_year')})
        return 'Financial trend unknown: only FY' + years[0] + ' accounts are available.' if len(years) == 1 else 'Financial trend unknown.'
    labels = {'accounts': 'Accounts', 'hiring': 'Job ads', 'website': 'Website',
              'roles': 'Leadership', 'subunits': 'Workplace', 'identity': 'Registry',
              'what_it_does': 'Activity', 'scale': 'Scale', 'leadership': 'Leadership'}
    label = labels.get(unknown.family, unknown.family.capitalize())
    if unknown.state == 'not_available':
        return {'hiring': 'No active job ads on NAV.', 'website': 'No verified website found.'}.get(unknown.family, label + ' not reported.')
    if unknown.state in {'failed', 'blocked'}:
        cause = 'source unavailable' if 'source_unavailable' in unknown.reason else 'source access refused' if unknown.state == 'blocked' else None
        return label + ' check incomplete' + (' (' + cause + ')' if cause else '') + '.'
    if unknown.state == 'ambiguous':
        return label + ' unknown: identity or source coverage is ambiguous.'
    if unknown.state == 'not_applicable':
        return label + ' not applicable.'
    return unknown.reason
