# Plan: Paper 07 - Mechanism-First Sim-to-Real Adaptation

## Objective
Produce a complete anonymous ICLR-style robotics paper and runnable repository for `07_mechanism_first_sim_to_real_adaptation`, grounded in a broad prior-work audit and centered on a genuinely mechanistic sim-to-real contribution.

## Constraints
- Stay within robotics / embodied physical intelligence.
- Treat the provided seed only as a hypothesis; replace it if the literature makes a stronger direction obvious.
- Avoid weak novelty moves unless they introduce a genuinely new mechanism.
- Maintain `child_status.md` with stages, exact commands, failures, and recovery steps.
- Preserve and reuse useful existing artifacts if present.
- Save final PDF only to `C:/Users/wangz/Downloads/07.pdf`.
- Create and push public GitHub repo `07_mechanism_first_sim_to_real_adaptation`, or document failure.

## Execution Stages
1. Initialize run bookkeeping.
   - Create/update `child_status.md`.
   - Inspect existing repo artifacts without deleting useful work.
   - Record tool availability and any missing dependencies safely.

2. Literature landscape construction.
   - Build `docs/related_work_matrix.csv` with at least 1000 robotics/sim-to-real entries.
   - Use bounded, resumable scripts and cache external metadata.
   - Extract for important papers: problem claimed, mechanism, hidden assumptions, fixed variables, ignored failures, novelty pressure, and openings.

3. Literature narrowing.
   - Produce a 300-paper serious skim, 200-250-paper deep read, and 100-paper hostile prior-work set.
   - Write `docs/literature_map.md` and `docs/hostile_prior_work.md`.
   - Identify at least 20 falseable hidden assumptions in the field box.

4. Novelty decision.
   - Generate candidate paper directions that break hidden assumptions.
   - Select the strongest idea only after adversarial comparison.
   - Write `docs/novelty_boundary_map.md`, `docs/novelty_decision.md`, `docs/claims.md`, and `docs/reviewer_attacks.md`.

5. Runnable evidence.
   - Implement a compact reproducible simulation demonstrating the chosen mechanism.
   - Prefer a small, deterministic experiment with cached outputs and clear progress logs.
   - Generate plots/tables for the paper.

6. Paper writing.
   - Fetch or recreate the latest official ICLR LaTeX template available at runtime.
   - Write an anonymous ICLR-style paper with honest claims and limitations.
   - Sanitize BibTeX/LaTeX for pdfLaTeX.

7. Build and verify.
   - Compile with direct `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` using generous timeouts.
   - Copy the final PDF to `C:/Users/wangz/Downloads/07.pdf` only.
   - If compilation fails, document logs and recovery attempts.

8. Repository publication.
   - Ensure runnable scripts, cached data, paper sources, and docs are committed.
   - Create/push the public GitHub repo `07_mechanism_first_sim_to_real_adaptation`, or document exact blocker.

9. Final audit.
   - Write `docs/final_audit.md` answering all required audit questions.
   - Record whether the visible Desktop PDF copy is pending orchestrator copy.
