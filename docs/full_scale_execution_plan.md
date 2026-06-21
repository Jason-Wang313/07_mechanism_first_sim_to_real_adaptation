# Full-Scale Execution Plan

Paper 07: Mechanism-First Sim-to-Real Adaptation

## Current Claim

The current paper claims that sim-to-real adaptation should sometimes target the mechanism of transfer failure rather than passive target-domain statistics. In the existing contact-control simulator, hidden target mechanisms include actuator gain loss, one-step delay, high-command slip, and contact compliance. A short diagnostic probe sequence maps the target domain to a repair-equivalence class before selecting a controller repair.

The existing artifact is a 6-page manuscript. Its strongest result is that mechanism-first repair matches the mechanism oracle in the clean simulator, with mean final error 0.0017 versus 0.0076 for a coarse passive-statistic oracle, 0.0550 for gain-only sysID, 0.0935 for nuisance nearest neighbor, and 0.0919 for no adaptation. The v2 hardening adds diagnostic probe-noise stress: mechanism accuracy drops to 0.830 at probe noise sigma 0.04 and 0.503 at sigma 0.12, with final error rising to 0.0294 and 0.1098.

The mechanism is crisp, but the current paper is too short and narrow. It needs broader mechanism mixes, probe designs, noise types, domain shifts, repair-library ablations, passive-summary controls, threshold sweeps, and failure analyses before it can meet the final batch standard.

## Main Gaps To Close

1. The current PDF is 6 pages; the final manuscript must be at least 25 pages with real scientific content.
2. The existing experiment has one default mechanism distribution, one hand-designed probe set, one passive-statistic binning scheme, and one Gaussian probe-noise stress.
3. The paper needs stronger baselines: richer passive summaries, nearest neighbor over mechanism probes, full repair oracle, partial sysID, robust repair, randomized repair, and wrong-mechanism controls.
4. The paper needs negative controls where mechanism-first should fail: noisy probes, missing probes, out-of-library mechanisms, mixed mechanisms, and ambiguous residual signatures.
5. The paper needs sensitivity studies over probe length, train/test scale, mechanism class imbalance, repair margin, nuisance strength, and success threshold.
6. The final manuscript must remove internal hardening/workshop/version language and read as a final paper.

## Target Experiments

1. Main mechanism sweep
   - Multiple seeds and larger train/test domain counts.
   - Compare no adaptation, single robust repair, passive-statistic adapter, nuisance nearest neighbor, gain-only sysID, mechanism-first, mechanism oracle, best-repair oracle, and randomized repair.
   - Report success, final error, reward, mechanism accuracy, repair accuracy, and regret to best repair.

2. Probe noise taxonomy
   - Gaussian noise, biased noise, dropout, quantization, and adversarial sign flips.
   - Report mechanism accuracy and final error across noise levels.

3. Probe set ablation
   - Low pulses only, high pulses only, alternating pulses only, no high pulse, no alternating pulse, full probe set.
   - Show which probes separate which mechanisms.

4. Mechanism mixture and imbalance
   - Uniform mechanism mix, gain-heavy mix, delay-heavy mix, slip-heavy mix, rare-compliance mix.
   - Test whether passive statistics exploit imbalance and whether mechanism-first remains robust.

5. Passive summary richness
   - Coarse nominal success/failure bins, finer nominal bins, passive rollout vector, nuisance-heavy nearest neighbor, and oracle passive bins.
   - Identify when passive summaries are sufficient and when repair aliasing remains.

6. Train/test scale
   - Sweep training domains and test domains.
   - Check whether mechanism-first is data-efficient because probes are hand-designed, and where nearest neighbor or passive tables catch up.

7. Repair-library ablation
   - Remove each repair from the library.
   - Add a wrong repair.
   - Test whether mechanism classification is useful only when a matching repair exists.

8. Out-of-library and mixed mechanisms
   - Add weak friction drift or combined gain+delay domains.
   - Measure rejection/unknown handling or misclassification cost.

9. Threshold and regret sensitivity
   - Sweep success threshold and report continuous regret/error metrics.
   - Avoid relying on one loose success threshold.

