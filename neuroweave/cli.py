"""Zero-runtime-dependency command-line interface."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .labs import chapters, run_lab
from .evaluation import benchmark
from .reporting import write_report
from .util import atomic_json, load_json
from .ledger import Ledger


def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(prog="neuroweave",description="Book-linked, synthetic, reproducible brain-inspired laboratories")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("list",help="Show all 18 book-to-lab mappings")
    run=sub.add_parser("run",help="Run one chapter recipe")
    run.add_argument("id");run.add_argument("--seed",type=int,default=17)
    run.add_argument("--parameters",default="{}",help="JSON object; e.g. chapter-07: current_na, dt_ms, duration_ms")
    run.add_argument("--out",default="outputs/run")
    demo=sub.add_parser("demo",help="Run all chapter recipes and the reference benchmark")
    demo.add_argument("--seed",type=int,default=17);demo.add_argument("--out",default="outputs/demo")
    bench=sub.add_parser("benchmark",help="Run 20 paired seeded cue-integration experiments")
    bench.add_argument("--out",default="outputs/benchmark")
    serve=sub.add_parser("serve",help="Open a loopback-only interactive laboratory")
    serve.add_argument("--port",type=int,default=8765)
    verify=sub.add_parser("verify-ledger",help="Verify an existing SQLite event log")
    verify.add_argument("database"); verify.add_argument("--expected-head")
    args=parser.parse_args(argv)
    try:
        if args.command=="list":
            for c in chapters(): print(f'{c["id"]}: {c["lab_title"]}')
        elif args.command=="run":
            result=run_lab(args.id,args.seed,json.loads(args.parameters))
            write_report(args.out,[result])
            print(str(Path(args.out)/"index.html"))
        elif args.command=="demo":
            results=[run_lab(c["id"],args.seed) for c in chapters()]
            b=benchmark();write_report(args.out,results,b)
            print(f"18 recipes and 20-seed benchmark written to {args.out}")
        elif args.command=="benchmark":
            b=benchmark();write_report(args.out,[],b)
            print(json.dumps(b["summary"],indent=2))
        elif args.command=="serve":
            from .server import serve
            serve(args.port)
        elif args.command=="verify-ledger":
            if not Path(args.database).is_file(): raise ValueError("Database does not exist")
            log=Ledger(args.database)
            try: print(log.verify(args.expected_head))
            finally: log.close()
        return 0
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(f"Error: {exc}",file=sys.stderr)
        return 2
