import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    sessions_root = tmp_path / "sessions"
    sessions_root.mkdir()

    # 创建一个测试会话
    wd_dir = sessions_root / "wd_test"
    session_dir = wd_dir / "session_test_001"
    agents_dir = session_dir / "agents" / "main"
    agents_dir.mkdir(parents=True)

    state = {"title": "API Test Session", "created_at": "2026-01-01T00:00:00"}
    import json

    (session_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
    (agents_dir / "wire.jsonl").write_text(
        json.dumps({"protocol_version": "1.0", "type": "metadata"}) + "\n"
        + json.dumps(
            {
                "type": "context.append_message",
                "message": {"role": "user", "content": [{"type": "text", "text": "Hello"}]},
            }
        )
        + "\n"
        + json.dumps(
            {
                "type": "context.append_message",
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": "# Section\n\nHi there!"}],
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("SESSIONS_ROOT", str(sessions_root))
    monkeypatch.setenv("LEGACY_SESSIONS_ROOT", str(tmp_path / "legacy_empty"))
    return TestClient(app)


@pytest.fixture
def client_with_legacy(tmp_path, monkeypatch):
    sessions_root = tmp_path / "sessions"
    sessions_root.mkdir()
    legacy_root = tmp_path / "legacy_sessions"
    legacy_root.mkdir()

    # 新版会话
    wd_dir = sessions_root / "wd_test"
    session_dir = wd_dir / "session_test_001"
    agents_dir = session_dir / "agents" / "main"
    agents_dir.mkdir(parents=True)

    import json

    (session_dir / "state.json").write_text(
        json.dumps({"title": "API Test Session", "created_at": "2026-01-01T00:00:00"}),
        encoding="utf-8",
    )
    (agents_dir / "wire.jsonl").write_text(
        json.dumps({"type": "context.append_message", "message": {"role": "user", "content": [{"type": "text", "text": "Hello"}]}})
        + "\n",
        encoding="utf-8",
    )

    # legacy 会话
    legacy_wd = legacy_root / "workspace_hash"
    legacy_session_dir = legacy_wd / "session_legacy_001"
    legacy_session_dir.mkdir(parents=True)
    (legacy_session_dir / "state.json").write_text(
        json.dumps({"custom_title": "Legacy API Test Session", "archived_at": 1778549116.0}),
        encoding="utf-8",
    )
    (legacy_session_dir / "wire.jsonl").write_text(
        json.dumps(
            {
                "timestamp": 1778549115.0,
                "message": {
                    "type": "TurnBegin",
                    "payload": {"user_input": [{"type": "text", "text": "Hello legacy"}]},
                },
            }
        )
        + "\n"
        + json.dumps({"timestamp": 1778549115.5, "message": {"type": "StepBegin", "payload": {"n": 1}}})
        + "\n"
        + json.dumps(
            {
                "timestamp": 1778549116.0,
                "message": {"type": "ContentPart", "payload": {"type": "text", "text": "Hi from legacy!"}},
            }
        )
        + "\n"
        + json.dumps({"timestamp": 1778549117.0, "message": {"type": "TurnEnd", "payload": {}}})
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("SESSIONS_ROOT", str(sessions_root))
    monkeypatch.setenv("LEGACY_SESSIONS_ROOT", str(legacy_root))
    return TestClient(app)


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_sessions(client):
    response = client.get("/api/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "API Test Session"
    assert data[0]["message_count"] == 2
    assert data[0]["source"] == "kimi-code"


def test_get_session(client):
    response = client.get("/api/sessions/session_test_001")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "API Test Session"
    assert len(data["qa_pairs"]) == 2
    assert data["qa_pairs"][0]["role"] == "user"
    assert data["qa_pairs"][1]["role"] == "assistant"


def test_get_session_not_found(client):
    response = client.get("/api/sessions/nonexistent")
    assert response.status_code == 404


def test_export_session(client):
    response = client.post(
        "/api/sessions/session_test_001/export",
        json={"selected_indices": [0, 1]},
    )
    assert response.status_code == 200
    body = response.text
    assert "API Test Session" in body
    assert "Hello" in body
    assert "Hi there!" in body
    assert response.headers["content-type"].startswith("text/markdown")
    # Issue #3: 用户/模型分节为一级标题，内容中的标题降级一级
    assert "# " in body
    assert "\n## Section\n" in body
    model_part = body.split("# ", 2)[2] if body.count("# ") >= 2 else body
    assert "\n# Section\n" not in model_part


def test_list_sessions_includes_legacy(client_with_legacy):
    response = client_with_legacy.get("/api/sessions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    by_id = {s["id"]: s for s in data}
    assert "session_test_001" in by_id
    assert "session_legacy_001" in by_id
    assert by_id["session_legacy_001"]["source"] == "kimi-legacy"
    assert by_id["session_legacy_001"]["title"] == "Legacy API Test Session"


def test_get_legacy_session(client_with_legacy):
    response = client_with_legacy.get("/api/sessions/session_legacy_001")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Legacy API Test Session"
    assert data["source"] == "kimi-legacy"
    assert len(data["qa_pairs"]) == 2
    assert data["qa_pairs"][0]["role"] == "user"
    assert "legacy" in data["qa_pairs"][0]["content"].lower()
    assert data["qa_pairs"][1]["role"] == "assistant"
    assert "Hi from legacy" in data["qa_pairs"][1]["content"]


def test_export_legacy_session(client_with_legacy):
    response = client_with_legacy.post(
        "/api/sessions/session_legacy_001/export",
        json={"selected_indices": [0, 1]},
    )
    assert response.status_code == 200
    body = response.text
    assert "Legacy API Test Session" in body
    assert "Hello legacy" in body
    assert "Hi from legacy" in body
    assert "# " in body
