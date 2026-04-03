# arXiv Digest — 2026-04-03
**Research focus:** Forward-Looking LLMs & Multi-Turn Dialogue
**Categories:** cs.AI · cs.CL · cs.LG · stat.ML
**Papers reviewed:** 24 | **Top Picks:** 5 | **Worth a Look:** 13 | **Quick Scan:** 6

> Note: arXiv API was unavailable (proxy block). Papers sourced via web search covering recent submissions (March–April 2026). All IDs verified.

---

## Top Picks (score ≥ 8)

---

### [When and What to Ask: AskBench and Rubric-Guided RLVR for LLM Clarification](https://arxiv.org/abs/2602.11199)
**Authors:** Jiale Zhao, Ke Fang, Lu Cheng
**Score: 10/10**

**One-line summary:** Introduces AskBench — an interactive multi-turn benchmark that rewards targeted clarification — and a GRPO-based RL recipe (rubric-guided RLVR) that trains LLMs to decide *when* to ask and *what* to ask.

**Key contribution:** AskBench transforms standard QA into multi-turn interactions with explicit checkpoints; a unified judge loop grades final answers and simulates user responses. Two sub-settings test different failure modes: *AskMind* (intent-deficient queries) and *AskOverconfidence* (false-premise queries). The rubric-guided RLVR training improves accuracy, rubric adherence, and interaction efficiency with strong generalization to unseen domains.

**Why it matters:** This is the most direct implementation of the "clarification vs. answering" decision framed as a learnable policy. AskBench's checkpoint-based evaluation and the false-premise track map directly onto the Commit / Repair intent taxonomy. The RLVR formulation is a concrete alternative to the DP/OR framing the research aims to pursue — the benchmark itself is immediately adoptable.

---

### [Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents](https://arxiv.org/abs/2603.26233)
**Authors:** Nicholas Edwards, Sebastian Schuster (University of Vienna)
**Score: 9/10**

**One-line summary:** Proposes a multi-agent scaffold that explicitly decouples uncertainty detection from code execution, achieving 69.4% on underspecified SWE-bench vs. 61.2% for a standard single-agent baseline.

**Key contribution:** Evaluates LLM agents on an underspecified variant of SWE-bench Verified. The scaffold separates (1) detecting underspecification and deciding whether to ask from (2) executing the task — an architectural instantiation of the "Clarify vs. Commit" split. Uses internal model uncertainty as the decision signal rather than a learned policy.

**Why it matters:** Provides empirical evidence that explicit clarification-seeking pays off at scale (+8.2 pp on a realistic software-engineering benchmark). The uncertainty-decoupling design aligns with the "decision layer as a first-class module" principle and can inform the typed action abstraction (Clarify, Commit, Repair).

---

### [Structured Uncertainty Guided Clarification for LLM Agents](https://arxiv.org/abs/2511.08798)
**Authors:** Manan Suri, Puneet Mathur, Nedim Lipka, Franck Dernoncourt, Ryan A. Rossi, Dinesh Manocha
**Score: 9/10**

**One-line summary:** SAGE-Agent models tool-parameter clarification as a POMDP with an EVPI (Expected Value of Perfect Information) objective, achieving 7–39% better coverage while reducing clarification questions by 1.5–2.7×.

**Key contribution:** Introduces structured uncertainty over tool-call parameters — modeling the joint clarification problem as a POMDP. Uses EVPI as the objective for selecting which question to ask, with aspect-based cost modeling to prevent redundant questions. SAGE-Agent significantly outperforms prompting and uncertainty-based baselines.

**Why it matters:** This is the closest existing work to the VoI formulation (Dong et al. 2026) applied to tool-use agents. The POMDP + EVPI framework is exactly the type of decision-theoretic, interpretable mechanism the research targets. Directly informs formal modeling of the Clarify action with a cost-benefit structure.

---

### [Intent Mismatch Causes LLMs to Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2602.07338)
**Authors:** Geng Liu, Fei Zhu, Rong Feng, Changyi Ma, Shiqi Wang, Gaofeng Meng
**Score: 9/10**

**One-line summary:** Argues the "Lost in Conversation" (LiC) phenomenon is not a capability failure but a structural *intent alignment gap* — and theoretically proves scaling alone cannot fix it.

