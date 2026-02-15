# Plan: 051 builtin_readonly_default_actions_clone_on_edit

## Goal
Expose a small set of **built-in default actions** from the backend, marked **readonly**, and implement **clone-on-edit**:
- Built-ins show up in `GET /api/actions` (metadata list) and `GET /api/actions/<id>` (full spec).
- `PUT`/`DELETE` against built-ins are rejected.
- A clone endpoint creates an editable copy in the DB so the UI can edit/save it.

Acceptance:
- Backend exposes built-in default actions (include multilingual-aware prompts) marked `readonly: true`.
- Update/delete built-ins are rejected.
- Backend provides clone endpoint (and PWA uses it when user tries to edit a built-in).

## Current State (Relevant Files)
- Backend action registry API:
  - `backend/app.py`: `ActionsHandler` (`GET/POST /api/actions`), `ActionHandler` (`GET/PUT/DELETE /api/actions/<id>`), routes in `make_app()`.
  - `backend/storage.py`: CRUD for `action_definitions` table (no readonly/builtin column).
  - `backend/action_registry.py`: validation/normalization for `prompt` + `command` action specs.
- PWA actions editor:
  - `pwa/app.js`: `refreshActionsList()`, `loadActionDefinition()`, `saveActionFromForm()`, `deleteSelectedAction()`.
  - `pwa/api-client.js`: errors include `err.status` + `err.data`.
- Docs:
  - `docs/api-contracts.md`: documents current Actions API (no readonly, no clone endpoint).

## Design (Minimal + No DB Migration)
Keep built-ins **virtual** (not persisted in Postgres) to avoid schema migrations and seeding logic:
- Built-ins live in a new module (ex: `backend/builtin_actions.py`) with a reserved high ID range (safe JS integer).
- API handlers merge built-ins with DB actions.
- Clone endpoint copies a builtin into `action_definitions` via existing `Storage.create_action_definition()`.

### Built-in Action Set (v0)
Provide a small default set (6) aligned with the pipeline phases, with prompts that are **language-aware** (multilingual support) without needing new schema:
- `Plan (multilingual)`
- `Work (multilingual)`
- `Debug/Verify (multilingual)`
- `Fix (multilingual)`
- `Summary (multilingual, include “how to verify”; mention translation/localization as a section)`
- `Commit/Release note (multilingual; remind that git is handled externally)`

All built-ins:
- `kind: "prompt"`
- `spec.prompt`: includes a “Language” section instructing to write in the user/workspace language if known, else English.
- `readonly: true`
- `enabled: true`

## Implementation Steps (Next Phase: WORK)

### 1) Add Built-in Actions Module
Create `backend/builtin_actions.py`:
- Define a reserved ID base (ex: `9_000_000_000`) and a list of builtin action dicts:
  - Full shape for single action: `{id, title, kind, spec, enabled, readonly, created_at, updated_at}`
- Provide helpers:
  - `is_builtin_action_id(aid: int) -> bool`
  - `get_builtin_action(aid: int) -> dict | None` (full, includes `spec`)
  - `list_builtin_action_summaries() -> list[dict]` (omit `spec`, used by `GET /api/actions`)

### 2) Backend: Merge Built-ins Into List/Get
Edit `backend/app.py`:
- `ActionsHandler.get`:
  - Fetch DB actions via `storage.list_action_definitions(limit=...)`
  - Prepend (or append) `builtin_actions.list_builtin_action_summaries()`
  - Ensure response items include `readonly`:
    - built-ins `readonly: true`
    - DB actions `readonly: false` (add field at handler level for consistency)
  - Apply `limit` to the final list (keep built-ins always included, then fill remaining from DB).
- `ActionHandler.get`:
  - If `aid` is builtin: return `{ "action": <builtin> }`
  - Else fallback to storage.

### 3) Backend: Reject Update/Delete For Built-ins
Edit `backend/app.py` `ActionHandler.put` and `ActionHandler.delete`:
- If `aid` is builtin: return `403` with a stable error:
  - body: `{ "error": "readonly", "detail": "built-in actions are read-only; clone to edit" }`

### 4) Backend: Add Clone Endpoint
Edit `backend/app.py`:
- Add a new handler, e.g. `ActionCloneHandler`:
  - Route: `POST /api/actions/<id>/clone`
  - Behavior:
    - Require `<id>` to be a builtin action id (otherwise 404 or 400 `not_builtin`).
    - Create a new DB action with:
      - `title`: default to `<builtin title> (copy)` (clamp to 200 chars)
      - `kind/spec/enabled`: copied from builtin
    - Use `validate_action_create(...)` to normalize/clamp spec and ensure it stays within v0 constraints.
    - Save via `storage.create_action_definition(...)`.
    - Return `{ "ok": true, "action": <created db action> }`.
- Register the route in `make_app()` near other actions routes:
  - `(r"/api/actions/([0-9]+)/clone", ActionCloneHandler, {"storage": storage})`

### 5) PWA: Clone-On-Edit UX (Minimal)
Edit `pwa/app.js`:
- When loading an action, retain `action.readonly` in `selectedAction`.
- Update `updateActionsButtons()`:
  - Disable `Delete` when selected action is readonly.
  - Optionally disable `Save` when readonly unless user changes anything; simplest: allow Save and clone-on-save.
- Update `saveActionFromForm()` update path (`PUT` case):
  - If current selected action is `readonly: true` (or backend returns `error=readonly`):
    1. Call `POST /api/actions/<id>/clone`
    2. Switch `selectedActionId` to the returned clone id
    3. Perform the `PUT` to the cloned id using the current form payload
    4. Refresh list + keep selection; show message `cloned and saved`

No new UI widgets required (keeps changes small); the existing Save flow becomes “clone-on-edit”.

### 6) Docs Update
Edit `docs/api-contracts.md` (Actions section):
- Mention built-in actions appear in lists and may include:
  - `readonly: true`
- Document update/delete rejection for readonly actions:
  - `403 { "error": "readonly", ... }`
- Add endpoint:
  - `POST /api/actions/<id>/clone` response shape.

## Verification (DEBUG/VERIFY Phase)
Static checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/action_registry.py backend/builtin_actions.py
timeout 10s node --check pwa/app.js
```

Logic smoke (no server needed):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 - <<'PY'
from backend.builtin_actions import list_builtin_action_summaries, get_builtin_action
items = list_builtin_action_summaries()
assert items and all(i.get("readonly") is True for i in items)
full = get_builtin_action(items[0]["id"])
assert isinstance(full.get("spec"), dict)
print("builtin_actions_ok", len(items))
PY
```

Manual acceptance checks (when backend is running):
1. `GET /api/actions?limit=200` includes builtin actions with `readonly:true`.
2. `GET /api/actions/<builtin_id>` returns full spec + `readonly:true`.
3. `PUT /api/actions/<builtin_id>` and `DELETE /api/actions/<builtin_id>` return `403 readonly`.
4. `POST /api/actions/<builtin_id>/clone` returns a new DB action id; that new id is editable.
5. In the PWA Actions tab: editing a builtin and pressing Save results in a cloned editable action being saved (no manual copy/paste).

