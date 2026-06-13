# Issue #7：支持读取 kimi-legacy 会话记录 — 实现方案

## 目标

在不影响现有新版 Kimi Code CLI 会话支持的前提下，让 KimiNoteBook 后端同时读取 `~/.kimi/sessions/`（kimi-legacy）下的历史会话，并在前端以相同方式展示、详情、导出。

## 开放性问题

- 已确认 kimi-legacy 会话根目录为 `~/.kimi/sessions/<workspace_hash>/<session_id>/`。
- 已确认 legacy `wire.jsonl` 协议与新版本完全不同，需新增独立解析器。
- 已确认 legacy `state.json` 使用 `custom_title` 字段且无 `created_at`，需兼容读取。
- session_id 在新旧两版均为 UUID 形式，存在理论冲突可能。本方案通过后端自动按“新版优先、legacy 兜底”的顺序查找，保持 API 路径不变；同时在前端展示 `source` 标签，便于用户识别。

## 拟修改文件列表

```
server/
  app/
    config.py                  # 新增 get_legacy_sessions_root()
    models/session.py          # SessionSummary / SessionDetail 增加 source 字段
    services/session_parser.py # 新增 legacy 解析器、统一 list_sessions / parse_session
    routers/sessions.py        # _find_session_dir 支持跨两个根目录查找
  tests/
    fixtures/legacy/           # 新增 legacy 会话测试夹具
      state.json
      wire.jsonl
    test_session_parser.py     # 新增 legacy 解析测试与混合 list_sessions 测试
    test_api.py                # 新增 legacy API 测试
web/
  src/
    models/session.ts          # 增加 source 字段类型
    components/SessionCard.vue # 显示 source 标签
    views/SessionDetailView.vue # 显示 source 标签
    views/SessionListView.vue  # 可选：搜索/筛选时不依赖 source
```

## 架构设计

### 后端数据源抽象

引入“会话来源（source）”概念，但**不**改变现有数据模型职责：

- `source == "kimi-code"`：来自 `~/.kimi-code/sessions/`，使用现有 `parse_wire_records` 解析。
- `source == "kimi-legacy"`：来自 `~/.kimi/sessions/`，使用新增 `parse_legacy_wire_records` 解析。

`list_sessions()` 改为返回合并后的列表；`parse_session(session_dir, source)` 根据 source 选择解析策略。`_find_session_dir(session_id)` 先在新版根目录查找，未找到再去 legacy 根目录查找，保证现有 API 路径不变。

### 前端展示

- 仅增加来源标签展示，不改动路由、不改动导出逻辑。
- `source` 字段由后端返回，前端 TS 类型同步扩展。

### 依赖关系

- `config.py` 只依赖 `pathlib`/`os`，不依赖上层业务。
- `session_parser.py` 依赖 `config.py` 和 `models/session.py`，方向正确。
- `routers/sessions.py` 依赖 `session_parser.py` 和 `config.py`。
- 无反向依赖、无循环依赖。

## 目录拓扑 diff

```diff
 server/tests/fixtures/
   old/
   new/
+  legacy/
+    state.json
+    wire.jsonl
```

仅新增测试夹具目录，无其他目录调整。

## 验收标准

- [ ] 后端单测新增 legacy wire.jsonl 解析测试。
- [ ] 后端单测新增 legacy 会话目录解析测试。
- [ ] 后端单测验证 `list_sessions()` 可同时返回两种来源会话。
- [ ] API 单测验证 legacy 会话可列表、可详情、可导出。
- [ ] 现有新版会话测试全部通过。
- [ ] `npm test` 全部通过。
