import datetime
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from .codex_api import atomic_write_json, atomic_write_text, now_iso
from .pipeline_parser import ParseError, parse_aaps_v1


def extract_aaps_artifacts(output: dict[str, Any] | None) -> list[dict[str, str]]:
    if not isinstance(output, dict):
        return []
    out: list[dict[str, str]] = []
    artifacts = output.get("artifacts")
    if isinstance(artifacts, list):
        for item in artifacts:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "artifact.aaps")
            kind = str(item.get("kind") or "").lower()
            content = item.get("content")
            if not isinstance(content, str) or not content.strip():
                continue
            if kind == "aaps" or name.lower().endswith(".aaps"):
                out.append({"name": name, "content": content})
    for key in ("aaps_script", "script_text"):
        content = output.get(key)
        if isinstance(content, str) and content.strip().startswith("AUTOAPPDEV_PIPELINE 1"):
            out.append({"name": f"{key}.aaps", "content": content})
    return out


class AutopilotStore:
    """Strict, recoverable storage for AutoPilot AAPS edits."""

    def __init__(self, *, repo_root: Path, base_dir: Path):
        self.repo_root = repo_root.resolve()
        self.base_dir = base_dir.resolve()
        self.history_dir = self.base_dir / "history"
        self.accepted_path = self.base_dir / "accepted.aaps"
        self.proposed_path = self.base_dir / "proposed.aaps"
        self.validation_path = self.base_dir / "validation.json"
        self.ledger_path = self.base_dir / "edits.jsonl"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def revision_id(self, label: str = "edit") -> str:
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        safe = re.sub(r"[^a-zA-Z0-9_.-]+", "-", label).strip(".-")[:40] or "edit"
        return f"{ts}-{safe}"

    def default_script(self) -> str:
        return (
            "AUTOAPPDEV_PIPELINE 1\n"
            "\n"
            "TASK {\"id\":\"meta\",\"title\":\"Default AutoAppDev loop\",\"meta\":{\"meta_round_v0\":{\"n_round\":2,\"goal\":\"Plan, implement, verify, summarize, and preserve recoverable versions.\",\"task_list_path\":\"references/meta_round/tasks_v0.json\",\"task_limit\":10,\"language\":\"en\"}}}\n"
            "STEP {\"id\":\"s1\",\"title\":\"Plan the next safe change\",\"block\":\"plan\"}\n"
            "ACTION {\"id\":\"a1\",\"kind\":\"codex_exec\",\"params\":{\"prompt\":\"Read project context, produce a small task list, and keep every change recoverable.\"}}\n"
            "STEP {\"id\":\"s2\",\"title\":\"Implement the smallest useful change\",\"block\":\"work\"}\n"
            "ACTION {\"id\":\"a1\",\"kind\":\"codex_exec\",\"params\":{\"prompt\":\"Implement one bounded change set.\"}}\n"
            "STEP {\"id\":\"s3\",\"title\":\"Verify with bounded commands\",\"block\":\"debug\"}\n"
            "ACTION {\"id\":\"a1\",\"kind\":\"run\",\"params\":{\"cmd\":\"timeout 30s python3 -m py_compile backend/app.py\"}}\n"
            "STEP {\"id\":\"s4\",\"title\":\"Fix only if verification fails\",\"block\":\"fix\",\"meta\":{\"conditional\":\"on_debug_failure\"}}\n"
            "ACTION {\"id\":\"a1\",\"kind\":\"codex_exec\",\"params\":{\"prompt\":\"Apply minimal fixes, then rerun verification.\"}}\n"
            "STEP {\"id\":\"s5\",\"title\":\"Summarize and record recovery notes\",\"block\":\"summary\"}\n"
            "ACTION {\"id\":\"a1\",\"kind\":\"note\",\"params\":{\"text\":\"Summarize changes, tests, and rollback path.\"}}\n"
            "STEP {\"id\":\"s6\",\"title\":\"Commit when policy allows\",\"block\":\"commit_push\"}\n"
            "ACTION {\"id\":\"a1\",\"kind\":\"note\",\"params\":{\"text\":\"Commit/push is explicit and policy-driven; never hide schema changes.\"}}\n"
        )

    def ensure_default(self) -> None:
        if not self.accepted_path.exists():
            atomic_write_text(self.accepted_path, self.default_script())
            validation = self.validate(self.accepted_path.read_text("utf-8"))
            atomic_write_json(self.validation_path, {"accepted": validation, "created_at": now_iso()})

    def validate(self, script_text: str) -> dict[str, Any]:
        try:
            ir = parse_aaps_v1(script_text)
        except ParseError as exc:
            return exc.to_dict()
        return {"ok": True, "ir": ir}

    def _append_ledger(self, record: dict[str, Any]) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    def _git_status(self) -> list[str]:
        try:
            proc = subprocess.run(
                ["git", "status", "--short", "--", str(self.base_dir.relative_to(self.repo_root))],
                cwd=str(self.repo_root),
                text=True,
                capture_output=True,
                timeout=5,
                check=False,
            )
        except Exception:
            return []
        return [line for line in proc.stdout.splitlines() if line.strip()]

    def _maybe_autocommit(self, message: str) -> dict[str, Any] | None:
        if os.environ.get("AUTOAPPDEV_AUTOPILOT_AUTOCOMMIT", "0").strip() != "1":
            return None
        rel = str(self.base_dir.relative_to(self.repo_root))
        try:
            add = subprocess.run(["git", "add", rel], cwd=self.repo_root, text=True, capture_output=True, timeout=20)
            commit = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_root,
                text=True,
                capture_output=True,
                timeout=60,
            )
        except Exception as exc:
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        return {
            "ok": add.returncode == 0 and commit.returncode == 0,
            "add_returncode": add.returncode,
            "commit_returncode": commit.returncode,
            "stdout": (add.stdout or "") + (commit.stdout or ""),
            "stderr": (add.stderr or "") + (commit.stderr or ""),
        }

    def propose(self, script_text: str, *, source: str = "manual", job_id: str = "", chat_session_id: str = "") -> dict[str, Any]:
        text = str(script_text or "").replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"
        if len(text) > 250_000:
            return {"ok": False, "error": "script_too_large", "detail": "AAPS script exceeds 250000 characters"}
        validation = self.validate(text)
        rev = self.revision_id("proposed" if validation.get("ok") else "rejected")
        history_path = self.history_dir / f"{rev}.aaps"
        atomic_write_text(history_path, text)
        record = {
            "revision": rev,
            "kind": "propose",
            "source": source,
            "job_id": job_id,
            "chat_session_id": chat_session_id,
            "created_at": now_iso(),
            "ok": bool(validation.get("ok")),
            "history_path": str(history_path.relative_to(self.repo_root)),
            "validation": validation,
        }
        if validation.get("ok"):
            atomic_write_text(self.proposed_path, text)
            atomic_write_json(self.validation_path, record)
        self._append_ledger(record)
        return {
            **record,
            "paths": self.paths(),
            "git_status": self._git_status(),
            "suggested_git_commands": self.suggested_git_commands(),
        }

    def accept(self, *, source: str = "manual") -> dict[str, Any]:
        self.ensure_default()
        if not self.proposed_path.exists():
            return {"ok": False, "error": "missing_proposed", "detail": "No proposed AAPS script exists"}
        proposed = self.proposed_path.read_text("utf-8")
        validation = self.validate(proposed)
        if not validation.get("ok"):
            return {"ok": False, "error": "invalid_proposed", "validation": validation}
        rev = self.revision_id("accepted")
        if self.accepted_path.exists():
            atomic_write_text(self.history_dir / f"{rev}.previous.aaps", self.accepted_path.read_text("utf-8"))
        atomic_write_text(self.history_dir / f"{rev}.accepted.aaps", proposed)
        atomic_write_text(self.accepted_path, proposed)
        record = {
            "revision": rev,
            "kind": "accept",
            "source": source,
            "created_at": now_iso(),
            "ok": True,
            "validation": validation,
        }
        atomic_write_json(self.validation_path, record)
        self._append_ledger(record)
        git_commit = self._maybe_autocommit(f"Accept AutoPilot loop {rev}")
        return {
            **record,
            "paths": self.paths(),
            "git_status": self._git_status(),
            "git_commit": git_commit,
            "suggested_git_commands": self.suggested_git_commands(),
        }

    def restore(self, revision_file: str) -> dict[str, Any]:
        name = str(revision_file or "").strip()
        if not name.endswith(".aaps") or "/" in name or "\\" in name:
            return {"ok": False, "error": "invalid_revision_file"}
        target = (self.history_dir / name).resolve()
        if self.history_dir not in target.parents or not target.exists():
            return {"ok": False, "error": "not_found"}
        return self.propose(target.read_text("utf-8"), source=f"restore:{name}")

    def paths(self) -> dict[str, str]:
        return {
            "base_dir": str(self.base_dir.relative_to(self.repo_root)),
            "accepted": str(self.accepted_path.relative_to(self.repo_root)),
            "proposed": str(self.proposed_path.relative_to(self.repo_root)),
            "validation": str(self.validation_path.relative_to(self.repo_root)),
            "ledger": str(self.ledger_path.relative_to(self.repo_root)),
        }

    def suggested_git_commands(self) -> list[str]:
        rel = str(self.base_dir.relative_to(self.repo_root))
        return [
            f"git add {rel}",
            "git commit -m \"Update AutoPilot loop schema\"",
            "git push",
        ]

    def history(self, limit: int = 20) -> list[dict[str, Any]]:
        items = sorted(self.history_dir.glob("*.aaps"), key=lambda p: p.name, reverse=True)
        out: list[dict[str, Any]] = []
        for p in items[: max(1, min(limit, 100))]:
            out.append({"name": p.name, "path": str(p.relative_to(self.repo_root)), "size": p.stat().st_size})
        return out

    def preview(self) -> dict[str, Any]:
        self.ensure_default()
        accepted = self.accepted_path.read_text("utf-8") if self.accepted_path.exists() else ""
        proposed = self.proposed_path.read_text("utf-8") if self.proposed_path.exists() else ""
        validation = {}
        if self.validation_path.exists():
            try:
                validation = json.loads(self.validation_path.read_text("utf-8"))
            except Exception:
                validation = {}
        return {
            "ok": True,
            "accepted": accepted,
            "proposed": proposed,
            "validation": validation,
            "paths": self.paths(),
            "history": self.history(),
            "git_status": self._git_status(),
            "suggested_git_commands": self.suggested_git_commands(),
        }
