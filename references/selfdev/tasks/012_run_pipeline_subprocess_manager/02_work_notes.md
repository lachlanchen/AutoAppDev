# Work Notes: 012 run_pipeline_subprocess_manager

## Summary of Changes
- Hardened `PipelineControl` subprocess handling in `backend/app.py`:
  - `_spawn()` now closes the parent-side log file handle after spawning.
  - `stop()` now waits after SIGKILL, updates `pipeline_runs` and `pipeline_state`, and clears internal process references.
  - Added `maybe_collect_exit()` to detect natural process exit and mark runs as `completed` (rc=0) or `failed`.
- Added a Tornado `PeriodicCallback` in `make_app()` to poll for subprocess exit.

## Files Changed
- Updated: `backend/app.py`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

python -m py_compile backend/app.py
```

## Notes
- Exit monitoring runs inside the Tornado IOLoop (no threads) and updates DB state when the subprocess ends.
- Live verification (start/stop + orphan check) is deferred to DEBUG/VERIFY because it requires a real `.env` / Postgres.
