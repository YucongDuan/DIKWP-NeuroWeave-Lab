# Bounded upstream audit and implementation response

**Inspection date:** 27 September 2026. **Owner:** YucongDuan.
**Purpose:** identify actionable obstacles to an executable companion for *A Brief
History of the Brain*, not score a person's research programme or claim an exhaustive
assessment of all their repositories.

## What was actually inspected

Six relevant public repositories were selected. Five were inspected at the recursive
Git-tree level, with available README context. PACT was inspected at repository,
source-directory, and two complete Python-source-file levels. GitHub's connected
repository interface returned the trees and source text. The five archive contents
were not unpacked or executed in this assessment. Network restrictions prevented
local clones and binary archive retrieval. These restrictions are an audit limit,
not evidence that the archives are empty or unusable.

The identifiers below distinguish **tree objects** from **file blobs**. They are not
mislabelled as commit IDs. A future audit should resolve the corresponding commits
and review archive internals before making broader implementation comparisons.

### 1. OmniMemory-OS — repository packaging / documentation scope

Repository: https://github.com/YucongDuan/OmniMemory-OS

Observed recursive tree: `8811996b9e845ef214f3036330af5907cf1d874f`.
The untruncated tree contains `LICENSE`, `README.md`, and
`MESH92-OmniMemory-OS-2026-v1.0.0.zip` (1,452,883 bytes).

Evidence endpoint:
https://api.github.com/repos/YucongDuan/OmniMemory-OS/git/trees/8811996b9e845ef214f3036330af5907cf1d874f

The available README describes purpose-aware memory capsules, provider-bound
budgeting, separate planning/sending, and source-deletion/tombstone propagation.
Those are substantive ideas to retain. This audit does not claim that reconstructive
or deletion-aware memory is absent. The directly observed limitation is that the
implementation is not expanded in the inspected Git tree, making code navigation,
line-level review, and ordinary source-diff workflows less immediate.

**Response in NeuroWeave:** expanded source; a small inspectable dependency engine;
selective invalidation; explicit recomputation; source-history replay; regression tests.
This is a tested companion-specific implementation, not a verified replacement for
all OmniMemory provider adapters or features.

### 2. WorldWeave — repository tree scope

Repository: https://github.com/YucongDuan/WorldWeave

Observed tree: `0c6ff7a6e3441ae62ff59ef20c98ad77b11def44`.
It contains `LICENSE`, `README.md`, and `worldweave_system_v0_9.zip` (62,838 bytes).

Evidence endpoint:
https://api.github.com/repos/YucongDuan/WorldWeave/git/trees/0c6ff7a6e3441ae62ff59ef20c98ad77b11def44

Only the delivery structure is established here. No claim is made about numerical
solvers, tests, world-model quality, or license details inside the archive.

**Response:** directly inspectable finite world models, an explicit observation
interface, intervention controls, and generated result artifacts. No upstream
WorldWeave code was run in a head-to-head experiment.

### 3. DIKWP-NeuroBody-SemanticOS-Platform-Package — tree scope

Repository:
https://github.com/YucongDuan/DIKWP-NeuroBody-SemanticOS-Platform-Package

Observed tree: `cc303795892906a331f7bad2d4f4055898b67dd3`.
It contains `LICENSE`, `README.md`, and
`DIKWP_NeuroBody_SemanticOS_Platform_Package.zip` (351,172 bytes).

Evidence endpoint:
https://api.github.com/repos/YucongDuan/DIKWP-NeuroBody-SemanticOS-Platform-Package/git/trees/cc303795892906a331f7bad2d4f4055898b67dd3

**Response:** a declared resource partition in the book-state runtime, a conservative
resource-accounting exercise, and numerical units specified at each model boundary.
No claim is made that the upstream archive lacks embodiment, resource models, or tests.
The new resource model uses arbitrary units and is not a metabolism or immunity model.

### 4. C-NOESISCOPE — tree scope

Repository: https://github.com/YucongDuan/C-NOESISCOPE

Observed tree: `86103f5f480e1b63b4fe333d7d972821027cc7c9`.
It contains `LICENSE`, `README.md`, and
`DIKWP_MESH64C_NOESISCOPE_v1.0.0_CN_EN.zip` (2,412,409 bytes).

Evidence endpoint:
https://api.github.com/repos/YucongDuan/C-NOESISCOPE/git/trees/86103f5f480e1b63b4fe333d7d972821027cc7c9

**Response:** a transparent exercise with observationally matched dynamical
realizations, an internal lesion, a report-channel lesion, sham handling, and restored
parameters. This supports inspection of functional identifiability, not certification
of consciousness. The internal algorithms or benchmarks of C-NOESISCOPE remain unaudited.

### 5. DIKWP-ProofLedger-OS — tree / README scope

Repository: https://github.com/YucongDuan/DIKWP-ProofLedger-OS

Observed tree: `a9b7729a96de8dabc2a1f5230937d02062afe17c`.
It contains `LICENSE`, `README.md`, and
`dikwp_proofledger_os_open_source_app.zip` (70,183 bytes).

