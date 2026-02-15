# Summary: 001 define_controller_mvp_scope

## What Changed
- Added `docs/controller-mvp-scope.md` describing the controller MVP screens (blocks, chat/inbox, controls, logs, settings), default light theme, and the minimal backend API surface.
- Updated `README.md` to link to the new doc in Contents.

## Why
This establishes a single, concrete MVP definition for the Scratch-like controller so subsequent tasks can implement features against a stable set of screens and endpoints.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Doc exists and is readable
sed -n '1,120p' docs/controller-mvp-scope.md

# README links to the scope doc
rg -n "docs/controller-mvp-scope\.md" README.md

# Required screens + endpoints are explicitly listed
rg -n "Blocks|Chat/Inbox|Pipeline Controls|Logs|Settings|Default UI theme: light" docs/controller-mvp-scope.md
rg -n "/api/health|/api/config|/api/chat\?limit|/api/pipeline/status|/api/pipeline/start|/api/pipeline/stop\|pause\|resume|/api/logs/tail" docs/controller-mvp-scope.md
```
