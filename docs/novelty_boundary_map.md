# Novelty Boundary Map

## What Is Not Novel Enough

- Training a larger robot policy or world model.
- Adding more randomized textures, lighting, masses, or friction ranges.
- Aligning source and target features without proving repair relevance.
- Estimating a larger set of simulator parameters before deployment.
- Adding uncertainty, active learning, a verifier, or an LLM planner without changing the central adaptation coordinate.
- Reporting a new benchmark without a new mechanism.

## Crowded Mechanism Boundaries

### policy_transfer (122 of top 300)
- Review of machine learning in robotic grasping control in space application (2024): makes less novel -> A general sim-trained policy transfer contribution.
- Learning Variable Impedance Control for Aerial Sliding on Uneven Heterogeneous Surfaces by Proprioceptive and Tactile Sensing (2022): makes less novel -> A general sim-trained policy transfer contribution.
- Bi-Touch: Bimanual Tactile Manipulation With Sim-to-Real Deep Reinforcement Learning (2023): makes less novel -> A general sim-trained policy transfer contribution.
- Zero-shot sim-to-real transfer of reinforcement learning framework for robotics manipulation with demonstration and force feedback (2022): makes less novel -> A general sim-trained policy transfer contribution.
- Sim-to-Real Robot Learning from Pixels with Progressive Nets (2016): makes less novel -> A general sim-trained policy transfer contribution.

### domain_randomization (55 of top 300)
- Domain Randomization for Sim2real Transfer of Automatically Generated Grasping Datasets (2024): makes less novel -> A broad claim that randomized simulation improves robustness or transfer.
- Domain randomization for transferring deep neural networks from simulation to the real world (2017): makes less novel -> A broad claim that randomized simulation improves robustness or transfer.
- Real-World Robotic Perception and Control Using Synthetic Data (2019): makes less novel -> A broad claim that randomized simulation improves robustness or transfer.
- Learning Locomotion for Quadruped Robots via Distributional Ensemble Actor-Critic (2024): makes less novel -> A broad claim that randomized simulation improves robustness or transfer.
- Robot Learning From Randomized Simulations: A Review (2022): makes less novel -> A broad claim that randomized simulation improves robustness or transfer.

### contact_manipulation (41 of top 300)
- Sim-to-Real Transfer for Robotic Manipulation with Tactile Sensory (2021): makes less novel -> Showing that contact dynamics matter for sim-to-real manipulation.
- Sim-to-Real for Robotic Tactile Sensing via Physics-Based Simulation and Learned Latent Projections (2021): makes less novel -> Showing that contact dynamics matter for sim-to-real manipulation.
- Grasp Stability Prediction with Sim-to-Real Transfer from Tactile Sensing (2022): makes less novel -> Showing that contact dynamics matter for sim-to-real manipulation.
- An Unconstrained Convex Formulation of Compliant Contact (2022): makes less novel -> Showing that contact dynamics matter for sim-to-real manipulation.
- Revolutionizing self-powered robotic systems with triboelectric nanogenerators (2023): makes less novel -> Showing that contact dynamics matter for sim-to-real manipulation.

### locomotion (24 of top 300)
- Cat-Like Jumping and Landing of Legged Robots in Low Gravity Using Deep Reinforcement Learning (2021): makes less novel -> Locomotion sim-to-real through randomized or adaptive policies.
- Optimization-Based Control for Dynamic Legged Robots (2023): makes less novel -> Locomotion sim-to-real through randomized or adaptive policies.
- The Transferability Approach: Crossing the Reality Gap in Evolutionary Robotics (2012): makes less novel -> Locomotion sim-to-real through randomized or adaptive policies.
- Learning Agile Robotic Locomotion Skills by Imitating Animals (2020): makes less novel -> Locomotion sim-to-real through randomized or adaptive policies.
- A Review of Jamming Actuation in Soft Robotics (2020): makes less novel -> Locomotion sim-to-real through randomized or adaptive policies.

