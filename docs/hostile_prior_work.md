# Hostile Prior Work Set

These 100 papers are treated as the adversarial prior set because they are closest to the seed idea by relevance, category, citation signal, and mechanism overlap. The annotations are intentionally skeptical and focus on what each class of work makes less novel.

## 1. Sim-to-Real Transfer for Robotic Manipulation with Tactile Sensory (2021)

- Venue/authors: 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS); Zihan Ding; Ya-Yen Tsai; Wang Wei Lee; Bidan Huang
- Category: contact_manipulation; citations: 27
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1109/iros51168.2021.9636259

## 2. Sim-to-Real: Learning Agile Locomotion For Quadruped Robots (2018)

- Venue/authors: ; Jie Tan; Tingnan Zhang; Erwin Coumans; Atıl Işçen; Yunfei Bai; Danijar Hafner; et al.
- Category: system_identification; citations: 673
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: https://doi.org/10.15607/rss.2018.xiv.010

## 3. A Sim-to-Real Learning-Based Framework for Contact-Rich Assembly by Utilizing CycleGAN and Force Control (2023)

- Venue/authors: IEEE Transactions on Cognitive and Developmental Systems; Yunlei Shi; Chengjie Yuan; Athanasios Tsitos; Lin Cong; Hamid Hadjar; Zhaopeng Chen; et al.
- Category: domain_adaptation; citations: 28
- Problem claimed: Align source and target distributions so learned perception or policies transfer across domains.
- Actual mechanism introduced: Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.
- Hidden assumptions: Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.
- Variables treated as fixed: Controller semantics, intervention set, simulator causal graph, and failure labels.
- Failure modes ignored: Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.
- What it makes less novel: A generic feature-alignment framing for sim-to-real transfer.
- What it leaves open: Intervention-relevant mechanism identification under sparse real trials.
- Source: https://doi.org/10.1109/tcds.2023.3237734

## 4. Review of machine learning in robotic grasping control in space application (2024)

- Venue/authors: Acta Astronautica; Hadi Jahanshahi; Zheng Zhu
- Category: policy_transfer; citations: 83
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1016/j.actaastro.2024.04.012

## 5. Domain Randomization for Sim2real Transfer of Automatically Generated Grasping Datasets (2024)

- Venue/authors: ; Johann Huber; François Hélénon; Hippolyte Watrelot; Faïz Ben Amar; Stéphane Doncieux
- Category: domain_randomization; citations: 20
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/icra57147.2024.10610677

## 6. Domain randomization for transferring deep neural networks from simulation to the real world (2017)

- Venue/authors: ; Josh Tobin; Rachel Fong; Alex Ray; Jonas Schneider; Wojciech Zaremba; Pieter Abbeel
- Category: domain_randomization; citations: 2737
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/iros.2017.8202133

## 7. Real-World Robotic Perception and Control Using Synthetic Data (2019)

- Venue/authors: eScholarship (California Digital Library); Joshua Tobin
- Category: domain_randomization; citations: 5
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://escholarship.org/uc/item/2p62j4cm

## 8. Learning Locomotion for Quadruped Robots via Distributional Ensemble Actor-Critic (2024)

- Venue/authors: IEEE Robotics and Automation Letters; Sicen Li; Yiming Pang; Panju Bai; Jiawei Li; Zhaojin Liu; Shihao Hu; et al.
- Category: domain_randomization; citations: 14
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/lra.2024.3349934

## 9. Robot Learning From Randomized Simulations: A Review (2022)

- Venue/authors: Frontiers in Robotics and AI; Fabio Muratore; Fábio Ramos; Greg Turk; Wenhao Yu; Michael Gienger; Jan Peters
- Category: domain_randomization; citations: 101
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.3389/frobt.2022.799893

## 10. Efficient Sim-to-Real Transfer in Reinforcement Learning Through Domain Randomization and Domain Adaptation (2023)

- Venue/authors: IEEE Access; Aidar Shakerimov; Tohid Alizadeh; Hüseyin Atakan Varol
- Category: domain_randomization; citations: 15
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/access.2023.3339568

## 11. Sim-to-Real Transfer of Robotic Control with Dynamics Randomization (2018)

- Venue/authors: ; Xue Bin Peng; Marcin Andrychowicz; Wojciech Zaremba; Pieter Abbeel
- Category: domain_randomization; citations: 787
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/icra.2018.8460528

## 12. Grasp Stability Assessment Through Attention-Guided Cross-Modality Fusion and Transfer Learning (2023)

- Venue/authors: ; Zhuangzhuang Zhang; Zhenning Zhou; Haili Wang; Zhinan Zhang; Huang Huang; Qixin Cao
- Category: domain_adaptation; citations: 11
- Problem claimed: Align source and target distributions so learned perception or policies transfer across domains.
- Actual mechanism introduced: Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.
- Hidden assumptions: Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.
- Variables treated as fixed: Controller semantics, intervention set, simulator causal graph, and failure labels.
- Failure modes ignored: Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.
- What it makes less novel: A generic feature-alignment framing for sim-to-real transfer.
- What it leaves open: Intervention-relevant mechanism identification under sparse real trials.
- Source: https://doi.org/10.1109/iros55552.2023.10342411

## 13. Sim-to-Real Transfer of Robotic Assembly with Visual Inputs Using CycleGAN and Force Control (2022)

- Venue/authors: 2022 IEEE International Conference on Robotics and Biomimetics (ROBIO); Chengjie Yuan; Yunlei Shi; Qian Feng; Chunyang Chang; Michael C. Liu; Zhaopeng Chen; et al.
- Category: domain_adaptation; citations: 13
- Problem claimed: Align source and target distributions so learned perception or policies transfer across domains.
- Actual mechanism introduced: Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.
- Hidden assumptions: Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.
- Variables treated as fixed: Controller semantics, intervention set, simulator causal graph, and failure labels.
- Failure modes ignored: Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.
- What it makes less novel: A generic feature-alignment framing for sim-to-real transfer.
- What it leaves open: Intervention-relevant mechanism identification under sparse real trials.
- Source: https://doi.org/10.1109/robio55434.2022.10011878

