# Operating the checker

A normal run needs none of this. Come here when a finding looks wrong, or when the checker missed a tell.

## Suppressing a false positive

Quoted material, blockquotes, code, and URLs are exempt already. So is YAML frontmatter, but only from the rhythm rules that count words: a skill description is a list of triggers, and length is not a fault in one. The slop patterns still apply to it. HTML comments are exempt from the prose rules only: the artifact categories (leaked citation markup, placeholders, chatbot phrases) look inside them, because comments are where chatbots leave their notes. For anything else, put a directive in the source text.

```
<!-- humanize-lint: ignore -->                    skips the next line
<!-- humanize-lint: ignore puffery -->            skips one category on the next line
<!-- humanize-lint: off -->                       starts an exempt region
<!-- humanize-lint: on -->                        ends it
<!-- humanize-lint: ignore-file ai-vocabulary --> skips one category in this file
```

Reach for these rarely. A directive on prose you wrote yourself usually means the prose is wrong rather than the rule. A directive earns its place on quoted source text, on a proper noun that collides with a banned word, and on a placeholder an author put there on purpose.

`ignore-file` covers the case a line directive handles badly: a document that defines a term the corpus happens to ban, and then uses it correctly throughout. A glossary of deep module vocabulary repeats `leverage` because that is the name of the concept, and marking every occurrence would bury the file in directives. Name the one category and nothing else relaxes; `ignore-file` with no category suppresses nothing, since a master switch for a whole file is just an argument for leaving the file out of the run.

The density rules have one more legitimate exemption. They assume structure has crowded out explanation, which is true of a plan that decayed into bullets and false of a checklist, where a flat list of peer criteria is the shape the content wants. Turn `list-density` and `inline-header-density` off for a document that is genuinely a checklist, and leave them on everywhere else.

## Adding a rule

The phrase corpus and the profile definitions live in `rules/patterns.json`, which sits beside `SKILL.md` and stays out of context on purpose. A profile entry maps a category to a severity or to `off`, so retuning strictness is a one-line change rather than a code edit.

A category carries an id, a severity, a scan mode, one line of guidance, and its patterns. Three scan modes exist: `prose` sees text with code, comments, quotes, and URLs masked out; `prose+comments` is the same but sees inside HTML comments; `raw` sees everything. Patterns are Python regex, case-insensitive by default. A bare string inherits the category severity, while an object with `re` can override severity for one pattern. Name a group `hit` to report a narrower span than the whole match.

Write the pattern into `rules/patterns.json`, add a line that trips it to `tests/fixtures/dirty.md`, list the category in `EXPECTED_IN_DIRTY`, then run the suite from this skill's directory:

```bash
python3 tests/run_tests.py
```

The suite fails on missed tells and on false positives against `tests/fixtures/clean.md`. A rule that fires on clean prose is worse than no rule, because it teaches the agent to skim the output.

When a new rule trips the clean fixture, tighten the pattern rather than editing the fixture. A rule that needs the fixture relaxed to pass is a rule that will misfire on real prose.

## Choosing a severity

A rule with an irreducible false positive rate belongs at `note`, where it stays visible without blocking. Passive voice, weak adverbs, and em dashes sit there because each has legitimate uses that no regex can separate from the bad ones. Reserve `error` for patterns that are wrong every time they appear.

Vocabulary corpora go stale. The words a model overuses shift with each generation, so a corpus that was exhaustive two years ago will both under- and over-fire today. Some entries stop being tells as models get tuned away from them, and new ones appear as new models ship. Re-check the corpus periodically against fresh examples of AI-generated prose rather than assuming it is still current. `ai-vocabulary` already treats this as clustering rather than as a blacklist: one instance is noise, and a run of several in one document is the tell, because that framing survives the underlying words changing under it.

Some constructions are too common in ordinary writing to regex at `error` even though they show up disproportionately in AI prose. "X rather than Y" is the clearest case: it is completely ordinary technical phrasing most of the time, and it only reads as a tell in a document already showing other signs. Question 12 in `judgment-pass.md` covers it, along with the cross-sentence "however" pivot. Neither joins `patterns.json` or the density markers, because this repo's own clean prose uses "rather than" several times per document. A rule that fires on correct writing teaches the agent to skim the output. That is worse than missing the pattern.

Negative parallelism gets a three-tier treatment for the same reason. The unambiguous forms are flat rules in `patterns.json`: "not just X, but Y" with plain or contracted leads, "doesn't just X; it Y", the repeated-negation list ("not a X, not a Y, just Z"), the it's-not-about pivot, and (at `review`) "not a X but a Y". The softer forms are legitimate one at a time, so `NEGATIVE_PARALLEL_MARKER` in `humanize_lint.py` counts them instead of flagging them:

- the bare "X, not Y" at a clause or sentence end
- the negated copula linked by an em dash, semicolon, or comma
- the comma-but pivot: "is not grounded in X, but in Y"
- the cross-sentence pivot: "is not dissolution. Rather, ..." and "isn't X. It's Y."
- the fronted "More than a X, this is ..."
- the clipped tail: ", no refresh needed"
- the definitional negation: "that is not the goal", "casual is not the target"

A single instance of a counted shape usually survives the deletion test. "The map is an index, not a store" genuinely loses meaning if you cut the tail, and that is why these count instead of firing. `negative-parallelism-density` reports them two ways:

- **Spread thin across a long document.** The same scaffold, repeated five or ten times over many paragraphs, becomes a habit standing in for plain statement, the same failure `rule-of-three` and `em-dash-density` count, no matter what any one instance says alone. Fires past 4 total.
- **Packed into one short passage.** Two sentences in a row that both define the same thing by negation read as broken even when each would pass the deletion test alone. A whole-document count would dilute this in a longer file, so the check also counts per paragraph and fires past 2 in the same one.

Don't promote the counted shapes to flat `review` rules. That was tried for the bare-comma form, and it drowns the report in defensible-looking hits with no way to tell the habit from the one legitimate use. Count occurrences and let density carry the signal.
