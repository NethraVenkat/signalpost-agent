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
    command = sub.add_parser("run", help="Write a terminal result for every supplied company")
    for flag in ("organisations", "output", "report"):
        command.add_argument("--" + flag, type=Path, required=True)
    for flag in ("bulk", "previous"):
        command.add_argument("--" + flag, type=Path)
    command.add_argument("--state-dir", type=Path, default=Path("state"))
    command.add_argument("--envelope-shape", choices=("union", "contract", "reference"), default="union")
    command.add_argument("--emit-duplicates", action="store_true")
    command.add_argument("--websites", action="store_true")
    command.add_argument("--website-request-cap", type=int, default=6)
    command.add_argument('--website-total-request-cap',type=int,default=9)
    command.add_argument('--hiring',action='store_true')
    for flag,kind,default in [('nav-max-pages',int,512),('nav-max-details',int,300),('nav-time-cap-seconds',float,300),('nav-lookback-days',int,185),('nav-concurrency',int,8),('nav-request-timeout',float,30),('nav-body-cap-mb',float,2)]:
        command.add_argument('--'+flag,type=kind,default=default)
    command.add_argument("--website-user-agent", default="SignalpostAgent/1.0 (+https://github.com/NethraVenkat/signalpost-agent)")
    command.add_argument("--expected-count", type=int)
    command.add_argument("--run-id", default="")
    for flag, kind, default in (("max-requests", int, 8000), ("time-budget-seconds", float, 1800),
                               ("deadline-fraction", float, .85), ("max-cost-usd", float, 0),
                               ("host-concurrency", int, 10), ("workers", int, 64), ("request-timeout", float, 10),
                               ("official-batch-size", int, 1100), ("max-output-mb", float, 64)):
        command.add_argument("--" + flag, type=kind, default=default)
    args = vars(parser.parse_args())
    args.pop("command")
    try:
        config = Config(**args)
        resolved = [config.output.resolve(), config.report.resolve()]
        protected = [p.resolve() for p in (config.organisations, config.bulk, config.previous) if p]
        if resolved[0] == resolved[1] or any(p in protected for p in resolved):
            raise ValueError("Output/report must not overwrite each other or input sources")
        report = asyncio.run(run(config))
        print(json.dumps({k: report[k] for k in ("emitted_envelopes", "invalid_inputs", "requests", "runtime_ms", "changes",'observation_changes', "deadline_hits", "warnings")}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"signalpost could not produce output: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
