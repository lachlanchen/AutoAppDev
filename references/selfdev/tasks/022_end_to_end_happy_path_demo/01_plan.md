# Plan: 022 end_to_end_happy_path_demo

## Goal
Add a deterministic, end-to-end manual demo checklist to the docs that proves the controller “happy path” works:
1. Start backend
2. Apply schema
3. Open PWA
4. Send inbox message
5. Drag blocks onto canvas
6. Start pipeline
7. See logs update
8. Pause/resume
9. Stop

Acceptance:
- Docs include a deterministic manual test covering the steps above.
- Default PWA theme remains light (no theme changes required).

## Current State (References)
- Backend run + schema:
  - `backend/app.py`: starts Tornado, ensures `backend/schema.sql` on startup.
  - `backend/apply_schema.py`: CLI tool to apply `backend/schema.sql` (`python -m backend.apply_schema`).
  - `backend/README.md`: includes “Apply schema.sql” command.
- PWA shell + UI features to exercise:
  - `pwa/index.html`: Inbox tab, Blocks palette/canvas, Controls (Start/Pause/Resume/Stop), Logs tab, agent/model selects.
  - `pwa/app.js`:
    - Inbox uses `/api/inbox`
    - Pipeline controls use `/api/pipeline/start|pause|resume|stop`
    - Logs tab uses incremental `/api/logs?source=...&since=...` with Follow/Pause toggle (`#log-follow`)
- Start scripts:
  - `scripts/run_autoappdev_tmux.sh`: starts backend + PWA together (optional convenience).
- Env conventions:
  - `docs/env.md` + `.env.example` (required keys include `DATABASE_URL`, `SECRET_KEY`, `AUTOAPPDEV_PORT/PORT`).

## Approach (Minimal / Deterministic)
1. Add a single doc page with a copy/paste “happy path demo” checklist and expected outcomes.
2. Add a tiny, safe pipeline demo script that produces logs for ~60-120 seconds and respects the runtime pause flag so pause/resume is observable.
3. Keep the default pipeline (self-dev driver) unchanged; the demo uses `AUTOAPPDEV_PIPELINE_SCRIPT` to point the backend at the demo script for the duration of the checklist.

## Implementation Steps (Next Phase)
1. Add a deterministic demo pipeline script.
   - Add `scripts/pipeline_demo.sh`:
     - Prints a header line (script name, start time).
     - Loops for a fixed duration (ex: 120 iterations, 1 line/sec).
     - Checks for pause flag at `${AUTOAPPDEV_RUNTIME_DIR:-runtime}/PAUSE`:
       - If present, prints a single “paused” line and sleeps until the flag is removed.
     - Traps SIGTERM/SIGINT and exits cleanly (so Stop is immediate and predictable).
     - Writes only to stdout/stderr (captured into `runtime/logs/pipeline.log` by backend).

2. Add the end-to-end demo checklist doc.
   - Add `docs/end-to-end-demo-checklist.md` containing:
     - Preconditions:
       - `.env` exists and includes `DATABASE_URL`, `SECRET_KEY`, `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT` (or `PORT`).
       - Postgres is reachable.
       - Python env ready (reference `./scripts/setup_autoappdev_env.sh`).
     - Step-by-step commands:
       - Apply schema: `conda run -n autoappdev python -m backend.apply_schema`
       - Start backend with demo script (so Start button is safe/deterministic):
         - `export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh`
         - `conda run -n autoappdev python -m backend.app`
       - Start PWA server:
         - `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
       - Open PWA and verify:
         - Status badges show Backend ok + DB ok.
         - Pipeline shows `stopped/idle` initially.
       - Inbox:
         - Send a message in Inbox tab.
         - Expected: message appears in list and a file appears under `runtime/inbox/`.
       - Blocks:
         - Drag 2-3 blocks to canvas; click “Export JSON” (optional) and/or “Send Plan” (optional).
       - Pipeline:
         - Click Start; expected: Pipeline state becomes `running`, PID appears.
         - Logs tab: expected: lines append over time; follow mode auto-scrolls.
         - Toggle Follow off (Pause): expected: no forced auto-scroll; selection/copy works.
         - Click Pause (pipeline control): expected: pipeline state becomes `paused`.
         - Click Resume: expected: pipeline state becomes `running`.
         - Click Stop: expected: pipeline state becomes `stopped`, PID clears, demo script exits.
     - Troubleshooting section:
       - Missing env vars -> link to `docs/env.md`.
       - Schema apply errors -> verify Postgres and `DATABASE_URL`.
       - If Start returns 400 “invalid transition” -> ensure pipeline is stopped first.

3. Link the new doc from an existing entrypoint (minimal).
   - Update `README.md` “Contents” list to include `docs/end-to-end-demo-checklist.md`.
   - (Optional) Add a short link section to `docs/controller-mvp-scope.md` under MVP Screens or APIs.

4. No backend/PWA feature changes expected.
   - This task is documentation + a small demo script only.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n \"end-to-end-demo-checklist\" README.md docs/controller-mvp-scope.md || true
test -f docs/end-to-end-demo-checklist.md
test -f scripts/pipeline_demo.sh

# Ensure docs mention required steps/endpoints
rg -n \"apply_schema|backend\\.apply_schema|/api/inbox|/api/pipeline|/api/logs|AUTOAPPDEV_PIPELINE_SCRIPT\" docs/end-to-end-demo-checklist.md
```

Manual verification (outside this sandbox, which cannot bind ports):
1. Follow `docs/end-to-end-demo-checklist.md` exactly.
2. Confirm each expected outcome in the checklist.

## Acceptance Checklist
- [ ] `docs/end-to-end-demo-checklist.md` exists and contains a deterministic manual test covering: backend start, schema apply, PWA open, inbox send, blocks drag, pipeline start, logs visible, pause/resume, stop.
- [ ] Demo uses a safe deterministic pipeline script (no git/codex side-effects) and is selectable via `AUTOAPPDEV_PIPELINE_SCRIPT`.
- [ ] README links to the checklist doc (or another obvious entrypoint does).

