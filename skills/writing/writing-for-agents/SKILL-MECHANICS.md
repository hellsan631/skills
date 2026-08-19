# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill (frontmatter, the invocation choice, and router skills). Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Two choices, trading the two loads:

- A **model-invoked** skill keeps a `description`, so the agent can fire it autonomously, and other skills can reach it. You can still type its name: model-invocation always _includes_ user reach; a description only ever adds agent discovery, never removes the human's. The description is the skill's top-level context pointer, forced to stay loaded at all times: permanent context load in exchange for discoverability. A model-invoked skill whose content is all reference is also one home for shared reference: another skill can invoke it, so reference needed by several skills lives in one place. Mechanics: omit `disable-model-invocation`, and write a model-facing description carrying the trigger branches (the pointer-writing rules in `SKILL.md` apply in full).
- A **user-invoked** skill strips the description from the agent's reach: only the human typing its name can invoke it, and no other skill can. Zero context load, but it spends cognitive load: you are the index that must remember it exists. Mechanics: set `disable-model-invocation: true`, and write the description as triggers regardless (see below).

Pick model-invocation only when the agent must reach the skill on its own, or another skill must. If it only ever fires by hand, make it user-invoked and pay no context load.

## Descriptions are triggers, not summaries

A description that names the skill's subject ("shared vocabulary for designing deep modules") says what the skill is about and nothing about when it applies. Build it from triggers instead ("use when deciding where a seam goes, or when another skill needs the deep-module vocabulary"). Same length, and now it does work: it names the situations that should reach the skill.

Write triggers for both invocation modes. For a model-invoked skill the reason is obvious, since the branches are what fire it. For a user-invoked one the description is free, because nothing loads it until the skill runs, and it still pays twice. The human scanning a list of names is carrying the cognitive load that user-invocation just handed them, and triggers are what turn that list into an index. Then the skill fires, and its description is the first line the agent reads: naming the situation tells the agent which one it is in before a single step runs.

Write the branches as parallel `when` clauses ("use when X, when Y, or when Z"). The repetition is the point: each `when` marks a separate branch, where a bare participle ("making the code testable") blurs into the branch before it and reads as one condition with a trailing flourish.

Strip a trigger only when it renames a branch you have already listed. Length is not the constraint here; a summary that costs the same tokens and triggers nothing is the expensive option.

Shared reference that two user-invoked skills both need can live in neither: with no descriptions, neither can fire the other. Push it to a plain file outside the skill system: external reference any skill can point at.

## Splitting by invocation

The invocation cut of splitting; the sequence cut lives in `SKILL.md`. Split off a model-invoked skill when another skill must reach it, or when you have a distinct leading word that should trigger it on its own: a trigger word you actually use in your prompts. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**. One user-invoked skill names the others and when to reach for each, so the human has one skill to remember instead of many. It can only hint, never fire them: user-invoked skills have no description, so nothing but the human can reach them.
