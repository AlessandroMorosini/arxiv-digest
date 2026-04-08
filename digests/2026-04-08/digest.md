# arXiv Daily Digest — 2026-04-08

**Research context:** Forward-Looking LLMs & Multi-Turn Dialogue  
**Papers fetched:** 15 | **Analyzed in depth:** 4 | **Relevance threshold:** 8  
**Categories:** cs.AI, cs.CL, cs.LG, stat.ML

---

## Top Picks (score ≥ 8)

### [Agentic Uncertainty Quantification](https://arxiv.org/abs/2601.15703) — 9/10
**Authors:** Jiaxin Zhang, Prafulla Kumar Choubey, Shubham Toshniwal, Caiming Xiong, Chien-Sheng Wu | *cs.AI, cs.CL, cs.LG*

*Dual-Process AUQ framework transforms verbalized uncertainty into active bi-directional control signals that trigger targeted reflection only when needed — training-free, inference-time only.*

**Key contribution:** Two-mechanism architecture — UAM (Uncertainty-Aware Memory, System 1: implicit confidence propagation to prevent blind decisions) + UAR (Uncertainty-Aware Reflection, System 2: targeted correction triggered by uncertainty cues only when necessary). Addresses the "Spiral of Hallucination" where early epistemic errors propagate irreversibly through agent trajectories.

**Why it matters for this research:** The "Spiral of Hallucination" is the exact *error propagation* failure mode motivating the Repair action. UAR's selective trigger logic ("only when necessary") is structurally equivalent to the Clarify/Commit/Repair gating decision. Trajectory-level calibration maps directly to rollout variance as an action selection signal. Strong baseline for the uncertainty → action decision pipeline.

---

### [Are LLM Decisions Faithful to Verbal Confidence?](https://arxiv.org/abs/2601.07767) — 9/10
**Authors:** Ori Shapira, Ori Ernst, Ran Levy, Ido Dagan | *cs.CL, cs.AI*

*Empirical study showing that models accurately verbalize uncertainty but systematically fail to act on it — leading to named failure modes: "partner-blind over-clarification" and "question-averse guessing."*

**Key contribution:** Identifies and names the calibration-action gap: verbalized confidence ≠ decision-level behavior. Specific failure modes — models clarify when they shouldn't (over-clarification) and commit when they should clarify (question-averse guessing under uncertainty). Provides empirical evidence and analysis of why this disconnect persists.

**Why it matters for this research:** This paper provides direct empirical motivation for the forward-LM project. The named failure modes are precisely what the {Clarify, Commit, Repair} action framework aims to fix. The calibration-action gap is the problem that explicit decision layers (DP/VoI) are designed to bridge. Can be cited as primary motivation; the failure modes serve as concrete benchmark targets.

---

### [AT2PO: Agentic Turn-based Policy Optimization via Tree Search](https://arxiv.org/abs/2601.04767) — 8/10
**Authors:** Zefang Zong, Dingwei Chen, Yang Li, Qi Yi, Bo Zhou, Chengming Li, Bo Qian, Peng Chen, Jie Jiang | *cs.AI, cs.CL*

*Unified multi-turn agentic RL with entropy-guided tree expansion, turn-level credit assignment, and a turn-granularity policy optimization objective — evaluated across 7 benchmarks.*

**Key contribution:** (1) Entropy-Guided Tree Expansion for strategic diversity in rollout exploration; (2) Turn-wise Credit Assignment for fine-grained reward propagation from sparse outcomes; (3) Turn-level policy optimization objective aligned with natural decision boundaries of agentic interactions.

**Why it matters for this research:** Tree search for turn-level policy optimization is the MCTS lookahead thread in this project. Turn-wise credit assignment addresses path-dependence and sparse-reward problems in multi-turn DP. Entropy-guided expansion links uncertainty to exploration — a key mechanism for the forward-looking action selection. Strong empirical baseline across diverse tasks.

---

### [Conversation Tree Architecture: A Structured Framework for Context-Aware Multi-Branch LLM Conversations](https://arxiv.org/abs/2603.21278) — 8/10
**Authors:** Pranav Hemanth, Sampriti Saha | *cs.CL, cs.AI*

*Hierarchical conversation trees with context-isolated nodes and "volatile" transient branches that can be selectively merged or permanently discarded — addressing "logical context poisoning."*

**Key contribution:** Formalizes context pollution as "logical context poisoning"; introduces volatile nodes — transient branches whose context must be selectively merged upward or permanently discarded before purging. Each node maintains its own local context window with structured parent-child context flow.

