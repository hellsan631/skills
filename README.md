# Desloped Skills

This repo contains a bunch of skills that originated elsewhere, but I've gone through the process of (mostly) de-ai-ifying their content. This is to hopefully avoid poisoning our context with slop writing that existed in bulk in the previous repos. Maybe this makes a difference in long context windows, maybe not.

## Install

<details> <summary><strong>Any agent (Cursor, Claude Code, Codex)</strong></summary>

```bash
curl -fsSL https://raw.githubusercontent.com/hellsan631/skills/main/scripts/install.sh | bash
```

Clones to `~/.local/share/agent-skills`, symlinks every skill into `~/.cursor/skills`, `~/.claude/skills`, and `~/.agents/skills`, then puts the `humanize-lint` command on your PATH. Re-run it to update, or `git pull` in the clone, since the installs are symlinks.

</details>

<details> <summary><strong>Claude Code plugin</strong></summary>

```
/plugin marketplace add hellsan631/skills
/plugin install hellsan631-skills@hellsan631
```

Installs a managed, read-only bundle. Run `scripts/install-shim.sh` from the installed humanize directory once so `humanize-lint` resolves.

</details>

<details> <summary><strong>Editable copy in one project</strong></summary>

```bash
npx skills@latest add hellsan631/skills
```

Copies the skills into your repo as ordinary files you own and can edit. Afterward, run `skills/writing/humanize/scripts/install-shim.sh` once.

</details>

## What is in here

`unslop` and `writing-for-agents` are the only skills here that are auto-invoked by the model. This is to improve the writing quality of the normal chat, or when you create more skills. The rest are ment to be used whenever you choose.

Below are the groupings for each of the skills.

- **[writing](./skills/writing/README.md)**: Skills ment to help desloping AI output.
- **[design](./skills/design/README.md)**: Pricipal-level personas for various domain-specific work.
- **[engineering](./skills/engineering/README.md)**: Useful engineering skills, hopefully with no overlap in effect.
- **[workflow](./skills/workflow/README.md)**: Just pure "workflow" helper skills, like grilling, and "show me your work".
- **[principles](./skills/principles/README.md)**: ten single-conviction skills that other
  skills cite by name as a test to apply.

I am releasing this code under the MIT License; see LICENSE for full text. See also ATTRIBUTION.md for all imported skills and their authors.
