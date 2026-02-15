# Debug/Verify Notes: 008 define_api_contracts

## What I Verified
Doc-only smoke verification (no services started) to confirm:
- The API contracts doc exists and is non-empty.
- It covers the required areas: inbox messages, pipeline controls, logs, settings.
- It includes example JSON payloads.
- `README.md` links to the doc.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

ls -la docs/api-contracts.md
wc -l docs/api-contracts.md

rg -n "Settings \(Config\)|/api/config" docs/api-contracts.md
rg -n "Inbox Messages \(Chat\)|/api/chat" docs/api-contracts.md
rg -n "## Pipeline|/api/pipeline" docs/api-contracts.md
rg -n "## Logs|/api/logs/tail" docs/api-contracts.md

rg -n "\\{[[:space:]]*\"" docs/api-contracts.md

rg -n "docs/api-contracts\\.md" README.md
```

## Issues Found
- None.
