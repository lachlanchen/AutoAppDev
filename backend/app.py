import asyncio
import json
import os
import signal
import subprocess
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import tornado.ioloop
import tornado.web

from .storage import Storage, safe_env


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = Path(safe_env("AUTOAPPDEV_RUNTIME_DIR", str(REPO_ROOT / "runtime"))).resolve()
LOG_DIR = RUNTIME_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


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


class HealthHandler(BaseHandler):
    async def get(self) -> None:
        self.write_json({"ok": True, "service": "autoappdev-backend"})


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


class ChatHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

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
        _write_inbox_message(RUNTIME_DIR, content)
        self.write_json({"ok": True})


class PipelineStatusHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        st = await self.storage.get_latest_status()
        self.write_json({"status": {"running": st.running, "pid": st.pid, "run_id": st.run_id, "state": st.status}})


class PipelineControl:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.proc: subprocess.Popen | None = None
        self.run_id: int | None = None
        self.log_path = LOG_DIR / "pipeline.log"
        self.pause_flag = RUNTIME_DIR / "PAUSE"

    async def refresh_from_storage(self) -> None:
        st = await self.storage.get_latest_status()
        if st.running and st.pid and not self.proc:
            # Server restarted while pipeline is running. We do not reattach to process.
            pass

    def _spawn(self, script: str, cwd: str, args: list[str]) -> subprocess.Popen:
        out = self.log_path.open("ab", buffering=0)
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
        if self.run_id:
            await self.storage.set_run_status(self.run_id, "stopped", pid=self.proc.pid)
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


class PipelineStartHandler(BaseHandler):
    def initialize(self, controller: PipelineControl, storage: Storage) -> None:
        self.controller = controller
        self.storage = storage

    async def post(self) -> None:
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
        self.write_json(res, status=200 if res.get("ok") else 409)


class PipelineStopHandler(BaseHandler):
    def initialize(self, controller: PipelineControl) -> None:
        self.controller = controller

    async def post(self) -> None:
        res = await self.controller.stop()
        self.write_json(res, status=200 if res.get("ok") else 409)


class PipelinePauseHandler(BaseHandler):
    def initialize(self, controller: PipelineControl) -> None:
        self.controller = controller

    async def post(self) -> None:
        res = await self.controller.pause()
        self.write_json(res)


class PipelineResumeHandler(BaseHandler):
    def initialize(self, controller: PipelineControl) -> None:
        self.controller = controller

    async def post(self) -> None:
        res = await self.controller.resume()
        self.write_json(res)


class LogsTailHandler(BaseHandler):
    async def get(self) -> None:
        name = self.get_query_argument("name", "pipeline")
        n = int(self.get_query_argument("lines", "200"))
        n = max(10, min(2000, n))
        allowed = {
            "pipeline": LOG_DIR / "pipeline.log",
            "backend": LOG_DIR / "backend.log",
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


async def make_app() -> tornado.web.Application:
    load_dotenv(dotenv_path=REPO_ROOT / ".env", override=False)
    host = safe_env("AUTOAPPDEV_HOST", "127.0.0.1")
    port = int(safe_env("AUTOAPPDEV_PORT", "8788"))
    db_url = safe_env("DATABASE_URL", "")

    storage = Storage(database_url=db_url, runtime_dir=RUNTIME_DIR)
    await storage.start()
    schema_path = Path(__file__).with_name("schema.sql")
    await storage.ensure_schema(schema_path.read_text("utf-8"))

    controller = PipelineControl(storage=storage)

    app = tornado.web.Application(
        [
            (r"/api/health", HealthHandler),
            (r"/api/config", ConfigHandler, {"storage": storage}),
            (r"/api/chat", ChatHandler, {"storage": storage}),
            (r"/api/pipeline/status", PipelineStatusHandler, {"storage": storage}),
            (r"/api/pipeline/start", PipelineStartHandler, {"controller": controller, "storage": storage}),
            (r"/api/pipeline/stop", PipelineStopHandler, {"controller": controller}),
            (r"/api/pipeline/pause", PipelinePauseHandler, {"controller": controller}),
            (r"/api/pipeline/resume", PipelineResumeHandler, {"controller": controller}),
            (r"/api/logs/tail", LogsTailHandler),
        ],
        debug=True,
    )
    app.listen(port, address=host)
    return app


def main() -> None:
    # Redirect tornado logs to file for easier tailing in the PWA.
    backend_log = (LOG_DIR / "backend.log").open("a", encoding="utf-8")
    import sys

    sys.stdout = backend_log  # type: ignore[assignment]
    sys.stderr = backend_log  # type: ignore[assignment]

    loop = asyncio.get_event_loop()
    loop.create_task(make_app())
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

