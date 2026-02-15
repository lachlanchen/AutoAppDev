# Summary: 041 pipeline_chat_outbox_channel

## What Changed
- Added a pipeline -> UI outbox channel in the backend:
  - `backend/schema.sql`: new `outbox_messages` table + `outbox_messages_created_at_idx`.
  - `backend/storage.py`: `add_outbox_message()` + `list_outbox_messages()`.
- Added `/api/outbox` + file-queue ingestion:
  - `backend/app.py`: `OutboxHandler` at `GET/POST /api/outbox` with validation and a role allowlist (`pipeline`, `system`).
  - `backend/app.py`: periodic ingestion of `runtime/outbox/<ts>_<role>.md|.txt`, moving processed files to `runtime/outbox/processed/`.
- Updated the PWA to display outbox messages:
  - `pwa/app.js`: `loadChat()` now fetches `/api/inbox` and `/api/outbox`, merges messages by `created_at`, and renders them together in the existing Inbox view.
- Updated docs:
  - `docs/api-contracts.md`: documented `/api/outbox` and `runtime/outbox/` queue semantics.
  - `docs/workspace-layout.md`: documented `runtime/outbox/` in the runtime directory contract.

## Why
Task 041 acceptance requires a safe pipeline message/status channel back to the UI (DB and/or `runtime/outbox/` files) and for the PWA to display those messages.

## How To Verify
Minimal checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python -m py_compile backend/app.py backend/storage.py
timeout 10s node --check pwa/app.js
```

Manual smoke (backend running):
1. `curl -sS -X POST http://127.0.0.1:8788/api/outbox -H 'content-type: application/json' -d '{"role":"pipeline","content":"hello outbox"}'`
2. Open the PWA and go to the Inbox/Chat tab; confirm the outbox message appears.

File-queue smoke (alternative to HTTP):
1. `mkdir -p runtime/outbox`
2. `printf 'hello from file\n' > runtime/outbox/$(date +%s%3N)_pipeline.md`
3. Wait ~1s, then reload the PWA Inbox/Chat tab; confirm the message appears.

