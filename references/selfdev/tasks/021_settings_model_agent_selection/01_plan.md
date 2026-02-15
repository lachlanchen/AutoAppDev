# Plan: 021 settings_model_agent_selection

## Goal
Wire the PWA agent/model selection UI to backend-persisted config so the selection survives reload:
- User can pick `agent` + `model` options in the UI.
- Selection is persisted via backend (`/api/config`) and restored on reload.
- Keep default PWA theme light.

Acceptance:
- Settings UI lets user pick agent/model options.
- Selection is persisted via backend and survives reload.

## Current State (References)
- PWA already has UI controls (topbar) for agent/model:
  - `pwa/index.html`: `#agent-select`, `#model-select`
  - These are not currently wired in JS.
- Backend config persistence exists:
  - `backend/app.py`: `ConfigHandler` `GET /api/config` returns `{"config": {...}}`, `POST /api/config` upserts keys.
  - `backend/storage.py`: config stored in Postgres `app_config` (`value jsonb`) with JSON-file fallback under `runtime/state.json`.
- API contracts already document `agent` + `model` config keys:
  - `docs/api-contracts.md`: “Settings (Config)” section.
- Service worker uses cache-first for shell assets:
  - `pwa/service-worker.js`: `CACHE_NAME` currently `autoappdev-shell-v4`.

## Approach (Minimal / Incremental)
Use the existing topbar selects as the “settings” UI and persist the selected values to backend config keys:
- Config keys: `agent`, `model` (matches `docs/api-contracts.md` examples).
- On PWA boot:
  - `GET /api/config`, apply `config.agent` and `config.model` to the selects if valid.
- On selection change:
  - `POST /api/config` with `{ agent, model }`.
- Bump `pwa/service-worker.js` `CACHE_NAME` so manual verification doesn’t get stale `app.js`/`index.html`.

## Implementation Steps (Next Phase)
1. Confirm UI elements are present (no structural changes unless needed).
   - `pwa/index.html` already contains:
     - `<select id="agent-select"> ...`
     - `<select id="model-select"> ...`
   - Keep as-is to stay minimal (no new tabs/panels).

2. Add agent/model elements to the PWA element map.
   - `pwa/app.js`:
     - Extend `els` with:
       - `agentSelect: document.getElementById("agent-select")`
       - `modelSelect: document.getElementById("model-select")`

3. Load settings from backend on boot and apply to selects.
   - `pwa/app.js`:
     - Add `async function loadSettings()`:
       - `const data = await api("/api/config")`
       - `const cfg = data.config || {}`
       - If `cfg.agent` is a string and matches an enabled option, set `els.agentSelect.value`.
       - If `cfg.model` is a string and matches an enabled option, set `els.modelSelect.value`.
       - If config is missing/invalid, keep the HTML defaults (`codex`, `gpt-5.3-codex`).
     - Call `loadSettings()` from `boot()` (non-blocking is fine).

4. Persist settings to backend when the user changes them.
   - `pwa/app.js`:
     - Add `async function saveSettings()`:
       - Read `agent = els.agentSelect.value`, `model = els.modelSelect.value`.
       - `await api("/api/config", { method: "POST", body: JSON.stringify({ agent, model }) })`
       - On error: `console.warn(...)` (keep minimal; no new UI required).
     - In `bindControls()` register change handlers:
       - `els.agentSelect.addEventListener("change", saveSettings)`
       - `els.modelSelect.addEventListener("change", saveSettings)`

5. Bump service worker cache name.
   - `pwa/service-worker.js`:
     - Increment `CACHE_NAME` to `autoappdev-shell-v5` (or next integer).
   - Rationale: cache-first precache can otherwise keep old `app.js`/`index.html` during manual verification.

6. Docs check (likely no changes).
   - `docs/api-contracts.md` already documents `GET/POST /api/config` and example keys `agent`/`model`.
   - Only update docs if the implementation uses different keys (not expected).

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'id=\"agent-select\"|id=\"model-select\"' pwa/index.html
rg -n 'agentSelect|modelSelect|/api/config|loadSettings\\(|saveSettings\\(' pwa/app.js
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
timeout 5s python3 -m py_compile backend/app.py backend/storage.py
```

Manual end-to-end verification (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`.
3. Change Agent/Model selects in the topbar.
4. Confirm backend persisted:
   - `curl -s http://127.0.0.1:8788/api/config | jq`
   - Expect `config.agent` and `config.model` to match the UI.
5. Reload the page and confirm selections restore to the persisted values.

## Acceptance Checklist
- [ ] Selecting agent/model triggers `POST /api/config` and persists values.
- [ ] Reloading the PWA restores agent/model via `GET /api/config`.
- [ ] Default theme remains light.

