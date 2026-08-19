<!-- A bucket README is a catalog: every entry is a skill name, so every entry is a label. -->
<!-- humanize-lint: ignore-file inline-header-density -->

# Engineering

Skills for designing, changing, and de-risking code.

The four model-invoked ones supply vocabulary and legwork the agent should reach for
unprompted. The rest are heavier moves you start deliberately, because each one spends
real time or produces an artifact you then have to read.

**Model-invoked**

- **[codebase-design](./codebase-design/SKILL.md)**: the deep-module vocabulary. `module`,
  `interface`, `depth`, `seam`, `adapter`, `leverage`, `locality`, and the principles that
  connect them.
- **[domain-modeling](./domain-modeling/SKILL.md)**: build and sharpen the project's
  domain language, writing `CONTEXT.md` and ADRs as terms get settled.
- **[prototype](./prototype/SKILL.md)**: build a throwaway to answer one design question,
  either a state model you can click through or a set of UI variations.
- **[research](./research/SKILL.md)**: investigate a question against primary sources and
  leave the findings in the repo as Markdown.
- **[wizard](./wizard/SKILL.md)**: generate an interactive bash wizard for the steps only
  a human can do, such as provisioning infrastructure or clicking through a dashboard.

**User-invoked**

- **[blast-radius](./blast-radius/SKILL.md)**: find what a change could break outside its
  own diff, and prove the safety claim by running code rather than reasoning about it.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)**: scan for
  deepening opportunities, render them as a visual HTML report, then grill whichever one
  you pick.
- **[setup-matt-pocock-skills](./setup-matt-pocock-skills/SKILL.md)**: configure a repo's
  issue tracker, triage labels, and domain doc layout. Run it once before
  [wayfinder](../workflow/wayfinder/SKILL.md), which reads what it writes.
