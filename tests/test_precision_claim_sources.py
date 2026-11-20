import base64,copy,gzip,importlib.util,json,sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'reports/r5/precision-sample/audit_sources.py'
spec=importlib.util.spec_from_file_location('precision_audit_sources',MODULE)
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

@pytest.fixture(scope='module')
def proof():
 packet=json.loads(gzip.decompress((MODULE.parent/'proof.json.gz').read_bytes()))
 return packet,{h:base64.b64decode(v) for h,v in packet['bodies'].items()}

@pytest.mark.parametrize('typ',['website','social','brand'])
def test_own_receipt_wins_over_first_bulk_identity_dependency(proof,typ):
 packet,bodies=proof
 item=copy.deepcopy(next(x for x in packet['items'] if x['type']==typ and any(e['locator'].startswith('row:') for e in x['evidence'] if e['id'] in x['claim']['evidence_ids'])))
 by={e['id']:e for e in item['evidence']}
 item['claim']['evidence_ids'].sort(key=lambda eid:not by[eid]['locator'].startswith('row:'))
 assert by[item['claim']['evidence_ids'][0]]['locator'].startswith('row:')
 own,reason=audit.verify(item,bodies,packet)
 assert own and all(not e['locator'].startswith('row:') for e in own)
 assert all(e['source_class']=='company_owned' for e in own)

@pytest.mark.parametrize('mutation',['url','body','span','social_value'])
def test_false_own_page_receipts_do_not_pass_even_with_valid_bulk_context(proof,mutation):
 packet,original=proof;bodies=dict(original)
 typ='social' if mutation=='social_value' else 'website'
 item=copy.deepcopy(next(x for x in packet['items'] if x['type']==typ));own=audit.primary(item)[0]
 if mutation=='url':own['source_url']='https://incorrect.invalid/proof'
 elif mutation=='body':bodies[own['content_sha256']]+=b'corrupt'
 elif mutation=='span':own['claim_span']='planted span absent from publisher response'
 else:item['claim']['value']['url']='https://www.facebook.com/unrelated-company'
 with pytest.raises(AssertionError):audit.verify(item,bodies,packet)
