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
OUTBOX_DIR="$RUNTIME_DIR/outbox"
PAUSE_FLAG="$RUNTIME_DIR/PAUSE"

mkdir -p "$LOG_DIR"

log() {
  printf '[runner] %s\n' "$*"
}

outbox_write() {
  # Best-effort status channel for operator UI (no HTTP required).
  # Backend ingests: runtime/outbox/<ts>_<role>.md|.txt (see docs/api-contracts.md).
  local content="${1:-}"
  local role="${2:-pipeline}"

  if [ -z "$content" ]; then
    return 0
  fi

  case "$role" in
    pipeline|system)
      ;;
    *)
      role="pipeline"
      ;;
  esac

  set +e

  mkdir -p "$OUTBOX_DIR" >/dev/null 2>&1

  local ts=""
  ts="$(
    python3 - <<'PY'
import time
print(time.time_ns(), end="")
PY
  )"
  if [ -z "$ts" ]; then
    ts="$(date +%s%3N 2>/dev/null)"
  fi
  if [ -z "$ts" ]; then
    ts="0"
  fi

  local tmp="$OUTBOX_DIR/.tmp.${ts}.$$"
  local out="$OUTBOX_DIR/${ts}_${role}.md"
  printf '%s\n' "$content" > "$tmp" 2>/dev/null
  mv "$tmp" "$out" 2>/dev/null
  local rc=$?
  if [ "$rc" -ne 0 ]; then
    rm -f "$tmp" 2>/dev/null
    log "warn: failed to write outbox message"
  fi

  set -e
  return 0
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

META_ROUND_RESUME_FILE="${AUTOAPPDEV_META_ROUND_RESUME_FILE:-$RUNTIME_DIR/meta_round_v0_resume.json}"

meta_round_read_task_list() {
  local task_list_path="${1:-}"
  python3 - "$task_list_path" <<'PY'
import json
import sys
from pathlib import Path

def die(msg: str) -> None:
    sys.stderr.write(f"[runner] meta_round: {msg}\n")
    raise SystemExit(2)

if len(sys.argv) < 2 or not sys.argv[1]:
    die("missing task_list_path")

p = Path(sys.argv[1])
try:
    obj = json.loads(p.read_text(encoding="utf-8"))
except FileNotFoundError:
    die(f"task list not found: {p}")
except json.JSONDecodeError as e:
    die(f"invalid JSON in task list {p}: {e}")

if not isinstance(obj, dict):
    die(f"task list must be an object: {p}")

if obj.get("kind") != "autoappdev_task_list" or obj.get("version") != 0:
    die(f"unexpected task list kind/version (expected autoappdev_task_list v0): {p}")

tasks = obj.get("tasks")
if not isinstance(tasks, list):
    die(f"task list .tasks must be an array: {p}")

out = sys.stdout.buffer
for i, t in enumerate(tasks):
    if not isinstance(t, dict):
        die(f"task list tasks[{i}] must be an object: {p}")
    tid = t.get("id")
    title = t.get("title")
    acc = t.get("acceptance") if t.get("acceptance") is not None else ""
    if not isinstance(tid, str) or not tid:
        die(f"task list tasks[{i}].id must be a non-empty string: {p}")
    if not isinstance(title, str) or not title:
        die(f"task list tasks[{i}].title must be a non-empty string: {p}")
    if not isinstance(acc, str):
        die(f"task list tasks[{i}].acceptance must be a string: {p}")

    out.write(tid.encode("utf-8") + b"\0")
    out.write(title.encode("utf-8") + b"\0")
    out.write(acc.encode("utf-8") + b"\0")
PY
}

meta_round_is_completed() {
  local task_id="${1:-}"
  local resume_file="${2:-$META_ROUND_RESUME_FILE}"
  set +e
  python3 - "$resume_file" "$task_id" <<'PY'
import json
import sys
from pathlib import Path

resume = Path(sys.argv[1])
task_id = sys.argv[2]

if not resume.exists():
    raise SystemExit(1)

try:
    obj = json.loads(resume.read_text(encoding="utf-8"))
except Exception as e:
    sys.stderr.write(f"[runner] meta_round: invalid resume JSON {resume}: {type(e).__name__}: {e}\n")
    raise SystemExit(2)

if not isinstance(obj, dict):
    sys.stderr.write(f"[runner] meta_round: resume must be an object: {resume}\n")
    raise SystemExit(2)

ids = obj.get("completed_task_ids", [])
if not isinstance(ids, list):
    sys.stderr.write(f"[runner] meta_round: resume completed_task_ids must be an array: {resume}\n")
    raise SystemExit(2)

if task_id in ids:
    raise SystemExit(0)
raise SystemExit(1)
PY
  local rc=$?
  set -e
  if [ "$rc" -eq 2 ]; then
    exit 2
  fi
  return "$rc"
}

meta_round_mark_completed() {
  local task_id="${1:-}"
  local resume_file="${2:-$META_ROUND_RESUME_FILE}"
  python3 - "$resume_file" "$task_id" <<'PY'
import datetime
import json
import sys
from pathlib import Path

resume = Path(sys.argv[1])
task_id = sys.argv[2]

resume.parent.mkdir(parents=True, exist_ok=True)

obj = {"kind": "autoappdev_meta_round_resume", "version": 0, "completed_task_ids": []}
if resume.exists():
    try:
        loaded = json.loads(resume.read_text(encoding="utf-8"))
    except Exception as e:
        sys.stderr.write(f"[runner] meta_round: invalid resume JSON {resume}: {type(e).__name__}: {e}\n")
        raise SystemExit(2)
    if isinstance(loaded, dict):
        obj = loaded
    else:
        sys.stderr.write(f"[runner] meta_round: resume must be an object: {resume}\n")
        raise SystemExit(2)

ids = obj.get("completed_task_ids")
if ids is None:
    ids = []
if not isinstance(ids, list):
    sys.stderr.write(f"[runner] meta_round: resume completed_task_ids must be an array: {resume}\n")
    raise SystemExit(2)

if task_id not in ids:
    ids.append(task_id)
obj["completed_task_ids"] = ids
obj["updated_at"] = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

tmp = resume.with_suffix(resume.suffix + ".tmp")
tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp.replace(resume)
PY
}

meta_round_run_template_tasks() {
  local task_list_path="${1:-}"
  if [ -z "$task_list_path" ]; then
    echo "[runner] meta_round: missing task_list_path" >&2
    exit 2
  fi

  local tmp_tasks=""
  tmp_tasks="$(mktemp "$RUNTIME_DIR/.meta_round_tasks.XXXXXX")"
  meta_round_read_task_list "$task_list_path" > "$tmp_tasks"

  while IFS= read -r -d '' task_id \
    && IFS= read -r -d '' task_title \
    && IFS= read -r -d '' task_acceptance; do
    if meta_round_is_completed "$task_id" "$META_ROUND_RESUME_FILE"; then
      log "SKIP META_TASK $task_id: already completed"
      outbox_write "SKIP META_TASK $task_id: already completed" pipeline
      continue
    fi

    log "META_TASK $task_id: start"
    outbox_write "META_TASK $task_id: start ($task_title)" pipeline
    run_task_template_v0 "$task_id" "$task_title" "$task_acceptance"
    meta_round_mark_completed "$task_id" "$META_ROUND_RESUME_FILE"
    log "META_TASK $task_id: done"
    outbox_write "META_TASK $task_id: done" pipeline
  done < "$tmp_tasks"

  rm -f "$tmp_tasks"
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
