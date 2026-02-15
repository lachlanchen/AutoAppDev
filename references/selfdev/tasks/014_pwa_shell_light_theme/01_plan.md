# Plan: 014 pwa_shell_light_theme

## Goal
Deliver an offline-friendly PWA shell with a clean light theme and the core controller layout:
- Top bar
- Left blocks palette
- Center workspace
- Right inspector/logs panel

Acceptance:
- PWA loads an offline-friendly shell with a clean light theme.
- Layout includes top bar, left blocks palette, center workspace, right inspector/logs panel.

## Current State (References)
- Layout already exists in `pwa/index.html`:
  - Top bar: `.topbar`
  - Left palette: `.panel--toolbox`
  - Workspace: `.panel--canvas`
  - Right panel: `.panel--right`
- Light theme tokens and responsive grid already exist in `pwa/styles.css`.
- Default theme is light (`<body data-theme="light">`) and theme persistence is in `pwa/app.js`.
- PWA is served via `python3 -m http.server` by `scripts/run_autoappdev_tmux.sh`.
- Missing “offline-friendly shell” pieces:
  - No web app manifest.
  - No service worker caching the shell.
- `pwa/README.md` currently contains literal `\n+` sequences (formatting cleanup is low-risk and should be fixed in this task).

## Approach (Minimal)
Add the minimum PWA primitives while preserving the current UI/layout:
1. Add a web app manifest.
2. Add a service worker that caches the app shell assets.
3. Register the service worker from the PWA.
4. Keep default theme light; do not redesign UI.

## Files To Change (Implementation Phase)
- Add: `pwa/manifest.json`
  - `name`, `short_name`, `start_url`, `display`, `theme_color`, `background_color`, `icons`.
- Add: `pwa/service-worker.js`
  - Precache `index.html`, `styles.css`, `app.js`, `favicon.svg`, `manifest.json`.
  - Cache-first for shell assets.
  - Navigation fallback to cached `index.html` when offline.
- Update: `pwa/index.html`
  - Add `<link rel="manifest" href="manifest.json">`.
  - Add `<meta name="theme-color" ...>`.
- Update: `pwa/app.js`
  - Register the service worker on boot (`navigator.serviceWorker.register(...)`).
- Update: `pwa/README.md`
  - Remove literal `\n+` sequences and make the README render correctly.

## Implementation Steps (Next Phase)
1. Create `pwa/manifest.json`.
   - Use `start_url: "./"` and `scope: "./"` for `http.server` usage.
   - Use existing `favicon.svg` as an icon entry (SVG is acceptable for modern browsers; keep minimal).
2. Create `pwa/service-worker.js`.
   - `CACHE_NAME = "autoappdev-shell-v1"`.
   - `install`: `cache.addAll([...])`, then `skipWaiting()`.
   - `activate`: delete old caches, `clients.claim()`.
   - `fetch`:
     - If request mode is `navigate`, return cached `index.html`.
     - Else if request URL path is in the precache list, return cache-first.
     - Otherwise fall back to `fetch`.
3. Update `pwa/index.html`.
   - Add manifest link and theme-color.
4. Update `pwa/app.js`.
   - Add a small service worker registration block in `boot()`.
5. Fix `pwa/README.md` formatting.

## Commands To Run (Verification)
Verification should not leave servers running; use `timeout`.

1) Static checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -s pwa/manifest.json
test -s pwa/service-worker.js

rg -n "rel=\"manifest\"" pwa/index.html
rg -n "theme-color" pwa/index.html
rg -n "serviceWorker\.register" pwa/app.js

# Ensure default light theme remains
rg -n "<body[^>]*data-theme=\"light\"" pwa/index.html
```

2) Serve and fetch assets:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 3s bash -lc 'cd pwa && python3 -m http.server 5173 --bind 127.0.0.1' &
# In another terminal (or after starting via tmux script), verify files are served:
# curl -fsS http://127.0.0.1:5173/
# curl -fsS http://127.0.0.1:5173/manifest.json
# curl -fsS http://127.0.0.1:5173/service-worker.js
```

3) Manual browser offline check (required for “offline-friendly”):
- Open `http://127.0.0.1:5173/`.
- Confirm service worker is installed (DevTools > Application > Service Workers).
- Toggle “Offline” in DevTools Network tab and reload.
- Expect: shell still loads (layout renders) even if backend calls fail.

## Acceptance Criteria Checks
- PWA layout renders with top bar, blocks palette, workspace, and right panel (already present in `pwa/index.html`).
- Default theme is light.
- Service worker caches the shell assets and allows reload while offline.
- README for PWA renders without literal escape artifacts.
