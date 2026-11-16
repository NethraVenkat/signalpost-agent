"""Tracked files must never contain a local home-directory path (user name leak)."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

from signalpost import portable_paths as pp

ROOT = Path(__file__).resolve().parents[1]

# Requested patterns.  The Unix forms only count at a path start, so a URL path
# such as https://example.no/home/index.html inside a saved publisher excerpt is
# not mistaken for a local home directory (see portable_paths.HOME_PATH_PATTERNS).
WINDOWS = re.compile(rb"[A-Za-z]:[\\/]+Users[\\/]+[^\\/]+", re.IGNORECASE)
START = rb"(?:(?<![\w.~%/:\-])|(?<=file://))"
# Literals are split ("/" "home/...") so this file never matches its own patterns.
UNIX_HOME = re.compile(START + rb"/" rb"home/[^/]+")
MAC_HOME = re.compile(START + rb"/" rb"Users/[^/]+")
PYTEST_USER = re.compile(rb"pytest-" rb"of-(?!<USER>)[^\\/\s\"'<>]+")


def _tracked_files() -> list[Path]:
    if shutil.which("git") is None or not (ROOT / ".git").exists():
        pytest.skip("not a git checkout")
    # Tracked files plus untracked, non-ignored ones: a new file is checked
    # before it is committed, not only after.
    out = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, check=True).stdout
    return [ROOT / p for p in out.decode("utf-8").split("\0") if p]


def _is_saved_source_body(rel: str) -> bool:
    # Verbatim third-party response bytes (hash-pinned evidence).  Their URL
    # paths, e.g. a home/index.html script string, are publisher content,
    # not local paths; the Windows/pytest user patterns still apply to them.
    return rel.endswith(".body") or "/blobs/" in rel


def test_no_tracked_text_file_contains_a_home_directory_path():
    offenders: list[str] = []
    for path in _tracked_files():
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data[:8192]:
            continue  # binary
        rel = path.relative_to(ROOT).as_posix()
        patterns = []
        # Cheap substring pre-filters keep the full-tree scan fast.
        if b"sers" in data or b"SERS" in data:
            patterns.append(WINDOWS)
        if not _is_saved_source_body(rel):
            if b"/" b"home/" in data:
                patterns.append(UNIX_HOME)
            if b"/" b"Users/" in data:
                patterns.append(MAC_HOME)
        if b"pytest-of-" in data:
            patterns.append(PYTEST_USER)
        for pattern in patterns:
            match = pattern.search(data)
            if match:
                offenders.append(f"{path.relative_to(ROOT).as_posix()}: {match.group(0)[:80]!r}")
                break
    assert not offenders, "home-directory paths in tracked files:\n" + "\n".join(offenders[:50])


def test_url_paths_are_not_home_directories():
    for text in (b'href="https://ted.europa.eu/home/index.html"', b"https://x.no/Users/guide"):
        assert not UNIX_HOME.search(text) and not MAC_HOME.search(text)
    # Positive samples are assembled at runtime so this file itself stays clean.
    home_dir, mac_dir = b"/" + b"home" + b"/alice", b"/" + b"Users" + b"/alice"
    for text in (b'"cwd": "' + home_dir + b'/repo"', b"file://" + home_dir + b"/x", b" " + mac_dir + b"/x"):
        assert UNIX_HOME.search(text) or MAC_HOME.search(text)


@pytest.mark.parametrize("sep", ["\\", "/", "\\\\"])
def test_portable_replaces_repo_temp_and_home(sep, monkeypatch, tmp_path):
    home = Path("C:/") / "Users" / "alice"  # assembled; no literal home path in this file
    repo = home / "work" / "repo"
    temp = home / "AppData" / "Local" / "Temp"
    monkeypatch.setattr(pp.Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr(pp, "_repo_root", lambda: repo)
    monkeypatch.setattr(pp.tempfile, "gettempdir", lambda: str(temp))
    monkeypatch.delenv("TEMP", raising=False)
    monkeypatch.delenv("TMP", raising=False)
    pp._rules.cache_clear()
    try:
        j = sep.join
        data = {
            "work": j(["C:", "Users", "alice", "work", "repo", ".data", "run"]),
            "tmp": j(["C:", "Users", "alice", "AppData", "Local", "Temp", "pytest-" + "of-alice", "x"]),
            "dl": "file:///" + "/".join(["C:", "Users", "alice", "Downloads", "a.csv"]),
            "other": j(["D:", "Users", "bob", "x"]),
            "sibling": j(["C:", "Users", "alice", "work", "repo-old"]),
            "url": "https://ted.europa.eu/home/index.html",
            "argv": ["-m", j(["C:", "Users", "alice", "work", "repo", "reports"])],
        }
        out = pp.portable(data)
        assert out["work"] == "<REPO>" + sep + ".data" + sep + "run"
        assert out["tmp"] == "<TEMP>" + sep + "pytest-of-<USER>" + sep + "x"
        assert out["dl"] == "file:///<HOME>/Downloads/a.csv"
        assert out["other"] == "<HOME>" + sep + "x"
        assert out["sibling"] == "<HOME>" + sep + "work" + sep + "repo-old"
        assert out["url"] == data["url"]
        assert out["argv"] == ["-m", "<REPO>" + sep + "reports"]
        assert not pp.find_home_paths(str(out))
        assert pp.expand("<REPO>/x") == str(repo) + "/x"
        assert pp.expand("<HOME>/d") == str(home) + "/d"
        assert pp.expand("relative/x") == "relative/x"
        saved = tmp_path / "log.txt"
        saved.write_bytes(("cwd " + data["work"] + "\r\n").encode())
        assert pp.sanitize_file(saved)
        assert saved.read_bytes() == ("cwd <REPO>" + sep + ".data" + sep + "run\r\n").encode()
        assert not pp.sanitize_file(saved)
    finally:
        pp._rules.cache_clear()
