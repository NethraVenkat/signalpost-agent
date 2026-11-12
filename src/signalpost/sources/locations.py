"""Types come from exact registry address fields, never geocoding or guessing."""
from .extract import add


def publish(section, source, org, family, prefix, kind, address, locator, unit=None):
    if address is None or address == {}: return
    if not isinstance(address, dict): return
    address = {k:v for k,v in address.items() if k != '_links'}
    if not address: return
    value = {'location_type': kind, 'address': address, 'organisation_number': unit or org}
    if unit: value['parent_organisation_number'] = org
    add(section, source, org, family, prefix + kind, value, locator,
        method='signalpost.registry_locations.v1')