**Key contribution:** Uses a semi-automated "sharding" pipeline (like Laban et al. 2025) to decompose fully-specified instructions into atomic, self-contained constraints revealed across turns. Proposes a Mediator-Assistant pipeline where a Mediator explicates user inputs and an LLM Refiner distills interaction guidelines from historical patterns. Proves theoretically that the LiC gap arises from structural ambiguity in conversational context, not representational limitations.

**Why it matters:** The theoretical impossibility result is a key motivating argument for this research agenda — scaling won't solve multi-turn degradation; explicit dialogue management is required. The sharding pipeline independently validates the approach from Laban et al. 2025. The Mediator-Refiner architecture maps to the Repair action and context-repair dialogue moves.

---

### [Confidence Estimation for LLMs in Multi-turn Interactions](https://arxiv.org/abs/2601.02179)
**Authors:** Caiqi Zhang, Ruihan Yang, Xiaochen Zhu, Chengzu Li, Tiancheng Hu, Yijiang River Dong, Deqing Yang, Nigel Collier
**Score: 8/10**

**One-line summary:** First systematic study of confidence calibration *across turns*, introducing monotonicity as a desideratum and a length-normalized ECE metric (InfoECE) using a new "Hinter-Guesser" paradigm.

**Key contribution:** Establishes a formal multi-turn confidence evaluation framework with two desiderata: (1) per-turn calibration and (2) monotonicity — confidence should increase as more information is revealed. Introduces InfoECE (length-normalized Expected Calibration Error) and a "Hinter-Guesser" dataset generator for controlled evaluation. Finds current LLMs violate monotonicity significantly.

**Why it matters:** The monotonicity requirement is precisely the property a forward-looking model needs when integrating sharded information across turns. InfoECE and the Hinter-Guesser paradigm are directly applicable as evaluation tools for the research. The monotonicity violation finding motivates training interventions.

---

## Worth a Look (score 5–7)

