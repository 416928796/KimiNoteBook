import os
from pathlib import Path


def get_sessions_root() -> Path:
    return Path(os.environ.get("SESSIONS_ROOT", Path.home() / ".kimi-code" / "sessions"))


def get_legacy_sessions_root() -> Path:
    return Path(os.environ.get("LEGACY_SESSIONS_ROOT", Path.home() / ".kimi" / "sessions"))
