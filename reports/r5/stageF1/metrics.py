"""Count supported dimensionless arithmetic and its cited sentence coverage."""
import json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]

def main():
    stage=sys.argv[1] if len(sys.argv)>1 else 'F1';result={}
    for sample in ('frozen','daily'):
        dest=ROOT/'reports/r5'/('stage'+stage)/sample
        settings=json.loads((dest/'settings.json').read_text(encoding='utf8'));out=Path(settings['working_directory'])
        rows=[json.loads(x) for x in (out/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
        formulas=Counter();yoy_sentences=0;companies=Counter();absolute_unscaled=0
        for row in rows:
            syn=row['run']['synthesis'];seen=set()
            for metric in syn['financial_metrics']:formulas[metric['formula']]+=1;seen.add(metric['formula'])
            companies.update(seen)
            sentences=list(syn.get('briefing',[]))
            for value in syn['sections'].values():
                if isinstance(value,list):sentences.extend(s for s in value if isinstance(s,dict) and 'claim_ids' in s)
            yoy_sentences+=len({s['text'] for s in sentences if s.get('value_kind')=='derived' and 'revenue change from FY' in s['text']})
            absolute_unscaled+=sum(c['availability']=='available' and c['family']=='accounts' and bool(c.get('reporting_period')) and c['reporting_period'].get('unit') is None for c in row['claims'])
        result[sample]={'formula_counts':dict(formulas),'companies_by_formula':dict(companies),
            'derived_ratios':formulas['operating_margin']+formulas['equity_ratio'],'yoy_metrics':formulas['revenue_yoy'],
            'yoy_cited_sentence_instances':yoy_sentences,'absolute_figures_with_unknown_unit':absolute_unscaled}
    (ROOT/'reports/r5'/('stage'+stage)/'financial_metrics.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result))

if __name__=='__main__':main()
