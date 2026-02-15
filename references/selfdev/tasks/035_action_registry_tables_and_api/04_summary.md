# Summary: 035 action_registry_tables_and_api

## What Changed
- Added an action registry table:
  - `backend/schema.sql`: new `action_definitions` table + `action_definitions_updated_at_idx`.
- Implemented storage + validation for action definitions:
  - `backend/storage.py`: CRUD methods for action definitions.
  - `backend/action_registry.py`: validates/normalizes `kind="prompt|command"` specs with safe defaults and path guardrails for command `cwd`.
- Exposed minimal CRUD HTTP API:
  - `backend/app.py`: `GET/POST /api/actions` and `GET/PUT/DELETE /api/actions/<id>`.
  - Kept executor endpoint `POST /api/actions/update-readme` unchanged.
- Documented the registry endpoints:
  - `docs/api-contracts.md`: new “Actions” subsections for the registry endpoints and a note distinguishing registry vs executor endpoints.

## Why
To make actions first-class, reusable, and editable via a stable backend contract, while enforcing safe defaults and preventing unsafe path settings for command-based actions.

## How To Verify (Smallest Smoke)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/action_registry.py

timeout 10s python3 - <<'PY'
from pathlib import Path
import tempfile
from backend.action_registry import ActionRegistryError, validate_action_create

with tempfile.TemporaryDirectory() as td:
  repo = Path(td) / "repo"
  repo.mkdir(parents=True, exist_ok=True)
  (repo / "backend").mkdir(parents=True, exist_ok=True)
  title, kind, spec, enabled = validate_action_create(
    {"title":"T","kind":"command","spec":{"cmd":"echo hi"}},
    repo_root=repo,
    cfg={},
  )
  assert kind == "command" and spec["shell"] == "bash" and spec["cwd"] == "."
  try:
    validate_action_create({"title":"T","kind":"command","spec":{"cmd":"x","cwd":"/etc"}}, repo_root=repo, cfg={})
    raise AssertionError("expected invalid_cwd")
  except ActionRegistryError:
    pass
print("ok")
PY

timeout 10s rg -n "/api/actions\\b" backend/app.py docs/api-contracts.md
```

