# Plan: 011 pipeline_control_endpoints

## Goal
Enforce pipeline state transitions for control endpoints:
- `POST /api/pipeline/start|stop|pause|resume`

Acceptance:
- State transitions are enforced (e.g. cannot pause if stopped).
- Invalid transitions return HTTP 400 with a clear reason.

## Current State (References)
- Endpoints exist in `backend/app.py`:
  - `POST /api/pipeline/start` (`PipelineStartHandler`)
  - `POST /api/pipeline/stop` (`PipelineStopHandler`)
  - `POST /api/pipeline/pause` (`PipelinePauseHandler`)
  - `POST /api/pipeline/resume` (`PipelineResumeHandler`)
- Current behavior is not state-machine enforced:
  - `PipelineControl.pause()` and `PipelineControl.resume()` always return `{ok: true}`.
  - `PipelineControl.stop()` returns `{ok:false,error:"not_running"}` but handler maps failure to 409.
  - `PipelineControl.start()` returns `{ok:false,error:"already_running"}` but handler maps failure to 409.
- Pipeline state is now persisted in `pipeline_state` and exposed by `GET /api/pipeline` (task 010):
  - `Storage.get_pipeline_state()` and `Storage.set_pipeline_state(...)` in `backend/storage.py`.

## Approach (Minimal)
Implement a simple state machine at the handler level using `Storage.get_pipeline_state()` as the source of truth.

State values (already used by `pipeline_state`):
- `stopped`
- `running`
- `paused`

Allowed transitions:
- `stopped` -> start -> `running`
- `running` -> pause -> `paused`
- `paused` -> resume -> `running`
- `running|paused` -> stop -> `stopped`

Disallowed examples (must return 400):
- pause when `stopped`
- resume when `stopped` or already `running`
- start when already `running` or `paused`
- stop when `stopped`

## Files To Change (Implementation Phase)
- Update: `backend/app.py`
  - Add a small transition validator helper.
  - Update each pipeline control handler to:
    - Read current state from `Storage.get_pipeline_state()`.
    - Enforce allowed transitions.
    - Return 400 on invalid transition with a reason.
  - Keep the actual controller operations as-is (subprocess mgmt and pause flag).

Optional (only if needed to keep logic clean):
- Update: `backend/storage.py`
  - No new storage API required; we already have `get_pipeline_state()`.

## Implementation Details

### Error Shape and Status Codes
On invalid transition, respond with HTTP 400 and JSON:
```json
{ "ok": false, "error": "invalid_transition", "from": "stopped", "action": "pause", "detail": "cannot pause when stopped" }
```

On success, preserve current success shapes.

For controller-level failures (e.g. subprocess already running/not running), normalize to:
- 400 if it is a state violation (maps to invalid transition)
- 500 only for unexpected exceptions

### Handler-by-Handler
In `backend/app.py`:

1) `PipelineStartHandler.post`
- Read `ps = await storage.get_pipeline_state()`.
- If `ps.state != 'stopped'`: return 400 invalid_transition.
- Else call `controller.start(...)`.
- On success, set pipeline_state start (already done) and return 200.

2) `PipelinePauseHandler.post`
- If `ps.state != 'running'`: return 400 invalid_transition.
- Else call `controller.pause()`.
- On success, update pipeline_state pause.

3) `PipelineResumeHandler.post`
- If `ps.state != 'paused'`: return 400 invalid_transition.
- Else call `controller.resume()`.
- On success, update pipeline_state resume.

4) `PipelineStopHandler.post`
- If `ps.state not in ('running','paused')`: return 400 invalid_transition.
- Else call `controller.stop()`.
- On success, update pipeline_state stop.

### Keep `GET /api/pipeline` And `/api/pipeline/status`
Do not change these endpoints in this task.

## Commands To Run (Verification)
Requires a working `.env` with Postgres.

1) Prep:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 5s python -m backend.db_smoketest

timeout 10s python -m backend.apply_schema
```

2) Run backend briefly, validate transitions:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

RT_DIR="$(mktemp -d)"
export AUTOAPPDEV_RUNTIME_DIR="$RT_DIR"

timeout 12s bash -lc '
  set -euo pipefail
  cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
  python -m backend.app &
  pid=$!
  trap "kill $pid 2>/dev/null || true; wait $pid 2>/dev/null || true" EXIT

  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 0.2
    curl -fsS http://127.0.0.1:8788/api/health >/dev/null && break || true
  done

  echo "--- initial ---"
  curl -fsS http://127.0.0.1:8788/api/pipeline
  echo

  echo "--- pause while stopped (expect 400) ---"
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/pause -H "Content-Type: application/json" -d '{}'

  echo "--- start (expect 200) ---"
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/start -H "Content-Type: application/json" -d '{}'

  echo "--- start again (expect 400) ---"
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/start -H "Content-Type: application/json" -d '{}'

  echo "--- pause (expect 200) ---"
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/pause -H "Content-Type: application/json" -d '{}'

  echo "--- resume (expect 200) ---"
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/resume -H "Content-Type: application/json" -d '{}'

  echo "--- stop (expect 200) ---"
  curl -sS -o /dev/null -w "HTTP:%{http_code}\n" -X POST http://127.0.0.1:8788/api/pipeline/stop -H "Content-Type: application/json" -d '{}'
'
```

## Acceptance Criteria Checks
- Invalid transition calls return HTTP 400 with `{ ok:false, error:"invalid_transition", detail:"..." }`.
- Valid transitions return 200.
- No background processes left running after verification (wrapped in `timeout` + trap cleanup).
