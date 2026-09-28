# DIKWP NeuroWeave Lab

[Online report and project home](https://yucongduan.github.io/DIKWP-NeuroWeave-Lab/) · [Download v1.0.0](https://github.com/YucongDuan/DIKWP-NeuroWeave-Lab/releases/tag/v1.0.0) · [中文入口](README.zh-CN.md) · [Quick start](GETTING_STARTED.md) · [Publication record](PUBLICATION_2026-09-28.md)

## The executable companion to *A Brief History of the Brain*

**Version 1.0.0 · English research release · MIT · Python 3.11+ · Zero third-party runtime dependencies**

Turn a chapter into a prediction, an intervention, a result, and a revisable record.
NeuroWeave combines inspectable numerical experiments with dependency-aware memory,
label-isolated evaluation, purpose-specific planning, and a local consent workflow.
The book is by **Yucong Duan and Zhongdao Wu**. This is newly generated companion
software, not a claim that either author has reviewed or manually implemented it.

## Start here

Open `outputs/reference/index.html` to inspect the already-computed English report.
This file is an offline snapshot, not a simulation running in the browser.

From this extracted project directory:

```bash
python -m neuroweave list
python -m neuroweave run chapter-10 --out outputs/my-memory-lab
python -m neuroweave serve --port 8765
```

Then open `http://127.0.0.1:8765`. Select a chapter, run it, inspect the protocol
hash and results, and export JSON. No API key, model download, cloud account,
JavaScript build tool, or `pip install` is needed to run from source.
On Windows, `py -3` can replace `python` when that is the installed launcher.

```bash
# All 18 chapter recipes plus a paired, 20-seed benchmark
python -m neuroweave demo --out outputs/my-demo

# Regression tests, fresh artifacts, and comparison with supplied reference JSON
python scripts/reproduce.py --out outputs/reproduced

# Direct test invocation
python -m unittest discover -s tests -v

# Example numerical experiment
python -m neuroweave run chapter-07 --parameters '{"current_na":0.25}'
```

Shell JSON quoting differs between terminals. The browser parameter editor avoids
that issue. Python API examples are in `examples/`.

## What is implemented

| Capability | Actual implementation | Entry point |
|---|---|---|
| Chapter laboratories | 18 recipes sharing named, inspectable engines | `neuroweave/labs.py` |
| Numerical mechanisms | Exact constant-current LIF, Gaussian cue integration, graph propagation, resource accounting, online adaptation, a known confounded SCM, matched dynamical realizations | `models.py`, `evaluation.py` |
| Reconstructive memory | Typed source records, explicitly registered dependency DAG, revisions, selective invalidation, explicit recomputation, withdrawal, persistent replay | `memory.py`, `ledger.py` |
| Unified book state | O/E/K/V/P/B partitions; plans pinned to evidence, purpose revision and resources; confirmation; local synthetic feedback | `runtime.py` |
| Purpose and consent | Candidate / confirmation / revocation / expiry / single-use local execution | `purpose.py` |
| Evidence discipline | Missing, inconsistent, imprecise and non-comparable records remain distinct | `evidence.py` |
| Evaluation | Label-free prediction type; all-case denominators; missing-loss penalty; duplicate/unknown-ID rejection; calibration bins and paired bootstrap intervals | `evaluation.py` |
| Interfaces | English local web app, CLI, Python API, self-contained HTML and JSON reports | `server.py`, `cli.py`, `reporting.py` |

There are **18 chapter recipes**, not 18 independent biophysical simulators. Several
recipes reuse one mechanism to teach a different question. No whole-brain model,
clinical efficacy, subjective experience, or universal DIKWP superiority is asserted.

## Why this is more than another renamed repository

The bounded upstream review found useful ideas worth retaining, and specific
engineering/evaluation gaps worth addressing. It does **not** say that Yucong Duan's
entire portfolio lacks implementations or tests.

- Five inspected repository trees deliver their implementation primarily inside ZIP
  archives. This release exposes all new source, tests and reproduction scripts directly.
- In the inspected PACT reference baseline, confidence depends on `expected_decision`.
  NeuroWeave's predictor receives an `Observation` without a truth field.
- PACT's inspected scorer excludes missing traces from conditional accuracy and its
  weighted score. Here, all-case accuracy and coverage are separate, and missing Brier
  predictions receive the maximum binary loss of 1.
- Structured trace fields are not treated as proof of correct semantic content. Here,
  explicit DAG dependencies, numerical checks and state-transition tests check actual behavior.
- Evidence, purpose and execution are coupled through a state signature: a plan cannot
  be confirmed after its evidence or purpose has changed.

See `docs/UPSTREAM_AUDIT.md` for exact files, blob/tree identifiers, audit scope,
qualifications, and source links. Archive internals were **not** reviewed or executed.

## Evidence produced by this release

`validation/TEST_RECEIPT.json` records the actual local test run.
`outputs/reference/benchmark.json` contains the protocol, seed-level results,
confidence intervals and limitations, not just a headline score.
`SHA256SUMS` permits checking delivered bytes; it is not a trusted digital signature.

The benchmark uses 20 seeded synthetic runs with 240 cases each. All models receive
the same cue fields, including the known reliabilities. The correctly specified
precision-weighted model is expected to do well by construction. This is an auditable
model check and evaluation example, **not** an independent comparison against upstream
repositories, commercial models, people, or biological brains.

## Documentation

Read `docs/HANDBOOK.md` or the accompanying `NeuroWeave_English_Handbook.pdf` for
architecture, mathematics, the complete chapter curriculum, API examples, experiments,
source-level audit findings, and limitations. Additional focused guides:

- `docs/UPSTREAM_AUDIT.md`, `docs/BOOK_TO_CODE.md`, `docs/REPRODUCIBILITY.md`
- `docs/DATA_CARD.md`, `docs/MODEL_CARD.md`, `SECURITY.md`, `CONTRIBUTING.md`
- `examples/reconstructive_memory.py`, `examples/unified_runtime.py`

## Release boundary

This is a local single-user research and teaching system. Only synthetic records are
bundled. There is no human-data ingestion pipeline, EEG/BCI decoder, real actuator,
authenticated patient identity, external LLM integration, autonomous internet agent,
or remote deployment. Identity labels in consent demonstrations are not authentication.
Persistent memory replay is implemented; consent and pending plans are session-local.

The new source and original accompanying documentation are provided under MIT.
The manuscript itself and upstream code archives are not redistributed. This package
is published with source, versioned downloads and a static report website. The complete Python runtime remains local.
