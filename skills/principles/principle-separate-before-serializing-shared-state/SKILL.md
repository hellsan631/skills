---
name: principle-separate-before-serializing-shared-state
description: "Apply when concurrent actors might write to the same file, branch, key, or state object. First remove the shared write target. Serialize structurally only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Separate before serializing shared state

When concurrent actors might share mutable state, determine whether they need the same mutable object. Give them separate objects when they publish independent facts. When the design requires one shared object, use lockfiles, sequential phases, or exclusive ownership to enforce serialization. Instructions and conventions cannot control concurrent access.

Concurrent writes to shared state create intermittent race conditions that are hard to reproduce and expensive to debug. Telling agents or goroutines to "take turns" does not serialize their writes.

## Pattern

1. Identify the shared mutable state, including files both actors read and write, branches both push to, and APIs both define and consume.
2. Eliminate the shared write target unless the actors need one canonical object. Give actors that publish independent facts their own files, keys, branches, or state directories. Merge their facts only at the read or reporting boundary. Two workers that put separate `lastX` fields in one `state.json` still share mutable state. Giving them `indexer-state.json` and `metrics-state.json` removes the sharing.
3. When one shared write target is a real invariant, serialize access with lockfiles, sequential phases, a single-writer actor, or atomic compare-and-swap. Treat "we need a lock" as a reason to check the design again. Use the lock only after confirming the invariant.
