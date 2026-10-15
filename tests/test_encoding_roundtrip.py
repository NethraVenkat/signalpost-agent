"""Minimized reported cases; no locale-dependent reads or content repair."""
import asyncio
import gzip
import hashlib
import json
import subprocess
import sys
from types import SimpleNamespace
import pytest
from signalpost.web.html import Page
from signalpost.web.descriptions import extract
from signalpost.sources.extract import Section
from signalpost.sources.text import decode_body
from signalpost.sources.blobstore import BlobStore
from signalpost.runner import update,finalize
from signalpost.io.envelope_writer import write
from scripts.accuracy_audit import audit_website_metadata_claim
from scripts.verify_output import verify
from tests.test_registry import config,execute

TEXT='På Stell tilbyr ærlige miljøvalg – klær, såpe og «vår» historie.'


@pytest.mark.parametrize('codec,bom', [('utf-8',False),('utf-8',True),('windows-1252',False),('iso-8859-1',False)])
def test_website_claim_serialization_and_verification(tmp_path,codec,bom):
    text=TEXT if codec!='iso-8859-1' else 'På Stell tilbyr ærlige miljøvalg og vår norske historie.'
    html=f'<html><head><meta charset="{codec}"></head><body><p>{text}</p></body></html>'
    raw=(b'\xef\xbb\xbf' if bom else b'')+html.encode(codec)
    cfg=config(tmp_path,['923609016'])
    _,rows=execute(cfg)
    from signalpost.models.envelope import Envelope
    envelope=Envelope.model_validate(rows[0]);envelope.run.synthesis=None;envelope.profile.synthesis=None
    blobs=BlobStore(cfg.state_dir);sha=blobs.put(raw)
    section=Section(state='available')
    proof=SimpleNamespace(availability='available',value={'identity_level':'VERIFIED'},id='proof',evidence_ids=[])
    response=SimpleNamespace(body=raw,url='https://example.no/about',sha=sha,retrieved_at='2026-10-15T10:00:00Z')
    extract(section,envelope.organisation_number,proof,[(response,Page(raw,response.url))])
    assert section.claims[0].value['text']==text
    assert audit_website_metadata_claim(envelope.organisation_number,section.claims[0].model_dump(),{},decode_body(raw))[0]=='CORRECT'
    update(envelope,'website',section)
    write(cfg.output,[envelope],'union',blobs)
    assert json.loads(cfg.output.read_text(encoding='utf8'))['claims'][-1]['value']['text']==text
    verify(cfg.output,cfg.state_dir,1)
    assert (blobs.directory/sha).read_bytes()==raw
    assert hashlib.sha256(raw).hexdigest()==sha


def test_literal_mojibake_is_preserved_and_markup_is_not_an_encoding_fault():
    literal='PÃ¥ Stell tilbyr varer som er omtalt med denne bokstavsekvensen.'
    body=f'<html><meta charset="utf-8"><p>{literal}</p></html>'.encode('utf8')
    assert literal in decode_body(body)
    text='På Stell er et norsk varemerke som tilbyr produkter uten å skade miljøet.'
    html='<p>På Stell er et <a href="/">norsk varemerke</a> som tilbyr produkter uten å skade miljøet.</p>'
    claim={'field':'website_description.about_paragraph.minimized','value':{'text':text}}
    assert audit_website_metadata_claim('964624046',claim,{},html)[0]=='CORRECT'
    claim['value']['text']=text.replace('uten','med')
    assert audit_website_metadata_claim('964624046',claim,{},html)[0]=='INCORRECT'


@pytest.mark.parametrize('bom',[False,True])
def test_bulk_gzip_prepare_read_roundtrip(tmp_path,bom):
    source=tmp_path/'download.csv.gz';batch=tmp_path/'batch.txt';output=tmp_path/'selected.csv'
    name='RØRLEGGER 1 MOLDE AS';raw=('organisasjonsnummer,navn\r\n812573942,'+name+'\r\n').encode('utf8')
    source.write_bytes(gzip.compress((b'\xef\xbb\xbf' if bom else b'')+raw));before=source.read_bytes()
    batch.write_text('812573942\n',encoding='utf8')
    subprocess.run([sys.executable,'scripts/extract_bulk.py','--bulk',str(source),'--batch',str(batch),'--output',str(output)],check=True,capture_output=True)
    assert name in output.read_text(encoding='utf-8-sig')
    cfg=config(tmp_path/'run',['812573942'],bulk=output)
    _,rows=execute(cfg)
    assert next(c['value'] for c in rows[0]['claims'] if c['field']=='identity.legal_name')==name
    assert source.read_bytes()==before


def test_json_embedded_meta_does_not_select_a_legacy_codec():
    body=json.dumps({'text':'æøå','html':'<meta charset="windows-1252">'},ensure_ascii=False).encode('utf8')
    assert json.loads(decode_body(body))['text']=='æøå'


def test_script_literal_meta_does_not_select_a_codec():
    body='<html><script>const x=\'<meta charset="windows-1252">\';</script><p>æøå</p></html>'.encode('utf8')
    assert 'æøå' in decode_body(body)
