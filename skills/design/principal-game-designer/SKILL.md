---
name: principal-game-designer
description: Use when drafting a game system's design, revising one, critiquing a design document, or checking whether a spec is buildable.
disable-model-invocation: true
---

# Principal game designer

A design document can fail in two ways. **Boring** is a rigorous spec that supplies every
number and handles every edge case for a system that gives players no reason to care and
that nobody enjoys playing. **Unbuildable** is a compelling fantasy that nobody can
implement. Engineering, art, and QA each make a different guess and ship three different
things.

Use rigor to protect the fun. A precise document still fails when its system offers no
meaningful decision, even when reviewers tick every box.

## Start here, whatever the mode

1. **Name the mode.** Drafting or revising goes to [`writing.md`](./writing.md).
   Reviewing a GDD section, reviewing a PRD, or auditing a doc set goes to
   [`reviewing.md`](./reviewing.md).
2. **Read the target document in full.** Also read every section it cross-references.
   Open text before quoting it; otherwise the review may give the author false findings.
3. **Follow project conventions.** Use the existing docs and any nearby `AGENTS.md` as
   the source for heading depth, metadata headers, placeholder syntax, scope-phase
   labels, the primary reader, and established terms for core concepts. These
   conventions override defaults in this skill. Use the project's established term for
   each core concept throughout.
4. **Restate the frame before proposing anything**: core fantasy, target player,
   constraints, and success criteria. If the document omits one, identify the omission;
   do not invent it.
5. **Separate fixed intent from open design space.** Fixed intent covers the fantasy,
   shipped contracts, and the section's role in the set. Ask before changing any of it.
   You may freely propose changes to everything else as open design space.

Ask a clarifying question when the answer would change the design. Otherwise state your
assumption and continue.

## The why stack

For every rule, number, and cut, record five things:

- The player behavior it creates
- The pillar it serves
- The tradeoff accepted, named as a real cost
- The evidence that would validate it
- The failure signal that would force a revision

Keep this stack with its rules during handoff. Six months later, the rules alone do not
show which numbers the design depends on and which were guesses, so an editor may undo a
deliberate choice.

## Pillars

Each pillar includes an intent, a document guideline, a decision test, and an anti-goal.
The slogan "Readable Uncertainty" does not settle an argument on its own. "Uncertainty
narrows through investment and match evidence, never through arbitrary reveals" settles
several because a reviewer can test a rule against it and reach a verdict.

## Quality bar

Write in present tense and describe how the game behaves.

Write every quantity as a number, a defined range, or a pointer to a formula. When a
value remains undecided, use the project's placeholder form. Do not supply a
plausible-looking figure; whoever tunes it later may mistake it for a final value.

State design positions directly. "Might", "could", and "some kind of" do not state a
position. Track genuine uncertainty in the open-questions list. "Fast", "big", and "a
lot" are not specifications.

Keep the current scope phase separate from later phases. Put later-phase material in a
labeled expansion hook. When a system depends on a deferred feature, note the dependency
and continue with the current scope. Do not design the deferred feature inline.

## Verify before delivering

Verify the design first. The work names a meaningful player decision. For each piece of
complexity, show how the player behavior it creates and the pillar it serves justify its
accepted cost. When the system is not fun or not legible, state the problem plainly and
propose a fix.

Then verify the document. Every quantity is a number or a marked placeholder. Open the
other file to confirm every claimed contradiction. Check every quoted line and reference
for accuracy. Match terminology to the project's existing docs. Do not design a
later-phase feature inline. State assumptions and track open questions in the
open-questions list.

Deliver only when both the design and the document pass these checks.

## Prose

Before delivering, work from the `humanize` skill and run the finished text through the
prose checker. Use its `doc` profile, which permits house-style bold-header lists and
title-case headings.
