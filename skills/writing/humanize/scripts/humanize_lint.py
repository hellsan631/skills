#!/usr/bin/env python3
"""Check one or more text files for AI-writing tells with deterministic rules.

The checker loads phrase patterns from rules/patterns.json and also runs structural
checks that regular expressions cannot handle alone. Each finding includes its location,
severity, and a suggested fix.

Exit codes are 0 for a clean run, 1 for failing findings, and 2 for usage or I/O errors.
"""

import argparse
import bisect
import json
import os
import re
import statistics
import sys
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Pattern, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def resolve_default_rules() -> str:
    """Return the first existing rules path, or the standard skill path if none exists."""
    candidates = [
        os.path.join(os.path.dirname(SCRIPT_DIR), "rules", "patterns.json"),
        os.path.join(SCRIPT_DIR, "patterns.json"),
        os.path.join(SCRIPT_DIR, "rules", "patterns.json"),
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return candidates[0]


DEFAULT_RULES = resolve_default_rules()

PROSE_FORMATS = {"markdown", "md", "plain", "text", "wikitext", "email", "html"}
NON_MARKDOWN_FORMATS = {"plain", "text", "wikitext", "email"}

# Leave out the Arrows block (U+2190-U+21FF). Technical writing uses symbols such as
# "question → file", so treating the whole block as emoji would create false positives.
# U+FE0F still catches an arrow explicitly displayed as emoji.
EMOJI_RANGES = re.compile(
    "[\U0001f000-\U0001faff\u2300-\u23ff\u2600-\u27bf\ufe0f\u2b00-\u2bff]"
)

FILLER_PARTICIPLES = {
    "adding", "allowing", "blending", "cementing", "contributing", "creating",
    "cultivating", "demonstrating", "driving", "emphasizing", "enabling",
    "encompassing", "ensuring", "facilitating", "fostering", "helping",
    "highlighting", "making", "marking", "offering", "positioning",
    "promoting", "providing", "reflecting", "reinforcing", "representing",
    "serving", "shaping", "showcasing", "solidifying", "symbolizing",
    "underscoring", "confirming", "illustrating", "affirming", "evidencing",
    "embodying", "accentuating", "imparting",
}

HEADING_CASE_EXEMPT = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into",
    "nor", "of", "on", "or", "the", "to", "up", "via", "with",
}

# The note severity keeps low-priority rules visible without failing the run.
SEVERITY_ORDER = {"error": 0, "review": 1, "note": 2}
FAILING_SEVERITIES = ("error",)
STRICT_SEVERITIES = ("error", "review")


@dataclass
class Finding:
    line: int
    col: int
    severity: str
    category: str
    excerpt: str
    guidance: str
    path: str = ""


@dataclass
class CompiledPattern:
    regex: Pattern
    severity: str
    note: str = ""


@dataclass
class Category:
    id: str
    severity: str
    scan: str
    guidance: str
    patterns: List[CompiledPattern] = field(default_factory=list)
    cluster_threshold: int = 0
    cluster_severity: str = "error"
    skip_formats: Tuple[str, ...] = ()


# Rule loading


def compile_flags(spec: str) -> int:
    flags = re.IGNORECASE
    if "m" in spec:
        flags |= re.MULTILINE
    if "s" in spec:
        flags |= re.DOTALL
    if "c" in spec:
        flags &= ~re.IGNORECASE
    return flags


def compile_pattern(raw, default_severity: str) -> CompiledPattern:
    if isinstance(raw, str):
        return CompiledPattern(re.compile(raw, compile_flags("")), default_severity)
    regex = re.compile(raw["re"], compile_flags(raw.get("flags", "")))
    severity = raw.get("severity", default_severity)
    return CompiledPattern(regex, severity, raw.get("note", ""))


@dataclass
class Profile:
    id: str
    label: str
    detail: str
    overrides: Dict[str, str] = field(default_factory=dict)

    def resolve(self, category: str, severity: str) -> Optional[str]:
        """Return the effective severity, or None when this profile disables the category."""
        override = self.overrides.get(category)
        if override is None:
            return severity
        if override == "off":
            return None
        return override


