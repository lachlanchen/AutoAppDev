#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

ir_path="${1:-$ROOT_DIR/examples/pipeline_ir_meta_round_v0_demo_v0.json}"
out_runner="${2:-/tmp/autoappdev_runner_meta_round_v0.sh}"
work_dir="${3:-}"
runtime_dir="${4:-}"

python3 -m json.tool "$ir_path" >/dev/null

python3 "$ROOT_DIR/scripts/pipeline_codegen/generate_runner_from_ir.py" \
  --in "$ir_path" \
  --out "$out_runner"

bash -n "$out_runner"

if [ -z "$work_dir" ]; then
  work_dir="$(mktemp -d /tmp/autoappdev_meta_round_work.XXXXXX)"
fi
if [ -z "$runtime_dir" ]; then
  runtime_dir="$(mktemp -d /tmp/autoappdev_meta_round_runtime.XXXXXX)"
fi

log1="$(mktemp /tmp/autoappdev_meta_round_run1.XXXXXX.log)"
log2="$(mktemp /tmp/autoappdev_meta_round_run2.XXXXXX.log)"

(cd "$work_dir" && AUTOAPPDEV_RUNTIME_DIR="$runtime_dir" timeout 20s bash "$out_runner" >"$log1" 2>&1)

test -f "$work_dir/task_list.json"
test -f "$runtime_dir/meta_round_v0_resume.json"

rg -n 'TEMPLATE_RUN id=t1' "$log1" >/dev/null
rg -n 'TEMPLATE_RUN id=t2' "$log1" >/dev/null

(cd "$work_dir" && AUTOAPPDEV_RUNTIME_DIR="$runtime_dir" timeout 20s bash "$out_runner" >"$log2" 2>&1)

rg -nF 'SKIP META_TASK t1: already completed' "$log2" >/dev/null
rg -nF 'SKIP META_TASK t2: already completed' "$log2" >/dev/null
if rg -n 'TEMPLATE_RUN id=' "$log2" >/dev/null; then
  echo "[smoke] error: template ran unexpectedly on second run (resume should skip)" >&2
  exit 1
fi

echo "[smoke] ok: $out_runner (work: $work_dir runtime: $runtime_dir)"

