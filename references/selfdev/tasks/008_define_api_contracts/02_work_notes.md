# Work Notes: 008 define_api_contracts

## Summary of Changes
- Added `docs/api-contracts.md` documenting request/response shapes (with example JSON) for:
  - Settings (`/api/config`)
  - Inbox messages (`/api/chat`)
  - Pipeline controls (`/api/pipeline/*`)
  - Logs (`/api/logs/tail`)
- Updated `README.md` to link to the new API contracts doc.

## Files Changed
- Added: `docs/api-contracts.md`
- Updated: `README.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -s docs/api-contracts.md
rg -n "Settings|Config|/api/config" docs/api-contracts.md
rg -n "Inbox|Chat|/api/chat" docs/api-contracts.md
rg -n "Pipeline|/api/pipeline" docs/api-contracts.md
rg -n "Logs|/api/logs/tail" docs/api-contracts.md
rg -n "\\{[[:space:]]*\"" docs/api-contracts.md
rg -n "docs/api-contracts\\.md" README.md
```
