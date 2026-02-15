# Debug Notes: 043 aaps_numbering_placeholders_spec

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s rg -n "AAPS Numbering|Numbered \\+ indented|\\{\\{task\\.title\\}\\}|\\{\\{task\\.acceptance\\}\\}|\\{\\{runtime_dir\\}\\}" \
  docs/aaps-numbering-placeholders.md docs/pipeline-formatted-script-spec.md examples/pipeline_meta_round_numbered_placeholders_v0.aaps
```

Result (excerpt):
```text
docs/aaps-numbering-placeholders.md:1:# AAPS Numbering + Placeholders (Convention v0)
docs/aaps-numbering-placeholders.md:76:- `{{task.title}}`
docs/aaps-numbering-placeholders.md:78:- `{{task.acceptance}}`
docs/aaps-numbering-placeholders.md:80:- `{{runtime_dir}}`
examples/pipeline_meta_round_numbered_placeholders_v0.aaps:19:    ACTION {"id":"a1","kind":"codex_exec","params":{"prompt":"Task: {{task.title}}...
examples/pipeline_meta_round_numbered_placeholders_v0.aaps:40:    ACTION {"id":"l1","kind":"run"...,"params":{"cmd":"mkdir -p {{runtime_dir}}/outbox ...
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_meta_round_numbered_placeholders_v0.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
assert ir["tasks"] and ir["tasks"][0]["steps"]
print("OK: example parses as AAPS v1")
PY
```

Result:
```text
OK: example parses as AAPS v1
```

## Issues Found
- None.

