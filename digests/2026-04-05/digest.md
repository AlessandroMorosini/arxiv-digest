# arXiv Digest — 2026-04-05

**Research context:** Self-Consistency in Language Models (Pres, Li, Ruis et al., MIT CSAIL & Goodfire)
**Coverage:** April 1–5, 2026 (Sunday lookback: 3 days) + recent high-signal 2026 papers
**Papers reviewed:** 18 | **Top Picks:** 7 | **Worth a Look:** 8 | **Quick Scan:** 3

> Note: arXiv API was unavailable (proxy 403); papers sourced via semantic web search across cs.CL / cs.AI / cs.LG / stat.ML. Coverage of April 2026 (2604.XXXXX) papers is confirmed; earlier papers included where highly relevant.

---

## Top Picks (Score ≥ 8)

---

### [Do Language Models Know When They'll Refuse? Probing Introspective Awareness of Safety Boundaries](https://arxiv.org/abs/2604.00228) — 9/10

**Authors:** Anonymous | **Category:** cs.CL | **Published:** 2026-04-01

*One-line summary:* Models predict their own refusal behavior across 3,754 test cases, achieving 88–96% accuracy — but introspective sensitivity degrades precisely at safety boundary cases.

**Key contribution:** Operationalizes meta-level self-consistency as a measurable quantity using Signal Detection Theory (d' = 2.4–3.5). Introduces a "predict then respond" protocol that directly separates self-description from behavior, revealing that all four frontier models (Claude Sonnet 4, Sonnet 4.5, GPT-5.2, Llama 3.1 405B) have partially faithful self-models of their safety behavior.

**Why it matters for this research:** This is nearly a direct empirical instantiation of the paper's *self-descriptive objectives* — testing whether φ(meta-response, instance-behavior) = 1, i.e., whether the model's description of "I will refuse X" matches the actual refusal. The degradation at safety boundaries is the exact failure mode the framework predicts for meta-level inconsistency. ECE scores across models (ECE=0.017 for Sonnet 4.5 vs 0.216 for Llama) provide a calibration baseline for meta-level self-description fidelity.

---

### [A Positive Case for Faithfulness: LLM Self-Explanations Help Predict Model Behavior](https://arxiv.org/abs/2602.02639) — 9/10

**Authors:** Anonymous | **Category:** cs.CL | **Published:** 2026-02-04

*One-line summary:* LLM self-explanations yield 11–37% gain in predicting model behavior on related inputs via the Normalized Simulatability Gain (NSG) metric.

**Key contribution:** Proposes NSG as a metric for explanation faithfulness grounded in *predictive power on related inputs* — an observer using the self-explanation to predict behavior on unseen but related inputs gains 11–37% over a baseline that uses no explanation. This is a formal behavioral test of whether self-descriptions carry genuine information about the model's decision procedure.

**Why it matters for this research:** NSG operationalizes the link between meta-responses and instance-level behavior central to the self-consistency framework. Rather than treating explanations as faithful or not in isolation, NSG measures whether φ(explanation, behavior_on_related_inputs) > 0 — directly quantifying meta-level consistency across the family of related inputs. This is a clean empirical handle on the *self-alignment* direction: if self-explanations predict behavior, they can be used as soft constraints.

---

### [Towards Reliable Truth-Aligned Uncertainty Estimation in Large Language Models](https://arxiv.org/abs/2604.00445) — 8/10

**Authors:** Anonymous | **Category:** cs.CL | **Published:** 2026-04-01

*One-line summary:* Formalizes "proxy failure" in uncertainty estimation and proposes Truth AnChoring (TAC) — a post-hoc calibration method that maps raw UE scores to truth-aligned scores.

**Key contribution:** Identifies that standard UE metrics are not grounded in factual correctness but in model behavior, making them non-discriminative in low-information regimes. TAC provides few-shot, post-hoc recalibration to truth-aligned scores, improving hallucination detection even with noisy supervision.

**Why it matters for this research:** Calibration as a consistency problem: a well-calibrated model's confidence verbalization should be invariant to how a question is posed while equivariantly tracking the underlying probability of correctness. TAC's proxy-failure analysis connects directly to the consistency framework's treatment of calibration — the model's confidence outputs should satisfy φ(conf(x₁), conf(x₂)) when x₁ and x₂ are paraphrases of the same question. The few-shot recalibration approach could be adapted as a *posterior regularization* technique.

---

### [When Agents Disagree With Themselves: Measuring Behavioral Consistency in LLM-Based Agents](https://arxiv.org/abs/2602.11619) — 8/10

**Authors:** Anonymous | **Category:** cs.AI | **Published:** 2026-02-17

*One-line summary:* ReAct-style agents produce 2.0–4.2 distinct action sequences per 10 identical runs on HotpotQA; consistency gap of 32–55 pp separates high vs low consistency tasks.

**Key contribution:** Large-scale empirical measurement (3,000 runs) of within-model behavioral consistency, showing consistency is strongly predictive of task accuracy, with 69% of divergence originating at step 2. Provides a decomposition of consistency by task type and model.

**Why it matters for this research:** This paper provides direct empirical grounding for the formal consistency function φ applied to agent trajectories. The finding that early-step divergence cascades into full trajectory inconsistency is relevant to how consistency constraints should be enforced (at the step level, not just output level). The 32–55 pp accuracy gap quantifies the practical value of optimizing for self-consistency, and the per-task decomposition could guide which types of agent tasks benefit most from consistency regularization.

---

### [Breaking the Reversal Curse in Autoregressive Language Models via Identity Bridge](https://arxiv.org/abs/2602.02470) — 8/10

**Authors:** Anonymous | **Category:** cs.CL | **Published:** 2026-02-04

*One-line summary:* A simple training data recipe (Identity Bridge) fixes the Reversal Curse — LLMs trained on "A is B" failing to infer "B is A" — enabling bidirectional factual generalization.

**Key contribution:** Introduces a data augmentation technique (Identity Bridge) consisting of intermediate identity-based training examples that connect forward and backward directions of factual statements, reliably enabling bidirectional generalization without architecture changes.

**Why it matters for this research:** The Reversal Curse is a canonical example of *equivariance failure* — the model's knowledge of "Alice's husband is Bob" should equivariantly produce knowledge of "Bob's wife is Alice", but doesn't. The Identity Bridge directly addresses this as a training-data consistency problem. For the self-consistency framework, this is a case study in using consistency constraints as a training signal: if φ("A is B", "B is A") = 1 is the desired equivariance, the Identity Bridge provides a practical method to enforce it. The recipe's simplicity makes it a strong template for other equivariance objectives.

---

### [Emergent Introspective Awareness in Large Language Models](https://arxiv.org/abs/2601.01828) — 8/10

**Authors:** Anonymous | **Category:** cs.CL | **Published:** 2026-01-03

*One-line summary:* Using interpretability + behavioral probing, the paper identifies emergent degrees of introspective fidelity that scale with model size and instruction-tuning intensity.

**Key contribution:** Provides a methodology for distinguishing genuine introspection from confabulation by combining internal representation probing (mechanistic) with behavioral consistency tests (observational). Shows that introspective fidelity is graded, not binary, and correlates with alignment training quality.

**Why it matters for this research:** This directly informs the *meta-level self-consistency* program. The graded fidelity finding suggests that self-descriptive objectives should be parameterized by confidence and uncertainty, not treated as binary constraints. The interpretability approach (probing internal representations) provides a complement to purely behavioral consistency tests — for the self-consistency framework, this suggests hybrid objectives that enforce φ(internal_state, self_description) in addition to φ(self_description, behavior).

---

### [Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay](https://arxiv.org/abs/2601.10589) — 8/10

**Authors:** Anonymous | **Category:** cs.CL | **Published:** 2026-01-14

*One-line summary:* Safety Self-Play (SSP) lets a single LLM act as both Attacker and Defender in a unified RL loop, discovering and patching its own safety vulnerabilities.

**Key contribution:** First application of self-play to LLM safety alignment. Introduces Reflective Experience Replay, which explicitly revisits low-reward historical trajectories, enabling systematic improvement over previously discovered vulnerabilities. The unified Attacker-Defender loop is fully automated, requiring no external red-teaming.

**Why it matters for this research:** This is a direct instantiation of *automated self-red-teaming* — one of the paper's explicit case studies. SSP operationalizes the consistency objective φ(response_to_attack, response_to_benign_variant) as a self-supervised signal: the Defender should be consistent whether or not adversarial framing is present. The RL loop over self-generated consistency violations is also a concrete implementation of the soft-constraint optimization approach described in the framework.

---

## Worth a Look (Score 5–7)

- **[Reasoning Shift: How Context Silently Shortens LLM Reasoning](https://arxiv.org/abs/2604.01161)** (7/10) — Reasoning models produce reasoning traces up to 50% shorter for identical problems when embedded in different contexts, suppressing self-verification. A clean equivariance failure: trace length/depth shouldn't change with irrelevant surrounding context. *cs.CL*

- **[Consistency Amplifies: How Behavioral Variance Shapes Agent Accuracy](https://arxiv.org/abs/2603.25764)** (7/10) — Across 50 SWE-bench runs per model, behavioral variance is strongly predictive of accuracy (Claude: CV 15.2%, 58% acc; Llama: CV 47%, 4% acc). Key finding: consistency amplifies outcomes — consistent errors are as harmful as consistent successes. *cs.AI*

- **[Evaluating Robustness of LLMs in Enterprise Applications: Perturbation Consistency Across Formats and Languages](https://arxiv.org/abs/2601.06341)** (7/10) — Comprehensive benchmark of invariance failures across 11 models under 4 perturbation classes (text edits, formatting, cross-lingual, positional). Minor perturbations reduce performance up to 40 pp. Directly measures φ-invariance for practical LLM deployment. *cs.CL*

- **[Optimizing Language Models for Crosslingual Knowledge Consistency](https://arxiv.org/abs/2603.04678)** (6/10) — Proposes training objectives enforcing equivariant knowledge representation across languages, so factual claims are consistent regardless of query language. A concrete equivariance-under-transformation study. *cs.CL*

- **[Self-Improving Code Generation via Semantic Entropy and Behavioral Consensus](https://arxiv.org/abs/2603.29292)** (6/10) — Uses behavioral consensus across multiple samples as a self-improvement signal, filtering unreliable outputs by cross-sample consistency. Applies self-consistency as an optimization target in code generation. *cs.CL*

- **[Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666)** (6/10) — Proposes 12 metrics decomposing agent reliability into consistency, robustness, predictability, safety dimensions. Uses 5 semantically equivalent paraphrases per task as a consistency probe. *cs.AI*

- **[ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions](https://arxiv.org/abs/2601.06112)** (6/10) — Benchmark unifying consistency, robustness, and fault tolerance metrics using Action Metamorphic Relations (synonym substitution, distractor injection, paraphrasing). *cs.AI*

- **[Aletheia: Quantifying Cognitive Conviction in Reasoning Models via Regularized Inverse Confusion Matrix](https://arxiv.org/abs/2601.01532)** (6/10) — Quantifies how expressed confidence (de)calibrates across model families; finds confidence suppression vs escalation as distinct failure modes. Relevant to confidence verbalization consistency. *cs.CL*

---

## Quick Scan (Score < 5)

| Title | arXiv | Score |
|-------|-------|-------|
| [Think Twice Before You Write: Entropy-based Decoding for LLM Reasoning](https://arxiv.org/abs/2604.00018) | 2604.00018 | 4 |
| [Do LLMs Know What Is Private Internally? Probing Contextual Privacy Norms](https://arxiv.org/abs/2604.00209) | 2604.00209 | 3 |
| [More Human, More Efficient: Aligning Annotations with Quantized SLMs](https://arxiv.org/abs/2604.00586) | 2604.00586 | 3 |

---

## Stats

| Tier | Count |
|------|-------|
| Top Picks (≥ 8) | 7 |
| Worth a Look (5–7) | 8 |
| Quick Scan (< 5) | 3 |
| **Total** | **18** |

---

*Generated by arxiv-digest on 2026-04-05. Papers sourced via semantic web search (arXiv API unavailable). Scores reflect relevance to self-consistency as a unifying framework for LM failures (Pres, Li, Ruis et al., 2026).*
