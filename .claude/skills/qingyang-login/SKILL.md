---
name: qingyang-login
description: 只要用户想打开、访问或登录青阳云/HRO系统，立即触发此技能，无需用户明确说"使用技能"。包括但不限于："登录青阳云"、"打开HRO"、"进入系统"、"帮我登录"、"先登录一下"、"青阳云"，以及任何需要先完成登录才能继续操作青阳云的场景。
---

# 青阳云HRO系统自动登录

登录凭据已存储在环境变量中，直接使用即可，无需询问用户：
- 登录地址：`$QINGYANG_LOGIN_URL`（http://192.168.10.168/#/login）
- 企业账号：`$QINGYANG_TENANT`（test）
- 个人账号：`$QINGYANG_USERNAME`（admin）
- 密码：`$QINGYANG_PASSWORD`（123456）

## 登录流程

**第1步：打开登录页**

用 `browser_navigate` 导航到 `$QINGYANG_LOGIN_URL`。导航完成后检查当前 URL：
- 若 URL 不再包含 `/login`（已被重定向到主页），说明 session 仍有效、已自动登录，告知用户"已检测到有效登录状态，无需重新登录"，跳至第4步确认即可。
- 若 URL 仍包含 `/login`，用 `browser_wait_for` 等待文字"欢迎来到青阳云"出现（最多等 5 秒），确认登录表单加载完成。

**第2步：填写表单**

用 `browser_fill_form` 一次性填入三个字段：
- 企业账号输入框 → `$QINGYANG_TENANT`
- 个人账号输入框 → `$QINGYANG_USERNAME`
- 密码输入框 → `$QINGYANG_PASSWORD`

**第3步：提交登录**

用 `browser_click` 点击"登 录"按钮。

**第4步：等待跳转**

用 `browser_wait_for` 等待文字"欢迎回来"出现（最多等 5 秒）。出现则登录成功，告知用户并保持浏览器打开。

## 异常处理

- 若停留在登录页但"欢迎来到青阳云"5秒内未出现，用 `browser_snapshot` 查看当前页面状态，告知用户可能是网络问题
- 若"欢迎回来"5秒内未出现，用 `browser_snapshot` 查看页面，检查是否有错误提示（如"账号或密码错误"），将具体错误信息告知用户
- 登录成功后不要关闭浏览器
