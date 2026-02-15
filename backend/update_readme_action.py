import datetime
import difflib
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


README_BEGIN = "<!-- AUTOAPPDEV:README:BEGIN -->"
README_END = "<!-- AUTOAPPDEV:README:END -->"


class UpdateReadmeError(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(detail or code)
        self.code = str(code)
        self.detail = str(detail or "")

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"ok": False, "error": self.code}
        if self.detail:
            out["detail"] = self.detail
        return out


def make_update_id(*, workspace: str, block_markdown: str) -> str:
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    h = hashlib.sha256()
    h.update(workspace.encode("utf-8", errors="replace"))
    h.update(b"\n")
    h.update(block_markdown.encode("utf-8", errors="replace"))
    h.update(b"\n")
    h.update(os.urandom(16))
    return f"{ts}_{h.hexdigest()[:8]}"


def validate_workspace_slug(workspace: str) -> str:
    w = str(workspace or "").strip()
    if not w:
        raise UpdateReadmeError("invalid_workspace", "workspace is required")
    if w in {".", ".."}:
        raise UpdateReadmeError("invalid_workspace", "workspace must not be '.' or '..'")
    if "/" in w or "\\" in w:
        raise UpdateReadmeError("invalid_workspace", "workspace must be a single path segment")
    if len(w) > 100:
        raise UpdateReadmeError("invalid_workspace", "workspace is too long")
    # Avoid control characters; they can confuse path handling/logging.
    if any(ord(ch) < 32 for ch in w):
        raise UpdateReadmeError("invalid_workspace", "workspace contains control characters")
    return w


def validate_block_markdown(block_markdown: str) -> None:
    if not isinstance(block_markdown, str):
        raise UpdateReadmeError("invalid_block_markdown", "block_markdown must be a string")
    if not block_markdown.strip():
        raise UpdateReadmeError("invalid_block_markdown", "block_markdown is required")
    if len(block_markdown) > 200_000:
        raise UpdateReadmeError("invalid_block_markdown", "block_markdown too large")
    if README_BEGIN in block_markdown or README_END in block_markdown:
        raise UpdateReadmeError("invalid_block_markdown", "block_markdown must not contain README markers")
    if not re.search(r"(?m)^##\s+Philosophy\b", block_markdown):
        raise UpdateReadmeError("missing_philosophy", "block_markdown must include a '## Philosophy' section")


def resolve_workspace_readme_path(repo_root: Path, workspace: str) -> Path:
    repo_real = repo_root.resolve()
    auto_apps_real = (repo_real / "auto-apps").resolve()
    # Guardrail: do not follow a symlinked auto-apps/ that escapes the repo.
    if repo_real not in auto_apps_real.parents and auto_apps_real != repo_real:
        raise UpdateReadmeError("path_outside_repo", f"auto-apps/ resolves outside repo: {auto_apps_real}")
    target = (auto_apps_real / workspace / "README.md").resolve()
    if auto_apps_real not in target.parents and target != auto_apps_real:
        raise UpdateReadmeError("path_outside_auto_apps", f"target resolves outside auto-apps/: {target}")
    return target


def _find_first_h1_insert_pos(text: str) -> int | None:
    # Insert after first H1 line (recommended in docs/common-actions.md).
    m = re.search(r"(?m)^#\s+.*$", text)
    if not m:
        return None
    nl = text.find("\n", m.end())
    return len(text) if nl < 0 else nl + 1


def upsert_readme_block(
    existing_text: str | None,
    *,
    workspace: str,
    block_markdown: str,
) -> tuple[str, dict[str, Any]]:
    block = f"{README_BEGIN}\n{block_markdown.rstrip()}\n{README_END}\n"

    if existing_text is None or not str(existing_text).strip():
        base = f"# {workspace}\n\n"
        out = base + block
        if not out.endswith("\n"):
            out += "\n"
        return out, {"updated": True, "markers_preexisted": False, "mode": "create"}

    text = str(existing_text)
    begin_count = text.count(README_BEGIN)
    end_count = text.count(README_END)

    if begin_count == 0 and end_count == 0:
        pos = _find_first_h1_insert_pos(text)
        if pos is None:
            out = block + "\n" + text.lstrip()
            return out, {"updated": True, "markers_preexisted": False, "mode": "insert_top"}
        out = text[:pos].rstrip() + "\n\n" + block + "\n" + text[pos:].lstrip()
        if not out.endswith("\n"):
            out += "\n"
        return out, {"updated": True, "markers_preexisted": False, "mode": "insert_after_h1"}

    if begin_count != 1 or end_count != 1:
        raise UpdateReadmeError(
            "marker_mismatch",
            f"expected exactly one begin+end marker; got begin={begin_count} end={end_count}",
        )

    idx_begin = text.find(README_BEGIN)
    idx_end = text.find(README_END)
    if idx_begin < 0 or idx_end < 0 or idx_end < idx_begin:
        raise UpdateReadmeError("marker_mismatch", "marker order mismatch")

    pre, rest = text.split(README_BEGIN, 1)
    _mid, post = rest.split(README_END, 1)
    out = pre.rstrip() + "\n\n" + block + "\n" + post.lstrip()
    if not out.endswith("\n"):
        out += "\n"
    return out, {"updated": True, "markers_preexisted": True, "mode": "replace"}


@dataclass(frozen=True)
class UpdateArtifacts:
    dir: Path
    before: Path
    after: Path
    diff: Path
    meta: Path


def write_update_artifacts(
    runtime_dir: Path,
    update_id: str,
    *,
    before: str,
    after: str,
    meta: dict[str, Any],
) -> UpdateArtifacts:
    base = runtime_dir / "logs" / "update_readme" / update_id
    base.mkdir(parents=True, exist_ok=True)

    before_p = base / "before.md"
    after_p = base / "after.md"
    diff_p = base / "diff.txt"
    meta_p = base / "meta.json"

    before_p.write_text(before, "utf-8")
    after_p.write_text(after, "utf-8")

    diff_lines = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile="before.md",
        tofile="after.md",
    )
    diff_p.write_text("".join(diff_lines), "utf-8")

    meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", "utf-8")

    return UpdateArtifacts(dir=base, before=before_p, after=after_p, diff=diff_p, meta=meta_p)

