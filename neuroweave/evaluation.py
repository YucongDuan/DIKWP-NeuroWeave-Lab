"""Label-isolated predictions and denominator-explicit benchmark scoring."""
from __future__ import annotations
from dataclasses import dataclass
import math
import random
import statistics
from .models import sigmoid
from .util import finite, integer, nonempty, digest


@dataclass(frozen=True, slots=True)
class Observation:
    id: str
    cue_a: float
    cue_b: float
    sigma_a: float
    sigma_b: float

    def __post_init__(self) -> None:
        nonempty(self.id, "observation id")
        for key in ("cue_a","cue_b"):
            finite(getattr(self,key),key)
        for key in ("sigma_a","sigma_b"):
            finite(getattr(self,key),key,minimum=.01,maximum=100)


@dataclass(frozen=True, slots=True)
class Prediction:
    id: str
    probability: float
    def __post_init__(self) -> None:
        nonempty(self.id, "prediction id")
        finite(self.probability, "probability", minimum=0, maximum=1)


@dataclass(frozen=True, slots=True)
class Truth:
    id: str
    label: int
    def __post_init__(self) -> None:
        nonempty(self.id, "truth id")
        integer(self.label,"label",0,1)


def predict(observation: Observation, model: str) -> Prediction:
    if not isinstance(observation, Observation):
        raise TypeError("Predictor accepts Observation, not an evaluator record")
    if model == "precision_weighted":
        log_odds = 2*observation.cue_a/observation.sigma_a**2 + 2*observation.cue_b/observation.sigma_b**2
    elif model == "equal_precision":
        log_odds = 2*(observation.cue_a+observation.cue_b)
    elif model == "cue_a_only":
        log_odds = 2*observation.cue_a/observation.sigma_a**2
    else:
        raise ValueError("Unknown model")
    return Prediction(observation.id, sigmoid(log_odds))


def generate(seed: int, n: int = 240, *, shifted: bool = False) -> tuple[list[Observation],list[Truth]]:
    integer(seed,"seed",0,2**31-1); integer(n,"n",1,100000)
    rng = random.Random(seed)
    observations, labels = [], []
    for i in range(n):
        label = int(rng.random() < .5)
        mean = 2*label-1
        sa, sb = (.45, 2.0) if not shifted or i % 2 == 0 else (2.0,.45)
        id = f"s{seed}-c{i}"
        observations.append(Observation(id,rng.gauss(mean,sa),rng.gauss(mean,sb),sa,sb))
        labels.append(Truth(id,label))
    return observations, labels


def score(truths: list[Truth], predictions: list[Prediction]) -> dict:
    if not truths:
        raise ValueError("Evaluation needs at least one case")
    labels = {t.id:t.label for t in truths}
    by_id = {p.id:p.probability for p in predictions}
    if len(labels) != len(truths) or len(by_id) != len(predictions):
        raise ValueError("Duplicate truth or prediction ID")
    if set(by_id)-set(labels):
        raise ValueError("Predictions contain unknown case IDs")
    correct = sum(int((p >= .5) == labels[id]) for id,p in by_id.items())
    missing = len(labels)-len(by_id)
    brier = (sum((p-labels[id])**2 for id,p in by_id.items())+missing)/len(labels)
    bins = []
    for b in range(10):
        rows = [(p,labels[id]) for id,p in by_id.items() if min(9,int(p*10)) == b]
        bins.append({"bin":b,"n":len(rows),"mean_probability": statistics.mean(x for x,_ in rows) if rows else None,
                     "positive_fraction": statistics.mean(y for _,y in rows) if rows else None})
    return {"n_total":len(labels),"n_predicted":len(by_id),"n_missing":missing,
            "coverage":len(by_id)/len(labels),"accuracy_all_cases":correct/len(labels),
            "accuracy_observed_only":correct/len(by_id) if by_id else None,
            "brier_all_cases_missing_penalty_1":brier,
            "calibration_bins_observed_only":bins}


def mean_ci(values: list[float], seed: int = 17, repetitions: int = 1500) -> dict:
    if len(values) < 2:
        raise ValueError("At least two independent runs are required for an interval")
    rng = random.Random(seed)
    samples = sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(repetitions))
    return {"mean":statistics.mean(values),"ci95_percentile":[samples[int(.025*repetitions)],samples[int(.975*repetitions)]],
            "n_independent_seeds":len(values),"bootstrap_resamples":repetitions}


def benchmark(seeds: list[int] | None = None, n: int = 240) -> dict:
    seeds = list(range(1000,1020)) if seeds is None else list(seeds)
    if len(seeds)<2 or len(set(seeds)) != len(seeds):
        raise ValueError("Use at least two distinct seeds")
    protocol = {"id":"NW-PERCEPTION-1","seeds":seeds,"cases_per_seed":n,
        "generator":"balanced Gaussian +/-1 classes, alternating known cue reliabilities",
        "models":["precision_weighted","equal_precision","cue_a_only"],
        "primary_metric":"brier_all_cases_missing_penalty_1","experimental_unit":"seed",
        "prediction":"Precision weighting has lower mean Brier loss than equal precision",
        "falsifier":"Paired precision-minus-equal mean Brier difference is >=0",
        "scope":"Synthetic model check; correctly specified noise is provided to all models"}
    # Materialize protocol before generation, predictions, or evaluation.
    protocol_hash = digest(protocol)
    rows, prediction_hashes = [], []
    for seed in seeds:
        observations, truths = generate(seed,n,shifted=True)
        all_predictions = {m:[predict(o,m) for o in observations] for m in protocol["models"]}
        prediction_hashes.append({"seed":seed,"hash":digest({m:[(p.id,p.probability) for p in ps] for m,ps in all_predictions.items()})})
        rows.append({"seed":seed,"models":{m:score(truths,ps) for m,ps in all_predictions.items()}})
    key=protocol["primary_metric"]
    stats={m:mean_ci([row["models"][m][key] for row in rows]) for m in protocol["models"]}
    differences=[row["models"]["precision_weighted"][key]-row["models"]["equal_precision"][key] for row in rows]
    paired=mean_ci(differences)
    return {"protocol":protocol,"protocol_hash":protocol_hash,"prediction_hashes":prediction_hashes,
        "per_seed":rows,"summary":stats,"paired_precision_minus_equal_brier":paired,
        "criterion_met":paired["mean"]<0,"independent_external_validation":False,
        "cost_note":"All models receive the same two cues. Cue-a-only deliberately ignores b. This is information-access parity, not measured equal CPU/energy cost.",
        "limits":["Public synthetic seeds are reproducible, not a blinded test set.",
                  "No training or parameter search occurs; formula/noise assumptions favor the correctly specified model.",
                  "Intervals reflect variation under this generator only; no human, clinical or consciousness inference."]}
