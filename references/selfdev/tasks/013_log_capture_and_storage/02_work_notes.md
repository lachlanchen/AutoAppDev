# Work Notes: 013 log_capture_and_storage

## Summary of Changes
- Added an in-memory rolling log buffer and an incremental log API.
- Implemented file-based capture into the rolling buffer (polls `runtime/logs/pipeline.log` and `runtime/logs/backend.log`).
- Added `GET /api/logs?source=...&since=<id>&limit=N` returning incremental entries.
- Kept existing `GET /api/logs/tail` intact.
- Updated `docs/api-contracts.md` to document the new endpoint.

## Files Changed
- Updated: `backend/app.py`
- Updated: `docs/api-contracts.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

python -m py_compile backend/app.py
rg -n "\(r\"/api/logs\"|class LogsSinceHandler|FileLogTailer|LogBuffer" backend/app.py
rg -n "GET /api/logs\?source" docs/api-contracts.md
```

## Notes
- Log capture uses a polling tailer to stay minimal and avoid changing the subprocess spawn behavior.
- DB persistence of log lines is not implemented in this step (optional in acceptance); the rolling buffer is in-memory only.