## 14. Learning Variable Impedance Control for Aerial Sliding on Uneven Heterogeneous Surfaces by Proprioceptive and Tactile Sensing (2022)

- Venue/authors: IEEE Robotics and Automation Letters; Weixuan Zhang; Lionel Ott; Marco Tognon; Roland Siegwart
- Category: policy_transfer; citations: 34
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2022.3194315

## 15. Bi-Touch: Bimanual Tactile Manipulation With Sim-to-Real Deep Reinforcement Learning (2023)

- Venue/authors: IEEE Robotics and Automation Letters; Yijiong Lin; Alex Church; Max Yang; Haoran Li; John W. Lloyd; Dandan Zhang; et al.
- Category: policy_transfer; citations: 34
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2023.3295991

## 16. Sim-to-Real Transfer of Compliant Bipedal Locomotion on Torque Sensor-Less Gear-Driven Humanoid (2023)

- Venue/authors: ; Shimpei Masuda; Kuniyuki Takahashi
- Category: system_identification; citations: 11
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: https://doi.org/10.1109/humanoids57100.2023.10375181

## 17. Zero-shot sim-to-real transfer of reinforcement learning framework for robotics manipulation with demonstration and force feedback (2022)

- Venue/authors: Robotica; Yuanpei Chen; Chao Zeng; Zhiping Wang; Peng Lu; Chenguang Yang
- Category: policy_transfer; citations: 11
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1017/s0263574722001230

## 18. Sim-To-Real via Sim-To-Sim: Data-Efficient Robotic Grasping via Randomized-To-Canonical Adaptation Networks (2019)

- Venue/authors: ; Stephen James; Paul Wohlhart; Mrinal Kalakrishnan; Dmitry Kalashnikov; Alex Irpan; Julian Ibarz; et al.
- Category: domain_randomization; citations: 25
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/cvpr.2019.01291

## 19. Robust Keypoint Detection and Pose Estimation of Robot Manipulators with Self-Occlusions via Sim-to-Real Transfer. (2020)

- Venue/authors: arXiv (Cornell University); Jingpei Lu; Florian Richter; Michael C. Yip
- Category: domain_randomization; citations: 8
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://arxiv.org/pdf/2010.08054

## 20. Data-Efficient Domain Randomization With Bayesian Optimization (2021)

- Venue/authors: IEEE Robotics and Automation Letters; Fabio Muratore; Christian Eilers; Michael Gienger; Jan Peters
- Category: domain_randomization; citations: 58
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/lra.2021.3052391

## 21. Self-Supervised Sim-to-Real Adaptation for Visual Robotic Manipulation (2020)

- Venue/authors: ; Rae Jeong; Yusuf Aytar; David Khosid; Yuxiang Zhou; Jackie Kay; Thomas Lampe; et al.
- Category: domain_randomization; citations: 56
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/icra40945.2020.9197326

## 22. Towards Precise Model-free Robotic Grasping with Sim-to-Real Transfer Learning (2022)

- Venue/authors: 2022 IEEE International Conference on Robotics and Biomimetics (ROBIO); Lei Zhang; Kaixin Bai; Zhaopeng Chen; Yunlei Shi; Jianwei Zhang
- Category: domain_randomization; citations: 6
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/robio55434.2022.10011794

## 23. Auto-Tuned Sim-to-Real Transfer (2021)

- Venue/authors: ; Yuqing Du; Olivia Watkins; Trevor Darrell; Pieter Abbeel; Deepak Pathak
- Category: domain_randomization; citations: 46
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/icra48506.2021.9562091

## 24. Pose Estimation for Robot Manipulators via Keypoint Optimization and Sim-to-Real Transfer (2022)

- Venue/authors: IEEE Robotics and Automation Letters; Jingpei Lu; Florian Richter; Michael C. Yip
- Category: domain_randomization; citations: 45
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/lra.2022.3151981

## 25. Sim-to-Real Robot Learning from Pixels with Progressive Nets (2016)

- Venue/authors: arXiv (Cornell University); Andrei A. Rusu; Vecerik, Mel; Thomas Rothörl; Nicolas Heess; Razvan Pascanu; Raia Hadsell
- Category: policy_transfer; citations: 109
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: http://arxiv.org/abs/1610.04286

## 26. The Reality Gap in Robotics: Challenges, Solutions, and Best Practices (2025)

- Venue/authors: Annual Review of Control Robotics and Autonomous Systems; Elie Aljalbout; Jiaxu Xing; Angel Romero; Iretiayo Akinola; Caelan Reed Garrett; Eric Heiden; et al.
- Category: domain_randomization; citations: 2
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1146/annurev-control-031924-100130

## 27. Sim-to-Real for Robotic Tactile Sensing via Physics-Based Simulation and Learned Latent Projections (2021)

- Venue/authors: ; Yashraj Narang; Balakumar Sundaralingam; Miles Macklin; Arsalan Mousavian; Dieter Fox
- Category: contact_manipulation; citations: 6
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1109/icra48506.2021.9561969

## 28. 6IMPOSE: bridging the reality gap in 6D pose estimation for robotic grasping (2023)

- Venue/authors: Frontiers in Robotics and AI; Hongpeng Cao; Lukas Dirnberger; Daniele Bernardini; Cristina Piazza; Marco Caccamo
- Category: domain_randomization; citations: 18
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.3389/frobt.2023.1176492

## 29. Cat-Like Jumping and Landing of Legged Robots in Low Gravity Using Deep Reinforcement Learning (2021)

