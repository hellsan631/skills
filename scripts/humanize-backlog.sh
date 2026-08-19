#!/usr/bin/env bash
# Shows what an imported skill still owes the checker. scripts/test.sh gates imported
# skills on errors alone; this prints the review-level findings a skill has to clear
# before it can be gated like prose we wrote.
#
#   scripts/humanize-backlog.sh                 every imported skill
#   scripts/humanize-backlog.sh codebase-design one of them
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECKER="$REPO/skills/writing/humanize/scripts/humanize_lint.py"
export PYTHONDONTWRITEBYTECODE=1

paths="$(python3 -c "
import json, sys
manifest = json.load(open(sys.argv[1]))
wanted = sys.argv[2] if len(sys.argv) > 2 else ''
for skill in manifest['skills']:
    path = skill['path']
    if not wanted or path.rsplit('/', 1)[-1] == wanted:
        print(sys.argv[1].rsplit('/', 1)[0] + '/' + path)
" "$REPO/imports.json" "${1:-}")"

if [ -z "$paths" ]; then
  echo "no imported skill named ${1:-}" >&2
  exit 1
fi

docs="$(printf '%s\n' "$paths" | while IFS= read -r dir; do
  find "$dir" -name '*.md' -not -path '*/tests/*'
done)"

printf '%s\n' "$docs" | tr '\n' '\0' | xargs -0 python3 "$CHECKER" --strict --all || true

cat <<'EOF'

Clearing these is how a skill graduates. Once it passes --strict, move its entry from
the imported list to the strict list by giving it a "humanized": true flag in
imports.json, and scripts/test.sh will hold it to the same bar as everything else.
EOF
