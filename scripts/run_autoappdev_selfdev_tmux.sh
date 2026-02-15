#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: run_autoappdev_selfdev_tmux.sh [options]

Starts (or attaches to) a tmux session running the AutoAppDev self-dev driver:
`scripts/auto-autoappdev-development.sh`

Options:
  --session <name>          tmux session name (default: autoappdev-selfdev)
  --model <name>            Codex model (default: gpt-5.3-codex)
  --reasoning <effort>      none|minimal|low|medium|high|xhigh (default: xhigh)
  --start-at <n>            start at task sequence n (default: 1)
  --max-tasks <n>           run at most n tasks (default: 0 = unlimited)
  --new-session             start a fresh Codex session (ignore saved session id)
  --sandbox <mode>          Codex sandbox (default: danger-full-access)
  --approval <mode>         Codex approval (default: never)
  --stop-file <path>        stop after finishing current task if file exists
  --verbose                 pass --verbose to the self-dev runner
  --restart                 kill the session first if it already exists
  --detached                start but do not attach
  -h, --help                show help

Examples:
  ./scripts/run_autoappdev_selfdev_tmux.sh --restart
  ./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh
USAGE
}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION="autoappdev-selfdev"
MODEL="gpt-5.3-codex"
REASONING="xhigh"
START_AT="1"
MAX_TASKS="0"
NEW_SESSION=0
SANDBOX="danger-full-access"
APPROVAL="never"
STOP_FILE=""
VERBOSE=0
RESTART=0
DETACHED=0

while [ $# -gt 0 ]; do
  case "$1" in
    --session) SESSION="${2:-}"; shift ;;
    --model) MODEL="${2:-}"; shift ;;
    --reasoning) REASONING="${2:-}"; shift ;;
    --start-at) START_AT="${2:-}"; shift ;;
    --max-tasks) MAX_TASKS="${2:-}"; shift ;;
    --new-session) NEW_SESSION=1 ;;
    --sandbox) SANDBOX="${2:-}"; shift ;;
    --approval) APPROVAL="${2:-}"; shift ;;
    --stop-file) STOP_FILE="${2:-}"; shift ;;
    --verbose) VERBOSE=1 ;;
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

mkdir -p "$ROOT_DIR/runtime/logs"
LOG_FILE="$ROOT_DIR/runtime/logs/selfdev_runner.log"

cmd=(bash -lc)
runner="cd \"$ROOT_DIR\" && ./scripts/auto-autoappdev-development.sh --model \"$MODEL\" --reasoning \"$REASONING\" --sandbox \"$SANDBOX\" --approval \"$APPROVAL\" --start-at \"$START_AT\""
if [ "$MAX_TASKS" != "0" ]; then
  runner+=" --max-tasks \"$MAX_TASKS\""
fi
if [ "$NEW_SESSION" -eq 1 ]; then
  runner+=" --new-session"
fi
if [ -n "$STOP_FILE" ]; then
  runner+=" --stop-file \"$STOP_FILE\""
fi
if [ "$VERBOSE" -eq 1 ]; then
  runner+=" --verbose"
fi
runner+=" 2>&1 | tee -a \"$LOG_FILE\""

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

tmux new-session -d -s "$SESSION" -c "$ROOT_DIR" -n selfdev
tmux send-keys -t "$SESSION:selfdev.0" "$runner" C-m
tmux select-pane -t "$SESSION:selfdev.0" -T "selfdev" 2>/dev/null || true

echo "AutoAppDev selfdev logs: $LOG_FILE"
echo "tmux attach -t $SESSION"

if [ "$DETACHED" -eq 1 ]; then
  exit 0
fi
tmux attach -t "$SESSION"

