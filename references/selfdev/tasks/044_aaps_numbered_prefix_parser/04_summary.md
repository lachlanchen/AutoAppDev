# Summary: 044 aaps_numbered_prefix_parser

## What Changed
- Updated the deterministic AAPS parser to accept optional numeric prefixes before `TASK|STEP|ACTION`:
  - `backend/pipeline_parser.py` now supports lines like `1.2 STEP {...}` (and `1.2. STEP {...}`) while keeping parsing deterministic and preserving existing semantics.
- Added a numbered-prefix example script:
  - `examples/pipeline_formatted_script_numbered_prefix_v1.aaps`
- Updated numbering docs to stay accurate:
  - `docs/aaps-numbering-placeholders.md` no longer claims numeric-prefix lines are unparseable; it still recommends comment numbering as the most portable convention.

## Why
Task 044 acceptance requires the backend parser to accept optional numeric prefixes (Scratch-like numbering) without changing the underlying deterministic AAPS v1 structure.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/pipeline_parser.py

timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_formatted_script_numbered_prefix_v1.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
print("OK")
PY
```

