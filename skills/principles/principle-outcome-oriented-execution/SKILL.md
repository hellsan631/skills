---
name: principle-outcome-oriented-execution
description: "Apply during planned rewrites and migrations with explicit phase boundaries. Accept intermediate breakage only after planning and scoping it and confirming that you can reverse it. Move toward the target architecture without adding throwaway compatibility code to smooth those phases."
disable-model-invocation: true
---

# Outcome-oriented execution

Prioritize the intended, verifiable end state over smooth intermediate states.

Keeping every intermediate step fully stable often leaves temporary compatibility code in place after the migration. Move toward the target architecture and prove correctness at explicit verification boundaries.

## Rules

- Give end-state integrity priority over transitional stability.
- Accept intermediate breakage only after planning and scoping it, and only if you can reverse it.
- Run final verification before declaring the work done.

## Guardrails

- Use this principle for planned rewrites and migrations with explicit phase boundaries.
- Declare where temporary breakage is acceptable.
- Run high-signal checks for actively touched areas while migrating.
- Require full static and runtime verification when the plan is complete.
