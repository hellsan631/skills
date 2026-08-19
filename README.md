# Agent skills that check their own work

Twenty-seven skills for writing, design, and engineering. The one that gives the repo its
name ships a deterministic checker: most writing skills hand the agent a checklist and
hope, while [humanize](./skills/writing/humanize/SKILL.md) makes it prove the prose is
clean rather than reread its own draft and declare victory.

## Install

Pick one route. Installing two leaves you with every skill twice.

<details>
<summary><strong>Any agent (Cursor, Claude Code, Codex)</strong></summary>

```bash
curl -fsSL https://raw.githubusercontent.com/hellsan631/skills/main/scripts/install.sh | bash
```

Clones to `~/.local/share/agent-skills`, symlinks every skill into `~/.cursor/skills`,
`~/.claude/skills`, and `~/.agents/skills`, then puts the `humanize-lint` command on your
PATH. Re-run it to update, or `git pull` in the clone, since the installs are symlinks.

</details>

<details>
<summary><strong>Claude Code plugin</strong></summary>

```
/plugin marketplace add hellsan631/skills
/plugin install hellsan631-skills@hellsan631
```

A managed, read-only bundle. Run `scripts/install-shim.sh` from the installed humanize
directory once so `humanize-lint` resolves.

</details>

<details>
<summary><strong>Editable copy in one project</strong></summary>

```bash
npx skills@latest add hellsan631/skills
```

Copies the skills into your repo as ordinary files you own and can edit. Nothing changes
behind your back. Afterward, run `skills/writing/humanize/scripts/install-shim.sh` once.

</details>

## What is in here

Skills split on who can invoke them. A **model-invoked** skill can be reached by you or by
the agent on its own, so it costs a permanently loaded description in exchange for firing
without being asked. A **user-invoked** skill is reachable only when you type its name,
which costs nothing to carry and nothing fires by accident. Eight of the twenty-seven are
model-invoked; the rest wait to be called.

Each bucket has its own README with the full list and what each skill is for.

- **[writing](./skills/writing/README.md)**: prose that reads as though a person wrote it,
  and documents an agent can execute.
- **[design](./skills/design/README.md)**: principal-game-designer.
- **[engineering](./skills/engineering/README.md)**: the deep-module vocabulary, domain
  modeling, prototyping, research, architecture review, blast radius.
- **[workflow](./skills/workflow/README.md)**: grilling and its documented variant, arena,
  wayfinder, decision logs.
- **[principles](./skills/principles/README.md)**: ten single-conviction skills that other
  skills cite by name as a test to apply.

Most of these began as work by [Matt Pocock](https://github.com/mattpocock/skills) and
[Lauren Tan](https://github.com/backnotprop/pstack), both MIT licensed. They are copies we
own and edit rather than pinned dependencies. [ATTRIBUTION.md](./ATTRIBUTION.md) credits
each one, and `imports.json` records the commit it came from so
`python3 scripts/imports.py diff` can show what changed upstream since, without
overwriting anything here.

## How humanize works

Prose fails in two directions. **Slop** is the mechanical tells, the puffery and filler and
borrowed significance that mark text as generated. **Sterile** is the over-correction:
every tell removed, nothing put back, which reads as machine-written just as loudly. The
checker catches slop. The skill's judgment pass catches sterile.

```bash
humanize-lint draft.md                        # internal docs, plans, specs
humanize-lint article.md --profile reference  # anything a stranger reads
```

Findings come back at three severities. An `error` is wrong every time it appears. A
`review` is context-dependent, so keep it only when you can say why. A `note` never fails a
run and collapses to one summary line, which is where rules with an irreducible false
positive rate live.

Two profiles decide structural strictness. `doc` allows bold-header lists and title-case
headings, because those are house style in most internal writing, while still catching a
document that has turned into nothing but an outline. `reference` applies every rule.
Neither profile relaxes a prose rule: puffery is wrong in a spec too.

The pattern corpus lives in
[`rules/patterns.json`](./skills/writing/humanize/rules/patterns.json), out of the agent's
context until the checker runs. That is the whole point of the design. The rules can grow
without the skill costing more to load.

## Working on this repo

```bash
scripts/test.sh              # skill test suites, then lint this repo's prose
scripts/humanize-backlog.sh  # what imported skills still owe the checker
scripts/link-skills.sh       # relink skills after adding or renaming one
```

The test suite fails on missed tells and on false positives against a hand-written clean
fixture. A rule that fires on good prose is worse than no rule, because it teaches the
agent to skim the output. Conventions for adding a skill are in [AGENTS.md](./AGENTS.md).

## License

Released under the MIT License. See [LICENSE](./LICENSE) for the full text, and
[ATTRIBUTION.md](./ATTRIBUTION.md) for the imported skills and their authors.
