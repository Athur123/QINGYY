# 通用日志查看器设计

## Context

用户需要一个统一的日志查看器前端，可适配多种业务日志类型（员工档案管理、社保管理、结算管理、合同管理、系统管理等），支持多维度筛选和详情查看。当前使用前端模拟数据快速原型，后端接口后补。

## 功能需求

1. **业务板块切换** — 下拉选择业务板块，不同板块显示不同日志
2. **多维度筛选** — 各板块筛选维度可配置，按需显示
3. **分页表格** — 列表展示 + 分页
4. **抽屉详情** — 右侧滑入抽屉展示完整日志信息

## 业务板块配置

```javascript
const BIZ_MODULES = {
  employee: {
    title: '员工档案管理',
    filters: ['keyword', 'status', 'method', 'time', 'employeeName']
  },
  social: {
    title: '社保管理',
    filters: ['keyword', 'status', 'method', 'time', 'insuranceType']
  },
  settlement: {
    title: '结算管理',
    filters: ['keyword', 'status', 'method', 'time', 'batchNumber']
  },
  contract: {
    title: '合同管理',
    filters: ['keyword', 'status', 'time', 'contractType']
  },
  system: {
    title: '系统管理',
    filters: ['keyword', 'status', 'method', 'time']
  }
};
```

业务板块可动态扩展，添加新板块只需在配置对象中增加条目。

## 筛选字段说明

| 字段 | 说明 |
|------|------|
| keyword | 关键词搜索（title、creator 模糊匹配） |
| status | 操作状态（0=成功, 9=异常） |
| method | 请求方式（GET/POST/PUT/DELETE） |
| time | 时间范围（startTime / endTime） |
| employeeName | 员工姓名（params 内部字段匹配） |
| insuranceType | 险种类型 |
| batchNumber | 批次号 |
| contractType | 合同类型 |

## 匹配方式

全部使用**包含匹配**（模糊匹配），不做精确、前缀、后缀区分。

## 数据结构

每条日志记录包含：

```javascript
{
  id: number,
  log_type: number,        // 0=正常, 9=异常
  title: string,           // 操作标题
  service_id: string,
  remote_addr: string,      // IP 地址
  user_agent: string,
  request_uri: string,     // 请求路径
  method: string,          // GET/POST/PUT/DELETE
  params: string,          // JSON 参数
  request_headers: string,
  time: number,
  exception: string | null,
  creator: string,
  create_time: datetime,
  tenant_id: number
}
```

## 文件结构

- `prototype/log-viewer.html` — 通用日志查看器页面（独立页面）

## 界面布局

沿用青阳云设计系统风格（蓝白配色、卡片布局）：
- 侧边栏：业务板块菜单
- 主内容区：筛选面板 + 分页表格 + 右侧抽屉详情

## 验证方式

1. 打开 `prototype/log-viewer.html`
2. 选择不同业务板块，验证筛选字段动态变化
3. 测试各筛选条件组合
4. 点击日志打开右侧抽屉查看详情
5. 验证分页功能
