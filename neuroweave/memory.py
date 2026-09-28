"""Event-sourced reconstructive memory with explicit computational dependencies.

Nodes are introduced in topological order. Rules are a closed allow-list of pure
numeric operations; imported text is never evaluated as code. Source revisions
invalidate only descendants. Recompute is an explicit, audited operation.
"""
from __future__ import annotations
from copy import deepcopy
from .ledger import Ledger
from .util import finite, nonempty, digest


class Memory:
    def __init__(self, ledger: Ledger | None = None) -> None:
        self.ledger = ledger if ledger is not None else Ledger()
        self.nodes: dict[str, dict] = {}
        self.ledger.verify()
        for event in self.ledger.events():
            if not event["kind"].startswith("memory."):
                raise ValueError("Memory requires a dedicated memory event stream")
            self._apply(event["kind"], event["payload"])
        self.head = self.ledger.head

    def _descendants(self, root: str) -> set[str]:
        found = {root}
        changed = True
        while changed:
            changed = False
            for key, node in self.nodes.items():
                if key not in found and found.intersection(node["dependencies"]):
                    found.add(key)
                    changed = True
        return found - {root}

    def _calculate(self, deps: list[str], rule: dict) -> float:
        values = [self.nodes[x]["value"] for x in deps]
        op = rule.get("op")
        if op == "sum":
            result = sum(values)
        elif op == "mean":
            result = sum(values) / len(values)
        elif op == "scale" and len(values) == 1:
            result = values[0] * finite(rule.get("factor"), "factor")
        elif op == "threshold_gt" and len(values) == 1:
            result = float(values[0] > finite(rule.get("threshold"), "threshold"))
        else:
            raise ValueError("Rule must be sum, mean, one-input scale or threshold_gt")
        return finite(result, "computed value")

    def _commit(self, kind: str, payload: dict) -> None:
        # Apply to a private copy first; failed validation never partially changes memory.
        saved = self.nodes
        self.nodes = deepcopy(saved)
        try:
            self._apply(kind, payload)
            event = self.ledger.append(kind, payload, expected_head=self.head)
            self.head = event["hash"]
        except BaseException:
            self.nodes = saved
            raise

    def add_source(self, id: str, value: float, *, source: str, context: str,
                   unit: str = "arbitrary_unit", kind: str = "synthetic") -> None:
        self._commit("memory.add", dict(id=id, value=value, source=source, context=context,
                     unit=unit, evidence_kind=kind, dependencies=[], rule=None))

    def derive(self, id: str, dependencies: list[str], rule: dict, *, context: str,
               unit: str = "arbitrary_unit") -> None:
        self._commit("memory.add", dict(id=id, value=None, source="registered-rule", context=context,
                     unit=unit, evidence_kind="inference", dependencies=list(dependencies), rule=rule))

    def revise(self, id: str, value: float, *, reason: str) -> list[str]:
        self._commit("memory.revise", dict(id=id, value=value, reason=reason))
        return sorted(self._descendants(id))

    def retract(self, id: str, *, reason: str) -> list[str]:
        self._commit("memory.retract", dict(id=id, reason=reason))
        return sorted(self._descendants(id))

    def recompute(self) -> None:
        self._commit("memory.recompute", {})

    def _apply(self, kind: str, p: dict) -> None:
        if kind == "memory.add":
            for field in ("id", "source", "context", "unit", "evidence_kind"):
                nonempty(p[field], field)
            if p["evidence_kind"] not in {"synthetic", "measurement", "literature", "hypothesis", "inference"}:
                raise ValueError("Invalid evidence kind")
            id, deps = p["id"], p["dependencies"]
            if id in self.nodes or id in deps or len(set(deps)) != len(deps):
                raise ValueError("Duplicate node/dependency or cyclic self-dependency")
            if any(x not in self.nodes for x in deps):
                raise ValueError("Dependencies must already exist (topological insertion)")
            if any(self.nodes[x]["status"] != "active" for x in deps):
                raise ValueError("Cannot derive from stale or retracted evidence")
            if any(self.nodes[x]["context"] != p["context"] for x in deps):
                raise ValueError("Cross-context derivation requires an explicit external mapping")
            if deps:
                if p["rule"].get("op") != "threshold_gt" and any(self.nodes[x]["unit"] != p["unit"] for x in deps):
                    raise ValueError("This rule does not perform unit conversion")
                value = self._calculate(deps, p["rule"])
            else:
                if p["rule"] is not None:
                    raise ValueError("A derived rule needs at least one dependency")
                value = finite(p["value"], "source value")
            self.nodes[id] = dict(deepcopy(p), value=value, revision=1, status="active",
                                  dependency_revisions={x: self.nodes[x]["revision"] for x in deps})
        elif kind in {"memory.revise", "memory.retract"}:
            nonempty(p["reason"], "reason")
            id = p["id"]
            if id not in self.nodes:
                raise ValueError("Unknown node")
            node = self.nodes[id]
            if kind == "memory.revise":
                if node["dependencies"]:
                    raise ValueError("Revise sources; recompute derived nodes instead")
                node["value"] = finite(p["value"], "new value")
                node["status"] = "active"
            else:
                node["status"] = "retracted"
            node["revision"] += 1
            for dependent in self._descendants(id):
                if self.nodes[dependent]["status"] != "retracted":
                    self.nodes[dependent]["status"] = "stale"
        elif kind == "memory.recompute":
            for node in self.nodes.values():
                deps = node["dependencies"]
                if node["status"] == "stale" and deps and all(self.nodes[x]["status"] == "active" for x in deps):
                    node["value"] = self._calculate(deps, node["rule"])
                    node["revision"] += 1
                    node["status"] = "active"
                    node["dependency_revisions"] = {x: self.nodes[x]["revision"] for x in deps}
        else:
            raise ValueError("Unsupported memory event")

    def read(self, id: str) -> float:
        if id not in self.nodes:
            raise ValueError("Unknown node")
        node = self.nodes[id]
        if node["status"] != "active":
            raise ValueError(f"Node {id} is {node['status']}; not usable as current knowledge")
        return node["value"]

    def snapshot(self) -> dict:
        return deepcopy(self.nodes)

    def facts_hash(self) -> str:
        return digest({k: n for k, n in self.nodes.items() if not n["dependencies"]})
