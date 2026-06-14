import csv
import json
import math
import os
from collections import defaultdict


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "results", "full_scale")
FIG_DIR = os.path.join(ROOT, "paper", "figures")
TABLE_DIR = os.path.join(OUT_DIR, "tables")

NAMES = [
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

METHOD_ORDER = [
    "nominal_no_adaptation",
    "random_repair",
    "single_robust_repair",
    "passive_stat_coarse",
    "passive_stat_medium",
    "passive_stat_fine",
    "passive_stat_trace",
    "passive_vector_nn",
    "nuisance_nearest_neighbor",
    "probe_nearest_neighbor",
    "gain_only_sysid",
    "mechanism_first",
    "mechanism_first_limited",
    "mechanism_first_reject",
    "mechanism_oracle",
    "oracle_best_repair",
]

LABEL = {
    "nominal_no_adaptation": "nominal",
    "random_repair": "random",
    "single_robust_repair": "single robust",
    "passive_stat_coarse": "passive coarse",
    "passive_stat_medium": "passive medium",
    "passive_stat_fine": "passive fine",
    "passive_stat_trace": "passive trace",
    "passive_vector_nn": "passive vector NN",
    "nuisance_nearest_neighbor": "nuisance NN",
    "probe_nearest_neighbor": "probe NN",
    "gain_only_sysid": "gain sysID",
    "mechanism_first": "mechanism-first",
    "mechanism_first_limited": "mechanism-first",
    "mechanism_first_reject": "mechanism reject",
    "mechanism_oracle": "mechanism oracle",
    "oracle_best_repair": "best repair oracle",
}

COLORS = [
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


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        return
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def load_rows(name):
    files = os.listdir(OUT_DIR)
    part_files = sorted(
        filename
        for filename in files
        if filename.startswith(name + "_") and filename.endswith(".csv") and not filename.startswith("artifact_metadata")
    )
    if part_files:
        rows = []
        for filename in part_files:
            rows.extend(read_csv(os.path.join(OUT_DIR, filename)))
        return rows
    return read_csv(os.path.join(OUT_DIR, name + ".csv"))


def load_artifacts():
    rows = []
    for filename in sorted(os.listdir(OUT_DIR)):
        if filename.startswith("artifact_metadata_") and filename.endswith(".csv"):
            rows.extend(read_csv(os.path.join(OUT_DIR, filename)))
    return rows


def fnum(value):
    if value in [None, ""]:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def sem(values):
    values = [v for v in values if v is not None]
    if len(values) <= 1:
        return 0.0
    m = sum(values) / len(values)
    var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(var / len(values))


def aggregate(rows, group_fields, metric_fields):
    grouped = defaultdict(lambda: defaultdict(list))
    examples = {}
    for row in rows:
        key = tuple(row.get(field, "") for field in group_fields)
        examples[key] = {field: row.get(field, "") for field in group_fields}
        for metric in metric_fields:
            value = fnum(row.get(metric, ""))
            if value is not None:
                grouped[key][metric].append(value)
    out = []
    for key, metrics in grouped.items():
        row = dict(examples[key])
        for metric in metric_fields:
            vals = metrics.get(metric, [])
            if vals:
                row[metric] = mean(vals)
                row[metric + "_sem"] = sem(vals)
        out.append(row)
    return out


def order_key(method):
    return METHOD_ORDER.index(method) if method in METHOD_ORDER else len(METHOD_ORDER)


def fmt(value, digits=3):
    if value in [None, ""]:
        return "--"
    return f"{float(value):.{digits}f}"


def write_tex_tables(rows_by_name):
    os.makedirs(TABLE_DIR, exist_ok=True)
    main = aggregate(rows_by_name["main_sweep"], ["method"], ["success_rate", "mean_final_error", "mean_regret", "repair_accuracy"])
    main = sorted(main, key=lambda r: order_key(r["method"]))
    lines = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Method & Success & Final error & Regret & Repair acc. \\\\",
        "\\midrule",
    ]
    for row in main:
        lines.append(
            f"{LABEL.get(row['method'], row['method'])} & {fmt(row.get('success_rate'))} & "
            f"{fmt(row.get('mean_final_error'), 4)} & {fmt(row.get('mean_regret'), 4)} & "
            f"{fmt(row.get('repair_accuracy'))} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    with open(os.path.join(TABLE_DIR, "main_aggregate.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    noise = aggregate(rows_by_name["probe_noise_taxonomy"], ["noise_type", "noise_level"], ["mechanism_accuracy", "success_rate", "mean_final_error"])
    noise = sorted(noise, key=lambda r: (r["noise_type"], float(r["noise_level"])))
    lines = [
        "\\begin{tabular}{llrrr}",
        "\\toprule",
        "Corruption & Level & Mechanism acc. & Success & Final error \\\\",
        "\\midrule",
    ]
    for row in noise[:24]:
        lines.append(
            f"{row['noise_type'].replace('_', ' ')} & {float(row['noise_level']):.2f} & "
            f"{fmt(row.get('mechanism_accuracy'))} & {fmt(row.get('success_rate'))} & "
            f"{fmt(row.get('mean_final_error'), 4)} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    with open(os.path.join(TABLE_DIR, "probe_noise_taxonomy.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    ablation = aggregate(rows_by_name["probe_set_ablation"], ["probe_group", "feature_count"], ["mechanism_accuracy", "success_rate", "mean_final_error"])
    ablation = sorted(ablation, key=lambda r: r["probe_group"])
    lines = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Probe group & Features & Mechanism acc. & Success & Final error \\\\",
        "\\midrule",
    ]
    for row in ablation:
        lines.append(
            f"{row['probe_group'].replace('_', ' ')} & {int(float(row['feature_count']))} & "
            f"{fmt(row.get('mechanism_accuracy'))} & {fmt(row.get('success_rate'))} & "
            f"{fmt(row.get('mean_final_error'), 4)} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    with open(os.path.join(TABLE_DIR, "probe_ablation.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    unknown = aggregate(rows_by_name["unknown_mixed"], ["condition", "method"], ["success_rate", "mean_final_error", "mean_regret", "unknown_reject_rate"])
    unknown = [r for r in unknown if r["method"] in ["mechanism_first", "mechanism_first_reject", "oracle_best_repair"]]
    unknown = sorted(unknown, key=lambda r: (r["condition"], order_key(r["method"])))
    lines = [
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Condition & Method & Success & Final error & Regret & Reject \\\\",
        "\\midrule",
    ]
    for row in unknown:
        lines.append(
            f"{row['condition'].replace('_', ' ')} & {LABEL.get(row['method'], row['method'])} & "
            f"{fmt(row.get('success_rate'))} & {fmt(row.get('mean_final_error'), 4)} & "
            f"{fmt(row.get('mean_regret'), 4)} & {fmt(row.get('unknown_reject_rate'))} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    with open(os.path.join(TABLE_DIR, "unknown_mixed_controls.tex"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def plot(rows_by_name):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(FIG_DIR, exist_ok=True)
    main = aggregate(rows_by_name["main_sweep"], ["method"], ["success_rate", "mean_final_error", "mean_regret"])
    main = sorted(main, key=lambda r: order_key(r["method"]))
    plt.figure(figsize=(10.6, 4.2))
    plt.bar(range(len(main)), [r["success_rate"] for r in main], color=COLORS[: len(main)])
    plt.xticks(range(len(main)), [LABEL.get(r["method"], r["method"]) for r in main], rotation=28, ha="right")
    plt.ylabel("success rate")
    plt.ylim(0, 1.04)
    plt.title("Full-scale method comparison")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_main_methods.png"), dpi=240)
    plt.close()

    noise = aggregate(rows_by_name["probe_noise_taxonomy"], ["noise_type", "noise_level"], ["mechanism_accuracy", "success_rate", "mean_final_error"])
    plt.figure(figsize=(8.6, 4.4))
    for i, noise_type in enumerate(sorted({r["noise_type"] for r in noise})):
        pts = sorted([r for r in noise if r["noise_type"] == noise_type], key=lambda r: float(r["noise_level"]))
        plt.plot([float(r["noise_level"]) for r in pts], [r["mechanism_accuracy"] for r in pts], marker="o", label=noise_type.replace("_", " "), color=COLORS[i % len(COLORS)])
    plt.xlabel("noise level")
    plt.ylabel("mechanism accuracy")
    plt.ylim(0, 1.04)
    plt.title("Probe noise taxonomy")
    plt.legend(frameon=False, ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_probe_noise.png"), dpi=240)
    plt.close()

    ablation = aggregate(rows_by_name["probe_set_ablation"], ["probe_group"], ["mechanism_accuracy", "success_rate", "mean_final_error"])
    ablation = sorted(ablation, key=lambda r: r["probe_group"])
    plt.figure(figsize=(8.8, 4.0))
    plt.bar(range(len(ablation)), [r["mechanism_accuracy"] for r in ablation], color=COLORS[: len(ablation)])
    plt.xticks(range(len(ablation)), [r["probe_group"].replace("_", " ") for r in ablation], rotation=25, ha="right")
    plt.ylabel("mechanism accuracy")
    plt.ylim(0, 1.04)
    plt.title("Probe set ablation")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_probe_ablation.png"), dpi=240)
    plt.close()

    passive = aggregate(rows_by_name["passive_summary"], ["method"], ["mean_final_error", "success_rate", "mean_regret"])
    passive = sorted(passive, key=lambda r: order_key(r["method"]))
    plt.figure(figsize=(9.2, 4.0))
    plt.bar(range(len(passive)), [r["mean_final_error"] for r in passive], color=COLORS[: len(passive)])
    plt.xticks(range(len(passive)), [LABEL.get(r["method"], r["method"]) for r in passive], rotation=25, ha="right")
    plt.ylabel("mean final error")
    plt.title("Passive summary richness")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_passive_richness.png"), dpi=240)
    plt.close()

    mix = aggregate(rows_by_name["mechanism_mix"], ["condition", "method"], ["mean_final_error", "success_rate"])
    conditions = ["uniform", "gain_heavy", "delay_heavy", "slip_heavy", "compliance_rare", "two_mechanism"]
    selected = ["passive_stat_fine", "probe_nearest_neighbor", "mechanism_first", "oracle_best_repair"]
    by_key = {(r["condition"], r["method"]): r for r in mix}
    plt.figure(figsize=(9.0, 4.2))
    for i, method in enumerate(selected):
        vals = [by_key.get((cond, method), {}).get("mean_final_error", 0.0) for cond in conditions]
        plt.plot(range(len(conditions)), vals, marker="o", label=LABEL.get(method, method), color=COLORS[i])
    plt.xticks(range(len(conditions)), [c.replace("_", " ") for c in conditions], rotation=20, ha="right")
    plt.ylabel("mean final error")
    plt.title("Mechanism mixture and imbalance")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_mechanism_mix.png"), dpi=240)
    plt.close()

    scale = aggregate(rows_by_name["scale_sweep"], ["train_n", "method"], ["mean_final_error", "success_rate"])
    train_sizes = sorted({int(float(r["train_n"])) for r in scale})
    scale_methods = ["passive_stat_fine", "passive_vector_nn", "probe_nearest_neighbor", "mechanism_first"]
    by_key = {(int(float(r["train_n"])), r["method"]): r for r in scale}
    plt.figure(figsize=(8.4, 4.2))
    for i, method in enumerate(scale_methods):
        vals = [by_key.get((n, method), {}).get("mean_final_error", 0.0) for n in train_sizes]
        plt.plot(train_sizes, vals, marker="o", label=LABEL.get(method, method), color=COLORS[i])
    plt.xscale("log")
    plt.xlabel("training domains")
    plt.ylabel("mean final error")
    plt.title("Data scale sensitivity")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_data_scale.png"), dpi=240)
    plt.close()

    repair = aggregate(rows_by_name["repair_ablation"], ["condition", "method"], ["mean_regret", "mean_final_error"])
    repair_conditions = sorted({r["condition"] for r in repair})
    repair_methods = ["mechanism_first_limited", "single_robust_repair", "oracle_best_repair"]
    by_key = {(r["condition"], r["method"]): r for r in repair}
    width = 0.24
    plt.figure(figsize=(9.4, 4.2))
    for i, method in enumerate(repair_methods):
        vals = [by_key.get((cond, method), {}).get("mean_regret", 0.0) for cond in repair_conditions]
        xs = [x + (i - 1) * width for x in range(len(repair_conditions))]
        plt.bar(xs, vals, width=width, label=LABEL.get(method, method), color=COLORS[i])
    plt.xticks(range(len(repair_conditions)), [c.replace("_", " ") for c in repair_conditions], rotation=22, ha="right")
    plt.ylabel("mean regret")
    plt.title("Repair-library ablation")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_repair_ablation.png"), dpi=240)
    plt.close()

    threshold = aggregate(rows_by_name["threshold_sensitivity"], ["success_threshold", "method"], ["success_rate"])
    xs = sorted({float(r["success_threshold"]) for r in threshold})
    by_key = {(float(r["success_threshold"]), r["method"]): r for r in threshold}
    plt.figure(figsize=(8.2, 4.0))
    for i, method in enumerate(["nominal_no_adaptation", "passive_stat_fine", "probe_nearest_neighbor", "mechanism_first", "oracle_best_repair"]):
        vals = [by_key.get((xv, method), {}).get("success_rate", 0.0) for xv in xs]
        plt.plot(xs, vals, marker="o", label=LABEL.get(method, method), color=COLORS[i])
    plt.xlabel("success threshold")
    plt.ylabel("success rate")
    plt.ylim(0, 1.04)
    plt.title("Threshold sensitivity")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "full_scale_threshold_sensitivity.png"), dpi=240)
    plt.close()

    counter = rows_by_name["formal_counterexamples"]
    if counter:
        show = counter[:12]
        plt.figure(figsize=(8.8, 3.8))
        plt.bar(range(len(show)), [float(r["randomized_uniform_lower_bound"]) for r in show], color=COLORS[: len(show)])
        plt.xticks(range(len(show)), [f"{r['kind_a']}/{r['kind_b']}" for r in show], rotation=25, ha="right")
        plt.ylabel("randomized lower bound")
        plt.title("Aliased passive-statistic counterexamples")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, "full_scale_counterexamples.png"), dpi=240)
        plt.close()


def write_summary(rows_by_name, artifacts):
    main = aggregate(rows_by_name["main_sweep"], ["method"], ["success_rate", "mean_final_error", "mean_regret", "repair_accuracy", "mechanism_accuracy"])
    main = sorted(main, key=lambda r: order_key(r["method"]))
    main_by_method = {r["method"]: r for r in main}
    noise = aggregate(rows_by_name["probe_noise_taxonomy"], ["noise_type", "noise_level"], ["mechanism_accuracy", "success_rate", "mean_final_error"])
    gaussian_004 = next((r for r in noise if r["noise_type"] == "gaussian" and abs(float(r["noise_level"]) - 0.04) < 1e-9), {})
    compact_rows = sum(len(v) for v in rows_by_name.values())
    method_domain_rows = 0
    for rows in rows_by_name.values():
        for row in rows:
            n = fnum(row.get("n", ""))
            if n is not None:
                method_domain_rows += int(n)
    lines = [
        "# Full-Scale Results Summary",
        "",
        "## Artifact Scope",
        "",
        f"- Aggregate CSV suites: {len(rows_by_name)}.",
        f"- Compact aggregate rows: {compact_rows}.",
        f"- Method-domain evaluations represented by aggregate rows: {method_domain_rows}.",
        f"- Artifact metadata rows: {len(artifacts)}.",
        f"- Formal passive-aliasing counterexample rows: {len(rows_by_name['formal_counterexamples'])}.",
        "",
        "## Main Result",
        "",
        "| Method | Success | Final error | Regret | Repair accuracy | Mechanism accuracy |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in main:
        lines.append(
            f"| {row['method']} | {fmt(row.get('success_rate'))} | {fmt(row.get('mean_final_error'), 4)} | "
            f"{fmt(row.get('mean_regret'), 4)} | {fmt(row.get('repair_accuracy'))} | {fmt(row.get('mechanism_accuracy'))} |"
        )
    lines += [
        "",
        "## Key Interpretation",
        "",
        f"- Mechanism-first final error: {fmt(main_by_method.get('mechanism_first', {}).get('mean_final_error'), 4)}.",
        f"- Fine passive-summary final error: {fmt(main_by_method.get('passive_stat_fine', {}).get('mean_final_error'), 4)}.",
        f"- Probe-nearest-neighbor final error: {fmt(main_by_method.get('probe_nearest_neighbor', {}).get('mean_final_error'), 4)}.",
        f"- Best-repair oracle final error: {fmt(main_by_method.get('oracle_best_repair', {}).get('mean_final_error'), 4)}.",
        f"- Gaussian probe noise at level 0.04: mechanism accuracy {fmt(gaussian_004.get('mechanism_accuracy'))}, final error {fmt(gaussian_004.get('mean_final_error'), 4)}.",
        "",
        "## Generated Files",
        "",
    ]
    for name in NAMES:
        lines.append(f"- `results/full_scale/{name}.csv` or condition-split `{name}_*.csv` parts")
    with open(os.path.join(OUT_DIR, "full_scale_results_summary.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(OUT_DIR, "full_scale_summary.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "compact_rows": compact_rows,
                "method_domain_evaluations": method_domain_rows,
                "artifact_metadata_rows": len(artifacts),
                "counterexample_rows": len(rows_by_name["formal_counterexamples"]),
                "main": main_by_method,
                "gaussian_noise_0_04": gaussian_004,
            },
            f,
            indent=2,
            sort_keys=True,
        )
        f.write("\n")


def main():
    os.makedirs(TABLE_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)
    rows_by_name = {name: load_rows(name) for name in NAMES}
    artifacts = load_artifacts()
    write_csv(os.path.join(OUT_DIR, "artifact_metadata.csv"), artifacts)
    write_tex_tables(rows_by_name)
    plot(rows_by_name)
    write_summary(rows_by_name, artifacts)
    print(json.dumps({"rows": {k: len(v) for k, v in rows_by_name.items()}, "artifacts": len(artifacts)}, indent=2))


if __name__ == "__main__":
    main()
