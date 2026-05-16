#!/bin/bash
# Check Obsidian frontmatter for staged Qingyang docs before commit.

set -euo pipefail

PROJECT_DIR="$(git rev-parse --show-toplevel)"

python3 "$PROJECT_DIR/scripts/check_docs_frontmatter.py" --staged
