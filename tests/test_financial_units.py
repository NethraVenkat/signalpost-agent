import asyncio
import json
import httpx
from signalpost.runner import run
from tests.test_registry import config,handler


def test_empirical_nok_unit_preserves_reported_values(tmp_path):
    for currency,expected_unit in [('NOK','NOK'),('EUR',None)]:
        cfg=config(tmp_path/currency,['923609016'])
        def response(request):
            result=handler(missing_accounts=False)(request)
            if '/regnskapsregisteret/' in request.url.path:
                body=json.loads(result.content)
                body[0]['valuta']=currency
                body[0]['resultatregnskapResultat']['aarsresultat']=1234567
                return httpx.Response(200,json=body)
            return result
        async def execute():
            async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
                return await run(cfg,client)
        asyncio.run(execute())
        row=json.loads(cfg.output.read_text().splitlines()[0])
        claim=next(c for c in row['claims'] if c['field']=='accounts.net_result')
        assert claim['value']==1234567
        assert claim['reporting_period']['unit']==expected_unit
        evidence={e['id']:e for e in row['evidence']}
        calibration=[evidence[key] for key in claim['evidence_ids'] if evidence[key]['source_class']=='company_report']
        assert len(calibration)==(2 if currency=='NOK' else 0)
        for item in calibration:
            assert item['claim_span'].encode() in (cfg.state_dir/'blobs'/item['content_sha256']).read_bytes()
