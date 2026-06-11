# Reviewer Attacks

## Likely Attack 1: This Is Just System Identification

**Concern.** The diagnostic probe estimates physical parameters, so the paper is a rebranding of online system identification.

**Response.** The mechanism-first adapter estimates a repair-equivalence class, not a simulator parameter vector. Domains with different numerical parameters can map to the same repair, and domains with similar passive statistics can map to different repairs. The paper should keep this distinction central and avoid claiming parameter estimation novelty.

## Likely Attack 2: The Experiment Is A Toy

**Concern.** A one-dimensional contact-control simulator is too small for an ICLR robotics claim.

**Response.** Agree in limitations. The simulator is evidence for a mechanistic boundary condition and a reproducible counterexample, not evidence of real-robot superiority. The paper-readiness judgment should be workshop/revise rather than full submit unless hardware or richer simulation is added.

## Likely Attack 3: Passive Baselines Are Too Weak

**Concern.** The coarse passive-statistic oracle is representation-limited by construction.

**Response.** The formal proposition is explicitly about representation aliasing: if the statistic aliases repair-critical mechanisms, no optimizer can recover the right repair. The empirical baseline instantiates that setting. The paper must not claim all passive adapters fail; it should claim statistic choice matters and provide a constructive diagnostic alternative.

## Likely Attack 4: Hand-Designed Probes Are Active Learning

**Concern.** Probe actions are just active learning or experiment design.

**Response.** The novelty is not "take active samples"; it is that probes are selected to identify repair mechanisms rather than reduce parameter uncertainty or maximize generic information. The method section should define probes by separation of repair-equivalence classes.

## Likely Attack 5: Mechanism Library May Be Incomplete

**Concern.** Real robots fail through coupled mechanisms not in the library.

**Response.** True. The current method is a closed-library adapter. The paper should flag out-of-library detection as future work and avoid open-world claims.

## Likely Attack 6: Nuisance Nearest Neighbor Is A Strawman

**Concern.** A better representation learner could ignore nuisance variables.

**Response.** The hostile prior-work set contains strong domain-randomization and adaptation methods. The paper should not argue that nearest neighbor represents the whole field. It is included to show how nuisance-heavy domain coordinates can be misleading in the controlled simulator.

## Likely Attack 7: The Passive Oracle Has Equal Success

**Concern.** The main table shows both passive-statistic oracle and mechanism-first have `1.000` success.

**Response.** The thresholded task success is intentionally loose. The repair-quality signal is mean final error and reward: mechanism-first has `0.0017` final error versus `0.0076` for passive statistics and matches both mechanism and best-repair oracles. The paper must present the result as precision/repair-quality improvement, not as a success-rate win over this oracle.

## Likely Attack 8: Literature Sweep Is Automatically Annotated

**Concern.** The 1500-paper matrix includes automatically generated annotations and may contain imperfect categorization.

**Response.** The matrix is used as a landscape and hostile-prior scaffold. The final related work should cite a smaller manually selected set and be honest that automatic annotations were used for breadth.

## Likely Attack 9: The Formal Claim Is Trivial

**Concern.** If two hidden states look the same under a statistic, of course a statistic-only method cannot distinguish them.

**Response.** The value is not mathematical difficulty; it is locating that trivial non-identifiability inside sim-to-real repair selection, where many methods implicitly treat domain statistics as the adaptation object. The paper should present it as a boundary lemma, not a deep theorem.

## Likely Attack 10: No Hardware

**Concern.** A sim-to-real paper without real hardware is incomplete.

**Response.** Correct for a mature conference submission. The current artifact is best positioned as a workshop paper or a methods note unless extended with hardware validation.
