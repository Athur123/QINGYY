#!/bin/bash
# Install local git hooks used by this repository.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_DIR="$PROJECT_DIR/.git/hooks"

mkdir -p "$HOOK_DIR"

cp "$PROJECT_DIR/scripts/pre-commit-docs-frontmatter.sh" "$HOOK_DIR/pre-commit"
chmod +x "$HOOK_DIR/pre-commit"

if [ -f "$PROJECT_DIR/scripts/post-commit-hook.sh" ]; then
  cp "$PROJECT_DIR/scripts/post-commit-hook.sh" "$HOOK_DIR/post-commit"
  chmod +x "$HOOK_DIR/post-commit"
fi

echo "Installed git hooks in $HOOK_DIR"
