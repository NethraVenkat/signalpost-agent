"""Fail on invalid published output, not honest live-source unavailability."""
import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.verify_output import verify,load
from signalpost.io.input_adapter import read
from signalpost.budget import HTTP_PER_100,SECONDS_PER_100
from signalpost.site import PROFILE_HTML_LIMIT


def check(output,organisations,state,report_path,site,count):
    output,organisations,state,report_path,site=map(Path,(output,organisations,state,report_path,site))
    result=verify(output,state,count,organisations,report_path)
    rows=load(output);report=json.loads(report_path.read_text(encoding='utf8'))
    inputs=read(organisations)
    assert report['input_readable'] and not inputs.invalid,'Invalid/unreadable smoke inputs'
    assert not report['output_limit_exceeded'],'Output was reduced by a size limit'
    assert report['unhandled_exceptions']==0,'Unhandled application exception'
    assert report['total_cost_usd']==0,'Nonzero provider cost'
    assert report['requests']<=HTTP_PER_100*len(inputs.unique)//100,'Hard HTTP budget exceeded'
    assert report['completion']['wall_seconds']<=SECONDS_PER_100*len(inputs.unique)/100,'Hard time budget exceeded'
    assert report['completion']['within_effective_time_budget'],'Effective time budget exceeded'
    assert report['site']['state']=='available','Site was not generated'
    assert report['site']['companies']==len(inputs.unique),'Site membership count differs'
    assert (site/'index.html').is_file() and (site/'compare.html').is_file(),'Missing site entry pages'
    profiles = {path.stem: path.stat().st_size for path in (site/'c').glob('*.html')}
    assert profiles.keys() == set(inputs.unique), 'Missing/extra company site pages'
    largest = max(profiles.values(), default=0)
    assert largest < PROFILE_HTML_LIMIT, 'Profile HTML exceeds the 250,000-byte cap'
    assert report['site']['largest_profile_bytes'] == largest, 'Largest profile size differs from run report'
    for row in rows:
        assert row['run']['terminal_status'] in {'completed','failed'},'Nonterminal envelope'
        data=row if 'claims' in row else row['profile']
        assert not any(e['code']=='not_started' for e in data['errors']),'Unfinished section placeholder'
    assert result['complete_briefing_contracts']==count,'Incomplete cited briefing topics'
    assert result['synthesis_unverified_values']==result['briefing_unverified_values']==0
    result.update(site_verified=True,terminal_envelopes=count,source_failures_permitted=True,
        http_requests=report['requests'],wall_seconds=report['completion']['wall_seconds'],cost_usd=0,
        largest_profile_bytes=largest)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('output','organisations','state','report','site'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--count',type=int,required=True)
    a=p.parse_args();print(json.dumps(check(a.output,a.organisations,a.state,a.report,a.site,a.count)))


if __name__=='__main__':main()
