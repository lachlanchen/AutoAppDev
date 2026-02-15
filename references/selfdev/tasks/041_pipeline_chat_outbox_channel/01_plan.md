# Plan: 041 pipeline_chat_outbox_channel

## Goal
Add a pipeline outbox/messages channel so pipelines can safely report messages/status back to the UI:
- Backend supports persistence and safe ingestion for pipeline -> UI messages.
- PWA displays pipeline outbox messages alongside user “Inbox” guidance.

Acceptance:
- Backend provides a safe way for pipelines to write messages/status back to the UI (DB and/or `runtime/outbox` files).
- PWA can display those messages.

## Current State (Relevant Files)
- Inbox (UI -> pipeline guidance) exists:
  - API: `backend/app.py` (`InboxHandler` at `/api/inbox`)
  - DB: `backend/schema.sql` (`inbox_messages`)
  - Storage: `backend/storage.py` (`add_inbox_message`, `list_inbox_messages`)
  - File queue for pipelines: `backend/app.py:_write_inbox_message` writes `runtime/inbox/*_user.md`
- PWA “Inbox” tab renders `/api/inbox` messages:
  - UI: `pwa/index.html` (`#tab-chat`, `#chatlog`)
  - Logic: `pwa/app.js` (`loadChat()` calls `/api/inbox?limit=50`)
- Runtime layout already documents `runtime/outbox/` as a design target:
  - `docs/workspace-layout.md`
- API docs already cover inbox/chat:
  - `docs/api-contracts.md` “Inbox Messages”

## Proposed Minimal Design
Implement a first-class **Outbox Messages** API backed by Postgres, and optionally support a file-based queue under `runtime/outbox/` that the backend can ingest.

Why this design:
- “Safe” means pipelines can only append messages (DB row insert and/or constrained runtime dir files), not arbitrary file writes.
- Keeps architecture consistent with existing inbox: DB persistence + runtime file queue patterns.
- PWA changes are minimal: fetch `/api/outbox` in addition to `/api/inbox` and render.

## Implementation Steps (Next Phase: WORK)

### 1) DB Schema: Add `outbox_messages`
Edit `backend/schema.sql`:
- Add:
  - `create table if not exists outbox_messages (...)`
    - `id bigserial primary key`
    - `role text not null` (e.g. `pipeline` / `system`)
    - `content text not null`
    - `created_at timestamptz not null default now()`
- Add an index if useful (optional, minimal):
  - `create index if not exists outbox_messages_created_at_idx on outbox_messages(created_at);`

Acceptance impact: enables persistence for pipeline messages.

### 2) Storage Methods
Edit `backend/storage.py`:
- Add:
  - `add_outbox_message(role: str, content: str) -> None`
  - `list_outbox_messages(limit: int = 50) -> list[dict[str, Any]]`
- Keep behavior consistent with inbox methods:
  - clamp `limit` (1..500)
  - return in chronological order (reverse after `order by id desc`)
  - fallback to `runtime/state.json` if needed (mirror `inbox` storage pattern)

### 3) Backend API: `/api/outbox`
Edit `backend/app.py`:
- Add helper(s):
  - `def _write_outbox_message(runtime_dir: Path, role: str, content: str) -> None`
    - writes to `runtime/outbox/<ts>_<role>.md` (same naming style as inbox, constrained to runtime dir)
    - used only as an optional side-effect for debugging or file-queue support
- Add `OutboxHandler(BaseHandler)`:
  - `GET /api/outbox?limit=N`: returns `{ "messages": [...] }` from `storage.list_outbox_messages`
  - `POST /api/outbox`: accepts `{ "content": "...", "role": "pipeline" }`
    - validate body is an object
    - `content` required, trimmed, max length (e.g. 10_000 like inbox)
    - `role` optional; clamp to a safe allowlist (`pipeline`, `system`) and default to `pipeline`
    - persist via `storage.add_outbox_message(role, content)`
    - (optional) also `_write_outbox_message(runtime_dir, role, content)`
    - respond `{ "ok": true }`
