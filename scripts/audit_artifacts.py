import csv
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def count_csv_rows(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def main():
    expected = [
        "docs/related_work_matrix.csv",
        "docs/literature_map.md",
        "docs/hostile_prior_work.md",
        "docs/novelty_boundary_map.md",
        "docs/novelty_decision.md",
        "docs/claims.md",
        "docs/reviewer_attacks.md",
        "docs/final_audit.md",
        "results/summary.csv",
        "results/success_by_mechanism.csv",
        "results/probe_confusion.csv",
        "results/aliasing_counterexample.csv",
        "results/experiment_report.md",
        "experiments/mechanism_first_sim.py",
        "paper/main.tex",
        "paper/references.bib",
        "paper/iclr2026_conference.sty",
        "paper/iclr2026_conference.bst",
    ]
    report = {
        "root": str(ROOT),
        "missing": [],
        "csv_rows": {},
        "paper_pdf_exists": (ROOT / "paper" / "main.pdf").exists(),
        "downloads_pdf_exists": Path("C:/Users/wangz/Downloads/07.pdf").exists(),
    }
    for rel in expected:
        path = ROOT / rel
        if not path.exists():
            report["missing"].append(rel)
        elif path.suffix.lower() == ".csv":
            report["csv_rows"][rel] = count_csv_rows(path)
    out_path = ROOT / "docs" / "artifact_audit.json"
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
