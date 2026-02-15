# Summary: 018 blocks_to_plan_payload

## What Changed
- Added a backend-recognized plan payload + storage endpoint:
  - `backend/app.py`: new `PlanHandler` with `GET /api/plan` and `POST /api/plan`.
  - Validates `{ kind: "autoappdev_plan", version: 1, steps: [...] }` and stores it as config key `pipeline_plan` (in `app_config`).
- Added PWA “Send Plan” flow:
  - `pwa/index.html`: new button `#btn-send-plan` in the Program panel.
  - `pwa/app.js`: `programToPlan()` transforms workspace blocks into the plan payload and `sendPlan()` posts it to `/api/plan`, showing the ack in `#export`.
- Documented the endpoint:
  - `docs/api-contracts.md`: “Plan Payload” section for `GET/POST /api/plan`.
- Bumped the service worker cache name:
  - `pwa/service-worker.js`: `CACHE_NAME` -> `autoappdev-shell-v2` to reduce stale shell assets during manual verification.

## Why
To make the workspace blocks exportable as a backend-recognized plan payload and allow the PWA to post it to the backend and get an acknowledgment (without a page reload).

## How To Verify
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
rg -n 'class PlanHandler|\\(r\"/api/plan\"|/api/plan' backend/app.py
rg -n 'btn-send-plan|programToPlan\\(|/api/plan' pwa/index.html pwa/app.js
rg -n '## Plan Payload|GET /api/plan|POST /api/plan' docs/api-contracts.md
timeout 5s node --check pwa/app.js
timeout 5s python3 -m py_compile backend/app.py
```

Manual end-to-end check (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`, drag blocks into the canvas.
3. Click “Send Plan”; confirm `POST /api/plan` returns `{ "ok": true }` and the ack renders in the UI.
4. (Optional) Confirm `GET /api/plan` returns the stored payload.