- Venue/authors: IEEE Transactions on Robotics; Nikita Rudin; Hendrik Kolvenbach; Vassilios Tsounis; Marco Hutter
- Category: locomotion; citations: 120
- Problem claimed: Transfer locomotion policies across terrain, morphology, sensing, and actuator gaps.
- Actual mechanism introduced: Dynamics randomization, privileged training, online adaptation, residual policies, or robust control.
- Hidden assumptions: Morphology and terrain variations can be covered by training distributions or latent adaptation.
- Variables treated as fixed: Named failure mechanisms and their repair semantics.
- Failure modes ignored: Aliased failure signatures and non-stationary faults after deployment.
- What it makes less novel: Locomotion sim-to-real through randomized or adaptive policies.
- What it leaves open: Mechanism-first repair when the robot must choose among incompatible fixes.
- Source: https://doi.org/10.1109/tro.2021.3084374

## 30. Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey (2020)

- Venue/authors: ; Wenshuai Zhao; Jorge Pena Queralta; Tomi Westerlund
- Category: policy_transfer; citations: 673
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/ssci47803.2020.9308468

## 31. Grasp Stability Prediction with Sim-to-Real Transfer from Tactile Sensing (2022)

- Venue/authors: 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS); Zilin Si; Zirui Zhu; Arpit Agarwal; Stuart Anderson; Wenzhen Yuan
- Category: contact_manipulation; citations: 29
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1109/iros47612.2022.9981863

## 32. A Survey on Sim-to-Real Transfer Methods for Robotic Manipulation (2024)

- Venue/authors: ; Andrei Vladimirovich Pitkevich; Ilya Makarov
- Category: domain_randomization; citations: 9
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/sisy62279.2024.10737545

## 33. An Unconstrained Convex Formulation of Compliant Contact (2022)

- Venue/authors: IEEE Transactions on Robotics; Alejandro Castro; Frank Permenter; Xuchen Han
- Category: contact_manipulation; citations: 25
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1109/tro.2022.3209077

## 34. Variable Compliance Control for Robotic Peg-in-Hole Assembly: A Deep-Reinforcement-Learning Approach (2020)

- Venue/authors: Applied Sciences; Cristian C. Beltran-Hernandez; Damien Petit; Ixchel G. Ramirez-Alpizar; Kensuke Harada
- Category: domain_randomization; citations: 169
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.3390/app10196923

## 35. Deep Reinforcement Learning for Robotic Control in High-Dexterity Assembly Tasks — A Reward Curriculum Approach (2022)

- Venue/authors: International Journal of Semantic Computing; Lars Leyendecker; Markus Schmitz; Hans Aoyang Zhou; Владимир Самсонов; Marius Rittstieg; Daniel Lütticke
- Category: domain_randomization; citations: 7
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1142/s1793351x22430024

## 36. RL-CycleGAN: Reinforcement Learning Aware Simulation-to-Real (2020)

- Venue/authors: ; Kanishka Rao; C.J. Harris; Alex Irpan; Sergey Levine; Julian Ibarz; Mohi Khansari
- Category: policy_transfer; citations: 154
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/cvpr42600.2020.01117

## 37. Sim-to-Real Model-Based and Model-Free Deep Reinforcement Learning for Tactile Pushing (2023)

- Venue/authors: IEEE Robotics and Automation Letters; Max Yang; Yijiong Lin; Alex Church; John W. Lloyd; Dandan Zhang; David A. W. Barton; et al.
- Category: policy_transfer; citations: 18
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2023.3295236

## 38. Tactile Gym 2.0: Sim-to-Real Deep Reinforcement Learning for Comparing Low-Cost High-Resolution Robot Touch (2022)

- Venue/authors: IEEE Robotics and Automation Letters; Yijiong Lin; John W. Lloyd; Alex Church; Nathan F. Lepora
- Category: policy_transfer; citations: 50
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2022.3195195

## 39. Modelling and identification methods for simulation of cable-suspended dual-arm robotic systems (2024)

- Venue/authors: Robotics and Autonomous Systems; Giancarlo D’Ago; Mario Selvaggio; Alejandro Suárez; Francisco Javier Gañán; Luca Rosario Buonocore; Mario Di Castro; et al.
- Category: system_identification; citations: 16
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: https://doi.org/10.1016/j.robot.2024.104643

## 40. Rapid Locomotion via Reinforcement Learning (2022)

- Venue/authors: ; Gabriel B. Margolis; Ge Yang; Kartik Paigwar; Tao Chen; Pulkit Agrawal
- Category: system_identification; citations: 116
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: https://doi.org/10.15607/rss.2022.xviii.022

## 41. Revolutionizing self-powered robotic systems with triboelectric nanogenerators (2023)

- Venue/authors: Nano Energy; Sugato Hajra; Swati Panda; Hamideh Khanberh; Venkateswaran Vivekananthan; Elham Chamanehpour; Yogendra Kumar Mishra; et al.
- Category: contact_manipulation; citations: 106
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1016/j.nanoen.2023.108729

## 42. Sim-to-Real Transfer with Incremental Environment Complexity for Reinforcement Learning of Depth-based Robot Navigation (2020)

- Venue/authors: ; Thomas Chaffre; Julien Moras; Adrien Chan-Hon-Tong; Julien Marzat
- Category: policy_transfer; citations: 4
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.5220/0009821603140323

## 43. Attention for Robot Touch: Tactile Saliency Prediction for Robust Sim-to-Real Tactile Control (2023)

- Venue/authors: ; Yijiong Lin; Mauro Comi; Alex Church; Dandan Zhang; Nathan F. Lepora
- Category: tactile; citations: 4
- Problem claimed: Use tactile sensing to bridge contact uncertainty in real robotic interaction.
- Actual mechanism introduced: Learn tactile representations, calibrate sensors, or fuse touch with vision/control.
- Hidden assumptions: Sensing reveals the relevant physical state once properly calibrated.
- Variables treated as fixed: Failure taxonomy and intervention selection.
- Failure modes ignored: When the same tactile distribution corresponds to different repair mechanisms.
- What it makes less novel: Using tactile observations as additional transfer signal.
- What it leaves open: Probe design that separates failure mechanisms rather than merely improving sensing.
- Source: http://dx.doi.org/10.1109/iros55552.2023.10341888

