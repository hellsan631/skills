---
name: wayfinder
description: Use when a piece of work is too large for one agent session to hold. Plans the work as a shared map of decision tickets on the issue tracker, then resolves them one at a time until the route is clear.
disable-model-invocation: true
---

Use Wayfinder when a loose idea is too large for one agent session and the decisions between the current state and the **destination** are still unclear. Track the effort in a **shared map** on the repo's issue tracker. Resolve the map's **decision tickets** one at a time until the route is clear. Each decision ticket asks a question and ends in a decision. Build slices belong outside these tickets.

The destination varies by effort. Name it first because it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place such as a data-structure migration. The map is domain-agnostic and may cover engineering work or course content.

## Plan by default

Wayfinder plans by default. Each ticket resolves a decision, and the map is complete when no decisions remain before execution can begin. The pull to start execution usually signals that the map has reached its edge and is ready for handoff. An effort's **Notes** can override this default and include execution in the map. Unless the Notes do so, decisions are the map's output and deliverables stay outside it.

## Refer by name

Every map and ticket is an issue. Its title is its **name**. Use the linked name in narration and the map's Decisions so far section. Never use a bare ID, number, or slug in human-facing text. A sequence such as `#42, #43, #44` hides what the issues cover. Put the ID and URL inside the linked name.

## The map

The map is a single issue on this repo's issue tracker, labelled `wayfinder:map`. Its tickets are child issues of the map.

The map is an index of decisions. Each entry gives a one-line gist and links to the ticket that holds the full decision. Keep that detail in exactly one place: the ticket.

The tracker determines where the map, child tickets, blocking relationships, and frontier queries live. The user should provide the issue tracker. If they do not, tell them to run `/setup-engineering-skills`. Consult the tracker document's "Wayfinding operations" section for how this repo represents each operation. If no tracker has been provided, default to the local-markdown tracker.

### The map body

