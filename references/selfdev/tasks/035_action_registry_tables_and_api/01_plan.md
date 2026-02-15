# Plan: 035 action_registry_tables_and_api

## Goal
Add a minimal **action registry** backed by Postgres so the controller can store reusable action definitions (prompt-based and command-based) and expose CRUD endpoints with validation and safe defaults.

Acceptance:
- Backend stores action definitions in Postgres (prompt + command)
- Minimal CRUD endpoints exist and validate inputs
- Safe defaults are applied for optional fields (agent/model/reasoning/timeouts/cwd)

## Current State (References)
- DB schema is applied at backend startup from:
  - `backend/schema.sql` (idempotent `create table if not exists ...`)
- DB access pattern:
  - `backend/storage.py` (`asyncpg` pool; CRUD methods for scripts/inbox/config)
- HTTP API patterns:
  - `backend/app.py` (Tornado handlers + routing in `make_app()`)
  - Existing special-case action execution endpoint: `POST /api/actions/update-readme`
- API docs:
  - `docs/api-contracts.md` (document existing endpoints; has `## Actions` section)
- Runner supports minimal action kinds (for context only):
  - `docs/pipeline-runner-codegen.md` (`codex_exec`, `run`, `note`)

## Data Model (v0)
Create a single table storing action definitions with a typed `kind` and JSON `spec`:
- Table: `action_definitions`
  - `id bigserial primary key`
  - `title text not null`
  - `kind text not null` (`prompt` | `command`)
  - `spec jsonb not null` (validated shape per kind)
  - `enabled boolean not null default true`
  - `created_at timestamptz not null default now()`
  - `updated_at timestamptz not null default now()`
  - Index: `updated_at` (and optionally `kind`)

### Action Spec Shapes
Prompt action (`kind="prompt"`) spec:
```json
{
  "agent": "codex",
  "model": "gpt-5.3-codex",
  "reasoning": "medium",
  "timeout_s": 45,
  "prompt": "..."
}
```

Command action (`kind="command"`) spec:
```json
{
  "shell": "bash",
  "cwd": ".",
  "timeout_s": 60,
  "cmd": "..."
}
```

Notes:
- `spec` is stored but **not executed** in this task; validation is about shape/safety for future execution.
- `cwd` must resolve under the repo root (similar to `PipelineStartHandler` checks in `backend/app.py`).

## API Design (Minimal CRUD)
Use `/api/actions` for the registry (definitions). Keep the existing executor endpoint at `/api/actions/update-readme` unchanged.

Endpoints:
1. `GET /api/actions?limit=N`
   - Response: `{ "actions": [ { id, title, kind, enabled, created_at, updated_at } ] }`
2. `POST /api/actions`
   - Request: `{ "title": "...", "kind": "prompt|command", "spec": { ... }, "enabled": true }`
   - Response: `{ "ok": true, "action": { ...full record... } }`
3. `GET /api/actions/<id>`
   - Response: `{ "action": { ... } }`
4. `PUT /api/actions/<id>`
   - Partial updates supported: any of `title`, `enabled`, `spec`, and (optionally) `kind` (recommended: disallow kind changes in v0).
   - Response: `{ "ok": true, "action": { ... } }`
5. `DELETE /api/actions/<id>`
   - Response: `{ "ok": true }`

Error codes (examples):
- `invalid_json`, `invalid_body`
- `invalid_title`, `invalid_kind`, `invalid_spec`
- `invalid_cmd`, `invalid_prompt`
- `invalid_cwd`, `cwd_outside_repo`
- `not_found`

## Implementation Steps (Next Phase: WORK)
1. Add the action registry table
   - Update `backend/schema.sql`:
     - Add `create table if not exists action_definitions (...)`
     - Add `create index if not exists action_definitions_updated_at_idx ...`

2. Add storage methods
   - Update `backend/storage.py`:
     - Implement:
       - `create_action_definition(title, kind, spec, enabled=True) -> dict`
       - `get_action_definition(id) -> dict | None`
       - `list_action_definitions(limit=50) -> list[dict]`
       - `update_action_definition(id, ...) -> dict | None` (partial)
       - `delete_action_definition(id) -> bool`
     - Follow existing patterns used by `pipeline_scripts` CRUD (timestamps to `.isoformat()`).

3. Add validation helpers (small module)
   - Add `backend/action_registry.py` (or similar):
     - `validate_action_payload(body: dict, *, repo_root: Path, for_update: bool=False) -> tuple[title, kind, spec, enabled]`
     - Prompt validation:
       - `prompt` required; clamp size (e.g. <= 200k)
       - default `agent="codex"`, `reasoning="medium"`
       - default `model` from config/env: `AUTOAPPDEV_CODEX_MODEL` fallback `gpt-5.3-codex`
       - default/clamp `timeout_s` (e.g. 5..300)
     - Command validation:
       - `cmd` required; clamp size (e.g. <= 20k)
       - `shell` default `"bash"` (optionally restrict to `"bash"` only for v0)
       - `cwd` default `"."`; resolve under `REPO_ROOT` and reject traversal/out-of-repo
       - default/clamp `timeout_s` (e.g. 1..3600)
     - Return a normalized `spec` dict containing only allowed keys (ignore unknowns).

4. Add Tornado handlers + routes
   - Update `backend/app.py`:
     - Add `ActionsHandler(BaseHandler)` wired with `storage`:
       - `get()` list with `limit` query param
       - `post()` create with validation
     - Add `ActionHandler(BaseHandler)` wired with `storage`:
       - `get(id)`, `put(id)`, `delete(id)`
     - Add routes in `make_app(...)` near existing endpoints:
       - `(r"/api/actions", ActionsHandler, {"storage": storage})`
       - `(r"/api/actions/([0-9]+)", ActionHandler, {"storage": storage})`
     - Ensure these do not conflict with existing `(r"/api/actions/update-readme", ...)` route.

5. Document the API
   - Update `docs/api-contracts.md` under `## Actions`:
     - Document the action registry endpoints and request/response shapes.
     - Link to `docs/common-actions.md` for the `update_readme` contract and clarify the difference:
       - registry (definitions) vs executor endpoints.

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Static compile
timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/action_registry.py

# Grep: ensure endpoints are wired + docs updated
timeout 10s rg -n \"/api/actions\\b\" backend/app.py docs/api-contracts.md

# (If a local Postgres is available) minimal CRUD smoke via curl:
# 1) start backend: python3 -m backend.app
# 2) create: curl -sS -X POST http://127.0.0.1:8788/api/actions -H 'content-type: application/json' \\
#      -d '{\"title\":\"Test Prompt\",\"kind\":\"prompt\",\"spec\":{\"prompt\":\"## Philosophy\\n...\"}}'
# 3) list:   curl -sS http://127.0.0.1:8788/api/actions
# 4) get:    curl -sS http://127.0.0.1:8788/api/actions/1
# 5) update: curl -sS -X PUT http://127.0.0.1:8788/api/actions/1 -H 'content-type: application/json' -d '{\"enabled\":false}'
# 6) delete: curl -sS -X DELETE http://127.0.0.1:8788/api/actions/1
```

## Acceptance Checklist
- [ ] `backend/schema.sql` creates `action_definitions` table + index.
- [ ] `backend/storage.py` has CRUD methods for action definitions.
- [ ] `backend/app.py` exposes CRUD endpoints under `/api/actions` with validation and safe defaults.
- [ ] `docs/api-contracts.md` documents the action registry endpoints and distinguishes registry vs executor endpoints.

