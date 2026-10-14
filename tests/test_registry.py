import asyncio
import base64
import csv
import hashlib
import json
import re
import time
from pathlib import Path
import httpx
import pytest
import respx
from signalpost.config import Config
from signalpost.identity.orgnr import normalize, valid
from signalpost.io.input_adapter import read
from signalpost.models.envelope import Error
from signalpost.models.shapes import CONTRACT_KEYS, REFERENCE_KEYS, validate
from signalpost.models.states import STATE_MAP, reference_state
from signalpost.sources import brreg_roller
from signalpost.sources.http import allow
from signalpost.budget import SourceFailure
from signalpost.runner import run


def number(index):
    prefix = f"{index:08d}"
    check = (11 - sum(int(d) * w for d, w in zip(prefix, (3, 2, 7, 6, 5, 4, 3, 2))) % 11) % 11
    return prefix + str(check) if check < 10 else None


def numbers(count):
    result = []
    index = 90000000
    while len(result) < count:
        candidate = number(index)
        if candidate:
            result.append(candidate)
        index += 1
    return result


def entity(org):
    body = json.loads((Path(__file__).parent / "fixtures/registry.json").read_text())
    body["organisasjonsnummer"] = org
    return body


def handler(role_name="Person One", missing_accounts=True):
    def response(request):
        url = str(request.url)
        org = request.url.params.get("overordnetEnhet") or re.search(r"/(\d{9})(?:/roller)?$", request.url.path)[1]
        if "/roller" in url:
            body = {"organisasjonsnummer": org, "rollegrupper": [{"roller": [{"type": {"kode": "DAGL"}, "person": {"navn": {"fornavn": role_name}}}]}]}
        elif "/underenheter?" in url:
            body = {"_embedded": {"underenheter": []}, "page": {"totalPages": 1}}
        elif "/regnskapsregisteret/" in url:
            body = [] if missing_accounts else [{"regnskapstype": "SELSKAP", "virksomhet": {"organisasjonsnummer": org},
                                                "regnskapsperiode": {"fraDato": "2025-01-01", "tilDato": "2025-12-31"}, "valuta": "NOK",
                                                "resultatregnskapResultat": {"aarsresultat": 0}}]
        else:
            body = entity(org)
        return httpx.Response(200, json=body)
    return response


def config(tmp, orgs, **kwargs):
    tmp.mkdir(parents=True, exist_ok=True)
    path = tmp / "batch.txt"
    path.write_text("\n".join(orgs), encoding="utf-8")
    kwargs.setdefault('nav_index_path',tmp/'missing-nav-index.json.gz')
    return Config(organisations=path, output=tmp / "envelopes.jsonl", report=tmp / "report.json", state_dir=tmp / "state", **kwargs)


def execute(cfg, response=None):
    with respx.mock(assert_all_called=False) as router:
        router.get(url__regex=r"https://data\.brreg\.no/.*").mock(side_effect=response or handler())
        report = asyncio.run(run(cfg))
    rows = [json.loads(x) for x in cfg.output.read_text(encoding="utf-8").splitlines()]
    return report, rows


@pytest.mark.parametrize("raw,expected", [("923609016", True), ("923609017", False), ("123", False), ("abc123456", False), ("923 609 016", True), ("\ufeff923609016", True), ("000000000", True), ("９２３６０９０１６", False)])
def test_checksum(raw, expected):
    assert valid(normalize(raw)) is expected
    assert normalize("012 345 678") == "012345678"


@pytest.mark.parametrize("text", ['{"organisation_number":"923609016"}\n{"organisation_number":"993578843"}', '["923609016", "993578843"]', '{"organisation_numbers":["923609016", "993578843"]}', '\ufeff923 609 016\n993578843'])
def test_input_formats(tmp_path, text):
    path = tmp_path / "input.any"
    path.write_text(text, encoding="utf-8")
    assert read(path).unique == ["923609016", "993578843"]


def test_empty_duplicates_invalid_and_warning(tmp_path):
    report, rows = execute(config(tmp_path / "empty", []))
    assert not rows and report["requests"] == 0
    report, rows = execute(config(tmp_path / "other", ["923609016", "923 609 016", "bad", "bad"], expected_count=100, emit_duplicates=False))
    assert [x["organisation_number"] for x in rows] == ["923609016", "bad"]
    assert report["duplicates"] == 2 and report["warnings"]
    assert any(e["code"] == "invalid_orgnr" for e in rows[1]["errors"])
    assert all(e["organisation_number"] != "bad" for e in report["request_log"])
    report, rows = execute(config(tmp_path / "duplicate", ["923609016", "bad", "923609016"], emit_duplicates=True))
    assert [x["organisation_number"] for x in rows] == ["923609016", "bad", "923609016"]


