# Working on this repo

Skills live in bucket folders under `skills/`: `writing/`, `design/`, `engineering/`, `workflow/`, and `principles/`. Add a bucket only when a new skill does not fit an existing one.

A skill is a directory holding `SKILL.md`, an `agents/openai.yaml` for Codex picker metadata, and whatever reference files, scripts, rules, and tests it owns. Everything a skill needs lives inside it, so a single directory copied anywhere still works.

Point at another skill by name, as `` `codebase-design` ``, and let the agent find it. Never write a `../other-skill/FILE.md` path, which holds only until someone installs that skill on its own. Say "work from" rather than "call the Skill tool with", because almost every skill here is user-invoked and so cannot be invoked by an agent at all; its `SKILL.md` is read instead.

## Adding a skill

1. Create `skills/<bucket>/<name>/SKILL.md` and `agents/openai.yaml`.
2. List it in `.claude-plugin/plugin.json` under `skills`.
3. Add it to the bucket's `README.md`, and to the top-level `README.md` if it changes what the bucket is for.
4. Run `scripts/link-skills.sh`, then `scripts/test.sh`.

A skill that ships an executable also ships `scripts/install-shim.sh` beside it, which puts the command on PATH given no arguments. `scripts/install.sh` finds and runs every such file, so it needs no per-skill knowledge.

## Importing a skill from elsewhere

`python3 scripts/imports.py add <source> <upstream-path> <dest-path>` copies a skill in, generates its picker metadata, and records where it came from in `imports.json`. Credit the author in [ATTRIBUTION.md](./ATTRIBUTION.md); both current sources are MIT, and a source that is not needs checking before anything is copied.

An imported skill is ours to edit. Nothing re-syncs it, so local changes are safe. `python3 scripts/imports.py diff` shows what the original author changed since we copied, which is how a good idea upstream gets adopted on purpose rather than merged in blind.

## Invocation

Every `SKILL.md` is user-invoked or model-invoked, and the two harnesses have to agree.

User-invoked is the norm here, and means `disable-model-invocation: true` in the frontmatter plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.

Model-invoked means omitting `disable-model-invocation`.

Every description is written as triggers, in both modes: name the situations that should reach the skill, not the subject it covers. A user-invoked description is free, since nothing loads it until the skill runs. It still has two jobs: turn a list of skill names into an index the human can use, and tell the agent which situation it is in when the skill fires. `SKILL-MECHANICS.md` in `writing-for-agents` has the full argument.

A model-invoked description is permanent context load in every session, which is the whole cost of the mode, so the bar is that the agent would be wrong not to reach the skill on its own. Exactly one skill clears it today: `unslop`, because prose quality applies to every reply whether or not anyone asks.

Needing another skill's material is not a reason to make it model-invoked. Read its `SKILL.md` instead.

## Writing

Documents here are written for agents to execute, not for people to admire. The [writing-for-agents](./skills/writing/writing-for-agents/SKILL.md) skill is the reference. The levers that matter most: push branch-gated material behind a pointer so the main file stays legible, end every step on a criterion the agent can check, and state the target behaviour rather than banning its opposite.

Prose here is functional, not decorative. A skill sits in the agent's context while it works, so the skill's own writing is a sample the agent imitates, and a sloppy one leaks into replies that have nothing to do with the skill. That is why the bar applies to skills we will never publish.

Prose in this repo passes its own checker, on two tiers. Anything we wrote is gated on errors and reviews alike. An imported skill is gated on errors only, because it arrived written to someone else's bar, and its review-level findings sit in a backlog that `scripts/humanize-backlog.sh` prints. Clear them and add `"humanized": true` to the skill's entry in `imports.json`; `scripts/test.sh` then holds it to the same bar as everything else.

Install commands live in `README.md` and nowhere else. A second copy drifts.
