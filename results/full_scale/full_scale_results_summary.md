# Full-Scale Results Summary

## Artifact Scope

- Aggregate CSV suites: 11.
- Compact aggregate rows: 1151.
- Method-domain evaluations represented by aggregate rows: 756750.
- Artifact metadata rows: 101.
- Formal passive-aliasing counterexample rows: 20.

## Main Result

| Method | Success | Final error | Regret | Repair accuracy | Mechanism accuracy |
| --- | ---: | ---: | ---: | ---: | ---: |
| nominal_no_adaptation | 0.662 | 0.0945 | 0.1030 | 0.000 | -- |
| random_repair | 0.728 | 0.0972 | 0.1104 | 0.206 | -- |
| single_robust_repair | 0.930 | 0.0213 | 0.0210 | 0.259 | -- |
| passive_stat_coarse | 1.000 | 0.0073 | 0.0108 | 0.506 | -- |
| passive_stat_medium | 1.000 | 0.0018 | 0.0007 | 0.837 | -- |
| passive_stat_fine | 0.999 | 0.0026 | 0.0014 | 0.900 | -- |
| passive_vector_nn | 1.000 | 0.0018 | 0.0000 | 1.000 | 1.000 |
| nuisance_nearest_neighbor | 0.752 | 0.1014 | 0.1148 | 0.294 | 0.294 |
| probe_nearest_neighbor | 1.000 | 0.0018 | 0.0000 | 1.000 | 1.000 |
| gain_only_sysid | 0.912 | 0.0546 | 0.0784 | 0.246 | -- |
| mechanism_first | 1.000 | 0.0018 | 0.0000 | 1.000 | 1.000 |
| mechanism_oracle | 1.000 | 0.0018 | 0.0000 | 1.000 | 1.000 |
| oracle_best_repair | 1.000 | 0.0018 | 0.0000 | 1.000 | -- |

## Key Interpretation

- Mechanism-first final error: 0.0018.
- Fine passive-summary final error: 0.0026.
- Probe-nearest-neighbor final error: 0.0018.
- Best-repair oracle final error: 0.0018.
- Gaussian probe noise at level 0.04: mechanism accuracy 0.828, final error 0.0320.

## Generated Files

- `results/full_scale/main_sweep.csv` or condition-split `main_sweep_*.csv` parts
- `results/full_scale/main_by_mechanism.csv` or condition-split `main_by_mechanism_*.csv` parts
- `results/full_scale/probe_noise_taxonomy.csv` or condition-split `probe_noise_taxonomy_*.csv` parts
- `results/full_scale/probe_set_ablation.csv` or condition-split `probe_set_ablation_*.csv` parts
- `results/full_scale/mechanism_mix.csv` or condition-split `mechanism_mix_*.csv` parts
- `results/full_scale/passive_summary.csv` or condition-split `passive_summary_*.csv` parts
- `results/full_scale/scale_sweep.csv` or condition-split `scale_sweep_*.csv` parts
- `results/full_scale/repair_ablation.csv` or condition-split `repair_ablation_*.csv` parts
- `results/full_scale/unknown_mixed.csv` or condition-split `unknown_mixed_*.csv` parts
- `results/full_scale/threshold_sensitivity.csv` or condition-split `threshold_sensitivity_*.csv` parts
- `results/full_scale/formal_counterexamples.csv` or condition-split `formal_counterexamples_*.csv` parts
