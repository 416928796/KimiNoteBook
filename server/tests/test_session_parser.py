import json
from pathlib import Path

import pytest

from app.services.session_parser import parse_session, list_sessions, parse_wire_records, format_content

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
    sessions = list_sessions()
    assert len(sessions) == 1
    assert sessions[0].title == "Listed Session"
    assert sessions[0].message_count == 1
