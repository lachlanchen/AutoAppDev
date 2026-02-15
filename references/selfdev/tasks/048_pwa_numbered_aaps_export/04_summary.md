# Summary: 048 pwa_numbered_aaps_export

## What Changed (And Why)
- Updated the PWA AAPS generator to export **numbered + indented** AAPS v1 for readability (Scratch-like), without changing semantics:
  - `pwa/app.js` `programToAapsScript()` now emits numbering as comment lines (`# 1`, `# 1.N`, `# 1.N.1`) and indents `STEP`/`ACTION` statements.
- Import tolerance for numeric prefixes (e.g. `1.2 STEP {...}`) is already supported by the deterministic backend parser (`backend/pipeline_parser.py`), so no additional code changes were required for imports.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

timeout 10s python3 -m py_compile backend/pipeline_parser.py
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
for p in [
  "examples/pipeline_meta_round_numbered_placeholders_v0.aaps",
  "examples/pipeline_formatted_script_numbered_prefix_v1.aaps",
]:
  ir = parse_aaps_v1(Path(p).read_text("utf-8"))
  assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
print("OK")
PY
```

