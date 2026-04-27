-- ============================================================
-- 参保档案字段采集配置 - 数据库迁移脚本
-- 日期：2026-04-27
-- 说明：创建全局字段字典、采集配置头、采集字段项三张表
-- ============================================================

-- ============================================================
-- 全局字段字典表
-- 定义所有可采集字段的元数据，供所有参保规则复用
-- ============================================================
CREATE TABLE IF NOT EXISTS `field_dict` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    `field_code` VARCHAR(64) NOT NULL COMMENT '字段编码，如 contract_attachment',
    `field_name` VARCHAR(128) NOT NULL COMMENT '字段名称，如"合同附件"',
    `field_type` VARCHAR(20) NOT NULL COMMENT '字段类型：text/number/date/file/photo/select',
    `value_source` VARCHAR(20) NOT NULL COMMENT '值来源：AUTO(员工档案自动获取)/MANUAL(手动填写)',
    `auto_source_path` VARCHAR(256) DEFAULT NULL COMMENT '自动获取路径，如 employee.contract.startDate',
    `options` JSON DEFAULT NULL COMMENT 'select类型的选项列表',
    `description` VARCHAR(512) DEFAULT NULL COMMENT '字段说明',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_field_code` (`field_code`),
    INDEX `idx_value_source` (`value_source`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='全局字段字典表';