def load_profiles(rules_path: str) -> Tuple[Dict[str, Profile], str]:
    with open(rules_path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    profiles = {
        name: Profile(name, spec.get("label", name), spec.get("detail", ""),
                      spec.get("overrides", {}))
        for name, spec in data.get("profiles", {}).items()
    }
    profiles.setdefault("reference", Profile("reference", "Strict", "", {}))
    return profiles, data.get("default_profile", "reference")


def apply_profile(findings: List[Finding], profile: Profile) -> List[Finding]:
    kept = []
    for finding in findings:
        severity = profile.resolve(finding.category, finding.severity)
        if severity is None:
            continue
        finding.severity = severity
        kept.append(finding)
    return kept


def load_categories(rules_path: str) -> List[Category]:
    with open(rules_path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    categories = []
    for entry in data["categories"]:
        cluster = entry.get("cluster") or {}
        category = Category(
            id=entry["id"],
            severity=entry.get("severity", "error"),
            scan=entry.get("scan", "prose"),
            guidance=entry.get("guidance", ""),
            cluster_threshold=int(cluster.get("threshold", 0)),
            cluster_severity=cluster.get("severity", "error"),
            skip_formats=tuple(entry.get("skip_formats", ())),
        )
        category.patterns = [
            compile_pattern(raw, category.severity) for raw in entry["patterns"]
        ]
        categories.append(category)
    return categories


# Utilities


def line_starts(text: str) -> List[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def position_of(starts: List[int], offset: int) -> Tuple[int, int]:
    line_index = bisect.bisect_right(starts, offset) - 1
    return line_index + 1, offset - starts[line_index] + 1


def blank_out(text: str, start: int, end: int) -> str:
    span = text[start:end]
    replacement = "".join("\n" if char == "\n" else " " for char in span)
    return text[:start] + replacement + text[end:]


# Keep a separate mask for HTML comments. The prose+comments mode needs to inspect them
# because chatbots often leave placeholders and messages to the requester inside
# <!-- --> blocks.
COMMENT_MASK = re.compile(r"<!--.*?-->", re.DOTALL)

CODE_MASKS_KEEP_COMMENTS = [
    re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.MULTILINE | re.DOTALL),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"https?://\S+"),
    re.compile(r"\]\([^)\n]+\)"),
]

CODE_MASKS = CODE_MASKS_KEEP_COMMENTS[:1] + [COMMENT_MASK] + CODE_MASKS_KEEP_COMMENTS[1:]

# Treat quoted text and worked examples as source material and skip them during scans.
# Otherwise, a document that names a banned phrase could fail its own rules.
QUOTE_MASKS = [
    re.compile(r"^[ \t]*>.*$", re.MULTILINE),
    re.compile(r"\"[^\"\n]{1,60}\""),
    re.compile(r"\u201c[^\u201d\n]{1,60}\u201d"),
]


def apply_masks(text: str, patterns: Iterable[Pattern]) -> str:
    masked = text
    for pattern in patterns:
        for match in list(pattern.finditer(masked)):
            masked = blank_out(masked, match.start(), match.end())
    return masked


def mask_code(text: str) -> str:
    """Replace fenced or inline code, HTML comments, URLs, and link destinations.

    Use spaces so source offsets stay unchanged.
    """
    return apply_masks(text, CODE_MASKS)


def mask_non_prose(text: str) -> str:
    """Replace code and quoted text with spaces without changing offsets."""
    return apply_masks(mask_code(text), QUOTE_MASKS)


# Put ignore-file before ignore in the alternation. If ignore comes first, it matches
# early and leaves "-file" behind, turning a file-wide directive into a line-wide one.
DIRECTIVE = re.compile(
    r"humanize-lint:\s*(off|on|ignore-file|ignore)(?:\s+([a-z][a-z0-9-]*))?",
    re.IGNORECASE,
)


def suppression_map(text: str) -> Tuple[set, Dict[int, set], set]:
    """Read directives into disabled lines plus per-line and file-wide category skips."""
    disabled, per_line, whole_file = set(), {}, set()
    active = False
    for index, line in enumerate(text.split("\n"), start=1):
        match = DIRECTIVE.search(line)
        if match:
            action, category = match.group(1).lower(), match.group(2)
            if action == "off":
                active = True
            elif action == "on":
                active = False
            elif action == "ignore":
                per_line.setdefault(index + 1, set()).add(category or "*")
            elif action == "ignore-file" and category:
                # A bare ignore-file would silence every rule. Leave the file out of the
                # run instead. This directive must name a category.
                whole_file.add(category)
        if active or match:
            disabled.add(index)
    return disabled, per_line, whole_file


def apply_suppressions(findings: List[Finding], disabled: set, per_line: Dict[int, set],
                       whole_file: set = frozenset()) -> List[Finding]:
    kept = []
    for finding in findings:
        if finding.line in disabled or finding.category in whole_file:
            continue
        skips = per_line.get(finding.line, set())
        if "*" in skips or finding.category in skips:
            continue
        kept.append(finding)
    return kept


BLOCK_BREAK = re.compile(r"^(?:[ \t]*$|[ \t]*(?:[-*+]|\d+\.)[ \t]|#{1,6}[ \t]|\|)", re.MULTILINE)


def iter_paragraphs(text: str) -> List[Tuple[int, str]]:
    """Split text at blank lines, list items, headings, and table rows.

    Treat each list item as a separate block so one em dash per item does not count as a
    paragraph-wide habit.
    """
    edges = sorted({0, len(text)} | {m.start() for m in BLOCK_BREAK.finditer(text)})
    blocks = []
    for index in range(len(edges) - 1):
        start, end = edges[index], edges[index + 1]
        chunk = text[start:end]
        if chunk.strip():
            blocks.append((start, chunk))
    return blocks


def iter_sections(text: str) -> List[Tuple[int, str]]:
    """Split at ATX Markdown headings for per-section bold counts."""
    boundaries = [m.start() for m in re.finditer(r"^#{1,6}[ \t]+\S", text, re.MULTILINE)]
    edges = [0] + boundaries + [len(text)]
    sections = []
    for index in range(len(edges) - 1):
        start, end = edges[index], edges[index + 1]
        if start < end:
            sections.append((start, text[start:end]))
    return sections


def excerpt_of(text: str, start: int, end: int, limit: int = 48) -> str:
    raw = text[start:end].replace("\n", " ").strip()
    raw = re.sub(r"\s+", " ", raw)
    if len(raw) > limit:
        raw = raw[: limit - 1] + "\u2026"
    return raw


# Pattern scanning


def scan_categories(
    raw_text: str, masked: str, masked_keep_comments: str,
    categories: Iterable[Category], target_format: str
) -> List[Finding]:
    starts = line_starts(raw_text)
    findings: List[Finding] = []
    for category in categories:
        if target_format in category.skip_formats:
            continue
        if category.scan == "raw":
            subject = raw_text
        elif category.scan == "prose+comments":
            subject = masked_keep_comments
        else:
            subject = masked
        hits = collect_category_hits(subject, starts, category)
        if category.cluster_threshold and len(hits) >= category.cluster_threshold:
            for hit in hits:
                hit.severity = category.cluster_severity
                hit.guidance = (
                    f"{category.guidance} Cluster of {len(hits)} in this text."
                )
        findings.extend(hits)
    return findings


def collect_category_hits(
    subject: str, starts: List[int], category: Category
) -> List[Finding]:
    seen: Dict[Tuple[int, int], Finding] = {}
    for compiled in category.patterns:
        for match in compiled.regex.finditer(subject):
            span = match.span("hit") if "hit" in compiled.regex.groupindex else match.span()
            if span[0] < 0:
                continue
            line, col = position_of(starts, span[0])
            guidance = category.guidance
            if compiled.note:
                guidance = f"{guidance} {compiled.note}"
            seen.setdefault(
                (line, col),
                Finding(
                    line=line,
                    col=col,
                    severity=compiled.severity,
                    category=category.id,
                    excerpt=excerpt_of(subject, *span),
                    guidance=guidance,
                ),
            )
    return list(seen.values())


# Structural checks


def check_em_dashes(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    """Treat em dashes and spaced double hyphens as dashes.

    In each paragraph, report the first as a note and the rest as reviews. The first
    finding records whether spaces surround the dash. Spaced dashes match the common AI
    pattern, while closed dashes are closer to conventional professional typography.
    Both count toward paragraph density.
    """
    findings = []
    for block_start, block in iter_paragraphs(masked):
        offsets = []
        spaced = []
        for match in re.finditer(r"\u2014|--", block):
            before = block[match.start() - 1:match.start()]
            after = block[match.end():match.end() + 1]
            if match.group(0) == "--" and (before != " " or after != " "):
                continue  # Ignore unspaced "--"; only the spaced form counts here.
            offsets.append(match.start() + block_start)
            spaced.append(before == " " and after == " ")
        for index, offset in enumerate(offsets):
            line, col = position_of(starts, offset)
            if index == 0:
                shape = ("surrounded by spaces, which is the more AI-typical shape"
                         if spaced[0] else
                         "not surrounded by spaces, which is closer to ordinary typography")
                findings.append(
                    Finding(line, col, "note", "em-dash-present", "\u2014",
                            f"Em dash {shape}. End the sentence or use a comma rather "
                            "than swapping in parentheses.")
                )
            else:
                findings.append(
                    Finding(line, col, "review", "em-dash-density", "\u2014",
                            "More than one em dash in this paragraph. Cut the extras.")
                )
    return findings


INLINE_HEADER_LINE = re.compile(r"^[ \t]*(?:[-*+\u2022\u2023\u25aa]|\d+\.)[ \t]+\*\*")


def check_bold_density(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    """Count bold spans per section, excluding list items that begin with bold text."""
    findings = []
    lines = masked.split("\n")
    for section_start, section in iter_sections(masked):
        spans = []
        for match in re.finditer(r"\*\*[^*\n]{1,80}\*\*", section):
            line, _ = position_of(starts, match.start() + section_start)
            if INLINE_HEADER_LINE.match(lines[line - 1]):
                continue
            spans.append((match.span(), line))
        for span, line in spans[2:]:
            _, col = position_of(starts, span[0] + section_start)
            findings.append(
                Finding(line, col, "review", "bold-density",
                        excerpt_of(section, *span),
                        f"{len(spans)} bold spans in this section. Bold should be rare.")
            )
    return findings


# Match bold labels used as list-item headers, with a colon, dash, or no punctuation.
# Leave a bold lead-in alone when it ends with a period.
COLON_HEADER_ITEM = re.compile(
    r"^[ \t]*(?:[-*+\u2022\u2023\u25aa]|\d+\.)[ \t]+\*\*(?P<label>[^*\n]+?)"
    r"(?::\*\*|\*\*[ \t]*[:\u2014-]|(?<=[^.!?])\*\*[ \t]+(?=[A-Za-z]))"
    r"(?P<body>[^\n]*)",
    re.MULTILINE,
)
STOPWORDS = {"a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "is", "are"}


def significant_words(text: str) -> List[str]:
    return [w.lower().rstrip("s") for w in re.findall(r"[A-Za-z]{3,}", text)
            if w.lower() not in STOPWORDS]


def restates_its_label(label: str, body: str) -> bool:
    """Return True when a short bold label repeats at the start of its body.

    A "Performance" label followed by "Performance improved..." matches. Reusing the
    label word later in the line does not.
    """
    label_words = significant_words(label)
    if not label_words or len(label_words) > 3:
        return False
    return bool(set(label_words) & set(significant_words(body)[:2]))


def check_inline_header_list(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    for match in COLON_HEADER_ITEM.finditer(masked):
        line, col = position_of(starts, match.start())
        if restates_its_label(match.group("label"), match.group("body")):
            findings.append(
                Finding(line, col, "error", "redundant-label",
                        excerpt_of(masked, match.start(), match.end()),
                        "The bold label repeats a word from the line it introduces, so it "
                        "adds nothing. Drop the label or make it say something new.")
            )
            continue
        findings.append(
            Finding(line, col, "error", "inline-header-list",
                    excerpt_of(masked, match.start("label") - 2, match.end("label") + 2),
                    "Bold label joined by a colon. Convert to prose, or use a bold lead-in "
                    "that ends in a period and is followed by new detail.")
        )
    return findings


def check_heading_case(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    for match in re.finditer(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", masked, re.MULTILINE):
        words = match.group(2).split()
        if len(words) < 3:
            continue
        rest = [w for w in words[1:] if w.lower() not in HEADING_CASE_EXEMPT]
        if len(rest) < 2:
            continue
        capped = [w for w in rest if w[:1].isupper() and not w.isupper()]
        if len(capped) / len(rest) < 0.6:
            continue
        line, col = position_of(starts, match.start(2))
        findings.append(
            Finding(line, col, "review", "heading-case", excerpt_of(masked, *match.span(2)),
                    "Title case heading. Use sentence case unless proper nouns require caps.")
        )
    return findings


def check_heading_levels(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    previous = 0
    for match in re.finditer(r"^(#{1,6})[ \t]+\S", masked, re.MULTILINE):
        level = len(match.group(1))
        if previous == 0 and level >= 3:
            line, col = position_of(starts, match.start())
            findings.append(
                Finding(line, col, "review", "first-heading-depth", "#" * level,
                        f"The document starts at H{level} with no higher-level heading. "
                        "Chatbot output often begins mid-outline; start at H1 or H2.")
            )
        if previous and level > previous + 1:
            line, col = position_of(starts, match.start())
            findings.append(
                Finding(line, col, "error", "heading-level-skip", "#" * level,
                        f"Heading jumps from H{previous} to H{level}. Do not skip levels.")
            )
        previous = level
    return findings


THEMATIC_BREAK = re.compile(r"^[ \t]*(?:-{3,}|\*{3,}|_{3,})[ \t]*$", re.MULTILINE)


def check_thematic_breaks(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    """Flag repeated horizontal rules used as section separators."""
    lines = masked.split("\n")
    hits = []
    for match in THEMATIC_BREAK.finditer(masked):
        line, col = position_of(starts, match.start())
        if line == 1:
            continue
        if lines[line - 2].strip():
            continue  # This may be a Setext underline or frontmatter delimiter.
        hits.append((line, col))
    if len(hits) < 2:
        return []
    return [
        Finding(line, col, "review", "thematic-break", "---",
                f"{len(hits)} horizontal rules between sections. Headings and blank lines "
                "already separate sections; repeated rules are a chatbot formatting habit.")
        for line, col in hits
    ]


def check_heading_only_sections(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    """Flag headings followed only by a deeper heading."""
    findings = []
    matches = list(re.finditer(r"^(#{1,6})[ \t]+.+$", masked, re.MULTILINE))
    for index, match in enumerate(matches[:-1]):
        nxt = matches[index + 1]
        if len(nxt.group(1)) <= len(match.group(1)):
            continue
        if masked[match.end():nxt.start()].strip():
            continue
        line, col = position_of(starts, match.start())
        findings.append(
            Finding(line, col, "review", "heading-only-section",
                    excerpt_of(masked, *match.span()),
                    "Heading whose entire section is another heading. Add the missing body "
                    "text or drop the parent heading.")
        )
    return findings


def check_quote_consistency(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    pairs = [
        ("double quotes", r"[\u201c\u201d]", r'"'),
        ("apostrophes", r"\u2019", r"'"),
    ]
    for label, curly, straight in pairs:
        curly_hits = list(re.finditer(curly, masked))
        straight_hits = list(re.finditer(straight, masked))
        if not curly_hits or not straight_hits:
            continue
        minority = curly_hits if len(curly_hits) <= len(straight_hits) else straight_hits
        line, col = position_of(starts, minority[0].start())
        findings.append(
            Finding(line, col, "error", "quote-consistency", minority[0].group(0),
                    f"Mixed curly and straight {label} "
                    f"({len(curly_hits)} curly, {len(straight_hits)} straight). Pick one.")
        )
    return findings


def check_emoji(masked: str, starts: List[int], fmt: str) -> List[Finding]:
    if fmt == "social":
        return []
    findings = []
    for match in EMOJI_RANGES.finditer(masked):
        line, col = position_of(starts, match.start())
        findings.append(
            Finding(line, col, "error", "emoji", match.group(0),
                    "No emoji in professional or reference writing.")
        )
    return findings


# Match the whole comma-separated run so the checker can count its items. A sliding
# three-item pattern would also match the tail of every four-item list.
WORD = r"[\w'\u2019-]+"
# Allow one newline so a wrapped item stays in the same run.
GAP = r"(?:[ \t]+|[ \t]*\n[ \t]*)"
# Cap each item at five words. A lower cap splits long items into false triples.
ITEM = rf"(?!(?:and|or)\b){WORD}(?:{GAP}{WORD}){{0,4}}"
# Keep the tail lazy so it does not consume the next list's first item.
LIST_RUN = re.compile(
    rf"(?P<head>(?:{ITEM},{GAP}?)+)(?:and|or){GAP}{WORD}(?:{GAP}{WORD}){{0,4}}?\b"
)
ASYNDETIC_ITEM = r"(?!(?:and|or)\b)[\w-]+(?:[ \t][\w-]+)?"
ASYNDETIC_TRIPLE = re.compile(
    rf"\b{ASYNDETIC_ITEM},[ \t]{ASYNDETIC_ITEM},[ \t]{ASYNDETIC_ITEM}[.!?;:]"
)
TRIPLE_THRESHOLD = 4


def check_rule_of_three(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    """Flag triples only after they repeat often enough to form a pattern."""
    runs = [m for m in LIST_RUN.finditer(masked) if m.group("head").count(",") == 2]
    runs += list(ASYNDETIC_TRIPLE.finditer(masked))
    if len(runs) < TRIPLE_THRESHOLD:
        return []
    findings = []
    for match in runs:
        line, col = position_of(starts, match.start())
        findings.append(
            Finding(line, col, "review", "rule-of-three", excerpt_of(masked, *match.span()),
                    f"{len(runs)} triple constructions in this text. Vary list length.")
        )
    return findings


# One "X, not Y" contrast can mark a useful boundary. This check looks for four matches
# across a document or two in one prose block. Its regex covers more forms than the
# negative-parallelism error rules because it counts clusters.
#
# The branches cover "not just X, but Y"; punctuation-linked variants; negated copulas
# joined by an em dash, semicolon, comma, or comma-plus-but; cross-sentence pivots such as
# "isn't X. It's Y"; repeated-negation lists; "More than a..."; clipped ", no X needed"
# tails; and a bare clause-ending "X, not Y".
#
# Leave out "X rather than Y". It appears often in the repository's clean prose and
# would create false positives at these thresholds. The judgment pass handles it.
NEGATIVE_PARALLEL_MARKER = re.compile(
    r"\b(?:not|(?:do|does|did)n(?:'|’)t)\s+(?:just|only|merely|simply)\s+[^,.;\n]{1,60},?\s+but\b"
    r"|\b(?:not|(?:do|does|did)n(?:'|’)t)\s+(?:just|only|merely|simply)\s+[^.;,\n]{1,80}[—;,]\s*(?:it|they|this)\b"
    r"|\b(?:is|are|was|were|ai)(?:\s+not|n(?:'|’)t)\s+[^.;,—\n]{1,90}[—;,]\s*(?:it|they|this|these)\b"
    r"|\b(?:is|are|was|were|ai)(?:\s+not|n(?:'|’)t)\s+[^,.;\n]{1,50},\s+but\s+(?:in|by|of|for|with|a|an|the|what|because|to)\b"
    r"|\b(?:is|are|was|were|ai)(?:\s+not|n(?:'|’)t)\s+[^.!?\n]{1,60}[.!?]\s+(?:Rather\b|Instead\b|It(?:'|’)s\s)"
    r"|\b(?:no|not)\s+[\w\s]{1,22},\s+(?:no|not)\s+[\w\s]{1,22}[,\s]*(?:[—–-]{1,2}\s*)?just\b"
    r"|\bmore\s+than\s+(?:a|an|just)\s+[^,.;\n]{1,40},\s+(?:this|it|the|he|she|they)\b"
    r"|,\s+no\s+\w+(?:\s+\w+){0,2}\s+(?:needed|required|necessary)\b"
    r"|[^,.;\n]{3,60},\s+not\s+[^,.;\n]{2,50}(?:[.!?]|,\s+(?:and|but|or|so|which|because)\b)"
    r"|\b(?:is|are|was|were)(?:\s+not|n(?:'|’)t)\s+the\s+(?:point|target|goal|aim|objective|job|answer|idea|fix|task|constraint)\b"
    r"|(?:'|’)s\s+not\s+the\s+(?:point|target|goal|aim|objective|job|answer|idea|fix|task|constraint)\b",
    re.IGNORECASE,
)
NEGATIVE_PARALLEL_DOC_THRESHOLD = 4
NEGATIVE_PARALLEL_PARAGRAPH_THRESHOLD = 2


def check_negative_parallelism_density(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    by_paragraph = [
        (block_start, list(NEGATIVE_PARALLEL_MARKER.finditer(block)))
        for block_start, block in iter_paragraphs(masked)
    ]
    doc_total = sum(len(matches) for _, matches in by_paragraph)
    doc_triggered = doc_total >= NEGATIVE_PARALLEL_DOC_THRESHOLD

    findings = []
    for block_start, matches in by_paragraph:
        local_triggered = len(matches) >= NEGATIVE_PARALLEL_PARAGRAPH_THRESHOLD
        if not (doc_triggered or local_triggered):
            continue
        if local_triggered:
            message = (f"{len(matches)} 'X, not Y'-shaped contrasts in this one passage. "
                        "That is a scaffold standing in for a plain claim, whatever each "
                        "half says alone. Cut most of them.")
        else:
            message = (f"{doc_total} 'X, not Y'-shaped contrasts across this document. One "
                        "states a boundary; this many is a scaffold standing in for plain "
                        "claims. Cut most of them.")
        for match in matches:
            line, col = position_of(starts, match.start() + block_start)
            findings.append(
                Finding(line, col, "review", "negative-parallelism-density",
                        excerpt_of(masked, match.start() + block_start, match.end() + block_start),
                        message)
            )
    return findings


def check_trailing_participle(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    # Check each comma-participle separately. One consuming scan could let an ordinary
    # phrase such as "..., including X, ..." swallow the rest of the sentence and hide a
    # later filler phrase.
    findings = []
    for match in re.finditer(r",\s+(\w+ing)\b", masked):
        if match.group(1).lower() not in FILLER_PARTICIPLES:
            continue
        tail = re.match(r"[^.!?\n]{0,140}[.!?]", masked[match.end():])
        if not tail:
            continue
        line, col = position_of(starts, match.start(1))
        findings.append(
            Finding(line, col, "error", "trailing-participle",
                    excerpt_of(masked, match.start(), match.end() + tail.end()),
                    "Sentence-final participial clause with no factual content. Delete it.")
        )
    return findings


def check_abrupt_ending(raw_text: str, starts: List[int], _fmt: str) -> List[Finding]:
    # Ignore trailing HTML comments, including any lint directives they contain. Check
    # the last line with actual content.
    trimmed = re.sub(r"(?:\s*<!--.*?-->)+\s*\Z", "", raw_text, flags=re.DOTALL)
    lines = trimmed.rstrip().split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return []
    last = lines[-1].strip()
    structural = re.match(r"^(#{1,6}\s|\||[-*+]\s|\d+\.\s|```|~~~|>|\[)", last)
    if structural or re.search(r"[.!?:;\"'\u201d\u2019)\]}|]$", last):
        return []
    line, col = position_of(starts, max(len(trimmed.rstrip()) - 1, 0))
    return [
        Finding(line, col, "error", "abrupt-ending", excerpt_of(last, 0, len(last)),
                "Text ends without completing its final thought.")
    ]


def check_small_tables(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    pattern = re.compile(r"(?:^\|.*\|[ \t]*$\n?){3,}", re.MULTILINE)
    for match in pattern.finditer(masked):
        rows = [r for r in match.group(0).strip().split("\n") if r.strip()]
        body = [r for r in rows[2:] if not re.match(r"^\|[\s:|-]+\|$", r)]
        columns = rows[0].count("|") - 1
        if len(body) <= 4 and columns <= 3:
            line, col = position_of(starts, match.start())
            findings.append(
                Finding(line, col, "review", "small-table",
                        f"{len(body)} rows x {columns} cols",
                        "Small table. State this in a sentence instead.")
            )
    return findings


def check_markdown_bleed(raw_text: str, starts: List[int], fmt: str) -> List[Finding]:
    if fmt not in NON_MARKDOWN_FORMATS:
        return []
    findings = []
    patterns = [
        (r"\*\*[^*\n]+\*\*", "bold asterisks"),
        (r"^#{1,6}[ \t]+\S", "hash heading"),
        (r"\[[^\]\n]+\]\([^)\n]+\)", "markdown link"),
    ]
    for expression, label in patterns:
        for match in re.finditer(expression, raw_text, re.MULTILINE):
            line, col = position_of(starts, match.start())
            findings.append(
                Finding(line, col, "error", "markdown-bleed",
                        excerpt_of(raw_text, *match.span()),
                        f"Markdown {label} in a {fmt} target. Use the target's own markup.")
            )
    return findings


def check_access_dates(raw_text: str, starts: List[int], _fmt: str) -> List[Finding]:
    pattern = re.compile(r"access[-\s]?date\s*=\s*([^|\n}]+)|accessed\s+(\d{1,2}\s+\w+\s+\d{4})",
                         re.IGNORECASE)
    tally: Dict[str, List[int]] = {}
    for match in pattern.finditer(raw_text):
        value = (match.group(1) or match.group(2) or "").strip()
        tally.setdefault(value, []).append(match.start())
    findings = []
    for value, offsets in tally.items():
        if len(offsets) < 3:
            continue
        line, col = position_of(starts, offsets[0])
        findings.append(
            Finding(line, col, "review", "identical-access-dates", value,
                    f"{len(offsets)} citations share this access date. Vary or remove them.")
        )
    return findings


LIST_LINE = re.compile(r"^[ \t]*(?:[-*+\u2022\u2023\u25aa]|\d+[.)])[ \t]+\S")
HEADING_LINE = re.compile(r"^[ \t]*#{1,6}[ \t]")
TABLE_LINE = re.compile(r"^[ \t]*\|")

LIST_SHARE_LIMIT = 0.55
LIST_RUN_LIMIT = 12
MIN_LINES_FOR_DENSITY = 12


def survey_lines(masked: str) -> Dict[str, int]:
    """Count line shapes used to distinguish prose from an outline."""
    content = lists = inline_headers = longest = current = 0
    for line in masked.split("\n"):
        if not line.strip() or HEADING_LINE.match(line) or TABLE_LINE.match(line):
            current = 0
            continue
        content += 1
        if LIST_LINE.match(line):
            lists += 1
            current += 1
            longest = max(longest, current)
            # Count list items that use a bold label as a header.
            if COLON_HEADER_ITEM.match(line):
                inline_headers += 1
        else:
            current = 0
    return {"content": content, "lists": lists, "inline_headers": inline_headers,
            "longest_run": longest}


def check_list_density(masked: str, _starts: List[int], _fmt: str) -> List[Finding]:
    """Report list-heavy documents once instead of once per list item."""
    counts = survey_lines(masked)
    if counts["content"] < MIN_LINES_FOR_DENSITY:
        return []
    share = counts["lists"] / counts["content"]
    if share < LIST_SHARE_LIMIT and counts["longest_run"] < LIST_RUN_LIMIT:
        return []
    return [
        Finding(1, 1, "review", "list-density",
                f"{share:.0%} list lines, longest run {counts['longest_run']}",
                "This document is mostly an outline. Turn the parts that explain "
                "something into paragraphs and keep bullets for genuinely parallel items.")
    ]


def check_inline_header_density(masked: str, _starts: List[int], _fmt: str) -> List[Finding]:
    """Report documents where at least six list items use bold headers.

    The check fires when those headers make up at least half of all list items.
    """
    counts = survey_lines(masked)
    if counts["inline_headers"] < 6 or not counts["lists"]:
        return []
    share = counts["inline_headers"] / counts["lists"]
    if share < 0.5:
        return []
    return [
        Finding(1, 1, "review", "inline-header-density",
                f"{counts['inline_headers']} of {counts['lists']} list items",
                "Most list items are bold-header entries. Convert some to prose or plain "
                "bullets so the pattern is a choice rather than the default.")
    ]


WEAK_ADVERBS = re.compile(
    r"\b(?:significantly|substantially|dramatically|greatly|highly|extremely|incredibly|"
    r"particularly|essentially|basically|actually|really|quite|simply|easily|"
    # Leave out "very". In the PNAS study cited by Wikipedia's "Signs of AI writing",
    # people used it more often than the tested models. Flagging it would make prose more
    # model-like.
    r"quickly|effectively|efficiently|seamlessly|notably|remarkably|considerably|"
    r"fundamentally|undoubtedly|obviously|clearly|definitely|truly|literally)\b",
    re.IGNORECASE,
)

PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?"
    r"(?P<verb>\w+ed|written|built|made|done|given|taken|seen|known|shown|held|kept|"
    r"found|sent|put|drawn|thrown|chosen|driven|broken)\b",
    re.IGNORECASE,
)

LONG_SENTENCE_WORDS = 40


FRONTMATTER = re.compile(r"\A---\n.*?\n---", re.S)


def blank_keeping_lines(text: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in text)


def prose_only(masked: str) -> str:
    """Blank frontmatter and unindented lines starting with a Markdown marker or digit.

    The recognized markers are #, >, |, -, *, and +. Keep offsets unchanged so findings
    still point to the source. Frontmatter descriptions list triggers, so the rhythm
    rules ignore their length.
    """
    text = FRONTMATTER.sub(lambda m: blank_keeping_lines(m.group(0)), masked)
    return re.sub(r"^[#>|\-*+\d].*$", lambda m: " " * len(m.group(0)),
                  text, flags=re.MULTILINE)


def check_weak_adverbs(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    for match in WEAK_ADVERBS.finditer(masked):
        line, col = position_of(starts, match.start())
        findings.append(
            Finding(line, col, "note", "weak-adverb", match.group(0),
                    "An adverb propping up a weak verb means the verb is wrong. Use a "
                    "stronger verb or the measured number.")
        )
    return findings


def check_passive_voice(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    for match in PASSIVE.finditer(masked):
        line, col = position_of(starts, match.start())
        findings.append(
            Finding(line, col, "note", "passive-voice", excerpt_of(masked, *match.span()),
                    "Name the actor. Passive is fine only when the actor is unknown or "
                    "genuinely does not matter.")
        )
    return findings


def iter_sentences(prose: str) -> List[Tuple[str, int]]:
    """Return each sentence with its offset, stopping at paragraph breaks.

    A paragraph that introduces a list with a colon has no terminal punctuation.
    Paragraph splitting keeps it from joining the prose after the list into one
    artificially long sentence.
    """
    found: List[Tuple[str, int]] = []
    block_cursor = 0
    for block in PARAGRAPH_BREAK.split(prose):
        block_start = prose.find(block, block_cursor) if block else -1
        if block_start < 0:
            continue
        block_cursor = block_start + len(block)
        cursor = 0
        for sentence in SENTENCE_SPLIT.split(block):
            index = block.find(sentence, cursor) if sentence else -1
            if index < 0:
                continue
            cursor = index + len(sentence)
            found.append((sentence, block_start + index))
    return found


def check_sentence_length(masked: str, starts: List[int], _fmt: str) -> List[Finding]:
    findings = []
    for sentence, start in iter_sentences(prose_only(masked)):
        if len(sentence.split()) <= LONG_SENTENCE_WORDS:
            continue
        lead = len(sentence) - len(sentence.lstrip())
        line, col = position_of(starts, start + lead)
        findings.append(
            Finding(line, col, "review", "long-sentence",
                    f"{len(sentence.split())} words", 
                    "The reader has to backtrack to parse this. Split it, or drop clauses "
                    "until it holds one idea.")
        )
    return findings


SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
PARAGRAPH_BREAK = re.compile(r"\n\s*\n")


def check_sentence_rhythm(masked: str, _starts: List[int], _fmt: str) -> List[Finding]:
    lengths = [
        len(sentence.split())
        for sentence, _ in iter_sentences(prose_only(masked))
        if len(sentence.split()) >= 4
    ]
    if len(lengths) < 8:
        return []
    spread = statistics.pstdev(lengths)
    if spread >= 5.0:
        return []
    return [
        Finding(1, 1, "review", "sentence-rhythm", f"stdev {spread:.1f} over {len(lengths)} sentences",
                "Sentence lengths are unusually uniform. Vary short and long sentences.")
    ]


STRUCTURAL_CHECKS_MASKED = [
    check_thematic_breaks,
    check_heading_only_sections,
    check_em_dashes, check_bold_density, check_inline_header_list, check_heading_case,
    check_heading_levels, check_emoji, check_rule_of_three,
    check_negative_parallelism_density,
    check_trailing_participle, check_small_tables, check_sentence_rhythm,
    check_list_density, check_inline_header_density, check_weak_adverbs,
    check_passive_voice, check_sentence_length,
]
STRUCTURAL_CHECKS_RAW = [check_abrupt_ending, check_markdown_bleed, check_access_dates]
# Quote checks need the unmasked quote marks.
STRUCTURAL_CHECKS_CODE_ONLY = [check_quote_consistency]


def run_structural(raw_text: str, masked: str, code_only: str, target_format: str) -> List[Finding]:
    starts = line_starts(raw_text)
    findings: List[Finding] = []
    for check in STRUCTURAL_CHECKS_MASKED:
        findings.extend(check(masked, starts, target_format))
    for check in STRUCTURAL_CHECKS_CODE_ONLY:
        findings.extend(check(code_only, starts, target_format))
    for check in STRUCTURAL_CHECKS_RAW:
        findings.extend(check(raw_text, starts, target_format))
    return findings


# Reporting


def analyze(raw_text: str, categories: List[Category], target_format: str,
            profile: Optional[Profile] = None) -> List[Finding]:
    code_only = mask_code(raw_text)
    masked = apply_masks(code_only, QUOTE_MASKS)
    masked_keep_comments = apply_masks(
        apply_masks(raw_text, CODE_MASKS_KEEP_COMMENTS), QUOTE_MASKS
    )
    findings = scan_categories(raw_text, masked, masked_keep_comments,
                               categories, target_format)
    findings.extend(run_structural(raw_text, masked, code_only, target_format))
    if profile is not None:
        findings = apply_profile(findings, profile)
    disabled, per_line, whole_file = suppression_map(raw_text)
    findings = apply_suppressions(findings, disabled, per_line, whole_file)
    findings.sort(key=lambda f: (f.line, f.col, f.category))
    return findings


def cap_per_category(findings: List[Finding], limit: int) -> Tuple[List[Finding], Dict[str, int]]:
    if limit <= 0:
        return findings, {}
    kept: List[Finding] = []
    counts: Dict[str, int] = {}
    hidden: Dict[str, int] = {}
    for finding in findings:
        counts[finding.category] = counts.get(finding.category, 0) + 1
        if counts[finding.category] <= limit:
            kept.append(finding)
        else:
            hidden[finding.category] = hidden.get(finding.category, 0) + 1
    return kept, hidden


def group_by_category(findings: List[Finding]) -> List[Tuple[str, List[Finding]]]:
    buckets: Dict[str, List[Finding]] = {}
    for finding in findings:
        buckets.setdefault(finding.category, []).append(finding)
    ordered = sorted(
        buckets.items(),
        key=lambda item: (min(SEVERITY_ORDER[f.severity] for f in item[1]),
                          -len(item[1]), item[0]),
    )
    return ordered


def describe_counts(hits: List[Finding]) -> str:
    tally = {level: sum(1 for f in hits if f.severity == level) for level in SEVERITY_ORDER}
    return ", ".join(f"{count} {level}" for level, count in tally.items() if count)


def format_text_report(
    findings: List[Finding], hidden: Dict[str, int], totals: Dict[str, int],
    multi_file: bool, profile: Profile, show_all: bool
) -> str:
    lines = [f"profile: {profile.id} ({profile.label})", ""]
    actionable = [f for f in findings if f.severity != "note"]
    notes = [f for f in findings if f.severity == "note"]

    for category, hits in group_by_category(actionable):
        lines.append(f"{category}  [{describe_counts(hits)}]  {hits[0].guidance}")
        width = max(len(location_of(f, multi_file)) for f in hits)
        for finding in hits:
            lines.append(f"    {location_of(finding, multi_file).ljust(width)}  {finding.excerpt}")
        if category in hidden:
            lines.append(f"    ... {hidden[category]} more hidden (use --all)")
        lines.append("")

    # Summarize notes by category so low-priority findings do not flood the report.
    if notes and not show_all:
        summary = ", ".join(
            f"{category} x{len(hits)}" for category, hits in group_by_category(notes)
        )
        lines.append(f"notes (not blocking): {summary}")
        lines.append("")
    elif notes:
        for category, hits in group_by_category(notes):
            lines.append(f"{category}  [{describe_counts(hits)}]  {hits[0].guidance}")
            for finding in hits:
                lines.append(f"    {location_of(finding, multi_file)}  {finding.excerpt}")
            lines.append("")

    lines.append(
        f"{sum(totals.values())} finding(s): " +
        ", ".join(f"{totals[level]} {level}" for level in SEVERITY_ORDER if totals[level])
    )
    return "\n".join(lines)


def location_of(finding: Finding, multi_file: bool) -> str:
    if multi_file:
        return f"{finding.path}:{finding.line}:{finding.col}"
    return f"{finding.line}:{finding.col}"


def read_source(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="humanize_lint.py",
        description="Flag mechanically detectable AI-writing tells.",
    )
    parser.add_argument("paths", nargs="+", help="Files to check, or - for stdin.")
    parser.add_argument("--profile", default=None,
                        help="Editorial strictness: doc (default) or reference. "
                             "Profiles relax structural rules only, never prose rules.")
    parser.add_argument("--format", default="markdown", choices=sorted(PROSE_FORMATS | {"social"}),
                        help="Target output format (default: markdown).")
    parser.add_argument("--rules", default=DEFAULT_RULES, help="Path to patterns.json.")
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on review findings too.")
    parser.add_argument("--all", action="store_true",
                        help="Show every finding instead of capping per category.")
    parser.add_argument("--limit", type=int, default=6,
                        help="Max findings shown per category (default: 6).")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        categories = load_categories(args.rules)
        profiles, default_profile = load_profiles(args.rules)
    except (OSError, ValueError, KeyError) as error:
        print(f"humanize_lint: cannot load rules: {error}", file=sys.stderr)
        return 2

    profile = profiles.get(args.profile or default_profile)
    if profile is None:
        print(f"humanize_lint: unknown profile {args.profile!r}. "
              f"Available: {', '.join(sorted(profiles))}", file=sys.stderr)
        return 2

    findings: List[Finding] = []
    for path in args.paths:
        try:
            text = read_source(path)
        except OSError as error:
            print(f"humanize_lint: {error}", file=sys.stderr)
            return 2
        label = "<stdin>" if path == "-" else path
        for finding in analyze(text, categories, args.format, profile):
            finding.path = label
            findings.append(finding)

    findings.sort(key=lambda f: (f.path, f.line, f.col, SEVERITY_ORDER[f.severity]))
    totals = {level: sum(1 for f in findings if f.severity == level) for level in SEVERITY_ORDER}
    shown, hidden = cap_per_category(findings, 0 if args.all else args.limit)

    if args.json:
        print(json.dumps({"profile": profile.id, "findings": [f.__dict__ for f in shown],
                          "totals": totals}, indent=2))
    elif not findings:
        print(f"clean ({profile.id} profile): no mechanical AI-writing tells found")
    else:
        print(format_text_report(shown, hidden, totals, len(args.paths) > 1, profile, args.all))

    blocking = STRICT_SEVERITIES if args.strict else FAILING_SEVERITIES
    if any(totals[level] for level in blocking):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
