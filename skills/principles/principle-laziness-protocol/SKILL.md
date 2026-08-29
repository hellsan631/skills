---
name: principle-laziness-protocol
description: "Apply while refactoring, evaluating diff size, or considering adding abstractions, layers, or signal threading. Prefer deletion and make the smallest change that solves the problem."
disable-model-invocation: true
---

# Laziness protocol

Code is cheap for an agent to produce, so over-engineering is easy. Judge a solution by the fatigue it would cause a human maintainer. Get the required result with the least code and complexity.

- When asked to refactor or improve, look for removals before additions.
- Keep the call hierarchy flat and avoid deep call chains. A rich interface that hides substantial work does not count as a deep call chain. If answering a question requires tracing through more than 3 files or layers, flatten it.
- Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- Make the smallest change that solves the problem. Prefer fewer lines to "elegant" boilerplate.
- If a task asks you to pass a new signal through types, schemas, pipelines, or similar layers, stop and look for a more direct path.
- Remove small pass-throughs, representation leaks, and duplicated choices before they spread. These leaks compound into permanent coordination costs.

Reject a solution that a human developer would find exhausting to maintain. Be lazy and keep it simple.
