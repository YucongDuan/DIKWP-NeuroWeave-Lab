"""Small, inspectable numerical models; none is a whole-brain simulation."""
from __future__ import annotations
import math
import random
import statistics
from .util import finite, integer


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-max(-700, min(700, x))))


def lif(*, current_na: float = .2, duration_ms: float = 200, dt_ms: float = .5,
        tau_ms: float = 20, resistance_mohm: float = 100, rest_mv: float = -65,
        reset_mv: float = -65, threshold_mv: float = -50, refractory_ms: float = 2) -> dict:
    """Constant-current LIF with analytic within-step crossing and refractory time.

    MOhm * nA = mV. dt is a recording interval, not Euler integration time.
    Only constant input is supported; no claim about biological spike shape.
    """
    for name, value in locals().copy().items():
        finite(value, name)
    if not (0 < dt_ms <= duration_ms <= 10000 and tau_ms > 0 and resistance_mohm > 0):
        raise ValueError("Positive time/resistance required; duration at most 10000 ms")
    if duration_ms / dt_ms > 50000 or refractory_ms < 0 or reset_mv >= threshold_mv or rest_mv >= threshold_mv:
        raise ValueError("Invalid resolution, refractory period or voltages")
    eq = finite(rest_mv + resistance_mohm * current_na, "equilibrium voltage")
    v, t, refractory_until = rest_mv, 0.0, -1.0
    spikes, series = [], [[0.0, v]]
    while t < duration_ms - 1e-10:
        end = min(duration_ms, t + dt_ms)
        while t < end - 1e-12:
            if t < refractory_until:
                t = min(end, refractory_until)
                v = reset_mv
                continue
            crossing = tau_ms * math.log1p((threshold_mv-v)/(eq-threshold_mv)) if eq > threshold_mv else math.inf
            remaining = end - t
            if crossing <= remaining + 1e-12:
                t += max(0.0, crossing)
                spikes.append(t)
                if len(spikes) > 100000:
                    raise ValueError("Spike event budget exceeded; reduce duration or current")
                v = reset_mv
                refractory_until = t + refractory_ms
            else:
                v = eq + (v-eq) * math.exp(-remaining/tau_ms)
                t = end
        series.append([end, v])
    isi = None if eq <= threshold_mv else refractory_ms + tau_ms * math.log((eq-reset_mv)/(eq-threshold_mv))
    return {"series": series, "spike_times_ms": spikes, "spike_count": len(spikes),
            "asymptotic_isi_ms": isi, "equilibrium_mv": eq,
            "units": {"x": "ms", "y": "mV"}, "solver": "exact constant-current subthreshold and crossing"}


def homeostasis(seed: int, steps: int = 120) -> dict:
    rng = random.Random(seed)
    disturbances = [rng.uniform(.1, .5) for _ in range(steps)]
    traces = {}
    for name in ("always_work", "resource_aware"):
        energy, initial, gained, spent = 6.0, 6.0, 0.0, 0.0
        series, work = [], 0
        for t, drain in enumerate(disturbances):
            recover = name == "resource_aware" and energy < 3
            inflow, requested = (1.4, drain) if recover else (0, .6 + drain)
            actual = min(energy + inflow, requested)
            energy += inflow - actual
            gained += inflow
            spent += actual
            if not recover and actual >= requested - 1e-10:
                work += 1
            series.append([t, energy])
        traces[name] = {"series": series, "completed_work_steps": work, "final_resource": energy,
                        "balance_residual": energy - (initial + gained - spent),
                        "resource_gained": gained, "resource_spent": spent}
    return {"policies": traces, "units": {"x": "step", "y": "arbitrary resource unit"},
            "note": "Toy resource accounting, not thermodynamic entropy or a physiological intervention."}


def network(seed: int, lesion: bool = False) -> dict:
    # Directed cycle versus chain: outgoing mass is transferred with gain .8.
    n, steps, gain = 6, 24, .8
    traces = {}
    for topology in ("chain", "cycle"):
        state, series = [1.] + [0.]*(n-1), []
        for t in range(steps):
            series.append([t, sum(state)])
            next_state = [0.]*n
            for i, value in enumerate(state):
                target = (i+1) % n
                if topology == "chain" and i == n-1:
                    continue
                if lesion and target == 3:
                    continue
                next_state[target] += gain*value
            state = next_state
        traces[topology] = {"series": series, "terminal_activity": sum(state)}
    return {"networks": traces, "lesion_node": 3 if lesion else None,
            "note": "Connectivity toy; not a ranking of living species or an evolutionary reconstruction."}


