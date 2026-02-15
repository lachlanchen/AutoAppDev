#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

ir_path="${1:-$ROOT_DIR/examples/pipeline_ir_conditional_steps_demo_v0.json}"
out_runner="${2:-/tmp/autoappdev_runner_conditional.sh}"
runtime_dir="${3:-/tmp/autoappdev_runtime_conditional_$$}"
out_log="${4:-/tmp/autoappdev_runner_conditional_$$.log}"

python3 -m json.tool "$ir_path" >/dev/null

python3 "$ROOT_DIR/scripts/pipeline_codegen/generate_runner_from_ir.py" \
  --in "$ir_path" \
  --out "$out_runner"

bash -n "$out_runner"

rm -rf "$runtime_dir"
mkdir -p "$runtime_dir"

AUTOAPPDEV_RUNTIME_DIR="$runtime_dir" \
timeout 10s bash "$out_runner" >"$out_log" 2>&1 || true

# First task: debug passes => fix should be skipped.
rg -n 'TASK t_cond_pass' "$out_log" >/dev/null
rg -n 'DEBUG_OK' "$out_log" >/dev/null
rg -n 'SKIP STEP f1 \\(fix\\): conditional=on_debug_failure' "$out_log" >/dev/null
if rg -n 'FIX_RAN_UNEXPECTED' "$out_log" >/dev/null; then
  echo "[smoke] error: fix ran unexpectedly for passing debug" >&2
  exit 1
fi

# Second task: debug fails => fix should run.
rg -n 'TASK t_cond_fail' "$out_log" >/dev/null
rg -n 'DEBUG_FAIL' "$out_log" >/dev/null
rg -n 'FIX_RAN_EXPECTED' "$out_log" >/dev/null

echo "[smoke] ok: $out_runner (log: $out_log)"

