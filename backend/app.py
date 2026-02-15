import asyncio
from collections import deque
import datetime
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import tornado.ioloop
import tornado.web

from .storage import Storage, safe_env
from .pipeline_parser import ParseError, parse_aaps_v1
from .pipeline_shell_import import ShellImportError, import_shell_annotated_to_ir


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR: Path | None = None
LOG_DIR: Path | None = None
STARTED_AT_ISO = datetime.datetime.now(datetime.timezone.utc).isoformat()
BUILD_ID = STARTED_AT_ISO


def _write_inbox_message(runtime_dir: Path, content: str) -> None:
    inbox = runtime_dir / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    # File-based queue for pipeline scripts: the runner can consume these messages.
    ts = int(asyncio.get_event_loop().time() * 1000)
    p = inbox / f"{ts}_user.md"
    p.write_text(content, "utf-8")


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self) -> None:
        # Dev-friendly CORS: PWA is typically served on a different localhost port.
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type, authorization")
        self.set_header("Access-Control-Allow-Methods", "GET,POST,PUT,PATCH,DELETE,OPTIONS")

    def options(self, *_args: Any, **_kwargs: Any) -> None:
        self.set_status(204)
        self.finish()

    def write_json(self, obj: Any, status: int = 200) -> None:
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.set_status(status)
        self.finish(json.dumps(obj, ensure_ascii=False))


class LogBuffer:
    def __init__(self, max_entries: int = 2000):
        self._max_entries = max(100, int(max_entries))
        self._items: deque[dict[str, Any]] = deque(maxlen=self._max_entries)
        self._next_id = 1

    def append(self, *, source: str, line: str) -> int:
        lid = self._next_id
        self._next_id += 1
        self._items.append(
            {
                "id": lid,
                "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "source": source,
                "line": line,
            }
        )
        return lid

    def since(self, *, since_id: int, limit: int, source: str | None = None) -> list[dict[str, Any]]:
        lim = max(1, min(2000, int(limit)))
        out: list[dict[str, Any]] = []
        for it in self._items:
            if int(it.get("id", 0)) <= since_id:
                continue
            if source and it.get("source") != source:
                continue
            out.append(it)
            if len(out) >= lim:
                break
        return out

    def latest_id(self, *, source: str | None = None) -> int:
        last = 0
        for it in self._items:
            if source and it.get("source") != source:
                continue
            try:
                last = max(last, int(it.get("id", 0)))
            except Exception:
                pass
        return last


class FileLogTailer:
    def __init__(self, *, source: str, path: Path, buf: LogBuffer):
        self.source = source
        self.path = path
        self.buf = buf
        self._offset = 0
        self._partial = ""

    def poll(self) -> None:
        if not self.path.exists():
            return
        try:
            size = self.path.stat().st_size
        except Exception:
            return
        if size < self._offset:
            # Log rotated/truncated.
            self._offset = 0
            self._partial = ""
        try:
            with self.path.open("rb") as f:
                f.seek(self._offset)
                data = f.read()
                self._offset = f.tell()
        except Exception:
            return
        if not data:
            return
        text = data.decode("utf-8", errors="replace")
        if self._partial:
            text = self._partial + text
            self._partial = ""
        lines = text.splitlines(keepends=True)
        for ln in lines:
            if ln.endswith("\n") or ln.endswith("\r\n"):
                self.buf.append(source=self.source, line=ln.rstrip("\r\n"))
            else:
                # Partial final line; keep for next poll.
                self._partial = ln


class HealthHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        db: dict[str, Any]
        try:
            t = await self.storage.get_server_time_iso()
            db = {"ok": True, "time": t}
        except Exception as e:
            db = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        self.write_json({"ok": True, "service": "autoappdev-backend", "db": db})


class VersionHandler(BaseHandler):
    async def get(self) -> None:
        version = safe_env("AUTOAPPDEV_VERSION", "dev")
        self.write_json(
            {
                "ok": True,
                "app": "autoappdev",
                "service": "autoappdev-backend",
                "version": version,
                "build": BUILD_ID,
                "started_at": STARTED_AT_ISO,
            }
        )


class ConfigHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        cfg = await self.storage.get_config()
        self.write_json({"config": cfg})

    async def post(self) -> None:
        body = json.loads(self.request.body or b"{}")
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return
        for k, v in body.items():
            await self.storage.set_config(str(k), v)
        self.write_json({"ok": True})


class PlanHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        cfg = await self.storage.get_config()
        self.write_json({"plan": cfg.get("pipeline_plan")})

    async def post(self) -> None:
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return
        if body.get("kind") != "autoappdev_plan":
            self.write_json({"error": "invalid_kind"}, status=400)
            return
        if body.get("version") != 1:
            self.write_json({"error": "invalid_version"}, status=400)
            return
        steps = body.get("steps")
        if not isinstance(steps, list):
            self.write_json({"error": "steps_must_be_list"}, status=400)
            return
        for i, st in enumerate(steps):
            if not isinstance(st, dict):
                self.write_json({"error": "invalid_step", "index": i}, status=400)
                return
            if not isinstance(st.get("id"), int):
                self.write_json({"error": "invalid_step_id", "index": i}, status=400)
                return
            block = st.get("block")
            if not isinstance(block, str) or not block.strip():
                self.write_json({"error": "invalid_step_block", "index": i}, status=400)
                return
        await self.storage.set_config("pipeline_plan", body)
        self.write_json({"ok": True})


class ScriptsHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        limit = int(self.get_query_argument("limit", "50"))
        items = await self.storage.list_pipeline_scripts(limit=limit)
        self.write_json({"scripts": items})

    async def post(self) -> None:
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return
        title = str(body.get("title") or "").strip()
        script_text = str(body.get("script_text") or "")
        if not script_text.strip():
            self.write_json({"error": "empty_script"}, status=400)
            return
        if len(script_text) > 200_000:
            self.write_json({"error": "script_too_large"}, status=400)
            return
        script_version = body.get("script_version", 1)
        if not isinstance(script_version, int):
            self.write_json({"error": "invalid_script_version"}, status=400)
            return
        script_format = str(body.get("script_format") or "aaps")
        ir = body.get("ir")
        if ir is not None and not isinstance(ir, (dict, list)):
            self.write_json({"error": "invalid_ir"}, status=400)
            return
        script = await self.storage.create_pipeline_script(
            title=title,
            script_text=script_text,
            script_version=script_version,
            script_format=script_format,
            ir=ir,
        )
        self.write_json({"ok": True, "script": script})


class ScriptHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self, script_id: str) -> None:
        try:
            sid = int(script_id)
        except Exception:
            self.write_json({"error": "invalid_id"}, status=400)
            return
        script = await self.storage.get_pipeline_script(sid)
        if not script:
            self.write_json({"error": "not_found"}, status=404)
            return
        self.write_json({"script": script})

    async def put(self, script_id: str) -> None:
        try:
            sid = int(script_id)
        except Exception:
            self.write_json({"error": "invalid_id"}, status=400)
            return
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return

        fields = {"title", "script_text", "script_version", "script_format", "ir"}
        if not any(k in body for k in fields):
            self.write_json({"error": "no_fields"}, status=400)
            return

        title = body.get("title") if "title" in body else None
        if title is not None and not isinstance(title, str):
            self.write_json({"error": "invalid_title"}, status=400)
            return

        script_text = body.get("script_text") if "script_text" in body else None
        if script_text is not None and not isinstance(script_text, str):
            self.write_json({"error": "invalid_script_text"}, status=400)
            return
        if isinstance(script_text, str) and script_text and len(script_text) > 200_000:
            self.write_json({"error": "script_too_large"}, status=400)
            return

        script_version = body.get("script_version") if "script_version" in body else None
        if script_version is not None and not isinstance(script_version, int):
            self.write_json({"error": "invalid_script_version"}, status=400)
            return

        script_format = body.get("script_format") if "script_format" in body else None
        if script_format is not None and not isinstance(script_format, str):
            self.write_json({"error": "invalid_script_format"}, status=400)
            return

        ir_set = "ir" in body
        ir = body.get("ir")
        if ir_set and ir is not None and not isinstance(ir, (dict, list)):
            self.write_json({"error": "invalid_ir"}, status=400)
            return

        script = await self.storage.update_pipeline_script(
            sid,
            title=(title.strip() if isinstance(title, str) else None),
            script_text=script_text,
            script_version=script_version,
            script_format=script_format,
            ir=ir,
            ir_set=ir_set,
        )
        if not script:
            self.write_json({"error": "not_found"}, status=404)
            return
        self.write_json({"ok": True, "script": script})

    async def delete(self, script_id: str) -> None:
        try:
            sid = int(script_id)
        except Exception:
            self.write_json({"error": "invalid_id"}, status=400)
            return
        ok = await self.storage.delete_pipeline_script(sid)
        if not ok:
            self.write_json({"error": "not_found"}, status=404)
            return
        self.write_json({"ok": True})


