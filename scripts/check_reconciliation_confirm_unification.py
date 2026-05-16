#!/usr/bin/env python3
"""Static regression checks for reconciliation confirm-flow unification."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "prototype" / "reconciliation" / "unified.html"
SUMMARY_HTML = ROOT / "prototype" / "reconciliation" / "summary.html"
DOCS = [
    ROOT / "docs" / "superpowers" / "specs" / "reconciliation" / "type-month-matching.md",
    ROOT / "docs" / "superpowers" / "prd" / "reconciliation" / "reconciliation.md",
    ROOT / "docs" / "superpowers" / "plans" / "reconciliation" / "v1-complete-plan.md",
    ROOT / "docs" / "superpowers" / "plans" / "reconciliation" / "development-test-handoff.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def function_body(text: str, name: str) -> str:
    marker = f"function {name}("
    start = text.find(marker)
    require(start >= 0, f"missing function {name}")
    brace = text.find("{", start)
    require(brace >= 0, f"missing function body for {name}")
    depth = 0
    for idx in range(brace, len(text)):
        if text[idx] == "{":
            depth += 1
        elif text[idx] == "}":
            depth -= 1
            if depth == 0:
                return text[brace + 1 : idx]
    fail(f"unterminated function {name}")
    return ""


def main() -> None:
    html = HTML.read_text(encoding="utf-8")
    summary_html = SUMMARY_HTML.read_text(encoding="utf-8")
    doc_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)

    require("手工核对" not in html, "prototype must not expose separate manual-check wording")
    forbidden_direct_match = [
        "唯一 1:1 也只进入 `PENDING`",
        "| 唯一 1:1 金额一致 | 进入 PENDING",
        "S1 | 唯一 1:1 自动识别待确认",
        "Pass 1：唯一 1:1 自动识别为 `PENDING` 候选",
    ]
    for phrase in forbidden_direct_match:
        require(phrase not in doc_text, f"docs must not retain old direct-match phrase: {phrase}")
    require("applyAutoMatch()" not in doc_text, "docs must not retain old applyAutoMatch() implementation path")
    require("组合合计金额相等\n   - 进入 PENDING" not in doc_text, "docs must not describe auto-created combination pending groups")
    require("汇缴" in doc_text and "自动进入 `MATCHED`" in doc_text, "docs must state huijiao unique 1:1 auto-enters MATCHED")

    execute_body = function_body(html, "executeMatching")
    require("sa.length===1&&la.length===1" in execute_body, "cannot find unique 1:1 branch in executeMatching")
    require("sr.feeType===BILL_TYPES.HUIJIAO" in execute_body, "unique 1:1 branch must distinguish huijiao records")
    require("!sr.forcePending" in execute_body, "huijiao auto match must respect forcePending")
    require("applyAutoMatchedPair(sr,lr,amt)" in execute_body, "huijiao unique 1:1 branch must auto-create matched relation")
    require("applyPendingCandidate(sa,la,amt,'auto_candidate')" in execute_body, "non-huijiao unique 1:1 branch must remain pending candidate")

    require("applyManualCombinationPending(sys,led)" not in execute_body, "executeMatching must not auto-create combination pending groups")

    require("matchGroupId" in html, "prototype should use unified matchGroupId relation wording/state")
    require("openPairingDrawerForSelection" in html, "batch-selected records must open the unified pairing drawer")
    require("批量确认核对" in html, "batch confirm button must use clear batch confirm wording")
    require("确认所选" not in html, "prototype must not use ambiguous confirm-selected wording")
    require("确认所选" not in doc_text, "active reconciliation docs must not use ambiguous confirm-selected wording")
    require("批量取消核对" in html, "batch cancel button must use clear batch cancel wording")
    require("取消确认" not in html, "prototype must not use ambiguous cancel-confirm wording")
    require("取消确认" not in doc_text, "active reconciliation docs must not use ambiguous cancel-confirm wording")
    require("doCancelMatch(\\''+r.id+'\\')\">取消核对</button>" in html, "matched row action must use cancel-reconciliation wording")
    require("doCancelMatch(\\''+r.id+'\\')\">取消</button>" not in html, "matched row action must not use ambiguous cancel wording")
    require("data-confirm-role=\"'+role+'\"" in html, "drawer must distinguish selected and candidate-side records")
    require("共同核对信息" in html, "pairing drawer must extract shared person/type/period context")
    require("getConfirmContextInfo" in html, "pairing drawer must derive shared confirmation context")
    pending_group_body = function_body(html, "buildPairingGroupFromPending")
    require(
        "group.systemRecords.length===1&&group.ledgerRecords.length===1" in pending_group_body,
        "pending 1:1 confirm drawer must detect one-to-one groups",
    )
    require(
        "selectedSystemIds:isOneToOne?group.systemRecords.map" in pending_group_body
        and "selectedLedgerIds:isOneToOne?group.ledgerRecords.map" in pending_group_body,
        "pending 1:1 confirm drawer must preselect both system and ledger records",
    )
    find_group_body = function_body(html, "findPairingGroup")
    require(
        "buildPairingGroupFromPending(group,id," in find_group_body,
        "findPairingGroup must preserve pending group selection defaults",
    )
    label_body = function_body(html, "renderConfirmRecordLabel")
    require("明细编码" in label_body, "record labels must explicitly show detail code")
    require("r.name" not in label_body, "record labels should not repeat shared person name")
    require("r.insuranceType" not in label_body, "record labels should not repeat shared insurance type")
    require("r.feePeriod" not in label_body and "r.billingMonth" not in label_body, "record labels should not repeat shared fee period")
    require("系统合计" in html and "台账合计" in html, "drawer must show total validation")

    require(
        "captureMatchRestoreSnapshot" in html and "restoreMatchRestoreSnapshot" in html,
        "cancel reconciliation must restore records from pre-match snapshots",
    )
    require(
        "restoreRecordsFromMatchGroup" in html,
        "match-group cancellation must restore the whole group from original state",
    )
    require(
        "状态已恢复至核对前原始状态" in html,
        "cancel success toast must state original-state restoration",
    )
    forbidden_restore_phrases = [
        "整组系统侧和台账侧记录一起恢复为待确认状态",
        "同一 `matchGroupId` 下的系统侧和台账侧记录一起恢复为待确认",
        "系统侧按原业务类型恢复为 `PENDING` 或 `UNMATCHED`",
        "MATCHED → 原业务状态",
        "取消后统一恢复 PENDING",
        "状态已恢复为待确认",
    ]
    for phrase in forbidden_restore_phrases:
        require(phrase not in doc_text and phrase not in html, f"docs/prototype must not retain old cancel-restore wording: {phrase}")
    require("恢复至核对前原始状态" in doc_text, "docs must state cancel reconciliation restores pre-match original state")
    require("| UNMATCHED | **确认核对** |" in doc_text, "system-side UNMATCHED single-row action must be confirm reconciliation")
    require("| DIFF | **确认核对** |" in doc_text, "system-side DIFF single-row action must be confirm reconciliation")
    require(
        "强制核对仅保留在系统侧批量操作栏" in doc_text,
        "docs must state force reconciliation is batch-bar only, not a high-frequency single-row action",
    )

    require("汇缴唯一 1:1" in doc_text and "自动进入 `MATCHED`" in doc_text, "docs must state huijiao unique 1:1 enters MATCHED")
    require("确认核对关系" in doc_text or "匹配组" in doc_text, "docs must describe unified confirm relation")
    require("一对多、多对一、多对多" in doc_text, "docs must cover 1:N, N:1 and N:N confirmation")

    require("function getPageContext()" in html, "detail page must expose a page context helper")
    require("function recordMatchesPageContext(" in html, "detail records must be filtered by page context")
    require("function getActiveSystemRecords()" in html, "detail page must scope system records to current context")
    require("function getActiveLedgerRecords()" in html, "detail page must scope ledger records to current context")
    require("function getEffectivePayableMonth(" in html, "matching key must use effective payable month")
    require("getEffectivePayableMonth(r,'system')" in html, "system matching key must use current-context payable month")
    require("getEffectivePayableMonth(r,'ledger')" in html, "ledger matching key must use ledger billing month")
    require("DIFF_TYPE.AMOUNT_MISMATCH" in html, "matching engine must classify amount-mismatch differences")
    require("diffType=DIFF_TYPE.AMOUNT_MISMATCH" in html, "amount-mismatch branch must assign AMOUNT_MISMATCH")
    require(
        "systemRecords.forEach(function(r){ r.matchStatus='UNMATCHED'" not in html,
        "executeMatching must not reset all system records globally",
    )
    require(
        "ledgerRecords.forEach(function(r){ r.matchStatus='UNMATCHED'" not in html,
        "executeMatching must not reset all ledger records globally",
    )
    sys_batch_body = function_body(html, "updateSystemBatchButtons")
    led_batch_body = function_body(html, "updateLedgerBatchButtons")
    require(
        "r.matchStatus===MATCH_STATUS.MATCHED&&!r.archived&&r.matchStatus!==MATCH_STATUS.PAID" in sys_batch_body,
        "system batch cancel button must only enable for cancellable matched records",
    )
    require(
        "r.matchStatus===MATCH_STATUS.MATCHED&&!r.archived&&r.matchStatus!==MATCH_STATUS.PAID" in led_batch_body,
        "ledger batch cancel button must only enable for cancellable matched records",
    )

    require("function getEffectivePayableMonth(" in summary_html, "summary page must use effective payable month helper")
    require("function makeSummaryGroupKey(" in summary_html, "summary page must use spec-aligned group key helper")
    require("feePeriod || '')" not in function_body(summary_html, "makeSummaryGroupKey"), "summary matching key must not include feePeriod")
    require("totalPending += result.systemPending" in summary_html, "summary batch result must accumulate pending counts")
    require("totalPending += 0" not in summary_html, "summary page must not keep simplified pending accumulator")

    prd = (ROOT / "docs" / "superpowers" / "prd" / "reconciliation" / "reconciliation.md").read_text(encoding="utf-8")
    require("版本：v2.2" in prd and "| 当前版本 | v2.2 |" in prd, "PRD version must be updated to v2.2")
    require("日期：2026-05-15" in prd and "| 最后更新日期 | 2026-05-15 |" in prd, "PRD update date must be 2026-05-15")

    print("PASS: reconciliation confirm-flow unification checks")


if __name__ == "__main__":
    main()
