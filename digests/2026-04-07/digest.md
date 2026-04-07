# arXiv Digest — 2026-04-07

**Research focus:** Forward-Looking LLMs & Multi-Turn Dialogue
**Context:** `contexts/forward_lm.md`
**Categories:** cs.AI · cs.CL · cs.LG · stat.ML
**Papers reviewed:** 15 | **Top Picks:** 5 | **Worth a Look:** 5 | **Quick Scan:** 5

> **Note:** arXiv API access blocked (proxy 403). Papers gathered via web search, covering
> recent submissions not yet included in any prior digest (Apr 3–7, 2026 + retroactive
> high-relevance finds from Jan–March 2026). All IDs verified.

---

## Top Picks (score ≥ 8)

---

### [AT²PO: Agentic Turn-based Policy Optimization via Tree Search](https://arxiv.org/abs/2601.04767)
**Authors:** Zefang Zong, Dingwei Chen, Yang Li, Qi Yi, Bo Zhou, Chengming Li, Bo Qian, Peng Chen, Jie Jiang
**Score: 9/10** | arXiv:2601.04767 | cs.AI/cs.CL | Jan 2026

**One-line summary:** Unified multi-turn RL framework that builds a turn-level tree structure for entropy-guided exploration and turn-wise credit assignment, with a dedicated turn-granularity policy objective.

**Key contribution:** AT²PO identifies three failure modes of existing multi-turn RL — limited exploration diversity, sparse credit assignment, and misaligned policy objectives — and addresses all three jointly. The tree is grown at turns where the agent is uncertain (high entropy), enabling targeted exploration of the most ambiguous decision points. Credit is propagated turn-by-turn rather than episode-level, and the policy objective is aligned to the natural granularity of agentic decision making. Consistent +1.84pp improvements across seven benchmarks.

**Why it matters for this research:** AT²PO directly instantiates forward-looking multi-turn planning via tree expansion at decision points. Entropy-guided expansion is a computationally tractable approximation of the VoI-based branching the research proposes: the agent builds the tree where it is most uncertain, which is precisely where clarification vs. commit decisions have the highest expected value. The turn-wise credit assignment solves the core training signal problem for DP-style multi-turn optimization.

---

### [Agentic Uncertainty Quantification](https://arxiv.org/abs/2601.15703)
**Authors:** Jiaxin Zhang, Prafulla Kumar Choubey, Shubham Toshniwal, Caiming Xiong, Chien-Sheng Wu
**Score: 9/10** | arXiv:2601.15703 | cs.AI/cs.CL/cs.LG | Jan 2026

**One-line summary:** Dual-process UQ framework (System 1: Uncertainty-Aware Memory; System 2: Uncertainty-Aware Reflection) transforms verbalized confidence into active, bidirectional control signals that prevent hallucination spirals.

**Key contribution:** The "Spiral of Hallucination" — the research equivalent of error propagation across multi-turn context — is addressed by a two-component system: UAM (System 1) implicitly propagates verbalized confidence and explanations in context so later decisions don't proceed blind; UAR (System 2) triggers targeted inference-time self-correction *only when uncertainty exceeds a threshold*, avoiding aimless continuous revision. This asymmetry (passive memory + triggered reflection) is exactly the kind of economical uncertainty management the research calls for. Training-free; strong empirical results on closed-loop and open-ended benchmarks.

**Why it matters for this research:** This is the most direct existing implementation of uncertainty-as-action-trigger for the Repair action. UAR's threshold-triggered correction is a concrete mechanism for deciding when the context has degraded enough to warrant a Repair vs. proceeding with Commit. UAM's propagation of confidence explanations in context operationalizes the "uncertainty state" the research wants to track across dialogue turns. The Spiral of Hallucination framing is the multi-turn version of context pollution — same problem, same solution architecture.

---

### [Are LLM Decisions Faithful to Verbal Confidence?](https://arxiv.org/abs/2601.07767)
**Authors:** Ori Shapira, Ori Ernst, Ran Levy, Ido Dagan
**Score: 9/10** | arXiv:2601.07767 | cs.CL/cs.AI | Jan 2026

**One-line summary:** LLMs accurately verbalize uncertainty but systematically fail to use it to guide decisions — a fundamental disconnect between stated confidence and actual behavioral choices.

