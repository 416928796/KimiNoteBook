# 实现基于 Vue + Element Plus 的 Kimi 会话浏览器与 Markdown 导出

## 变更内容

本 PR 实现了一个完整的本地 Kimi 会话浏览器：

- **后端（FastAPI）**：读取 `~/.kimi-code/sessions/`，解析新旧两种 `wire.jsonl` 格式，提供会话列表、详情、Markdown 导出三个 REST API。
- **前端（Vue 3 + Element Plus）**：美观的会话卡片列表、详情页问答对展示、勾选导出 Markdown，列表↔详情切换带有过渡动画。
- **测试**：后端 13 个 pytest 用例，前端 2 个 Vitest 组件测试。

## 主要文件

- `server/app/services/session_parser.py` — 会话解析器
- `server/app/routers/sessions.py` — API 路由
- `web/src/views/SessionListView.vue` — 列表页
- `web/src/views/SessionDetailView.vue` — 详情页
- `web/src/components/ExportDialog.vue` — 导出弹窗

## 验证方式

```bash
npm install
npm run dev      # 同时启动前后端
npm test         # 运行全部测试
```

## 截图

（可在本地 http://localhost:5173 查看效果）

Closes #1
