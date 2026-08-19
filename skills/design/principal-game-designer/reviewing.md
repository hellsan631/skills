<!-- humanize-lint: ignore list-density -->
<!-- humanize-lint: ignore inline-header-density -->
<!-- The density rules assume structure has crowded out explanation. This file is four
     review checklists, where a flat list of peer criteria is the shape the content
     wants, so the rules are switched off here rather than obeyed. -->

# Reviewing and auditing

Three modes share this file. **Review GDD** evaluates one design section. **Review PRD**
evaluates a product requirements doc for design feasibility. **Audit** checks a doc set
for cross-section problems.

Never rewrite the document during a review. Identify the problem, quote it, and
recommend the fix. The author revises.

## Verdicts

Every review ends on one label plus a sentence saying why.

- `Blocking`: cannot safely guide implementation, testing, or scope decisions
- `Needs Work`: the direction is useful, and important gaps or contradictions remain
- `Usable`: buildable after follow-up clarification, and not yet strong
- `Strong`: clear, consistent, decision-relevant, ready for handoff

A review that passes says specifically what makes the document strong. Rubber-stamping
teaches the author nothing.

## Review GDD

Work the document against each of these. The pass is done when every one has an answer,
rather than when the findings list looks long enough.

- **Player experience**: every system ties to a player decision, motivation, or beat
- **Why stack**: rules, numbers, and cuts carry behavior, pillar fit, tradeoff, validating
  evidence, and a revision-forcing failure signal
- **Pillar alignment**: are they concrete, and do the rules actually serve them
- **Precision**: numbers present or explicitly marked, no vague qualifiers
- **Completeness**: expected subsections present, no critical gap
- **Consistency**: no contradiction with other sections, cross-references resolve
- **Scope**: no later-phase feature smuggled into the current one
- **Handoff clarity**: the primary reader can act without inventing a design decision,
  measured against the bar the project set rather than an assumed one
- **Failure states**: edge and abuse cases handled or flagged as open questions
- **Hygiene**: status, revision notes, owner, and open questions current

Confirm every claimed cross-file contradiction by opening the other file. An unverified
consistency finding wastes more of the author's time than the problem it reports.

## Review PRD

- **Problem statement**: is the player pain point articulated?
- **Success criteria**: measurable and testable, rather than aspirational
- **Scope boundaries**: in and out stated explicitly
- **Design alignment**: respects the core fantasy, pillars, and current GDD
- **Feasibility**: realistic for the stated timeline, team, and tech
- **Dependencies and risks**: cross-system needs and failure modes identified
- **Acceptance criteria**: QA can write test cases from this
- **Handoff readiness**: engineering can build without another design meeting
- **Open questions**: unknowns surfaced rather than buried in soft language

## Audit

Check the set rather than the section: cross-section contradictions, scope drift,
duplicated rule ownership, broken cross-references, and structural gaps. Report systemic
issues ordered by severity, and name the owning file for each rule that appears twice.

## Anti-patterns

Hunt for these by name. Each is a class of failure that survives a rule-by-rule read
because no individual line looks wrong.

- **Scope leakage**: later-phase material mixed into current-scope rules
- **Fake specificity**: numbers that look precise with no rationale, test plan, or
  placeholder marking
- **Feature soup**: many mechanics listed, core player decision unclear
- **Duplicate rule ownership**: the same behavior specified in two sections, with no
  single owner
- **Invisible agency**: the player chooses, and no UI, report, or downstream state ever
  proves it mattered
- **Unbounded progression**: power, money, certainty, or roster value accumulates with no
  meaningful brake
- **Onboarding overload**: too many concepts at once, worst in first-session beats
- **Flavor without function**: lore or UX copy with no trigger, state change, or
  consequence
- **Success-path-only**: the happy case is specified, and collapse and recovery are not

## Output template

```markdown
# Review: [Document or section name]

## Verdict
- [`Blocking` | `Needs Work` | `Usable` | `Strong`]: [one-sentence rationale]

## Summary
- [1-3 sentence assessment]

## Design pillar alignment
- [Whether pillars are concrete, and whether the rules support them]

## Why stack gaps
- [Rules, numbers, or cuts missing behavior, pillar fit, tradeoff, validation, or
  revision trigger]

## Critical issues
- [Must fix before the section is usable]

## Significant gaps
- [Important content or decisions missing]

## Precision problems
- [Vague language, missing numbers, untracked placeholders]

## Consistency concerns
- [Contradictions with other sections or the stated scope]

## Recommended next steps
- [Ordered list of actions]
```

