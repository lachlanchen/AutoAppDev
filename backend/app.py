import asyncio
from collections import deque
import datetime
import hashlib
import json
import os
import re
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
from .llm_assisted_parse import LlmParseError, build_prompt, extract_aaps, make_request_id, run_codex_to_jsonl, write_artifacts
from .action_registry import ActionRegistryError, validate_action_create, validate_action_update
from .builtin_actions import get_builtin_action, is_builtin_action_id, list_builtin_action_summaries
from .update_readme_action import (
    UpdateReadmeError,
    make_update_id,
    resolve_workspace_readme_path,
    upsert_readme_block,
    validate_block_markdown,
    validate_workspace_slug,
    write_update_artifacts,
)
from .workspace_config import WorkspaceConfigError, default_workspace_config, normalize_workspace_config, validate_workspace


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


def _parse_outbox_role(raw: Any) -> str:
    role = str(raw or "").strip().lower()
    if role in ("system", "pipeline"):
        return role
    return "pipeline"


def _infer_outbox_role_from_name(name: str) -> str:
    n = str(name or "")
    m = re.match(r"^[0-9]+_([a-zA-Z0-9-]+)\.", n)
    if not m:
        return "pipeline"
    return _parse_outbox_role(m.group(1))


async def _ingest_outbox_files(*, storage: Storage, runtime_dir: Path, max_files: int = 50) -> None:
    outbox = runtime_dir / "outbox"
    outbox.mkdir(parents=True, exist_ok=True)
    processed = outbox / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    try:
        items = sorted([p for p in outbox.iterdir() if p.is_file()])
    except Exception:
        return

    n = 0
    for p in items:
        if n >= max_files:
            break
        if p.name.startswith("."):
            continue
        if p.suffix.lower() not in (".md", ".txt"):
            continue
        role = _infer_outbox_role_from_name(p.name)
        try:
            txt = p.read_text("utf-8", errors="replace")
        except Exception:
            continue
        content = txt.strip()
        if content:
            await storage.add_outbox_message(role, content[:10_000])
        # Move to processed to prevent re-ingest.
        dest = processed / p.name
        if dest.exists():
            ts = int(asyncio.get_event_loop().time() * 1000)
            dest = processed / f"{p.stem}_{ts}{p.suffix}"
        try:
            p.replace(dest)
        except Exception:
            # Best-effort: if move fails, avoid tight loops by removing the file.
            try:
                p.unlink()
            except Exception:
                pass
        n += 1


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


class WorkspaceConfigHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self, workspace: str) -> None:
        try:
            ws = validate_workspace(workspace)
        except WorkspaceConfigError as e:
            self.write_json(e.to_dict(), status=400)
            return
        rec = await self.storage.get_workspace_config(ws)
        if not rec:
            self.write_json(
                {"ok": True, "workspace": ws, "exists": False, "config": default_workspace_config(), "updated_at": None}
            )
            return
        cfg = rec.get("config") if isinstance(rec.get("config"), dict) else {}
        self.write_json(
            {
                "ok": True,
                "workspace": ws,
                "exists": True,
                "config": cfg,
                "updated_at": rec.get("updated_at"),
            }
        )

    async def post(self, workspace: str) -> None:
        try:
            ws = validate_workspace(workspace)
        except WorkspaceConfigError as e:
            self.write_json(e.to_dict(), status=400)
            return
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return

        existing = await self.storage.get_workspace_config(ws)
        base = existing.get("config") if existing and isinstance(existing.get("config"), dict) else None
        try:
            cfg = normalize_workspace_config(body, repo_root=REPO_ROOT, workspace=ws, base=base)
        except WorkspaceConfigError as e:
            self.write_json(e.to_dict(), status=400)
            return
        rec = await self.storage.upsert_workspace_config(ws, cfg)
        self.write_json({"ok": True, "workspace": ws, "config": cfg, "updated_at": rec.get("updated_at")})


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


