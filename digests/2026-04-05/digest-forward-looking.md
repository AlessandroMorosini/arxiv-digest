# arXiv Digest — 2026-04-05

**Research focus:** Forward-Looking LLMs & Multi-Turn Dialogue
**Categories:** cs.AI · cs.CL · cs.LG · stat.ML
**Lookback:** 3 days (Sunday schedule — covers April 2–4)
**Papers reviewed:** 15 | **Top Picks:** 4 | **Worth a Look:** 7 | **Quick Scan:** 4

> Note: arXiv API unavailable (proxy block). Papers sourced via web search covering recent
> submissions (late March – April 2026). Papers from the 2026-04-03 digest (same research focus)
> are not repeated; one retroactive find from March 2025 (2503.22674) is included as it was
> absent from all prior digests.

---

## Top Picks (score ≥ 8)

---

### [Decision-Centric Design for LLM Systems](https://arxiv.org/abs/2604.00414)
**Authors:** Wei Sun (IBM Research)
**Score: 10/10**

**One-line summary:** Proposes an explicit *decision layer* that separates decision-relevant signals from the policy that maps them to actions — covering whether/when to answer, clarify, retrieve, repair, or escalate.

**Key contribution:** Rather than leaving control decisions (clarify vs. commit, repair vs. continue) implicit inside generation, the paper separates: (1) *signal estimation* — confidence, uncertainty, task completeness; (2) *decision policy* — mapping signals to typed actions; (3) *execution* — generating the response. This three-part decomposition enables modular failure attribution and targeted improvement. It unifies single-step settings (routing, adaptive inference) and extends naturally to sequential, multi-turn settings where each action alters the information available before the next.

**Why it matters for this research:** This paper is the closest published work to the action abstraction framework the research proposes. The explicit enumeration of control actions — answer, clarify, retrieve, repair, escalate — directly instantiates the `{Clarify, Commit, Repair}` intent set. The sequential extension (where actions alter future information) is precisely the path-dependence structure motivating forward-looking planning. The separation of signal, policy, and execution is exactly what makes the decision layer interpretable and compatible with DP/OR formulations.

---

### [Leveraging the Value of Information in POMDP Planning](https://arxiv.org/abs/2604.01434)
**Authors:** Zakariya Laouar, Qi Heng Ho, Zachary Sunberg
**Score: 9/10**

**One-line summary:** Introduces VOIMCP — a DP framework + MCTS algorithm that allocates planning effort based on the Value of Information at each belief state, with theoretical near-optimality guarantees.

**Key contribution:** Observes that in many POMDPs the VOI — expected performance gain from reasoning about observations — varies over the belief space. Introduces a DP framework that *conditionally processes* observations only where VOI is non-negligible, reducing the curse of dimensionality and history. Builds VOIMCP (Value of Information Monte Carlo Planning), which proves convergence bounds and outperforms baselines on standard POMDP benchmarks.

**Why it matters for this research:** This is the cleanest recent instantiation of the VoI formulation (cf. Dong et al. 2026) in a rigorous planning framework. The belief-conditioned VOI calculation maps directly onto the clarification decision: ask a question only when the expected information gain exceeds its cost. VOIMCP's theoretical guarantees provide a principled baseline for formal analysis of the Clarify action. The MCTS variant also connects to trajectory simulation / rollout-based value estimation.

---

### [Adaptive Stopping for Multi-Turn LLM Reasoning](https://arxiv.org/abs/2604.01413)
**Authors:** Xiaofan Zhou, Huy Nguyen, Bo Yu, Chenxi Liu, Lu Cheng (University of Illinois Chicago / University of Utah)
**Score: 9/10**

**One-line summary:** MiCP — the first conformal prediction framework for multi-turn LLM reasoning — allocates error budgets across turns and provides formal stopping guarantees while reducing turn count and cost.

**Key contribution:** Existing multi-turn reasoning (adaptive RAG, ReAct agents) uses heuristic stopping rules that provide no guarantee the answer remains valid. MiCP applies conformal prediction across turns: it allocates different error budgets per turn, allowing early stopping while maintaining a user-specified coverage guarantee over final predictions. Evaluated on single-hop and multi-hop QA benchmarks; reduces turns and inference cost without sacrificing correctness bounds.

**Why it matters for this research:** MiCP directly formalizes the optimal stopping problem for multi-turn LLM interactions. The per-turn error budget allocation is analogous to the dynamic programming state that tracks how much uncertainty remains before commitment is safe. The conformal guarantee provides what pure RL-based approaches lack: a provable relationship between stopping time and answer quality. This is the formal machinery the research needs to move from "good heuristics" to "theoretically grounded Commit decisions."

---

### [Beyond the Assistant Turn: User Turn Generation as a Probe of Interaction Awareness in Language Models](https://arxiv.org/abs/2604.02315)
**Authors:** Sarath Shekkizhar, Romain Cosentino, Adam Earle
**Score: 8/10**

**One-line summary:** Proposes generating the *next user turn* (not the assistant response) as a probe of whether a model's weights encode awareness of what follows its own outputs — finding this is decoupled from task accuracy across 7B–397B models.

**Key contribution:** Standard benchmarks only score the assistant turn; this leaves unmeasured whether the model anticipates conversational consequences of its response. The paper formalizes *user-turn generation* as a probe: given (user query, assistant response), generate the follow-up user turn. Models with genuine interaction awareness should produce grounded, reactive follow-ups. Experiments across models (7B–397B parameters) show interaction awareness is orthogonal to task accuracy — large, capable models can be unaware, small models occasionally aware.

