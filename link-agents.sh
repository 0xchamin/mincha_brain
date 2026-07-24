#!/usr/bin/env bash
# link-agents.sh - macOS / Linux
# One canonical contract (AGENTS.md), symlinked to the pointer paths some harnesses expect.
# Run ONCE per clone. The links are git-ignored, so nothing tool-specific is ever maintained.
#
#   Copilot CLI, Codex, Cursor  -> read AGENTS.md natively (no link needed)
#   Claude Code                 -> CLAUDE.md
#   GitHub Copilot (IDE/agent)  -> .github/copilot-instructions.md
#
# Usage:  ./link-agents.sh
set -euo pipefail
cd "$(dirname "$0")"

ln -sf AGENTS.md CLAUDE.md
mkdir -p .github
ln -sf ../AGENTS.md .github/copilot-instructions.md

echo "Linked -> AGENTS.md:"
echo "  CLAUDE.md                        (Claude Code)"
echo "  .github/copilot-instructions.md  (GitHub Copilot IDE / coding agent)"
echo "Codex, Cursor and Copilot CLI read AGENTS.md natively - no link needed."
