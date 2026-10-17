from .workers import offload
from .progress import ProgressWriter
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
# Bound on waiting for cancelled work; terminal output is written regardless.
CANCEL_GRACE_SECONDS = 5


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


def finalize(envelope, old, blobs, budget, began, verify_identity=False):
    for family in envelope.run.sections:
        if any(e.section == family and e.code == "not_started" for e in envelope.errors):
            update(envelope, family, missing(family, "deadline"))
    try:
        if verify_identity and old is not None:
            # Strict identity checks cannot be bypassed by refresh carry-forward.
            import copy
            old = copy.deepcopy(old)
            holder = old if 'claims' in old else old.get('profile', old)
            holder['claims'] = [c for c in holder.get('claims', []) if c.get('family') != 'identity']
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

def extract_company_scope(envelope, bulk_row=None, prior_row=None):
    org = envelope.organisation_number
    subunits = {org}
    names = set()
    for c in envelope.claims:
        if c.availability == 'available':
            if c.field == 'identity.legal_name' and c.value:
                names.add(nav.normal_name(c.value))
            elif c.family == 'subunits' and isinstance(c.value, dict):
                unit = c.value.get('organisation_number')
                if valid(str(unit)):
                    subunits.add(str(unit))
                if c.value.get('name'):
                    names.add(nav.normal_name(c.value.get('name')))
            elif c.family == 'website' and 'brand' in c.field:
                val = c.value.get('name') if isinstance(c.value, dict) else c.value
                if val:
                    names.add(nav.normal_name(val))
    if bulk_row:
        try:
            val = bulk_registry.column(bulk_row[0], 'navn')[0]
            if val:
                names.add(nav.normal_name(val))
        except Exception:
            pass
    if prior_row:
        for claim in prior_row.get('claims', prior_row.get('profile', {}).get('claims', [])):
            if claim.get('availability') == 'available' and claim.get('family') == 'website' and 'brand' in claim.get('field', ''):
                val = claim.get('value')
                if val:
                    names.add(nav.normal_name(val.get('name') if isinstance(val, dict) else val))
    return org, subunits, names


def write_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