## 44. Zero-Shot Sim-to-Real Transfer of Tactile Control Policies for Aggressive Swing-Up Manipulation (2021)

- Venue/authors: IEEE Robotics and Automation Letters; Thomas Bi; Carmelo Sferrazza; Raffaello D’Andrea
- Category: domain_adaptation; citations: 30
- Problem claimed: Align source and target distributions so learned perception or policies transfer across domains.
- Actual mechanism introduced: Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.
- Hidden assumptions: Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.
- Variables treated as fixed: Controller semantics, intervention set, simulator causal graph, and failure labels.
- Failure modes ignored: Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.
- What it makes less novel: A generic feature-alignment framing for sim-to-real transfer.
- What it leaves open: Intervention-relevant mechanism identification under sparse real trials.
- Source: https://doi.org/10.1109/lra.2021.3084880

## 45. Learning ambidextrous robot grasping policies (2019)

- Venue/authors: Science Robotics; Jeffrey Mahler; Matthew Matl; Vishal Satish; Michael Danielczuk; Bill DeRose; Stephen McKinley; et al.
- Category: domain_randomization; citations: 578
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1126/scirobotics.aau4984

## 46. Kalman Filter-Based One-Shot Sim-to-Real Transfer Learning (2023)

- Venue/authors: IEEE Robotics and Automation Letters; Qingwei Dong; Peng Zeng; Guangxi Wan; Yunpeng He; Xiaoting Dong
- Category: domain_adaptation; citations: 9
- Problem claimed: Align source and target distributions so learned perception or policies transfer across domains.
- Actual mechanism introduced: Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.
- Hidden assumptions: Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.
- Variables treated as fixed: Controller semantics, intervention set, simulator causal graph, and failure labels.
- Failure modes ignored: Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.
- What it makes less novel: A generic feature-alignment framing for sim-to-real transfer.
- What it leaves open: Intervention-relevant mechanism identification under sparse real trials.
- Source: https://doi.org/10.1109/lra.2023.3333661

## 47. Benchmarking the Sim-to-Real Gap in Cloth Manipulation (2024)

- Venue/authors: IEEE Robotics and Automation Letters; David Blanco–Mulero; Oriol Barbany; Gökhan Alcan; Adrià Colomé; Carme Torras; Ville Kyrki
- Category: contact_manipulation; citations: 24
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1109/lra.2024.3360814

## 48. Sim-to-Real Transfer for Visual Reinforcement Learning of Deformable Object Manipulation for Robot-Assisted Surgery (2022)

- Venue/authors: IEEE Robotics and Automation Letters; Paul Maria Scheikl; Eleonora Tagliabue; Balázs Gyenes; Martin Wagner; Diego Dall’Alba; Paolo Fiorini; et al.
- Category: policy_transfer; citations: 66
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2022.3227873

## 49. EMERGE Modular Robot: A Tool for Fast Deployment of Evolved Robots (2021)

- Venue/authors: Frontiers in Robotics and AI; Rodrigo Moreno; Andrés Faíña
- Category: policy_transfer; citations: 23
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.3389/frobt.2021.699814

## 50. Deep-learning in Mobile Robotics - from Perception to Control Systems: A Survey on Why and Why not. (2016)

- Venue/authors: arXiv (Cornell University); Lei Tai; Ming Liu
- Category: policy_transfer; citations: 62
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://arxiv.org/pdf/1612.07139

## 51. Unsupervised Adversarial Domain Adaptation for Sim-to-Real Transfer of Tactile Images (2023)

- Venue/authors: IEEE Transactions on Instrumentation and Measurement; Xingshuo Jing; Kun Qian; Tudor Jianu; Shan Luo
- Category: domain_adaptation; citations: 22
- Problem claimed: Align source and target distributions so learned perception or policies transfer across domains.
- Actual mechanism introduced: Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.
- Hidden assumptions: Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.
- Variables treated as fixed: Controller semantics, intervention set, simulator causal graph, and failure labels.
- Failure modes ignored: Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.
- What it makes less novel: A generic feature-alignment framing for sim-to-real transfer.
- What it leaves open: Intervention-relevant mechanism identification under sparse real trials.
- Source: https://doi.org/10.1109/tim.2023.3268458

## 52. Contact Reduction with Bounded Stiffness for Robust Sim-to-Real Transfer of Robot Assembly (2023)

- Venue/authors: ; Nghia Vuong; Quang‐Cuong Pham
- Category: policy_transfer; citations: 2
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/iros55552.2023.10341866

## 53. Optimization-Based Control for Dynamic Legged Robots (2023)

- Venue/authors: IEEE Transactions on Robotics; Patrick M. Wensing; Michael Posa; Yue Hu; Adrien Escande; Nicolas Mansard; Andrea Del Prete
- Category: locomotion; citations: 162
- Problem claimed: Transfer locomotion policies across terrain, morphology, sensing, and actuator gaps.
- Actual mechanism introduced: Dynamics randomization, privileged training, online adaptation, residual policies, or robust control.
- Hidden assumptions: Morphology and terrain variations can be covered by training distributions or latent adaptation.
- Variables treated as fixed: Named failure mechanisms and their repair semantics.
- Failure modes ignored: Aliased failure signatures and non-stationary faults after deployment.
- What it makes less novel: Locomotion sim-to-real through randomized or adaptive policies.
- What it leaves open: Mechanism-first repair when the robot must choose among incompatible fixes.
- Source: https://doi.org/10.1109/tro.2023.3324580

## 54. An End-to-End Differentiable Framework for Contact-Aware Robot Design (2021)

