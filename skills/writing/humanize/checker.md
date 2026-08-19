# Operating the checker

Two branches beyond a normal run: a finding you believe is wrong, and a tell the checker
missed.

## Suppressing a false positive

Quoted material, blockquotes, code, and URLs are exempt already. For anything else, put a
directive in the source text.

```
<!-- humanize-lint: ignore -->            skips the next line
<!-- humanize-lint: ignore puffery -->    skips one category on the next line
<!-- humanize-lint: off -->               starts an exempt region
<!-- humanize-lint: on -->                ends it
```

Reach for these rarely. A directive on prose you wrote yourself usually means the prose
is wrong rather than the rule. A directive earns its place on quoted source text, on a
proper noun that collides with a banned word, and on a placeholder an author put there on
purpose.

## Adding a rule

The phrase corpus and the profile definitions live in `rules/patterns.json`, which sits
beside `SKILL.md` and stays out of context on purpose. A profile entry maps a category to a severity or to `off`, so
retuning strictness is a one-line change rather than a code edit.

A category carries an id, a severity, a scan mode, one line of guidance, and its
patterns. Patterns are Python regex, case-insensitive by default. A bare string inherits
the category severity, while an object with `re` can override severity for one pattern.
Name a group `hit` to report a narrower span than the whole match.

Write the pattern into `rules/patterns.json`, add a line that trips it to
`tests/fixtures/dirty.md`, list the category in `EXPECTED_IN_DIRTY`, then run the suite
from this skill's directory:

```bash
python3 tests/run_tests.py
```

The suite fails on missed tells and on false positives against `tests/fixtures/clean.md`.
A rule that fires on clean prose is worse than no rule, because it teaches the agent to
skim the output.

When a new rule trips the clean fixture, tighten the pattern rather than editing the
fixture. A rule that needs the fixture relaxed to pass is a rule that will misfire on
real prose.

## Choosing a severity

A rule with an irreducible false positive rate belongs at `note`, where it stays visible
without blocking. Passive voice, weak adverbs, and em dashes sit there because each has
legitimate uses that no regex can separate from the bad ones. Reserve `error` for
patterns that are wrong every time they appear.
