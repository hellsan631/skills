<!-- A bucket README is a catalog: every entry is a skill name, so every entry is a label. -->
<!-- humanize-lint: ignore-file inline-header-density -->

# Principles

Each of these is a single engineering conviction, written so it can be applied to a
decision and argued with. They are short on purpose: a principle you have to scroll
through is one nobody invokes mid-task.

They are all user-invoked, so none of them costs context until you name one. Other skills
cite them as a test to apply rather than a rule to obey, which is why
[arena](../workflow/arena/SKILL.md) can say a design fails
`separate-before-serializing-shared-state` and have that mean something specific.

- **[boundary-discipline](./principle-boundary-discipline/SKILL.md)**: concentrate guards
  at system boundaries so the interior can trust its inputs.
- **[build-the-lever](./principle-build-the-lever/SKILL.md)**: make the tool that does the
  work instead of grinding through it by hand.
- **[encode-lessons-in-structure](./principle-encode-lessons-in-structure/SKILL.md)**: when
  a correction recurs, change the structure that allowed it instead of repeating yourself.
- **[experience-first](./principle-experience-first/SKILL.md)**: resolve product tradeoffs
  toward what the user feels, not what is convenient to implement.
- **[guard-the-context-window](./principle-guard-the-context-window/SKILL.md)**: route bulk
  output to subagents and files so the main thread keeps its judgment.
- **[laziness-protocol](./principle-laziness-protocol/SKILL.md)**: bias against new
  abstractions, layers, and threaded signals.
- **[outcome-oriented-execution](./principle-outcome-oriented-execution/SKILL.md)**:
  converge on the target architecture instead of preserving intermediate states.
- **[prove-it-works](./principle-prove-it-works/SKILL.md)**: verify against the real
  artifact before declaring anything done.
- **[redesign-from-first-principles](./principle-redesign-from-first-principles/SKILL.md)**:
  integrate a new requirement as though it had been there from the start.
- **[separate-before-serializing-shared-state](./principle-separate-before-serializing-shared-state/SKILL.md)**:
  when concurrent actors might write the same thing, remove the sharing before adding a lock.
