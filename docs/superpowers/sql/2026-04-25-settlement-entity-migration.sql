-- ============================================================
-- 结算主体维度财务归属 - 阶段一：档案版本化与费用固化
-- 日期：2026-04-25
-- ============================================================

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
