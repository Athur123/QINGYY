# 参保档案字段采集配置实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现参保规则字段采集配置的数据模型（SQL迁移）和交互式HTML演示原型

**Architecture:** 三表关系模型（全局字段字典 → 采集配置头 → 采集字段项），通过SQL迁移脚本创建表结构和初始数据，通过HTML原型展示配置UI交互效果

**Tech Stack:** MySQL DDL/DML, HTML/CSS/JavaScript（青阳云设计系统）

---

## 文件清单

| 文件 | 操作 | 职责 |
|------|------|------|
| `docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql` | 创建 | 数据库迁移脚本：3张表的DDL + field_dict初始化数据 + 回滚脚本 |
| `prototype/field-collection-config-demo.html` | 创建 | 交互式HTML原型：嵌入字段采集配置面板的社保规则配置页面 |

## 设计原则

- 本计划产出可运行的SQL脚本和可交互的HTML原型
- SQL遵循项目已有的迁移脚本模式（参见 `2026-04-25-settlement-entity-migration.sql`）
- HTML原型遵循青阳云设计系统（`styles/qingyang-*.css`）和已有社保规则页面的布局模式

---

### Task 1: 数据库迁移脚本 — 全局字段字典表

**Files:**
- Create: `docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql`

- [ ] **Step 1: 创建 migration SQL 文件，写入表头注释和 field_dict 表 DDL**

```sql
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
```

- [ ] **Step 2: 提交**

```bash
git add docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql
git commit -m "feat: 创建全局字段字典表 field_dict"
```

---

### Task 2: 数据库迁移脚本 — 采集配置头和采集字段项表

**Files:**
- Modify: `docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql`

- [ ] **Step 1: 在 migration 文件中追加 field_collection_config 和 field_collection_item 表 DDL**

```sql
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
```

- [ ] **Step 2: 提交**

```bash
git add docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql
git commit -m "feat: 创建采集配置头表和采集字段项表"
```

---

### Task 3: 数据库迁移脚本 — 字段字典初始化数据

**Files:**
- Modify: `docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql`

- [ ] **Step 1: 在 migration 文件中追加 field_dict 初始化数据**

```sql
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
```

- [ ] **Step 2: 追加回滚脚本到文件末尾**

```sql
-- ============================================================
-- 回滚脚本（迁移失败或需要回退时使用）
-- ============================================================

-- 删除表（注意外键依赖顺序）
DROP TABLE IF EXISTS `field_collection_item`;
DROP TABLE IF EXISTS `field_collection_config`;
DROP TABLE IF EXISTS `field_dict`;
```

- [ ] **Step 3: 提交**

```bash
git add docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql
git commit -m "feat: 添加字段字典初始化数据和回滚脚本"
```

---

### Task 4: HTML原型 — 页面框架和左侧导航

**Files:**
- Create: `prototype/field-collection-config-demo.html`

