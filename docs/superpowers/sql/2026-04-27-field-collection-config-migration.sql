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

-- ============================================================
-- 采集配置头表
-- 关联参保规则与操作类型，每个规则的每种操作对应一条记录
-- ============================================================
CREATE TABLE IF NOT EXISTS `field_collection_config` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    `rule_id` BIGINT NOT NULL COMMENT '关联参保规则ID',
    `operation_type` VARCHAR(20) NOT NULL COMMENT '操作类型：ADD(增员)/REMOVE(减员)/ADJUST(调基)/SUPPLEMENT(补缴)',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_rule_operation` (`rule_id`, `operation_type`),
    INDEX `idx_rule_id` (`rule_id`),
    INDEX `idx_operation_type` (`operation_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='采集配置头表';

-- ============================================================
-- 采集字段项表
-- 从字典中选择字段并配置其在特定操作中的行为
-- ============================================================
CREATE TABLE IF NOT EXISTS `field_collection_item` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
    `config_id` BIGINT NOT NULL COMMENT '关联采集配置头ID',
    `field_dict_id` BIGINT NOT NULL COMMENT '关联全局字段字典ID',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '展示排序顺序',
    `is_required` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否必填：0-否, 1-是',
    `validation_rule` VARCHAR(512) DEFAULT NULL COMMENT '校验规则：正则表达式或预定义规则编码',
    `display_label` VARCHAR(128) DEFAULT NULL COMMENT '覆盖字典中的默认标签',
    `placeholder` VARCHAR(256) DEFAULT NULL COMMENT '输入框提示语（仅MANUAL类型）',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_config_id` (`config_id`),
    INDEX `idx_field_dict_id` (`field_dict_id`),
    INDEX `idx_config_sort` (`config_id`, `sort_order`),
    CONSTRAINT `fk_item_config` FOREIGN KEY (`config_id`) REFERENCES `field_collection_config` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_item_dict` FOREIGN KEY (`field_dict_id`) REFERENCES `field_dict` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='采集字段项表';

-- ============================================================
-- 全局字段字典初始化数据
-- 预置常见员工档案采集字段
-- ============================================================
INSERT INTO `field_dict` (`field_code`, `field_name`, `field_type`, `value_source`, `auto_source_path`, `options`, `description`) VALUES
('contract_attachment', '合同附件', 'file', 'MANUAL', NULL, NULL, '劳动合同扫描件附件'),
('contract_start_date', '合同开始日期', 'date', 'AUTO', 'employee.contract.startDate', NULL, '劳动合同生效日期'),
('contract_end_date', '合同结束日期', 'date', 'AUTO', 'employee.contract.endDate', NULL, '劳动合同到期日期'),
('id_card_front', '身份证正面', 'photo', 'MANUAL', NULL, NULL, '身份证正面照片'),
('id_card_back', '身份证反面', 'photo', 'MANUAL', NULL, NULL, '身份证国徽面照片'),
('household_type', '户籍类型', 'select', 'AUTO', 'employee.household.type', '[{"label":"城镇户口","value":"urban"},{"label":"农村户口","value":"rural"}]', '员工户籍性质分类'),
('household_address', '户籍地址', 'text', 'AUTO', 'employee.household.address', NULL, '员工户籍所在地详细地址'),
('social_security_card', '社保卡号', 'text', 'AUTO', 'employee.socialSecurity.cardNo', NULL, '社会保障卡卡号'),
('bank_account', '银行账号', 'text', 'AUTO', 'employee.bankAccount.no', NULL, '员工工资卡银行账号'),
('marriage_status', '婚姻状况', 'select', 'AUTO', 'employee.basic.marriageStatus', '[{"label":"未婚","value":"single"},{"label":"已婚","value":"married"},{"label":"离异","value":"divorced"},{"label":"丧偶","value":"widowed"}]', '员工婚姻状态'),
('emergency_contact', '紧急联系人', 'text', 'AUTO', 'employee.emergency.name', NULL, '紧急联系人姓名'),
('emergency_phone', '紧急联系电话', 'text', 'AUTO', 'employee.emergency.phone', NULL, '紧急联系人电话号码');

-- ============================================================
-- 回滚脚本（迁移失败或需要回退时使用）
-- ============================================================

-- 删除表（注意外键依赖顺序）
DROP TABLE IF EXISTS `field_collection_item`;
DROP TABLE IF EXISTS `field_collection_config`;
DROP TABLE IF EXISTS `field_dict`;
