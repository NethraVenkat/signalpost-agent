from ..models.claim import Claim
from ..models.evidence import Evidence, canonical, utc_now
from ..models.envelope import Change

CHECKED={'available','not_available','not_applicable'}

def newly_supported_field(field):
    from ..sources.registry_fields import EXTRA,GROUPS
    from ..sources.regnskap import PATHS
    legacy={'revenue','operating_result','result_before_tax','net_result','equity','total_assets','total_liabilities'}
    return (field.startswith(('roles.detail.','subunits.detail.')) or
            field in {'identity.'+k for k in (*EXTRA,*GROUPS,'founding_date','vat_registration_date')} or
            field in {'accounts.'+k for k in PATHS.keys()-legacy})


def meaning(claim):
    if claim is None or claim.availability!='available': return None
    if claim.field=='official_website':
        from ..web.policy import domain
        # Proof strength/location and www/HTTPS variants describe observation,
        # rather than a move to another company website domain.
        return domain(claim.value['final_url'])
    if claim.field.startswith('website_description.'):
        return canonical({k:v for k,v in claim.value.items() if k not in {'identity_level','identity_claim_id'}})
    if claim.family=='accounts' and claim.reporting_period:
        period=claim.reporting_period
        return {'value':canonical(claim.value),'period':{k:period.get(k) for k in ('fiscal_year','period_start','period_end','currency','account_type')},
                'source_unit':period.get('source_unit',period.get('unit'))}
    return canonical(claim.value)


