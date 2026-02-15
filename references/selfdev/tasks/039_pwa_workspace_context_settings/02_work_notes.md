# Work Notes: 039 pwa_workspace_context_settings

## What Changed
- Added a **Workspace** settings section to the PWA **Status** tab:
  - Select workspace slug
  - Edit materials paths (one per line)
  - Edit shared context text and optional shared context path
  - Choose default language (allowed list)
  - Load/Save buttons with inline status/errors
- Persist behavior:
  - Workspace config persists in backend via `GET/POST /api/workspaces/<workspace>/config`
  - Selected workspace slug persists locally via `localStorage["autoappdev_workspace"]`
- Script generation now includes workspace metadata (when a workspace is selected):
  - `programToIr()` and `programToAapsScript()` attach `TASK.meta = { workspace, workspace_config }`
  - When no workspace is selected, exports remain unchanged.
- Small QoL: `Update README` block prompt defaults to the selected workspace slug (if set).

## Files Touched
- `pwa/index.html`
- `pwa/app.js`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

timeout 10s rg -n 'ws-slug|ws-load|ws-save|ws-materials|ws-language|ws-context-text|ws-context-path|/api/workspaces' pwa/index.html pwa/app.js
```

Results:
- `node --check` exited `0` (syntax OK).
- `rg` confirms new UI ids and `/api/workspaces/.../config` usage.

