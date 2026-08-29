---
name: domain-modeling
description: Use when codebase terminology is in dispute, when writing or editing a CONTEXT.md, or when recording an ADR. Builds and sharpens the project's domain model as terms settle.
disable-model-invocation: true
---

# Domain modeling

Build and sharpen the project's domain model while you design. Challenge terms, invent edge-case scenarios, and record glossary entries and decisions as soon as they settle. This skill applies when changing the model. Reading `CONTEXT.md` to reuse its vocabulary is a separate one-line habit that any skill can follow.

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create each file only when you have something to write. If the repository has no `CONTEXT.md`, create one when you resolve the first term. If it has no `docs/adr/`, create that directory when you need the first ADR.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen vague language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When discussing domain relationships, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-check the code

When the user states how something works, check whether the code agrees. If you find a contradiction, point it out: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update CONTEXT.md inline

Update `CONTEXT.md` as soon as you resolve a term. Capture each term as it settles instead of batching updates. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` contains no implementation details. It is a glossary. Do not use it as a spec, a scratch pad, or a repository for implementation decisions.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse.** Changing the decision later has a meaningful cost.
2. **Surprising without context.** A future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off.** There were genuine alternatives, and you picked one for specific reasons.

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
