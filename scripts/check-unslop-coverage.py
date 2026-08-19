#!/usr/bin/env python3
"""Assert the unslop reflex still covers every unconditional rule in the corpus.

unslop carries the shapes of humanize's error-severity categories so they can be applied
without running anything. Adding an error category to patterns.json without naming it in
unslop would leave the reflex quietly narrower than the audit, which is the kind of drift
nobody notices until the writing is already out.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULES = REPO / "skills/writing/humanize/rules/patterns.json"
REFLEX = REPO / "skills/writing/unslop/SKILL.md"


def error_entries():
    payload = json.loads(RULES.read_text())
    entries = payload.get("categories", payload)
    return [
        entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("severity") == "error" and "id" in entry
    ]


def phrasing_count(entries):
    """Patterns an error category can match, minus any the category demotes."""
    total = 0
    for entry in entries:
        for pattern in entry["patterns"]:
            demoted = isinstance(pattern, dict) and pattern.get("severity", "error") != "error"
            total += 0 if demoted else 1
    return total


def main():
    entries = error_entries()
    expected = {entry["id"] for entry in entries}
    text = REFLEX.read_text()
    missing = sorted(name for name in expected if f"`{name}`" not in text)

    if missing:
        print(f"{REFLEX.relative_to(REPO)} does not name these error categories:",
              file=sys.stderr)
        for name in missing:
            print(f"    {name}", file=sys.stderr)
        print("\nAdd each to the shape it belongs to, or demote it in patterns.json.",
              file=sys.stderr)
        return 1

    # unslop quotes this figure at the reader, so a silent drift makes the skill lie
    # about its own corpus in a document whose whole argument is to be specific.
    phrasings = phrasing_count(entries)
    if f"knows {phrasings} phrasings" not in text:
        print(f"{REFLEX.relative_to(REPO)} misstates the corpus size: "
              f"the error categories hold {phrasings} phrasings.", file=sys.stderr)
        return 1

    print(f"unslop covers all {len(expected)} unconditional categories "
          f"and quotes {phrasings} phrasings correctly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
