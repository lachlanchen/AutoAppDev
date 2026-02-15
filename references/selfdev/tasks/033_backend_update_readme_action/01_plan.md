# Plan: 033 backend_update_readme_action

## Goal
Implement a backend endpoint that executes the common `ACTION.kind="update_readme"` contract by safely upserting a workspace `README.md` block between fixed markers under `auto-apps/`.

Acceptance:
- Backend exposes a **safe** endpoint that patches a workspace README between markers
- Rejects path traversal / any resolved path outside `auto-apps/`
- Logs the change (writes artifacts under runtime logs and/or emits a backend log line)

## Current State (References)
- Action contract/spec (markers + safe target path + required `block_markdown` + Philosophy requirement):
  - `docs/common-actions.md` (`## update_readme`)
- Backend routing patterns + path safety example:
  - `backend/app.py` (Tornado handlers; `REPO_ROOT`; `PipelineStartHandler` path validation)
- Existing marker-based README patching example (controller README status block):
  - `scripts/auto-autoappdev-development.sh` (`update_readme_autogen`)
- Runtime log/artifact pattern to follow:
  - `backend/llm_assisted_parse.py` (writes artifacts under `AUTOAPPDEV_RUNTIME_DIR/logs/...`)
  - `backend/app.py` (`_compute_paths()` creates `runtime/logs/`)

## API Design (Minimal)
Add a single endpoint (no general “action runner” yet):
- `POST /api/actions/update-readme`

Request JSON:
```json
{
  "workspace": "my_workspace",
  "block_markdown": "## Workspace Status...\\n\\n## Philosophy\\n..."
}
```

Response JSON (success):
```json
{
  "ok": true,
  "workspace": "my_workspace",
  "path": "auto-apps/my_workspace/README.md",
  "updated": true,
  "markers_preexisted": false,
  "artifacts": { "dir": "runtime/logs/update_readme/<id>" }
}
```

Errors (non-exhaustive; 400 unless noted):
- `invalid_json`
- `invalid_body`
- `invalid_workspace` (empty, contains `/` or `\\`, `.`/`..`, etc.)
- `invalid_block_markdown` (empty, too large, contains markers, etc.)
- `missing_philosophy` (no `## Philosophy` heading)
- `marker_mismatch` (begin without end, end without begin, end before begin)
- `path_outside_auto_apps` (resolved path check fails; 403/400)

## Implementation Steps (Next Phase: WORK)
1. Implement the patching + validation helpers (new module)
   - Add `backend/update_readme_action.py`:
     - Constants for markers (must match `docs/common-actions.md`):
       - `README_BEGIN = "<!-- AUTOAPPDEV:README:BEGIN -->"`
       - `README_END = "<!-- AUTOAPPDEV:README:END -->"`
     - `validate_workspace_slug(workspace: str) -> str`
       - Must be non-empty, single path segment (no `/` or `\\`), and not `.` / `..`.
       - Optionally clamp length (e.g. <= 100) to prevent abuse.
     - `resolve_workspace_readme_path(repo_root: Path, workspace: str) -> Path`
       - Compute `auto_apps_root = (repo_root / "auto-apps").resolve()`
       - Resolve target and reject if the resolved README path is not under `auto_apps_root`
         - This should also protect against `auto-apps/<workspace>` being a symlink to outside the repo.
     - `validate_block_markdown(block_markdown: str) -> None`
       - Must be non-empty and include `^## Philosophy\\b` (multiline).
       - Must NOT contain `README_BEGIN` or `README_END` to avoid marker injection.
       - Clamp max length (e.g. 200k) to prevent huge writes.
     - `upsert_readme_block(existing_text: str | None, *, workspace: str, block_markdown: str) -> tuple[str, dict]`
       - Build the full marker block:
         - `README_BEGIN + "\\n" + block_markdown.rstrip() + "\\n" + README_END + "\\n"`
       - If both markers exist exactly once and ordered: replace the owned region.
       - If no markers: insert after the first H1 line (`^# `) if present, else insert at the top.
       - If file missing: create a minimal heading (deterministic; e.g. `# <workspace>`) and insert marker block.
       - If marker mismatch: raise a typed error (so handler returns `marker_mismatch`).
     - `write_update_artifacts(runtime_dir: Path, update_id: str, *, before: str, after: str, meta: dict) -> dict`
       - Create `runtime_dir/logs/update_readme/<update_id>/`
       - Write `before.md`, `after.md`, `diff.txt` (stdlib `difflib.unified_diff`), and `meta.json`.

