# arXiv Digest — 2026-04-06
**Research context:** Forward-Looking LLMs & Multi-Turn Dialogue
**Categories:** cs.AI, cs.CL, cs.LG, stat.ML
**Papers reviewed:** 42 | **Top Picks:** 17 | **Worth a Look:** 5 | **Quick Scan:** 20

> **Note:** arXiv network access is blocked in this environment. This digest covers papers fetched through 2026-04-05, including all recent papers from the cs.AI/CL/LG/stat.ML feeds. Today is Monday; arXiv typically announces Friday submissions on Monday, so this captures the most recent available batch.

---

## Top Picks (score ≥ 8)

### [ClarifyMT-Bench: Benchmarking Multi-Turn Clarification for Conversational LLMs](https://arxiv.org/abs/2512.21120)
**Score: 10/10** | arXiv:2512.21120 | Dec 2025

**One-line summary:** A benchmark specifically designed to evaluate multi-turn clarification quality across a taxonomy of ambiguity types in conversational LLMs.

**Key contribution:** Introduces ClarifyMT-Bench, a structured evaluation framework for multi-turn clarification that categorises ambiguity (linguistic, intent, contextual, epistemic, interactional) and measures model performance on when and how to seek clarification across conversation turns.

**Why it matters:** This is one of the key reference works cited directly in the research context (ClarifyMT-Bench taxonomy). It operationalises the ambiguity taxonomy central to the clarification-decision problem and provides the evaluation infrastructure needed to benchmark any forward-looking clarification model. Essential reading.

---

### [When and What to Ask: AskBench and Rubric-Guided RLVR for LLM Clarification](https://arxiv.org/abs/2602.11199)
**Authors:** Jiale Zhao, Ke Fang, Lu Cheng
**Score: 10/10** | arXiv:2602.11199 | Feb 2026

**One-line summary:** Introduces AskBench, a benchmark for the joint "when to ask" and "what to ask" clarification decision, trained with rubric-guided reinforcement learning from verifiable rewards.

**Key contribution:** Formulates clarification as a two-part decision problem (timing + content), builds a dataset with rubric annotations, and uses RLVR to train a model that outperforms prompting baselines on both dimensions.

**Why it matters:** Directly targets the clarify-vs-answer decision at the heart of this research. The RL formulation and rubric-guided reward signal are strong methodological anchors. The "when" framing maps onto the optimal-stopping / DP view of clarification decisions.

---

### [Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents](https://arxiv.org/abs/2603.26233)
**Score: 9/10** | arXiv:2603.26233 | Mar 2026

**One-line summary:** Studies the clarify-or-commit decision in coding agents under uncertainty, using uncertainty signals to decide when to ask rather than assume.

**Key contribution:** Proposes an uncertainty-aware clarification policy for agentic coding tasks, distinguishing between high-confidence assumptions (commit) and low-confidence situations requiring clarification (ask), with empirical benchmarking.

**Why it matters:** Directly instantiates the {Clarify, Commit} intent tuple from the action-abstraction model. The uncertainty-as-trigger framing is precisely the mechanism needed to make clarification decisions interpretable and principled.

---

### [Structured Uncertainty guided Clarification for LLM Agents](https://arxiv.org/abs/2511.08798)
**Score: 9/10** | arXiv:2511.08798 | Nov 2025

**One-line summary:** Uses structured representations of uncertainty to systematically guide when and how LLM agents generate clarifying questions.

**Key contribution:** Introduces a typed uncertainty representation (epistemic vs. aleatoric, scope vs. intent) and uses it to condition clarification generation, producing more targeted and useful clarifying questions than unstructured approaches.

**Why it matters:** The structured uncertainty representation directly maps onto the epistemic/interactional ambiguity taxonomy from ClarifyMT-Bench. Provides a concrete mechanism for the uncertainty-driven clarification layer central to the research agenda.

---

### [Clarify or Answer: Reinforcement Learning for Agentic VQA with Context Under-specification](https://arxiv.org/abs/2601.16400)
**Score: 9/10** | arXiv:2601.16400 | Jan 2026

**One-line summary:** Frames the clarify-vs-answer trade-off as an RL problem in visual question answering when instructions are under-specified, training agents to make optimal decisions at each turn.

**Key contribution:** Casts each dialogue turn as a binary action (clarify / answer), defines reward based on downstream task success, and trains via RL to learn a context-sensitive policy that decides based on estimated information sufficiency.

**Why it matters:** This is one of the closest instantiations of the optimal stopping / DP view of clarification decisions. The under-specification framing directly connects to sharded-instruction scenarios and VoI thinking. The RL approach also contrasts with the DP/OR preference stated in the research context, making it a useful methodological comparison point.

---