def test_one_hundred_membership_with_crashes_and_timeouts(tmp_path, monkeypatch):
    orgs = numbers(97) + ["invalid-1", "invalid-2", "invalid-3"]
    original = brreg_roller.fetch
    async def failing(org, http):
        if org in orgs[:10]:
            raise RuntimeError("synthetic section failure")
        if org in orgs[10:15]:
            raise SourceFailure("timeout")
        return await original(org, http)
    monkeypatch.setattr(brreg_roller, "fetch", failing)
    report, rows = execute(config(tmp_path, orgs))
    assert len(rows) == 100 and [x["organisation_number"] for x in rows] == orgs
    assert report["unhandled_exceptions"] == 0 and report["handled_exceptions"] == 10
    assert len([x for x in rows if any(e["code"] == "timeout" for e in x["errors"])]) == 5
    assert len(report["invalid_inputs"]) == 3
    assert all(x["run"]["sections"]["accounts"] == "not_available" for x in rows[:15])


def test_deadline_partial_progress(tmp_path):
    async def slow(request):
        if request.url.path.endswith("/roller"):
            await asyncio.sleep(10)
        return handler()(request)
    began = time.monotonic()
    report, rows = execute(config(tmp_path, numbers(20), time_budget_seconds=2, workers=2), slow)
    assert time.monotonic() - began < 3
    assert len(rows) == 20 and report["deadline_hits"] == 20
    assert any(c["availability"] == "available" for c in rows[0]["claims"])
    assert all(any(e["code"] == "deadline" for e in row["errors"]) for row in rows)


def test_no_zero_provenance_and_report(tmp_path):
    cfg = config(tmp_path, ["923609016"])
    report, rows = execute(cfg)
    claims = {c["field"]: c for c in rows[0]["claims"]}
    assert claims["identity.employees"]["value"] is None
    assert claims["identity.employees"]["availability"] == "not_available"
    assert claims["accounts.latest"]["value"] is None
    for e in rows[0]["evidence"]:
        blob = cfg.state_dir / "blobs" / e["content_sha256"]
        assert hashlib.sha256(blob.read_bytes()).hexdigest() == e["content_sha256"]
        assert e["source_url"] and e["retrieved_at"].endswith("Z") and e["locator"] and e["extraction_method"]
    evidence_ids = {e["id"] for e in rows[0]["evidence"]}
    assert all(set(c["evidence_ids"]) <= evidence_ids for c in rows[0]["claims"])
    assert report["total_cost_usd"] == 0 and report["requests_by_host"] == {"data.brreg.no": 4}


@pytest.mark.parametrize("shape", ["union", "contract", "reference"])
def test_shapes_and_roundtrip(tmp_path, shape):
    first = config(tmp_path / "first", ["923609016"], envelope_shape=shape)
    _, rows = execute(first)
    assert set(rows[0]) == (CONTRACT_KEYS | REFERENCE_KEYS if shape == "union" else CONTRACT_KEYS if shape == "contract" else REFERENCE_KEYS)
    validate(rows[0], shape)
    second = config(tmp_path / "second", ["923609016"], previous=first.output, envelope_shape=shape)
    report, rerun = execute(second)
    assert report["changes"] == 0
    before = rows[0] if shape != "reference" else rows[0]["profile"]
    after = rerun[0] if shape != "reference" else rerun[0]["profile"]
    assert [c["id"] for c in before["claims"]] == [c["id"] for c in after["claims"]]
    assert [e["id"] for e in before["evidence"]] == [e["id"] for e in after["evidence"]]


def test_role_change_and_carried_forward(tmp_path):
    first = config(tmp_path / "first", ["923609016"])
    _, original = execute(first)
    second = config(tmp_path / "second", ["923609016"], previous=first.output)
    report, changed = execute(second, handler(role_name="Person Two"))
    assert report["changes"] == 1
    event = changed[0]["changes"][0]
    assert event["field"] == "roles.roles" and event["materiality"] == "material"
    assert event["old_evidence_ids"] and event["new_evidence_ids"]
    def blocked(request):
        if request.url.path.endswith("/roller"):
            return httpx.Response(403, content=b"blocked")
        return handler()(request)
    third = config(tmp_path / "third", ["923609016"], previous=first.output)
    report, carried = execute(third, blocked)
    assert report["changes"] == 0
    c = next(c for c in carried[0]["claims"] if c["family"] == "roles")
    assert c["carried_forward"] and c["value"] == next(c for c in original[0]["claims"] if c["family"] == "roles")["value"]
    assert not (third.state_dir / "blobs" / event["old_content_sha256"]).exists()


