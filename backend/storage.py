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
            self._pool = await asyncpg.create_pool(dsn=self._database_url, min_size=1, max_size=5, timeout=2.0)
        except Exception as e:
            self._pool = None
            raise RuntimeError(
                f"failed to create Postgres pool (DATABASE_URL is set): {type(e).__name__}: {e}"
            ) from e

    def require_pool(self) -> asyncpg.Pool:
        if not self._pool:
            raise RuntimeError("postgres pool is not initialized")
        return self._pool

    @property
    def pool(self) -> asyncpg.Pool:
        return self.require_pool()

    async def execute(self, sql: str, *args: Any) -> str:
        async with self.require_pool().acquire() as conn:
            return await conn.execute(sql, *args)

    async def fetch(self, sql: str, *args: Any) -> list[asyncpg.Record]:
        async with self.require_pool().acquire() as conn:
            return await conn.fetch(sql, *args)

    async def fetchrow(self, sql: str, *args: Any) -> asyncpg.Record | None:
        async with self.require_pool().acquire() as conn:
            return await conn.fetchrow(sql, *args)

    async def fetchval(self, sql: str, *args: Any) -> Any:
        async with self.require_pool().acquire() as conn:
            return await conn.fetchval(sql, *args)

    async def get_server_time_iso(self) -> str:
        async with self.require_pool().acquire() as conn:
            v = await conn.fetchval("select now()", timeout=2.0)
        try:
            return v.isoformat()  # type: ignore[no-any-return]
        except Exception:
            return str(v)

    async def stop(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def ensure_schema(self, schema_sql: str) -> None:
        if not self._pool:
            return
        await self.execute(schema_sql)

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

    async def add_inbox_message(self, role: str, content: str) -> None:
        if self._pool:
            async with self._pool.acquire() as conn:
                await conn.execute(
                    "insert into inbox_messages(role, content) values($1, $2)",
                    role,
                    content,
                )
            return
        st = self._read_state()
        st.setdefault("inbox", [])
        st["inbox"].append({"role": role, "content": content})
        st["inbox"] = st["inbox"][-200:]
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

    async def list_inbox_messages(self, limit: int = 50) -> list[dict[str, Any]]:
        lim = max(1, min(500, int(limit)))
        if self._pool:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(
                    "select id, role, content, created_at from inbox_messages order by id desc limit $1",
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
        inbox = st.get("inbox", [])
        if not isinstance(inbox, list):
            return []
        return inbox[-lim:]

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

    async def get_pipeline_state(self) -> dict[str, Any]:
        def iso(v: Any) -> Any:
            if v is None:
                return None
            try:
                return v.isoformat()
            except Exception:
                return str(v)

        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "select state, pid, run_id, started_at, paused_at, resumed_at, stopped_at, updated_at "
                    "from pipeline_state where id=1"
                )
                if not row:
                    return {"state": "stopped"}
                return {
                    "state": str(row["state"]),
                    "pid": row["pid"],
                    "run_id": row["run_id"],
                    "started_at": iso(row["started_at"]),
                    "paused_at": iso(row["paused_at"]),
                    "resumed_at": iso(row["resumed_at"]),
                    "stopped_at": iso(row["stopped_at"]),
                    "updated_at": iso(row["updated_at"]),
                }

        st = self._read_state()
        ps = st.get("pipeline_state") if isinstance(st.get("pipeline_state"), dict) else {}
        return ps if ps else {"state": "stopped"}

    async def set_pipeline_state(
        self,
        *,
        state: str,
        pid: Optional[int],
        run_id: Optional[int],
        ts_kind: str,
    ) -> None:
        """Update the singleton pipeline_state row (id=1).

        ts_kind: start|pause|resume|stop
        """
        if not self._pool:
            st = self._read_state()
            st["pipeline_state"] = {
                "state": state,
                "pid": pid,
                "run_id": run_id,
                "ts_kind": ts_kind,
            }
            self._write_state(st)
            return

        async with self._pool.acquire() as conn:
            if ts_kind == "start":
                await conn.execute(
                    "insert into pipeline_state(id, state, pid, run_id, started_at, paused_at, resumed_at, stopped_at, updated_at) "
                    "values (1, $1, $2, $3, now(), null, null, null, now()) "
                    "on conflict (id) do update set "
                    "state=$1, pid=$2, run_id=$3, started_at=now(), paused_at=null, resumed_at=null, stopped_at=null, updated_at=now()",
                    state,
                    pid,
                    run_id,
                )
            elif ts_kind == "pause":
                await conn.execute(
                    "insert into pipeline_state(id, state, pid, run_id, paused_at, updated_at) "
                    "values (1, $1, $2, $3, now(), now()) "
                    "on conflict (id) do update set "
                    "state=$1, pid=$2, run_id=$3, paused_at=now(), updated_at=now()",
                    state,
                    pid,
                    run_id,
                )
            elif ts_kind == "resume":
                await conn.execute(
                    "insert into pipeline_state(id, state, pid, run_id, resumed_at, stopped_at, updated_at) "
                    "values (1, $1, $2, $3, now(), null, now()) "
                    "on conflict (id) do update set "
                    "state=$1, pid=$2, run_id=$3, resumed_at=now(), stopped_at=null, updated_at=now()",
                    state,
                    pid,
                    run_id,
                )
            elif ts_kind == "stop":
                await conn.execute(
                    "insert into pipeline_state(id, state, pid, run_id, stopped_at, updated_at) "
                    "values (1, $1, $2, $3, now(), now()) "
                    "on conflict (id) do update set "
                    "state=$1, pid=$2, run_id=$3, stopped_at=now(), updated_at=now()",
                    state,
                    pid,
                    run_id,
                )
            else:
                raise ValueError("invalid ts_kind")


def safe_env(key: str, default: str = "") -> str:
    v = os.getenv(key)
    if v is None:
        return default
    return str(v)
