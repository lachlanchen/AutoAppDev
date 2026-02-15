# Plan: 020 logs_panel_incremental_view

## Goal
Upgrade the PWA Logs panel so it behaves like a basic log viewer:
- Polls (or streams) **incremental** logs (append-only, not full replace each refresh).
- **Auto-scrolls** to the bottom while “follow” is enabled.
- Provides a **pause toggle** to stop auto-scroll (so the user can read/select/copy).
- User can **copy selected text** from the log view.

Acceptance:
- Logs panel polls/streams incremental logs.
- Auto-scroll with a pause toggle.
- Selected text can be copied.
- Default PWA theme remains light (`<body data-theme="light">`).

## Current State (References)
- PWA logs UI:
  - `pwa/index.html`: Logs tab contains:
    - `#log-select` (pipeline/backend)
    - `#log-refresh` button
    - `#logview` `<pre>` where logs render
- PWA logs behavior:
  - `pwa/app.js`:
    - `refreshLogs()` calls `GET /api/logs/tail?name=...&lines=400`
    - Replaces `#logview.textContent` each time (not incremental)
    - Polling runs every ~2.5s only when Logs tab is visible (`if (!els.tabLogs.hidden) refreshLogs()`)
- Backend already supports incremental log reads:
  - `backend/app.py`: `LogsSinceHandler` is mounted at `GET /api/logs?source=...&since=...&limit=...`
  - Uses `LogBuffer` + `FileLogTailer` to track appended lines with monotonic `id`.
- API is already documented:
  - `docs/api-contracts.md`: “Logs” section includes `GET /api/logs` and `GET /api/logs/tail`.

## Approach (Minimal / Incremental)
Use the existing backend incremental endpoint (`GET /api/logs`) and make the PWA:
1. Track a per-source cursor (`since`) so each poll fetches only new entries.
2. Append new lines to `#logview` without re-rendering the whole `<pre>` (reduces selection disruption).
3. Auto-scroll only when “follow” is enabled; pause toggle disables follow so the user can select/copy.

## Implementation Steps (Next Phase)
1. Add a pause/follow toggle control in the Logs panel.
   - Edit `pwa/index.html` in the Logs tab `.logbar`:
     - Add a new button, e.g.:
       - `<button class="btn btn--ghost" id="log-follow" aria-pressed="true" title="Toggle auto-scroll (pause to select/copy)">Pause</button>`
     - Keep existing `#log-refresh` and `#log-select` unchanged.

2. Add minimal styling (only if needed for clarity/usability).
   - Edit `pwa/styles.css`:
     - Ensure logs are selectable (explicit is fine): `.logview { user-select: text; }`
     - Optional: add a subtle “pressed” style using `aria-pressed` if the toggle needs affordance (keep small).

3. Switch PWA logs from tail-replace to incremental-append.
   - Edit `pwa/app.js`:
     - Extend `els` with `logFollow: document.getElementById("log-follow")`.
     - Add state:
       - `const logSince = { pipeline: 0, backend: 0 };`
       - `let logFollow = true;` (default: follow enabled)
     - Add helpers:
       - `setLogFollow(on)`:
         - sets `logFollow`
         - updates `#log-follow` label (`Pause` when follow=true, `Follow` or `Resume` when follow=false)
         - updates `aria-pressed`
         - when turning follow on, scroll to bottom immediately
       - `appendLogText(text)`:
         - use `els.logview.insertAdjacentText("beforeend", text)` (append-only)
       - `scrollLogsToBottom()`:
         - scroll the correct container; prefer `els.logview` if it is the scroller, otherwise fall back to `els.tabLogs`
       - `pollLogsIncremental({ reset })`:
         - Determine `source` from `els.logSelect.value`
         - If `reset`:
           - clear `#logview`
           - set `logSince[source] = 0`
           - fetch a larger window once: `GET /api/logs?source=...&since=0&limit=2000`
           - render only the last N entries (e.g. 400) but set cursor to `next` from the response
         - Else:
           - fetch `GET /api/logs?source=...&since=<cursor>&limit=400`
           - append new lines; update cursor to `next`
         - If `logFollow` is true, call `scrollLogsToBottom()` after appending.
     - Wiring changes:
       - Replace the old `refreshLogs()` implementation with the incremental poller (keep the function name if you want minimal callsite changes).
       - `#log-refresh` should trigger a reset reload (clear + reset cursor + fetch last window).
       - On `#log-select` change, reset view and cursor, then fetch the initial window.
       - In the existing 2.5s interval block, call the incremental poller when Logs tab is visible.
       - When switching to the Logs tab, trigger an immediate poll so the user sees fresh logs without waiting for the interval.

4. Bump service worker cache name (recommended).
   - If `pwa/index.html` / `pwa/styles.css` / `pwa/app.js` are modified, edit `pwa/service-worker.js`:
     - Increment `CACHE_NAME` (e.g., `autoappdev-shell-v4`) to reduce stale shell assets during manual verification.

5. Docs (optional)
   - No backend API changes are expected; `docs/api-contracts.md` already documents `GET /api/logs`.
   - Only update docs if new UI controls need to be mentioned somewhere (likely not needed for this small step).

## Commands To Run (Verification)
Static checks (safe in this sandbox):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# New UI elements
rg -n 'id=\"log-follow\"' pwa/index.html

# Ensure incremental endpoint used from PWA
rg -n '/api/logs\\?source=|/api/logs\\b' pwa/app.js

# Ensure pause/follow + append logic exists
rg -n 'logSince|setLogFollow\\(|pollLogsIncremental\\(|insertAdjacentText\\(' pwa/app.js

# Theme remains light
rg -n '<body[^>]*data-theme=\"light\"' pwa/index.html

timeout 5s node --check pwa/app.js
timeout 5s node --check pwa/service-worker.js
```

Manual UI verification (outside this sandbox, which cannot bind ports):
1. Start backend + PWA:
   - Backend: `python3 -m backend.app`
   - PWA: `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open Logs tab and confirm:
   - New lines append over time (not full replace) while the pipeline/back end produces logs.
   - While “Pause” is active (follow=true), the view auto-scrolls to the bottom.
   - Toggle follow off (pause auto-scroll), scroll/select text, and copy it; the page should not force-scroll to bottom.
   - Toggle follow on again and confirm it snaps to the bottom and continues following new lines.

## Acceptance Checklist
- [ ] Logs panel appends incremental entries using `GET /api/logs?source=...&since=...`.
- [ ] Auto-scroll is enabled by default and can be paused via a toggle.
- [ ] User can select and copy text from the logs view (pause prevents forced scrolling).
- [ ] Default theme remains light.

