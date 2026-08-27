---
name: writing-for-agents
description: Use when creating or editing a skill, or when modifying AGENTS.md or CLAUDE.md.
disable-model-invocation: false
---

This document applies to any agent-consumed document: skills, AGENTS.md, CLAUDE.md, or any doc referenced via one of these documents. The same levers make each document predictable because the agent follows the same process every run. See SKILL-MECHANICS.md for info on agent-facing skill documents for frontmatter, invocation choice, and router skills.

### Context Pointers

A context pointer (or just pointer) is a name that points to out-of-context material and usually encodes the condition that needs to be met to reach that material. A skill description is a pointer. A line in AGENTS.md naming a doc (that doc itself must exist) is a pointer.

### The Two Loads

Every document and every pointer spends one of two budgets on an agent: context load (the cost of material that is always loaded and visible on the agent's window), and cognitive load (the cost on the human to know which documents exist and when to reach for each). Material that's reached only through a pointer escapes context load at the price of the pointer's own line; it's loaded into context only as needed. Material with no pointer rides entirely on cognitive load.

### Information Hierarchy

A document is built from steps (ordered actions) and reference (definitions, rules, facts); steps and reference mix freely in any document, at any level. The information hierarchy is a ladder: in-file step, in-file reference, disclosed reference (reference pushed to a separate file behind a pointer). Progressive disclosure moves material down the ladder to keep the top legible; branching is the cleanest disclosure test. Co-location keeps a concept's definition, rules, and caveats together under one heading; the test is that the document reads like documentation written for the agent. Sprawl, the failure mode, is cured by the ladder: disclose reference behind pointers and split it by branch or sequence.

### Steps and Completion Criteria

Every step ends on a completion criterion, the condition that tells the agent the work is done. Clarity of the criterion prevents premature completion; the post-completion steps supply pull, and the criterion's clarity is the resistance. Defend against rush by sharpening the bound first; hide later steps only if the bound is irreducibly fuzzy and rush is observed, and only across a real context boundary. Demand drives legwork; "every modified model accounted for" forces thoroughness, and demand is not step-bound; demand can bind a body of flat reference.

### When to Split

Splitting one document into two spends one of the two loads; split only when the cut earns it.

### Leading Words

A leading word is a compact concept from the model's pretraining that anchors a region of behavior in few tokens by recruiting existing priors. A leading word anchors execution (an agent reaches for the same behavior when it hears the word) and invocation (shared language in prompts, docs, codebase links the word to the material). Refactor by finding restatements and collapsing them into a single token. Examples: "fast, deterministic, low-overhead" → tight, "a loop you believe in" → red. Negation is the failure mode: prohibition makes the forbidden behavior more available; prompt the positive target instead, and pair a prohibition with the positive target when needed.

### Voice Leak

Voice leak is the document's prose reproducing itself in the agent's output; an agent imitates the document's style, and style is the most reliably transmitted thing. Prose quality in an agent document is a functional property, not a courtesy. Write the voice you want back and verify it with a checker.

### Pruning

Keep each meaning in a single source of truth. Duplication costs maintenance, costs tokens, inflates a meaning's prominence in a memory-crunched model. The environment is a source of truth; a document that restates it is a cache, earning its load only when the lookup is expensive. Cache the unwritten convention, the reason behind a choice, the gotcha no config confesses. Leave one-file, one-command lookups to the environment. Check every line in your document for relevance to the task; stale lines become sediment. Hunt no-ops: an instruction the model already obeys by default pays load to say nothing. Test by running the document; delete the whole sentence when it fails.