# Reconciliation Index

对账复核模块当前已经收口为一条明确主线：`summary.html + unified.html + type-month-matching.md`。

## Prototype Entry

- List-level entry:
  - `/Users/athur/PycharmProjects/qyy/prototype/reconciliation/summary.html`
- Detail-level entry:
  - `/Users/athur/PycharmProjects/qyy/prototype/reconciliation/unified.html`
- Legacy page:
  - `/Users/athur/PycharmProjects/qyy/prototype/reconciliation/obsolete/index.html` (obsolete, archived only, do not use as current prototype)

## Specs

- Complete primary spec:
  - `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/type-month-matching.md`
- Supporting import/input spec:
  - `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/ledger-import.md`
- Earlier background/base design:
  - `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/reconciliation-design.md`

## Plans

- Current implementation-plan anchors:
  - `/Users/athur/PycharmProjects/qyy/docs/superpowers/plans/reconciliation/v1-complete-plan.md`
  - `/Users/athur/PycharmProjects/qyy/docs/superpowers/plans/reconciliation/development-test-handoff.md`

## Reference Assets

- `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/社保台账导入模板-长表格式.csv`
- `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/社保台账导入模板-宽表格式.csv`

## Source of Truth

- `type-month-matching.md` is the only complete source of truth for:
  - matching rules
  - field semantics
  - status machine
  - page interactions
  - archive and paid-state behavior
- If any other reconciliation document conflicts with it, follow `type-month-matching.md`.

特别说明：

- 如果你要理解“匹配算法怎么判定”，先看 `type-month-matching.md` 的 `匹配算法` 章节
- 如果你要理解“哪些输入会影响匹配结果”，再看 `ledger-import.md` 的“导入校验与标准化”“导入后进入主 spec 的方式”
- 如果你要理解“研发怎么拆任务”，再看 `v1-complete-plan.md` 的 `Task 3`

## Reading Order

Recommended order for new collaborators:

1. Read `type-month-matching.md` to understand the current full model.
2. Re-read the `匹配算法` section in `type-month-matching.md` if your question is about matching branches, amount mismatch, forcePending, or fill-back behavior.
3. Read `ledger-import.md` for import/input rules and customer-facing data preparation.
3. Read `reconciliation-design.md` only for early background and the original design context.
4. Read `v1-complete-plan.md` for the current implementation breakdown.
5. Read `development-test-handoff.md` if you need a direct engineering/testing kickoff checklist.
6. Open `summary.html` and `unified.html` to inspect the active prototype flow.

## Maintenance Notes

- Update `type-month-matching.md` first when reconciliation rules, fields, statuses, or interactions change.
- Update `ledger-import.md` when import requirements or file-preparation rules change.
- Keep `reconciliation-design.md` as background context unless the team explicitly wants to rewrite or retire it.
- If the prototype behavior changes, verify that `summary.html`, `unified.html`, and `type-month-matching.md` still describe the same flow.
