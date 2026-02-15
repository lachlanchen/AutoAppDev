# Work Notes: 030 workspace_layout_standardization

## Summary
- Added a dedicated workspace contract doc describing standard folders and how AutoAppDev uses workspace vs runtime storage.
- Linked the new doc from `README.md`.

## Changes Made
- `docs/workspace-layout.md`
  - Defined the standard workspace folders: `materials/`, `interactions/`, `outputs/`, `docs/`, `references/`, `scripts/`, `tools/`, `logs/`, and the `auto-apps/` workspace container.
  - Documented runtime (ephemeral) paths and current implementations: `AUTOAPPDEV_RUNTIME_DIR`, `runtime/PAUSE`, `runtime/logs/`, `runtime/inbox/`.
  - Added a simple init checklist with concrete `mkdir -p ...` commands.
- `README.md`
  - Added `docs/workspace-layout.md` to the Contents list.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n "## Contents" -n -C 2 README.md
sed -n '28,70p' README.md

rg -n "runtime_dir.*inbox|inbox_dir" backend/app.py
sed -n '1,80p' backend/app.py
sed -n '1,220p' scripts/run_autoappdev_tmux.sh

sed -n '1,200p' docs/workspace-layout.md

rg -n "docs/workspace-layout\\.md" README.md
python3 -m py_compile backend/app.py >/dev/null
```

