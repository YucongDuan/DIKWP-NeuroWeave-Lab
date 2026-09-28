# Data card

All bundled experimental observations are synthetic. No patient data, neural recording,
BCI stream, private messages, manuscript full text, or copied upstream data archive is
included. Chapter titles are English teaching interpretations of the identified book.

## Cue experiment

Each case uses a balanced binary label with Gaussian class means -1 and +1. Two cues
are drawn conditionally independently given that label. Their standard deviations are
0.45 and 2.0. In the reference benchmark their roles alternate by case. Labels are
stored in evaluator-only `Truth` objects; the predictor receives numerical cues and
the declared noise levels, not the label. `generate()` lives in the evaluator module;
this is logical API separation rather than operating-system process isolation.

Reference seeds: 1000 through 1019 inclusive. Cases per seed: 240. These are public
reproduction seeds, not a blinded holdout. Default chapter illustrations use seed 17.
No training, hyperparameter search, human study, or model selection occurred. The
likelihood assumptions match the precision-weighted predictor, so low loss is expected
under the supplied generator and does not demonstrate superiority outside it.

## Other records

Memory, purpose, communication and source-conflict examples use invented identifiers
and values. A resource unit is a toy budget unit, not joules or a clinical measurement.
The LIF model has explicit ms/mV/nA/MOhm units. Its parameters are illustrative, not
estimated from a biological experiment. The structural causal model supplies its own
graph and exogenous noise; it is not inferred from an observational human dataset.

## Bias, dependence and retention

The case generator covers only two Gaussian classes. It cannot represent ordinary
language, sensor drift, adversarial measurement, social context or biological diversity.
Paired models share each generated case. Bootstrap sampling is over seed-level metrics,
not individual correlated outputs of one run. Source groups in the evidence checker
are declarations, not verified evidence of independent measurements.

The ledger retains old source values by design. Retraction removes a record's authority
for current derivation but is not deletion or anonymisation. Do not add sensitive records
without a separate lawful collection, retention, access and deletion architecture.
