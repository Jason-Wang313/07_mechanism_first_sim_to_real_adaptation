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
- `results/`: saved CSV results and plots.
- `results/probe_noise_stress.csv`: v2 diagnostic probe-noise stress.
- `paper/main.tex`: anonymous ICLR-style paper source.

## Reproduce Evidence

```powershell
python experiments\mechanism_first_sim.py
python scripts\audit_artifacts.py
```

The simulator writes aggregate metrics to `results/summary.csv`, mechanism-level metrics to `results/success_by_mechanism.csv`, and figures to `results/*.png`.

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

This is a complete runnable paper artifact, but the evidence is simulation-only. The honest readiness judgment in `docs/final_audit.md` is expected to be `workshop` or `revise` unless hardware validation is added.

## Submission-Hardening v2

The v2 pass adds a probe-noise stress for the mechanism classifier. With clean
hand-designed probes, mechanism-first matches the mechanism oracle. Under
Gaussian probe-feature noise, mechanism accuracy drops to 0.830 at
`sigma=0.04` and 0.503 at `sigma=0.12`; mean final error rises to 0.0294 and
0.1098 respectively. The supported claim is now explicitly conditional on
reliable diagnostic probes.
