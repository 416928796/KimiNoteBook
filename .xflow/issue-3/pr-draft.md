# 优化会话浏览器 UI 与 Markdown 导出格式

## 变更内容

本 PR 对 KimiNoteBook 进行三项体验优化：

- **Kimi Logo**：列表页顶部标题左侧的聊天图标已替换为 Kimi Logo（SVG 资源）。
- **Markdown 渲染开关**：详情页右下角新增悬浮开关，可在「源码」与「渲染」两种展示模式间切换。渲染模式使用 `marked` 解析 Markdown，`DOMPurify` 做 HTML 消毒。
- **导出大纲降级**：导出 Markdown 中「用户 / 模型」分节标题改为一级标题 `# 用户` / `# 模型`，其内部所有 Markdown 标题统一降级一级，避免大纲结构混乱。

## 主要文件

- `server/app/routers/sessions.py` — 调整导出 Markdown 结构与标题降级
- `web/src/views/SessionListView.vue` — 替换顶部图标
- `web/src/components/MessageItem.vue` — 双模式展示
- `web/src/components/RenderToggle.vue` — 悬浮切换开关
- `web/src/stores/sessions.ts` — 渲染模式状态

## 验证方式

```bash
npm test         # 后端 13 passed，前端 5 passed
cd web && npm run build
```

Closes #3
