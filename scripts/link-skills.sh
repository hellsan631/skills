#!/usr/bin/env bash
# Symlinks every skill in this repo into the local skill directory of each agent
# harness, so `git pull` is all it takes to update an installed skill.
#
#   ~/.cursor/skills   Cursor
#   ~/.claude/skills   Claude Code
#   ~/.agents/skills   Codex and other Agent Skills harnesses
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DESTS=("$HOME/.cursor/skills" "$HOME/.claude/skills" "$HOME/.agents/skills")

names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/deprecated/*' -print0)

if [ ${#names[@]} -eq 0 ]; then
  echo "error: no SKILL.md found under $REPO/skills" >&2
  exit 1
fi

for DEST in "${DESTS[@]}"; do
  # A destination that is itself a symlink into this repo would make us write the
  # per-skill links back into our own tree. Bail rather than pollute the working copy.
  if [ -L "$DEST" ]; then
    resolved="$(cd "$DEST" 2>/dev/null && pwd -P || true)"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo ($resolved)." >&2
        echo "Remove it and re-run; this script will recreate it as a real directory." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    target="$DEST/${names[$i]}"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skipped ${names[$i]} in $DEST (a real directory is already there)" >&2
      continue
    fi
    ln -sfn "${srcs[$i]}" "$target"
    echo "linked ${names[$i]} -> ${srcs[$i]} ($DEST)"
  done

  # Renaming or deleting a skill leaves its old link behind pointing at nothing, and a
  # harness that reads the directory will keep offering a skill that no longer exists.
  for link in "$DEST"/*; do
    if [ -L "$link" ] && [ ! -e "$link" ]; then
      rm "$link"
      echo "pruned $(basename "$link") in $DEST (target is gone)"
    fi
  done
done
