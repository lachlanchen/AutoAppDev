# Plan: 019 controls_buttons_wiring

## Goal
Make the pipeline control buttons behave correctly:
- Buttons call the pipeline control endpoints (already wired).
- UI disables invalid actions based on current pipeline state.
- UI shows an error message when the backend returns HTTP 400 (invalid transition, etc).

Acceptance:
- Buttons call `/api/pipeline/start|pause|resume|stop`.
- UI disables invalid actions based on current state.
- UI shows error text on 400.
- Default PWA theme remains light.

## Current State (References)
- Buttons already exist in `pwa/index.html`:
  - `#btn-start`, `#btn-pause`, `#btn-resume`, `#btn-stop`
- Buttons are wired in `pwa/app.js` `bindControls()`:
  - `POST /api/pipeline/start` (shows `alert()` on error)
  - `POST /api/pipeline/pause|resume|stop` (errors are currently ignored)
- Current state is polled every 2s:
  - `pwa/app.js` `refreshStatus()` calls `GET /api/pipeline/status` and updates `#pipeline-status` / `#pipeline-pid`.
- Backend enforces transitions and returns 400 with details:
  - `backend/app.py` `PipelineStartHandler|PipelinePauseHandler|PipelineResumeHandler|PipelineStopHandler`
  - Error shape includes `{ ok:false, error:"invalid_transition", from, action, detail }` (see `docs/api-contracts.md`).
- CSS currently has no disabled styling:
  - `pwa/styles.css` defines `.btn` but no `.btn:disabled`.

## Approach (Minimal / Incremental)
1. Use the polled pipeline state from `GET /api/pipeline/status` to compute which actions are valid.
2. Set `disabled` on the buttons accordingly.
3. Add a small inline control message area to show 400 errors (and clear it on success).
4. Add minimal CSS for disabled buttons and the message text.

State mapping (from `status.state`):
- Treat `running` as running.
- Treat `paused` as paused.
- Treat `idle|stopped|completed|failed|unknown` as “not running” (start allowed).

Button enable rules:
- Start enabled only when not running/paused.
- Pause enabled only when running.
- Resume enabled only when paused.
- Stop enabled when running or paused.

## Implementation Steps (Next Phase)
1. Add a control message element in `pwa/index.html`.
   - In the top bar `.controls` (near the buttons), add:
     - `<span class="ctrl-msg" id="ctrl-msg" aria-live="polite"></span>`
   - Keep existing layout and `<body data-theme="light">` unchanged.

2. Add minimal CSS in `pwa/styles.css`.
   - Add:
     - `.btn:disabled { opacity: 0.55; cursor: not-allowed; }`
     - `.btn:disabled:active { transform: none; }`
   - Add `.ctrl-msg` styles (small, non-intrusive):
     - font-size 11-12px, muted default, red for error (ex: `.ctrl-msg.is-error`).

3. Update `pwa/app.js` to disable buttons based on current state.
   - Extend `els` with `ctrlMsg: document.getElementById("ctrl-msg")`.
   - Add helper functions:
     - `normalizePipelineState(state)` -> `"running"|"paused"|"stopped"`.
     - `updateActionButtons(state)` sets `.disabled` on `els.start/pause/resume/stop`.
     - `setCtrlMsg(text, {error:boolean})` updates `#ctrl-msg`.
   - Call `updateActionButtons(...)` from `refreshStatus()`:
     - On successful fetch: compute normalized state and update buttons.
     - On failure: set a safe default (disable all, or enable only Start) and set `#pipeline-status` to unknown (existing behavior already does unknown).

4. Update pipeline button handlers to show error text on 400.
   - Wrap calls in a single helper `doPipelineAction(name, fn)`:
     - Clears previous message.
     - Runs the API call.
     - If it throws and `e.status === 400`:
       - Prefer `e.data.detail` (api-client sets `err.data = data`) and display it in `#ctrl-msg` with error styling.
       - Fall back to `e.message`.
     - Always call `refreshStatus()` at the end to resync button disabled states.
   - Replace the current `alert()` for Start with the same inline error display.
   - Stop ignoring errors for pause/resume/stop; display inline error on 400.

5. (Recommended) Bump service worker cache name in `pwa/service-worker.js`.
   - The SW uses cache-first for shell assets; changing `app.js`/`index.html` can appear stale without a cache bump.
   - Increment `CACHE_NAME` (ex: `autoappdev-shell-v3`) for reliable manual verification.

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n 'id=\"ctrl-msg\"' pwa/index.html
rg -n '\\.btn:disabled|ctrl-msg' pwa/styles.css
rg -n 'updateActionButtons\\(|normalizePipelineState\\(|doPipelineAction\\(|ctrlMsg' pwa/app.js

# Ensure endpoints still referenced
rg -n '/api/pipeline/(start|pause|resume|stop)' pwa/app.js

# Ensure default theme remains light
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Manual UI verification (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Confirm disabled states:
   - When stopped: Start enabled; Pause/Resume/Stop disabled.
   - When running: Pause/Stop enabled; Start/Resume disabled.
   - When paused: Resume/Stop enabled; Start/Pause disabled.
3. Force an invalid transition (race or manual) and confirm HTTP 400 shows an inline error message (no page reload).

## Acceptance Checklist
- [ ] Buttons are enabled/disabled based on current pipeline state.
- [ ] Attempting an invalid transition results in visible error text on 400.
- [ ] Default theme remains light.

