# Experiment Report

## Setup

A one-dimensional contact-control simulator instantiates four transfer-failure mechanisms: actuator gain loss, one-step actuation delay, high-command slip, and contact compliance. Each domain also carries nuisance appearance and lighting variables that do not determine the repair. The task is to move a pushed object to a target within eight control steps.

The tested adapters are: no adaptation; the best single robust repair learned from training domains; a passive-statistic oracle that can choose the best repair for each coarse nominal-rollout outcome bin but cannot observe the mechanism; a nearest-neighbor adapter over nuisance-heavy domain statistics; a gain-only system-identification adapter; the proposed mechanism-first probe classifier; and two oracles.

Best single robust repair from training: `delay_brake`.
Passive statistic table bins learned: 2.

## Overall Results

| Method | Success | Mean final error | Mean reward |
| --- | ---: | ---: | ---: |
| passive_stat_oracle | 1.000 | 0.008 | -0.033 |
| mechanism_first | 1.000 | 0.002 | -0.022 |
| oracle_mechanism | 1.000 | 0.002 | -0.022 |
| oracle_best_repair | 1.000 | 0.002 | -0.022 |
| single_robust_repair | 0.922 | 0.023 | -0.044 |
| gain_only_sysid | 0.916 | 0.055 | -0.100 |
| nuisance_nearest_neighbor | 0.773 | 0.093 | -0.128 |
| nominal_no_adaptation | 0.679 | 0.092 | -0.122 |

## Results By Mechanism

| Method | Mechanism | Success | Mean final error |
| --- | --- | ---: | ---: |
| gain_only_sysid | compliance | 1.000 | 0.000 |
| gain_only_sysid | delay | 0.976 | 0.025 |
| gain_only_sysid | gain | 1.000 | 0.000 |
| gain_only_sysid | slip | 0.687 | 0.195 |
| mechanism_first | compliance | 1.000 | 0.000 |
| mechanism_first | delay | 1.000 | 0.007 |
| mechanism_first | gain | 1.000 | 0.000 |
| mechanism_first | slip | 1.000 | 0.000 |
| nominal_no_adaptation | compliance | 1.000 | 0.001 |
| nominal_no_adaptation | delay | 0.000 | 0.198 |
| nominal_no_adaptation | gain | 1.000 | 0.025 |
| nominal_no_adaptation | slip | 0.687 | 0.147 |
| nuisance_nearest_neighbor | compliance | 1.000 | 0.004 |
| nuisance_nearest_neighbor | delay | 0.584 | 0.075 |
| nuisance_nearest_neighbor | gain | 0.797 | 0.035 |
| nuisance_nearest_neighbor | slip | 0.710 | 0.260 |
| oracle_best_repair | compliance | 1.000 | 0.000 |
| oracle_best_repair | delay | 1.000 | 0.007 |
| oracle_best_repair | gain | 1.000 | 0.000 |
| oracle_best_repair | slip | 1.000 | 0.000 |
| oracle_mechanism | compliance | 1.000 | 0.000 |
| oracle_mechanism | delay | 1.000 | 0.007 |
| oracle_mechanism | gain | 1.000 | 0.000 |
| oracle_mechanism | slip | 1.000 | 0.000 |
| passive_stat_oracle | compliance | 1.000 | 0.000 |
| passive_stat_oracle | delay | 1.000 | 0.007 |
| passive_stat_oracle | gain | 1.000 | 0.013 |
| passive_stat_oracle | slip | 1.000 | 0.010 |
| single_robust_repair | compliance | 1.000 | 0.011 |
| single_robust_repair | delay | 1.000 | 0.007 |
| single_robust_repair | gain | 0.705 | 0.063 |
| single_robust_repair | slip | 1.000 | 0.008 |

## Probe Confusion

| True | Predicted | Count |
| --- | --- | ---: |
| compliance | compliance | 294 |
| delay | delay | 291 |
| gain | gain | 315 |
| slip | slip | 300 |

## Interpretation

The passive-statistic oracle is deliberately strong within its representation: it is allowed to pick the empirically best repair for each nominal-rollout statistic bin. Its weakness is representational, not optimization-related. When different hidden mechanisms share similar passive summaries but require incompatible repairs, it must collapse them. The mechanism-first probe uses intervention responses instead, so its selected repair tracks the failure cause.

This is not hardware evidence and does not prove broad real-world superiority. It is runnable evidence for the paper's narrower claim: adapting domain statistics can be the wrong coordinate when repair-critical mechanisms are aliased.
