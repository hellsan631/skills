---
name: improve-codebase-architecture
description: Use when a codebase has architectural friction and the user wants refactoring options. Finds deepening opportunities, presents them in a visual HTML report, then explores the selected candidate through the grilling decision tree.
disable-model-invocation: true
---

<!-- Leverage is a defined term borrowed from codebase-design, not a stray buzzword. -->
<!-- humanize-lint: ignore-file ai-vocabulary -->

# Improve codebase architecture

Find architectural friction and propose **deepening opportunities**, refactors that turn shallow modules into deep ones. The goals are testability and code that an AI can navigate.

Use the project's domain model and the shared design vocabulary:

- Read the `codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- Use the domain language in `CONTEXT.md` to name seams. ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Explore

Apply YAGNI when choosing the scan scope. Deepening a module makes future changes to it easier, so give extra weight to parts of the codebase that changed recently. Decide *where* to look before scanning:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, review `git log --oneline` far enough to identify hot spots, the files and areas that recur in commit history. Start with those paths. If the changes are scattered and no hot spot emerges, widen the scan.

Read the project's domain glossary (`CONTEXT.md`) and any ADRs in the area you're touching first.

Then spawn a sub-agent to walk the codebase. Use these questions as prompts instead of a fixed checklist. Follow the codebase wherever the questions lead, and record the friction the sub-agent encounters:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repository. Resolve the temp directory from `$TMPDIR`, falling back to `/tmp` or `%TEMP%` on Windows. Write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user with `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows, then give them the absolute path.

Use **Tailwind via CDN** for the report's layout and styling. Use **Mermaid via CDN** when a graph, flow, or sequence communicates the structure, including call graphs, dependencies, and sequences. Mix Mermaid with hand-crafted CSS and SVG, using hand-built divs or SVG for editorial forms such as mass diagrams, cross-sections, and collapse animations. Give every candidate a **before/after visualisation**.

For each candidate, render a card with:

- **Scope**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: the locality and leverage gained, and how tests would improve
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section that names the candidate you would tackle first and explains why.

Use `CONTEXT.md` vocabulary for the domain and `codebase-design` vocabulary for the architecture. If `CONTEXT.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

If a candidate conflicts with an existing ADR, include it only when the observed friction warrants revisiting that ADR. Mark the conflict in the card, for example with a warning callout: _"contradicts ADR-0007, but worth reopening because…"_. Do not list every theoretical refactor that an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, work from the `grilling` skill to walk the decision tree with them. The tree covers constraints, dependencies, the shape of the deepened module, what sits behind the seam, and what tests survive.

Record decisions as they settle. Work from the `domain-modeling` skill to keep the domain model current during the conversation:

- If you name the deepened module after a concept that is absent from `CONTEXT.md`, add the term. Create the file lazily if it does not exist.
- When the conversation sharpens a vague term, update `CONTEXT.md` immediately.
- If the user rejects the candidate for a reason that a future explorer needs to avoid suggesting it again, offer an ADR with this wording: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Skip ephemeral reasons ("not worth it right now") and self-evident reasons.
- If the user wants to explore alternative interfaces for the deepened module, read the `codebase-design` skill and use its design-it-twice parallel sub-agent pattern.
