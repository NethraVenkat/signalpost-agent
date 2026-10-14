"""Reference-runner raw profiles projected only from verified envelope claims."""
import json
import os
from pathlib import Path

MODULES = {'registry_live':'identity', 'financials':'accounts', 'roles':'roles',
           'locations':'subunits', 'website':'website', 'hiring':'hiring', 'activity':'activity'}
STATUS = {'available':'available', 'not_available':'not_found', 'not_applicable':'not_applicable',
          'failed':'source_error', 'ambiguous':'source_error', 'blocked':'blocked'}
IDENTITY = {'organisation_number':None, 'name':'legal_name', 'legal_form':'organisation_form',
            'employees':'employees','bankrupt':'bankrupt','liquidating':'under_liquidation',
            'website':'registered_website','industry':'nace1','business_address':'registered_address',
            'postal_address':'postal_address','latest_submitted_accounts':'latest_submitted_accounts'}
FINANCIAL = {'revenue':'revenue','operating_result':'operating_result','profit_before_tax':'result_before_tax',
             'annual_result':'net_result','assets':'total_assets','equity':'equity','debt':'total_liabilities'}


def project(envelope):
    claims = [c for c in envelope.claims if c.availability == 'available']
    fields = {c.field:c for c in claims}
    def value(field): return fields[field].value if field in fields else None
    registry = {key:value('identity.'+field) if field else None for key,field in IDENTITY.items()}
    if 'identity.legal_name' in fields:
        registry['organisation_number'] = envelope.organisation_number
    form=registry['legal_form']
    if isinstance(form,dict): registry['legal_form']=form.get('kode')
    roles=[]
    for c in claims:
        if not c.field.startswith('roles.role.') or not isinstance(c.value,dict):continue
        v=c.value;role=v.get('role_type') or {};group=v.get('group_type') or {}
        roles.append({'name':v.get('name'),'organisation_number':v.get('entity_organisation_number'),
                      'role_code':role.get('kode'),'role':role.get('beskrivelse'),
                      'group_code':group.get('kode'),'group':group.get('beskrivelse'),
                      'last_changed':v.get('last_changed'),'inactive':v.get('inactive')})
    locations=[]
    for c in claims:
        if not c.field.startswith('subunits.unit.') or not isinstance(c.value,dict):continue
        v=c.value;raw=v.get('raw') or v
        locations.append({'organisation_number':v.get('organisation_number'),'name':v.get('name'),
                          'address':raw.get('beliggenhetsadresse') or raw.get('postadresse') or v.get('address'),
                          'industry':raw.get('naeringskode1') or v.get('nace') or v.get('industry'),
                          'employees':raw.get('antallAnsatte') if 'antallAnsatte' in raw else v.get('employees')})
    account_claims=[c for c in claims if c.family=='accounts']
    financials=[]
    if account_claims:
        period=account_claims[0].reporting_period or {}
        financials=[{'record_id':None,'account_type':period.get('account_type'),
                     'period':{'fraDato':period.get('period_start'),'tilDato':period.get('period_end')},
                     'currency':period.get('currency'),**{key:value('accounts.'+field) for key,field in FINANCIAL.items()}}]
    website=value('official_website')
    values={'registry_live':registry if registry['organisation_number'] else None,
            'financials':{'records':financials} if financials else None,
            'roles':{'roles':roles} if roles else None,'locations':{'locations':locations} if locations else None,
            'website':website,'hiring':{'jobs':[c.value for c in claims if c.family=='hiring']} or None,
            'activity':{'items':[c.value for c in claims if c.family=='activity']} or None}
    records={e.id:e for e in envelope.evidence};evidence={}
    for module,family in MODULES.items():
        selected=[c for c in claims if c.family==family]
        ids=list(dict.fromkeys(eid for c in selected for eid in c.evidence_ids))
        primary=records[ids[0]] if ids else None
        state=envelope.run.sections.get(family,'not_applicable')
        # No collection zero or empty list is invented when work did not complete.
        payload=values[module] if selected else None
        if not selected and state=='not_available' and module in {'roles','locations','hiring','activity'}:
            payload={ {'roles':'roles','locations':'locations','hiring':'jobs','activity':'items'}[module]:[] }
        evidence[module]={'field':module,'status':STATUS[state],
                          'source_type':primary.source_class if primary else family,
                          'source_class':primary.source_class if primary else family,
                          'source_url':primary.source_url if primary else '',
                          'retrieved_at':primary.retrieved_at if primary else envelope.completed_at,
                          'value':payload,'as_of':None,
                          'note':'Projected from verified claims; section coverage: '+state,
                          'content_sha256':primary.content_sha256 if primary else None,
                          'source_row_key':envelope.organisation_number if primary else None,
                          'effective_at':primary.effective_at if primary else None}
    # Lossless value/provenance index; module views never add facts absent here.
    verified=[{'id':c.id,'field':c.field,'value':c.value,'evidence_ids':c.evidence_ids} for c in claims]
    ids={eid for c in claims for eid in c.evidence_ids}
    provenance={eid:records[eid].model_dump(mode='json') for eid in sorted(ids)}
    return {'organisation_number':envelope.organisation_number,'name':value('identity.legal_name'),
            'municipality':value('identity.municipality'),'website':website.get('final_url') if isinstance(website,dict) else None,
            'evidence':evidence,'verified_claims':verified,'source_records':provenance}


def write(path, envelopes):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.tmp')
    with temporary.open('w',encoding='utf8',newline='\n') as handle:
        for envelope in envelopes:
            handle.write(json.dumps(project(envelope),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
        handle.flush();os.fsync(handle.fileno())
    os.replace(temporary,path)
    return {'state':'available','rows':len(envelopes),'bytes':path.stat().st_size}
