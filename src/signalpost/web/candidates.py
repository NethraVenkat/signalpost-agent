import re
from dataclasses import dataclass
from .policy import domain, normalize_url, SOCIAL, DIRECTORIES, FREE_MAIL
from ..sources.bulk_registry import column

FORMS = r"\b(?:as|asa|ans|da|enk|nuf|sa|ba|ks|iks|sti)\b$"
GENERIC = {"holding", "invest", "eiendom", "bygg", "service", "consult", "regnskap", "transport", "og"}


@dataclass(frozen=True)
class Candidate:
    url: str
    domain: str
    origin: str


def legal_name(value):
    text = str(value or "").casefold().strip(" .,-")
    while re.search(FORMS, text):
        text = re.sub(FORMS, "", text).strip(" .,-")
    return " ".join(re.findall(r"\w+", text))


def context_from_bulk(row):
    return {"name": column(row, "navn")[0], "website": column(row, "hjemmeside")[0],
            "email": column(row, "epostadresse")[0], "phone": column(row, "telefon")[0],
            "municipality": column(row, "forretningsadresse.kommune")[0],
            "street": column(row, "forretningsadresse.adresse")[0],
            "postcode": column(row, "forretningsadresse.postnummer")[0], "city": column(row, "forretningsadresse.poststed")[0]}


def generate(context):
    output = []
    seen = set()
    def add(value, origin):
        url = normalize_url(value)
        root = domain(url) if url else ""
        if root and root not in seen and root not in SOCIAL | DIRECTORIES | FREE_MAIL:
            output.append(Candidate(url, root, origin))
            seen.add(root)
    add(context.get("website"), "registry_website")
    email = str(context.get("email") or "")
    if "@" in email:
        add(email.rsplit("@", 1)[1], "registry_email")
    name = legal_name(context.get("name"))
    tokens = [t for t in name.split() if t != "og"]
    if tokens and not all(t in GENERIC for t in tokens):
        for replacements in (("ae", "o", "aa"), ("a", "oe", "a")):
            converted = " ".join(tokens).replace("æ", replacements[0]).replace("ø", replacements[1]).replace("å", replacements[2])
            words = re.findall(r"[a-z0-9]+", converted)
            for separator in ("", "-"):
                slug = separator.join(words)
                if len(slug) >= 4:
                    for suffix in ("no", "com"):
                        add(slug + "." + suffix, "legal_name_slug")
    return output[:4]
