# Summary: 033 backend_update_readme_action

## What Changed
- Implemented the `update_readme` backend execution endpoint:
  - New helpers in `backend/update_readme_action.py` for workspace slug validation, safe path resolution under `auto-apps/`, marker-based README upsert, and runtime artifact writing (before/after/diff/meta).
  - New Tornado handler + route in `backend/app.py`: `POST /api/actions/update-readme` which writes the README atomically and logs artifacts under `AUTOAPPDEV_RUNTIME_DIR/logs/update_readme/<id>/`.
- Documented the endpoint in `docs/api-contracts.md`.

## Why
To safely execute the common `ACTION.kind="update_readme"` contract from `docs/common-actions.md` without permitting arbitrary filesystem writes, while keeping changes auditable via runtime artifacts.

## How To Verify (Smallest Smoke)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/update_readme_action.py

timeout 10s python3 - <<'PY'
from pathlib import Path
import tempfile

from backend.update_readme_action import (
    README_BEGIN,
    README_END,
    UpdateReadmeError,
    resolve_workspace_readme_path,
    upsert_readme_block,
    validate_block_markdown,
    validate_workspace_slug,
)

assert validate_workspace_slug("ok_slug") == "ok_slug"
try:
    validate_workspace_slug("a/b")
    raise AssertionError("expected invalid_workspace")
except UpdateReadmeError:
    pass

validate_block_markdown("## Philosophy\ntext\n")

with tempfile.TemporaryDirectory() as td:
    repo_root = Path(td) / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    (repo_root / "auto-apps").mkdir(parents=True, exist_ok=True)
    p = resolve_workspace_readme_path(repo_root, "ws1")
    assert str(p).endswith("/auto-apps/ws1/README.md")

before = "# Title\n\nUser intro.\n"
after, _ = upsert_readme_block(before, workspace="ws1", block_markdown="## Philosophy\nX\n")
assert README_BEGIN in after and README_END in after
print("ok")
PY

timeout 10s rg -n "/api/actions/update-readme" backend/app.py docs/api-contracts.md
```