**Why it matters for this research:** Volatile nodes with merge/discard semantics are a structural implementation of the Repair action. The CTA framework operationalizes context pollution repair as a first-class mechanism. Context isolation and structured context flow provide an architectural foundation for the DP state representation. Complements Laban et al. 2025 on multi-turn degradation with a structural fix.

---

## Worth a Look (score 5–7)

- **[Let's Have a Conversation: Designing and Evaluating LLM Agents for Interactive Optimization](https://arxiv.org/abs/2604.02666)** (7/10) — LLM agents for interactive optimization governed by internal utility functions; proposes conversation-based evaluation by having LLMs role-play stakeholders with different utility functions. Methodology for evaluating conversation quality is directly useful. *cs.AI, cs.CL*

- **[Adaptive Confidence Gating in Multi-Agent Collaboration](https://arxiv.org/abs/2601.21469)** (7/10) — Confidence-based routing/stopping criterion in multi-agent pipelines; gates whether tasks proceed or route back for revision based on confidence scores. Analogous to Clarify/Commit gating decisions, though applied to code generation. *cs.AI*

- **[RACER: Risk-Aware Calibrated Efficient Routing for LLMs](https://arxiv.org/abs/2603.06616)** (7/10) — LLM routing as alpha-VOR problem; calibrated model sets with distribution-free risk control and abstention. Rigorous theoretical guarantees on routing risk. Related to routing/cascading with uncertainty thread. *cs.LG*

- **[Proximity-Based Multi-Turn Optimization (ProxMO)](https://arxiv.org/abs/2602.19225)** (7/10) — Multi-turn credit assignment integrating episode-level difficulty (success-rate-aware modulation) and step-level semantic baselines (proximity-based soft aggregation). Methodologically relevant to DP formulations for multi-turn dialogue. *cs.AI*

- **[Reward-Based Online LLM Routing via NeuralUCB](https://arxiv.org/abs/2603.30035)** (6/10) — LLM routing as contextual bandit with NeuralUCB; online cost-quality tradeoff learning. UCB exploration connects to uncertainty-driven routing. *cs.LG*

- **[Variational Routing: Bayesian Framework for Calibrated MoE Transformers](https://arxiv.org/abs/2603.09453)** (6/10) — Bayesian inference for MoE routing with 94% calibration error reduction and 38% routing stability improvement. Architecture-level calibration. *cs.LG*

- **[ProRL Agent: Rollout-as-a-Service for RL Training of Multi-Turn LLM Agents](https://arxiv.org/abs/2603.18815)** (6/10) — Decoupled rollout infrastructure for multi-turn RL training; asynchronous assembly line separating env interactions from GPU policy updates. Infrastructure for trajectory simulation at scale. *cs.AI*

- **[Beyond the Context Window: Fact-Based Memory vs. Long-Context LLMs](https://arxiv.org/abs/2603.04814)** (5/10) — Cost-performance analysis showing fact-based memory outperforms long-context on multi-session tasks; context management for persistent agents. Tangentially relevant to context state in dialogue. *cs.CL*

- **[SIEVE: Sample-Efficient Parametric Learning from Natural Language](https://arxiv.org/abs/2604.02339)** (5/10) — Iterative refinement of parametric models from underspecified natural language feedback. Underspecification theme connects to ambiguity in dialogue, though different application. *cs.CL*

---

## Quick Scan (score < 5)

| Title | Authors | Score |
|---|---|---|
| [Analysis of Optimality of Large Language Models on Planning Problems](https://arxiv.org/abs/2604.02910) | Bohnet, Nova, Croce, Vinyals, Bachem | 4 |
| [Speaker-Reasoner: Scaling Interaction Turns and Reasoning Patterns for Timestamped Speaker-Attributed ASR](https://arxiv.org/abs/2604.03074) | Wang, Lee, Liang, Qin, Cheng, Chen | 3 |

---

## Paper Analysis Cards
*(Generated by deep-analysis subagents — see individual card files)*

- `card_2601.15703.md` — Agentic Uncertainty Quantification (9/10)
- `card_2601.07767.md` — Are LLM Decisions Faithful to Verbal Confidence? (9/10)
- `card_2601.04767.md` — AT2PO: Agentic Turn-based Policy Optimization (8/10)
- `card_2603.21278.md` — Conversation Tree Architecture (8/10)

---

*Generated: 2026-04-08 | Context: contexts/forward_lm.md*
