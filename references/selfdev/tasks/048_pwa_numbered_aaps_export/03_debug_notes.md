# Debug Notes: 048 pwa_numbered_aaps_export

## What I Verified (Smallest Possible)
This sandbox cannot bind/listen on ports, so I could not run the PWA in a browser. Verification here is limited to:
- Static JS syntax check for the updated AAPS generator.
- Deterministic backend parser checks showing imports tolerate both:
  - comment-numbered + indented AAPS (the PWA export format), and
  - numeric-prefix AAPS lines (e.g. `1.2 STEP {...}`).

## Verification Commands (With Results)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

timeout 10s python3 -m py_compile backend/pipeline_parser.py

timeout 10s python3 - <<'PY'
from pathlib import Path
from backend.pipeline_parser import parse_aaps_v1

paths = [
  'examples/pipeline_meta_round_numbered_placeholders_v0.aaps',
  'examples/pipeline_formatted_script_numbered_prefix_v1.aaps',
]
for p in paths:
  ir = parse_aaps_v1(Path(p).read_text('utf-8'))
  assert ir['kind'] == 'autoappdev_ir' and ir['version'] == 1
print('OK')
PY

timeout 10s python3 - <<'PY'
# Synthetic smoke: accept PWA-shaped output (numbering comments + indentation).
from backend.pipeline_parser import parse_aaps_v1

script = """AUTOAPPDEV_PIPELINE 1

# 1 Task
TASK  {"id":"t1","title":"Demo"}

# 1.1 Step
  STEP  {"id":"s1","title":"Plan","block":"plan"}
# 1.1.1 Action
    ACTION {"id":"a1","kind":"noop","params":{}}

"""

ir = parse_aaps_v1(script)
assert ir["kind"] == "autoappdev_ir"
assert ir["tasks"][0]["steps"][0]["block"] == "plan"
print("OK")
PY
```

Result:
- `node --check pwa/app.js`: exit 0
- `python3 -m py_compile backend/pipeline_parser.py`: exit 0
- parser checks: `OK`

## Issues Found + Minimal Fixes Applied
- None.

## Manual Verification (Outside This Sandbox)
1. Serve `pwa/` and run backend locally (see `pwa/README.md`).
2. Script tab:
   - Add 2-3 blocks and click `From Blocks`.
   - Confirm the textarea AAPS includes `# 1 ...` numbering comments and indented `STEP`/`ACTION` lines.
   - Click `Download AAPS` and confirm the downloaded `.aaps` matches.
   - Paste `examples/pipeline_formatted_script_numbered_prefix_v1.aaps` and click `Parse AAPS -> Blocks`; confirm it parses.

