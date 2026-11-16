"""Record supplied independent human reviews, preserving automated verdicts."""
from signalpost.portable_paths import portable, portable_text  # saved paths stay repo-relative
import json
import hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parent


def save(path,data):
    path.write_text(portable_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n'),encoding='utf8',newline='\n')


def identity(org,kind,value):
    if kind=='website':value=value.get('final_url') or value.get('url')
    elif kind=='social':value=value['url']
    elif kind=='LEI':value=value['lei']
    elif kind=='parent':value={k:value.get(k) for k in ('child_lei','parent_lei','relationship_type')}
    elif kind=='job':value=value.get('uuid') or value.get('url') or value
    return org,kind,json.dumps(value,sort_keys=True,ensure_ascii=False)


def main():
    notes={
        '986464492':'Own legal name, address, phone and email match the register; not a client listing.',
        '986128662':'Independent web hand-check confirms the company website.',
        '980616622':'Independent web hand-check confirms the company website.',
        '934626176':'Organisation number verified on the privacy page.',
        '997274253':'Independent web hand-check confirms the company website.',
        '994882597':'Independent web hand-check confirms the company website.',
        '984204663':'Independent web hand-check confirms the company website.',
        '984406622':'Independent web hand-check confirms the company website.',
        '984177070':'Independent web hand-check confirms the company website.',
        '948039958':'Both braudbakeri.no and valakerbakeri.no confirmed; organisation number in the footer.',
        '918638628':'Organisation number verified on page; saved apex/www variants are scoped separately.'}
    social={('986464492','https://www.facebook.com/optimalregnskap'),('986128662','https://www.facebook.com/maskinkurs'),
            ('980616622','https://www.facebook.com/BAGGES.AS'),('980616622','https://www.linkedin.com/company/bagges-as')}
    current={}
    for stage in ('stageR5','stageR3'):
        data=json.loads((ROOT/f'reports/r5/{stage}/items.json').read_text(encoding='utf8'))
        for item in data['all_published_items']:
            key=identity(item['orgnr'],item['kind'],item['value'])
            if key not in current:current[key]={**item,'stages':[]}
            current[key]['stages'].append(stage)
    reviews=[]
    for key,item in sorted(current.items()):
        org,kind,_=key;url=item['url']
        if not (kind=='website' and org in notes or kind=='social' and (org,url) in social):continue
        note=notes[org] if kind=='website' else ('Link confirmed present on the company’s own site.'+
             (' LinkedIn also links back to bagges.no.' if 'linkedin.com' in url else ''))
        reviews.append({'organisation_number':org,'company':item['legal_name'],'kind':kind,'url':url,
            'verdict':'correct','reviewer':'Nethra Venkat','review_date':'2026-11-14',
            'method':'Human hand-check with independent web verification, supplied explicitly in conversation.',
            'note':note,'automated_verdict':item['automated_verdict'],'proof_tier':item['tier'],
            'receipts':item['own_receipts'],'registry_receipts':item['registry_receipts'],'stages':item['stages']})
    assert len({r['organisation_number'] for r in reviews if r['kind']=='website'})==11
    assert Counter(r['kind'] for r in reviews)=={'website':13,'social':4}
    cumulative={}
    observations=0
    for name in ('reports/r5/precision/ledger.json','reports/r5/stageH/precision/ledger.json'):
        data=json.loads((ROOT/name).read_text(encoding='utf8'))
        for item in data['items']:
            observations+=1;key=identity(item['organisation_number'],item['kind'],item['value'])
            cumulative[key]={'kind':item['kind'],'automated_verdict':item['verdict'],'human_verified':bool(item.get('human_review') and item['human_review']['verdict']=='correct')}
    for key,item in current.items():
        observations+=1
        old=cumulative.get(key,{})
        cumulative[key]={'kind':item['kind'],'automated_verdict':item['automated_verdict'],'human_verified':old.get('human_verified',False)}
    for r in reviews:
        key=identity(r['organisation_number'],r['kind'],{'final_url':r['url']} if r['kind']=='website' else {'url':r['url']})
        cumulative[key]['human_verified']=True
    counts={kind:{'items_checked':sum(k['kind']==kind for k in cumulative.values()),
        'human_verified_correct':sum(k['kind']==kind and k['human_verified'] for k in cumulative.values()),
        'automated_correct':sum(k['kind']==kind and k['automated_verdict']=='correct' for k in cumulative.values()),
        'automated_doubtful':sum(k['kind']==kind and k['automated_verdict']=='doubtful' for k in cumulative.values()),
        'wrong':sum(k['kind']==kind and k['automated_verdict']=='wrong' for k in cumulative.values())}
        for kind in ('website','social','job','LEI','parent','award')}
    totals={field:sum(c[field] for c in counts.values()) for field in next(iter(counts.values()))}
    assert totals['wrong']==0 and totals['human_verified_correct']==24
    result={'reviewer':'Nethra Venkat','review_date':'2026-11-14','reviews':reviews,'counts':counts,'totals':totals,
        'counting_method':'Cumulative distinct organisation/type/URL (website/social), LEI, parent relationship or job UUID; same item across stages counted once. Original automated verdicts are not rewritten by a human verdict.',
        'input_ledgers':['reports/r5/precision/ledger.json','reports/r5/stageH/precision/ledger.json','reports/r5/stageR5/items.json','reports/r5/stageR3/items.json'],
        'limits':'Human verification is the reviewer’s supplied independent web hand-check, not an assistant re-fetch or population precision estimate. Published outputs and proof tiers unchanged.'}
    save(DEST/'human_reviews.json',result)
    lines=['# R5/R3 human precision ledger','',
        'Reviewer: **Nethra Venkat**. Date: **2026-11-14**. Method: **human hand-check with independent web verification**, supplied explicitly in conversation. These are the reviewer’s findings, not a new assistant web fetch. All 11 reviewed company websites are CORRECT; 13 distinct website URLs include both VALAKER domains and VESTFJORDEN hostname variants. Four social profiles are separately human-confirmed. Original automated verdicts, evidence and proof tiers remain unchanged.','',
        '## Cumulative precision totals','',result['counting_method'],'',
        '| Type | Items checked | Human-verified correct | Automated correct | Automated doubtful | Wrong |',
        '|---|---:|---:|---:|---:|---:|']
    for kind,c in counts.items():lines.append('| '+kind+' | '+' | '.join(str(c[k]) for k in totals)+' |')
    lines+=['| **Total** | '+' | '.join(str(v) for v in totals.values())+' |','',
        'This cumulative union covers the original T/H precision ledgers and R5/R3 website/social receipts; it does not claim that every later job/LEI/parent/award was re-audited. Repeated observations are deduplicated. Automated doubtful items retain their labels even where separately human-confirmed. Human wrong = 0; automated wrong = 0. Unreviewed items are not human-verified.','',
        '## Exact human verdicts','',
        '| Org number | Company | Type | URL | Original proof tier | Human verdict | Review basis |',
        '|---|---|---|---|---|---|---|']
    for r in reviews:lines.append(f"| {r['organisation_number']} | {r['company']} | {r['kind']} | {r['url']} | {r['proof_tier']} | **CORRECT** | {r['note']} |")
    lines+=['','Full saved response excerpts, hashes, retrieval times and registry receipts are retained in [human_reviews.json](human_reviews.json), [R5 URL receipts](../stageR5/new_websites.md) and [R3 URL receipts](new_websites.md). Findings are URL/company-scoped; no other domain or social profile is approved by inference.','']
    (DEST/'LEDGER.md').write_text(portable_text('\n'.join(lines)),encoding='utf8',newline='\n')
    readme=ROOT/'README.md';text=readme.read_text(encoding='utf8')
    start='<!-- R5/R3 human precision review -->';end='<!-- End R5/R3 human precision review -->'
    block='\n'.join([start,'',
        'R5/R3 human hand review — **Nethra Venkat, 2026-11-14, independent web verification**: all **11 company websites CORRECT**, covering 13 saved URLs (both VALAKER domains and VESTFJORDEN apex/www). OPTIMAL REGNSKAP’s own name/address/phone/email match the register; it is not a client listing. Tashakori’s orgnr is on its privacy page; VALAKER’s is in the footer, and VESTFJORDEN’s is on page. MASKINKURS, BAGGES, ELEKTROFIL, DICA, A TIL Å PROFILERING, TIDEMANN and KRAABOL are confirmed correct. Optimal, Maskinkurs and Bagges Facebook links are confirmed on their own sites; Bagges LinkedIn links back to bagges.no. [Exact URL-scoped human ledger and receipts](reports/r5/stageR3/LEDGER.md).','',
        f"Cumulative deduplicated checked items: **{totals['items_checked']}**; **{totals['human_verified_correct']} human-verified correct**; **0 wrong**. This union covers the original T/H precision ledgers plus R5/R3 website/social receipts, counting an organisation/type/URL, LEI, parent relationship or job UUID once. It does not treat unreviewed items as human-verified, overwrite automated doubtful verdicts, re-audit all later source families, or claim population accuracy. See the ledger for per-type totals, methodology and source limits.",'',end,''])
    if start in text:text=text[:text.index(start)]+block+text[text.index(end)+len(end):].lstrip('\n')
    else:text=text.replace('### Historical scale measurements',block+'\n### Historical scale measurements',1)
    readme.write_text(portable_text(text),encoding='utf8',newline='\n')
    print(json.dumps({'reviewed_companies':11,'new_human_website_URLs':13,'new_human_social_URLs':4,'cumulative':totals}))


if __name__=='__main__':main()
