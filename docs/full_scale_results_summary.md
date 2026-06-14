# Full-Scale Results Summary

This file records the final Paper 07 full-scale pass. The machine-readable
summary is `results/full_scale/full_scale_summary.json`; the generated
human-readable report is `results/full_scale/full_scale_results_summary.md`.

## Scope

- Compact aggregate rows: 1,151.
- Represented method-domain evaluations: 756,750.
- Artifact metadata rows: 101.
- Constructive passive-aliasing counterexamples: 20.
- Final manuscript: 25 pages.

## Main Results

| Method | Success | Mean final error | Mean regret |
| --- | ---: | ---: | ---: |
| mechanism_first | 1.000 | 0.0018 | 0.0000 |
| oracle_best_repair | 1.000 | 0.0018 | 0.0000 |
| passive_stat_fine | 0.999 | 0.0026 | 0.0014 |
| passive_stat_coarse | 1.000 | 0.0073 | 0.0108 |
| gain_only_sysID | 0.912 | 0.0546 | 0.0784 |
| nuisance_nearest_neighbor | 0.752 | 0.1014 | 0.1148 |
| nominal_no_adaptation | 0.662 | 0.0945 | 0.1030 |

## Boundary Results

- Gaussian probe noise at level 0.04: mechanism accuracy 0.828, final error
  0.0320.
- Alternating-only probe ablation: mechanism accuracy 0.885, final error
  0.0629.
- Gain+delay mixed mechanism: mechanism-first success 0.000, best-repair oracle
  success 1.000.
- Missing delay-brake repair: mechanism-first limited success 0.739.

## Final Judgment

The artifact is final under the batch standard and has enough real content for
the 25-page threshold. The scientific claim remains simulation-only and is
bounded accordingly in the manuscript.
