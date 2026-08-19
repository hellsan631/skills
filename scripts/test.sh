#!/usr/bin/env bash
# Runs every skill's test suite, then lints the repo's own prose with the humanize
# checker under the strictest profile. A skills repo that fails its own writing rules
# has no business shipping them.
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

CHECKER="$REPO/skills/writing/humanize/scripts/humanize_lint.py"

# Everything here is an internal operational document read by an agent, which is the doc
# profile's genre. It still enforces every prose rule; it only stops treating bold-header
# lists and title-case headings as faults, and those are the right shape for a checklist.
echo
echo "== prose =="
find "$REPO" -name '*.md' -not -path '*/.git/*' -not -path '*/tests/*' -print0 \
  | xargs -0 python3 "$CHECKER" --strict || failed=1

echo
if [ "$failed" -eq 0 ]; then
  echo "all checks passed"
else
  echo "checks failed" >&2
fi
exit "$failed"
