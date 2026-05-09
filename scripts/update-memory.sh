#!/bin/bash
# update-memory.sh - 自动更新项目记忆
# 用法:
#   ./update-memory.sh              # 分析最新 commit 并更新 memory
#   ./update-memory.sh HEAD~3..HEAD # 分析指定范围的 commits

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
# Claude memory is stored in ~/.claude/projects/<path>/memory/
# Convert /Users/athur/PycharmProjects/qyy to -Users-athur-PycharmProjects-qyy
MEMORY_PATH="$(echo "$PROJECT_DIR" | sed 's|^/||; s|/|-|g')"
MEMORY_DIR="$HOME/.claude/projects/-$MEMORY_PATH/memory"
MEMORY_INDEX="$MEMORY_DIR/MEMORY.md"

# Ensure memory directory exists
mkdir -p "$MEMORY_DIR"

# 获取 commit 范围
if [ $# -gt 0 ]; then
    RANGE="$1"
else
    RANGE="HEAD^..HEAD"
fi

echo "📝 分析 commits: $RANGE"

# 获取变更文件列表
CHANGED_FILES=$(git diff --name-only "$RANGE" 2>/dev/null || echo "")

if [ -z "$CHANGED_FILES" ]; then
    echo "✅ 无文件变更"
    exit 0
fi

echo "📂 变更文件:"
echo "$CHANGED_FILES" | while read -r f; do echo "  - $f"; done

# 获取 commit 信息
COMMITS=$(git log --oneline --no-merges "$RANGE" 2>/dev/null || echo "")

if [ -z "$COMMITS" ]; then
    echo "ℹ️  无 commit 信息"
    exit 0
fi

echo ""
echo "📋 Commits:"
echo "$COMMITS" | while read -r c; do echo "  $c"; done

# 检测变更类型
TYPES=()
PROTOTYPE_CHANGES=""
STYLE_CHANGES=""
DOC_CHANGES=""
SPEC_CHANGES=""
PLAN_CHANGES=""
SQL_CHANGES=""

while IFS= read -r file; do
    case "$file" in
        prototype/*)
            PROTOTYPE_CHANGES="${PROTOTYPE_CHANGES}  - ${file#prototype/}
"
            ;;
        styles/*)
            STYLE_CHANGES="${STYLE_CHANGES}  - ${file#styles/}
"
            ;;
        docs/superpowers/specs/*)
            SPEC_CHANGES="${SPEC_CHANGES}  - ${file#docs/superpowers/specs/}
"
            ;;
        docs/superpowers/plans/*)
            PLAN_CHANGES="${PLAN_CHANGES}  - ${file#docs/superpowers/plans/}
"
            ;;
        docs/superpowers/sql/*)
            SQL_CHANGES="${SQL_CHANGES}  - ${file#docs/superpowers/sql/}
"
            ;;
    esac
done <<< "$CHANGED_FILES"

# 生成变更摘要文件
CHANGELOG_FILE="$MEMORY_DIR/changes/$(date +%Y-%m-%d)-$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown').md"

mkdir -p "$MEMORY_DIR/changes"

cat > "$CHANGELOG_FILE" << EOF
# 变更 $(date +%Y-%m-%d)

## Commits
$(echo "$COMMITS" | sed 's/^/- /')

## 变更文件

### 原型页面
${PROTOTYPE_CHANGES:-无变更}

### 样式/组件
${STYLE_CHANGES:-无变更}

### 设计规格
${SPEC_CHANGES:-无变更}

### 实现计划
${PLAN_CHANGES:-无变更}

### SQL 脚本
${SQL_CHANGES:-无变更}

## 摘要
$(git log --format="- %s" "$RANGE" 2>/dev/null || echo "无")
EOF

echo ""
echo "📄 变更记录已写入: $CHANGELOG_FILE"

# 更新 MEMORY.md 的变更记录部分
echo "🔄 更新 MEMORY.md 索引..."

# 提取变更摘要行（最多10条）
SUMMARY_LINES=$(git log --format="- %s" "$RANGE" 2>/dev/null | head -10)

# 如果 MEMORY.md 中有 "## 变更记录" 段，在其后添加新的记录
if grep -q "## 变更记录" "$MEMORY_INDEX" 2>/dev/null; then
    # 检查是否已存在今天的记录，避免重复
    TODAY=$(date +%Y-%m-%d)
    NEW_ENTRY="- $TODAY: $(echo "$SUMMARY_LINES" | head -1 | sed 's/^- //')"

    # 只在该日期没有记录时才添加
    if ! grep -q "^- $TODAY:" "$MEMORY_INDEX" 2>/dev/null; then
        TEMP_FILE=$(mktemp)
        awk -v new_lines="$NEW_ENTRY" '
        /^## 变更记录$/ { print; print new_lines; next }
        { print }
        ' "$MEMORY_INDEX" > "$TEMP_FILE"
        mv "$TEMP_FILE" "$MEMORY_INDEX"
    fi
else
    echo "" >> "$MEMORY_INDEX"
    echo "## 变更记录" >> "$MEMORY_INDEX"
    echo "- $(date +%Y-%m-%d): $(echo "$SUMMARY_LINES" | head -1 | sed 's/^- //')" >> "$MEMORY_INDEX"
fi

echo "✅ Memory 更新完成"
