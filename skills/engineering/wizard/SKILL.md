---
name: wizard
description: Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Generates an interactive bash wizard for the steps only a human can do.
disable-model-invocation: true
---

# Wizard

A **wizard** is a bash script that guides a human through a manual procedure one step at a time. Use one for a procedure that is both tedious to perform by hand and tedious to explain to an AI every time. The script opens each URL, gives exact click-and-copy instructions, captures values, writes them where they belong in `.env` or GitHub secrets, asks for confirmation at every stage, and shows how many stages remain. It might configure third-party services, run a one-off migration, or move the project from one state to another.

Use [template.sh](template.sh) for stage-by-stage progress, confirmation gates, cross-platform URL opening including WSL, hidden secret entry, idempotent `.env` upserts, `gh secret` and `gh variable` writes, and the closing summary. Scope the procedure and author its stages. Keep the library above the `STAGES` marker identical in every wizard. Never edit it by hand.

By default, build a wizard for one run, save it to a scratch or `scripts/` path, and delete it after the run. Commit it only when the user wants a repeatable setup path in the repo.

## Process

### 1. Scope the procedure

List every manual step the human must take and every value the wizard must capture. Inspect the repo before asking the user:

- For setup, inspect `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework config, and `.github/workflows/*`. The wizard must produce a value for every `secrets.*` and `vars.*` reference.
- For a migration or transition, inspect the current state, the target state, and the irreversible actions between them.

Show the user the ordered list of stages and the values each one produces. Ask them to confirm the list and let them add, drop, or reorder stages.

**Done when:** every stage has a name and a position in the sequence. For each captured value, record:

- Where the human gets it
- Where the wizard writes it: `.env`, a GitHub secret, both, or nowhere. Some stages perform an action without capturing a value.
- Whether it is secret and needs hidden entry, or public

### 2. Map each stage's journey

For each stage, write the exact path a human follows. Include the URL to open, the actions to take, where the service shows a value, and which variable it fills. For example: "Dashboard → Developers → API keys → Reveal test key → copy". If you do not know the current UI or the exact command, say so and ask the user or check the docs. Never invent steps that may not exist.

**Done when:** every stage traces to concrete instructions a stranger could follow.

### 3. Author the wizard

Copy `template.sh` to the target path. Replace the example stage with one `stage` for each step, in dependency order. Use the library helpers: `stage`, `say`/`step`, `open_url`, `ask`/`ask_secret`, `write_env`, `set_secret`/`set_var`, and `pause`/`confirm`. Set `TOTAL_STAGES` to the number of stages you wrote.

Open the URL before asking for its value. Use `ask_secret` for every secret, `write_env` for every persisted value, `set_secret` only for values that CI needs, and `confirm` before every irreversible action. Each `stage` clears the screen so only the current step is visible. Keep each stage to one focused task so nothing the human needs scrolls away. Do not touch the library above the marker.

### 4. Verify and hand off

- `bash -n <script>`; run `shellcheck` if available.
- `chmod +x <script>`.
- Do not run it end to end yourself. It opens browsers and blocks on human input. Trace it statically: verify that the wizard captures every value from step 1 and writes it where step 1 specified, and that every `set_secret` name exactly matches a `secrets.*` reference in CI.
- Tell the user how to run it. If it's a repeatable setup path, commit it and link it from the README so the next person runs the script instead of asking an AI.