### [TSR: Trajectory-Search Rollouts for Multi-Turn RL of LLM Agents](https://arxiv.org/abs/2602.11767)
**Score: 9/10** | arXiv:2602.11767 | Feb 2026

**One-line summary:** Uses trajectory search via multi-step rollouts to evaluate candidate actions before committing, enabling forward-looking multi-turn RL for LLM agents.

**Key contribution:** Proposes Trajectory-Search Rollouts (TSR), which simulate future conversation trajectories from candidate actions to estimate their downstream value, then use these value estimates to guide policy updates in multi-turn RL.

**Why it matters:** This is the most direct existing implementation of "forward-looking planning via trajectory simulation" — exactly the mechanism described in the research context. TSR's value-to-go estimates, rollout-based action evaluation, and multi-turn RL setting are all central to the research agenda. Must-read.

---

### [Intent Mismatch Causes LLMs to Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2602.07338)
**Score: 9/10** | arXiv:2602.07338 | Feb 2026

**One-line summary:** Diagnoses how intent misalignment propagates and compounds across turns, causing multi-turn LLM conversations to degrade — framing "getting lost" as a measurable failure mode.

**Key contribution:** Introduces an intent-tracking evaluation framework that measures when and how LLMs lose alignment with user intent across turns, showing that small per-turn errors compound into large multi-turn failures.

**Why it matters:** Directly quantifies the error-propagation and path-dependence problems that motivate the forward-looking research. The "getting lost" failure mode is precisely what context repair (the Repair action) is designed to address.

---

### [Confidence Estimation for LLMs in Multi-turn Interactions](https://arxiv.org/abs/2601.02179)
**Score: 8/10** | arXiv:2601.02179 | Jan 2026

**One-line summary:** Studies how to estimate and propagate confidence across turns in multi-turn dialogue, where uncertainty accumulates and context shifts.

**Key contribution:** Proposes turn-aware confidence estimation methods that account for context history, showing that single-turn calibration methods degrade in multi-turn settings and proposing corrections.

**Why it matters:** Uncertainty estimation in multi-turn settings is a prerequisite for any confidence-threshold–based routing or clarification policy. The finding that single-turn UE methods fail is foundational justification for research into multi-turn–aware uncertainty.

---

### [Routing, Cascades, and User Choice for LLMs](https://arxiv.org/abs/2602.09902)
**Score: 8/10** | arXiv:2602.09902 | Feb 2026

**One-line summary:** Surveys and unifies LLM routing, cascading, and user-choice frameworks, analysing the trade-offs between cost, quality, and latency across model tiers.

**Key contribution:** Provides a formal treatment of when to route to a stronger model vs. commit to a cheaper one, connecting speculative decoding, cascading, and query routing under a single framework with confidence thresholds as the key decision variable.

**Why it matters:** The routing-as-cascading framing is directly cited in the research context as an analogy for clarification decisions. The confidence-threshold mechanism here maps onto when to ask vs. answer in dialogue. Key methodological resource.

---

### [Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey](https://arxiv.org/abs/2603.04445)
**Score: 8/10** | arXiv:2603.04445 | Mar 2026

**One-line summary:** Comprehensive survey of routing and cascading approaches for LLM inference, covering confidence-based, cost-aware, and multi-model strategies.

**Key contribution:** Taxonomises routing and cascading approaches into confidence-based vs. learned routing, single-call vs. multi-call cascades, and discusses calibration requirements for each strategy.

**Why it matters:** The cascading/routing survey provides the methodological landscape for one of the research context's core topics. Useful for situating new routing-based dialogue policies within the broader literature.

---

### [Quantifying Conversational Reliability of Large Language Models under Multi-Turn Interaction](https://arxiv.org/abs/2603.01423)
**Score: 8/10** | arXiv:2603.01423 | Mar 2026

**One-line summary:** Introduces metrics to quantify how reliably LLMs maintain coherent, consistent behaviour across multiple turns in extended dialogue.

**Key contribution:** Proposes multi-turn reliability metrics capturing consistency (same intent → same response), error propagation (turn-N failure rates conditioned on turn-N-1 errors), and recovery rates (how often models self-repair after mistakes).

**Why it matters:** The error-propagation and recovery-rate metrics directly operationalise path dependence and context repair. The multi-turn coupling perspective aligns closely with the core research claim that turns are not independent subtasks.

---

### [Confidence Before Answering: A Paradigm Shift for Efficient LLM Uncertainty Estimation](https://arxiv.org/abs/2603.05881)
**Score: 8/10** | arXiv:2603.05881 | Mar 2026

**One-line summary:** Proposes generating an explicit confidence estimate before producing an answer, reframing uncertainty estimation as a pre-generation step rather than post-hoc calibration.

**Key contribution:** Shows that prompting or training models to output confidence before answering (rather than extracting it from answer distributions) produces better-calibrated estimates and can be used as a decision gate for routing or clarification.

