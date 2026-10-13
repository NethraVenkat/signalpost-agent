import json
from datetime import datetime,date
from decimal import Decimal
from ..models.synthesis import Synthesis,Generator,Sentence,Unknown
from .catalog import input_hash,change_claims,leaves
from .validate import validate_synthesis,permitted


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
        return ' '.join(x for x in [period.get('currency'),text(value)] if x)+' (fiscal year '+str(period.get('fiscal_year'))+')' if period.get('fiscal_year') else text(value)
    if field.startswith('subunits.unit.'):
        address=value.get('address') or {}
        return ', '.join(text(x) for x in [value.get('name'),address.get('kommune') or address.get('poststed')] if x)
    if field.startswith('hiring.job.'):return value['title']
    if field.endswith('.old') or field.endswith('.new'):
        if field.startswith('roles.') and isinstance(value,list):return '; '.join(text(x.get('name')) for x in value if isinstance(x,dict) and x.get('name'))
        return text(value)
    return text(value)


def generate(envelope):
    result=Synthesis(generator=Generator(input_sha256=input_hash(envelope)),change_claims=change_claims(envelope))
    claims=sorted((c for c in envelope.claims if c.availability=='available' and permitted(c,envelope)),key=lambda c:c.field)
    by_field={c.field:c for c in claims}
    def add(section,label,claim,quote=False):
        value=projected(claim)
        if not value or value=='None':return
        # Verbatim description substring, not a paraphrase or a new claim.
        if quote:
            value='«'+(next((x for x in leaves(claim.value) if x),value) if isinstance(claim.value,list) else value)[:300]+'»'
        prefix='Previously supported. ' if claim.carried_forward else ''
        getattr(result.sections,section).append(Sentence(text=prefix+label+': '+value+'.',claim_ids=[claim.id]))
    for field,label in [('identity.registered_activity','Registered activity'),('identity.statutory_purpose','Registered purpose')]:
        if field in by_field:add('what_it_does',label,by_field[field],True)
    descriptions=set()
    for claim in claims:
        if claim.field.startswith('identity.nace'):add('what_it_does','NACE',claim)
        if claim.field.startswith('website_description.'):
            description=projected(claim)
            if description not in descriptions and len(descriptions)<2:
                add('what_it_does','Website self-description',claim,True)
                descriptions.add(description)
    for field,label in [('identity.employees','Employees as registered'),('accounts.revenue','Reported revenue'),
                        ('accounts.net_result','Annual result'),('identity.municipality','Registered municipality')]:
        if field in by_field:add('scale',label,by_field[field])
    examples={'subunits':0,'social':0,'ads':0}
    for claim in claims:
        if claim.field.startswith('subunits.unit.') and examples['subunits']<3:
            add('scale','Registered workplace',claim);examples['subunits']+=1
        if claim.field=='official_website':add('scale','Official website',claim)
        if claim.field.startswith('social_profile.') and examples['social']<2:
            add('scale','Social profile',claim);examples['social']+=1
        if claim.field.startswith('hiring.job.') and examples['ads']<3:
            add('scale','Verified active ad',claim);examples['ads']+=1
        if claim.field.startswith('roles.role.') and claim.value.get('inactive') is not True:
            role=(claim.value.get('role_type') or {}).get('kode')
            label={'DAGL':'CEO','LEDE':'Chair','REVI':'Auditor'}.get(role)
            if label and claim.value.get('name'):add('leadership',label,claim)
    def count(section,label,records,kind):
        records={c.id:c for c in records}
        if records:getattr(result.sections,section).append(Sentence(text=label+': '+str(len(records))+'.',claim_ids=sorted(records),value_kind='derived',count=len(records),record_type=kind))
    if envelope.run.sections.get('subunits')=='available':
        count('scale','Registered workplaces',[c for c in claims if c.field.startswith('subunits.unit.')],'workplaces')
    if envelope.run.sections.get('roles')=='available':
        count('leadership','Registered board members',[c for c in claims if c.family=='roles' and isinstance(c.value,dict) and
            (c.value.get('group_type') or {}).get('kode')=='STYR' and (c.value.get('role_type') or {}).get('kode') in {'LEDE','NEST','MEDL'} and c.value.get('inactive') is not True],'board_members')
    count('scale','Verified active ads found',[c for c in claims if c.family=='hiring' and c.field.startswith('hiring.job.') and not c.carried_forward],'active_ads')
    for event in envelope.changes:
        sides=[c for c in result.change_claims if c.field in {event.field+'.old',event.field+'.new'}]
        if sides:
            parts=[]
            for side in ('old','new'):
                claim=next((c for c in sides if c.field.endswith('.'+side)),None)
                if claim:parts.append(('Previous' if side=='old' else 'Current')+': '+projected(claim))
            result.sections.changes.append(Sentence(text='Change. '+'; '.join(parts)+'.',claim_ids=[c.id for c in sides]))
    try:asof=datetime.fromisoformat(envelope.started_at.replace('Z','+00:00')).date()
    except ValueError:asof=date.today()
    registered=by_field.get('identity.registration_date')
    if registered:
        try:recent=0<=(asof-date.fromisoformat(str(registered.value)[:10])).days<=731
        except ValueError:recent=False
        if recent:add('changes','Registration date',registered)
    for field,label in [('identity.bankrupt','Bankruptcy'),('identity.under_liquidation','Liquidation'),('identity.deleted','Deletion')]:
        claim=by_field.get(field)
        if claim and claim.value is True:add('changes',label,claim)
    if envelope.run.refresh.get('mode')=='baseline':
        if claims:
            result.sections.changes.append(Sentence(text='First observation; no earlier run to compare.',claim_ids=[claims[0].id]))
        else:
            result.sections.unknowns.append(Unknown(family='refresh',state='not_available',reason='First observation; no earlier run to compare.'))
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
        if not getattr(result.sections,key):
            result.sections.unknowns.append(Unknown(family=key,state='not_available',reason='No supported claims are available for this section.'))
    return validate_synthesis(result,envelope)