class ScriptsParseLlmHandler(BaseHandler):
    def initialize(self, storage: Storage, runtime_dir: Path) -> None:
        self.storage = storage
        self.runtime_dir = runtime_dir

    async def post(self) -> None:
        if safe_env("AUTOAPPDEV_ENABLE_LLM_PARSE", "0").strip() != "1":
            self.write_json({"ok": False, "error": "disabled"}, status=403)
            return

        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"ok": False, "error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"ok": False, "error": "invalid_body"}, status=400)
            return

        source_text = body.get("source_text")
        if not isinstance(source_text, str) or not source_text.strip():
            self.write_json({"ok": False, "error": "invalid_source_text"}, status=400)
            return
        if len(source_text) > 100_000:
            self.write_json({"ok": False, "error": "source_too_large"}, status=400)
            return

        source_format = body.get("source_format", "unknown")
        if not isinstance(source_format, str):
            self.write_json({"ok": False, "error": "invalid_source_format"}, status=400)
            return

        save = body.get("save", False)
        if not isinstance(save, bool):
            self.write_json({"ok": False, "error": "invalid_save"}, status=400)
            return

        title = str(body.get("title") or "").strip()

        req_model = body.get("model")
        if req_model is not None and not isinstance(req_model, str):
            self.write_json({"ok": False, "error": "invalid_model"}, status=400)
            return

        req_reasoning = body.get("reasoning")
        if req_reasoning is not None and not isinstance(req_reasoning, str):
            self.write_json({"ok": False, "error": "invalid_reasoning"}, status=400)
            return

        timeout_s = body.get("timeout_s", 45)
        if not isinstance(timeout_s, (int, float)):
            self.write_json({"ok": False, "error": "invalid_timeout_s"}, status=400)
            return
        timeout_s = float(timeout_s)
        timeout_s = max(5.0, min(120.0, timeout_s))

        cfg = await self.storage.get_config()
        cfg_model = cfg.get("model") if isinstance(cfg, dict) and isinstance(cfg.get("model"), str) else ""
        model = str(req_model or cfg_model or safe_env("AUTOAPPDEV_CODEX_MODEL", "gpt-5.3-codex"))
        reasoning = str(req_reasoning or safe_env("AUTOAPPDEV_CODEX_REASONING", "medium"))
        skip_git_check = safe_env("AUTOAPPDEV_CODEX_SKIP_GIT_CHECK", "0").strip() == "1"

        req_id = make_request_id(source_text=source_text)
        artifacts_dir = self.runtime_dir / "logs" / "llm_parse" / req_id
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        prompt = build_prompt(source_text=source_text, source_format=source_format)
        warnings: list[str] = []

        provenance: dict[str, Any] = {
            "id": req_id,
            "model": model,
            "reasoning": reasoning,
            "timeout_s": timeout_s,
            "source_format": source_format,
            "source_sha256": hashlib.sha256(source_text.encode("utf-8", errors="replace")).hexdigest(),
        }

        # Precompute artifact paths for provenance (write_artifacts uses these names).
        provenance["artifacts"] = {
            "dir": str(artifacts_dir),
            "source": str(artifacts_dir / "source.txt"),
            "prompt": str(artifacts_dir / "prompt.txt"),
            "codex_jsonl": str(artifacts_dir / "codex.jsonl"),
            "codex_stderr": str(artifacts_dir / "codex.stderr.log"),
            "assistant": str(artifacts_dir / "assistant.txt"),
            "aaps": str(artifacts_dir / "result.aaps"),
            "provenance": str(artifacts_dir / "provenance.json"),
        }

        assistant_text = ""
        codex_jsonl = ""
        codex_stderr = ""
        rc = 0
        script_text: str | None = None

        try:
            assistant_text, codex_jsonl, codex_stderr, rc = await run_codex_to_jsonl(
                prompt=prompt,
                model=model,
                reasoning=reasoning,
                timeout_s=timeout_s,
                cwd=artifacts_dir,
                skip_git_check=skip_git_check,
            )
            provenance["codex_exit_code"] = rc
            if rc != 0:
                warnings.append("codex_nonzero_exit")
            if not assistant_text.strip():
                tail = (codex_stderr or "").strip().splitlines()[-5:]
                hint = "\n".join(tail).strip()
                raise LlmParseError("missing_assistant_text", hint or "no agent_message found in codex JSONL output")

            script_text, w2 = extract_aaps(assistant_text)
            warnings.extend(w2)
            provenance["aaps_sha256"] = hashlib.sha256(script_text.encode("utf-8", errors="replace")).hexdigest()

            ir = parse_aaps_v1(script_text)
            provenance["ok"] = True
            provenance["warnings"] = warnings
        except ParseError as e:
            provenance["ok"] = False
            provenance["warnings"] = warnings
            provenance["parse_error"] = e.to_dict()
            write_artifacts(
                artifacts_dir=artifacts_dir,
                source_text=source_text,
                prompt=prompt,
                codex_jsonl=codex_jsonl,
                codex_stderr=codex_stderr,
                assistant_text=assistant_text,
                script_text=script_text,
                provenance=provenance,
            )
            self.write_json({**e.to_dict(), "provenance": provenance}, status=400)
            return
        except LlmParseError as e:
            provenance["ok"] = False
            provenance["warnings"] = warnings
            provenance["llm_error"] = e.to_dict()
            write_artifacts(
                artifacts_dir=artifacts_dir,
                source_text=source_text,
                prompt=prompt,
                codex_jsonl=codex_jsonl,
                codex_stderr=codex_stderr,
                assistant_text=assistant_text,
                script_text=script_text,
                provenance=provenance,
            )
            status = 504 if e.code == "timeout" else 503 if e.code == "codex_not_found" else 400
            self.write_json({**e.to_dict(), "provenance": provenance}, status=status)
            return

        # Success path: always write artifacts.
        write_artifacts(
            artifacts_dir=artifacts_dir,
            source_text=source_text,
            prompt=prompt,
            codex_jsonl=codex_jsonl,
            codex_stderr=codex_stderr,
            assistant_text=assistant_text,
            script_text=script_text,
            provenance=provenance,
        )

        script_obj: dict[str, Any] | None = None
        if save:
            script_obj = await self.storage.create_pipeline_script(
                title=title or f"llm_import_{req_id}",
                script_text=script_text or "",
                script_version=1,
                script_format="aaps",
                ir=ir,
            )

        self.write_json(
            {
                "ok": True,
                "script_format": "aaps",
                "script_text": script_text or "",
                "ir": ir,
                "warnings": warnings,
                "provenance": provenance,
                "script": script_obj,
            }
        )


