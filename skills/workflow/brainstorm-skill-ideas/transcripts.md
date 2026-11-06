# Finding Past Chats

Each harness stores a chat as one JSONL file. Most lines are agent turns and tool output, so pulling the user's messages first shrinks a multi-megabyte transcript to a few hundred bytes. Use the section for the harness the user names, or the one you are running in.

## Cursor

Chats live in `~/.cursor/projects/<workspace-slug>/agent-transcripts/<uuid>/<uuid>.jsonl`. The slug for `/Users/me/github/app` is `Users-me-github-app`. Cursor also names this folder in your context.

```bash
jq -r 'select(.role=="user") | .message.content[] | select(.type=="text") | .text' <file>
```

## Claude Code

Chats live in `~/.claude/projects/<cwd-slug>/<session-uuid>.jsonl`. The slug for `/Users/me/github/app` is `-Users-me-github-app`. Claude Code stores tool results as user turns, so keep only text content:

```bash
jq -r 'select(.type=="user") | .message.content | if type=="string" then . else (.[] | select(.type=="text") | .text) end' <file>
```

## Codex

Chats live in `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl`, grouped by date. The first command prints the directory a chat ran in, for matching chats to a project. Codex stores injected context such as `<environment_context>` as user turns, so the second command keeps only text that opens with something other than `<`:

```bash
jq -r 'select(.type=="session_meta") | .payload.cwd' <file>
jq -r 'select(.type=="response_item" and .payload.type=="message" and .payload.role=="user") | .payload.content[] | select(.type=="input_text") | .text | select(startswith("<") | not)' <file>
```
