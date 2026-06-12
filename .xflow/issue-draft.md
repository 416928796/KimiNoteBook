# 实现基于 Vue + Element Plus 的 Kimi 会话浏览器与 Markdown 导出功能

## 背景

当前 Kimi Code CLI 的会话数据存放在 `~/.kimi-code/sessions/` 目录下，每个会话以 `wire.jsonl` 文件记录完整对话过程。为了方便用户回顾、整理和导出与模型的对话内容，需要一个可视化的 Web 系统来浏览这些本地会话，并支持将选中的问答内容导出为 Markdown。

## 目标

构建一个基于网页的系统，能够：

1. **读取本地会话目录**：扫描 `~/.kimi-code/sessions/`（可配置），解析每个 `wire.jsonl` 与会话元数据 `state.json`。
2. **会话列表展示**：以卡片或表格形式展示所有会话，显示标题、创建时间、消息数等关键信息，支持搜索与排序。
3. **对话详情展示**：点击会话后进入详情页，仅展示「用户提问」与「模型回答」的内容，过滤掉工具调用、系统事件等非对话消息。
4. **Markdown 导出**：在详情页中，用户可以勾选任意问答对，导出为 `.md` 文件。
5. **界面美观与动效**：使用 Vue 3 + Element Plus 构建响应式界面，列表↔详情切换、卡片悬停、加载状态等需有过渡动画。

## 技术栈

- 前端：Vue 3 + Element Plus + Vue Router + Pinia（可选）+ CSS Transitions
- 后端：Python + FastAPI（提供读取本地文件系统的 API，避免浏览器直接访问本地路径的安全限制）
- 构建：Vite
- 会话解析：自定义 `wire.jsonl` 解析器，兼容旧版 `protocol_version: 1.0` 与新版 `1.3/1.4`

## 验收标准（TDD）

### 后端 API

- [ ] `GET /api/sessions` 返回会话列表，每个会话至少包含 `id`、`title`、`createdAt`、`messageCount`。
- [ ] `GET /api/sessions/:id` 返回指定会话的用户-模型问答对数组。
- [ ] `POST /api/sessions/:id/export` 接收 `selectedIndices`，返回对应问答对的 Markdown 文本。
- [ ] 当会话目录不存在或 `wire.jsonl` 格式不兼容时，API 返回清晰的错误信息，不崩溃。

### 前端交互

- [ ] 首页加载会话列表，空状态时展示友好提示。
- [ ] 点击会话卡片/行后，通过动画过渡到详情页。
- [ ] 详情页展示问答对，每个问答对可单独勾选。
- [ ] 点击「导出 Markdown」后，浏览器下载 `.md` 文件。
- [ ] 返回按钮可从详情页回到列表页。

### 会话解析

- [ ] 解析器能正确提取旧版 `context.append_message` 类型中的用户与助手消息。
- [ ] 解析器能正确提取新版 `context.append_loop_event` 类型中的用户与助手消息。
- [ ] 过滤掉工具调用、配置事件、权限事件等非对话消息。

## 建议测试命令

```bash
# 后端单元测试
cd server && pytest

# 前端单元测试
cd web && npm test

# 端到端：启动前后端后验证 API
curl http://localhost:8000/api/sessions
```

## 非目标

- 不实现远程会话同步。
- 不实现用户登录与权限管理。
- 不修改 Kimi Code CLI 的原始会话文件。
