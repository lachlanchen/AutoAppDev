#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: codex_analyze_ls.sh [options]

Runs `ls -la`, then asks Codex to analyze the listing.

Options:
  --resume-last               Resume the most recent exec session
  --session <id>              Resume a specific exec session
  --session-file <path>       Persist a session ID and reuse it
  --session-mode <mode>       Session mode: auto, new, or resume (default: auto)
  --skip-git-check            Allow running outside a Git repo
  --json                      Emit JSONL events instead of formatted text
  --output-last-message <p>   Write the final assistant message to a file
  --prompt <text>             Custom prompt prefix (listing is appended)
  -h, --help                  Show help
USAGE
}

resume_last=0
session_id=""
session_file=""
session_mode="auto"
skip_git_check=0
json_out=0
output_last=""
custom_prompt=""

while [ $# -gt 0 ]; do
  case "$1" in
    --resume-last)
      resume_last=1
      ;;
    --session)
      session_id="${2:-}"
      shift
      ;;
    --session-file)
      session_file="${2:-}"
      shift
      ;;
    --session-mode)
      session_mode="${2:-}"
      shift
      ;;
    --skip-git-check)
      skip_git_check=1
      ;;
    --json)
      json_out=1
      ;;
    --output-last-message)
      output_last="${2:-}"
      shift
      ;;
    --prompt)
      custom_prompt="${2:-}"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found in PATH. Install it first." >&2
  exit 1
fi

if [ "$session_mode" != "auto" ] && [ "$session_mode" != "new" ] && [ "$session_mode" != "resume" ]; then
  echo "Invalid --session-mode: $session_mode (expected auto, new, or resume)." >&2
  exit 1
fi

if [ "$resume_last" -eq 1 ] && [ -n "$session_id" ]; then
  echo "Choose only one of --resume-last or --session." >&2
  exit 1
fi

if [ -n "$session_file" ] && { [ "$resume_last" -eq 1 ] || [ -n "$session_id" ]; }; then
  echo "Choose only one of --session-file or --resume-last/--session." >&2
  exit 1
fi

if [ "$session_mode" = "new" ] && { [ "$resume_last" -eq 1 ] || [ -n "$session_id" ]; }; then
  echo "--session-mode new cannot be combined with --resume-last or --session." >&2
  exit 1
fi

if [ "$session_mode" = "resume" ] && [ "$resume_last" -eq 0 ] && [ -z "$session_id" ] && [ -z "$session_file" ]; then
  echo "--session-mode resume requires --session-file, --session, or --resume-last." >&2
  exit 1
fi

if [ "$skip_git_check" -eq 0 ]; then
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Not inside a Git repo. Re-run with --skip-git-check if this is intentional." >&2
    exit 1
  fi
fi

listing=$(ls -la)
if [ -n "$custom_prompt" ]; then
  prompt="$custom_prompt"$'\n\n'"$listing"
else
  prompt=$'Analyze this directory listing and summarize anything notable:\n\n'"$listing"
fi

read_session_file() {
  if [ -f "$1" ]; then
    tr -d ' \t\r\n' < "$1"
  fi
}

print_session_id() {
  echo "Session ID: $1" >&2
}

session_id_from_file=""
if [ -n "$session_file" ] && [ "$session_mode" != "new" ]; then
  session_id_from_file=$(read_session_file "$session_file")
fi

if [ "$session_mode" = "resume" ] && [ -n "$session_file" ] && [ -z "$session_id_from_file" ]; then
  echo "Session file is empty or missing: $session_file" >&2
  exit 1
fi

if [ -z "$session_id" ]; then
  session_id="$session_id_from_file"
fi

need_capture=0
resume_args=()

if [ "$session_mode" = "new" ]; then
  need_capture=1
elif [ "$resume_last" -eq 1 ]; then
  resume_args=(resume --last)
  need_capture=1
elif [ -n "$session_id" ]; then
  resume_args=(resume "$session_id")
else
  need_capture=1
fi

