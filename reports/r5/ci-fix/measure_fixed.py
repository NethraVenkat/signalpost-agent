"""Local equivalent of the corrected CI commands, using isolated state."""
import json,os,subprocess,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]


def main():
    attempt=sys.argv[1];assert attempt.isalnum()
    dest=ROOT/'reports/r5/ci-fix'/attempt;dest.mkdir(exist_ok=False)
    work=ROOT/'.data/r5'/('ci-seven-'+attempt);work.mkdir(exist_ok=False)
    env=os.environ.copy();env.update(SIGNALPOST_SEARCH_PROVIDER='disabled',SIGNALPOST_SEARCH_MOCK='0',PYTHONUTF8='1')
    flags={'organisations':ROOT/'tests/fixtures/ci20.jsonl','bulk':ROOT/'tests/fixtures/ci20.csv',
        'output':work/'envelopes.jsonl','profiles-output':work/'profiles.jsonl','report':work/'report.json',
        'run-id':'ci-seven-'+attempt,'expected-count':20}
    argv=['uv','run','--project',str(ROOT),'signalpost','run']
    for k,v in flags.items():argv+=['--'+k,str(v)]
    began=time.perf_counter()
    with (dest/'process.txt').open('w',encoding='utf8') as log:r=subprocess.run(argv,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
    (dest/'execution.json').write_text(json.dumps({'argv':argv,'cwd':str(work),'exit_code':r.returncode,
        'wall_seconds':time.perf_counter()-began,'platform':'Local Windows; GitHub Linux execution not performed'},indent=2)+'\n')
    r.check_returncode()
    check=['uv','run','python','scripts/check_live_run.py','--output',str(work/'envelopes.jsonl'),
        '--organisations','tests/fixtures/ci20.jsonl','--count','20','--state',str(work/'state'),
        '--report',str(work/'report.json'),'--site',str(work/'site')]
    with (dest/'verification.json').open('w',encoding='utf8') as log:v=subprocess.run(check,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
    (dest/'verification-command.json').write_text(json.dumps({'argv':check,'exit_code':v.returncode},indent=2)+'\n')
    (dest/'report.json').write_bytes((work/'report.json').read_bytes());v.check_returncode()


if __name__=='__main__':main()