- Venue/authors: ; Jie Xu; Tao Chen; Lara Zlokapa; Michael Foshey; Wojciech Matusik; Shinjiro Sueda; et al.
- Category: contact_manipulation; citations: 58
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.15607/rss.2021.xvii.008

## 55. KOVIS: Keypoint-based Visual Servoing with Zero-Shot Sim-to-Real Transfer for Robotics Manipulation (2020)

- Venue/authors: ; En Yen Puang; Keng Peng Tee; Wei Jing
- Category: domain_randomization; citations: 52
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/iros45743.2020.9341370

## 56. Human-Robot Shared Control for Surgical Robot Based on Context-Aware Sim-to-Real Adaptation (2022)

- Venue/authors: 2022 International Conference on Robotics and Automation (ICRA); Dandan Zhang; Zicong Wu; Junhong Chen; Ruiqi Zhu; Adnan Munawar; Bo Xiao; et al.
- Category: domain_adaptation; citations: 49
- Problem claimed: Align source and target distributions so learned perception or policies transfer across domains.
- Actual mechanism introduced: Learn domain-invariant features, adversarial alignments, image translations, or target-conditioned representations.
- Hidden assumptions: Distributional alignment preserves task-relevant causal factors and does not merge domains requiring different repairs.
- Variables treated as fixed: Controller semantics, intervention set, simulator causal graph, and failure labels.
- Failure modes ignored: Identical marginal statistics with different mechanisms, contact discontinuities, and policy-induced data shift.
- What it makes less novel: A generic feature-alignment framing for sim-to-real transfer.
- What it leaves open: Intervention-relevant mechanism identification under sparse real trials.
- Source: https://doi.org/10.1109/icra46639.2022.9812379

## 57. SimGAN: Hybrid Simulator Identification for Domain Adaptation via Adversarial Reinforcement Learning (2021)

- Venue/authors: ; Yifeng Jiang; Tingnan Zhang; Daniel E. Ho; Yunfei Bai; C. Karen Liu; Sergey Levine; et al.
- Category: policy_transfer; citations: 48
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/icra48506.2021.9561731

## 58. Multimodality Driven Impedance-Based Sim2Real Transfer Learning for Robotic Multiple Peg-in-Hole Assembly (2023)

- Venue/authors: IEEE Transactions on Cybernetics; Wenkai Chen; Chao Zeng; Hongzhuo Liang; Fuchun Sun; Jianwei Zhang
- Category: policy_transfer; citations: 47
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/tcyb.2023.3310505

## 59. Predicting the Force Map of an ERT-Based Tactile Sensor Using Simulation and Deep Networks (2022)

- Venue/authors: IEEE Transactions on Automation Science and Engineering; Hyosang Lee; Huanbo Sun; Hyunkyu Park; Gokhan Serhat; Bernard Javot; Georg Martius; et al.
- Category: tactile; citations: 46
- Problem claimed: Use tactile sensing to bridge contact uncertainty in real robotic interaction.
- Actual mechanism introduced: Learn tactile representations, calibrate sensors, or fuse touch with vision/control.
- Hidden assumptions: Sensing reveals the relevant physical state once properly calibrated.
- Variables treated as fixed: Failure taxonomy and intervention selection.
- Failure modes ignored: When the same tactile distribution corresponds to different repair mechanisms.
- What it makes less novel: Using tactile observations as additional transfer signal.
- What it leaves open: Probe design that separates failure mechanisms rather than merely improving sensing.
- Source: https://doi.org/10.1109/tase.2022.3156184

## 60. Bidirectional Sim-to-Real Transfer for GelSight Tactile Sensors With CycleGAN (2022)

- Venue/authors: IEEE Robotics and Automation Letters; Weihang Chen; Yuan Xu; Zhenyang Chen; Peiyu Zeng; Renjun Dang; Rui Chen; et al.
- Category: policy_transfer; citations: 38
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2022.3167064

## 61. Sim-to-Real in Reinforcement Learning for Everyone (2019)

- Venue/authors: ; Juliano Vacaro; Guilherme Marques; Bruna Oliveira; Gabriel Andrade Paz; Thomas Paula; Wagston Staehler; et al.
- Category: policy_transfer; citations: 13
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lars-sbr-wre48964.2019.00060

## 62. Contact Models in Robotics: A Comparative Analysis (2024)

- Venue/authors: IEEE Transactions on Robotics; Quentin Le Lidec; Wilson Jallet; Louis Montaut; Ivan Laptev; Cordelia Schmid; Justin Carpentier
- Category: policy_transfer; citations: 36
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/tro.2024.3434208

## 63. Optical Tactile Sim-to-Real Policy Transfer via Real-to-Sim Tactile Image Translation. (2021)

- Venue/authors: arXiv (Cornell University); Alex Church; John W. Lloyd; Raia Hadsell; Nathan F. Lepora
- Category: policy_transfer; citations: 4
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://arxiv.org/pdf/2106.08796

## 64. DROPO: Sim-to-real transfer with offline domain randomization (2023)

- Venue/authors: Robotics and Autonomous Systems; Gabriele Tiboni; Karol Arndt; Ville Kyrki
- Category: domain_randomization; citations: 34
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1016/j.robot.2023.104432

## 65. Understanding Domain Randomization for Sim-to-real Transfer (2021)

- Venue/authors: arXiv (Cornell University); Xiaoyu Chen; Jiachen Hu; Chi Jin; Lihong Li; Liwei Wang
- Category: policy_transfer; citations: 33
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: http://arxiv.org/abs/2110.03239

## 66. Triboelectric nanogenerator sensors for soft robotics aiming at digital twin applications (2020)

- Venue/authors: Nature Communications; Tao Jin; Zhongda Sun; Long Li; Quan Zhang; Minglu Zhu; Zixuan Zhang; et al.
- Category: contact_manipulation; citations: 659
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1038/s41467-020-19059-3

## 67. Bayesian Domain Randomization for Sim-to-Real Transfer. (2020)

