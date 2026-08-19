#!/usr/bin/env bash
# Runs every skill's test suite, then lints this repo's prose with the humanize checker.
# A skills repo that fails its own writing rules has no business shipping them.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
failed=0

echo "== skill test suites =="
while IFS= read -r suite; do
  skill="$(basename "$(dirname "$(dirname "$suite")")")"
  printf '%-24s ' "$skill"
  if (cd "$(dirname "$(dirname "$suite")")" && python3 "$suite"); then :; else failed=1; fi
done < <(find "$REPO/skills" -path '*/tests/run_tests.py' | sort)

echo
echo "== cross-skill invariants =="
printf '%-24s ' "unslop coverage"
python3 "$REPO/scripts/check-unslop-coverage.py" || failed=1

CHECKER="$REPO/skills/writing/humanize/scripts/humanize_lint.py"

# Imported skills are ours to edit, but they arrived written to someone else's bar, so
# they are gated on errors while prose we wrote is gated on errors and reviews alike.
# A skill graduates to the strict list once it has had a humanize pass; see AGENTS.md.
IMPORTED="$(mktemp)"
trap 'rm -f "$IMPORTED"' EXIT
python3 -c "
import json, sys
manifest = json.load(open(sys.argv[1]))
for skill in manifest['skills']:
    if not skill.get('humanized'):
        print(sys.argv[2] + '/' + skill['path'] + '/')
" "$REPO/imports.json" "$REPO" > "$IMPORTED"

all_docs="$(find "$REPO" -name '*.md' -not -path '*/.git/*' -not -path '*/tests/*')"
first_party="$(printf '%s\n' "$all_docs" | grep -vFf "$IMPORTED" || true)"
imported="$(printf '%s\n' "$all_docs" | grep -Ff "$IMPORTED" || true)"

# Everything here is an internal operational document read by an agent, which is the doc
# profile's genre. It still enforces every prose rule; it only stops treating bold-header
# lists and title-case headings as faults, and those are the right shape for a checklist.
echo
echo "== prose we wrote (errors and reviews) =="
printf '%s\n' "$first_party" | tr '\n' '\0' | xargs -0 python3 "$CHECKER" --strict || failed=1

if [ -n "$imported" ]; then
  echo
  echo "== imported skills (errors only) =="
  # Printing every review and note here would bury the errors that actually gate the run,
  # which is the habit the checker exists to break. The backlog gets one line instead.
  if report="$(printf '%s\n' "$imported" | tr '\n' '\0' | xargs -0 python3 "$CHECKER" 2>&1)"; then
    printf '%s\n' "$imported" | tr '\n' '\0' \
      | xargs -0 python3 "$CHECKER" --json --all 2>/dev/null \
      | python3 -c "
import collections, json, sys
try:
    findings = json.load(sys.stdin)['findings']
except (ValueError, KeyError):
    sys.exit()
counts = collections.Counter(f['severity'] for f in findings)
print('no errors. humanize backlog: '
      f\"{counts['review']} review, {counts['note']} note\")
print('  see them with: scripts/humanize-backlog.sh')
"
  else
    printf '%s\n' "$report"
    failed=1
  fi
fi

echo
if [ "$failed" -eq 0 ]; then
  echo "all checks passed"
else
  echo "checks failed" >&2
fi
exit "$failed"
