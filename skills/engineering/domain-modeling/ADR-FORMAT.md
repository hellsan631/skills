<!-- humanize-lint: ignore-file list-density — format reference: the arguing already happens in the prose between the lists, and what remains is parallel sets whose entries pair a decision type with the sample ADR sentence that illustrates it -->

# ADR Format

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create the `docs/adr/` directory lazily: only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why*, not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`): useful when decisions are revisited
- **Considered Options**: only when the rejected alternatives are worth remembering
- **Consequences**: only when non-obvious downstream effects need to be called out

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it: you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library: just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it; otherwise someone will suggest GraphQL again in six months.

### What doesn't qualify

Routine, reversible design and implementation choices: spacing tweaks, icon sizing, which
component library handles positioning, copy wording, which of two similar layouts reads
better. Each fails at least one of the three tests above — cheap to reverse, unsurprising,
or no real alternative was ever on the table. These are just the document, updated in
place when they change; they don't need a permanent ID or a citation trail. A project that
mints one for every design tweak ends up with a decision log numbering past 100 entries
that read like citations rather than explanation, which is the failure this section exists
to prevent.

## Don't let the log become the document

A decision log or ADR index is a citation anchor into an explanation that exists somewhere
else, readable start to end. It is not that explanation. If a design or architecture document's entire body is its numbered log, with no prose
grouped by topic for a reader to land on, the log has quietly become the document. Readers
are stuck reconstructing "what is actually true now" by chasing citation chains (`D82`
amends `D80` amends `D76`...) instead of reading a current, correct account in one place.

When a later decision amends or supersedes an earlier one, restate the current, authoritative
behavior in the prose the reader encounters, in the section about that topic. The citation
records provenance and history for whoever wants it; it is never a substitute for saying,
once, in the present tense, what is true now. If tracing a single feature requires jumping
between five non-adjacent numbered entries, that feature needs its own section, and the log
entries collapse into that section's history, not its explanation.