**Key contribution:** Controlled experiments show that models which correctly detect speaker unreliability in explicit confidence ratings then *fail* to adjust their clarification behavior accordingly — they exhibit "partner-blind over-clarification" (asking even when confident the interlocutor is reliable) and "question-averse guessing" (committing even when uncertain). The gap is not a calibration failure (the verbalized uncertainty is accurate) but a faithfulness failure: information is generated but not consumed by the decision layer.

**Why it matters for this research:** This result defines the precise architectural problem the research needs to solve. A forward-looking dialogue policy that reads verbalized confidence and routes to Clarify/Commit/Repair cannot rely on the LLM's natural generation behavior — the decision layer must be explicitly decoupled. This is strong empirical justification for the research's "explicit decision layer" design choice and against end-to-end generation of both uncertainty and action in a single pass.

---

### [RACER: Risk-Aware Calibrated Efficient Routing for Large Language Models](https://arxiv.org/abs/2603.06616)
**Authors:** Ming-Hua Tsai, Phat Tran (Oregon State University)
**Score: 8/10** | arXiv:2603.06616 | cs.LG/cs.AI | Mar 2026

**One-line summary:** Distribution-free, post-hoc LLM routing via the α-VOR problem — select the smallest set of models with provable misrouting risk control, supporting variable set sizes and abstention.

**Key contribution:** Reformulates routing as *set selection* under a risk constraint: RACER returns a set of models (not a single choice) such that the probability of misrouting is bounded at level α, with formal finite-sample guarantees. The nested model set construction via augmented scoring and concentration-bound calibration works post-hoc on any base router. Supports abstention (returning empty set when no model meets the risk threshold). Distribution-free — no assumption on query or response distribution.

**Why it matters for this research:** RACER's abstention mechanism is the routing analogue of the Clarify action: when confidence falls below threshold, don't commit to a model (or an answer) — defer. The distribution-free risk control provides formal grounding for the routing confidence thresholds the research uses to trigger Clarify vs. Commit. The α-VOR formulation connects to the decision-theoretic framing of VoI: the cost of asking is bounded by the risk of misrouting.

---

### [Conversation Tree Architecture: A Structured Framework for Context-Aware Multi-Branch LLM Conversations](https://arxiv.org/abs/2603.21278)
**Authors:** Pranav Hemanth, Sampriti Saha
**Score: 8/10** | arXiv:2603.21278 | cs.CL/cs.AI | Mar 2026

**One-line summary:** Organizes multi-turn LLM conversations as trees of context-isolated nodes to prevent "logical context poisoning" — the progressive corruption of conversational coherence from accumulated off-topic context.

**Key contribution:** Identifies "logical context poisoning" as a structural failure mode distinct from model error: topically distinct conversation threads accumulate in a single window, degrading coherence even when the model is performing correctly. The Conversation Tree Architecture (CTA) uses hierarchical, context-isolated nodes where structured mechanisms govern parent-child context flow. Volatile nodes allow transient branches to be selectively merged upstream or discarded. This is a *structural* solution to context repair — not post-hoc cleanup, but architectural prevention.

**Why it matters for this research:** CTA directly addresses the context pollution problem the research identifies as a core failure mode. The volatile node mechanism is a concrete implementation of the Repair action's "context reset" semantics — the ability to branch, explore, and then merge or discard. The structured context flow rules provide a formal basis for modelling when the interaction state has degraded enough to require repair. CTA's "logical context poisoning" label is a contribution to the failure-mode taxonomy the research is developing.

---

## Worth a Look (score 5–7)

