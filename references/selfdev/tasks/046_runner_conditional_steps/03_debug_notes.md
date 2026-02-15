# Debug Notes: 046 runner_conditional_steps

## Verification Commands (With Results)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

chmod +x scripts/pipeline_codegen/smoke_conditional_steps.sh
timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_conditional_steps_demo_v0.json >/dev/null

timeout 20s scripts/pipeline_codegen/smoke_conditional_steps.sh
timeout 20s scripts/pipeline_codegen/smoke_placeholders.sh
timeout 20s scripts/pipeline_codegen/smoke_codegen.sh
```

Result:
- `smoke_conditional_steps.sh`: `[smoke] ok: /tmp/autoappdev_runner_conditional.sh (log: /tmp/autoappdev_runner_conditional_*.log)`
- `smoke_placeholders.sh`: `[smoke] ok: /tmp/autoappdev_runner_placeholders.sh (log: /tmp/autoappdev_runner_placeholders_*.log)`
- `smoke_codegen.sh`: `[smoke] ok: /tmp/autoappdev_runner_a.sh`

## Issues Found + Minimal Fixes Applied
- `scripts/pipeline_codegen/smoke_conditional_steps.sh` initially failed because the `rg` pattern for the skip line had over-escaped parentheses.
  - Fix: switched to fixed-string match for the skip log line: `rg -nF 'SKIP STEP f1 (fix): conditional=on_debug_failure' ...`.