def plasticity(seed: int, steps: int = 120) -> dict:
    rng = random.Random(seed)
    data = [(1 if t < steps//2 else -1) + rng.gauss(0,.2) for t in range(steps)]
    estimates = {"running_average": 0., "adaptive_ema": 0.}
    traces = {k: [] for k in estimates}
    errors = {k: [] for k in estimates}
    for t, x in enumerate(data):
        target = 1 if t < steps//2 else -1
        for name, value in estimates.items():
            errors[name].append((value-target)**2)
            alpha = 1/(t+1) if name == "running_average" else .2
            estimates[name] = value + alpha*(x-value)
            traces[name].append([t, estimates[name]])
    return {"estimators": {k: {"series": traces[k], "post_change_prediction_mse": statistics.mean(errors[k][steps//2:])}
                           for k in estimates}, "change_step": steps//2,
            "note": "Prediction precedes each update. Faster adaptation trades stability for responsiveness."}


def causal(seed: int, n: int = 4000, beta: float = 1.0, gamma: float = 2.0) -> dict:
    integer(n, "n", 10, 100000)
    finite(beta, "beta"); finite(gamma, "gamma")
    rng = random.Random(seed)
    xs, ys, intervention_differences = [], [], []
    for _ in range(n):
        u, ex, ey = rng.gauss(0,1), rng.gauss(0,1), rng.gauss(0,1)
        x = u + ex
        xs.append(x); ys.append(beta*x + gamma*u + ey)
        # Pair do(X=1) and do(X=0) using the same exogenous U and noise.
        intervention_differences.append((beta + gamma*u + ey) - (gamma*u + ey))
    xm, ym = statistics.mean(xs), statistics.mean(ys)
    slope = sum((x-xm)*(y-ym) for x,y in zip(xs,ys)) / sum((x-xm)**2 for x in xs)
    return {"observational_slope": slope, "analytical_observational_slope": beta+gamma/2,
            "paired_do_effect": statistics.mean(intervention_differences), "structural_beta": beta,
            "n": n, "equations": ["X=U+epsilon_X", "Y=beta*X+gamma*U+epsilon_Y"],
            "note": "Known synthetic SCM. Exact paired effect follows its additive equations; not discovered human causality."}


def mechanism_trace(seed: int, mechanism: str, condition: str, steps: int = 40) -> dict:
    if mechanism not in {"recurrent_workspace", "sensory_filter"}:
        raise ValueError("Unknown competing mechanism")
    if condition not in {"baseline", "sham", "workspace_lesion", "report_lesion", "rescue"}:
        raise ValueError("Unknown intervention")
    rng = random.Random(seed)
    inputs = [(1 if t in {2,20} else 0) + rng.gauss(0,.015) for t in range(steps)]
    state, latent, reports = 0., [], []
    for t, x in enumerate(inputs):
        persistence = 0.0 if condition == "workspace_lesion" and mechanism == "recurrent_workspace" else .85
        state = persistence*state + x
        latent.append([t,state])
        reports.append([t,0. if condition == "report_lesion" else state])
    return {"latent": latent, "series": reports, "report_energy": sum(v*v for _,v in reports),
            "latent_energy": sum(v*v for _,v in latent), "mechanism": mechanism, "condition": condition}


def mechanism_suite(seed: int) -> dict:
    trials = {m: {c: mechanism_trace(seed,m,c) for c in
                ("baseline","sham","workspace_lesion","report_lesion","rescue")}
              for m in ("recurrent_workspace","sensory_filter")}
    equal = trials["recurrent_workspace"]["baseline"]["series"] == trials["sensory_filter"]["baseline"]["series"]
    return {"trials": trials, "observationally_matched": equal,
            "note": "Two hand-constructed realizations share a transfer function but differ under a targeted internal lesion. Rescue resets original parameters in a new paired trial. Not a validated consciousness test."}
