---
name: principle-guard-the-context-window
description: "Apply when large outputs, long files, repeated reads, or fan-out planning fill the context. Send bulk material to subagents. Keep summaries in the main thread and raw payloads out."
disable-model-invocation: true
---

# Guard the context window

A session has a fixed context window. Include only material that helps the current work.

Context overflow harms reasoning, creates compression artifacts, and halts progress. More compute or time cannot reclaim context already spent inside a session.

## Pattern

- Send verbose outputs, screenshots, and large documents to subagents. Put their summaries in the main context and leave out the raw data.
- Read only the files and sections relevant to the current task. Skip any file you will not use.
- Keep templates and references used on every invocation in the skill file. A separate file costs another read each time.
- Limit the files in each phase, set turn budgets, and account for mechanism costs.
