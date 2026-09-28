"""Eighteen book-linked recipes sharing explicit, documented engine families."""
from __future__ import annotations
from dataclasses import asdict
from copy import deepcopy
import json
from pathlib import Path
from . import models
from .evidence import Evidence, assess, claim_support
from .evaluation import generate, predict, score
from .memory import Memory
from .purpose import Purpose, ConsentSession
from .runtime import ResearchRuntime
from .util import digest, integer


def chapters() -> list[dict]:
    return json.loads(Path(__file__).with_name("chapters.json").read_text(encoding="utf-8"))


def evidence_demo() -> dict:
    def e(id,lo,hi,kind="synthetic",group="instrument-a"):
        return Evidence(id,"synthetic://record",kind,"same-trial","mV",lo,hi,group,"t=0")
    uncertain=[e("a",1,3),e("b",2,4,group="instrument-b")]
    conflict=[e("c",1,2),e("d",3,4,group="instrument-b")]
    return {"compatible_intervals":assess(uncertain),"conflict":assess(conflict),
            "missing":assess([e("unknown",None,None)]),"biological_claim":claim_support("biological",uncertain),
            "experience_claim":claim_support("subjective_experience",uncertain),"records":[asdict(x) for x in uncertain]}


def context_demo() -> dict:
    observations = ["resource=1","resource=1"]
    required = {"preserve_specimen":"store", "consume_for_test":"use"}
    observation_only = ["store","store"]
    with_context = list(required.values())
    return {"observations":observations,"contexts":list(required),"required_actions":with_context,
            "observation_only_actions":observation_only,"context_actions":with_context,
            "observation_only_correct":1,"context_correct":2,"denominator":2,
            "proof_witness":"Equal input to a deterministic function yields equal output; required outputs differ.",
            "uniqueness_claim":False}


def make_memory() -> Memory:
    m=Memory()
    m.add_source("sensor",6,source="synthetic://sensor",context="trial")
    m.derive("scaled",["sensor"],{"op":"scale","factor":2},context="trial")
    m.derive("above_threshold",["scaled"],{"op":"threshold_gt","threshold":10},context="trial",unit="boolean")
    m.add_source("unrelated",80,source="synthetic://other",context="other-trial")
    return m


def memory_demo(corrected_source: float = 2) -> dict:
    m=make_memory()
    before=m.snapshot()
    affected=m.revise("sensor",corrected_source,reason="Synthetic calibration correction")
    invalidated=m.snapshot()
    m.recompute()
    after=m.snapshot()
    replay=Memory(m.ledger).snapshot()
    result={"before":before,"after_invalidation":invalidated,"after_recompute":after,"affected":affected,
            "unchanged_unrelated":before["unrelated"]==after["unrelated"],"replay_equal":after==replay,
            "events":m.ledger.events(),"checkpoint":m.ledger.verify(),
            "comparators":{"append_only":"Keeps both readings but does not specify current dependent values",
                           "overwrite_without_dependencies":"Updates the source while leaving the two descendants stale in meaning",
                           "dependency_memory":"Marks exactly the two descendants stale, then recomputes"}}
    m.ledger.close()
    return result


def purpose_demo() -> dict:
    m=make_memory()
    before=m.facts_hash()
    belief=.7
    p=Purpose("researcher","goal-1","explore",5)
    q=Purpose("researcher","goal-2","preserve",5)
    result={"belief":belief,"purpose_a":asdict(p),"purpose_b":asdict(q),"action_a":p.choose(belief),
            "action_b":q.choose(belief),"facts_hash_before":before,"facts_hash_after":m.facts_hash(),
            "zero_budget_action":Purpose("researcher","goal-3","explore",0).choose(belief)}
    m.ledger.close()
    return result


def semantic_diff(source: dict, transfer: dict) -> dict:
    fields=("owner","action","negated","context")
    missing=[k for k in fields if k not in transfer]
    changed=[k for k in fields if k in transfer and source.get(k)!=transfer[k]]
    return {"fields_checked":list(fields),"missing":missing,"changed":changed,"faithful":not missing and not changed}


def semantics_demo() -> dict:
    original={"owner":"person-a","action":"share_message","negated":True,"context":"private"}
    broken={"owner":"person-a","action":"share_message","context":"private"}
    return {"source":original,"correct_transfer":semantic_diff(original,dict(original)),
            "lossy_transfer":semantic_diff(original,broken),"scope":"Four declared semantic fields; no natural-language parser"}


def consent_demo() -> dict:
    p=Purpose("person-a","communication","preserve",3)
    payload={"action":"simulated_message","text":"Do not share my note."}
    s=ConsentSession()
    f=s.propose("msg-1",payload,p,now=0)
    blocked=[]
    try: s.execute("msg-1",payload,p,actor="person-a",now=1)
    except PermissionError: blocked.append("unconfirmed")
    s.confirm("msg-1",f,actor="person-a",now=2)
    try: s.execute("msg-1",{**payload,"text":"Share my note."},p,actor="person-a",now=3)
    except PermissionError: blocked.append("payload_change")
    receipt=s.execute("msg-1",payload,p,actor="person-a",now=4)
    try: s.execute("msg-1",payload,p,actor="person-a",now=5)
    except PermissionError: blocked.append("replay")
    f=s.propose("msg-2",payload,p,now=6)
    s.confirm("msg-2",f,actor="person-a",now=7)
    s.revoke("msg-2",actor="person-a",now=8)
    try: s.execute("msg-2",payload,p,actor="person-a",now=9)
    except PermissionError: blocked.append("revoked")
    s.propose("msg-3",payload,p,now=10,ttl=1)
    try: s.confirm("msg-3",f,actor="person-a",now=12)
    except PermissionError: blocked.append("expired")
    return {"blocked_cases":blocked,"receipt":receipt,"audit":s.audit,
            "identity_authentication":"Not implemented: declared actors inside a local teaching process"}