| # | Paper | Score | One-line summary |
|---|-------|-------|-----------------|
| 1 | [Asymmetric Actor-Critic for Multi-turn LLM Agents](https://arxiv.org/abs/2604.00304) — Jiang et al. (Apr 2026) | **7** | A large proprietary LLM acts as actor while a small open-source critic monitors and intervenes at runtime — separates policy from evaluation without full RL retraining. |
| 2 | [Confidence Before Answering: A Paradigm Shift for Efficient LLM Uncertainty Estimation](https://arxiv.org/abs/2603.05881) — Li et al. (Mar 2026) | **7** | CoCA uses GRPO RL with segmented rewards to train models to output calibrated confidence *before* answering, improving calibration without sacrificing accuracy. |
| 3 | [Quantifying Conversational Reliability of LLMs under Multi-Turn Interaction](https://arxiv.org/abs/2603.01423) — Myung (Mar 2026) | **7** | Systematic reliability degradation study across global-constraint, tool-selection, and entity-tracking tasks; identifies instruction drift, intent confusion, and contextual overwriting as key failure modes. |
| 4 | [Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey](https://arxiv.org/abs/2603.04445) — Moslem & Kelleher (Mar 2026) | **7** | Comprehensive survey of routing/cascading paradigms (difficulty, uncertainty, RL, clustering) across independently trained LLMs — the reference survey for the routing-as-dialogue-policy angle. |
| 5 | [Routing, Cascades, and User Choice for LLMs](https://arxiv.org/abs/2602.09902) — Mahmood (Feb 2026) | **7** | Game-theoretic model of provider-user routing misalignment; derives the optimal routing policy as a static threshold rule, revealing a fundamental misalignment gap when utility rankings differ. |
| 6 | [Clarify or Answer: Reinforcement Learning for Agentic VQA with Context Under-specification](https://arxiv.org/abs/2601.16400) — Cao, Wen, Wang (Jan 2026) | **6** | CoA agent uses GRPO-CR RL to train a binary Clarify/Answer decision + question generation for under-specified visual QA; introduces CONTEXTCLARIFY benchmark. |
| 7 | [ClarEval: A Benchmark for Evaluating Clarification Skills of Code Agents under Ambiguous Instructions](https://arxiv.org/abs/2603.00187) — Li, Wu, Chang (Feb 2026) | **6** | Injects 3 ambiguity types (missing goals, premises, ambiguous terminology) into coding tasks; proposes Average Turns to Clarify (ATC) and Key Question Coverage (KQC) metrics. |
| 8 | [TSR: Trajectory-Search Rollouts for Multi-Turn RL of LLM Agents](https://arxiv.org/abs/2602.11767) — (Feb 2026) | **6** | Lightweight tree-style search at training time constructs high-quality multi-turn trajectories by selecting high-scoring actions per turn — relevant to forward-looking rollout planning. |
| 9 | [ProAgentBench: Evaluating LLM Agents for Proactive Assistance with Real-World Data](https://arxiv.org/abs/2602.04482) — (Feb 2026) | **6** | Benchmarks proactive agents on timing prediction + content generation for assistance without explicit prompts; evaluates anticipatory intent modeling. |
| 10 | [Clarifying Ambiguities: On the Role of Ambiguity Types in Prompting Methods for Clarification Generation](https://arxiv.org/abs/2504.12113) — Tang, Soulier, Guigue (Apr 2025) | **6** | AT-CoT: predict ambiguity type first, then generate clarification — improves over vanilla CoT; validates the ClarifyMT-Bench ambiguity taxonomy in practice. |
| 11 | [ClarifyMT-Bench: Benchmarking Multi-Turn Clarification for Conversational LLMs](https://arxiv.org/abs/2512.21120) — (Dec 2025) | **6** | First benchmark with 5-dimensional ambiguity taxonomy and 6 user personas; 6,120 multi-turn interactions for evaluating open-domain clarification under noisy user behavior. |
| 12 | [Evaluating LLM-based Agents for Multi-Turn Conversations: A Survey](https://arxiv.org/abs/2503.22458) — (Mar 2025) | **5** | Survey of evaluation methods for multi-turn agents covering context management, reliability, and component-level assessment. |
| 13 | [Beyond Single-Turn: A Survey on Multi-Turn Interactions with Large Language Models](https://arxiv.org/abs/2504.04717) — (Apr 2025) | **5** | Broad survey of multi-turn interaction capabilities, failure modes, and evaluation methodologies. |

---

## Quick Scan (score < 5)

| Paper | arXiv ID | Score |
|-------|----------|-------|
| Agent Q-Mix: Selecting the Right Action for LLM Multi-Agent Systems through RL | [2604.00344](https://arxiv.org/abs/2604.00344) | 4 |
| Cascade-Aware Multi-Agent Routing: Spatio-Temporal Sidecars | [2603.17112](https://arxiv.org/abs/2603.17112) | 4 |
| Reward Shaping to Mitigate Reward Hacking in RLHF | [2502.18770](https://arxiv.org/abs/2502.18770) | 3 |
| Scheduling LLM Inference with Uncertainty-Aware Output Length Predictions | [2604.00499](https://arxiv.org/abs/2604.00499) | 3 |
| "Who Am I, and Who Else Is Here?" Behavioral Differentiation in Multi-Agent LLM Systems | [2604.00026](https://arxiv.org/abs/2604.00026) | 3 |
| Competition and Cooperation of LLM Agents in Games | [2604.00487](https://arxiv.org/abs/2604.00487) | 2 |

---

## Digest Notes

**Emerging cluster:** There is now a tight cluster of papers all attacking the *clarify-vs-answer* decision from different angles (AskBench/RLVR, Ask-or-Assume, CoA/VQA, ClarEval, SAGE/POMDP). Together they establish: (a) the decision is learnable via RL; (b) uncertainty-based gating reliably outperforms always-answer baselines; (c) cost-efficient clarification requires VoI-style question selection, not naive entropy thresholds.

**Routing connection:** The routing papers (2603.04445 survey, 2602.09902 game-theoretic) confirm the analogy between speculative decoding/cascading and the Commit→clarify decision ladder. The misalignment gap in 2602.09902 maps directly to the provider/user utility divergence in multi-turn dialogue.

**Missing gap:** No paper yet treats *repair* as a first-class planned action (versus reactive error correction). The Mediator-Refiner in 2602.07338 is the closest, but it doesn't model Repair within the same decision framework as Clarify/Commit.
