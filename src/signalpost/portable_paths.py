"""Portable path rendering for saved reports and receipts.

Saved reports must never contain an absolute path that reveals a local user
name.  Writers pass text or JSON-like data through :func:`portable` /
:func:`portable_text`, which replace the repository checkout with ``<REPO>``,
the temporary directory with ``<TEMP>`` and any other home directory with
``<HOME>``.  The original separators after the prefix are kept, so a JSON
string such as ``C:\\\\Users\\\\x\\\\repo\\\\.data`` becomes
``<REPO>\\\\.data``.  Readers of saved paths use :func:`expand` to resolve
the placeholders on the current machine.
"""
from __future__ import annotations

import os
import re
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO = "<REPO>"
HOME = "<HOME>"
TEMP = "<TEMP>"

# One or more separators, in raw (\ or /) or JSON-escaped (\\) form.
_SEP = r"[\\/]+"

# Home-directory patterns that must never appear in tracked report text.  The
# Unix forms only match at a path start (beginning, whitespace, quote, `=`,
# `(` or a ``file://`` scheme), so a URL path such as
# ``https://example.no/home/index.html`` from a saved publisher page is not a
# local home directory.
_UNIX_START = r"(?:(?<![\w.~%/:\-])|(?<=file://))"
HOME_PATH_PATTERNS = (
    re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s\"'<>|*?]+", re.IGNORECASE),
    re.compile(_UNIX_START + r"/home/[^/\s\"'<>]+"),
    re.compile(_UNIX_START + r"/Users/[^/\s\"'<>]+"),
)
_PYTEST_USER = re.compile(r"pytest-of-(?!<USER>)[^\\/\s\"'<>]+")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _path_regex(path: str | os.PathLike[str]) -> re.Pattern[str] | None:
    parts = [p for p in re.split(r"[\\/]+", str(path)) if p]
    if len(parts) < 2:
        return None
    # Do not match a longer sibling such as ``repo-old`` for ``repo``.
    return re.compile(
        _SEP.join(re.escape(p) for p in parts) + r"(?![\w.\-])", re.IGNORECASE
    )


@lru_cache(maxsize=1)
def _rules() -> tuple[tuple[re.Pattern[str], str], ...]:
    rules: list[tuple[re.Pattern[str], str]] = []
    home = Path.home()
    temps = {tempfile.gettempdir(), os.environ.get("TEMP", ""), os.environ.get("TMP", "")}
    for temp in sorted({t for t in temps if t}, key=len, reverse=True):
        regex = _path_regex(temp)
        if regex is not None and temp != "/tmp":
            rules.append((regex, TEMP))
    rules.append((re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s\"'<>|*?]+" + _SEP
                             + r"AppData" + _SEP + r"Local" + _SEP + r"Temp(?![\w.\-])",
                             re.IGNORECASE), TEMP))
    regex = _path_regex(_repo_root())
    if regex is not None:
        rules.append((regex, REPO))
    regex = _path_regex(home)
    if regex is not None:
        rules.append((regex, HOME))
    for pattern in HOME_PATH_PATTERNS:
        rules.append((pattern, HOME))
    return tuple(rules)


def portable_text(text: str) -> str:
    """Return ``text`` with local repository/temp/home prefixes replaced."""
    if not isinstance(text, str) or not text:
        return text
    for pattern, placeholder in _rules():
        text = pattern.sub(placeholder, text)
    return _PYTEST_USER.sub("pytest-of-<USER>", text)


def portable(value: Any) -> Any:
    """Recursively apply :func:`portable_text` to strings, keys and paths."""
    if isinstance(value, str):
        return portable_text(value)
    if isinstance(value, os.PathLike):
        return portable_text(os.fspath(value))
    if isinstance(value, dict):
        return {(portable_text(k) if isinstance(k, str) else k): portable(v)
                for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [portable(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(portable(v) for v in value)
    return value


def expand(text: str | os.PathLike[str]) -> str:
    """Resolve ``<REPO>``, ``<TEMP>`` and ``<HOME>`` placeholders locally."""
    text = os.fspath(text)
    return (text.replace(REPO, str(_repo_root()))
                .replace(TEMP, tempfile.gettempdir())
                .replace(HOME, str(Path.home())))


def find_home_paths(text: str) -> list[str]:
    """Return every local home-directory path occurrence in ``text``."""
    return [m.group(0) for pattern in HOME_PATH_PATTERNS for m in pattern.finditer(text)]


def sanitize_file(path: str | os.PathLike[str]) -> bool:
    """Rewrite a saved text file in place with portable paths; keep bytes otherwise."""
    path = Path(path)
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    new = portable_text(text)
    if new == text:
        return False
    path.write_bytes(new.encode("utf-8"))
    return True
