"""Resolve sampled facts via their own receipt and production source replays."""
import csv,hashlib,io,json,re
from urllib.parse import urlsplit
from signalpost.sources.http import Response
from signalpost.sources.extract import Source,Section
from signalpost.sources.text import decode_body


def primary(item):
 c=item['claim'];by={e['id']:e for e in item['evidence']};refs=[by[eid] for eid in c['evidence_ids']]
 f=c['field']
 if f=='public_brand' or f.startswith('brand.'):
  chosen=[e for e in refs if e['extraction_method']=='signalpost.public_names.v1']
 elif f=='official_website':chosen=[e for e in refs if e['source_class']=='company_owned' and e['source_url']==c['value']['proof_page_url'] and e['locator'].startswith('identity-proof:')]
 elif f.startswith('social_profile.'):chosen=[e for e in refs if e['source_class']=='company_owned' and (e['locator'].startswith('company-link:') or 'social' in e['extraction_method'])]
 elif f.startswith('website_description.'):chosen=[e for e in refs if e['extraction_method']=='signalpost.website_description.v1']
 elif f.startswith('contact.'):chosen=[e for e in refs if e['source_class']=='company_owned' and e['locator'].startswith('contact:')]
 else:chosen=refs
 assert chosen,'Missing claim-specific primary receipt'
 return chosen


