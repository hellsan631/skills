---
name: how
description: "Use for \"how does X work\", subsystem architecture, runtime flow, onboarding mental models, code walkthroughs before changing something, architectural critique, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions. Explain the architecture for a senior engineer who is new to the subsystem. Give them a working mental model.

Two modes:

1. **Explain** (default). Explore the codebase, then explain what you find
2. **Critique.** Explain first, then spawn multiple models to independently identify architectural issues

## Explain mode

### Step 1. Understand the question and assess complexity

Parse what the user is asking about:

- "How does the rate limiter work?", a subsystem
- "How do we handle billing for on-demand usage?", a feature flow
- "How is the auth service structured?", an architectural overview
- "Walk me through what happens when a user submits a form", a runtime trace

Identify the scope. If it is ambiguous, state your best-guess interpretation before exploring. Do not ask for clarification. Let the user redirect you if your interpretation is wrong.

Assess complexity before choosing an approach:

- **Simple.** For a single module, small utility, or narrow question such as "how does function X work?", skip explorer agents and go to Step 2b. There, the explainer explores and explains in one pass.
- **Complex.** For a subsystem spanning multiple files or services, a cross-cutting feature, or a full architectural overview, go to Step 2a. Spawn parallel explorer agents first, then hand their findings to the explainer.

When in doubt, lean simple. You can always spawn explorers if the explainer hits a wall.

### Step 2a. Explore (complex questions only)

Decompose the question into 2-4 parallel exploration angles, each a distinct slice of the subsystem so explorers don't duplicate work. Example split for "how does the rate limiter work?":

- Explorer 1: data model and state management
- Explorer 2: request path and enforcement
- Explorer 3: configuration and metrics infrastructure

Choose the split based on the question. Use your judgment. Two explorers are enough for a narrow question; use up to four for a broad subsystem.

Spawn all explorers in a single message:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explorer model (default `grok-4.6-fast-xhigh`)
- `readonly`: `true`

Each explorer gets the same base prompt from `references/explorer-prompt.md` plus a specific exploration angle naming its slice. Each explorer should:
- Search broadly with Glob for relevant directories and Grep for key types, interfaces, and class names
- Start at an entry point and trace callers, callees, data flow, and type definitions
- Read the code itself. Do not infer behavior from file names
- Continue until it can describe the full path from input to output, or from trigger to effect, without skipping a step
- Record details that may surprise or mislead a newcomer

Each explorer returns the components found, flow traced, files read, and non-obvious details. Explorers may overlap; the explainer reconciles their reports.

Then proceed to Step 3.

### Step 2b. Direct explain (simple questions)

Spawn one Task subagent to explore and explain in one pass:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explainer model (default `claude-fable-5-thinking-max`)
- `readonly`: `true`

The agent explores with Glob, Grep, and Read, then writes the explanation. Read `references/explainer-prompt.md` for the communication style and output format. Use the same structure and omit explorer findings from its input.

Proceed to Step 4.

### Step 3. Synthesize (complex questions only)

Once all explorers return, spawn one Task subagent to combine their findings into one explanation:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explainer model (default `claude-fable-5-thinking-max`)
- `readonly`: `true`

Give the explainer every explorer's findings. Read `references/explainer-prompt.md` for the full prompt template and use the output format below. The explainer reconciles overlaps and contradictions before combining the slices.

### Step 4. Present

Present the explainer's output to the user. Keep its wording except for small clarity edits or context from the conversation.

### Output format

Adapt this structure to the question and include only the sections it requires.

**Overview.** In one or two paragraphs, explain what it is, what it does, and why it exists. Give the reader enough context to decide whether the rest is relevant.

**Key Concepts.** Briefly define only the types, services, or abstractions needed to understand the rest.

**How It Works.** Walk through the trigger, each step, the data flow, and the decision points. Use prose. Reference specific files and functions so the reader can inspect them, and include a code block only when a snippet is necessary.

**Where Things Live.** Briefly map only the files and directories needed to start working in this area.

**Gotchas.** Call out non-obvious details and surprising behavior that may trip up a newcomer. Include historical context that explains oddities and known sharp edges.

## Critique mode

Use this mode only when the user asks for architectural issues, problems, or improvements.

### Step 1. Explain first

Run the full explain flow above (Steps 1-4). You must understand the architecture before critiquing it.

### Step 2. Spawn critics

After the explanation is complete, spawn one architectural critic per model in your configured how-critics list (defaults `claude-fable-5-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, `claude-opus-5-thinking-xhigh`), all in a single message.

For each critic:
- `subagent_type`: `generalPurpose`
- `model`: one model from the configured how-critics list. These are minimum reasoning levels. The lead should escalate any model when the architecture warrants deeper analysis.
- `readonly`: `true`

Read `references/critic-prompt.md` for the prompt template. Each critic gets:
1. The explanation from Step 1 (so they don't re-explore)
2. The relevant file paths (so they can read the actual code)
3. The architectural critique rubric from `references/critique-rubric.md`

### Step 3. Lead judgment

Use the same framework as the `interrogate` skill. Judge each finding before categorizing it.

Categorize findings:
- **Act on.** Architectural problems worth fixing now
- **Consider.** Real concerns, but the cost/benefit is unclear
- **Noted.** Valid observations, low priority
- **Dismissed.** Wrong, missing context, or style preference

Present the Step 1 explanation first, then put the critique verdict below it. A reader who only wants to understand the system should be able to stop after the explanation.
