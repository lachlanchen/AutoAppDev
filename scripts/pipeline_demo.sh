#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="${AUTOAPPDEV_RUNTIME_DIR:-$ROOT_DIR/runtime}"
PAUSE_FLAG="$RUNTIME_DIR/PAUSE"

cleanup() {
  echo "[demo] received stop signal, exiting"
  exit 0
}

trap cleanup INT TERM

echo "[demo] pipeline_demo.sh starting"
echo "[demo] time: $(date -Iseconds)"
echo "[demo] runtime_dir: $RUNTIME_DIR"

i=1
max="${DEMO_TICKS:-120}"

while [ "$i" -le "$max" ]; do
  if [ -f "$PAUSE_FLAG" ]; then
    echo "[demo] paused (remove $PAUSE_FLAG to resume)"
    while [ -f "$PAUSE_FLAG" ]; do
      sleep 0.5
    done
    echo "[demo] resumed"
  fi

  echo "[demo] tick $i/$max"
  i=$((i + 1))
  sleep 1
done

echo "[demo] done"

