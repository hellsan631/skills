# Writing

Skills for producing and editing prose.

**Model-invoked**

- **[unslop](./unslop/SKILL.md)**: the always-on reflex. Carries the shapes of the rules
  that are wrong every time, so they can be applied while writing without running
  anything. The only skill in this repo the agent reaches on its own.

**User-invoked**

- **[humanize](./humanize/SKILL.md)**: the audit. Strip AI tells from prose and verify the
  result with a deterministic checker rather than a from-memory checklist. Escalate here
  when the text lands in a file or someone will publish it.
- **[writing-for-agents](./writing-for-agents/SKILL.md)**: write documents an agent has to
  execute, covering context pointers, progressive disclosure, and the wording that decides
  whether material gets reached at all. The reference behind how this repo is written.

`unslop` and `humanize` split on cost. The reflex is free and unconditional, so it rides
along in every reply. The audit spends a tool call and a judgment pass, so it waits to be
asked. `scripts/check-unslop-coverage.py` keeps the reflex from drifting narrower than the
corpus it summarizes.
