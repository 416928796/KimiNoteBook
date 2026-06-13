import json
from pathlib import Path

import pytest

from app.services.session_parser import (
    parse_session,
    list_sessions,
    parse_wire_records,
    parse_legacy_wire_records,
    format_content,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_format_content_text():
    content = [{"type": "text", "text": "Hello"}]
    assert format_content(content) == "Hello"


def test_format_content_think_and_text():
    content = [
        {"type": "think", "think": "Thinking..."},
        {"type": "text", "text": "Answer."},
    ]
    assert format_content(content) == "Answer."


def test_format_content_text_dict():
    assert format_content({"type": "text", "text": "Plain"}) == "Plain"


def test_parse_wire_records_old_format():
    wire_path = FIXTURES / "old" / "agents" / "main" / "wire.jsonl"
    qa_pairs = parse_wire_records(wire_path)
    assert len(qa_pairs) == 4
    assert qa_pairs[0].role == "user"
    assert "Hello" in qa_pairs[0].content
    assert qa_pairs[1].role == "assistant"
    assert "coding" in qa_pairs[1].content
    assert qa_pairs[2].role == "user"
    assert qa_pairs[3].role == "assistant"
    assert "print" in qa_pairs[3].content


def test_parse_wire_records_new_format():
    wire_path = FIXTURES / "new" / "agents" / "main" / "wire.jsonl"
    qa_pairs = parse_wire_records(wire_path)
    assert len(qa_pairs) == 4
    assert qa_pairs[0].role == "user"
    assert "Hello" in qa_pairs[0].content
    assert qa_pairs[1].role == "assistant"
    assert "coding" in qa_pairs[1].content
    assert qa_pairs[2].role == "user"
    assert qa_pairs[3].role == "assistant"
    assert "print" in qa_pairs[3].content


def test_parse_legacy_wire_records():
    wire_path = FIXTURES / "legacy" / "wire.jsonl"
    qa_pairs = parse_legacy_wire_records(wire_path)
    assert len(qa_pairs) == 4
    assert qa_pairs[0].role == "user"
    assert "Hello" in qa_pairs[0].content
    assert qa_pairs[1].role == "assistant"
    assert "coding" in qa_pairs[1].content
    assert qa_pairs[2].role == "user"
    assert "hello world" in qa_pairs[2].content.lower()
    assert qa_pairs[3].role == "assistant"
    assert "print" in qa_pairs[3].content


def test_parse_session_old_format():
    session_dir = FIXTURES / "old"
    session = parse_session(session_dir)
    assert session.title == "Old Format Test Session"
    assert session.message_count == 4
    assert len(session.qa_pairs) == 4


def test_parse_session_new_format():
    session_dir = FIXTURES / "new"
    session = parse_session(session_dir)
    assert session.title == "New Format Test Session"
    assert session.message_count == 4
    assert len(session.qa_pairs) == 4


def test_parse_session_legacy_format():
    session_dir = FIXTURES / "legacy"
    session = parse_session(session_dir, source="kimi-legacy")
    assert session.title == "Legacy Format Test Session"
    assert session.message_count == 4
    assert len(session.qa_pairs) == 4


def test_list_sessions(tmp_path, monkeypatch):
    sessions_root = tmp_path / "sessions"
    sessions_root.mkdir()
    (sessions_root / "wd_old").mkdir()
    (sessions_root / "wd_old" / "session_old").mkdir()
    (sessions_root / "wd_old" / "session_old" / "agents").mkdir()
    (sessions_root / "wd_old" / "session_old" / "agents" / "main").mkdir()

    state = {"title": "Listed Session", "created_at": "2026-01-01T00:00:00"}
    (sessions_root / "wd_old" / "session_old" / "state.json").write_text(
        json.dumps(state), encoding="utf-8"
    )
    (sessions_root / "wd_old" / "session_old" / "agents" / "main" / "wire.jsonl").write_text(
        json.dumps({"protocol_version": "1.0", "type": "metadata"}) + "\n"
        + json.dumps({"type": "context.append_message", "message": {"role": "user", "content": [{"type": "text", "text": "Hi"}]}}) + "\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("SESSIONS_ROOT", str(sessions_root))
    monkeypatch.setenv("LEGACY_SESSIONS_ROOT", str(tmp_path / "legacy_empty"))
    sessions = list_sessions()
    assert len(sessions) == 1
    assert sessions[0].title == "Listed Session"
    assert sessions[0].message_count == 1


def test_list_sessions_merges_sources(tmp_path, monkeypatch):
    """当新版与 legacy 两个根目录都存在时，list_sessions 应合并返回。"""
    sessions_root = tmp_path / "sessions"
    sessions_root.mkdir()
    legacy_root = tmp_path / "legacy_sessions"
    legacy_root.mkdir()

    # 新版会话
    modern_dir = sessions_root / "wd_modern" / "session_modern"
    (modern_dir / "agents" / "main").mkdir(parents=True)
    (modern_dir / "state.json").write_text(
        json.dumps({"title": "Modern Session", "created_at": "2026-01-02T00:00:00"}),
        encoding="utf-8",
    )
    (modern_dir / "agents" / "main" / "wire.jsonl").write_text(
        json.dumps({"type": "context.append_message", "message": {"role": "user", "content": [{"type": "text", "text": "Hi"}]}}) + "\n",
        encoding="utf-8",
    )

    # legacy 会话
    legacy_dir = legacy_root / "workspace_hash" / "session_legacy"
    legacy_dir.mkdir(parents=True)
    (legacy_dir / "state.json").write_text(
        json.dumps({"custom_title": "Legacy Session", "archived_at": 1778549116.0}),
        encoding="utf-8",
    )
    (legacy_dir / "wire.jsonl").write_text(
        json.dumps({"timestamp": 1778549115.0, "message": {"type": "TurnBegin", "payload": {"user_input": [{"type": "text", "text": "Hi legacy"}]}}}) + "\n"
        + json.dumps({"timestamp": 1778549116.0, "message": {"type": "TurnEnd", "payload": {}}}) + "\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("SESSIONS_ROOT", str(sessions_root))
    monkeypatch.setenv("LEGACY_SESSIONS_ROOT", str(legacy_root))

    sessions = list_sessions()
    assert len(sessions) == 2
    titles = {s.title for s in sessions}
    assert titles == {"Modern Session", "Legacy Session"}
    sources = {s.source for s in sessions}
    assert sources == {"kimi-code", "kimi-legacy"}
