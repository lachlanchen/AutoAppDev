# AutoAppDev Layout and Small Webapp Update Plan

Date: 2026-04-25

This is a planning reference only. It learns from the recent AutoNovelWriter layout, chat, live-sync, and toast updates, but it does not implement them. Use this document to guide a later AutoAppDev task with small, reviewable commits.

Implementation follow-up: see `references/autoappdev_webapp_mobile_desktop_update_notes.md` for the actual AutoAppDev desktop/mobile layout, chat, toast, live-sync, fallback, and logo changes implemented after this plan.

## Source Notes Read

- `/home/lachlan/ProjectsLFS/AutoNovelWriter/references/ui_layout_chat_update_notes.md`
- `/home/lachlan/ProjectsLFS/AutoNovelWriter/references/autonovelwriter_webapp_architecture.md`
- Current AutoAppDev surfaces in `pwa/index.html`, `pwa/styles.css`, `pwa/app.js`, `docs/studio-codex-api.md`, and `pwa/README.md`

## Current AutoAppDev Baseline

AutoAppDev already has the same broad app shape as AutoNovelWriter:

- Bottom tabs: `Notes`, `Design`, `AutoPilot Loop`, `AutoPilot Setup`.
- `Notes`, `Design`, and `AutoPilot Loop` use `writing-screen` panels with preview plus chat.
- `AutoPilot Setup` keeps the Scratch-like blocks/program/inspector workspace inside `setup-shell`.
- The backend has Studio chat, preview, job, and monitor-style routes: `/api/studio/chat`, `/api/studio/preview`, `/api/studio/agent/status`, `/api/codex/jobs`.
- The PWA uses `config.local.js` for API base selection and a service worker cache that must be bumped for shell behavior changes.

The main gap is polish: desktop layout should keep context visible beside chat, mobile should feel like one stable app flow, and fixed mechanical acknowledgements should not pollute durable chat history.

## First Layout Update: Desktop

Goal: make the main non-setup tabs feel like workbenches, not stacked panels.

Proposed behavior:

- Convert `Notes`, `Design`, and `AutoPilot Loop` desktop layout to a two-column grid.
- Left column: preview/status context.
- Right column: chat log and input.
- Keep `AutoPilot Setup` as the existing three-column Scratch-like editor.
- Preserve bottom navigation and current tab names.
- Keep preview scroll independent from chat scroll.
- Keep `AutoPilot Loop` actions such as `Propose Current Setup` and `Accept Proposed` visible in the preview header.

Suggested desktop CSS direction:

- `writing-screen`: `grid-template-columns: minmax(360px, 0.9fr) minmax(420px, 1.1fr)`.
- `writing-screen`: one row with `height: 100%`.
- `writing-preview` and `writing-chat`: `min-width: 0; min-height: 0`.
- `studio-chatbar`: keep `grid-template-columns: 1fr auto`.
- Ensure long button rows in preview headers can shrink without pushing content offscreen.

Acceptance:

- On a normal desktop browser, preview and chat are visible at the same time.
- No panel causes horizontal scrolling.
- Setup tab still behaves like the current blocks/program/inspector workspace.

## First Layout Update: Mobile

Goal: make the mobile app usable as a chat-first control surface.

Proposed behavior:

- Keep bottom tabs full width and safe-area aware.
- Fold preview panels by default for `Notes`, `Design`, and `AutoPilot Loop`.
- Add `Preview` / `Hide` controls to expand or collapse preview.
- Chat gets most of the vertical height.
- Topbar controls should collapse behind a `Settings` button on small screens.
- Header height must be measured dynamically and written to `--topbar-h`.
- Prevent horizontal drag and accidental zoom:
  - `html, body { overflow-x: hidden; overscroll-behavior-x: none; }`
  - mobile interactive area should prefer `touch-action: pan-y`.
  - text inputs should use at least `16px` font size on mobile.

Acceptance:

- Phone width has no horizontal drag.
- Focusing textareas does not zoom the page.
- Opening and closing Settings does not leave blank space or clipped panels.
- Preview actions remain reachable in both folded and expanded states.

## Later Small Webapp Updates

### 1. Same-Origin Remote API

If AutoAppDev is exposed through ngrok or another public proxy, avoid mixed-content calls from HTTPS pages to `http://127.0.0.1`.

