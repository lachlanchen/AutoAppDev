import asyncio
import datetime
import hashlib
import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_CODE_FENCE_RE = re.compile(r"^\s*```")


@dataclass
class LlmParseError(Exception):
    code: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {"ok": False, "error": self.code, "detail": str(self.detail)}


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def make_request_id(*, source_text: str) -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{ts}_{_sha256_text(source_text)[:8]}"


def build_prompt(*, source_text: str, source_format: str = "unknown") -> str:
    # Guardrails: do not run tools/commands; output only deterministic AAPS text.
    return (
        "You are a deterministic converter.\n"
        "Convert the input into AutoAppDev formatted pipeline script (AAPS v1).\n"
        "\n"
        "Hard rules:\n"
        "- Do NOT run shell commands.\n"
        "- Do NOT read or write any files.\n"
        "- Output ONLY the AAPS v1 text (no markdown, no code fences, no commentary).\n"
        "- The first non-comment line MUST be: AUTOAPPDEV_PIPELINE 1\n"
        "- Use only these STEP.block values: plan, work, debug, fix, summary, commit_push\n"
        "- Prefer ACTION.kind=\"note\" with params.text summarizing what would happen.\n"
        "- Use stable ids: task id \"t1\"; step ids \"s1\", \"s2\"...; action ids \"a1\".\n"
        "- Keep it minimal and safe: do not invent destructive commands.\n"
        "\n"
        f"Input format hint: {source_format}\n"
        "\n"
        "INPUT BEGIN\n"
        f"{source_text}\n"
        "INPUT END\n"
    )


def extract_aaps(text: str) -> tuple[str, list[str]]:
    """Extract an AAPS v1 script from arbitrary text.

    Returns (script_text, warnings). Raises LlmParseError on failure.
    """

    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    t = text.replace("\r\n", "\n").replace("\r", "\n")

    warnings: list[str] = []
    lines = t.split("\n")

    # Strip code fences if present; keep inner content.
    filtered: list[str] = []
    removed_fences = False
    for ln in lines:
        if _CODE_FENCE_RE.match(ln):
            removed_fences = True
            continue
        filtered.append(ln)
    if removed_fences:
        warnings.append("stripped_code_fences")

    for i, ln in enumerate(filtered):
        if ln.strip() == "AUTOAPPDEV_PIPELINE 1":
            out = "\n".join(filtered[i:]).strip() + "\n"
            return out, warnings

    raise LlmParseError("missing_aaps_header", "expected AAPS header: AUTOAPPDEV_PIPELINE 1")


def _extract_last_agent_text(jsonl_text: str) -> str:
    last = ""
    for raw in jsonl_text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        item = obj.get("item")
        if isinstance(item, dict):
            t = item.get("type")
            txt = item.get("text")
            if t in ("agent_message", "assistant_message") and isinstance(txt, str) and txt:
                last = txt
                continue
        t2 = obj.get("type")
        txt2 = obj.get("text")
        if t2 in ("agent_message", "assistant_message") and isinstance(txt2, str) and txt2:
            last = txt2
            continue
    return last


async def run_codex_to_jsonl(
    *,
    prompt: str,
    model: str,
    reasoning: str,
    timeout_s: float,
    cwd: Path,
    skip_git_check: bool = False,
) -> tuple[str, str, str, int]:
    """Run Codex non-interactively and return (assistant_text, jsonl_text, stderr_text, exit_code)."""

    if not shutil.which("codex"):
        raise LlmParseError("codex_not_found", "codex not found on PATH")

    cmd = [
        "codex",
        "exec",
        "--json",
        "-m",
        str(model),
        "-c",
        f'model_reasoning_effort="{reasoning}"',
    ]
    if skip_git_check:
        cmd.append("--skip-git-repo-check")
    cmd.append("-")

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=str(cwd),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=os.environ.copy(),
    )

    try:
        out_b, err_b = await asyncio.wait_for(proc.communicate(prompt.encode("utf-8")), timeout=timeout_s)
    except asyncio.TimeoutError as e:
        try:
            proc.kill()
        except Exception:
            pass
        try:
            await proc.wait()
        except Exception:
            pass
        raise LlmParseError("timeout", f"codex exec exceeded timeout_s={timeout_s}") from e

    jsonl_text = out_b.decode("utf-8", errors="replace")
    stderr_text = err_b.decode("utf-8", errors="replace")
    rc = int(proc.returncode or 0)

    assistant_text = _extract_last_agent_text(jsonl_text) or ""
    return assistant_text, jsonl_text, stderr_text, rc


def write_artifacts(
    *,
    artifacts_dir: Path,
    source_text: str,
    prompt: str,
    codex_jsonl: str,
    assistant_text: str,
    script_text: str | None,
    provenance: dict[str, Any],
    codex_stderr: str = "",
) -> dict[str, str]:
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    source_path = artifacts_dir / "source.txt"
    prompt_path = artifacts_dir / "prompt.txt"
    jsonl_path = artifacts_dir / "codex.jsonl"
    stderr_path = artifacts_dir / "codex.stderr.log"
    assistant_path = artifacts_dir / "assistant.txt"
    aaps_path = artifacts_dir / "result.aaps"
    prov_path = artifacts_dir / "provenance.json"

    source_path.write_text(source_text, "utf-8")
    prompt_path.write_text(prompt, "utf-8")
    jsonl_path.write_text(codex_jsonl, "utf-8")
    stderr_path.write_text(codex_stderr or "", "utf-8")
    assistant_path.write_text(assistant_text, "utf-8")
    if script_text is not None:
        aaps_path.write_text(script_text, "utf-8")
    prov_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", "utf-8")

    return {
        "dir": str(artifacts_dir),
        "source": str(source_path),
        "prompt": str(prompt_path),
        "codex_jsonl": str(jsonl_path),
        "codex_stderr": str(stderr_path),
        "assistant": str(assistant_path),
        "aaps": str(aaps_path),
        "provenance": str(prov_path),
    }
