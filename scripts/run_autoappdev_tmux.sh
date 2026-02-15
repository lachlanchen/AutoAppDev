#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: run_autoappdev_tmux.sh [options]

Starts (or attaches to) a tmux session that runs:
- AutoAppDev backend (Tornado) via conda env `autoappdev`
- AutoAppDev PWA via a simple static HTTP server

Options:
  --session <name>          tmux session name (default: autoappdev)
  --backend-host <host>     backend bind host (default: $AUTOAPPDEV_HOST or 127.0.0.1)
  --backend-port <port>     backend port      (default: $AUTOAPPDEV_PORT or 8788)
  --pwa-host <host>         PWA bind host     (default: 127.0.0.1)
  --pwa-port <port>         PWA port          (default: $AUTOAPPDEV_PWA_PORT or 5173)
  --skip-setup              do not run scripts/setup_autoappdev_env.sh
  --restart                 kill the session first if it already exists
  --detached                start but do not attach
  -h, --help                show help

Examples:
  ./scripts/run_autoappdev_tmux.sh
  ./scripts/run_autoappdev_tmux.sh --restart
  ./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174
USAGE
}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION="autoappdev"
BACKEND_HOST="${AUTOAPPDEV_HOST:-127.0.0.1}"
BACKEND_PORT="${AUTOAPPDEV_PORT:-8788}"
PWA_HOST="127.0.0.1"
PWA_PORT="${AUTOAPPDEV_PWA_PORT:-5173}"
SKIP_SETUP=0
RESTART=0
DETACHED=0

while [ $# -gt 0 ]; do
  case "$1" in
    --session) SESSION="${2:-}"; shift ;;
    --backend-host) BACKEND_HOST="${2:-}"; shift ;;
    --backend-port) BACKEND_PORT="${2:-}"; shift ;;
    --pwa-host) PWA_HOST="${2:-}"; shift ;;
    --pwa-port) PWA_PORT="${2:-}"; shift ;;
    --skip-setup) SKIP_SETUP=1 ;;
    --restart) RESTART=1 ;;
    --detached) DETACHED=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
  shift
done

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found." >&2
  exit 1
fi

if [ "$SKIP_SETUP" -eq 0 ]; then
  "$ROOT_DIR/scripts/setup_autoappdev_env.sh"
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
  if [ "$RESTART" -eq 1 ]; then
    tmux kill-session -t "$SESSION"
  else
    if [ "$DETACHED" -eq 1 ]; then
      echo "tmux session already running: $SESSION"
      exit 0
    fi
    tmux attach -t "$SESSION"
    exit 0
  fi
fi

tmux new-session -d -s "$SESSION" -c "$ROOT_DIR" -n dev

# Left pane: backend (tornado)
tmux send-keys -t "$SESSION:dev.0" "cd \"$ROOT_DIR\" && export AUTOAPPDEV_HOST=\"$BACKEND_HOST\" AUTOAPPDEV_PORT=\"$BACKEND_PORT\" && conda run -n autoappdev python -m backend.app" C-m

# Right pane: PWA static server
tmux split-window -h -t "$SESSION:dev" -c "$ROOT_DIR/pwa"
if command -v python3 >/dev/null 2>&1; then
  tmux send-keys -t "$SESSION:dev.1" "cd \"$ROOT_DIR/pwa\" && python3 -m http.server \"$PWA_PORT\" --bind \"$PWA_HOST\"" C-m
else
  tmux send-keys -t "$SESSION:dev.1" "cd \"$ROOT_DIR/pwa\" && conda run -n autoappdev python -m http.server \"$PWA_PORT\" --bind \"$PWA_HOST\"" C-m
fi

tmux select-pane -t "$SESSION:dev.0" -T "backend" 2>/dev/null || true
tmux select-pane -t "$SESSION:dev.1" -T "pwa" 2>/dev/null || true
tmux select-pane -t "$SESSION:dev.0"

echo "AutoAppDev backend: http://$BACKEND_HOST:$BACKEND_PORT"
echo "AutoAppDev PWA:     http://$PWA_HOST:$PWA_PORT"
echo "tmux attach -t $SESSION"

if [ "$DETACHED" -eq 1 ]; then
  exit 0
fi

tmux attach -t "$SESSION"
