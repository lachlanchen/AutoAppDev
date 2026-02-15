# Work Notes: 025 pipeline_script_parser_v0

## Summary
- Implemented a deterministic parser for the formatted pipeline script (AAPS v1) into canonical IR (`autoappdev_ir` v1).
- Added a backend endpoint to parse script text into IR with actionable 400 errors that include line number and detail.
- Updated API contracts to document the parse endpoint and error shape.

## Changes Made
- `backend/pipeline_parser.py`
  - New pure parser module:
    - `parse_aaps_v1(text)` -> IR dict
    - `ParseError(code, line, detail)` for actionable failures (no execution, no I/O)
  - Enforces:
    - Header `AUTOAPPDEV_PIPELINE 1`
    - `TASK/STEP/ACTION` nesting rules
    - Required fields and `STEP.block` allowed set (`plan/work/debug/fix/summary/commit_push`)
    - Per-scope uniqueness of IDs
- `backend/app.py`
  - New handler `ScriptsParseHandler`:
    - `POST /api/scripts/parse` with `{ "script_text": "..." }`
    - Returns `{ ok:true, ir:... }` or `400` with `{ ok:false, error, line, detail }`
  - Route registered in `make_app()`.
- `docs/api-contracts.md`
  - Added `POST /api/scripts/parse` documentation and an error example.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 5s python3 -m py_compile backend/pipeline_parser.py backend/app.py

python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path('examples/pipeline_formatted_script_v1.aaps').read_text('utf-8')
ir = parse_aaps_v1(text)
assert ir['kind'] == 'autoappdev_ir' and ir['version'] == 1
assert ir['tasks'] and ir['tasks'][0]['steps']
print('OK')
PY

rg -n '/api/scripts/parse' backend/app.py docs/api-contracts.md
```

