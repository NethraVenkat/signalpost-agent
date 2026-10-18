import argparse
import asyncio
import json
import sys
from pathlib import Path
from .config import Config
from .runner import run


def main():
    parser = argparse.ArgumentParser(prog="signalpost")
    sub = parser.add_subparsers(dest="command", required=True)
    site = sub.add_parser('site', help='Build offline searchable company profiles')
    site.add_argument('--input', type=Path, required=True)
    site.add_argument('--out', type=Path, required=True)
    site.add_argument('--title', default='Signalpost')
    command = sub.add_parser("run", help="Write a terminal result for every supplied company")
    for flag in ("organisations", "output", "report"):
        command.add_argument("--" + flag, type=Path, required=True)
    for flag in ("bulk", "previous"):
        command.add_argument("--" + flag, type=Path)
    command.add_argument("--state-dir", type=Path, default=Path("state"))
    command.add_argument('--verify-bulk', action='store_true',
                         help='Require an API identity check even on bulk hits; never fall back to CSV on verification failure')
    command.add_argument('--site-dir', type=Path)
    command.add_argument('--profiles-output', type=Path, help='Write kit-compatible raw profiles from the same verified claims')
    command.add_argument("--envelope-shape", choices=("union", "contract", "reference"), default="union")
    command.add_argument("--emit-duplicates", action="store_true", default=True)
    command.add_argument('--deduplicate', dest='emit_duplicates', action='store_false')
    command.add_argument("--websites", action="store_true")
    command.add_argument('--no-dns-precheck', dest='dns_precheck', action='store_false')
    command.add_argument('--no-website-stop-after-verified', dest='website_stop_after_verified', action='store_false')
    command.add_argument('--no-nav-rank-candidates', dest='nav_rank_candidates', action='store_false')
    command.add_argument('--public-activity', action='store_true')
    command.add_argument('--registry-changes', action=argparse.BooleanOptionalAction, default=True,
                         help='Publish narrowly verified registry changes (default on; disable with --no-registry-changes)')
    command.add_argument('--registry-declared', action='store_true', help='Enable the default-off weak registry-declared website path')
    command.add_argument("--website-request-cap", type=int, default=6)
    command.add_argument('--website-total-request-cap',type=int,default=9)
    command.add_argument('--hiring',action='store_true')
    command.add_argument('--nav-index-path',type=Path)
    command.add_argument('--nav-index-max-age-days',type=float,default=21)
    command.add_argument('--allow-system-sleep',dest='prevent_system_sleep',action='store_false',default=True)
    command.add_argument('--search-max-queries',type=int)
    command.add_argument('--search-max-cost-usd',type=float,default=5.)
    command.add_argument('--search-unit-price-usd',type=float,default=.005)
    command.add_argument('--synthesis',choices=('auto','template','llm'),default='template')
    command.add_argument('--llm-max-calls',type=int,default=100)
    command.add_argument('--llm-max-cost-usd',type=float,default=.50)
    for flag,kind,default in [('nav-max-pages',int,512),('nav-max-details',int,None),('nav-time-cap-seconds',float,None),('nav-lookback-days',int,185),('nav-concurrency',int,4),('nav-request-timeout',float,30),('nav-body-cap-mb',float,2)]:
        command.add_argument('--'+flag,type=kind,default=default)
    command.add_argument("--website-user-agent", default="SignalpostAgent/1.0 (+https://github.com/NethraVenkat/signalpost-agent)")
    command.add_argument("--expected-count", type=int)
    command.add_argument("--run-id", default="")
    for flag, kind, default in (("max-requests", int, None), ("time-budget-seconds", float, 2400),
                               ("deadline-fraction", float, .85), ("max-cost-usd", float, 0),
                               ("host-concurrency", int, 10), ("workers", int, 64), ("request-timeout", float, 10),
                               ("official-batch-size", int, 1100), ("max-output-mb", float, 256)):
        command.add_argument("--" + flag, type=kind, default=default)
    args = vars(parser.parse_args())
    action = args.pop("command")
    try:
        if action == 'site':
            from .site import generate_site
            print(json.dumps(generate_site(args['input'], args['out'], args['title'])))
            return 0
        config = Config(**args)
        resolved = [p.resolve() for p in (config.output, config.report, config.profiles_output) if p]
        temporary = [p.with_name(p.name+'.tmp').resolve() for p in (config.output,config.profiles_output) if p]
        protected = [p.resolve() for p in (config.organisations, config.bulk, config.previous) if p]
        targets=resolved+temporary
        if len(targets) != len(set(targets)) or any(p in protected for p in targets):
            raise ValueError("Output/report must not overwrite each other or input sources")
        report = asyncio.run(run(config))
        print(json.dumps({k: report[k] for k in ("emitted_envelopes", "invalid_inputs", "requests", "runtime_ms", "changes",'observation_changes', "deadline_hits", "warnings")}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"signalpost could not produce output: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

