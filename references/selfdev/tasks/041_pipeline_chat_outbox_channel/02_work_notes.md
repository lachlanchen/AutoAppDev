# Work Notes: 041 pipeline_chat_outbox_channel

## Implementation Notes
- Added persistent outbox message storage:
  - `backend/schema.sql`: new `outbox_messages` table + `outbox_messages_created_at_idx`.
  - `backend/storage.py`: `add_outbox_message()` + `list_outbox_messages()`.
- Added backend outbox API + file queue ingestion:
  - `backend/app.py`: new `OutboxHandler` at `GET/POST /api/outbox` with validation (`invalid_body`, `empty`, `too_long`) and role allowlist (`pipeline`, `system`).
  - `backend/app.py`: periodic ingestor for `runtime/outbox/*.md|*.txt`:
    - infers role from filename `<ts>_<role>.md`
    - clamps stored content to 10_000 chars
    - moves ingested files to `runtime/outbox/processed/` to prevent reprocessing.
- Updated PWA to display pipeline outbox messages:
  - `pwa/app.js`: `loadChat()` now fetches both `/api/inbox` and `/api/outbox`, merges by `created_at`, and renders all messages in the existing Inbox view.
- Updated docs:
  - `docs/api-contracts.md`: new “Outbox Messages” section + runtime outbox file queue semantics.
  - `docs/workspace-layout.md`: documented `runtime/outbox/` queue usage.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

sed -n '1,200p' references/selfdev/tasks/041_pipeline_chat_outbox_channel/context.md
rg -n "inbox" backend | head -n 200
sed -n '880,1040p' backend/app.py
sed -n '1,120p' backend/schema.sql
nl -ba backend/storage.py | sed -n '540,720p'
nl -ba docs/api-contracts.md | sed -n '420,520p'
sed -n '1,120p' docs/workspace-layout.md

timeout 10s python -m py_compile backend/app.py backend/storage.py
timeout 10s node --check pwa/app.js
```

