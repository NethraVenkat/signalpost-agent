from ..models.claim import Claim
from ..models.evidence import Evidence, canonical, utc_now
from ..models.envelope import Change

CHECKED={'available','not_available','not_applicable'}


def meaning(claim):
    if claim is None or claim.availability!='available': return None
    if claim.field=='official_website':
        from ..web.policy import domain
        # Proof strength/location and www/HTTPS variants describe observation,
        # rather than a move to another company website domain.
        return domain(claim.value['final_url'])
    if claim.family=='accounts' and claim.reporting_period:
        period=claim.reporting_period
        return {'value':canonical(claim.value),'period':{k:period.get(k) for k in ('fiscal_year','period_start','period_end','currency','account_type')},
                'source_unit':period.get('source_unit',period.get('unit'))}
    return canonical(claim.value)


def apply(envelope, previous, blobs):
    envelope.run.refresh = {**envelope.run.refresh,"mode": "baseline" if previous is None else "refresh", "previous_run_id": None,'observation_changes':[]}
    if previous is None:
        return
    old = previous.get("profile", previous) if "claims" not in previous else previous
    old_claims = {x["field"]: Claim.model_validate(x) for x in old.get("claims", [])}
    old_evidence = {x["id"]: Evidence.model_validate(x) for x in old.get("evidence", [])}
    for item in old_evidence.values():
        if item.snapshot_body_base64:
            import base64
            from ..sources.excerpt import excerpt
            item.claim_span = excerpt(base64.b64decode(item.snapshot_body_base64), locator=item.locator)
            item.snapshot_body_base64 = None
    new_evidence = {x.id: x for x in envelope.evidence}
    envelope.run.refresh["previous_run_id"] = previous.get("run_id", previous.get("run", {}).get("run_id"))
    envelope.run.refresh["mode"] = "refresh"
    old_sections=previous.get('run',{}).get('sections',old.get('sections',{}))
    failed = {family for family,state in envelope.run.sections.items() if state not in CHECKED or old_sections.get(family) not in CHECKED}
    for family in failed:
        before=old_sections.get(family); after=envelope.run.sections.get(family)
        old_values=canonical([c.value for c in old_claims.values() if c.family==family and c.availability=='available'])
        new_values=canonical([c.value for c in envelope.claims if c.family==family and c.availability=='available'])
        if before!=after or old_values!=new_values:
            reasons=sorted({e.code for e in envelope.errors if e.section==family})
            envelope.run.refresh['observation_changes'].append({'section':family,'previous_state':before,'current_state':after,'reason':','.join(reasons) or 'section_not_successfully_checked_in_both_runs'})
    for family in failed:
        available = {c.field: c for c in envelope.claims if c.family == family and c.availability == "available"}
        for claim in old_claims.values():
            if claim.family == family and claim.availability == "available":
                if family=='hiring':
                    from ..sources.nav import timestamp
                    from datetime import datetime,timezone
                    expires=timestamp(claim.value.get('expires'))
                    if expires is None or expires<=datetime.now(timezone.utc) or claim.value.get('uuid') in envelope.run.refresh.get('hiring',{}).get('known_closed_jobs',[]):
                        continue
                carried = claim.model_copy(update={"carried_forward": True})
                available.setdefault(carried.field,carried)
        retained = list(available.values())
        if retained:
            envelope.claims = [c for c in envelope.claims if c.family != family] + retained
    new_claims = {c.field: c for c in envelope.claims}
    for field in sorted(set(old_claims) | set(new_claims)):
        before, after = old_claims.get(field), new_claims.get(field)
        family = (after or before).family
        if family not in envelope.run.sections or family in failed:
            continue
        if family == "roles":
            if before and after:
                after.first_observed_at = before.first_observed_at
            continue
        if before and after:
            after.first_observed_at = before.first_observed_at
            # Source retrieval time/hash/locator ordering is not material content.
            if meaning(before) == meaning(after):
                continue
        if meaning(before)==meaning(after): continue
        if before is None and after and after.availability != "available":
            continue
        if after is None and before and before.availability != "available":
            continue
        old_ids = before.evidence_ids if before else []
        new_ids = after.evidence_ids if after else []
        newest = new_evidence.get(new_ids[0]) if new_ids else None
        oldest = old_evidence.get(old_ids[0]) if old_ids else None
        envelope.changes.append(Change(
            organisation_number=envelope.organisation_number, type="closed_job" if family=='hiring' and meaning(before) is not None and meaning(after) is None else "added" if meaning(before) is None else "removed" if meaning(after) is None else "changed",
            field=field, old_value=before.value if before else None, new_value=after.value if after else None,
            old_evidence_ids=old_ids, new_evidence_ids=new_ids,
            materiality="minor" if field == "identity.registered_website" else "material",
            first_observed_at=(before or after).first_observed_at, last_observed_at=utc_now(),
            source_url=newest.source_url if newest else None, retrieved_at=newest.retrieved_at if newest else None,
            effective_at=newest.effective_at if newest else None, source_class=newest.source_class if newest else None,
            old_content_sha256=oldest.content_sha256 if oldest else None, new_content_sha256=newest.content_sha256 if newest else None,
            status=after.availability if after else "not_available"))
    if "roles" not in failed:
        before_roles = [c for c in old_claims.values() if c.family == "roles" and c.availability == "available"]
        after_roles = [c for c in new_claims.values() if c.family == "roles" and c.availability == "available"]
        before_values = [c.value for c in before_roles]
        after_values = [c.value for c in after_roles]
        if canonical(before_values) != canonical(after_values):
            old_ids = list(dict.fromkeys(ref for c in before_roles for ref in c.evidence_ids))
            new_ids = list(dict.fromkeys(ref for c in after_roles for ref in c.evidence_ids))
            oldest = old_evidence.get(old_ids[0]) if old_ids else None
            newest = new_evidence.get(new_ids[0]) if new_ids else None
            envelope.changes.append(Change(organisation_number=envelope.organisation_number, type="changed", field="roles.roles",
                                           old_value=before_values or None, new_value=after_values or None,
                                           old_evidence_ids=old_ids, new_evidence_ids=new_ids, materiality="material",
                                           first_observed_at=(before_roles or after_roles)[0].first_observed_at, last_observed_at=utc_now(),
                                           source_url=newest.source_url if newest else None, retrieved_at=newest.retrieved_at if newest else None,
                                           effective_at=newest.effective_at if newest else None, source_class=newest.source_class if newest else None,
                                           old_content_sha256=oldest.content_sha256 if oldest else None, new_content_sha256=newest.content_sha256 if newest else None,
                                           status="available" if after_roles else "not_available"))
    # Preserve prior source metadata even when the current source changes;
    # a fresh state directory needs no historical blobs or refetch.
    for evid in old_evidence.values():
        new_evidence.setdefault(evid.id, evid)
    envelope.evidence = list(new_evidence.values())
