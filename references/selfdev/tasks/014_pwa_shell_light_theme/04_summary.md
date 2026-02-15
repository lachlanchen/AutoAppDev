# Summary: 014 pwa_shell_light_theme

## What Changed
- Added minimal PWA primitives for an offline-friendly shell:
  - `pwa/manifest.json`
  - `pwa/service-worker.js` (precache shell assets + navigation fallback to cached `index.html`)
- Wired the manifest + `theme-color` into `pwa/index.html`.
- Registered the service worker from `pwa/app.js`.
- Cleaned up `pwa/README.md` so it renders correctly.

## Why
To make the existing controller layout installable and resilient to offline reloads while keeping the default UI theme light.

## How To Verify
Static wiring checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
test -s pwa/manifest.json
test -s pwa/service-worker.js
rg -n 'rel="manifest"' pwa/index.html
rg -n 'theme-color' pwa/index.html
rg -n 'serviceWorker\\.register' pwa/app.js
rg -n '<body[^>]*data-theme="light"' pwa/index.html
node --check pwa/app.js
node --check pwa/service-worker.js
```

Manual offline-shell check (in a normal local environment that can bind ports):
1. `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1`
2. Open `http://127.0.0.1:5173/`, confirm UI renders.
3. DevTools -> Application -> Service Workers: confirm it installs.
4. DevTools -> Network: set Offline, reload.
5. Expect: the shell (top bar + panels) still loads (backend/API calls may fail, but the shell should render).

