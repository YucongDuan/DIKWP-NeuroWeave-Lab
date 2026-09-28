"""Single-session consent state machine for local simulations ONLY.

Actor names are declarations inside a teaching process, not authenticated human
identities. No network, BCI, medical device or real-world actuator is provided.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from .util import digest, finite, nonempty


@dataclass(frozen=True)
class Purpose:
    owner: str
    id: str
    mode: str
    resource_budget: float

    def __post_init__(self) -> None:
        nonempty(self.owner, "owner")
        nonempty(self.id, "purpose id")
        if self.mode not in {"explore", "preserve"}:
            raise ValueError("Mode must be explore or preserve")
        finite(self.resource_budget, "resource_budget", minimum=0)

    def choose(self, belief: float) -> str:
        belief = finite(belief, "belief", minimum=0, maximum=1)
        # Same evidence, different declared utility. Toy costs, not advice.
        if self.resource_budget < 1:
            return "rest"
        if self.mode == "explore":
            return "sample" if belief < 0.9 else "rest"
        return "rest" if belief < 0.9 else "sample"


class ConsentSession:
    def __init__(self) -> None:
        self.candidates: dict[str, dict] = {}
        self.audit: list[dict] = []

    def propose(self, id: str, payload: dict, purpose: Purpose, *, now: float, ttl: float = 60) -> str:
        nonempty(id, "candidate id")
        if id in self.candidates:
            raise ValueError("Candidate ID already used")
        finite(now, "now", minimum=0)
        finite(ttl, "ttl", minimum=0.001, maximum=3600)
        if payload.get("action") not in {"simulated_message", "simulated_sample"}:
            raise ValueError("Only local simulated actions are supported")
        fingerprint = digest({"payload": payload, "purpose": asdict(purpose)})
        self.candidates[id] = {"fingerprint": fingerprint, "purpose": asdict(purpose),
            "expires_at": now + ttl, "status": "candidate", "created_at": now, "last_at": now}
        self.audit.append({"event": "candidate", "id": id, "at": now})
        return fingerprint

    def _get(self, id: str, actor: str, now: float) -> dict:
        if id not in self.candidates:
            raise ValueError("Unknown candidate")
        c = self.candidates[id]
        finite(now, "now", minimum=c["last_at"])
        if actor != c["purpose"]["owner"]:
            raise PermissionError("Actor differs from declared owner")
        c["last_at"] = now
        if now >= c["expires_at"]:
            raise PermissionError("Candidate expired")
        return c

    def confirm(self, id: str, fingerprint: str, *, actor: str, now: float) -> None:
        c = self._get(id, actor, now)
        if c["status"] != "candidate" or fingerprint != c["fingerprint"]:
            raise PermissionError("Candidate is not confirmable or content changed")
        c["status"] = "confirmed"
        self.audit.append({"event": "confirmed", "id": id, "at": now})

    def revoke(self, id: str, *, actor: str, now: float) -> None:
        c = self._get(id, actor, now)
        if c["status"] in {"executed", "revoked"}:
            raise PermissionError("Cannot revoke an already consumed candidate")
        c["status"] = "revoked"
        self.audit.append({"event": "revoked", "id": id, "at": now})

    def execute(self, id: str, payload: dict, purpose: Purpose, *, actor: str, now: float) -> dict:
        c = self._get(id, actor, now)
        if c["status"] != "confirmed":
            raise PermissionError("Explicit confirmation required; no automatic actuation")
        if digest({"payload": payload, "purpose": asdict(purpose)}) != c["fingerprint"]:
            raise PermissionError("Confirmed payload or purpose has changed")
        c["status"] = "executed"
        receipt = {"event": "local_simulation_executed", "id": id, "at": now,
                   "fingerprint": c["fingerprint"], "external_side_effect": False}
        self.audit.append(receipt)
        return dict(receipt)
