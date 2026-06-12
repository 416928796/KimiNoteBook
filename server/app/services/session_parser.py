from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from app.models.session import QAPair, SessionDetail, SessionSummary


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def format_content(content: Any) -> str:
    """统一将 content 字段转换为纯文本。"""
    if isinstance(content, str):
        return content

    if isinstance(content, dict):
        if content.get("type") == "text":
            return str(content.get("text", ""))
        if content.get("type") == "think":
            return ""
        return ""

    if isinstance(content, list):
        texts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    texts.append(str(item.get("text", "")))
                elif item.get("type") == "think":
                    continue
        return "\n".join(texts)

    return ""


def parse_wire_records(wire_path: Path) -> List[QAPair]:
    """解析 wire.jsonl，返回按时间顺序的 user/assistant 消息列表。"""
    qa_pairs: List[QAPair] = []
    current_assistant_parts: List[str] = []
    current_assistant_time: datetime | None = None
    current_step: int | None = None

    with open(wire_path, "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            record_type = record.get("type")
            time = _parse_datetime(record.get("time"))

            if record_type == "context.append_message":
                # 关闭之前的 assistant 聚合
                if current_assistant_parts and current_step is not None:
                    qa_pairs.append(
                        QAPair(
                            index=len(qa_pairs),
                            role="assistant",
                            content="\n".join(current_assistant_parts),
                            created_at=current_assistant_time,
                        )
                    )
                    current_assistant_parts = []
                    current_step = None

                message = record.get("message", {})
                role = message.get("role")
                if role in ("user", "assistant"):
                    qa_pairs.append(
                        QAPair(
                            index=len(qa_pairs),
                            role=role,
                            content=format_content(message.get("content")),
                            created_at=time,
                        )
                    )

            elif record_type == "context.append_loop_event":
                event = record.get("event", {})
                event_type = event.get("type")

                if event_type == "step.begin":
                    # 关闭之前的 assistant 聚合
                    if current_assistant_parts and current_step is not None:
                        qa_pairs.append(
                            QAPair(
                                index=len(qa_pairs),
                                role="assistant",
                                content="\n".join(current_assistant_parts),
                                created_at=current_assistant_time,
                            )
                        )
                    current_assistant_parts = []
                    current_step = event.get("step")
                    current_assistant_time = time

                elif event_type == "content.part":
                    part = event.get("part", {})
                    text = format_content(part)
                    if text:
                        current_assistant_parts.append(text)

                elif event_type == "step.end":
                    if current_assistant_parts:
                        qa_pairs.append(
                            QAPair(
                                index=len(qa_pairs),
                                role="assistant",
                                content="\n".join(current_assistant_parts),
                                created_at=current_assistant_time,
                            )
                        )
                    current_assistant_parts = []
                    current_step = None

    # 文件末尾可能还有未关闭的 assistant 聚合
    if current_assistant_parts and current_step is not None:
        qa_pairs.append(
            QAPair(
                index=len(qa_pairs),
                role="assistant",
                content="\n".join(current_assistant_parts),
                created_at=current_assistant_time,
            )
        )

    return qa_pairs


def parse_session(session_dir: Path) -> SessionDetail:
    """解析单个会话目录。"""
    session_id = session_dir.name
    state_path = session_dir / "state.json"
    wire_path = session_dir / "agents" / "main" / "wire.jsonl"

    state: Dict[str, Any] = {}
    if state_path.exists():
        with open(state_path, "r", encoding="utf-8") as fp:
            state = json.load(fp)

    qa_pairs = parse_wire_records(wire_path) if wire_path.exists() else []
    created_at = _parse_datetime(state.get("created_at"))
    updated_at = _parse_datetime(state.get("updated_at"))

    return SessionDetail(
        id=session_id,
        title=state.get("title") or session_id,
        created_at=created_at,
        updated_at=updated_at,
        message_count=len(qa_pairs),
        qa_pairs=qa_pairs,
    )


def list_sessions() -> List[SessionSummary]:
    """扫描会话根目录，返回会话摘要列表。"""
    root = Path(os.environ.get("SESSIONS_ROOT", Path.home() / ".kimi-code" / "sessions"))
    if not root.exists():
        return []

    sessions: List[SessionSummary] = []
    for wd_dir in root.iterdir():
        if not wd_dir.is_dir():
            continue
        for session_dir in wd_dir.iterdir():
            if not session_dir.is_dir():
                continue
            detail = parse_session(session_dir)
            sessions.append(
                SessionSummary(
                    id=detail.id,
                    title=detail.title,
                    created_at=detail.created_at,
                    updated_at=detail.updated_at,
                    message_count=detail.message_count,
                )
            )

    sessions.sort(key=lambda s: s.created_at or datetime.min, reverse=True)
    return sessions