- Venue/authors: arXiv (Cornell University); Fabio Muratore; Christian Eilers; Michael Gienger; Jan Peters
- Category: domain_randomization; citations: 11
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://arxiv.org/pdf/2003.02471

## 68. CausalWorld: A Robotic Manipulation Benchmark for Causal Structure and Transfer Learning (2020)

- Venue/authors: arXiv (Cornell University); Ossama Ahmed; Frederik Träuble; Anirudh Goyal; Alexander Neitz; Yoshua Bengio; Bernhard Schölkopf; et al.
- Category: policy_transfer; citations: 31
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: http://arxiv.org/abs/2010.04296

## 69. DROID: Minimizing the Reality Gap Using Single-Shot Human Demonstration (2021)

- Venue/authors: IEEE Robotics and Automation Letters; Ya-Yen Tsai; Hui Xu; Zihan Ding; Chong Zhang; Edward Johns; Bidan Huang
- Category: policy_transfer; citations: 29
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2021.3062311

## 70. Preparing for the Unknown: Learning a Universal Policy with Online System Identification (2017)

- Venue/authors: ; Wenhao Yu; Jie Tan; C. Karen Liu; Greg Turk
- Category: system_identification; citations: 220
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: https://doi.org/10.15607/rss.2017.xiii.048

## 71. Dojo: A Differentiable Physics Engine for Robotics (2022)

- Venue/authors: arXiv (Cornell University); Taylor A. Howell; Simon Le Cleac’h; Brüdigam, Jan; Chen, Qianzhong; Sun, Jiankai; Kolter, J. Zico; et al.
- Category: system_identification; citations: 10
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: http://arxiv.org/abs/2203.00806

## 72. Safe and Efficient Auto-tuning to Cross Sim-to-real Gap for Bipedal Robot (2024)

- Venue/authors: ; Yidong Du; Xuechao Chen; Zhangguo Yu; Yuanxi Zhang; Zishun Zhou; Jindai Zhang; et al.
- Category: policy_transfer; citations: 3
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/iros58592.2024.10801318

## 73. Robot Manipulation Skills Transfer for Sim-to-Real in Unstructured Environments (2023)

- Venue/authors: Electronics; Zikang Yin; Chao Ye; Hao An; Weiyang Lin; Zhifeng Wang
- Category: policy_transfer; citations: 3
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.3390/electronics12020411

## 74. Tactile Sim-to-Real Policy Transfer via Real-to-Sim Image Translation (2021)

- Venue/authors: arXiv (Cornell University); Alex Church; John W. Lloyd; Raia Hadsell; Nathan F. Lepora
- Category: policy_transfer; citations: 3
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: http://arxiv.org/abs/2106.08796

## 75. Learning garment manipulation policies toward robot-assisted dressing (2022)

- Venue/authors: Science Robotics; Fan Zhang; Yiannis Demiris
- Category: policy_transfer; citations: 77
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1126/scirobotics.abm6010

## 76. Reinforcement Learning for Robust Parameterized Locomotion Control of Bipedal Robots (2021)

- Venue/authors: ; Zhongyu Li; Xuxin Cheng; Xue Bin Peng; Pieter Abbeel; Sergey Levine; Glen Berseth; et al.
- Category: domain_randomization; citations: 200
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/icra48506.2021.9560769

## 77. Digital Twin (DT)-CycleGAN: Enabling Zero-Shot Sim-to-Real Transfer of Visual Grasping Models (2023)

- Venue/authors: IEEE Robotics and Automation Letters; David Liu; Yuzhong Chen; Zihao Wu
- Category: policy_transfer; citations: 23
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2023.3254460

## 78. Crossing the Reality Gap: A Survey on Sim-to-Real Transferability of Robot Controllers in Reinforcement Learning (2021)

- Venue/authors: IEEE Access; Erica Salvato; Gianfranco Fenu; Eric Medvet; Felice Andrea Pellegrino
- Category: policy_transfer; citations: 174
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/access.2021.3126658

## 79. Development of a Sperm‐Flagella Driven Micro‐Bio‐Robot (2013)

- Venue/authors: Advanced Materials; Veronika Magdanz; Samuel Sánchez; Oliver G. Schmidt
- Category: contact_manipulation; citations: 437
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1002/adma.201302544

## 80. Sim-to-real via latent prediction: Transferring visual non-prehensile manipulation policies (2023)

- Venue/authors: Frontiers in Robotics and AI; Carlo Rizzardo; Fei Chen; Darwin G. Caldwell
- Category: policy_transfer; citations: 7
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.3389/frobt.2022.1067502

## 81. An autonomous strawberry‐harvesting robot: Design, development, integration, and field evaluation (2019)

- Venue/authors: Journal of Field Robotics; Ya Xiong; Yuanyue Ge; Lars Grimstad; Pål Johan From
- Category: contact_manipulation; citations: 418
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.1002/rob.21889

## 82. Dynamics as Prompts: In-Context Learning for Sim-to-Real System Identifications (2025)

- Venue/authors: IEEE Robotics and Automation Letters; Xilun Zhang; Shiqi Liu; Peide Huang; William Jongwon Han; Yiqi Lyu; Mengdi Xu; et al.
- Category: system_identification; citations: 6
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: https://doi.org/10.1109/lra.2025.3540391

## 83. Modelling Generalized Forces with Reinforcement Learning for Sim-to-Real Transfer (2019)

- Venue/authors: arXiv (Cornell University); Rae Jeong; Jackie Kay; Francesco Romano; Thomas Lampe; Rothorl, Tom; Abbas Abdolmaleki; et al.
- Category: policy_transfer; citations: 16
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: http://arxiv.org/abs/1910.09471

## 84. Learning High Speed Precision Table Tennis on a Physical Robot (2022)

- Venue/authors: 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS); Tianli Ding; Laura Graesser; Saminda Abeyruwan; David B. D’Ambrosio; Anish Shankar; Pierre Sermanet; et al.
- Category: policy_transfer; citations: 16
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/iros47612.2022.9982205

