# Debug Notes: 035 action_registry_tables_and_api

## Verification (Smallest Smoke)
- Static compile of backend modules changed in this task.
- Pure-function smoke test for action payload validation/normalization:
  - prompt actions get safe defaults and clamp timeout
  - command actions default to `shell="bash"` + `cwd="."` and reject unsafe `cwd` values
  - updates merge `spec` patches and reject kind changes
- Grep check confirming schema/storage/routes/docs reference the new registry.

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/action_registry.py && echo "py_compile_ok"
# -> py_compile_ok

timeout 10s python3 - <<'PY'
from pathlib import Path
import tempfile

from backend.action_registry import ActionRegistryError, validate_action_create, validate_action_update

with tempfile.TemporaryDirectory() as td:
    repo = Path(td) / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    (repo / "backend").mkdir(parents=True, exist_ok=True)

    # create prompt (minimal)
    title, kind, spec, enabled = validate_action_create(
        {"title": "T", "kind": "prompt", "spec": {"prompt": "hello"}},
        repo_root=repo,
        cfg={"agent": "codex", "model": "gpt-5.3-codex"},
    )
    assert kind == "prompt" and enabled is True
    assert spec["prompt"] == "hello"
    assert spec["agent"] == "codex"
    assert spec["model"]
    assert spec["reasoning"]
    assert 5 <= float(spec["timeout_s"]) <= 300

    # create prompt invalid reasoning
    try:
        validate_action_create(
            {"title": "T", "kind": "prompt", "spec": {"prompt": "x", "reasoning": "nope"}},
            repo_root=repo,
            cfg={},
        )
        raise AssertionError("expected invalid_reasoning")
    except ActionRegistryError as e:
        assert e.code == "invalid_reasoning"

    # create command (minimal)
    title, kind, spec, enabled = validate_action_create(
        {"title": "C", "kind": "command", "spec": {"cmd": "echo hi"}},
        repo_root=repo,
        cfg={},
    )
    assert kind == "command"
    assert spec["cmd"] == "echo hi"
    assert spec["shell"] == "bash"
    assert spec["cwd"] == "."
    assert 1 <= float(spec["timeout_s"]) <= 3600

    # command: reject non-bash shell
    try:
        validate_action_create(
            {"title": "C", "kind": "command", "spec": {"cmd": "echo hi", "shell": "sh"}},
            repo_root=repo,
            cfg={},
        )
        raise AssertionError("expected invalid_shell")
    except ActionRegistryError as e:
        assert e.code == "invalid_shell"

    # command: reject absolute cwd
    try:
        validate_action_create(
            {"title": "C", "kind": "command", "spec": {"cmd": "echo hi", "cwd": "/etc"}},
            repo_root=repo,
            cfg={},
        )
        raise AssertionError("expected invalid_cwd")
    except ActionRegistryError as e:
        assert e.code == "invalid_cwd"

    # command: reject traversal out of repo
    try:
        validate_action_create(
            {"title": "C", "kind": "command", "spec": {"cmd": "echo hi", "cwd": ".."}},
            repo_root=repo,
            cfg={},
        )
        raise AssertionError("expected cwd_outside_repo")
    except ActionRegistryError as e:
        assert e.code == "cwd_outside_repo"

    # update merges spec patches
    existing = {
        "id": 1,
        "title": "Old",
        "kind": "prompt",
        "enabled": True,
        "spec": {"prompt": "p", "agent": "codex", "model": "m", "reasoning": "medium", "timeout_s": 45},
    }
    t2, s2, en2 = validate_action_update({"spec": {"reasoning": "high"}}, repo_root=repo, existing=existing, cfg={})
    assert t2 is None and en2 is None
    assert s2["prompt"] == "p" and s2["reasoning"] == "high"

    # update: kind change rejected
    try:
        validate_action_update({"kind": "command", "enabled": False}, repo_root=repo, existing=existing, cfg={})
        raise AssertionError("expected kind_change_not_allowed")
    except ActionRegistryError as e:
        assert e.code == "kind_change_not_allowed"

print("ok")
PY
# -> ok

timeout 10s rg -n "action_definitions|/api/actions\\b|validate_action_" backend/schema.sql backend/storage.py backend/app.py docs/api-contracts.md
# -> shows schema table/index, storage CRUD, routes, and docs sections
```

## Issues Found
- None in these smoke checks.

