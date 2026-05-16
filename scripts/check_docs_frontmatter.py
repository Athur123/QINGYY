#!/usr/bin/env python3
"""Check Obsidian frontmatter for Qingyang docs.

This checker is intentionally scoped to changed or explicitly supplied files by
default, so historical Markdown debt does not block unrelated work.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_PREFIXES = (
    Path("docs/HOME.md"),
    Path("docs/superpowers/specs"),
    Path("docs/superpowers/plans"),
    Path("docs/superpowers/prd"),
    Path("docs/manuals"),
    Path("docs/reference"),
)

REQUIRED_KEYS = (
    "title",
    "module",
    "type",
    "status",
    "owner",
    "updated",
    "source_of_truth",
)

VALID_TYPES = {
    "home",
    "spec",
    "plan",
    "prd",
    "guide",
    "reference",
    "note",
    "decision",
    "readme",
    "adr",
    "index",
}

VALID_STATUSES = {
    "draft",
    "active",
    "deprecated",
    "archived",
    "done",
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BOOL_RE = re.compile(r"^(true|false)$", re.IGNORECASE)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def rel(path: Path) -> Path:
    try:
        return path.resolve().relative_to(ROOT)
    except ValueError:
        return path


def is_target(path: Path) -> bool:
    if path.suffix != ".md":
        return False
    relative = rel(path)
    for prefix in DOC_PREFIXES:
        if relative == prefix or relative.is_relative_to(prefix):
            return True
    return False


def git_files(args: list[str]) -> list[Path]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or f"git {' '.join(args)} failed")
    return [ROOT / line for line in result.stdout.splitlines() if line.strip()]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"{rel(path)} missing YAML frontmatter at file start")

    end = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = idx
            break
    if end is None:
        fail(f"{rel(path)} has unterminated YAML frontmatter")

    data: dict[str, str] = {}
    for line_no, line in enumerate(lines[1:end], start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            fail(f"{rel(path)}:{line_no} invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            fail(f"{rel(path)}:{line_no} has empty frontmatter key")
        if key in data:
            fail(f"{rel(path)}:{line_no} duplicates frontmatter key: {key}")
        data[key] = value
    return data


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = parse_frontmatter(path)
    relative = rel(path)

    for key in REQUIRED_KEYS:
        if key not in data or data[key] == "":
            errors.append(f"{relative} missing required frontmatter key: {key}")

    doc_type = data.get("type", "")
    if doc_type and doc_type not in VALID_TYPES:
        errors.append(f"{relative} has invalid type: {doc_type}")

    status = data.get("status", "")
    if status and status not in VALID_STATUSES:
        errors.append(f"{relative} has invalid status: {status}")

    updated = data.get("updated", "")
    if updated and not DATE_RE.match(updated):
        errors.append(f"{relative} has invalid updated date: {updated}")

    source_of_truth = data.get("source_of_truth", "")
    if source_of_truth and not BOOL_RE.match(source_of_truth):
        errors.append(f"{relative} has invalid source_of_truth: {source_of_truth}")

    text = path.read_text(encoding="utf-8")
    if "file:///Users/" in text:
        errors.append(f"{relative} contains local file:///Users/ absolute link")

    return errors


def collect_files(args: argparse.Namespace) -> list[Path]:
    if args.staged:
        files = git_files(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    elif args.changed:
        files = git_files(["diff", "--name-only", "--diff-filter=ACMR"])
        files += git_files(["ls-files", "--others", "--exclude-standard"])
    elif args.strict:
        files = [
            path
            for base in (
                ROOT / "docs" / "HOME.md",
                ROOT / "docs" / "superpowers" / "specs",
                ROOT / "docs" / "superpowers" / "plans",
                ROOT / "docs" / "superpowers" / "prd",
                ROOT / "docs" / "manuals",
                ROOT / "docs" / "reference",
            )
            for path in ([base] if base.is_file() else base.rglob("*.md"))
        ]
    else:
        files = [ROOT / item for item in args.files]

    unique: dict[Path, None] = {}
    for path in files:
        if path.exists() and is_target(path):
            unique[path.resolve()] = None
    return sorted(unique)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="Markdown files to check")
    parser.add_argument("--staged", action="store_true", help="check staged target docs")
    parser.add_argument("--changed", action="store_true", help="check changed and untracked target docs")
    parser.add_argument("--strict", action="store_true", help="check all target docs")
    args = parser.parse_args()

    modes = sum(bool(value) for value in (args.staged, args.changed, args.strict))
    if modes > 1:
        fail("use only one of --staged, --changed, or --strict")
    if not args.files and modes == 0:
        print("No files supplied. Use --changed, --staged, --strict, or pass Markdown files.")
        return

    files = collect_files(args)
    if not files:
        print("PASS: no target docs to check")
        return

    errors: list[str] = []
    for path in files:
        errors.extend(check_file(path))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        sys.exit(1)

    checked = ", ".join(str(rel(path)) for path in files)
    print(f"PASS: docs frontmatter checks ({checked})")


if __name__ == "__main__":
    main()
