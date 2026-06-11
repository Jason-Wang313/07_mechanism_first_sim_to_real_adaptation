# Final Audit

## 1. Chosen thesis

Sim-to-real adaptation should sometimes adapt the mechanism of transfer failure rather than the target-domain statistics themselves. A short diagnostic intervention can classify a deployment into a repair-equivalence class before selecting the controller repair.

## 2. Field assumption broken

The broken assumption is that passive domain statistics, randomized-domain embeddings, or target-domain summaries are the right coordinates for adaptation. They can alias domains that require different repairs.

## 3. New central mechanism

The central mechanism is a mechanism-first repair coordinate: diagnostic probe residuals identify a hidden failure mechanism such as gain loss, actuation delay, high-command slip, or compliance, then a repair map selects the controller intervention.

## 4. Genuine novelty

The novelty is not a larger model, more data, a new benchmark, uncertainty, active learning, reinforcement learning, or an LLM planner. The contribution changes the adaptation target from domain/statistic/parameter coordinates to repair-equivalence classes induced by physical failure mechanisms.

## 5. Closest hostile prior work

Closest hostile prior work includes:

- Domain randomization and dynamics randomization: Tobin et al. 2017; Peng et al. 2018; Muratore et al. 2022.
- System identification for sim-to-real locomotion and adaptation: Tan et al. 2018; Yu et al. 2017; Chebotar et al. 2019.
- Domain adaptation for contact-rich assembly: Shi et al. 2023; Yuan et al. 2022.
- Contact/tactile sim-to-real transfer: Ding et al. 2021; Lin et al. 2023.

These works make broad sim-to-real transfer, contact modeling, randomization, alignment, and parameter identification less novel. They leave open repair-mechanism diagnosis under aliased deployment summaries.

## 6. Literature coverage

The run produced:

- `docs/related_work_matrix.csv`: 1500 entries.
- 1000-paper landscape sweep: satisfied by the 1500-row matrix.
- 300-paper serious skim: recorded in `docs/literature_map.md`.
- 240-paper deep-read set: recorded in `docs/literature_map.md`.
- 100-paper hostile prior-work set: recorded in `docs/hostile_prior_work.md`.
- At least 20 hidden assumptions: 25 listed in `docs/literature_map.md`.

The annotations are breadth-oriented and partly automatic, so the paper relies on a smaller manually selected citation set for final claims.

## 7. Proof/formal-claim status if any

The paper proves a small repair-aliasing proposition: if two domains share the same observed statistic but have distinct margin-separated optimal repairs, any deterministic statistic-only adapter incurs regret on one domain, and any randomized statistic-only adapter incurs expected regret at least half the margin under the uniform pair.

This is a boundary lemma for aliased statistics, not a universal impossibility theorem for all passive information.

## 8. Strongest evidence

The strongest evidence is the runnable simulator in `experiments/mechanism_first_sim.py` plus saved outputs in `results/`.

Key rerun results:

- `mechanism_first`: success `1.000`, mean final error `0.0017`.
- `passive_stat_oracle`: success `1.000`, mean final error `0.0076`.
- `single_robust_repair`: success `0.922`, mean final error `0.0226`.
- `gain_only_sysid`: success `0.916`, mean final error `0.0550`.
- `nuisance_nearest_neighbor`: success `0.773`, mean final error `0.0935`.
- `nominal_no_adaptation`: success `0.679`, mean final error `0.0919`.

The probe classifier is perfect on the saved 1200-domain run. The separate `results/aliasing_counterexample.csv` instantiates the formal non-identifiability case.

## 9. Biggest weaknesses

- No hardware validation.
- The simulator is one-dimensional and stylized.
- The mechanism library is closed.
- Probes are hand-designed rather than synthesized.
- The coarse passive-statistic oracle is intentionally representation-limited; the paper must not imply all passive or learned representations fail.
- The literature matrix is broad but partly automatic and should not be treated as perfect manual scholarship.

## 10. Paper-readiness judgment

Workshop. The artifact is complete, runnable, and honestly positioned, but a full ICLR submission would need richer simulation, hardware evidence, or a stronger probe-synthesis result.

## 11. Exact Downloads PDF path

`C:/Users/wangz/Downloads/07.pdf`

## 12. GitHub URL

`https://github.com/Jason-Wang313/07_mechanism_first_sim_to_real_adaptation`

## 13. Visible Desktop PDF copy status

`present`

The orchestrator copied `C:\Users\wangz\Downloads\07.pdf` to `C:\Users\wangz\OneDrive\Desktop\07.pdf` after the child PDF build. Both files have matching size and timestamp.
