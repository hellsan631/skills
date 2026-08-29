---
name: humanize
description: Use when asked to humanize or de-slop text, and before delivering a draft anyone will publish or share. Strips AI tells from prose and verifies the result with a deterministic checker.
disable-model-invocation: true
---

# Humanize

Humanization removes AI tells. Preserve the text's meaning and register. Cut empty wording. When a sentence hides what happened or what must happen, replace the vague wording with details from the source. Never fill a gap with a plausible detail.

## The loop

Every humanize pass goes through all six steps.

1. **Choose the profile.** Match it to the text's medium and audience. Ask for clarification only when it would change the rewrite.
2. **Draft from the source.** Treat supplied material as evidence. When no separate source exists, the original text is the source. Check each unclear claim against that source. Delete a phrase when removing it changes no fact or requirement. If the phrase is the only statement of a requirement, ask the author what the software must do.
3. **Run the checker.** Fix every `error`. For each `review`, revise the text or give a specific reason to keep it.
4. **Re-run until zero errors.** Sometimes applying fixes can reintroduce tells.
5. **Add grounded voice.** Use concrete details. Editorial judgment is optional. Add it only when the medium allows it and the source supports its reason.
6. **Run the judgment pass.** Done when every question in `judgment-pass.md` has an answer against this draft. This step is part of every humanize pass, on every draft, at every length. Delegate to a subagent if the subagent is of the same capability as you.

## Vague claims

"The principles transfer cleanly," "parallel work is first-class," and "version-bound approvals keep the process honest" leave basic questions unanswered. Which principles apply elsewhere? Which work can run at the same time? What does the approval system do? Use answers found in the source.

AI prose often invents a technical label for behavior that nearby prose already explains. Remove the label if the passage still means the same thing without it. Keep it when the document defines it, the code uses it as a name, or the author says the intended readers already know it. After removing a label, change only the grammar affected by its deletion.

Try deleting unclear words first. If the sentence keeps the same fact or requirement, stop. If it does not, replace those words with the detail they stood for in the source. Reread the whole sentence and fix its grammar. Split it only when the replacement leaves two complete statements.

Only add an opinion when the source supports it. Put the supporting fact beside the opinion. When a draft calls software honest, smart, or thoughtful, replace that trait with the action or result it refers to in the source. If the trait is the only statement of a requirement, ask what the software must do.

## Contrasts

`Not just X, but Y` says that X and Y are both true. Write `X and Y` when both matter. Write Y alone when X only sets up Y. Removing only `just` turns the first claim into its opposite.

A bare `X, not Y` may state a real exclusion. Keep Y when removing it changes the document's meaning or a requirement. Drop Y when X already makes the point or another sentence already states the boundary. Rewriting Y as a separate `Do not Y` sentence does not make it necessary. Use that command only when the source states a prohibition; otherwise keep a descriptive exclusion descriptive.

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
