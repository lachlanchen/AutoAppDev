# Work Notes: 001 define_controller_mvp_scope

## Summary of Changes
- Added `docs/controller-mvp-scope.md` to define the controller MVP screens and minimal backend API surface.
- Updated `README.md` Contents to link to the new scope doc.

## Files Changed
- Added: `docs/controller-mvp-scope.md`
- Updated: `README.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Wrote docs/controller-mvp-scope.md
# Edited README.md to add a Contents bullet

test -s docs/controller-mvp-scope.md
rg -n "Blocks|Chat|Inbox|Controls|Logs|Settings|Theme" docs/controller-mvp-scope.md
rg -n "/api/health|/api/config|/api/chat|/api/pipeline/status|/api/pipeline/(start|stop|pause|resume)|/api/logs/tail" docs/controller-mvp-scope.md
rg -n "controller-mvp-scope" README.md
```

## Acceptance Check
- Doc explicitly lists required screens (blocks, chat/inbox, controls, logs, settings) and states default light theme.
- Doc lists minimal backend APIs aligned to existing routes in `backend/app.py`.
- Doc is short and intended to be readable in under ~5 minutes.
- `README.md` links to the new doc.