Evidence endpoint:
https://api.github.com/repos/YucongDuan/DIKWP-ProofLedger-OS/git/trees/a9b7729a96de8dabc2a1f5230937d02062afe17c

Its available description distinguishes verification scaffolding from a guarantee of
truth. That boundary is retained, not presented as a newly discovered principle.

**Response:** hash-linked event records and separately retained checkpoints, with
explicit tests for altered payloads, deletion in the middle, and suffix deletion when
an expected head is supplied. These hashes establish consistency relative to a
checkpoint; they do not establish empirical truth or prevent privileged full-log rewriting.

### 6. DIKWP-PACT-v0.1.0 — source-level scope

Repository: https://github.com/YucongDuan/DIKWP-PACT-v0.1.0

The inspected repository has expanded source, tests, schemas, benchmark materials,
and a reproduction script. It must not be characterised as an archive-only concept.
The README describes a paired synthetic benchmark and explicitly limits what its
structured signals demonstrate.

Two complete files were inspected:

`src/dikwp_pact/baselines.py`

Blob ID: `f523a8ab3fbed0fc49f76637128123f23afe36d7`.

Source:
https://github.com/YucongDuan/DIKWP-PACT-v0.1.0/blob/main/src/dikwp_pact/baselines.py

`src/dikwp_pact/scoring.py`

Blob ID: `7ed83ee213f98df937793fa4d42b4b5da985000a`.

Source:
https://github.com/YucongDuan/DIKWP-PACT-v0.1.0/blob/main/src/dikwp_pact/scoring.py

## Source finding A: answer-dependent confidence

In `pact_reference`, the decision is selected from the provided categorical signals.
The returned confidence is 0.94 when that decision equals the scenario's
`expected_decision`, and 0.78 otherwise. Thus the reported confidence depends on
an evaluator answer that would be unavailable during ordinary prediction.

This finding is narrowly about **confidence leakage**. The inspected decision rules
do not use the expected answer to choose the decision, and the inspected aggregate
scorer does not use this confidence field. Therefore it would be incorrect to claim
that this line proves inflated decision accuracy or explains PACT's entire benchmark.

**Implemented response:** `Observation` contains only ID, two cues and their declared
noise levels; `Truth` is a separate type. `predict()` rejects evaluator dictionaries.
Tests flip all labels and verify that prediction probabilities do not change, while
evaluation outcomes do. This is an API/implementation discipline, not a hostile-code
sandbox: malicious Python code in the same process could still seek labels elsewhere.

## Source finding B: conditional accuracy can hide missing cases

The inspected scorer marks missing traces, then builds a `valid` list containing only
returned traces. Decision accuracy is computed over that list. Coverage is reported
separately, but is not included in the displayed weighted composite. Consequently,
a favourable returned subset can retain high conditional metrics while its coverage
is low. Conditional accuracy is not intrinsically invalid; the problem is allowing
it to stand in for complete-task performance without a missingness-sensitive measure.

**Implemented response:** `accuracy_all_cases` uses all declared truth cases as its
denominator, so omissions are failures. `accuracy_observed_only` remains separately
available and is null when no prediction is returned. Coverage and missing count are
explicit. Missing binary Brier predictions receive loss 1. Duplicate prediction IDs,
duplicate truth IDs and unknown returned IDs are rejected instead of silently merged.
There is no unexplained overall score.

## Source finding C: syntactic completeness is not semantic correctness

The inspected PACT scorer measures stage coverage from the presence of stage keys.
Its residual metric checks whether a residual list is nonempty, and its recovery
metric includes the presence of at least two recovery entries. Such measures can be
useful structural checks; they cannot alone establish that a residual is honest,
that a recovery is executable, or that evidence supports an assertion.

**Implemented response:** the companion does not claim to solve unrestricted semantic
verification. It instead narrows each assurance to a behavior actually checked:
dependency sets, exact revision links, rejected stale reads, resource conservation,
consent transitions, numerical expectations and evidence-domain restrictions.
Manual or externally parsed claims still require review.

## Source finding D: preannotated signals constrain the conclusion

The PACT reference is a deterministic policy over supplied categories such as
unauthorised access, purpose drift or corrupted evidence. Correct handling of those
signals is valuable, but does not independently demonstrate that an agent can infer
them from unconstrained language or real-world observations.

**Implemented response:** the cue laboratory computes probabilities from continuous
synthetic observations before truth scoring, while the memory and runtime laboratories
make evidence-state changes executable. However, these models also make strong
assumptions: known noise, manually registered dependencies and declared owners. The
new release does not convert those assumptions into a general intelligence claim.

## What “advance” means in this delivery

The advance is the integration of the book's questions into an exposed, executable,
regression-tested research workflow. The basic numerical methods, provenance ideas,
and explicit authorisation principles are not claimed as newly invented algorithms.
No head-to-head execution of all six upstream systems was possible. No statement of
state-of-the-art accuracy, comprehensive portfolio superiority, independent adoption,
or biological validation follows from this audit.
