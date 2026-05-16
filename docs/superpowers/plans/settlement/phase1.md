---
title: 结算主体维度财务归属 - 阶段一：档案版本化与费用固化
module: settlement
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 结算主体维度财务归属 - 阶段一：档案版本化与费用固化

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立员工档案版本化机制，实现费用归属固化，为后续各模块隔离提供数据基础。

**Architecture:** 创建数据库迁移脚本定义新版本表和费用固化字段，创建交互原型演示档案版本管理和费用归属查询的 UI 交互。

**Tech Stack:** 
- SQL 迁移脚本（MySQL/PostgreSQL 兼容）
- 前端原型：HTML + CSS（复用青阳云设计系统）
- JavaScript：原生，模拟数据

---

## 文件结构

```
prototype/
├── employee-archive-version.html      # 新建：员工档案版本管理原型
└── cost-attribution-demo.html          # 新建：费用归属固化演示原型

docs/superpowers/sql/
└── 2026-04-25-settlement-entity-migration.sql  # 新建：数据库迁移脚本

docs/superpowers/specs/
└── 2026-04-25-settlement-entity-financial-attribution-design.md  # 已存在：设计文档
```

---

## Task 1: 数据库迁移脚本

**Files:**
- Create: `docs/superpowers/sql/2026-04-25-settlement-entity-migration.sql`

- [ ] **Step 1: 创建员工档案版本表**

