# Working on this repo

Skills live in bucket folders under `skills/`: `writing/`, `design/`, `engineering/`,
`workflow/`, and `principles/`. Add a bucket when a new skill does not fit an existing
one, not before.

A skill is a directory holding `SKILL.md`, an `agents/openai.yaml` for Codex picker
metadata, and whatever reference files, scripts, rules, and tests it owns. Everything a
skill needs lives inside it, so a single directory copied anywhere still works. Reach
another skill's material by calling the Skill tool with its name, never by a
`../other-skill/FILE.md` path.

## Adding a skill

1. Create `skills/<bucket>/<name>/SKILL.md` and `agents/openai.yaml`.
2. List it in `.claude-plugin/plugin.json` under `skills`.
3. Add it to the bucket's `README.md`, and to the top-level `README.md` if it changes what
   the bucket is for.
4. Run `scripts/link-skills.sh`, then `scripts/test.sh`.

A skill that ships an executable also ships `scripts/install-shim.sh` beside it, which puts
the command on PATH given no arguments. `scripts/install.sh` finds and runs every such
file, so it needs no per-skill knowledge.

## Importing a skill from elsewhere

`python3 scripts/imports.py add <source> <upstream-path> <dest-path>` copies a skill in,
generates its picker metadata, and records where it came from in `imports.json`. Credit the
author in [ATTRIBUTION.md](./ATTRIBUTION.md); both current sources are MIT, and a source
that is not needs checking before anything is copied.

An imported skill is ours to edit. Nothing re-syncs it, so local changes are safe.
`python3 scripts/imports.py diff` shows what the original author changed since we copied,
which is how a good idea upstream gets adopted on purpose rather than merged in blind.

## Invocation

Every `SKILL.md` is user-invoked or model-invoked, and the two harnesses have to agree.

Model-invoked is the default: omit `disable-model-invocation`, and write a model-facing
`description` carrying the trigger branches so auto-invocation fires. User-invoked means
`disable-model-invocation: true` in the frontmatter plus
`policy.allow_implicit_invocation: false` in `agents/openai.yaml`, and the `description`
becomes a human-facing one-liner with trigger lists stripped.

Pick model-invoked only when the agent should reach the skill on its own, or another skill
must. A skill that only ever fires by hand should be user-invoked, because a description is
permanent context load.

## Writing

Documents here are written for agents to execute, not for people to admire. The
[writing-for-agents](./skills/writing/writing-for-agents/SKILL.md) skill is the reference.
The levers that matter most: push branch-gated material behind a pointer so the main file
stays legible, end every step on a criterion the agent can check, and state the target
behaviour rather than banning its opposite.

Prose in this repo passes its own checker, on two tiers. Anything we wrote is gated on
errors and reviews alike. An imported skill is gated on errors only, because it arrived
written to someone else's bar, and its review-level findings sit in a backlog that
`scripts/humanize-backlog.sh` prints. Clear them and add `"humanized": true` to the skill's
entry in `imports.json`; `scripts/test.sh` then holds it to the same bar as everything else.

Install commands live in `README.md` and nowhere else. A second copy drifts.
