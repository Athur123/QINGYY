#!/bin/bash
# .git/hooks/post-commit - 每次 commit 后自动更新记忆
# 安装: cp scripts/post-commit-hook.sh .git/hooks/post-commit && chmod +x .git/hooks/post-commit

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$PROJECT_DIR/scripts/update-memory.sh"

if [ -x "$SCRIPT" ]; then
    "$SCRIPT" > /dev/null 2>&1
fi
