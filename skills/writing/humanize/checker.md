# Operating the checker

Two branches beyond a normal run: a finding you believe is wrong, and a tell the checker
missed.

## Suppressing a false positive

Quoted material, blockquotes, code, and URLs are exempt already. So is YAML frontmatter,
but only from the rhythm rules that count words: a skill description is a list of triggers,
and length is not a fault in one. The slop patterns still apply to it. For anything else,
put a directive in the source text.

```
<!-- humanize-lint: ignore -->                    skips the next line
<!-- humanize-lint: ignore puffery -->            skips one category on the next line
<!-- humanize-lint: off -->                       starts an exempt region
<!-- humanize-lint: on -->                        ends it
<!-- humanize-lint: ignore-file ai-vocabulary --> skips one category in this file
```

Reach for these rarely. A directive on prose you wrote yourself usually means the prose
is wrong rather than the rule. A directive earns its place on quoted source text, on a
proper noun that collides with a banned word, and on a placeholder an author put there on
purpose.

`ignore-file` covers the case a line directive handles badly: a document that defines a
term the corpus happens to ban, and then uses it correctly throughout. A glossary of deep
module vocabulary repeats `leverage` because that is the name of the concept, and marking
every occurrence would bury the file in directives. Name the one category and nothing
else relaxes; `ignore-file` with no category suppresses nothing, since a master switch for
a whole file is just an argument for leaving the file out of the run.

The density rules have one more legitimate exemption. They assume structure has crowded
out explanation, which is true of a plan that decayed into bullets and false of a
checklist, where a flat list of peer criteria is the shape the content wants. Turn
`list-density` and `inline-header-density` off for a document that is genuinely a
checklist, and leave them on everywhere else.

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

Vocabulary corpora go stale. The words a model overuses shift with each generation of
models, so a phrase corpus that was exhaustive two years ago will both under- and
over-fire today: some entries stop being tells as models get tuned away from them,
new ones appear as new models ship. Re-check the corpus periodically against fresh
examples of AI-generated prose rather than assuming it is still current. `ai-vocabulary`
already treats this as a clustering problem, not a blacklist: one instance is noise, a
run of several in one document is the tell, because that is the only framing that
survives the underlying words changing under it.

Some constructions are too common in ordinary writing to regex at `error` even though
they show up disproportionately in AI prose. "X rather than Y" is the clearest case: it
is completely ordinary technical phrasing most of the time, and only reads as a tell in
a document already showing other signs. Patterns like this belong in `judgment-pass.md`
as something to notice when several other findings are already firing, not in
`patterns.json` as a standalone rule — a rule that fires on correct writing teaches the
agent to skim the output, which is worse than missing the pattern entirely.

The bare "X, not Y." shape (no "but," no em dash, just a comma and a short trailing
clause) and the semicolon-linked shape ("X; it's Y") are not in `patterns.json` as flat
rules, because a single instance almost always survives the deletion test — "the map is
an index, not a store" and "the answer isn't part of the body; it's recorded on
resolution" both genuinely lose meaning if you cut the tail. Judged sentence by sentence
either one looks fine every time. But the tic fails two different ways once you stop
judging sentence by sentence, and `negative-parallelism-density` in `humanize_lint.py`
catches both:

- **Spread thin across a long document.** The same scaffold five or ten times over
  many paragraphs, the `rule-of-three` / `em-dash-density` shape: a habit standing in
  for plain statement, whatever any one instance says alone. Fires past 4 total.
- **Packed into one short passage.** Two sentences in a row, both defining the same
  thing by what it isn't — "a role, not an identity. ... It is not a new persona
  ...; it's a hat ..." — reads as broken even though each half might individually pass
  the deletion test. A whole-document count would dilute this to nothing in a longer
  file, so this check also counts per paragraph and fires past 2 in the same one,
  independent of the document-wide total.

Don't try to turn either shape back into a flat `patterns.json` rule with a `review`
severity per line; that was tried for the bare-comma form, and it drowns the report in
defensible-looking hits with no way to tell the habit from the one legitimate use. Count
occurrences and let density carry the signal instead.