@pytest.mark.parametrize("state", list(STATE_MAP))
def test_state_mapping(state):
    assert reference_state(state) == STATE_MAP[state]
    assert reference_state("failed", [Error(section="x", code="budget_exhausted", message="x")]) == "budget_exhausted"
    assert reference_state("blocked", [Error(section="x", code="robots", message="x")]) == "blocked_robots"


def test_request_budget(tmp_path):
    report, rows = execute(config(tmp_path, numbers(30), max_requests=5))
    assert report["requests"] == 5 and len(rows) == 30
    assert any(e["code"] == "budget_exhausted" for row in rows for e in row["errors"])


@pytest.mark.parametrize("url", ["https://example.com/", "http://data.brreg.no/", "https://data.brreg.no.evil.test/", "https://user@data.brreg.no/", "https://data.brreg.no:444/"])
def test_url_policy(url):
    with pytest.raises(SourceFailure):
        allow(url)


def test_bulk_streaming_and_live_fallback(tmp_path):
    cfg = config(tmp_path, ["923609016", "993578843"])
    cfg.bulk = tmp_path / "registry.csv"
    with cfg.bulk.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["organisasjonsnummer", "navn", "organisasjonsform.kode", "antallAnsatte"], delimiter=";")
        writer.writeheader()
        writer.writerow({"organisasjonsnummer": "923609016", "navn": "Bulk Company", "organisasjonsform.kode": "AS", "antallAnsatte": ""})
    report, rows = execute(cfg)
    assert report["requests"] == 7
    evidence = next(e for e in rows[0]["evidence"] if e["source_identifier"])
    assert evidence["source_identifier"].endswith(hashlib.sha256(cfg.bulk.read_bytes()).hexdigest())
    assert "snapshot_body_base64" not in evidence
    assert b"Bulk Company" in (cfg.state_dir / "blobs" / evidence["content_sha256"]).read_bytes()
    assert evidence["claim_span"] in (cfg.state_dir / "blobs" / evidence["content_sha256"]).read_bytes().decode("utf8")


def test_reported_zero_and_wrong_company_financials(tmp_path):
    _, rows = execute(config(tmp_path / "zero", ["923609016"]), handler(missing_accounts=False))
    claim = next(c for c in rows[0]["claims"] if c["field"] == "accounts.net_result")
    assert claim["value"] == 0 and claim["availability"] == "available"
    assert claim["reporting_period"]["fiscal_year"] == "2025"
    def wrong(request):
        if "/regnskapsregisteret/" in str(request.url):
            return httpx.Response(200, json=[{"regnskapstype": "SELSKAP", "virksomhet": {"organisasjonsnummer": "993578843"}}])
        return handler()(request)
    _, rows = execute(config(tmp_path / "wrong", ["923609016"]), wrong)
    assert rows[0]["run"]["sections"]["accounts"] == "ambiguous"
    assert not any(c["family"] == "accounts" and c["availability"] == "available" for c in rows[0]["claims"])


def test_format_only_and_corrupt_previous(tmp_path):
    first = config(tmp_path / "first", ["923609016"])
    execute(first)
    def formatted(request):
        if request.url.path.endswith("/923609016") and "/enhetsregisteret/" in str(request.url):
            body = entity("923609016")
            body["navn"] = "  EXAMPLE    AS  "
            return httpx.Response(200, json=body)
        return handler()(request)
    report, _ = execute(config(tmp_path / "second", ["923609016"], previous=first.output), formatted)
    assert report["changes"] == 0
    bad = tmp_path / "bad.jsonl"
    bad.write_text('{"organisation_number":"923609016"}')
    report, rows = execute(config(tmp_path / "bad-run", ["923609016"], previous=bad))
    assert len(rows) == 1 and report["warnings"]


def test_retry_and_redirect(tmp_path):
    calls = 0
    def retry(request):
        nonlocal calls
        if request.url.path.endswith("/roller"):
            calls += 1
            if calls == 1:
                return httpx.Response(429, headers={"Retry-After": "0"}, content=b"busy")
        return handler()(request)
    report, rows = execute(config(tmp_path / "retry", ["923609016"]), retry)
    assert report["requests"] == 5 and rows[0]["modules"]["roles"]["retry_count"] == 1
    def redirect(request):
        return httpx.Response(302, headers={"Location": "https://evil.test/"})
    report, rows = execute(config(tmp_path / "redirect", ["923609016"]), redirect)
    assert report["requests"] == 1 and any(e["code"] == "url_refused" for e in rows[0]["errors"])


