# Issue #3 变更交付

## 变更摘要

对 KimiNoteBook 进行三项体验优化：

1. 将顶部标题栏的聊天图标替换为 Kimi Logo。
2. 在会话详情页增加悬浮开关，切换原生 Markdown 源码 / 渲染后展示。
3. 调整导出 Markdown 的大纲结构：用户/模型分节作为一级标题，其内部 Markdown 标题统一降级一级。

## 修改文件

### 后端

- `server/app/routers/sessions.py` — 调整导出 Markdown 标题结构，新增 `_demote_headings` 函数对内容标题降级。
- `server/tests/test_api.py` — 补充导出格式断言，验证 `# 用户` / `# 模型` 分节与内容标题降级。

### 前端

- `web/public/kimi-logo.svg` — 新增 Kimi Logo SVG 资源。
- `web/src/views/SessionListView.vue` — 使用 `<img>` 替换 `ChatLineRound` 图标。
- `web/src/stores/sessions.ts` — 新增 `renderMode` 状态与 `setRenderMode` 方法。
- `web/src/components/RenderToggle.vue` — 新增详情页右下角悬浮渲染切换开关。
- `web/src/components/MessageItem.vue` — 支持源码 `<pre>` 与 `marked` 渲染后 HTML 双模式展示。
- `web/src/views/SessionDetailView.vue` — 集成 `RenderToggle`。
- `web/src/utils/markdown.ts` — 新增 `demoteHeadings`，同步前端导出预览格式。
- `web/src/components/__tests__/MessageItem.spec.ts` — 新增 MessageItem 双模式切换测试。
- `web/package.json` — 新增 `marked`、`dompurify`、`@types/marked`、`@types/dompurify` 依赖。

### 规划文件

- `.xflow/issue-3/implementation_plan.md`
- `.xflow/issue-3/task.md`
- `.xflow/issue-3/walkthrough.md`
- `.xflow/issue-3/issue-body.md`

## 测试命令与结果

### 后端测试

```bash
cd server && .venv\Scripts\python.exe -m pytest -v
```

结果：`13 passed`

### 前端测试

```bash
cd web && npm test
```

结果：`5 passed`（新增 3 个 MessageItem 测试）

### 前端构建

```bash
cd web && npm run build
```

结果：构建成功（存在与 node_modules 注释相关的无关警告）

### 全部测试

```bash
npm test
```

结果：后端 13 passed，前端 5 passed

## 注意事项

- 渲染模式默认开启，使用 `marked` 解析 Markdown，`DOMPurify` 对生成 HTML 做基础消毒。
- 导出 Markdown 中内容标题降级时，代码块（```...```）内的 `#` 不会被误处理。
