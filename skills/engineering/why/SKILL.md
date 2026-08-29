---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and searches each evidence category (source control, issue tracker, long-form docs, real-time chat, infrastructure observability, error tracking, product analytics warehouse) in parallel, then returns a cited account of decisions and tradeoffs. Use how for runtime behavior."
disable-model-invocation: true
---

# Why

Investigate the motivation and intent behind code. Why was it built this way? What edge cases were considered? What product, business, or operational constraints shaped the design? What alternatives were rejected, and why?

Companion to the `how` skill. `how` answers what the code does and how it works. `why` answers what forces led to its shape.

## How this skill works

Historical context may live in seven evidence categories: source control history, issue or ticket tracking, long-form documents, real-time team chat, infrastructure observability, error or exception tracking, and product analytics warehouses. The question alone cannot tell you which category holds the answer. At run time, list the available MCPs, map each to a category, search all seven categories in parallel, and synthesize the results with explicit confidence calibration. Treat null results as evidence about how the decision was made and report them alongside positive findings. Search every available category by default.

## Operating posture

Check each claim against the record and state its confidence precisely. Treat the available evidence as fragments of a historical record. When the record is thin, say so.

Collect the evidence before writing a narrative. Follow what the records support instead of selecting evidence for a story you have already chosen.

Prefer an exact quote and citation to a smooth paraphrase. A reader should be able to follow any claim back to its source and verify it in under a minute.

Treat the evidence you find as a sample of a larger, partly inaccessible record. Before concluding, identify what you would expect to find if an alternative explanation were true and whether you searched for it.

Document every gap, including cold threads, unsearchable sources, and unanswered questions. Do not replace a gap with an authoritative-sounding guess.

Use "appears to", "likely", or "suggests" when evidence is indirect. The synthesizer must preserve language that matches the confidence level.

Read code to establish what it does. Do not infer intent from its shape; code rarely records why it exists.

## Core epistemics

Historical evidence is fragmented. Tickets go stale, chat threads get deleted, and commit messages can be wrong. People change their minds between a PR description and its implementation, and the original author may have left the company.

Distinguish what the record states from what you infer. Show the evidence and mark its confidence. Leave the judgment to the user.

Cite every claim about intent with a specific commit hash, PR number, ticket ID, doc URL, chat permalink, or code comment. Label any claim without such a citation as inference.

Use "appears to" in place of "because" when evidence is indirect. Reserve confident language for direct, explicit evidence.

Show both accounts when sources contradict each other. Do not quietly select the one that fits your narrative.

If none of the searched sources answers a question, say, "we couldn't find out why." Do not substitute a confident guess.

When the evidence supports several explanations, present each one with its supporting evidence and let the user triangulate.

Code that makes sense today may have been written for reasons that no longer apply, or for no good reason. Do not retrofit intent.

Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the target and the question

Parse what the user is asking. The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** usually falls into one of these forms:

