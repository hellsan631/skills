---
name: principle-redesign-from-first-principles
description: "Apply when integrating a new requirement into an existing design. Rework the design under the assumption that the requirement existed on day one."
disable-model-invocation: true
---

# Redesign from first principles

Start with the whole design when integrating a change. Treat the new requirement as an assumption that existed from the beginning. The result should match what we would have built if we had known about it on day one.

- Read every affected file and understand the current design as a whole.
- Ask, "If we were writing this from scratch with this new requirement, what would we build?"
- Carry the change through every reference, including types, docs, examples, and rationale sections.
- Design the change as a whole, then deliver it incrementally.

This is the method for preserving option value when integrating changes into an existing design.
