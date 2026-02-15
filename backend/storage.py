import datetime
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

    async def get_workspace_config(self, workspace: str) -> dict[str, Any] | None:
        ws = str(workspace or "").strip()
        if not ws:
            return None
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "select workspace, config, updated_at from workspace_configs where workspace=$1",
                    ws,
                )
                if not row:
                    return None
                return {
                    "workspace": str(row["workspace"] or ""),
                    "config": row["config"],
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }
        st = self._read_state()
        items = st.get("workspace_configs", {})
        if not isinstance(items, dict):
            return None
        rec = items.get(ws)
        if not isinstance(rec, dict):
            return None
        return {
            "workspace": ws,
            "config": rec.get("config") if isinstance(rec.get("config"), dict) else rec.get("config"),
            "updated_at": rec.get("updated_at"),
        }

    async def upsert_workspace_config(self, workspace: str, config: dict[str, Any]) -> dict[str, Any]:
        ws = str(workspace or "").strip()
        if not ws:
            raise ValueError("workspace is required")
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "insert into workspace_configs(workspace, config) values($1, $2) "
                    "on conflict(workspace) do update set config=excluded.config, updated_at=now() "
                    "returning workspace, config, updated_at",
                    ws,
                    config,
                )
                assert row is not None
                return {
                    "workspace": str(row["workspace"] or ""),
                    "config": row["config"],
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }
        st = self._read_state()
        st.setdefault("workspace_configs", {})
        items = st["workspace_configs"] if isinstance(st.get("workspace_configs"), dict) else {}
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        items[ws] = {"config": config, "updated_at": now}
        st["workspace_configs"] = items
        self._write_state(st)
        return {"workspace": ws, "config": config, "updated_at": now}

    async def create_pipeline_script(
        self,
        *,
        title: str,
        script_text: str,
        script_version: int = 1,
        script_format: str = "aaps",
        ir: Any = None,
    ) -> dict[str, Any]:
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "insert into pipeline_scripts(title, script_text, script_version, script_format, ir) "
                    "values($1, $2, $3, $4, $5) "
                    "returning id, title, script_text, script_version, script_format, ir, created_at, updated_at",
                    title,
                    script_text,
                    int(script_version),
                    str(script_format),
                    ir,
                )
                assert row is not None
                return {
                    "id": int(row["id"]),
                    "title": str(row["title"] or ""),
                    "script_text": str(row["script_text"] or ""),
                    "script_version": int(row["script_version"] or 1),
                    "script_format": str(row["script_format"] or "aaps"),
                    "ir": row["ir"],
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }

        st = self._read_state()
        st.setdefault("scripts", [])
        items = st["scripts"] if isinstance(st.get("scripts"), list) else []
        next_id = 1
        for it in items:
            if isinstance(it, dict) and isinstance(it.get("id"), int):
                next_id = max(next_id, int(it.get("id")) + 1)
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        obj = {
            "id": next_id,
            "title": str(title or ""),
            "script_text": str(script_text or ""),
            "script_version": int(script_version),
            "script_format": str(script_format or "aaps"),
            "ir": ir,
            "created_at": now,
            "updated_at": now,
        }
        items.append(obj)
        st["scripts"] = items[-200:]
        self._write_state(st)
        return obj

    async def get_pipeline_script(self, script_id: int) -> dict[str, Any] | None:
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "select id, title, script_text, script_version, script_format, ir, created_at, updated_at "
                    "from pipeline_scripts where id=$1",
                    int(script_id),
                )
                if not row:
                    return None
                return {
                    "id": int(row["id"]),
                    "title": str(row["title"] or ""),
                    "script_text": str(row["script_text"] or ""),
                    "script_version": int(row["script_version"] or 1),
                    "script_format": str(row["script_format"] or "aaps"),
                    "ir": row["ir"],
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }

        st = self._read_state()
        items = st.get("scripts", [])
        if not isinstance(items, list):
            return None
        for it in items:
            if isinstance(it, dict) and it.get("id") == script_id:
                return it
        return None

    async def list_pipeline_scripts(self, limit: int = 50) -> list[dict[str, Any]]:
        lim = max(1, min(200, int(limit)))
        if self._pool:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(
                    "select id, title, script_version, script_format, created_at, updated_at "
                    "from pipeline_scripts order by id desc limit $1",
                    lim,
                )
                items = [
                    {
                        "id": int(r["id"]),
                        "title": str(r["title"] or ""),
                        "script_version": int(r["script_version"] or 1),
                        "script_format": str(r["script_format"] or "aaps"),
                        "created_at": r["created_at"].isoformat() if r["created_at"] else None,
                        "updated_at": r["updated_at"].isoformat() if r["updated_at"] else None,
                    }
                    for r in rows
                ]
                items.reverse()
                return items

        st = self._read_state()
        items = st.get("scripts", [])
        if not isinstance(items, list):
            return []
        # Return most-recent first, similar to DB list.
        out = items[-lim:]
        out.reverse()
        return out

    async def update_pipeline_script(
        self,
        script_id: int,
        *,
        title: str | None = None,
        script_text: str | None = None,
        script_version: int | None = None,
        script_format: str | None = None,
        ir: Any = None,
        ir_set: bool = False,
    ) -> dict[str, Any] | None:
        cur = await self.get_pipeline_script(script_id)
        if not cur:
            return None
        next_ir = ir if ir_set else cur.get("ir")
        next_title = cur.get("title") if title is None else title
        next_text = cur.get("script_text") if script_text is None else script_text
        next_ver = cur.get("script_version") if script_version is None else script_version
        next_fmt = cur.get("script_format") if script_format is None else script_format

        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "update pipeline_scripts set title=$1, script_text=$2, script_version=$3, script_format=$4, ir=$5, updated_at=now() "
                    "where id=$6 "
                    "returning id, title, script_text, script_version, script_format, ir, created_at, updated_at",
                    str(next_title or ""),
                    str(next_text or ""),
                    int(next_ver or 1),
                    str(next_fmt or "aaps"),
                    next_ir,
                    int(script_id),
                )
                if not row:
                    return None
                return {
                    "id": int(row["id"]),
                    "title": str(row["title"] or ""),
                    "script_text": str(row["script_text"] or ""),
                    "script_version": int(row["script_version"] or 1),
                    "script_format": str(row["script_format"] or "aaps"),
                    "ir": row["ir"],
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }

        st = self._read_state()
        items = st.get("scripts", [])
        if not isinstance(items, list):
            return None
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for it in items:
            if isinstance(it, dict) and it.get("id") == script_id:
                it["title"] = str(next_title or "")
                it["script_text"] = str(next_text or "")
                it["script_version"] = int(next_ver or 1)
                it["script_format"] = str(next_fmt or "aaps")
                it["ir"] = next_ir
                it["updated_at"] = now
                self._write_state(st)
                return it
        return None

    async def delete_pipeline_script(self, script_id: int) -> bool:
        if self._pool:
            async with self._pool.acquire() as conn:
                res = await conn.execute("delete from pipeline_scripts where id=$1", int(script_id))
                # res is like: "DELETE 1"
                return "DELETE 1" in str(res)

        st = self._read_state()
        items = st.get("scripts", [])
        if not isinstance(items, list):
            return False
        before = len(items)
        items = [it for it in items if not (isinstance(it, dict) and it.get("id") == script_id)]
        st["scripts"] = items
        self._write_state(st)
        return len(items) != before

    async def create_action_definition(
        self,
        *,
        title: str,
        kind: str,
        spec: Any,
        enabled: bool = True,
    ) -> dict[str, Any]:
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "insert into action_definitions(title, kind, spec, enabled) values($1, $2, $3, $4) "
                    "returning id, title, kind, spec, enabled, created_at, updated_at",
                    str(title or ""),
                    str(kind or ""),
                    spec,
                    bool(enabled),
                )
                assert row is not None
                return {
                    "id": int(row["id"]),
                    "title": str(row["title"] or ""),
                    "kind": str(row["kind"] or ""),
                    "spec": row["spec"],
                    "enabled": bool(row["enabled"]),
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }

        st = self._read_state()
        st.setdefault("actions", [])
        items = st["actions"] if isinstance(st.get("actions"), list) else []
        next_id = 1
        for it in items:
            if isinstance(it, dict) and isinstance(it.get("id"), int):
                next_id = max(next_id, int(it.get("id")) + 1)
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        obj = {
            "id": next_id,
            "title": str(title or ""),
            "kind": str(kind or ""),
            "spec": spec,
            "enabled": bool(enabled),
            "created_at": now,
            "updated_at": now,
        }
        items.append(obj)
        st["actions"] = items[-200:]
        self._write_state(st)
        return obj

    async def get_action_definition(self, action_id: int) -> dict[str, Any] | None:
        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "select id, title, kind, spec, enabled, created_at, updated_at from action_definitions where id=$1",
                    int(action_id),
                )
                if not row:
                    return None
                return {
                    "id": int(row["id"]),
                    "title": str(row["title"] or ""),
                    "kind": str(row["kind"] or ""),
                    "spec": row["spec"],
                    "enabled": bool(row["enabled"]),
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }

        st = self._read_state()
        items = st.get("actions", [])
        if not isinstance(items, list):
            return None
        for it in items:
            if isinstance(it, dict) and it.get("id") == action_id:
                return it
        return None

    async def list_action_definitions(self, limit: int = 50) -> list[dict[str, Any]]:
        lim = max(1, min(200, int(limit)))
        if self._pool:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(
                    "select id, title, kind, enabled, created_at, updated_at "
                    "from action_definitions order by id desc limit $1",
                    lim,
                )
                items = [
                    {
                        "id": int(r["id"]),
                        "title": str(r["title"] or ""),
                        "kind": str(r["kind"] or ""),
                        "enabled": bool(r["enabled"]),
                        "created_at": r["created_at"].isoformat() if r["created_at"] else None,
                        "updated_at": r["updated_at"].isoformat() if r["updated_at"] else None,
                    }
                    for r in rows
                ]
                items.reverse()
                return items

        st = self._read_state()
        items = st.get("actions", [])
        if not isinstance(items, list):
            return []
        out = items[-lim:]
        out.reverse()
        return [
            {
                "id": int(it.get("id")),
                "title": str(it.get("title") or ""),
                "kind": str(it.get("kind") or ""),
                "enabled": bool(it.get("enabled", True)),
                "created_at": it.get("created_at"),
                "updated_at": it.get("updated_at"),
            }
            for it in out
            if isinstance(it, dict) and isinstance(it.get("id"), int)
        ]

    async def update_action_definition(
        self,
        action_id: int,
        *,
        title: str | None = None,
        spec: Any = None,
        spec_set: bool = False,
        enabled: bool | None = None,
        kind: str | None = None,
    ) -> dict[str, Any] | None:
        cur = await self.get_action_definition(int(action_id))
        if not cur:
            return None
        next_title = cur.get("title") if title is None else str(title)
        next_kind = cur.get("kind") if kind is None else str(kind)
        next_spec = cur.get("spec") if not spec_set else spec
        next_enabled = cur.get("enabled") if enabled is None else bool(enabled)

        if self._pool:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "update action_definitions set title=$1, kind=$2, spec=$3, enabled=$4, updated_at=now() "
                    "where id=$5 "
                    "returning id, title, kind, spec, enabled, created_at, updated_at",
                    next_title,
                    next_kind,
                    next_spec,
                    next_enabled,
                    int(action_id),
                )
                if not row:
                    return None
                return {
                    "id": int(row["id"]),
                    "title": str(row["title"] or ""),
                    "kind": str(row["kind"] or ""),
                    "spec": row["spec"],
                    "enabled": bool(row["enabled"]),
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                    "updated_at": row["updated_at"].isoformat() if row["updated_at"] else None,
                }

        st = self._read_state()
        items = st.get("actions", [])
        if not isinstance(items, list):
            return None
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        out: dict[str, Any] | None = None
        for it in items:
            if not (isinstance(it, dict) and it.get("id") == action_id):
                continue
            it["title"] = next_title
            it["kind"] = next_kind
            it["spec"] = next_spec
            it["enabled"] = next_enabled
            it["updated_at"] = now
            out = it
            break
        if out is None:
            return None
        st["actions"] = items[-200:]
        self._write_state(st)
        return out

    async def delete_action_definition(self, action_id: int) -> bool:
        if self._pool:
            async with self._pool.acquire() as conn:
                res = await conn.execute("delete from action_definitions where id=$1", int(action_id))
                return "DELETE 1" in str(res)

        st = self._read_state()
        items = st.get("actions", [])
        if not isinstance(items, list):
            return False
        before = len(items)
        items = [it for it in items if not (isinstance(it, dict) and it.get("id") == action_id)]
        st["actions"] = items
        self._write_state(st)
        return len(items) != before

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

    async def add_outbox_message(self, role: str, content: str) -> None:
        if self._pool:
            async with self._pool.acquire() as conn:
                await conn.execute(
                    "insert into outbox_messages(role, content) values($1, $2)",
                    role,
                    content,
                )
            return
        st = self._read_state()
        st.setdefault("outbox", [])
        st["outbox"].append({"role": role, "content": content})
        st["outbox"] = st["outbox"][-200:]
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

    async def list_outbox_messages(self, limit: int = 50) -> list[dict[str, Any]]:
        lim = max(1, min(500, int(limit)))
        if self._pool:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(
                    "select id, role, content, created_at from outbox_messages order by id desc limit $1",
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
        outbox = st.get("outbox", [])
        if not isinstance(outbox, list):
            return []
        return outbox[-lim:]

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
