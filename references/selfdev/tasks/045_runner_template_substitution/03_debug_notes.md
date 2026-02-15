# Debug Notes: 045 runner_template_substitution

## Verification Commands (With Results)
`rg` availability:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
command -v rg
rg --version | head -n 1
```
Result: `rg` present (ripgrep 14.1.1).

Main checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

chmod +x scripts/pipeline_codegen/smoke_placeholders.sh
timeout 10s python3 -m py_compile scripts/pipeline_codegen/generate_runner_from_ir.py
python3 -m json.tool examples/pipeline_ir_placeholders_smoke_v0.json >/dev/null
timeout 20s scripts/pipeline_codegen/smoke_placeholders.sh
timeout 20s scripts/pipeline_codegen/smoke_codegen.sh
```
Result:
- `smoke_placeholders.sh`: `[smoke] ok: /tmp/autoappdev_runner_placeholders.sh (log: /tmp/autoappdev_runner_placeholders_*.log)`
- `smoke_codegen.sh`: `[smoke] ok: /tmp/autoappdev_runner_a.sh`

## Issues Found + Minimal Fixes Applied
- `scripts/pipeline_codegen/smoke_placeholders.sh` initially used `rg -n '{{' ...` which fails because `{` is a regex metacharacter.
  - Fix: switched to fixed-string search `rg -nF '{{' ...`.
- Placeholder substitution initially produced empty substituted strings because `subst_placeholders()` used `python3 - <<'PY'` (the here-doc consumed stdin).
  - Fix: updated `subst_placeholders()` to preserve piped input on fd3 (`python3 - 3<&0 <<'PY'`) and read from fd3 in Python.
- Substitution still didn’t apply due to an over-escaped placeholder regex.
  - Fix: corrected pattern to `re.compile(r"\{\{\s*([^{}]+?)\s*\}\}")` in `scripts/pipeline_codegen/templates/runner_v0.sh.tpl`.
