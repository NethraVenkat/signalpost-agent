"""Subunit metadata extraction and pre-cached employer mappings."""
import csv
import time
from collections import defaultdict
from pathlib import Path
from ..identity.orgnr import normalize, valid


class SubunitMap(dict):
    """In-memory map of employer_orgnr -> [legal_name, brand_name].
    Also tracks employer_orgnr -> parent_orgnr and parent_orgnr -> set(subunit_orgnrs).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parents: dict[str, str] = {}
        self.parent_subunits: dict[str, set[str]] = defaultdict(set)

    def add_mapping(self, employer_orgnr: str, parent_orgnr: str, legal_name: str = None, brand_name: str = None):
        emp = normalize(str(employer_orgnr or ""))
        parent = normalize(str(parent_orgnr or ""))
        if not valid(emp) or not valid(parent):
            return
        self[emp] = [legal_name, brand_name]
        self.parents[emp] = parent
        self.parent_subunits[parent].add(emp)


def build_subunit_map(inputs=None, bulk=None, prior=None, matches_path=None) -> SubunitMap:
    t0 = time.monotonic()
    smap = SubunitMap()

    # 1. From inputs metadata (company JSON fields during bulk load)
    if inputs and getattr(inputs, "metadata", None):
        for parent_org, item in inputs.metadata.items():
            if not isinstance(item, dict):
                continue
            for key in ("subunits", "underenheter", "units", "workplaces", "virksomheter"):
                sub_list = item.get(key)
                if isinstance(sub_list, list):
                    for sub in sub_list:
                        if isinstance(sub, dict):
                            sub_org = sub.get("organisation_number") or sub.get("orgnr")
                            sub_name = sub.get("name") or sub.get("navn") or sub.get("legal_name")
                            brand = sub.get("brand_name") or sub.get("brand")
                            smap.add_mapping(sub_org, parent_org, sub_name, brand)
                        elif isinstance(sub, (str, int)):
                            smap.add_mapping(str(sub), parent_org)

    # 2. From bulk registry (if CSV has overordnetEnhet)
    if bulk:
        for org, (row, _) in bulk.items():
            parent = row.get("overordnetEnhet")
            if parent:
                legal = row.get("navn")
                smap.add_mapping(org, parent, legal)

    # 3. From prior envelopes (if present)
    if prior:
        for parent_org, row in prior.items():
            for c in row.get("claims", row.get("profile", {}).get("claims", [])):
                if c.get("family") == "subunits" and c.get("availability") == "available" and isinstance(c.get("value"), dict):
                    val = c["value"]
                    sub_org = val.get("organisation_number")
                    sub_name = val.get("name")
                    smap.add_mapping(sub_org, parent_org, sub_name)

    # 4. From pre-cached/known matches if present
    candidates_paths = [
        matches_path,
        Path("dev-notes/w5/nav_matches.csv"),
        Path("src/signalpost/data/subunits.csv"),
    ]
    for p in candidates_paths:
        if p and Path(p).exists():
            try:
                with Path(p).open(encoding="utf-8") as f:
                    r = csv.DictReader(f)
                    for row in r:
                        comp = row.get("company") or row.get("parent_orgnr")
                        emp = row.get("employer_orgnr") or row.get("subunit_orgnr")
                        name = row.get("name") or row.get("legal_name")
                        brand = row.get("brand_name") or row.get("brand")
                        if comp and emp:
                            smap.add_mapping(emp, comp, name, brand)
            except Exception:
                pass

    return smap