def apply(envelope, previous, blobs):
    envelope.run.refresh = {**envelope.run.refresh,"mode": "baseline" if previous is None else "refresh", "previous_run_id": None,'observation_changes':[]}
    if previous is None:
        envelope.run.refresh['observed_claim_ids'] = sorted(c.id for c in envelope.claims if c.availability == 'available')
        return
    old = previous.get("profile", previous) if "claims" not in previous else previous
    old_claims = {x["field"]: Claim.model_validate(x) for x in old.get("claims", [])}
    previous_refresh = previous.get('run', {}).get('refresh', old.get('refresh', {}))
    known_ids = set(previous_refresh.get('observed_claim_ids', []))
    known_ids.update(c.id for c in old_claims.values() if c.availability == 'available')
    envelope.run.refresh['observed_claim_ids'] = sorted(known_ids | {
        c.id for c in envelope.claims if c.availability == 'available'})
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
                    if envelope.run.refresh.get('hiring',{}).get('closure_requires_live_detail'):
                        continue  # Current-run live proof is mandatory for every ad.
                carried = claim.model_copy(update={"carried_forward": True})
                available.setdefault(carried.field,carried)
        retained = list(available.values())
        if retained:
            envelope.claims = [c for c in envelope.claims if c.family != family] + retained
    new_claims = {c.field: c for c in envelope.claims}
    for scoped_family in ('website','activity'):
        checked_urls = envelope.run.refresh.get(scoped_family, {}).get('checked_urls')
        if checked_urls is None or envelope.run.sections.get(scoped_family) not in {'available','not_available'}:continue
        for field, claim in old_claims.items():
            if claim.family != scoped_family or claim.availability != 'available' or field in new_claims or field == 'official_website': continue
            source_urls = {old_evidence[eid].source_url for eid in claim.evidence_ids if old_evidence[eid].source_class == 'company_owned'}
            if source_urls and not source_urls <= set(checked_urls):
                carried = claim.model_copy(update={'carried_forward': True})
                envelope.claims.append(carried);new_claims[field]=carried
                envelope.run.refresh['observation_changes'].append({'section':scoped_family,'field':field,
                    'previous_state':'available','current_state':'unchecked_page','reason':'supporting_'+scoped_family+'_page_not_checked'})
    for field in sorted(set(old_claims) | set(new_claims)):
        before, after = old_claims.get(field), new_claims.get(field)
        family = (after or before).family
        if family not in envelope.run.sections or family in failed:
            continue
        if family=='hiring' and before and before.availability=='available' and meaning(after) is None:
            hiring=envelope.run.refresh.get('hiring',{})
            if hiring.get('closure_requires_live_detail') and before.value.get('uuid') not in hiring.get('known_closed_jobs',[]):
                envelope.run.refresh['observation_changes'].append({'section':'hiring','field':field,
                    'previous_state':'available','current_state':'closure_not_verified','reason':'live_detail_did_not_prove_inactive_or_expired'})
                continue
        if before is None and newly_supported_field(field):
            envelope.run.refresh['observation_changes'].append({'section': family, 'field': field,
                'previous_state': 'unchecked_field', 'current_state': after.availability,
                'reason': 'dated_field_not_checked_in_previous_extractor'})
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
        if after and after.availability == 'available' and after.id in known_ids and meaning(before) is None:
            envelope.run.refresh['observation_changes'].append({
                'section': family, 'field': field, 'claim_id': after.id,
                'previous_state': before.availability if before else 'not_observed',
                'current_state': 'available', 'reason': 'previously_observed_claim_recovered'})
            continue
        if before is None and after and family in {'website', 'activity'} and after.availability == 'available':
            checked_before = previous_refresh.get(family, {}).get('checked_urls')
            source_urls = {new_evidence[eid].source_url for eid in after.evidence_ids
                           if eid in new_evidence and new_evidence[eid].source_class == 'company_owned'}
            old_site = old_claims.get('official_website')
            new_site = new_claims.get('official_website')
            same_site = meaning(old_site) is not None and meaning(old_site) == meaning(new_site)
            if same_site and checked_before is not None and source_urls and not source_urls <= set(checked_before):
                envelope.run.refresh['observation_changes'].append({
                    'section': family, 'field': field, 'claim_id': after.id,
                    'previous_state': 'unchecked_page', 'current_state': 'available',
                    'reason': 'newly_checked_supporting_page'})
                continue
        if before is None and after and after.availability != "available":
            continue
        if after is None and before and before.availability != "available":
            continue
        old_ids = before.evidence_ids if before else []
        new_ids = after.evidence_ids if after else []
        if family=='hiring' and before and meaning(after) is None:
            new_ids=envelope.run.refresh.get('hiring',{}).get('closure_evidence',{}).get(before.value.get('uuid'),new_ids)
        newest = new_evidence.get(new_ids[0]) if new_ids else None
        oldest = old_evidence.get(old_ids[0]) if old_ids else None
        envelope.changes.append(Change(
            organisation_number=envelope.organisation_number, type="closed_job" if family=='hiring' and meaning(before) is not None and meaning(after) is None else "added" if meaning(before) is None else "removed" if meaning(after) is None else "changed",
            field=field, old_value=before.value if before else None, new_value=after.value if after else None,
            old_evidence_ids=old_ids, new_evidence_ids=new_ids,
            materiality="minor" if field == "identity.registered_website" or family=='activity' else "material",
            first_observed_at=(before or after).first_observed_at, last_observed_at=utc_now(),
            source_url=newest.source_url if newest else None, retrieved_at=newest.retrieved_at if newest else None,
            effective_at=newest.effective_at if newest else None, source_class=newest.source_class if newest else None,
            old_locator=oldest.locator if oldest else None, new_locator=newest.locator if newest else None,
            old_content_sha256=oldest.content_sha256 if oldest else None, new_content_sha256=newest.content_sha256 if newest else None,
            status=after.availability if after else "not_available"))
    if "roles" not in failed:
        before_roles = [c for c in old_claims.values() if c.field.startswith('roles.role.') and c.availability == "available"]
        after_roles = [c for c in new_claims.values() if c.field.startswith('roles.role.') and c.availability == "available"]
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
                                           old_locator=oldest.locator if oldest else None, new_locator=newest.locator if newest else None,
                                           old_content_sha256=oldest.content_sha256 if oldest else None, new_content_sha256=newest.content_sha256 if newest else None,
                                           status="available" if after_roles else "not_available"))
    # Preserve prior source metadata even when the current source changes;
    # a fresh state directory needs no historical blobs or refetch.
    for evid in old_evidence.values():
        new_evidence.setdefault(evid.id, evid)
    envelope.evidence = list(new_evidence.values())
