#!/usr/bin/env bash
# One-command install: clone (or reuse) the repo, link every skill into each agent
# harness, and put any skill-provided commands on PATH.
#
#   curl -fsSL https://raw.githubusercontent.com/hellsan631/skills/main/scripts/install.sh | bash
#
# Re-running updates an existing clone rather than failing.
set -euo pipefail

REPO_URL="${SKILLS_REPO_URL:-https://github.com/hellsan631/skills.git}"
REPO_DIR="${SKILLS_REPO_DIR:-$HOME/.local/share/agent-skills}"

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "error: $1 is required but not installed." >&2; exit 1; }
}
need git
need python3

# Running from inside an existing clone should use that clone, not make a second one.
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." 2>/dev/null && pwd || true)"
if [ -n "$here" ] && [ -d "$here/skills" ] && [ -d "$here/.git" ]; then
  REPO_DIR="$here"
  echo "using this clone: $REPO_DIR"
elif [ -d "$REPO_DIR/.git" ]; then
  echo "updating $REPO_DIR"
  git -C "$REPO_DIR" pull --ff-only
else
  echo "cloning into $REPO_DIR"
  mkdir -p "$(dirname "$REPO_DIR")"
  git clone --depth 1 "$REPO_URL" "$REPO_DIR"
fi

bash "$REPO_DIR/scripts/link-skills.sh"

# Skills that ship a command install it themselves, so this loop needs no per-skill
# knowledge and keeps working as skills are added.
while IFS= read -r shim; do
  echo
  bash "$shim"
done < <(find "$REPO_DIR/skills" -name 'install-shim.sh' | sort)

echo
echo "done. Restart your agent so it picks up the new skills."
