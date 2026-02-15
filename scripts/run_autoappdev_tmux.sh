#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION="autoappdev"
BACKEND_HOST="${AUTOAPPDEV_HOST:-127.0.0.1}"
BACKEND_PORT="${AUTOAPPDEV_PORT:-8788}"
PWA_HOST="127.0.0.1"
PWA_PORT="${AUTOAPPDEV_PWA_PORT:-5173}"

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found." >&2
  exit 1
fi

"$ROOT_DIR/scripts/setup_autoappdev_env.sh"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux attach -t "$SESSION"
  exit 0
fi

tmux new-session -d -s "$SESSION" -c "$ROOT_DIR" -n dev

# Left pane: backend (tornado)
tmux send-keys -t "$SESSION:dev.0" "cd \"$ROOT_DIR\" && export AUTOAPPDEV_HOST=\"$BACKEND_HOST\" AUTOAPPDEV_PORT=\"$BACKEND_PORT\" && conda run -n autoappdev python -m backend.app" C-m

# Right pane: PWA static server
tmux split-window -h -t "$SESSION:dev" -c "$ROOT_DIR/pwa"
tmux send-keys -t "$SESSION:dev.1" "cd \"$ROOT_DIR/pwa\" && python3 -m http.server \"$PWA_PORT\" --bind \"$PWA_HOST\"" C-m

tmux select-pane -t "$SESSION:dev.0"

echo "AutoAppDev backend: http://$BACKEND_HOST:$BACKEND_PORT"
echo "AutoAppDev PWA:     http://$PWA_HOST:$PWA_PORT"
echo "tmux attach -t $SESSION"

tmux attach -t "$SESSION"

