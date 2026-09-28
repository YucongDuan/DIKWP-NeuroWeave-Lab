"""Generate the English curriculum manifest; no manuscript text is redistributed."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
titles=[
"Three Histories: Life, Mind, and Self-Discovery",
"Before Neurons: How Life Maintains Itself",
"The Origin of Nervous Systems: From Local Response to Coordination",
"Diverse Brains: Comparative Evolution and Organizational Possibility",
"The Emergence of Humans: Tools, Cooperation, and Cumulative Culture",
"The Brain Across a Lifetime: Development, Learning, and Plasticity",
"Electricity and Chemistry: The Working Language of Nervous Systems",
"Brain and Body: Metabolism, Immunity, Interoception, and Sleep",
"Perceiving the World: Evidence, Attention, and Active Construction",
"The History of Memory: Retention, Reconstruction, and the Future",
"The Direction of Action: Emotion, Value, and Purpose",
"Language and Social Minds: How Meaning Is Jointly Built",
"The Boundaries of Consciousness: Experience, Report, and Testable Theories",
"When Maintenance Fails: Injury, Infection, Degeneration, and Mental Disorders",
"Seeing, Mapping, and Intervening: From Brain Maps to Causal Models",
"From Brain to AI: Semantics, World Models, and Reconstructive Memory",
"Brain-Computer Interfaces: Restoring Channels, Not Speaking for People",
"An Unfinished History: The Open Future of Life, Semantics, and the Brain"]
recipes=[
("evidence", "Evidence Is Not Its Interpretation", "Typed records prevent synthetic results from silently becoming biological validation.","Remove the source kind and ask which claim changes without new measurement.","Record provenance is not source authentication or scientific peer review."),
("homeostasis", "A Body Has a Budget", "A resource-aware controller sustains more completed work than always-work in the specified toy environment.","Increase resource inflow or work cost and compare energy balance and useful work.","Arbitrary resource units are not metabolism, entropy, health advice, or evidence of life."),
("network", "Local Signals, Global Coordination", "Recurrence prolongs activity relative to a finite chain at the same edge gain.","Set the gain to zero in a copy and inspect loss of propagation.","Graph recurrence alone does not explain the evolutionary origin of neurons."),
("network", "Different Architectures, Different Failure Paths", "A lesion changes propagation differently in a chain and cycle.","Move the disabled edge in code; distinguish architecture from organism rankings.","Six-node graphs are neither connectomes nor a ladder of species."),
("context", "The Same Observation, Two Tasks", "An observation-only deterministic policy cannot satisfy two contrary task requirements.","Exchange task labels without changing the observation; inspect the selected action.","The context labels are supplied, not learned cultural understanding."),
("plasticity", "Learning Under a Changing World", "An exponential learner adapts more rapidly to the specified reversal than a cumulative average.","Remove the reversal and compare the cost of fast adaptation.","Two scalar estimators are not a developmental or synaptic plasticity theory."),
("lif", "A Neuron Model You Can Check", "Constant-current spike intervals agree with the analytic LIF expression.","Vary current and recording interval; test subthreshold and suprathreshold cases.","The model does not generate action-potential shape, ion-channel chemistry, or a whole brain."),
("homeostasis", "Rest as a Resource Decision", "A controller can preserve its ability to act by accepting short-term rest.","Compare cumulative work with final resources; neither alone defines success.","This is not a physiological model of sleep, immunity, or interoception."),
("perception", "Reliable Cues, Calibrated Beliefs", "Known cue precision improves Brier loss under the specified Gaussian generator.","Swap cue reliabilities while keeping the prediction interface label-free.","A correctly specified Gaussian model is an assumption, not evidence of universal perception."),
("memory", "Correct the Past Without Inventing It", "A source revision invalidates exactly its dependency descendants and preserves unrelated nodes.","Retract the source after recomputation and attempt to read its descendant.","Dependencies are explicitly registered; the system does not infer them from arbitrary text."),
("purpose", "Change the Goal, Keep the Facts", "A purpose reversal can change actions while the source-state hash stays fixed.","Change only the resource budget and inspect action versus evidence state.","Utility settings are declared engineering choices, not a measure of moral or experiential value."),
("semantics", "Meaning Has Conditions and Owners", "Structured negation and owner fields can be preserved or detectably lost in a transfer.","Drop the negation field and inspect the semantic-difference report.","This is schema-level checking, not an automatic natural-language understanding engine."),
("mechanisms", "Matched Behavior, Different Mechanisms", "Observationally matched realizations diverge under a targeted internal lesion.","Compare sham, workspace lesion, report lesion, and parameter-restored rescue.","Functional discrimination is not a test proving subjective experience."),
("network", "Loss of Output Is Not Loss of Every State", "Disabling an output channel can eliminate reports while leaving a latent proxy unchanged.","Compare internal lesion and output lesion before interpreting silence.","This toy cannot diagnose consciousness, neurological injury, or any medical condition."),
("causal", "Observation Is Not Intervention", "The observational slope differs from the paired do-effect in the confounded structural model.","Set the confounder coefficient gamma to zero and repeat.","The graph and equations are supplied. Causality is not automatically identified from observational data."),
("integrated", "The Book's State Model, Executed", "Purpose changes preserve sources; source revisions trigger dependency repair and changed candidate actions.","Change exactly one of evidence, purpose, consent, or resources; compare state partitions.","This is one finite realization of the book model, not its unique implementation or a brain equation."),
("consent", "Prediction, Confirmation, Execution", "An unconfirmed, revoked, expired, or changed proposal cannot produce even a local execution receipt.","Confirm one payload and attempt to execute a modified message.","Actor names are simulated identities; no real BCI decoder, authenticated person, or actuator is connected."),
("closure", "An Open Future Needs Revisable Claims", "An experiment can record a falsifier and preserve history when its supporting source is withdrawn.","Withdraw the source and verify that an unrelated conclusion is retained.","A complete software loop is not proof of complete scientific explanation.")]
falsifiers=[
"A synthetic-only record is marked sufficient biological validation.",
"Resource-aware completed work does not exceed always-work under the reference environment, or the balance residual is nonzero beyond tolerance.",
"The reference cycle fails to retain more terminal activity than the chain.",
"The specified lesion leaves every relevant propagation trajectory unchanged.",
"An observation-only deterministic policy satisfies both conflicting required actions without extra input.",
"The adaptive estimator fails to reduce post-change prediction MSE in the specified reference reversal.",
"Recorded crossings differ from the constant-current analytic expression beyond floating-point tolerance.",
"Resource conservation fails or the reference recovery policy does not sustain useful work.",
"Mean Brier loss of precision weighting is not lower than equal weighting under the reference Gaussian protocol.",
"A descendant remains readable before repair, an unrelated source changes, or replay differs.",
"Source-state hashes change when only the declared purpose changes, or the specified purpose contrast gives no action difference.",
"A transfer missing negation is marked faithful by the four-field checker.",
"Baseline matching fails, the targeted lesion does not distinguish realizations, or a report lesion silently changes latent state.",
"The report lesion fails to zero report energy or changes the preserved latent trajectory.",
"The paired intervention effect differs from beta under the supplied additive equations.",
"An old plan can be confirmed after purpose/evidence change, or resource/feedback state fails to update after a fresh simulated action.",
"An unconfirmed, modified, reused, revoked or expired candidate obtains a local execution receipt.",
"A withdrawn source regains active descendants without new evidence, or unrelated evidence is lost."]
controls=[
"Incomplete, precise, imprecise, inconsistent and domain-mismatched records",
"Always-work policy with the same disturbances","Chain versus cycle at identical gain",
"Intact and lesioned topologies","Observation-only versus context-preserving policy",
"Cumulative average versus adaptive exponential estimator","Analytic solution and alternate recording intervals",
"Identical resource environment under both policies","Equal-precision and single-cue ablations",
"Unrelated source and retained historical events","Identical facts and a zero-resource case",
"Exact structured transfer versus a missing-negation transfer","Baseline, sham, targeted lesion, report lesion, restored-parameter rescue",
"Intact report with the same latent dynamics","Known analytic slope; gamma=0 comparison available",
"Old plan versus newly reconstructed and confirmed plan","Valid explicitly confirmed local execution",
"Unrelated active source and preserved history"]
chapters=[]
for i,(title,r) in enumerate(zip(titles,recipes),1):
 engine,lab,hypothesis,exercise,limit=r
 chapters.append({"id":f"chapter-{i:02}","chapter":i,"title":title,"lab_title":lab,"engine":engine,
 "hypothesis":hypothesis,"exercise":exercise,"limit":limit,"evidence":"synthetic",
 "falsifier":falsifiers[i-1],"control":controls[i-1],
 "book":"A Brief History of the Brain","authors":["Yucong Duan","Zhongdao Wu"],
 "source_manuscript":"Brain_History_Duan_Wu_Complete_20260927.docx",
 "mapping_status":"English teaching interpretation; not a verbatim manuscript translation"})
(root/'neuroweave/chapters.json').write_text(json.dumps(chapters,indent=2)+'\n')
