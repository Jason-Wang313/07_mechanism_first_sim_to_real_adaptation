# Mechanism-First Sim-to-Real Adaptation

This repository contains the paper artifact for paper `07_mechanism_first_sim_to_real_adaptation`.

## Thesis

The project studies a narrow but important sim-to-real failure mode: adapting to target-domain statistics can be the wrong coordinate when different hidden physical mechanisms share the same passive deployment summary but require incompatible repairs. The proposed alternative is to run short diagnostic probes that classify the transfer failure into a repair-equivalence class before selecting the controller repair.

## Main Artifacts

- `docs/related_work_matrix.csv`: 1500-paper landscape matrix.
- `docs/literature_map.md`: field map, hidden assumptions, and candidate directions.
- `docs/hostile_prior_work.md`: 100-paper hostile prior-work set.
- `docs/claims.md`: supported and unsupported claims.
- `experiments/mechanism_first_sim.py`: runnable contact-control simulator.
- `experiments/full_scale_mechanism_first.py`: full-scale suite runner.
- `scripts/summarize_full_scale_results.py`: aggregate/figure/table finalizer.
- `results/full_scale/`: compact full-scale CSVs, generated tables, figures summary, and formal counterexamples.
- `paper/figures/`: manuscript figures regenerated from full-scale CSVs.
- `paper/main.tex`: final 25-page anonymous ICLR-style paper source.

## Reproduce Evidence

```powershell
python experiments\mechanism_first_sim.py
python experiments\full_scale_mechanism_first.py --profile smoke
python scripts\summarize_full_scale_results.py
python scripts\audit_artifacts.py
```

The original simulator writes aggregate metrics to `results/summary.csv`.
The final full-scale evidence is in `results/full_scale/`; the summary reports
1,151 compact rows, 756,750 represented method-domain evaluations, 101 artifact
metadata rows, and 20 constructive passive-aliasing counterexamples.

## Build Paper

From the `paper` directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The paper uses the official ICLR 2026 style and bibliography files downloaded from the ICLR Master-Template repository.

## Current Readiness

Final full-scale batch artifact: the manuscript compiles to 25 pages and the
canonical final PDF is `C:/Users/wangz/Downloads/07.pdf` after verification.
The claim remains honestly bounded to simulation: mechanism-first repair
coordinates are supported in the closed-library simulator, with explicit probe
noise, missing-repair, and mixed-mechanism failure cases.

Current final export: 25 pages, 1,241,363 bytes, SHA256 `EF54EDF6F2F0396D0C784CF563C8E8957D4253A29CEF0D050A9B99083BF43764`.

VLA-style boxed-link verification:

- Link annotations: 41 total on pages `[(1, 13), (4, 2), (5, 2), (7, 1), (8, 2), (9, 1), (10, 6), (11, 14)]`.
- Annotation colors: green = 33, red = 8, cyan = 0.
- Border widths: `(0, 0, 1)` for all link annotations.
- Visual audit: rendered pages 1, 4, 5, 7, 8, 9, 10, and 11; green citation/URL boxes and red internal-reference boxes are crisp and aligned.
