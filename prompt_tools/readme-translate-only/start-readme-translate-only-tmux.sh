#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: prompt_tools/readme-translate-only/start-readme-translate-only-tmux.sh [options]

Start a tmux session that runs README translations one language at a time.

Options:
  --repo-root <path>      target repository root
  --source <path>         source README path relative to repo root (default: README.md)
  --i18n-dir <path>       output directory relative to repo root (default: i18n)
  --languages "<list>"    space-separated language codes
  --session <name>        tmux session name (default: readme-translate-<repo>)
  --model <name>          Codex model (default: gpt-5.4)
  --reasoning <level>     low|medium|high|xhigh (default: medium)
  --max-languages <n>     stop after n generated languages
  --branch <name>         push branch (default: current branch or main)
  --no-commit             skip git commit/push checkpoints
  --kill                  kill an existing session and recreate it
  --no-attach             do not attach after startup
  -h, --help              show help
USAGE
}

tool_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root=""
source_rel="README.md"
i18n_dir="i18n"
languages="ar es fr ja ko vi zh-Hans zh-Hant de ru"
session=""
model="${README_TRANSLATE_MODEL:-gpt-5.4}"
reasoning="${README_TRANSLATE_REASONING:-medium}"
max_languages=0
branch=""
do_commit=1
kill_existing=0
attach=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      repo_root="${2:-}"
      shift 2
      ;;
    --source)
      source_rel="${2:-}"
      shift 2
      ;;
    --i18n-dir)
      i18n_dir="${2:-}"
      shift 2
      ;;
    --languages)
      languages="${2:-}"
      shift 2
      ;;
    --session)
      session="${2:-}"
      shift 2
      ;;
    --model)
      model="${2:-}"
      shift 2
      ;;
    --reasoning)
      reasoning="${2:-}"
      shift 2
      ;;
    --max-languages)
      max_languages="${2:-0}"
      shift 2
      ;;
    --branch)
      branch="${2:-}"
      shift 2
      ;;
    --no-commit)
      do_commit=0
      shift
      ;;
    --kill)
      kill_existing=1
      shift
      ;;
    --no-attach)
      attach=0
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
done

if [[ -z "$repo_root" ]]; then
  echo "--repo-root is required" >&2
  usage >&2
  exit 1
fi
repo_root="$(cd "$repo_root" && pwd)"

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found." >&2
  exit 1
fi

repo_slug="$(basename "$repo_root")"
if [[ -z "$session" ]]; then
  session="readme-translate-$repo_slug"
fi
if [[ -z "$branch" ]]; then
  branch="$(git -C "$repo_root" branch --show-current 2>/dev/null || true)"
fi
if [[ -z "$branch" ]]; then
  branch="main"
fi

log_dir="$repo_root/.readme-translate-work/logs"
mkdir -p "$log_dir"
timestamp="$(date +%Y%m%d_%H%M%S)"
log_path="$log_dir/${session}_${timestamp}.log"

if tmux has-session -t "$session" 2>/dev/null; then
  if [[ "$kill_existing" -eq 1 ]]; then
    tmux kill-session -t "$session"
  else
    echo "tmux session already running: $session"
    echo "attach: tmux attach -t $session"
    if [[ "$attach" -eq 1 ]]; then
      exec tmux attach -t "$session"
    fi
    exit 0
  fi
fi

cmd=(
  bash "$tool_dir/translate-readme-only.sh"
  --repo-root "$repo_root"
  --source "$source_rel"
  --i18n-dir "$i18n_dir"
  --languages "$languages"
  --model "$model"
  --reasoning "$reasoning"
  --branch "$branch"
)
if [[ "$max_languages" -gt 0 ]]; then
  cmd+=(--max-languages "$max_languages")
fi
if [[ "$do_commit" -eq 0 ]]; then
  cmd+=(--no-commit)
fi

printf -v quoted_cmd '%q ' "${cmd[@]}"
tmux new-session -d -s "$session" -c "$repo_root" "bash -lc 'cd \"$repo_root\" && $quoted_cmd 2>&1 | tee \"$log_path\"'"
tmux rename-window -t "$session:0" "translate"
tmux set-option -t "$session" -g mouse on

echo "tmux session: $session"
echo "log: $log_path"
echo "attach: tmux attach -t $session"

if [[ "$attach" -eq 1 ]]; then
  exec tmux attach -t "$session"
fi
