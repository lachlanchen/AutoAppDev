# Work Notes: 026 pipeline_shell_script_import_v0

## Summary
- Implemented a best-effort importer that extracts embedded AAPS v1 lines from annotated shell scripts (`# AAPS:` comments) and parses them into canonical IR (`autoappdev_ir` v1).
- Added a backend endpoint to import shell text and return extracted `script_text` + `ir`, with errors mapped to original shell line numbers.
- Added a repo example shell script that imports successfully and documented the format/limitations.

## Changes Made
- `backend/pipeline_shell_import.py`
  - Added `extract_aaps_from_shell(shell_text)` and `import_shell_annotated_to_ir(shell_text)`.
  - Added `ShellImportError(code,line,detail)` with `to_dict()` for consistent API errors.
  - Only `# AAPS:` comment lines are extracted; no bash parsing or execution.
- `backend/app.py`
  - Added `ScriptsImportShellHandler` for `POST /api/scripts/import-shell`.
  - Registered the route in `make_app()`.
- `examples/pipeline_shell_annotated_v0.sh`
  - New example annotated shell script with embedded AAPS v1 content (imports to IR).
- `docs/pipeline-formatted-script-spec.md`
  - Added “Shell Annotations v0” section describing `# AAPS:` embedding and limitations.
- `docs/api-contracts.md`
  - Documented `POST /api/scripts/import-shell` request/response and error behavior (shell line numbers).

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

rg -n "import-shell|ScriptsImportShellHandler" backend/app.py docs/api-contracts.md

timeout 10s python3 -m py_compile backend/app.py backend/pipeline_parser.py backend/pipeline_shell_import.py

timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_shell_import import import_shell_annotated_to_ir

shell_text = Path('examples/pipeline_shell_annotated_v0.sh').read_text('utf-8')
res = import_shell_annotated_to_ir(shell_text)
assert res['aaps_text'].lstrip().startswith('AUTOAPPDEV_PIPELINE 1')
ir = res['ir']
assert ir['kind'] == 'autoappdev_ir' and ir['version'] == 1
assert ir['tasks'] and ir['tasks'][0]['steps']
print('OK', len(ir['tasks']), 'tasks')
PY

timeout 10s python3 - <<'PY'
from backend.pipeline_shell_import import import_shell_annotated_to_ir, ShellImportError

bad = "#!/usr/bin/env bash\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"X\"}\n"
try:
    import_shell_annotated_to_ir(bad)
except ShellImportError as e:
    print(e.to_dict())
else:
    raise SystemExit("expected error")
PY
```

