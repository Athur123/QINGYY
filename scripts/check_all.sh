#!/bin/bash
# Run the standard Qingyang prototype/documentation checks.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

python3 scripts/check_design_system.py
python3 scripts/check_reconciliation_confirm_unification.py
python3 scripts/check_docs_frontmatter.py --strict

echo "PASS: all project checks"
