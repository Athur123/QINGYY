#!/usr/bin/env python3
"""Static checks for Qingyang design-system consistency."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def fail(errors, message):
    errors.append(message)


def require_contains(errors, path, needle, label=None):
    text = read(path)
    if needle not in text:
        fail(errors, f"{path}: missing {label or needle!r}")


def require_not_contains(errors, path, needle, label=None):
    text = read(path)
    if needle in text:
        fail(errors, f"{path}: contains deprecated {label or needle!r}")


def require_regex(errors, path, pattern, label):
    text = read(path)
    if not re.search(pattern, text, flags=re.MULTILINE):
        fail(errors, f"{path}: missing {label}")


def main():
    errors = []

    require_contains(errors, "qingyang-hro-design-system.md", "# 青阳云HRO设计系统 v2.1", "v2.1 title")
    require_contains(errors, "styles/qingyang-variables.css", "Version: 2.1.0", "variables version")
    require_contains(errors, "styles/qingyang-base.css", "Version: 2.1.0", "base version")
    require_contains(errors, "styles/qingyang-components.css", "Version: 2.1.0", "components version")
    require_contains(errors, "styles/qingyang-forms.css", "Version: 2.1.0", "forms version")
    require_contains(errors, "styles/qingyang-design-system.css", "Version: 2.1.0", "combined version")

    require_contains(errors, "styles/qingyang-variables.css", "--qy-font-family:", "canonical font-family token")
    require_contains(errors, "styles/qingyang-variables.css", "--qy-font-primary: var(--qy-font-family);", "font-primary alias")
    require_contains(errors, "styles/qingyang-variables.css", "--qy-font-size-base: var(--qy-font-size-14);", "semantic base font token")
    require_contains(errors, "styles/qingyang-variables.css", "--qy-focus-ring: var(--qy-shadow-focus);", "focus-ring alias")
    require_contains(errors, "styles/qingyang-variables.css", "--qy-danger-500: var(--qy-error-500);", "danger alias")
    require_contains(errors, "styles/qingyang-variables.css", "--qy-content-padding-x: 20px;", "v2.1 horizontal page padding")
    require_contains(errors, "styles/qingyang-variables.scss", "$font-primary: 'Plus Jakarta Sans'", "SCSS canonical font")

    require_contains(errors, "styles/qingyang-base.css", "font-family: var(--qy-font-family);", "base font-family")
    require_contains(errors, "styles/qingyang-base.css", "font-size: var(--qy-font-size-base);", "base body font-size")
    require_not_contains(errors, "styles/qingyang-base.css", "body {\n  font-family: var(--qy-font-primary);\n  font-size: var(--qy-font-size-13);", "v1 body typography")

    require_contains(errors, "styles/qingyang-components.css", ".qy-table-container", "table container compatibility")
    require_contains(errors, "styles/qingyang-components.css", ".qy-pagination__btn", "pagination button compatibility")
    require_contains(errors, "styles/qingyang-components.css", ".qy-btn--small", "button size alias")
    require_contains(errors, "styles/qingyang-forms.css", ".qy-input--sm", "input size alias")

    require_contains(errors, "styles/README.md", "推荐入口", "recommended stylesheet entry")
    require_contains(errors, "styles/README.md", "组件 API 兼容说明", "component API compatibility notes")
    require_contains(errors, "qingyang-hro-design-system.md", "Canonical CSS 入口", "canonical CSS entry section")

    require_contains(errors, "prototype/reconciliation/summary.html", "../../styles/qingyang-design-system.css", "combined design-system link")
    require_contains(errors, "prototype/reconciliation/unified.html", "../../styles/qingyang-design-system.css", "combined design-system link")
    require_not_contains(errors, "prototype/reconciliation/unified.html", "--qy-primary-50: #EFF6FF", "inline qy token block")

    require_regex(
        errors,
        "styles/qingyang-components.css",
        r"\.qy-table-wrapper,\s*\n\.qy-table-container",
        "shared table wrapper/container rule",
    )

    if errors:
        print("Design system check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Design system check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
