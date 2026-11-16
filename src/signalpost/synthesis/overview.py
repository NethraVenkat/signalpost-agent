"""A closed, cited briefing contract; observations are not publisher facts."""
from ..models.evidence import digest
from ..models.synthesis import Sentence, RunObservation
from .financial import analyze, metric_sentence
from .catalog import change_claims, leaves

TOPICS = ('activity','change','unknown','financial','takeaway')
from ..sources.exact_official import FAMILIES as OFFICIAL_FAMILIES
FAMILIES = ('identity','roles','subunits','accounts','website','hiring','activity','gleif','procurement')+OFFICIAL_FAMILIES
STATE_REASON = {'available':'Supported section facts were returned.', 'failed':'Source checking was incomplete.',
                'blocked':'Source access was refused.', 'ambiguous':'Attribution or coverage was ambiguous.',
                'not_available':'No supported value was found in the checked source scope.',
                'not_applicable':'This source was not enabled or was not applicable.',
                'not_recorded':'No source-check state was recorded.'}


def supported(envelope):
    from .validate import permitted
    evidence={e.id for e in envelope.evidence}
    return [c for c in envelope.claims if c.availability=='available' and c.evidence_ids
            and not set(c.evidence_ids)-evidence and permitted(c,envelope)]


def observation(envelope, kind, section, data):
    return RunObservation(id='obs-'+digest([envelope.organisation_number,kind,section,data]),kind=kind,section=section,data=data)


def observations(envelope):
    claims=supported(envelope); metrics,year_check,gaps=analyze(envelope)
    result=[]
    for family in FAMILIES:
        if family in {'gleif','procurement',*OFFICIAL_FAMILIES} and family not in envelope.run.sections:continue
        codes=sorted({e.code for e in getattr(envelope,'errors',[]) if e.section==family and e.code!='website_candidates'})
        state=envelope.run.sections.get(family,'not_recorded')
        result.append(observation(envelope,'source_status',family,{'state':state,'reason':STATE_REASON[state],'reason_codes':codes}))
    first=not envelope.changes and envelope.run.refresh.get('mode')!='refresh'
    result.append(observation(envelope,'comparison','refresh',{'first_run':first,'mode':envelope.run.refresh.get('mode'),'verified_changes':len(envelope.changes)}))
    activity=[c.id for c in claims if c.field in {'identity.registered_activity','identity.statutory_purpose'} or c.field.startswith(('identity.nace','website_description.'))]
    result.append(observation(envelope,'coverage','description',{'supported_activity_claim_ids':sorted(activity)}))
    result.append(observation(envelope,'coverage','financials',{'gaps':gaps,'input_claim_ids':sorted(c.id for c in claims if c.family=='accounts'), 'year_check':year_check}))
    result.append(observation(envelope,'scope','report',{'future_performance_assessed':False,'commercial_suitability_assessed':False}))
    return result


def gap(envelope, contexts):
    ranked={'failed':0,'blocked':1,'ambiguous':2,'not_recorded':3,'not_available':4,'not_applicable':5}
    options=[c for c in contexts if c.kind=='source_status' and c.data['state']!='available']
    return min(options,key=lambda c:(ranked.get(c.data['state'],9),FAMILIES.index(c.section))) if options else None


