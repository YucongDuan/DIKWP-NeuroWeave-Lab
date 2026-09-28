"""Typed evidence and distinct missing / conflicting / imprecise reports.

These are declared record semantics, not automatic source authentication.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .util import finite, nonempty

EvidenceKind = Literal["synthetic", "measurement", "literature", "hypothesis", "inference"]
KINDS = {"synthetic", "measurement", "literature", "hypothesis", "inference"}


@dataclass(frozen=True)
class Evidence:
    id: str
    source: str
    kind: EvidenceKind
    context: str
    unit: str
    low: float | None
    high: float | None
    source_group: str
    observed_at: str

    def __post_init__(self) -> None:
        for field in ("id", "source", "context", "unit", "source_group", "observed_at"):
            nonempty(getattr(self, field), field)
        if self.kind not in KINDS:
            raise ValueError("Unknown evidence kind")
        if (self.low is None) != (self.high is None):
            raise ValueError("Both bounds must be present or both missing")
        if self.low is not None:
            finite(self.low, "low")
            finite(self.high, "high")
            if self.low > self.high:
                raise ValueError("Interval lower bound exceeds upper bound")


def assess(records: list[Evidence]) -> dict:
    if not records:
        return {"status": "incomplete", "independent_source_groups": 0, "interval": None}
    if len({r.id for r in records}) != len(records):
        raise ValueError("Duplicate evidence IDs")
    if len({(r.context, r.unit, r.observed_at) for r in records}) != 1:
        return {"status": "not_comparable", "reason": "Context, units or observation time differ", "interval": None}
    groups = len({r.source_group for r in records})
    observed = [r for r in records if r.low is not None]
    if not observed:
        return {"status": "incomplete", "independent_source_groups": groups, "interval": None}
    low, high = max(r.low for r in observed), min(r.high for r in observed)
    status = "inconsistent" if low > high else "imprecise" if low < high else "precise"
    return {"status": status, "has_missing": len(observed) < len(records),
            "independent_source_groups": groups,
            "interval": None if low > high else [low, high],
            "note": "Intersection is a compatibility check, not a statistical confidence interval."}


def claim_support(claim_domain: str, records: list[Evidence]) -> dict:
    nonempty(claim_domain, "claim_domain")
    if claim_domain not in {"software", "biological", "subjective_experience"}:
        raise ValueError("Unknown claim domain")
    if not records:
        return {"status": "unsupported", "reason": "No evidence"}
    if claim_domain == "subjective_experience":
        return {"status": "unresolved", "reason": "This runtime has no validated experience adjudicator"}
    if claim_domain == "biological" and all(r.kind in {"synthetic", "hypothesis", "inference"} for r in records):
        return {"status": "unsupported", "reason": "Synthetic results and hypotheses alone are not biological validation"}
    return {"status": "review_required", "reason": "Typed provenance permits review; it does not validate the claim"}
