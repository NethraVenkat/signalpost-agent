"""Independent saved-output checks; never rewrites an envelope to pass a gate."""
import argparse
import hashlib
import json
import csv,io
from functools import lru_cache
from pathlib import Path
from signalpost.models.shapes import validate
from signalpost.io.input_adapter import read
from signalpost.models.claim import Claim
from signalpost.models.evidence import Evidence
from signalpost.models.envelope import Change,Error
from signalpost.models.synthesis import Synthesis
from signalpost.synthesis.validate import sentence_error,SECTIONS
from signalpost.synthesis.catalog import change_claims
from types import SimpleNamespace
from signalpost.sources.text import decode_body
from decimal import Decimal, ROUND_HALF_UP, localcontext
from datetime import date


def verify_financial_sources(row, data, evidence, stored_body):
    raw=(row.get('run',{}).get('synthesis') or data.get('synthesis') or {})
    if raw.get('contract_version')!='r5-S': return 0,0
    claims={c['id']:c for c in data['claims']}
    documents={};checked=0
    for c in data['claims']:
        if c['family']!='accounts' or c['availability']!='available':continue
        source=next((evidence[eid] for eid in c['evidence_ids'] if
                     evidence[eid]['source_url'].startswith('https://data.brreg.no/regnskapsregisteret/regnskap/')
                     and evidence[eid]['locator'].startswith('/')),None)
        if source is None: continue  # Synthetic unit-test sources are checked by their own receipts.
        sha=source['content_sha256']
        if sha not in documents: documents[sha]=json.loads(stored_body(sha))
        document=documents[sha];parts=source['locator'].strip('/').split('/')
        value=document
        for part in parts:value=value[int(part)] if isinstance(value,list) else value[part.replace('~1','/').replace('~0','~')]
        assert not isinstance(value,bool) and value==c['value'], 'Financial value differs from source JSON pointer'
        record=document[int(parts[0])]
        assert str(record['virksomhet']['organisasjonsnummer'])==row['organisation_number'], 'Financial source has wrong entity'
        assert record['regnskapstype']=='SELSKAP', 'Consolidated values presented as entity figures'
        p=c['reporting_period'];dates=record['regnskapsperiode']
        assert p['period_start']==dates.get('fraDato') and p['period_end']==dates.get('tilDato'), 'Financial period differs from source'
        assert p['fiscal_year']==str(dates.get('tilDato'))[:4] and p['account_type']=='SELSKAP'
        assert p['currency']==record.get('valuta'), 'Financial currency differs from source'
        if record.get('enhet') is None and p.get('unit')=='NOK':
            assert not c['field'].startswith('accounts.history.') and p['currency']=='NOK'
            assert p.get('unit_basis')=='four_exact_parent_2025_ratios_within_0.995_1.005'
            assert any(evidence[eid]['source_class']=='company_report' for eid in c['evidence_ids']), 'Missing unit calibration evidence'
        else: assert p.get('unit')==record.get('enhet'), 'Unsupported financial unit'
        checked+=1
    for m in raw.get('financial_metrics',[]):
        a,b=[claims[cid] for cid in m['input_claim_ids']]
        pa,pb=a['reporting_period'],b['reporting_period']
        assert a['availability']==b['availability']=='available'
        assert pa['account_type']==pb['account_type']=='SELSKAP'
        assert pa.get('currency') and pa.get('unit') and all(pa.get(k)==pb.get(k) for k in ('currency','unit','account_type'))
        top,bottom=Decimal(str(a['value'])),Decimal(str(b['value']))
        assert top.is_finite() and bottom.is_finite() and bottom>0
        if m['formula']=='revenue_yoy':
            assert a['field']=='accounts.revenue' and b['field'].startswith('accounts.history.') and b['field'].endswith('.revenue')
            sa,ea,sb,eb=[date.fromisoformat(p[k]) for p,k in [(pa,'period_start'),(pa,'period_end'),(pb,'period_start'),(pb,'period_end')]]
            assert ea.year==eb.year+1 and sa.year==sb.year+1 and eb<sa
            assert (sa.month,sa.day,ea.month,ea.day)==(sb.month,sb.day,eb.month,eb.day)
            assert 350 <= (ea-sa).days+1 <=366 and 350 <= (eb-sb).days+1 <=366
            top-=bottom
        else:
            assert all(pa.get(k)==pb.get(k) for k in ('fiscal_year','period_start','period_end'))
            fields={'operating_margin':('accounts.operating_result','accounts.revenue'), 'equity_ratio':('accounts.equity','accounts.total_assets')}
            assert (a['field'],b['field'])==fields[m['formula']]
        with localcontext() as ctx:
            ctx.prec=80
            expected=format((top/bottom*100).quantize(Decimal('.01'),rounding=ROUND_HALF_UP),'f')
        assert m['value']==expected and m['unit']=='percent', 'Unsupported derived financial value'
    year=raw.get('financial_year_check')
    if year:
        registered=claims[year['claim_ids'][0]]
        assert registered['field']=='identity.latest_submitted_accounts'
        source=next((evidence[eid] for eid in registered['evidence_ids'] if
                     evidence[eid]['source_url'].startswith('https://data.brreg.no/enhetsregisteret/')),None)
        if source:
            body=stored_body(source['content_sha256']);locator=source['locator']
            if '/column:' in locator:
                column=locator.rsplit('/column:',1)[1]
                assert column.casefold().replace(' ','').replace('å','aa')=='sisteinnsendteaarsregnskap'
                dialect=csv.Sniffer().sniff(body,delimiters=';,\t')
                records=list(csv.DictReader(io.StringIO(body),dialect=dialect))
                record=next(r for r in records if next((v for k,v in r.items() if k.casefold().lstrip('\ufeff')=='organisasjonsnummer'),None)==row['organisation_number'])
                actual=record[column]
            else:
                assert locator=='/sisteInnsendteAarsregnskap'
                record=json.loads(body)
                assert str(record['organisasjonsnummer'])==row['organisation_number']
                actual=record['sisteInnsendteAarsregnskap']
            assert str(actual)==year['registry_year'], 'Registry filing year differs from source'
    return checked,len(raw.get('financial_metrics',[]))