def test_live_roles_link_and_unregistered_employees(tmp_path):
    def live_shape(request):
        if request.url.path.endswith("/roller"):
            return httpx.Response(200, json={"_links": {"enhet": {"href": "https://data.brreg.no/enhetsregisteret/api/enheter/923609016"}},
                                             "rollegrupper": [{"roller": [{"type": {"kode": "DAGL"}, "person": {"navn": {"fornavn": "Person"}}}]}]})
        if request.url.path.endswith("/923609016") and "/enhetsregisteret/" in str(request.url):
            body = entity("923609016")
            body.update({"antallAnsatte": 0, "harRegistrertAntallAnsatte": False})
            return httpx.Response(200, json=body)
        return handler()(request)
    _, rows = execute(config(tmp_path, ["923609016"]), live_shape)
    assert rows[0]["run"]["sections"]["roles"] == "available"
    assert next(c for c in rows[0]["claims"] if c["field"] == "identity.employees")["value"] is None


def test_consolidated_only_abstention(tmp_path):
    def consolidated(request):
        if "/regnskapsregisteret/" in str(request.url):
            return httpx.Response(200, json=[{"regnskapstype": "KONSERN", "virksomhet": {"organisasjonsnummer": "923609016"},
                                             "resultatregnskapResultat": {"aarsresultat": 99}}])
        return handler()(request)
    _, rows = execute(config(tmp_path, ["923609016"]), consolidated)
    assert rows[0]["run"]["sections"]["accounts"] == "not_available"
    assert any(e["code"] == "entity_accounts_unavailable" for e in rows[0]["errors"])


def test_actual_http_timeout_and_five_hundred_retry(tmp_path):
    calls = 0
    def transport(request):
        nonlocal calls
        if request.url.path.endswith("/roller"):
            raise httpx.ReadTimeout("synthetic", request=request)
        if "/regnskapsregisteret/" in str(request.url):
            calls += 1
            if calls == 1:
                return httpx.Response(503, content=b"busy")
        return handler()(request)
    report, rows = execute(config(tmp_path, ["923609016"]), transport)
    assert report["requests"] == 6
    assert rows[0]["run"]["sections"]["roles"] == "failed"
    assert any(e["code"] == "timeout" for e in rows[0]["errors"])
    assert rows[0]["modules"]["roles"]["retry_count"] == 1


def test_multiple_subunit_pages_and_parent_verification(tmp_path):
    def pages(request):
        if "/underenheter?" in str(request.url):
            page = int(request.url.params["page"])
            return httpx.Response(200, json={"_embedded": {"underenheter": [{"organisasjonsnummer": str(100 + page), "overordnetEnhet": "923609016", "navn": "Place"}]}, "page": {"totalPages": 2}})
        return handler()(request)
    report, rows = execute(config(tmp_path, ["923609016"]), pages)
    assert report["requests"] == 5
    assert len([c for c in rows[0]["claims"] if c["family"] == "subunits"]) == 2
    def wrong_parent(request):
        if "/underenheter?" in str(request.url):
            return httpx.Response(200, json={"_embedded": {"underenheter": [{"overordnetEnhet": "993578843"}]}})
        return handler()(request)
    _, rows = execute(config(tmp_path / "wrong", ["923609016"]), wrong_parent)
    assert rows[0]["run"]["sections"]["subunits"] == "ambiguous"


def test_paginated_deadline_keeps_verified_page(tmp_path):
    async def page_timeout(request):
        if "/underenheter?" in str(request.url):
            if request.url.params["page"] == "1":
                await asyncio.sleep(10)
            return httpx.Response(200, json={"_embedded": {"underenheter": [{"organisasjonsnummer": "993578843", "overordnetEnhet": "923609016", "navn": "Place"}]}, "page": {"totalPages": 2}})
        return handler()(request)
    report, rows = execute(config(tmp_path, ["923609016"], time_budget_seconds=1), page_timeout)
    assert report["deadline_hits"] == 1
    assert rows[0]["run"]["sections"]["subunits"] == "failed"
    assert any(c["field"] == "subunits.unit.993578843" and c["availability"] == "available" for c in rows[0]["claims"])
