---
name: humanize
description: Strip AI tells from prose: puffery, filler, borrowed significance, bold-header lists, em dashes. Use when asked to humanize or de-slop text, and before delivering a draft the user will publish or share.
---

# Humanize

Prose fails in two directions. **Slop** is the mechanical tells, the puffery and filler
and borrowed significance that mark text as generated. **Sterile** is the
over-correction: every tell removed, nothing put back, which reads as machine-written
just as loudly.

The checker catches slop. Only you catch sterile. A pass that trades one for the other
has not landed.

Humanizing preserves register. A grant paragraph, a legal note, and a forum reply still
sound different from each other afterward. Casual is not the target.

Verify with the checker rather than by rereading. Self-inspection is the weakest verifier
available, because you are checking work against the rules you just wrote it with.

## The loop

Every humanize pass goes through all six steps.

1. **Pick the profile.** Identify medium and audience, inferring when obvious. Ask one
   question only when the answer changes the rewrite.
2. **Draft.**
3. **Run the checker.** Clear every `error`. Fix each `review` or justify keeping it in a
   sentence you could say out loud.
4. **Re-run until zero errors.** Applied fixes reintroduce tells.
5. **Add voice.** Done when no sentence could appear unchanged in some other project's
   writing.
6. **Run the judgment pass.** Done when every question in `judgment-pass.md` has an
   answer against this draft.

## Profiles

`doc` is the default and covers internal docs, plans, specs, PRDs, and READMEs.
Bold-header lists and title-case headings are house style there, so the checker skips
them line by line and watches only whether the document has become an outline.

`reference` covers wiki articles, essays, bios, and anything a stranger reads as a
finished piece. Every structural rule applies.

Profiles move structural strictness only. Puffery, filler, significance bloat, vague
attribution, and assistant artifacts stay errors in both. Wanting a profile to relax a
prose rule means the prose is wrong.

## Running the checker

```bash
humanize-lint draft.md
humanize-lint article.md --profile reference
```

When that command is missing, run `scripts/install-shim.sh` from this skill's own
directory once. It takes no arguments and puts `humanize-lint` on PATH, wherever the
install route placed the skill.

Chat replies go through the checker too. Write the reply to a temp file and lint that
with `--format plain`.

`--format` matches the delivery target and is independent of profile. `--strict` fails on
reviews, `--all` expands notes. Run `--help` for the rest.

## Severities

`error` is a violation and goes. `review` is context-dependent: `crucial` may be right in
a safety notice, and one em dash may be right in a long paragraph. Keep one only when you
can say why. `note` never fails a run and collapses into a single summary line, so act on
it when the fix is cheap and move on.

Findings arrive grouped by category, so fix a whole pattern at a time. Fix the pattern
rather than the string match. Swapping "plays a pivotal role in" for "is significant for"
lands clean and still says nothing.

`list-density` and `inline-header-density` report once for the document instead of per
line. Both mean structure has replaced explanation. Convert the parts that argue or
explain into paragraphs, and keep bullets for genuinely parallel items.

## Voice

Where the medium has an author, take a position instead of listing considerations evenly.
Say which option you would choose and what you would regret about the other. Vary
sentence length on purpose, because one short sentence after two long ones does more for
rhythm than any word choice. Let the structure stay slightly uneven, since perfectly
parallel sections look machine-made. Name the awkward part rather than resolving it:
"fast, but it silently drops duplicates" beats "fast".

Where the medium is reference writing, voice comes from specificity rather than opinion.
Neutral point of view rules out "I think" but not the named source or the number that
makes a sentence belong to this subject and no other.

## Guardrails

When a sentence has nothing behind it, delete it or ask the user for the fact. Inventing
a plausible founding date to replace "renowned for its rich heritage" is a worse failure
than the puffery was. Watch the moment you replace vague praise with concrete detail,
because that is where invention happens.

Carry through unchanged: names, dates, numbers, citations, quoted text, commitments,
domain terminology, and the placeholder markers an author put there on purpose. In specs
that extends to acceptance criteria, rationale, tuning ranges, and open questions. Prose
that reads well but no longer says what to build is a failed edit.

## Reference

`judgment-pass.md` holds what the checker cannot see: register drift, unsupported claims,
invention, dropped facts, unearned structure. Step 6 works through it. For a long draft
or for public writing, hand that pass to a subagent, and the file says how.

`checker.md` covers suppressing a false positive and adding a rule the checker missed.