### domain_adaptation (22 of top 300)
- A Sim-to-Real Learning-Based Framework for Contact-Rich Assembly by Utilizing CycleGAN and Force Control (2023): makes less novel -> A generic feature-alignment framing for sim-to-real transfer.
- Grasp Stability Assessment Through Attention-Guided Cross-Modality Fusion and Transfer Learning (2023): makes less novel -> A generic feature-alignment framing for sim-to-real transfer.
- Sim-to-Real Transfer of Robotic Assembly with Visual Inputs Using CycleGAN and Force Control (2022): makes less novel -> A generic feature-alignment framing for sim-to-real transfer.
- Zero-Shot Sim-to-Real Transfer of Tactile Control Policies for Aggressive Swing-Up Manipulation (2021): makes less novel -> A generic feature-alignment framing for sim-to-real transfer.
- Kalman Filter-Based One-Shot Sim-to-Real Transfer Learning (2023): makes less novel -> A generic feature-alignment framing for sim-to-real transfer.

### system_identification (18 of top 300)
- Sim-to-Real: Learning Agile Locomotion For Quadruped Robots (2018): makes less novel -> Claims that transfer can be repaired by estimating simulator parameters.
- Sim-to-Real Transfer of Compliant Bipedal Locomotion on Torque Sensor-Less Gear-Driven Humanoid (2023): makes less novel -> Claims that transfer can be repaired by estimating simulator parameters.
- Modelling and identification methods for simulation of cable-suspended dual-arm robotic systems (2024): makes less novel -> Claims that transfer can be repaired by estimating simulator parameters.
- Rapid Locomotion via Reinforcement Learning (2022): makes less novel -> Claims that transfer can be repaired by estimating simulator parameters.
- Preparing for the Unknown: Learning a Universal Policy with Online System Identification (2017): makes less novel -> Claims that transfer can be repaired by estimating simulator parameters.

### simulation_training (8 of top 300)
- Scalable sim-to-real transfer of soft robot designs (2020): makes less novel -> More simulation as the source of robot generalization.
- Collaborative Multi-Robot Search and Rescue: Planning, Coordination, Perception, and Active Vision (2020): makes less novel -> More simulation as the source of robot generalization.
- Render-in-the-loop Aerial Robotics Simulator: Case Study on Yield Estimation in Indoor Agriculture (2022): makes less novel -> More simulation as the source of robot generalization.
- Fully neuromorphic vision and control for autonomous drone flight (2024): makes less novel -> More simulation as the source of robot generalization.
- Transferability in the Automatic Off-Line Design of Robot Swarms: From Sim-to-Real to Embodiment and Design-Method Transfer Across Different Platforms (2024): makes less novel -> More simulation as the source of robot generalization.

### tactile (6 of top 300)
- Attention for Robot Touch: Tactile Saliency Prediction for Robust Sim-to-Real Tactile Control (2023): makes less novel -> Using tactile observations as additional transfer signal.
- Predicting the Force Map of an ERT-Based Tactile Sensor Using Simulation and Deep Networks (2022): makes less novel -> Using tactile observations as additional transfer signal.
- Deep Neural Network Based Electrical Impedance Tomographic Sensing Methodology for Large-Area Robotic Tactile Sensing (2021): makes less novel -> Using tactile observations as additional transfer signal.
- Methods and Sensors for Slip Detection in Robotics: A Survey (2020): makes less novel -> Using tactile observations as additional transfer signal.
- A soft thumb-sized vision-based sensor with accurate all-round force perception (2022): makes less novel -> Using tactile observations as additional transfer signal.

### failure_analysis (3 of top 300)
- A High-Fidelity Simulation Platform for Industrial Manufacturing by Incorporating Robotic Dynamics Into an Industrial Simulation Tool (2022): makes less novel -> Failure classification or recovery as a standalone robotics module.
- Empirical assessment and comparison of neuro-evolutionary methods for the automatic off-line design of robot swarms (2021): makes less novel -> Failure classification or recovery as a standalone robotics module.
- Detecting Attacks Against Robotic Vehicles (2018): makes less novel -> Failure classification or recovery as a standalone robotics module.

### causal_robotics (1 of top 300)
- 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) (2024): makes less novel -> The abstract claim that causal variables aid transfer.

## Surviving Boundary

The surviving boundary is not another domain-randomized policy, residual adapter, or system identifier. The proposed contribution must show that domain-level statistics are the wrong object in at least one realistic robotics transfer setting, and that diagnosing the failure mechanism yields a different and better repair. The contribution is strongest if it includes an impossibility example for statistic-only adapters and a runnable robot-control simulation where the same domain summary aliases incompatible repairs.
