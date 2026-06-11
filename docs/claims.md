# Claims

## Chosen Thesis

Sim-to-real adaptation should sometimes target the mechanism of transfer failure rather than the target-domain statistics themselves. In contact-control settings, a short diagnostic intervention can identify a repair-equivalence class such as gain loss, delay, slip, or compliance before the robot spends trials adapting to nuisance-dominated domain summaries.

## Supported Claims

1. **Repair aliasing is possible.** Two target domains can have the same passive deployment statistic while requiring incompatible repairs. The saved counterexample in `results/aliasing_counterexample.csv` gives a two-domain construction where any deterministic statistic-only adapter must choose the same repair for both domains and therefore fails on at least one; a randomized adapter has expected regret at least one half under the uniform pair.

2. **Mechanism-first coordinates are distinct from full system identification.** The proposed adapter does not estimate all physical parameters. It maps a diagnostic residual signature to the repair-equivalence class needed by the controller.

3. **Mechanism probes can be more repair-relevant than nuisance-heavy summaries in the runnable simulator.** In the saved run, `mechanism_first` matches the mechanism oracle and obtains mean final error `0.0017`, while the coarse passive-statistic oracle obtains `0.0076`, nuisance nearest neighbor obtains `0.0935`, gain-only sysID obtains `0.0550`, and no adaptation obtains `0.0919`.

4. **The literature boundary is crowded around other coordinates.** The 1500-row matrix and 100-paper hostile set show many methods centered on randomized simulation, visual/domain alignment, residual policies, parameter identification, or general policy transfer. The surviving contribution is the repair-equivalence coordinate, not a larger policy or more randomization.

5. **The evidence is robotics-relevant but stylized.** The simulator explicitly models embodied control failure mechanisms: actuator gain loss, one-step delay, high-command slip, and contact compliance. It is not hardware evidence.

## Unsupported Or Too Strong

1. The method is not shown to outperform domain randomization or system identification on real robots.
2. The paper does not prove that every sim-to-real failure should be represented by a small named mechanism library.
3. The experiment does not cover perception-heavy, deformable-object, multi-contact, or locomotion-scale deployments.
4. The diagnostic probes are hand-designed, not automatically synthesized.
5. The passive-statistic oracle is intentionally limited to a coarse nominal outcome bin in the main simulator. The formal lower bound, not the empirical baseline alone, carries the broader non-identifiability point.

## Formal Claim Status

The paper can state and prove a small proposition:

If two domains share the same statistic observed by an adapter but have different unique optimal repairs separated by margin `Delta`, any deterministic statistic-only adapter incurs regret at least `Delta` on one of them. A randomized statistic-only adapter incurs expected regret at least `Delta / 2` under the uniform distribution over the two domains.

This is an impossibility result for aliased statistics, not a universal impossibility theorem for all passive information.

## Evidence Files

- `experiments/mechanism_first_sim.py`: runnable simulator.
- `results/summary.csv`: aggregate metrics.
- `results/success_by_mechanism.csv`: mechanism-level metrics.
- `results/probe_confusion.csv`: diagnostic probe confusion matrix.
- `results/aliasing_counterexample.csv`: formal counterexample artifact.
- `results/experiment_report.md`: readable experiment report.
