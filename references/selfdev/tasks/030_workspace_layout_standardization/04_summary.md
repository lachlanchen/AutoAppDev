# Summary: 030 workspace_layout_standardization

## What Changed
- Added `docs/workspace-layout.md` defining the standard workspace folder contract (`materials/`, `interactions/`, `outputs/`, `docs/`, `references/`, `scripts/`, `tools/`, `logs/`) plus the `auto-apps/` workspace container and the separate runtime dir conventions (`AUTOAPPDEV_RUNTIME_DIR`, `runtime/PAUSE`, `runtime/logs/`, `runtime/inbox/`).
- Linked the new doc from `README.md`.

## Why
To make pipeline/workspace file placement predictable and portable, and to clearly separate durable workspace storage from ephemeral runtime state (pause/logs/inbox).

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/workspace-layout.md
rg -n "docs/workspace-layout\\.md" README.md
rg -n "materials/|interactions/|outputs/|docs/|references/|scripts/|tools/|logs/|auto-apps/" docs/workspace-layout.md
```