Plan:

- Add or adapt a public runner/proxy only when a public URL is chosen.
- For remote mode, write `pwa/config.local.js` with `API_BASE_URL = ""`.
- Route `/api/...` through the same public origin.
- Keep local development defaulting to `http://127.0.0.1:<backend-port>`.

### 2. Preview Header Overflow

Problem to avoid: `Refresh`, `Preview`, `Hide`, `Propose`, and `Accept` buttons can push past the viewport.

Plan:

- Give title containers `min-width: 0`.
- Keep action containers flexible but bounded.
- Let button text ellipsize on narrow screens.
- Keep action row height stable when preview folds/unfolds.

### 3. Chat Bubble Styling

Plan:

- User messages align right with a distinct action color.
- Assistant replies align left with a calmer panel color.
- System/debug messages remain visually separate.
- Preserve `white-space: pre-wrap`.
- Scroll chat to bottom after each refresh.

Durable chat should contain meaningful conversation and results. Fixed acknowledgements should become transient UI.

### 4. Toast Notices

Plan:

- Add a `showToast()` channel for mechanical acknowledgements such as "request accepted" or "assistant job queued".
- Backend responses may include:

```json
{
  "notice": {
    "kind": "mechanical_ack",
    "text": "Request accepted; assistant job queued."
  }
}
```

- Frontend displays the notice as a toast and does not append it to durable chat.
- Historical fixed acknowledgement messages can be filtered from display if needed.

### 5. Cross-Device Live Sync

Plan:

- Add a visibility-aware polling loop.
- Refresh active chat, active preview, and agent/job status every 2.5 seconds while visible.
- Force-refresh when the tab becomes visible again.
- Use a busy guard so polling does not overlap.

Acceptance:

- A message sent on phone appears on desktop without manual refresh.
- Job status changes appear without switching tabs.
- Polling does not stack requests if the backend is slow.

### 6. Agent Monitor

Plan:

- Convert monitor behavior to a normal overlay/popover pattern.
- Click `Agent` to open.
- Click outside, press `Escape`, or click `Close` to dismiss.
- Monitor should show recent job counts, running jobs, failed jobs, and relevant runtime paths.

### 7. Service Worker Discipline

Every shell behavior change should bump `pwa/service-worker.js` cache version.

Plan:

- Increment `CACHE_NAME` once per UI behavior batch.
- Verify updated assets are served with no-cache headers in local dev.
- Avoid relying on hard refresh as the only update path.

## Suggested Implementation Order

1. Desktop two-column layout for `writing-screen`.
2. Mobile foldable preview and anti-horizontal-drag fixes.
3. Topbar Settings collapse and dynamic `--topbar-h` measurement.
4. Preview header overflow fixes.
5. Chat bubble styling.
6. Toast notice channel for mechanical acknowledgements.
7. Cross-device live sync.
8. Agent monitor overlay behavior.
9. Optional public same-origin API proxy, only after deciding the remote URL.

Each batch should be independently verifiable and committed separately.

## Verification Checklist

Static checks:

```bash
node --check pwa/app.js
node --check pwa/api-client.js
node --check pwa/i18n.js
node --check pwa/service-worker.js
python3 -m json.tool pwa/manifest.json
python3 - <<'PY'
from pathlib import Path
css = Path("pwa/styles.css").read_text()
assert css.count("{") == css.count("}")
PY
```

Runtime checks:

```bash
./scripts/run_autoappdev_tmux.sh --restart --backend-port 8790 --pwa-port 5174
curl -sS http://127.0.0.1:8790/api/health
curl -I http://127.0.0.1:5174/app.js
curl -I http://127.0.0.1:5174/styles.css
```

Manual checks:

- Desktop: preview and chat visible side by side.
- Mobile: no horizontal drag, no input zoom, bottom nav reachable.
- Preview fold/unfold: action buttons remain visible.
- Chat: user/assistant/system messages are visually distinct.
- Live sync: two browsers update chat/status without manual refresh.

## Boundaries

- Do not change AAPS grammar as part of layout polish.
- Do not mix runtime files or generated chat logs into commits.
- Do not change AutoNovelWriter from this plan.
- Keep AutoAppDev product language generic; AutoNovelWriter is only a design reference.