def integrated_demo(seed: int) -> dict:
    m=make_memory()
    p=Purpose("researcher","exploration","explore",5)
    runtime=ResearchRuntime(m,p)
    initial=runtime.state()
    facts_before=m.facts_hash()
    runtime.propose("original","above_threshold",now=0)
    runtime.set_purpose(Purpose("researcher","preservation","preserve",5))
    goal_changed=runtime.state()
    blocked=[]
    try: runtime.confirm("original",actor="researcher",now=1)
    except PermissionError: blocked.append("purpose_changed_after_planning")
    runtime.propose("before-correction","above_threshold",now=2)
    m.revise("sensor",2,reason="New calibration evidence Y_t")
    invalidated=runtime.state()
    try: runtime.confirm("before-correction",actor="researcher",now=3)
    except PermissionError: blocked.append("evidence_changed_after_planning")
    m.recompute()
    updated=runtime.state()
    runtime.propose("fresh","above_threshold",now=4)
    runtime.confirm("fresh",actor="researcher",now=5)
    outcome=runtime.execute("fresh",actor="researcher",now=6,seed=seed)
    result={"initial":initial,"goal_changed":goal_changed,"after_evidence_revision":invalidated,
            "after_reconstruction":updated,"after_feedback":outcome["state_after"],
            "facts_preserved_under_goal_change":initial["O"]==goal_changed["O"],
            "source_hash_at_start":facts_before,"blocked_stale_plans":blocked,
            "decision_value_before":initial["K"]["above_threshold"]["value"],
            "decision_value_after":updated["K"]["above_threshold"]["value"],
            "receipt":outcome["receipt"],"feedback_kind":"synthetic",
            "resource_before":initial["B"]["remaining_resource"],"resource_after":outcome["resource_remaining"],
            "event_count":len(m.ledger.events()),"checkpoint":m.ledger.head,
            "replay_equal":Memory(m.ledger).snapshot()==m.snapshot()}
    m.ledger.close()
    return result


def run_lab(id: str, seed: int = 17, parameters: dict | None = None) -> dict:
    integer(seed,"seed",0,2**31-1)
    by_id={c["id"]:c for c in chapters()}
    if id not in by_id:
        raise ValueError("Unknown chapter ID")
    parameters={} if parameters is None else deepcopy(parameters)
    if not isinstance(parameters,dict):
        raise ValueError("Parameters must be a JSON object")
    allowed={7:{"current_na","dt_ms","duration_ms"},10:{"corrected_source"},15:{"beta","gamma","n"}}
    c=by_id[id]; n=c["chapter"]
    if set(parameters)-allowed.get(n,set()):
        raise ValueError(f"Unsupported parameters for {id}: {sorted(set(parameters)-allowed.get(n,set()))}")
    protocol={"id":f"NW-CH{n:02}-1","chapter":n,"seed":seed,"parameters":parameters,
              "hypothesis":c["hypothesis"],"exercise":c["exercise"],"limit":c["limit"],"evidence":"synthetic",
              "falsifier":c["falsifier"],"control":c["control"],"evaluation_mode":"inspect_result_and_regression_tests"}
    protocol_hash=digest(protocol)
    if n==1: result=evidence_demo()
    elif n in {2,8}: result=models.homeostasis(seed)
    elif n==3: result=models.network(seed)
    elif n==4: result={"intact":models.network(seed),"lesioned":models.network(seed,True)}
    elif n==5: result=context_demo()
    elif n==6: result=models.plasticity(seed)
    elif n==7: result=models.lif(**parameters)
    elif n==9:
        observations,truths=generate(seed)
        predictions={model:[predict(o,model) for o in observations] for model in ("precision_weighted","equal_precision","cue_a_only")}
        result={"scores":{model:score(truths,ps) for model,ps in predictions.items()},
                "examples":[asdict(o) for o in observations[:12]],"interface_contains_labels":False}
    elif n==10: result=memory_demo(**parameters)
    elif n==11: result=purpose_demo()
    elif n==12: result=semantics_demo()
    elif n==13: result=models.mechanism_suite(seed)
    elif n==14:
        baseline=models.mechanism_trace(seed,"recurrent_workspace","baseline")
        output_loss=models.mechanism_trace(seed,"recurrent_workspace","report_lesion")
        result={"baseline":baseline,"output_loss":output_loss,"same_latent_state":baseline["latent"]==output_loss["latent"],"medical_interpretation":"Not supported"}
    elif n==15: result=models.causal(seed,**parameters)
    elif n==16: result=integrated_demo(seed)
    elif n==17: result=consent_demo()
    else:
        m=make_memory()
        initial=m.snapshot()
        affected=m.retract("sensor",reason="Source withdrawal after failed replication in synthetic exercise")
        m.recompute()
        result={"initial":initial,"after_withdrawal":m.snapshot(),"affected":affected,"claim_status":"reopened",
                "unrelated_preserved":m.read("unrelated")==80,"falsifier":"Source cannot be independently reproduced",
                "ledger_valid":bool(m.ledger.verify()),"event_count":len(m.ledger.events())}
        m.ledger.close()
    return {"system":"DIKWP NeuroWeave Lab","version":"1.0.0","chapter":c,"protocol":protocol,
            "protocol_hash":protocol_hash,"result":result,"result_hash":digest(result),
            "evidence_status":"synthetic_software_demonstration","biological_validation":False,
            "subjective_experience_proven":False}
