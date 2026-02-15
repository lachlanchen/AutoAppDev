# Work Notes: 011 pipeline_control_endpoints

## Summary of Changes
- Enforced pipeline state transitions for control endpoints in `backend/app.py` using `Storage.get_pipeline_state()`:
  - Start only allowed from `stopped`.
  - Pause only allowed from `running`.
  - Resume only allowed from `paused`.
  - Stop only allowed from `running|paused`.
- Invalid transitions now return HTTP 400 with `{ ok:false, error:"invalid_transition", from, action, detail }`.
- Updated `docs/api-contracts.md` with an example invalid-transition response.

## Files Changed
- Updated: `backend/app.py`
- Updated: `docs/api-contracts.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

python -m py_compile backend/app.py
rg -n "invalid_transition" backend/app.py docs/api-contracts.md | head
```

## Notes
- This task performs enforcement at the handler layer; the underlying controller still performs best-effort stop/pause/resume operations.
- Live verification (HTTP 400 vs 200) is deferred to DEBUG/VERIFY because it requires a real `.env` / Postgres.
