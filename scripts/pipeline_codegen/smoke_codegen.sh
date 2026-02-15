#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

ir_path="${1:-$ROOT_DIR/examples/pipeline_ir_codegen_demo_v0.json}"
out_a="${2:-/tmp/autoappdev_runner_a.sh}"
out_b="${3:-/tmp/autoappdev_runner_b.sh}"

python3 -m json.tool "$ir_path" >/dev/null

python3 "$ROOT_DIR/scripts/pipeline_codegen/generate_runner_from_ir.py" --in "$ir_path" --out "$out_a"
python3 "$ROOT_DIR/scripts/pipeline_codegen/generate_runner_from_ir.py" --in "$ir_path" --out "$out_b"

diff -u "$out_a" "$out_b" >/dev/null
bash -n "$out_a"

echo "[smoke] ok: $out_a"