- Register route in `make_app(...)`:
  - `(r"/api/outbox", OutboxHandler, {"storage": storage, "runtime_dir": runtime_dir}),`

Acceptance impact: provides a safe HTTP-based outbox for pipelines (curl from runner scripts).

### 4) Optional: File-Based `runtime/outbox/` Ingestion (If Needed For Acceptance)
If we want to explicitly satisfy “DB and/or runtime/outbox files” via files (not just via POST side-effect):
- Add a periodic poller in `backend/app.py` (similar to log polling):
  - Scan `runtime/outbox/` for files matching `^[0-9]+_.*\\.(md|txt)$`
  - For each file:
    - read up to a max size (e.g. 100 KB)
    - infer role from filename suffix (`_pipeline.md`, `_system.md`) or default `pipeline`
    - insert via `storage.add_outbox_message(...)`
    - move to `runtime/outbox/processed/` (or delete) to prevent double ingestion
  - Run via `tornado.ioloop.PeriodicCallback(..., 500 or 1000).start()`

This step is optional; if implemented, document a recommended atomic write pattern for pipelines:
- write to temp + rename into `runtime/outbox/` so backend never ingests partial writes.

### 5) PWA: Display Outbox Messages
Edit `pwa/app.js`:
- Update `loadChat()` to also fetch outbox messages:
  - `GET /api/inbox?limit=50`
  - `GET /api/outbox?limit=50` (or 200)
- Render combined view in `#chatlog`:
  - Map inbox messages as `{role:"user", ...}`
  - Map outbox messages as `{role:"pipeline" or "system", ...}`
  - Merge + sort by `created_at` when present; if missing, preserve stable order (inbox first then outbox) as a fallback.
  - Reuse existing styling: `msg--user` for `role === "user"`, otherwise `msg--system`.
- Keep message send path unchanged (`POST /api/inbox`).

Keep changes minimal:
- Prefer no `pwa/index.html` edits.
- If a new label is added (e.g. “Outbox”), use `data-i18n` and add keys to `pwa/i18n.js` (task 040 i18n system).

### 6) Docs
Edit `docs/api-contracts.md`:
- Add a new “Outbox Messages” section next to “Inbox Messages”:
  - `GET /api/outbox?limit=N`
  - `POST /api/outbox`
  - Mention optional file queue under `runtime/outbox/` if implemented.

Edit `docs/workspace-layout.md`:
- Add a short paragraph under “Runtime Dir” describing `runtime/outbox/` message queue semantics and how pipelines can write to it (if ingestion is implemented).

## Verification Commands (DEBUG/VERIFY Phase)
Smallest reasonable checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python -m py_compile backend/app.py backend/storage.py
timeout 10s node --check pwa/app.js

timeout 10s rg -n \"/api/outbox|outbox_messages|runtime/outbox\" backend/app.py backend/storage.py backend/schema.sql pwa/app.js docs/api-contracts.md docs/workspace-layout.md
```

Manual smoke (with backend running):
1. Send an outbox message via HTTP:
   - `curl -sS -X POST -H 'Content-Type: application/json' http://127.0.0.1:8788/api/outbox -d '{\"role\":\"pipeline\",\"content\":\"hello from pipeline\"}'`
2. Open PWA, go to `Inbox`, confirm the pipeline message appears styled as system.
3. (If file ingestion is implemented) write a file into `runtime/outbox/` and confirm it shows up in the UI:
   - `mkdir -p runtime/outbox && printf 'file outbox hello\\n' > runtime/outbox/$(date +%s%3N)_pipeline.md`

## Acceptance Checklist
- [ ] `backend/schema.sql` has `outbox_messages` table.
- [ ] Backend exposes `GET/POST /api/outbox` with validation + size limits.
- [ ] Pipeline can write a message via the outbox mechanism (HTTP and/or runtime/outbox file).
- [ ] PWA `Inbox` view shows pipeline outbox messages.
- [ ] Default PWA theme remains light (no theme behavior changes).