Load the whole map at low resolution once per session. Find open tickets by querying open child issues. Keep them out of the map body.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- one line per closed ticket, enough to judge relevance, with a link to the detail in that ticket -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog that cannot become a ticket yet; it graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed and never graduates -->
```

### Tickets

Each ticket is a child issue of the map, and the tracker's issue ID is its identity. Limit the question so one 100K token agent session can resolve it:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries one `wayfinder:<type>` label: `research`, `prototype`, `grilling`, or `task` (see [Ticket types](#ticket-types)).

Before any work, claim the ticket by assigning it to the developer driving the map. Concurrent sessions skip assigned tickets. The assignment is the claim, and an open, unassigned ticket is unclaimed.

Use the tracker's native dependency relationship for blocking. It displays the frontier in the tracker's UI, so the human can see which tickets are available without opening the map. Use a body convention only when the tracker lacks native blocking. A ticket is **unblocked** when every ticket blocking it is closed. The **frontier** consists of the open, unblocked, unclaimed child issues at the edge of the known route.

Record the answer when resolving the ticket, outside the ticket body (see [Work through the map](#work-through-the-map)). Link assets created during resolution from the issue instead of pasting them into it.

## Ticket types

Every ticket is either **HITL** or **AFK**. HITL means human in the loop. The agent works a HITL ticket with a human who speaks for themselves. The agent drives an AFK ticket alone. A HITL ticket requires a live exchange. The agent cannot supply the human's side of the exchange; a grilling agent that answers its own questions violates this requirement.

- **Research** (AFK): Read documentation, third-party APIs, or local resources such as knowledge bases to find a fact needed for a decision. Have a subagent resolve the ticket by working from the `research` skill. Use this type when the decision requires knowledge outside the current working directory.
- **Prototype** (HITL): Work from the `prototype` skill to make a cheap, rough, concrete artifact for the human to react to, such as an outline, rough take, stub, or UI or logic code. Link the prototype as an asset. Use this type when the key question is "how should it look" or "how should it behave."
- **Grilling** (HITL): Conversation. The default case. Always work from both `grilling` and `domain-modeling`.
- **Task** (HITL or AFK): Complete manual work that must happen before a decision can be made. Use this type when there is no decision to discuss, prototype to make, or research to conduct, but the discussion remains blocked until the work is done. Examples include signing up for a service so its API can be judged, provisioning access, and moving data so its shape can be seen. A task is the only ticket type whose resolution is the work itself. Its purpose is to unblock a decision; it must not deliver the destination. The agent completes it alone where possible (AFK). Otherwise, the agent gives the human a precise checklist (HITL). Resolve the ticket when the work is done. In the answer, record the work and any resulting facts that later tickets depend on, such as a credentials location, new URLs, or row counts.

## Fog of war

The map is intentionally incomplete. Do not chart what you cannot see yet. The **fog of war** covers decisions and investigations you expect but cannot state precisely because they depend on open questions. Resolving a ticket may make some of them precise enough to become new tickets. Create those tickets one at a time until the route to the destination is clear and no tickets remain.

Record that incomplete view in the map's **Not yet specified** section as a suspected question or an area to revisit. Everything there is in scope but is not precise enough to become a ticket. Include as much detail as the current information supports. This tells collaborators where the effort is headed.

Classify an item by whether you can state its question precisely now. Your ability to answer it now does not affect the classification.

- Create a ticket when the question is precise, even if it is blocked and cannot be acted on yet.
- Put the item in **Not yet specified** when you cannot phrase the question precisely. Keep the fog coarser than a ticket. Once the frontier reaches one patch of fog, it may produce several tickets or none.

Keep decided items in Decisions so far, active questions in live tickets, and excluded work in Out of scope. None of them belongs in **Not yet specified**.

## Out of scope

Fog covers only in-scope uncertainty on the route to the destination. The destination sets the scope. Put work beyond it in the map's **Out of scope** section and keep it out of **Not yet specified**. Classification here depends on scope, regardless of how precisely the work can be stated.

Out-of-scope work never graduates because the frontier stops at the destination. If the destination is redrawn to include that work, start a fresh effort rather than resuming this one.

Treat a ruling of out of scope as a scope boundary. An existing ticket may turn out to sit past the destination because it was mis-scoped during charting or because a resolution exposed its position. Close the ticket to remove it from the frontier. Add one line to **Out of scope** with a gist, the reason it is out, and a link to the closed ticket. Keep it out of **Decisions so far**, which records the decisions made along the route.

## Invocation

Wayfinder has two modes. Resolve at most one non-research ticket per session.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Work from both `grilling` and `domain-modeling` to define the spec, decision, or change that the map must reach. The destination fixes the scope, so settle it first.
2. **Map the frontier.** Work from `grilling` again and proceed breadth-first. Cover the whole space before going deep on one thread, surfacing the open decisions and the first steps available now. If this reveals no fog because the route is already clear and the whole journey fits in one session, stop and ask the user how they want to proceed without a map.
3. **Create the map.** Apply the `wayfinder:map` label. Fill in Destination and Notes, leave Decisions so far empty, and sketch the fog in **Not yet specified**.
4. **Create the tickets you can specify now.** Make them child issues of the map. Wire their blocking edges in a second pass because issues need IDs before they can reference each other. The wiring divides them between the frontier and the blocked set. Keep everything you cannot specify yet in **Not yet specified**.
5. **Start the research subagents.** For each `research` ticket you just created, start a subagent that works from the `research` skill. Run these subagents in parallel. Each one resolves its ticket and captures its findings on a throwaway `research/<name>` branch with a context pointer from the ticket.
6. Charting is one session's work. Stop after charting; the charting session does not resolve a ticket itself.

### Work through the map

The user invokes with a map URL or number and may name a ticket. When no ticket is named, choose the next decision.

1. Load the low-resolution **map** without loading every ticket body.
2. Choose the ticket. Use the one the user named, or take the first frontier ticket in order. Claim it by assigning it to yourself before any work.
3. Resolve the ticket. Fetch the full body of a related or closed ticket only when needed. Work from the skills named in the `## Notes` block. If in doubt, use `grilling` and `domain-modeling`.
4. Record the resolution. Post the answer and its reasoning as a resolution comment. A future reader uses that reasoning to decide whether to trust the answer or reopen the question. Close the issue and append a context pointer to the map's Decisions so far section.
5. Add newly surfaced tickets by creating and then wiring them. Graduate any fog that the answer has made precise enough to become a ticket. Remove each graduated patch from **Not yet specified** so its new ticket is the only copy. Handle any ticket beyond the destination with the out-of-scope process above. If the decision invalidates other parts of the map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.
