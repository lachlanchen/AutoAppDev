# Plan: 001 define_controller_mvp_scope

## Goal
Add a short, readable (<5 minutes) doc section that defines the AutoAppDev controller MVP scope:
- Required screens: blocks, chat/inbox, controls, logs, settings.
- Minimal backend APIs that make the PWA usable.

This phase writes docs only (no code changes).

## Existing Reference Points (Do Not Change In This Task)
- Backend routes already exist in `backend/app.py`:
  - `GET /api/health`
  - `GET|POST /api/config`
  - `GET|POST /api/chat`
  - `GET /api/pipeline/status`
  - `POST /api/pipeline/start|stop|pause|resume`
  - `GET /api/logs/tail`
- Current controller UI scaffold already exists in `pwa/index.html` and `pwa/app.js`:
  - Blocks toolbox + draggable canvas + export
  - Tabs for Status / Chat / Logs
  - Start/Stop/Pause/Resume controls
  - Theme toggle (default light)

## Files To Change
- Add: `docs/controller-mvp-scope.md`
- Update: `README.md` (add a single bullet under Contents linking to the new doc)

## Content Outline For `docs/controller-mvp-scope.md`
Keep it short (target 60-120 lines). Use simple headings and bullet lists.

1. **Purpose**
- One paragraph: “Scratch-like PWA to control/observe the auto-development pipeline, with a Tornado+Postgres backend.”

2. **MVP Screens (PWA)**
- Blocks: palette + canvas + program list + export JSON.
- Chat/Inbox: send guidance; see recent messages.
- Pipeline Controls: start/stop/pause/resume; show state + PID.
- Logs: tail backend/pipeline logs; refresh.
- Settings: agent + model selection (UI now; persistence later).
- Theme: default light (explicitly state).

3. **Minimal Backend API Surface**
List endpoints and the minimum semantics the PWA expects. Keep to what exists today in `backend/app.py`, but note any “next” additions as non-blocking.
- Health: `GET /api/health` returns `{ ok: true }`.
- Config/settings: `GET|POST /api/config` for agent/model settings (already present; persistence details handled elsewhere).
- Chat: `GET /api/chat?limit=N`, `POST /api/chat { content }`.
- Pipeline state: `GET /api/pipeline/status`.
- Pipeline control: `POST /api/pipeline/start|stop|pause|resume`.
- Logs: `GET /api/logs/tail?name=pipeline|backend&lines=N`.

4. **Runtime Directories / Artifacts**
Document the intended runtime artifacts (align with `backend/app.py` and task context):
- `runtime/inbox/` message files written for the running pipeline.
- `runtime/logs/` backend + pipeline logs.
- `references/selfdev/` tasks and state.

5. **Non-Goals (For MVP)**
A short list to prevent scope creep (examples):
- Auth/multi-user
- Complex Scratch control flow / nesting / parameter blocks
- Robust streaming logs or websockets

## Implementation Steps (Next Phase)
1. Create `docs/controller-mvp-scope.md` with the outline above.
2. Edit `README.md` to add one bullet in Contents linking to `docs/controller-mvp-scope.md`.

## Commands To Run (Verification)
Doc-only verification (no servers required):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# File exists and non-empty
test -s docs/controller-mvp-scope.md

# Quick scan (top of doc)
sed -n '1,120p' docs/controller-mvp-scope.md

# Ensure required screens are explicitly mentioned
rg -n "Blocks|Chat|Inbox|Controls|Logs|Settings|Theme" docs/controller-mvp-scope.md

# Ensure minimal API list is present (and matches current backend)
rg -n "/api/health|/api/config|/api/chat|/api/pipeline/status|/api/pipeline/(start|stop|pause|resume)|/api/logs/tail" docs/controller-mvp-scope.md
```

Optional consistency check against backend routes:
```bash
rg -n "/api/" backend/app.py
```

## Acceptance Criteria Checks
- `docs/controller-mvp-scope.md` exists, is non-empty, and is readable in under ~5 minutes.
- The doc explicitly lists the required screens: blocks, chat/inbox, controls, logs, settings.
- The doc lists the minimal backend APIs (matching existing routes in `backend/app.py`).
- `README.md` Contents includes a link to the new doc.