async def run(config, client=None,synthesis_provider=None):
    from .monitor import LoopMonitor
    from .power import SystemAwake
    with SystemAwake(config.prevent_system_sleep) as power:
        monitor=LoopMonitor();monitor.start()
        try:report=await _run(config,client,synthesis_provider)
        finally:lag=await monitor.stop()
    report['event_loop']=lag
    report['system_awake_request']=power.result
    try:
        await offload(write_report,config.report,report)
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
    valid_orgs = {org for org in inputs.unique if valid(org)}
    # Initialize progress writer for optional status panel.
    stage_names = ["Registry & Subunits"]
    if config.websites:
        stage_names.append("Website Verification")
    if config.hiring:
        stage_names.append("NAV Hiring Matching")
    stage_names.extend(["Cited Synthesis", "Output & Site Publishing"])
    progress = ProgressWriter(
        state_dir=config.state_dir,
        run_id=config.run_id,
        total_companies=len(valid_orgs) if valid_orgs else len(inputs.unique),
        input_rows=len(inputs.rows),
        duplicate_inputs=len(inputs.rows) - len(inputs.unique),
        request_limit=budget.cap if hasattr(budget, 'cap') else None,
        stages=stage_names,
        extra_path=(config.site_dir / "progress.json") if config.site_dir else None,
    )
    progress.start(budget)
    progress.log_event(f"Pipeline started with {len(inputs.rows)} input rows, {len(inputs.unique)} unique companies")
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
            bulk, bulk_sha = await offload(bulk_registry.load,config.bulk,valid_orgs,blobs,budget)
        except Exception as exc:
            warnings.append(f"bulk unavailable: {getattr(exc, 'code', type(exc).__name__)}; live fallback")
    if bulk and not config.verify_bulk:
        # Identity comes straight from the CSV row, before any network work and
        # outside the deadline, so a deadline can never remove it. Only companies
        # missing from the CSV depend on the live registry.
        def csv_identities():
            found = {}
            for org in valid_orgs:
                if org in bulk:
                    try:
                        found[org] = bulk_registry.extract(org, *bulk[org])
                    except Exception:
                        pass  # The company task retries and records the failure.
            return found
        for org, section in (await offload(csv_identities)).items():
            update(envelopes[org], "identity", section)
    from .sources.subunits import build_subunit_map
    pre_loaded_subunit_map = await offload(build_subunit_map, inputs, bulk, prior)
    semaphore = asyncio.Semaphore(config.workers)
    website_semaphore = asyncio.Semaphore(config.workers)
    nav_index=nav.Index()
    nav_index.started=asyncio.Event()
    registry_done=set()
    registry_ready=asyncio.Event()
    timing_markers = {}
    subunits_done = set()
    registry_families_done = set()
    scopes_pushed = set()
    scopes_dict = {org: {org} for org in valid_orgs}
    if pre_loaded_subunit_map:
        for p, subs in pre_loaded_subunit_map.parent_subunits.items():
            if p in scopes_dict:
                scopes_dict[p].update(subs)
    subunit_queue = asyncio.Queue(maxsize=100) if config.hiring else None
    queue_closed = asyncio.Event()
    # NAV prefetch sets `stopped` when its queue reader exits; the streaming
    # fallback clears `used` because it never reads the queue. Producers must
    # then stop waiting for queue space.
    subunit_consumer = SimpleNamespace(stopped=asyncio.Event(), used=True)
    undelivered_scopes = {}
    scopes_delivered = set()

    async def deliver(item):
        """Queue one item, never waiting past the deadline or after the reader stopped."""
        if subunit_consumer.stopped.is_set():
            return 'nav_consumer_stopped'
        try:
            subunit_queue.put_nowait(item)
            return None
        except asyncio.QueueFull:
            pass
        remaining = budget.deadline - time.monotonic()
        if remaining <= 0:
            return 'deadline'
        put = asyncio.ensure_future(subunit_queue.put(item))
        stopped = asyncio.ensure_future(subunit_consumer.stopped.wait())
        try:
            await asyncio.wait({put, stopped}, timeout=remaining, return_when=asyncio.FIRST_COMPLETED)
        finally:
            for waiter in (put, stopped):
                if not waiter.done():
                    waiter.cancel()
            await asyncio.gather(put, stopped, return_exceptions=True)
        if put.done() and not put.cancelled() and put.exception() is None:
            return None
        return 'nav_consumer_stopped' if subunit_consumer.stopped.is_set() else 'deadline'

    async def push_subunit_scope(org, envelope):
        if org in scopes_pushed:
            return
        scopes_pushed.add(org)
        if subunit_queue is not None:
            item = await offload(extract_company_scope, envelope, bulk.get(org), prior.get(org))
            scopes_dict[org] = item[1]
            if not subunit_consumer.used:
                return
            failure = await deliver(item)
            if failure and subunit_consumer.used:
                # NAV never saw this scope. The queue stays open, so coverage is
                # never reported ready and this company's hiring section fails.
                undelivered_scopes[org] = failure
                return
            scopes_delivered.add(org)
            # Close only after every scope is enqueued, so none lands behind the sentinel.
            if valid_orgs <= scopes_delivered and not queue_closed.is_set():
                if await deliver(None) is None:
                    queue_closed.set()

    def mark_registry(org):
        registry_done.add(org)
        if valid_orgs <= registry_done: registry_ready.set()
    async def nav_names():
        await registry_ready.wait()
        return await offload(nav.company_names,list(envelopes.values()),prior)
    # Seed discovery before the first page; verified subunit names augment this
    # index when registry work completes. These names never authorize publication.
    nav_names.initial_names = {
        org: {nav.normal_name(bulk_registry.column(bulk[org][0], 'navn')[0])}
        if org in bulk else set() for org in valid_orgs
    }
    nav_names.pre_loaded_subunit_map = pre_loaded_subunit_map
    nav_names.subunit_queue = subunit_queue
    nav_names.subunit_consumer = subunit_consumer
    async def nav_scopes():
        await registry_ready.wait()
        return scopes_dict
    nav_names.scopes_ready=nav_scopes
    async def company(org, http, website_http, nav_task):
        from .web.policy import DNS_ORG
        DNS_ORG.set(org)
        envelope = envelopes[org]
        begin = time.monotonic()
        progress.company_started(org)
        if not valid(org):
            for family in families:
                update(envelope, family, missing(family, "invalid_orgnr"))
            progress.company_completed(org, success=False)
            return
        try:
            async with semaphore:
                budget.check()
                async def identity():
                    if org in bulk and not config.verify_bulk:
                        return await offload(bulk_registry.extract,org,*bulk[org])
                    return await brreg_enhet.fetch(org, http)
                if envelope.run.sections["identity"] != "available":
                    await isolate(envelope, "identity", identity)
                if envelope.run.sections["identity"] != "available":
                    for family in families[1:]:
                        state = envelope.run.sections["identity"]
                        inherited = next((e.code for e in envelope.errors if e.section == "identity" and e.code in {"budget_exhausted", "deadline"}), "identity_unverified")
                        update(envelope, family, missing(family, inherited, state=state))
                    subunits_done.add(org)
                    if valid_orgs <= subunits_done and 'subunits_complete_seconds' not in timing_markers:
                        timing_markers['subunits_complete_seconds'] = time.monotonic() - budget.start
                    registry_families_done.add(org)
                    if valid_orgs <= registry_families_done and 'registry_complete_seconds' not in timing_markers:
                        timing_markers['registry_complete_seconds'] = time.monotonic() - budget.start
                    await push_subunit_scope(org, envelope)
                    return
                await isolate(envelope, "subunits", lambda: brreg_underenheter.fetch(org, http, progress=lambda partial: update(envelope, "subunits", partial)))
                subunits_done.add(org)
                if valid_orgs <= subunits_done and 'subunits_complete_seconds' not in timing_markers:
                    timing_markers['subunits_complete_seconds'] = time.monotonic() - budget.start
                await push_subunit_scope(org, envelope)
                mark_registry(org)
            async with semaphore:
                for family, source in (("roles", brreg_roller), ("accounts", regnskap)):
                    await isolate(envelope, family, lambda source=source: source.fetch(org, http))
                registry_families_done.add(org)
                if valid_orgs <= registry_families_done and 'registry_complete_seconds' not in timing_markers:
                    timing_markers['registry_complete_seconds'] = time.monotonic() - budget.start
            async with website_semaphore:
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
                    if org in undelivered_scopes:
                        raise SourceFailure(undelivered_scopes[org])
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
            subunits_done.add(org)
            if valid_orgs <= subunits_done and 'subunits_complete_seconds' not in timing_markers:
                timing_markers['subunits_complete_seconds'] = time.monotonic() - budget.start
            registry_families_done.add(org)
            if valid_orgs <= registry_families_done and 'registry_complete_seconds' not in timing_markers:
                timing_markers['registry_complete_seconds'] = time.monotonic() - budget.start
            await push_subunit_scope(org, envelope)
            mark_registry(org)
            envelope.operations.runtime_ms = round((time.monotonic() - begin) * 1000)
            is_success = not all(s == 'failed' for s in envelope.run.sections.values())
            progress.company_completed(org, success=is_success)
    async def execute(active_client, nav_client=None):
        if storage_error is not None:return
        http = Http(active_client, config, budget, blobs)
        website_http = WebsiteHttp(active_client, config, budget, blobs, dns_metrics=dns_metrics)
        from .web.search import Search
        website_http.search=Search(active_client,config,budget)
        search_metrics.update(website_http.search.metrics)
        website_http.search.metrics=search_metrics
        nav_task=asyncio.create_task(nav.prefetch(nav_client or active_client,config,budget,blobs,nav_index,nav_names,prior)) if config.hiring and valid_orgs else None
        if nav_task:
            nav_task.add_done_callback(lambda _: subunit_consumer.stopped.set())
        else:
            subunit_consumer.stopped.set()
        # Start the credential/feed request before scheduling company crawls.
        if nav_task:
            started_task=asyncio.create_task(nav_index.started.wait())
            try:
                await asyncio.wait({nav_task,started_task},return_when=asyncio.FIRST_COMPLETED,
                                   timeout=max(0,budget.deadline-time.monotonic()))
            finally:
                if not started_task.done():started_task.cancel()
                await asyncio.gather(started_task,return_exceptions=True)
        progress.stage_update("Registry & Subunits", "running")
        tasks = [asyncio.create_task(company(org, http, website_http,nav_task)) for org in inputs.unique if valid(org)]
        try:
            pending, stuck = await finish_before_deadline(tasks, budget, CANCEL_GRACE_SECONDS)
            if stuck:
                warnings.append(f"{stuck} company tasks did not stop within {CANCEL_GRACE_SECONDS}s of cancellation; unfinished sections are reported as deadline")
            return pending
        finally:
            dns_metrics.update({'dns_precheck_lookups': website_http.dns_lookups, 'dns_candidates_by_company': website_http.dns_counts,
                                'dns_scope': 'prechecks, website preflight and pinned-transport connection resolutions'})
            if subunit_queue is not None:
                for org in valid_orgs:
                    if org not in scopes_pushed:
                        await push_subunit_scope(org, envelopes[org])
            if nav_task and not nav_task.done(): nav_task.cancel()
            if nav_task:
                await asyncio.wait({nav_task}, timeout=CANCEL_GRACE_SECONDS)
                if not nav_task.done():
                    warnings.append(f"NAV prefetch did not stop within {CANCEL_GRACE_SECONDS}s of cancellation")
                elif not nav_task.cancelled():
                    nav_task.exception()  # Retrieved; failures are already recorded on the index.
    dns_metrics = {'dns_lookups': 0}
    search_metrics={'status':'not configured','queries':0,'estimated_usd':0.}
    if client is None:
        transport = safe_transport(config.workers * 2, dns_metrics) if config.websites or config.hiring else httpx.AsyncHTTPTransport(limits=httpx.Limits(max_connections=config.workers * 2))
        async with AsyncExitStack() as stack:
            shared=await stack.enter_async_context(httpx.AsyncClient(transport=transport, trust_env=False, headers={"Accept": "application/json", "User-Agent": "SignalpostAgent/1.0"}))
            dedicated=await stack.enter_async_context(httpx.AsyncClient(transport=safe_transport(config.nav_concurrency+1,dns_metrics),trust_env=False)) if config.hiring else None
            await execute(shared,dedicated)
    else:
        await execute(client)
    progress.stage_update("Registry & Subunits", "completed")
    progress.log_event("Registry and subunit processing complete")
    if config.websites:
        progress.stage_update("Website Verification", "completed")
        progress.log_event("Website verification complete")
    if config.hiring:
        progress.stage_update("NAV Hiring Matching", "completed")
        progress.log_event("NAV hiring matching complete")
    finalisation_began = time.monotonic()
    for org, envelope in envelopes.items():
        # A company's website deadline must not hide NAV details already
        # verified by the independent shared reader. No requests occur here.
        if config.hiring and valid(org) and not any(c.family=='hiring' and c.availability=='available' for c in envelope.claims):
            scope={org} | {c.value['organisation_number'] for c in envelope.claims
                if c.family=='subunits' and c.availability=='available' and isinstance(c.value,dict) and c.value.get('organisation_number')}
            if any(nav_index.ads.get(number) for number in scope):
                await isolate(envelope,'hiring',lambda:offload(nav.section,envelope,nav_index,blobs,prior.get(org)))
        # Invalid numbers must never inherit previously published information.
        await offload(finalize,envelope,prior.get(org) if valid(org) and storage_error is None else None,blobs,budget,budget.start,config.verify_bulk)
    progress.stage_update("Cited Synthesis", "running")
    synthesis_service=SynthesisService(config,budget,synthesis_provider)
    for envelope in envelopes.values():
        envelope.run.synthesis=await synthesis_service.summarize(envelope)
        envelope.profile.synthesis=envelope.run.synthesis
    progress.stage_update("Cited Synthesis", "completed")
    progress.log_event("Cited synthesis complete")
    progress.stage_update("Output & Site Publishing", "running")
    order = inputs.rows if config.emit_duplicates else inputs.unique
    result = [envelopes[org] for org in order]
    size, output_limited, minimum_exceeded = await offload(write,config.output,result,config.envelope_shape,blobs,config.max_output_mb)
    report = await offload(build,result,inputs,budget,config,warnings,time.monotonic() - budget.start)
    report['limits']['max_requests']=budget.cap
    report['request_budget_basis']='20 per unique normalized input' if config.max_requests is None else 'explicit override'
    report['measured_request_projection']={'baseline':'1000-company retained-features run',
        'baseline_mean_http':5.975,'projected_http':round(5.975*len(inputs.unique)),
        'note':'Projection from a measured sample; source pagination/retries and feed changes can differ.'}
    report.update(dns_metrics)
    report['dns_amortized_per_company'] = dns_metrics.get('dns_lookups', 0) / len(result) if result else 0
    report['max_dns_requests_per_company'] = max((n for org,n in dns_metrics.get('dns_by_company', {}).items() if org in envelopes), default=0)
    report["bulk_snapshot_sha256"] = bulk_sha
    from .io.provenance import registry_provenance
    report['registry_provenance'] = await offload(registry_provenance,result,budget.events,injected_client=client is not None)
    report['registry_provenance']['verify_bulk'] = config.verify_bulk
    report['llm']=synthesis_service.metrics
    report['search']=search_metrics
    total=synthesis_service.metrics['estimated_usd']+search_metrics['estimated_usd']
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
    if 'first_detail_seconds' in nav_index.metrics:
        timing_markers['first_detail_seconds'] = nav_index.metrics.get('first_detail_seconds')
    if 'last_detail_seconds' in nav_index.metrics:
        timing_markers['last_detail_seconds'] = nav_index.metrics.get('last_detail_seconds')
    if 'runtime_seconds' in nav_index.metrics:
        timing_markers['nav_runtime_seconds'] = nav_index.metrics.get('runtime_seconds')
    if timing_markers:
        report['timing_markers'] = timing_markers
    report["output_bytes"] = size
    report["output_bytes_per_company"] = size / len(result) if result else 0
    report["output_limit_exceeded"] = size > config.max_output_mb * 1024 * 1024
    report["output_limited_companies"] = output_limited
    if config.profiles_output is not None:
        from .profiles import write as write_profiles
        try:
            report['profiles_output']=await offload(write_profiles,config.profiles_output,result)
        except OSError as exc:
            report['profiles_output']={'state':'failed','error':type(exc).__name__}
            report['warnings'].append('profiles output failed: '+type(exc).__name__)
    if minimum_exceeded:
        report["warnings"].append("max-output-mb is smaller than mandatory terminal membership; minimal output written and limit flagged")
    # Envelopes and profiles are already written. Write the report next, so the
    # required outputs exist before the optional site is attempted.
    outputs_done = time.monotonic()
    report['finalisation'] = {'crawl_seconds': round(finalisation_began - budget.start, 2),
        'outputs_seconds': round(outputs_done - finalisation_began, 2),
        'estimate_seconds': round(budget.finalise_estimate, 2), 'site_estimate_seconds': round(budget.site_estimate, 2),
        'site_reserved': budget.site_reserved}
    if config.site_dir is not None:
        report['site'] = {'state': 'pending'}
    async def save_report():
        try:
            await offload(write_report,config.report,report)
        except OSError as exc:
            report["warnings"].append(f"report write failed: {type(exc).__name__}")
    await save_report()
    if config.site_dir is not None:
        site_estimate = budget.site_estimate
        if budget.seconds_left() < site_estimate:
            report['site'] = {'state': 'skipped', 'reason': 'time_budget', 'seconds_left': round(budget.seconds_left(), 2),
                              'estimated_seconds': round(site_estimate, 2)}
            report['warnings'].append('site generation skipped: not enough time budget left; envelopes, profiles and report are complete')
        else:
            try:
                from .site import generate_site
                if any(p.resolve().is_relative_to(config.site_dir.resolve()) for p in
                       (config.output, config.report, config.profiles_output, config.organisations, config.bulk, config.previous) if p):
                    raise ValueError('Site directory overlaps a run input or output')
                site_began = time.monotonic()
                report['site'] = {'state': 'available', **await offload(generate_site,config.output,config.site_dir)}
                report['finalisation']['site_seconds'] = round(time.monotonic() - site_began, 2)
            except Exception as exc:
                report['site'] = {'state': 'failed', 'error': type(exc).__name__, 'message': str(exc)}
                report['warnings'].append('site generation failed: ' + type(exc).__name__)
        await save_report()
    progress.stage_update("Output & Site Publishing", "completed")
    progress.log_event("Pipeline complete")
    progress.set_cost(total)
    await progress.stop(budget)
    return report
