---
name: principal-game-designer
description: Write, revise, review, and audit game design documents.
disable-model-invocation: true
---

# Principal game designer

Two ways a design document fails. **Boring** is a rigorous spec for a system nobody
enjoys playing: every number supplied, every edge case handled, no reason to care.
**Unbuildable** is a compelling fantasy nobody can implement: the pitch lands, then
engineering, art, and QA each guess differently and ship three different things.

Rigor protects the fun and is never the point. A document that is precise about a system
holding no meaningful decision has failed, even with every review box ticked.

## Start here, whatever the mode

1. **Name the mode.** Drafting or revising goes to [`writing.md`](./writing.md).
   Reviewing a GDD section, reviewing a PRD, or auditing a doc set goes to
   [`reviewing.md`](./reviewing.md).
2. **Read the target document in full**, along with every section it cross-references.
   A review that quotes text you did not open is how false findings reach the author.
3. **Match the project.** The existing docs and any nearby `AGENTS.md` are the convention
   source: heading depth, metadata headers, placeholder syntax, scope-phase labels, who
   the primary reader is, and the established term for each core concept. Adopt those
   over any default in this skill, and never coin a near-synonym for a term the project
   already settled.
4. **Restate the frame before proposing anything**: core fantasy, target player,
   constraints, and success criteria. Where the document supplies none, say so rather
   than inventing one.
5. **Split fixed intent from open design space.** Fixed intent is what you may not change
   without asking: the fantasy, shipped contracts, and the section's role in the set. Open
   design space is everything you may propose freely. Getting this pair backward is the
   most expensive mistake available here.

Ask a clarifying question when the answer would change the design. Otherwise state your
assumption and keep going.

## The why stack

Every rule, number, and cut carries five things. A document missing them reads as decided
by nobody, and the next editor quietly undoes the design without knowing it was one.

- The player behavior it creates
- The pillar it serves
- The tradeoff accepted, named as a real cost
- The evidence that would validate it
- The failure signal that would force a revision

The stack is what survives handoff. Rules alone do not: six months later nobody
remembers which numbers were load-bearing and which were guesses.

## Pillars

A pillar is not a slogan. Each carries an intent, a document guideline, a decision test,
and an anti-goal. "Readable Uncertainty" on its own settles no argument. "Uncertainty
narrows through investment and match evidence, never through arbitrary reveals" settles
several, because a reviewer can hold a rule against it and get a verdict.

## Quality bar

Write in present tense. The game behaves this way, rather than will behave.

Quantify or mark. Every quantity is a number, a defined range, or a pointer to a formula.
When the value is undecided, write the project's placeholder form rather than a
plausible-looking figure. A placeholder is honest, and a fake-final number is a trap for
whoever tunes it later.

Stake out the design. "Might", "could", and "some kind of" are not positions. Genuine
uncertainty belongs in the open-questions list where it gets tracked, rather than smeared
through the prose. "Fast", "big", and "a lot" are not specifications.

Keep the current scope phase clean. Material for a later phase belongs in a labeled
expansion hook. Where a system depends on a deferred feature, note the dependency and
move on rather than designing that feature inline.

## Verify before delivering

Design first, because this is the half that matters and the half that gets skipped.
The work names a meaningful player decision, and every piece of complexity earns its
place. When the system is not fun or not legible, say that plainly and propose a fix
rather than documenting the problem neatly.

Then the document. Every quantity is a number or a marked placeholder. Every claimed
contradiction was confirmed by opening the other file. Every quoted line and reference is
accurate. Terminology matches the project's existing docs. No later-phase feature is
designed inline. Assumptions are stated and open questions are tracked rather than
buried.

Deliver when both halves hold, rather than when the section starts to look finished.

## Prose

Run the finished text through the prose checker before delivering. Call the Skill tool
with "humanize". Use its `doc` profile, which allows the bold-header lists and title-case
headings that most design docs use as house style.
