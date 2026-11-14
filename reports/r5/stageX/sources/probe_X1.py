"""Two bounded official source checks after documentation/licence review."""
import asyncio
import hashlib
import json
import time
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
import httpx
from signalpost.web.policy import safe_transport
from signalpost.io.input_adapter import read


async def main():
    dest=Path(__file__).resolve().parent
    orgs=read(Path('reports/r5/baseline/companies.jsonl')).unique
    urls=['https://data.brreg.no/robots.txt','https://data.brreg.no/enhetsregisteret/api/oppdateringer/roller?'+urlencode(
        {'organisasjonsnummer':','.join(orgs),'afterTime':'2023-11-14T00:00:00.000Z','size':1000})]
    receipts=[]
    async with httpx.AsyncClient(transport=safe_transport(1),trust_env=False,follow_redirects=False,timeout=20,
                                headers={'User-Agent':'SignalpostAgent/1.3.0','Accept':'application/json'}) as client:
        for url in urls:
            started=time.monotonic()
            try:
                r=await client.get(url);body=r.content;sha=hashlib.sha256(body).hexdigest()
                (dest/(sha+'.body')).write_bytes(body)
                item={'url':url,'status':r.status_code,'sha256':sha,'retrieved_at':datetime.now(timezone.utc).isoformat(),
                    'runtime':time.monotonic()-started,'headers':dict(r.headers)}
                print(r.status_code,body[:1000],flush=True)
            except Exception as exc:item={'url':url,'error':type(exc).__name__,'runtime':time.monotonic()-started};print(item,flush=True)
            receipts.append(item);await asyncio.sleep(1)
    (dest/'X1-probe.json').write_text(json.dumps({'diagnostic_HTTP_attempts':len(receipts),'cost_usd':0,'receipts':receipts},indent=2)+'\n',encoding='utf8')


if __name__=='__main__':asyncio.run(main())