class ScriptsParseHandler(BaseHandler):
    async def post(self) -> None:
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"ok": False, "error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"ok": False, "error": "invalid_body"}, status=400)
            return
        script_text = body.get("script_text")
        if not isinstance(script_text, str):
            self.write_json({"ok": False, "error": "invalid_script_text"}, status=400)
            return
        if len(script_text) > 200_000:
            self.write_json({"ok": False, "error": "script_too_large"}, status=400)
            return
        try:
            ir = parse_aaps_v1(script_text)
        except ParseError as e:
            self.write_json(e.to_dict(), status=400)
            return
        self.write_json({"ok": True, "ir": ir})


class ScriptsImportShellHandler(BaseHandler):
    async def post(self) -> None:
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"ok": False, "error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"ok": False, "error": "invalid_body"}, status=400)
            return
        shell_text = body.get("shell_text")
        if not isinstance(shell_text, str):
            self.write_json({"ok": False, "error": "invalid_shell_text"}, status=400)
            return
        if len(shell_text) > 200_000:
            self.write_json({"ok": False, "error": "shell_too_large"}, status=400)
            return
        try:
            res = import_shell_annotated_to_ir(shell_text)
        except ShellImportError as e:
            self.write_json(e.to_dict(), status=400)
            return
        self.write_json(
            {
                "ok": True,
                "script_format": "aaps",
                "script_text": res.get("aaps_text") or "",
                "ir": res.get("ir") or {},
                "warnings": res.get("warnings") or [],
            }
        )


class ChatHandler(BaseHandler):
    def initialize(self, storage: Storage, runtime_dir: Path) -> None:
        self.storage = storage
        self.runtime_dir = runtime_dir

    async def get(self) -> None:
        limit = int(self.get_query_argument("limit", "50"))
        items = await self.storage.list_chat_messages(limit=limit)
        self.write_json({"messages": items})

    async def post(self) -> None:
        body = json.loads(self.request.body or b"{}")
        content = str(body.get("content") or "").strip()
        if not content:
            self.write_json({"error": "empty"}, status=400)
            return
        await self.storage.add_chat_message("user", content)
        _write_inbox_message(self.runtime_dir, content)
        self.write_json({"ok": True})


class InboxHandler(BaseHandler):
    def initialize(self, storage: Storage, runtime_dir: Path) -> None:
        self.storage = storage
        self.runtime_dir = runtime_dir

    async def get(self) -> None:
        limit = int(self.get_query_argument("limit", "50"))
        items = await self.storage.list_inbox_messages(limit=limit)
        self.write_json({"messages": items})

    async def post(self) -> None:
        body = json.loads(self.request.body or b"{}")
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return
        content = str(body.get("content") or "").strip()
        if not content:
            self.write_json({"error": "empty"}, status=400)
            return
        if len(content) > 10_000:
            self.write_json({"error": "too_long"}, status=400)
            return
        await self.storage.add_inbox_message("user", content)
        _write_inbox_message(self.runtime_dir, content)
        self.write_json({"ok": True})


class PipelineStatusHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        st = await self.storage.get_latest_status()
        self.write_json({"status": {"running": st.running, "pid": st.pid, "run_id": st.run_id, "state": st.status}})


class PipelineStateHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        ps = await self.storage.get_pipeline_state()
        self.write_json({"pipeline": ps})