- [ ] **Step 1: 创建HTML原型文件，写入页面框架（DOCTYPE、head、布局样式）**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>社保参保规则配置 - 字段采集配置 - 青阳云HRO</title>
  <link rel="stylesheet" href="../styles/qingyang-variables.css">
  <link rel="stylesheet" href="../styles/qingyang-components.css">
  <link rel="stylesheet" href="../styles/qingyang-forms.css">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --primary: #2563EB;
      --primary-hover: #1D4ED8;
      --primary-light: #EFF6FF;
      --primary-border: #BFDBFE;
      --success: #10B981;
      --success-light: #ECFDF5;
      --warning: #F59E0B;
      --warning-light: #FFFBEB;
      --error: #EF4444;
      --error-light: #FEF2F2;
      --gray-50: #F8FAFC;
      --gray-100: #F1F5F9;
      --gray-200: #E2E8F0;
      --gray-300: #CBD5E1;
      --gray-400: #94A3B8;
      --gray-500: #64748B;
      --gray-600: #475569;
      --gray-700: #334155;
      --gray-800: #1E293B;
      --gray-900: #0F172A;
      --radius-md: 8px;
      --radius-lg: 12px;
    }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 14px;
      color: var(--gray-800);
      background: var(--gray-100);
      line-height: 1.5;
    }
    .app-container { display: flex; min-height: 100vh; }

    /* Sidebar */
    .sidebar {
      width: 220px; background: #fff; border-right: 1px solid var(--gray-200);
      flex-shrink: 0; position: fixed; height: 100vh; z-index: 100;
    }
    .sidebar-logo { padding: 20px 24px; border-bottom: 1px solid var(--gray-200); }
    .sidebar-logo h1 { font-size: 18px; font-weight: 700; color: var(--primary); }
    .sidebar-nav { list-style: none; padding: 12px 0; }
    .sidebar-nav-item {
      padding: 10px 24px; cursor: pointer; display: flex; align-items: center;
      gap: 10px; color: var(--gray-500); font-size: 13px; transition: all 150ms;
    }
    .sidebar-nav-item:hover { background: var(--gray-50); color: var(--gray-800); }
    .sidebar-nav-item.active { background: var(--primary-light); color: var(--primary); font-weight: 500; }
    .sidebar-nav-group { margin-top: 8px; border-top: 1px solid var(--gray-200); padding-top: 8px; }
    .sidebar-nav-sub { list-style: none; }
    .sidebar-nav-sub li {
      padding: 7px 24px 7px 48px; cursor: pointer; font-size: 12px; color: var(--gray-400);
      transition: all 150ms;
    }
    .sidebar-nav-sub li:hover { color: var(--gray-700); }
    .sidebar-nav-sub li.active { color: var(--primary); font-weight: 500; }

    /* Main */
    .main-content { flex: 1; margin-left: 220px; display: flex; flex-direction: column; }
    .topbar {
      height: 56px; background: #fff; border-bottom: 1px solid var(--gray-200);
      display: flex; align-items: center; justify-content: space-between; padding: 0 32px;
    }
    .topbar-breadcrumb { font-size: 13px; color: var(--gray-500); }
    .topbar-user { font-size: 13px; color: var(--gray-600); }
    .content-area { flex: 1; padding: 32px; }
  </style>
</head>
<body>
  <div class="app-container">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo"><h1>青阳云 HRO</h1></div>
      <ul class="sidebar-nav">
        <li class="sidebar-nav-item">📋 薪资档案</li>
        <li class="sidebar-nav-item active">
          🛡️ 保险福利
          <ul class="sidebar-nav-sub">
            <li>保险台账</li>
            <li class="active">参保规则</li>
            <li>二级户</li>
            <li>员工参保档案</li>
            <li>保险福利核算</li>
            <li>保险分组</li>
            <li>险种配置</li>
          </ul>
        </li>
        <li class="sidebar-nav-item">📝 异动申报</li>
        <li class="sidebar-nav-item">📊 报表</li>
      </ul>
    </aside>

    <!-- Main -->
    <div class="main-content">
      <div class="topbar">
        <div class="topbar-breadcrumb">保险福利 / 参保规则 / 配置</div>
        <div class="topbar-user">管理员</div>
      </div>
      <div class="content-area">
        <!-- Content injected below -->
      </div>
    </div>
  </div>
</body>
</html>
```

- [ ] **Step 2: 在 content-area 中追加页面头部（返回按钮 + 标题）**

```html
        <!-- Page Header -->
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 28px;">
          <button style="padding: 8px 16px; background: white; border: 1px solid var(--gray-200); border-radius: var(--radius-md); cursor: pointer; font-size: 13px; color: var(--gray-600); display: flex; align-items: center; gap: 6px;">
            ← 返回
          </button>
          <h2 style="font-size: 20px; font-weight: 700; color: var(--gray-900);">配置社保参保规则</h2>
        </div>
