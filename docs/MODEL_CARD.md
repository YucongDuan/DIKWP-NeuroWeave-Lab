# Model and system card

## Intended use

Teaching and inspecting finite implementations of reconstructive memory, context
sufficiency, purpose-conditioned action, synthetic perception, causal intervention,
and experimental accountability. All interfaces and authored documentation are English.
The companion is associated with the manuscript by Yucong Duan and Zhongdao Wu;
publication, endorsement, independent evaluation and author code review are not asserted.

## Implemented capabilities

The source contains numerical toy mechanisms, explicit dependency-graph reconstruction,
a SQLite event log, a state-pinned local planning runtime, consent simulations, strict
benchmark accounting, a browser UI, CLI and reproducible reports. Actual verification
is recorded in `validation/`, rather than inferred from a README badge.

## Explicit limitations

No whole-brain reconstruction, electrophysiological parameter fitting, actual EEG/MEG
analysis, neuromodulation, diagnosis, clinical decision support, authenticated human
consent, model training pipeline, LLM adapter, vector retrieval engine, automatic
ontology extraction or real actuator is implemented. Memory relations are registered
by code or a trusted adapter; text similarity cannot substitute for missing provenance.

The runtime shares a process with its models. Label isolation and authority boundaries
are enforced by the provided APIs/tests, not a adversarial sandbox. The HTTP app is
single-user and loopback-only. The ledger scales poorly for very large histories:
verification scans the event chain and descendant invalidation scans registered nodes.
The consent session is not persistent, and resource/receipt/feedback updates are not
one distributed transaction. These limitations are documented instead of hidden by
an operating-system or autonomous-agent label.

## Evaluation interpretation

Numerical tests concern finite equations. Benchmarks concern one public synthetic
family. Matched dynamical realizations differ under an internal lesion by construction;
this is an identifiability exercise, not a validated consciousness theory. Functional
performance, inspectability and evidence of subjective experience are not equivalent.
The system does not score whether a person or artificial system is conscious.

## Extension boundary

A new integration requires actual adapters, independent data rights, validation,
identity/authentication appropriate to the use case, resource controls and new tests.
An empty interface or future design is not a delivered feature. Use explicit named
variants to report architecture changes without implying universal scientific progress.
