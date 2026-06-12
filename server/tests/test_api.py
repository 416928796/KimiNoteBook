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
                    "content": [{"type": "text", "text": "Hi there!"}],
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("SESSIONS_ROOT", str(sessions_root))
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
