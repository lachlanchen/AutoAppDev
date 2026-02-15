# Work Notes: 009 inbox_messages_table_and_api

## Summary of Changes
- Added `inbox_messages` table to `backend/schema.sql`.
- Added inbox persistence methods to `backend/storage.py`:
  - `add_inbox_message(...)`
  - `list_inbox_messages(...)`
- Added `/api/inbox` endpoints in `backend/app.py`:
  - `GET /api/inbox?limit=N` returns latest N.
  - `POST /api/inbox { content }` creates a message with basic validation.
  - Side effect: writes `runtime/inbox/*_user.md` like chat does.
- Updated `docs/api-contracts.md` to include `/api/inbox` contract.

## Files Changed
- Updated: `backend/schema.sql`
- Updated: `backend/storage.py`
- Updated: `backend/app.py`
- Updated: `docs/api-contracts.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

python -m py_compile backend/app.py backend/storage.py

rg -n "create table if not exists inbox_messages" backend/schema.sql
rg -n "add_inbox_message|list_inbox_messages" backend/storage.py
rg -n "class InboxHandler|/api/inbox" backend/app.py
```

## Notes
- This task adds new endpoints without changing the existing `/api/chat` behavior used by the current PWA.
- Full runtime verification (schema apply + live endpoint calls) is deferred to DEBUG/VERIFY because it requires a real `.env` / Postgres.
