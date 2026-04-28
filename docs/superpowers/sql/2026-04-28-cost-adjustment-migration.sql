-- ============================================================
-- 员工调动后费用归属调整 - 数据库迁移脚本
-- 日期：2026-04-28
-- 说明：创建费用调整日志表，记录每次重算操作的明细
-- 前置依赖：employee_archive_version, bill, bill_detail, cost_detail
-- ============================================================

-- ============================================================
-- 费用调整日志表
-- 记录因员工调动、政策调整等触发的费用归属调整操作
-- 每次重算生成一条主记录，明细存储拆分结果
-- ============================================================
CREATE TABLE IF NOT EXISTS `cost_adjustment_log` (
    `log_id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `trigger_type` VARCHAR(50) NOT NULL COMMENT '触发类型：transfer-调动/重新入职, policy_change-政策调整, manual_backpay-手动补缴, retroactive_enroll-追溯参保, retroactive_approval-审批生效日不一致, rehire_no_stop-离职未停保',
    `bill_month` VARCHAR(7) NOT NULL COMMENT '费用月份（YYYY-MM）',
    `old_settlement_entity_id` BIGINT DEFAULT NULL COMMENT '调整前结算主体',
    `new_settlement_entity_id` BIGINT NOT NULL COMMENT '调整后结算主体',
    `old_customer_id` BIGINT DEFAULT NULL COMMENT '调整前客户',
    `new_customer_id` BIGINT DEFAULT NULL COMMENT '调整后客户',
    `old_project_id` BIGINT DEFAULT NULL COMMENT '调整前项目',
    `new_project_id` BIGINT DEFAULT NULL COMMENT '调整后项目',
    `amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '涉及金额',
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态：pending-待处理, recalculated-已重算, failed-失败',
    `fail_reason` VARCHAR(512) DEFAULT NULL COMMENT '失败原因',
    `original_bill_id` BIGINT DEFAULT NULL COMMENT '原账单ID',
    `new_bill_id` BIGINT DEFAULT NULL COMMENT '新账单ID（拆分后）',
    `archive_version_id` BIGINT DEFAULT NULL COMMENT '触发时的档案版本号',
    `annotated_original_entity` VARCHAR(128) DEFAULT NULL COMMENT '标注的原归属信息（用于场景四：追溯参保）',
    `operator_id` BIGINT DEFAULT NULL COMMENT '操作人',
    `processed_at` TIMESTAMP NULL DEFAULT NULL COMMENT '处理时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_employee` (`employee_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_trigger_type` (`trigger_type`),
    INDEX `idx_bill_month` (`bill_month`),
    INDEX `idx_settlement` (`new_settlement_entity_id`, `bill_month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='费用调整日志表';

-- ============================================================
-- 回滚脚本（迁移失败时使用）
-- ============================================================

DROP TABLE IF EXISTS `cost_adjustment_log`;
