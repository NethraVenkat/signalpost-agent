import re


def normalize(value: object) -> str:
    if value is None or isinstance(value, (bool, dict, list)):
        return "" if value is None else str(value)
    return re.sub(r"\s", "", str(value).lstrip("\ufeff"))


def valid(number: str) -> bool:
    if not re.fullmatch(r"[0-9]{9}", number):
        return False
    check = (11 - sum(int(d) * w for d, w in zip(number[:8], (3, 2, 7, 6, 5, 4, 3, 2))) % 11) % 11
    return check != 10 and check == int(number[-1])
