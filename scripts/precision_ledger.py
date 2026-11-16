"""Offline, exhaustive publication ledger; verdicts never edit published outputs."""
from signalpost.portable_paths import expand, portable, portable_text  # saved paths stay repo-relative
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from functools import lru_cache

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.verify_output import verify_exact_public,verify_careers
from signalpost.web.html import Page
from signalpost.web.proof import score,orgnrs
from signalpost.web.candidates import legal_name
from signalpost.web.social import discover_strict,shared_group_context
from signalpost.web.policy import domain
from signalpost.sources.text import decode_body

KINDS=('website','social','job','LEI','parent','award')


def kind(claim):
    field=claim['field']
    if field=='official_website':return 'website'
    for prefix,name in [('social_profile.','social'),('hiring.job.','job'),('gleif.parent.','parent'),('procurement.award.','award')]:
        if field.startswith(prefix):return name
    if field=='gleif.record':return 'LEI'


def name_match(name,text):
    expected=re.sub(r'[^\w]','',legal_name(name).casefold())
    actual=re.sub(r'[^\w]','',text.casefold())
    return bool(expected and expected in actual)


def recheck(row,claim,body):
    """Wrong = broken saved proof; doubtful = extra conservative hand-check flag.

    A foreign parent/counterparty is not a foreign attribution: structured IDs
    must be in the correct role. Multi-entity websites still get a hand flag.
    """
    org=row['organisation_number'];typ=kind(claim);value=claim['value']
    evidence={e['id']:e for e in row['evidence']};receipts=[evidence[e] for e in claim['evidence_ids']]
    reasons=[];checks={};name=next(c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available')
    try:
        for e in receipts:
            raw=body(e['content_sha256'])
            assert hashlib.sha256(raw).hexdigest()==e['content_sha256'],'body hash mismatch'
            assert e['claim_span'] and e['claim_span'] in decode_body(raw),'non-verbatim/missing excerpt'
        checks['all_receipts_hash_and_excerpt']=True
        if typ in {'website','social'}:
            proof=claim if typ=='website' else next(c for c in row['claims'] if c['field']=='official_website' and c['availability']=='available')
            proof_receipts=[evidence[e] for e in proof['evidence_ids']]
            identity=next(e for e in proof_receipts if e['locator'].startswith('identity-proof:'))
            assert domain(identity['source_url'])==domain(proof['value']['final_url']),'published site URL differs from identity-proof domain'
            page=Page(body(identity['content_sha256']),identity['source_url'])
            checks['exact_company_number']=org in orgnrs(page.owner_text+' '+identity['claim_span'])
            if not checks['exact_company_number']:
                assert proof['value'].get('identity_level')!='VERIFIED','claimed exact-number proof lacks the target orgnr'
                reasons.append('No exact target orgnr in saved owner/proof context; published signal-only tier requires hand review')
            checks['identity_level_verified']=proof['value'].get('identity_level')=='VERIFIED'
            if not checks['identity_level_verified']:reasons.append('Published identity tier is below exact-number VERIFIED')
            rescored=score(page,org,{'name':name},proof['value'].get('candidate_origin','legal_name_slug'),[])
            checks['replayed_exact_number_score']=rescored.level=='VERIFIED'
            if not checks['replayed_exact_number_score']:reasons.append('Saved page proof needs review: '+rescored.reason)
            foreign=sorted(orgnrs(page.owner_text)-{org})
            checks['other_owner_orgnrs']=foreign
            if foreign:reasons.append('Other valid Norwegian identifiers in owner text: '+', '.join(foreign))
            group=shared_group_context(page) or proof['value'].get('relationship_note')=='group_site'
            checks['no_group_site']=not group
            if group:reasons.append('Group/multi-company site context needs hand review')
            checks['name_match']=name_match(name,page.title+' '+page.meta.get('og:site_name','')+' '+page.owner_text)
            if not checks['name_match']:reasons.append('Exact registry legal/brand spelling not located in saved page text')
            if typ=='social':
                receipt=next(e for e in receipts if e['locator'].startswith('company-link:'))
                assert domain(receipt['source_url'])==domain(proof['value']['final_url']),'social source outside verified site'
                social_page=Page(body(receipt['content_sha256']),receipt['source_url'])
                strict=discover_strict(social_page,name)
                assert strict.get(value['url'])==receipt['claim_span'],'own header/footer/name/numeric-link policy no longer verifies'
                checks['own_header_footer_and_no_founder_agency_context']=True
                if shared_group_context(social_page):reasons.append('Social link page has group context')
        elif typ=='job':
            verify_careers(row,row,evidence,lambda sha:decode_body(body(sha)))
            checks['current_at_retrieval_and_exact_employer_or_proven_subunit']=True
            if value.get('source')=='verified_site_careers':
                checks['own_link_and_allowed_posting_host']=True
            else:
                receipt=next(e for e in receipts if e['extraction_method']=='signalpost.nav.v1' and e['locator']=='/ad_content')
                ad=json.loads(body(receipt['content_sha256']))['ad_content']
                checks['name_match']=name_match(name,ad.get('employer',{}).get('name',''))
                if not checks['name_match']:reasons.append('NAV employer spelling differs; exact employer/subunit proof passes, hand-check spelling')
        elif typ in {'LEI','parent','award'}:
            verify_exact_public(row,row,evidence,lambda sha:decode_body(body(sha)))
            checks['structured_exact_id_country_and_role']=True
            if typ in {'LEI','parent'}:
                identity=claim if typ=='LEI' else next(c for c in row['claims'] if c['field']=='gleif.record' and c['availability']=='available')
                names=[]
                for eid in identity['evidence_ids']:
                    e=evidence[eid];document=json.loads(body(e['content_sha256']))
                    for item in document.get('data',[]):
                        if item.get('id')==identity['value']['lei']:names.append(item['attributes']['entity'].get('legalName',{}).get('name',''))
                names=sorted(set(names));checks['gleif_legal_names']=names
                checks['name_match']=any(name_match(name,n) for n in names)
                if not checks['name_match']:reasons.append('Exact-ID GLEIF legal name differs from registry spelling; saved GLEIF name: '+('; '.join(names) or 'not supplied')+'; review source recency')
                if typ=='parent':checks['active_relationship_correct_child_type']=True
            else:
                checks['selected_lot_contract_award_link_and_no_notice_total']=True
                if not any(name_match(name,body(e['content_sha256']).decode('utf8')) for e in receipts):
                    reasons.append('Exact role ID verified, but registry spelling not located in structured notice')
        else:raise AssertionError('unknown ledger type')
        if claim.get('carried_forward'):reasons.append('Historical carried-forward proof; no current re-verification')
    except (AssertionError,KeyError,ValueError,StopIteration,TypeError) as exc:
        return 'wrong',[str(exc) or type(exc).__name__],checks
    return ('doubtful' if reasons else 'correct'),reasons,checks


def build(root=ROOT,runs=None,dest=None):
    dest=Path(dest) if dest else root/'reports/r5/precision';dest.mkdir(parents=True,exist_ok=True)
    runs=runs or [(s,n,root/'reports/r5/stageT'/s) for s,n in [('frozen',20261017),('daily',20261113),('mock',20261114)]]
    review_path=root/'reports/r5/precision/human_reviews.json'
    human=json.loads(review_path.read_text(encoding='utf8')) if review_path.exists() else {'reviews':[],'pending':[]}
    records=[];inputs={};measurements={}
    for sample,seed,folder in runs:
        folder=Path(folder)
        settings=json.loads((folder/'settings.json').read_text(encoding='utf8'));work=Path(expand(settings['working_directory']))
        output=work/'envelopes.jsonl';rows=[json.loads(x) for x in output.read_text(encoding='utf8').splitlines()]
        assert len(rows)==100
        inputs[sample]={'seed':seed,'output':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'run_id':settings['resolved_config']['run_id'],'source_manifest_sha256':settings['source_manifest_sha256']}
        @lru_cache(maxsize=16)
        def body(sha):return (work/'state/blobs'/sha).read_bytes()
        for row in rows:
            evidence={e['id']:e for e in row['evidence']}
            name=next(c['value'] for c in row['claims'] if c['field']=='identity.legal_name' and c['availability']=='available')
            for claim in row['claims']:
                typ=kind(claim)
                if claim['availability']!='available' or not typ:continue
                verdict,reasons,checks=recheck(row,claim,body)
                receipts=[evidence[e] for e in claim['evidence_ids']]
                value=claim['value']
                tier=(value.get('identity_level') if typ=='website' else value.get('proof_tier') if typ=='social' else
                    'current_live_exact_employer_or_proven_subunit' if typ=='job' and value.get('source')!='verified_site_careers' else
                    'verified_site_own_link_current_posting' if typ=='job' else 'exact_NO_RA000472' if typ=='LEI' else
                    'exact_child_LEI_ACTIVE_relationship' if typ=='parent' else 'exact_NO_buyer_or_selected_winner_lot_contract')
                value_sha=hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
                review=next((r for r in human['reviews'] if r['sample']==sample and r['organisation_number']==row['organisation_number']
                    and r['field']==claim['field'] and r['value_sha256']==value_sha),None)
                records.append({'sample':sample,'seed':seed,'organisation_number':row['organisation_number'],'company':name,'kind':typ,
                    'field':claim['field'],'claim_id':claim['id'],'value':value,'proof_tier':tier,'verdict':verdict,'reasons':reasons,
                    'checks':checks,'evidence':receipts,'human_review':review})
        metrics=json.loads((folder/'counts.json').read_text(encoding='utf8'))['metrics']
        metrics.update(lei_companies=sum(any(c['field']=='gleif.record' and c['availability']=='available' for c in r['claims']) for r in rows),
            parent_companies=sum(any(c['field'].startswith('gleif.parent.') and c['availability']=='available' for c in r['claims']) for r in rows),
            award_companies=sum(any(c['family']=='procurement' and c['availability']=='available' for c in r['claims']) for r in rows),
            award_claims=sum(c['family']=='procurement' and c['availability']=='available' for r in rows for c in r['claims']),
            ratios=sum(m['formula']!='revenue_yoy' for r in rows for m in (r['run'].get('synthesis') or {}).get('financial_metrics',[])),
            yoy=sum(m['formula']=='revenue_yoy' for r in rows for m in (r['run'].get('synthesis') or {}).get('financial_metrics',[])))
        measurements[sample]=metrics
    counts={kind:{v:sum(r['kind']==kind and r['verdict']==v for r in records) for v in ('correct','doubtful','wrong')} for kind in KINDS}
    report={'method':'Offline recheck of saved bytes and original proof/link/role constraints; no live re-fetch and no output edits',
        'unit':'published claim per sample, not deduplicated entities or a random hand-labelled accuracy sample',
        'inputs':inputs,'counts':counts,'measurements':measurements,'items':records,'human_reviews':human,
        'limits':['Automated verdicts are rule checks, not independent human precision ground truth.',
            'correct means clear under saved evidence rules at retrieval, not guaranteed current internet truth.',
            'Name/cross-entity/group/historical concerns are doubtful even if publication identity checks passed.',
            'Foreign counterparties/parents are legitimate; exact country/ID must match the target role, not every party in a batch.']}
    (dest/'ledger.json').write_text(portable_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n'),encoding='utf8')
    text='# Precision ledger - measured samples\n\n'+report['method']+'. No item is silently removed. Correct/doubtful/wrong are automated saved-evidence verdicts, not human-labelled accuracy. The separate human-review column records explicit user verdicts for the exact sample/value, without upgrading original proof tiers. Remaining unreviewed doubtful/wrong items need hand review.\n\n'
    text+='| Type | Checked | Correct | Doubtful | Wrong |\n|---|---:|---:|---:|---:|\n'
    for typ,c in counts.items():text+=f"| {typ} | {sum(c.values())} | {c['correct']} | {c['doubtful']} | {c['wrong']} |\n"
    text+='\nMethod and limits:\n\n'+''.join('- '+x+'\n' for x in report['limits'])
    text+='\nChecks: SHA-256 and verbatim excerpts; website exact number, replayed proof, registry spelling, other owner numbers and group context; social strict own header/footer link, handle/numeric LinkedIn rule and founder/agency exclusion; jobs current at retrieval with exact employer/proven subunit or own careers link; GLEIF exact Norwegian registry identity and ACTIVE parent relationship; TED exact Norwegian buyer/selected tenderer and structured lot/contract award link.\n\n'
    for i,item in enumerate(records,1):
        text+=f"## {i}. {item['kind']} - {item['organisation_number']} - {item['company']} (seed {item['seed']})\n\n"
        display=json.dumps(item['value'],ensure_ascii=False,sort_keys=True)
        text+='| Value / URL | Proof tier | Automated verdict | Human review | Review reason |\n|---|---|---|---|---|\n'
        review=item['human_review']
        human_text=(review['verdict']+' - '+review['reviewer']+' ('+review['review_date']+')') if review else 'Pending explicit verdict' if item['organisation_number']=='995194163' else 'Not reviewed'
        text+='| '+display.replace('|','&#124;').replace('\n',' ')+' | '+str(item['proof_tier'])+' | **'+item['verdict']+'** | '+human_text+' | '+('; '.join(item['reasons']) or 'All saved-evidence checks passed').replace('|','&#124;')+' |\n\n'
        for e in item['evidence']:
            text+=f"Source: {e['source_url']}\n\nRetrieved: {e['retrieved_at']}; SHA-256: `{e['content_sha256']}`; locator: `{e['locator']}`.\n\nExact excerpt:\n\n```text\n{e['claim_span']}\n```\n\n"
    (dest/'LEDGER.md').write_text(portable_text(text),encoding='utf8',newline='')
    return report


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs',type=Path,help='JSON list of sample/seed/folder entries')
    parser.add_argument('--destination',type=Path)
    args=parser.parse_args()
    runs=[(r['sample'],r['seed'],Path(expand(r['folder']))) for r in json.loads(args.runs.read_text(encoding='utf8'))] if args.runs else None
    report=build(runs=runs,dest=args.destination);print(json.dumps({'counts':report['counts'],'measurements':report['measurements']}))
