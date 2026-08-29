---
name: arena
description: "Spawn N parallel candidates for the same task, pick a base, and graft the strongest parts of the others into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact could lock in the wrong shape."
disable-model-invocation: true
---

# Arena

Run N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base, graft the best ideas from the others into it, and verify the synthesized result.

## Start

Before launching anything, open a todolist with one entry per phase. Once launched, continue through all six phases on your own. Track each phase in the list until all six are complete.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The shared prompt is the contract for every candidate. Settle it before spawning them.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete, gradeable criteria. `Adds a --dry-run flag that skips writes` is concrete. `code is correct` is vague. The picker uses the rubric in Phase D. Candidates receive only the task.
3. Pick the runners. Use `arena runners` from `~/.cursor/rules/pstack-models.mdc` when present. Otherwise default to one each on `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, and `claude-opus-5-thinking-xhigh`. Spawn more when the arena covers multiple design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive.
4. Assign each candidate its own output path, as required by `principle-separate-before-serializing-shared-state`. Use a git worktree where possible; otherwise use `/tmp/arena-<slug>/candidate-<n>/`. If N candidates write to the same path, they create shared mutable state.

## Phase B: Fan out

Spawn all N subagents in one message with `run_in_background: true`. Give each subagent the task, the path to the shared grounding, its own output path, and instructions to produce both the artifact and a short rationale.

Require the rationale to name the alternatives the candidate considered and rejected. The parent uses that comparison to choose what to graft in Phase E.

If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Cross-judge

After all Phase B candidates complete, choose one model from the `arena cross-judge pool` in `~/.cursor/rules/pstack-models.mdc` when present. Otherwise choose one of `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, or `claude-opus-5-thinking-xhigh`. Prefer a model family different from the parent's. Spawn one readonly judge subagent on that model. Give it the rubric and each candidate's labeled path. It scores every criterion and recommends a base with a rationale. Start the judge after every candidate finishes, at the same time as the parent begins reading them in Phase D. Starting it earlier exposes partial or empty outputs, which the judge reports as dropouts.

## Phase D: Pick a base

Read every candidate end to end before picking. A skim favors the candidate whose presentation looks most familiar.

Score each candidate separately on every rubric criterion and use those scores for the comparison. Compare your result with the cross-judge's recommendation. Choosing the same base confirms the pick. If the choices differ, bias affected one evaluation or the rubric is ambiguous. Read both rationales before deciding.

Pick the candidate that requires the least effort for a future maintainer to extend while preserving its invariants. If two candidates remain tied, follow the Laziness Protocol: prefer the cleaner boundary or smaller surface area.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Review each losing candidate once more and identify the parts worth porting into the base. Usually only one or two parts per candidate are worth grafting.

Integrate each graft by hand. Work from `principle-redesign-from-first-principles` and adapt the graft to the base so the result follows one design.

Record every graft and its source candidate. Also record each rejection and its reason. Future readers learn from both the grafts and rejections. The rejection notes carry the most signal because they show which alternatives you considered and dropped.

When N candidates converge on the same shape, note their agreement in the record and ship the consensus shape without a graft. When N candidates diverge widely, Phase A was under-specified. Reframe and re-run.

## Phase F: Verify

Apply the same verification checks to the synthesized artifact as you would to any other output. Work from `principle-prove-it-works`.

If verification finds a problem that the arena missed, determine which failure occurred. If Phase A was wrong, re-frame and re-run. If one candidate caught the problem but you missed the graft, return to Phase E. Fix the problem through the corresponding phase.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.
