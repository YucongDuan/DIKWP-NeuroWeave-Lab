"""Unified book-state runtime: evidence -> plan -> confirmation -> local feedback.

Plans pin the evidence-log head, purpose revision and remaining resource budget.
Changing any of those invalidates confirmation/execution until a new plan is made.
Only single-process synthetic actions exist; this is not an authenticated actuator.
"""
from __future__ import annotations
from dataclasses import asdict
from copy import deepcopy
import random
from .memory import Memory
from .purpose import Purpose, ConsentSession
from .util import digest, finite, integer


class ResearchRuntime:
    def __init__(self, memory: Memory, purpose: Purpose) -> None:
        self.memory=memory
        self.purpose=purpose
        self.purpose_revision=1
        self.remaining=purpose.resource_budget
        self.session=ConsentSession()
        self.plans: dict[str,dict]={}

    def set_purpose(self, purpose: Purpose) -> None:
        if purpose.owner != self.purpose.owner:
            raise PermissionError("Changing the declared owner needs a new runtime")
        self.purpose=purpose
        self.purpose_revision+=1
        self.remaining=min(self.remaining,purpose.resource_budget)

    def state(self) -> dict:
        nodes=self.memory.snapshot()
        return {"O":{k:v for k,v in nodes.items() if not v['dependencies']},
                "E":{k:v['dependencies'] for k,v in nodes.items()},
                "K":{k:v for k,v in nodes.items() if v['dependencies']},
                "V":{"source_history_required":True,"confirmation_required":True,"simulation_only":True},
                "P":{**asdict(self.purpose),"revision":self.purpose_revision},
                "B":{"remaining_resource":self.remaining,"unit":"arbitrary resource unit"}}

    def _signature(self) -> str:
        # Compare local state with the current log, detecting a concurrent writer.
        self.memory.ledger.verify(self.memory.head)
        return digest({"memory_head":self.memory.head,"purpose":asdict(self.purpose),
                       "purpose_revision":self.purpose_revision,"remaining":self.remaining})

    def propose(self, id: str, node: str, *, now: float, cost: float=.5, ttl: float=60) -> dict:
        finite(cost,"cost",minimum=.001,maximum=10000)
        if cost > self.remaining:
            raise PermissionError("Insufficient declared resources")
        value=self.memory.read(node)
        if f"feedback:{id}" in self.memory.nodes:
            raise ValueError("Feedback record for this plan already exists")
        signature=self._signature()
        payload={"action":"simulated_sample","node":node,"node_revision":self.memory.nodes[node]['revision'],
                 "value_at_plan":value,"state_signature":signature,"resource_cost":cost}
        fingerprint=self.session.propose(id,payload,self.purpose,now=now,ttl=ttl)
        plan={"id":id,"payload":payload,"fingerprint":fingerprint,"state_signature":signature,
              "purpose":asdict(self.purpose)}
        self.plans[id]=deepcopy(plan)
        return deepcopy(plan)

    def _validate(self,id: str) -> dict:
        if id not in self.plans:
            raise ValueError("Unknown plan")
        p=self.plans[id]
        if p['state_signature'] != self._signature():
            raise PermissionError("Evidence, purpose, or resources changed; create a fresh plan")
        self.memory.read(p['payload']['node'])
        return p

    def confirm(self,id: str,*,actor: str,now: float) -> None:
        p=self._validate(id)
        self.session.confirm(id,p['fingerprint'],actor=actor,now=now)

    def execute(self,id: str,*,actor: str,now: float,seed: int) -> dict:
        integer(seed,"seed",0,2**31-1)
        p=self._validate(id)
        receipt=self.session.execute(id,p['payload'],self.purpose,actor=actor,now=now)
        self.remaining-=p['payload']['resource_cost']
        # A declared synthetic measurement around the planned value, not real sensor data.
        outcome=p['payload']['value_at_plan']+random.Random(seed).gauss(0,.1)
        self.memory.add_source(f"feedback:{id}",outcome,source=f"synthetic://receipt/{id}",
                               context="local-feedback",kind="synthetic")
        return {"receipt":receipt,"feedback":outcome,"resource_remaining":self.remaining,
                "state_after":self.state(),"state_hash":digest(self.state())}
