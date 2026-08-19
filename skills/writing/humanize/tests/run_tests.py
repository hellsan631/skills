#!/usr/bin/env python3
"""Self-test for humanize_lint.py.

Guards two failure modes that would each make the checker useless: missing real
tells, and firing on clean prose until the agent learns to ignore it.

Run: python3 tests/run_tests.py
"""

import os
import sys
from typing import Dict, List

sys.dont_write_bytecode = True
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
# Works from the skill layout (../scripts) and from a flat vendored copy (..).
for candidate in ("..", os.path.join("..", "scripts")):
    sys.path.insert(0, os.path.join(TESTS_DIR, candidate))

import humanize_lint as lint  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

# Every category the dirty fixture is written to trigger. Missing one means either
# the fixture drifted or a rule stopped matching.
EXPECTED_IN_DIRTY = [
    "ai-vocabulary", "assistant-artifact", "bold-density", "challenges-formula",
    "citation-artifact", "conclusion-formula", "copula-avoidance",
    "didactic-disclaimer", "ecology-filler", "em-dash-density", "emoji",
    "gap-filling", "heading-case", "heading-level-skip", "hype-cliche",
    "inline-header-list", "meta-commentary", "negative-parallelism",
    "notability-performance", "placeholder-text", "puffery", "quote-consistency",
    "rule-of-three", "significance-bloat", "small-table", "subject-line",
    "superficial-analysis", "trailing-participle", "vague-attribution",
]

