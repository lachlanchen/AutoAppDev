# Plan: 018 blocks_to_plan_payload

## Goal
Convert the current PWA workspace (`program` blocks) into a backend-recognized “plan payload”, and add a UI button that posts the plan to the backend and receives an ack.

Acceptance:
- Workspace JSON can be transformed into a backend-recognized plan payload.
- PWA has a UI button to post the plan to backend and get an ack.
- Default PWA theme remains light.

## Current State (References)
- Workspace JSON (blocks program) already exists in the PWA:
  - `pwa/app.js`: `program` array + `persistProgram()` / `loadProgram()`; “Export JSON” renders `JSON.stringify({ program }, ...)`.
  - `pwa/index.html`: “Program” panel includes `#btn-export` and `#export`.
- Backend has a generic config store:
  - DB table: `backend/schema.sql` `app_config(key, value jsonb)`.
  - API: `GET /api/config` and `POST /api/config` in `backend/app.py` (`ConfigHandler`), documented in `docs/api-contracts.md`.
- There is no dedicated “plan” endpoint yet.

## Approach (Minimal / Incremental)
1. Define a minimal plan payload shape (versioned) derived from the workspace JSON.
2. Add a dedicated backend endpoint `POST /api/plan` (and optional `GET /api/plan`) that validates the payload shape and stores it under a single config key (ex: `pipeline_plan`).
3. Add a “Send Plan” button in the PWA Program panel that:
   - transforms `program` -> plan payload,
   - posts to `/api/plan`,
   - shows the ack (without page reload).
4. Keep the UI/layout and default light theme unchanged.

## Proposed Plan Payload (Backend-Recognized)
Store a single JSON object under key `pipeline_plan`:
```json
{
  "kind": "autoappdev_plan",
  "version": 1,
  "steps": [
    { "id": 1, "block": "plan" },
    { "id": 2, "block": "work" }
  ]
}
```

Rules (minimal validation):
- Body must be a JSON object.
- `kind` must equal `autoappdev_plan`.
- `version` must equal `1`.
- `steps` must be a list of objects with `id` (int) and `block` (string).

## Implementation Steps (Next Phase)
1. Backend: add a plan endpoint in `backend/app.py`.
   - Add `PlanHandler` near `ConfigHandler`.
   - `POST /api/plan`:
     - Parse JSON body.
     - Validate against the rules above.
     - Store via `await storage.set_config("pipeline_plan", body)`.
     - Respond `{ "ok": true }`.
   - (Optional but helpful for verification) `GET /api/plan`:
     - Read `await storage.get_config()` and return `{ "plan": cfg.get("pipeline_plan") }`.
   - Register route in `make_app()`:
     - Add `(r"/api/plan", PlanHandler, {"storage": storage})`.

2. Docs: update `docs/api-contracts.md`.
   - Add a new section (ex: “Plan Payload”) documenting:
     - `POST /api/plan` request/response and validation errors.
     - Optional `GET /api/plan` response.
     - Include the plan payload example above.

3. PWA: add a “Send Plan” button in `pwa/index.html`.
   - In the “Program” panel actions, add a new button next to Export:
     - `id="btn-send-plan"`, label “Send Plan”.
   - Keep light theme default unchanged (`<body data-theme="light">`).

4. PWA: implement block->plan transform + POST in `pwa/app.js`.
   - Extend `els` with `sendPlanBtn: document.getElementById("btn-send-plan")`.
   - Add `programToPlan(program)`:
     - Converts `[{type:"plan"}, ...]` into `{kind, version, steps:[{id, block}, ...]}`.
     - Handles empty program: either refuse to send (show message) or send `steps: []` (prefer refuse).
   - Add `sendPlan()`:
     - Builds payload from current `program`.
     - `await api("/api/plan", { method: "POST", body: JSON.stringify(payload) })`.
     - Show ack in the existing `#export` area (set `hidden=false` and print the ack JSON), or use a minimal `alert()` on success.
   - Wire click handler in `bindControls()`:
     - `els.sendPlanBtn.addEventListener("click", sendPlan)`.

5. (Recommended) Service worker cache bump in `pwa/service-worker.js`.
   - Current SW uses cache-first for shell assets and can serve stale `app.js`/`index.html`.
   - Bump `CACHE_NAME` (ex: `autoappdev-shell-v2`) so manual verification reliably sees new UI without requiring cache clearing.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# PWA wiring
rg -n 'btn-send-plan' pwa/index.html pwa/app.js
rg -n 'programToPlan\\(' pwa/app.js
rg -n '/api/plan' pwa/app.js backend/app.py docs/api-contracts.md

# Ensure default light theme remains
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

# Syntax checks
timeout 5s node --check pwa/app.js
timeout 5s python3 -m py_compile backend/app.py
```

Manual end-to-end check (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`.
3. Drag blocks into the canvas to build a `program`.
4. Click “Send Plan”; confirm:
   - Network: `POST /api/plan` returns `{ "ok": true }`.
   - UI shows an ack without a full page reload.
5. (If GET is implemented) `GET /api/plan` returns the stored payload.

## Acceptance Checklist
- [ ] `program` blocks can be transformed into the defined plan payload.
- [ ] PWA “Send Plan” posts to backend and receives `{ok:true}` (ack) without page reload.
- [ ] Default theme remains light.

