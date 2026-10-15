import csv
import io
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
            first_line = text.splitlines()[0].strip() if text.splitlines() else ""
            is_csv = path.suffix.lower() == ".csv" or ("," in first_line and not first_line.startswith(("{", "[")))
            if is_csv:
                csv_rows = [r for r in csv.reader(io.StringIO(text)) if any(cell.strip() for cell in r)]
                header_tokens = {"organisasjonsnummer", "orgnr", "organisation_number", "organization_number", "org_nr"}
                if csv_rows and (csv_rows[0][0].strip().lower() in header_tokens or any(h.strip().lower() in header_tokens for h in csv_rows[0])):
                    col_idx = next((i for i, h in enumerate(csv_rows[0]) if h.strip().lower() in header_tokens), 0)
                    header_cols = [h.strip() for h in csv_rows[0]]
                    values = []
                    for r in csv_rows[1:]:
                        org_val = r[col_idx].strip() if col_idx < len(r) else ""
                        row_dict = {header_cols[i]: r[i] for i in range(min(len(header_cols), len(r)))}
                        row_dict["organisation_number"] = org_val
                        values.append(row_dict)
                else:
                    values = []
                    for r in csv_rows:
                        org_val = r[0].strip() if r else ""
                        values.append(org_val)
            else:
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
