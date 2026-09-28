"""Self-contained offline report: escaped data, no active external resources."""
from __future__ import annotations
from html import escape
import json
from pathlib import Path
from .util import atomic_json


def write_report(out: str | Path, results: list[dict], benchmark_result: dict | None=None) -> None:
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    sections=[]
    for r in results:
        c=r["chapter"]
        atomic_json(out/(c["id"]+".json"),r)
        sections.append(f'<section id="{c["id"]}"><p class="eyebrow">CHAPTER {c["chapter"]:02d} / {escape(c["engine"])}</p><h2>{escape(c["lab_title"])}</h2><p>{escape(c["title"])}</p><p><b>Prediction:</b> {escape(c["hypothesis"])}</p><p><b>Experiment:</b> {escape(c["exercise"])}</p><p class="limit"><b>Boundary:</b> {escape(c["limit"])}</p><p class="hash">Protocol SHA-256: {r["protocol_hash"]}</p><details><summary>Inspect actual result JSON</summary><pre>{escape(json.dumps(r["result"],indent=2))}</pre></details></section>')
    if benchmark_result is not None:
        atomic_json(out/"benchmark.json",benchmark_result)
        rows=''.join(f'<tr><td>{escape(m)}</td><td>{s["mean"]:.6f}</td><td>{s["ci95_percentile"][0]:.6f} to {s["ci95_percentile"][1]:.6f}</td></tr>' for m,s in benchmark_result["summary"].items())
        sections.insert(0,'<section><p class="eyebrow">PAIRED MULTI-SEED EXPERIMENT</p><h2>Perception benchmark</h2><p>Lower Brier loss is better. Each interval resamples independent seeded runs, not correlated time steps. All data are synthetic; no external superiority claim is made.</p><table><tr><th>Model</th><th>Mean Brier</th><th>95% bootstrap interval</th></tr>'+rows+'</table><p>Every model receives the same cue fields. Known Gaussian noise matches the precision-weighted formula by design. Missing predictions receive loss 1.</p></section>')
    nav=''.join(f'<a href="#{r["chapter"]["id"]}">{r["chapter"]["chapter"]:02}</a>' for r in results)
    text='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NeuroWeave | Reproducible Research Report</title><style>
body{margin:0;background:#edf2f5;color:#142b3a;font:17px/1.65 system-ui,sans-serif}header{background:#122c3c;color:white;padding:70px max(6vw,24px)}main{max-width:1060px;margin:auto;padding:32px 20px}h1{font-size:clamp(32px,5vw,58px);line-height:1.1;max-width:900px}h2{font-size:28px;line-height:1.3}.eyebrow{letter-spacing:.16em;font-size:12px;font-weight:750;color:#198d82}header .eyebrow{color:#8ee3ca}section{background:white;border:1px solid #dce5ec;border-radius:12px;padding:32px;margin:24px 0}nav a{display:inline-block;padding:6px 12px;margin:4px;background:#fff;border-radius:5px;color:#163c4d;text-decoration:none}.limit{border-left:4px solid #ba8740;padding:12px;background:#fff7eb}.hash{font:12px monospace;overflow-wrap:anywhere}pre{font:12px/1.6 monospace;overflow:auto;max-height:600px;background:#f4f7fa;padding:20px}summary{cursor:pointer;font-weight:700}td,th{text-align:left;padding:12px;border-bottom:1px solid #ddd}table{width:100%;font-size:14px}footer{padding:30px;text-align:center;font-size:13px}
</style><header><p class="eyebrow">DIKWP NEUROWEAVE LAB / 1.0.0</p><h1>From ideas about the brain<br>to experiments you can inspect.</h1><p>Executable companion to <i>A Brief History of the Brain</i><br>Book authors: Yucong Duan and Zhongdao Wu</p><p>Offline result snapshot. Use the local Python app to change parameters and rerun.</p></header><main><nav>'''+nav+'</nav>'+''.join(sections)+'''</main><footer>Original English teaching software. Synthetic evidence only. No manuscript full text, external tracker, or cloud dependency is embedded.</footer></html>'''
    (out/"index.html").write_text(text,encoding="utf-8")
