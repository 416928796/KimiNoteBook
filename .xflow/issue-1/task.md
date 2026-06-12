# Issue #1 开发进度看板

## 全局

- [x] 创建远程 Issue #1
- [x] 编写 implementation_plan.md
- [ ] 切出功能分支 `feature/1-implement-session-browser-and-export`

---

## 后端（FastAPI）

### 会话解析器

- [ ] 先编写/确认对应的失败测试：旧版 wire.jsonl 解析
- [ ] 先编写/确认对应的失败测试：新版 wire.jsonl 解析
- [ ] 实现 `session_parser.py`：读取 state.json + wire.jsonl
- [ ] 实现新旧格式兼容：提取 user/assistant 消息，过滤工具事件
- [ ] 运行 `pytest` 并通过

### API 路由

- [ ] 先编写/确认对应的失败测试：`GET /api/sessions`
- [ ] 先编写/确认对应的失败测试：`GET /api/sessions/{id}`
- [ ] 先编写/确认对应的失败测试：`POST /api/sessions/{id}/export`
- [ ] 实现 `routers/sessions.py`
- [ ] 实现 CORS 与异常处理
- [ ] 运行 `pytest` 并通过

---

## 前端（Vue 3 + Element Plus）

### 项目脚手架

- [ ] 使用 Vite 初始化 `web/` 目录
- [ ] 安装 Element Plus、Vue Router、Pinia、axios
- [ ] 配置路由：列表页 / 详情页

### API 与状态

- [ ] 实现 `api/sessions.ts` axios 封装
- [ ] 实现 Pinia store 管理会话数据

### 列表页

- [ ] 实现 `SessionListView.vue`
- [ ] 实现 `SessionCard.vue` 卡片组件
- [ ] 添加加载动画、空状态、搜索过滤
- [ ] 添加进入详情页的过渡动画

### 详情页

- [ ] 实现 `SessionDetailView.vue`
- [ ] 实现 `MessageItem.vue` 展示问答对
- [ ] 实现问答对勾选、全选/反选
- [ ] 实现返回列表页动画

### 导出功能

- [ ] 实现 `ExportDialog.vue`
- [ ] 实现 `utils/markdown.ts` Markdown 拼接与下载
- [ ] 联调后端导出 API

---

## 集成与交付

- [ ] 根目录添加 `package.json` 一键启动脚本
- [ ] 更新 README.md 使用说明
- [ ] 端到端验证：启动前后端，浏览会话，导出 Markdown
- [ ] 提交代码并发起 PR
- [ ] 更新 walkthrough.md