def verify_registry_events(row,data,evidence,stored_body,cache=None):
    cache={} if cache is None else cache
    def document(sha):
        key=('json',sha)
        if key not in cache:cache[key]=json.loads(stored_body(sha))
        return cache[key]
    events=[c for c in data['claims'] if c['availability']=='available' and c['field'].startswith('registry_change.')
            and any(evidence[eid]['extraction_method']=='signalpost.registry_changes.v3' for eid in c['evidence_ids'])]
    assert len(events)<=50,'Registry event cap exceeded'
    from signalpost.sources.registry_changes import timestamp
    order=[(timestamp(c['value']['date']),c['value']['event_id'],c['field']) for c in events]
    assert order==sorted(order,reverse=True),'Registry events are not newest first'
    assert len({c['field'] for c in events})==len(events)
    for c in events:
        v=c['value'];source=next(evidence[eid] for eid in c['evidence_ids'] if evidence[eid]['extraction_method']=='signalpost.registry_changes.v3')
        raw=document(source['content_sha256'])
        for key in source['locator'].strip('/').split('/'):
            raw=raw[int(key)] if isinstance(raw,list) else raw[key.replace('~1','/').replace('~0','~')]
        assert raw['dato']==v['date'] and raw['oppdateringsid']==v['event_id'] and raw['endringstype']==v['event_type'],'Registry event differs from source'
        assert raw['organisasjonsnummer']==v['record_orgnr']
        assert v['company_orgnr']==row['organisation_number']
        assert v['changed_fields']==[{'path':x['path'],'operation':x['op']} for x in raw.get('endringer') or []]
        if 'new_value' in v:
            assert any(x.get('path')==v['changed_field'] and x.get('op')==v['operation'] and x.get('value')==v['new_value'] for x in raw.get('endringer') or [])
        if v.get('subunit_orgnr'):
            unit=v['subunit_orgnr'];assert unit==raw['organisasjonsnummer']
            proofs=[evidence[eid] for eid in c['evidence_ids'] if evidence[eid]['source_url'].startswith('https://data.brreg.no/enhetsregisteret/api/underenheter?')]
            assert any(any(u.get('organisasjonsnummer')==unit and u.get('overordnetEnhet')==row['organisation_number']
                           for u in document(e['content_sha256']).get('_embedded',{}).get('underenheter',[])) for e in proofs),'Subunit event lacks exact parent source proof'
        else:assert raw['organisasjonsnummer']==row['organisation_number']
        # Reconstruct the complete closed event frame, including labels and
        # optional values, from the raw event and independently verified scope.
        from signalpost.sources import registry_changes as rc
        from signalpost.sources.http import Response
        scope={}
        if v.get('subunit_orgnr'):
            for e in proofs:
                for unitrow in document(e['content_sha256']).get('_embedded',{}).get('underenheter',[]):
                    if unitrow.get('organisasjonsnummer')==v['subunit_orgnr'] and unitrow.get('overordnetEnhet')==row['organisation_number']:
                        scope[v['subunit_orgnr']]=(unitrow,Evidence.model_validate(e))
        key=('response',source['content_sha256'],source['source_url'])
        if key not in cache:cache[key]=Response(stored_body(source['content_sha256']).encode('utf8'),200,source['source_url'],source['retrieved_at'],source['content_sha256'])
        response=cache[key]
        endpoint='underenheter' if '/oppdateringer/underenheter?' in source['source_url'] else 'enheter'
        expected=rc.extract(raw,response,source['locator'],row['organisation_number'],endpoint,scope)
        assert len(expected.claims)==1 and expected.claims[0].value==v,'Unsupported registry event frame'
    return len(events)