## 85. Sim-to-Real for Soft Robots Using Differentiable FEM: Recipes for Meshing, Damping, and Actuation (2022)

- Venue/authors: IEEE Robotics and Automation Letters; Mathieu Dubied; Mike Y. Michelis; Andrew Spielberg; Robert K. Katzschmann
- Category: system_identification; citations: 45
- Problem claimed: Estimate physical parameters of the real system and update the simulator or controller.
- Actual mechanism introduced: Fit masses, friction, delays, gains, or dynamics parameters from observed trajectories.
- Hidden assumptions: The chosen parameterization contains the real gap and estimated parameters map monotonically to better control.
- Variables treated as fixed: Mechanism library boundaries, unmodeled contacts, failure observability, and nuisance appearance variables.
- Failure modes ignored: Non-identifiable parameters, aliased mechanisms with similar rollouts, and repairs that need categorical decisions.
- What it makes less novel: Claims that transfer can be repaired by estimating simulator parameters.
- What it leaves open: Mechanism-level probes that identify the repair before accurate full-parameter estimation.
- Source: https://doi.org/10.1109/lra.2022.3154050

## 86. Overcoming the Sim-to-Real Gap in Autonomous Robots (2022)

- Venue/authors: Procedia CIRP; Pascalis Trentsios; Mario Wolf; Detlef Gerhard
- Category: domain_randomization; citations: 15
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1016/j.procir.2022.05.251

## 87. ALDM-Grasping: Diffusion-aided Zero-Shot Sim-to-Real Transfer for Robot Grasping (2024)

- Venue/authors: arXiv (Cornell University); Yiwei Li; Zihao Wu; Huaqin Zhao; Tianze Yang; Zhengliang Liu; Peng Shu; et al.
- Category: contact_manipulation; citations: 1
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: http://arxiv.org/abs/2403.11459

## 88. Transferring Multi-Agent Reinforcement Learning Policies for Autonomous Driving using Sim-to-Real (2022)

- Venue/authors: 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS); Eduardo Candela; Leandro Parada; Luís Marques; Tiberiu-Andrei Georgescu; Yiannis Demiris; Panagiotis Angeloudis
- Category: domain_randomization; citations: 38
- Problem claimed: Close the reality gap by training policies over many randomized simulator domains.
- Actual mechanism introduced: Expose the policy to sampled visual, dynamics, and nuisance parameters during training.
- Hidden assumptions: The randomization family covers the real transfer gap and the policy can learn invariances without knowing the failure mechanism.
- Variables treated as fixed: Failure taxonomy, repair action space, diagnostic interventions, and causal structure of contact/control failures.
- Failure modes ignored: Mechanism aliasing, rare coupled failures, repair-dependent observability, and nuisance dimensions that dominate domain statistics.
- What it makes less novel: A broad claim that randomized simulation improves robustness or transfer.
- What it leaves open: Which physical failure mechanism caused transfer collapse and which minimal repair should be applied.
- Source: https://doi.org/10.1109/iros47612.2022.9981319

## 89. Deep Object Pose Estimation for Semantic Robotic Grasping of Household\n Objects (2018)

- Venue/authors: arXiv (Cornell University); Jonathan Tremblay; Thang To; Balakumar Sundaralingam; Xiang Yu; Dieter Fox; Stan Birchfield
- Category: contact_manipulation; citations: 283
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: http://arxiv.org/abs/1809.10790

## 90. Sim-to-Real Surgical Robot Learning and Autonomous Planning for Internal Tissue Points Manipulation Using Reinforcement Learning (2023)

- Venue/authors: IEEE Robotics and Automation Letters; Yafei Ou; Mahdi Tavakoli
- Category: policy_transfer; citations: 35
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2023.3254860

## 91. The Transferability Approach: Crossing the Reality Gap in Evolutionary Robotics (2012)

- Venue/authors: IEEE Transactions on Evolutionary Computation; Sylvain Koos; J-B Mouret; Stéphane Doncieux
- Category: locomotion; citations: 263
- Problem claimed: Transfer locomotion policies across terrain, morphology, sensing, and actuator gaps.
- Actual mechanism introduced: Dynamics randomization, privileged training, online adaptation, residual policies, or robust control.
- Hidden assumptions: Morphology and terrain variations can be covered by training distributions or latent adaptation.
- Variables treated as fixed: Named failure mechanisms and their repair semantics.
- Failure modes ignored: Aliased failure signatures and non-stationary faults after deployment.
- What it makes less novel: Locomotion sim-to-real through randomized or adaptive policies.
- What it leaves open: Mechanism-first repair when the robot must choose among incompatible fixes.
- Source: https://doi.org/10.1109/tevc.2012.2185849

## 92. Learning Agile Robotic Locomotion Skills by Imitating Animals (2020)

- Venue/authors: ; Xue Bin Peng; Erwin Coumans; Tingnan Zhang; Tsang-Wei Lee; Jie Tan; Sergey Levine
- Category: locomotion; citations: 34
- Problem claimed: Transfer locomotion policies across terrain, morphology, sensing, and actuator gaps.
- Actual mechanism introduced: Dynamics randomization, privileged training, online adaptation, residual policies, or robust control.
- Hidden assumptions: Morphology and terrain variations can be covered by training distributions or latent adaptation.
- Variables treated as fixed: Named failure mechanisms and their repair semantics.
- Failure modes ignored: Aliased failure signatures and non-stationary faults after deployment.
- What it makes less novel: Locomotion sim-to-real through randomized or adaptive policies.
- What it leaves open: Mechanism-first repair when the robot must choose among incompatible fixes.
- Source: https://doi.org/10.15607/rss.2020.xvi.064

## 93. SafeAPT: Safe Simulation-to-Real Robot Learning Using Diverse Policies Learned in Simulation (2022)

