# Issue #7：支持读取 kimi-legacy 会话记录 — 任务看板

## 阶段 1：准备与规划

- [x] 探查项目上下文（README、后端结构、测试结构）。
- [x] 定位 kimi-legacy 会话存储路径与文件格式差异。
- [x] 编写并创建远程 Issue #7。
- [x] 编写实现方案（implementation_plan.md）。
- [x] 切换开发分支。

## 阶段 2：后端 TDD 开发

- [x] 编写 legacy wire.jsonl 解析失败测试。
- [x] 实现 legacy wire.jsonl 解析器，使测试通过。
- [x] 编写 legacy 会话目录解析失败测试。
- [x] 实现 legacy 会话目录解析，使测试通过。
- [x] 编写混合 list_sessions 失败测试（同时包含新版与 legacy）。
- [x] 修改 `list_sessions()` 支持双数据源，使测试通过。
- [x] 修改 `_find_session_dir()` 支持跨根目录查找。
- [x] 运行后端全部测试，确保零破坏。

## 阶段 3：前端展示

- [x] 更新 TS 类型增加 source 字段。
- [x] 在 SessionCard 显示 source 标签。
- [x] 在 SessionDetailView 显示 source 标签。
- [x] 运行前端测试与 typecheck，确保零破坏。

## 阶段 4：验证与交付

- [x] 运行完整 `npm test`。
- [ ] 更新 walkthrough.md。
- [ ] 提交 PR/MR。
