from decimal import Decimal
from ..models.synthesis import Synthesis,Generator,Sentence,Unknown
from .catalog import input_hash,change_claims,leaves
from .validate import validate_synthesis,permitted
from .readability import money,headline,nace_sentence,dual_role,normalised_description,unknown_text,workplaces_sentence
from .nace import unspecified


def text(value):
    if isinstance(value,str):return value
    if isinstance(value,(int,float)) and not isinstance(value,bool):return format(Decimal(str(value)),'f').rstrip('0').rstrip('.') if '.' in format(Decimal(str(value)),'f') else str(value)
    if isinstance(value,list):return '; '.join(text(x) for x in value if x is not None)
    if isinstance(value,dict):return '; '.join(leaves(value))
    return str(value)


def projected(claim):
    value=claim.value;field=claim.field
    if field.startswith('identity.nace'):return value.get('kode','')+': '+value.get('beskrivelse','')
    if field.startswith('website_description.'):return value['text']
    if field=='official_website':return value['final_url']
    if field.startswith('social_profile.'):return value['url']
    if field.startswith('roles.role.'):return text(value.get('name'))
    if field.startswith('accounts.') and getattr(claim,'reporting_period',None):
        period=claim.reporting_period
        amount=money(value) if period.get('currency') else text(value)
        return ' '.join(x for x in [period.get('currency'),amount] if x)+' (fiscal year '+str(period.get('fiscal_year'))+')' if period.get('fiscal_year') else amount
    if field.startswith('accounts.') and isinstance(value,(int,float)) and not isinstance(value,bool):return money(value)
    if field.startswith('subunits.unit.'):
        address=value.get('address') or {}
        return ', '.join(text(x) for x in [value.get('name'),address.get('kommune') or address.get('poststed')] if x)
    if field.startswith('hiring.job.'):return value['title']
    if field.endswith('.old') or field.endswith('.new'):
        if field.startswith('roles.') and isinstance(value,list):return '; '.join(text(x.get('name')) for x in value if isinstance(x,dict) and x.get('name'))
        return text(value)
    return text(value)


