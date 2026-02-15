# Work Notes: 033 backend_update_readme_action

## Summary
- Implemented a safe backend endpoint `POST /api/actions/update-readme` to upsert a workspace `README.md` owned block between fixed markers under `auto-apps/<workspace>/README.md`.
- Added runtime artifacts for each update under `AUTOAPPDEV_RUNTIME_DIR/logs/update_readme/<id>/` (before/after/diff/meta).
- Documented the endpoint in `docs/api-contracts.md`.

## Changes Made
- `backend/update_readme_action.py`
  - Added marker constants: `<!-- AUTOAPPDEV:README:BEGIN -->` / `<!-- AUTOAPPDEV:README:END -->`.
  - Added validation helpers for:
    - workspace slug (`single path segment`, no traversal)
    - `block_markdown` (required, size clamp, forbids marker injection, requires `## Philosophy`)
  - Added safe path resolver ensuring resolved path stays within repo `auto-apps/`.
  - Added deterministic README upsert logic (create/insert/replace) and artifact writer (before/after/diff/meta).
- `backend/app.py`
  - Added `UpdateReadmeHandler` and route: `POST /api/actions/update-readme`.
  - Writes README atomically and logs a one-line summary; writes artifacts under runtime logs.
- `docs/api-contracts.md`
  - Documented `POST /api/actions/update-readme` request/response, safety notes, and error examples.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/update_readme_action.py && echo "py_compile_ok"

timeout 10s rg -n "/api/actions/update-readme" backend/app.py docs/api-contracts.md
```

