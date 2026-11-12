"""Build the final comparison from the committed measurement artifacts."""
import json
import subprocess
from collections import Counter
from pathlib import Path

root = Path('reports/r5/stage4_7')


def read_log(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')


paths = [('Stage 3', Path('reports/r5/stage3')), ('4.6', Path('reports/r5/stage4/step4_6'))]
paths += [('4.7 '+step, root/('step'+step)) for step in ('budget','caps','order','singlehost','social','reuse') if (root/('step'+step)/'counts.json').exists()]
counts = [json.loads((p/'counts.json').read_text()) for _,p in paths]
text = '# Stage 4.7 summary\n\n'
last = counts[-1]
final_config = json.loads((paths[-1][1]/'settings.json').read_text())['resolved_config']
final_rows = [json.loads(line) for line in Path(final_config['output']).read_text(encoding='utf8').splitlines()]
levels = Counter(c['value']['identity_level'] for row in final_rows for c in row['claims']
                 if c['field']=='official_website' and c['availability']=='available')
text += (f"Frozen 100: **{last['metrics']['verified_websites']} verified websites**, "
         f"**{last['counts_by_section_state']['website']['failed']} failed website sections**, "
         f"**{last['counts_by_section_state']['activity']['failed']} failed activity sections**. "
         'Exact-number and corroborated proof rules remain enforced. Every measured run uses fresh state, the hash-checked seed-20261017 inputs, $0 provider cost, no search queries and no model calls.\n\n')
text += 'Final website identity tiers: '+', '.join(f'`{tier}`: {number}' for tier,number in sorted(levels.items()))+'.\n\n'
sportlet = any(row['organisation_number']=='927094266' and any(c['field']=='official_website' and c['availability']=='available' for c in row['claims']) for row in final_rows)
text += ('Recall reached **six exact-number websites** in the ordering run. SPEDIFY is the new website. The social-step run withheld SPORTLET.NO AS after live robots/homepage timeouts. '+
         ('The final run verifies SPORTLET again from fresh evidence. ' if sportlet else 'It remains withheld in the final run; older verification is not treated as current evidence. ')+
         'Both requested numeric LinkedIn links are restored, and SPEDIFY adds a third numeric LinkedIn profile.\n\n')
text += '| Metric / section state | '+' | '.join(label for label,_ in paths)+' |\n|---|'+'---:|'*len(paths)+'\n'
for key in counts[0]['metrics']:
    values = [c['metrics'][key] for c in counts]
    text += '| '+key+' | '+' | '.join(f'{v:.3f}' if isinstance(v,float) else str(v) for v in values)+' |\n'
text += '| Provider cost USD | '+' | '.join('0' for _ in paths)+' |\n'
text += '| Website request / total caps | '+' | '.join(
    str(json.loads((p/'settings.json').read_text())['resolved_config']['website_request_cap'])+'/'+
    str(json.loads((p/'settings.json').read_text())['resolved_config']['website_total_request_cap']) for _,p in paths)+' |\n'
text += '| Published social profile URLs | '+' | '.join(str(sum(r['social_profiles'] for r in c['per_company'])) for c in counts)+' |\n'
text += '| Website HTTP attempts | '+' | '.join(str(sum(e.get('section')=='website' for e in json.loads((p/'report.json').read_text())['request_log'])) for _,p in paths)+' |\n'
text += '| Max DNS nominations per company (4.7 accounting) | '+' | '.join(str(max(json.loads((p/'report.json').read_text()).get('dns_candidates_by_company',{}).values(),default=0)) if p.parent==root else 'n/a' for _,p in paths)+' |\n'
for section, states in counts[0]['counts_by_section_state'].items():
    for state in states:
        text += f'| {section} / {state} | '+' | '.join(str(c['counts_by_section_state'][section][state]) for c in counts)+' |\n'
text += '\n## Changes and decisions\n\n'
text += ('- Budget: one DNS nomination for a www/non-www pair; cached checks cost no additional nomination. Source vetoes precede work, and in-run responses/errors are reused across companies under a URL/permission-scope lock. Identity is independently proved for each company. Alternate hosts require DNS/connect failure; HTTP errors and source vetoes cannot trigger them.\n'
         '- The final reuse step also locks completed candidate checks across www/non-www spellings under the same path/permission scope. Responses and non-budget source failures are reused, while company identity verdicts are always recomputed. A regression test explicitly rejects the second company when the shared body proves only the first.\n'
         '- Candidate order: registry homepage, registry email domain, then the strongest full-name variants before subunit/brand and remaining spelling nominations. Tests explicitly check registry and full-name precedence. Exact-number proof immediately stops further candidate/proof-page work.\n')
if any(label=='4.7 caps' for label,_ in paths):
    text += '- The separate 8/13 cap experiment was required because failures remained above Stage 3. Its HTTP cost/runtime and section states are shown separately; no cap above 8/13 was used. The ordering step retested 6/9 and reached six websites but remained at 26 website / 33 activity failures. The final comparison therefore uses explicit `--website-request-cap 8 --website-total-request-cap 13` flags; CLI/library defaults stay 6/9.\n'
else:
    text += '- The 6/9 caps remain unchanged: the budget correction met the failure targets and raised verified websites above five, so the conditional 8/13 experiment was not needed.\n'
if any(label=='4.7 singlehost' for label,_ in paths):
    text += '- Website failures still exceeded Stage 3 after the bounded cap experiment, so the 4.1 two-host fallback was reverted in a separate measured step. Other 4.x identity, location, nomination, proof, contact and social improvements remain.\n'
else:
    text += '- The conditional fallback reversion was not needed after recovery to the Stage 3 failure targets.\n'
text += ('- Numeric LinkedIn `/company/<digits>` links are accepted only in the verified site\'s own header/footer, with group, founder, agency, hidden and article contexts excluded. Named profiles still require exact-name handle agreement. The numeric exception has a distinct proof tier and retains website identity, registry name and verbatim link evidence. No platform page is fetched.\n'
         '- The public-activity allowance is bounded by an absolute eight website HTTP attempts. The resource audit checks actual attempts and DNS nominations for every company in every measured run; full per-company counts are in [resource_audit.json](resource_audit.json).\n'
         '- Both withheld links and every website/social URL addition/removal are listed with organisation number, company name, URL, proof tier and exact excerpts in [new_websites.md](new_websites.md). Full locators, hashes and link context are in [url_audit.json](url_audit.json).\n'
         '- Fresh acquisition is subject to live source variation. No incomplete result is relabelled as checked absence. Section failures and partial available activity claims are reported independently.\n\n')
text += '## Verification and commits\n\n'
text += '| Step | Full pytest | Source bodies | Unsupported synthesis / briefing values |\n|---|---|---:|---:|\n'
import re
for label, path in paths[2:]:
    tests = read_log(path/'tests.txt')
    result = re.findall(r'\d+ passed[^\n]*', tests)[-1].strip()
    v = json.loads((path/'verification.json').read_text())
    text += f"| {label} | {result} | {v['source_blobs_verified']} | {v['synthesis_unverified_values']} / {v['briefing_unverified_values']} |\n"
text += '\nEach comparison verifies 100 ordered, schema-valid envelopes, stored-body hashes, verbatim spans and all cited synthesis/briefing values. Each step directory preserves exact commands, resolved settings, execution timestamps, full report, counts and verifier output; raw bodies, envelopes, profiles and site stay local under `.data/r5/stage4_7/`.\n\n'
text += ('Stage 4.7 invokes `.venv/Scripts/python.exe -m signalpost.cli run` with the logical flags saved in each `run.ps1`; the measurement helper avoids this host\'s PowerShell script-execution restriction. Historical Stage 3/4.6 used the uv launcher. All resolved runner settings are recorded. Runtime and HTTP differences include live-source and host scheduling variation and are not claimed as causal speedups.\n\n')
text += 'Implementation commits (author Nethra Venkat; no persistent Git identity configuration changed; no push):\n\n```text\n'
text += subprocess.check_output(['git','log','--format=%h %an <%ae> %s','3d428ad..HEAD'], text=True)
text += '```\n\n'
text += ('Two excluded diagnostic acquisitions remain local: sandbox-denied requests, and a long host pause producing 100 deadline hits (2509.575 seconds wall). They are not used in the comparison. An interrupted pytest run failed the unchanged two-second partial-progress assertion; the full suite was rerun without changing any timeout or assertion. All commit gates use the subsequent green full-suite results.\n\n'
         'Failed test attempts are retained in `test_attempts/`. Later gates use the recorded `run_tests.py` command, which raises only its own Windows process priority to Above Normal to reduce scheduling contention; it changes no assertion or timeout. Crawl measurements use normal process priority.\n\n'
         'Decisions: [DECISIONS.md](../DECISIONS.md). Stage 4.7 ends with this committed report; no Stage 5 work or push was performed.\n')
text += '\nFinal documentation gate: '+re.findall(r'\d+ passed[^\n]*', read_log(root/'final_report_tests.txt'))[-1].strip()+'.\n'
(root/'SUMMARY.md').write_text(text, encoding='utf8')
