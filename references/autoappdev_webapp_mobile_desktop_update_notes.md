# AutoAppDev Webapp Mobile and Desktop Update Notes

Date: 2026-04-25

This document records the AutoAppDev-specific webapp changes made after studying the recent AutoNovelWriter mobile/desktop updates. AutoNovelWriter is a design reference, not a source of behavior to copy blindly. AutoAppDev remains a generic app-development controller with Notes, Design, AutoPilot Loop, and AutoPilot Setup surfaces.

## Source Material Reviewed

- `/home/lachlan/ProjectsLFS/AutoNovelWriter/references/ui_layout_chat_update_notes.md`
- `/home/lachlan/ProjectsLFS/AutoNovelWriter/references/autonovelwriter_webapp_architecture.md`
- `/home/lachlan/.codex/sessions/2026/03/28/rollout-2026-03-28T21-14-28-019d3494-ec26-7df2-bd32-bd770f60a790.jsonl`
- AutoAppDev commits `4d60fe6` and `c816099`

The Codex session log was useful as implementation context: it showed the local AutoAppDev API/PWA work, route smoke tests, tmux restart behavior, and the database startup problem that later led to runtime JSON fallback support. The durable source of truth is still the committed code and this reference file.

## Implemented AutoAppDev Changes

### Desktop Layout

Desktop moved the non-setup workspace tabs toward a two-pane workbench:

- `Notes`, `Design`, and `AutoPilot Loop` use `.writing-screen` as a two-column grid.
- The left column holds preview/status context.
- The right column holds chat log and input.
- Preview and chat scroll independently.
- Header/action rows use `min-width: 0`, bounded action containers, and ellipsis-friendly buttons to avoid overflow.
- `AutoPilot Setup` intentionally keeps the Scratch-like blocks/program/inspector workspace.

This mirrors the AutoNovelWriter idea of keeping context visible beside chat, but the content is AutoAppDev-specific: project notes, design/contracts, and AAPS loop state rather than story beats or prose drafts.

### Mobile Layout

Mobile was made chat-first without adopting AutoNovelWriter's latest single-hamburger model:

- A `Settings` button collapses the topbar controls on narrow screens.
- `Notes`, `Design`, and `AutoPilot Loop` preview panels start collapsed on mobile.
- Each preview card has its own `Preview` / `Hide` control.
- `--topbar-h` is recalculated after settings changes, resize, orientation changes, and visibility return.
- `overflow-x: hidden`, `overscroll-behavior-x: none`, and `touch-action: pan-y` reduce horizontal drag.
- Mobile form controls use at least `16px` font size to avoid iOS/Safari input zoom.
- Bottom navigation remains full width and safe-area aware.

Difference from AutoNovelWriter v29: AutoNovelWriter now uses one global top-left hamburger to toggle the active preview on mobile. AutoAppDev does not yet have that compact header model, history drawer, or dedicated Settings page, so keeping per-card preview buttons is simpler and more explicit for the current UI.

### Chat Presentation

The Studio chat UI now separates message roles visually:

- User messages align right.
- Assistant, system, and agent messages align left with distinct panel colors.
- Messages preserve line breaks through `white-space: pre-wrap`.
- Long content wraps instead of forcing horizontal scroll.
- Chat scrolls to the bottom after rendering.

This follows the AutoNovelWriter principle: durable chat should contain meaningful conversation and results, not app plumbing.

### Toast and Durable Chat Rules

AutoAppDev now uses transient toast notices for mechanical events:

- assistant job queued,
- send failed,
- inbox message saved,
- AutoPilot proposal/acceptance result.

The backend changed `/api/studio/chat` so a delegated assistant queue acknowledgement is returned as:

```json
{
  "notice": {
    "kind": "assistant_queued",
    "text": "Delegated assistant job queued: <job-id>",
    "job_id": "<job-id>"
  }
}
```

The frontend displays the notice through `showToast()` and does not add that queue acknowledgement as a durable chat message. Real quick replies, assistant/agent results, and proposal validation messages remain durable.

### Live Sync

AutoAppDev now has guarded live refresh behavior:

- `liveSync()` runs every 2.5 seconds while visible.
- It refreshes health, pipeline status, Studio agent status, active chat, active preview, and logs when their surfaces are open.
- It force-runs when the browser tab becomes visible again.
- `liveSyncBusy` prevents overlapping polling when requests are slow.

This is intended to make phone and desktop browser views converge without manual refresh.

