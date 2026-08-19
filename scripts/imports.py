#!/usr/bin/env python3
"""Track skills imported from other repos, recorded in imports.json.

Imported skills are ours to edit. Nothing here overwrites a local file: the point is to
see what the original authors changed after we took a copy, so a good idea upstream can
be read and applied on purpose.

    python3 scripts/imports.py diff                 # upstream changes since we imported
    python3 scripts/imports.py diff codebase-design # just one skill
    python3 scripts/imports.py diff --stat          # names and line counts only
    python3 scripts/imports.py add mattpocock skills/engineering/foo skills/engineering/foo
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "imports.json"
CACHE = Path(tempfile.gettempdir()) / "agent-skills-import-cache"

SMALL_WORDS = {"a", "an", "and", "the", "to", "of", "in", "on", "for", "before", "from"}


def git(args, cwd, check=True):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f"error: git {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout


def checkout_for(name, spec):
    """A full local mirror of one upstream, so history is available for diffing."""
    path = CACHE / name
    if not (path / ".git").exists():
        path.mkdir(parents=True, exist_ok=True)
        git(["init", "-q"], path)
        git(["remote", "add", "origin", spec["repo"]], path)
    git(["fetch", "-q", "origin"], path)
    return path


def upstream_head(path):
    return git(["rev-parse", "origin/HEAD"], path, check=False).strip() or git(
        ["rev-parse", "FETCH_HEAD"], path
    ).strip()


def frontmatter_of(skill_md):
    match = re.match(r"^---\n(.*?)\n---", skill_md.read_text(errors="ignore"), re.S)
    return match.group(1) if match else ""


def field(front, key):
    match = re.search(rf"^{key}:\s*(.+)$", front, re.M)
    return match.group(1).strip().strip("\"'") if match else ""


def display_name_for(skill_name):
    prefix, words = "", skill_name.split("-")
    if words[0] == "principle":
        prefix, words = "Principle: ", words[1:]
    titled = [
        word if index and word in SMALL_WORDS else word.capitalize()
        for index, word in enumerate(words)
    ]
    return prefix + " ".join(titled)


def short_description_for(description):
    first = re.split(r"(?<=[.!?])\s", description.strip())[0].rstrip(".")
    return first if len(first) <= 90 else first[:87].rstrip() + "..."


def write_picker_metadata(skill_dir):
    """Codex reads agents/openai.yaml for picker metadata; not every source ships one."""
    target = skill_dir / "agents" / "openai.yaml"
    if target.exists() or not (skill_dir / "SKILL.md").exists():
        return False
    front = frontmatter_of(skill_dir / "SKILL.md")
    lines = [
        "interface:",
        f'  display_name: "{display_name_for(field(front, "name") or skill_dir.name)}"',
        f'  short_description: "{short_description_for(field(front, "description"))}"',
    ]
    if field(front, "disable-model-invocation") == "true":
        lines += ["policy:", "  allow_implicit_invocation: false"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n")
    return True


def command_diff(manifest, args):
    wanted = args.skill
    selected = [
        entry
        for entry in manifest["skills"]
        if not wanted or Path(entry["path"]).name == wanted
    ]
    if not selected:
        raise SystemExit(f"error: no imported skill named {wanted}")

    checkouts, heads = {}, {}
    for name in {entry["source"] for entry in selected}:
        checkouts[name] = checkout_for(name, manifest["sources"][name])
        heads[name] = upstream_head(checkouts[name])

    changed = 0
    for entry in selected:
        source = entry["source"]
        since = manifest["sources"][source]["imported_at"]
        head = heads[source]
        if since == head:
            continue
        flags = ["--stat"] if args.stat else []
        patch = git(
            ["diff", *flags, f"{since}..{head}", "--", entry["upstream_path"]],
            checkouts[source],
        )
        if patch.strip():
            changed += 1
            print(f"\n=== {entry['path']}  ({source} {since[:9]}..{head[:9]}) ===")
            print(patch.rstrip())

    if changed == 0:
        print("no upstream changes since import")
    else:
        print(f"\n{changed} imported skill(s) changed upstream. Adopt what is worth adopting.")
    return 0


def command_add(manifest, args):
    if args.source not in manifest["sources"]:
        raise SystemExit(f"error: unknown source {args.source}")
    dest = REPO / args.path
    if dest.exists():
        raise SystemExit(f"error: {args.path} already exists; this never overwrites")

    checkout = checkout_for(args.source, manifest["sources"][args.source])
    head = upstream_head(checkout)
    git(["checkout", "-q", "--detach", head], checkout)

    src = checkout / args.upstream_path
    if not (src / "SKILL.md").exists():
        raise SystemExit(f"error: {args.upstream_path} has no SKILL.md")

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)
    write_picker_metadata(dest)

    manifest["skills"].append(
        {"source": args.source, "upstream_path": args.upstream_path, "path": args.path}
    )
    manifest["sources"][args.source]["imported_at"] = head
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"imported {args.path} from {args.source}@{head[:9]}")
    print("Register it in .claude-plugin/plugin.json and README.md, then run scripts/test.sh")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    diff = sub.add_parser("diff", help="show upstream changes since import")
    diff.add_argument("skill", nargs="?", help="limit to one skill directory name")
    diff.add_argument("--stat", action="store_true", help="summarise instead of full patch")

    add = sub.add_parser("add", help="import a new skill from a known source")
    add.add_argument("source")
    add.add_argument("upstream_path")
    add.add_argument("path")

    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    return command_diff(manifest, args) if args.command == "diff" else command_add(manifest, args)


if __name__ == "__main__":
    sys.exit(main())
