"""Run the regression suite, rerun all artifacts, and compare reference JSON.

Standard library only. Exact comparisons concern the same code/parameters and
compatible Python behavior; the manifest states the actually tested interpreter.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from neuroweave.labs import chapters, run_lab
from neuroweave.evaluation import benchmark
from neuroweave.reporting import write_report
from neuroweave.util import atomic_json, digest, load_json


def main() -> int:
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='outputs/reproduced');args=parser.parse_args()
    out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    test=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,capture_output=True,text=True)
    (out/'tests.txt').write_text(test.stdout+test.stderr,encoding='utf-8')
    if test.returncode:
        print(test.stdout+test.stderr);return test.returncode
    results=[run_lab(c['id'],17) for c in chapters()]
    b=benchmark();write_report(out,results,b)
    mismatches=[];comparisons=[]
    expected=[c['id']+'.json' for c in chapters()]+['benchmark.json']
    for name in expected:
        p=out/name;reference=ROOT/'outputs/reference'/name
        if not p.exists() or not reference.exists():
            mismatches.append(name)
            comparisons.append({'file':name,'equal':False,'reason':'Required result or reference is missing'})
            continue
        same=load_json(p)==load_json(reference)
        comparisons.append({'file':name,'equal':same,'result_hash':digest(load_json(p))})
        if not same:mismatches.append(name)
    receipt={'python':platform.python_version(),'platform':platform.platform(),'tests_exit_code':test.returncode,
             'reference_json_files_compared':len(comparisons),'comparisons':comparisons,'mismatches':mismatches,
             'elapsed_seconds':round(time.perf_counter()-start,3),'external_validation':False}
    atomic_json(out/'reproduction_receipt.json',receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k!='comparisons'},indent=2))
    return 1 if mismatches else 0

if __name__=='__main__':raise SystemExit(main())
