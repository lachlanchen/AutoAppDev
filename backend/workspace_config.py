from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .update_readme_action import UpdateReadmeError, validate_workspace_slug


ALLOWED_LANGUAGES = {"zh-Hans", "zh-Hant", "en", "ja", "ko", "vi", "ar", "fr", "es"}


@dataclass
class WorkspaceConfigError(Exception):
    code: str
    detail: str = ""

    def __str__(self) -> str:  # pragma: no cover
        return self.detail or self.code

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"error": str(self.code)}
        if self.detail:
            out["detail"] = str(self.detail)
        return out


def validate_workspace(workspace: str) -> str:
    try:
        return validate_workspace_slug(workspace)
    except UpdateReadmeError as e:
        raise WorkspaceConfigError(e.code, e.detail) from e


def resolve_workspace_root(repo_root: Path, workspace: str) -> Path:
    """Return the safe workspace root path under auto-apps/<workspace>/ (resolved)."""
    repo_real = repo_root.resolve()
    auto_apps_real = (repo_real / "auto-apps").resolve()
    # Guardrail: do not follow a symlinked auto-apps/ that escapes the repo.
    if repo_real not in auto_apps_real.parents and auto_apps_real != repo_real:
        raise WorkspaceConfigError("path_outside_repo", f"auto-apps/ resolves outside repo: {auto_apps_real}")
    target = (auto_apps_real / workspace).resolve()
    if auto_apps_real not in target.parents and target != auto_apps_real:
        raise WorkspaceConfigError("path_outside_auto_apps", f"workspace resolves outside auto-apps/: {target}")
    return target


def _normalize_rel_path(workspace_root: Path, raw: str, *, field: str) -> str:
    s = str(raw or "").strip()
    if not s:
        raise WorkspaceConfigError(f"invalid_{field}", f"{field} must be a non-empty string")
    p = Path(s)
    if p.is_absolute():
        raise WorkspaceConfigError(f"invalid_{field}", f"{field} must be workspace-relative (not absolute)")
    resolved = (workspace_root / p).resolve()
    root_real = workspace_root.resolve()
    if resolved != root_real and root_real not in resolved.parents:
        raise WorkspaceConfigError("path_outside_workspace", f"{field} resolves outside workspace: {resolved}")
    try:
        rel = resolved.relative_to(root_real)
    except Exception:
        rel = Path(".")
    return "." if str(rel) in {"", "."} else str(rel)


def default_workspace_config() -> dict[str, Any]:
    return {
        "materials_paths": ["materials"],
        "default_language": "en",
        "shared_context_text": "",
        "shared_context_path": "",
    }


def normalize_workspace_config(
    body: dict[str, Any],
    *,
    repo_root: Path,
    workspace: str,
    base: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(body, dict):
        raise WorkspaceConfigError("invalid_body", "body must be an object")

    ws = validate_workspace(workspace)
    ws_root = resolve_workspace_root(repo_root, ws)

    # Merge base -> defaults -> patch.
    cur = base if isinstance(base, dict) else {}
    merged: dict[str, Any] = {**default_workspace_config(), **cur, **body}

    # default_language
    lang = merged.get("default_language")
    if lang is None:
        lang = "en"
    if not isinstance(lang, str) or not lang.strip():
        raise WorkspaceConfigError("invalid_default_language", "default_language must be a non-empty string")
    l = lang.strip()
    if l not in ALLOWED_LANGUAGES:
        raise WorkspaceConfigError(
            "invalid_default_language",
            f"default_language must be one of: {', '.join(sorted(ALLOWED_LANGUAGES))}",
        )

    # shared_context_text
    sct = merged.get("shared_context_text")
    if sct is None:
        sct = ""
    if not isinstance(sct, str):
        raise WorkspaceConfigError("invalid_shared_context_text", "shared_context_text must be a string")
    if len(sct) > 200_000:
        raise WorkspaceConfigError("invalid_shared_context_text", "shared_context_text too large")

    # shared_context_path (optional)
    scp = merged.get("shared_context_path")
    if scp is None:
        scp = ""
    if not isinstance(scp, str):
        raise WorkspaceConfigError("invalid_shared_context_path", "shared_context_path must be a string")
    scp_norm = ""
    if scp.strip():
        scp_norm = _normalize_rel_path(ws_root, scp, field="shared_context_path")

    # materials_paths (list)
    mp = merged.get("materials_paths")
    if mp is None:
        mp = ["materials"]
    if not isinstance(mp, list):
        raise WorkspaceConfigError("invalid_materials_paths", "materials_paths must be a list of strings")
    if not (1 <= len(mp) <= 20):
        raise WorkspaceConfigError("invalid_materials_paths", "materials_paths must have 1..20 entries")
    out_paths: list[str] = []
    for it in mp:
        if not isinstance(it, str):
            raise WorkspaceConfigError("invalid_materials_path", "materials_paths entries must be strings")
        norm = _normalize_rel_path(ws_root, it, field="materials_path")
        out_paths.append(norm)

    return {
        "materials_paths": out_paths,
        "shared_context_text": sct,
        "shared_context_path": scp_norm,
        "default_language": l,
    }

