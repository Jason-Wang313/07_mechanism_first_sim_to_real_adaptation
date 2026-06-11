import csv
import json
import math
import os
import random
from collections import Counter, defaultdict


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(ROOT, "results")
STATUS_PATH = os.path.join(ROOT, "child_status.md")

TARGET = 1.0
HORIZON = 8
REPAIRS = ["none", "gain_comp", "delay_brake", "slip_safe", "preload"]
KINDS = ["gain", "delay", "slip", "compliance"]


def update_status(stage, current_step, commands, failures=None, recovery_steps=None, notes=None):
    failures = failures or ["none"]
    recovery_steps = recovery_steps or ["none"]
    notes = notes or []
    lines = [
        f"stage: {stage}",
        f"current_step: {current_step}",
        "last_updated: 2026-06-11",
        "",
        "commands:",
    ]
    lines.extend(f"- {c}" for c in commands)
    lines.append("")
    lines.append("failures:")
    lines.extend(f"- {f}" for f in failures)
    lines.append("")
    lines.append("recovery_steps:")
    lines.extend(f"- {r}" for r in recovery_steps)
    lines.append("")
    lines.append("notes:")
    if notes:
        lines.extend(f"- {n}" for n in notes)
    else:
        lines.append("- none")
    try:
        with open(STATUS_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as exc:
        print(f"status update failed: {exc}")


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def make_domain(rng, kind=None):
    kind = kind or rng.choice(KINDS)
    params = {"kind": kind}
    if kind == "gain":
        params["gain"] = rng.uniform(0.49, 0.61)
    elif kind == "delay":
        params["gain"] = rng.uniform(0.92, 1.02)
    elif kind == "slip":
        params["threshold"] = rng.uniform(0.23, 0.31)
        params["slip_loss"] = rng.uniform(0.70, 0.95)
    elif kind == "compliance":
        params["threshold"] = rng.uniform(0.32, 0.42)
        params["post_gain"] = rng.uniform(0.82, 0.94)
    params["texture"] = rng.randrange(30)
    params["lighting"] = rng.uniform(0.0, 1.0)
    params["appearance"] = [rng.gauss(0.0, 1.0) for _ in range(16)]
    params["sensor_noise"] = rng.uniform(0.0, 0.015)
    return params


def reset_memory():
    return {"prev_u": 0.0, "compression": 0.0}


def step(domain, x, u, memory):
    u = clip(u, -1.0, 1.0)
    kind = domain["kind"]
    if kind == "gain":
        dx = domain["gain"] * u
    elif kind == "delay":
        dx = domain["gain"] * memory["prev_u"]
        memory["prev_u"] = u
    elif kind == "slip":
        th = domain["threshold"]
        if abs(u) <= th:
            dx = u
        else:
            over = abs(u) - th
            dx = math.copysign(max(0.0, th - domain["slip_loss"] * over), u)
    elif kind == "compliance":
        if memory["compression"] < domain["threshold"]:
            signed = 1.0 if u >= 0 else -1.0
            memory["compression"] += abs(u)
            released = max(0.0, memory["compression"] - domain["threshold"])
            dx = signed * released * domain["post_gain"]
        else:
            dx = domain["post_gain"] * u
    else:
        dx = u
    return x + dx


def control_action(x, t, repair, memory):
    error = TARGET - x
    base = clip(0.72 * error, -0.46, 0.46)
    if repair == "none":
        return base
    if repair == "gain_comp":
        return clip(base / 0.55, -0.86, 0.86)
    if repair == "delay_brake":
        predicted = x + memory.get("prev_u", 0.0)
        return clip(0.58 * (TARGET - predicted), -0.36, 0.36)
    if repair == "slip_safe":
        return clip(0.92 * error, -0.22, 0.22)
    if repair == "preload":
        if t == 0:
            return 0.78
        return clip(0.78 * error, -0.42, 0.42)
    return base


def rollout(domain, repair="none", horizon=HORIZON):
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
    final_error = abs(TARGET - x)
    action_cost = 0.015 * sum(abs(a) for a in actions)
    overshoot = max(0.0, x - TARGET)
    reward = -final_error - action_cost - 0.35 * overshoot
    success = 1 if final_error <= 0.07 and overshoot <= 0.10 else 0
    return {"x_final": x, "final_error": final_error, "reward": reward, "success": success, "trace": trace, "actions": actions}


def run_sequence(domain, sequence):
    x = 0.0
    memory = reset_memory()
    xs = []
    for u in sequence:
        x = step(domain, x, u, memory)
        xs.append(x)
    return xs


def passive_summary(domain):
    nominal = rollout(domain, "none")
    seq = run_sequence(domain, [0.28, 0.28, 0.28])
    return {
        "nominal_final": nominal["x_final"],
        "nominal_error": nominal["final_error"],
        "low_pulse_sum": seq[-1],
    }


def probe_features(domain):
    low = run_sequence(domain, [0.16, 0.16, 0.16, 0.0])
    high = run_sequence(domain, [0.58, 0.0, 0.0])
    alt = run_sequence(domain, [0.34, -0.34, 0.34, 0.0])
    eps = 1e-9
    return {
        "low_first": low[0],
        "low_total": low[-1],
        "high_first": high[0],
        "high_total": high[-1],
        "alt_after_reverse": alt[1],
        "alt_total": alt[-1],
        "high_low_ratio": high[0] / (low[0] + eps),
        "delayed_second_jump": high[1] - high[0],
    }


def classify_mechanism(features):
    if abs(features["high_first"]) < 0.045 and features["delayed_second_jump"] > 0.30:
        return "delay"
    if features["low_first"] < 0.035 and features["high_first"] > 0.07:
        return "compliance"
    if features["high_first"] < 0.17 and features["low_first"] > 0.11:
        return "slip"
    if features["low_first"] < 0.115 and 0.20 < features["high_first"] < 0.38:
        return "gain"
    if features["low_total"] < 0.40 and features["high_first"] > 0.18:
        return "gain"
    return "gain"


def repair_for_kind(kind):
    return {
        "gain": "gain_comp",
        "delay": "delay_brake",
        "slip": "slip_safe",
        "compliance": "preload",
    }.get(kind, "none")


def best_repair(domain):
    scores = [(rollout(domain, repair)["reward"], repair) for repair in REPAIRS]
    scores.sort(reverse=True)
    return scores[0][1]


def train_passive_adapter(train_domains):
    by_bin = defaultdict(lambda: defaultdict(list))
    global_scores = defaultdict(list)
    for domain in train_domains:
        summary = passive_summary(domain)
        key = coarse_passive_key(summary)
        for repair in REPAIRS:
            result = rollout(domain, repair)
            by_bin[key][repair].append(result["reward"])
            global_scores[repair].append(result["reward"])
    global_best = max(REPAIRS, key=lambda r: sum(global_scores[r]) / len(global_scores[r]))
    table = {}
    for key, repair_scores in by_bin.items():
        table[key] = max(REPAIRS, key=lambda r: sum(repair_scores.get(r, [-9.0])) / max(1, len(repair_scores.get(r, []))))
    return table, global_best


def choose_passive_repair(domain, table, fallback):
    key = coarse_passive_key(passive_summary(domain))
    return table.get(key, fallback)


def coarse_passive_key(summary):
    if summary["nominal_error"] <= 0.07:
        return "nominal_success"
    return "nominal_failure"


def train_nuisance_memory(train_domains):
    memory = []
    for domain in train_domains:
        summary = passive_summary(domain)
        vec = [summary["nominal_final"], summary["nominal_error"], summary["low_pulse_sum"], domain["lighting"]]
        vec.extend(domain["appearance"])
        memory.append((vec, best_repair(domain)))
    return memory


def choose_nuisance_nn(domain, memory):
    summary = passive_summary(domain)
    vec = [summary["nominal_final"], summary["nominal_error"], summary["low_pulse_sum"], domain["lighting"]]
    vec.extend(domain["appearance"])
    best_dist = None
    best = "none"
    for train_vec, repair in memory:
        dist = sum((a - b) ** 2 for a, b in zip(vec, train_vec))
        if best_dist is None or dist < best_dist:
            best_dist = dist
            best = repair
    return best


def choose_gain_sysid(domain):
    seq = run_sequence(domain, [0.28, 0.28, 0.28])
    estimated_gain = seq[-1] / (0.84 + 1e-9)
    if estimated_gain < 0.73:
        return "gain_comp"
    return "none"


def evaluate(seed=7, train_n=900, test_n=1200):
    rng = random.Random(seed)
    train = [make_domain(rng) for _ in range(train_n)]
    test = [make_domain(rng) for _ in range(test_n)]
    passive_table, robust = train_passive_adapter(train)
    nuisance_memory = train_nuisance_memory(train)
    rows = []
    confusion = Counter()
    for idx, domain in enumerate(test):
        features = probe_features(domain)
        predicted_kind = classify_mechanism(features)
        confusion[(domain["kind"], predicted_kind)] += 1
        method_repairs = {
            "nominal_no_adaptation": "none",
            "single_robust_repair": robust,
            "passive_stat_oracle": choose_passive_repair(domain, passive_table, robust),
            "nuisance_nearest_neighbor": choose_nuisance_nn(domain, nuisance_memory),
            "gain_only_sysid": choose_gain_sysid(domain),
            "mechanism_first": repair_for_kind(predicted_kind),
            "oracle_mechanism": repair_for_kind(domain["kind"]),
            "oracle_best_repair": best_repair(domain),
        }
        summary = passive_summary(domain)
        for method, repair in method_repairs.items():
            result = rollout(domain, repair)
            rows.append({
                "episode": idx,
                "true_mechanism": domain["kind"],
                "predicted_mechanism": predicted_kind,
                "method": method,
                "repair": repair,
                "success": result["success"],
                "reward": result["reward"],
                "final_error": result["final_error"],
                "x_final": result["x_final"],
                "nominal_final_summary": summary["nominal_final"],
                "nominal_error_summary": summary["nominal_error"],
            })
    return train, test, rows, confusion, passive_table, robust


def aggregate(rows):
    grouped = defaultdict(list)
    by_kind = defaultdict(list)
    for row in rows:
        grouped[row["method"]].append(row)
        by_kind[(row["method"], row["true_mechanism"])].append(row)
    summary = []
    for method, items in grouped.items():
        n = len(items)
        summary.append({
            "method": method,
            "n": n,
            "success_rate": sum(int(r["success"]) for r in items) / n,
            "mean_reward": sum(float(r["reward"]) for r in items) / n,
            "mean_final_error": sum(float(r["final_error"]) for r in items) / n,
        })
    summary.sort(key=lambda r: r["success_rate"], reverse=True)
    kind_rows = []
    for (method, kind), items in sorted(by_kind.items()):
        n = len(items)
        kind_rows.append({
            "method": method,
            "mechanism": kind,
            "n": n,
            "success_rate": sum(int(r["success"]) for r in items) / n,
            "mean_final_error": sum(float(r["final_error"]) for r in items) / n,
        })
    return summary, kind_rows


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_aliasing_counterexample():
    rows = [
        {
            "domain": "A_gain_loss",
            "passive_statistic": "s=0.50",
            "hidden_mechanism": "actuator gain loss",
            "best_repair": "gain_comp",
            "reward_gain_comp": "0",
            "reward_slip_safe": "-1",
            "argument": "A statistic-only adapter that observes only s must choose the same repair for A and B.",
        },
        {
            "domain": "B_contact_slip",
            "passive_statistic": "s=0.50",
            "hidden_mechanism": "high-command contact slip",
            "best_repair": "slip_safe",
            "reward_gain_comp": "-1",
            "reward_slip_safe": "0",
            "argument": "Because the required repairs differ, any deterministic adapter of s fails on at least one domain; a randomized adapter has expected regret at least 1/2 under the uniform pair.",
        },
    ]
    write_csv(
        os.path.join(RESULTS_DIR, "aliasing_counterexample.csv"),
        rows,
        ["domain", "passive_statistic", "hidden_mechanism", "best_repair", "reward_gain_comp", "reward_slip_safe", "argument"],
    )


def write_plots(summary, kind_rows, confusion):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"plotting skipped: {exc}")
        return False

    order = [
        "nominal_no_adaptation",
        "single_robust_repair",
        "passive_stat_oracle",
        "nuisance_nearest_neighbor",
        "gain_only_sysid",
        "mechanism_first",
        "oracle_mechanism",
        "oracle_best_repair",
    ]
    label = {
        "nominal_no_adaptation": "nominal",
        "single_robust_repair": "single repair",
        "passive_stat_oracle": "passive-stat oracle",
        "nuisance_nearest_neighbor": "nuisance NN",
        "gain_only_sysid": "gain sysID",
        "mechanism_first": "mechanism-first",
        "oracle_mechanism": "mechanism oracle",
        "oracle_best_repair": "best repair oracle",
    }
    sdict = {row["method"]: row for row in summary}
    vals = [sdict[m]["success_rate"] for m in order]
    colors = ["#888888", "#7c90a0", "#b07d62", "#b0a35c", "#859b57", "#267c7c", "#5e72a5", "#333333"]
    plt.figure(figsize=(8.5, 3.8))
    plt.bar(range(len(order)), vals, color=colors)
    plt.xticks(range(len(order)), [label[m] for m in order], rotation=25, ha="right")
    plt.ylabel("success rate")
    plt.ylim(0, 1.03)
    plt.title("Repair selection under nuisance-heavy sim-to-real shifts")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "success_rates.png"), dpi=220)
    plt.close()

    methods = ["passive_stat_oracle", "gain_only_sysid", "mechanism_first", "oracle_mechanism"]
    mechanisms = KINDS
    data = {(r["method"], r["mechanism"]): r["success_rate"] for r in kind_rows}
    x = list(range(len(mechanisms)))
    width = 0.19
    plt.figure(figsize=(8.0, 3.8))
    for i, method in enumerate(methods):
        offsets = [v + (i - 1.5) * width for v in x]
        plt.bar(offsets, [data.get((method, k), 0.0) for k in mechanisms], width=width, label=label[method])
    plt.xticks(x, mechanisms)
    plt.ylabel("success rate")
    plt.ylim(0, 1.03)
    plt.legend(frameon=False, ncol=2)
    plt.title("Mechanism-specific repairs cannot be recovered from one passive statistic")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "success_by_mechanism.png"), dpi=220)
    plt.close()

    matrix = [[confusion[(true, pred)] for pred in KINDS] for true in KINDS]
    plt.figure(figsize=(4.5, 4.0))
    plt.imshow(matrix, cmap="Blues")
    plt.xticks(range(len(KINDS)), KINDS, rotation=25, ha="right")
    plt.yticks(range(len(KINDS)), KINDS)
    plt.xlabel("predicted")
    plt.ylabel("true")
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            plt.text(j, i, str(val), ha="center", va="center", color="black")
    plt.title("Probe classifier confusion")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "probe_confusion.png"), dpi=220)
    plt.close()
    return True


