# Summary: 036 pwa_action_library_editor

## What Changed
- Added an **Actions** tab to the PWA right panel to manage the backend **action registry** without reloading:
  - List actions (`GET /api/actions`)
  - Load (`GET /api/actions/<id>`)
  - Create (`POST /api/actions`)
  - Update (`PUT /api/actions/<id>`)
  - Delete (`DELETE /api/actions/<id>`)
- Implemented a minimal editor for both action kinds:
  - `prompt`: prompt template + optional agent/model + reasoning + optional timeout
  - `command`: cmd + repo-relative cwd + optional timeout (shell fixed to `bash`)
- UI enforces v0 constraints: existing actions cannot change `kind` (backend disallows).

Files:
- `pwa/index.html`
- `pwa/styles.css`
- `pwa/app.js`

## Why
AutoAppDev needs a reusable, configurable action toolchain; this adds the first UI surface to manage stored action definitions so pipelines can reference them later.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
timeout 10s rg -n 'data-tab="actions"|tab-actions|/api/actions' pwa/index.html pwa/app.js pwa/styles.css
```

Manual smoke (with backend running):
1. Open the PWA and click **Actions**.
2. Create a prompt action (title + prompt) and save; it should appear immediately in the list without reload.
3. Edit and save; then delete; list updates without reload.

