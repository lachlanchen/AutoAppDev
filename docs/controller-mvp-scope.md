# AutoAppDev Controller MVP Scope

## Purpose
AutoAppDev is a Scratch-like PWA for controlling and observing a long-running auto-development pipeline. The controller UI is static HTML/CSS/JS, backed by a Python Tornado API with PostgreSQL for persistence (config, messages, run status) and a small runtime directory for inbox + logs.

Default UI theme: light.

## MVP Screens (PWA)
The MVP controller is considered usable when it has these screens/panels and they are wired to minimal APIs.

- Blocks
  - A small block palette (Plan/Work/Debug/Fix/Summary/Release, etc.)
  - Drag blocks onto a canvas to form a linear “program”
  - Export the program as JSON
- Chat/Inbox
  - See recent messages
  - Send guidance while the pipeline is running
- Pipeline Controls
  - Start / Pause / Resume / Stop
  - Show current state and PID
- Logs
  - Tail backend and pipeline logs
  - Manual refresh (polling is fine for MVP)
- Settings
  - Select agent and model (UI first; persistence via backend config)

## Minimal Backend APIs
This is the minimal API surface that makes the controller functional. The current implementation lives in `backend/app.py`.

- Health
  - `GET /api/health` -> `{ "ok": true, "service": "autoappdev-backend" }`
- Settings/config
  - `GET /api/config` -> `{ "config": { ... } }`
  - `POST /api/config` with JSON object body -> `{ "ok": true }`
- Chat
  - `GET /api/chat?limit=N` -> `{ "messages": [...] }`
  - `POST /api/chat` with `{ "content": "..." }` -> `{ "ok": true }`
- Pipeline status
  - `GET /api/pipeline/status` -> `{ "status": { "running": bool, "pid": int|null, "run_id": int|null, "state": "..." } }`
- Pipeline control
  - `POST /api/pipeline/start` -> `{ "ok": true, "pid": int, "run_id": int }` (or `{ "ok": false, "error": "..." }`)
  - `POST /api/pipeline/stop|pause|resume` -> `{ "ok": true }` (or conflict/error)
- Logs
  - `GET /api/logs/tail?name=pipeline|backend&lines=N` -> `{ "name": "...", "lines": ["..."] }`

## Runtime Artifacts
The controller and pipeline exchange a few file-based artifacts under the runtime directory.

- `runtime/inbox/`
  - Chat messages are written as individual `*_user.md` files so shell scripts can consume guidance during a run.
- `runtime/logs/`
  - `backend.log` for Tornado logs
  - `pipeline.log` for the pipeline subprocess output
- `references/selfdev/`
  - Task plans, work notes, summaries, and other self-development state

## Non-Goals (For MVP)
- Authentication / multi-user
- Full Scratch compatibility (nesting, variables, custom blocks, complex control flow)
- Websocket streaming logs (simple polling/tail endpoints are enough)
- Robust job orchestration across restarts (reattaching to a prior pipeline process)
