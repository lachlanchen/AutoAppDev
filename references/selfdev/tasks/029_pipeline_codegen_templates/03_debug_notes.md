# Debug Notes: 029 pipeline_codegen_templates

## Verification (Smallest Smoke)

### Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

test -f scripts/pipeline_codegen/generate_runner_from_ir.py \
  && test -f scripts/pipeline_codegen/templates/runner_v0.sh.tpl \
  && test -f scripts/pipeline_codegen/smoke_codegen.sh \
  && test -f examples/pipeline_ir_codegen_demo_v0.json \
  && test -f docs/pipeline-runner-codegen.md \
  && echo "files_ok"
# -> files_ok

timeout 10s python3 -m json.tool examples/pipeline_ir_codegen_demo_v0.json >/dev/null && echo "json_ok"
# -> json_ok

timeout 10s python3 scripts/pipeline_codegen/generate_runner_from_ir.py --in examples/pipeline_ir_codegen_demo_v0.json --out /tmp/runner_a.sh
timeout 10s python3 scripts/pipeline_codegen/generate_runner_from_ir.py --in examples/pipeline_ir_codegen_demo_v0.json --out /tmp/runner_b.sh
diff -u /tmp/runner_a.sh /tmp/runner_b.sh >/dev/null && echo "deterministic_ok"
# -> deterministic_ok

timeout 10s bash -n /tmp/runner_a.sh && echo "bash_syntax_ok"
# -> bash_syntax_ok

timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py && echo "py_compile_ok"
# -> py_compile_ok

head -n 40 /tmp/runner_a.sh
# -> shows generated runner header + pause helpers + action_note wiring
```

## Issues Found
- None in the smoke checks above.

