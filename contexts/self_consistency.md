# Optimizing for Self-Consistency in Language Models

## Research Focus
Self-consistency as a unifying framework for understanding and improving LM behavior — moving from per-input optimization (SFT/RL) to cross-input consistency constraints that capture relational properties between model behaviors.

## Core Problems
- Standard training optimizes per-input independently, leading to inconsistent behavior across related inputs
- Sycophancy: models shift responses based on user framing rather than maintaining stable positions
- Incomplete logical generalization and factual inconsistency
- Confident but incorrect responses that can only be detected by examining relationships between outputs
- Current desiderata for LMs cannot be expressed at the level of single datapoints

## Key Concepts & Framework
- Consistency function phi(x1,...,xn, y1,...,yn) scoring groups of input-output pairs
- Three optimization approaches: hard constraints, soft regularization, posterior regularization
- Instance-level objectives: symmetric constraints between model input-output instances
  - Invariances: transformations that should leave output unchanged (sycophancy, robustness to spurious cues, bias)
  - Equivariances: input transformations that should induce corresponding output transformations (factual consistency, knowledge modification)
- Meta-level objectives: consistency between self-referential "meta-responses" and instance-level behavior
  - Self-descriptive objectives: making model introspection faithful
  - Self-alignment objectives: using self-descriptions for model self-improvement

## Methods of Interest
- Cross-input optimization directly enforcing relational structure at the output level
- Defining R (input relations) and S (output relations) to recover existing alignment techniques
- RLHF/RLVR objectives and their limitations (per-input optimization)
- Calibration as a self-consistency constraint
- Chain-of-thought faithfulness as consistency between reasoning trace and output
- Automated self-red-teaming via consistency constraints
- Scientific hypothesis generation through self-consistent model behavior

## Applications
- Anti-sycophancy: penalizing models that change answers based on user preference cues
- Factual consistency under knowledge modification
- Model bias reduction via paraphrase consistency
- Faithful chain-of-thought reasoning
- Model self-improvement through self-critique
- Pluralistic alignment and reversal curse mitigation
- Multilingual consistency

## Key References
- Pres, Li, Ruis et al. (2026) — "Position: It's Time to Optimize for Self-Consistency" (MIT CSAIL / Goodfire)
- Framework connects to: DPO, RLHF, adversarial training, calibration, introspection
