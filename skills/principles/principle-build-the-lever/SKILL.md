---
name: principle-build-the-lever
description: "Apply to any non-trivial work, whether one-off or bulk, including edits, migrations, analyses, and checks. Build a codemod, script, generator, or skill for subagents that does or proves the work. The resulting file gives reviewers something they can rerun."
disable-model-invocation: true
---
# Build the lever

For work beyond a couple of obvious edits, build a tool that does the job.

A codemod, generator, or script follows the same recipe every time and reruns without repeating the hand work. It also gives a reviewer one artifact to read and run. Checking hand-done changes requires redoing them. A deterministic script turns "trust me" into "run this."

## Pattern

Build the lever by default. Skip it only when the task is genuinely trivial, meaning a couple of obvious edits you can see at a glance.

- Complete the first unit by hand to learn the recipe, then build the tool. Run it on that unit and diff its output against the hand-done version. Make the lever safe to rerun because a reviewer will rerun it.
- Use a codemod or script for edits, a generator for repetitive files, a dump-to-sqlite query for analysis, and a rerunnable check for verification.
- If one deterministic tool can process every unit in a single pass, run it yourself.
- When work does need subagents, write the lever as a skill they all read. Put the recipe, verification contract, and do-not-touch fences in that one artifact so every delegate follows the same version. This avoids re-explaining the contract in each prompt, where versions can drift. Keep the skill outside the delegates' write scope so they cannot edit the contract.
- Applying this principle produces a file. If you cite it, the diff must contain a codemod, script, generator, or delegate skill.
- Commit the lever when the work outlives the session. The next run can then rerun it instead of redoing the work.

## Limits

The threshold is whether the task is trivial. A one-off still earns a lever when the lever makes the work checkable. Per the [Laziness Protocol](../principle-laziness-protocol/SKILL.md), build the smallest script that does or proves the job. Do not build a framework.

[Encode Lessons in Structure](../principle-encode-lessons-in-structure/SKILL.md) turns a recurring instruction into a durable guardrail. Build the Lever improves throughput by doing the current work and reviewability by leaving a rerunnable file. For a script that performs the verification itself, see [Prove It Works](../principle-prove-it-works/SKILL.md).
