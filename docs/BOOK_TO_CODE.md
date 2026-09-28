# Book-to-code traceability

Book: A Brief History of the Brain, by Yucong Duan and Zhongdao Wu. Manuscript: Brain_History_Duan_Wu_Complete_20260927.docx. All mappings below are original English teaching interpretations.

## Chapter 01 — Three Histories: Life, Mind, and Self-Discovery

Recipe `chapter-01` uses `evidence` in `neuroweave/labs.py`.

Typed records prevent synthetic results from silently becoming biological validation.

Inspect the distinct incomplete, imprecise and inconsistent outputs. Then inspect biological_claim and experience_claim: provenance organisation can reveal an unsupported promotion of evidence without claiming to settle the underlying scientific question. Suggested extension: add a record with a different observation time and show why it cannot be silently merged.

Boundary: Record provenance is not source authentication or scientific peer review.

## Chapter 02 — Before Neurons: How Life Maintains Itself

Recipe `chapter-02` uses `homeostasis` in `neuroweave/labs.py`.

A resource-aware controller sustains more completed work than always-work in the specified toy environment.

Compare useful completed work, not only terminal resource. The always-work policy can consume its initial budget rapidly and then remain unable to complete work. The resource-aware policy accepts recovery steps. Check that final resource equals initial resource plus inflow minus actual expenditure to numerical tolerance.

Boundary: Arbitrary resource units are not metabolism, entropy, health advice, or evidence of life.

## Chapter 03 — The Origin of Nervous Systems: From Local Response to Coordination

Recipe `chapter-03` uses `network` in `neuroweave/labs.py`.

Recurrence prolongs activity relative to a finite chain at the same edge gain.

Observe the total activity trajectory in both graph topologies. A chain eventually loses its initial signal because no edge returns it to an earlier node. A cycle can preserve a decaying circulation. Its persistence is a property of the specified edge dynamics, not an assertion of awareness or biological coordination.

Boundary: Graph recurrence alone does not explain the evolutionary origin of neurons.

## Chapter 04 — Diverse Brains: Comparative Evolution and Organizational Possibility

Recipe `chapter-04` uses `network` in `neuroweave/labs.py`.

A lesion changes propagation differently in a chain and cycle.

Read the intact and lesioned structures together. A visible change in topology can alter when activity disappears, but a particular output difference does not identify every possible internal mechanism. Modify the disabled target in models.network() and keep the original as a named comparison instead of silently replacing the reference.

Boundary: Six-node graphs are neither connectomes nor a ladder of species.

## Chapter 05 — The Emergence of Humans: Tools, Cooperation, and Cumulative Culture

Recipe `chapter-05` uses `context` in `neuroweave/labs.py`.

An observation-only deterministic policy cannot satisfy two contrary task requirements.

The two records deliberately have the same observation string. The correct actions differ only because the task conditions differ. The observation-only witness gets one of two correct. This is a finite proof example, not an empirical claim that all non-DIKWP architectures fail contextual tasks.

Boundary: The context labels are supplied, not learned cultural understanding.

## Chapter 06 — The Brain Across a Lifetime: Development, Learning, and Plasticity

Recipe `chapter-06` uses `plasticity` in `neuroweave/labs.py`.

An exponential learner adapts more rapidly to the specified reversal than a cumulative average.

The default world reverses midway through the run. Read post_change_prediction_mse alongside the trajectory, and verify that predictions are scored before the next observation is used for an update. A stable-world variant can expose the noise sensitivity of the faster estimator; such a variant should have its own protocol name.

Boundary: Two scalar estimators are not a developmental or synaptic plasticity theory.

## Chapter 07 — Electricity and Chemistry: The Working Language of Nervous Systems

Recipe `chapter-07` uses `lif` in `neuroweave/labs.py`.

Constant-current spike intervals agree with the analytic LIF expression.

Run current_na=0.1 for a subthreshold example and current_na=0.2 for a spiking example. Compare dt_ms=0.3 with dt_ms=0.8: recording density changes while the analytic crossing times remain equal up to floating-point tolerance. This is stronger verification than merely plotting an oscillating line.

Boundary: The model does not generate action-potential shape, ion-channel chemistry, or a whole brain.

## Chapter 08 — Brain and Body: Metabolism, Immunity, Interoception, and Sleep

Recipe `chapter-08` uses `homeostasis` in `neuroweave/labs.py`.

A controller can preserve its ability to act by accepting short-term rest.

Reuse the resource engine to ask a different question: when can rest preserve future capacity to act? Compare the path of the budget with cumulative useful work. The numerical result is not a prescription about human rest, sleep duration or illness. It is an explicit demonstration of a resource-constrained policy trade-off.

Boundary: This is not a physiological model of sleep, immunity, or interoception.

## Chapter 09 — Perceiving the World: Evidence, Attention, and Active Construction

Recipe `chapter-09` uses `perception` in `neuroweave/labs.py`.

Known cue precision improves Brier loss under the specified Gaussian generator.

Inspect the Observation examples and verify that labels are absent. The full label set belongs to scoring. The separate 20-seed benchmark alternates which cue is reliable, so the one-cue ablation cannot always rely on the same favourable channel. The known reliabilities remain a declared modelling advantage.

