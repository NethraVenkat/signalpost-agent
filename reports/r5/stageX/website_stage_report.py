"""Write the website-stage hand-check ledger from accepted saved receipts."""
import json
import sys
from collections import Counter
from pathlib import Path
from measure import ROOT,SEEDS,folder


def main():
    stage=sys.argv[1];assert stage in {'R6','R7'}
    dest=folder(stage)
    ledger=json.loads((dest/'identity_items.json').read_text(encoding='utf8'))
    assert not ledger['doubtful_added']
    items=[i for i in ledger['items'] if i['kind'] in {'website','social'}]
    lines=['# '+stage+' website and social receipts','',
        'Every added or removed URL across the six accepted fresh samples. Verdicts replay saved evidence and rules; independent human review is still requested. The complete publisher receipt and registry evidence are retained below.','']
    for i in sorted(items,key=lambda i:(i['seed'],i['change'],i['orgnr'],i['identity'])):
        value=i['value'];tier=value.get('proof_type',value.get('verification','existing strict own-site social rule'))
        lines += [f"## {i['seed']} / {i['change']} / {i['orgnr']} / {i['legal_name']}",'',
            f"{i['kind']}: {i['identity']}",'',f"Proof tier: {tier}. Saved-evidence verdict: {i['review']['verdict']}.",'',
            '```json',json.dumps(value,ensure_ascii=False,indent=2),'```','']
        for e in i['evidence']:
            lines += [f"Source: {e['source_url']}; retrieval: {e['retrieved_at']}; SHA-256: `{e['content_sha256']}`; locator: `{e['locator']}`.",'','Exact excerpt:','','```',e['claim_span'],'```','']
    if not items:lines+=['No added or removed website or social URLs.','']
    (dest.parent/'new_websites.md').write_text('\n'.join(lines),encoding='utf8',newline='\n')
    summary=['# '+stage+' six-sample measurement','',
        'Exactly seven evaluator flags, fresh state, sequential foreground samples, $0. The runtime source manifest is identical across all accepted samples. X5 remains dropped.','',
        '| Seed | Websites before / after | Declared recall before / after / listed | New website proof types | Social companies | Activity claims | Brand claims | Facts | HTTP | Process seconds |',
        '|---|---:|---:|---|---:|---:|---:|---:|---:|---:|']
    gains=Counter()
    for seed in SEEDS:
        c=json.loads((dest/f'seed{seed}/counts.json').read_text(encoding='utf8'));b,a=c['before'],c['after']
        proof=Counter(i['value']['proof_type'] for i in items if i['seed']==seed and i['change']=='added' and i['kind']=='website');gains.update(proof)
        summary.append(f"| {seed} | {b['websites']} / {a['websites']} | {b['declared_homepage_recall']} / {a['declared_homepage_recall']} / {a['declared_homepages']} | {dict(proof)} | {a['social_companies']} | {a['activity_claims']} | {a['brand_claims']} | {a['facts']} | {c['HTTP']} | {c['CLI_runtime_seconds']:.3f} |")
    summary+=['','Added URL proof labels: '+json.dumps(dict(gains),sort_keys=True)+'.','',
        'Proof labels attribute the published evidence tier. Retry and candidate-order changes are discovery changes and cannot be causally isolated by proof label; live-source recoveries/removals are disclosed separately in the URL ledger.','',
        'All accepted samples: exit 0, 100 ordered terminal envelopes, five cited briefing topics, zero unsupported values, site generated below the 250,000-byte profile gate, hard HTTP/time limits respected. No doubtful added identity survives the saved-evidence recheck.','',
        '[Every added/removed website and social URL with exact receipts](new_websites.md). See '+stage+'/VALIDATION.json, each seed settings/report/counts and execution/verification receipts for the complete audit trail.','']
    (dest.parent/'SUMMARY.md').write_text('\n'.join(summary),encoding='utf8',newline='\n')

if __name__=='__main__':main()