def verify_synthesis(row):
    data=row if 'claims' in row else row['profile']
    raw=row['run'].get('synthesis') if 'run' in row else row['profile'].get('synthesis')
    if raw is None:return 0,0
    synthesis=Synthesis.model_validate(raw)
    envelope=SimpleNamespace(organisation_number=row['organisation_number'], claims=[Claim.model_validate(c) for c in data['claims']],
        evidence=[Evidence.model_validate(e) for e in data['evidence']],changes=[Change.model_validate(c) for c in data['changes']],
        errors=[Error.model_validate(e) for e in data.get('errors',[])],
        run=SimpleNamespace(refresh=row['run']['refresh'] if 'run' in row else data['refresh'],
                            sections=row['run']['sections'] if 'run' in row else data['sections'],
                            completed_at=row['run']['completed_at'] if 'run' in row else row['completed_at']))
    sentences=[s for key in SECTIONS for s in getattr(synthesis.sections,key)]
    assert all(sentence_error(s,envelope) is None for s in sentences),'Unverified synthesis sentence'
    assert len(synthesis.briefing) <= 6, 'Briefing exceeds six sentences'
    assert all((s.claim_ids or s.observation_ids) and sentence_error(s,envelope) is None for s in synthesis.briefing), 'Unverified briefing sentence'
    if synthesis.contract_version == 'r5-S':
        from signalpost.synthesis.overview import contract_errors
        assert not contract_errors(synthesis,envelope), 'Incomplete or tampered synthesis contract'
    assert synthesis.summary==' '.join(s.text for s in sentences),'Summary differs from checked sentences'
    assert synthesis.checks.sentences==synthesis.checks.cited==len(sentences) and synthesis.checks.values_verified
    assert synthesis.change_claims==change_claims(envelope),'Change citations differ from source events'
    if 'run' in row and 'profile' in row:assert row['profile'].get('synthesis')==raw,'Synthesis mirror differs'
    return 1,len(sentences)


def load(path):
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").split("\n") if line.strip()]
    for row in rows:
        shape = "union" if "profile" in row and "claims" in row else "reference" if "profile" in row else "contract"
        validate(row, shape)
    return rows


def ids(rows):
    return {r["organisation_number"]: sorted(c["id"] for c in (r if "claims" in r else r["profile"])["claims"]) for r in rows}