| # | Paper | Score | One-line summary |
|---|-------|-------|-----------------|
| 1 | [Proximity-Based Multi-Turn Optimization (ProxMO)](https://arxiv.org/abs/2602.19225) — Zhao, Lu, Li (Feb 2026) | **7** | Episode-level difficulty modulation + step-level proximity-based baselines solve multi-turn credit assignment; 1.5B/7B models match GPT-4o/Gemini-2.5-Pro on long-horizon tasks. Directly relevant to training multi-turn forward-looking policies with well-calibrated credit. |
| 2 | [ProRL Agent: Rollout-as-a-Service for RL Training of Multi-Turn LLM Agents](https://arxiv.org/abs/2603.18815) — NVIDIA NeMo Team (Mar 2026) | **7** | Decouples rollout orchestration from RL training loop via HTTP service; async INIT/RUN/EVAL assembly line; Qwen3-8B 9.6%→18.0% on SWE-bench. Infrastructure for the rollout-based trajectory simulation the research requires. |
| 3 | [Variational Routing: A Scalable Bayesian Framework for Calibrated MoE Transformers](https://arxiv.org/abs/2603.09453) — Li, Wicker (Mar 2026) | **6** | Bayesian inference over MoE routing logits (VMoER): 94% calibration error reduction, 38% noise stability improvement, <1% FLOPs overhead. Provides a principled uncertainty representation for routing decisions. |
| 4 | [Adaptive Confidence Gating in Multi-Agent Collaboration for Code Generation](https://arxiv.org/abs/2601.21469) — Ding, Kan (Jan 2026) | **6** | Confidence-based stopping criterion routes uncertain outputs to downstream agents while letting confident outputs pass; reduces cost while maintaining accuracy. Concrete implementation of confidence-gated cascading in a multi-turn agentic setting. |
| 5 | [Reward-Based Online LLM Routing via NeuralUCB](https://arxiv.org/abs/2603.30035) — Tsai, Tran (Mar 2026) | **6** | Contextual bandit (NeuralUCB) learns non-linear routing policy online, improving utility/cost trade-off over time. Online learning framing of routing decisions — relevant to adaptive clarification thresholds that improve through conversation. |

---

## Quick Scan (score < 5)

| Title | arXiv ID | Score | Note |
|-------|----------|-------|------|
| [Beyond the Context Window: Memory vs. Long-Context for Persistent Agents](https://arxiv.org/abs/2603.04814) | 2603.04814 | 5 | Fact-based memory (Mem0) vs. long-context LLMs on LongMemEval/LoCoMo/PersonaMemv2; memory wins on multi-session. Relevant to repair via memory restructuring. |
| [Analysis of Optimality of LLMs on Planning Problems](https://arxiv.org/abs/2604.02910) | 2604.02910 | 5 | Frontier LLMs track theoretical optimality in Blocksworld/P* with ~47 tokens/step; evidence for serial algorithmic simulation hypothesis. Background on LLM planning capability. |
| [Let's Have a Conversation: LLM Agents for Interactive Optimization](https://arxiv.org/abs/2604.02666) | 2604.02666 | 4 | Evaluation framework for multi-turn optimization conversations with stakeholder role-playing agents. Evaluation methodology for multi-turn goal-directed interactions. |
| [SIEVE: Sample-Efficient Parametric Learning from Natural Language](https://arxiv.org/abs/2604.02339) | 2604.02339 | 4 | Iterative hypothesis generation from NL feedback; relevant to learning structured representations from underspecified instructions. |
| [Speaker-Reasoner: Multi-turn Reasoning for Speaker-Attributed ASR](https://arxiv.org/abs/2604.03074) | 2604.03074 | 3 | Multi-turn iterative reasoning for ASR with speaker attribution; not relevant to dialogue planning. |

---

## Digest Notes

**This week's focus: the confidence-action gap and structural repair**

Three papers this cycle converge on a single uncomfortable finding: LLMs are good at generating uncertainty estimates but bad at acting on them. Shapira et al. (2601.07767) provide the clearest empirical demonstration — the disconnect is not a calibration problem but a *faithfulness* problem. This has a direct architectural implication: the decision layer (Clarify/Commit/Repair) cannot be implicitly folded into generation; it must be explicitly decoupled. This aligns with Sun's Decision-Centric Design (2604.00414, covered last digest) and makes the case that the research's "explicit intent operator" architecture is not just principled but *necessary*.

**AT²PO's entropy-guided tree expansion is the closest existing approximation of VoI-based rollout:**

The research proposes evaluating candidate actions via trajectory simulation before committing. AT²PO (2601.04767) implements this as entropy-guided tree expansion — the tree grows exactly where uncertainty is highest, which is where the expected gain from exploration (= value of information) is greatest. The connection is not coincidental: entropy-guided search is a computationally tractable VoI approximation that doesn't require explicit utility functions. For the research, this is the bridge between the theoretical VoI formulation and a practical RL training algorithm.

**CTA's "logical context poisoning" names a failure mode the research needs to model:**

Conversation Tree Architecture (2603.21278) introduces precise terminology for the context pollution the research describes informally. The structural solution (context-isolated nodes with explicit merge/discard semantics) is essentially an architectural Repair action — the ability to scope, branch, and selectively propagate context. The volatile node mechanism deserves attention as a model for the Repair action's "context reset" semantics.