def verify(item,bodies,packet):
 from signalpost.sources import brreg_corporate,brreg_roller,brreg_underenheter,bulk_registry,brreg_enhet,regnskap
 from scripts import verify_output as vo
 c=item['claim'];org=item['org'];evidence={e['id']:e for e in item['evidence']}
 claims={x['id']:x for x in item['context']};claims[c['id']]=c
 data={'claims':list(claims.values())};row={'organisation_number':org,'run':{'synthesis':{'contract_version':'r5-S'}}}
 def stored(h):return decode_body(bodies[h])
 def response(e):return Response(bodies[e['content_sha256']],200,e['source_url'],e['retrieved_at'],e['content_sha256'])
 def matches(section):return any(x.field==c['field'] and x.value==c['value'] and x.reporting_period==c.get('reporting_period') for x in section.claims)
 own=primary(item)
 # All references still have their hashes/spans checked by replay.py; only
 # claim-specific receipts supply values. Registry receipts are dependencies.
 for e in own:
  ledger=any(r['url']==e['source_url'] and r['content_sha256']==e['content_sha256'] and r['status']==200 for r in packet['request_receipts'])
  bulk=e['source_url']=='https://data.brreg.no/enhetsregisteret/api/enheter/lastned/csv' and e['locator'].startswith('row:'+org+'/') and packet['bulk_input_sha256'] in (e.get('source_identifier') or '')
  bundle=e['extraction_method']=='signalpost.exact_official.v1' and c['family'] in {'state_aid','research','inspections'}
  assert ledger or bulk or bundle,'Primary URL/hash pair not in original retrieval ledger or authenticated bundle'
  assert hashlib.sha256(bodies[e['content_sha256']]).hexdigest()==e['content_sha256'],'Own response hash differs'
  assert e['claim_span'] in stored(e['content_sha256']),'Own span is not verbatim'
 if c['family'] in brreg_corporate.FAMILIES:
  assert brreg_corporate.verify(org,{'claims':[c]},evidence,stored)==1;return own,'production corporate source replay'
 if c['field'].startswith('accounts.filed_year'):
  assert vo.verify_filing_years(row,{'claims':[c]},evidence,stored)==1;return own,'production filing-years replay'
 if c['family']=='accounts':
  assert vo.verify_financial_sources(row,{'claims':[c]},evidence,stored)[0]==1;return own,'production financial source replay'
 if c['family']=='gleif':
  assert vo.verify_exact_public(row,{'claims':[c]},evidence,stored)==1;return own,'production exact-ID replay'
 if c['family'] in {'state_aid','research','inspections','licences'}:
  # Restore only the real, attached subunit scope receipts needed by the
  # existing inspector validator. Never search the identity CSV for the value.
  for e in item['evidence']:
   if '/api/underenheter?' in e['source_url']:
    section=Section();brreg_underenheter.extract_page(org,response(e),section,0)
    for x in section.claims:claims[x.id]=x.model_dump(mode='json')
  data['claims']=list(claims.values())
  assert vo.verify_exact_official(row,data,evidence,stored)==1;return own,'production exact official replay'
 if c['field']=='public_brand' or c['field'].startswith('brand.'):
  from signalpost.public_names import verify as names_verify
  assert c['id'] in names_verify(org,data,evidence,stored);return own,'production public-name replay'
 if c['family']=='website':
  from signalpost.web.html import Page
  from signalpost.web.policy import domain
  from signalpost.web.social import discover_strict,profile_url
  from signalpost.web.proof import score
  from scripts.verify_publisher_identity import registry_context,verify as publisher_verify
  site=next(x for x in data['claims'] if x['field']=='official_website')
  publisher_verify(org,{'claims':[x for x in data['claims'] if x['id']!=c['id'] or c['field']=='official_website']},evidence,stored)
  context,_=registry_context(org,data,evidence,stored);site_value=site['value']
  proof_refs=[evidence[eid] for eid in site['evidence_ids'] if evidence[eid]['source_class']=='company_owned' and evidence[eid]['source_url']==site_value['proof_page_url'] and evidence[eid]['locator'].startswith('identity-proof:')]
  if site_value['identity_level']=='VERIFIED':
   assert any(score(Page(bodies[e['content_sha256']],e['source_url']),org,context,site_value.get('candidate_origin'),[]).level=='VERIFIED' for e in proof_refs),'Exact website publisher proof failed'
  else:assert publisher_verify(org,data,evidence,stored)>0,'Registry-declared/corroborated publisher proof missing'
  assert domain(site_value['final_url'])==domain(site_value['proof_page_url'])
  if c['field']=='official_website':return own,'own page exact publisher proof / production registry corroboration'
  for e in own:
   assert domain(e['source_url'])==domain(site_value['final_url']),'Foreign claim page'
   page=Page(bodies[e['content_sha256']],e['source_url'])
   if c['field'].startswith('social_profile.'):
    from signalpost.web.owner_social import page_profiles,visible_profiles
    found=page_profiles(page,site_value,org,context,visible_profiles([page]),site_value.get('relationship_note')=='group_site')
    assert c['value']['url'] in found,'Social link is not supported by own-page extractor'
    assert found[c['value']['url']]['tier']==c['value']['proof_tier'],'Social proof tier differs'
    assert c['value']['url'] in e['claim_span'],'Social URL absent from own link span'
   elif c['field'].startswith('website_description.'):
    assert c['value']['identity_claim_id']==site['id']
    text=c['value']['text'];assert text in stored(e['content_sha256']) and text in e['claim_span'],'Description missing from own page/span'
   elif c['field'].startswith('contact.'):
    value=c['value'];assert isinstance(value,str)
    # Production contact output normalizes phone punctuation; compare the
    # actual own-page contact receipt, retaining verbatim span separately.
    from signalpost.web.proof import phone
    supported=value in e['claim_span'] or any(link.span==e['claim_span'] and link.href.startswith('tel:') and phone(link.href[4:])==value for link in page.links)
    assert supported,'Contact absent from own span / production phone normalization'
   else:raise NotImplementedError('Unsupported website projection')
  return own,'own-page extractor and exact publisher identity'
 if c['family']=='activity':
  vo.verify_registry_events(row,{'claims':[c]},evidence,stored);return own,'production exact registry event replay'
 for e in own:
  r=response(e)
  if c['family']=='identity':
   if e['locator'].startswith('row:'):
    from signalpost.sources.bulk_registry import column
    record=next(x for x in csv.DictReader(io.StringIO(stored(e['content_sha256']))) if column(x,'organisasjonsnummer')[0]==org)
    section=bulk_registry.extract(org,record,Source(e['source_url'],r.body,r.sha,r.retrieved_at))
   else:section=brreg_enhet.extract(org,json.loads(r.body),Source(e['source_url'],r.body,r.sha,r.retrieved_at))
  elif c['family']=='roles':section=brreg_roller.extract(org,r)
  elif c['family']=='subunits':section=Section();brreg_underenheter.extract_page(org,r,section,0)
  else:raise NotImplementedError('No independent replay for family '+c['family'])
  if matches(section):return own,'exact company registry extractor replay'
 raise AssertionError('Claim value differs from its own saved source')
