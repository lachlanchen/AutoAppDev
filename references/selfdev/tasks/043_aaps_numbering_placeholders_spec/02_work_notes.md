# Work Notes: 043 aaps_numbering_placeholders_spec

## Implementation Notes
- Added docs for a Scratch-like readability + templating convention while keeping AAPS v1 grammar unchanged:
  - `docs/aaps-numbering-placeholders.md` defines:
    - display-only numbering via `# 1.2.3` comment lines + indentation levels (TASK/STEP/ACTION), remaining AAPS v1-compatible
    - minimal `{{...}}` placeholder syntax for string fields (recommended: `ACTION.params.prompt`, `ACTION.params.cmd`)
    - required placeholders: `{{task.title}}`, `{{task.acceptance}}` (from `TASK.meta.acceptance`), `{{runtime_dir}}` (from `AUTOAPPDEV_RUNTIME_DIR`, default `./runtime`)
- Linked the convention from the canonical spec:
  - `docs/pipeline-formatted-script-spec.md` section “1.8 Numbering + Placeholders (Conventions v0)”
- Added a complete example script:
  - `examples/pipeline_meta_round_numbered_placeholders_v0.aaps`
  - Includes `meta_round_v0`, conditional fix step (`STEP.meta.conditional="on_debug_failure"`), numbering comments, indentation, and placeholder usage in prompt/cmd strings.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

nl -ba scripts/auto-autoappdev-development.sh | sed -n '270,320p'
sed -n '1,140p' docs/pipeline-formatted-script-spec.md
sed -n '1,240p' backend/pipeline_parser.py

timeout 10s rg -n "AAPS Numbering|Numbered \\+ indented|\\{\\{task\\.title\\}\\}|\\{\\{task\\.acceptance\\}\\}|\\{\\{runtime_dir\\}\\}" \
  docs/aaps-numbering-placeholders.md docs/pipeline-formatted-script-spec.md examples/pipeline_meta_round_numbered_placeholders_v0.aaps

timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1
text = Path("examples/pipeline_meta_round_numbered_placeholders_v0.aaps").read_text("utf-8")
ir = parse_aaps_v1(text)
assert ir["kind"] == "autoappdev_ir" and ir["version"] == 1
assert ir["tasks"]
print("OK: example parses as AAPS v1")
PY
```

