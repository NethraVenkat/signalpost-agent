import hashlib,json,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.robotparser import RobotFileParser
import httpx
from signalpost.config import Config
from signalpost.portable_paths import portable_text
out=Path(__file__).resolve().parent; url='https://data.brreg.no/robots.txt'
ua=Config.model_fields['website_user_agent'].default
result={'recorded_at':datetime.now(timezone.utc).isoformat(),'baseline':'ac88ab0','robots_url':url,'user_agent':ua,'attempts':[],'backoff_seconds':[5,20],'company_data_requests':0,'execution_scope':'normal network when escalated; sandbox receipt saved separately'}
orgs=['923609016','984851006','914778271']
paths=[f'https://data.brreg.no/{path}' for org in orgs for path in [f'fullmakt/enheter/{org}/signatur',f'fullmakt/enheter/{org}/prokura',f'enhetsregisteret/api/konsernstruktur/{org}']]
with httpx.Client(headers={'User-Agent':ua},follow_redirects=False,trust_env=False,timeout=20) as client:
 for i in range(3):
  if i:time.sleep([5,20][i-1])
  item={'attempt':i+1,'status':None,'content':None,'content_sha256':None}
  try:
   r=client.get(url); item.update(status=r.status_code,content_sha256=hashlib.sha256(r.content).hexdigest(),content=r.text,headers=dict(r.headers))
   (out/f'robots-{i+1}.body').write_bytes(r.content)
   if 200<=r.status_code<300:
    rp=RobotFileParser();rp.parse(r.text.splitlines());result['allowed']={p:rp.can_fetch(ua,p) for p in paths};result['decision']='robots retrieved';result['attempts'].append(item);break
   if 400<=r.status_code<500:
    result['allowed']={p:True for p in paths};result['decision']='4xx: allow per RFC 9309';result['attempts'].append(item);break
  except httpx.HTTPError as e:item.update(error=type(e).__name__,message=portable_text(str(e)))
  result['attempts'].append(item)
 else:result['decision']='fail closed: robots unreachable after retries'
(out/'preflight.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(result,ensure_ascii=False))