def generate(envelope):
    result=Synthesis(generator=Generator(version='3',input_sha256=input_hash(envelope)),change_claims=change_claims(envelope))
    claims=sorted((c for c in envelope.claims if c.availability=='available' and permitted(c,envelope)),key=lambda c:c.field)
    by_field={c.field:c for c in claims}
    opening=headline(claims)
    opening_ids=set(opening[1]) if opening else set()
    if opening:result.sections.what_it_does.append(Sentence(text=opening[0],claim_ids=opening[1]))
    def add(section,label,claim,quote=False):
        value=projected(claim)
        if not value or value=='None':return
        # Verbatim description substring, not a paraphrase or a new claim.
        if quote:
            value='«'+(next((x for x in leaves(claim.value) if x),value) if isinstance(claim.value,list) else value)[:300]+'»'
        prefix='Previously supported. ' if claim.carried_forward else ''
        getattr(result.sections,section).append(Sentence(text=prefix+label+': '+value+'.',claim_ids=[claim.id]))
    activity=by_field.get('identity.registered_activity');purpose=by_field.get('identity.statutory_purpose')
    if activity and purpose and normalised_description(activity.value)==normalised_description(purpose.value):
        prefix='Previously supported. ' if activity.carried_forward or purpose.carried_forward else ''
        result.sections.what_it_does.append(Sentence(text=prefix+'Registered activity and purpose: «'+normalised_description(activity.value)[:300]+'».',claim_ids=[activity.id,purpose.id]))
    else:
        for field,label in [('identity.registered_activity','Registered activity'),('identity.statutory_purpose','Registered purpose')]:
            if field in by_field:add('what_it_does',label,by_field[field],True)
    descriptions=set()
    for claim in claims:
        if claim.field.startswith('identity.nace'):
            if unspecified(claim.value):
                if not any(u.field=='industry' for u in result.sections.unknowns):
                    result.sections.unknowns.append(Unknown(family='identity',field='industry',state='not_available',reason='Industry code not specified.'))
            else:result.sections.what_it_does.append(Sentence(text=nace_sentence(claim),claim_ids=[claim.id]))
        if claim.field.startswith('website_description.'):
            description=projected(claim)
            if description not in descriptions and len(descriptions)<2:
                add('what_it_does','Website self-description',claim,True)
                descriptions.add(description)
    for field,label in [('identity.employees','Employees as registered'),('accounts.revenue','Reported revenue'),
                        ('accounts.net_result','Annual result'),('identity.municipality','Registered municipality')]:
        if field in by_field and by_field[field].id not in opening_ids:add('scale',label,by_field[field])
    active_roles=[c for c in claims if c.field.startswith('roles.role.') and c.value.get('inactive') is not True and c.value.get('name')]
    combined=dual_role(active_roles)
    combined_ids=set(combined[1]) if combined else set()
    if combined:result.sections.leadership.append(Sentence(text=combined[0],claim_ids=combined[1]))
    examples={'subunits':0,'social':0,'ads':0}
    for claim in claims:
        if claim.field=='official_website':add('scale','Official website',claim)
        if claim.field.startswith('social_profile.') and examples['social']<2:
            add('scale','Social profile',claim);examples['social']+=1
        if claim.field.startswith('hiring.job.') and examples['ads']<3:
            add('scale','Verified active ad',claim);examples['ads']+=1
        if claim.field.startswith('roles.role.') and claim.value.get('inactive') is not True:
            role=(claim.value.get('role_type') or {}).get('kode')
            label={'DAGL':'CEO','LEDE':'Chair','REVI':'Auditor'}.get(role)
            if label and claim.value.get('name') and claim.id not in combined_ids:add('leadership',label,claim)
    def count(section,label,records,kind):
        records={c.id:c for c in records}
        if records:getattr(result.sections,section).append(Sentence(text=label+': '+str(len(records))+'.',claim_ids=sorted(records),value_kind='derived',count=len(records),record_type=kind))
    units=[c for c in claims if c.field.startswith('subunits.unit.')]
    if len(units)==1:
        same_name=normalised_description(units[0].value.get('name'))==normalised_description(getattr(by_field.get('identity.legal_name'),'value',None))
        address=units[0].value.get('address') or {}
        same_city=str(address.get('kommune') or address.get('poststed') or '').casefold()==str(getattr(by_field.get('identity.municipality'),'value',None)).casefold()
        if not (same_name and same_city):add('scale','Registered workplace',units[0])
    elif len(units)>1:
        result.sections.scale.append(Sentence(text=workplaces_sentence(units),claim_ids=sorted(c.id for c in units),value_kind='derived',count=len(units),record_type='workplaces'))
    if envelope.run.sections.get('roles')=='available':
        board=[c for c in claims if c.family=='roles' and isinstance(c.value,dict) and
            (c.value.get('group_type') or {}).get('kode')=='STYR' and (c.value.get('role_type') or {}).get('kode') in {'LEDE','NEST','MEDL'} and c.value.get('inactive') is not True]
        if len({c.id for c in board})>1:count('leadership','Registered board members',board,'board_members')
    ads=[c for c in claims if c.family=='hiring' and c.field.startswith('hiring.job.') and not c.carried_forward]
    listed={cid for s in result.sections.scale if s.text.startswith('Verified active ad: ') for cid in s.claim_ids}
    if any(c.id not in listed for c in ads):count('scale','Verified active ads found',ads,'active_ads')
    for event in envelope.changes:
        sides=[c for c in result.change_claims if c.field in {event.field+'.old',event.field+'.new'}]
        if sides:
            parts=[]
            for side in ('old','new'):
                claim=next((c for c in sides if c.field.endswith('.'+side)),None)
                if claim:parts.append(('Previous' if side=='old' else 'Current')+': '+projected(claim))
            result.sections.changes.append(Sentence(text='Change: '+'; '.join(parts)+'.',claim_ids=[c.id for c in sides]))
    for field,label in [('identity.bankrupt','Bankruptcy'),('identity.under_liquidation','Liquidation'),('identity.deleted','Deletion')]:
        claim=by_field.get(field)
        if claim and claim.value is True:add('scale',label,claim)
    if envelope.run.refresh.get('mode')=='baseline':
        if claims:
            result.sections.changes.append(Sentence(text='First observation; no earlier run to compare.',claim_ids=[claims[0].id]))
        else:
            result.sections.unknowns.append(Unknown(family='refresh',state='not_available',reason='First observation; no earlier run to compare.'))
    elif not envelope.changes and claims:
        result.sections.changes.append(Sentence(text='No changes since the previous run.',claim_ids=[claims[0].id]))
    elif not envelope.changes:
        result.sections.unknowns.append(Unknown(family='refresh',state='not_available',reason='No changes since the previous run.'))
    for family,state in sorted(envelope.run.sections.items()):
        if state!='available':
            codes=sorted({e.code for e in envelope.errors if e.section==family and e.code!='website_candidates'})
            reasons={'not_available':'No supported values were found in the checked source scope.',
                     'blocked':'Source access was refused.','ambiguous':'Company identity or source coverage is ambiguous.',
                     'failed':'Source checking was incomplete.','not_applicable':'The source explicitly marks this question inapplicable.'}
            reason=reasons[state]+(' Recorded reason: '+', '.join(codes)+'.' if codes else '')
            result.sections.unknowns.append(Unknown(family=family,state=state,reason=reason))
    if 'identity.employees' not in by_field:
        result.sections.unknowns.append(Unknown(family='identity',field='employees',state='not_available',reason='Employee count is not reported.'))
    periods={c.reporting_period.get('fiscal_year') for c in claims if c.family=='accounts' and c.reporting_period}
    if len(periods)==1:
        result.sections.unknowns.append(Unknown(family='accounts',field='financial_direction',state='not_available',reason="Only the latest year's accounts are available."))
    for key in ('what_it_does','scale','leadership'):
        if key=='scale' and any(c.id in opening_ids and c.field in {'identity.municipality','identity.employees','accounts.revenue'} for c in claims):continue
        if not getattr(result.sections,key):
            result.sections.unknowns.append(Unknown(family=key,state='not_available',reason='No supported claims are available for this section.'))
    for unknown in result.sections.unknowns:unknown.text=unknown_text(unknown,envelope)
    return validate_synthesis(result,envelope)
