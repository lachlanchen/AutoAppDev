import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import asyncpg


@dataclass
class PipelineStatus:
    running: bool
    pid: Optional[int] = None
    run_id: Optional[int] = None
    status: str = "idle"


class Storage:
    """
    Storage with Postgres-first behavior.
    Falls back to a local JSON file if Postgres is unavailable.
    """

    def __init__(self, database_url: str, runtime_dir: Path):
        self._database_url = database_url
        self._runtime_dir = runtime_dir
        self._pool: Optional[asyncpg.Pool] = None
        self._state_path = runtime_dir / "state.json"

    async def start(self) -> None:
        self._runtime_dir.mkdir(parents=True, exist_ok=True)
        if not self._database_url:
            return
        try:
            self._pool = await asyncpg.create_pool(dsn=self._database_url, min_size=1, max_size=5)
        except Exception:
            self._pool = None

    async def stop(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def ensure_schema(self, schema_sql: str) -> None:
        if not self._pool:
            return
        async with self._pool.acquire() as conn:
            await conn.execute(schema_sql)

    def _read_state(self) -> dict[str, Any]:
        if not self._state_path.exists():
            return {}
        try:
            return json.loads(self._state_path.read_text("utf-8"))
        except Exception:
            return {}

    def _write_state(self, obj: dict[str, Any]) -> None:
        tmp = self._state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), "utf-8")
        tmp.replace(self._state_path)

    async def get_config(self) -> dict[str, Any]:
        if self._pool:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch("select key, value from app_config")
                return {r["key"]: r["value"] for r in rows}
        st = self._read_state()
        return st.get("config", {}) if isinstance(st.get("config", {}), dict) else {}

    async def set_config(self, key: str, value: Any) -> None:
        if self._pool:
            async with self._pool.acquire() as conn:
                await conn.execute(
                    "insert into app_config(key, value) values($1, $2) "
                    "on conflict(key) do update set value=excluded.value, updated_at=now()",
                    key,
                    value,
                )
            return
        st = self._read_state()
        st.setdefault("config", {})
        st["config"][key] = value
        self._write_state(st)

    async def add_chat_message(self, role: str, content: str) -> None:
        if self._pool:
            async with self._pool.acquire() as conn:
                await conn.execute(
                    "insert into chat_messages(role, content) values($1, $2)",
                    role,
                    content,
                )
            return
        st = self._read_state()
        st.setdefault("chat", [])
        st["chat"].append({"role": role, "content": content})
        st["chat"] = st["chat"][-200:]
        self._write_state(st)

    async def list_chat_messages(self, limit: int = 50) -> list[dict[str, Any]]:
        lim = max(1, min(500, int(limit)))
        if self._pool:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(
                    "select id, role, content, created_at from chat_messages order by id desc limit $1",
                    lim,
                )
                items = [
                    {
                        "id": int(r["id"]),
                        "role": r["role"],
                        "content": r["content"],
                        "created_at": r["created_at"].isoformat(),
                    }
                    for r in rows
                ]
                items.reverse()
                return items
        st = self._read_state()
        chat = st.get("chat", [])
        if not isinstance(chat, list):
            return []
        return chat[-lim:]

    async def create_run(self, script: str, cwd: str, args: list[str], pid: Optional[int]) -> int:
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "insert into pipeline_runs(status, pid, script, cwd, args) values($1, $2, $3, $4, $5) returning id",
                    "running",
                    pid,
                    script,
                    cwd,
                    args,
                )
                return int(row["id"])
        st = self._read_state()
        st["run"] = {"status": "running", "pid": pid, "script": script, "cwd": cwd, "args": args, "id": 1}
        self._write_state(st)
        return 1

    async def set_run_status(self, run_id: int, status: str, pid: Optional[int] = None) -> None:
        if self._pool:
            async with self._pool.acquire() as conn:
                if status in ("stopped", "failed", "completed"):
                    await conn.execute(
                        "update pipeline_runs set status=$1, pid=$2, stopped_at=now() where id=$3",
                        status,
                        pid,
                        run_id,
                    )
                else:
                    await conn.execute("update pipeline_runs set status=$1, pid=$2 where id=$3", status, pid, run_id)
            return
        st = self._read_state()
        run = st.get("run") if isinstance(st.get("run"), dict) else {}
        if run.get("id") == run_id:
            run["status"] = status
            run["pid"] = pid
            st["run"] = run
            self._write_state(st)

    async def get_latest_status(self) -> PipelineStatus:
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "select id, status, pid from pipeline_runs order by id desc limit 1"
                )
                if not row:
                    return PipelineStatus(running=False, status="idle")
                st = str(row["status"] or "idle")
                pid = row["pid"]
                return PipelineStatus(running=(st == "running"), pid=pid, run_id=int(row["id"]), status=st)
        st = self._read_state()
        run = st.get("run") if isinstance(st.get("run"), dict) else {}
        status = str(run.get("status", "idle"))
        pid = run.get("pid")
        return PipelineStatus(running=(status == "running"), pid=pid, run_id=run.get("id"), status=status)


def safe_env(key: str, default: str = "") -> str:
    v = os.getenv(key)
    if v is None:
        return default
    return str(v)

