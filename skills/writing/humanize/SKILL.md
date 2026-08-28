---
name: humanize
description: Use when asked to humanize or de-slop text, and before delivering a draft anyone will publish or share. Strips AI tells from prose and verifies the result with a deterministic checker.
disable-model-invocation: true
---

# Humanize

Humanization removes AI tells, especially vague claims shaped to sound deliberate or insightful. Preserve the text's meaning and register. Delete empty phrasing, replace it with a precise word or clause, or explain a source-backed mechanism. Use only as much text as the claim needs.

## The loop

Every humanize pass goes through all six steps.

1. **Choose the profile.** Match it to the text's medium and audience. Ask for clarification only when it would change the rewrite.
2. **Draft from the source.** Treat supplied material as evidence. When no separate source exists, the original text is the source. Find vague or calculated claims, then choose the smallest repair that makes each one plain.
3. **Run the checker.** Fix every `error`. For each `review`, revise the text or give a specific reason to keep it.
4. **Re-run until zero errors.** Sometimes applying fixes can reintroduce tells.
5. **Add grounded voice.** Use concrete details. Editorial judgment is optional. Add it only when the medium allows it and the source supports its reason.
6. **Run the judgment pass.** Done when every question in `judgment-pass.md` has an answer against this draft. This step is part of every humanize pass, on every draft, at every length. Delegate to a subagent if the subagent is of the same capability as you.

## Unwinding vague claims

A calculated statement sounds finished while leaving the relationship unnamed. "The principles transfer cleanly," "parallel work is first-class," and "version-bound approvals keep the process honest" all perform clarity without explaining the claim.

Technical-sounding compounds can hide the same gap. "Capability-oriented `AgentFactory`" adds nothing when the following prose already says that callers request an agent by task. Use the stated behavior and remove the label. Keep a technical term when the document defines it, the code names it, or the audience already shares its meaning.

Find the literal claim in the source. Then choose the smallest repair that carries it: delete an empty phrase, replace it with a precise word or clause, or explain the mechanism. Humanization may shorten or expand the text. Editorial judgment is optional and needs an observable fact or source-backed reason. When the source defines the operation behind a human virtue applied to software, name that operation. Delete the virtue when it adds no unique content. Flag a load-bearing commitment for clarification when no source explains it.

## Profiles

There are two humanize profiles, `doc` and `reference`. The difference between them is the structural strictness: some structural rules apply only in `reference`.

### `doc` profile

Apply for internal docs, plans, specs, PRDs, READMEs. These docs often have "house style": bold-header lists and title-case headings are both common. So in `doc` profile, the checker will skip them line by line, and we'll watch for outline structure manually.

### `reference` profile

Apply for wiki articles, essays, bios, finished pieces of prose of any kind. Every structural rule applies.

Any puffery, filler, significance bloat, vague attribution, or assistant artifact is an error and should be rewritten. Wanting a profile to relax a rule that applies to your piece of prose means the prose is wrong.

## Running the checker

Run from terminal with command like this:

`humanize-lint draft.md` or `humanize-lint article.md --profile reference`

If the shell can't find the command, see repository README.

`--format` matches delivery target (html etc.); the format is independent of profile. `--strict` fails on reviews. `--all` expands notes. For the rest, try `--help`.

## Severities: error, review, note - and density checks

- `error` means a violation, ought to be removed
- `review` means context-dependent; may be right choice in safety notice
- `note` means never fails a run; if many, collapses into one summary line; do act on when it's easy to do

Findings are grouped by category. Look for the pattern that generates them, then fix that pattern.

- `list-density`: checks for excessive explanatory text in list items; reports once per document; if it appears, it means your list structure has replaced explanation: if you had an explanation, convert it into a paragraph - keep bullets where items have parallel values.
- `inline-header-density`: checks for excessive explanatory text in inline headers; reports once per document; it means the inline headers have replaced explanation: if you had an explanation, convert it into a paragraph - keep inline headers where they're needed to show the cell value.

## Voice: Adding voice to the text

For media with a named author (docs, web pages, essays), a supported position can add voice. Give its reason. Vary sentence lengths for a better rhythm. Let the structure be slightly uneven. If something sounds awkward, name it.

Reference writing uses supported facts and attributed judgments. A neutral point of view rules out "I think" and similar phrases. It still allows named sources and specific numbers.

## Guardrails: What to avoid changing

When a claim has nothing behind it, delete it or ask for a fact to make it real. Every added actor, action, motive, mechanism, and consequence must be traceable to the supplied material or the original text.

- Keep names, dates, numbers, citations, quoted text, commitments, domain terms, and intentional placeholders such as `[[citation]]` and `[[item in outline]]`. In specs, also keep acceptance criteria, rationale, tuning ranges, and open questions.

## Reference: Additional documentation files

- `judgment-pass.md` covers register drift, unsupported claims, invention, dropped facts, unearned structure; this must be run on every draft in Step 6
- `checker.md` covers suppressing false positives and adding rules
