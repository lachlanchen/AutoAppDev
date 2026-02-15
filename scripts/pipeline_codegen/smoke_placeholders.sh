#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

ir_path="${1:-$ROOT_DIR/examples/pipeline_ir_placeholders_smoke_v0.json}"
out_runner="${2:-/tmp/autoappdev_runner_placeholders.sh}"
runtime_dir="${3:-/tmp/autoappdev_runtime_placeholders_$$}"
out_log="${4:-/tmp/autoappdev_runner_placeholders_$$.log}"

python3 -m json.tool "$ir_path" >/dev/null

python3 "$ROOT_DIR/scripts/pipeline_codegen/generate_runner_from_ir.py" \
  --in "$ir_path" \
  --out "$out_runner"

bash -n "$out_runner"

rm -rf "$runtime_dir"
mkdir -p "$runtime_dir"

AUTOAPPDEV_CODEX_DISABLE=1 \
AUTOAPPDEV_RUNTIME_DIR="$runtime_dir" \
timeout 10s bash "$out_runner" >"$out_log" 2>&1

if rg -nF '{{' "$out_log" >/dev/null; then
  echo "[smoke] error: found unsubstituted placeholders in output log: $out_log" >&2
  rg -nF '{{' "$out_log" >&2 || true
  exit 1
fi

rg -n 'PLACEHOLDERS_RUN task=t_ph' "$out_log" >/dev/null
rg -n 'step=s1' "$out_log" >/dev/null
rg -nF "runtime=$runtime_dir" "$out_log" >/dev/null
rg -n 'acceptance=Acceptance_placeholders_smoke_v0' "$out_log" >/dev/null
rg -n 'title=Runner_placeholders_smoke_v0' "$out_log" >/dev/null
rg -n 'action=a_run/run' "$out_log" >/dev/null
rg -n 'PLACEHOLDERS_CODEX task=t_ph' "$out_log" >/dev/null

echo "[smoke] ok: $out_runner (log: $out_log)"
