# Issue #1 实现方案

## 目标

为 KimiNoteBook 项目实现一个基于网页的本地会话浏览器：
- 读取 `~/.kimi-code/sessions/` 目录下的 Kimi Code CLI 会话
- 列表展示会话，详情展示用户与模型的问答对
- 支持勾选任意问答对导出为 Markdown
- 界面使用 Vue 3 + Element Plus，切换有过渡动画

## 开放性问题

1. 会话目录路径是否需要可配置？
   - **决策**：第一期硬编码为 `~/.kimi-code/sessions/`（通过后端环境变量或配置文件），后续再考虑 UI 配置。
2. 新旧 wire.jsonl 格式差异如何处理？
   - **决策**：后端解析器统一处理两种协议版本，前端只接收标准化后的问答对数组。
3. 是否需要持久化导出模板？
   - **决策**：第一期使用固定 Markdown 模板，后续按需扩展。

## 架构设计

采用前后端分离架构，后端负责本地文件系统访问，前端负责展示与交互。

### 目录树 diff

```
KimiNoteBook/
├── .xflow/
│   └── issue-1/
│       ├── implementation_plan.md
│       ├── task.md
│       └── walkthrough.md
├── server/                              # 新增：FastAPI 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI 应用入口、CORS、路由挂载
│   │   ├── config.py                    # 会话目录等配置
│   │   ├── models/
│   │   │   └── session.py               # Pydantic 模型：Session / QAPair / ExportRequest
│   │   ├── routers/
│   │   │   └── sessions.py              # REST API：/api/sessions / /api/sessions/{id} / /api/sessions/{id}/export
│   │   └── services/
│   │       └── session_parser.py        # wire.jsonl / state.json 解析器
│   ├── tests/
│   │   ├── fixtures/                    # 测试用的旧版/新版 wire.jsonl 样本
│   │   │   ├── old_format/
│   │   │   │   └── wire.jsonl
│   │   │   └── new_format/
│   │   │       └── wire.jsonl
│   │   └── test_session_parser.py       # 解析器单元测试
│   ├── requirements.txt
│   └── pyproject.toml
├── web/                                 # 新增：Vue 3 前端
│   ├── src/
│   │   ├── api/
│   │   │   └── sessions.ts              # axios 封装的 API 调用
│   │   ├── components/
│   │   │   ├── SessionCard.vue          # 会话卡片（列表页）
│   │   │   ├── MessageItem.vue          # 单条问答展示
│   │   │   └── ExportDialog.vue         # 导出确认弹窗
│   │   ├── router/
│   │   │   └── index.ts                 # / 列表页， /sessions/:id 详情页
│   │   ├── stores/
│   │   │   └── sessions.ts              # Pinia store
│   │   ├── types/
│   │   │   └── index.ts                 # TypeScript 类型定义
│   │   ├── utils/
│   │   │   └── markdown.ts              # Markdown 导出与下载
│   │   ├── views/
│   │   │   ├── SessionListView.vue      # 会话列表页
│   │   │   └── SessionDetailView.vue    # 会话详情页
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css                    # 全局样式与动画
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── package.json                         # 根目录：同时启动前后端的脚本
└── README.md                            # 更新：补充项目说明与启动方式
```

### 模块职责

| 模块 | 职责 |
|------|------|
| `server/app/services/session_parser.py` | 唯一负责读取本地文件系统并解析 `wire.jsonl` 为标准化数据结构 |
| `server/app/routers/sessions.py` | 定义 REST API，参数校验，异常转换 |
| `server/app/models/session.py` | 定义请求/响应数据模型 |
| `web/src/api/sessions.ts` | 封装 axios，统一错误处理 |
| `web/src/stores/sessions.ts` | 管理会话列表、当前会话、加载状态 |
| `web/src/views/*.vue` | 页面级组件，负责布局与路由 |
| `web/src/components/*.vue` | 可复用 UI 组件 |

## 依赖关系

- 后端不依赖前端，仅依赖 Python 标准库 + FastAPI + Pydantic
- 前端依赖后端 API，通过 axios 调用
- 解析器只读取 `.kimi-code/sessions`，不写回任何文件

## API 设计

```
GET  /api/sessions
     Response: [{ id, title, createdAt, updatedAt, messageCount }]

GET  /api/sessions/{session_id}
     Response: { id, title, createdAt, updatedAt, qaPairs: [{ index, role, content, createdAt }] }

POST /api/sessions/{session_id}/export
     Body: { selectedIndices: number[] }
     Response: text/markdown; 浏览器触发下载
```

## 测试策略

1. **解析器单元测试**：使用旧版/新版 fixture 验证提取结果
2. **API 集成测试**：启动 TestClient 调用三个端点
3. **前端组件测试**：使用 Vitest + Vue Test Utils 验证列表/详情/导出

## 关键实现注意点

1. `wire.jsonl` 首行为 metadata，后续行为事件记录；仅提取 `role` 为 `user` / `assistant` 的消息。
2. 新版 `context.append_loop_event` 的事件对象嵌套在 `event.message` 或 `event.content` 中，需递归查找 role。
3. 导出 Markdown 时，使用 `## User` 和 `## Assistant` 作为标题，保留原始顺序。
4. 前端动画统一使用 Vue `<Transition>` + `<TransitionGroup>` + Element Plus 的 loading 动画。