## Example: GDD review

Reviewing a draft scouting section.

```markdown
# Review: Scouting draft

## Verdict
- `Needs Work`: the information-game fantasy is right, and the section conflicts with
  the established cadence and lacks the rationale to survive future edits.

## Summary
- The draft correctly avoids treating scouting as a raw stat dump.
- It is not implementation-ready: player inputs, timing, output contract, and the scope
  boundary are all underspecified.

## Design pillar alignment
- **Readable uncertainty** is directionally present. The draft wants partial information
  and better reports over time.
- **Scarce attention** is missing. The player never chooses between scouting depth,
  breadth, timing, or opportunity cost.
- **Production clarity** is weak. Engineering and QA cannot infer report states,
  confidence bands, or reveal rules from this prose.

## Why stack gaps
- The draft says reports improve over time without saying why that cadence produces
  better decisions than an immediate full reveal.
- The manual analysis minigame has no stated player-behavior goal. For mastery it is
  later-phase scope. For uncertainty, report confidence already covers it.
- No failure signal. A tuning pass needs to know whether scouting fails by being too
  vague, too deterministic, too frequent, or too costly.

## Critical issues
- The draft says scouting happens "every week". The core loop defines a `2-week` cycle.
- A manual analysis minigame is placed in the current phase, which the report-driven
  scope defers.

## Significant gaps
- What the player allocates each cycle is unstated: capacity, target list, depth, focus,
  or budget.
- Outputs are "better reports" rather than concrete claims, confidence bands, trait
  hints, or risk flags.

## Precision problems
- "Better reports over time" needs to say what changes: narrower stat ranges, more trait
  hints, higher confidence, or fresher form evidence.
- "Deep analysis" is not a spec. Say whether the player reads, filters, compares
  opportunity cost, or makes a tactical choice.

## Consistency concerns
- The section assumes scouting is available at league entry. Org progression gates it
  behind a `Scouting` coaching slot.

## Recommended next steps
- Restore the `2-week` cadence.
- Define per-cycle player inputs: capacity split, target list, depth, focus.
- Convert vague outputs into a report model with confidence, recency, and trait hints.
- Add a short rationale for why uncertainty narrows through investment.
- Move manual analysis into a later-phase hook.
```

## Example: PRD review

Reviewing a sponsor-goals PRD. The pattern to notice is scope pushback grounded in
existing systems rather than taste.

```markdown
# Review: Sponsor goals PRD

## Verdict
- `Usable`: it addresses a real mid-season motivation gap, and it needs tighter scope
  boundaries and acceptance criteria before handoff.

## Summary
- Sponsors are a reasonable way to create short-term goals between major competitive
  beats.
- The risk is a second progression system, unless goals reuse the existing exposure,
  economy, inbox, and rivalry surfaces.

## Why stack gaps
- No explanation of why sponsor goals beat rivalry beats, board expectations, or
  contract clauses for this problem.
- Reward and penalty bands have no stated purpose. A tuning pass needs to know whether
  sponsors apply economy, morale, or reputation pressure.

## Critical issues
- Whether goals are mandatory, optional, or auto-expiring is unstated, and it drives UX,
  economy tuning, and failure handling.

## Significant gaps
- Dependencies on exposure, sponsor tier, inbox delivery, and economy rules are implied
  rather than stated.
- No failure-state design for ignoring, failing, or repeatedly declining a goal.
- The active-goal limit is missing.

## Precision problems
- "Small reward" and "meaningful penalty" need placeholder ranges or a bounded corridor.
- "More variety week to week" is not testable. Use acceptance rate, ignored-goal rate, or
  mid-season session continuation.

## Consistency concerns
- The draft suggests streaming and content tasks, which the current scope phase defers.

## Recommended next steps
- Define active-goal limits, expiration, and reward or penalty bands.
- Reframe around existing systems: exposure, morale, budget pressure, rivalry beats.
- Add acceptance criteria for trigger, delivery surface, payout timing, expiration, and
  failure handling.
```
