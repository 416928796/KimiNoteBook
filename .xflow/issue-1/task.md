# Issue #1 开发进度看板

## 全局

- [x] 创建远程 Issue #1
- [x] 编写 implementation_plan.md
- [x] 切出功能分支 `feat/1-implement-session-browser-and-export`

---

## 后端（FastAPI）

### 会话解析器

- [x] 先编写/确认对应的失败测试：旧版 wire.jsonl 解析
- [x] 先编写/确认对应的失败测试：新版 wire.jsonl 解析
- [x] 实现 `session_parser.py`：读取 state.json + wire.jsonl
- [x] 实现新旧格式兼容：提取 user/assistant 消息，过滤工具事件
- [x] 运行 `pytest` 并通过

### API 路由

- [x] 先编写/确认对应的失败测试：`GET /api/sessions`
- [x] 先编写/确认对应的失败测试：`GET /api/sessions/{id}`
- [x] 先编写/确认对应的失败测试：`POST /api/sessions/{id}/export`
- [x] 实现 `routers/sessions.py`
- [x] 实现 CORS 与异常处理
- [x] 运行 `pytest` 并通过

---

## 前端（Vue 3 + Element Plus）

### 项目脚手架

- [x] 使用 Vite 初始化 `web/` 目录
- [x] 安装 Element Plus、Vue Router、Pinia、axios
- [x] 配置路由：列表页 / 详情页

### API 与状态

- [x] 实现 `api/sessions.ts` axios 封装
- [x] 实现 Pinia store 管理会话数据

### 列表页

- [x] 实现 `SessionListView.vue`
- [x] 实现 `SessionCard.vue` 卡片组件
- [x] 添加加载动画、空状态、搜索过滤
- [x] 添加进入详情页的过渡动画

### 详情页

- [x] 实现 `SessionDetailView.vue`
- [x] 实现 `MessageItem.vue` 展示问答对
- [x] 实现问答对勾选、全选/反选
- [x] 实现返回列表页动画

### 导出功能

- [x] 实现 `ExportDialog.vue`
- [x] 实现 `utils/markdown.ts` Markdown 拼接与下载
- [x] 联调后端导出 API

---

## 集成与交付

- [x] 根目录添加 `package.json` 一键启动脚本
- [x] 更新 README.md 使用说明
- [x] 端到端验证：启动前后端，浏览会话，导出 Markdown
- [x] 提交代码并发起 PR
- [x] 更新 walkthrough.md