run_with_json_capture() {
  local parse_cmd
  if command -v python3 >/dev/null 2>&1; then
    parse_cmd=(python3)
  elif command -v python >/dev/null 2>&1; then
    parse_cmd=(python)
  else
    echo "python3 or python is required to parse JSONL output." >&2
    exit 1
  fi

  local json_file
  local output_last_file
  local cleanup_output_last=0
  local cmd
  local allow_output_last=1
  local message_file=""

  if [ "${#resume_args[@]}" -gt 0 ]; then
    allow_output_last=0
  fi

  json_file=$(mktemp)
  if [ "$allow_output_last" -eq 1 ]; then
    output_last_file="$output_last"
    if [ -z "$output_last_file" ]; then
      output_last_file=$(mktemp)
      cleanup_output_last=1
    fi
  else
    message_file=$(mktemp)
  fi

  cmd=(codex exec)
  if [ "$skip_git_check" -eq 1 ]; then
    cmd+=(--skip-git-repo-check)
  fi
  if [ "${#resume_args[@]}" -gt 0 ]; then
    cmd+=("${resume_args[@]}")
  fi
  if [ "$allow_output_last" -eq 1 ]; then
    cmd+=(--json --output-last-message "$output_last_file" -)
  else
    cmd+=(--json -)
  fi

  printf "%s" "$prompt" | "${cmd[@]}" >"$json_file"

  local captured_id
  if [ "$allow_output_last" -eq 1 ]; then
    captured_id=$("${parse_cmd[@]}" - "$json_file" <<'PY'
import json
import sys

thread_id = ""
with open(sys.argv[1], "r", encoding="utf-8") as handle:
    for line in handle:
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if isinstance(obj, dict):
            thread_id = obj.get("thread_id") or obj.get("session_id") or thread_id
            if not thread_id:
                thread = obj.get("thread")
                if isinstance(thread, dict):
                    thread_id = thread.get("id") or thread_id
        if thread_id:
            break
print(thread_id)
PY
)
  else
    captured_id=$("${parse_cmd[@]}" - "$json_file" "$message_file" <<'PY'
import json
import sys

json_path = sys.argv[1]
message_path = sys.argv[2]

thread_id = ""
deltas = []
fallback = []

def add_fallback(text):
    if text:
        fallback.append(text)

with open(json_path, "r", encoding="utf-8") as handle:
    for line in handle:
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if not thread_id and isinstance(obj, dict):
            thread_id = obj.get("thread_id") or obj.get("session_id") or thread_id
            if not thread_id:
                thread = obj.get("thread")
                if isinstance(thread, dict):
                    thread_id = thread.get("id") or thread_id

        if not isinstance(obj, dict):
            continue

        t = obj.get("type")
        if not isinstance(t, str):
            t = ""

        delta = obj.get("delta")
        if isinstance(delta, str) and "output_text" in t:
            deltas.append(delta)

        text = obj.get("text")
        if isinstance(text, str):
            if "output_text" in t and "delta" in t:
                deltas.append(text)
            elif "output_text" in t:
                add_fallback(text)

        msg = obj.get("message")
        if isinstance(msg, dict):
            content = msg.get("content")
            if isinstance(content, list):
                for item in content:
                    if (
                        isinstance(item, dict)
                        and item.get("type") == "output_text"
                        and isinstance(item.get("text"), str)
                    ):
                        add_fallback(item["text"])

        output = obj.get("output")
        if isinstance(output, list):
            for item in output:
                if (
                    isinstance(item, dict)
                    and item.get("type") == "output_text"
                    and isinstance(item.get("text"), str)
                ):
                    add_fallback(item["text"])

        resp = obj.get("response")
        if isinstance(resp, dict):
            ot = resp.get("output_text")
            if isinstance(ot, list):
                for item in ot:
                    if isinstance(item, str):
                        add_fallback(item)
            elif isinstance(ot, str):
                add_fallback(ot)
            out = resp.get("output")
            if isinstance(out, list):
                for item in out:
                    if (
                        isinstance(item, dict)
                        and item.get("type") == "output_text"
                        and isinstance(item.get("text"), str)
                    ):
                        add_fallback(item["text"])

text_out = "".join(deltas) if deltas else "\n\n".join(fallback)
with open(message_path, "w", encoding="utf-8") as handle:
    handle.write(text_out)

print(thread_id)
PY
)
  fi

  if [ -z "$captured_id" ]; then
    echo "Failed to capture session ID from JSON output." >&2
    rm -f "$json_file"
    if [ -n "$message_file" ]; then
      rm -f "$message_file"
    fi
    if [ "$cleanup_output_last" -eq 1 ]; then
      rm -f "$output_last_file"
    fi
    exit 1
  fi

  if [ -n "$session_file" ] && { [ "$session_mode" != "resume" ] || [ -z "$session_id_from_file" ]; }; then
    printf "%s\n" "$captured_id" > "$session_file"
  fi

  print_session_id "$captured_id"

  if [ "$json_out" -eq 1 ]; then
    cat "$json_file"
  else
    if [ "$allow_output_last" -eq 1 ]; then
      cat "$output_last_file"
    else
      cat "$message_file"
    fi
  fi

  rm -f "$json_file"
  if [ -n "$message_file" ]; then
    rm -f "$message_file"
  fi
  if [ "$cleanup_output_last" -eq 1 ]; then
    rm -f "$output_last_file"
  fi
}

if [ "$need_capture" -eq 1 ]; then
  run_with_json_capture
  exit 0
fi

cmd=(codex exec)

if [ "${#resume_args[@]}" -gt 0 ]; then
  cmd+=("${resume_args[@]}")
fi

if [ "$skip_git_check" -eq 1 ]; then
  cmd+=(--skip-git-repo-check)
fi
if [ "$json_out" -eq 1 ]; then
  cmd+=(--json)
fi
if [ -n "$output_last" ]; then
  cmd+=(--output-last-message "$output_last")
fi

cmd+=(-)

if [ -n "$session_id" ]; then
  print_session_id "$session_id"
fi

printf "%s" "$prompt" | "${cmd[@]}"
