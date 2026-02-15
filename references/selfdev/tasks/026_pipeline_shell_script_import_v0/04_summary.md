# Summary: 026 pipeline_shell_script_import_v0

## What Changed
- Added a pure, deterministic shell annotation importer:
  - `backend/pipeline_shell_import.py` extracts `# AAPS:` comment lines into AAPS v1 `script_text`, parses via `backend/pipeline_parser.py`, and maps parse errors back to original shell line numbers.
- Added backend endpoint:
  - `POST /api/scripts/import-shell` in `backend/app.py` returns `{ok:true, script_text, ir, warnings}` or `400` with `{ok:false, error, line, detail}` (line refers to the shell).
- Added importing example:
  - `examples/pipeline_shell_annotated_v0.sh`
- Documented format + limitations:
  - `docs/pipeline-formatted-script-spec.md` (Shell Annotations v0)
  - `docs/api-contracts.md` (import-shell endpoint)

## Why
To support best-effort import of existing pipeline shell scripts into canonical IR without attempting to parse or execute bash. The import is deterministic and debuggable via shell line-numbered errors.

## How To Verify
In this repo (static + function smoke):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 -m py_compile backend/app.py backend/pipeline_parser.py backend/pipeline_shell_import.py
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_shell_import import import_shell_annotated_to_ir
shell_text = Path("examples/pipeline_shell_annotated_v0.sh").read_text("utf-8")
res = import_shell_annotated_to_ir(shell_text)
assert res["aaps_text"].lstrip().startswith("AUTOAPPDEV_PIPELINE 1")
assert res["ir"]["kind"] == "autoappdev_ir" and res["ir"]["version"] == 1
print("OK")
PY
```

Manual HTTP check (requires running the backend; not possible in this sandbox):
```bash
curl -sS -X POST 'http://127.0.0.1:8788/api/scripts/import-shell' \
  -H 'content-type: application/json' \
  -d @- <<'JSON'
{ "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n" }
JSON
```
