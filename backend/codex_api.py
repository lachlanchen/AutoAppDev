import asyncio
import datetime
import hashlib
import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Any


FINAL_STATUSES = {"succeeded", "failed"}
REASONING_LEVELS = {"low", "medium", "high", "xhigh"}


class CodexJobError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code
        self.detail = detail

    def to_dict(self) -> dict[str, Any]:
        return {"ok": False, "error": self.code, "detail": self.detail}


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def safe_job_id(raw: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_.-]+", "-", str(raw or "").strip())
    s = s.strip(".-")
    if not s:
        raise CodexJobError("invalid_job_id", "job id is required")
    return s[:160]


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, "utf-8")
    tmp.replace(path)


def atomic_write_json(path: Path, obj: Any) -> None:
    atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text("utf-8"))
    except Exception:
        return default


def tail_text(path: Path, max_chars: int = 8000) -> str:
    if not path.exists():
        return ""
    try:
        data = path.read_text("utf-8", errors="replace")
    except Exception:
        return ""
    return data[-max_chars:]


def normalize_reasoning(raw: Any, default: str) -> str:
    r = str(raw or default).strip().lower()
    return r if r in REASONING_LEVELS else default


class CodexJobManager:
    """File-backed Codex response/job API for AutoAppDev.

    This is intentionally independent from LazyBlog. Jobs are inspectable and
    resumable from runtime/codex-jobs/<job-id>/.
    """

    def __init__(self, *, repo_root: Path, runtime_dir: Path, prompt_path: Path, schema_path: Path):
        self.repo_root = repo_root.resolve()
        self.runtime_dir = runtime_dir.resolve()
        self.jobs_root = self.runtime_dir / "codex-jobs"
        self.prompt_path = prompt_path.resolve()
        self.schema_path = schema_path.resolve()
        self.jobs_root.mkdir(parents=True, exist_ok=True)
        self._tasks: dict[str, asyncio.Task[Any]] = {}
        self.default_model = os.environ.get("AUTOAPPDEV_CODEX_MODEL", "gpt-5.5")
        self.default_response_reasoning = os.environ.get("AUTOAPPDEV_RESPONSE_REASONING", "medium")
        self.default_assistant_reasoning = os.environ.get("AUTOAPPDEV_ASSISTANT_REASONING", "high")
        self.default_timeout_s = float(os.environ.get("AUTOAPPDEV_CODEX_TIMEOUT_S", "300"))
        self.mock = os.environ.get("AUTOAPPDEV_MOCK_CODEX", "0").strip() == "1"

    def new_job_id(self, tool: str) -> str:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        suffix = _sha256_text(f"{ts}:{tool}:{time.monotonic()}")[:8]
        return f"{ts}-{suffix}-{tool}"

    def job_dir(self, job_id: str) -> Path:
        return self.jobs_root / safe_job_id(job_id)

    def job_path(self, job_id: str) -> Path:
        return self.job_dir(job_id) / "job.json"

    def read_job(self, job_id: str) -> dict[str, Any]:
        job = read_json(self.job_path(job_id))
        if not isinstance(job, dict):
            raise CodexJobError("unknown_job", f"unknown job: {job_id}")
        return job

    def write_job(self, job_id: str, job: dict[str, Any]) -> None:
        atomic_write_json(self.job_path(job_id), job)

    def update_job(self, job_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        job = self.read_job(job_id)
        job.update(updates)
        job["updated_at"] = now_iso()
        self.write_job(job_id, job)
        return job

    def normalize_tool(self, raw: Any) -> str:
        tool = str(raw or "response").strip().lower()
        if tool == "respond":
            tool = "response"
        if tool not in {"response", "assistant"}:
            raise CodexJobError("invalid_tool", "tool must be response or assistant")
        return tool

    def default_reasoning_for_tool(self, tool: str) -> str:
        if tool == "assistant":
            return normalize_reasoning(self.default_assistant_reasoning, "high")
        return normalize_reasoning(self.default_response_reasoning, "medium")

    def submit_job(self, payload: dict[str, Any], *, start: bool = True) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise CodexJobError("invalid_body", "request body must be an object")
        tool = self.normalize_tool(payload.get("tool"))
        prompt = str(payload.get("prompt") or "").strip()
        if not prompt:
            raise CodexJobError("empty_prompt", "prompt is required")

        model = str(payload.get("model") or self.default_model).strip() or self.default_model
        reasoning = normalize_reasoning(payload.get("reasoning"), self.default_reasoning_for_tool(tool))
        allow_edits = bool(payload.get("allow_edits", tool == "assistant"))

        job_id = self.new_job_id(tool)
        job_dir = self.job_dir(job_id)
        job_dir.mkdir(parents=True, exist_ok=True)
        job = {
            "id": job_id,
            "tool": tool,
            "status": "queued",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "started_at": None,
            "finished_at": None,
            "elapsed_seconds": None,
            "model": model,
            "reasoning": reasoning,
            "allow_edits": allow_edits,
            "mode": str(payload.get("mode") or ""),
            "session_id": str(payload.get("session_id") or ""),
            "prompt_preview": prompt[:240],
            "poll_url": f"/api/codex/job?id={job_id}",
            "result_url": f"/api/codex/result?id={job_id}",
            "paths": {
                "dir": str(job_dir),
                "input": str(job_dir / "input.json"),
                "prompt": str(job_dir / "prompt.txt"),
                "output": str(job_dir / "output.json"),
                "stdout": str(job_dir / "stdout.log"),
                "stderr": str(job_dir / "stderr.log"),
            },
        }
        atomic_write_json(job_dir / "input.json", payload)
        self.write_job(job_id, job)
        if start:
            self.start_job(job_id)
        return self.job_status(job_id, include_logs=False, include_output=False)

    def start_job(self, job_id: str) -> None:
        jid = safe_job_id(job_id)
        task = self._tasks.get(jid)
        if task and not task.done():
            return
        self._tasks[jid] = asyncio.create_task(self.run_job(jid))

    def build_prompt(self, job: dict[str, Any], payload: dict[str, Any]) -> str:
        template = self.prompt_path.read_text("utf-8")
        prompt = str(payload.get("prompt") or "").strip()
        tool_input = {
            "prompt": prompt,
            "input": payload.get("input") if isinstance(payload.get("input"), dict) else {},
            "mode": "assistant_handoff" if job.get("tool") == "assistant" else "definite_response",
            "studio_mode": str(payload.get("mode") or ""),
            "session_id": str(payload.get("session_id") or ""),
            "api_contract": {
                "job_id": job["id"],
                "tool": job["tool"],
                "output_path": job["paths"]["output"],
                "schema_path": str(self.schema_path),
            },
        }
        return (
            template
            + "\n\nInput JSON follows. Return only JSON matching the selected schema.\n\n"
            + json.dumps(tool_input, ensure_ascii=False, indent=2)
            + "\n"
        )

    def mock_result(self, job: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        prompt = str(payload.get("prompt") or "")
        return {
            "status": "answered" if job.get("tool") == "response" else "completed",
            "answer": f"Mock AutoAppDev Codex result for: {prompt[:240]}",
            "summary": "Mock response generated without calling Codex.",
            "actions": [{"label": "poll", "detail": f"Poll {job['poll_url']} for job details."}],
            "artifacts": [],
            "needs_followup": False,
            "confidence": 0.5,
        }

    async def run_job(self, job_id: str) -> dict[str, Any]:
        jid = safe_job_id(job_id)
        job_dir = self.job_dir(jid)
        payload = read_json(job_dir / "input.json", {})
        if not isinstance(payload, dict):
            payload = {}
        started = time.monotonic()
        try:
            job = self.update_job(jid, {"status": "running", "started_at": now_iso()})
            full_prompt = self.build_prompt(job, payload)
            atomic_write_text(job_dir / "prompt.txt", full_prompt)

            if self.mock or bool(payload.get("mock", False)):
                output = self.mock_result(job, payload)
                atomic_write_json(job_dir / "output.json", output)
                return self.update_job(
                    jid,
                    {
                        "status": "succeeded",
                        "finished_at": now_iso(),
                        "elapsed_seconds": round(time.monotonic() - started, 2),
                        "returncode": 0,
                    },
                )

            if not shutil.which("codex"):
                raise CodexJobError("codex_not_found", "codex executable was not found on PATH")

            cmd = [
                "codex",
                "exec",
                "--ephemeral",
                "--model",
                str(job["model"]),
                "-c",
                f'model_reasoning_effort="{job["reasoning"]}"',
                "--cd",
                str(self.repo_root),
                "--output-schema",
                str(self.schema_path),
                "--output-last-message",
                str(job_dir / "output.json"),
            ]
            if bool(job.get("allow_edits")):
                cmd.append("--dangerously-bypass-approvals-and-sandbox")
            else:
                cmd.extend(["--sandbox", "read-only"])
            cmd.append("-")

            timeout_s = float(payload.get("timeout_s") or self.default_timeout_s)
            timeout_s = max(10.0, min(timeout_s, 3600.0))
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.repo_root),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=os.environ.copy(),
            )
            try:
                out_b, err_b = await asyncio.wait_for(
                    proc.communicate(full_prompt.encode("utf-8")), timeout=timeout_s
                )
            except asyncio.TimeoutError as exc:
                try:
                    proc.kill()
                except Exception:
                    pass
                try:
                    await proc.wait()
                except Exception:
                    pass
                raise CodexJobError("timeout", f"codex exec exceeded timeout_s={timeout_s}") from exc

            atomic_write_text(job_dir / "stdout.log", out_b.decode("utf-8", errors="replace"))
            atomic_write_text(job_dir / "stderr.log", err_b.decode("utf-8", errors="replace"))
            status = "succeeded" if proc.returncode == 0 and (job_dir / "output.json").exists() else "failed"
            updates: dict[str, Any] = {
                "status": status,
                "finished_at": now_iso(),
                "elapsed_seconds": round(time.monotonic() - started, 2),
                "returncode": proc.returncode,
            }
            if status == "failed":
                updates["error"] = f"codex exec failed with returncode {proc.returncode}"
            return self.update_job(jid, updates)
        except CodexJobError as exc:
            atomic_write_text(job_dir / "stderr.log", exc.detail + "\n")
            return self.update_job(
                jid,
                {
                    "status": "failed",
                    "finished_at": now_iso(),
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                    "error": exc.code,
                    "detail": exc.detail,
                },
            )
        except Exception as exc:
            atomic_write_text(job_dir / "stderr.log", f"{type(exc).__name__}: {exc}\n")
            return self.update_job(
                jid,
                {
                    "status": "failed",
                    "finished_at": now_iso(),
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                    "error": f"{type(exc).__name__}: {exc}",
                },
            )

    async def wait_job(self, job_id: str, timeout_s: float = 120.0) -> dict[str, Any]:
        deadline = time.monotonic() + max(0.0, timeout_s)
        while True:
            job = self.read_job(job_id)
            if str(job.get("status")) in FINAL_STATUSES:
                return job
            if time.monotonic() >= deadline:
                return job
            await asyncio.sleep(0.25)

    async def respond(self, payload: dict[str, Any]) -> dict[str, Any]:
        request = dict(payload)
        request["tool"] = request.get("tool") or "response"
        request.setdefault("reasoning", self.default_reasoning_for_tool(self.normalize_tool(request["tool"])))
        wait_seconds = float(request.pop("wait_seconds", 120))
        job_payload = self.submit_job(request, start=False)
        job_id = str(job_payload["job"]["id"])
        await self.run_job(job_id)
        await self.wait_job(job_id, timeout_s=wait_seconds)
        return self.job_status(job_id, include_logs=True, include_output=True)

    def job_status(self, job_id: str, *, include_logs: bool = True, include_output: bool = True) -> dict[str, Any]:
        job = self.read_job(job_id)
        job_dir = self.job_dir(job["id"])
        payload: dict[str, Any] = {"job": job}
        if include_output and (job_dir / "output.json").exists():
            output = read_json(job_dir / "output.json")
            if output is None:
                payload["output_text"] = (job_dir / "output.json").read_text("utf-8", errors="replace")
            else:
                payload["output"] = output
        if include_logs:
            payload["logs"] = {
                "stdout_tail": tail_text(job_dir / "stdout.log"),
                "stderr_tail": tail_text(job_dir / "stderr.log"),
            }
        return payload

    def list_jobs(self, *, limit: int = 20, session_id: str | None = None) -> list[dict[str, Any]]:
        lim = max(1, min(int(limit), 200))
        sid = str(session_id or "").strip()
        jobs: list[dict[str, Any]] = []
        for path in self.jobs_root.glob("*/job.json"):
            job = read_json(path)
            if not isinstance(job, dict):
                continue
            if sid and str(job.get("session_id") or "") != sid:
                continue
            jobs.append(job)
        return sorted(jobs, key=lambda item: str(item.get("created_at") or ""), reverse=True)[:lim]
