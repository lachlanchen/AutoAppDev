# Debug Notes: 038 workspace_materials_and_context_api

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/app.py backend/storage.py backend/workspace_config.py

# Pure-function validation smoke (no DB required)
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.workspace_config import normalize_workspace_config

repo = Path('/home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev')

cfg = normalize_workspace_config({}, repo_root=repo, workspace='my_workspace', base=None)
assert cfg['materials_paths'] == ['materials']
assert cfg['default_language'] == 'en'

cfg = normalize_workspace_config(
    {'materials_paths':['materials','docs'], 'shared_context_path':'docs/shared_context.md', 'default_language':'fr'},
    repo_root=repo,
    workspace='my_workspace',
    base=None,
)
assert cfg['materials_paths'] == ['materials','docs']
assert cfg['shared_context_path'] == 'docs/shared_context.md'
assert cfg['default_language'] == 'fr'

try:
    normalize_workspace_config({'materials_paths':['../secrets']}, repo_root=repo, workspace='my_workspace', base=None)
    raise SystemExit('expected traversal to fail')
except Exception:
    pass

print('ok')
PY

timeout 10s rg -n \"workspace_configs|/api/workspaces/\\(\\[\\^/\\]\\+\\)/config|WorkspaceConfigHandler\" backend
timeout 10s rg -n \"GET /api/workspaces/<workspace>/config|POST /api/workspaces/<workspace>/config\" docs/api-contracts.md
```

## Results
- `py_compile` exit code: `0`
- Validation smoke output: `ok` (exit code `0`)
- `rg` confirms:
  - schema + storage + handler + route exist
  - docs include both endpoints

## Issues Found
- None in these minimal checks.

