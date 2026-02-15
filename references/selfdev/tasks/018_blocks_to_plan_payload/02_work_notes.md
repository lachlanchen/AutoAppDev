# Work Notes: 018 blocks_to_plan_payload

## Summary of Changes
- Defined a minimal, versioned plan payload derived from the PWA workspace `program` blocks.
- Backend now recognizes and stores the plan payload:
  - Added `PlanHandler` in `backend/app.py` with `GET /api/plan` and `POST /api/plan`.
  - Validates `{ kind: "autoappdev_plan", version: 1, steps: [...] }` and stores it under config key `pipeline_plan` (via `app_config`).
- PWA can transform blocks -> plan payload and post it:
  - `pwa/index.html` adds a “Send Plan” button (`#btn-send-plan`) in the Program panel.
  - `pwa/app.js` adds `programToPlan()` + `sendPlan()` and posts to `/api/plan`, rendering the ack in the existing `#export` area.
- Docs updated:
  - `docs/api-contracts.md` documents `GET/POST /api/plan`.
- Service worker cache name bumped (`pwa/service-worker.js`) to reduce stale shell assets during manual verification.

## Files Changed
- Updated: `backend/app.py`
- Updated: `docs/api-contracts.md`
- Updated: `pwa/index.html`
- Updated: `pwa/app.js`
- Updated: `pwa/service-worker.js`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'class PlanHandler|/api/plan' backend/app.py
rg -n 'btn-send-plan|programToPlan\\(|/api/plan' pwa/index.html pwa/app.js
rg -n '## Plan Payload|GET /api/plan|POST /api/plan' docs/api-contracts.md

timeout 5s node --check pwa/app.js
timeout 5s python3 -m py_compile backend/app.py
```

