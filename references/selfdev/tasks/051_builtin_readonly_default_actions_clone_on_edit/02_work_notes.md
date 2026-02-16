# Work Notes: 051 builtin_readonly_default_actions_clone_on_edit

## Summary of Changes
- Added a backend-built-in action set (virtual, read-only) exposed via the existing Actions API.
- Marked built-ins as `readonly:true` and enforced immutability:
  - `PUT`/`DELETE` on built-in ids now return `403` with `{ error: "readonly" }`.
- Added `POST /api/actions/<id>/clone` to copy a built-in action into the DB as an editable action definition.
- Updated the PWA Actions editor to support **clone-on-edit**:
  - Delete is disabled for readonly actions.
  - Save on a readonly action clones it, then saves updates to the clone automatically.
- Updated `docs/api-contracts.md` to document `readonly` and the clone endpoint.

## Implementation Details
- Built-ins are **not persisted** in Postgres (no schema migration). They live in a new module:
  - `backend/builtin_actions.py`
  - IDs are in a reserved high range (`9_000_000_000+`) to avoid collisions while staying in JS safe integer range.
- Built-in prompts include a stable multilingual preamble and placeholder note:
  - Encourages output in the same language as the task/context
  - Mentions `{{task.title}}`, `{{task.acceptance}}`, `{{runtime_dir}}` placeholders (when used by runners/templates)
- API behavior changes:
  - `GET /api/actions`: returns built-in summaries + DB actions; DB actions get `readonly:false` injected for consistency.
  - `GET /api/actions/<id>`: built-ins return full spec; DB actions return `readonly:false`.

## Files Changed / Added
- Added: `backend/builtin_actions.py`
- Updated: `backend/app.py`
  - Merged built-ins into actions list/get
  - Enforced readonly for built-ins on update/delete
  - Added `ActionCloneHandler` + route `/api/actions/<id>/clone`
- Updated: `pwa/app.js`
  - Clone-on-save when selected action is readonly (or backend returns `error=readonly`)
  - Disabled delete for readonly actions
- Updated: `docs/api-contracts.md`
  - Documented `readonly` and clone endpoint

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

sed -n '1,240p' references/selfdev/tasks/051_builtin_readonly_default_actions_clone_on_edit/context.md

rg -n "class Actions|/api/actions|actions" backend/app.py backend/storage.py backend/models.py backend/schema.sql backend/migrations -S | head -n 80
sed -n '820,940p' backend/app.py
rg -n "action_def" backend/schema.sql backend/storage.py backend/action_registry.py backend/ -S | head -n 120
sed -n '60,110p' backend/schema.sql

rg -n "action registry|action_definitions|readonly|built-?in|clone" docs backend pwa -S | head -n 120
sed -n '220,340p' docs/api-contracts.md
rg -n "validate_action_create|validate_action_update|class ActionRegistryError" backend -S
sed -n '1,420p' backend/action_registry.py

sed -n '1040,1360p' pwa/app.js
sed -n '340,620p' backend/storage.py
sed -n '1310,1410p' backend/app.py

python3 -m py_compile backend/app.py backend/builtin_actions.py backend/action_registry.py backend/storage.py
node --check pwa/app.js

python3 - <<'PY'
from backend.builtin_actions import list_builtin_action_summaries, get_builtin_action, is_builtin_action_id
items = list_builtin_action_summaries()
assert items and all(i.get("readonly") is True for i in items)
first_id = items[0]["id"]
assert is_builtin_action_id(first_id)
full = get_builtin_action(first_id)
assert isinstance(full.get("spec"), dict)
print("ok", len(items), "first=", first_id)
PY

git diff --stat
git status --porcelain
```

