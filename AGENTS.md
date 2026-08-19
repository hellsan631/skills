# Working on this repo

Skills live in bucket folders under `skills/`. Right now there is one bucket, `writing/`.
Add a bucket when a new skill does not fit an existing one, not before.

A skill is a directory holding `SKILL.md`, an `agents/openai.yaml` for Codex picker
metadata, and whatever reference files, scripts, rules, and tests it owns. Everything a
skill needs lives inside it, so a single directory copied anywhere still works. Reach
another skill's material by calling the Skill tool with its name, never by a
`../other-skill/FILE.md` path.

## Adding a skill

1. Create `skills/<bucket>/<name>/SKILL.md` and `agents/openai.yaml`.
2. List it in `.claude-plugin/plugin.json` under `skills`.
3. Add it to the top-level `README.md`, with the name linked to its `SKILL.md`.
4. Run `scripts/link-skills.sh`, then `scripts/test.sh`.

A skill that ships an executable also ships `scripts/install-shim.sh` beside it, which
puts the command on PATH given no arguments. `scripts/install.sh` finds and runs every
such file, so it needs no per-skill knowledge.

## Invocation

Every `SKILL.md` is user-invoked or model-invoked, and the two harnesses have to agree.

Model-invoked is the default: omit `disable-model-invocation`, and write a model-facing
`description` carrying the trigger branches so auto-invocation fires. User-invoked means
`disable-model-invocation: true` in the frontmatter plus
`policy.allow_implicit_invocation: false` in `agents/openai.yaml`, and the `description`
becomes a human-facing one-liner with trigger lists stripped.

Pick model-invoked only when the agent should reach the skill on its own, or another
skill must. A skill that only ever fires by hand should be user-invoked, because a
description is permanent context load.

## Writing

Documents here are written for agents to execute, not for people to admire. The
[writing-for-agents](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
skill is the reference. The levers that matter most: push branch-gated material behind a
pointer so the main file stays legible, end every step on a criterion the agent can check,
and state the target behaviour rather than banning its opposite.

Prose in this repo passes its own checker. `scripts/test.sh` lints every skill document
under the `reference` profile with `--strict`, so a rule you ship applies to you first.

Install commands live in `README.md` and nowhere else. A second copy drifts.