```

- [ ] **Step 3: 提交**

```bash
git add prototype/field-collection-config-demo.html
git commit -m "feat: 创建字段采集配置HTML原型 - 页面框架"
```

---

### Task 5: HTML原型 — 现有三个分段（基本信息、参保险种、规则配置）

**Files:**
- Modify: `prototype/field-collection-config-demo.html`

- [ ] **Step 1: 在 content-area 中追加 Tab 导航栏和基本信息分段**

在 `</div>` (content-area closing) 之前插入：

```html
        <!-- Tab Navigation -->
        <div style="display: flex; border-bottom: 2px solid var(--gray-200); margin-bottom: 24px;">
          <div class="config-tab active" data-tab="basic" onclick="switchTab('basic')">基本信息</div>
          <div class="config-tab" data-tab="insurance" onclick="switchTab('insurance')">参保险种</div>
          <div class="config-tab" data-tab="rules" onclick="switchTab('rules')">规则配置</div>
          <div class="config-tab new" data-tab="collection" onclick="switchTab('collection')">
            <span style="background: var(--primary); color: white; padding: 1px 8px; border-radius: 4px; font-size: 10px; margin-right: 6px; font-weight: 600;">NEW</span>
            字段采集配置
          </div>
        </div>

        <style>
          .config-tab {
            padding: 12px 20px; cursor: pointer; font-size: 14px; color: var(--gray-500);
            border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 150ms;
            font-weight: 500;
          }
          .config-tab:hover { color: var(--gray-700); }
          .config-tab.active { color: var(--primary); border-bottom-color: var(--primary); font-weight: 600; }
          .config-tab.new { color: var(--primary); }
        </style>

        <!-- Tab: Basic Info -->
        <div class="tab-panel" id="panel-basic">
          <div style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--gray-200); padding: 24px; margin-bottom: 20px;">
            <h3 style="font-size: 15px; font-weight: 600; color: var(--gray-800); margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--gray-100);">基本信息</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
              <div>
                <label style="font-size: 13px; color: var(--gray-600); font-weight: 500; display: block; margin-bottom: 6px;"><span style="color: var(--error);">*</span> 规则名称</label>
                <input type="text" value="二级户专属社保规则" style="width: 100%; height: 40px; padding: 0 12px; border: 1px solid var(--gray-300); border-radius: var(--radius-md); font-size: 14px;">
              </div>
              <div>
                <label style="font-size: 13px; color: var(--gray-600); font-weight: 500; display: block; margin-bottom: 6px;"><span style="color: var(--error);">*</span> 所属组织</label>
                <input type="text" value="2046892568145866753" disabled style="width: 100%; height: 40px; padding: 0 12px; border: 1px solid var(--gray-200); border-radius: var(--radius-md); font-size: 14px; background: var(--gray-50); color: var(--gray-400);">
              </div>
              <div>
                <label style="font-size: 13px; color: var(--gray-600); font-weight: 500; display: block; margin-bottom: 6px;"><span style="color: var(--error);">*</span> 生效月份</label>
                <input type="text" value="2026-05" style="width: 100%; height: 40px; padding: 0 12px; border: 1px solid var(--gray-300); border-radius: var(--radius-md); font-size: 14px;">
              </div>
              <div>
                <label style="font-size: 13px; color: var(--gray-600); font-weight: 500; display: block; margin-bottom: 6px;"><span style="color: var(--error);">*</span> 规则编码</label>
                <input type="text" value="EJH20260427" disabled style="width: 100%; height: 40px; padding: 0 12px; border: 1px solid var(--gray-200); border-radius: var(--radius-md); font-size: 14px; background: var(--gray-50); color: var(--gray-400);">
              </div>
              <div>
                <label style="font-size: 13px; color: var(--gray-600); font-weight: 500; display: block; margin-bottom: 6px;"><span style="color: var(--error);">*</span> 参保地区</label>
                <input type="text" value="云南省 / 昭通市 / 巧家县" disabled style="width: 100%; height: 40px; padding: 0 12px; border: 1px solid var(--gray-200); border-radius: var(--radius-md); font-size: 14px; background: var(--gray-50); color: var(--gray-400);">
              </div>
              <div>
                <label style="font-size: 13px; color: var(--gray-600); font-weight: 500; display: block; margin-bottom: 6px;"><span style="color: var(--error);">*</span> 负责人</label>
                <input type="text" value="于佳" disabled style="width: 100%; height: 40px; padding: 0 12px; border: 1px solid var(--gray-200); border-radius: var(--radius-md); font-size: 14px; background: var(--gray-50); color: var(--gray-400);">
              </div>
            </div>
          </div>
        </div>
