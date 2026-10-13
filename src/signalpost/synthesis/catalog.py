import json
from ..models.evidence import digest
from ..models.synthesis import ChangeClaim


def leaves(value):
    if isinstance(value,dict):
        for item in value.values():yield from leaves(item)
    elif isinstance(value,list):
        for item in value:yield from leaves(item)
    elif value is not None:yield str(value)


def change_claims(envelope):
    result=[]
    for event in envelope.changes:
        for side in ('old','new'):
            value=getattr(event,side+'_value');evidence=getattr(event,side+'_evidence_ids')
            if value is not None and evidence:
                result.append(ChangeClaim(id=digest(['change',event.field,side,value,sorted(evidence)]),
                    field=event.field+'.'+side,value=value,evidence_ids=evidence))
    return sorted(result,key=lambda claim:claim.id)


def catalog(envelope):
    result={c.id:c for c in envelope.claims if c.availability=='available'}
    result.update({c.id:c for c in change_claims(envelope)})
    return result


def input_hash(envelope):
    # Retrieval/run timestamps and observation metadata are deliberately excluded.
    claims=[{'id':c.id,'field':c.field,'value':c.value,'availability':c.availability,
             'reporting_period':c.reporting_period,'carried_forward':c.carried_forward} for c in envelope.claims]
    events=[{'field':e.field,'type':e.type,'old_value':e.old_value,'new_value':e.new_value,
             'old_evidence_ids':sorted(e.old_evidence_ids),'new_evidence_ids':sorted(e.new_evidence_ids)} for e in envelope.changes]
    return digest({'claims':sorted(claims,key=lambda c:c['id']),'changes':events,
        'sections':envelope.run.sections,'baseline':envelope.run.refresh.get('mode')=='baseline',
        'errors':sorted({(e.section,e.code) for e in envelope.errors if e.section in envelope.run.sections and e.code!='website_candidates'})})
