# Reproducibility and evidence trail

## Reference artifacts

`outputs/reference/` contains JSON results for 18 chapters, `benchmark.json`, and a
standalone HTML report. They were computed by the delivered Python code; they are not
handwritten illustrations of hoped-for results. Protocol and result SHA-256 fields
permit checking exactly which configuration produced a particular artifact.

`validation/TEST_RECEIPT.json` and `validation/tests.txt` record the actual local
regression suite. `validation/REPRODUCTION_RECEIPT.json` records a fresh comparison.
`validation/UI_RECEIPT.json`, when present, records the separately performed browser
smoke test and its actual status. Tests do not become biological or clinical evidence.

## Repeat the complete workflow

From the extracted root, use:

```bash
python scripts/verify_release.py
python -m unittest discover -s tests -v
python scripts/reproduce.py --out outputs/reproduced
```

The reproduction script first invokes the standard-library test runner. It then runs
all 18 chapter recipes with seed 17, the 20-seed cue benchmark, and compares the 19
JSON artifacts with the supplied reference. Its output folder receives the fresh HTML,
JSON, raw test transcript and reproduction receipt. A reference mismatch returns
nonzero; deliberate scientific changes require a new protocol version and explanation.

The exact reference interpreter and platform are in the receipt. Source syntax targets
Python 3.11+. A GitHub Actions matrix for Python 3.11/3.12/3.13 on Linux and Windows is
supplied, but remote CI was not executed merely by creating this package. Floating-point
and pseudorandom-library differences in other environments should be investigated;
matching a single checksum is not a general portability proof.

## Statistical protocol

The benchmark protocol is constructed and hashed before case generation or prediction.
This is a local configuration commitment, not an independent preregistration or trusted
time stamp. Models see identical observation fields. Their full prediction lists are
created before the scorer is called; no answer labels are arguments to `predict()`.
Hashing prediction lists provides a record, not external proof of when they were made.

For each seed and model, compute all-case accuracy, missingness, coverage and Brier
loss. A missing prediction receives binary Brier loss 1. Probability bins describe
only returned predictions and explicitly state that denominator. Mean Brier loss is
summarised across 20 runs. Percentile intervals use 1,500 seeded bootstrap resamples of
those 20 seed-level values. The paired difference resamples the 20 per-seed differences.
No p-value, multiple-comparison discovery, human effect size, or universal score is claimed.

## Scope of fairness

All three cue models receive the same cue fields, including known reliabilities. The
one-cue ablation deliberately ignores one field. This is parity of available input,
not equality of wall time, number of arithmetic operations, power consumption or energy.
The reference does not benchmark upstream executables, closed models, or human subjects.
The book's recommendation to compare compute-matched architectures remains an important
requirement for a broader empirical study, not a feature fabricated by this release.

## Publishing without hiding the source

Create a repository only under an authorised account, then commit the extracted project
contents at its root. Keep source and tests expanded; a release ZIP is additional
convenience, not a substitute. Update CITATION.cff with confirmed implementation
contributors and a real repository URL. Do not invent a DOI, endorsement or maintainer.
After CI actually runs, preserve its link and results with the tagged version.

Generating this delivery did not publish a GitHub repository, create a release, deploy
a website, or change any upstream file. No token or account credential is included.

## Optional documentation and browser fixtures

The runtime and default regression suite need no third-party packages. Regenerating
the formatted PDF is an optional developer step using ReportLab and locally installed
DejaVu fonts: `python scripts/render_handbook_pdf.py`. No font files are redistributed.
The Markdown handbook and HTML report remain directly readable without those tools.

`scripts/browser_smoke_relay.py` is an optional Playwright/Chromium fixture. In the
delivery environment, direct Chromium navigation to a loopback URL was blocked by
administrator policy. The fixture loads the exact UI assets into the browser and
relays fetch calls through Python HTTPConnection to the real local HTTP server. This
checks interaction, rendered results, export and responsive layout, but does not verify
native browser networking or claim an ordinary direct-browser end-to-end test.
The delivered app itself uses native fetch and does not contain the test relay.
