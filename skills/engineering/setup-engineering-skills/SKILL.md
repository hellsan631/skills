---
name: setup-engineering-skills
description: "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills."
disable-model-invocation: true
---

# Setup Matt Pocock's skills

Create the per-repo configuration that the engineering skills expect:

- **Issue tracker**: where work items live. GitHub is the default, and local Markdown is also supported.
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This skill uses prompts rather than a deterministic script. Explore the repo, present what you found, confirm it with the user, and then write.

## Process

### 1. Explore

Inspect the current repo and read what exists before drawing conclusions:

- Run `git remote -v` and read `.git/config` to determine whether this is a GitHub repo and which repo it is.
- Check `AGENTS.md` and `CLAUDE.md` at the repo root. Determine whether either exists and whether either already has an `## Agent skills` section.
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- Check `docs/agents/` for output from a previous run of this skill.
- Treat `.scratch/` as a sign that the repo already uses a local-Markdown issue tracker convention.
- Check whether `triage` is installed. Either a `triage` skill folder beside this one or `triage` in the available skills counts as installed. Run Section B only when it is installed.
- Check for monorepo signals: `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or populated `packages/*` directories with their own `src/`. These signals indicate a large multi-package repo. If none is present, classify the repo as single-context.

### 2. Present findings and ask

Summarise what is present and what is missing. Work through the sections in order, waiting for one answer before moving to the next.

Start each section with the recommended answer so the user can accept it in one word. Give a one-line explanation only when the choice branches. Skip Section B when `triage` is not installed. When the repo has no monorepo signals, skip Section C entirely and apply its single-context default without asking.

#### Section A: Issue tracker

> The issue tracker is where this repo's issues live. `to-tickets`, `triage`, and `to-spec` read from and write to it. They need its location so they know whether to call `gh issue create`, write a Markdown file under `.scratch/`, or follow another workflow you describe. Choose the place where you track work for this repo.

These skills default to GitHub. If a `git remote` points at GitHub, recommend GitHub. If a `git remote` points at either `gitlab.com` or a self-hosted GitLab host, recommend GitLab. Otherwise, or if the user prefers another option, offer:

- **GitHub.** Issues live in the repo's GitHub Issues and use the `gh` CLI.
- **GitLab.** Issues live in the repo's GitLab Issues and use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI.
- **Local Markdown.** Issues live as files under `.scratch/<feature>/` in this repo. This option suits solo projects and repos without a remote.
- **Other.** For Jira, Linear, or another tracker, ask the user to describe the workflow in one paragraph. Record it as freeform prose.

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates include a "PRs as a request surface" flag that defaults to **off**. Keep it off and do not ask about it. A user who wants external PRs in the triage queue can change the flag in the file later.

#### Section B: Triage label vocabulary

Skip this section entirely if `triage` is not installed. An uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, with each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. If the user answers **yes**, write them as-is. Collect overrides only if the user says no, usually because the tracker already uses other names such as `bug:triage` for `needs-triage`. The overrides let `triage` apply existing labels instead of creating duplicates.

#### Section C: Domain docs

Default to **single-context**, with one `CONTEXT.md` and `docs/adr/` at the repo root. When exploration finds no monorepo signals, write this layout without asking.

Offer **multi-context**, a root `CONTEXT-MAP.md` that points to per-context `CONTEXT.md` files, only when exploration found monorepo signals. Then confirm which layout the user wants.

### 3. Confirm and edit

Before writing, show the user a draft of:

- The `## Agent skills` block for the file selected under step 4, either `CLAUDE.md` or `AGENTS.md`
- The contents of `docs/agents/issue-tracker.md` and `docs/agents/domain.md`
- The contents of `docs/agents/triage-labels.md` when `triage` is installed

Let the user edit the draft before writing.

### 4. Write

#### Pick the file to edit

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create. Do not choose for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists, or vice versa. Always edit the file that already exists.

If the chosen file already has an `## Agent skills` block, update that block in place instead of appending a duplicate. Preserve user edits in the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the `### Triage labels` sub-block and write `docs/agents/triage-labels.md` only when `triage` is installed and Section B ran. Otherwise, omit both.

Use the seed templates in this skill folder to write the docs files:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping (only if `triage` is installed)
- [domain.md](./domain.md): domain doc consumer rules + layout

For an "other" issue tracker, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user that setup is complete and name the engineering skills that will now read these files. Tell them they can edit `docs/agents/*.md` directly later. Re-run this skill only to switch issue trackers or restart from scratch.
