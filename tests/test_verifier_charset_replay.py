"""Verifiers replay stored receipts exactly as the runtime parsed them.

Regression for P2 seed 20261118: a page declaring windows-1252 with non-ASCII
footer text (e.g. "Lilleåsgata", "SPRÅK"). The runtime parses the original
bytes once; the verifier receives already-decoded text. Re-encoding that text
as UTF-8 and decoding it again under the declared windows-1252 charset turned
"å" into "Ã¥", so a correct HIGH publisher receipt failed to replay.
"""
import pytest

from signalpost.sources.text import decode_body
from signalpost.web.html import Page
from signalpost.web.publisher import extract_publisher

URL = "https://example-skole.no/"
HTML = ('<!DOCTYPE html><html lang="nb"><head><meta http-equiv="Content-Type" content="text/html; charset=windows-1252">'
        "<title>Nettbutikk - Eksempel Skolemateriell AS</title></head><body><main>"
        + "<p>Læringsmateriell for skoler og barnehager i hele Norge. </p>" * 8
        + "</main><footer><p>Kontakt Eksempel Skolemateriell AS Lilleåsgata 4B 3340 Åmot Norge "
          "Telefon: 22 70 00 10 E-post: post@example-skole.no SPRÅK MATEMATIKK</p></footer></body></html>")
RAW = HTML.encode("cp1252")


def stored_text():
    # verify_output.stored_body(): one decode of the saved blob bytes.
    return decode_body(RAW)


def test_runtime_and_verifier_pages_are_identical_for_declared_cp1252():
    runtime = Page(RAW, URL)
    text = stored_text()
    replay = Page(text.encode("utf8"), URL, text=text)
    assert "Lilleåsgata" in runtime.raw and "Åmot" in runtime.raw
    assert replay.raw == runtime.raw
    assert replay.visible == runtime.visible
    assert extract_publisher(replay).fragments == extract_publisher(runtime).fragments


def test_old_double_decode_corrupted_non_ascii_text():
    # Documents the defect the verifiers no longer use.
    text = stored_text()
    legacy = Page(text.encode("utf8"), URL)
    assert "Lilleåsgata" not in legacy.raw and "LilleÃ¥sgata" in legacy.raw


@pytest.mark.parametrize("charset,codec", [("utf-8", "utf8"), ("iso-8859-1", "latin1")])
def test_text_replay_matches_runtime_for_other_charsets(charset, codec):
    html = HTML.replace("windows-1252", charset)
    raw = html.encode(codec)
    text = decode_body(raw)
    assert Page(text.encode("utf8"), URL, text=text).raw == Page(raw, URL).raw
