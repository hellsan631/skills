---
name: principle-boundary-discipline
description: "Apply when wiring validation, error handling, or framework adapters. Put guards at system boundaries such as the CLI, config, network, and external APIs. Trust internal types, and keep business logic in pure functions."
disable-model-invocation: true
---

# Boundary discipline

Put validation, type narrowing, and error handling at system boundaries. Once data has crossed a validated boundary, internal code trusts it without rechecking. Keep business logic in pure functions and the shell thin and mechanical.

Scattered validation adds noise, repeats work, and can suggest safety it does not provide. Validate data once at the boundary. Keep business logic out of framework wiring so tests can exercise it without the framework.

## Pattern

At boundaries such as CLI args, config files, external APIs, and network protocols, validate input, return errors, and handle defensively.

Inside the system, work with typed data, propagate errors, and skip re-validation. Trust the types.

Across the boundary, expose domain concepts instead of the boundary's private representation. Keep general-purpose mechanism inside and special-purpose policy at the edge.

## Applications

### Validation and error handling

- Validate config at parse time, before it reaches business logic.
- Parse raw data into domain types at the boundary.
- Keep transport, storage, framework, and wire types out of the public surface.
- Once the boundary has validated the data, skip redundant nil checks deep in call chains.

### Code organization

Keep business logic in pure functions with no framework dependencies. Make parse functions pure transforms from raw bytes to typed state. Build prompts by transforming structured state into strings. Make scoring and assessment pure transforms from state to results.

## Tests

Ask, "Is this data crossing a system boundary right now?" If the answer is no, validation is redundant.

Ask, "Can this be a pure function that the shell just calls?" If the answer is yes, extract it.