class UpdateReadmeHandler(BaseHandler):
    def initialize(self, runtime_dir: Path) -> None:
        self.runtime_dir = runtime_dir

    async def post(self) -> None:
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"ok": False, "error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"ok": False, "error": "invalid_body"}, status=400)
            return

        workspace = body.get("workspace")
        if not isinstance(workspace, str):
            self.write_json({"ok": False, "error": "invalid_workspace"}, status=400)
            return
        block_markdown = body.get("block_markdown")
        if not isinstance(block_markdown, str):
            self.write_json({"ok": False, "error": "invalid_block_markdown"}, status=400)
            return

        try:
            ws = validate_workspace_slug(workspace)
            validate_block_markdown(block_markdown)
            update_id = make_update_id(workspace=ws, block_markdown=block_markdown)
            target = resolve_workspace_readme_path(REPO_ROOT, ws)
        except UpdateReadmeError as e:
            status = 403 if e.code in {"path_outside_repo", "path_outside_auto_apps"} else 400
            self.write_json(e.to_dict(), status=status)
            return

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.write_json({"ok": False, "error": "mkdir_failed", "detail": f"{type(e).__name__}: {e}"}, status=500)
            return

        before: str | None = None
        if target.exists():
            try:
                before = target.read_text("utf-8")
            except Exception as e:
                self.write_json({"ok": False, "error": "read_failed", "detail": f"{type(e).__name__}: {e}"}, status=500)
                return

        try:
            after, meta = upsert_readme_block(before, workspace=ws, block_markdown=block_markdown)
        except UpdateReadmeError as e:
            self.write_json(e.to_dict(), status=400)
            return

        updated = before is None or after != before
        if updated:
            tmp = target.with_name(target.name + f".{update_id}.tmp")
            try:
                tmp.write_text(after, "utf-8")
                tmp.replace(target)
            except Exception as e:
                try:
                    if tmp.exists():
                        tmp.unlink()
                except Exception:
                    pass
                self.write_json({"ok": False, "error": "write_failed", "detail": f"{type(e).__name__}: {e}"}, status=500)
                return

        rel = str(target.relative_to(REPO_ROOT)) if REPO_ROOT in target.parents else str(target)
        meta_out: dict[str, Any] = {
            **(meta or {}),
            "id": update_id,
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "workspace": ws,
            "path": rel,
            "updated": updated,
        }
        try:
            artifacts = write_update_artifacts(
                runtime_dir=self.runtime_dir,
                update_id=update_id,
                before=before or "",
                after=after,
                meta=meta_out,
            )
        except Exception as e:
            self.write_json(
                {"ok": False, "error": "artifact_write_failed", "detail": f"{type(e).__name__}: {e}"},
                status=500,
            )
            return

        print(
            f"update_readme id={update_id} workspace={ws} path={rel} updated={updated} "
            f"markers_preexisted={bool(meta_out.get('markers_preexisted'))}"
        )
        self.write_json(
            {
                "ok": True,
                "workspace": ws,
                "path": rel,
                "updated": updated,
                "markers_preexisted": bool(meta_out.get("markers_preexisted")),
                "artifacts": {"dir": str(artifacts.dir)},
            }
        )


class ActionsHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        limit_raw = int(self.get_query_argument("limit", "50"))
        limit = max(1, min(200, int(limit_raw)))

        builtins = list_builtin_action_summaries()
        if len(builtins) >= limit:
            self.write_json({"actions": builtins[:limit]})
            return

        remaining = max(0, limit - len(builtins))
        items = await self.storage.list_action_definitions(limit=remaining)
        # Add a stable readonly field for non-builtin actions.
        items_out = [dict(it, readonly=False) for it in items]
        self.write_json({"actions": builtins + items_out})

    async def post(self) -> None:
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return
        cfg = await self.storage.get_config()
        try:
            title, kind, spec, enabled = validate_action_create(body, repo_root=REPO_ROOT, cfg=cfg)
        except ActionRegistryError as e:
            self.write_json(e.to_dict(), status=400)
            return
        action = await self.storage.create_action_definition(title=title, kind=kind, spec=spec, enabled=enabled)
        self.write_json({"ok": True, "action": action})


class ActionHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self, action_id: str) -> None:
        try:
            aid = int(action_id)
        except Exception:
            self.write_json({"error": "invalid_id"}, status=400)
            return
        if is_builtin_action_id(aid):
            action = get_builtin_action(aid)
            if not action:
                self.write_json({"error": "not_found"}, status=404)
                return
            self.write_json({"action": action})
            return
        action = await self.storage.get_action_definition(aid)
        if not action:
            self.write_json({"error": "not_found"}, status=404)
            return
        action = dict(action, readonly=False)
        self.write_json({"action": action})

    async def put(self, action_id: str) -> None:
        try:
            aid = int(action_id)
        except Exception:
            self.write_json({"error": "invalid_id"}, status=400)
            return
        if is_builtin_action_id(aid):
            self.write_json(
                {"error": "readonly", "detail": "built-in actions are read-only; clone to edit"},
                status=403,
            )
            return
        try:
            body = json.loads(self.request.body or b"{}")
        except Exception:
            self.write_json({"error": "invalid_json"}, status=400)
            return
        if not isinstance(body, dict):
            self.write_json({"error": "invalid_body"}, status=400)
            return
        cur = await self.storage.get_action_definition(aid)
        if not cur:
            self.write_json({"error": "not_found"}, status=404)
            return
        cfg = await self.storage.get_config()
        try:
            title, spec, enabled = validate_action_update(body, repo_root=REPO_ROOT, existing=cur, cfg=cfg)
        except ActionRegistryError as e:
            self.write_json(e.to_dict(), status=400)
            return
        spec_set = "spec" in body
        updated = await self.storage.update_action_definition(
            aid,
            title=title,
            spec=spec,
            spec_set=spec_set,
            enabled=enabled,
        )
        if not updated:
            self.write_json({"error": "not_found"}, status=404)
            return
        updated = dict(updated, readonly=False)
        self.write_json({"ok": True, "action": updated})

    async def delete(self, action_id: str) -> None:
        try:
            aid = int(action_id)
        except Exception:
            self.write_json({"error": "invalid_id"}, status=400)
            return
        if is_builtin_action_id(aid):
            self.write_json(
                {"error": "readonly", "detail": "built-in actions are read-only; clone to edit"},
                status=403,
            )
            return
        ok = await self.storage.delete_action_definition(aid)
        if not ok:
            self.write_json({"error": "not_found"}, status=404)
            return
        self.write_json({"ok": True})


class ActionCloneHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def post(self, action_id: str) -> None:
        try:
            aid = int(action_id)
        except Exception:
            self.write_json({"error": "invalid_id"}, status=400)
            return
        builtin = get_builtin_action(aid)
        if not builtin:
            self.write_json({"error": "not_found"}, status=404)
            return

        base_title = str(builtin.get("title") or "Action").strip() or "Action"
        clone_title = f"{base_title} (copy)"
        if len(clone_title) > 200:
            clone_title = clone_title[:200].rstrip()
            if not clone_title:
                clone_title = "Action (copy)"

        body = {
            "title": clone_title,
            "kind": str(builtin.get("kind") or "prompt"),
            "enabled": bool(builtin.get("enabled", True)),
            "spec": builtin.get("spec") if isinstance(builtin.get("spec"), dict) else {},
        }
        cfg = await self.storage.get_config()
        try:
            title, kind, spec, enabled = validate_action_create(body, repo_root=REPO_ROOT, cfg=cfg)
        except ActionRegistryError as e:
            self.write_json(e.to_dict(), status=400)
            return
        action = await self.storage.create_action_definition(title=title, kind=kind, spec=spec, enabled=enabled)
        self.write_json({"ok": True, "action": dict(action, readonly=False)})


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


class OutboxHandler(BaseHandler):
    def initialize(self, storage: Storage) -> None:
        self.storage = storage

    async def get(self) -> None:
        limit = int(self.get_query_argument("limit", "50"))
        items = await self.storage.list_outbox_messages(limit=limit)
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
        role = _parse_outbox_role(body.get("role"))
        await self.storage.add_outbox_message(role, content)
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

    outbox_state: dict[str, Any] = {"running": False}

    async def _run_outbox_ingest() -> None:
        try:
            await _ingest_outbox_files(storage=storage, runtime_dir=runtime_dir, max_files=50)
        except Exception:
            pass
        finally:
            outbox_state["running"] = False

    def _poll_outbox() -> None:
        if outbox_state.get("running"):
            return
        outbox_state["running"] = True
        asyncio.create_task(_run_outbox_ingest())

    tornado.ioloop.PeriodicCallback(_poll_outbox, 750).start()

    app = tornado.web.Application(
        [
            (r"/api/health", HealthHandler, {"storage": storage}),
            (r"/api/version", VersionHandler),
            (r"/api/config", ConfigHandler, {"storage": storage}),
            (r"/api/plan", PlanHandler, {"storage": storage}),
            (r"/api/workspaces/([^/]+)/config", WorkspaceConfigHandler, {"storage": storage}),
            (r"/api/scripts", ScriptsHandler, {"storage": storage}),
            (r"/api/scripts/([0-9]+)", ScriptHandler, {"storage": storage}),
            (r"/api/scripts/parse", ScriptsParseHandler),
            (r"/api/scripts/import-shell", ScriptsImportShellHandler),
            (r"/api/scripts/parse-llm", ScriptsParseLlmHandler, {"storage": storage, "runtime_dir": runtime_dir}),
            (r"/api/actions", ActionsHandler, {"storage": storage}),
            (r"/api/actions/([0-9]+)/clone", ActionCloneHandler, {"storage": storage}),
            (r"/api/actions/([0-9]+)", ActionHandler, {"storage": storage}),
            (r"/api/actions/update-readme", UpdateReadmeHandler, {"runtime_dir": runtime_dir}),
            (r"/api/chat", ChatHandler, {"storage": storage, "runtime_dir": runtime_dir}),
            (r"/api/inbox", InboxHandler, {"storage": storage, "runtime_dir": runtime_dir}),
            (r"/api/outbox", OutboxHandler, {"storage": storage}),
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
