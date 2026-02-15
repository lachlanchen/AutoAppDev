# Work Notes: 035 action_registry_tables_and_api

## Summary
- Added an action registry stored in Postgres (`action_definitions`) and exposed minimal CRUD endpoints under `/api/actions`.
- Implemented validation + safe defaults for prompt- and command-based action definitions.
- Documented the registry endpoints in `docs/api-contracts.md`.

## Changes Made
- `backend/schema.sql`
  - Added `action_definitions` table + `action_definitions_updated_at_idx`.
- `backend/storage.py`
  - Added CRUD methods:
    - `create_action_definition`, `get_action_definition`, `list_action_definitions`, `update_action_definition`, `delete_action_definition`.
- `backend/action_registry.py`
  - Added validation/normalization for action payloads:
    - `kind`: `prompt|command`
    - prompt spec: requires `prompt`, defaults `agent/model/reasoning/timeout_s` with clamps
    - command spec: requires `cmd`, defaults `shell/cwd/timeout_s`, restricts `shell="bash"`, and normalizes `cwd` under repo root
  - Update validation merges `spec` patches onto existing `spec` so partial updates work.
- `backend/app.py`
  - Added registry endpoints:
    - `GET/POST /api/actions`
    - `GET/PUT/DELETE /api/actions/<id>`
  - Kept existing executor endpoint `POST /api/actions/update-readme` unchanged.
- `docs/api-contracts.md`
  - Documented the action registry endpoints and clarified registry vs executor endpoints under `/api/actions/*`.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/action_registry.py && echo "py_compile_ok"

timeout 10s rg -n "\\(r\\\"/api/actions|/api/actions\\b" backend/app.py docs/api-contracts.md
```

