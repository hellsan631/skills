---
name: prototype
description: Use when you need to sanity-check a state model or interaction before building it, or when you need to decide what a UI should look like. Builds a throwaway prototype to answer the question.
disable-model-invocation: true
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Use the user's prompt and the surrounding code to identify the question. If they do not settle it and the user is available, ask:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build one shareable HTML file with free-play buttons and tabbed guided walkthroughs. It must push the state machine through cases that are hard to reason about on paper, and a non-developer must be able to drive it.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on one route. Make them switchable through a URL search parameter and a floating bottom bar.

The branches produce different artifacts, and choosing the wrong one wastes the prototype. If the question remains ambiguous and the user is unavailable, use the surrounding code: choose logic for a backend module and UI for a page or component. State the assumption at the top of the prototype.

## Rules for both branches

1. **Mark it as throwaway code from the start.** Put the prototype next to the module or page it tests so its context is visible. Name it as a prototype so a casual reader does not mistake it for production code. For throwaway UI routes, follow the project's existing routing convention. Do not add a new top-level structure.
2. **Make it one step to run.** Start a UI prototype with one command in the project's task runner, such as `pnpm <name>`, `python <path>`, or `bun <path>`. Make a logic demo a single HTML file the user can open by double-clicking.
3. **Keep state in memory by default.** Add persistence only when the prototype is checking persistence. If the question explicitly involves a database, use a scratch database or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Build only enough to answer the question.** Add no tests or abstractions, and no error handling beyond what makes the prototype runnable. The point is to learn something fast.
5. **Show the state.** After every logic action and every UI variant switch, print or render the full relevant state so the user can see what changed.
6. **Capture the result.** Fold every validated decision into the real code. Preserve the prototype as a **primary source** by committing it to a throwaway branch outside main and leaving a context pointer to that branch on the implementation issue. Record the answer, including the verdict and the question it settled, in the issue or a commit. Keep only the validated decision on the main branch.