- "Why was X designed this way?" Design rationale.
- "Why do we do X instead of Y?" Tradeoff or alternatives.
- "What edge cases motivated this?" Defensive reasoning.
- "What business or product constraint led to this?" External forcing function.
- "Why does this code still exist?" Existing or dead code.
- "What's the history of X?" Broad history.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from conversation context (open files, recent edits, cursor location, what was just discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the code anchor

Before spawning investigators, anchor the investigation in concrete code. You need:

- The relevant file path(s) and line range(s)
- The key symbols (function names, class names, constants)
- An initial list of the last few commits touching the target
- PR numbers from merge commits (pattern `(#1234)` in the subject line)

Build the anchor in the lead agent and give the same information to every investigator.

```bash
# Blame target lines for last-touch commits
git blame -L <start>,<end> <file>

# Full file history, with patches, through renames
git log --follow -p -- <file>

# Last N commits touching the file, PR numbers visible
git log --oneline -20 -- <file>

# Extract PR numbers from a commit message
git log -1 --format=%B <commit>
```

Pull PR bodies and discussion via `gh` for any substantive commits:

```bash
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

Capture the file paths, symbols, commits, PR numbers, and linked ticket IDs as seed context. Pass it to the investigators so they do not repeat this search.

## Step 3. Spawn parallel investigators

Search every available evidence category in parallel by default. Each category lives in a different kind of system, and the question alone cannot reveal which one holds the answer.

### Discovery

Before spawning investigators, list the available MCPs from the Cursor environment. Use the available-tools map when present. Otherwise inspect the `mcps/` directory Cursor exposes for enabled MCP servers.

Map each available MCP to one evidence category:

1. Source control history
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics warehouse

Source control is always available through git and `gh`. For the other six, classify using the MCP name, server instructions, tool names, and resource descriptors. If an MCP could fit more than one category, choose the one matching its primary evidence. Record ambiguous cases in the coverage map.

Build a complete **coverage map**. A null result from an issue tracker is evidence that the decision was not ticketed. Run the search, then document any null result.

Launch all matching investigators in a single message so they run concurrently. Assign one category and one MCP to each investigator so it can specialize in that tool's query vocabulary and result shape.

Subagent config (each):
- `subagent_type`: `generalPurpose`
- `model`: your configured why-investigators model (default `grok-4.6-fast-xhigh`)
- `readonly`: `false` (agent mode). **Do not use readonly/Ask mode.** It strips MCP access and disables MCP-backed investigators. The source control investigator would be safe in readonly, but keep modes uniform. Agent mode permits writes; investigators must still leave files and external systems unchanged.

Each investigator gets:
1. The base prompt from `references/investigator-prompt.md`
2. The category playbook `references/sources/<source>.md` for the selected MCP, adapted from the examples in `references/source-playbook.md`
3. The cross-cutting `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
4. The code anchor from Step 2 (file paths, symbols, commit hashes, PR numbers, ticket IDs)
5. The user's original question

### Investigator roster

Spawn one investigator for each category that has a matching MCP. Each investigator owns exactly one tool or MCP.

The entries below name the records in each category, the rationale they can reveal, the expected results, and the grounds for reporting a gap or a rare skip. The categories overlap. Each can reveal evidence the others cannot recover.

#### 1. Source control investigator

Search Git history, `gh` PRs, code comments, and tests. Always spawn this investigator because source control is the only guaranteed source. It can find implementation-time rationale captured during review: PR descriptions that state the problem, review threads that debate alternatives, inline comments that record non-obvious constraints, test names that record motivating edge cases, and commit messages that link tickets or incidents. Give this evidence the most weight because it ties directly to the diff that shipped.

#### 2. Issue or ticket tracker investigator

Search ticket systems such as Linear, Jira, GitHub Issues, Plane, or Shortcut for tickets, project docs, status updates, and spec attachments. These records can reveal the product or business forcing function: customer requests such as "Acme needs X for their SOC2 audit," compliance deadlines, parent-initiative framing such as "Q3 enterprise readiness," ticket-level scope changes, and motivation labels such as `customer:*`, `incident-followup`, `compliance`, or `perf-regression`. This category is most useful when the motivation is external to engineering.

#### 3. Long-form documents investigator

Search systems such as Notion, Confluence, Google Docs, or Coda for PRDs, specs, RFCs, design docs, ADRs, postmortems, team pages, and meeting notes. These records can contain long-form design rationale: problem statements, explicit "alternatives considered" and "rejected approaches" sections, strategy documents that set priorities, ADRs with finalized decisions, and postmortem action items tied directly to code. This is where authors may record the reason before it becomes code.

#### 4. Real-time team chat investigator

Search systems such as Slack, Discord, Microsoft Teams, or Mattermost by feature name, symbol, PR URL, incident channel (`#sev-*`, `#incident-*`), and author activity around the ship date. Chat can reveal real-time deliberation that never reached a document: decisions made during incidents, questions and answers between the PR author and reviewers, casual "we decided X because Y" threads, and rationale for small changes that did not warrant a PRD. This category matters most when source control, tickets, and long-form documents provide little evidence.

#### 5. Infrastructure observability investigator

Search systems such as Datadog, New Relic, Honeycomb, Grafana, or Splunk for metrics, monitors, dashboards, logs, APM traces, and formal incidents. This infrastructure and runtime evidence can include monitor thresholds that match code constants, metric spikes just before a PR merge, dashboards created as postmortem action items, and incident timelines that reference the target. It is most useful when the target reacts to an infrastructure signal such as a timeout, retry, rate limit, or circuit breaker.

#### 6. Error or exception tracking investigator

Search systems such as Sentry, Rollbar, Bugsnag, or Airbrake for issues, events, stack traces, and releases. These records can reveal the exceptions and error trajectories that motivated defensive or corrective code. Look for stack traces through the target function, first-seen and last-seen windows that bracket the PR ship date, and release correlations that show an error stopping at a specific version. This category is most useful for catch blocks, null guards, type checks, retries, and other defenses.

#### 7. Product analytics warehouse investigator

Search systems such as Databricks, Snowflake, BigQuery, ClickHouse, dbt, or Redshift for product-analytics events, experiment and feature-flag exposure tables, usage and billing events, query history, and warehouse telemetry. This product and data view complements infrastructure observability by covering user behavior and data around the ship date. Look for feature-usage trajectories. A step-function ramp from zero is strong evidence that the PR launched a feature. Also search experiment or flag exposure data tied to ship decisions, and pre-ship distributions that reveal where a threshold constant came from. For example, `limit = 128 * 1024` may match the p99 of an upload-size column. Check data-pipeline scale evidence for migrations or backfills. This category is most useful for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from" questions.

### When to skip an investigator

Skip only with an **explicit, written justification** in the final "Sources Consulted" section. Two reasons qualify:

- **No MCP is available for that category** in this environment. Report the missing MCP as a gap. Example: "Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable."
- **You can prove the source is irrelevant.** Apply a high bar. Example: "Error / exception tracking skipped. Target is a build-time script with no runtime code path." A probability judgment such as "probably not in error tracking, it's a feature not an error" does not qualify.

Statements such as "It's pure feature code, error tracking won't have anything" and "I doubt long-form docs would have this" do not justify a skip. Run the search and report a null result. An empty search costs one investigator; a missed design document can produce a wrong answer.

If your scope assessment finds a trivial, single-commit target whose PR description contains the complete answer, you may answer inline **only after** confirming that all seven available category searches would be redundant. State that confirmation explicitly. This should be rare.

## Step 4. Synthesize

Spawn one synthesizer subagent:

- `subagent_type`: `generalPurpose`
- `model`: your configured why-synthesizer model (default `claude-fable-5-thinking-max`)
- `readonly`: `false` (agent mode). The synthesizer's quality check spot-verifies citations and may require MCP access. Readonly/Ask mode strips that access.

The synthesizer gets:
1. The investigator findings, including any null results and any categories skipped with justification
2. The code anchor from Step 2 (file paths, symbols, commit hashes, PR numbers, ticket IDs)
3. The user's original question
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

Its output must be a confidence-weighted, evidence-cited account with separate "what we know" and "what we're inferring" sections, plus the gaps and null-result sources.

## Step 5. Present

Present the synthesizer's output to the user. You may make small clarity edits or add context from the conversation. **Preserve the confidence language and every hedge.** Removing a hedge can turn an inference into an unsupported assertion.

## Output format

The final output uses this structure. Adapt it while preserving the confidence separation.

**The Question**. Restate what the user asked, concisely.

**The Code in Question**. Give the file paths, line ranges, and key symbols in one or two lines.

**What We Found (direct evidence)**. Include only claims backed by text and give each an explicit citation (PR #, ticket ID, doc URL, chat permalink, commit hash, or code comment with file:line). Use present tense and quote or paraphrase the source.

**What We Can Reasonably Infer**. Put claims here when no source states them explicitly but indirect evidence or combined signals support them well. For each bullet, explain the inference chain: "Given A and B, it's likely that C." Use hedged language ("appears to", "likely", "suggests").

**Competing Hypotheses**. If the evidence fits multiple stories, list them. For each, give the hypothesis, the evidence for it, and the evidence against it. Don't force a winner when the record doesn't support one. (Skip this section if there's a clear answer.)

**What We Don't Know**. Name the gaps, unanswered questions, and searches that returned no results. Include the exact query and missing answer, for example: "We searched the issue tracker for 'rate limit' and found no ticket discussing this specific threshold."

**Sources Consulted**. One line per investigator, including the ones that returned nothing. Show which MCPs the investigators queried, which searches returned empty, and which categories they skipped and why. This coverage map lets the user judge breadth and redirect if the search missed an expected source.

Format each line as: `- <Source>: <what was searched>. <what was found, or "no relevant results," or "skipped. reason">.`

Example:
- Source control (git/gh): `git log --follow backend/retry.ts`, PRs #49074, #47812. Found PR #49074 introduced exponential backoff and linked ENG-4421.
- Issue tracker (Linear): searched for "retry" and ENG-4421. Found ENG-4421 parent issue but no discussion of backoff parameters.
- Long-form docs (Notion): searched for "retry policy," "backend retries," "ENG-4421." No relevant results.
- Real-time team chat (Slack): skipped. No matching MCP available in this environment. Gap: conversational record not searched.
- Infrastructure observability (Datadog): searched for `retry_count` metric and monitors around 2024-08-14. Found monitor "Upstream 5xx rate > 1%" created same day as PR #49074.
- Error / exception tracking (Sentry): searched for issues first-seen in Aug 2024 with stack through `retry.ts`. Found issue SENTRY-3821 spiking in the week before the PR.
- Product analytics warehouse (Databricks): queried `<your_analytics_db>.<schema>.stg_backend_upstream_retry` for the 30-day window around 2024-08-14. Daily failure-classified event count fell from ~1.2k/day pre-PR to <50/day post-PR. Also checked `system.query.history` for relevant migration queries. None found.

After the Sources Consulted block, if the user's `why` question is a precursor to changing this code, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set suitable for planning the change.

## Common failure modes

- **Confident storytelling**. A plausible narrative built from thin evidence. A bullet with no citation goes in "inferred" or "hypotheses," not "what we found."
- **Citing the code as evidence for its own intent**. "Handles the null case because it checks for null" is mechanics, not motivation. Motivation comes from an external source (PR discussion, ticket, comment, conversation); otherwise, label the claim as inference.
- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.
- **Sycophantic agreement**. If the user suggests a reason ("I assume this is for performance?"), treat it as a hypothesis and check the evidence independently, don't just confirm it.
- **Skipping the gaps section**. List what the searches did not answer.
- **Skipping investigators by anticipation**. Search all seven available categories, even when you expect "long-form docs probably don't have this" or "this isn't an error tracking thing." A null result records an empty search; skipping leaves that category unexamined.
- **Collapsing investigators into one agent**. Each MCP has its own query vocabulary, result shape, and pitfalls; pooling them dilutes specialization and makes coverage harder to reason about. Always one investigator per category.

## Reference files

- `references/epistemics.md`. Confidence tiers and phrasing guide. The synthesizer must follow it.
- `references/investigator-prompt.md`. Base prompt template for investigator subagents.
- `references/source-playbook.md`. Index pointing at the category playbooks below.
- `references/sources/*.md`. One self-contained example playbook per category, plus cross-cutting `incident-postmortem.md`. Give an investigator the single file that matches its category and adapt it to the available MCP.
- `references/synthesizer-prompt.md`. Prompt template for the synthesizer subagent, including the output format.
