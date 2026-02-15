# Summary: 008 define_api_contracts

## What Changed
- Added `docs/api-contracts.md` defining request/response shapes (with example JSON) for:
  - Settings (`/api/config`)
  - Inbox messages (`/api/chat`)
  - Pipeline controls (`/api/pipeline/*`)
  - Logs (`/api/logs/tail`)
- Updated `README.md` to link to the new API contracts doc.

## Why
This creates a single, stable contract reference so the PWA and backend can evolve without drifting endpoint shapes.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Required areas are present
test -s docs/api-contracts.md
rg -n "Settings \(Config\)|/api/config" docs/api-contracts.md
rg -n "Inbox Messages \(Chat\)|/api/chat" docs/api-contracts.md
rg -n "## Pipeline|/api/pipeline" docs/api-contracts.md
rg -n "## Logs|/api/logs/tail" docs/api-contracts.md

# Example JSON payloads exist
rg -n "\\{[[:space:]]*\"" docs/api-contracts.md

# README link present
rg -n "docs/api-contracts\\.md" README.md
```
