import os
from pathlib import Path
from typing import Any


ALLOWED_ACTION_KINDS = {"prompt", "command"}
ALLOWED_REASONING = {"low", "medium", "high", "xhigh"}


class ActionRegistryError(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(detail or code)
        self.code = str(code)
        self.detail = str(detail or "")

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"error": self.code}
        if self.detail:
            out["detail"] = self.detail
        return out


def _require_str(obj: dict[str, Any], key: str) -> str:
    v = obj.get(key)
    if not isinstance(v, str) or not v.strip():
        raise ActionRegistryError(f"invalid_{key}", f"{key} must be a non-empty string")
    return v.strip()


def _optional_bool(obj: dict[str, Any], key: str, default: bool) -> bool:
    if key not in obj:
        return default
    v = obj.get(key)
    if not isinstance(v, bool):
        raise ActionRegistryError(f"invalid_{key}", f"{key} must be a boolean")
    return bool(v)


def _optional_number(obj: dict[str, Any], key: str) -> float | None:
    if key not in obj:
        return None
    v = obj.get(key)
    if v is None:
        return None
    if not isinstance(v, (int, float)):
        raise ActionRegistryError(f"invalid_{key}", f"{key} must be a number")
    return float(v)


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(v)))


def _default_agent(cfg: dict[str, Any] | None = None) -> str:
    if isinstance(cfg, dict) and isinstance(cfg.get("agent"), str) and cfg["agent"].strip():
        return str(cfg["agent"]).strip()
    return "codex"


def _default_model(cfg: dict[str, Any] | None = None) -> str:
    if isinstance(cfg, dict) and isinstance(cfg.get("model"), str) and cfg["model"].strip():
        return str(cfg["model"]).strip()
    v = os.getenv("AUTOAPPDEV_CODEX_MODEL")
    if v and v.strip():
        return v.strip()
    return "gpt-5.3-codex"


def _default_reasoning() -> str:
    v = os.getenv("AUTOAPPDEV_CODEX_REASONING")
    if v and v.strip():
        return v.strip()
    return "medium"


def _normalize_cwd(cwd: str, *, repo_root: Path) -> str:
    c = str(cwd or "").strip() or "."
    p = Path(c)
    if p.is_absolute():
        raise ActionRegistryError("invalid_cwd", "cwd must be a repo-relative path (not absolute)")
    resolved = (repo_root / p).resolve()
    repo_real = repo_root.resolve()
    if resolved != repo_real and repo_real not in resolved.parents:
        raise ActionRegistryError("cwd_outside_repo", f"cwd resolves outside repo: {resolved}")
    try:
        rel = resolved.relative_to(repo_real)
    except Exception:
        rel = Path(".")
    return "." if str(rel) in {"", "."} else str(rel)


def normalize_action_spec(
    *,
    kind: str,
    spec_patch: dict[str, Any],
    base_spec: dict[str, Any] | None,
    repo_root: Path,
    cfg: dict[str, Any] | None,
) -> dict[str, Any]:
    k = str(kind or "").strip()
    if k not in ALLOWED_ACTION_KINDS:
        raise ActionRegistryError("invalid_kind", f"kind must be one of: {', '.join(sorted(ALLOWED_ACTION_KINDS))}")
    if not isinstance(spec_patch, dict):
        raise ActionRegistryError("invalid_spec", "spec must be an object")
    base = base_spec if isinstance(base_spec, dict) else {}

    if k == "prompt":
        allowed = {"agent", "model", "reasoning", "timeout_s", "prompt"}
        out: dict[str, Any] = {kk: base[kk] for kk in allowed if kk in base}
        for kk in allowed:
            if kk in spec_patch:
                out[kk] = spec_patch.get(kk)

        prompt = out.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ActionRegistryError("invalid_prompt", "spec.prompt must be a non-empty string")
        if len(prompt) > 200_000:
            raise ActionRegistryError("invalid_prompt", "spec.prompt too large")
        out["prompt"] = prompt

        agent = out.get("agent")
        if agent is None:
            agent = _default_agent(cfg)
        if not isinstance(agent, str) or not agent.strip():
            raise ActionRegistryError("invalid_agent", "spec.agent must be a non-empty string")
        out["agent"] = agent.strip()

        model = out.get("model")
        if model is None:
            model = _default_model(cfg)
        if not isinstance(model, str) or not model.strip():
            raise ActionRegistryError("invalid_model", "spec.model must be a non-empty string")
        out["model"] = model.strip()

        reasoning = out.get("reasoning")
        if reasoning is None:
            reasoning = _default_reasoning()
        if not isinstance(reasoning, str) or not reasoning.strip():
            raise ActionRegistryError("invalid_reasoning", "spec.reasoning must be a string")
        r = reasoning.strip()
        if r not in ALLOWED_REASONING:
            raise ActionRegistryError("invalid_reasoning", f"reasoning must be one of: {', '.join(sorted(ALLOWED_REASONING))}")
        out["reasoning"] = r

        timeout_s = out.get("timeout_s")
        if timeout_s is None:
            timeout_s = 45.0
        if not isinstance(timeout_s, (int, float)):
            raise ActionRegistryError("invalid_timeout_s", "spec.timeout_s must be a number")
        out["timeout_s"] = _clamp(float(timeout_s), 5.0, 300.0)
        return out

    # k == "command"
    allowed = {"shell", "cwd", "timeout_s", "cmd"}
    out = {kk: base[kk] for kk in allowed if kk in base}
    for kk in allowed:
        if kk in spec_patch:
            out[kk] = spec_patch.get(kk)

    cmd = out.get("cmd")
    if not isinstance(cmd, str) or not cmd.strip():
        raise ActionRegistryError("invalid_cmd", "spec.cmd must be a non-empty string")
    if len(cmd) > 20_000:
        raise ActionRegistryError("invalid_cmd", "spec.cmd too large")
    out["cmd"] = cmd

    shell = out.get("shell")
    if shell is None:
        shell = "bash"
    if not isinstance(shell, str) or not shell.strip():
        raise ActionRegistryError("invalid_shell", "spec.shell must be a non-empty string")
    sh = shell.strip()
    if sh != "bash":
        raise ActionRegistryError("invalid_shell", "only shell='bash' is supported in v0")
    out["shell"] = sh

    cwd = out.get("cwd")
    if cwd is None:
        cwd = "."
    if not isinstance(cwd, str):
        raise ActionRegistryError("invalid_cwd", "spec.cwd must be a string")
    out["cwd"] = _normalize_cwd(cwd, repo_root=repo_root)

    timeout_s = out.get("timeout_s")
    if timeout_s is None:
        timeout_s = 60.0
    if not isinstance(timeout_s, (int, float)):
        raise ActionRegistryError("invalid_timeout_s", "spec.timeout_s must be a number")
    out["timeout_s"] = _clamp(float(timeout_s), 1.0, 3600.0)
    return out


