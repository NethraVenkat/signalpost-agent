import asyncio,json
from pathlib import Path
import httpx
from signalpost.config import Config
from signalpost.budget import Budget,SourceFailure
from signalpost.sources.http import Http
from signalpost.sources.blobstore import BlobStore
from signalpost.portable_paths import portable_text
async def main():
 out=Path('out/g1-api-probe');out.mkdir(exist_ok=True)
 c=Config(organisations=Path('reports/r5/baseline/companies.jsonl'),output=out/'envelopes.jsonl',report=out/'report.json')
 b=Budget(c);blobs=BlobStore(out/'state');items=[]
 async with httpx.AsyncClient(trust_env=False,headers={'Accept':'application/json','User-Agent':'SignalpostAgent/1.0'}) as client:
  h=Http(client,c,b,blobs)
  for org in ['923609016','984851006','914778271']:
   for kind in ['signatur','prokura','group']:
    url=f'https://data.brreg.no/enhetsregisteret/api/konsernstruktur/{org}' if kind=='group' else f'https://data.brreg.no/fullmakt/enheter/{org}/{kind}'
    item={'org':org,'kind':kind,'url':url}
    try:
     r=await h.get(url,org);item.update(status=r.status,sha=r.sha,retrieved_at=r.retrieved_at)
     (out/f'{org}-{kind}.body').write_bytes(r.body)
     print(json.dumps(item),flush=True)
    except SourceFailure as e:item.update(error=e.code,message=portable_text(str(e)));print(json.dumps(item),flush=True)
    items.append(item)
    await asyncio.sleep(1)
 Path('reports/r5/gaps/g1-api/probe.json').write_text(portable_text(json.dumps({'baseline':'ac88ab0','policy':'documented official API; existing registry Http client; no crawler robots gate','responses':items,'events':b.events},indent=2))+'\n',encoding='utf8',newline='\n')
asyncio.run(main())
