"""Aggregate measured items without silently dropping doubtful identities."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from measure import SEEDS,ORDER,folder,manifest,save
from signalpost.sources.text import decode_body
from signalpost.web.html import Page
from signalpost.web.policy import domain
from signalpost.web.social import discover_strict
from scripts.accuracy_audit import audit_website_claim,extract_org_context_and_leaders


def review(item,row,work):
    evidence={e['id']:e for e in row['evidence']};context,leaders=extract_org_context_and_leaders(row['claims'])
    site=next((c for c in row['claims'] if c['field']=='official_website' and c['availability']=='available'),None)
    proofs=[]
    for e in item['evidence']:
        path=work/'state/blobs'/e['content_sha256'];body=path.read_bytes()
        assert hashlib.sha256(body).hexdigest()==e['content_sha256'] and e['claim_span'] in decode_body(body)
        if item['kind']=='website' and e['source_class']=='company_owned' and e['source_url']==item['value']['proof_page_url']:
            units={row['organisation_number']:{c['value']['organisation_number'] for c in row['claims'] if c['field'].startswith('subunits.unit.') and c['availability']=='available'}}
            claim=next(c for c in row['claims'] if c['field']==item['field'] and c['value']==item['value'])
            verdict,reason,_=audit_website_claim(row['organisation_number'],claim,e,decode_body(body),context=context,leaders=leaders,subunit_map=units)
            proofs.append({'verdict':verdict,'reason':reason})
        elif item['kind']=='social' and e['locator']=='company-link:'+item['identity'] and site:
            page=Page(body,e['source_url'])
            links=discover_strict(page,context['name'])
            correct=item['identity'] in links and links[item['identity']]==e['claim_span'] and domain(e['source_url'])==domain(site['value']['final_url']) and not site['value'].get('other_orgnrs') and site['value'].get('relationship_note')!='group_site'
            proofs.append({'verdict':'CORRECT' if correct else 'DOUBTFUL','reason':'Existing strict own-publisher social link replay'})
        elif item['kind']=='brand' and item['field']=='public_brand' and e['source_class']=='company_owned' and site:
            from signalpost.web.collector import extract_public_brand
            from signalpost.web.publisher import extract_publisher
            page=Page(body,e['source_url']);value=extract_public_brand(page,context['name'])
            own=domain(e['source_url'])==domain(site['value']['final_url'])
            text=' '.join(f.text for f in extract_publisher(page).fragments if f.location in {'og:site_name','title'})
            correct=own and value==item['identity'] and value.casefold() in text.casefold()
            proofs.append({'verdict':'CORRECT' if correct else 'DOUBTFUL','reason':'Site title/site-name brand matches saved publisher bytes'})
    return {'verdict':'correct' if any(p['verdict']=='CORRECT' for p in proofs) else 'doubtful','checks':proofs}


def main():
    stage=sys.argv[1];dest=folder(stage)
    source=json.loads((dest/'source_manifest.json').read_text(encoding='utf8'));assert source==manifest()
    records=[];table=[];validation=[]
    for seed in SEEDS:
        directory=dest/f'seed{seed}'
        settings=json.loads((directory/'settings.json').read_text(encoding='utf8'));work=Path(settings['working_directory'])
        counts=json.loads((directory/'counts.json').read_text(encoding='utf8'))
        assert sum(a.startswith('--') for a in settings['command_argv'])==7
        assert counts['envelopes_sha256']==hashlib.sha256((work/'envelopes.jsonl').read_bytes()).hexdigest()
        verification=json.loads((directory/'verification.json').read_text(encoding='utf8'))
        execution=json.loads((directory/'execution.json').read_text(encoding='utf8'));assert execution['exit_code']==0
        assert verification['complete_briefing_contracts']==verification['terminal_envelopes']==100
        assert verification['briefing_unverified_values']==verification['synthesis_unverified_values']==verification['cost_usd']==0
        assert counts['HTTP']<=1850 and counts['CLI_runtime_seconds']<2100 and counts['site']['largest_profile_bytes']<250000
        rows={r['organisation_number']:r for r in (json.loads(s) for s in (work/'envelopes.jsonl').read_text(encoding='utf8').splitlines())}
        oldwork=Path(settings['previous_working_directory'])
        oldrows={r['organisation_number']:r for r in (json.loads(s) for s in (oldwork/'envelopes.jsonl').read_text(encoding='utf8').splitlines())}
        for change in ('added','removed'):
            for item in counts['changes'][change]:
                result=review(item,rows[item['orgnr']] if change=='added' else oldrows[item['orgnr']],work if change=='added' else oldwork)
                records.append({'stage':stage,'seed':seed,'change':change,**item,'review':result})
        table.append(counts);validation.append({'seed':seed,'verification':verification,'execution':execution,'site':counts['site']})
    doubtful=[i for i in records if i['change']=='added' and i['review']['verdict']!='correct']
    save(dest/'identity_items.json',{'stage':stage,'items':records,'doubtful_added':doubtful,'method':'Independent saved-evidence rule recheck, not a human review'})
    all_records=[]
    for name in ORDER:
        path=folder(name)/'identity_items.json'
        if path.exists():all_records.extend(json.loads(path.read_text(encoding='utf8'))['items'])
    reportroot=ROOT/'reports/r5/stageX';reportroot.mkdir(exist_ok=True)
    lines=['# X-stage new/removed identity items','',
        'Every new website, social profile and brand claim is retained with organisation number, legal name, value, original proof context and exact evidence. Removed URLs/brands are explicit. Saved-evidence verdicts do not replace independent human verification.','']
    for i in all_records:
        lines += [f"## {i['stage']} / {i['seed']} / {i['change']} / {i['orgnr']} / {i['legal_name']}",'',
            f"Type: {i['kind']}; identity: {i['identity']}; saved-evidence verdict: {i['review']['verdict']}.",'',
            '```json',json.dumps(i['value'],ensure_ascii=False,indent=2),'```','']
        for e in i['evidence']:
            lines += [f"Source: {e['source_url']} / retrieved {e['retrieved_at']} / SHA-256 `{e['content_sha256']}` / locator `{e['locator']}`",'','Exact excerpt:','','```',e['claim_span'],'```','']
    if not all_records:lines += ['No new or removed website/social/brand item in the completed measured stages.','']
    (reportroot/'new_items.md').write_text('\n'.join(lines),encoding='utf8',newline='\n')
    save(dest/'VALIDATION.json',{'stage':stage,'runtime_source_unchanged':True,'samples':validation,'doubtful_added':doubtful,'cost_usd':0})
    assert not doubtful,'Doubtful identity item: revert this item as instructed; do not silently remove it'
    totals=Counter()
    for c in table:
        for k,v in c['after'].items():
            if isinstance(v,int):totals[k]+=v
    summary=['# '+stage+' measured item','',
        'Author/committer Nethra Venkat; revision/r5; no push; $0. Exactly seven flags, fresh state/new IDs, all six samples; unchanged runtime source. Settings, input/output hashes, request logs and independent verification are retained per seed.','',
        '| Seed | Sites before → after | Declared recall before → after / N | Activity companies / claims | Brand companies / claims | Social companies | Facts | HTTP | Runtime seconds | Largest profile bytes |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for c in table:
        b,a=c['before'],c['after']
        summary.append(f"| {c['seed']} | {b['websites']} → {a['websites']} | {b['declared_homepage_recall']} → {a['declared_homepage_recall']} / {a['declared_homepages']} | {a['activity_companies']} / {a['activity_claims']} | {a['brand_companies']} / {a['brand_claims']} | {a['social_companies']} | {a['facts']} | {c['HTTP']} | {c['CLI_runtime_seconds']:.3f} | {c['site']['largest_profile_bytes']} |")
    summary+=['','Totals: '+json.dumps(dict(totals),sort_keys=True)+'.','',
        'All runs exit 0, 100 ordered terminal envelopes, five cited briefing topics, zero unsupported values, generated site with profile HTML below 250,000 bytes, and hard HTTP/time budgets respected. No doubtful new identity item. [Full new/removed identity receipts](../new_items.md).','']
    if stage=='X1':summary += ['Source capability limitation: the open role-update feed publishes generic role-registry events with exact event type/company/ID/publication time. It does not supply changed role types or persons, so these remain explicitly unknown; a current role roster is never used to invent a past leadership appointment. Leadership-specific preference cannot be applied without source evidence. The timeline and briefing can cite the generic role-registry update. Shared 50-event cap and source-namespaced IDs remain. [Official terms/docs and diagnostic response review](../sources/X1_SOURCE_REVIEW.md).','']
    (dest/'REPORT.md').write_text('\n'.join(summary),encoding='utf8',newline='\n')
    print(json.dumps({'stage':stage,'totals':dict(totals),'new_items':dict(Counter(i['kind'] for i in records if i['change']=='added')),'doubtful':len(doubtful)}))


if __name__=='__main__':main()
