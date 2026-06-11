# Literature Map

## Field Box

This run treats the field box as robotics sim-to-real transfer under embodied physical intelligence: policy transfer, domain randomization, system identification, domain adaptation, residual learning, contact-rich manipulation, locomotion, tactile/3D perception, robot world models, and causal/failure-diagnosis methods when they directly support robot deployment.

## Corpus

- Landscape sweep target: at least 1000 papers; collected matrix rows: 1500.
- Serious skim set: 300 rows.
- Deep-read set: 240 rows.
- Hostile prior-work set: 100 rows.

## Category Counts

- policy_transfer: 447
- domain_randomization: 422
- simulation_training: 320
- contact_manipulation: 90
- domain_adaptation: 53
- locomotion: 51
- system_identification: 38
- tactile: 30
- failure_analysis: 23
- causal_robotics: 16
- world_models: 5
- foundation_robotics: 4
- residual_learning: 1

## Top Relevance Slice

| rank_relevance | title | year | category | citation_count |
| --- | --- | --- | --- | --- |
| 1 | Sim-to-Real Transfer for Robotic Manipulation with Tactile Sensory | 2021 | contact_manipulation | 27 |
| 2 | Sim-to-Real: Learning Agile Locomotion For Quadruped Robots | 2018 | system_identification | 673 |
| 3 | A Sim-to-Real Learning-Based Framework for Contact-Rich Assembly by Utilizing CycleGAN an... | 2023 | domain_adaptation | 28 |
| 4 | Review of machine learning in robotic grasping control in space application | 2024 | policy_transfer | 83 |
| 5 | Domain Randomization for Sim2real Transfer of Automatically Generated Grasping Datasets | 2024 | domain_randomization | 20 |
| 6 | Domain randomization for transferring deep neural networks from simulation to the real world | 2017 | domain_randomization | 2737 |
| 7 | Real-World Robotic Perception and Control Using Synthetic Data | 2019 | domain_randomization | 5 |
| 8 | Learning Locomotion for Quadruped Robots via Distributional Ensemble Actor-Critic | 2024 | domain_randomization | 14 |
| 9 | Robot Learning From Randomized Simulations: A Review | 2022 | domain_randomization | 101 |
| 10 | Efficient Sim-to-Real Transfer in Reinforcement Learning Through Domain Randomization and... | 2023 | domain_randomization | 15 |
| 11 | Sim-to-Real Transfer of Robotic Control with Dynamics Randomization | 2018 | domain_randomization | 787 |
| 12 | Grasp Stability Assessment Through Attention-Guided Cross-Modality Fusion and Transfer Le... | 2023 | domain_adaptation | 11 |
| 13 | Sim-to-Real Transfer of Robotic Assembly with Visual Inputs Using CycleGAN and Force Control | 2022 | domain_adaptation | 13 |
| 14 | Learning Variable Impedance Control for Aerial Sliding on Uneven Heterogeneous Surfaces b... | 2022 | policy_transfer | 34 |
| 15 | Bi-Touch: Bimanual Tactile Manipulation With Sim-to-Real Deep Reinforcement Learning | 2023 | policy_transfer | 34 |
| 16 | Sim-to-Real Transfer of Compliant Bipedal Locomotion on Torque Sensor-Less Gear-Driven Hu... | 2023 | system_identification | 11 |
| 17 | Zero-shot sim-to-real transfer of reinforcement learning framework for robotics manipulat... | 2022 | policy_transfer | 11 |
| 18 | Sim-To-Real via Sim-To-Sim: Data-Efficient Robotic Grasping via Randomized-To-Canonical A... | 2019 | domain_randomization | 25 |
| 19 | Robust Keypoint Detection and Pose Estimation of Robot Manipulators with Self-Occlusions ... | 2020 | domain_randomization | 8 |
| 20 | Data-Efficient Domain Randomization With Bayesian Optimization | 2021 | domain_randomization | 58 |
| 21 | Self-Supervised Sim-to-Real Adaptation for Visual Robotic Manipulation | 2020 | domain_randomization | 56 |
| 22 | Towards Precise Model-free Robotic Grasping with Sim-to-Real Transfer Learning | 2022 | domain_randomization | 6 |
| 23 | Auto-Tuned Sim-to-Real Transfer | 2021 | domain_randomization | 46 |
| 24 | Pose Estimation for Robot Manipulators via Keypoint Optimization and Sim-to-Real Transfer | 2022 | domain_randomization | 45 |
| 25 | Sim-to-Real Robot Learning from Pixels with Progressive Nets | 2016 | policy_transfer | 109 |