```

- [ ] **Step 2: 追加参保险种和规则配置分段的简化版**

```html
        <!-- Tab: Insurance Types -->
        <div class="tab-panel" id="panel-insurance" style="display: none;">
          <div style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--gray-200); padding: 24px; margin-bottom: 20px;">
            <h3 style="font-size: 15px; font-weight: 600; color: var(--gray-800); margin-bottom: 16px;">参保险种</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
              <thead>
                <tr style="border-bottom: 2px solid var(--gray-200);">
                  <th style="text-align: left; padding: 10px 12px; color: var(--gray-500); font-weight: 500;">险种名称</th>
                  <th style="text-align: left; padding: 10px 12px; color: var(--gray-500); font-weight: 500;">编码</th>
                  <th style="text-align: center; padding: 10px 12px; color: var(--gray-500); font-weight: 500;">单位比例</th>
                  <th style="text-align: center; padding: 10px 12px; color: var(--gray-500); font-weight: 500;">个人比例</th>
                  <th style="text-align: center; padding: 10px 12px; color: var(--gray-500); font-weight: 500;">基数范围</th>
                </tr>
              </thead>
              <tbody>
                <tr style="border-bottom: 1px solid var(--gray-100);"><td style="padding: 10px 12px;">养老保险</td><td style="padding: 10px 12px;">001</td><td style="text-align: center;">15%</td><td style="text-align: center;">8%</td><td style="text-align: center;">4357 - 21789</td></tr>
                <tr style="border-bottom: 1px solid var(--gray-100);"><td style="padding: 10px 12px;">医疗保险</td><td style="padding: 10px 12px;">002</td><td style="text-align: center;">8%</td><td style="text-align: center;">2%</td><td style="text-align: center;">4357 - 21789</td></tr>
                <tr style="border-bottom: 1px solid var(--gray-100);"><td style="padding: 10px 12px;">工伤保险</td><td style="padding: 10px 12px;">003</td><td style="text-align: center;">0.4%</td><td style="text-align: center;">0%</td><td style="text-align: center;">4357 - 21789</td></tr>
                <tr style="border-bottom: 1px solid var(--gray-100);"><td style="padding: 10px 12px;">失业保险</td><td style="padding: 10px 12px;">004</td><td style="text-align: center;">0.7%</td><td style="text-align: center;">0.3%</td><td style="text-align: center;">4357 - 21789</td></tr>
                <tr style="border-bottom: 1px solid var(--gray-100);"><td style="padding: 10px 12px;">生育保险</td><td style="padding: 10px 12px;">005</td><td style="text-align: center;">0.8%</td><td style="text-align: center;">0%</td><td style="text-align: center;">4357 - 21789</td></tr>
                <tr><td style="padding: 10px 12px;">大病险种</td><td style="padding: 10px 12px;">007</td><td style="text-align: center;">固定240</td><td style="text-align: center;">固定100</td><td style="text-align: center;">4357 - 21789</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Tab: Rules -->
        <div class="tab-panel" id="panel-rules" style="display: none;">
          <div style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--gray-200); padding: 24px; margin-bottom: 20px;">
            <h3 style="font-size: 15px; font-weight: 600; color: var(--gray-800); margin-bottom: 16px;">规则配置</h3>
            <div style="display: flex; flex-direction: column; gap: 16px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 13px; color: var(--gray-600); min-width: 140px;">新参保强制参保险种:</span>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 13px;"><input type="checkbox" checked> 养老保险</label>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 13px;"><input type="checkbox" checked> 医疗保险</label>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 13px;"><input type="checkbox"> 工伤保险</label>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 13px;"><input type="checkbox"> 失业保险</label>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 13px;"><input type="checkbox"> 生育保险</label>
              </div>
            </div>
          </div>
        </div>