2. Add the Tornado handler + route
   - Update `backend/app.py`:
     - Import helpers from `backend/update_readme_action.py`.
     - Add `UpdateReadmeHandler(BaseHandler)`:
       - `initialize(runtime_dir: Path)` for artifact logging.
       - `post()`:
         - Parse JSON with `try/except` for `invalid_json`.
         - Validate `workspace`, `block_markdown`.
         - Compute target path via `resolve_workspace_readme_path(REPO_ROOT, workspace)`.
         - `mkdir(parents=True, exist_ok=True)` for `auto-apps/<workspace>/`.
         - Read existing README (if any), compute new text via `upsert_readme_block`.
         - Write atomically (tmp + replace) to avoid partial writes.
         - Write artifacts under `runtime/logs/update_readme/<id>/` and emit a single `print(...)` log line summarizing change.
         - Return JSON including relative path and artifact dir.
     - Add route in `make_app(...)`:
       - `(r"/api/actions/update-readme", UpdateReadmeHandler, {"runtime_dir": runtime_dir})`

3. Document the endpoint
   - Update `docs/api-contracts.md`:
     - Add a new section `## Actions` (or similar) documenting:
       - `POST /api/actions/update-readme` request/response
       - Safety rules and markers (reference `docs/common-actions.md`)
       - Error codes

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Static checks
timeout 10s python3 -m py_compile backend/app.py backend/update_readme_action.py

# Pure-function smoke tests (no server, no DB)
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.update_readme_action import (
  README_BEGIN, README_END,
  validate_workspace_slug, validate_block_markdown,
  resolve_workspace_readme_path, upsert_readme_block,
)

repo_root = Path("/tmp/autoappdev_repo_root")

assert validate_workspace_slug("ok_slug") == "ok_slug"
for bad in ["", ".", "..", "../x", "a/b", "a\\\\b"]:
  try:
    validate_workspace_slug(bad)
    raise AssertionError(f"expected invalid_workspace for {bad!r}")
  except Exception:
    pass

validate_block_markdown("## Philosophy\\ntext\\n")
try:
  validate_block_markdown("no philosophy here")
  raise AssertionError("expected missing_philosophy")
except Exception:
  pass

_ = resolve_workspace_readme_path(repo_root, "ws1")  # should be under /tmp/.../auto-apps/ws1/README.md

before = "# Title\\n\\nSome text.\\n"
after, meta = upsert_readme_block(before, workspace="ws1", block_markdown="## Philosophy\\nX\\n")
assert README_BEGIN in after and README_END in after
assert after.index(README_BEGIN) > after.index("# Title")
assert meta.get("markers_preexisted") is False

after2, meta2 = upsert_readme_block(after, workspace="ws1", block_markdown="## Philosophy\\nY\\n")
assert "Y" in after2 and "X" not in after2
assert meta2.get("markers_preexisted") is True
print("ok")
PY

# Ensure docs mention the endpoint
timeout 10s rg -n "/api/actions/update-readme" backend/app.py docs/api-contracts.md
```

## Acceptance Checklist
- [ ] `POST /api/actions/update-readme` exists in `backend/app.py` routing.
- [ ] Workspace slug/path traversal is rejected; resolved README path must remain under `auto-apps/`.
- [ ] README owned block is inserted/replaced between `<!-- AUTOAPPDEV:README:BEGIN -->` and `<!-- AUTOAPPDEV:README:END -->`.
- [ ] `block_markdown` is required and must include a `## Philosophy` section.
- [ ] Update writes change artifacts under `AUTOAPPDEV_RUNTIME_DIR/logs/update_readme/<id>/` (before/after/diff/meta).
- [ ] `docs/api-contracts.md` documents the new endpoint.

