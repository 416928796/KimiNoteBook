# Issue #7：支持读取 kimi-legacy 会话记录 — 变更交付

## 关联

- Issue: [#7 支持读取 kimi-legacy 会话记录](https://github.com/416928796/KimiNoteBook/issues/7)
- 分支: `feat/7-support-kimi-legacy`

## 修改文件

### 后端

- `server/app/config.py`
  - 新增 `get_legacy_sessions_root()`，默认返回 `~/.kimi/sessions`。
- `server/app/models/session.py`
  - `SessionSummary` / `SessionDetail` 增加 `source` 字段，默认 `"kimi-code"`。
- `server/app/services/session_parser.py`
  - 扩展 `_parse_datetime` 支持浮点数秒。
  - 新增 `parse_legacy_wire_records()` 解析 kimi-legacy 的 `TurnBegin` / `StepBegin` / `ContentPart` / `TurnEnd` 协议。
  - `parse_session()` 增加 `source` 参数，按来源选择 wire 解析策略与 state.json 字段兼容逻辑。
  - `list_sessions()` 合并扫描新版与 legacy 两个根目录。
- `server/app/routers/sessions.py`
  - `_find_session_dir()` 改为在新版与 legacy 根目录中查找，返回 `(path, source)`，新版优先。
  - `get_session()` / `export_session()` 使用解析出的 source 调用 `parse_session()`。

### 前端

- `web/src/types/index.ts`
  - `SessionSummary` 增加可选 `source` 字段。
- `web/src/components/SessionCard.vue`
  - 在卡片头部显示来源标签：`kimi-legacy` → "Kimi Legacy"（warning），其他 → "新版 Kimi"（success）。
- `web/src/views/SessionDetailView.vue`
  - 在详情页 meta 信息中显示来源标签。

### 测试

- `server/tests/fixtures/legacy/`
  - 新增 legacy 会话测试夹具（`state.json` + `wire.jsonl`）。
- `server/tests/test_session_parser.py`
  - 新增 `test_parse_legacy_wire_records`。
  - 新增 `test_parse_session_legacy_format`。
  - 新增 `test_list_sessions_merges_sources`。
  - 修复 `test_list_sessions` 以隔离 legacy 根目录。
- `server/tests/test_api.py`
  - 新增 `client_with_legacy` fixture。
  - 新增 `test_list_sessions_includes_legacy`。
  - 新增 `test_get_legacy_session`。
  - 新增 `test_export_legacy_session`。

## 验证结果

```bash
$ npm test

> kiminotebook@0.1.0 test
> npm run test:server && npm run test:web

# 后端
21 passed

# 前端
2 passed (5 tests)
```

前端 TypeScript 类型检查：

```bash
$ cd web && npx vue-tsc -b
# 无错误
```

真实环境联调：

```bash
$ cd server && python -m uvicorn app.main:app --port 8003
$ curl http://localhost:8003/api/sessions | jq '{count: length, sources: map(.source) | unique}'
{
  "count": 360,
  "sources": ["kimi-code", "kimi-legacy"]
}
```

## 联调中发现并修复的问题

1. **毫秒 vs 秒时间戳混淆**
   - 现象：启动后 `/api/sessions` 报 `OSError: [Errno 22] Invalid argument`。
   - 原因：新版 `wire.jsonl` 的 `time` 字段为毫秒整数，而 kimi-legacy 为浮点秒；统一按秒解析导致整数过大。
   - 修复：`_parse_datetime` 中 `int` 按毫秒处理，`float` 按秒处理。

2. **时区感知与不感知 datetime 混排**
   - 现象：修复时间戳后报 `TypeError: can't compare offset-naive and offset-aware datetimes`。
   - 原因：ISO 字符串含 `Z` 时解析为 aware datetime，而时间戳解析为 naive datetime，排序时无法比较。
   - 修复：ISO 解析后若带时区则转换为 naive datetime。

## 行为变更

- 新版 Kimi 会话的原有行为完全不变。
- 若用户 `~/.kimi/sessions/` 目录存在且包含有效 legacy 会话，启动后端后列表会自动合并展示。
- 详情页、导出 Markdown 对 legacy 会话与新版会话体验一致。
