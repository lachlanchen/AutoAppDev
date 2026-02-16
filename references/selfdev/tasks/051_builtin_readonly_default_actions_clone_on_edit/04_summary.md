# Summary: 051 builtin_readonly_default_actions_clone_on_edit

## What Changed
- Backend now exposes a small set of **built-in default actions** (virtual, not stored in Postgres) marked `readonly:true`.
- Built-in actions cannot be modified directly:
  - `PUT`/`DELETE /api/actions/<builtin_id>` returns `403` `{ error: "readonly" }`.
- Added clone endpoint:
  - `POST /api/actions/<builtin_id>/clone` creates an editable DB copy and returns it (`readonly:false`).
- PWA Actions editor now supports **clone-on-edit**:
  - Saving changes on a readonly action clones it and saves changes to the clone automatically.
  - Delete is disabled for readonly actions.
- Updated `docs/api-contracts.md` to document `readonly` and the clone endpoint.

## Why
To provide a default, reusable action palette while keeping defaults stable and safe to upgrade (read-only), and still letting users customize behavior via cloning.

## How To Verify
Static checks:
```bash
timeout 10s python3 -m py_compile backend/app.py backend/builtin_actions.py backend/action_registry.py backend/storage.py
timeout 10s node --check pwa/app.js
```

Manual API/UI smoke (when backend is running):
1. `GET /api/actions?limit=200` includes built-ins with `readonly:true`.
2. `PUT /api/actions/<builtin_id>` returns `403 readonly`.
3. `POST /api/actions/<builtin_id>/clone` returns a new DB action id (`readonly:false`), which can then be `PUT` updated.
4. In the PWA Actions tab: edit a builtin and click Save; it should clone and then save to the clone.

