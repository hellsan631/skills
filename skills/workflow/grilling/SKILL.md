---
name: grilling
description: Use when a plan, decision, or idea needs stress-testing, or when the user asks you to grill them. Challenges its assumptions and decisions to expose their weak points.
disable-model-invocation: true
---

Keep questioning the user until you reach a shared understanding. Map the interview as a `design tree`, with every decision branching into the decisions that depend on it.

Work through the tree in `rounds`. The `frontier` contains every decision with settled prerequisites. Ask the whole frontier in one round, numbering each question and giving your recommended answer. Then wait for the user's answers before the next round.

Use this format for every question:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

After the user answers a round, recompute the frontier and ask the next round. Defer any question whose answer depends on another question that remains open in the current round.

You are responsible for finding facts. When a frontier question needs a fact from the environment, including the filesystem or tools, dispatch a sub-agent to find it. Ask the user only for decisions. Continue the interview while the exploration runs. Treat the running exploration as an unsettled prerequisite: delay only its downstream questions and ask the rest of the frontier now. Put each decision to the user and wait for their answer.

The session ends when the frontier is empty, you have visited every branch of the design tree, and no assumption remains unspoken. Wait for the user to confirm the shared understanding before acting on it.