class PipelineControl:
    def __init__(self, storage: Storage, runtime_dir: Path, log_dir: Path):
        self.storage = storage
        self.proc: subprocess.Popen | None = None
        self.run_id: int | None = None
        self.log_path = log_dir / "pipeline.log"
        self.pause_flag = runtime_dir / "PAUSE"

    async def refresh_from_storage(self) -> None:
        st = await self.storage.get_latest_status()
        if st.running and st.pid and not self.proc:
            # Server restarted while pipeline is running. We do not reattach to process.
            pass

    def _spawn(self, script: str, cwd: str, args: list[str]) -> subprocess.Popen:
        out = self.log_path.open("ab", buffering=0)
        try:
            cmd = ["/usr/bin/env", "bash", script, *args]
            # Start in its own process group for reliable stop.
            return subprocess.Popen(
                cmd,
                cwd=cwd,
                stdout=out,
                stderr=subprocess.STDOUT,
                preexec_fn=os.setsid,
                env=os.environ.copy(),
            )
        finally:
            # Close parent handle; child keeps the fd.
            try:
                out.close()
            except Exception:
                pass

    async def start(self, script: str, cwd: str, args: list[str]) -> dict[str, Any]:
        if self.proc and self.proc.poll() is None:
            return {"ok": False, "error": "already_running"}
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text("", "utf-8")
        self.proc = self._spawn(script=script, cwd=cwd, args=args)
        self.run_id = await self.storage.create_run(script=script, cwd=cwd, args=args, pid=self.proc.pid)
        return {"ok": True, "pid": self.proc.pid, "run_id": self.run_id}

    async def stop(self) -> dict[str, Any]:
        if not self.proc or self.proc.poll() is not None:
            return {"ok": False, "error": "not_running"}
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except Exception:
            pass
        try:
            self.proc.wait(timeout=10)
        except Exception:
            try:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)
            except Exception:
                pass
            try:
                self.proc.wait(timeout=2)
            except Exception:
                pass
        if self.run_id:
            await self.storage.set_run_status(self.run_id, "stopped", pid=self.proc.pid)
            await self.storage.set_pipeline_state(state="stopped", pid=None, run_id=self.run_id, ts_kind="stop")
        self.proc = None
        self.run_id = None
        return {"ok": True}

    async def pause(self) -> dict[str, Any]:
        self.pause_flag.write_text("pause\n", "utf-8")
        if self.run_id:
            await self.storage.set_run_status(self.run_id, "paused", pid=(self.proc.pid if self.proc else None))
        return {"ok": True}

    async def resume(self) -> dict[str, Any]:
        if self.pause_flag.exists():
            self.pause_flag.unlink()
        if self.run_id:
            await self.storage.set_run_status(self.run_id, "running", pid=(self.proc.pid if self.proc else None))
        return {"ok": True}

    async def maybe_collect_exit(self) -> None:
        if not self.proc:
            return
        rc = self.proc.poll()
        if rc is None:
            return
        run_id = self.run_id
        pid = self.proc.pid
        self.proc = None
        self.run_id = None
        if not run_id:
            return
        status = "completed" if rc == 0 else "failed"
        await self.storage.set_run_status(run_id, status, pid=pid)
        await self.storage.set_pipeline_state(state="stopped", pid=None, run_id=run_id, ts_kind="stop")


class PipelineStartHandler(BaseHandler):
    def initialize(self, controller: PipelineControl, storage: Storage) -> None:
        self.controller = controller
        self.storage = storage

    async def post(self) -> None:
        ps = await self.storage.get_pipeline_state()
        cur = str(ps.get("state") or "stopped")
        if cur != "stopped":
            self.write_json(
                {
                    "ok": False,
                    "error": "invalid_transition",
                    "from": cur,
                    "action": "start",
                    "detail": f"cannot start when {cur}",
                },
                status=400,
            )
            return
        body = json.loads(self.request.body or b"{}")
        script = str(body.get("script") or safe_env("AUTOAPPDEV_PIPELINE_SCRIPT", "scripts/auto-autoappdev-development.sh"))
        cwd = str(body.get("cwd") or safe_env("AUTOAPPDEV_PIPELINE_CWD", str(REPO_ROOT)))
        args = body.get("args") or []
        if not isinstance(args, list):
            self.write_json({"ok": False, "error": "args_must_be_list"}, status=400)
            return
        # Safety guardrail: only allow scripts inside this repo.
        script_path = (Path(cwd) / script).resolve() if not Path(script).is_absolute() else Path(script).resolve()
        if REPO_ROOT not in script_path.parents and script_path != (REPO_ROOT / script).resolve():
            self.write_json({"ok": False, "error": "script_outside_repo"}, status=400)
            return
        if not script_path.exists():
            self.write_json({"ok": False, "error": "script_not_found", "path": str(script_path)}, status=404)
            return
        res = await self.controller.start(script=str(script_path), cwd=cwd, args=[str(a) for a in args])
        if res.get("ok"):
            await self.storage.set_pipeline_state(
                state="running", pid=res.get("pid"), run_id=res.get("run_id"), ts_kind="start"
            )
        self.write_json(res, status=200 if res.get("ok") else 409)