def verify(first, state_dir, count, organisations=None, report=None, require_clean=False, second=None):
    rows = load(first)
    assert len(rows) == count, f"Expected {count}, got {len(rows)}"
    repeated={}
    for row in rows:
        org=row['organisation_number']
        if org in repeated:assert row==repeated[org], 'Duplicate input rows have inconsistent envelopes'
        repeated[org]=row
    if organisations is not None:
        inputs=read(organisations)
        expected=inputs.rows
        if report is not None and json.loads(report.read_text(encoding='utf8')).get('emit_duplicates') is False:
            expected=inputs.unique
        assert [r['organisation_number'] for r in rows] == expected, 'Membership/order differs from input'
    seen, published = set(), 0
    @lru_cache(maxsize=8)
    def stored_body(sha):
        return decode_body((state_dir/'blobs'/sha).read_bytes())
    synthesis_companies=synthesis_sentences=0
    financial_inputs=derived_metrics=registry_events=0
    registry_documents={}
    for row in rows:
        companies,sentences=verify_synthesis(row)
        synthesis_companies+=companies;synthesis_sentences+=sentences
        data = row if "claims" in row else row["profile"]
        evidence = {e["id"]: e for e in data["evidence"]}
        for claim in data["claims"]:
            if claim["availability"] != "available":
                assert claim["value"] is None
                continue
            published += 1
            assert claim["evidence_ids"]
            for ref in claim["evidence_ids"]:
                e = evidence[ref]
                assert e["source_url"] and e["retrieved_at"].endswith("Z") and e["locator"] and e["extraction_method"]
                sha = e["content_sha256"]
                if sha not in seen:
                    assert hashlib.sha256((state_dir / "blobs" / sha).read_bytes()).hexdigest() == sha
                    seen.add(sha)
                body = stored_body(sha)
                assert len(e['claim_span']) <= 300 and e['claim_span'] in body, 'Non-verbatim evidence span'
        inputs_checked,metrics_checked=verify_financial_sources(row,data,evidence,stored_body)
        financial_inputs+=inputs_checked; derived_metrics+=metrics_checked
        registry_events+=verify_registry_events(row,data,evidence,stored_body,registry_documents)
    result = {"lines": len(rows), "schema_valid": True, "published_claims": published, "source_blobs_verified": len(seen)}
    result.update(synthesis_companies=synthesis_companies,synthesis_sentences=synthesis_sentences,synthesis_unverified_values=0)
    result.update(financial_inputs_verified=financial_inputs,derived_financial_metrics_verified=derived_metrics)
    result['registry_events_verified']=registry_events
    briefings = [(row['run'].get('synthesis') if 'run' in row else row['profile'].get('synthesis')) or {} for row in rows]
    result.update(briefing_companies=sum(bool(s.get('briefing')) for s in briefings),
                  briefing_sentences=sum(len(s.get('briefing', [])) for s in briefings),
                  briefing_short_companies=sum(len(s.get('briefing', [])) < 4 for s in briefings),
                  briefing_unverified_values=0)
    topics=('activity','change','unknown','financial','takeaway')
    result['briefing_topic_coverage']={t:sum(any(s.get('topic')==t for s in b.get('briefing',[])) for b in briefings) for t in topics}
    result['complete_briefing_contracts']=sum(b.get('contract_version')=='r5-S' and all(any(s.get('topic')==t for s in b.get('briefing',[])) for t in topics) for b in briefings)
    result['newer_filing_flags']=sum(bool((b.get('financial_year_check') or {}).get('newer_filing_exists')) for b in briefings)
    if report is not None:
        metrics = json.loads(report.read_text(encoding='utf8'))
        assert metrics['emitted_envelopes'] == len(rows)
        assert metrics['schema_validated'] and metrics['membership_validated']
        if require_clean:
            assert metrics['input_readable'] and not metrics['invalid_inputs'] and not metrics['warnings']
            assert metrics['handled_exceptions'] == metrics['unhandled_exceptions'] == metrics['deadline_hits'] == 0
            assert not metrics['output_limit_exceeded']
            for row in rows:
                sections = row['run']['sections'] if 'run' in row else row['profile']['sections']
                assert all(state in {'available', 'not_available', 'not_applicable'} for state in sections.values()), 'Incomplete smoke-test section'
    if second is not None:
        rerun = load(second)
        for row in rerun:verify_synthesis(row)
        assert len(rerun) == len(rows)
        assert [r["organisation_number"] for r in rerun] == [r["organisation_number"] for r in rows]
        assert ids(rerun) == ids(rows), "Claim IDs differ"
        changes = sum(len((r if "changes" in r else r["profile"])["changes"]) for r in rerun)
        assert changes == 0, f"Changes={changes}"
        observations = sum(len((r['run']['refresh'] if 'run' in r else r['profile']['refresh']).get('observation_changes', [])) for r in rerun)
        assert observations == 0, f'Observation changes={observations}'
        result.update({'rerun_lines': len(rerun), 'identical_claim_ids': True, 'changes': changes, 'observation_changes': observations})
    return result


def main():
    parser = argparse.ArgumentParser(description='Validate membership, envelope schemas and exact stored source evidence')
    parser.add_argument('--first', type=Path, required=True)
    parser.add_argument('--second', type=Path)
    parser.add_argument('--state-dir', type=Path, required=True)
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('--organisations', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--require-clean', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.first, args.state_dir, args.count, args.organisations, args.report, args.require_clean, args.second)))


if __name__ == "__main__":
    main()
