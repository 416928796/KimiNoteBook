from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from app.config import get_sessions_root
from app.models.session import ExportRequest, SessionDetail, SessionSummary
from app.services.session_parser import list_sessions, parse_session


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def _demote_headings(content: str) -> str:
    """将内容中的 Markdown 标题统一降级一级，代码块内不受影响。"""
    lines = content.split("\n")
    in_code_block = False
    result: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue
        if in_code_block:
            result.append(line)
            continue
        match = _HEADING_RE.match(line)
        if match:
            result.append(f"#{match.group(1)} {match.group(2)}")
        else:
            result.append(line)
    return "\n".join(result)

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _find_session_dir(session_id: str) -> Path | None:
    root = get_sessions_root()
    for wd_dir in root.iterdir():
        if not wd_dir.is_dir():
            continue
        for session_dir in wd_dir.iterdir():
            if session_dir.name == session_id:
                return session_dir
    return None


@router.get("", response_model=list[SessionSummary])
def get_sessions() -> list[SessionSummary]:
    return list_sessions()


@router.get("/{session_id}", response_model=SessionDetail)
def get_session(session_id: str) -> SessionDetail:
    session_dir = _find_session_dir(session_id)
    if not session_dir:
        raise HTTPException(status_code=404, detail="Session not found")
    return parse_session(session_dir)


@router.post("/{session_id}/export")
def export_session(session_id: str, request: ExportRequest) -> PlainTextResponse:
    session_dir = _find_session_dir(session_id)
    if not session_dir:
        raise HTTPException(status_code=404, detail="Session not found")

    session = parse_session(session_dir)
    selected = sorted(request.selected_indices)
    lines: list[str] = []
    lines.append(f"# {session.title}")
    lines.append("")
    lines.append(f"_导出时间：{datetime.now().isoformat()}_")
    lines.append("")

    for idx in selected:
        if idx < 0 or idx >= len(session.qa_pairs):
            continue
        pair = session.qa_pairs[idx]
        if pair.role == "user":
            lines.append("# 用户")
        elif pair.role == "assistant":
            lines.append("# 模型")
        else:
            lines.append(f"# {pair.role}")
        lines.append("")
        lines.append(_demote_headings(pair.content))
        lines.append("")

    content = "\n".join(lines)
    filename = f"{session_id}.md"
    return PlainTextResponse(
        content,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