### Backend Runtime Fallback

The existing storage comment said the backend was Postgres-first with local JSON fallback. Startup did not actually tolerate a missing configured database. The backend now:

- records `Storage.database_error` when asyncpg cannot connect,
- continues startup with runtime JSON storage,
- reports fallback mode through `/api/health`,
- lets the frontend display database fallback as a warning, not a backend-down failure.

Current local note: this machine's `.env` points at `lightmind_db`, but that database does not exist and the user cannot create databases without sudo password. Runtime JSON fallback keeps the PWA usable locally. Production should still provision the intended Postgres database and apply `backend/schema.sql`.

### Logo and Shell Cache

The LazyingArt panda logo was removed from AutoAppDev because it used too much header space and was company-level branding rather than product-specific branding.

- `pwa/favicon.svg` is now a compact AutoAppDev mark.
- Header logo returned to the original `42x42` footprint.
- `pwa/manifest.json` and `pwa/index.html` use `favicon.svg`.
- The tracked `pwa/lazyingart-logo.png` asset was removed.
- `pwa/service-worker.js` cache moved to `autoappdev-shell-v14`.

Cache history for this pass:

- `autoappdev-shell-v13`: layout/chat/toast/live-sync update.
- `autoappdev-shell-v14`: compact AutoAppDev SVG logo update.

## What Was Not Ported From AutoNovelWriter

The following AutoNovelWriter concepts are not yet implemented in AutoAppDev:

- single global mobile hamburger that controls active preview visibility,
- dedicated Settings workspace page,
- Settings-only Agent Monitor,
- History popover and backend-owned per-tab/default shared chat sessions,
- same-origin public ngrok/proxy API mode,
- full monitor overlay with click-outside and Escape behavior.

These should be separate implementation tasks. The current AutoAppDev update deliberately kept the app's existing topbar and tab model.

## Files Changed

Primary frontend files:

- `pwa/index.html`
- `pwa/styles.css`
- `pwa/app.js`
- `pwa/service-worker.js`
- `pwa/favicon.svg`
- `pwa/manifest.json`

Primary backend files:

- `backend/app.py`
- `backend/storage.py`

## Verification Used

Static checks:

```bash
node --check pwa/app.js
node --check pwa/service-worker.js
python3 -m py_compile backend/app.py backend/storage.py backend/studio_chat.py
python3 -m json.tool pwa/manifest.json
python3 - <<'PY'
from pathlib import Path
css = Path("pwa/styles.css").read_text()
assert css.count("{") == css.count("}")
PY
```

Runtime checks:

```bash
./scripts/run_autoappdev_tmux.sh --restart --skip-setup --detached --backend-port 8790 --pwa-port 5174
curl -sS http://127.0.0.1:8790/api/health
curl -I http://127.0.0.1:5174/app.js
curl -I http://127.0.0.1:5174/styles.css
curl -I http://127.0.0.1:5174/favicon.svg
```

Smoke API checks:

```bash
curl -sS "http://127.0.0.1:8790/api/studio/preview?mode=notes"
curl -sS -X POST http://127.0.0.1:8790/api/studio/chat \
  -H "Content-Type: application/json" \
  --data '{"mode":"notes","message":"smoke notice","mock":true,"assistant_enabled":true}'
```

## Future AutoAppDev Update Candidates

1. Decide whether AutoAppDev should adopt AutoNovelWriter v29's single global mobile preview toggle.
2. Move topbar controls into a dedicated Settings tab or page if the header keeps growing.
3. Add a real Agent Monitor overlay with click-outside, Escape, and close button behavior.
4. Add backend-owned chat session history if AutoAppDev needs durable multi-chat workflows like AutoNovelWriter.
5. Add same-origin public proxy support before exposing the app through ngrok or HTTPS.
6. Provision the intended Postgres database so `/api/health` returns DB `ok: true` instead of runtime JSON fallback.

## Acceptance Criteria For This Pass

- Desktop shows preview and chat side by side for Notes, Design, and AutoPilot Loop.
- AutoPilot Setup remains the Scratch-like editor.
- Mobile starts with chat-first collapsed previews.
- Mobile has no horizontal drag and no input zoom.
- Settings collapse does not leave stale workspace height.
- Mechanical queue acknowledgements appear as toasts, not durable chat messages.
- Live sync does not stack overlapping requests.
- Service worker cache is bumped for shell updates.
- AutoAppDev uses its own compact logo, not the LazyingArt panda asset.
