# Submission Attack Log

## Paper 07 v2

- Attack: The mechanism classifier is perfect because the probes are hand-designed and clean.
  - Response: Added probe-noise stress over five repeats per noise level. Accuracy falls to 0.830 at sigma 0.04 and 0.503 at sigma 0.12.
  - Residual risk: The noise model is still synthetic and does not replace hardware probe validation.
- Attack: Passive baselines are too weak.
  - Response: The paper relies on the formal aliasing proposition for the broad point and keeps the empirical passive oracle as a controlled instantiation, not a field-wide defeat.
- Attack: The method is closed-library.
  - Response: Preserved as a limitation; out-of-library detection is not claimed.
- Attack: No hardware.
  - Response: Terminal decision is workshop-only.

## Artifact Hardening Note

The 2026-06-21 export explicitly installs the visible VLA-v4 boxed-link convention:
green citation/URL boxes, red internal-reference boxes, one-point borders, and no
cyan link boxes in the audited final PDF. The previous final PDF had no link
annotations because active `paper/main.tex` did not load `hyperref`.
