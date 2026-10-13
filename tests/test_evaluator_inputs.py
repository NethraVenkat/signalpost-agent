import json
import pytest
from signalpost.io.input_adapter import read
from scripts.verify_output import verify
from tests.test_registry import config,execute

ORG='923609016'
PAYLOADS=[
    '{"organisation_number":"923609016","evaluation_split":"test","sample_slice":2,"unknown":{"x":1}}\n',
    '{"organisation_number":923609016}\n',
    '["923609016",923609016,"bad"]',
    '{"organisation_numbers":["923609016","bad","923609016"]}',
    '923609016\nbad\n923609016',
    '\ufeff923609016\r\nbad\r\n923609016\r\n\r\n',
    '{"organisation_number":"923609016"}\r\n{"organisation_number":"bad"}\r\n',
    '\ufeff[{"organisation_number":923609016,"extra":true},{"organisation_number":"bad"}]',
    '923609016\n\n',
    '{"organisation_number":"923609016"}',
]


@pytest.mark.parametrize('payload',PAYLOADS)
@pytest.mark.parametrize('shape',['union','contract','reference'])
def test_every_input_row_is_reserved_in_order_and_all_shapes_verify(tmp_path,payload,shape):
    cfg=config(tmp_path,[],envelope_shape=shape)
    cfg.organisations.write_text(payload,encoding='utf8',newline='')
    expected=read(cfg.organisations).rows
    report,rows=execute(cfg)
    assert [row['organisation_number'] for row in rows]==expected
    assert report['emitted_envelopes']==len(expected)
    assert report['emit_duplicates'] is True
    verify(cfg.output,cfg.state_dir,len(expected),cfg.organisations,cfg.report)
    assert all(e['organisation_number']!='bad' for e in report['request_log'])


def test_duplicate_rows_do_not_repeat_research(tmp_path):
    report,rows=execute(config(tmp_path,[ORG,ORG,ORG]))
    assert len(rows)==3 and report['requests']==4
    assert rows[0]==rows[1]==rows[2]
