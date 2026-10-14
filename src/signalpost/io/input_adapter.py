import json
from dataclasses import dataclass, field
from pathlib import Path
from ..identity.orgnr import normalize, valid


@dataclass
class Inputs:
    unique: list[str]
    rows: list[str]
    invalid: list[str]
    duplicates: int
    metadata: dict[str, dict] = field(default_factory=dict)


def read(path: Path) -> Inputs:
    text = path.read_text(encoding="utf-8-sig").strip()
    rows = []
    metadata = {}
    if not text:
        values = []
    else:
        try:
            body = json.loads(text)
            if isinstance(body, dict) and "organisation_numbers" in body:
                values = body["organisation_numbers"]
                if not isinstance(values, list):
                    values = [values]
            elif isinstance(body, list):
                values = body
            else:
                values = [body]
        except json.JSONDecodeError:
            values = []
            for line in text.splitlines():
                if not line.strip():
                    continue
                try:
                    values.append(json.loads(line))
                except json.JSONDecodeError:
                    values.append(line)
    for item in values:
        org = normalize(item.get("organisation_number") if isinstance(item, dict) else item)
        rows.append(org)
        if isinstance(item, dict) and org:
            metadata.setdefault(org, {}).update(item)
    unique = list(dict.fromkeys(rows))
    return Inputs(unique, rows, [x for x in unique if not valid(x)], len(rows) - len(unique), metadata)
