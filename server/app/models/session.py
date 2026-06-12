from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class QAPair(BaseModel):
    index: int
    role: str
    content: str
    created_at: datetime | None = None


class SessionSummary(BaseModel):
    id: str
    title: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    message_count: int = 0


class SessionDetail(SessionSummary):
    qa_pairs: List[QAPair] = []


class ExportRequest(BaseModel):
    selected_indices: List[int]
