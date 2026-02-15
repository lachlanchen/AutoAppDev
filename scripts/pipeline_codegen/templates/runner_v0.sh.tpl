#!/usr/bin/env bash
set -euo pipefail

# AutoAppDev Pipeline Runner (generated)
# Template: scripts/pipeline_codegen/templates/runner_v0.sh.tpl
# Generator: scripts/pipeline_codegen/generate_runner_from_ir.py
#
# This file is generated deterministically from an autoappdev_ir v1 JSON file.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="${AUTOAPPDEV_RUNTIME_DIR:-$ROOT_DIR/runtime}"
export AUTOAPPDEV_RUNTIME_DIR_RESOLVED="$RUNTIME_DIR"
LOG_DIR="$RUNTIME_DIR/logs"
PAUSE_FLAG="$RUNTIME_DIR/PAUSE"

mkdir -p "$LOG_DIR"

log() {
  printf '[runner] %s\n' "$*"
}

cleanup() {
  log "received stop signal, exiting"
  exit 0
}

trap cleanup INT TERM

wait_if_paused() {
  if [ -f "$PAUSE_FLAG" ]; then
    log "paused (remove $PAUSE_FLAG to resume)"
    while [ -f "$PAUSE_FLAG" ]; do
      sleep 0.5
    done
    log "resumed"
  fi
}

AUTOAPPDEV_TASK_LAST_DEBUG_FAILED=0

step_should_run() {
  local cond="${1:-}"
  if [ -z "$cond" ]; then
    return 0
  fi

  case "$cond" in
    on_debug_failure)
      [ "${AUTOAPPDEV_TASK_LAST_DEBUG_FAILED:-0}" = "1" ]
      ;;
    *)
      echo "[runner] unknown step conditional: $cond" >&2
      exit 2
      ;;
  esac
}

subst_placeholders() {
  python3 - 3<&0 <<'PY'
import os
import re
import sys

with os.fdopen(3, "r", encoding="utf-8") as f:
    text = f.read()

mapping = {
    "runtime_dir": os.environ.get("AUTOAPPDEV_RUNTIME_DIR_RESOLVED", ""),
    "task.id": os.environ.get("AUTOAPPDEV_CTX_TASK_ID", ""),
    "task.title": os.environ.get("AUTOAPPDEV_CTX_TASK_TITLE", ""),
    "task.acceptance": os.environ.get("AUTOAPPDEV_CTX_TASK_ACCEPTANCE", ""),
    "step.id": os.environ.get("AUTOAPPDEV_CTX_STEP_ID", ""),
    "step.title": os.environ.get("AUTOAPPDEV_CTX_STEP_TITLE", ""),
    "step.block": os.environ.get("AUTOAPPDEV_CTX_STEP_BLOCK", ""),
    "action.id": os.environ.get("AUTOAPPDEV_CTX_ACTION_ID", ""),
    "action.kind": os.environ.get("AUTOAPPDEV_CTX_ACTION_KIND", ""),
}

pattern = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}")


def repl(m: re.Match[str]) -> str:
    key = m.group(1).strip()
    if key in mapping:
        return mapping[key]
    sys.stderr.write(f"[runner] unknown placeholder key: {key!r}\\n")
    raise SystemExit(2)


sys.stdout.write(pattern.sub(repl, text))
PY
}

action_note() {
  local text="${1:-}"
  wait_if_paused
  log "NOTE: $text"
}

action_run() {
  local cmd="${1:-}"
  wait_if_paused
  cmd="$(printf '%s' "$cmd" | subst_placeholders)"
  log "RUN: $cmd"
  bash -lc "$cmd"
}

extract_session_id_from_jsonl() {
  local json_file="$1"
  python3 - "$json_file" <<'PY'
import json
import sys

sid = ""
with open(sys.argv[1], "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        sid = obj.get("thread_id") or obj.get("session_id") or sid
        if not sid:
            th = obj.get("thread")
            if isinstance(th, dict):
                sid = th.get("id") or sid
        if sid:
            break
print(sid)
PY
}

CODEX_MODEL_DEFAULT="${AUTOAPPDEV_CODEX_MODEL:-gpt-5.3-codex}"
CODEX_REASONING_DEFAULT="${AUTOAPPDEV_CODEX_REASONING:-medium}"
CODEX_SESSION_FILE="${AUTOAPPDEV_CODEX_SESSION_FILE:-$RUNTIME_DIR/.codex_pipeline_session}"
CODEX_SKIP_GIT_CHECK="${AUTOAPPDEV_CODEX_SKIP_GIT_CHECK:-0}"
CODEX_FULL_AUTO="${AUTOAPPDEV_CODEX_FULL_AUTO:-1}"
CODEX_ACTION_COUNTER=0

action_codex_exec() {
  local prompt="${1:-}"
  local model="${2:-$CODEX_MODEL_DEFAULT}"
  local reasoning="${3:-$CODEX_REASONING_DEFAULT}"

  wait_if_paused
  prompt="$(printf '%s' "$prompt" | subst_placeholders)"

  CODEX_ACTION_COUNTER=$((CODEX_ACTION_COUNTER + 1))
  local n="$CODEX_ACTION_COUNTER"

  local prompt_file="$LOG_DIR/codex_${n}.prompt.txt"
  local json_file="$LOG_DIR/codex_${n}.jsonl"

  local sid=""
  if [ -f "$CODEX_SESSION_FILE" ]; then
    sid="$(tr -d ' \t\r\n' < "$CODEX_SESSION_FILE" || true)"
  fi

  printf '%s\n' "$prompt" > "$prompt_file"

  if [ "${AUTOAPPDEV_CODEX_DISABLE:-0}" = "1" ]; then
    log "CODEX(disabled): wrote prompt to $prompt_file"
    cat "$prompt_file"
    return 0
  fi

  if ! command -v codex >/dev/null 2>&1; then
    echo "[runner] codex not found on PATH" >&2
    exit 1
  fi

  local -a cmd
  if [ -n "$sid" ]; then
    cmd=(codex exec resume "$sid" --json -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  else
    cmd=(codex exec --json -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  fi

  if [ "$CODEX_FULL_AUTO" = "1" ]; then
    cmd+=(--full-auto)
  fi
  if [ "$CODEX_SKIP_GIT_CHECK" = "1" ]; then
    cmd+=(--skip-git-repo-check)
  fi
  cmd+=(-)

  log "CODEX: model=$model reasoning=$reasoning session=${sid:-new} output=$json_file"
  "${cmd[@]}" < "$prompt_file" > "$json_file" 2>>"$LOG_DIR/codex_stderr.log"

  if [ -z "$sid" ]; then
    sid="$(extract_session_id_from_jsonl "$json_file" || true)"
    if [ -n "$sid" ]; then
      printf '%s\n' "$sid" > "$CODEX_SESSION_FILE"
      log "CODEX: saved session id to $CODEX_SESSION_FILE"
    fi
  fi
}

main() {
  log "runner starting"
  log "runtime_dir: $RUNTIME_DIR"

  wait_if_paused

__PIPELINE_BODY__

  log "runner done"
}

main "$@"
