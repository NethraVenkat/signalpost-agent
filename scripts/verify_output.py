"""Independent saved-output checks; never rewrites an envelope to pass a gate."""
import argparse
import sys
import hashlib
import json
import csv,io
from functools import lru_cache
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
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


def verify_careers(row,data,evidence,stored_body):
    from signalpost.web.careers import postings,links,target
    from signalpost.web.html import Page
    from signalpost.web.policy import domain
    from signalpost.web.social import shared_group_context
    from datetime import datetime
    claims={c['id']:c for c in data['claims']}
    for claim in data['claims']:
        value=claim.get('value')
        if claim['availability']=='available' and claim['field'].startswith('hiring.job.') and isinstance(value,dict) and value.get('source')!='verified_site_careers':
            receipt=next(evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']=='signalpost.nav.v1' and evidence[eid]['locator']=='/ad_content')
            document=json.loads(stored_body(receipt['content_sha256']))
            ad=document['ad_content']
            assert document['status']=='ACTIVE' and document['uuid']==ad['uuid']==value['uuid']
            assert ad['title']==value['title'] and ad['published']==value['published'] and ad['expires']==value['expires']
            employer=str(ad['employer']['orgnr']);assert employer==value['employer_orgnr']
            scopes={row['organisation_number']}|{str(c['value']['organisation_number']) for c in data['claims'] if c['family']=='subunits' and c['availability']=='available' and isinstance(c['value'],dict) and c['value'].get('organisation_number')}
            assert employer in scopes,'Job has no proven employer relationship'
            from signalpost.sources.nav import timestamp
            assert timestamp(value['expires'])>timestamp(receipt['retrieved_at'])>=timestamp(value['published'])
        if claim['availability']!='available' or not isinstance(value,dict) or value.get('source')!='verified_site_careers':continue
        proof=claims[value['identity_claim_id']]
        assert proof['field']=='official_website' and proof['availability']=='available' and not proof['carried_forward']
        assert proof['value']['identity_level']=='VERIFIED' and proof['value'].get('relationship_note')!='group_site'
        root=domain(proof['value']['final_url'])
        receipts=[evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']=='signalpost.careers.v1']
        posting=next(e for e in receipts if e['locator']=='JobPosting/title')
        assert posting['source_url']==value['url']
        text=stored_body(posting['content_sha256'])
        page=Page(text.encode('utf8'),posting['source_url'],text=text)
        found=postings(page,row['organisation_number'],datetime.fromisoformat(posting['retrieved_at'].replace('Z','+00:00')))
        assert any(all(value.get(k)==v for k,v in parsed.items()) for parsed,spans in found),'Unsupported careers posting values'
        chain=sorted((e for e in receipts if e['locator'].startswith('careers/link/')),key=lambda e:int(e['locator'].rsplit('/',1)[1]))
        assert 1<=len(chain)<=2
        expected=None
        for depth,receipt in enumerate(chain):
            text=stored_body(receipt['content_sha256'])
            parent=Page(text.encode('utf8'),receipt['source_url'],text=text)
            assert not shared_group_context(parent)
            if depth==0:
                assert domain(parent.url)==root
                allowed=links(parent,root)
            else:
                assert parent.url==expected
                allowed=[(link,url) for link in parent.links if (url:=target(link.href,root)) and domain(url)==domain(parent.url)]
            next_url=chain[depth+1]['source_url'] if depth+1<len(chain) else value['url']
            assert any(url==next_url and link.span==receipt['claim_span'] for link,url in allowed),'Missing own careers link'
            expected=next_url


def verify_exact_public(row,data,evidence,stored_body):
    from signalpost.sources.exact_public import lei_record,parent_record,ted_xml,GLEIF,METHOD
    from datetime import datetime
    count=0
    for claim in data['claims']:
        if claim['family'] not in {'gleif','procurement'} or claim['availability']!='available':continue
        receipts=[evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']==METHOD]
        assert receipts,'Missing exact-ID source receipt'
        org=row['organisation_number'];value=claim['value'];matched=False
        for receipt in receipts:
            url=receipt['source_url'];body=stored_body(receipt['content_sha256'])
            if claim['field']=='gleif.record':
                assert url.startswith(GLEIF+'lei-records?')
                document=json.loads(body)
                matched |= any(lei_record(item,org)==value for item in document['data'])
            elif claim['field'].startswith('gleif.parent.'):
                kind=claim['field'].rsplit('.',1)[-1];child=value['child_lei']
                parent_identity=next(c for c in data['claims'] if c['field']=='gleif.record' and c['availability']=='available')
                assert parent_identity['value']['lei']==child
                assert set(parent_identity['evidence_ids'])<=set(claim['evidence_ids'])
                if url==GLEIF+'lei-records/'+child+'/'+kind+'-parent-relationship':
                    matched |= parent_record(json.loads(body)['data'],child,kind)==value
            elif claim['field'].startswith('procurement.award.'):
                assert url=='https://ted.europa.eu/en/notice/'+value['notice_id']+'/xml'
                at=datetime.fromisoformat(receipt['retrieved_at'].replace('Z','+00:00'))
                matched |= value in ted_xml(body.encode('utf8'),org,value['notice_id'],at)
            else:raise AssertionError('Unknown public exact-ID claim')
        assert matched,'Unsupported GLEIF/TED value or attribution'
        count+=1
    return count


def bundled_match(eo,bundle_path,derive,claim,receipt,body,org,row):
    """The receipt body must be one exact bundled record of this org, from the named source."""
    from datetime import datetime
    bundle=eo.load_bundle(bundle_path)
    if body not in bundle['records'].get(org,[]):return False
    record=json.loads(body);meta=eo.bundled_sources(bundle)[record['source']]
    if receipt['source_url']!=meta['source_url'] or receipt['retrieved_at']!=meta['retrieved_at']:return False
    completed=(row.get('run') or {}).get('completed_at') or row.get('completed_at') or meta['retrieved_at']
    derived=derive(record,org,datetime.fromisoformat(completed.replace('Z','+00:00')))
    if not derived:return False
    value,_=derived
    record_id=value.get('project_id') or value.get('inspection_id')
    return value==claim['value'] and claim['field'].endswith('.'+record['source']+'.'+str(record_id))


def verify_exact_official(row,data,evidence,stored_body):
    """Stage S: re-derive every exact-ID official claim from its saved source record."""
    from signalpost.sources import exact_official as eo
    from datetime import datetime
    count=0
    org=row['organisation_number']
    for claim in data['claims']:
        if claim['family'] not in eo.FAMILIES or claim['availability']!='available':continue
        receipts=[evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']==eo.METHOD]
        assert receipts,'Missing exact-ID official receipt'
        value=claim['value'];matched=False
        assert value.get('company_orgnr')==org,'Official record is not attributed to this company'
        for receipt in receipts:
            body=stored_body(receipt['content_sha256'])
            at=datetime.fromisoformat(receipt['retrieved_at'].replace('Z','+00:00'))
            if claim['field'].startswith('state_aid.award.'):
                assert receipt['source_url'].startswith(eo.STOTTE+'?'),'Wrong state-aid endpoint'
                items=json.loads(body)['stoettetildeling']
                index=int(receipt['locator'].split('/')[2])
                award=eo.state_aid_award(items[index],org,at)
                matched |= bool(award) and award[0]==value and claim['field']=='state_aid.award.'+value['award_id']
            elif claim['field'].startswith('licences.'):
                assert receipt['source_url']==eo.ft_entity_url(value['registry_entity_id']),'Wrong Finanstilsynet record'
                entities=json.loads(body)['legalEntities']
                assert len(entities)==1
                matched |= any('licences.'+key==claim['field'] and found==value for key,found,_ in eo.licence_values(entities[0],org))
            elif claim['field'].startswith('research.project.'):
                matched |= bundled_match(eo,eo.RESEARCH_BUNDLE,eo.research_value,claim,receipt,body,org,row)
            else:raise AssertionError('Unknown exact-ID official claim')
        assert matched,'Unsupported exact-ID official value or attribution'
        count+=1
    return count


def verify_filing_years(row,data,evidence,stored_body):
    from signalpost.sources.accounts_years import YEARS
    checked=0
    for claim in data['claims']:
        if claim['availability']!='available' or not claim['field'].startswith(('accounts.filed_years','accounts.filed_year.')):continue
        source=next(evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']=='signalpost.accounts_years.v1')
        assert source['source_url']==YEARS.format(org=row['organisation_number']),'Wrong entity filing-years endpoint'
        values=json.loads(stored_body(source['content_sha256']))
        assert isinstance(values,list) and all(isinstance(y,str) and len(y)==4 and y.isascii() and y.isdigit() for y in values)
        if claim['field']=='accounts.filed_years':
            assert claim['value']==sorted(set(values),reverse=True),'Filing year list differs from official source'
        else:
            assert source['locator'].startswith('/')
            actual=values[int(source['locator'][1:])]
            assert claim['value']==actual and claim['field']=='accounts.filed_year.'+actual,'Unsupported filed year'
        assert claim.get('reporting_period') is None
        checked+=1
    return checked


def verify_financial_sources(row, data, evidence, stored_body):
    raw=(row.get('run',{}).get('synthesis') or data.get('synthesis') or {})
    if raw.get('contract_version')!='r5-S': return 0,0
    claims={c['id']:c for c in data['claims']}
    documents={};checked=0
    for c in data['claims']:
        if c['family']!='accounts' or c['availability']!='available' or c['field'].startswith(('accounts.filed_years','accounts.filed_year.')):continue
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
        assert p.get('unit')==record.get('enhet'), 'Unsupported financial unit'
        checked+=1
    for m in raw.get('financial_metrics',[]):
        a,b=[claims[cid] for cid in m['input_claim_ids']]
        pa,pb=a['reporting_period'],b['reporting_period']
        assert a['availability']==b['availability']=='available'
        assert pa['account_type']==pb['account_type']=='SELSKAP'
        assert pa.get('currency') and all(pa.get(k)==pb.get(k) for k in ('currency','unit','account_type'))
        def refs(c):
            import re
            return {(evidence[eid]['source_url'],evidence[eid]['content_sha256'],evidence[eid]['locator'].split('/')[1])
                    for eid in c['evidence_ids'] if re.match(r'^/[0-9]+/',evidence[eid]['locator'])
                    and evidence[eid]['source_url']=='https://data.brreg.no/regnskapsregisteret/regnskap/'+row['organisation_number']
                    and evidence[eid]['extraction_method']=='signalpost.registry.v1'}
        top,bottom=Decimal(str(a['value'])),Decimal(str(b['value']))
        assert top.is_finite() and bottom.is_finite() and bottom>0
        if m['formula']=='revenue_yoy':
            if pa.get('unit') is None:assert {x[0] for x in refs(a)} & {x[0] for x in refs(b)},'Missing units from incompatible source schemas'
            assert a['field']=='accounts.revenue' and b['field'].startswith('accounts.history.') and b['field'].endswith('.revenue')
            sa,ea,sb,eb=[date.fromisoformat(p[k]) for p,k in [(pa,'period_start'),(pa,'period_end'),(pb,'period_start'),(pb,'period_end')]]
            assert ea.year==eb.year+1 and sa.year==sb.year+1 and eb<sa
            assert (sa.month,sa.day,ea.month,ea.day)==(sb.month,sb.day,eb.month,eb.day)
            assert 350 <= (ea-sa).days+1 <=366 and 350 <= (eb-sb).days+1 <=366
            top-=bottom
        else:
            assert refs(a)&refs(b),'Ratio inputs are not from the same statement'
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
        assert registered['field'] in {'identity.latest_submitted_accounts','accounts.filed_years'}
        if registered['field']=='accounts.filed_years':
            verify_filing_years(row,data,evidence,stored_body)
            assert max(registered['value'])==year['registry_year'],'Filing-year comparison differs from source'
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
    all_events=[c for c in data['claims'] if c['availability']=='available' and c['field'].startswith('registry_change.')]
    assert len(all_events)<=50,'Shared registry/role event cap exceeded'
    from signalpost.sources import role_changes
    from signalpost.sources.http import Response
    for claim in all_events:
        if not claim['field'].startswith('registry_change.roles.'):continue
        source=next(evidence[eid] for eid in claim['evidence_ids'] if evidence[eid]['extraction_method']==role_changes.METHOD)
        assert source['source_url'].startswith(role_changes.ENDPOINT+'?'),'Unapproved role-update source'
        raw=document(source['content_sha256'])
        for token in source['locator'].strip('/').split('/'):raw=raw[int(token)] if isinstance(raw,list) else raw[token]
        response=Response(stored_body(source['content_sha256']).encode('utf8'),200,source['source_url'],source['retrieved_at'],source['content_sha256'])
        expected=role_changes.extract(raw,response,source['locator'],row['organisation_number'])
        assert expected.claims[0].value==claim['value'],'Unsupported role-change event frame'
        assert claim['value']['role_type'] is None and claim['value']['person_name'] is None
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
    return len(all_events)


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
    from signalpost.sources.exact_public import briefing_sentences
    assert len(synthesis.briefing) <= 6+len(briefing_sentences(envelope)), 'Briefing exceeds cited frame bound'
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
    financial_inputs=derived_metrics=registry_events=filing_year_facts=0
    registry_documents={}
    exact_public=0
    exact_official=0
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
        verify_careers(row,data,evidence,stored_body)
        exact_public+=verify_exact_public(row,data,evidence,stored_body)
        exact_official+=verify_exact_official(row,data,evidence,stored_body)
        from signalpost.public_names import verify as verify_public_names
        verify_public_names(row['organisation_number'],data,evidence,stored_body)
        from scripts.verify_publisher_identity import verify as verify_publisher
        verify_publisher(row['organisation_number'],data,evidence,stored_body)
        from scripts.verify_legal_pdf import verify as verify_pdf
        verify_pdf(row['organisation_number'],data,evidence,stored_body,lambda sha:(state_dir/'blobs'/sha).read_bytes())
        from scripts.verify_owner_social import verify as verify_owner_social
        verify_owner_social(row['organisation_number'],data,evidence,stored_body)
        filing_year_facts+=verify_filing_years(row,data,evidence,stored_body)
    result = {"lines": len(rows), "schema_valid": True, "published_claims": published, "source_blobs_verified": len(seen)}
    result.update(synthesis_companies=synthesis_companies,synthesis_sentences=synthesis_sentences,synthesis_unverified_values=0)
    result.update(financial_inputs_verified=financial_inputs,derived_financial_metrics_verified=derived_metrics)
    result['registry_events_verified']=registry_events
    result['filing_year_facts_verified']=filing_year_facts
    result['exact_public_items_verified']=exact_public
    result['exact_official_items_verified']=exact_official
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
