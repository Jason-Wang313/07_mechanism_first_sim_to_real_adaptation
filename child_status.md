# Child Status - Paper 07

## Current Stage

VLA-style boxed-link hardening complete; final artifact exported and verified at
`C:/Users/wangz/Downloads/07.pdf`.

## Full-Scale Evidence

- Full-scale execution plan written before paper edits:
  `docs/full_scale_execution_plan.md`.
- Main runner: `experiments/full_scale_mechanism_first.py`.
- Standalone finalizer: `scripts/summarize_full_scale_results.py`.
- Full-scale result directory: `results/full_scale/`.
- Compact aggregate rows: 1,151.
- Represented method-domain evaluations: 756,750.
- Artifact metadata rows: 101.
- Constructive passive-aliasing counterexample rows: 20.

## Main Full-Scale Results

- `mechanism_first`: success 1.000, mean final error 0.0018, regret 0.0000.
- `oracle_best_repair`: success 1.000, mean final error 0.0018.
- `passive_stat_fine`: success 0.999, mean final error 0.0026.
- `passive_stat_coarse`: success 1.000, mean final error 0.0073.
- `gain_only_sysid`: success 0.912, mean final error 0.0546.
- `nuisance_nearest_neighbor`: success 0.752, mean final error 0.1014.
- `nominal_no_adaptation`: success 0.662, mean final error 0.0945.
- Gaussian probe noise at level 0.04: mechanism accuracy 0.828, final error 0.0320.

## Verification

- Built with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` from `paper/`.
- Added explicit `hyperref` plus VLA-style boxed-link policy to `paper/main.tex`; the baseline final PDF had no link annotations.
- Copied final verified PDF to `C:/Users/wangz/Downloads/07.pdf` (25 pages, 1,241,363 bytes, SHA256 `EF54EDF6F2F0396D0C784CF563C8E8957D4253A29CEF0D050A9B99083BF43764`).
- Final link inventory: 41 annotations on pages `[(1, 13), (4, 2), (5, 2), (7, 1), (8, 2), (9, 1), (10, 6), (11, 14)]`; colors green = 33, red = 8, cyan = 0; all borders `(0, 0, 1)`.
- Rendered and visually inspected pages 1, 4, 5, 7, 8, 9, 10, and 11; highlighted boxes are crisp and aligned.
- Local `paper/main.pdf` removed after canonical copy.
- No duplicate `C:/Users/wangz/Downloads/7.pdf` was created.
- Log scan found no LaTeX errors, undefined references/citations, or overfull matches.
- PDF text scan found no stale `Submission-hardening`, `workshop`, `v2`, `TODO`,
  `placeholder`, `draft`, `accidental`, or `cleanup` markers.
- MiKTeX printed routine update warnings only.

## Current Limitation

The final artifact is full-scale under the batch standard, but the evidence is
still simulation-only. The manuscript states this explicitly and includes
negative controls for noisy probes, missing repairs, mixed mechanisms, and
out-of-library targets.