- Venue/authors: IEEE Robotics and Automation Letters; Rituraj Kaushik; Karol Arndt; Ville Kyrki
- Category: policy_transfer; citations: 11
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/lra.2022.3177294

## 94. Robotic Manipulation and Capture in Space: A Survey (2021)

- Venue/authors: Frontiers in Robotics and AI; Evangelos Papadopoulos; Farhad Aghili; Ou Ma; Roberto Lampariello
- Category: contact_manipulation; citations: 199
- Problem claimed: Transfer contact-rich manipulation skills despite friction, compliance, geometry, and sensing gaps.
- Actual mechanism introduced: Model, randomize, or learn contact dynamics and manipulation policies.
- Hidden assumptions: Contact uncertainty can be represented as parameters or broad robustness margins.
- Variables treated as fixed: Failure onset signatures, controller repair choices, and mechanism-specific contact probes.
- Failure modes ignored: Ambiguous contacts with identical task statistics but opposite corrective actions.
- What it makes less novel: Showing that contact dynamics matter for sim-to-real manipulation.
- What it leaves open: Failure-mechanism diagnosis for contact repairs under few real interactions.
- Source: https://doi.org/10.3389/frobt.2021.686723

## 95. A Survey of Deep Network Solutions for Learning Control in Robotics: From Reinforcement to Imitation (2016)

- Venue/authors: arXiv (Cornell University); Lei Tai; Jingwei Zhang; Ming Liu; Joschka Boedecker; Wolfram Burgard
- Category: policy_transfer; citations: 70
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: http://arxiv.org/abs/1612.07139

## 96. Scalable sim-to-real transfer of soft robot designs (2020)

- Venue/authors: ; Sam Kriegman; Amir Mohammadi Nasab; Dylan Shah; Hannah Steele; Gabrielle Branin; Michael Levin; et al.
- Category: simulation_training; citations: 67
- Problem claimed: Use simulation to generate robot training data and policies.
- Actual mechanism introduced: Procedural simulation, synthetic data, imitation, policy learning, or sim-trained perception.
- Hidden assumptions: Simulator coverage and transfer procedures are sufficient for real deployment.
- Variables treated as fixed: Deployment-time repair mechanism and causal diagnosis.
- Failure modes ignored: Mechanism-specific transfer failures hidden by aggregate success rates.
- What it makes less novel: More simulation as the source of robot generalization.
- What it leaves open: Evidence that adapting failure mechanisms can dominate adapting domain statistics.
- Source: https://doi.org/10.1109/robosoft48309.2020.9116004

## 97. A Review of Jamming Actuation in Soft Robotics (2020)

- Venue/authors: Actuators; Seth G. Fitzgerald; Gary W. Delaney; David Howard
- Category: locomotion; citations: 168
- Problem claimed: Transfer locomotion policies across terrain, morphology, sensing, and actuator gaps.
- Actual mechanism introduced: Dynamics randomization, privileged training, online adaptation, residual policies, or robust control.
- Hidden assumptions: Morphology and terrain variations can be covered by training distributions or latent adaptation.
- Variables treated as fixed: Named failure mechanisms and their repair semantics.
- Failure modes ignored: Aliased failure signatures and non-stationary faults after deployment.
- What it makes less novel: Locomotion sim-to-real through randomized or adaptive policies.
- What it leaves open: Mechanism-first repair when the robot must choose among incompatible fixes.
- Source: https://doi.org/10.3390/act9040104

## 98. ReBot: Scaling Robot Learning with Real-to-Sim-to-Real Robotic Video Synthesis (2025)

- Venue/authors: ; Fang Yu; Yue Yang; Xinghao Zhu; Kaiyuan Zheng; Gedas Bertasius; Daniel Szafır; et al.
- Category: policy_transfer; citations: 2
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/iros60139.2025.11246305

## 99. DrEureka: Language Model Guided Sim-To-Real Transfer (2024)

- Venue/authors: arXiv (Cornell University); Yecheng Jason Ma; William Liang; Hung-Ju Wang; Sam Wang; Yuke Zhu; Linxi Fan; et al.
- Category: locomotion; citations: 7
- Problem claimed: Transfer locomotion policies across terrain, morphology, sensing, and actuator gaps.
- Actual mechanism introduced: Dynamics randomization, privileged training, online adaptation, residual policies, or robust control.
- Hidden assumptions: Morphology and terrain variations can be covered by training distributions or latent adaptation.
- Variables treated as fixed: Named failure mechanisms and their repair semantics.
- Failure modes ignored: Aliased failure signatures and non-stationary faults after deployment.
- What it makes less novel: Locomotion sim-to-real through randomized or adaptive policies.
- What it leaves open: Mechanism-first repair when the robot must choose among incompatible fixes.
- Source: http://arxiv.org/abs/2406.01967

## 100. Bridging the Reality Gap: Analyzing Sim-to-Real Transfer Techniques for Reinforcement Learning in Humanoid Bipedal Locomotion (2024)

- Venue/authors: IEEE Robotics & Automation Magazine; Donghyeon Kim; Hokyun Lee; Junhyeok Cha; Jaeheung Park
- Category: policy_transfer; citations: 7
- Problem claimed: Train policies in simulation that perform on a physical robot.
- Actual mechanism introduced: Use reinforcement learning, robust objectives, demonstrations, curriculum, or adaptation at deployment.
- Hidden assumptions: Task return can drive the right invariant behavior despite sparse real feedback.
- Variables treated as fixed: Failure explanation, deployment probes, and causal separation between nuisance shift and mechanism shift.
- Failure modes ignored: Low-trial diagnostic settings and mechanisms whose repairs reduce immediate reward before improving transfer.
- What it makes less novel: A general sim-trained policy transfer contribution.
- What it leaves open: A repairable failure-mechanism representation for sample-limited deployment.
- Source: https://doi.org/10.1109/mra.2024.3505784

