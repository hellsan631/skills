---
name: blast-radius
description: "Use for 'blast radius of X', 'what could this break', or when reviewing a small diff you do not trust. Trace breakage beyond the diff and prove the fact the change's safety depends on by running real code."
disable-model-invocation: true
---

# Blast radius

Find what a change could break elsewhere before it ships. Use for "blast radius of X", "what could this break", or when reviewing a small diff you do not trust yet.

`how` explains what the code does, and `why` explains why it has its current shape. Blast radius traces what a change could break elsewhere.

A list of callers from grep is only a starting point. Trace the breakage that grep does not reveal.

## Prove the safety claim

A plausible blast-radius writeup can still be wrong. Identify the one or two facts on which the analysis depends and prove them by running code. Do not return the analysis as settled until you have executable proof or have marked those facts unproven. Use the written analysis to decide what to execute.

### Evidence levels

For each fact on which the change's safety depends, reach the highest level that is cheap and report where the evidence stopped.

1. **Claim only.** Your assertion has no evidentiary value on its own.
2. **Source line.** Cite a real `file:line` or the library's own source.
3. **Failure walk-through.** Trace the failure step by step and show that it cannot reach the bad outcome.
4. **Executable proof.** Run a script or test that calls the real code and fails loudly if the claim is wrong.
5. **Running app.** Reproduce the behavior in the running app.

Report any safety fact that does not reach step 4 as unproven. Do not present it as settled. Step 4 usually needs one small script that imports the same library the app ships and calls the exact function in question.

## Steps

1. Read the diff, the symbols it adds, changes, and deletes, and the resulting behavior, including effects the diff leaves implicit. Work from step 2 of `why` to pull the PR and commits.
2. Find the one fact that makes the change safe. Most changes that appear risky are safe because of one fact, such as "this call only drops already-dead cache entries and does nothing else". If that fact holds, it eliminates most of the alarming cases. Concentrate on verifying it. Pursue another risk only while the evidence gives it a real chance of happening.
3. Trace dependencies beyond grep. Read the called library's source, then check its pinned version and any local patch. Determine when code runs: microtask timing, unmount and teardown order, and lifecycle differences between Solid and React. Follow what a symbol search misses: JSON returned by an API, a DB column, a wire format, another language reading the same bytes, a feature flag, or code three hops downstream.
4. Assess each risk. State a realistic likelihood and cost. Keep confirmed risks and list checked, cleared risks separately. Apply the same rules as `why`: cite a real `file:line`; a search with no matches is still an answer; never invent a caller or an API.
5. Prove the safety fact. Write and run a script or test against the real code, then paste the result. If proof would be expensive, mark the fact unproven. Do not claim more confidence than the evidence supports.
6. For a big or wide change, run it as an `arena`. Ask several models the same question and merge the answers. Different models catch different real bugs.

## What to hand back

Open with the change's behavior, including effects that are not explicit in the diff. Then state the one fact that makes it safe, report the evidence level, and show the proof. If you could not prove it, label it unproven.

List only real risks. For each one, state how it breaks, the `file:line`, its likelihood and cost, and how to check it. Paste proof for the risks that matter. Then list what you checked and cleared, with the reason each risk does not apply. Finish with the cheapest test or repro that catches the real bug before merge, and include the script you wrote.

Work from `unslop` while writing, cite real code, and remove private information before publishing anything.

**Reply:** the writeup above, with the one safety fact either proven or marked unproven.