def validate_action_create(
    body: dict[str, Any],
    *,
    repo_root: Path,
    cfg: dict[str, Any] | None = None,
) -> tuple[str, str, dict[str, Any], bool]:
    if not isinstance(body, dict):
        raise ActionRegistryError("invalid_body", "body must be an object")
    title = _require_str(body, "title")
    if len(title) > 200:
        raise ActionRegistryError("invalid_title", "title is too long")
    kind = _require_str(body, "kind")
    if kind not in ALLOWED_ACTION_KINDS:
        raise ActionRegistryError("invalid_kind", f"kind must be one of: {', '.join(sorted(ALLOWED_ACTION_KINDS))}")
    spec = body.get("spec")
    if not isinstance(spec, dict):
        raise ActionRegistryError("invalid_spec", "spec must be an object")
    enabled = _optional_bool(body, "enabled", True)
    norm_spec = normalize_action_spec(kind=kind, spec_patch=spec, base_spec=None, repo_root=repo_root, cfg=cfg)
    return title, kind, norm_spec, enabled


def validate_action_update(
    body: dict[str, Any],
    *,
    repo_root: Path,
    existing: dict[str, Any],
    cfg: dict[str, Any] | None = None,
) -> tuple[str | None, dict[str, Any] | None, bool | None]:
    """Validate a partial update.

    Returns (title, spec, enabled) where each may be None if not provided.
    """
    if not isinstance(body, dict):
        raise ActionRegistryError("invalid_body", "body must be an object")
    if not any(k in body for k in ("title", "spec", "enabled", "kind")):
        raise ActionRegistryError("no_fields", "no updatable fields provided")

    if "kind" in body:
        k = body.get("kind")
        if not isinstance(k, str) or not k.strip():
            raise ActionRegistryError("invalid_kind", "kind must be a non-empty string")
        cur_kind = str(existing.get("kind") or "")
        if k.strip() != cur_kind:
            raise ActionRegistryError("kind_change_not_allowed", "changing kind is not supported in v0")

    title: str | None = None
    if "title" in body:
        t = body.get("title")
        if t is None:
            title = ""
        elif not isinstance(t, str):
            raise ActionRegistryError("invalid_title", "title must be a string")
        else:
            title = t.strip()
        if not title:
            raise ActionRegistryError("invalid_title", "title must be a non-empty string")
        if len(title) > 200:
            raise ActionRegistryError("invalid_title", "title is too long")

    enabled: bool | None = None
    if "enabled" in body:
        v = body.get("enabled")
        if not isinstance(v, bool):
            raise ActionRegistryError("invalid_enabled", "enabled must be a boolean")
        enabled = bool(v)

    spec: dict[str, Any] | None = None
    if "spec" in body:
        patch = body.get("spec")
        if not isinstance(patch, dict):
            raise ActionRegistryError("invalid_spec", "spec must be an object")
        kind = str(existing.get("kind") or "")
        base = existing.get("spec") if isinstance(existing.get("spec"), dict) else {}
        spec = normalize_action_spec(kind=kind, spec_patch=patch, base_spec=base, repo_root=repo_root, cfg=cfg)

    return title, spec, enabled