**Why it matters:** The "confidence before answering" paradigm maps directly onto the decision layer in the clarify-vs-commit action abstraction: estimate uncertainty first, then choose action. This is a concrete implementation of the pre-commitment deliberation mechanism.

---

### [ClarEval: A Benchmark for Evaluating Clarification Skills of Code Agents under Ambiguous Instructions](https://arxiv.org/abs/2603.00187)
**Score: 8/10** | arXiv:2603.00187 | Mar 2026

**One-line summary:** Evaluates the clarification abilities of code agents when instructions are ambiguous, measuring both when to ask and how useful the generated clarifying questions are.

**Key contribution:** ClarEval provides a suite of ambiguous coding tasks annotated with ground-truth ambiguities and evaluates agents on question necessity (should they ask?), question quality (is it targeted?), and downstream task performance after clarification.

**Why it matters:** Extends the clarification evaluation paradigm to the agentic coding domain, with direct applicability to any tool-use or code-generation dialogue agent. The question-necessity evaluation aligns with the optimal-stopping framing.

---

### [Beyond Single-Turn: A Survey on Multi-Turn Interactions with Large Language Models](https://arxiv.org/abs/2504.04717)
**Score: 8/10** | arXiv:2504.04717 | Apr 2025

**One-line summary:** Comprehensive survey of multi-turn LLM interaction, covering dialogue management, context accumulation, error propagation, and evaluation methodologies.

**Key contribution:** Maps the landscape of multi-turn LLM challenges including turn coupling, context window management, consistency across turns, and the gap between single-turn and multi-turn evaluation.

**Why it matters:** The most comprehensive survey backdrop for the research context. Explicitly covers the "turns as coupled subtasks" framing and identifies the absence of forward-looking planning as a gap in current approaches.

---

### [Asymmetric Actor-Critic for Multi-turn LLM Agents](https://arxiv.org/abs/2604.00304)
**Authors:** Shuli Jiang, Zhaoyang Zhang, Yi Zhang, Shuo Yang, Wei Xia, Stefano Soatto
**Score: 8/10** | arXiv:2604.00304 | Mar 2026

**One-line summary:** An asymmetric actor-critic architecture for multi-turn LLM agents where the critic has access to future trajectory information unavailable to the actor, enabling better value estimation for multi-turn decisions.

**Key contribution:** The asymmetric design gives the critic privileged information (e.g., future turn outcomes) during training, improving value estimates for sequential dialogue decisions without requiring the actor to have oracle access at inference time.

**Why it matters:** The asymmetric critic with future-trajectory access is a direct implementation of value-to-go estimation for multi-turn dialogue. The architecture bridges RL-based and planning-based approaches to forward-looking dialogue.

---

### [Evaluating LLM-based Agents for Multi-Turn Conversations: A Survey](https://arxiv.org/abs/2503.22458)
**Score: 8/10** | arXiv:2503.22458 | Mar 2025

**One-line summary:** Surveys evaluation methodologies for multi-turn LLM conversation agents, identifying gaps in how current benchmarks capture turn-level dependencies and long-horizon performance.

**Key contribution:** Systematically reviews how existing benchmarks fail to capture multi-turn coupling effects, proposes evaluation criteria including turn-conditional success rates, error recovery metrics, and dialogue-level coherence scores.

**Why it matters:** Directly identifies the evaluation gap this research must address. The critique of single-turn–centric evaluation benchmarks is the justification for building multi-turn–aware metrics and training objectives.

---

### [Clarifying Ambiguities: on the Role of Ambiguity Types in Prompting Methods for Clarification Generation](https://arxiv.org/abs/2504.12113)
**Score: 8/10** | arXiv:2504.12113 | Apr 2025

**One-line summary:** Analyses how different ambiguity types (lexical, syntactic, intent, reference) require different prompting strategies for effective clarification generation.

**Key contribution:** Shows that a single prompting approach underperforms across ambiguity types and that type-aware prompting significantly improves clarification quality, validating the importance of the ambiguity taxonomy.

**Why it matters:** Directly supports the ClarifyMT-Bench taxonomy and provides prompting baselines to beat with the typed action-abstraction model. The finding that ambiguity type matters confirms that the {Clarify, Commit, Repair} intent set needs type-conditional instantiation.

---

## Worth a Look (score 5–7)

