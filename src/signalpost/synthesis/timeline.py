"""Dated synthesis view of existing supported claims. No I/O or source access."""
import re
from datetime import date,datetime,timezone
from ..models.synthesis import TimelineEntry

# Exact published fields/paths, scope and precision; no receipt timestamp dates.
DATED_FIELDS = {
 'identity.founding_date': ('value','Founding date recorded'),
 'identity.registration_date': ('value','Enhetsregisteret registration date recorded'),
 'identity.vat_registration_date': ('value','VAT registration date recorded'),
 'accounts.filed_years': ('value[]','Accounting year with a filed copy recorded'),
 'accounts.filed_year.*': ('value','Accounting year with a filed copy recorded'),
 'roles.role.*': ('from_date,last_changed','Role record start date / last changed date recorded'),
 'registry_change.roles.*': ('date','Registry role-update publication recorded'),
 'state_aid.award.*': ('date','State-aid award date recorded'),
 'procurement.award.*': ('date','Contract award date recorded'),
 'status_events.event.*': ('date','Registry event publication recorded'),
 'signature.* / prokura.*': ('none','No published change date; omitted'),
}


def precision(value):
 if not isinstance(value,str):return None
 if re.fullmatch(r'\d{4}',value):
  return ('year',value) if 1<=int(value)<=9999 else None
 if re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):
  try:date.fromisoformat(value);return 'day',value
  except ValueError:return None
 if re.fullmatch(r'\d{4}-\d{2}-\d{2}T.+',value):
  try:
   parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
   if parsed.tzinfo is not None:return 'timestamp',parsed.astimezone(timezone.utc).isoformat()
  except ValueError:pass
 return None


def build(claims,evidence):
 """Return a stable oldest-first dated section; never mutate claims/evidence."""
 def obj(x):return x.model_dump(mode='json') if hasattr(x,'model_dump') else x
 records={obj(e)['id']:obj(e) for e in evidence};entries={}
 for original in claims:
  c=obj(original);field=c['field'];value=c.get('value');refs=c.get('evidence_ids') or []
  if c['availability']!='available' or not refs:continue
  complete=True
  for ref in refs:
   e=records.get(ref)
   if not e or not all(e.get(k) for k in ('source_url','retrieved_at','content_sha256','locator','claim_span','extraction_method')):
    complete=False;break
   if not re.fullmatch(r'[0-9a-f]{64}',e['content_sha256']) or not e['source_url'].startswith('https://') or not e['retrieved_at'].endswith('Z'):
    complete=False;break
  if not complete:continue
  candidates=[]
  if field in {'identity.founding_date','identity.registration_date','identity.vat_registration_date'}:
   candidates=[(value,DATED_FIELDS[field][1])]
  elif field=='accounts.filed_years' and isinstance(value,list):
   candidates=[(v,'Accounting year with a filed copy recorded') for v in value]
  elif field.startswith('accounts.filed_year.'):
   # The list and each individual year duplicate one fact. Prefer individual
   # claims if present; skip only the corresponding list year below.
   candidates=[(value,'Accounting year with a filed copy recorded')]
  elif isinstance(value,dict):
   if field.startswith('roles.role.'):
    candidates=[(value.get('from_date'),'Role record start date recorded'),(value.get('last_changed'),'Role record last changed date recorded')]
   elif field.startswith('registry_change.roles.'):
    candidates=[(value.get('date'),'Registry role-update publication recorded')]
   elif field.startswith('state_aid.award.'):
    candidates=[(value.get('date'),'State-aid award date recorded')]
   elif field.startswith('procurement.award.'):
    candidates=[(value.get('date'),'Contract award date recorded')]
   elif field.startswith('status_events.event.'):
    # Raw codes might contain arbitrary source text; use only documented,
    # safe codes in the name-free presentation, otherwise neutral wording.
    code=value.get('change_type')
    label={'Ny':'Entity added to Enhetsregisteret','Endring':'Entity changed in Enhetsregisteret',
           'Sletting':'Entity deleted from Enhetsregisteret','Fjernet':'Entity removed from Open Data',
           'Ukjent':'Registry change type unknown'}.get(code,'Registry change event recorded')
    candidates=[(value.get('date'),label+'; API publication time')]
  for raw,label in candidates:
   parsed=precision(raw)
   if not parsed:continue
   p,sortdate=parsed
   if isinstance(value,dict) and value.get('date_precision') and value['date_precision']!=p:continue
   key=(c['id'],raw,label)
   entries[key]=(sortdate,p,TimelineEntry(date=raw,precision=p,text=label,claim_ids=[c['id']],evidence_ids=list(refs),source_field=field))
 result=[item[2] for item in sorted(entries.values(),key=lambda x:(x[0],{'year':0,'day':1,'timestamp':2}[x[1]],x[2].source_field,x[2].claim_ids[0],x[2].text))]
 # File-year list is a summary of the individual claims, not another event.
 individual={(e.date,e.text) for e in result if e.source_field.startswith('accounts.filed_year.')}
 result=[e for e in result if e.source_field!='accounts.filed_years' or (e.date,e.text) not in individual]
 # Need two distinct source facts, not two date attributes of one claim.
 return result if len({e.claim_ids[0] for e in result})>=2 else []


def for_row(row):
 return [e.model_dump(mode='json') for e in build(row['claims'],row['evidence'])]


def verify(row):
 synthesis=(row.get('run') or {}).get('synthesis') or {}
 sections=synthesis.get('sections') or {}
 if 'timeline' in sections:assert sections['timeline']==for_row(row),'Unsupported dated timeline view'
