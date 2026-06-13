# Issue #3 开发进度看板

## 全局

- [x] 创建远程 Issue #3
- [x] 编写 implementation_plan.md
- [x] 切出功能分支 `feat/3-improve-ui-and-export-markdown`

---

## 后端（导出 Markdown 标题降级）

- [x] 先编写/确认对应的失败测试：导出 Markdown 分节标题为 `# 用户` / `# 模型`
- [x] 先编写/确认对应的失败测试：内容中的 Markdown 标题统一降级一级
- [x] 修改 `server/app/routers/sessions.py` 调整导出结构
- [x] 运行 `pytest` 并通过

---

## 前端（Kimi Logo）

- [x] 新增 `web/public/kimi-logo.svg`
- [x] 修改 `web/src/views/SessionListView.vue` 替换 `ChatLineRound` 图标
- [x] 运行 `npm run build` 验证资源引用

---

## 前端（Markdown 渲染开关）

- [x] 安装 `marked` 与 `@types/marked`、`dompurify`
- [x] 先编写/确认对应的失败测试：MessageItem 渲染模式切换
- [x] 在 `web/src/stores/sessions.ts` 增加 `renderMode` 状态
- [x] 新增 `web/src/components/RenderToggle.vue` 悬浮开关
- [x] 修改 `web/src/components/MessageItem.vue` 支持双模式展示
- [x] 修改 `web/src/views/SessionDetailView.vue` 集成开关
- [x] 运行 `npm test` 并通过
- [x] 运行 `npm run build` 并通过

---

## 集成与交付

- [x] 运行全部测试：`npm test`
- [x] 更新 walkthrough.md
- [x] 提交代码并发起 PR