| Title | Score | One-line summary |
|-------|-------|-----------------|
| [Reasoning Shift: How Context Silently Shortens LLM Reasoning](https://arxiv.org/abs/2604.01161) | 7 | Demonstrates that provided context silently suppresses extended reasoning traces in test-time scaling models — a context-pollution mechanism relevant to dialogue context repair. |
| [Towards Reliable Truth-Aligned Uncertainty Estimation in Large Language Models](https://arxiv.org/abs/2604.00445) | 7 | Addresses instability in UE metrics across configurations; proposes truth-aligned calibration objectives — relevant to building reliable confidence signals for routing/clarification. |
| [Think Twice Before You Write — an Entropy-based Decoding Strategy to Enhance LLM Reasoning](https://arxiv.org/abs/2604.00018) | 6 | Entropy-based decoding that triggers deliberation at high-uncertainty token positions; analogous to the pre-commitment uncertainty check in the clarify-vs-commit decision. |
| [Aletheia: Quantifying Cognitive Conviction in Reasoning Models via Regularized Inverse Confusion Matrix](https://arxiv.org/abs/2601.01532) | 6 | Proposes calibration metrics for reasoning model confidence, including suppression and escalation failure modes across Claude Sonnet 4.6, GPT-5.2, and others. |
| [ProAgentBench: Evaluating LLM Agents for Proactive Assistance with Real-World Data](https://arxiv.org/abs/2602.04482) | 6 | Benchmark for proactive agent behaviour; overlaps with clarification-seeking in that proactive assistance requires anticipating user needs across turns. |
| [Do Language Models Know When They'll Refuse? Probing Introspective Awareness of Safety Boundaries](https://arxiv.org/abs/2604.00228) | 5 | Models can partially predict their own refusals; introspective accuracy is relevant to self-aware uncertainty estimation. |
| [Emergent Introspective Awareness in Large Language Models](https://arxiv.org/abs/2601.01828) | 5 | Investigates LLM introspection on internal states via interpretability; relevant to whether uncertainty representations are genuine or confabulated. |
| [Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666) | 5 | Proposes a 12-metric decomposition of agent reliability across consistency, robustness, predictability, and safety — useful scaffolding for multi-turn reliability evaluation. |

---

## Quick Scan (score < 5)

| Title | arXiv ID | Score |
|-------|----------|-------|
| Cascade-Aware Multi-Agent Routing: Spatio-Temporal Sidecars and Geometry-Switching | [2603.17112](https://arxiv.org/abs/2603.17112) | 4 |
| Consistency Amplifies: How Behavioral Variance Shapes Agent Accuracy | [2603.25764](https://arxiv.org/abs/2603.25764) | 4 |
| When Agents Disagree With Themselves: Measuring Behavioral Consistency in LLM-Based Agents | [2602.11619](https://arxiv.org/abs/2602.11619) | 4 |
| A Positive Case for Faithfulness: LLM Self-Explanations Help Predict Model Behavior | [2602.02639](https://arxiv.org/abs/2602.02639) | 4 |
| ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions | [2601.06112](https://arxiv.org/abs/2601.06112) | 4 |
| Agent Q-Mix: Selecting the Right Action for LLM Multi-Agent Systems through Reinforcement Learning | [2604.00344](https://arxiv.org/abs/2604.00344) | 4 |
| Scheduling LLM Inference with Uncertainty-Aware Output Length Predictions | [2604.00499](https://arxiv.org/abs/2604.00499) | 3 |
| "Who Am I, and Who Else Is Here?" Behavioral Differentiation Without Role Assignment in Multi-Agent LLM Systems | [2604.00026](https://arxiv.org/abs/2604.00026) | 3 |
| Evaluating Robustness of Large Language Models in Enterprise Applications | [2601.06341](https://arxiv.org/abs/2601.06341) | 3 |
| Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus | [2603.29292](https://arxiv.org/abs/2603.29292) | 3 |
| Reward Shaping to Mitigate Reward Hacking in RLHF | [2502.18770](https://arxiv.org/abs/2502.18770) | 3 |
| Competition and Cooperation of LLM Agents in Games | [2604.00487](https://arxiv.org/abs/2604.00487) | 3 |
| Do LLMs Know What Is Private Internally? Probing and Steering Contextual Privacy Norms | [2604.00209](https://arxiv.org/abs/2604.00209) | 2 |
| Breaking the Reversal Curse in Autoregressive Language Models via Identity Bridge | [2602.02470](https://arxiv.org/abs/2602.02470) | 2 |
| Optimizing Language Models for Crosslingual Knowledge Consistency | [2603.04678](https://arxiv.org/abs/2603.04678) | 2 |
| Competition and Cooperation of LLM Agents in Games | [2604.00487](https://arxiv.org/abs/2604.00487) | 2 |
| Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay | [2601.10589](https://arxiv.org/abs/2601.10589) | 2 |
| More Human, More Efficient: Aligning Annotations with Quantized SLMs | [2604.00586](https://arxiv.org/abs/2604.00586) | 1 |

---

*Generated 2026-04-06 · Forward-Looking LLMs & Multi-Turn Dialogue research context · 42 papers reviewed*
