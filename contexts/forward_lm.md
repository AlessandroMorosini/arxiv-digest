# Forward-Looking LLMs: Multi-Turn Decision Making Under Uncertainty

## Research Focus
Building non-myopic, forward-looking dialogue agents that make better decisions in multi-turn LLM interactions by anticipating future conversation trajectories.

## Core Problems
- Current LLMs are myopic: each response is conditioned only on past turns with no explicit consideration of the future
- Multi-turn failures: premature commitment, error propagation, context pollution, over-reliance on incorrect earlier responses
- The binary Answer/Clarify action space is too narrow — agents also need Repair actions
- Underspecification and ambiguity are tightly coupled to trajectory-level failures

## Key Research Questions
- When should an LLM clarify vs. answer vs. repair? How to make this decision optimally?
- How to use trajectory simulation / lookahead to enforce better present actions?
- How to formalize the value of information for clarification decisions in multi-turn settings?
- How to handle context pollution and error propagation across turns?
- Does multi-period lookahead actually help over single-step greedy policies?

## Methods & Frameworks of Interest
- Dynamic programming / RL for multi-turn dialogue policies
- Trajectory rollout and simulation for action selection
- Value of Information (VoI) — decision-theoretic approach to clarification
- Monte Carlo Tree Search (MCTS) for deeper lookahead
- Action abstraction with typed interaction actions: a = (intent, operator, arguments)
- Intent set: {Clarify, Commit, Repair} — Clarify reduces uncertainty, Commit advances the task, Repair corrects or stabilizes interaction state
- Contrastive self-training (DPO) with clarify vs. answer trajectories
- Sharded instruction simulation for evaluating multi-turn behavior

## Related Work & Baselines
- CollabLLM (Wu et al., 2025): RL-based, 2-step lookahead, simulating user to build training data
- VoI (Dong et al., 2026): decision-theoretic, greedy, one-step value of next question
- FLARE (Wang et al., 2026): receding-horizon replanning with MCTS, fully deterministic experiment setup
- Learning to Clarify (Chen et al., 2025): action-based contrastive self-training
- Lost in Conversation / Sharded Instructions (Laban et al., 2025): multi-turn degradation, underspecification
- Uncertainty of Thought (Hu et al., 2024): simulation trees for clarifying questions

## Key Themes
- Uncertainty and calibration in LLMs as drivers of action selection
- The "repair" action as a novel contribution — recovering from context degradation
- Irreversibility of errors in reasoning-based policies
- Variance across rollout trajectories as an informative signal
- Cost/benefit analysis: repair cost depends on context quality, clarification value depends on belief entropy
