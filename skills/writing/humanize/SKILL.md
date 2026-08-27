---
name: humanize
description: Use when asked to humanize or de-slop text, and before delivering a draft anyone will publish or share. Strips AI tells from prose and verifies the result with a deterministic checker.
disable-model-invocation: true
---

# Humanize

Humanization removes AI tells without changing the text's meaning or register. Cut generic phrasing, make each sentence carry a specific fact, position, or instruction, then verify the result with the checker and judgment pass.

## The loop

Every humanize pass goes through all six steps.

1. **Choose the profile.** Match it to the text's medium and audience. Ask for clarification only when it would change the rewrite.
2. **Draft.**
3. **Run the checker.** Fix every `error`. For each `review`, revise the text or give a specific reason to keep it.
4. **Re-run until zero errors.** Sometimes applying fixes can reintroduce tells.
5. **Add voice.** Use concrete details, and take a position when the medium allows it.
6. **Run the judgment pass.** Done when every question in `judgment-pass.md` has an answer against this draft. This step is part of every humanize pass, on every draft, at every length. Delegate to a subagent if the subagent is of the same capability as you.

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

Findings are grouped by category; look for the pattern that generates them (rather than just string-match). Fix that pattern.

- `list-density`: checks for excessive explanatory text in list items; reports once per document; if it appears, it means your list structure has replaced explanation: if you had an explanation, convert it into a paragraph - keep bullets where items have parallel values.
- `inline-header-density`: checks for excessive explanatory text in inline headers; reports once per document; it means the inline headers have replaced explanation: if you had an explanation, convert it into a paragraph - keep inline headers where they're needed to highlight the cell value.

## Voice: Adding voice to the text

For media with a named author (docs, web pages, essays), take a position rather than listing all options evenly: say which option you would choose, which you would regret, etc. Vary sentence lengths for a better rhythm. Let the structure be slightly uneven. If something sounds awkward, name it: "It may be awkward to split it this way..." etc.

For reference writing, be specific rather than giving opinion: a neutral point of view rules out 'I think' and similar phrases, but does not rule out certain named sources, or specific numbers.

## Guardrails: What to avoid changing

When a sentence has nothing behind it, delete it or ask for a fact to make it real. Do not invent plausible details to replace vague praise.

- Do not change: names, dates, numbers, citations to documents and media, quoted text, commitments, phrasing etc. that refers to domain terminology, placeholder markers such as `[[citation]]` and `[[item in outline]]`; in specs also acceptance criteria, rationale, tuning ranges, open questions.

## Reference: Additional documentation files

- `judgment-pass.md` covers register drift, unsupported claims, invention, dropped facts, unearned structure; this must be run on every draft in Step 6
- `checker.md` covers suppressing false positives and adding rules
