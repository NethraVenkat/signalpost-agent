"""Registry-backed foreign-entity checks for website social attribution."""

import gzip
import hashlib
import json
import re
import unicodedata
from bisect import bisect_left
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .rarity import FILLERS, FORMS

DEFAULT_PATH = Path(__file__).resolve().parents[1] / 'data/social_registry.bin.gz'
LEGAL_FORMS = FORMS | {'sf', 'kf', 'fkf', 'se', 'borettslag', 'eierseksjonssameie'}
WIDTH = 12
MAX_NAMES = 2_000_000
MAX_WORDS = 64
MAX_DOMAINS_BYTES = 8 * 1024 * 1024
WORD = re.compile(r'[^\W_]+')
SLASH_AS = re.compile(r'\ba\s*/\s*s\b', re.I)


def legal_words(text):
    return tuple(WORD.findall(SLASH_AS.sub('AS', unicodedata.normalize('NFKC', text)).casefold()))


def fingerprint(words):
    return hashlib.sha256(' '.join(words).encode('utf8')).digest()[:WIDTH]


@dataclass(frozen=True)
class RegistryNames:
    max_words: int
    names: bytes
    shared_domains: dict

    def contains(self, words):
        target = fingerprint(words)
        offsets = range(0, len(self.names), WIDTH)
        pos = bisect_left(offsets, target, key=lambda offset: self.names[offset:offset + WIDTH])
        return self.names[pos * WIDTH:(pos + 1) * WIDTH] == target


@lru_cache(maxsize=2)
def load(path=DEFAULT_PATH):
    with gzip.open(path, 'rb') as stream:
        header = json.loads(stream.readline(4096))
        count, max_words = header['name_count'], header['max_words']
        if header['version'] != 1 or not 0 < count <= MAX_NAMES or not 2 <= max_words <= MAX_WORDS:
            raise ValueError('Invalid social registry name index')
        names = stream.read(count * WIDTH)
        shared = stream.read(MAX_DOMAINS_BYTES + 1)
        if len(names) != count * WIDTH or len(shared) > MAX_DOMAINS_BYTES:
            raise ValueError('Invalid social registry index size')
        domains = json.loads(shared)
        if not isinstance(domains, dict):
            raise ValueError('Invalid social registry domain index')
        return RegistryNames(max_words, names, domains)


def foreign_name(text, index, own_names, *, ignore_filler_prose=False):
    """Find a complete registered name ending in an explicit legal form."""
    text = SLASH_AS.sub('AS', unicodedata.normalize('NFKC', text))
    tokens = list(WORD.finditer(text))
    words = tuple(token.group().casefold() for token in tokens)
    for end, word in enumerate(words):
        if word not in LEGAL_FORMS or end == 0:
            continue
        # Lowercase short forms can be ordinary prose. Accept them at the
        # end of a text block or before punctuation, as in a company label.
        suffix = tokens[end]
        rest = text[suffix.end():].lstrip()
        if len(word) <= 3 and not suffix.group().isupper() and rest[:1].isalpha():
            continue
        for start in range(max(0, end + 1 - index.max_words), end):
            candidate = words[start:end + 1]
            if candidate in own_names:
                break
            # A lowercase connective can precede a legal form in prose, as in
            # “endra organisasjonsform til AS”. It is not a company mention.
            if (ignore_filler_prose and len(candidate) == 2 and candidate[0] in FILLERS
                    and tokens[start].group().islower()):
                continue
            if index.contains(candidate):
                return text[tokens[start].start():suffix.end()]
    return None


def shared_domain_name(text, indexed_stems, own_stems):
    """Match the full registered stem when that entity declares the same site."""
    words = legal_words(text)
    for size, keys in indexed_stems.items():
        for start in range(len(words) - size + 1):
            end = start + size
            candidate = words[start:end]
            if candidate in own_stems or end < len(words) and words[end] in LEGAL_FORMS:
                continue
            if fingerprint(candidate).hex() in keys:
                return ' '.join(candidate)
    return None