```

- [ ] **Step 3: 提交**

```bash
git add prototype/field-collection-config-demo.html
git commit -m "feat: 添加现有配置分段（基本信息、参保险种、规则配置）"
```

---

### Task 6: HTML原型 — 字段采集配置 Tab（核心功能）

**Files:**
- Modify: `prototype/field-collection-config-demo.html`

- [ ] **Step 1: 在文件 `</body>` 之前追加字段采集配置面板的 HTML**

```html
        <!-- Tab: Field Collection Config -->
        <div class="tab-panel" id="panel-collection" style="display: none;">
          <!-- Operation type buttons -->
          <div style="display: flex; gap: 8px; margin-bottom: 20px;">
            <button class="op-btn active" data-op="add" onclick="switchOp('add')">增员</button>
            <button class="op-btn" data-op="remove" onclick="switchOp('remove')">减员</button>
            <button class="op-btn" data-op="adjust" onclick="switchOp('adjust')">调基</button>
            <button class="op-btn" data-op="supplement" onclick="switchOp('supplement')">补缴</button>
          </div>

          <style>
            .op-btn {
              padding: 8px 20px; border: 1px solid var(--gray-200); border-radius: var(--radius-md);
              background: white; color: var(--gray-600); font-size: 13px; cursor: pointer;
              transition: all 150ms; font-weight: 500;
            }
            .op-btn:hover { border-color: var(--gray-300); color: var(--gray-800); }
            .op-btn.active { background: var(--primary); color: white; border-color: var(--primary); }
          </style>

          <!-- Field list panel for ADD -->
          <div class="op-panel" id="op-add">
            <div style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--gray-200); overflow: hidden;">
              <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                <thead>
                  <tr style="background: var(--gray-50); border-bottom: 2px solid var(--gray-200);">
                    <th style="text-align: left; padding: 12px 16px; color: var(--gray-500); font-weight: 500; width: 60px;">排序</th>
                    <th style="text-align: left; padding: 12px 16px; color: var(--gray-500); font-weight: 500;">字段名称</th>
                    <th style="text-align: left; padding: 12px 16px; color: var(--gray-500); font-weight: 500; width: 100px;">字段类型</th>
                    <th style="text-align: left; padding: 12px 16px; color: var(--gray-500); font-weight: 500; width: 100px;">值来源</th>
                    <th style="text-align: center; padding: 12px 16px; color: var(--gray-500); font-weight: 500; width: 70px;">必填</th>
                    <th style="text-align: left; padding: 12px 16px; color: var(--gray-500); font-weight: 500; width: 140px;">校验规则</th>
                    <th style="text-align: center; padding: 12px 16px; color: var(--gray-500); font-weight: 500; width: 120px;">操作</th>
                  </tr>
                </thead>
                <tbody id="field-table-body">
                  <!-- Rows rendered by JS -->
                </tbody>
              </table>
            </div>
            <!-- Add field button -->
            <button onclick="openFieldPicker()" style="margin-top: 16px; width: 100%; padding: 12px; background: white; border: 1px dashed var(--primary); border-radius: var(--radius-md); color: var(--primary); font-size: 14px; cursor: pointer; font-weight: 500;">
              + 添加字段
            </button>
          </div>

          <!-- Empty panels for other ops -->
          <div class="op-panel" id="op-remove" style="display: none;">
            <div style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--gray-200); padding: 48px; text-align: center;">
              <div style="font-size: 36px; margin-bottom: 12px;">📋</div>
              <div style="font-size: 14px; color: var(--gray-400);">减员操作暂未配置采集字段</div>
              <button onclick="switchOp('add')" style="margin-top: 16px; padding: 8px 20px; background: var(--primary); color: white; border: none; border-radius: var(--radius-md); cursor: pointer; font-size: 13px;">前往增员配置</button>
            </div>
          </div>
          <div class="op-panel" id="op-adjust" style="display: none;">
            <div style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--gray-200); padding: 48px; text-align: center;">
              <div style="font-size: 36px; margin-bottom: 12px;">📋</div>
              <div style="font-size: 14px; color: var(--gray-400);">调基操作暂未配置采集字段</div>
            </div>
          </div>
          <div class="op-panel" id="op-supplement" style="display: none;">
            <div style="background: white; border-radius: var(--radius-lg); border: 1px solid var(--gray-200); padding: 48px; text-align: center;">
              <div style="font-size: 36px; margin-bottom: 12px;">📋</div>
              <div style="font-size: 14px; color: var(--gray-400);">补缴操作暂未配置采集字段</div>
            </div>
          </div>
        </div>
