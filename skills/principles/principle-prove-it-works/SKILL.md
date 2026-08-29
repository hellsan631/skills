---
name: principle-prove-it-works
description: "Apply after completing a task and before declaring it done. Verify the real artifact by running the feature, reading the actual value, or inspecting the diff. Proxies, self-reports, and successful compilation do not prove the task works."
disable-model-invocation: true
---

# Prove it works

Check every task's real output directly. Do not infer correctness from proxies, self-reports, or successful compilation.

Until you verify the work, its correctness is unknown. File mtimes, output freshness, agent self-reports, and cached screenshots are indirect checks. They may feel cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

After completing any task, ask, "How do I prove this actually works?"

## Direct evidence

- Check process liveness directly. Derived state alone does not establish liveness.
- Read the actual value. A cached or derived representation is insufficient.
- When verification fails, check the observation method before diagnosing the system.

## Code checks

1. Build it. A successful build is necessary but insufficient.
2. Run it and exercise the actual feature path.
3. Check the full chain. Confirm that data flows from input to output.
4. For integrations, test the full communication path end-to-end.

## Delegated work

Verify delegated work from its actual output artifact, such as the git diff, file contents, or runtime behavior. A delegate's summary reports intent and may not match what happened.

## Script the check when you can

A deterministic script provides the strongest proof because it reruns the same comparison. Write the script, run it, and keep its output so a reviewer can rerun it without trusting your word. A script that compares the old and new compiled output catches what a glance misses.

Keep the artifact visible for the human. Commit it only for large or complex work where the trail must remain auditable, such as a big port or migration covered by the **show-me-your-work** skill. For most work, leave the artifact visible and uncommitted.
