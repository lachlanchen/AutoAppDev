# Debug Notes: 044 aaps_numbered_prefix_parser

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s python3 -m py_compile backend/pipeline_parser.py
```

Result:
```text
OK: py_compile
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_formatted_script_numbered_prefix_v1.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
assert ir["tasks"] and ir["tasks"][0]["steps"] and ir["tasks"][0]["steps"][0]["actions"]
print("OK: numbered-prefix example parses")
PY
```

Result:
```text
OK: numbered-prefix example parses
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_formatted_script_v1.aaps").read_text("utf-8")
parse_aaps_v1(text)
print("OK: existing example still parses")
PY
```

Result:
```text
OK: existing example still parses
```

## Issues Found
- None.

