# Work Notes: 036 pwa_action_library_editor

## What Changed
- Added an **Actions** tab to the PWA right panel to manage action registry entries without page reload:
  - List action definitions (`GET /api/actions?limit=200`)
  - Load selected action (`GET /api/actions/<id>`)
  - Create action (`POST /api/actions`)
  - Update action (`PUT /api/actions/<id>`)
  - Delete action (`DELETE /api/actions/<id>`)
- Implemented a minimal editor form supporting both backend kinds:
  - `prompt`: prompt template + optional agent/model + reasoning + optional timeout
  - `command`: cmd + repo-relative cwd + optional timeout (shell fixed to `bash`)
- Enforced v0 guardrails in the UI:
  - Existing actions cannot change `kind` (kind select disabled when editing an existing action).
  - Optional fields: blank on **create** omits the field (backend defaults apply); blank on **update** sends `null` to reset to backend defaults.

## Files Touched
- `pwa/index.html`
  - Added `data-tab="actions"` button and `#tab-actions` tabview containing the list + editor controls.
- `pwa/styles.css`
  - Updated `.tabs` to `repeat(5, 1fr)` and added minimal styles for actions list/editor (`.actionbar`, `.actionlist`, `.actionrow`, `.actiongrid`, `.action-text`).
- `pwa/app.js`
  - Added DOM bindings/state + CRUD wiring for `/api/actions`.
  - Hooked tab switching so actions are loaded on first open (and manual Refresh is available).

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

timeout 10s rg -n 'data-tab="actions"|tab-actions|/api/actions' pwa/index.html pwa/app.js pwa/styles.css
```

Results:
- `node --check` exited `0` (syntax OK).
- `rg` shows the new tab/view and the API calls are present.