Boundary: A correctly specified Gaussian model is an assumption, not evidence of universal perception.

## Chapter 10 — The History of Memory: Retention, Reconstruction, and the Future

Recipe `chapter-10` uses `memory` in `neuroweave/labs.py`.

A source revision invalidates exactly its dependency descendants and preserves unrelated nodes.

Run the default correction from 6 to 2, then use corrected_source=8. The same dependency mechanism should compute a different resulting flag because the new evidence differs. A successful repair process is not defined as always lowering confidence or always rejecting a conclusion; it applies the registered rule to the current supported state.

Boundary: Dependencies are explicitly registered; the system does not infer them from arbitrary text.

## Chapter 11 — The Direction of Action: Emotion, Value, and Purpose

Recipe `chapter-11` uses `purpose` in `neuroweave/labs.py`.

A purpose reversal can change actions while the source-state hash stays fixed.

Compare the source-state hashes before and after switching from explore to preserve. They remain identical while the toy action differs. Then inspect zero_budget_action. Resource limits and utility priorities can change behavior without rewriting the observation into a more convenient fact.

Boundary: Utility settings are declared engineering choices, not a measure of moral or experiential value.

## Chapter 12 — Language and Social Minds: How Meaning Is Jointly Built

Recipe `chapter-12` uses `semantics` in `neuroweave/labs.py`.

Structured negation and owner fields can be preserved or detectably lost in a transfer.

The communication record carries owner, action, negation and context. Its lossy transfer drops negation and is marked unfaithful. The checker verifies these four schema fields only. It does not parse free-form language or infer that a person's fluently predicted sentence has been authorised by that person.

Boundary: This is schema-level checking, not an automatic natural-language understanding engine.

## Chapter 13 — The Boundaries of Consciousness: Experience, Report, and Testable Theories

Recipe `chapter-13` uses `mechanisms` in `neuroweave/labs.py`.

Observationally matched realizations diverge under a targeted internal lesion.

Inspect every condition for both realizations, not only the row with the largest effect. Baseline matching makes the intervention informative under the supplied construction. Report-channel loss and recurrence loss have different internal consequences. The appropriate conclusion is about these functional mappings, not subjective experience.

Boundary: Functional discrimination is not a test proving subjective experience.

## Chapter 14 — When Maintenance Fails: Injury, Infection, Degeneration, and Mental Disorders

Recipe `chapter-14` uses `network` in `neuroweave/labs.py`.

Disabling an output channel can eliminate reports while leaving a latent proxy unchanged.

The output-loss example has report energy zero and a nonzero latent proxy. This prevents one particular modelling error: equating absent output with absence of every internal variable. It supplies no clinical diagnostic rule and cannot be used to classify an unresponsive patient or a real artificial system.

Boundary: This toy cannot diagnose consciousness, neurological injury, or any medical condition.

## Chapter 15 — Seeing, Mapping, and Intervening: From Brain Maps to Causal Models

Recipe `chapter-15` uses `causal` in `neuroweave/labs.py`.

The observational slope differs from the paired do-effect in the confounded structural model.

Use beta and gamma to separate the structural effect from the confounding contribution. Increasing n reduces sampling fluctuation in the observational slope; it does not remove confounding. The paired do-effect is exact under this additive synthetic construction, not an achievement of recovering an unknown causal graph.

Boundary: The graph and equations are supplied. Causality is not automatically identified from observational data.

## Chapter 16 — From Brain to AI: Semantics, World Models, and Reconstructive Memory

Recipe `chapter-16` uses `integrated` in `neuroweave/labs.py`.

Purpose changes preserve sources; source revisions trigger dependency repair and changed candidate actions.

This is the integrated demonstration. It proposes a plan, changes purpose and rejects the old plan; proposes again, corrects evidence and rejects that plan; reconstructs the dependency graph, creates and confirms a fresh plan, then records synthetic feedback and a resource debit. Inspect each O/E/K/V/P/B snapshot rather than only the final receipt.

Boundary: This is one finite realization of the book model, not its unique implementation or a brain equation.

## Chapter 17 — Brain-Computer Interfaces: Restoring Channels, Not Speaking for People

Recipe `chapter-17` uses `consent` in `neuroweave/labs.py`.

An unconfirmed, revoked, expired, or changed proposal cannot produce even a local execution receipt.

The demonstration rejects five cases: missing confirmation, changed message, reuse after execution, revocation and expiration. It then exhibits a valid local receipt with external_side_effect=false. Owner labels are declarations inside the process, so this is a consent-protocol teaching model rather than a real identity system.

Boundary: Actor names are simulated identities; no real BCI decoder, authenticated person, or actuator is connected.

## Chapter 18 — An Unfinished History: The Open Future of Life, Semantics, and the Brain

Recipe `chapter-18` uses `closure` in `neuroweave/labs.py`.

An experiment can record a falsifier and preserve history when its supporting source is withdrawn.

Withdraw the source and inspect the reopened claim and stale descendants. The unrelated source remains usable. A withdrawal is not deletion: the log still records how the old conclusion arose. The exercise ends with revisable evidence and a preserved audit trail, not with a claim that the whole scientific question has been closed.

Boundary: A complete software loop is not proof of complete scientific explanation.
