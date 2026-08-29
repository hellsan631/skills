---
name: codebase-design
description: Use when designing or improving a module's interface, when deciding where a seam goes, when code needs to be more testable or navigable, or when another skill needs the deep-module vocabulary of depth, seams, adapters, leverage, and locality.
disable-model-invocation: true
---

<!-- Leverage is a defined term in this vocabulary, not a stray buzzword. -->
<!-- humanize-lint: ignore-file ai-vocabulary -->

# Codebase design

Design **deep modules** by placing a large amount of behaviour behind a small interface at a clean seam. Test the module through that interface. Use this vocabulary and these principles whenever you design or restructure code. Depth gives callers leverage, gives maintainers locality, and lets tests use the same interface as callers.

## Glossary

Use these terms exactly. Do not substitute "component," "service," "API," or "boundary."

**Module**: anything with an interface and an implementation. The term applies at any scale, including a function, class, package, or tier-spanning slice. _Avoid_: unit, component, service.

**Interface**: everything a caller must know to use the module correctly. This includes the type signature, invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API and signature, which refer only to the type-level surface and are too narrow.

**Implementation**: the code inside a module. Keep it distinct from **Adapter**. A Postgres repository can be a small adapter with a large implementation, while an in-memory fake can be a large adapter with a small implementation. Use "adapter" when discussing the seam and "implementation" otherwise.

**Depth**: leverage at the interface. The amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation.

**Seam** _(Michael Feathers)_: a place where you can alter behaviour without editing code at that place. It is the *location* of a module's interface. Seam placement is a separate design decision from what goes behind it. _Avoid_: boundary, which is overloaded with DDD's bounded context.

**Adapter**: a concrete thing that satisfies an interface at a seam. The term describes its *role*, the slot it fills.

**Leverage**: what callers get from depth. More capability per unit of interface they learn. One implementation serves N call sites and M tests.

**Locality**: what maintainers get from depth. Changes, bugs, required knowledge, and verification stay in one place instead of spreading across callers. A fix in the implementation applies to every caller.

## Deep and shallow modules

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can contain small, mockable, swappable parts. Those parts remain outside its interface. A module can have **internal seams**, private to its implementation and used by its own tests, as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If deletion removes complexity, the module was a pass-through. If the same complexity reappears across N callers, the module keeps that complexity out of those callers.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Do not introduce a seam unless something varies across it.

## Designing for testability

These interface choices reduce test setup and let tests cross the same seam as callers:

1. **Accept dependencies, don't create them.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **Return results, don't produce side effects.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **Keep the interface small.** Fewer methods require fewer tests. Fewer parameters simplify test setup.

## Relationships

- A **Module** has exactly one **Interface**, which it presents to callers and tests.
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as a ratio of implementation lines to interface lines** (Ousterhout) rewards padding the implementation. Use depth as leverage instead.
- **"Interface" as the TypeScript `interface` keyword or a class's public methods** is too narrow. Interface here includes every fact a caller must know.
- **"Boundary"** is overloaded with DDD's bounded context. Say **seam** or **interface**.

## Going deeper

- For dependency categories, seam discipline, and replace-don't-layer testing when deepening a cluster, read [DEEPENING.md](DEEPENING.md).
- To explore alternative interfaces, read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md). Spin up parallel sub-agents to design the interface in several radically different ways, then compare them on depth, locality, and seam placement.
