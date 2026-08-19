# Writing and revising

Two modes share this file. **Write** produces new content. **Revise** improves existing
content without redirecting the design unless the user asks for a redesign.

## Write mode

Answer these before drafting, from the document or from the user. They are the intake,
and skipping them is how a spec turns into a feature list.

- What player decision does this section create, change, or explain?
- What player-facing state changes as a result?
- What does the player see before acting, during the event, and after the outcome?
- What pressure or carryover does this create for the next decision?
- What numbers, ranges, thresholds, or bands does this need?
- What is in the current scope phase, and what is explicitly deferred?
- What are the failure states, edge cases, and abuse cases?
- What would QA verify from this section?
- Which linked sections have to stay consistent with this one?

When the answers point in several directions, propose pillars and ask before drafting.
Writing the wrong document well is more expensive than one question. See
[example 1](#example-1-align-before-drafting).

Done when every intake question has an answer, each rule carries its why stack, and the
document's primary reader could act on it without inventing a design decision. Which
reader that is varies: some doc sets hand off to engineering directly, others hand off to
a product manager who writes the downstream spec. Match the bar the project set rather
than assuming the engineering one.

## Revise mode

Start by naming what stays fixed: fantasy, scope, existing contracts, and the section's
current role in the set. Then tighten vague language, fill critical gaps, and resolve
contradictions with linked sections.

Preserve the author's intent. Do not preserve ambiguity, drift, or a rule duplicated from
another section. Keep placeholders explicit rather than promoting them to final numbers
to make the section look complete.

Where the section needs structural change rather than tightening, say so before
rewriting. Where the source text supports several valid directions, present them and ask.
See [example 3](#example-3-ask-before-rewriting).

Done when the fixed intent is intact, every change traces to a stated problem, and the
diff contains no invented values.

## Templates

Adapt these. Not every field applies, and project conventions override the defaults.

### System or feature spec

```markdown
# [Feature or system name]

## Context
- Document purpose:
- Primary reader:
- Core fantasy:
- Design intent:
- Target audience:
- Constraints:
- Success criteria:
- Fixed intent:
- Open design space:
- Assumptions:

## Design pillars
- Pillar 1: intent, document guideline, decision test, anti-goal
- Pillar 2: intent, document guideline, decision test, anti-goal
- Pillar 3: intent, document guideline, decision test, anti-goal

## Core loops
- Moment-to-moment:
- Session loop:
- Long-term loop:

## System design
- Player goal:
- Rules:
- Inputs and outputs:
- Resources or currencies:
- Progression:
- Skill expression or counterplay:
- Failure states:
- Edge cases:
- Tuning levers:

## Why this design
- Player behavior this creates
- Pillar fit
- Tradeoff accepted
- Evidence that would validate it
- Failure signal that would force revision

## Rejected alternatives
- Alternative considered, and why it lost

## Open questions
- Numbered list of unresolved decisions

## Decision log
- Finalized decisions and the rationale for each

## Validation plan
- What to prototype first
- What to measure
- What failure looks like
```

### GDD section

```markdown
# [Section title]

<!-- Metadata only where the project's existing sections carry it -->
- **Document owner**: [name or TBD]
- **Status**: [Draft | In Review | Stable]
- **Last updated**: [date]
- **Revision note**: [what changed and why]

## Design foundation
- Document purpose:
- Primary reader:
- Design intent:
- Design pillars and concrete guidelines:
- Fixed intent:
- Open design space:

## Intro summary
[What this section builds and why each named system matters. Not a comma-separated
inventory of systems.]

## [Subsection per the project's structure]

## Open questions
```

### Beat sheet or onboarding sequence

```markdown
# [Phase or sequence name]

| Beat | Trigger | What unlocks | What the player learns | First success moment |
|------|---------|--------------|------------------------|----------------------|
| 1    |         |              |                        |                      |

## Design rules
- [Constraints governing pacing and sequencing]
```

## Example 1: align before drafting

The user asks for an academy system doc. The fantasy could go several ways, so propose
pillars first.

```markdown
Before drafting, I want to align on pillars so this becomes a point of view rather than
a feature list.

- **Prospect authorship**
  - Intent: the player feels they shaped a prospect's path rather than waiting on hidden
    growth rolls.
  - Guideline: every rule names the player decision, the signal before it, and the
    development consequence after it.
  - Decision test: if the player cannot explain why a prospect changed, the rule fails.
  - Anti-goal: passive youth intake with opaque stat changes.

- **Scarce attention**
  - Intent: academy management creates commitment pressure without becoming a second
    full roster screen.
  - Guideline: define capacity limits, review cadence, and the tradeoff between
    fast-tracking, broad development, and release.
  - Decision test: every academy action competes for time, coaching, budget, or roster
    opportunity.
  - Anti-goal: optimal weekly maintenance where every prospect improves at once.

Does this match your intended fantasy, or should it lean toward realism, prospect
bonding, or ruthless roster optimization?
```

## Example 2: revise without inventing

Weak source text:

```markdown
Players can train hard or rest. If they train too much they get tired, and if they rest
too much they lose momentum.
```

Revision notes first. Fixed intent: training and rest create a readable weekly tradeoff.
Pillar to preserve: the player understands the cost before choosing and sees the
consequence after the next match. Required improvement: named states, thresholds,
warnings, and carryover rules in place of vague outcomes.

```markdown
Fatigue pressures the player in a deliberate order.

1. Training efficiency drops first. Above `[PLACEHOLDER: 50]` fatigue, high-intensity
   blocks lose value faster than low-intensity blocks.
2. Match readiness degrades later. Above `[PLACEHOLDER: 60]` fatigue, error rates rise
   and execution windows narrow.
3. Rest recovers `[PLACEHOLDER: -10 to -15]` fatigue per block, but advances time and
   cools `Form` toward neutral.

The player sees the current fatigue band, the expected change for each training block,
and a plain-language warning when fatigue is reducing gains.
```

The revision keeps the original tradeoff while making the decision testable. UX gets
surfacing requirements, QA gets threshold checks, and the balance values stay honest as
placeholders rather than pretending the system is tuned. A single "training risk" score
was rejected because it hides too many causes behind one number.

## Example 3: ask before rewriting

The user says to make the game-plans section better, but the draft supports several
directions.

```markdown
There are three different designs hiding in this draft:

1. **Coach-authored plans**: compact strategic commitments made before match day.
   Readable, and it fits the current scope phase.
2. **Adaptive tactical scripting**: conditional logic reacting during the match. More
   mastery, and a real risk of overrunning the current phase.
3. **Narrative-first preparation**: plans mainly produce explainable match reports and
   rivalry beats. Stronger payoff, less direct control.

I recommend the first with a little of the third. It protects the manager fantasy, stays
in scope, and gives match reports enough evidence to prove the player's choices mattered.

Should game plans be a pre-match commitment system, a tactical scripting system, or a
payoff system?
```
