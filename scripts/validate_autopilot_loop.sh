#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

run_python_check() {
  python3 - "$@" <<'PY'
import sys
from pathlib import Path

from backend.pipeline_parser import parse_aaps_v1

paths = [Path("references/autopilot/loop/accepted.aaps")]
proposed = Path("references/autopilot/loop/proposed.aaps")
if proposed.exists():
    paths.append(proposed)

ok = True
for path in paths:
    try:
        ir = parse_aaps_v1(path.read_text("utf-8"))
    except Exception as exc:
        ok = False
        print(f"{path}: FAIL {type(exc).__name__}: {exc}")
    else:
        print(f"{path}: OK tasks={len(ir.get('tasks', []))}")
if not ok:
    raise SystemExit(1)
PY
}

if [[ "${AUTOAPPDEV_VALIDATE_IN_DOCKER:-0}" == "1" ]] && command -v docker >/dev/null 2>&1; then
  docker run --rm -v "$PWD":/repo -w /repo python:3.11-slim bash -lc "$(declare -f run_python_check); run_python_check"
else
  run_python_check
fi
