# End-to-End Demo Checklist (Happy Path)

This checklist is a deterministic manual test for the AutoAppDev controller (Tornado backend + PWA).

Goal: prove you can start backend, apply schema, open PWA, send inbox message, drag blocks, start pipeline, see logs, pause/resume, and stop.

## Preconditions
- You are in the repo root: `/home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev`
- You have a `.env` file:
  - `cp .env.example .env`
  - Set at least:
    - `DATABASE_URL` (Postgres connection string)
    - `SECRET_KEY` (any non-empty value in dev)
    - `AUTOAPPDEV_HOST` (default `127.0.0.1`)
    - `AUTOAPPDEV_PORT` (default `8788`) or `PORT`
- Backend python env is ready:
  - `./scripts/setup_autoappdev_env.sh`

## 1) Apply Schema (Idempotent)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
conda run -n autoappdev python -m backend.apply_schema
```
Expected:
- Prints `OK: schema applied`

## 2) Start Backend (Use Deterministic Demo Pipeline)
This demo uses a safe pipeline script that only prints log lines and respects the runtime pause flag.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Expected:
- Backend starts on `http://127.0.0.1:8788` (or your configured host/port).
- Startup prints DB time (proof DB is reachable).

## 3) Start PWA Static Server
In another terminal:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev/pwa
python3 -m http.server 5173 --bind 127.0.0.1
```
Open:
- `http://127.0.0.1:5173/`

Expected:
- Default theme is light.
- Status tab:
  - Backend: `ok`
  - DB: `ok`
  - Pipeline: `stopped`/`idle` (initially)

## 4) Inbox Message
1. Open the **Inbox** tab.
2. Send a short message, e.g. `hello pipeline`.

Expected:
- The message appears in the inbox list.
- A new file appears under `runtime/inbox/` (e.g. `*_user.md`).

## 5) Drag Blocks and (Optional) Send Plan
1. Drag a few blocks into the canvas (e.g. Plan, Work, Summary).
2. Optional: click `Export JSON` to see the program JSON.
3. Optional: click `Send Plan` to post the plan payload to backend.

Expected:
- Blocks appear on canvas.
- `Send Plan` returns an `ok` ack (rendered in the export panel).

## 6) Start Pipeline
1. Click **Start** in the top bar.
2. Watch the Status panel.

Expected:
- Pipeline status becomes `running`.
- PID becomes a number.
- Start becomes disabled; Pause/Stop become enabled.

## 7) Observe Logs (Incremental + Follow/Pause)
1. Open the **Logs** tab.
2. Ensure the follow toggle is enabled (button label shows `Pause`).

Expected:
- New log lines append over time (demo prints `tick N/M`).
- View auto-scrolls to the bottom while following.

Pause log follow (for selection/copy):
1. Click the follow toggle so it shows `Follow`.
2. Select some text in the log view and copy it.

Expected:
- View does not force-scroll while follow is paused.
- Copy works (browser selection).

## 8) Pause/Resume Pipeline
1. Click **Pause** (pipeline control).
2. Wait a moment, then click **Resume**.

Expected:
- Status panel shows `paused` after Pause, then `running` after Resume.
- Logs show a `[demo] paused ...` line and later a `[demo] resumed` line.

## 9) Stop Pipeline
1. Click **Stop**.

Expected:
- Status becomes `stopped`.
- PID clears (`-`).
- Logs show a stop/exit line from the demo script.

## Troubleshooting
- If backend refuses to start with missing env vars:
  - Follow `docs/env.md` and ensure `DATABASE_URL` is set.
- If Start returns HTTP 400 invalid transition:
  - Ensure the pipeline is currently stopped, then try Start again.
- If logs don’t show:
  - Confirm backend is running and `runtime/logs/pipeline.log` exists and is changing.
  - In the PWA Logs tab, click `Refresh` to reset the cursor and reload the last window.

