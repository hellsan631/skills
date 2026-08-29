---
name: show-me-your-work
description: "Use for /show-me-your-work, autonomous or multi-phase runs, long-running or unattended work, or work a human reviews after stepping away. Keeps a TSV decision log with one row per decision covering what, why, evidence, and result. Leaves the log local by default and commits it when a reviewer needs the trail to trust the result."
disable-model-invocation: true
---

# Show me your work

For work a human reviews after the fact, a decision trail records decisions with their reasons and supporting evidence. The reviewer can reconstruct the run without rerunning the work or reading the whole transcript. Keep one log so a future agent can find the complete trail in one place.

## The format

Keep all decisions in one TSV file, with one decision per row. GitHub renders TSV as a sortable table. Spreadsheets and `column -s$'\t' -t` can read it, and the helper appends a row with one command. Keep every cell on one line and use a link or path for evidence.

Copy `references/decision-log-template.tsv` (the header row) to start a clean log. Columns:

- **ts.** ISO8601 timestamp.
- **phase.** The phase or workstream.
- **decision.** What you chose or did, in one line.
- **why.** The reason in plain words. Spell out any principle that drove it (`explored options first, this was a one-way door`).
- **evidence.** A link or path that proves the row's claim, such as a commit SHA, PR number, `file:line`, artifact, trace, or screenshot path. Keep prose out of this cell.
- **result.** The outcome or current state, such as `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, or `open`.

This example shows the intended plain-spoken style. Do not copy its rows into a real log.

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Logging a row

Write each entry the way you'd tell a teammate what you did. Use plain words and concrete actions. The `unslop` skill applies to log text too, so remove AI speak and abstract jargon. A reviewer should understand each row without decoding it.

Use `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>` so rows stay well-formed. The helper stamps `ts`, writes the header on first use, and strips stray tabs and newlines. It also prefixes any cell starting with `=`, `+`, `-`, or `@` with a single quote. This prevents formula execution when a reviewer opens the log in a spreadsheet. You may append a row with a bare `printf`, but apply the same protection when cells contain generated or user-supplied text.

Only log decision points and checkpoints. These include a chosen fork, a completed unit and its verification result, a pivot or revert and its trigger, a surfaced blocker, or a fixed gate. For loop runs, write one row per iteration. Skip trivial and self-evident actions.

## Where it lives

By default, keep the log as an uncommitted working artifact. Store it at `decisions.tsv` in the work directory, or at `.audit/<task-slug>.tsv` when several efforts run at once, and leave it out of git. You can discard the local log after the run.

Commit the log only when a reviewer needs the trail to trust the result of ambitious work, such as a large cross-language port or a multi-week migration. A committed log renders as a table in the PR.

## Rules

- One row covers one decision or checkpoint. If an entry does not fit on one line, clarify the decision before logging it.
- The log is append-only. When a call was wrong, append a new row that supersedes it. Never edit or delete history.
- Use evidence produced by committed scripts when possible so a reviewer can rerun it. Work from the `encode-lessons-in-structure` principle skill.

## Audit the log against the transcript

At the end of the run, compare the log with the work before handing back. Read this run's transcript under the active workspace's `agent-transcripts/` directory; the system prompt names the path. Do not glob across `~/.cursor/projects/*/` because that reads unrelated private chats. Check every row against the transcript:

- Every row maps to a real action. Remove invented or aspirational entries.
- Each row's evidence resolves and shows what the row claims.
- Add any fork, pivot, or abandoned approach that shaped the work but is missing from the log.
- Remove padding. Keep only rows someone would audit.

If a row diverges from the work, correct the row to match what happened.

## Cross-model review of the trail

Before handing back, you must spawn a subagent from a different model family than the one that did the work. The different model family brings fresh eyes that the original model cannot. The subagent reads the audit trail and the run's transcript, then scans only for the following suboptimal or risky points:

- Decisions logged with weak or absent evidence.
- Verification steps skipped or claimed without proof in the transcript.
- Choices that look risky in hindsight (premature, scope-creeping, papering over a symptom).
- Gaps the user would otherwise miss on a casual skim.

Every reply for a run that produced a trail ends with an "Attention" section. Put the reviewer's model on its own line (`reviewed by <model>`), then list each flag with a pointer to specific rows or moments. When the review finds none, write `No flags` after the model line. The model name alone does not complete the section. The self-audit checks whether the log matches the work. The cross-model review identifies what the user should still scrutinize even when it does.

## Reviewing the trail

Read the trail from top to bottom, follow its evidence pointers, and spot-check the claims. GitHub renders a committed TSV as a table. Run `column -s$'\t' -t decisions.tsv` to render it in a terminal. Treat unresolved evidence or an unverified result as a gap.

## Composing this skill

Other skills use this skill for their audit trail. Reference it by name and use its format. Do not restate the columns.
