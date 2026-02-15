# Debug Notes: 023 pipeline_formatted_script_spec

## Goal
Smallest possible verification for the new formatted script + IR spec:
- Ensure the doc exists and contains the required concepts (versioned script, TASK/STEP/ACTION, IR schema, mapping to PWA blocks).
- Ensure the example IR JSON is valid.
- Ensure `README.md` links to the spec for discoverability.

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f docs/pipeline-formatted-script-spec.md
test -f examples/pipeline_formatted_script_v1.aaps
test -f examples/pipeline_ir_v1.json

rg -n 'AUTOAPPDEV_PIPELINE\\s+1|\\bTASK\\b|\\bSTEP\\b|\\bACTION\\b' docs/pipeline-formatted-script-spec.md
rg -n 'autoappdev_ir|\"tasks\"\\s*:' docs/pipeline-formatted-script-spec.md
rg -n 'plan\\b|work\\b|debug\\b|fix\\b|summary\\b|commit_push\\b' docs/pipeline-formatted-script-spec.md

python3 -m json.tool examples/pipeline_ir_v1.json >/dev/null

rg -n 'pipeline-formatted-script-spec\\.md' README.md
```

Result:
- Spec doc and both example artifacts exist.
- Spec includes:
  - Script header `AUTOAPPDEV_PIPELINE 1`
  - Statement keywords `TASK`, `STEP`, `ACTION`
  - Canonical IR `kind: autoappdev_ir` with `tasks -> steps -> actions`
  - Explicit mapping of `STEP.block` to PWA blocks (`plan/work/debug/fix/summary/commit_push`)
- Example IR JSON validates via `python3 -m json.tool`.
- `README.md` links to the spec doc.

## Issues Found
- None in static verification.

