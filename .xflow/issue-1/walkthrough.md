# Issue #1 变更交付

## 变更摘要

实现了一个基于 Vue 3 + Element Plus + FastAPI 的本地 Kimi 会话浏览器，支持会话列表展示、详情查看、问答对勾选导出 Markdown。

## 修改文件

### 后端

- `server/app/main.py` — FastAPI 应用入口，CORS 配置
- `server/app/config.py` — 会话目录配置
- `server/app/models/session.py` — Pydantic 数据模型
- `server/app/routers/sessions.py` — REST API 路由
- `server/app/services/session_parser.py` — wire.jsonl 解析器
- `server/tests/test_session_parser.py` — 解析器单元测试
- `server/tests/test_api.py` — API 集成测试
- `server/tests/fixtures/old/` — 旧版 wire.jsonl fixture
- `server/tests/fixtures/new/` — 新版 wire.jsonl fixture
- `server/requirements.txt` / `server/pyproject.toml` — 依赖配置

### 前端

- `web/src/main.ts` — Vue 应用入口
- `web/src/App.vue` — 页面过渡动画
- `web/src/router/index.ts` — 路由配置
- `web/src/stores/sessions.ts` — Pinia 状态管理
- `web/src/api/sessions.ts` — API 封装
- `web/src/utils/markdown.ts` — Markdown 导出工具
- `web/src/types/index.ts` — TypeScript 类型
- `web/src/views/SessionListView.vue` — 会话列表页
- `web/src/views/SessionDetailView.vue` — 会话详情页
- `web/src/components/SessionCard.vue` — 会话卡片
- `web/src/components/MessageItem.vue` — 问答展示
- `web/src/components/ExportDialog.vue` — 导出弹窗
- `web/src/components/__tests__/SessionCard.spec.ts` — 组件测试
- `web/src/style.css` — 全局样式
- `web/vite.config.ts` / `web/vitest.config.ts` — 构建与测试配置
- `web/package.json` / `web/tsconfig.app.json` — 项目配置

### 项目根目录

- `package.json` — 一键启动前后端脚本
- `README.md` — 项目说明与使用方式
- `.gitignore` — 忽略缓存与依赖目录

## 测试命令与结果

### 后端测试

```bash
cd server && PYTHONPATH=. pytest -v
```

结果：13 passed

### 前端测试

```bash
cd web && npm test
```

结果：2 passed

### 前端构建

```bash
cd web && npm run build
```

结果：构建成功

### 端到端验证

```bash
npm run dev:server  # 端口 8000
npm run dev:web     # 端口 5173
```

已验证：

- `GET /api/sessions` 返回本地会话列表
- `GET /api/sessions/{id}` 返回问答对详情
- `POST /api/sessions/{id}/export` 返回 Markdown 文件
- 前端代理 `/api` 到后端正常工作

## 注意事项

- 后端默认读取 `~/.kimi-code/sessions/`，可通过 `SESSIONS_ROOT` 环境变量覆盖。
- 解析器兼容旧版 `protocol_version: 1.0` 与新版 `1.3/1.4`，已过滤 `<system-reminder>` 系统提示。
