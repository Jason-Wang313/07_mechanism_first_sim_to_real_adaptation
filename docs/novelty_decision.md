# Novelty Decision

## Candidate Directions Considered

### Mechanism-First Repair Coordinates
- Broken assumption: Domain statistics are the right adaptation coordinate.
- New central mechanism: Use short diagnostic interventions to classify transfer failures into intervention-relevant mechanisms before choosing repair.
- Strength: Directly attacks non-identifiability: two domains can share statistics but require opposite repairs.
- Risk: Synthetic evidence may be seen as too narrow unless tied to contact/control failures.

### Counterfactual Contact Probes
- Broken assumption: Passive deployment rollouts are enough for adaptation.
- New central mechanism: Choose small probe actions whose residual signatures separate friction, compliance, delay, and gain mechanisms.
- Strength: Makes observability central rather than adding another estimator.
- Risk: Probe design can look like active learning unless the mechanism/repair link is explicit.

### Repair-Equivalence Classes for Sim-to-Real
- Broken assumption: Parameter accuracy is the right success metric for adaptation.
- New central mechanism: Group domains by the repair they require, even when their physical parameters differ.
- Strength: Changes the target from identifying the world to identifying the intervention.
- Risk: Needs careful distinction from robust control and residual policy switching.

### Failure-Aliasing Lower Bounds
- Broken assumption: Distribution alignment can always recover transfer-relevant invariances.
- New central mechanism: Prove adapters using only passive domain statistics fail under aliased mechanisms, then show diagnostic probes break the alias.
- Strength: Provides an adversarial formal boundary for existing domain adaptation claims.
- Risk: The lower bound must not overclaim beyond the stylized setting.

## Chosen Direction

**Mechanism-first repair coordinates for sim-to-real adaptation.** The paper will argue and demonstrate that the deploy-time object of adaptation should be the failure mechanism that determines the repair, not the full target-domain statistics. A short diagnostic probe exposes mechanism-specific residual signatures; the adapter chooses among incompatible repairs such as gain compensation, delay prediction, slip damping, or compliance preload.

## Why This Is Strongest

The hostile set already covers randomized training, feature alignment, residual correction, online system identification, contact modeling, and broad policy transfer. The chosen direction changes the central variable: it targets repair-equivalence classes induced by physical failure mechanisms. This lets the paper make a precise negative claim about statistic-only adapters under aliased mechanisms and a positive claim about diagnostic mechanisms under few real trials.

## Claims Allowed After Literature Sweep

- Allowed: existing sim-to-real methods often adapt domain distributions, parameters, latent context, or residuals rather than named failure mechanisms.
- Allowed: statistic-only adaptation can be non-identifiable when two mechanisms share the same passive domain summary but require different repairs.
- Allowed if experiments succeed: in the provided toy contact-control simulator, mechanism-first probes select better repairs than domain-statistic baselines under nuisance-heavy shifts.
- Unsupported without hardware: superiority on real robots, broad coverage of all transfer failures, or replacement of domain randomization/system identification in general.
