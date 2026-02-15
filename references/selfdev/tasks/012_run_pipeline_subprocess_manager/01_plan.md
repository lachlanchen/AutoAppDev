# Plan: 012 run_pipeline_subprocess_manager

## Goal
Harden the backend subprocess manager so the pipeline can be reliably controlled:
- Start the pipeline driver as a subprocess.
- Stop it reliably (no orphaned process group).
- Detect subprocess exit and update DB state accordingly.

Acceptance:
- Backend can start the driver/pipeline as a subprocess.
- Backend can stop it.
- Backend detects exit.
- No orphan processes after stop.

## Current State (References)
- Subprocess manager exists in `backend/app.py` as `PipelineControl`.
  - Uses `preexec_fn=os.setsid` and `os.killpg(...)` (good foundation).
  - Writes subprocess output to `runtime/logs/pipeline.log`.
  - `stop()` sends SIGTERM, waits 10s, then SIGKILL, but does not wait after SIGKILL.
  - The file handle opened for stdout in `_spawn()` is not closed in the parent process.
  - There is no exit detection loop; return codes are not recorded.
- Run state is stored in Postgres:
  - `pipeline_runs` table in `backend/schema.sql`.
  - `Storage.set_run_status(...)` in `backend/storage.py` supports terminal statuses (`stopped|failed|completed`) and sets `stopped_at`.
- Current pipeline state is stored in:
  - `pipeline_state` table and `Storage.set_pipeline_state(...)` (task 010).

## Approach (Minimal)
1. Fix resource/process handling in `PipelineControl`:
- Close the parent-side log file handle after spawning.
- Make stop() stronger:
  - After SIGKILL, wait again (short timeout).
  - Always clear `self.proc` and `self.run_id` when the process is confirmed dead.

2. Add an exit monitor that runs inside Tornado’s IOLoop:
- Periodically (e.g. every 0.5s) check `self.proc.poll()`.
- When it exits:
  - Determine terminal status:
    - `completed` if returncode == 0
    - `failed` otherwise
  - Update `pipeline_runs` status via `Storage.set_run_status(run_id, status, pid=...)`.
  - Update `pipeline_state` via `Storage.set_pipeline_state(state='stopped', pid=None, run_id=..., ts_kind='stop')`.
  - Clear `self.proc`/`self.run_id`.

3. Keep changes localized (no API changes required).

## Files To Change (Implementation Phase)
- Update: `backend/app.py`
  - `PipelineControl._spawn()` close stdout log file handle in parent.
  - `PipelineControl.stop()` wait after SIGKILL and clear internal references.
  - Add `PipelineControl.maybe_collect_exit()` method.
  - In `make_app(...)`, register a `tornado.ioloop.PeriodicCallback` to call `controller.maybe_collect_exit()`.
- Optional: `backend/storage.py`
  - No schema or storage changes required if we reuse existing `set_run_status` and `set_pipeline_state`.

## Step-by-Step Implementation Details

### Step 1: Close Log FD After Spawn
In `PipelineControl._spawn()` (`backend/app.py`):
- Open `pipeline.log` as it currently does.
- After `subprocess.Popen(...)` returns, immediately close the file object in the parent process.
  - The child retains the underlying fd.

### Step 2: Strengthen stop()
In `PipelineControl.stop()`:
- On SIGTERM: wait up to 10s.
- On timeout:
  - send SIGKILL
  - wait again up to ~2s
- After the process is confirmed exited:
  - update run status to `stopped`
  - clear `self.proc` and `self.run_id`

Also handle edge cases:
- If `killpg` fails (process already gone), treat as stopped.

### Step 3: Detect Exit
Add `async def maybe_collect_exit(self) -> None`:
- If no `self.proc`: return.
- `rc = self.proc.poll()`; if `rc is None`: return.
- Determine status:
  - `completed` if rc == 0 else `failed`
- Update storage:
  - `set_run_status(run_id, status, pid=proc.pid)`
  - `set_pipeline_state(state='stopped', pid=None, run_id=run_id, ts_kind='stop')`
- Clear `self.proc`/`self.run_id`.

### Step 4: Register Monitor
In `make_app(...)` in `backend/app.py`:
- After `controller = PipelineControl(...)`:
  - Create `tornado.ioloop.PeriodicCallback(lambda: loop.create_task(controller.maybe_collect_exit()), 500)`
  - Start the callback.

(Keep it simple: one periodic callback; avoid background threads.)

## Commands To Run (Verification)
Requires a working `.env` with Postgres.

1) Preflight:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 5s python -m backend.db_smoketest

timeout 10s python -m backend.apply_schema
```

2) Start backend briefly and start/stop the pipeline:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

RT_DIR="$(mktemp -d)"
export AUTOAPPDEV_RUNTIME_DIR="$RT_DIR"

timeout 20s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  python -m backend.app &
  bpid=$!
  cleanup() { kill "$bpid" 2>/dev/null || true; wait "$bpid" 2>/dev/null || true; }
  trap cleanup EXIT

  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done

  # Start pipeline
  curl -fsS -X POST http://127.0.0.1:8788/api/pipeline/start -H "Content-Type: application/json" -d '{}'
  sleep 0.5

  # Stop pipeline
  curl -fsS -X POST http://127.0.0.1:8788/api/pipeline/stop -H "Content-Type: application/json" -d '{}'
  sleep 1.0

  # Verify backend reports stopped
  curl -fsS http://127.0.0.1:8788/api/pipeline
  echo
'
```

3) Orphan check (best-effort):
- Use the PID returned by `/api/pipeline/start` and verify it does not exist after stop.
- Also verify the process group is gone (if tooling available).

## Acceptance Criteria Checks
- Starting sets a running PID/run_id.
- Stopping terminates the entire process group (no remaining PID).
- Backend detects natural exit and updates `pipeline_runs` to `completed`/`failed` and `pipeline_state` to `stopped`.
- No leftover background processes after the verification scripts (all wrapped in `timeout` and traps).
