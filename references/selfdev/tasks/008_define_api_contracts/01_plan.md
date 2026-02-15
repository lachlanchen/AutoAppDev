# Plan: 008 define_api_contracts

## Goal
Write an API contract doc that lists request/response shapes (with example JSON) for:
- Inbox messages (chat/inbox)
- Pipeline controls
- Logs view
- Settings

Acceptance:
- Docs list request/response shapes for: inbox messages, pipeline controls, logs, and settings.
- Includes example JSON payloads.

This phase (PLAN) does not modify code.

## Current State (References)
Backend routes currently implemented in `backend/app.py`:
- `GET /api/health`
- `GET /api/version`
- `GET|POST /api/config`
- `GET|POST /api/chat`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start|stop|pause|resume`
- `GET /api/logs/tail`

PWA currently calls these endpoints in `pwa/app.js`:
- `/api/health`
- `/api/chat?limit=50` and `POST /api/chat { content }`
- `/api/pipeline/status`
- `/api/pipeline/start|pause|resume|stop`
- `/api/logs/tail?name=...&lines=...`

Design note from `docs/controller-mvp-scope.md`:
- “Chat/Inbox” is the UI term; the backend uses `/api/chat` and also writes file artifacts under `runtime/inbox/`.

## Files To Change (Implementation Phase)
- Add: `docs/api-contracts.md`
  - This doc is the contract reference for frontend + backend.
- Update: `README.md`
  - Add a single bullet under Contents linking to `docs/api-contracts.md`.
- Optional (keep minimal): update `docs/controller-mvp-scope.md` to link to `docs/api-contracts.md`.

## Doc Outline For `docs/api-contracts.md`
Keep it short, concrete, and focused on the four required areas.

1) **General Conventions**
- Base URL and JSON content-type.
- Common error shape (what clients should expect):
  - Non-2xx with `{ "error": "..." }` (matches `BaseHandler.write_json` usage and `pwa/app.js` error parsing).

2) **Settings (Config)**
- `GET /api/config`
  - Response: `{ "config": { <key>: <json_value>, ... } }`
  - Example response includes agent/model selection keys used by PWA (`agent`, `model`).
- `POST /api/config`
  - Request: JSON object of key/value pairs.
  - Response: `{ "ok": true }`
  - Example request/response.

3) **Inbox Messages (Chat)**
Define “Inbox” as:
- API: chat messages list + send message (`/api/chat`).
- Side effect: sent messages also land in `runtime/inbox/` as `*_user.md` files for pipeline scripts.

- `GET /api/chat?limit=N`
  - Response: `{ "messages": [ { "id", "role", "content", "created_at" }, ... ] }`
  - Note: storage fallback may omit `id/created_at` (file-state). Document as “may be missing” if relevant, or state “backend will provide” if you plan to enforce it soon.
- `POST /api/chat`
  - Request: `{ "content": "..." }`
  - Response: `{ "ok": true }` or `{ "error": "empty" }`.
  - Example payloads.

4) **Pipeline**
- `GET /api/pipeline/status`
  - Response: `{ "status": { "running": bool, "pid": int|null, "run_id": int|null, "state": "idle|running|paused|stopped|..." } }`
  - Example response.
- `POST /api/pipeline/start`
  - Request: `{ "script"?: string, "cwd"?: string, "args"?: string[] }` (optional fields supported by backend).
  - Success: `{ "ok": true, "pid": int, "run_id": int }`
  - Errors: 409 already_running; 404 script_not_found; 400 args_must_be_list/script_outside_repo.
  - Example start request/response.
- `POST /api/pipeline/stop|pause|resume`
  - Request body may be `{}`.
  - Response: `{ "ok": true }` or conflict `{ "ok": false, "error": "not_running" }`.

5) **Logs**
- `GET /api/logs/tail?name=pipeline|backend&lines=N`
  - Response: `{ "name": "pipeline", "lines": ["...", ...] }`
  - Errors: `{ "error": "unknown_log" }`.
  - Example response.

6) **Non-Goals / Stability**
- Clarify this is a lightweight, versionless contract for now.
- Note: `/api/version` exists for build id; optionally include it as a small appendix.

## Implementation Steps (Next Phase)
1. Create `docs/api-contracts.md` with the outline above.
2. Update `README.md` Contents to link to `docs/api-contracts.md`.
3. (Optional) Add a single link in `docs/controller-mvp-scope.md` to the contract doc.

## Commands To Run (Verification)
Doc-only verification:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# File exists and has the required sections
test -s docs/api-contracts.md

# Ensure it documents the required areas
rg -n "Settings|Config|/api/config" docs/api-contracts.md
rg -n "Inbox|Chat|/api/chat" docs/api-contracts.md
rg -n "Pipeline|/api/pipeline" docs/api-contracts.md
rg -n "Logs|/api/logs/tail" docs/api-contracts.md

# Ensure it includes example JSON payloads
rg -n "\\{[[:space:]]*\"" docs/api-contracts.md

# README link present
rg -n "docs/api-contracts\\.md" README.md
```

## Acceptance Criteria Checks
- `docs/api-contracts.md` exists and includes request/response shapes + example JSON for:
  - inbox messages, pipeline controls, logs, settings.
- Doc is consistent with existing backend routes in `backend/app.py` and current frontend calls in `pwa/app.js`.
