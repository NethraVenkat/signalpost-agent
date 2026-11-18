"""Load bundled website nominations without contacting the source archives."""

import gzip
import json
import re
from functools import lru_cache
from pathlib import Path

from ..identity.orgnr import valid
from .policy import DIRECTORIES, FREE_MAIL, MARKETPLACES, SOCIAL, domain

DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "website_seeds"
ORIGINS = {"commoncrawl": "seed_commoncrawl", "openstreetmap": "seed_openstreetmap"}
SEED_ORIGINS = frozenset(ORIGINS.values())
HOST = re.compile(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+")


@lru_cache(maxsize=1)
def load():
    entries = {}
    for source, origin in ORIGINS.items():
        try:
            with gzip.open(DIRECTORY / f"{source}.json.gz", "rt", encoding="utf8") as stream:
                payload = json.load(stream)
        except (OSError, EOFError, ValueError):
            continue
        if not isinstance(payload, dict) or payload.get("version") != 1 or payload.get("source") != source:
            continue
        rows = payload.get("entries")
        if not isinstance(rows, dict):
            continue
        for org, nominations in rows.items():
            if not valid(org) or not isinstance(nominations, list):
                continue
            for record in nominations:
                if not isinstance(record, list) or not record or not isinstance(record[0], str):
                    continue
                root = record[0]
                if not HOST.fullmatch(root) or domain(root) != root:
                    continue
                if root in DIRECTORIES | FREE_MAIL | MARKETPLACES | SOCIAL:
                    continue
                entries.setdefault(org, []).append((root, origin))
    return {org: tuple(nominations) for org, nominations in entries.items()}


def publisher_has_number(page, organisation_number):
    from .proof import orgnrs
    from .publisher import extract_publisher

    fragments = extract_publisher(page).fragments
    return any(organisation_number in orgnrs(fragment.text) for fragment in fragments)
