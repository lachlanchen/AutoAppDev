# Work Notes: 010 pipeline_state_table_and_api

## Summary of Changes
- Added `pipeline_state` table (singleton row `id=1`) to `backend/schema.sql` with state + timestamps.
- Added storage helpers in `backend/storage.py`:
  - `get_pipeline_state()` returns state + timestamp fields.
  - `set_pipeline_state(...)` upserts state transitions (`start|pause|resume|stop`).
- Added `GET /api/pipeline` in `backend/app.py` returning `{ pipeline: ... }`.
- Updated pipeline control endpoints to update `pipeline_state` on successful start/pause/resume/stop.
- Updated `docs/api-contracts.md` to document `GET /api/pipeline`.

## Files Changed
- Updated: `backend/schema.sql`
- Updated: `backend/storage.py`
- Updated: `backend/app.py`
- Updated: `docs/api-contracts.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

python -m py_compile backend/app.py backend/storage.py

rg -n "create table if not exists pipeline_state" backend/schema.sql
rg -n "get_pipeline_state|set_pipeline_state" backend/storage.py
rg -n "\(r\"/api/pipeline\"" backend/app.py
rg -n "GET /api/pipeline" docs/api-contracts.md
```

## Notes
- Existing `/api/pipeline/status` remains unchanged for current PWA compatibility.
- Live verification (schema apply + endpoint calls) is deferred to DEBUG/VERIFY because it requires a real `.env` / Postgres.
