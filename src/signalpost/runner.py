import asyncio
import json
import time
import uuid
from contextlib import AsyncExitStack
from types import SimpleNamespace
from collections import Counter
import httpx
from .budget import Budget, SourceFailure
from .identity.orgnr import valid
from .io.input_adapter import read, Inputs
from .io.envelope_writer import previous, write
from .io.report import build
from .models.envelope import Envelope, Run, Operations, Module, Error, Profile, CompactProfile
from .models.claim import Claim
from .models.evidence import utc_now, digest
from .models.states import reference_state
from .sources import brreg_enhet, brreg_roller, brreg_underenheter, regnskap, bulk_registry
from .sources.extract import Section, missing
from .sources.blobstore import BlobStore
from .sources.http import Http
from .refresh.diff import apply
from .watchdog import finish_before_deadline
from .web.fetcher import WebsiteHttp
from .web import collector
from .web.policy import safe_transport
from .sources import nav
from .synthesis.service import Service as SynthesisService

FAMILIES = ("identity", "roles", "subunits", "accounts")


def placeholder(org, run_id, started, families=FAMILIES):
    sections = {f: "failed" for f in families}
    errors = [Error(section=f, code="not_started", message="Section has not started") for f in families]
    envelope = Envelope(organisation_number=org, run=Run(run_id=run_id, started_at=started, completed_at=started, sections=sections),
                        claims=[], evidence=[], changes=[], errors=errors, operations=Operations(), run_id=run_id,
                        state="submission_error", started_at=started, completed_at=started,
                        modules={f: Module(state="submission_error", final_timestamp=started) for f in families}, profile={})
    for family in families:
        update(envelope, family, missing(family, "not_started"))
    return envelope


def update(envelope, family, section):
    if section.state in {"failed", "blocked"} and not section.claims:
        # Preserve already verified pages when a later page hits a deadline.
        section.claims = [c for c in envelope.claims if c.family == family and c.availability == "available"]
    envelope.run.sections[family] = section.state
    envelope.errors = [e for e in envelope.errors if e.section != family] + section.errors
    envelope.claims = [c for c in envelope.claims if c.family != family] + section.claims
    if not section.claims:
        now = utc_now()
        envelope.claims.append(Claim(field=family + ".section", value=None, availability=section.state,
                                    evidence_ids=[], confidence=0, family=family,
                                    id=digest([envelope.organisation_number, family + ".section", None, section.state, None]),
                                    first_observed_at=now, last_observed_at=now))
    evidence = {e.id: e for e in envelope.evidence}
    evidence.update({e.id: e for e in section.evidence})
    envelope.evidence = list(evidence.values())
    envelope.modules[family] = Module(state=reference_state(section.state, section.errors), retry_count=section.retries, final_timestamp=utc_now())


async def isolate(envelope, family, call):
    try:
        result = await call()
    except SourceFailure as exc:
        result = missing(family, exc.code, str(exc), "ambiguous" if exc.code == "wrong_company" else "failed")
    except asyncio.CancelledError:
        update(envelope, family, missing(family, "deadline"))
        raise
    except Exception as exc:
        # Never print downloaded content or credentials in exception messages.
        result = missing(family, "section_exception", type(exc).__name__)
    update(envelope, family, result)


def finalize(envelope, old, blobs, budget, began):
    for family in envelope.run.sections:
        if any(e.section == family and e.code == "not_started" for e in envelope.errors):
            update(envelope, family, missing(family, "deadline"))
    try:
        apply(envelope, old, blobs)
    except Exception as exc:
        envelope.errors.append(Error(section="refresh", code="previous_invalid", message=type(exc).__name__))
        envelope.changes = []
        envelope.run.refresh = {"mode": "baseline", "previous_rejected": True}
    envelope.completed_at = utc_now()
    envelope.run.completed_at = envelope.completed_at
    envelope.run.legal_identity = {c.field.removeprefix("identity."): c.value for c in envelope.claims if c.family == "identity"}
    failures = any(s == "failed" for s in envelope.run.sections.values())
    envelope.state = "submission_error" if any(m.state == "submission_error" for m in envelope.modules.values()) else "complete"
    envelope.run.terminal_status = "failed" if all(s == "failed" for s in envelope.run.sections.values()) else "completed"
    events = [e for e in budget.events if e["organisation_number"] == envelope.organisation_number]
    envelope.operations.requests = len(events)
    for family, module in envelope.modules.items():
        hints = {"identity": "/api/enheter/", "roles": "/roller", "subunits": "/underenheter?", "accounts": "/regnskapsregisteret/"}
        matching = [] if family in {'hiring','activity'} else [e for e in events if e.get("section") == "website"] if family == "website" else [e for e in events if hints[family] in e["url"] and (family != "identity" or not e["url"].endswith("/roller"))]
        module.retry_count = max(0, len(matching) - len({e["url"] for e in matching}))
    envelope.profile = CompactProfile(organisation_number=envelope.organisation_number,
                                      values={c.field: c.value for c in envelope.claims},
                                      evidence_ids=[e.id for e in envelope.evidence])