```sql
-- ============================================================
-- 员工档案版本表
-- 每次调动/重新入职/客户变更/合同变更时生成新版本
-- ============================================================
CREATE TABLE IF NOT EXISTS `employee_archive_version` (
    `version_id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '版本号',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `settlement_entity_id` BIGINT DEFAULT NULL COMMENT '结算主体（管理归属）',
    `customer_id` BIGINT DEFAULT NULL COMMENT '所属客户',
    `contract_id` BIGINT DEFAULT NULL COMMENT '所属合同',
    `project_id` BIGINT DEFAULT NULL COMMENT '所属项目',
    `insurance_entity_id` BIGINT DEFAULT NULL COMMENT '参保主体（保险关系归属）',
    `start_date` DATE NOT NULL COMMENT '生效开始日期',
    `end_date` DATE DEFAULT NULL COMMENT '生效结束日期，NULL表示当前版本',
    `change_reason` VARCHAR(50) DEFAULT NULL COMMENT '变更原因：transfer-调动, rehire-重新入职, customer_change-客户变更, contract_change-合同变更',
    `change_date` DATE DEFAULT NULL COMMENT '变更日期',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `created_by` BIGINT DEFAULT NULL COMMENT '创建人',
    INDEX `idx_employee` (`employee_id`),
    INDEX `idx_settlement_entity` (`settlement_entity_id`),
    INDEX `idx_date_range` (`start_date`, `end_date`),
    INDEX `idx_settlement_date` (`settlement_entity_id`, `start_date`, `end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='员工档案版本表';
```

- [ ] **Step 2: 创建结算历史表**

```sql
-- ============================================================
-- 结算历史表（从档案版本表派生的快速查询表）
-- 用于快速查询某结算主体下曾管理过的员工
-- ============================================================
CREATE TABLE IF NOT EXISTS `settlement_history` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `settlement_entity_id` BIGINT NOT NULL COMMENT '曾属于的结算主体',
    `start_date` DATE NOT NULL COMMENT '加入时间',
    `end_date` DATE DEFAULT NULL COMMENT '调出时间',
    `change_type` VARCHAR(50) DEFAULT NULL COMMENT '变动类型：transfer-调动, rehire-重新入职',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_employee` (`employee_id`),
    INDEX `idx_settlement_entity` (`settlement_entity_id`),
    INDEX `idx_entity_date` (`settlement_entity_id`, `start_date`, `end_date`),
    UNIQUE KEY `uk_employee_entity_start` (`employee_id`, `settlement_entity_id`, `start_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='结算历史表';
```

- [ ] **Step 3: 费用明细表增加固化字段**

```sql
-- ============================================================
-- 费用明细表增加归档字段
-- 费用产生时固化结算主体/客户/合同/项目，不随员工调动变更
-- ============================================================

-- 增加档案版本快照字段
ALTER TABLE `cost_detail` 
    ADD COLUMN IF NOT EXISTS `archive_version_id` BIGINT DEFAULT NULL COMMENT '产生费用时的档案版本号',
    ADD COLUMN IF NOT EXISTS `settlement_entity_id_snapshot` BIGINT DEFAULT NULL COMMENT '费用归属的结算主体（固化）',
    ADD COLUMN IF NOT EXISTS `customer_id_snapshot` BIGINT DEFAULT NULL COMMENT '费用归属的客户（固化）',
    ADD COLUMN IF NOT EXISTS `contract_id_snapshot` BIGINT DEFAULT NULL COMMENT '费用归属的合同（固化）',
    ADD COLUMN IF NOT EXISTS `project_id_snapshot` BIGINT DEFAULT NULL COMMENT '费用归属的项目（固化）',
    ADD COLUMN IF NOT EXISTS `insurance_entity_id` BIGINT DEFAULT NULL COMMENT '参保主体',
    ADD INDEX `idx_settlement_snapshot` (`settlement_entity_id_snapshot`),
    ADD INDEX `idx_customer_snapshot` (`customer_id_snapshot`),
    ADD INDEX `idx_version` (`archive_version_id`);
```

- [ ] **Step 4: 创建账单明细固化结构**

```sql
-- ============================================================
-- 账单表结构（如不存在则创建）
-- 账单生成后明细锁定，不受员工调动影响
-- ============================================================
CREATE TABLE IF NOT EXISTS `bill` (
    `bill_id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '账单ID',
    `settlement_entity_id` BIGINT NOT NULL COMMENT '结算主体',
    `customer_id` BIGINT NOT NULL COMMENT '客户',
    `bill_month` VARCHAR(7) NOT NULL COMMENT '账单月份（YYYY-MM）',
    `total_amount` DECIMAL(12,2) NOT NULL DEFAULT 0.00 COMMENT '总金额',
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态：pending-待确认, confirmed-已确认, paid-已结清',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
    `confirmed_at` TIMESTAMP NULL DEFAULT NULL COMMENT '确认时间',
    `created_by` BIGINT DEFAULT NULL COMMENT '创建人',
    INDEX `idx_settlement_month` (`settlement_entity_id`, `bill_month`),
    INDEX `idx_customer_month` (`customer_id`, `bill_month`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='账单表';

CREATE TABLE IF NOT EXISTS `bill_detail` (
    `detail_id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '明细ID',
    `bill_id` BIGINT NOT NULL COMMENT '关联账单',
    `cost_id` BIGINT DEFAULT NULL COMMENT '关联费用',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `archive_version_id` BIGINT DEFAULT NULL COMMENT '费用产生时的版本号（固化）',
    `settlement_entity_id` BIGINT NOT NULL COMMENT '结算主体（固化）',
    `customer_id` BIGINT NOT NULL COMMENT '客户（固化）',
    `contract_id` BIGINT DEFAULT NULL COMMENT '合同（固化）',
    `project_id` DEFAULT NULL COMMENT '项目（固化）',
    `amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '金额',
    `insurance_type` VARCHAR(50) DEFAULT NULL COMMENT '险种名称',
    `is_locked` TINYINT(1) DEFAULT 0 COMMENT '是否已锁定（账单生成后锁定）',
    INDEX `idx_bill` (`bill_id`),
    INDEX `idx_employee` (`employee_id`),
    INDEX `idx_settlement` (`settlement_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='账单明细表';
```

- [ ] **Step 5: 创建付款申请表结构**

```sql
-- ============================================================
-- 付款申请表
-- 支持合并付款，财务归属到发起主体
-- ============================================================
CREATE TABLE IF NOT EXISTS `payment_request` (
    `payment_id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '付款申请ID',
    `settlement_entity_id` BIGINT NOT NULL COMMENT '发起申请的结算主体',
    `insurance_entity_id` BIGINT NOT NULL COMMENT '收款方参保主体',
    `total_amount` DECIMAL(12,2) NOT NULL DEFAULT 0.00 COMMENT '付款总金额',
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态：pending-待审批, approved-已审批, paid-已缴费, rejected-已拒绝',
    `is_merge` TINYINT(1) DEFAULT 0 COMMENT '是否合并付款',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
    `approved_at` TIMESTAMP NULL DEFAULT NULL COMMENT '审批时间',
    `created_by` BIGINT DEFAULT NULL COMMENT '申请人',
    INDEX `idx_settlement` (`settlement_entity_id`),
    INDEX `idx_insurance` (`insurance_entity_id`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='付款申请表';

CREATE TABLE IF NOT EXISTS `payment_request_detail` (
    `detail_id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '明细ID',
    `payment_id` BIGINT NOT NULL COMMENT '关联付款申请',
    `cost_id` BIGINT DEFAULT NULL COMMENT '关联费用',
    `settlement_entity_id` BIGINT NOT NULL COMMENT '费用归属的结算主体（固化）',
    `internal_transfer_flag` TINYINT(1) DEFAULT 0 COMMENT '是否内部划转（合并付款时其他主体的费用）',
    `amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '金额',
    INDEX `idx_payment` (`payment_id`),
    INDEX `idx_settlement` (`settlement_entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='付款申请明细表';
```

- [ ] **Step 6: 历史数据迁移脚本**

```sql
-- ============================================================
-- 历史数据迁移
-- 从现有员工异动记录中提取历史结算关系
-- ============================================================

-- 步骤 1: 从异动记录生成档案版本
-- 假设现有 employee_transfer 表记录了调动历史
INSERT INTO `employee_archive_version` 
    (`employee_id`, `settlement_entity_id`, `customer_id`, `contract_id`, 
     `project_id`, `insurance_entity_id`, `start_date`, `end_date`, 
     `change_reason`, `change_date`, `created_by`)
SELECT 
    et.employee_id,
    et.target_settlement_entity_id AS settlement_entity_id,
    et.target_customer_id AS customer_id,
    et.target_contract_id AS contract_id,
    et.target_project_id AS project_id,
    e.insurance_entity_id,  -- 参保主体不变
    et.transfer_date AS start_date,
    NULL AS end_date,  -- 当前版本
    'transfer' AS change_reason,
    et.transfer_date AS change_date,
    et.operator_id AS created_by
FROM `employee_transfer` et
LEFT JOIN `employee` e ON et.employee_id = e.employee_id
WHERE et.status = 'success'
ORDER BY et.transfer_date ASC;

-- 步骤 2: 为每个员工生成初始版本（入职时）
INSERT INTO `employee_archive_version`
    (`employee_id`, `settlement_entity_id`, `customer_id`, `contract_id`,
     `project_id`, `insurance_entity_id`, `start_date`, `end_date`,
     `change_reason`, `change_date`, `created_by`)
SELECT 
    e.employee_id,
    e.settlement_entity_id,
    e.customer_id,
    e.contract_id,
    e.project_id,
    e.insurance_entity_id,
    e.hire_date AS start_date,
    -- end_date 为第一次调动日期，如无调动则为 NULL
    (SELECT MIN(et.transfer_date) FROM `employee_transfer` et 
     WHERE et.employee_id = e.employee_id AND et.status = 'success') AS end_date,
    'hire' AS change_reason,
    e.hire_date AS change_date,
    e.created_by
FROM `employee` e
WHERE NOT EXISTS (
    SELECT 1 FROM `employee_archive_version` v 
    WHERE v.employee_id = e.employee_id
);

-- 步骤 3: 生成结算历史
INSERT INTO `settlement_history`
    (`employee_id`, `settlement_entity_id`, `start_date`, `end_date`, `change_type`)
SELECT DISTINCT
    v.employee_id,
    v.settlement_entity_id,
    v.start_date,
    v.end_date,
    v.change_reason AS change_type
FROM `employee_archive_version` v
WHERE v.change_reason IN ('transfer', 'rehire')
ORDER BY v.employee_id, v.start_date;

-- 步骤 4: 固化现有费用明细的归属
UPDATE `cost_detail` c
JOIN `employee` e ON c.employee_id = e.employee_id
SET 
    c.archive_version_id = NULL,  -- 历史费用无版本号，需要后续人工确认
    c.settlement_entity_id_snapshot = e.settlement_entity_id,
    c.customer_id_snapshot = e.customer_id,
    c.contract_id_snapshot = e.contract_id,
    c.project_id_snapshot = e.project_id,
    c.insurance_entity_id = e.insurance_entity_id
WHERE c.archive_version_id IS NULL;
```

- [ ] **Step 7: 创建回滚脚本**

```sql
-- ============================================================
-- 回滚脚本（迁移失败时使用）
-- ============================================================

-- 删除新增的索引
DROP INDEX IF EXISTS `idx_settlement_snapshot` ON `cost_detail`;
DROP INDEX IF EXISTS `idx_customer_snapshot` ON `cost_detail`;
DROP INDEX IF EXISTS `idx_version` ON `cost_detail`;

-- 删除新增的列
ALTER TABLE `cost_detail` 
    DROP COLUMN IF EXISTS `archive_version_id`,
    DROP COLUMN IF EXISTS `settlement_entity_id_snapshot`,
    DROP COLUMN IF EXISTS `customer_id_snapshot`,
    DROP COLUMN IF EXISTS `contract_id_snapshot`,
    DROP COLUMN IF EXISTS `project_id_snapshot`,
    DROP COLUMN IF EXISTS `insurance_entity_id`;

-- 删除新表
DROP TABLE IF EXISTS `payment_request_detail`;
DROP TABLE IF EXISTS `payment_request`;
DROP TABLE IF EXISTS `bill_detail`;
DROP TABLE IF EXISTS `bill`;
DROP TABLE IF EXISTS `settlement_history`;
DROP TABLE IF EXISTS `employee_archive_version`;
```

- [ ] **Step 8: 提交**

```bash
git add docs/superpowers/sql/2026-04-25-settlement-entity-migration.sql
git commit -m "feat: 结算主体维度财务归属 - 阶段一数据库迁移脚本

- 创建 employee_archive_version 员工档案版本表
- 创建 settlement_history 结算历史表
- 费用明细表增加固化字段
- 创建账单和付款申请表结构
- 包含历史数据迁移和回滚脚本

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 2: 员工档案版本管理原型

**Files:**
- Create: `prototype/employee-archive-version.html`

- [ ] **Step 1: 创建基础页面结构**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>员工档案版本管理 - 青阳云HR SaaS</title>
    <link rel="stylesheet" href="../styles/qingyang-variables.css">
    <link rel="stylesheet" href="../styles/qingyang-components.css">
    <link rel="stylesheet" href="../styles/qingyang-forms.css">
    <style>
        .page-container { max-width: 1400px; margin: 0 auto; padding: 24px; }
        .page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
        .page-title { font-size: 18px; font-weight: 600; }

        /* 员工信息卡片 */
        .employee-hero {
            background: var(--qy-bg-primary); border-radius: var(--qy-radius-lg);
            border: 1px solid var(--qy-border-light); padding: 24px; margin-bottom: 24px;
            display: grid; grid-template-columns: auto 1fr auto; gap: 24px; align-items: center;
        }
        .employee-avatar {
            width: 56px; height: 56px; border-radius: 50%;
            background: var(--qy-primary-50); display: flex; align-items: center;
            justify-content: center; font-size: 24px; color: var(--qy-primary-600); font-weight: 600;
        }
        .employee-name { font-size: 20px; font-weight: 600; margin-bottom: 4px; }
        .employee-meta { display: flex; gap: 16px; font-size: 13px; color: var(--qy-text-secondary); }
        .employee-meta span { display: flex; align-items: center; gap: 4px; }

        /* 版本时间线 */
        .version-timeline { position: relative; padding-left: 32px; }
        .version-timeline::before {
            content: ''; position: absolute; left: 12px; top: 0; bottom: 0;
            width: 2px; background: var(--qy-border);
        }
        .version-item {
            position: relative; margin-bottom: 16px;
            background: var(--qy-bg-primary); border: 1px solid var(--qy-border-light);
            border-radius: var(--qy-radius-md); overflow: hidden;
        }
        .version-item.current { border-color: var(--qy-primary-500); box-shadow: 0 0 0 1px var(--qy-primary-500); }
        .version-item::before {
            content: ''; position: absolute; left: -26px; top: 20px;
            width: 12px; height: 12px; border-radius: 50%;
            background: var(--qy-border); border: 2px solid var(--qy-bg-primary);
        }
        .version-item.current::before { background: var(--qy-primary-500); border-color: var(--qy-primary-100); }
        .version-header {
            padding: 12px 16px; display: flex; align-items: center; justify-content: space-between;
            background: var(--qy-bg-secondary); border-bottom: 1px solid var(--qy-border-light);
        }
        .version-badge {
            display: inline-flex; align-items: center; gap: 4px;
            padding: 2px 8px; border-radius: var(--qy-radius-full); font-size: 12px; font-weight: 500;
        }
        .version-badge.current { background: var(--qy-primary-50); color: var(--qy-primary-600); }
        .version-badge.historical { background: var(--qy-bg-tertiary); color: var(--qy-text-secondary); }
        .version-body { padding: 16px; }
        .version-field { display: grid; grid-template-columns: 120px 1fr; gap: 8px; margin-bottom: 8px; }
        .version-field:last-child { margin-bottom: 0; }
        .version-label { font-size: 12px; color: var(--qy-text-secondary); }
        .version-value { font-size: 13px; }

        /* 变更对比 */
        .change-diff {
            display: inline-flex; align-items: center; gap: 4px; padding: 2px 6px;
            border-radius: var(--qy-radius-sm); font-size: 12px;
        }
        .change-diff.old { background: var(--qy-error-50); color: var(--qy-error-600); text-decoration: line-through; }
        .change-diff.new { background: var(--qy-success-50); color: var(--qy-success-600); }
        .change-arrow { color: var(--qy-text-muted); margin: 0 4px; }

        /* 操作按钮组 */
        .action-bar {
            display: flex; gap: 8px; padding: 16px;
            border-top: 1px solid var(--qy-border-light);
        }

        /* 筛选面板 */
        .filter-bar {
            display: flex; gap: 12px; margin-bottom: 24px; align-items: center; flex-wrap: wrap;
        }
        .qy-select { min-width: 180px; }
    </style>
</head>
<body>
    <div class="page-container">
        <!-- 页面标题 -->
        <div class="page-header">
            <button class="qy-btn qy-btn--text" onclick="history.back()">← 返回</button>
            <h1 class="page-title">员工档案版本管理</h1>
        </div>

        <!-- 员工信息 -->
        <div class="employee-hero">
            <div class="employee-avatar">张</div>
            <div>
                <div class="employee-name">张三</div>
                <div class="employee-meta">
                    <span>📱 15827115531</span>
                    <span>🪪 421023199802058319</span>
                    <span>🏢 全职 · 正式 · 在职</span>
                </div>
            </div>
            <div>
                <button class="qy-btn qy-btn--primary" onclick="showTransferModal()">发起调动</button>
            </div>
        </div>

        <!-- 筛选 -->
        <div class="filter-bar">
            <span style="font-size: 13px; font-weight: 500;">筛选：</span>
            <select class="qy-select" id="filterEntity">
                <option value="">全部结算主体</option>
                <option value="1" selected>无锡一技信息科技有限公司</option>
                <option value="2">深圳青阳财税服务有限公司</option>
            </select>
            <select class="qy-select" id="filterStatus">
                <option value="">全部状态</option>
                <option value="current">当前版本</option>
                <option value="historical">历史版本</option>
            </select>
            <span style="font-size: 12px; color: var(--qy-text-secondary); margin-left: auto;">
                共 3 个版本
            </span>
        </div>

        <!-- 版本时间线 -->
        <div class="version-timeline" id="versionTimeline">
            <!-- 当前版本 -->
            <div class="version-item current" data-version="3">
                <div class="version-header">
                    <div>
                        <span class="version-badge current">● 当前版本</span>
                        <span style="font-size: 13px; font-weight: 500; margin-left: 8px;">V3</span>
                    </div>
                    <span style="font-size: 12px; color: var(--qy-text-secondary);">2026-04-01 至今</span>
                </div>
                <div class="version-body">
                    <div class="version-field">
                        <span class="version-label">结算主体</span>
                        <span class="version-value">深圳青阳财税服务有限公司</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">所属客户</span>
                        <span class="version-value">立人科技</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">所属合同</span>
                        <span class="version-value">立人服务协议</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">所属项目</span>
                        <span class="version-value">立人外包项目</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">参保主体</span>
                        <span class="version-value">深圳青阳人力资源服务有限公司</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">变更原因</span>
                        <span class="version-value">调动（从无锡一技 → 深圳青阳）</span>
                    </div>
                </div>
            </div>

            <!-- 历史版本 2 -->
            <div class="version-item" data-version="2">
                <div class="version-header">
                    <div>
                        <span class="version-badge historical">历史版本</span>
                        <span style="font-size: 13px; font-weight: 500; margin-left: 8px;">V2</span>
                    </div>
                    <span style="font-size: 12px; color: var(--qy-text-secondary);">2026-01-01 ~ 2026-03-31</span>
                </div>
                <div class="version-body">
                    <div class="version-field">
                        <span class="version-label">结算主体</span>
                        <span class="version-value">
                            <span class="change-diff old">无锡一技信息科技有限公司</span>
                        </span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">所属客户</span>
                        <span class="version-value">
                            <span class="change-diff old">优派人力</span>
                            <span class="change-arrow">→</span>
                            <span class="change-diff new">优派人力</span>
                        </span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">变更原因</span>
                        <span class="version-value">客户变更</span>
                    </div>
                    <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--qy-border-light);">
                        <span style="font-size: 12px; color: var(--qy-text-secondary);">该版本下的保险记录：</span>
                        <div style="display: flex; gap: 6px; margin-top: 4px;">
                            <span class="qy-tag qy-tag--success">养老保险 已参保</span>
                            <span class="qy-tag qy-tag--success">医疗保险 已参保</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 历史版本 1 -->
            <div class="version-item" data-version="1">
                <div class="version-header">
                    <div>
                        <span class="version-badge historical">历史版本</span>
                        <span style="font-size: 13px; font-weight: 500; margin-left: 8px;">V1（初始）</span>
                    </div>
                    <span style="font-size: 12px; color: var(--qy-text-secondary);">2026-02-02 ~ 2025-12-31</span>
                </div>
                <div class="version-body">
                    <div class="version-field">
                        <span class="version-label">结算主体</span>
                        <span class="version-value">无锡一技信息科技有限公司</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">所属客户</span>
                        <span class="version-value">优派人力</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">所属合同</span>
                        <span class="version-value">深圳外包服务合同A</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">所属项目</span>
                        <span class="version-value">深圳外包项目一</span>
                    </div>
                    <div class="version-field">
                        <span class="version-label">变更原因</span>
                        <span class="version-value">入职</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 筛选功能
        document.getElementById('filterEntity').addEventListener('change', function() {
            const val = this.value;
            document.querySelectorAll('.version-item').forEach(item => {
                if (!val) { item.style.display = ''; return; }
                // 模拟筛选逻辑
                item.style.display = '';
            });
        });

        document.getElementById('filterStatus').addEventListener('change', function() {
            const val = this.value;
            document.querySelectorAll('.version-item').forEach(item => {
                if (!val) { item.style.display = ''; return; }
                if (val === 'current') {
                    item.style.display = item.classList.contains('current') ? '' : 'none';
                } else if (val === 'historical') {
                    item.style.display = item.classList.contains('current') ? 'none' : '';
                }
            });
        });

        function showTransferModal() {
            alert('调动功能原型：选择新结算主体、客户、合同、项目，提交后生成新版本。');
        }
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交**

```bash
git add prototype/employee-archive-version.html
git commit -m "feat: 员工档案版本管理交互原型

- 版本时间线展示
- 当前/历史版本区分
- 变更前后对比显示
- 版本关联保险记录
- 筛选功能

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 3: 费用归属固化演示原型

**Files:**
- Create: `prototype/cost-attribution-demo.html`

- [ ] **Step 1: 创建费用归属演示页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>费用归属固化演示 - 青阳云HR SaaS</title>
    <link rel="stylesheet" href="../styles/qingyang-variables.css">
    <link rel="stylesheet" href="../styles/qingyang-components.css">
    <style>
        .page-container { max-width: 1400px; margin: 0 auto; padding: 24px; }
        .page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
        .page-title { font-size: 18px; font-weight: 600; }

        /* 场景说明 */
        .scenario-card {
            background: var(--qy-bg-primary); border: 1px solid var(--qy-border-light);
            border-radius: var(--qy-radius-lg); padding: 20px; margin-bottom: 24px;
            border-left: 4px solid var(--qy-primary-500);
        }
        .scenario-title { font-size: 14px; font-weight: 600; margin-bottom: 8px; }
        .scenario-desc { font-size: 13px; color: var(--qy-text-secondary); line-height: 1.6; }

        /* 双层模型展示 */
        .dual-model {
            display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;
        }
        .model-panel {
            background: var(--qy-bg-primary); border: 1px solid var(--qy-border-light);
            border-radius: var(--qy-radius-lg); overflow: hidden;
        }
        .model-header {
            padding: 14px 20px; background: var(--qy-bg-secondary);
            border-bottom: 1px solid var(--qy-border-light); font-weight: 600; font-size: 14px;
        }
        .model-header.payment { background: var(--qy-primary-50); color: var(--qy-primary-600); }
        .model-header.attribution { background: var(--qy-success-50); color: var(--qy-success-600); }
        .model-body { padding: 16px 20px; }

        /* 费用流水表 */
        .cost-table { width: 100%; border-collapse: collapse; font-size: 13px; }
        .cost-table th {
            text-align: left; padding: 10px 12px; background: var(--qy-bg-secondary);
            font-weight: 500; color: var(--qy-text-secondary); border-bottom: 1px solid var(--qy-border-light);
            font-size: 12px; white-space: nowrap;
        }
        .cost-table td {
            padding: 12px; border-bottom: 1px solid var(--qy-border-light); vertical-align: top;
        }
        .cost-table tr:last-child td { border-bottom: none; }
        .cost-table .frozen { background: var(--qy-warning-50); }
        .cost-table .frozen td { position: relative; }
        .frozen-badge {
            display: inline-flex; align-items: center; gap: 2px;
            padding: 1px 6px; border-radius: var(--qy-radius-sm);
            font-size: 11px; font-weight: 500; background: var(--qy-warning-100); color: var(--qy-warning-600);
        }

        /* 调动影响演示 */
        .transfer-impact {
            display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; margin-bottom: 24px;
            align-items: start;
        }
        .transfer-before, .transfer-after {
            background: var(--qy-bg-primary); border: 1px solid var(--qy-border-light);
            border-radius: var(--qy-radius-lg); padding: 20px;
        }
        .transfer-arrow {
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; color: var(--qy-primary-500); padding-top: 40px;
        }
        .transfer-label {
            font-size: 12px; color: var(--qy-text-secondary); margin-bottom: 8px;
            text-transform: uppercase; letter-spacing: 0.05em;
        }
        .transfer-entity {
            font-size: 14px; font-weight: 600; padding: 8px 12px;
            background: var(--qy-bg-secondary); border-radius: var(--qy-radius-sm); margin-bottom: 12px;
        }
        .transfer-costs { font-size: 13px; }
        .transfer-cost {
            display: flex; justify-content: space-between; padding: 6px 0;
            border-bottom: 1px solid var(--qy-border-light);
        }
        .transfer-cost:last-child { border-bottom: none; }
        .cost-amount { font-weight: 600; }

        /* 关键规则 */
        .rule-list { list-style: none; padding: 0; }
        .rule-item {
            display: flex; gap: 12px; padding: 12px 16px;
            border-bottom: 1px solid var(--qy-border-light);
        }
        .rule-item:last-child { border-bottom: none; }
        .rule-icon {
            width: 20px; height: 20px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: 600; flex-shrink: 0; margin-top: 1px;
        }
        .rule-icon.success { background: var(--qy-success-50); color: var(--qy-success-600); }
        .rule-icon.warning { background: var(--qy-warning-50); color: var(--qy-warning-600); }
        .rule-icon.info { background: var(--qy-primary-50); color: var(--qy-primary-600); }
        .rule-text { font-size: 13px; line-height: 1.5; }
    </style>
</head>
<body>
    <div class="page-container">
        <div class="page-header">
            <button class="qy-btn qy-btn--text" onclick="history.back()">← 返回</button>
            <h1 class="page-title">费用归属固化演示</h1>
        </div>

        <!-- 场景说明 -->
        <div class="scenario-card">
            <div class="scenario-title">📋 场景：员工张三调动前后的费用归属</div>
            <div class="scenario-desc">
                张三原属「无锡一技信息科技有限公司」，2026-04-01 调动至「深圳青阳财税服务有限公司」。<br>
                调动前在无锡参保了养老/医疗保险，调动后在深圳重新参保。关键问题：3月的费用归属哪个主体？退费归属哪个主体？
            </div>
        </div>

        <!-- 调动影响 -->
        <div class="transfer-impact">
            <div class="transfer-before">
                <div class="transfer-label">调动前（2026-01 ~ 2026-03）</div>
                <div class="transfer-entity">🏢 无锡一技信息科技有限公司</div>
                <div class="transfer-costs">
                    <div class="transfer-cost">
                        <span>养老保险</span>
                        <span class="cost-amount">¥1,200/月</span>
                    </div>
                    <div class="transfer-cost">
                        <span>医疗保险</span>
                        <span class="cost-amount">¥800/月</span>
                    </div>
                    <div class="transfer-cost" style="color: var(--qy-text-muted); font-style: italic;">
                        <span>→ 费用归属：无锡一技</span>
                        <span>（固化，不随调动变更）</span>
                    </div>
                </div>
            </div>

            <div class="transfer-arrow">→</div>

            <div class="transfer-after">
                <div class="transfer-label">调动后（2026-04 起）</div>
                <div class="transfer-entity">🏢 深圳青阳财税服务有限公司</div>
                <div class="transfer-costs">
                    <div class="transfer-cost">
                        <span>养老保险（新）</span>
                        <span class="cost-amount">¥1,500/月</span>
                    </div>
                    <div class="transfer-cost">
                        <span>医疗保险（新）</span>
                        <span class="cost-amount">¥900/月</span>
                    </div>
                    <div class="transfer-cost" style="color: var(--qy-text-muted); font-style: italic;">
                        <span>→ 费用归属：深圳青阳</span>
                        <span>（新主体新建保险关系）</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 双层模型 -->
        <div class="dual-model">
            <div class="model-panel">
                <div class="model-header payment">缴费层（参保主体维度）</div>
                <div class="model-body">
                    <table class="cost-table">
                        <thead>
                            <tr>
                                <th>参保主体</th>
                                <th>月份</th>
                                <th>应缴金额</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>深圳青阳人力资源</td>
                                <td>2026-03</td>
                                <td>¥6,000</td>
                                <td><span class="qy-tag qy-tag--success">已缴费</span></td>
                            </tr>
                            <tr>
                                <td>深圳青阳人力资源</td>
                                <td>2026-04</td>
                                <td>¥7,200</td>
                                <td><span class="qy-tag qy-tag--info">待缴费</span></td>
                            </tr>
                        </tbody>
                    </table>
                    <p style="font-size: 12px; color: var(--qy-text-secondary); margin-top: 12px;">
                        对外（社保局）的唯一出口，按参保主体统一缴费
                    </p>
                </div>
            </div>

            <div class="model-panel">
                <div class="model-header attribution">对账层（结算主体维度）</div>
                <div class="model-body">
                    <table class="cost-table">
                        <thead>
                            <tr>
                                <th>结算主体</th>
                                <th>月份</th>
                                <th>应收金额</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>无锡一技</td>
                                <td>2026-03</td>
                                <td>¥2,000</td>
                                <td><span class="qy-tag qy-tag--success">已结清</span></td>
                            </tr>
                            <tr>
                                <td>深圳青阳</td>
                                <td>2026-04</td>
                                <td>¥2,400</td>
                                <td><span class="qy-tag qy-tag--warning">待收款</span></td>
                            </tr>
                        </tbody>
                    </table>
                    <p style="font-size: 12px; color: var(--qy-text-secondary); margin-top: 12px;">
                        对内（客户）的收费依据，按结算主体分别收款
                    </p>
                </div>
            </div>
        </div>

        <!-- 费用流水 -->
        <div class="model-panel" style="margin-bottom: 24px;">
            <div class="model-header" style="background: var(--qy-bg-secondary);">费用流水明细</div>
            <div class="model-body" style="padding: 0;">
                <table class="cost-table">
                    <thead>
                        <tr>
                            <th>费用ID</th>
                            <th>员工</th>
                            <th>险种</th>
                            <th>月份</th>
                            <th>结算主体（固化）</th>
                            <th>参保主体</th>
                            <th>金额</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="frozen">
                            <td>C-001</td>
                            <td>张三</td>
                            <td>养老保险</td>
                            <td>2026-03</td>
                            <td>无锡一技</td>
                            <td>深圳青阳人力资源</td>
                            <td>¥1,200</td>
                            <td><span class="frozen-badge">🔒 已固化</span></td>
                        </tr>
                        <tr class="frozen">
                            <td>C-002</td>
                            <td>张三</td>
                            <td>医疗保险</td>
                            <td>2026-03</td>
                            <td>无锡一技</td>
                            <td>深圳青阳人力资源</td>
                            <td>¥800</td>
                            <td><span class="frozen-badge">🔒 已固化</span></td>
                        </tr>
                        <tr>
                            <td>C-003</td>
                            <td>张三</td>
                            <td>养老保险</td>
                            <td>2026-04</td>
                            <td>深圳青阳</td>
                            <td>深圳青阳人力资源</td>
                            <td>¥1,500</td>
                            <td><span class="qy-tag qy-tag--info">新生成</span></td>
                        </tr>
                        <tr>
                            <td>C-004</td>
                            <td>张三</td>
                            <td>医疗保险</td>
                            <td>2026-04</td>
                            <td>深圳青阳</td>
                            <td>深圳青阳人力资源</td>
                            <td>¥900</td>
                            <td><span class="qy-tag qy-tag--info">新生成</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 关键规则 -->
        <div class="model-panel">
            <div class="model-header" style="background: var(--qy-bg-secondary);">费用归属固化规则</div>
            <div class="model-body">
                <ul class="rule-list">
                    <li class="rule-item">
                        <span class="rule-icon success">✓</span>
                        <span class="rule-text"><strong>正常费用</strong>：产生时按员工档案版本固化归属，后续调动不影响已产生费用</span>
                    </li>
                    <li class="rule-item">
                        <span class="rule-icon warning">!</span>
                        <span class="rule-text"><strong>退费/补收补退</strong>：按原费用产生时的归属处理，不随员工当前属性变化</span>
                    </li>
                    <li class="rule-item">
                        <span class="rule-icon info">i</span>
                        <span class="rule-text"><strong>合并付款申请</strong>：财务归属到发起的结算主体，其他主体费用通过内部划转追溯</span>
                    </li>
                    <li class="rule-item">
                        <span class="rule-icon success">✓</span>
                        <span class="rule-text"><strong>账单锁定</strong>：账单生成后明细锁定，员工调动不影响已生成的账单</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
```

- [ ] **Step 2: 提交**

```bash
git add prototype/cost-attribution-demo.html
git commit -m "feat: 费用归属固化演示原型

- 调动前后费用归属对比展示
- 双层模型（缴费层+对账层）
- 费用流水明细（含固化标识）
- 费用归属固化规则说明

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## Task 4: 更新设计文档并创建 PRD

**Files:**
- Modify: `docs/superpowers/specs/2026-04-25-settlement-entity-financial-attribution-design.md`
- Create: `docs/superpowers/specs/2026-04-25-settlement-entity-phase1-prd.md`

- [ ] **Step 1: 创建阶段一 PRD 文档**

```markdown
# 结算主体维度财务归属 - 阶段一 PRD

> 日期：2026-04-25
> 状态：待开发

## 阶段一范围

### 包含功能

1. **数据库迁移**
   - 员工档案版本表 (`employee_archive_version`)
   - 结算历史表 (`settlement_history`)
   - 费用明细表固化字段
   - 账单和付款申请表结构
   - 历史数据迁移脚本 + 回滚脚本

2. **交互原型**
   - 员工档案版本管理页面
   - 费用归属固化演示页面

### 不包含功能

- 前端页面实际开发（后续阶段）
- 后端 API 开发（后续阶段）
- 各业务模块权限矩阵落地（阶段二/三）

## 验收标准

1. 数据库迁移脚本可在测试环境执行成功
2. 历史数据迁移正确，可回滚
3. 交互原型可通过浏览器访问，演示核心交互逻辑
```

- [ ] **Step 2: 提交**

```bash
git add docs/superpowers/specs/2026-04-25-settlement-entity-phase1-prd.md
git commit -m "docs: 结算主体维度财务归属阶段一 PRD

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

## 后续阶段说明

本计划仅覆盖阶段一（数据基础 + 原型演示）。后续阶段需单独创建计划：

### 阶段二：业务权限矩阵落地
- 核心人事模块（花名册、异动、合同）权限适配
- 保险福利模块（参保档案、核算、待遇、申报）权限适配
- 上下游模块（结算、工资条）权限适配
- 各模块前端页面增加「已调出」标识和筛选

### 阶段三：财务管理模块
- 付款申请合并付款功能
- 账单生成与锁定
- 内部划转记录
- 退费/补收补退按原归属处理
