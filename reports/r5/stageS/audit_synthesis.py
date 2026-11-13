"""Save a reviewable synthesis inventory from the Stage S saved output."""
import hashlib,json
from pathlib import Path
from collections import Counter
root=Path('.data/r5/stageS-run');dest=Path('reports/r5/stageS')
rows=[json.loads(s) for s in (root/'envelopes.jsonl').read_text(encoding='utf8').splitlines()]
items=[]
for row in rows:
 s=row['run']['synthesis']; ev={e['id']:e for e in row['evidence']}; claims={c['id']:c for c in row['claims']}
 items.append({'organisation_number':row['organisation_number'],'topics':[x['topic'] for x in s['briefing'] if x.get('topic')], 'mirror_matches':s==row['profile']['synthesis'],'metrics':s['financial_metrics'],'year_check':s['financial_year_check'],'briefing':s['briefing']})
result={'source':str(root/'envelopes.jsonl'),'sha256':hashlib.sha256((root/'envelopes.jsonl').read_bytes()).hexdigest(),'companies':len(rows),'formulas':dict(Counter(m['formula'] for i in items for m in i['metrics'])),'newer_filing_flags':sum(bool((i['year_check'] or {}).get('newer_filing_exists')) for i in items),'per_company':items}
(dest/'synthesis_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='per_company'}))
