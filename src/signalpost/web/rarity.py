"""Local registry frequency data; frequency is not ownership proof."""
import gzip
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from .policy import FREE_MAIL

DEFAULT_PATH = Path(__file__).resolve().parents[1] / 'data/identity_rarity.json.gz'
KINDS = ('phone', 'email', 'domain', 'name')
FORMS = {'as', 'asa', 'ans', 'da', 'enk', 'nuf', 'sa', 'ba', 'ks', 'iks', 'sti', 'bedr', 'forening', 'stiftelse', 'stiftelsen', 'aksjeselskap'}
FILLERS = {'og', 'and', 'the', 'av', 'i', 'for', 'til', 'of', 'selskap', 'selskapet'}


def name_key(value):
    text = str(value or '').casefold().replace('ø', 'o').replace('æ', 'ae')
    text = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    return ' '.join(sorted(t for t in re.findall(r'[a-z0-9]+', text) if t not in FORMS | FILLERS))


def phone_key(value):
    value = str(value or '').strip()
    if value.startswith('+') and not value.startswith('+47'):
        return None
    digits = re.sub(r'\D', '', value)
    if digits.startswith('0047'):
        digits = digits[4:]
    elif len(digits) == 10 and digits.startswith('47'):
        digits = digits[2:]
    return digits if len(digits) == 8 else None


def email_key(value):
    value = str(value or '').strip().casefold()
    return value if re.fullmatch(r'[^\s@;,]+@[^\s@;,]+\.[^\s@;,]+', value) else None


def domain_key(value):
    email = email_key(value)
    if not email:
        return None
    domain = email.rsplit('@', 1)[1].rstrip('.')
    try:
        domain = domain.encode('idna').decode('ascii')
    except UnicodeError:
        return None
    # Provider subdomains remain free-mail as well. No network PSL lookup.
    if any(domain == provider or domain.endswith('.' + provider) for provider in FREE_MAIL):
        return None
    return domain


def keys(row):
    phones = {k for v in (row.get('telefon'), row.get('mobil')) if (k := phone_key(v))}
    email = email_key(row.get('epostadresse'))
    domain = domain_key(row.get('epostadresse'))
    name = name_key(row.get('navn'))
    return {'phone': phones, 'email': {email} if email else set(),
            'domain': {domain} if domain else set(), 'name': {name} if name else set()}


@lru_cache(maxsize=2)
def load(path=DEFAULT_PATH):
    """Load only the bundled file. Missing/invalid data never triggers a fetch."""
    path = Path(path)
    if path.stat().st_size > 32_000_000:
        raise ValueError('rarity compressed size limit')
    with gzip.open(path, 'rb') as f:
        body = f.read(160_000_001)
    if len(body) > 160_000_000:
        raise ValueError('rarity expanded size limit')
    data = json.loads(body)
    if data.get('schema_version') != 1 or set(data.get('counts', {})) != set(KINDS):
        raise ValueError('rarity schema')
    for values in data['counts'].values():
        if not isinstance(values, dict) or any(not isinstance(k, str) or not k or type(v) is not int or v < 1 for k, v in values.items()):
            raise ValueError('rarity counts')
    return data


def count(kind, value, path=DEFAULT_PATH):
    normalizers = {'phone': phone_key, 'email': email_key, 'domain': domain_key, 'name': name_key}
    if kind not in normalizers:
        raise ValueError('unknown rarity kind')
    key = normalizers[kind]('lookup@' + str(value) if kind == 'domain' and '@' not in str(value) else value)
    return load(path)['counts'][kind].get(key, 0) if key else 0
