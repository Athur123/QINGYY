---
title: 动态记录筛选条件移除“变更字段”
date: 2026-04-22
scope: prototype/employee-detail-redesign.html
---

## 背景

动态记录（Timeline）顶部筛选区当前包含：时间、操作类型、操作人、变更字段。由于当前原型未实现“变更字段”的筛选逻辑，该筛选项属于冗余控件，需要移除以简化交互。

## 目标

- 筛选区移除“变更字段”下拉框
- 页面不保留任何与“变更字段筛选”相关的 UI/占位逻辑

## 非目标

- 不新增或完善任何筛选逻辑（本次仅做 UI 简化）
- 不调整其他筛选项（时间/操作类型/操作人保持不变）

## 方案

- 直接删除 `prototype/employee-detail-redesign.html` 中 `aria-label="筛选变更字段"` 的 `<select>` 节点及其 `<option>` 子项
- 保留 `.timeline-filters` 的现有布局；删除一个控件后，flex 布局自动收缩对齐

## 验收标准

- 页面筛选区仅保留：时间（month input）、操作类型（select）、操作人（select）
- 全文件中不再存在 `aria-label="筛选变更字段"` / `全部变更字段` 文案