```

- [ ] **Step 2: 在 `</body>` 之前追加 JavaScript（字段数据、Tab切换、操作切换、渲染逻辑）**

```html
  <script>
    // ========== Tab switching ==========
    function switchTab(tabId) {
      document.querySelectorAll('.config-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
      document.querySelector(`.config-tab[data-tab="${tabId}"]`).classList.add('active');
      document.getElementById(`panel-${tabId}`).style.display = '';
    }

    // ========== Operation switching ==========
    function switchOp(opId) {
      document.querySelectorAll('.op-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.op-panel').forEach(p => p.style.display = 'none');
      document.querySelector(`.op-btn[data-op="${opId}"]`).classList.add('active');
      document.getElementById(`op-${opId}`).style.display = '';
    }

    // ========== Field data (demo for ADD operation) ==========
    let fields = [
      { id: 1, sort: 1, dictId: 'contract_attachment', label: '合同附件', required: true, validation: '', placeholder: '' },
      { id: 2, sort: 2, dictId: 'contract_start_date', label: '合同开始日期', required: true, validation: '', placeholder: '' },
      { id: 3, sort: 3, dictId: 'id_card_front', label: '身份证正面', required: false, validation: '', placeholder: '' },
      { id: 4, sort: 4, dictId: 'household_type', label: '户籍类型', required: true, validation: '', placeholder: '' },
    ];
    let nextId = 5;

    // ========== Field dictionary ==========
    const fieldDict = {
      contract_attachment:  { name: '合同附件',       type: 'file',   source: 'MANUAL' },
      contract_start_date:  { name: '合同开始日期',   type: 'date',   source: 'AUTO',   path: 'employee.contract.startDate' },
      contract_end_date:    { name: '合同结束日期',   type: 'date',   source: 'AUTO',   path: 'employee.contract.endDate' },
      id_card_front:        { name: '身份证正面',     type: 'photo',  source: 'MANUAL' },
      id_card_back:         { name: '身份证反面',     type: 'photo',  source: 'MANUAL' },
      household_type:       { name: '户籍类型',       type: 'select', source: 'AUTO',   path: 'employee.household.type' },
      household_address:    { name: '户籍地址',       type: 'text',   source: 'AUTO',   path: 'employee.household.address' },
      social_security_card: { name: '社保卡号',       type: 'text',   source: 'AUTO',   path: 'employee.socialSecurity.cardNo' },
      bank_account:         { name: '银行账号',       type: 'text',   source: 'AUTO',   path: 'employee.bankAccount.no' },
      marriage_status:      { name: '婚姻状况',       type: 'select', source: 'AUTO',   path: 'employee.basic.marriageStatus' },
      emergency_contact:    { name: '紧急联系人',     type: 'text',   source: 'AUTO',   path: 'employee.emergency.name' },
      emergency_phone:      { name: '紧急联系电话',   type: 'text',   source: 'AUTO',   path: 'employee.emergency.phone' },
    };

    const typeLabels = { text: '文本', number: '数值', date: '日期', file: '附件', photo: '照片', select: '下拉' };
    const sourceLabels = { AUTO: '员工档案', MANUAL: '手动填写' };
    const typeColors = { text: '#3b82f6', number: '#8b5cf6', date: '#10b981', file: '#f59e0b', photo: '#ec4899', select: '#06b6d4' };

    // ========== Render field table ==========
    function renderFields() {
      const tbody = document.getElementById('field-table-body');
      if (!fields.length) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:32px;color:var(--gray-400);">未配置采集字段，点击下方"添加字段"开始配置</td></tr>`;
        return;
      }
      fields.sort((a, b) => a.sort - b.sort);
      tbody.innerHTML = fields.map((f, i) => {
        const dict = fieldDict[f.dictId];
        if (!dict) return '';
        const bgColor = typeColors[dict.type] || '#64748b';
        return `<tr style="border-bottom: 1px solid var(--gray-100); transition: background 150ms;" onmouseover="this.style.background='var(--gray-50)'" onmouseout="this.style.background=''">
          <td style="padding: 10px 16px;"><input type="number" value="${f.sort}" onchange="updateField(${f.id},'sort',this.value)" style="width: 50px; padding: 4px 6px; border: 1px solid var(--gray-300); border-radius: 4px; font-size: 13px; text-align: center;"></td>
          <td style="padding: 10px 16px; font-weight: 500;">${f.label || dict.name}</td>
          <td style="padding: 10px 16px;"><span style="background:${bgColor}15; color:${bgColor}; padding: 2px 10px; border-radius: 4px; font-size: 12px; font-weight: 500;">${typeLabels[dict.type]}</span></td>
          <td style="padding: 10px 16px; font-size: 12px; color: var(--gray-500);">${sourceLabels[dict.source]}${dict.path ? '<br><span style="font-size:11px;color:var(--gray-400);font-family:monospace;">'+dict.path+'</span>' : ''}</td>
          <td style="padding: 10px 16px; text-align: center;">
            <label style="cursor:pointer;position:relative;width:36px;height:20px;display:inline-block;">
              <input type="checkbox" ${f.required?'checked':''} onchange="updateField(${f.id},'required',this.checked)" style="opacity:0;width:0;height:0;">
              <span style="position:absolute;inset:0;background:${f.required?'var(--primary)':'var(--gray-300)'};border-radius:10px;transition:200ms;" onclick="this.previousSibling.checked=!this.previousSibling.checked;this.previousSibling.dispatchEvent(new Event('change'))">
                <span style="position:absolute;left:${f.required?'18px':'2px'};top:2px;width:16px;height:16px;background:white;border-radius:50%;transition:200ms;"></span>
              </span>
            </label>
          </td>
          <td style="padding: 10px 16px;">
            ${f.validation ? `<span style="font-size:12px;color:var(--gray-600);font-family:monospace;">${f.validation}</span>` : '<span style="color:var(--gray-300);font-size:12px;">-</span>'}
            <button onclick="editValidation(${f.id})" style="margin-left:8px;background:none;border:none;color:var(--primary);cursor:pointer;font-size:12px;">编辑</button>
          </td>
          <td style="padding: 10px 16px; text-align: center;">
            <button onclick="removeField(${f.id})" style="background:none;border:none;color:var(--error);cursor:pointer;font-size:13px;">移除</button>
          </td>
        </tr>`;
      }).join('');
    }

    function updateField(id, key, val) {
      const f = fields.find(x => x.id === id);
      if (!f) return;
      if (key === 'sort') f.sort = parseInt(val) || 0;
      if (key === 'required') f.required = val;
      renderFields();
    }

    function removeField(id) {
      fields = fields.filter(x => x.id !== id);
      renderFields();
    }

    function editValidation(id) {
      const f = fields.find(x => x.id === id);
      if (!f) return;
      const val = prompt('输入校验规则（正则表达式）：', f.validation || '');
      if (val !== null) { f.validation = val; renderFields(); }
    }

    // ========== Field picker modal ==========
    function openFieldPicker() {
      const existing = fields.map(f => f.dictId);
      const available = Object.keys(fieldDict).filter(k => !existing.includes(k));
      if (!available.length) { alert('所有字段已添加'); return; }
      const html = available.map(k => {
        const d = fieldDict[k];
        return `<label style="display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid var(--gray-100);cursor:pointer;">
          <input type="checkbox" value="${k}" class="picker-cb">
          <span style="font-size:13px;font-weight:500;">${d.name}</span>
          <span style="font-size:11px;color:var(--gray-400);">(${typeLabels[d.type]})</span>
          <span style="font-size:11px;color:${d.source==='AUTO'?'#10b981':'#f59e0b'};">${sourceLabels[d.source]}</span>
        </label>`;
      }).join('');
      const overlay = document.createElement('div');
      overlay.id = 'picker-overlay';
      overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:1000;display:flex;align-items:center;justify-content:center;';
      overlay.innerHTML = `<div style="background:white;border-radius:12px;width:480px;max-height:80vh;overflow-y:auto;box-shadow:0 20px 40px rgba(0,0,0,0.15);">
        <div style="padding:20px 24px;border-bottom:1px solid var(--gray-200);display:flex;justify-content:space-between;align-items:center;">
          <h3 style="font-size:16px;font-weight:600;">选择字段</h3>
          <button onclick="closePicker()" style="background:none;border:none;font-size:20px;cursor:pointer;color:var(--gray-400);">×</button>
        </div>
        <div style="padding:16px 24px;" id="picker-list">${html}</div>
        <div style="padding:16px 24px;border-top:1px solid var(--gray-200);display:flex;justify-content:flex-end;gap:8px;">
          <button onclick="closePicker()" style="padding:8px 20px;background:white;border:1px solid var(--gray-300);border-radius:6px;cursor:pointer;">取消</button>
          <button onclick="confirmPicker()" style="padding:8px 20px;background:var(--primary);color:white;border:none;border-radius:6px;cursor:pointer;">确认添加</button>
        </div>
      </div>`;
      overlay.addEventListener('click', (e) => { if (e.target === overlay) closePicker(); });
      document.body.appendChild(overlay);
    }

    function closePicker() {
      const el = document.getElementById('picker-overlay');
      if (el) el.remove();
    }

    function confirmPicker() {
      const cbs = document.querySelectorAll('.picker-cb:checked');
      cbs.forEach(cb => {
        const maxSort = fields.length ? Math.max(...fields.map(f => f.sort)) : 0;
        fields.push({ id: nextId++, sort: maxSort + 1, dictId: cb.value, label: '', required: false, validation: '', placeholder: '' });
      });
      closePicker();
      renderFields();
    }

    // ========== Init ==========
    renderFields();
  </script>
```

- [ ] **Step 3: 提交**

```bash
git add prototype/field-collection-config-demo.html
git commit -m "feat: 实现字段采集配置面板（Tab切换、操作切换、字段增删改、字段选择器）"
```

---

### Task 7: 验证与最终检查

**Files:**
- `docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql`
- `prototype/field-collection-config-demo.html`

- [ ] **Step 1: 验证 SQL 脚本语法**

运行以下命令检查 SQL 文件完整性：

```bash
cat docs/superpowers/sql/2026-04-27-field-collection-config-migration.sql | grep -c "CREATE TABLE"
```

预期输出：`3`（3张表）

- [ ] **Step 2: 验证 HTML 原型可正常打开**

```bash
open prototype/field-collection-config-demo.html
```

检查项：
- Tab 切换正常（基本信息 → 字段采集配置）
- 操作类型切换正常（增员/减员/调基/补缴）
- 增员面板字段列表正确渲染
- Toggle 开关可切换必填状态
- 排序号可修改
- 移除按钮可删除字段
- "添加字段"弹出选择器，支持多选
- 减员/调基/补缴显示空状态

- [ ] **Step 3: 提交最终版本**

```bash
git status
git diff --stat
```

确认所有变更已提交后，完成。
