import datetime
import json
import re
from pathlib import Path
from typing import Any

from .codex_api import atomic_write_json, now_iso


def safe_session_id(raw: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_.-]+", "-", str(raw or "").strip()).strip(".-")
    return s[:140]


def normalize_mode(raw: Any) -> str:
    mode = str(raw or "notes").strip().lower().replace("-", "_")
    if mode in {"notes", "design", "loop", "autopilot_loop", "setup", "autopilot_setup"}:
        return {"loop": "autopilot_loop", "setup": "autopilot_setup"}.get(mode, mode)
    return "notes"


class StudioChatStore:
    def __init__(self, *, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def new_session_id(self, mode: str) -> str:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        return f"{ts}-{normalize_mode(mode)}"

    def session_dir(self, session_id: str) -> Path:
        sid = safe_session_id(session_id)
        if not sid:
            raise ValueError("session_id is required")
        return self.root / sid

    def message_path(self, session_id: str) -> Path:
        return self.session_dir(session_id) / "messages.jsonl"

    def create_session(self, *, mode: str = "notes", title: str = "") -> dict[str, Any]:
        m = normalize_mode(mode)
        sid = self.new_session_id(m)
        sdir = self.session_dir(sid)
        sdir.mkdir(parents=True, exist_ok=True)
        session = {
            "id": sid,
            "mode": m,
            "title": title or m.replace("_", " ").title(),
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        atomic_write_json(sdir / "session.json", session)
        self.message_path(sid).touch(exist_ok=True)
        return session

    def get_or_create_session(self, *, session_id: str = "", mode: str = "notes") -> dict[str, Any]:
        sid = safe_session_id(session_id)
        if sid:
            path = self.session_dir(sid) / "session.json"
            if path.exists():
                try:
                    data = json.loads(path.read_text("utf-8"))
                    if isinstance(data, dict):
                        return data
                except Exception:
                    pass
        return self.create_session(mode=mode)

    def append_message(self, session_id: str, *, role: str, content: str, meta: dict[str, Any] | None = None) -> dict[str, Any]:
        sdir = self.session_dir(session_id)
        sdir.mkdir(parents=True, exist_ok=True)
        msg = {
            "id": f"m{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}",
            "role": role if role in {"user", "assistant", "system", "agent"} else "system",
            "content": str(content or ""),
            "created_at": now_iso(),
            "meta": meta or {},
        }
        with self.message_path(session_id).open("a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False, sort_keys=True) + "\n")
        path = sdir / "session.json"
        session = {}
        if path.exists():
            try:
                session = json.loads(path.read_text("utf-8"))
            except Exception:
                session = {}
        if isinstance(session, dict):
            session["updated_at"] = now_iso()
            atomic_write_json(path, session)
        return msg

    def list_messages(self, session_id: str, *, limit: int = 80) -> list[dict[str, Any]]:
        path = self.message_path(session_id)
        if not path.exists():
            return []
        msgs: list[dict[str, Any]] = []
        for line in path.read_text("utf-8", errors="replace").splitlines():
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict):
                msgs.append(obj)
        return msgs[-max(1, min(limit, 300)) :]

    def transcript(self, session_id: str, *, limit: int = 24) -> str:
        lines = []
        for msg in self.list_messages(session_id, limit=limit):
            role = str(msg.get("role") or "system")
            content = str(msg.get("content") or "")
            lines.append(f"{role}: {content}")
        return "\n".join(lines)