class PipelineStopHandler(BaseHandler):
    def initialize(self, controller: PipelineControl, storage: Storage) -> None:
        self.controller = controller
        self.storage = storage

    async def post(self) -> None:
        ps = await self.storage.get_pipeline_state()
        cur = str(ps.get("state") or "stopped")
        if cur not in ("running", "paused"):
            self.write_json(
                {
                    "ok": False,
                    "error": "invalid_transition",
                    "from": cur,
                    "action": "stop",
                    "detail": f"cannot stop when {cur}",
                },
                status=400,
            )
            return
        res = await self.controller.stop()
        if res.get("ok"):
            pid = self.controller.proc.pid if self.controller.proc else None
            await self.storage.set_pipeline_state(state="stopped", pid=None, run_id=self.controller.run_id, ts_kind="stop")
        self.write_json(res, status=200 if res.get("ok") else 500)


class PipelinePauseHandler(BaseHandler):
    def initialize(self, controller: PipelineControl, storage: Storage) -> None:
        self.controller = controller
        self.storage = storage

    async def post(self) -> None:
        ps = await self.storage.get_pipeline_state()
        cur = str(ps.get("state") or "stopped")
        if cur != "running":
            self.write_json(
                {
                    "ok": False,
                    "error": "invalid_transition",
                    "from": cur,
                    "action": "pause",
                    "detail": f"cannot pause when {cur}",
                },
                status=400,
            )
            return
        res = await self.controller.pause()
        if res.get("ok"):
            pid = self.controller.proc.pid if self.controller.proc else None
            await self.storage.set_pipeline_state(state="paused", pid=pid, run_id=self.controller.run_id, ts_kind="pause")
        self.write_json(res)


class PipelineResumeHandler(BaseHandler):
    def initialize(self, controller: PipelineControl, storage: Storage) -> None:
        self.controller = controller
        self.storage = storage

    async def post(self) -> None:
        ps = await self.storage.get_pipeline_state()
        cur = str(ps.get("state") or "stopped")
        if cur != "paused":
            self.write_json(
                {
                    "ok": False,
                    "error": "invalid_transition",
                    "from": cur,
                    "action": "resume",
                    "detail": f"cannot resume when {cur}",
                },
                status=400,
            )
            return
        res = await self.controller.resume()
        if res.get("ok"):
            pid = self.controller.proc.pid if self.controller.proc else None
            await self.storage.set_pipeline_state(state="running", pid=pid, run_id=self.controller.run_id, ts_kind="resume")
        self.write_json(res)


class LogsTailHandler(BaseHandler):
    def initialize(self, log_dir: Path) -> None:
        self.log_dir = log_dir

    async def get(self) -> None:
        name = self.get_query_argument("name", "pipeline")
        n = int(self.get_query_argument("lines", "200"))
        n = max(10, min(2000, n))
        allowed = {
            "pipeline": self.log_dir / "pipeline.log",
            "backend": self.log_dir / "backend.log",
        }
        p = allowed.get(name)
        if not p:
            self.write_json({"error": "unknown_log"}, status=400)
            return
        if not p.exists():
            self.write_json({"lines": []})
            return
        try:
            data = p.read_text("utf-8", errors="replace").splitlines()[-n:]
        except Exception:
            data = []
        self.write_json({"lines": data, "name": name})


class LogsSinceHandler(BaseHandler):
    def initialize(self, log_buffer: LogBuffer) -> None:
        self.log_buffer = log_buffer

    async def get(self) -> None:
        source = self.get_query_argument("source", "pipeline")
        since = int(self.get_query_argument("since", "0"))
        limit = int(self.get_query_argument("limit", "200"))
        items = self.log_buffer.since(since_id=since, limit=limit, source=source or None)
        nxt = since
        if items:
            try:
                nxt = int(items[-1].get("id", since))
            except Exception:
                nxt = since
        self.write_json({"source": source, "since": since, "next": nxt, "lines": items})


def _load_env() -> None:
    load_dotenv(dotenv_path=REPO_ROOT / ".env", override=False)


def _compute_paths() -> tuple[Path, Path]:
    runtime_dir = Path(safe_env("AUTOAPPDEV_RUNTIME_DIR", str(REPO_ROOT / "runtime"))).resolve()
    log_dir = runtime_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return runtime_dir, log_dir


def _require_env() -> None:
    missing: list[str] = []
    if not safe_env("DATABASE_URL", "").strip():
        missing.append("DATABASE_URL")
    if missing:
        print(f"ERROR: missing required env: {', '.join(missing)}", file=sys.stderr)
        print("Hint: cp .env.example .env and set required values (see docs/env.md).", file=sys.stderr)
        raise SystemExit(2)