async def run(config, client=None,synthesis_provider=None):
    from .monitor import LoopMonitor
    monitor=LoopMonitor();monitor.start()
    try:report=await _run(config,client,synthesis_provider)
    finally:lag=await monitor.stop()
    report['event_loop']=lag
    try:
        await asyncio.to_thread(config.report.write_text,json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    except OSError:pass  # Original report error handling remains authoritative.
    return report


async def _run(config, client=None,synthesis_provider=None):
    budget = Budget(config)
    if not config.run_id:
        config.run_id = uuid.uuid4().hex
    started = utc_now()
    warnings = []
    try:
        inputs = read(config.organisations)
    except Exception as exc:
        # Unreadable input has unknowable membership. Preserve this as a report
        # warning, never falsely claim the supplied batch was processed.
        inputs = Inputs([], [], [], 0)
        warnings.append(f"input unreadable: {type(exc).__name__}")
    families = FAMILIES + (("website",) if config.websites else ()) + (('hiring',) if config.hiring else ()) + (('activity',) if config.public_activity else ())
    envelopes = {org: placeholder(org, config.run_id, started, families) for org in inputs.unique}
    for org in inputs.invalid:
        for family in families:
            update(envelopes[org], family, missing(family, "invalid_orgnr"))
    expected_membership = len(inputs.rows) if config.emit_duplicates else len(inputs.unique)
    if config.expected_count is not None and config.expected_count != expected_membership:
        warnings.append(f"expected-count={config.expected_count} differs from emitted input membership={expected_membership}")
    prior, previous_warnings = previous(config.previous)
    warnings.extend(previous_warnings)
    storage_error = None
    try:
        blobs = BlobStore(config.state_dir)
    except OSError as exc:
        storage_error = type(exc).__name__
        blobs = SimpleNamespace(directory=config.state_dir / 'blobs')
        warnings.append('state storage unavailable: ' + storage_error + '; source checks skipped')
        for org,envelope in envelopes.items():
            if valid(org):
                for family in families:update(envelope,family,missing(family,'state_unavailable',storage_error))
    bulk, bulk_sha = {}, None
    valid_orgs = {org for org in inputs.unique if valid(org)}
    if config.bulk is not None and valid_orgs and storage_error is None:
        try:
            # Cooperative checks during synchronous streamed preparation include
            # bulk work in the deadline and bound memory to selected rows.
            bulk, bulk_sha = await asyncio.to_thread(bulk_registry.load,config.bulk,valid_orgs,blobs,budget)
        except Exception as exc:
            warnings.append(f"bulk unavailable: {getattr(exc, 'code', type(exc).__name__)}; live fallback")
    semaphore = asyncio.Semaphore(config.workers)
    nav_index=nav.Index()
    registry_done=set()
    registry_ready=asyncio.Event()
    def mark_registry(org):
        registry_done.add(org)
        if valid_orgs <= registry_done: registry_ready.set()
    async def nav_names():
        await registry_ready.wait()
        return await asyncio.to_thread(nav.company_names,list(envelopes.values()),prior)
    # Seed discovery before the first page; verified subunit names augment this
    # index when registry work completes. These names never authorize publication.
    nav_names.initial_names = {
        org: {nav.normal_name(bulk_registry.column(bulk[org][0], 'navn')[0])}
        if org in bulk else set() for org in valid_orgs
    }
    async def company(org, http, website_http, nav_task):
        from .web.policy import DNS_ORG
        DNS_ORG.set(org)
        envelope = envelopes[org]
        begin = time.monotonic()
        if not valid(org):
            for family in families:
                update(envelope, family, missing(family, "invalid_orgnr"))
            return
        try:
            async with semaphore:
                budget.check()
                async def identity():
                    if org in bulk:
                        return await asyncio.to_thread(bulk_registry.extract,org,*bulk[org])
                    return await brreg_enhet.fetch(org, http)
                await isolate(envelope, "identity", identity)
                if envelope.run.sections["identity"] != "available":
                    for family in families[1:]:
                        state = envelope.run.sections["identity"]
                        inherited = next((e.code for e in envelope.errors if e.section == "identity" and e.code in {"budget_exhausted", "deadline"}), "identity_unverified")
                        update(envelope, family, missing(family, inherited, state=state))
                    return
                for family, source in (("roles", brreg_roller), ("subunits", brreg_underenheter), ("accounts", regnskap)):
                    if family == "subunits":
                        await isolate(envelope, family, lambda: source.fetch(org, http, progress=lambda partial: update(envelope, "subunits", partial)))
                        mark_registry(org)
                    else:
                        await isolate(envelope, family, lambda source=source: source.fetch(org, http))
                if config.websites:
                    await isolate(envelope, "website", lambda: collector.fetch(org, envelope, bulk.get(org), website_http))
                if config.public_activity:
                    from .web.activity import fetch as fetch_activity
                    await isolate(envelope, 'activity', lambda: fetch_activity(org, envelope, website_http, website_http.accepted_pages.get(org, [])))
            # Waiting for the shared feed must not occupy registry worker slots.
            mark_registry(org)
            if config.hiring and nav_task:
                async def hiring():
                    await asyncio.shield(nav_task)
                    return nav.section(envelope,nav_index,blobs,prior.get(org))
                await isolate(envelope,'hiring',hiring)
        except asyncio.CancelledError:
            raise
        except SourceFailure as exc:
            for family in families:
                if any(e.section == family and e.code == "not_started" for e in envelope.errors):
                    update(envelope, family, missing(family, exc.code))
        except Exception as exc:
            for family in families:
                if any(e.section == family and e.code == "not_started" for e in envelope.errors):
                    update(envelope, family, missing(family, "company_exception", type(exc).__name__))
        finally:
            mark_registry(org)
            envelope.operations.runtime_ms = round((time.monotonic() - begin) * 1000)
    async def execute(active_client, nav_client=None):
        if storage_error is not None:return
        http = Http(active_client, config, budget, blobs)
        website_http = WebsiteHttp(active_client, config, budget, blobs, dns_metrics=dns_metrics)
        nav_task=asyncio.create_task(nav.prefetch(nav_client or active_client,config,budget,blobs,nav_index,nav_names,prior)) if config.hiring and valid_orgs else None
        # Start the credential/feed request before scheduling company crawls.
        if nav_task: await asyncio.sleep(0)
        tasks = [asyncio.create_task(company(org, http, website_http,nav_task)) for org in inputs.unique if valid(org)]
        try:
            return await finish_before_deadline(tasks, budget)
        finally:
            dns_metrics.update({'dns_precheck_lookups': website_http.dns_lookups, 'dns_candidates_by_company': website_http.dns_counts,
                                'dns_scope': 'prechecks, website preflight and pinned-transport connection resolutions'})
            if nav_task and not nav_task.done(): nav_task.cancel()
            if nav_task: await asyncio.gather(nav_task,return_exceptions=True)
    dns_metrics = {'dns_lookups': 0}
    if client is None:
        transport = safe_transport(config.workers * 2, dns_metrics) if config.websites or config.hiring else httpx.AsyncHTTPTransport(limits=httpx.Limits(max_connections=config.workers * 2))
        async with AsyncExitStack() as stack:
            shared=await stack.enter_async_context(httpx.AsyncClient(transport=transport, trust_env=False, headers={"Accept": "application/json", "User-Agent": "SignalpostAgent/1.0"}))
            dedicated=await stack.enter_async_context(httpx.AsyncClient(transport=safe_transport(config.nav_concurrency+1,dns_metrics),trust_env=False)) if config.hiring else None
            await execute(shared,dedicated)
    else:
        await execute(client)
    for org, envelope in envelopes.items():
        # Invalid numbers must never inherit previously published information.
        await asyncio.to_thread(finalize,envelope,prior.get(org) if valid(org) and storage_error is None else None,blobs,budget,budget.start)
    synthesis_service=SynthesisService(config,budget,synthesis_provider)
    for envelope in envelopes.values():
        envelope.run.synthesis=await synthesis_service.summarize(envelope)
        envelope.profile.synthesis=envelope.run.synthesis
    order = inputs.rows if config.emit_duplicates else inputs.unique
    result = [envelopes[org] for org in order]
    size, output_limited, minimum_exceeded = await asyncio.to_thread(write,config.output,result,config.envelope_shape,blobs,config.max_output_mb)
    report = build(result, inputs, budget, config, warnings, time.monotonic() - budget.start)
    report['limits']['max_requests']=budget.cap
    report['request_budget_basis']='20 per unique normalized input' if config.max_requests is None else 'explicit override'
    report['measured_request_projection']={'baseline':'1000-company retained-features run',
        'baseline_mean_http':5.975,'projected_http':round(5.975*len(inputs.unique)),
        'note':'Projection from a measured sample; source pagination/retries and feed changes can differ.'}
    report.update(dns_metrics)
    report['dns_amortized_per_company'] = dns_metrics.get('dns_lookups', 0) / len(result) if result else 0
    report['max_dns_requests_per_company'] = max((n for org,n in dns_metrics.get('dns_by_company', {}).items() if org in envelopes), default=0)
    report["bulk_snapshot_sha256"] = bulk_sha
    report['llm']=synthesis_service.metrics
    total=synthesis_service.metrics['estimated_usd']
    report.update({'total_cost_usd':total,'cost_per_100_companies_usd':total*100/len(envelopes) if envelopes else 0,
        'cost_per_official_batch_usd':total*config.official_batch_size/len(envelopes) if envelopes else 0})
    report['synthesis']={'companies':len(envelopes),'sentences':sum(e.run.synthesis.checks.sentences for e in envelopes.values()),
        'cited':sum(e.run.synthesis.checks.cited for e in envelopes.values()),
        'dropped_sentences':sum(e.run.synthesis.checks.dropped_sentences for e in envelopes.values())}
    report["input_readable"] = not any(w.startswith("input unreadable") for w in warnings)
    if config.hiring:
        report['hiring_prefetch']=nav_index.metrics
        details=sum('/feedentry/' in e['url'] and e.get('section')=='hiring_prefetch' for e in budget.events)
        report['nav_detail_requests']=details
        report['nav_detail_requests_per_company']=details/len(valid_orgs) if valid_orgs else 0
        report['nav_detail_requests_by_company']={org:nav_index.metrics.get('detail_requests_by_company',{}).get(org,0) for org in valid_orgs}
        report['hiring_prefetch']['matches_published']=sum(c.family=='hiring' and c.availability=='available' and not c.carried_forward for e in result for c in e.claims)
        report['hiring_prefetch']['companies_with_ads']=sum(any(c.family=='hiring' and c.availability=='available' and not c.carried_forward for c in e.claims) for e in result)
    report["output_bytes"] = size
    report["output_bytes_per_company"] = size / len(result) if result else 0
    report["output_limit_exceeded"] = size > config.max_output_mb * 1024 * 1024
    report["output_limited_companies"] = output_limited
    if config.profiles_output is not None:
        from .profiles import write as write_profiles
        try:
            report['profiles_output']=await asyncio.to_thread(write_profiles,config.profiles_output,result)
        except OSError as exc:
            report['profiles_output']={'state':'failed','error':type(exc).__name__}
            report['warnings'].append('profiles output failed: '+type(exc).__name__)
    if minimum_exceeded:
        report["warnings"].append("max-output-mb is smaller than mandatory terminal membership; minimal output written and limit flagged")
    if config.site_dir is not None:
        try:
            from .site import generate_site
            if any(p.resolve().is_relative_to(config.site_dir.resolve()) for p in
                   (config.output, config.report, config.profiles_output, config.organisations, config.bulk, config.previous) if p):
                raise ValueError('Site directory overlaps a run input or output')
            report['site'] = {'state': 'available', **await asyncio.to_thread(generate_site,config.output,config.site_dir)}
        except Exception as exc:
            report['site'] = {'state': 'failed', 'error': type(exc).__name__, 'message': str(exc)}
            report['warnings'].append('site generation failed: ' + type(exc).__name__)
    try:
        config.report.parent.mkdir(parents=True, exist_ok=True)
        config.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        report["warnings"].append(f"report write failed: {type(exc).__name__}")
    return report
