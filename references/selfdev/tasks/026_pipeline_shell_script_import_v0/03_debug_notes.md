# Debug Notes: 026 pipeline_shell_script_import_v0

Date: 2026-02-15

## Commands Run

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && rg -n "ScriptsImportShellHandler|/api/scripts/import-shell|Shell Annotations v0" backend/app.py docs/api-contracts.md docs/pipeline-formatted-script-spec.md
```

Output:
```text
backend/app.py:390:class ScriptsImportShellHandler(BaseHandler):
backend/app.py:822:            (r"/api/scripts/import-shell", ScriptsImportShellHandler),
docs/api-contracts.md:187:### POST /api/scripts/import-shell
docs/pipeline-formatted-script-spec.md:74:### 1.7 Shell Annotations v0 (Import Helper)
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s python3 -m py_compile backend/app.py backend/pipeline_parser.py backend/pipeline_shell_import.py
```

Result: exit 0, no output.

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_shell_import import import_shell_annotated_to_ir

shell_text = Path('examples/pipeline_shell_annotated_v0.sh').read_text('utf-8')
res = import_shell_annotated_to_ir(shell_text)
assert res['aaps_text'].lstrip().startswith('AUTOAPPDEV_PIPELINE 1')
ir = res['ir']
assert ir['kind'] == 'autoappdev_ir' and ir['version'] == 1
assert ir['tasks'] and ir['tasks'][0]['steps']
print('OK', len(ir['tasks']), 'tasks', len(ir['tasks'][0]['steps']), 'steps')
PY
```

Output:
```text
OK 1 tasks 2 steps
```

Negative case: parse error line mapping should report the original shell line number of the failing AAPS line.
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s python3 - <<'PY'
from backend.pipeline_shell_import import import_shell_annotated_to_ir, ShellImportError

bad = "#!/usr/bin/env bash\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"X\"}\n"
try:
    import_shell_annotated_to_ir(bad)
except ShellImportError as e:
    print(e.to_dict())
else:
    raise SystemExit('expected error')
PY
```

Output:
```text
{'ok': False, 'error': 'invalid_header', 'line': 2, 'detail': 'expected header: AUTOAPPDEV_PIPELINE 1'}
```

Negative case: missing annotations.
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev && timeout 10s python3 - <<'PY'
from backend.pipeline_shell_import import import_shell_annotated_to_ir, ShellImportError

try:
    import_shell_annotated_to_ir('#!/usr/bin/env bash\necho hi\n')
except ShellImportError as e:
    print(e.to_dict())
else:
    raise SystemExit('expected error')
PY
```

Output:
```text
{'ok': False, 'error': 'missing_annotations', 'line': 1, 'detail': 'expected at least one "# AAPS:" annotation line'}
```

## Notes / Limitations
- Full HTTP verification of `POST /api/scripts/import-shell` requires running the backend server; this sandbox environment cannot bind/listen on ports, so verification here is limited to static checks and direct function smoke tests.

