# Specs 变更指南

这份文档用于说明：在当前仓库中，什么时候应该更新 spec，如何更新，以及更新后要同步哪些内容。

## 1. 先判断这次是不是 spec 变更

满足以下任一情况，建议先改 spec，再改 prototype 或 plan：

- 页面主流程发生变化
- 页面信息架构发生变化
- 关键字段定义、状态机、匹配规则发生变化
- 新增一块独立功能，需要别人依据文档继续实现
- 现有 prototype 的交互或命名已经与文档不一致

如果只是以下情况，通常不必新开 spec：

- 文案润色
- 明显笔误修正
- 不影响流程和规则的细节补充

## 2. 先找到模块，再找到主 spec

本仓库的 spec 目录按模块组织：

- `docs/superpowers/specs/approval/`
- `docs/superpowers/specs/calculator/`
- `docs/superpowers/specs/employee/`
- `docs/superpowers/specs/insurance-config/`
- `docs/superpowers/specs/reconciliation/`
- `docs/superpowers/specs/settlement/`
- `docs/superpowers/specs/system/`

每次修改前，先看对应模块下的 `README.md`。

模块 `README.md` 的用途：

- 标明当前主入口 prototype
- 标明主 spec
- 标明补充 spec
- 区分当前内容与历史探索内容

例如，对账模块应先看：

- `docs/superpowers/specs/reconciliation/README.md`

## 3. 三种常见变更方式

### 方式 A：直接修改现有 spec

适用场景：

- 只是补充说明
- 修正文档歧义
- 细化已有规则
- 不改变主流程和主结构

做法：

1. 找到当前主 spec
2. 直接在原文档中修订
3. 若影响 prototype 或 plan，同步检查它们是否一致

### 方式 B：新增一份专题 spec

适用场景：

- 新增一个独立子主题
- 原 spec 仍然成立，但需要展开一个专题
- 某项规则值得单独沉淀，避免把基础 spec 写得过重

常见例子：

- 导入规则单独一篇
- 匹配规则单独一篇
- 某个批处理或归档流程单独一篇

做法：

1. 在对应模块目录下新增一个语义清晰的 Markdown 文件
2. 文件名尽量使用业务语义，不以日期前缀作为主规范
3. 更新该模块 `README.md`，把它加入 `Main specs` 或补充说明
4. 如果已有 plan 依赖旧说明，同步补充 plan 引用

### 方式 C：重写主 spec

适用场景：

- 主流程变了
- 页面主结构变了
- 主状态机或主术语体系变了
- 原文档已无法继续作为事实来源

做法：

1. 回到模块主 spec 直接系统性修订
2. 明确哪些历史规则已失效
3. 检查模块 `README.md` 中推荐阅读顺序是否还成立
4. 检查 prototype 与 plan 是否需要同步调整

## 4. 推荐的 spec 文件命名方式

优先使用短文件名和业务语义名，例如：

- `reconciliation-design.md`
- `ledger-import.md`
- `type-month-matching.md`
- `field-collection.md`

不建议继续把“日期前缀文件名”当成默认主模式，除非是明确的历史归档或外部约束要求。

## 5. 每次修改 spec 后，要同步检查什么

至少检查以下三类内容：

### 5.1 Prototype 是否一致

检查路径：

- `prototype/<module>/`

重点看：

- 页面名称是否一致
- 状态名称是否一致
- 字段名称是否一致
- 页面流程是否与 spec 一致

### 5.2 Plan 是否一致

检查路径：

- `docs/superpowers/plans/<module>/`

重点看：

- plan 中引用的 spec 是否还是当前版本
- 实现步骤是否仍覆盖新的需求
- 是否存在只改了 spec、但 plan 还按旧逻辑执行的情况

### 5.3 模块 README 是否一致

检查路径：

- `docs/superpowers/specs/<module>/README.md`

重点看：

- 主 spec 是否还是当前主文档
- 新增 spec 是否已加入索引
- 推荐阅读顺序是否仍然正确

## 6. 推荐的最小变更流程

适用于大多数日常变更：

1. 确认变更属于哪个模块
2. 阅读该模块 `README.md`
3. 判断是直接修改、专题新增，还是主 spec 重写
4. 更新对应 spec
5. 同步检查 prototype、plan、模块 README
6. 提交变更

## 7. 推荐的完整流程（适合较大变更）

适用于流程改造、规则改造、页面结构重构：

1. 先明确变更目标和边界
2. 更新或新增 spec
3. 让相关人员确认 spec
4. 再更新 plan
5. 最后再改 prototype 或实现代码

如果按 superpowers 工作流执行，通常是：

`brainstorming -> spec -> plan -> implement`

## 8. 一个实用判断原则

如果这次改动会改变下面任一项，就应优先更新 spec：

- 别人应该如何实现
- 别人应该如何验收
- 页面或功能应该如何工作

如果这次改动只是在表达层面更准确，但不改变任何行为，通常只需要小范围修订文档。

## 9. 建议的 spec 文档最小结构

一个可维护的 spec，至少建议包含这些部分：

- 背景 / 目标
- 适用范围
- 核心流程
- 字段或数据定义
- 状态说明
- 关键规则 / 边界条件
- 与 prototype / plan 的对应关系

## 10. 提交前自检清单

- 是否改对了模块目录
- 是否改的是当前主 spec，而不是历史遗留文档
- 是否更新了模块 `README.md`
- 是否检查了 prototype 一致性
- 是否检查了 plan 一致性
- 文档中的术语是否前后一致
- 文件名是否简洁、可读、符合当前仓库习惯
