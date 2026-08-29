---
name: principle-encode-lessons-in-structure
description: "Apply when you write the same instruction a second time or notice a recurring correction. Replace repeated text with a lint, metadata flag, runtime check, or script."
disable-model-invocation: true
---

# Encode lessons in structure

Enforce recurring fixes with tools, code, metadata, or automation. Treat every error, human correction, and unexpected outcome as a lesson: record it, decide where it belongs, and act on it.

Textual instructions depend on the reader noticing, remembering, and following them. Lint rules, metadata flags, runtime checks, and automation scripts enforce the rule without that cooperation.

## Pattern

When you catch yourself writing the same instruction a second time:
1. Ask whether a lint rule, metadata flag, runtime check, or script can enforce it.
2. If one can, implement that mechanism and delete the instruction.
3. If the rule genuinely requires judgment, keep the instruction, make it more prominent, and add an example of the failure mode.

## Choose the mechanism

When several mechanisms would work, choose the strongest one the situation allows, in this order:
1. Make the invalid state unrepresentable so it cannot compile.
2. Add a lint or banned API that fails CI.
3. Provide a canonical helper.
4. Add a runtime check.

Agents copy what the surrounding code already does, so a weaker guard becomes the next template.

When a fix is structural, make only the structural fix and delete the textual instruction that exposed the symptom.

## Handle feedback

- When a human intervenes or a test fails, decide whether the correction is a one-off or a pattern.
- Put a one-off in a brain note, a recurring fix in a skill or lint rule, and a systemic issue in a principle.
- Apply the lesson now or create a concrete todo. Recording it alone does not close the loop.

## Failure modes

- Saying "I'll keep that in mind" without recording the correction does not persist.
- A brain note cannot enforce a lint rule. Implement the lint rule in the right layer.
- Fixing one instance while leaving the recurring pattern intact does not generalize the fix.
