# Recovery Notes

Attempt 2 failed after useful artifacts were created. The failure was not a missing literature sweep or failed experiment; it was a timed-out diagnostic PowerShell command over `results/episode_results.csv`:

- child log ended with Codex tool router `Exit code: 124`
- launcher recorded `EXIT_CODE 999`
- `C:/Users/wangz/Downloads/07.pdf` was not produced

Valid artifacts to reuse:

- `docs/related_work_matrix.csv`: 1500 rows / 1500 unique titles after title-level de-duplication
- `docs/literature_map.md`
- `docs/hostile_prior_work.md`
- `docs/novelty_boundary_map.md`
- `docs/novelty_decision.md`
- `scripts/fetch_literature.py`
- `data/openalex_literature_raw.jsonl`
- `experiments/mechanism_first_sim.py`
- `results/summary.csv`
- `results/success_by_mechanism.csv`
- `results/probe_confusion.csv`
- `results/aliasing_counterexample.csv`
- `results/episode_results.csv`
- `results/experiment_report.md`
- `results/success_rates.png`
- `results/success_by_mechanism.png`
- `results/probe_confusion.png`

Current evidence facts:

- `mechanism_first` success: 1.000, mean final error 0.0017
- `passive_stat_oracle` success: 1.000, mean final error 0.0060
- `single_robust_repair` success: 0.9225
- `gain_only_sysid` success: 0.9158
- `nuisance_nearest_neighbor` success: 0.7733
- `nominal_no_adaptation` success: 0.6792
- probe confusion is perfect on the saved run

Attempt 2 noticed that the passive-statistic oracle was too strong for a crisp negative claim. On recovery, inspect `experiments/mechanism_first_sim.py` and either:

1. Keep the result and frame the claim around mechanism-first lower final error / fewer nuisance failures, or
2. Patch the simulator so `passive_stat_oracle` only receives coarse passive bins that alias incompatible mechanisms, rerun the script once, and update the report.

Important recovery instructions:

- Do not recollect OpenAlex/literature unless the cached files are missing.
- Do not rerun slow or complex inline PowerShell over CSV files.
- If extra analysis is needed, write a small Python helper script and run it with an explicit generous timeout.
- Avoid inline PowerShell commands with nested quotes, `Group-Object`, `ForEach-Object`, or full `Import-Csv` over large CSVs.
- Continue from evidence to `docs/claims.md`, `docs/reviewer_attacks.md`, paper writing, direct `pdflatex`/`bibtex` build, `C:/Users/wangz/Downloads/07.pdf`, public GitHub repo push, and `docs/final_audit.md`.
