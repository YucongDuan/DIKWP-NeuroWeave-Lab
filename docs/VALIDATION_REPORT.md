# NeuroWeave validation report

Version 1.0.0 | 27 September 2026

## Executed software checks

**155 tests passed, zero failures and zero errors.** The actual unittest run took
3.730 seconds on Python 3.13.5, Linux-6.18.44-x86_64-with-glibc2.41.
The raw transcript and structured receipt are included under validation/.

A fresh execution produced **19 of 19 reference JSON artifacts identical**, with zero
mismatches: 18 chapter recipes plus the benchmark. Both Python examples also ran.
There are 14 core Python files comprising 1220 lines;
comments and docstrings are included in this line count. This is not a quality score.

The suite checks label isolation, duplicate/unknown IDs, missing predictions, exact
memory descendants, source-history retention, replay, stale writers, stale action
plans, resource debit, consent transitions, numerical solutions, HTTP input controls,
CLI behavior, and deterministic chapter artifacts.

## Browser smoke checks

Eight interaction/layout checks completed in Chromium 144.0.7559.96, with no JavaScript
page errors. The exact delivered UI assets were loaded in memory. A Python HTTP relay
sent requests to the real local HTTP server and numerical engine. Direct browser
navigation to the loopback URL was blocked by container administrator policy and
**was not verified**. The delivered app uses ordinary native fetch, not this relay.
See UI_RECEIPT.json, screenshots, and the optional browser fixture for precise scope.

## Reference cue benchmark

20 public seeded runs, 240 cases per run, 4,800 synthetic cases total. Three model
prediction sets are scored on the same cases. All predictors receive the same cue
fields, including known noise scales; the ablations intentionally ignore some fields.

| Model | Mean Brier loss | Seed-bootstrap 95% interval |
|---|---:|---:|
| precision_weighted | 0.00822883 | 0.00658528 to 0.00980858 |
| equal_precision | 0.12478559 | 0.11537809 to 0.13395977 |
| cue_a_only | 0.10512248 | 0.09960828 to 0.10979809 |

Precision-minus-equal paired mean difference: **-0.11655676**.
95% seed-bootstrap interval: **-0.12573653 to -0.10705566**.
Each interval uses 1,500 resamples of independent seeded-run summaries. Smaller Brier
loss is better. Missing predictions receive loss 1 and remain in the denominator.

This is a check of a correctly specified Gaussian model under its own disclosed
generator, not a blinded study, learned general capability, energy-matched architecture
comparison, or head-to-head benchmark against upstream repositories or biological brains.
No claim of subjective experience or clinical validation follows from these results.

## Release and document checks

The English handbook contains approximately 7,300 words and 26 A4 pages. It was rendered
with ReportLab and inspected using Poppler image output. The UI desktop and mobile
screenshots were inspected; the 390-pixel viewport had no horizontal overflow.
All listed release bytes can be checked with scripts/verify_release.py. Checksums are
not author authentication. No remote GitHub CI job, repository publication, or public
website deployment was performed by generating this package.
