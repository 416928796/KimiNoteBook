# Issue #3 实现方案

## 目标

对 KimiNoteBook 进行三项体验优化：

1. 将顶部标题栏的聊天图标替换为 Kimi Logo。
2. 在会话详情页增加悬浮开关，切换原生 Markdown 源码 / 渲染后展示。
3. 将导出 Markdown 中「用户 / 模型」分节标题作为一级标题，并将其内部 Markdown 标题统一降级一级。

## 开放性问题

1. **Kimi Logo 来源**
   - **决策**：使用一个自包含的 SVG 组件 `KimiLogo.vue`，不依赖外部图片资源，避免网络请求与版权问题。Logo 采用简化的「K」字形几何风格，主色使用 Element Plus 主题色。
2. **Markdown 渲染库选择**
   - **决策**：前端使用 `marked` 进行渲染，体积小、只读场景成熟。不对 HTML 做额外过滤（内容来自本地可信会话文件），但使用 Vue 的 `v-html` 时仍通过 DOMPurify 做基础消毒。
3. **大纲降级边界**
   - **决策**：仅对导出 Markdown 中用户/模型消息内部的标题进行降级（`#` → `##`、`##` → `###` 等），代码块内的标题语法不处理。用户/模型分节标题本身固定为 `# 用户` / `# 模型`。文件顶部仍保留 `# {session.title}`。

## 架构设计

本次改动集中在表现层与导出格式层，不触及会话解析与数据模型。

### 目录树 diff

```
KimiNoteBook/
├── .xflow/
│   └── issue-3/
│       ├── implementation_plan.md
│       ├── task.md
│       ├── walkthrough.md
│       └── issue-body.md
├── server/
│   └── app/
│       └── routers/
│           └── sessions.py          # 修改：调整导出 Markdown 的标题层级
├── web/
│   ├── public/
│   │   └── kimi-logo.svg            # 新增：Kimi Logo SVG 资源
│   ├── src/
│   │   ├── components/
│   │   │   ├── KimiLogo.vue         # 新增：SVG Logo 组件
│   │   │   ├── MessageItem.vue      # 修改：支持源码/渲染双模式
│   │   │   └── RenderToggle.vue     # 新增：悬浮渲染切换开关
│   │   ├── stores/
│   │   │   └── sessions.ts          # 修改：详情页渲染模式全局状态
│   │   ├── utils/
│   │   │   └── markdown.ts          # 修改：新增标题降级函数
│   │   └── views/
│   │       ├── SessionListView.vue  # 修改：替换图标为 KimiLogo
│   │       └── SessionDetailView.vue # 修改：集成 RenderToggle
│   └── package.json                 # 修改：新增 marked、dompurify 依赖
└── server/tests/test_api.py         # 修改：补充导出格式断言
```

### 模块职责

| 模块 | 职责 |
|------|------|
| `web/src/components/KimiLogo.vue` | 渲染 Kimi 品牌 SVG Logo |
| `web/src/components/RenderToggle.vue` | 提供详情页右下角悬浮开关，切换全局渲染模式 |
| `web/src/components/MessageItem.vue` | 根据当前模式展示源码 `<pre>` 或渲染后的 HTML |
| `web/src/stores/sessions.ts` | 维护 `renderMode: 'source' \| 'rendered'` 状态 |
| `web/src/utils/markdown.ts` | 提供 `renderMarkdown` 与 `demoteHeadings` 工具函数 |
| `server/app/routers/sessions.py` | 调整导出 Markdown 的标题结构并降级内容标题 |
| `server/tests/test_api.py` | 验证导出 Markdown 中分节标题与内容降级 |

## 依赖关系

- 前端新增 `marked` 与 `@types/marked`（开发依赖），可选 `dompurify` 做 HTML 消毒。
- 后端仅使用 Python 标准库正则处理标题降级，不新增依赖。
- 后端导出逻辑依赖 `session_parser` 输出的 `QAPair`，接口不变。

## API 调整

`POST /api/sessions/{session_id}/export` 返回的 Markdown 结构变更为：

```markdown
# {session.title}

_导出时间：{iso_time}_

# 用户

{用户内容（标题已降级）}

# 模型

{模型内容（标题已降级）}
```

## 测试策略

1. **后端单元测试**：在 `test_api.py` 中新增测试，验证导出内容包含 `# 用户` / `# 模型`，且内容中的 `#` 已降级为 `##`。
2. **前端单元测试**：在 `SessionCard.spec.ts` 同级新增 `MessageItem.spec.ts`，验证源码模式与渲染模式切换。
3. **前端构建**：运行 `vue-tsc -b && vite build` 确保类型无误。