def required(envelope):
    claims=supported(envelope); by_field={c.field:c for c in claims}
    contexts=observations(envelope); lookup={(c.kind,c.section):c for c in contexts}
    metrics,year_check,gaps=analyze(envelope)
    identity=by_field.get('identity.legal_name')
    reference=[identity.id] if identity else ([claims[0].id] if claims else [])
    name=str(identity.value) if identity else envelope.organisation_number
    selected_gap=gap(envelope,contexts)
    result={}
    def make(topic,text,ids=None,obs=(),derived=False):
        return Sentence(text=text,claim_ids=list(dict.fromkeys(reference if ids is None else ids)),
                        observation_ids=list(dict.fromkeys(obs)),topic=topic,value_kind='derived' if derived else 'reported')
    activity=next((by_field[f] for f in ('identity.registered_activity','identity.statutory_purpose') if f in by_field and any(v.strip() for v in leaves(by_field[f].value))),None)
    if activity:
        value=next((v for v in leaves(activity.value) if v.strip()),'')[:300]
        prefix='Previously supported ' if activity.carried_forward else ''
        result['activity']=make('activity',prefix+'Registered activity: «'+value+'».',[activity.id])
    else:
        description=next((c for c in claims if c.field.startswith('website_description.')),None)
        from .nace import unspecified
        industry=next((c for c in claims if c.field.startswith('identity.nace') and isinstance(c.value,dict) and c.value.get('kode') and not unspecified(c.value)),None)
        if description:
            result['activity']=make('activity',('Previously supported ' if description.carried_forward else '')+'Website self-description: «'+str(description.value['text'])[:300]+'».',[description.id])
        elif industry:
            from .readability import nace_sentence
            result['activity']=make('activity',nace_sentence(industry),[industry.id])
        else:
            result['activity']=make('activity','What the company does is unknown in this report: no supported activity, purpose, industry or website description is present.',obs=[lookup['coverage','description'].id])
    names=sorted((c for c in claims if c.field=='public_brand' or c.field.startswith('brand.')),
                 key=lambda c:(c.field!='public_brand',c.field))
    if names:
        alias=names[0];value=alias.value if isinstance(alias.value,str) else alias.value['name']
        label='Site-declared public name: ' if alias.field=='public_brand' else 'Registered workplace name: '
        if alias.carried_forward:label='Previously supported '+label.lower()
        sentence=result['activity']
        result['activity']=sentence.model_copy(update={'text':sentence.text+' '+label+'«'+value+'».',
            'claim_ids':list(dict.fromkeys([*sentence.claim_ids,alias.id]))})
    refresh=lookup['comparison','refresh']
    if not refresh.data['first_run'] and envelope.changes:
        event=sorted(envelope.changes,key=lambda e:(e.last_observed_at,e.field),reverse=True)[0]
        sides=[c for c in change_claims(envelope) if c.field in {event.field+'.old',event.field+'.new'}]
        from .template import projected
        detail='; '.join(('Previous: ' if c.field.endswith('.old') else 'Current: ')+projected(c) for c in sorted(sides,key=lambda c:not c.field.endswith('.old')))
        qualifier=' reported observations changed (not a year-on-year calculation)' if event.field.startswith('accounts.') else ' changed'
        result['change']=make('change','Since the previous run, '+event.field+qualifier+'; '+detail+'.',[c.id for c in sides],[refresh.id])
    elif not refresh.data['first_run']:
        text='No verified changes were detected in the compared source scope'
        obs=[refresh.id]
        if selected_gap:
            text+='; '+selected_gap.section+' remains '+selected_gap.data['state']
            obs.append(selected_gap.id)
        result['change']=make('change',text+'.',obs=obs)
    else:
        from ..registry_activity import recent
        from ..sources.registry_changes import sentence as registry_sentence, significant_recent
        formal=significant_recent([c for c in claims if c.field.startswith('registry_change.') and not c.carried_forward])
        events=[(formal.value['date'],registry_sentence(formal.value),formal)] if formal else []
        events += [(day,label+': '+day+'.',c) for day,label,c in recent(envelope)]
        if events:
            day,text,item=events[0] if formal else max(events,key=lambda item:(item[0],item[2].id))
            wording='significant recent registry event: ' if formal else 'most recent dated registry observation: '
            result['change']=make('change','First run for this company; '+wording+text,[item.id],[refresh.id])
        else:
            registry_status=lookup['source_status','activity']
            result['change']=make('change','First run for this company; no supported dated registry event is available in this report (activity state: '+registry_status.data['state']+').',obs=[refresh.id,registry_status.id])
    if selected_gap:
        state=selected_gap.data['state']; codes=selected_gap.data['reason_codes']
        reasons={'failed':'checking was incomplete','blocked':'source access was refused','ambiguous':'attribution or coverage was ambiguous',
                 'not_recorded':'no check state was recorded','not_available':'no supported value was found in the checked scope',
                 'not_applicable':'this source was not enabled or applicable'}
        text='What is unknown: '+selected_gap.section+' is '+state+' because '+reasons.get(state,'the source state is unresolved')
        if codes:text+=' (recorded reasons: '+', '.join(codes)+')'
        result['unknown']=make('unknown',text+'.',obs=[selected_gap.id])
    elif gaps:
        result['unknown']=make('unknown','What is unknown: financial comparison remains limited because '+gaps.get('revenue_yoy',next(iter(gaps.values())))+'.',obs=[lookup['coverage','financials'].id])
    else:
        result['unknown']=make('unknown','Future performance and commercial suitability are unknown: this report covers observed source facts, not a forecast or suitability assessment.',obs=[lookup['scope','report'].id])
    metric_ids=list(dict.fromkeys(cid for m in metrics for cid in m.input_claim_ids))
    current_revenue=by_field.get('accounts.revenue')
    if current_revenue:metric_ids.append(current_revenue.id)
    pieces=[metric_sentence(m).text.removesuffix('.') for m in metrics]
    if year_check and year_check['newer_filing_exists']:
        pieces.append('Newer filing exists: the registry lists accounts year '+year_check['registry_year']+' while these figures cover '+year_check['figures_year'])
        metric_ids+=year_check['claim_ids']
    if 'revenue_yoy' in gaps:pieces.append('Year-on-year revenue direction is unknown because '+gaps['revenue_yoy'])
    if pieces:
        result['financial']=make('financial','; '.join(pieces)+'.',metric_ids or reference,[lookup['coverage','financials'].id],derived=bool(metrics))
    else:
        result['financial']=make('financial','Financial ratios are unknown: '+('; '.join(sorted(set(gaps.values()))) or 'supported inputs are missing')+'.',obs=[lookup['coverage','financials'].id])
    if result['activity'].observation_ids:
        takeaway='Partner-screening takeaway: establish what '+name+' actually does before outreach because this report has no supported activity description.'
        ids=reference; obs=[lookup['coverage','description'].id]
    else:
        takeaway='Partner-screening takeaway: use the cited activity for '+name+' as an initial relevance check'
        ids=reference+result['activity'].claim_ids
        if selected_gap:
            takeaway+=', and resolve the '+selected_gap.section+' gap ('+selected_gap.data['state']+') before outreach.'
            obs=[selected_gap.id]
        else:
            takeaway+=', while independently assessing commercial fit because this report covers source facts only.'
            obs=[lookup['scope','report'].id]
    result['takeaway']=make('takeaway',takeaway,ids,obs)
    return result