## Hidden Assumptions That May Be False

1. The domain statistics that differ between sim and real are the variables that determine repair.
2. A single randomized simulator family contains the real deployment mechanism.
3. Visual appearance shift and physical mechanism shift can be handled by the same invariant representation.
4. Better prediction of next observations implies better selection of adaptation repairs.
5. Physical parameters are identifiable from the few rollouts available during deployment.
6. Continuous residual corrections are adequate for discrete failure mechanisms.
7. The policy can learn to ignore all nuisance variables without being told which are nuisances.
8. A real-world failure is a point in a parameter space rather than a member of a mechanism class.
9. Training-time robustness transfers to deployment-time diagnosis.
10. Contact failures can be averaged into smooth dynamics residuals.
11. The same repair is safe for all domains that share a distributional embedding.
12. Task reward gives timely information about the cause of failure.
13. Domain labels are more useful than causal failure labels.
14. Probe actions are too costly to be part of sim-to-real adaptation.
15. More diverse simulation is the main bottleneck rather than the wrong adaptation coordinate.
16. The simulator should be updated before the repair policy is chosen.
17. Failure modes are independent of the controller used to expose them.
18. Texture, lighting, and other nuisance shifts are harmless once randomized.
19. Mechanisms that have identical passive rollouts will need identical repairs.
20. The target domain is stationary during adaptation.
21. A learned latent variable will align with human-interpretable physical mechanisms.
22. The adaptation objective can be specified without naming what counts as a repaired failure.
23. Averaging over randomized domains does not wash out rare but repair-critical signatures.
24. Full system identification is necessary before useful sim-to-real repair.
25. The failure boundary observed in simulation is the same boundary that matters on hardware.

## Direction Seeds That Break Assumptions

### Mechanism-First Repair Coordinates
- Broken assumption: Domain statistics are the right adaptation coordinate.
- Proposed central mechanism: Use short diagnostic interventions to classify transfer failures into intervention-relevant mechanisms before choosing repair.
- Why it survived the sweep: Directly attacks non-identifiability: two domains can share statistics but require opposite repairs.
- Main risk: Synthetic evidence may be seen as too narrow unless tied to contact/control failures.

### Counterfactual Contact Probes
- Broken assumption: Passive deployment rollouts are enough for adaptation.
- Proposed central mechanism: Choose small probe actions whose residual signatures separate friction, compliance, delay, and gain mechanisms.
- Why it survived the sweep: Makes observability central rather than adding another estimator.
- Main risk: Probe design can look like active learning unless the mechanism/repair link is explicit.

### Repair-Equivalence Classes for Sim-to-Real
- Broken assumption: Parameter accuracy is the right success metric for adaptation.
- Proposed central mechanism: Group domains by the repair they require, even when their physical parameters differ.
- Why it survived the sweep: Changes the target from identifying the world to identifying the intervention.
- Main risk: Needs careful distinction from robust control and residual policy switching.

### Failure-Aliasing Lower Bounds
- Broken assumption: Distribution alignment can always recover transfer-relevant invariances.
- Proposed central mechanism: Prove adapters using only passive domain statistics fail under aliased mechanisms, then show diagnostic probes break the alias.
- Why it survived the sweep: Provides an adversarial formal boundary for existing domain adaptation claims.
- Main risk: The lower bound must not overclaim beyond the stylized setting.

## Field Pattern

The landscape is crowded around training-time coverage: randomized simulation, domain-aligned representation learning, parameter identification, residual correction, and large pretrained robot policies. The recurring gap is that these methods usually adapt coordinates of the domain or policy, while the transfer failure that matters to deployment is often categorical and intervention-specific: delay, gain loss, slip, compliance, saturation, sensing bias, or contact-mode ambiguity. The strongest paper direction should therefore make the repair mechanism the primary variable and use domain statistics only as possible evidence.
