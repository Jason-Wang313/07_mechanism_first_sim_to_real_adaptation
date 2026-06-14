"""Full-scale, RAM-light experiment suite for Paper 07.

The original simulator in mechanism_first_sim.py is intentionally small. This
driver keeps the same control task but expands the evidence surface: larger
seed sweeps, richer baselines, ablations, stress tests, out-of-library controls,
threshold sensitivity, and generated paper figures/tables. It stores compact
aggregate rows only.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
from collections import defaultdict

import mechanism_first_sim as sim


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "results", "full_scale")
TABLE_DIR = os.path.join(OUT_DIR, "tables")
FIG_DIR = os.path.join(ROOT, "paper", "figures")
PROGRESS_PATH = os.path.join(OUT_DIR, "full_run_progress.log")

KNOWN_KINDS = list(sim.KINDS)
BASE_REPAIRS = list(sim.REPAIRS)
FULL_PROBE_KEYS = [
    "low_first",
    "low_total",
    "low_second_jump",
    "high_first",
    "high_total",
    "high_decay",
    "alt_after_reverse",
    "alt_total",
    "high_low_ratio",
    "delayed_second_jump",
]

MAIN_METHODS = [
    "nominal_no_adaptation",
    "random_repair",
    "single_robust_repair",
    "passive_stat_coarse",
    "passive_stat_medium",
    "passive_stat_fine",
    "passive_vector_nn",
    "nuisance_nearest_neighbor",
    "probe_nearest_neighbor",
    "gain_only_sysid",
    "mechanism_first",
    "mechanism_oracle",
    "oracle_best_repair",
]

PLOT_METHOD_ORDER = [
    "nominal_no_adaptation",
    "random_repair",
    "single_robust_repair",
    "passive_stat_coarse",
    "passive_stat_fine",
    "passive_vector_nn",
    "nuisance_nearest_neighbor",
    "probe_nearest_neighbor",
    "gain_only_sysid",
    "mechanism_first",
    "mechanism_oracle",
    "oracle_best_repair",
]

METHOD_LABEL = {
    "nominal_no_adaptation": "nominal",
    "random_repair": "random",
    "single_robust_repair": "single robust",
    "passive_stat_coarse": "passive coarse",
    "passive_stat_medium": "passive medium",
    "passive_stat_fine": "passive fine",
    "passive_vector_nn": "passive vector NN",
    "nuisance_nearest_neighbor": "nuisance NN",
    "probe_nearest_neighbor": "probe NN",
    "gain_only_sysid": "gain sysID",
    "mechanism_first": "mechanism-first",
    "mechanism_first_limited": "mechanism-first",
    "mechanism_first_reject": "mechanism-first reject",
    "mechanism_oracle": "mechanism oracle",
    "oracle_best_repair": "best repair oracle",
}

MIXES = {
    "uniform": {"gain": 0.25, "delay": 0.25, "slip": 0.25, "compliance": 0.25},
    "gain_heavy": {"gain": 0.62, "delay": 0.13, "slip": 0.13, "compliance": 0.12},
    "delay_heavy": {"gain": 0.13, "delay": 0.62, "slip": 0.13, "compliance": 0.12},
    "slip_heavy": {"gain": 0.13, "delay": 0.12, "slip": 0.62, "compliance": 0.13},
    "compliance_rare": {"gain": 0.34, "delay": 0.33, "slip": 0.28, "compliance": 0.05},
    "two_mechanism": {"gain": 0.50, "delay": 0.00, "slip": 0.50, "compliance": 0.00},
}

PROBE_GROUPS = {
    "full_probe": FULL_PROBE_KEYS,
    "low_only": ["low_first", "low_total", "low_second_jump"],
    "high_only": ["high_first", "high_total", "high_decay", "delayed_second_jump"],
    "alternating_only": ["alt_after_reverse", "alt_total"],
    "no_low": [
        "high_first",
        "high_total",
        "high_decay",
        "alt_after_reverse",
        "alt_total",
        "delayed_second_jump",
    ],
    "no_high": ["low_first", "low_total", "low_second_jump", "alt_after_reverse", "alt_total"],
    "no_alternating": [
        "low_first",
        "low_total",
        "low_second_jump",
        "high_first",
        "high_total",
        "high_decay",
        "high_low_ratio",
        "delayed_second_jump",
    ],
}

NOISE_LEVELS = {
    "gaussian": [0.0, 0.01, 0.02, 0.04, 0.08, 0.12],
    "bias": [0.0, 0.01, 0.02, 0.04, 0.08, 0.12],
    "dropout": [0.0, 0.05, 0.10, 0.20, 0.35, 0.50],
    "quantization": [0.0, 0.01, 0.02, 0.04, 0.08, 0.12],
    "sign_flip": [0.0, 0.02, 0.05, 0.10, 0.20, 0.35],
}

FIG_COLORS = [
    "#4c78a8",
    "#f58518",
    "#54a24b",
    "#b279a2",
    "#e45756",
    "#72b7b2",
    "#8c6d31",
    "#6b6ecf",
    "#9c755f",
    "#2f7f7f",
    "#555555",
    "#222222",
]

EVAL_COUNTER = defaultdict(int)


def ensure_dirs() -> None:
    for path in [OUT_DIR, TABLE_DIR, FIG_DIR]:
        os.makedirs(path, exist_ok=True)


def progress(message: str) -> None:
    line = f"{message} | rollouts={EVAL_COUNTER['rollouts']}"
    print(line, flush=True)
    try:
        with open(PROGRESS_PATH, "a", encoding="utf-8", newline="\n") as f:
            f.write(line + "\n")
    except OSError:
        pass


def stable_seed(*parts: object) -> int:
    value = 2166136261
    for part in parts:
        for ch in str(part):
            value ^= ord(ch)
            value = (value * 16777619) & 0xFFFFFFFF
    return value


def clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = int(round((len(ordered) - 1) * q))
    return ordered[max(0, min(len(ordered) - 1, idx))]


def sem(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    m = mean(values)
    var = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(var / len(values))


def qbin(x: float, width: float) -> int:
    return int(math.floor(x / width))


def weighted_choice(rng: random.Random, weights: dict[str, float]) -> str:
    total = sum(max(0.0, w) for w in weights.values())
    if total <= 0:
        return rng.choice(KNOWN_KINDS)
    point = rng.random() * total
    running = 0.0
    last = None
    for key, weight in weights.items():
        if weight <= 0:
            continue
        running += weight
        last = key
        if point <= running:
            return key
    return last or rng.choice(KNOWN_KINDS)


def write_csv(path: str, rows: list[dict], fields: list[str] | None = None) -> None:
    if fields is None:
        field_set = []
        seen = set()
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    field_set.append(key)
        fields = field_set
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: str, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


def make_domain(
    rng: random.Random,
    kind: str | None = None,
    mix: dict[str, float] | None = None,
    severity: float = 1.0,
    nuisance_strength: float = 1.0,
) -> dict:
    if kind is None:
        kind = weighted_choice(rng, mix or MIXES["uniform"])

    if kind in KNOWN_KINDS:
        domain = sim.make_domain(rng, kind)
        if kind == "gain":
            domain["gain"] = clip(1.0 - (1.0 - domain["gain"]) * severity, 0.40, 0.82)
        elif kind == "slip":
            domain["threshold"] = clip(domain["threshold"] / (0.92 + 0.08 * severity), 0.18, 0.45)
            domain["slip_loss"] = clip(domain["slip_loss"] * severity, 0.45, 1.25)
        elif kind == "compliance":
            domain["threshold"] = clip(domain["threshold"] * severity, 0.20, 0.62)
            domain["post_gain"] = clip(1.0 - (1.0 - domain["post_gain"]) * severity, 0.65, 0.98)
        domain["family"] = "known"
    elif kind == "friction":
        domain = {
            "kind": "friction",
            "friction_gain": rng.uniform(0.76, 0.89),
            "coulomb": rng.uniform(0.025, 0.060),
            "texture": rng.randrange(30),
            "lighting": rng.uniform(0.0, 1.0),
            "appearance": [rng.gauss(0.0, 1.0) for _ in range(16)],
            "sensor_noise": rng.uniform(0.0, 0.015),
            "family": "out_of_library",
        }
    elif kind == "gain_delay":
        domain = {
            "kind": "gain_delay",
            "gain": rng.uniform(0.52, 0.66),
            "texture": rng.randrange(30),
            "lighting": rng.uniform(0.0, 1.0),
            "appearance": [rng.gauss(0.0, 1.0) for _ in range(16)],
            "sensor_noise": rng.uniform(0.0, 0.015),
            "family": "mixed",
        }
    elif kind == "slip_compliance":
        domain = {
            "kind": "slip_compliance",
            "threshold": rng.uniform(0.24, 0.36),
            "compression_threshold": rng.uniform(0.20, 0.34),
            "post_gain": rng.uniform(0.78, 0.92),
            "slip_loss": rng.uniform(0.60, 0.90),
            "texture": rng.randrange(30),
            "lighting": rng.uniform(0.0, 1.0),
            "appearance": [rng.gauss(0.0, 1.0) for _ in range(16)],
            "sensor_noise": rng.uniform(0.0, 0.015),
            "family": "mixed",
        }
    else:
        domain = sim.make_domain(rng, rng.choice(KNOWN_KINDS))
        domain["kind"] = kind
        domain["family"] = "unknown"

    domain["lighting"] = clip(domain.get("lighting", 0.5) * nuisance_strength, 0.0, 1.5)
    domain["appearance"] = [nuisance_strength * a for a in domain.get("appearance", [])]
    domain["sensor_noise"] = clip(domain.get("sensor_noise", 0.0) * nuisance_strength, 0.0, 0.05)
    return domain


def reset_memory() -> dict:
    return {"prev_u": 0.0, "compression": 0.0}


def step(domain: dict, x: float, u: float, memory: dict) -> float:
    u = clip(u, -1.0, 1.0)
    kind = domain["kind"]
    if kind == "gain":
        dx = domain["gain"] * u
    elif kind == "delay":
        dx = domain["gain"] * memory["prev_u"]
        memory["prev_u"] = u
    elif kind == "slip":
        threshold = domain["threshold"]
        if abs(u) <= threshold:
            dx = u
        else:
            over = abs(u) - threshold
            dx = math.copysign(max(0.0, threshold - domain["slip_loss"] * over), u)
    elif kind == "compliance":
        if memory["compression"] < domain["threshold"]:
            signed = 1.0 if u >= 0 else -1.0
            memory["compression"] += abs(u)
            released = max(0.0, memory["compression"] - domain["threshold"])
            dx = signed * released * domain["post_gain"]
        else:
            dx = domain["post_gain"] * u
    elif kind == "friction":
        if abs(u) <= domain["coulomb"]:
            dx = 0.0
        else:
            dx = domain["friction_gain"] * (u - math.copysign(domain["coulomb"], u))
    elif kind == "gain_delay":
        dx = domain["gain"] * memory["prev_u"]
        memory["prev_u"] = u
    elif kind == "slip_compliance":
        effective_u = u
        if memory["compression"] < domain["compression_threshold"]:
            signed = 1.0 if u >= 0 else -1.0
            memory["compression"] += abs(u)
            released = max(0.0, memory["compression"] - domain["compression_threshold"])
            effective_u = signed * released * domain["post_gain"]
        threshold = domain["threshold"]
        if abs(effective_u) <= threshold:
            dx = effective_u
        else:
            over = abs(effective_u) - threshold
            dx = math.copysign(max(0.0, threshold - domain["slip_loss"] * over), effective_u)
    else:
        dx = u
    return x + dx


def control_action(x: float, t: int, repair: str, memory: dict) -> float:
    error = sim.TARGET - x
    base = clip(0.72 * error, -0.46, 0.46)
    if repair == "none":
        return base
    if repair == "gain_comp":
        return clip(base / 0.55, -0.86, 0.86)
    if repair == "delay_brake":
        predicted = x + memory.get("prev_u", 0.0)
        return clip(0.58 * (sim.TARGET - predicted), -0.36, 0.36)
    if repair == "slip_safe":
        return clip(0.92 * error, -0.22, 0.22)
    if repair == "preload":
        if t == 0:
            return 0.78
        return clip(0.78 * error, -0.42, 0.42)
    if repair == "wrong_boost":
        return clip(1.18 * error, -0.96, 0.96)
    return base


def rollout(domain: dict, repair: str = "none", horizon: int = sim.HORIZON, success_threshold: float = 0.07) -> dict:
    EVAL_COUNTER["rollouts"] += 1
    x = 0.0
    memory = reset_memory()
    actions = []
    trace = []
    for t in range(horizon):
        u = control_action(x, t, repair, memory)
        x_next = step(domain, x, u, memory)
        actions.append(u)
        trace.append((t, x, u, x_next))
        x = x_next
    final_error = abs(sim.TARGET - x)
    action_cost = 0.015 * sum(abs(a) for a in actions)
    overshoot = max(0.0, x - sim.TARGET)
    reward = -final_error - action_cost - 0.35 * overshoot
    success = 1 if final_error <= success_threshold and overshoot <= 0.10 else 0
    return {
        "x_final": x,
        "final_error": final_error,
        "reward": reward,
        "success": success,
        "trace": trace,
        "actions": actions,
    }


def run_sequence(domain: dict, sequence: list[float]) -> list[float]:
    x = 0.0
    memory = reset_memory()
    xs = []
    for u in sequence:
        x = step(domain, x, u, memory)
        xs.append(x)
    return xs


def passive_summary(domain: dict) -> dict:
    cached = domain.get("_passive_summary_cache")
    if cached is not None:
        return cached
    nominal = rollout(domain, "none")
    low = run_sequence(domain, [0.28, 0.28, 0.28])
    trace = nominal["trace"]
    summary = {
        "nominal_final": nominal["x_final"],
        "nominal_error": nominal["final_error"],
        "low_pulse_sum": low[-1],
        "nominal_step1": trace[0][3],
        "nominal_step2": trace[1][3],
        "nominal_step4": trace[3][3],
        "nominal_overshoot": max(0.0, nominal["x_final"] - sim.TARGET),
    }
    domain["_passive_summary_cache"] = summary
    return summary


def probe_features(domain: dict) -> dict:
    cached = domain.get("_probe_features_cache")
    if cached is not None:
        return cached
    low = run_sequence(domain, [0.16, 0.16, 0.16, 0.0])
    high = run_sequence(domain, [0.58, 0.0, 0.0])
    alt = run_sequence(domain, [0.34, -0.34, 0.34, 0.0])
    eps = 1e-9
    features = {
        "low_first": low[0],
        "low_total": low[-1],
        "low_second_jump": low[1] - low[0],
        "high_first": high[0],
        "high_total": high[-1],
        "high_decay": high[0] - high[-1],
        "alt_after_reverse": alt[1],
        "alt_total": alt[-1],
        "high_low_ratio": high[0] / (low[0] + eps),
        "delayed_second_jump": high[1] - high[0],
    }
    domain["_probe_features_cache"] = features
    return features


def classify_mechanism(features: dict) -> str:
    base_features = {
        "low_first": features.get("low_first", 0.0),
        "low_total": features.get("low_total", 0.0),
        "high_first": features.get("high_first", 0.0),
        "high_total": features.get("high_total", 0.0),
        "alt_after_reverse": features.get("alt_after_reverse", 0.0),
        "alt_total": features.get("alt_total", 0.0),
        "high_low_ratio": features.get("high_low_ratio", 0.0),
        "delayed_second_jump": features.get("delayed_second_jump", 0.0),
    }
    return sim.classify_mechanism(base_features)


def corrupt_features(features: dict, rng: random.Random, noise_type: str, level: float) -> dict:
    out = dict(features)
    if level <= 0:
        return out
    if noise_type == "gaussian":
        return {key: value + rng.gauss(0.0, level) for key, value in out.items()}
    if noise_type == "bias":
        signed_bias = rng.choice([-1.0, 1.0]) * level
        for key in out:
            if key.startswith("high") or key.startswith("low"):
                out[key] += signed_bias
        return out
    if noise_type == "dropout":
        for key in list(out):
            if rng.random() < level:
                out[key] = 0.0
        return out
    if noise_type == "quantization":
        quantum = max(1e-6, level)
        return {key: round(value / quantum) * quantum for key, value in out.items()}
    if noise_type == "sign_flip":
        for key in list(out):
            if rng.random() < level:
                out[key] = -out[key]
        return out
    return out


def repair_for_kind(kind: str) -> str:
    return sim.repair_for_kind(kind)


def vector_from_features(features: dict, keys: list[str]) -> list[float]:
    return [float(features.get(key, 0.0)) for key in keys]


def passive_key(summary: dict, mode: str) -> tuple:
    if mode == "coarse":
        return ("success" if summary["nominal_error"] <= 0.07 else "failure",)
    if mode == "medium":
        return (
            "success" if summary["nominal_error"] <= 0.07 else "failure",
            qbin(summary["nominal_final"], 0.10),
            qbin(summary["low_pulse_sum"], 0.10),
        )
    if mode == "fine":
        return (
            "success" if summary["nominal_error"] <= 0.07 else "failure",
            qbin(summary["nominal_final"], 0.04),
            qbin(summary["nominal_error"], 0.04),
            qbin(summary["low_pulse_sum"], 0.04),
            qbin(summary["nominal_step2"], 0.04),
        )
    if mode == "trace":
        return (
            qbin(summary["nominal_step1"], 0.035),
            qbin(summary["nominal_step2"], 0.035),
            qbin(summary["nominal_step4"], 0.035),
            qbin(summary["nominal_final"], 0.035),
            qbin(summary["low_pulse_sum"], 0.035),
        )
    raise ValueError(f"unknown passive key mode: {mode}")


def passive_vector(domain: dict) -> list[float]:
    s = passive_summary(domain)
    return passive_vector_from_summary(s)


def passive_vector_from_summary(s: dict) -> list[float]:
    return [
        s["nominal_final"],
        s["nominal_error"],
        s["low_pulse_sum"],
        s["nominal_step1"],
        s["nominal_step2"],
        s["nominal_step4"],
        s["nominal_overshoot"],
    ]


def nuisance_vector(domain: dict) -> list[float]:
    vec = passive_vector_from_summary(passive_summary(domain))
    return nuisance_vector_from_parts(domain, vec)


def nuisance_vector_from_parts(domain: dict, passive_vec: list[float]) -> list[float]:
    vec = list(passive_vec)
    vec.append(domain.get("lighting", 0.0))
    vec.append(float(domain.get("texture", 0)) / 30.0)
    vec.extend(domain.get("appearance", []))
    return vec


def probe_vector(domain: dict, keys: list[str] | None = None) -> list[float]:
    keys = keys or FULL_PROBE_KEYS
    return vector_from_features(probe_features(domain), keys)


def dist2(a: list[float], b: list[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def best_repair_from_results(results: dict[str, dict]) -> tuple[str, float]:
    best = max(results, key=lambda repair: results[repair]["reward"])
    return best, results[best]["reward"]


def best_single_repair(train_domains: list[dict], repair_library: list[str]) -> str:
    scores = defaultdict(list)
    for domain in train_domains:
        for repair in repair_library:
            scores[repair].append(rollout(domain, repair)["reward"])
    return max(repair_library, key=lambda r: mean(scores[r]))


def train_passive_table(train_domains: list[dict], mode: str, repair_library: list[str]) -> tuple[dict, str]:
    by_bin = defaultdict(lambda: defaultdict(list))
    global_scores = defaultdict(list)
    for domain in train_domains:
        key = passive_key(passive_summary(domain), mode)
        for repair in repair_library:
            result = rollout(domain, repair)
            by_bin[key][repair].append(result["reward"])
            global_scores[repair].append(result["reward"])
    fallback = max(repair_library, key=lambda r: mean(global_scores[r]))
    table = {}
    for key, repair_scores in by_bin.items():
        table[key] = max(repair_library, key=lambda r: mean(repair_scores.get(r, [-9.0])))
    return table, fallback


def train_nn(
    train_domains: list[dict],
    vector_fn,
    label_fn,
) -> list[tuple[list[float], str, str]]:
    memory = []
    for domain in train_domains:
        memory.append((vector_fn(domain), label_fn(domain), domain["kind"]))
    return memory


def nearest(memory: list[tuple[list[float], str, str]], vec: list[float]) -> tuple[str, str, float]:
    best_label = "none"
    best_kind = "unknown"
    best_dist = None
    for train_vec, label, kind in memory:
        d = dist2(vec, train_vec)
        if best_dist is None or d < best_dist:
            best_dist = d
            best_label = label
            best_kind = kind
    return best_label, best_kind, float(best_dist or 0.0)


def train_probe_kind_memory(train_domains: list[dict], keys: list[str]) -> list[tuple[list[float], str, str]]:
    return train_nn(train_domains, lambda d: probe_vector(d, keys), lambda d: d["kind"])


def prepare_training_records(train_domains: list[dict], repair_library: list[str]) -> list[dict]:
    records = []
    for domain in train_domains:
        summary = passive_summary(domain)
        repair_results = {repair: rollout(domain, repair) for repair in repair_library}
        best, best_reward = best_repair_from_results(repair_results)
        passive_vec = passive_vector_from_summary(summary)
        records.append(
            {
                "domain": domain,
                "summary": summary,
                "repair_results": repair_results,
                "best_repair": best,
                "best_reward": best_reward,
                "passive_vec": passive_vec,
                "nuisance_vec": nuisance_vector_from_parts(domain, passive_vec),
                "probe_vec": probe_vector(domain, FULL_PROBE_KEYS),
            }
        )
    return records


def best_single_repair_from_records(records: list[dict], repair_library: list[str]) -> str:
    scores = defaultdict(list)
    for record in records:
        for repair in repair_library:
            scores[repair].append(record["repair_results"][repair]["reward"])
    return max(repair_library, key=lambda r: mean(scores[r]))


def train_passive_table_from_records(records: list[dict], mode: str, repair_library: list[str]) -> tuple[dict, str]:
    by_bin = defaultdict(lambda: defaultdict(list))
    global_scores = defaultdict(list)
    for record in records:
        key = passive_key(record["summary"], mode)
        for repair in repair_library:
            reward = record["repair_results"][repair]["reward"]
            by_bin[key][repair].append(reward)
            global_scores[repair].append(reward)
    fallback = max(repair_library, key=lambda r: mean(global_scores[r]))
    table = {}
    for key, repair_scores in by_bin.items():
        table[key] = max(repair_library, key=lambda r: mean(repair_scores.get(r, [-9.0])))
    return table, fallback


def estimate_reject_threshold(memory: list[tuple[list[float], str, str]]) -> float:
    if len(memory) <= 2:
        return 1.0
    distances = []
    stride = max(1, len(memory) // 300)
    sampled = memory[::stride]
    for vec, _, _ in sampled:
        best = None
        for train_vec, _, _ in memory:
            d = dist2(vec, train_vec)
            if d == 0.0:
                continue
            if best is None or d < best:
                best = d
        if best is not None:
            distances.append(best)
    return max(0.0025, 3.0 * quantile(distances, 0.95))


def choose_gain_sysid(domain: dict) -> str:
    seq = run_sequence(domain, [0.28, 0.28, 0.28])
    estimated_gain = seq[-1] / (0.84 + 1e-9)
    if estimated_gain < 0.73:
        return "gain_comp"
    return "none"


def build_artifacts(train_domains: list[dict], repair_library: list[str], seed: int) -> dict:
    artifacts = {"seed": seed, "repair_library": list(repair_library)}
    records = prepare_training_records(train_domains, repair_library)
    artifacts["robust"] = best_single_repair_from_records(records, repair_library)
    for mode in ["coarse", "medium", "fine", "trace"]:
        table, fallback = train_passive_table_from_records(records, mode, repair_library)
        artifacts[f"passive_{mode}_table"] = table
        artifacts[f"passive_{mode}_fallback"] = fallback
        artifacts[f"passive_{mode}_bins"] = len(table)

    artifacts["passive_vector_nn"] = [
        (record["passive_vec"], record["best_repair"], record["domain"]["kind"]) for record in records
    ]
    artifacts["nuisance_nn"] = [
        (record["nuisance_vec"], record["best_repair"], record["domain"]["kind"]) for record in records
    ]
    artifacts["probe_repair_nn"] = [
        (record["probe_vec"], record["best_repair"], record["domain"]["kind"]) for record in records
    ]
    artifacts["probe_kind_nn"] = [(record["probe_vec"], record["domain"]["kind"], record["domain"]["kind"]) for record in records]
    artifacts["probe_reject_threshold"] = estimate_reject_threshold(artifacts["probe_kind_nn"])
    return artifacts


def repair_limited(desired: str, repair_library: list[str], fallback: str) -> str:
    if desired in repair_library:
        return desired
    if fallback in repair_library:
        return fallback
    if "none" in repair_library:
        return "none"
    return repair_library[0]


def choose_repair(
    method: str,
    domain: dict,
    artifacts: dict,
    repair_library: list[str],
    rng: random.Random,
) -> tuple[str, str, float]:
    fallback = artifacts.get("robust", "none")
    predicted_kind = ""
    distance = 0.0
    if method == "nominal_no_adaptation":
        return repair_limited("none", repair_library, fallback), predicted_kind, distance
    if method == "random_repair":
        return rng.choice(repair_library), predicted_kind, distance
    if method == "single_robust_repair":
        return repair_limited(fallback, repair_library, "none"), predicted_kind, distance
    if method == "passive_stat_coarse":
        table = artifacts["passive_coarse_table"]
        key = passive_key(passive_summary(domain), "coarse")
        return repair_limited(table.get(key, artifacts["passive_coarse_fallback"]), repair_library, fallback), predicted_kind, distance
    if method == "passive_stat_medium":
        table = artifacts["passive_medium_table"]
        key = passive_key(passive_summary(domain), "medium")
        return repair_limited(table.get(key, artifacts["passive_medium_fallback"]), repair_library, fallback), predicted_kind, distance
    if method == "passive_stat_fine":
        table = artifacts["passive_fine_table"]
        key = passive_key(passive_summary(domain), "fine")
        return repair_limited(table.get(key, artifacts["passive_fine_fallback"]), repair_library, fallback), predicted_kind, distance
    if method == "passive_stat_trace":
        table = artifacts["passive_trace_table"]
        key = passive_key(passive_summary(domain), "trace")
        return repair_limited(table.get(key, artifacts["passive_trace_fallback"]), repair_library, fallback), predicted_kind, distance
    if method == "passive_vector_nn":
        repair, predicted_kind, distance = nearest(artifacts["passive_vector_nn"], passive_vector(domain))
        return repair_limited(repair, repair_library, fallback), predicted_kind, distance
    if method == "nuisance_nearest_neighbor":
        repair, predicted_kind, distance = nearest(artifacts["nuisance_nn"], nuisance_vector(domain))
        return repair_limited(repair, repair_library, fallback), predicted_kind, distance
    if method == "probe_nearest_neighbor":
        repair, predicted_kind, distance = nearest(artifacts["probe_repair_nn"], probe_vector(domain, FULL_PROBE_KEYS))
        return repair_limited(repair, repair_library, fallback), predicted_kind, distance
    if method == "gain_only_sysid":
        return repair_limited(choose_gain_sysid(domain), repair_library, fallback), predicted_kind, distance
    if method in ["mechanism_first", "mechanism_first_limited"]:
        predicted_kind = classify_mechanism(probe_features(domain))
        return repair_limited(repair_for_kind(predicted_kind), repair_library, fallback), predicted_kind, distance
    if method == "mechanism_first_reject":
        predicted_kind, _, distance = nearest(artifacts["probe_kind_nn"], probe_vector(domain, FULL_PROBE_KEYS))
        if distance > artifacts["probe_reject_threshold"]:
            return repair_limited("none", repair_library, fallback), "unknown", distance
        return repair_limited(repair_for_kind(predicted_kind), repair_library, fallback), predicted_kind, distance
    if method == "mechanism_oracle":
        if domain["kind"] in KNOWN_KINDS:
            return repair_limited(repair_for_kind(domain["kind"]), repair_library, fallback), domain["kind"], distance
        return repair_limited(fallback, repair_library, "none"), "unknown", distance
    if method == "oracle_best_repair":
        results = {repair: rollout(domain, repair) for repair in repair_library}
        best, _ = best_repair_from_results(results)
        return best, predicted_kind, distance
    raise ValueError(f"unknown method: {method}")


def new_stats() -> dict:
    return {
        "n": 0,
        "success": 0.0,
        "reward": 0.0,
        "final_error": 0.0,
        "regret": 0.0,
        "repair_correct": 0.0,
        "repair_seen": 0.0,
        "mechanism_correct": 0.0,
        "mechanism_seen": 0.0,
        "unknown_reject": 0.0,
        "errors": [],
        "regrets": [],
    }


def add_stats(stats: dict, result: dict, best_reward: float, chosen: str, best: str, predicted_kind: str, true_kind: str) -> None:
    stats["n"] += 1
    stats["success"] += float(result["success"])
    stats["reward"] += float(result["reward"])
    stats["final_error"] += float(result["final_error"])
    regret = max(0.0, best_reward - result["reward"])
    stats["regret"] += regret
    stats["repair_seen"] += 1.0
    stats["repair_correct"] += 1.0 if chosen == best else 0.0
    if predicted_kind:
        stats["mechanism_seen"] += 1.0
        stats["mechanism_correct"] += 1.0 if predicted_kind == true_kind else 0.0
        stats["unknown_reject"] += 1.0 if predicted_kind == "unknown" else 0.0
    stats["errors"].append(float(result["final_error"]))
    stats["regrets"].append(regret)


def finalize_stats(meta: dict, stats: dict) -> dict:
    n = max(1, stats["n"])
    row = dict(meta)
    row.update(
        {
            "n": stats["n"],
            "success_rate": stats["success"] / n,
            "mean_final_error": stats["final_error"] / n,
            "p95_final_error": quantile(stats["errors"], 0.95),
            "mean_reward": stats["reward"] / n,
            "mean_regret": stats["regret"] / n,
            "p95_regret": quantile(stats["regrets"], 0.95),
            "repair_accuracy": stats["repair_correct"] / max(1.0, stats["repair_seen"]),
            "mechanism_accuracy": (
                stats["mechanism_correct"] / stats["mechanism_seen"] if stats["mechanism_seen"] > 0 else ""
            ),
            "unknown_reject_rate": (
                stats["unknown_reject"] / stats["mechanism_seen"] if stats["mechanism_seen"] > 0 else ""
            ),
        }
    )
    return row


def generate_domains(
    seed: int,
    count: int,
    mix: dict[str, float] | None = None,
    fixed_kind: str | None = None,
    severity: float = 1.0,
    nuisance_strength: float = 1.0,
) -> list[dict]:
    rng = random.Random(seed)
    return [
        make_domain(rng, kind=fixed_kind, mix=mix, severity=severity, nuisance_strength=nuisance_strength)
        for _ in range(count)
    ]


def evaluate_condition(
    suite: str,
    condition: str,
    seed: int,
    train_n: int,
    test_n: int,
    methods: list[str],
    repair_library: list[str] | None = None,
    train_mix: dict[str, float] | None = None,
    test_mix: dict[str, float] | None = None,
    fixed_test_kind: str | None = None,
    success_threshold: float = 0.07,
    severity: float = 1.0,
    nuisance_strength: float = 1.0,
) -> tuple[list[dict], list[dict], dict]:
    repair_library = list(repair_library or BASE_REPAIRS)
    train_seed = stable_seed(suite, condition, seed, "train")
    test_seed = stable_seed(suite, condition, seed, "test")
    train_domains = generate_domains(
        train_seed,
        train_n,
        mix=train_mix or MIXES["uniform"],
        severity=severity,
        nuisance_strength=nuisance_strength,
    )
    test_domains = generate_domains(
        test_seed,
        test_n,
        mix=test_mix or MIXES["uniform"],
        fixed_kind=fixed_test_kind,
        severity=severity,
        nuisance_strength=nuisance_strength,
    )
    EVAL_COUNTER["train_domains"] += train_n
    EVAL_COUNTER["test_domains"] += test_n
    artifacts = build_artifacts(train_domains, repair_library, seed)
    stats = defaultdict(new_stats)
    kind_stats = defaultdict(new_stats)

    for idx, domain in enumerate(test_domains):
        repair_results = {
            repair: rollout(domain, repair, success_threshold=success_threshold) for repair in repair_library
        }
        best, best_reward = best_repair_from_results(repair_results)
        true_kind = domain["kind"]
        for method in methods:
            method_rng = random.Random(stable_seed(suite, condition, seed, idx, method))
            if method == "oracle_best_repair":
                chosen, predicted_kind = best, ""
            else:
                chosen, predicted_kind, _ = choose_repair(method, domain, artifacts, repair_library, method_rng)
            if chosen not in repair_results:
                chosen = repair_limited(chosen, repair_library, artifacts.get("robust", "none"))
            result = repair_results[chosen]
            add_stats(stats[method], result, best_reward, chosen, best, predicted_kind, true_kind)
            add_stats(kind_stats[(method, true_kind)], result, best_reward, chosen, best, predicted_kind, true_kind)

    rows = []
    kind_rows = []
    for method, values in stats.items():
        rows.append(
            finalize_stats(
                {
                    "suite": suite,
                    "condition": condition,
                    "seed": seed,
                    "train_n": train_n,
                    "test_n": test_n,
                    "method": method,
                    "repair_library_size": len(repair_library),
                    "success_threshold": success_threshold,
                    "severity": severity,
                    "nuisance_strength": nuisance_strength,
                },
                values,
            )
        )
    for (method, kind), values in kind_stats.items():
        kind_rows.append(
            finalize_stats(
                {
                    "suite": suite,
                    "condition": condition,
                    "seed": seed,
                    "train_n": train_n,
                    "test_n": test_n,
                    "method": method,
                    "mechanism": kind,
                    "repair_library_size": len(repair_library),
                    "success_threshold": success_threshold,
                    "severity": severity,
                    "nuisance_strength": nuisance_strength,
                },
                values,
            )
        )
    artifact_summary = {
        "robust_repair": artifacts["robust"],
        "passive_coarse_bins": artifacts["passive_coarse_bins"],
        "passive_medium_bins": artifacts["passive_medium_bins"],
        "passive_fine_bins": artifacts["passive_fine_bins"],
        "passive_trace_bins": artifacts["passive_trace_bins"],
        "probe_reject_threshold": artifacts["probe_reject_threshold"],
    }
    return rows, kind_rows, artifact_summary


def evaluate_probe_noise(args) -> list[dict]:
    rows = []
    seeds = range(args.seed, args.seed + args.noise_seeds)
    for noise_type, levels in NOISE_LEVELS.items():
        for level in levels:
            for seed in seeds:
                rng = random.Random(stable_seed("noise", noise_type, level, seed))
                stats = new_stats()
                for _ in range(args.noise_test_n):
                    domain = make_domain(rng, mix=MIXES["uniform"])
                    features = corrupt_features(probe_features(domain), rng, noise_type, level)
                    predicted = classify_mechanism(features)
                    repair = repair_for_kind(predicted)
                    results = {rep: rollout(domain, rep) for rep in BASE_REPAIRS}
                    best, best_reward = best_repair_from_results(results)
                    add_stats(stats, results[repair], best_reward, repair, best, predicted, domain["kind"])
                rows.append(
                    finalize_stats(
                        {
                            "suite": "probe_noise_taxonomy",
                            "condition": noise_type,
                            "noise_type": noise_type,
                            "noise_level": level,
                            "seed": seed,
                            "train_n": 0,
                            "test_n": args.noise_test_n,
                            "method": "mechanism_first",
                        },
                        stats,
                    )
                )
    return rows


def evaluate_probe_ablation(args) -> list[dict]:
    rows = []
    seeds = range(args.seed, args.seed + args.ablation_seeds)
    for group_name, keys in PROBE_GROUPS.items():
        for seed in seeds:
            train = generate_domains(stable_seed("probe_ablation", group_name, seed, "train"), args.ablation_train_n)
            test = generate_domains(stable_seed("probe_ablation", group_name, seed, "test"), args.ablation_test_n)
            memory = train_probe_kind_memory(train, keys)
            stats = new_stats()
            for domain in test:
                predicted, _, _ = nearest(memory, probe_vector(domain, keys))
                repair = repair_for_kind(predicted)
                results = {rep: rollout(domain, rep) for rep in BASE_REPAIRS}
                best, best_reward = best_repair_from_results(results)
                add_stats(stats, results[repair], best_reward, repair, best, predicted, domain["kind"])
            rows.append(
                finalize_stats(
                    {
                        "suite": "probe_set_ablation",
                        "condition": group_name,
                        "probe_group": group_name,
                        "feature_count": len(keys),
                        "seed": seed,
                        "train_n": args.ablation_train_n,
                        "test_n": args.ablation_test_n,
                        "method": "probe_subset_nn",
                    },
                    stats,
                )
            )
    return rows


def evaluate_counterexamples(args) -> list[dict]:
    rows = []
    rng = random.Random(stable_seed("counterexamples", args.seed))
    target_pairs = [("gain", "slip"), ("gain", "delay"), ("delay", "slip"), ("slip", "compliance")]
    pair_id = 0
    attempts = 0
    while len(rows) < args.counterexample_pairs and attempts < args.counterexample_pairs * 5000:
        attempts += 1
        kind_a, kind_b = target_pairs[pair_id % len(target_pairs)]
        a = make_domain(rng, kind=kind_a)
        b = make_domain(rng, kind=kind_b)
        summary_a = passive_summary(a)
        summary_b = passive_summary(b)
        if passive_key(summary_a, "coarse") != passive_key(summary_b, "coarse"):
            continue
        results_a = {rep: rollout(a, rep) for rep in BASE_REPAIRS}
        results_b = {rep: rollout(b, rep) for rep in BASE_REPAIRS}
        best_a, reward_a = best_repair_from_results(results_a)
        best_b, reward_b = best_repair_from_results(results_b)
        if best_a == best_b:
            continue
        second_a = max(v["reward"] for r, v in results_a.items() if r != best_a)
        second_b = max(v["reward"] for r, v in results_b.items() if r != best_b)
        margin_a = reward_a - second_a
        margin_b = reward_b - second_b
        if min(margin_a, margin_b) <= 0.005:
            continue
        rows.append(
            {
                "suite": "formal_counterexamples",
                "pair_id": len(rows),
                "kind_a": kind_a,
                "kind_b": kind_b,
                "passive_key_mode": "coarse",
                "shared_passive_key": str(passive_key(summary_a, "coarse")),
                "best_repair_a": best_a,
                "best_repair_b": best_b,
                "margin_a": margin_a,
                "margin_b": margin_b,
                "deterministic_lower_bound": min(margin_a, margin_b),
                "randomized_uniform_lower_bound": 0.5 * min(margin_a, margin_b),
                "nominal_final_a": summary_a["nominal_final"],
                "nominal_final_b": summary_b["nominal_final"],
                "low_pulse_a": summary_a["low_pulse_sum"],
                "low_pulse_b": summary_b["low_pulse_sum"],
            }
        )
        pair_id += 1
    return rows


def aggregate_rows(rows: list[dict], group_fields: list[str], metric_fields: list[str]) -> list[dict]:
    grouped = defaultdict(lambda: defaultdict(list))
    exemplar = {}
    for row in rows:
        key = tuple(row.get(field, "") for field in group_fields)
        exemplar[key] = {field: row.get(field, "") for field in group_fields}
        for metric in metric_fields:
            value = row.get(metric, "")
            if value == "":
                continue
            grouped[key][metric].append(float(value))
    out = []
    for key, metrics in grouped.items():
        row = dict(exemplar[key])
        for metric in metric_fields:
            vals = metrics.get(metric, [])
            if vals:
                row[metric] = mean(vals)
                row[f"{metric}_sem"] = sem(vals)
        out.append(row)
    return out


def maybe_plot():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except Exception as exc:
        print(f"plotting skipped: {exc}")
        return None


def method_sort_key(method: str) -> int:
    if method in PLOT_METHOD_ORDER:
        return PLOT_METHOD_ORDER.index(method)
    return len(PLOT_METHOD_ORDER) + 1


def plot_outputs(all_rows: dict[str, list[dict]]) -> bool:
    plt = maybe_plot()
    if plt is None:
        return False

    main = aggregate_rows(
        all_rows["main_sweep"],
        ["method"],
        ["success_rate", "mean_final_error", "mean_regret", "repair_accuracy"],
    )
    main = sorted(main, key=lambda r: method_sort_key(r["method"]))
    labels = [METHOD_LABEL.get(r["method"], r["method"]) for r in main]
    success = [r["success_rate"] for r in main]
    plt.figure(figsize=(10.6, 4.2))
    plt.bar(range(len(main)), success, color=FIG_COLORS[: len(main)])
    plt.xticks(range(len(main)), labels, rotation=28, ha="right")
    plt.ylabel("success rate")
    plt.ylim(0, 1.04)
    plt.title("Full-scale method comparison")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_main_methods.png"), dpi=240)
    plt.close()

    kind_rows = aggregate_rows(
        all_rows["main_by_mechanism"],
        ["method", "mechanism"],
        ["success_rate", "mean_final_error", "mean_regret"],
    )
    selected = ["passive_stat_fine", "passive_vector_nn", "probe_nearest_neighbor", "mechanism_first", "mechanism_oracle"]
    mechanisms = KNOWN_KINDS
    by_key = {(r["method"], r["mechanism"]): r for r in kind_rows}
    width = 0.16
    x = list(range(len(mechanisms)))
    plt.figure(figsize=(9.4, 4.2))
    for i, method in enumerate(selected):
        vals = [by_key.get((method, kind), {}).get("mean_final_error", 0.0) for kind in mechanisms]
        offs = [v + (i - 2) * width for v in x]
        plt.bar(offs, vals, width=width, label=METHOD_LABEL.get(method, method), color=FIG_COLORS[i])
    plt.xticks(x, mechanisms)
    plt.ylabel("mean final error")
    plt.title("Mechanism-specific error")
    plt.legend(frameon=False, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_by_mechanism.png"), dpi=240)
    plt.close()

    noise = aggregate_rows(
        all_rows["probe_noise_taxonomy"],
        ["noise_type", "noise_level"],
        ["mechanism_accuracy", "success_rate", "mean_final_error"],
    )
    plt.figure(figsize=(8.6, 4.4))
    for i, noise_type in enumerate(NOISE_LEVELS):
        pts = sorted([r for r in noise if r["noise_type"] == noise_type], key=lambda r: float(r["noise_level"]))
        plt.plot(
            [float(r["noise_level"]) for r in pts],
            [float(r["mechanism_accuracy"]) for r in pts],
            marker="o",
            label=noise_type.replace("_", " "),
            color=FIG_COLORS[i],
        )
    plt.xlabel("noise level")
    plt.ylabel("mechanism accuracy")
    plt.ylim(0, 1.04)
    plt.title("Probe noise taxonomy")
    plt.legend(frameon=False, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_probe_noise.png"), dpi=240)
    plt.close()

    ablation = aggregate_rows(
        all_rows["probe_set_ablation"],
        ["probe_group"],
        ["mechanism_accuracy", "success_rate", "mean_final_error"],
    )
    ablation = sorted(ablation, key=lambda r: r["probe_group"])
    plt.figure(figsize=(8.8, 4.0))
    plt.bar(
        range(len(ablation)),
        [float(r["mechanism_accuracy"]) for r in ablation],
        color=FIG_COLORS[: len(ablation)],
    )
    plt.xticks(range(len(ablation)), [r["probe_group"].replace("_", " ") for r in ablation], rotation=25, ha="right")
    plt.ylabel("mechanism accuracy")
    plt.ylim(0, 1.04)
    plt.title("Probe set ablation")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_probe_ablation.png"), dpi=240)
    plt.close()

    passive = aggregate_rows(
        all_rows["passive_summary"],
        ["method"],
        ["success_rate", "mean_final_error", "mean_regret", "repair_accuracy"],
    )
    passive = sorted(passive, key=lambda r: method_sort_key(r["method"]))
    plt.figure(figsize=(8.8, 4.0))
    plt.bar(
        range(len(passive)),
        [float(r["mean_final_error"]) for r in passive],
        color=FIG_COLORS[: len(passive)],
    )
    plt.xticks(range(len(passive)), [METHOD_LABEL.get(r["method"], r["method"]) for r in passive], rotation=25, ha="right")
    plt.ylabel("mean final error")
    plt.title("Passive summary richness")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_passive_richness.png"), dpi=240)
    plt.close()

    mix = aggregate_rows(
        all_rows["mechanism_mix"],
        ["condition", "method"],
        ["success_rate", "mean_final_error"],
    )
    mix_conditions = list(MIXES)
    selected_mix = ["passive_stat_fine", "probe_nearest_neighbor", "mechanism_first", "oracle_best_repair"]
    by_key = {(r["condition"], r["method"]): r for r in mix}
    plt.figure(figsize=(9.0, 4.2))
    for i, method in enumerate(selected_mix):
        vals = [by_key.get((cond, method), {}).get("mean_final_error", 0.0) for cond in mix_conditions]
        plt.plot(range(len(mix_conditions)), vals, marker="o", label=METHOD_LABEL.get(method, method), color=FIG_COLORS[i])
    plt.xticks(range(len(mix_conditions)), [c.replace("_", " ") for c in mix_conditions], rotation=20, ha="right")
    plt.ylabel("mean final error")
    plt.title("Mechanism mixture and imbalance")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_mechanism_mix.png"), dpi=240)
    plt.close()

    scale = aggregate_rows(
        all_rows["scale_sweep"],
        ["train_n", "method"],
        ["success_rate", "mean_final_error"],
    )
    scale_methods = ["passive_stat_fine", "passive_vector_nn", "probe_nearest_neighbor", "mechanism_first"]
    train_sizes = sorted({int(r["train_n"]) for r in scale})
    by_key = {(int(r["train_n"]), r["method"]): r for r in scale}
    plt.figure(figsize=(8.4, 4.2))
    for i, method in enumerate(scale_methods):
        vals = [by_key.get((n, method), {}).get("mean_final_error", 0.0) for n in train_sizes]
        plt.plot(train_sizes, vals, marker="o", label=METHOD_LABEL.get(method, method), color=FIG_COLORS[i])
    plt.xscale("log")
    plt.xlabel("training domains")
    plt.ylabel("mean final error")
    plt.title("Data scale sensitivity")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_data_scale.png"), dpi=240)
    plt.close()

    repair = aggregate_rows(
        all_rows["repair_ablation"],
        ["condition", "method"],
        ["success_rate", "mean_final_error", "mean_regret"],
    )
    repair_conditions = sorted({r["condition"] for r in repair})
    repair_methods = ["mechanism_first_limited", "single_robust_repair", "oracle_best_repair"]
    by_key = {(r["condition"], r["method"]): r for r in repair}
    width = 0.24
    x = list(range(len(repair_conditions)))
    plt.figure(figsize=(9.4, 4.2))
    for i, method in enumerate(repair_methods):
        vals = [by_key.get((cond, method), {}).get("mean_regret", 0.0) for cond in repair_conditions]
        offs = [v + (i - 1) * width for v in x]
        plt.bar(offs, vals, width=width, label=METHOD_LABEL.get(method, method), color=FIG_COLORS[i])
    plt.xticks(x, [c.replace("_", " ") for c in repair_conditions], rotation=22, ha="right")
    plt.ylabel("mean regret")
    plt.title("Repair-library ablation")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_repair_ablation.png"), dpi=240)
    plt.close()

    thresholds = aggregate_rows(
        all_rows["threshold_sensitivity"],
        ["success_threshold", "method"],
        ["success_rate", "mean_final_error"],
    )
    threshold_methods = ["passive_stat_fine", "probe_nearest_neighbor", "mechanism_first", "oracle_best_repair"]
    xs = sorted({float(r["success_threshold"]) for r in thresholds})
    by_key = {(float(r["success_threshold"]), r["method"]): r for r in thresholds}
    plt.figure(figsize=(8.4, 4.2))
    for i, method in enumerate(threshold_methods):
        vals = [by_key.get((xv, method), {}).get("success_rate", 0.0) for xv in xs]
        plt.plot(xs, vals, marker="o", label=METHOD_LABEL.get(method, method), color=FIG_COLORS[i])
    plt.xlabel("success threshold")
    plt.ylabel("success rate")
    plt.ylim(0, 1.04)
    plt.title("Threshold sensitivity")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_threshold_sensitivity.png"), dpi=240)
    plt.close()

    counter = all_rows["formal_counterexamples"]
    if counter:
        show = counter[: min(12, len(counter))]
        plt.figure(figsize=(8.8, 3.8))
        plt.bar(
            range(len(show)),
            [float(r["randomized_uniform_lower_bound"]) for r in show],
            color=FIG_COLORS[: len(show)],
        )
        plt.xticks(range(len(show)), [f"{r['kind_a']}/{r['kind_b']}" for r in show], rotation=25, ha="right")
        plt.ylabel("randomized lower bound")
        plt.title("Aliased passive-statistic counterexamples")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, "full_scale_counterexamples.png"), dpi=240)
        plt.close()

    return True


def tex_float(x, digits=3) -> str:
    if x is None or x == "":
        return "--"
    return f"{float(x):.{digits}f}"


def write_tex_tables(all_rows: dict[str, list[dict]]) -> None:
    main = aggregate_rows(
        all_rows["main_sweep"],
        ["method"],
        ["success_rate", "mean_final_error", "mean_regret", "repair_accuracy", "mechanism_accuracy"],
    )
    main = sorted(main, key=lambda r: method_sort_key(r["method"]))
    lines = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Method & Success & Final error & Regret & Repair acc. \\\\",
        "\\midrule",
    ]
    for row in main:
        lines.append(
            f"{METHOD_LABEL.get(row['method'], row['method'])} & "
            f"{tex_float(row.get('success_rate'))} & {tex_float(row.get('mean_final_error'), 4)} & "
            f"{tex_float(row.get('mean_regret'), 4)} & {tex_float(row.get('repair_accuracy'))} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    with open(os.path.join(TABLE_DIR, "main_aggregate.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    noise = aggregate_rows(
        all_rows["probe_noise_taxonomy"],
        ["noise_type", "noise_level"],
        ["mechanism_accuracy", "success_rate", "mean_final_error"],
    )
    selected_noise = [
        r
        for r in noise
        if r["noise_type"] in ["gaussian", "dropout", "sign_flip"]
        and float(r["noise_level"]) in [0.0, 0.02, 0.04, 0.08, 0.10, 0.20, 0.35]
    ]
    selected_noise = sorted(selected_noise, key=lambda r: (r["noise_type"], float(r["noise_level"])))
    lines = [
        "\\begin{tabular}{llrrr}",
        "\\toprule",
        "Corruption & Level & Mechanism acc. & Success & Final error \\\\",
        "\\midrule",
    ]
    for row in selected_noise[:18]:
        lines.append(
            f"{row['noise_type'].replace('_', ' ')} & {float(row['noise_level']):.2f} & "
            f"{tex_float(row.get('mechanism_accuracy'))} & {tex_float(row.get('success_rate'))} & "
            f"{tex_float(row.get('mean_final_error'), 4)} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    with open(os.path.join(TABLE_DIR, "probe_noise_taxonomy.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    ablation = aggregate_rows(
        all_rows["probe_set_ablation"],
        ["probe_group", "feature_count"],
        ["mechanism_accuracy", "success_rate", "mean_final_error"],
    )
    ablation = sorted(ablation, key=lambda r: r["probe_group"])
    lines = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Probe group & Features & Mechanism acc. & Success & Final error \\\\",
        "\\midrule",
    ]
    for row in ablation:
        lines.append(
            f"{row['probe_group'].replace('_', ' ')} & {int(row['feature_count'])} & "
            f"{tex_float(row.get('mechanism_accuracy'))} & {tex_float(row.get('success_rate'))} & "
            f"{tex_float(row.get('mean_final_error'), 4)} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    with open(os.path.join(TABLE_DIR, "probe_ablation.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    unknown = aggregate_rows(
        all_rows["unknown_mixed"],
        ["condition", "method"],
        ["success_rate", "mean_final_error", "mean_regret", "unknown_reject_rate"],
    )
    selected_methods = {"mechanism_first", "mechanism_first_reject", "oracle_best_repair"}
    unknown = [r for r in unknown if r["method"] in selected_methods]
    unknown = sorted(unknown, key=lambda r: (r["condition"], method_sort_key(r["method"])))
    lines = [
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Condition & Method & Success & Final error & Regret & Reject \\\\",
        "\\midrule",
    ]
    for row in unknown:
        lines.append(
            f"{row['condition'].replace('_', ' ')} & {METHOD_LABEL.get(row['method'], row['method'])} & "
            f"{tex_float(row.get('success_rate'))} & {tex_float(row.get('mean_final_error'), 4)} & "
            f"{tex_float(row.get('mean_regret'), 4)} & {tex_float(row.get('unknown_reject_rate'))} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    with open(os.path.join(TABLE_DIR, "unknown_mixed_controls.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def write_summary_report(all_rows: dict[str, list[dict]], artifact_rows: list[dict], plotted: bool) -> None:
    main = aggregate_rows(
        all_rows["main_sweep"],
        ["method"],
        ["success_rate", "mean_final_error", "mean_regret", "repair_accuracy", "mechanism_accuracy"],
    )
    main_by_method = {r["method"]: r for r in main}
    mechanism_first = main_by_method.get("mechanism_first", {})
    passive_fine = main_by_method.get("passive_stat_fine", {})
    probe_nn = main_by_method.get("probe_nearest_neighbor", {})
    oracle = main_by_method.get("oracle_best_repair", {})
    noise = aggregate_rows(
        all_rows["probe_noise_taxonomy"],
        ["noise_type", "noise_level"],
        ["mechanism_accuracy", "success_rate", "mean_final_error"],
    )
    gaussian_004 = next(
        (r for r in noise if r["noise_type"] == "gaussian" and abs(float(r["noise_level"]) - 0.04) < 1e-9),
        {},
    )
    counter = all_rows["formal_counterexamples"]
    lines = [
        "# Full-Scale Results Summary",
        "",
        "## Artifact Scope",
        "",
        f"- Aggregate CSV suites: {len(all_rows)}.",
        f"- Compact aggregate rows: {sum(len(v) for v in all_rows.values())}.",
        f"- Rollout evaluations counted by runner: {EVAL_COUNTER['rollouts']}.",
        f"- Train domains generated: {EVAL_COUNTER['train_domains']}.",
        f"- Test domains generated: {EVAL_COUNTER['test_domains']}.",
        f"- Figures written: {plotted}.",
        "",
        "## Main Result",
        "",
        "| Method | Success | Final error | Regret | Repair accuracy | Mechanism accuracy |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for method in sorted(main_by_method, key=method_sort_key):
        row = main_by_method[method]
        lines.append(
            f"| {method} | {tex_float(row.get('success_rate'))} | {tex_float(row.get('mean_final_error'), 4)} | "
            f"{tex_float(row.get('mean_regret'), 4)} | {tex_float(row.get('repair_accuracy'))} | "
            f"{tex_float(row.get('mechanism_accuracy'))} |"
        )
    lines.extend(
        [
            "",
            "## Key Interpretation",
            "",
            f"- Mechanism-first final error: {tex_float(mechanism_first.get('mean_final_error'), 4)}.",
            f"- Fine passive-summary final error: {tex_float(passive_fine.get('mean_final_error'), 4)}.",
            f"- Probe-nearest-neighbor final error: {tex_float(probe_nn.get('mean_final_error'), 4)}.",
            f"- Best-repair oracle final error: {tex_float(oracle.get('mean_final_error'), 4)}.",
            f"- Gaussian probe noise at level 0.04: mechanism accuracy {tex_float(gaussian_004.get('mechanism_accuracy'))}, final error {tex_float(gaussian_004.get('mean_final_error'), 4)}.",
            f"- Formal passive-aliasing counterexample rows: {len(counter)}.",
            "",
            "## Generated Files",
            "",
            "- `results/full_scale/main_sweep.csv`",
            "- `results/full_scale/main_by_mechanism.csv`",
            "- `results/full_scale/probe_noise_taxonomy.csv`",
            "- `results/full_scale/probe_set_ablation.csv`",
            "- `results/full_scale/mechanism_mix.csv`",
            "- `results/full_scale/passive_summary.csv`",
            "- `results/full_scale/scale_sweep.csv`",
            "- `results/full_scale/repair_ablation.csv`",
            "- `results/full_scale/unknown_mixed.csv`",
            "- `results/full_scale/threshold_sensitivity.csv`",
            "- `results/full_scale/formal_counterexamples.csv`",
            "",
            "## Artifact Metadata",
            "",
            "| Suite | Condition | Seed | Robust repair | Coarse bins | Fine bins | Trace bins |",
            "| --- | --- | ---: | --- | ---: | ---: | ---: |",
        ]
    )
    for row in artifact_rows[:60]:
        lines.append(
            f"| {row['suite']} | {row['condition']} | {row['seed']} | {row['robust_repair']} | "
            f"{row['passive_coarse_bins']} | {row['passive_fine_bins']} | {row['passive_trace_bins']} |"
        )
    with open(os.path.join(OUT_DIR, "full_scale_results_summary.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    summary_payload = {
        "rollout_evaluations": EVAL_COUNTER["rollouts"],
        "train_domains": EVAL_COUNTER["train_domains"],
        "test_domains": EVAL_COUNTER["test_domains"],
        "main": main_by_method,
        "gaussian_noise_0_04": gaussian_004,
        "counterexample_rows": len(counter),
        "plotted": plotted,
    }
    write_json(os.path.join(OUT_DIR, "full_scale_summary.json"), summary_payload)


def run_full(args) -> dict[str, list[dict]]:
    progress("starting full-scale experiment suite")
    all_rows = {
        "main_sweep": [],
        "main_by_mechanism": [],
        "probe_noise_taxonomy": [],
        "probe_set_ablation": [],
        "mechanism_mix": [],
        "passive_summary": [],
        "scale_sweep": [],
        "repair_ablation": [],
        "unknown_mixed": [],
        "threshold_sensitivity": [],
        "formal_counterexamples": [],
    }
    artifact_rows = []

    if args.suite in ["all", "main_sweep"]:
        for seed in range(args.seed, args.seed + args.main_seeds):
            rows, kind_rows, artifacts = evaluate_condition(
                "main_sweep",
                "uniform",
                seed,
                args.main_train_n,
                args.main_test_n,
                MAIN_METHODS,
            )
            all_rows["main_sweep"].extend(rows)
            all_rows["main_by_mechanism"].extend(kind_rows)
            artifact_rows.append({"suite": "main_sweep", "condition": "uniform", "seed": seed, **artifacts})
        progress(f"completed main_sweep seeds={args.main_seeds}")

    if args.suite in ["all", "probe_noise_taxonomy"]:
        all_rows["probe_noise_taxonomy"] = evaluate_probe_noise(args)
        progress("completed probe_noise_taxonomy")
    if args.suite in ["all", "probe_set_ablation"]:
        all_rows["probe_set_ablation"] = evaluate_probe_ablation(args)
        progress("completed probe_set_ablation")

    mix_methods = [
        "nominal_no_adaptation",
        "single_robust_repair",
        "passive_stat_fine",
        "passive_vector_nn",
        "probe_nearest_neighbor",
        "mechanism_first",
        "oracle_best_repair",
    ]
    if args.suite in ["all", "mechanism_mix"]:
        mix_items = [(condition, mix) for condition, mix in MIXES.items() if not args.condition or args.condition == condition]
        for condition, mix in mix_items:
            for seed in range(args.seed, args.seed + args.mix_seeds):
                rows, _, artifacts = evaluate_condition(
                    "mechanism_mix",
                    condition,
                    seed,
                    args.mix_train_n,
                    args.mix_test_n,
                    mix_methods,
                    train_mix=mix,
                    test_mix=mix,
                )
                all_rows["mechanism_mix"].extend(rows)
                artifact_rows.append({"suite": "mechanism_mix", "condition": condition, "seed": seed, **artifacts})
            progress(f"completed mechanism_mix condition={condition}")

    passive_methods = [
        "passive_stat_coarse",
        "passive_stat_medium",
        "passive_stat_fine",
        "passive_stat_trace",
        "passive_vector_nn",
        "nuisance_nearest_neighbor",
        "probe_nearest_neighbor",
        "mechanism_first",
        "oracle_best_repair",
    ]
    if args.suite in ["all", "passive_summary"]:
        for seed in range(args.seed, args.seed + args.passive_seeds):
            rows, _, artifacts = evaluate_condition(
                "passive_summary",
                "uniform",
                seed,
                args.passive_train_n,
                args.passive_test_n,
                passive_methods,
            )
            all_rows["passive_summary"].extend(rows)
            artifact_rows.append({"suite": "passive_summary", "condition": "uniform", "seed": seed, **artifacts})
        progress("completed passive_summary")

    scale_methods = ["passive_stat_fine", "passive_vector_nn", "probe_nearest_neighbor", "mechanism_first", "oracle_best_repair"]
    if args.suite in ["all", "scale_sweep"]:
        for train_n in args.scale_train_ns:
            if args.condition and args.condition not in [str(train_n), f"train_{train_n}"]:
                continue
            progress(f"starting scale_sweep train_n={train_n}")
            for seed in range(args.seed, args.seed + args.scale_seeds):
                progress(f"starting scale_sweep train_n={train_n} seed={seed}")
                try:
                    rows, _, artifacts = evaluate_condition(
                        "scale_sweep",
                        f"train_{train_n}",
                        seed,
                        train_n,
                        args.scale_test_n,
                        scale_methods,
                    )
                except BaseException as exc:
                    progress(f"failed scale_sweep train_n={train_n} seed={seed} exc={repr(exc)}")
                    raise
                all_rows["scale_sweep"].extend(rows)
                artifact_rows.append({"suite": "scale_sweep", "condition": f"train_{train_n}", "seed": seed, **artifacts})
                progress(f"completed scale_sweep train_n={train_n} seed={seed}")
            progress(f"completed scale_sweep train_n={train_n}")

    repair_conditions = []
    for missing in ["gain_comp", "delay_brake", "slip_safe", "preload"]:
        repair_conditions.append((f"missing_{missing}", [r for r in BASE_REPAIRS if r != missing]))
    repair_conditions.append(("with_wrong_boost", BASE_REPAIRS + ["wrong_boost"]))
    repair_methods = ["single_robust_repair", "mechanism_first_limited", "mechanism_oracle", "oracle_best_repair"]
    if args.suite in ["all", "repair_ablation"]:
        repair_items = [(condition, library) for condition, library in repair_conditions if not args.condition or args.condition == condition]
        for condition, library in repair_items:
            for seed in range(args.seed, args.seed + args.repair_seeds):
                rows, _, artifacts = evaluate_condition(
                    "repair_ablation",
                    condition,
                    seed,
                    args.repair_train_n,
                    args.repair_test_n,
                    repair_methods,
                    repair_library=library,
                )
                all_rows["repair_ablation"].extend(rows)
                artifact_rows.append({"suite": "repair_ablation", "condition": condition, "seed": seed, **artifacts})
            progress(f"completed repair_ablation condition={condition}")

    unknown_methods = [
        "nominal_no_adaptation",
        "single_robust_repair",
        "passive_stat_fine",
        "probe_nearest_neighbor",
        "mechanism_first",
        "mechanism_first_reject",
        "oracle_best_repair",
    ]
    if args.suite in ["all", "unknown_mixed"]:
        for kind in ["friction", "gain_delay", "slip_compliance"]:
            if args.condition and args.condition != kind:
                continue
            for seed in range(args.seed, args.seed + args.unknown_seeds):
                rows, _, artifacts = evaluate_condition(
                    "unknown_mixed",
                    kind,
                    seed,
                    args.unknown_train_n,
                    args.unknown_test_n,
                    unknown_methods,
                    fixed_test_kind=kind,
                )
                all_rows["unknown_mixed"].extend(rows)
                artifact_rows.append({"suite": "unknown_mixed", "condition": kind, "seed": seed, **artifacts})
            progress(f"completed unknown_mixed kind={kind}")

    threshold_methods = [
        "nominal_no_adaptation",
        "passive_stat_fine",
        "probe_nearest_neighbor",
        "mechanism_first",
        "oracle_best_repair",
    ]
    if args.suite in ["all", "threshold_sensitivity"]:
        for threshold in args.thresholds:
            if args.condition and args.condition not in [f"{threshold:.2f}", str(threshold), f"threshold_{threshold:.2f}"]:
                continue
            for seed in range(args.seed, args.seed + args.threshold_seeds):
                rows, _, artifacts = evaluate_condition(
                    "threshold_sensitivity",
                    f"threshold_{threshold:.2f}",
                    seed,
                    args.threshold_train_n,
                    args.threshold_test_n,
                    threshold_methods,
                    success_threshold=threshold,
                )
                all_rows["threshold_sensitivity"].extend(rows)
                artifact_rows.append({"suite": "threshold_sensitivity", "condition": f"{threshold:.2f}", "seed": seed, **artifacts})
            progress(f"completed threshold_sensitivity threshold={threshold:.2f}")

    if args.suite in ["all", "formal_counterexamples"]:
        all_rows["formal_counterexamples"] = evaluate_counterexamples(args)
        progress("completed formal_counterexamples")
    all_rows["_artifact_rows"] = artifact_rows
    return all_rows


def write_all_outputs(all_rows: dict[str, list[dict]]) -> None:
    artifact_rows = all_rows.pop("_artifact_rows")
    field_map = {
        "main_sweep": None,
        "main_by_mechanism": None,
        "probe_noise_taxonomy": None,
        "probe_set_ablation": None,
        "mechanism_mix": None,
        "passive_summary": None,
        "scale_sweep": None,
        "repair_ablation": None,
        "unknown_mixed": None,
        "threshold_sensitivity": None,
        "formal_counterexamples": None,
    }
    for name, fields in field_map.items():
        write_csv(os.path.join(OUT_DIR, f"{name}.csv"), all_rows[name], fields)
    write_csv(os.path.join(OUT_DIR, "artifact_metadata.csv"), artifact_rows)
    plotted = plot_outputs(all_rows)
    write_tex_tables(all_rows)
    write_summary_report(all_rows, artifact_rows, plotted)
    all_rows["_artifact_rows"] = artifact_rows


def safe_suffix(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ["_", "-"] else "_" for ch in value)
    return cleaned.strip("_")


def write_partial_outputs(all_rows: dict[str, list[dict]], suite: str, condition: str = "") -> None:
    artifact_rows = all_rows.pop("_artifact_rows")
    suffix = f"_{safe_suffix(condition)}" if condition else ""
    for name, rows in all_rows.items():
        if rows:
            write_csv(os.path.join(OUT_DIR, f"{name}{suffix}.csv"), rows)
    if artifact_rows:
        write_csv(os.path.join(OUT_DIR, f"artifact_metadata_{suite}{suffix}.csv"), artifact_rows)
    all_rows["_artifact_rows"] = artifact_rows


def read_csv_rows(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_existing_outputs() -> dict[str, list[dict]]:
    names = [
        "main_sweep",
        "main_by_mechanism",
        "probe_noise_taxonomy",
        "probe_set_ablation",
        "mechanism_mix",
        "passive_summary",
        "scale_sweep",
        "repair_ablation",
        "unknown_mixed",
        "threshold_sensitivity",
        "formal_counterexamples",
    ]
    all_rows = {}
    existing = os.listdir(OUT_DIR)
    for name in names:
        part_files = sorted(
            filename
            for filename in existing
            if filename.startswith(f"{name}_") and filename.endswith(".csv") and not filename.startswith("artifact_metadata")
        )
        if part_files:
            rows = []
            for filename in part_files:
                rows.extend(read_csv_rows(os.path.join(OUT_DIR, filename)))
            all_rows[name] = rows
        else:
            all_rows[name] = read_csv_rows(os.path.join(OUT_DIR, f"{name}.csv"))
    artifact_rows = []
    for path in sorted(os.path.join(OUT_DIR, name) for name in os.listdir(OUT_DIR) if name.startswith("artifact_metadata_")):
        artifact_rows.extend(read_csv_rows(path))
    all_rows["_artifact_rows"] = artifact_rows
    return all_rows


def configure_profile(args) -> None:
    if args.profile == "smoke":
        args.main_seeds = 1
        args.main_train_n = 80
        args.main_test_n = 100
        args.noise_seeds = 1
        args.noise_test_n = 80
        args.ablation_seeds = 1
        args.ablation_train_n = 80
        args.ablation_test_n = 80
        args.mix_seeds = 1
        args.mix_train_n = 80
        args.mix_test_n = 80
        args.passive_seeds = 1
        args.passive_train_n = 80
        args.passive_test_n = 80
        args.scale_seeds = 1
        args.scale_train_ns = [40, 80]
        args.scale_test_n = 80
        args.repair_seeds = 1
        args.repair_train_n = 80
        args.repair_test_n = 80
        args.unknown_seeds = 1
        args.unknown_train_n = 80
        args.unknown_test_n = 80
        args.threshold_seeds = 1
        args.threshold_train_n = 80
        args.threshold_test_n = 80
        args.thresholds = [0.05, 0.07]
        args.counterexample_pairs = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["full", "smoke"], default="full")
    parser.add_argument(
        "--suite",
        choices=[
            "all",
            "main_sweep",
            "probe_noise_taxonomy",
            "probe_set_ablation",
            "mechanism_mix",
            "passive_summary",
            "scale_sweep",
            "repair_ablation",
            "unknown_mixed",
            "threshold_sensitivity",
            "formal_counterexamples",
            "finalize",
        ],
        default="all",
    )
    parser.add_argument("--condition", default="", help="Optional condition filter for condition-split suite runs.")
    parser.add_argument("--seed", type=int, default=7100)
    parser.add_argument("--main-seeds", type=int, default=10)
    parser.add_argument("--main-train-n", type=int, default=900)
    parser.add_argument("--main-test-n", type=int, default=1200)
    parser.add_argument("--noise-seeds", type=int, default=8)
    parser.add_argument("--noise-test-n", type=int, default=1100)
    parser.add_argument("--ablation-seeds", type=int, default=8)
    parser.add_argument("--ablation-train-n", type=int, default=800)
    parser.add_argument("--ablation-test-n", type=int, default=1100)
    parser.add_argument("--mix-seeds", type=int, default=7)
    parser.add_argument("--mix-train-n", type=int, default=800)
    parser.add_argument("--mix-test-n", type=int, default=1100)
    parser.add_argument("--passive-seeds", type=int, default=8)
    parser.add_argument("--passive-train-n", type=int, default=1000)
    parser.add_argument("--passive-test-n", type=int, default=1100)
    parser.add_argument("--scale-seeds", type=int, default=6)
    parser.add_argument("--scale-train-ns", type=int, nargs="+", default=[60, 120, 250, 500, 1000, 1800])
    parser.add_argument("--scale-test-n", type=int, default=900)
    parser.add_argument("--repair-seeds", type=int, default=7)
    parser.add_argument("--repair-train-n", type=int, default=800)
    parser.add_argument("--repair-test-n", type=int, default=1100)
    parser.add_argument("--unknown-seeds", type=int, default=7)
    parser.add_argument("--unknown-train-n", type=int, default=800)
    parser.add_argument("--unknown-test-n", type=int, default=1100)
    parser.add_argument("--threshold-seeds", type=int, default=6)
    parser.add_argument("--threshold-train-n", type=int, default=800)
    parser.add_argument("--threshold-test-n", type=int, default=1000)
    parser.add_argument("--thresholds", type=float, nargs="+", default=[0.03, 0.05, 0.07, 0.10, 0.15])
    parser.add_argument("--counterexample-pairs", type=int, default=24)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    configure_profile(args)
    ensure_dirs()
    if os.path.exists(PROGRESS_PATH):
        os.remove(PROGRESS_PATH)
    if args.suite == "finalize":
        all_rows = load_existing_outputs()
        write_all_outputs(all_rows)
    else:
        all_rows = run_full(args)
        if args.suite == "all":
            write_all_outputs(all_rows)
        else:
            write_partial_outputs(all_rows, args.suite, args.condition)
    main = aggregate_rows(
        all_rows["main_sweep"],
        ["method"],
        ["success_rate", "mean_final_error", "mean_regret", "repair_accuracy", "mechanism_accuracy"],
    )
    main_by_method = {row["method"]: row for row in main}
    print(
        json.dumps(
            {
                "profile": args.profile,
                "rollouts": EVAL_COUNTER["rollouts"],
                "compact_rows": sum(len(v) for k, v in all_rows.items() if not k.startswith("_")),
                "mechanism_first": main_by_method.get("mechanism_first"),
                "passive_stat_fine": main_by_method.get("passive_stat_fine"),
                "oracle_best_repair": main_by_method.get("oracle_best_repair"),
                "out_dir": OUT_DIR,
                "figure_dir": FIG_DIR,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
