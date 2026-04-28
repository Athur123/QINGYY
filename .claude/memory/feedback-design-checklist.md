---
name: 青阳云HRO设计检查清单
description: 青阳云HRO前端开发必须遵守的设计检查项，适用于所有页面和组件开发
type: feedback
---

每次开发页面/组件时必须确认：

- [ ] 不用 emoji 做图标（使用 SVG / Lucide）
- [ ] 交互元素有可见焦点环
- [ ] 触摸目标 ≥ 44×44px
- [ ] 支持 `prefers-reduced-motion`
- [ ] Warning 橙色配图标（对比度不足）
- [ ] 使用语义化颜色 token，无硬编码色值
- [ ] 禁用状态视觉清晰且不可交互