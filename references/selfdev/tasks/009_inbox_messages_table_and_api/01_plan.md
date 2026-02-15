# Plan: 009 inbox_messages_table_and_api

## Goal
Add a first-class “Inbox” persistence API backed by Postgres.

Acceptance:
- Create DB table for inbox messages.
- Implement `GET /api/inbox` (latest N) and `POST /api/inbox` (create) with basic validation.

## Current State (References)
- DB schema in `backend/schema.sql` includes `chat_messages`, but no `inbox_messages` table.
- Backend has a Chat handler in `backend/app.py` (`GET|POST /api/chat`).
  - `POST /api/chat` already writes a file artifact to `runtime/inbox/*_user.md` via `_write_inbox_message()`.
- Storage layer `backend/storage.py` persists chat messages into `chat_messages`.

## Design Choice (Minimal)
Introduce a new “Inbox” API and table without breaking existing `/api/chat`.

- New table: `inbox_messages`
- New endpoints: `GET /api/inbox`, `POST /api/inbox`
- Keep `/api/chat` unchanged for now (PWA currently uses it in `pwa/app.js`).
- Mirror the existing runtime side effect:
  - When an inbox message is created, also write `runtime/inbox/*_user.md` (so pipeline scripts can consume it).

## Files To Change (Implementation Phase)
- Update: `backend/schema.sql`
  - Add `create table if not exists inbox_messages (...)`.
- Update: `backend/storage.py`
  - Add methods to insert/list inbox messages using the shared pool.
- Update: `backend/app.py`
  - Add `InboxHandler` and route wiring.
- Optional docs touch (keep minimal): `docs/api-contracts.md`
  - Add `/api/inbox` contract section (or a short note mapping inbox to chat/inbox semantics).

## Schema Details
In `backend/schema.sql`, add:
- `inbox_messages` table:
  - `id bigserial primary key`
  - `role text not null` (keep consistent with `chat_messages`; for now accept at least `user`)
  - `content text not null`
  - `created_at timestamptz not null default now()`
- Optional indices are not required for MVP.

Because the schema uses `IF NOT EXISTS`, running apply twice is safe.

## Storage API
In `backend/storage.py`, add:
- `async def add_inbox_message(self, role: str, content: str) -> None`
  - Insert into `inbox_messages(role, content)`.
- `async def list_inbox_messages(self, limit: int = 50) -> list[dict[str, Any]]`
  - Query `select id, role, content, created_at from inbox_messages order by id desc limit $1`.
  - Return items sorted ascending by id (same pattern as `list_chat_messages`).

Keep implementation consistent with existing Postgres helpers (`require_pool()` + acquire) added in task 006.

## Handler API
In `backend/app.py`, add `InboxHandler(BaseHandler)`:

### GET /api/inbox
- Query param: `limit` (default `50`, clamp `1..500`).
- Response:
  - `{ "messages": [ { "id": ..., "role": ..., "content": ..., "created_at": ... }, ... ] }`

### POST /api/inbox
- Request body: `{ "content": "..." }`
- Basic validation:
  - Must be JSON object.
  - `content` required and `strip()` non-empty.
  - Optional: max length (e.g. 10_000) to prevent abuse.
- Behavior:
  - Persist to DB via `Storage.add_inbox_message("user", content)`.
  - Write runtime inbox file via existing `_write_inbox_message(runtime_dir, content)`.
- Response:
  - `{ "ok": true }`.
- Errors:
  - `400 {"error":"invalid_body"}` for non-object.
  - `400 {"error":"empty"}` for empty content.

## Route Wiring
In `backend/app.py` route list inside `make_app(...)`:
- Add `(r"/api/inbox", InboxHandler, {"storage": storage, "runtime_dir": runtime_dir})`.

## Commands To Run (Verification)
Requires a working `.env` with `DATABASE_URL`.

1) Apply schema:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Ensure DB reachable
timeout 5s python -m backend.db_smoketest

# Apply schema.sql (includes new inbox_messages table)
timeout 10s python -m backend.apply_schema
```

2) Endpoint smoke (start backend briefly; no leftover processes):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

RT_DIR="$(mktemp -d)"
export AUTOAPPDEV_RUNTIME_DIR="$RT_DIR"

timeout 10s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  python -m backend.app &
  pid=$!
  cleanup() { kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true; }
  trap cleanup EXIT

  # Wait until backend responds
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done

  echo "--- POST /api/inbox ---"
  curl -fsS -X POST http://127.0.0.1:8788/api/inbox \
    -H "Content-Type: application/json" \
    -d '{"content":"hello inbox"}'
  echo

  echo "--- GET /api/inbox?limit=5 ---"
  curl -fsS "http://127.0.0.1:8788/api/inbox?limit=5"
  echo
'

# Verify runtime side-effect exists
ls -la "$RT_DIR/inbox" | head
```

## Acceptance Criteria Checks
- DB table `inbox_messages` exists after applying schema.
- `POST /api/inbox` accepts valid content and returns `{ ok: true }`.
- `GET /api/inbox` returns latest N messages with `id/role/content/created_at`.
- Creating an inbox message writes a file under `runtime/inbox/`.
