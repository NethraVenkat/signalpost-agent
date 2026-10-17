import csv
import gzip
import hashlib
import io
from pathlib import Path
from .extract import Section, Source, add, finish
from ..models.evidence import utc_now
from ..budget import SourceFailure
from .registry_fields import EXTRA,GROUPS,boolean

ALIASES = {"organisasjonsnummer": "Organisasjonsnummer", "navn": "Navn", "antallAnsatte": "Antall ansatte",
           "konkurs": "Konkurs", "underAvvikling": "Under avvikling", "hjemmeside": "Hjemmeside",
           "sisteInnsendteAarsregnskap": "Siste innsendte årsregnskap"}


def column(row, name):
    candidates = (name, ALIASES.get(name, name[:1].upper() + name[1:]), name.replace("naeringskode", "Næringskode"))
    for key in candidates:
        if row.get(key) not in (None, ""):
            return row[key], key
    for key, value in row.items():
        if key and key.casefold() == name.casefold() and value not in (None, ""):
            return value, key
    return None, name


def snapshot_hash(path, budget):
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            budget.check()
            sha.update(chunk)
    return sha.hexdigest()


def load(path: Path, wanted: set[str], blobs, budget):
    # Hash in chunks and index only requested rows. Per-claim blobs retain exact CSV
    # header + raw selected record, not the multi-gigabyte nationwide body.
    sha = snapshot_hash(path, budget)
    with path.open("rb") as check:
        compressed = check.read(2) == b"\x1f\x8b"
    opener = gzip.open if compressed else open
    found = {}
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(16384)
        handle.seek(0)
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=";,\t").delimiter
        except csv.Error:
            delimiter = ";" if ";" in sample.splitlines()[0] else ","
        captured = []

        def lines():
            for line in handle:
                captured.append(line)
                yield line

        reader = csv.reader(lines(), delimiter=delimiter)
        fields = next(reader, [])
        normalized_fields = [str(name).casefold() for name in fields]
        required = set(normalized_fields)
        if len(required) != len(normalized_fields):
            raise SourceFailure('malformed_bulk_columns', 'Bulk column names must be unique, including case variants')
        if not {'organisasjonsnummer','navn'} <= required:
            raise SourceFailure('malformed_bulk_columns','Bulk requires organisation-number and legal-name columns')
        header = "".join(captured)
        captured.clear()
        org_index = next(i for i, name in enumerate(fields) if name.casefold() == 'organisasjonsnummer')
        for values in reader:
            budget.check()
            raw = "".join(captured)
            captured.clear()
            org = values[org_index] if len(values) > org_index else None
            if org in wanted:
                # Avoid allocating a full dictionary for every nationwide row.
                # Preserve DictReader's selected-row semantics and exact bytes.
                row = dict(zip(fields, values))
                if len(values) > len(fields):
                    row[None] = values[len(fields):]
                elif len(values) < len(fields):
                    row.update((key, None) for key in fields[len(values):])
                body = (header + raw).encode("utf-8")
                source = Source("https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv", body,
                                blobs.put(body), utc_now(), f"{path.name}:sha256:{sha}")
                found[org] = (row, source)
        return found, sha


def extract(org, row, source):
    section = Section()
    for name, col in [('founding_date', 'stiftelsesdato'), ('vat_registration_date', 'registreringsdatoMerverdiavgiftsregisteret')]:
        value, actual = column(row, col)
        if value:
            add(section, source, org, 'identity', 'identity.' + name, value, f'row:{org}/column:{actual}', effective=value)
    simple = {"legal_name": "navn", "registration_date": "registreringsdatoEnhetsregisteret", "employees": "antallAnsatte",
              "registered_website": "hjemmeside", "bankrupt": "konkurs", "under_liquidation": "underAvvikling",
              "deleted": "slettedato", "latest_submitted_accounts": "sisteInnsendteAarsregnskap", "municipality": "forretningsadresse.kommune",
              "registered_activity": "aktivitet", "statutory_purpose": "vedtektsfestetFormaal"}
    for name, col in simple.items():
        value, actual = column(row, col)
        if value is not None and name == "employees":
            try:
                value = int(value)
            except ValueError:
                raise SourceFailure("malformed_employees")
            if str(column(row, "harRegistrertAntallAnsatte")[0]).casefold() == "false":
                value = None
        effective = value if name == "registration_date" else None
        if name == "deleted" and value is not None:
            effective, value = value, True
        if value is not None and name in ("bankrupt", "under_liquidation"):
            if value.casefold() not in {"true", "false"}:
                raise SourceFailure("malformed_flag")
            value = value.casefold() == "true"
        add(section, source, org, "identity", "identity." + name, value, f"row:{org}/column:{actual}", effective=effective)
    for name, prefix, keys in (("organisation_form", "organisasjonsform", ("kode", "beskrivelse")),
                               ("registered_address", "forretningsadresse", ("adresse", "postnummer", "poststed", "kommune", "kommunenummer", "land")),
                               ("postal_address", "postadresse", ("adresse", "postnummer", "poststed", "kommune", "kommunenummer", "land"))):
        value = {key: column(row, prefix + "." + key)[0] for key in keys if column(row, prefix + "." + key)[0] is not None}
        add(section, source, org, "identity", "identity." + name, value or None, f"row:{org}/columns:{prefix}.*")
    for i in range(1, 4):
        prefix = f"naeringskode{i}"
        value = {k: column(row, prefix + "." + k)[0] for k in ("kode", "beskrivelse") if column(row, prefix + "." + k)[0] is not None}
        add(section, source, org, "identity", f"identity.nace{i}", value or None, f"row:{org}/columns:{prefix}.*")
    for field,(key,kind) in EXTRA.items():
        value,actual=column(row,key)
        if value is None:continue
        if kind=='bool':value=boolean(value)
        add(section,source,org,'identity','identity.'+field,value,f'row:{org}/column:{actual}',
            effective=value if field.endswith('_date') else None)
    for field,(prefix,keys) in GROUPS.items():
        value={k:column(row,prefix+'.'+k)[0] for k in keys if column(row,prefix+'.'+k)[0] is not None}
        if not value:continue
        add(section,source,org,'identity','identity.'+field,value or None,f'row:{org}/columns:{prefix}.*')
    return finish(section)
