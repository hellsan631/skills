---
name: brainstorm-skill-ideas
description: Use when the user asks for skill ideas drawn from a chat history, the current conversation, or past chats. Proposes up to five skills, each with the moment that suggests it, how it would help, and how to make it better.
disable-model-invocation: true
---

# Brainstorm Skill Ideas

Find the skills that would have saved the most time or rework in a chat history, and present at most five. A skill is a reusable SKILL.md an agent loads when a matching task comes up. It is worth having when it supplies knowledge, judgment, or steps the agent kept missing.

## Sources

Use the chat history the user pasted or pointed to. With no pointer, use the current conversation. When the user asks about recent or past chats, find them with [transcripts.md](transcripts.md), which covers where Cursor, Claude Code, and Codex store chats and how to pull out the user's messages. Read the user's messages first, since corrections and repeated explanations show up there, and open the agent's surrounding turns only for the moments you plan to cite.

Check ideas against the skills listed in your context.

## Finding ideas

Look for moments where the user corrected the agent, repeated an explanation, walked it through the same steps again, or spent several turns on a problem that will come back. Consider many ideas, then keep at most five: the ones that would save the most time or rework if they existed today.

If an existing skill could cover an idea with a small change, propose that change instead of a new skill.

## Output

For each idea:

- **Name**: lowercase-hyphenated.
- **What it does**: one sentence.
- **Why it's worth having**: the moment in the history that suggests it, briefly quoted.
- **How it would help**: what changes in a session that uses it.
- **How to make it better**: one or two concrete improvements, such as a bundled script, a checklist, or examples from the history.

The brainstorm is complete when every idea quotes a real moment from the history. Offer to build the one the user picks.
