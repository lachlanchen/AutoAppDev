# Summary: 025 pipeline_script_parser_v0

## What Changed
- Added deterministic AAPS v1 parser: `backend/pipeline_parser.py` (`parse_aaps_v1()` + structured `ParseError` with `{error,line,detail}`).
- Added parse endpoint: `POST /api/scripts/parse` in `backend/app.py` to convert `{script_text}` into canonical IR (or return actionable 400 errors).
- Documented the endpoint/error shape in `docs/api-contracts.md`.

## Why
To support importing/validating the formatted pipeline script format (AAPS v1) into a canonical IR (`autoappdev_ir` v1) without executing code, and with errors that point to the exact failing line.

## How To Verify
In this repo (static + functional smoke):
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 -m py_compile backend/app.py backend/pipeline_parser.py
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_formatted_script_v1.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
assert ir["tasks"] and ir["tasks"][0]["steps"]
print("OK")
PY
```

Manual HTTP check (requires running the backend; not possible in this sandbox):
```bash
curl -sS -X POST 'http://127.0.0.1:8788/api/scripts/parse' \
  -H 'content-type: application/json' \
  -d '{"script_text":"AUTOAPPDEV_PIPELINE 1\n\nTASK {\"id\":\"t1\",\"title\":\"Demo\"}\nSTEP {\"id\":\"s1\",\"title\":\"Work\",\"block\":\"work\"}\nACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"}'
```