10. Formal counterexample expansion
   - Generate multiple aliased statistic pairs with different margins.
   - Report deterministic and randomized lower-bound cases in compact CSV form.

## Baselines And Comparators

Required methods:

1. Nominal no adaptation.
2. Best single robust repair.
3. Random repair.
4. Passive-statistic table with coarse bins.
5. Passive-statistic table with finer bins.
6. Nuisance nearest neighbor.
7. Probe nearest neighbor.
8. Gain-only sysID.
9. Mechanism-first probe classifier.
10. Mechanism oracle.
11. Best-repair oracle.

## Figures And Tables

Target figures:

1. Main method comparison.
2. Results by mechanism.
3. Probe confusion matrix.
4. Probe noise taxonomy.
5. Probe set ablation.
6. Passive summary richness.
7. Mechanism imbalance.
8. Train/test scale.
9. Repair-library ablation.
10. Threshold/regret sensitivity.

Target tables:

1. Main aggregate results.
2. Artifact inventory and compact row counts.
3. Probe-noise taxonomy.
4. Probe ablation by mechanism.
5. Negative controls and what each says.
6. Formal counterexample table.

## Writing Expansion Plan

The final manuscript should:

1. Remove internal hardening/version text.
2. Expand the introduction around adaptation-coordinate mismatch.
3. Deepen related work on domain randomization, sysID, domain adaptation, residual policies, contact-rich transfer, and diagnostic probing.
4. Formalize repair-equivalence classes, repair aliasing, diagnostic residual signatures, and passive-statistic insufficiency.
5. Add algorithmic details for mechanism-first repair.
6. Add full suite descriptions, figures, and tables.
7. Add boundary controls and negative controls.
8. Add real-robot audit protocol and probe-design guidance.
9. Add limitations, failure narratives, and falsification criteria.
10. Add reproducibility appendix and artifact inventory.

## RAM-Light Execution Strategy

1. Write a new full-scale runner that streams compact rows suite by suite.
2. Store aggregate CSVs, summary JSON, and figures only.
3. Do not store raw per-episode traces except small illustrative counterexamples.
4. Use deterministic seeds and modest per-condition domain counts across many conditions.
5. Run suites sequentially and avoid large in-memory matrices.
6. Keep plotting separate from raw simulation loops.

## Final Acceptance Checklist

1. Plan exists before any other paper-07 edits.
2. Full-scale runner produces compact outputs and summary JSON.
3. Final evidence includes positives, boundary controls, negative controls, and failure cases.
4. Manuscript compiles to at least 25 pages.
5. Final log has no unresolved citations/references, fatal errors, or damaging overfull boxes.
6. Extracted PDF text contains full-scale claims and no internal hardening/workshop/version markers.
7. `C:/Users/wangz/Downloads/07.pdf` is overwritten only after final verification.
8. Docs/logs/readme/reproducibility/audits are updated to final full-scale state.
9. Local `paper/main.pdf` is removed after copying the final PDF.
10. Repo is committed, pushed, clean, and upstream-matched before moving to paper 08.

## Post-v3 VLA Link-Hardening Acceptance

Checked: 2026-06-21

- Active `paper/main.tex` now loads `hyperref` and the explicit VLA-style `\hypersetup` policy.
- Final PDF remains 25 pages and is exported to `C:/Users/wangz/Downloads/07.pdf`.
- Final export metadata: 1,241,363 bytes, SHA256 `EF54EDF6F2F0396D0C784CF563C8E8957D4253A29CEF0D050A9B99083BF43764`.
- Link inventory: 41 annotations on pages `[(1, 13), (4, 2), (5, 2), (7, 1), (8, 2), (9, 1), (10, 6), (11, 14)]`; green = 33, red = 8, cyan = 0; all borders `(0, 0, 1)`.
- Visual audit rendered pages 1, 4, 5, 7, 8, 9, 10, and 11 and confirmed crisp, aligned green citation/URL boxes and red internal-reference boxes.
- Local `paper/main.pdf` was removed after the canonical copy.
- No duplicate `C:/Users/wangz/Downloads/7.pdf` was created.