def _listen_port() -> int:
    # Prefer AUTOAPPDEV_PORT (current convention), but allow PORT as an alias.
    raw = safe_env("AUTOAPPDEV_PORT", "").strip() or safe_env("PORT", "8788").strip()
    try:
        return int(raw)
    except Exception:
        return 8788


async def make_app(runtime_dir: Path, log_dir: Path) -> tornado.web.Application:
    host = safe_env("AUTOAPPDEV_HOST", "127.0.0.1")
    port = _listen_port()
    db_url = safe_env("DATABASE_URL", "")

    storage = Storage(database_url=db_url, runtime_dir=runtime_dir)
    await storage.start()
    schema_path = Path(__file__).with_name("schema.sql")
    await storage.ensure_schema(schema_path.read_text("utf-8"))
    # Smoke check: prove DB is reachable by fetching server time during startup.
    db_time = await storage.get_server_time_iso()
    print(f"DB time: {db_time}")

    controller = PipelineControl(storage=storage, runtime_dir=runtime_dir, log_dir=log_dir)
    tornado.ioloop.PeriodicCallback(lambda: asyncio.create_task(controller.maybe_collect_exit()), 500).start()

    log_buffer = LogBuffer(max_entries=2000)
    tailers = [
        FileLogTailer(source="pipeline", path=log_dir / "pipeline.log", buf=log_buffer),
        FileLogTailer(source="backend", path=log_dir / "backend.log", buf=log_buffer),
    ]

    def _poll_logs() -> None:
        for t in tailers:
            t.poll()

    tornado.ioloop.PeriodicCallback(_poll_logs, 500).start()

    app = tornado.web.Application(
        [
            (r"/api/health", HealthHandler, {"storage": storage}),
            (r"/api/version", VersionHandler),
            (r"/api/config", ConfigHandler, {"storage": storage}),
            (r"/api/plan", PlanHandler, {"storage": storage}),
            (r"/api/scripts", ScriptsHandler, {"storage": storage}),
            (r"/api/scripts/([0-9]+)", ScriptHandler, {"storage": storage}),
            (r"/api/scripts/parse", ScriptsParseHandler),
            (r"/api/scripts/import-shell", ScriptsImportShellHandler),
            (r"/api/chat", ChatHandler, {"storage": storage, "runtime_dir": runtime_dir}),
            (r"/api/inbox", InboxHandler, {"storage": storage, "runtime_dir": runtime_dir}),
            (r"/api/pipeline", PipelineStateHandler, {"storage": storage}),
            (r"/api/pipeline/status", PipelineStatusHandler, {"storage": storage}),
            (r"/api/pipeline/start", PipelineStartHandler, {"controller": controller, "storage": storage}),
            (r"/api/pipeline/stop", PipelineStopHandler, {"controller": controller, "storage": storage}),
            (r"/api/pipeline/pause", PipelinePauseHandler, {"controller": controller, "storage": storage}),
            (r"/api/pipeline/resume", PipelineResumeHandler, {"controller": controller, "storage": storage}),
            (r"/api/logs", LogsSinceHandler, {"log_buffer": log_buffer}),
            (r"/api/logs/tail", LogsTailHandler, {"log_dir": log_dir}),
        ],
        debug=True,
    )
    app.listen(port, address=host)
    return app


def main() -> None:
    _load_env()
    _require_env()
    runtime_dir, log_dir = _compute_paths()
    global RUNTIME_DIR, LOG_DIR
    RUNTIME_DIR = runtime_dir
    LOG_DIR = log_dir

    loop = asyncio.get_event_loop()
    try:
        # Fail fast: ensure DB connectivity/schema application happens before entering the IOLoop.
        loop.run_until_complete(make_app(runtime_dir=runtime_dir, log_dir=log_dir))
    except Exception as e:
        print(f"ERROR: backend startup failed: {type(e).__name__}: {e}", file=sys.stderr)
        print("Hint: verify Postgres is running and DATABASE_URL is correct (see docs/env.md).", file=sys.stderr)
        raise SystemExit(1)

    # Redirect tornado logs to file for easier tailing in the PWA.
    backend_log = (log_dir / "backend.log").open("a", encoding="utf-8")
    sys.stdout = backend_log  # type: ignore[assignment]
    sys.stderr = backend_log  # type: ignore[assignment]
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
