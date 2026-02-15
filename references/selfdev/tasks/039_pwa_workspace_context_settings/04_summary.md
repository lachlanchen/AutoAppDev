# Summary: 039 pwa_workspace_context_settings

## What Changed
- Added a **Workspace** settings section to the PWA **Status** tab (`pwa/index.html`):
  - Workspace slug + Load/Save
  - Materials paths (one per line)
  - Shared context text + optional shared context path
  - Default language select
- Wired it to the backend workspace config API (`/api/workspaces/<workspace>/config`) in `pwa/app.js`.
- Persisted selected workspace slug in `localStorage["autoappdev_workspace"]`.
- When a workspace is selected, generated exports include workspace metadata:
  - `TASK.meta = { workspace, workspace_config }` in both IR (`programToIr()`) and AAPS (`programToAapsScript()`).
- `Update README` block now defaults its workspace prompt to the selected workspace slug (if set).

## Why
Workspace-scoped materials + shared context + language are required inputs for consistent prompt/script generation across pipelines; the PWA now provides a minimal UI to manage those settings and persist them.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
timeout 10s rg -n 'ws-slug|ws-load|ws-save|ws-materials|ws-language|ws-context-text|ws-context-path|/api/workspaces' pwa/index.html pwa/app.js
```

Manual smoke (with backend running):
1. Open PWA -> Status -> Workspace.
2. Enter workspace slug -> Load (defaults should populate).
3. Edit fields -> Save; then generate AAPS and confirm `TASK ...` contains `meta.workspace` and `meta.workspace_config`.