**Why it matters for this research:** This is a direct empirical test of the forward-looking capability the research aims to cultivate. The dissociation between task accuracy and interaction awareness is a key finding: it implies that standard capability scaling does not solve forward-looking dialogue, motivating explicit training for the property. The user-turn generation probe is also a lightweight evaluation method that could assess whether a trained forward-looking model actually anticipates the user's likely follow-up.

---

## Worth a Look (score 5–7)

| # | Paper | Score | One-line summary |
|---|-------|-------|-----------------|
| 1 | [Developing Adaptive Context Compression Techniques for LLMs in Long-Running Interactions](https://arxiv.org/abs/2603.29193) — Fofadiya & Tiwari (Mar 31, 2026) | **7** | Importance-aware memory selection + coherence-sensitive filtering + dynamic budget allocation; evaluated on LOCOMO and LongBench; reduces token usage while preserving conversational stability. Directly relevant to the Repair action and managing polluted multi-turn context. |
| 2 | [Answering the Wrong Question: Reasoning Trace Inversion for Abstention in LLMs](https://arxiv.org/abs/2604.02230) — Gourabathina et al. | **7** | Trace Inversion: generate reasoning trace → reconstruct implicit query → compare to original → abstain if low similarity. SOTA on 9 datasets across 4 frontier models. Operationalizes answer faithfulness as consistency between stated question and actual reasoning. |
| 3 | [Do Language Models Know When They'll Refuse? Probing Introspective Awareness of Safety Boundaries](https://arxiv.org/abs/2604.00228) — Tanay Gondil (Purdue) | **7** | SDT-based study across Claude 4/4.5, GPT-5.2, Llama 405B: models have high introspective sensitivity (d′ ≈ 2.4–3.5) for predicting their own behavior, but sensitivity drops sharply at safety-relevant boundaries. Empirical baseline for meta-level self-awareness in confidence-driven dialogue decisions. |
| 4 | [QuestBench: Can LLMs ask the right question to acquire information in reasoning tasks?](https://arxiv.org/abs/2503.22674) — Belinda Z. Li, Been Kim, Zi Wang (DeepMind, Mar 2025) | **7** | Formalizes underspecified reasoning as a CSP with one missing variable; 4 tracks (Logic-Q, Planning-Q, GSM-Q, GSME-Q); models achieve only 40–50% on hard tracks even when fully capable of solving the complete problem. Demonstrates that task competence ≠ clarification competence. |
| 5 | [Towards Reliable Truth-Aligned Uncertainty Estimation in Large Language Models (TAC)](https://arxiv.org/abs/2604.00445) | **6** | Post-hoc calibration (Truth AnChoring) maps raw UE scores to truth-aligned scores; works under noisy, few-shot supervision; addresses proxy failure in standard UE metrics. Relevant to building confidence signals that drive the Clarify/Commit decision. |
| 6 | [Reasoning Shift: How Context Silently Shortens LLM Reasoning](https://arxiv.org/abs/2604.01161) | **6** | Irrelevant context + multi-turn embedding cause reasoning models to produce up to 50% shorter traces for the same problem, specifically losing self-verification steps. Illustrates error propagation via context pollution across turns — a core motivation for the Repair action. |
| 7 | [YCBench: Benchmarking AI Agents for Long-Term Planning and Consistent Execution](https://arxiv.org/abs/2604.01212) | **5** | Multi-turn startup simulation spanning hundreds of turns in a partially observable environment; adversarial clients + growing payroll create compounding consequences for early errors. Useful as an evaluation harness for path-dependent, error-propagating multi-turn scenarios. |

---

## Quick Scan (score < 5)

| Title | arXiv ID | Score |
|-------|----------|-------|
| Agent Psychometrics: Task-Level Performance Prediction in Agentic Coding Benchmarks | [2604.00594](https://arxiv.org/abs/2604.00594) | 4 |
| Open-loop POMDP Simplification and Safe Skipping of Replanning with Formal Guarantees | [2604.01352](https://arxiv.org/abs/2604.01352) | 3 |
| Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs | [2604.00824](https://arxiv.org/abs/2604.00824) | 2 |
| Competition and Cooperation of LLM Agents in Games | [2604.00487](https://arxiv.org/abs/2604.00487) | 2 |

---

## Digest Notes

**This week's standout cluster — the decision layer is crystallizing:**

Three independent papers (2604.00414, 2604.01413, 2604.01434) converge on the same architectural insight from different directions: the act-or-clarify-or-repair decision should be *explicit, separable, and formally grounded*. Sun (2604.00414) makes this argument at the systems design level; Zhou et al. (2604.01413) implement it via conformal stopping theory; Laouar et al. (2604.01434) ground it in POMDP VoI. Together they sketch the full stack: (1) formal decision objective, (2) algorithmic realization, (3) system integration.

**The interaction awareness gap (2604.02315):**

Shekkizhar et al.'s finding that interaction awareness is orthogonal to task capability — large capable models can be "interaction-blind" — is the clearest empirical justification yet for making forward-looking training a *distinct* objective, not an emergent property of scale. The user-turn generation probe is a cheap, off-the-shelf evaluation that should be added to any forward-looking training loop.

**Still missing:**

No paper this week treats the *Repair* action with the same formal rigor as Clarify/Commit. The context compression work (2603.29193) handles repair *implicitly* via memory management, but no paper yet models Repair as an explicit planned action with a value function. This remains the gap.