def install(synthesis,envelope):
    synthesis.contract_version='r5-S'
    synthesis.observations=observations(envelope)
    synthesis.financial_metrics,synthesis.financial_year_check,_=analyze(envelope)
    core=required(envelope)
    synthesis.sections.changes=[s for s in synthesis.sections.changes if not s.text.startswith(('First observation;','No changes since the previous run.'))]
    synthesis.sections.changes=[s for s in synthesis.sections.changes if not (s.text.startswith('Change:') and set(s.claim_ids)==set(core['change'].claim_ids))]
    synthesis.sections.what_it_does=[s for s in synthesis.sections.what_it_does if s.text!=core['activity'].text]
    synthesis.sections.what_it_does.append(core['activity'])
    synthesis.sections.changes.insert(0,core['change'])
    synthesis.sections.limitations=[core['unknown']]
    synthesis.sections.scale.append(core['financial'])
    synthesis.sections.scale.extend(metric_sentence(m) for m in synthesis.financial_metrics)
    synthesis.sections.takeaway=[core['takeaway']]
    synthesis.briefing=[core[t] for t in TOPICS]
    leader=next((s for s in synthesis.sections.leadership if s.claim_ids),None)
    if leader:synthesis.briefing.insert(1,leader)
    from ..sources.exact_public import briefing_sentences
    for sentence in briefing_sentences(envelope):
        synthesis.briefing.append(sentence)
        synthesis.sections.leadership.append(sentence)
    return synthesis


def contract_errors(synthesis,envelope):
    expected=required(envelope)
    errors=[]
    if synthesis.observations != observations(envelope):errors.append('run_observation_mismatch')
    metrics,check,_=analyze(envelope)
    if synthesis.financial_metrics!=metrics or synthesis.financial_year_check!=check:errors.append('financial_metadata_mismatch')
    for topic in TOPICS:
        if expected[topic] not in synthesis.briefing:errors.append('missing_briefing_'+topic)
    for topic,section in [('activity','what_it_does'),('change','changes'),('unknown','limitations'),('financial','scale'),('takeaway','takeaway')]:
        if expected[topic] not in getattr(synthesis.sections,section):errors.append('missing_summary_'+topic)
    return errors