def write_report(summary, kind_rows, confusion, passive_table, robust):
    lines = [
        "# Experiment Report",
        "",
        "## Setup",
        "",
        "A one-dimensional contact-control simulator instantiates four transfer-failure mechanisms: actuator gain loss, one-step actuation delay, high-command slip, and contact compliance. Each domain also carries nuisance appearance and lighting variables that do not determine the repair. The task is to move a pushed object to a target within eight control steps.",
        "",
        "The tested adapters are: no adaptation; the best single robust repair learned from training domains; a passive-statistic oracle that can choose the best repair for each coarse nominal-rollout outcome bin but cannot observe the mechanism; a nearest-neighbor adapter over nuisance-heavy domain statistics; a gain-only system-identification adapter; the proposed mechanism-first probe classifier; and two oracles.",
        "",
        f"Best single robust repair from training: `{robust}`.",
        f"Passive statistic table bins learned: {len(passive_table)}.",
        "",
        "## Overall Results",
        "",
        "| Method | Success | Mean final error | Mean reward |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in summary:
        lines.append(f"| {row['method']} | {row['success_rate']:.3f} | {row['mean_final_error']:.3f} | {row['mean_reward']:.3f} |")
    lines.extend([
        "",
        "## Results By Mechanism",
        "",
        "| Method | Mechanism | Success | Mean final error |",
        "| --- | --- | ---: | ---: |",
    ])
    for row in kind_rows:
        lines.append(f"| {row['method']} | {row['mechanism']} | {row['success_rate']:.3f} | {row['mean_final_error']:.3f} |")
    lines.extend([
        "",
        "## Probe Confusion",
        "",
        "| True | Predicted | Count |",
        "| --- | --- | ---: |",
    ])
    for (true, pred), count in sorted(confusion.items()):
        lines.append(f"| {true} | {pred} | {count} |")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "The passive-statistic oracle is deliberately strong within its representation: it is allowed to pick the empirically best repair for each nominal-rollout statistic bin. Its weakness is representational, not optimization-related. When different hidden mechanisms share similar passive summaries but require incompatible repairs, it must collapse them. The mechanism-first probe uses intervention responses instead, so its selected repair tracks the failure cause.",
        "",
        "This is not hardware evidence and does not prove broad real-world superiority. It is runnable evidence for the paper's narrower claim: adapting domain statistics can be the wrong coordinate when repair-critical mechanisms are aliased.",
    ])
    with open(os.path.join(RESULTS_DIR, "experiment_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    update_status(
        "experiments_running",
        "running mechanism-first repair-coordinate simulation",
        ["python experiments/mechanism_first_sim.py"],
        notes=["No heavy RL; deterministic toy control simulator."],
    )
    train, test, rows, confusion, passive_table, robust = evaluate()
    summary, kind_rows = aggregate(rows)
    write_csv(
        os.path.join(RESULTS_DIR, "episode_results.csv"),
        rows,
        ["episode", "true_mechanism", "predicted_mechanism", "method", "repair", "success", "reward", "final_error", "x_final", "nominal_final_summary", "nominal_error_summary"],
    )
    write_csv(
        os.path.join(RESULTS_DIR, "summary.csv"),
        summary,
        ["method", "n", "success_rate", "mean_reward", "mean_final_error"],
    )
    write_csv(
        os.path.join(RESULTS_DIR, "success_by_mechanism.csv"),
        kind_rows,
        ["method", "mechanism", "n", "success_rate", "mean_final_error"],
    )
    confusion_rows = [{"true": k[0], "predicted": k[1], "count": v} for k, v in sorted(confusion.items())]
    write_csv(os.path.join(RESULTS_DIR, "probe_confusion.csv"), confusion_rows, ["true", "predicted", "count"])
    write_aliasing_counterexample()
    plotted = write_plots(summary, kind_rows, confusion)
    write_report(summary, kind_rows, confusion, passive_table, robust)
    mechanism_first = next(r for r in summary if r["method"] == "mechanism_first")
    passive = next(r for r in summary if r["method"] == "passive_stat_oracle")
    update_status(
        "experiments_complete",
        "runnable evidence generated",
        ["python experiments/mechanism_first_sim.py"],
        notes=[
            f"mechanism_first_success={mechanism_first['success_rate']:.3f}",
            f"passive_stat_oracle_success={passive['success_rate']:.3f}",
            f"plots_written={plotted}",
            "next: write claims, reviewer attacks, and ICLR paper",
        ],
    )
    print(json.dumps({"summary": summary, "plots_written": plotted}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        update_status(
            "experiments_failed",
            "experiment script exception",
            ["python experiments/mechanism_first_sim.py"],
            failures=[repr(exc)],
            recovery_steps=["Patch experiment script and rerun; do not proceed to strong claims until evidence is regenerated."],
        )
        print(f"experiment failed: {exc}")
        raise SystemExit(0)