failures: List[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def profile_named(name: str) -> lint.Profile:
    profiles, _ = lint.load_profiles(lint.DEFAULT_RULES)
    return profiles[name]


def findings_for(name: str, target_format: str = "markdown",
                 profile: str = "reference") -> List[lint.Finding]:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    with open(os.path.join(FIXTURES, name), "r", encoding="utf-8") as handle:
        return lint.analyze(handle.read(), categories, target_format, profile_named(profile))


def by_category(findings: List[lint.Finding]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for finding in findings:
        counts[finding.category] = counts.get(finding.category, 0) + 1
    return counts


def test_dirty_fixture_triggers_every_category() -> None:
    counts = by_category(findings_for("dirty.md"))
    for category in EXPECTED_IN_DIRTY:
        check(category in counts, f"dirty.md did not trigger {category}")


def blocking(findings: List[lint.Finding]) -> List[lint.Finding]:
    """Notes are advisory by design, so only error and review count as false positives."""
    return [f for f in findings if f.severity != "note"]


def test_clean_fixture_is_silent() -> None:
    for finding in blocking(findings_for("clean.md")):
        failures.append(
            f"false positive in clean.md: {finding.category} at "
            f"{finding.line}:{finding.col} on {finding.excerpt!r}"
        )


def test_doc_profile_allows_house_style() -> None:
    """A plan may use bold-header lists and title case without being nagged per line."""
    relaxed = by_category(findings_for("outline.md", profile="doc"))
    for category in ("inline-header-list", "heading-case"):
        check(category not in relaxed, f"doc profile should silence {category}")
    strict = by_category(findings_for("outline.md", profile="reference"))
    check("inline-header-list" in strict,
          "reference profile should still flag bold-header lists")


def test_density_catches_documents_that_are_only_lists() -> None:
    """The per-line rule is off in doc profile, so density has to carry the signal."""
    relaxed = by_category(findings_for("outline.md", profile="doc"))
    check("list-density" in relaxed, "list-density missed an outline-shaped document")
    check("inline-header-density" in relaxed,
          "inline-header-density missed a document of wall-to-wall bold headers")
    for category in ("list-density", "inline-header-density"):
        check(relaxed.get(category, 0) == 1,
              f"{category} should report once per document, not per line")
    prose = by_category(findings_for("clean.md", profile="doc"))
    check("list-density" not in prose, "list-density fired on a prose document")


def test_profiles_never_relax_prose_rules() -> None:
    """Structure is a house-style choice. Puffery and filler are not."""
    categories = lint.load_categories(lint.DEFAULT_RULES)
    source = "The vibrant campus boasts a rich heritage and serves as a testament.\n"
    for name in ("doc", "reference"):
        found = {f.category for f in lint.analyze(source, categories, "markdown",
                                                  profile_named(name))}
        check("puffery" in found, f"{name} profile dropped a puffery rule")


TRIPLE_HEAVY = (
    "The archive holds letters, ledgers, and maps. The reading room has desks, lamps, "
    "and chairs. Staff catalog books, films, and photographs. Visitors bring notebooks, "
    "pencils, and cameras.\n"
)


def test_doc_profile_demotes_rather_than_deletes() -> None:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    strict = lint.analyze(TRIPLE_HEAVY, categories, "markdown", profile_named("reference"))
    check(any(f.category == "rule-of-three" and f.severity == "review" for f in strict),
          "reference profile should keep rule-of-three at review")
    relaxed = lint.analyze(TRIPLE_HEAVY, categories, "markdown", profile_named("doc"))
    check(any(f.category == "rule-of-three" for f in relaxed),
          "doc profile should keep rule-of-three visible, not delete it")
    check(all(f.severity == "note" for f in relaxed if f.category == "rule-of-three"),
          "doc profile should demote rule-of-three to note")


def test_notes_never_fail_a_run() -> None:
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
        handle.write(TRIPLE_HEAVY)
        path = handle.name
    try:
        check(run_cli_quietly([path, "--profile", "doc"]) == 0,
              "notes alone should not fail a run")
        check(run_cli_quietly([path, "--profile", "doc", "--strict"]) == 0,
              "notes alone should not fail even under --strict")
        check(run_cli_quietly([path, "--profile", "reference", "--strict"]) == 1,
              "the same text should fail under --strict in the reference profile")
    finally:
        os.unlink(path)


BORROWED_RULES = {
    "filler-phrase": "We shipped the parser in order to reduce startup cost.",
    "plain-word": "The team will utilize the new parser.",
    "abstract-metaphor": "The scheduler is the substrate for everything else.",
    "engineering-jargon": "The API surface area grew by nine endpoints.",
    "hedging": "This could potentially break the nightly build.",
    "sycophancy": "Great question. The parser runs before the loader.",
    "false-range": "It handles everything from parsing to rendering.",
    "long-sentence": (
        "The loader reads the manifest and then walks every declared module in order "
        "while checking the cache for a prior build result, and if it finds one that "
        "matches the content hash it skips compilation entirely, which is the main "
        "reason incremental builds finish so much faster than cold ones."
    ),
}


def test_borrowed_rules_all_fire() -> None:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    for category, sample in BORROWED_RULES.items():
        found = {f.category for f in lint.analyze(sample + "\n", categories, "markdown",
                                                  profile_named("reference"))}
        check(category in found, f"{category} did not fire on {sample!r}")


def test_bold_lead_in_colon_versus_period() -> None:
    """A colon label is the tell. A period lead-in followed by new detail is not."""
    categories = lint.load_categories(lint.DEFAULT_RULES)

    def categories_for(text: str) -> set:
        return {f.category for f in lint.analyze(text, categories, "markdown",
                                                 profile_named("reference"))}

    allowed = categories_for("- **Schema in TypeScript.** Tables live in one file.\n")
    check("inline-header-list" not in allowed and "redundant-label" not in allowed,
          "a bold lead-in ending in a period should not be flagged")

    tell = categories_for("- **Latency:** the p99 dropped to 40ms.\n")
    check("inline-header-list" in tell, "a bold colon label should be flagged")

    restates = categories_for("- **Performance:** Performance improved by 12 percent.\n")
    check("redundant-label" in restates,
          "a label that repeats a word from its own line should be flagged as redundant")


def test_redundant_label_survives_the_doc_profile() -> None:
    """doc turns off inline-header-list, but a label that says nothing is never fine."""
    categories = lint.load_categories(lint.DEFAULT_RULES)
    source = "- **Performance:** Performance improved by 12 percent.\n"
    found = {f.category for f in lint.analyze(source, categories, "markdown",
                                              profile_named("doc"))}
    check("inline-header-list" not in found, "doc profile should allow bold colon labels")
    check("redundant-label" in found, "doc profile should still reject a redundant label")


def test_arrows_read_as_notation_not_decoration() -> None:
    """Technical writing maps one thing to another with an arrow. That is not an emoji."""
    categories = lint.load_categories(lint.DEFAULT_RULES)

    def categories_for(text: str) -> set:
        return {f.category for f in lint.analyze(text, categories, "markdown",
                                                 profile_named("reference"))}

    for arrow in ("\u2192", "\u2190", "\u2194", "\u21d2"):
        found = categories_for(f"Send the state question {arrow} the logic branch.\n")
        check("emoji" not in found, f"{arrow!r} is notation and should not read as emoji")

    check("emoji" in categories_for("The release shipped \U0001f680 this morning.\n"),
          "a pictograph should still be flagged")
    check("emoji" in categories_for("The release shipped \u27a1\ufe0f this morning.\n"),
          "an arrow given emoji presentation should still be flagged")


def test_ignore_file_exempts_one_category_everywhere() -> None:
    """A term the document defines is vocabulary. Repeating it is correct, not a tell."""
    categories = lint.load_categories(lint.DEFAULT_RULES)
    source = (
        "<!-- humanize-lint: ignore-file ai-vocabulary -->\n"
        "# Depth and leverage\n\n"
        "Leverage is what callers get from depth. Leverage compounds across call sites,\n"
        "and leverage is why a deep module repays the cost of building it.\n\n"
        "The museum boasts four rooms.\n"
    )
    found = {f.category for f in lint.analyze(source, categories, "markdown",
                                              profile_named("reference"))}
    check("ai-vocabulary" not in found, "the named category should be exempt file-wide")
    check("puffery" in found, "ignore-file must not mute a category it did not name")


def test_bare_ignore_file_is_not_a_master_switch() -> None:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    source = "<!-- humanize-lint: ignore-file -->\nThe museum boasts four rooms.\n"
    found = {f.category for f in lint.analyze(source, categories, "markdown",
                                              profile_named("reference"))}
    check("puffery" in found, "ignore-file without a category should suppress nothing")


def test_unknown_profile_is_rejected() -> None:
    import contextlib
    import io

    with contextlib.redirect_stderr(io.StringIO()):
        code = lint.main([os.path.join(FIXTURES, "clean.md"), "--profile", "nonsense"])
    check(code == 2, "an unknown profile should exit 2 rather than silently defaulting")


def test_masking_and_directives() -> None:
    findings = blocking(findings_for("suppression.md"))
    check(
        len(findings) == 1,
        "suppression.md should yield exactly one finding, got "
        + repr([(f.category, f.line, f.excerpt) for f in findings]),
    )
    if findings:
        check(findings[0].category == "puffery",
              f"expected the deliberate puffery violation, got {findings[0].category}")


def test_abrupt_ending_only_when_unfinished() -> None:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    unfinished = lint.analyze("The budget grew because of\n", categories, "markdown")
    check(any(f.category == "abrupt-ending" for f in unfinished),
          "abrupt-ending missed a sentence that stops mid-thought")
    finished = lint.analyze("The budget grew by 12 percent.\n", categories, "markdown")
    check(not any(f.category == "abrupt-ending" for f in finished),
          "abrupt-ending fired on a completed sentence")


def test_markdown_bleed_is_format_scoped() -> None:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    source = "## Heading\n\nThe **archive** opened in 1801.\n"
    as_markdown = lint.analyze(source, categories, "markdown")
    check(not any(f.category == "markdown-bleed" for f in as_markdown),
          "markdown-bleed fired on a markdown target")
    as_plain = lint.analyze(source, categories, "plain")
    check(any(f.category == "markdown-bleed" for f in as_plain),
          "markdown-bleed missed markdown syntax in a plain-text target")


def test_subject_line_allowed_in_email() -> None:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    source = "Subject: Archive access\n\nThe reading room opens at nine.\n"
    check(any(f.category == "subject-line" for f in lint.analyze(source, categories, "markdown")),
          "subject-line missed a subject header on non-email text")
    check(not any(f.category == "subject-line" for f in lint.analyze(source, categories, "email")),
          "subject-line fired on an actual email")


def test_cluster_escalates_ai_vocabulary() -> None:
    categories = lint.load_categories(lint.DEFAULT_RULES)
    single = lint.analyze("The report is robust and well sourced.\n", categories, "markdown")
    vocab = [f for f in single if f.category == "ai-vocabulary"]
    check(all(f.severity == "review" for f in vocab),
          "a lone AI-vocabulary hit should stay at review severity")
    many = lint.analyze(
        "The robust and holistic approach will leverage synergy to foster growth "
        "and streamline the myriad of options.\n", categories, "markdown")
    vocab = [f for f in many if f.category == "ai-vocabulary"]
    check(len(vocab) >= 3 and all(f.severity == "error" for f in vocab),
          "an AI-vocabulary cluster should escalate every hit to error")


def run_cli_quietly(argv: List[str]) -> int:
    import contextlib
    import io

    with contextlib.redirect_stdout(io.StringIO()):
        return lint.main(argv)


def test_exit_code_reflects_severity() -> None:
    clean = os.path.join(FIXTURES, "clean.md")
    dirty = os.path.join(FIXTURES, "dirty.md")
    check(run_cli_quietly([clean]) == 0, "clean fixture should exit 0")
    check(run_cli_quietly([dirty]) == 1, "dirty fixture should exit 1")
    check(run_cli_quietly([clean, "--strict"]) == 0,
          "clean fixture should survive --strict")


def main() -> int:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    if failures:
        print(f"FAIL: {len(failures)} problem(s)\n")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"ok: {len(tests)} tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
