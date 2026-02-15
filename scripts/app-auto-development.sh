#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: app-auto-development.sh [options]

Automates iterative app development from screenshot+markdown pairs by repeatedly
calling Codex non-interactively in ONE shared session.

High-level flow:
1) Ask Codex to design a development order for all image+markdown pairs
2) For each ordered pair, run these Codex-driven steps:
   plan -> backend -> pwa -> android -> android_sim_test ->
   ios -> ios_mac_sync -> review -> summary

Options:
  --manifest <path>         Input manifest TSV (default: prefer app_screenshot_description_markdown/group_subfolder_mapping.tsv, fallback to screen_manifest.tsv)
  --doc-root <path>         Screenshot doc root (default: app_screenshot_description_markdown)
  --decompiled-ref <path>   Decompiled app reference root (default: /home/lachlan/ProjectsLFS/HeyCyan/decompiled)
  --sdk-demo-ref <path>     SDK/demo reference root (default: /home/lachlan/ProjectsLFS/HeyCyan/HeyCyanSdkAndDemo)
  --auto-apps-root <path>   Generated app workspace root (default: auto-apps)
  --ordered <path>          Ordered pairs TSV output (default: references/development/ordered_pairs.tsv)
  --session-file <path>     Codex session file (default: references/development/.codex_app_auto_session)
  --state-file <path>       Progress state file (default: references/development/app_auto_state.tsv)
  --model <name>            Codex model (default: gpt-5.3-codex)
  --reasoning <level>       low|medium|high|xhigh (default: medium)
  --new-session             Start a new Codex session
  --reset-state             Clear progress state file before run
  --force-reorder           Regenerate ordered pairs even if file exists
  --start-at <n>            Start from ordered step n (1-based, default: 1)
  --max-steps <n>           Process at most n steps (default: 0 = all)
  --skip-git-check          Pass --skip-git-repo-check to codex exec
  --mac-host <host>         Mac host for iOS sync (default: 192.168.1.71)
  --mac-user <user>         Mac SSH user (default: lachlan)
  --mac-remote-dir <path>   Mac repo dir (default: /Users/lachlan/Local/LightMindApp)
  --mac-password <pass>     Mac SSH password (or set MAC_PASSWORD env)
  --skip-mac-sync           Skip mac sync step
  --skip-sim-tests          Skip local simulator validation phases (Android emulator; iOS sim if added later)
  --verbose                 Verbose logs
  -h, --help                Show this help
USAGE
}

manifest=""
doc_root="app_screenshot_description_markdown"
decompiled_ref="/home/lachlan/ProjectsLFS/HeyCyan/decompiled"
sdk_demo_ref="/home/lachlan/ProjectsLFS/HeyCyan/HeyCyanSdkAndDemo"
auto_apps_root="auto-apps"
ordered_pairs="references/development/ordered_pairs.tsv"
session_file="references/development/.codex_app_auto_session"
state_file="references/development/app_auto_state.tsv"
model="gpt-5.3-codex"
reasoning="medium"
new_session=0
reset_state=0
force_reorder=0
start_at=1
max_steps=0
skip_git_check=0
mac_host="192.168.1.71"
mac_user="lachlan"
mac_remote_dir="/Users/lachlan/Local/LightMindApp"
mac_password="${MAC_PASSWORD:-}"
skip_mac_sync=0
skip_sim_tests=0
verbose=0

while [ $# -gt 0 ]; do
  case "$1" in
    --manifest)
      manifest="${2:-}"; shift ;;
    --doc-root)
      doc_root="${2:-}"; shift ;;
    --decompiled-ref)
      decompiled_ref="${2:-}"; shift ;;
    --sdk-demo-ref)
      sdk_demo_ref="${2:-}"; shift ;;
    --auto-apps-root)
      auto_apps_root="${2:-}"; shift ;;
    --ordered)
      ordered_pairs="${2:-}"; shift ;;
    --session-file)
      session_file="${2:-}"; shift ;;
    --state-file)
      state_file="${2:-}"; shift ;;
    --model)
      model="${2:-}"; shift ;;
    --reasoning)
      reasoning="${2:-}"; shift ;;
    --new-session)
      new_session=1 ;;
    --reset-state)
      reset_state=1 ;;
    --force-reorder)
      force_reorder=1 ;;
    --start-at)
      start_at="${2:-}"; shift ;;
    --max-steps)
      max_steps="${2:-}"; shift ;;
    --skip-git-check)
      skip_git_check=1 ;;
    --mac-host)
      mac_host="${2:-}"; shift ;;
    --mac-user)
      mac_user="${2:-}"; shift ;;
    --mac-remote-dir)
      mac_remote_dir="${2:-}"; shift ;;
    --mac-password)
      mac_password="${2:-}"; shift ;;
    --skip-mac-sync)
      skip_mac_sync=1 ;;
    --skip-sim-tests)
      skip_sim_tests=1 ;;
    --verbose)
      verbose=1 ;;
    -h|--help)
      usage
      exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1 ;;
  esac
  shift
done

case "$reasoning" in
  low|medium|high|xhigh) ;;
  *)
    echo "Invalid --reasoning '$reasoning'. Use low|medium|high|xhigh." >&2
    exit 1 ;;
esac

if ! [[ "$start_at" =~ ^[0-9]+$ ]] || [ "$start_at" -lt 1 ]; then
  echo "--start-at must be an integer >= 1." >&2
  exit 1
fi

if ! [[ "$max_steps" =~ ^[0-9]+$ ]]; then
  echo "--max-steps must be an integer >= 0." >&2
  exit 1
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found in PATH." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required." >&2
  exit 1
fi

if [ -z "$manifest" ]; then
  if [ -f "app_screenshot_description_markdown/group_subfolder_mapping.tsv" ]; then
    manifest="app_screenshot_description_markdown/group_subfolder_mapping.tsv"
  elif [ -f "app_screenshot_description_markdown/screen_manifest.tsv" ]; then
    manifest="app_screenshot_description_markdown/screen_manifest.tsv"
  else
    echo "No default manifest found. Expected one of:" >&2
    echo "  app_screenshot_description_markdown/group_subfolder_mapping.tsv" >&2
    echo "  app_screenshot_description_markdown/screen_manifest.tsv" >&2
    exit 1
  fi
fi

if [ ! -f "$manifest" ]; then
  echo "Manifest not found: $manifest" >&2
  exit 1
fi

if [ ! -d "$decompiled_ref" ]; then
  echo "Decompiled reference directory not found: $decompiled_ref" >&2
  exit 1
fi

if [ ! -d "$sdk_demo_ref" ]; then
  echo "SDK/demo reference directory not found: $sdk_demo_ref" >&2
  exit 1
fi

if [ -n "$mac_password" ]; then
  export MAC_PASSWORD="$mac_password"
fi

ref_dev_root="references/development"
plan_dir="$ref_dev_root/plan"
summary_dir="references/summaries"
prompt_dir="$ref_dev_root/prompts"
log_dir="$ref_dev_root/logs"
step_work_root="$ref_dev_root/steps"
master_plan="$plan_dir/MASTER_PLAN.md"
ordering_rationale="$ref_dev_root/ORDERING_RATIONALE.md"
run_log="$log_dir/app_auto_development_run.log"
backend_root="$auto_apps_root/backend"
pwa_root="$auto_apps_root/pwa"
android_root="$auto_apps_root/android"
ios_root="$auto_apps_root/ios"

mkdir -p "$ref_dev_root" "$plan_dir" "$summary_dir" "$prompt_dir" "$log_dir" "$step_work_root"
mkdir -p "$backend_root" "$pwa_root" "$android_root" "$ios_root"

lock_file="$ref_dev_root/app-auto-development.lock"
if command -v flock >/dev/null 2>&1; then
  exec 200>"$lock_file"
  # Prevent stale lockouts: don't leak the lock FD into long-running children
  # (e.g., `codex exec`), otherwise a crash can leave the lock held.
  python3 - <<'PY'
import fcntl

fd = 200
flags = fcntl.fcntl(fd, fcntl.F_GETFD)
fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
PY
  if ! flock -n 200; then
    echo "Another scripts/app-auto-development.sh instance is already running (lock: $lock_file)." >&2
    echo "If you believe it's stuck, find and stop the other process, then retry." >&2
    exit 1
  fi
else
  echo "flock not available; skipping single-instance lock." >&2
fi

cleanup() {
  # Driver should be linear. If any background jobs were started accidentally,
  # stop them on exit (tmux-managed services are unaffected).
  local pids
  pids="$(jobs -pr 2>/dev/null || true)"
  if [ -n "$pids" ]; then
    kill $pids 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

if [ ! -f "$backend_root/README.md" ]; then
  cat > "$backend_root/README.md" <<'EOF'
# LightMind Backend
Generated and iteratively updated by scripts/app-auto-development.sh.
EOF
fi
if [ ! -f "$pwa_root/README.md" ]; then
  cat > "$pwa_root/README.md" <<'EOF'
# LightMind PWA
Generated and iteratively updated by scripts/app-auto-development.sh.
EOF
fi
if [ ! -f "$android_root/README.md" ]; then
  cat > "$android_root/README.md" <<'EOF'
# LightMind Android
Generated and iteratively updated by scripts/app-auto-development.sh.
EOF
fi
if [ ! -f "$ios_root/README.md" ]; then
  cat > "$ios_root/README.md" <<'EOF'
# LightMind iOS
Generated and iteratively updated by scripts/app-auto-development.sh.
EOF
fi

touch "$run_log"

if [ "$reset_state" -eq 1 ]; then
  rm -f "$state_file"
fi
mkdir -p "$(dirname "$state_file")"
touch "$state_file"

log() {
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  printf '[%s] %s\n' "$ts" "$*" | tee -a "$run_log"
}

git_push_best_effort() {
  # Codex tries to push in each phase, but transient DNS issues do happen.
  # Make pushes more reliable without blocking indefinitely.
  local max_tries=6
  local delay_s=3
  local i
  for i in $(seq 1 "$max_tries"); do
    if git push; then
      return 0
    fi
    log "git push failed (attempt $i/$max_tries). Retrying in ${delay_s}s..."
    sleep "$delay_s"
    delay_s=$((delay_s * 2))
    if [ "$delay_s" -gt 60 ]; then
      delay_s=60
    fi
  done
  log "git push still failing after $max_tries attempts; continuing (will retry on next phase)."
  return 1
}

vlog() {
  if [ "$verbose" -eq 1 ]; then
    log "$*"
  fi
}

declare -A phase_state_done

load_state() {
  while IFS=$'\t' read -r step_key phase status _ts _rest; do
    [ -z "${step_key:-}" ] && continue
    [ -z "${phase:-}" ] && continue
    if [ "${status:-}" = "done" ]; then
      phase_state_done["$step_key|$phase"]=1
    fi
  done < "$state_file"
}

phase_done() {
  local step_key="$1"
  local phase="$2"
  [ "${phase_state_done[$step_key|$phase]:-0}" -eq 1 ]
}

mark_phase_done() {
  local step_key="$1"
  local phase="$2"
  local ts
  ts="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  printf '%s\t%s\tdone\t%s\n' "$step_key" "$phase" "$ts" >> "$state_file"
  phase_state_done["$step_key|$phase"]=1
}

phase_done_with_artifacts() {
  local step_key="$1"
  local phase="$2"
  shift 2
  if ! phase_done "$step_key" "$phase"; then
    return 1
  fi
  local f
  for f in "$@"; do
    if [ -n "$f" ] && [ ! -s "$f" ]; then
      log "State says done for $step_key/$phase but artifact missing: $f. Re-running phase."
      return 1
    fi
  done
  return 0
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

run_codex_new_session_from_file() {
  local prompt_file="$1"
  local json_file="$2"
  local image_file="${3:-}"
  local cmd=(codex exec --json --full-auto -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  if [ "$skip_git_check" -eq 1 ]; then
    cmd+=(--skip-git-repo-check)
  fi
  if [ -n "$image_file" ]; then
    cmd+=(--image "$image_file")
  fi
  cmd+=(-)
  "${cmd[@]}" < "$prompt_file" > "$json_file" 2>>"$log_dir/codex_stderr.log"
}

run_codex_new_session_init_from_file() {
  local prompt_file="$1"
  local json_file="$2"
  local cmd=(codex exec --json -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  if [ "$skip_git_check" -eq 1 ]; then
    cmd+=(--skip-git-repo-check)
  fi
  cmd+=(-)
  "${cmd[@]}" < "$prompt_file" > "$json_file" 2>>"$log_dir/codex_stderr.log"
}

run_codex_resume_from_file() {
  local sid="$1"
  local prompt_file="$2"
  local json_file="$3"
  local image_file="${4:-}"
  local cmd=(codex exec resume "$sid" --json --full-auto -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  if [ "$skip_git_check" -eq 1 ]; then
    cmd+=(--skip-git-repo-check)
  fi
  if [ -n "$image_file" ]; then
    cmd+=(--image "$image_file")
  fi
  cmd+=(-)
  "${cmd[@]}" < "$prompt_file" > "$json_file" 2>>"$log_dir/codex_stderr.log"
}

assert_nonempty_file() {
  local f="$1"
  local label="$2"
  if [ ! -s "$f" ]; then
    echo "Expected non-empty $label file: $f" >&2
    exit 1
  fi
}

assert_dir_has_files() {
  local d="$1"
  local label="$2"
  if [ ! -d "$d" ]; then
    echo "Expected $label directory: $d" >&2
    exit 1
  fi
  if ! find "$d" -type f -print -quit | grep -q .; then
    echo "Expected at least one file in $label directory: $d" >&2
    exit 1
  fi
}

sanitize_slug() {
  local in="$1"
  local out
  out="$(printf '%s' "$in" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/_/g; s/^_+//; s/_+$//')"
  if [ -z "$out" ]; then
    out="step"
  fi
  printf '%s\n' "$out"
}

load_state

session_id=""
if [ "$new_session" -eq 0 ] && [ -f "$session_file" ]; then
  session_id="$(tr -d ' \t\r\n' < "$session_file")"
fi

if [ -z "$session_id" ]; then
  init_prompt="$prompt_dir/000_init.txt"
  init_json="$log_dir/000_init.jsonl"
  cat > "$init_prompt" <<EOF
Session initialization only.

Store these constraints for subsequent prompts:
- Work only inside this repository.
- Execution mode:
  - This outer driver script runs phases linearly and calls you once per phase.
  - Inside a single \`codex exec\` call, you may run multiple shell commands as needed, but keep them ordered and avoid unnecessary parallelism.
  - Do not leave behind extra background processes/terminals when you finish a phase.
    If you start temporary monitors (e.g., \`tail -f\`, \`watch\`), stop them before responding.
  - Allowed long-running processes:
    - Backend service inside tmux session \`lightmind_backend\`
    - A single Android emulator process (only during android simulator testing)
  - Do not create multiple tmux sessions/windows/panes; only use the explicitly requested tmux session name(s).
- App identity and naming:
  - App name/brand is "LightMind" (not HeyCyan).
  - Prefer \`LightMind\` for user-facing strings and UI labels.
  - Prefer \`lightmind\` for file names, IDs, and internal identifiers.
  - Avoid introducing new identifiers containing "HeyCyan" unless strictly required for compatibility (e.g., SDK/protocol constants).
  - Android: default package/namespace should be \`com.lightmind.*\`.
  - iOS: default target/module names should be \`LightMind\`.
- Read-only reference paths:
  - /home/lachlan/ProjectsLFS/AiMemo
  - $decompiled_ref
  - $sdk_demo_ref
- Do not modify files under those read-only reference paths.
- Implementation code must be created/updated only under:
  - $backend_root
  - $pwa_root
  - $android_root
  - $ios_root

Important for this initialization step:
- Do NOT run shell commands.
- Do NOT read or write any files.
- Reply with exactly: READY_APP_AUTO_SESSION
EOF
  log "Initializing Codex session for app auto development"
  run_codex_new_session_init_from_file "$init_prompt" "$init_json"
  if ! grep -q "READY_APP_AUTO_SESSION" "$init_json"; then
    echo "Initialization response missing READY_APP_AUTO_SESSION marker." >&2
    exit 1
  fi
  session_id="$(extract_session_id_from_jsonl "$init_json")"
  if [ -z "$session_id" ]; then
    echo "Failed to initialize session ID." >&2
    exit 1
  fi
  printf '%s\n' "$session_id" > "$session_file"
fi

log "Using session ID: $session_id"

global_step_key="GLOBAL"
if [ "$force_reorder" -eq 1 ]; then
  vlog "Force reorder enabled: regenerating ordered pairs."
fi

if [ "$force_reorder" -eq 0 ] && [ ! -s "$state_file" ] && [ -s "$ordered_pairs" ] && [ -s "$ordering_rationale" ]; then
  log "Adopting existing ordering artifacts into state file."
  mark_phase_done "$global_step_key" "ordering"
fi

if [ "$force_reorder" -eq 1 ] || ! phase_done_with_artifacts "$global_step_key" "ordering" "$ordered_pairs" "$ordering_rationale"; then
  mkdir -p "$(dirname "$ordered_pairs")"
  order_prompt="$prompt_dir/001_order_pairs.txt"
  order_json="$log_dir/001_order_pairs.jsonl"
  cat > "$order_prompt" <<EOF
Design the best development order for all screenshot+markdown pairs from:
$manifest

Read the manifest and each markdown file to infer feature dependency flow.
If manifest has group/subfolder columns, use them to preserve visual flow coherence.
You may also read these references for dependency/context inference:
- $decompiled_ref
- $sdk_demo_ref
Do not modify any files under those reference directories.

Write ordered output directly to:
$ordered_pairs

Required TSV format (NO header, exactly 5 columns):
1) sequence (1-based integer)
2) screen_slug
3) image_path
4) markdown_path
5) flow_stage

Rules:
- Include every row from manifest exactly once.
- Use repository-relative paths exactly.
- flow_stage should be concise snake_case (e.g., auth_core, home_shell, settings_profile).
- Order should support incremental full-app delivery.

Also write ordering rationale to:
$ordering_rationale

Rationale requirements:
- explain phase strategy and key dependencies
- explain where AiMemo-style auth logic should be integrated
- explain risk controls for backend/pwa/android/ios parallel consistency

Do not modify app code in this step. Only write/update ordering and rationale docs.
Commit and push these docs.

Final response must be exactly:
DONE_ORDERING
EOF
  log "Generating ordered pair sequence"
  run_codex_resume_from_file "$session_id" "$order_prompt" "$order_json"
  git_push_best_effort || true
  assert_nonempty_file "$ordered_pairs" "ordered pairs"
  assert_nonempty_file "$ordering_rationale" "ordering rationale"
  mark_phase_done "$global_step_key" "ordering"
else
  log "Skipping ordering: already completed."
fi

mapfile -t ordered_rows < <(awk -F '\t' 'NF>=4 {print $0}' "$ordered_pairs")
if [ "${#ordered_rows[@]}" -eq 0 ]; then
  echo "No ordered rows found in $ordered_pairs" >&2
  exit 1
fi

declare -A manifest_group_by_screen
declare -A manifest_subfolder_by_screen
while IFS=$'\t' read -r m_screen_slug m_image_path m_md_path m_group_slug m_group_subfolder _rest; do
  [ -z "${m_screen_slug:-}" ] && continue
  if [ -n "${m_group_slug:-}" ]; then
    manifest_group_by_screen["$m_screen_slug"]="$m_group_slug"
  fi
  if [ -n "${m_group_subfolder:-}" ]; then
    manifest_subfolder_by_screen["$m_screen_slug"]="$m_group_subfolder"
  fi
done < "$manifest"

processed=0
row_idx=0

for row in "${ordered_rows[@]}"; do
  row_idx=$((row_idx + 1))
  if [ "$row_idx" -lt "$start_at" ]; then
    continue
  fi
  if [ "$max_steps" -gt 0 ] && [ "$processed" -ge "$max_steps" ]; then
    break
  fi

  IFS=$'\t' read -r seq slug image_path md_path flow_stage _ <<< "$row"

  # Accept files that may not include sequence column.
  if ! [[ "${seq:-}" =~ ^[0-9]+$ ]]; then
    flow_stage="${md_path:-unknown_stage}"
    md_path="${image_path:-}"
    image_path="${slug:-}"
    slug="$(sanitize_slug "${seq:-step_$row_idx}")"
    seq="$row_idx"
  fi

  if [ -z "${slug:-}" ] || [ -z "${image_path:-}" ] || [ -z "${md_path:-}" ]; then
    echo "Malformed ordered row: $row" >&2
    exit 1
  fi

  if [ ! -f "$image_path" ]; then
    echo "Image not found for step $seq: $image_path" >&2
    exit 1
  fi

  if [ ! -f "$md_path" ]; then
    echo "Markdown not found for step $seq: $md_path" >&2
    exit 1
  fi

  step_id="$(printf '%03d' "$seq")"
  step_slug="$(sanitize_slug "$slug")"
  step_key="${step_id}_${step_slug}"
  source_group_slug="${manifest_group_by_screen[$slug]:-unknown_group}"
  source_group_subfolder="${manifest_subfolder_by_screen[$slug]:-unknown_subfolder}"
  step_dir="$step_work_root/${step_id}_${step_slug}"
  mkdir -p "$step_dir"

  plan_file="$plan_dir/${step_id}_${step_slug}_plan.md"
  summary_file="$summary_dir/${step_id}_${step_slug}_summary.md"
  step_context="$step_dir/context.md"

  cat > "$step_context" <<EOF
# Step Context
- sequence: $seq
- step_id: $step_id
- slug: $step_slug
- app_name: LightMind
- android_package_base: com.lightmind
- ios_module_name: LightMind
- execution_mode: linear_one_command_at_a_time
- flow_stage: ${flow_stage:-unknown_stage}
- image: $image_path
- markdown: $md_path
- source_group: $source_group_slug
- source_group_subfolder: $source_group_subfolder
- ordered_pairs: $ordered_pairs
- master_plan: $master_plan
- step_plan: $plan_file
- step_summary: $summary_file
- backend_root: $backend_root
- pwa_root: $pwa_root
- android_root: $android_root
- ios_root: $ios_root

Read-only reference:
- /home/lachlan/ProjectsLFS/AiMemo (learn auth only, do not modify)
- $decompiled_ref (decompiled app reference, do not modify)
- $sdk_demo_ref (SDK/demo reference, do not modify)
EOF

  plan_prompt="$step_dir/01_plan_prompt.txt"
  plan_json="$step_dir/01_plan_response.jsonl"
  if phase_done_with_artifacts "$step_key" "plan" "$plan_file"; then
    log "Step $step_id $step_slug: planning already done, skipping"
  else
    log "Step $step_id $step_slug: planning"
    cat > "$plan_prompt" <<EOF
Current step context:
$step_context

Task:
1) Read image + markdown for this step.
2) Read /home/lachlan/ProjectsLFS/AiMemo for login/auth pattern reference only.
3) Read-only references allowed:
   - $decompiled_ref
   - $sdk_demo_ref
4) Never modify /home/lachlan/ProjectsLFS/AiMemo, $decompiled_ref, or $sdk_demo_ref.
5) Naming and branding rules (IMPORTANT):
   - This app is named LightMind.
   - Use LightMind naming for new code: classes/modules/packages/targets should not be named HeyCyan.
   - Android: use \`com.lightmind.*\` namespaces by default.
   - iOS: use \`LightMind\` module/target naming by default.
6) Execution mode (IMPORTANT):
   - Complete this phase within this single \`codex exec\` call.
   - Keep commands simple and linear; avoid parallel/background processes.
   - Do not leave behind any background processes when you finish.
6) Plan implementation changes only under:
   - $backend_root
   - $pwa_root
   - $android_root
   - $ios_root
7) Write detailed step plan directly to:
$plan_file
8) Update or create master plan:
$master_plan

Plan must include:
- backend scope (data model, API endpoints, auth requirements)
- pwa scope (screen composition, state, API integration)
- android scope (screen parity, architecture integration)
- ios scope (screen parity, architecture integration)
- test plan and acceptance criteria
- explicit dependencies on previous steps
- exact files/components to add or update under auto-apps roots

Do not implement feature code in this planning step.
Commit and push planning docs.

Final response: DONE_PLAN $step_id $step_slug
EOF
    run_codex_resume_from_file "$session_id" "$plan_prompt" "$plan_json" "$image_path"
    git_push_best_effort || true
    assert_nonempty_file "$plan_file" "step plan"
    mark_phase_done "$step_key" "plan"
  fi

  backend_notes="$step_dir/02_backend_notes.md"
  backend_prompt="$step_dir/02_backend_prompt.txt"
  backend_json="$step_dir/02_backend_response.jsonl"
  if phase_done_with_artifacts "$step_key" "backend" "$backend_notes"; then
    log "Step $step_id $step_slug: backend already done, skipping"
  else
    log "Step $step_id $step_slug: backend"
    cat > "$backend_prompt" <<EOF
Current step context:
$step_context

Implement backend increment for this step.

Requirements:
- Use current step image + markdown + plan:
  $plan_file
- Naming and branding rules:
  - App name is LightMind.
  - Avoid introducing new identifiers containing "HeyCyan" in code/artifacts under $backend_root.
- Execution mode:
  - Driver script is linear; do not start multiple unrelated tasks in parallel.
  - Allowed long-running process: backend service inside tmux session \`lightmind_backend\`.
  - Do not leave behind extra background processes/terminals when you finish this phase.
- Keep app architecture coherent with prior steps.
- Learn auth behavior from /home/lachlan/ProjectsLFS/AiMemo (read-only only).
- Read-only references allowed:
  - $decompiled_ref
  - $sdk_demo_ref
- Never modify /home/lachlan/ProjectsLFS/AiMemo, $decompiled_ref, or $sdk_demo_ref.
- Create or update backend code only under:
  $backend_root
- Backend runtime env (recommended):
  - Create/update conda env: \`./scripts/setup_backend_env.sh\` (env name: \`lightmind_backend\`)
  - Prefer running Python/uvicorn via: \`conda run -n lightmind_backend ...\`
- Start/restart backend in tmux using send-keys:
  - session name: lightmind_backend
  - include step environment variable LIGHTMIND_STEP=$step_slug
  - document exact command and health check result.
- Write backend notes to:
  $backend_notes
- Commit and push backend changes.

Final response: DONE_BACKEND $step_id $step_slug
EOF
    run_codex_resume_from_file "$session_id" "$backend_prompt" "$backend_json" "$image_path"
    git_push_best_effort || true
    assert_nonempty_file "$backend_notes" "backend notes"
    assert_dir_has_files "$backend_root" "backend"
    mark_phase_done "$step_key" "backend"
  fi

  pwa_notes="$step_dir/03_pwa_notes.md"
  pwa_prompt="$step_dir/03_pwa_prompt.txt"
  pwa_json="$step_dir/03_pwa_response.jsonl"
  if phase_done_with_artifacts "$step_key" "pwa" "$pwa_notes"; then
    log "Step $step_id $step_slug: pwa already done, skipping"
  else
    log "Step $step_id $step_slug: pwa"
    cat > "$pwa_prompt" <<EOF
Current step context:
$step_context

Implement PWA increment for this step.

Requirements:
- Build UI to closely match screenshot style while keeping modern polish.
- Naming and branding rules:
  - App name is LightMind.
  - Prefer LightMind labels and titles in new UI.
- Execution mode:
  - Driver script is linear; do not start multiple unrelated tasks in parallel.
  - Avoid leaving behind background processes (e.g., chrome, chromedriver). Use bounded runs and stop them before finishing.
- Integrate with current backend behavior.
- Keep flow coherent with full app perspective.
- Read-only references allowed:
  - $decompiled_ref
  - $sdk_demo_ref
- Implement PWA code only under:
  $pwa_root
- Use step plan:
  $plan_file
- Run PWA verification with Selenium + chromedriver (available on this machine).
- Save test/verification notes (commands + result) to:
  $pwa_notes
- Commit and push PWA changes.

Final response: DONE_PWA $step_id $step_slug
EOF
    run_codex_resume_from_file "$session_id" "$pwa_prompt" "$pwa_json" "$image_path"
    git_push_best_effort || true
    assert_nonempty_file "$pwa_notes" "pwa notes"
    assert_dir_has_files "$pwa_root" "pwa"
    mark_phase_done "$step_key" "pwa"
  fi

  android_notes="$step_dir/04_android_notes.md"
  android_prompt="$step_dir/04_android_prompt.txt"
  android_json="$step_dir/04_android_response.jsonl"
  if phase_done_with_artifacts "$step_key" "android" "$android_notes"; then
    log "Step $step_id $step_slug: android already done, skipping"
  else
    log "Step $step_id $step_slug: android implementation"
    cat > "$android_prompt" <<EOF
Current step context:
$step_context

Implement Android increment for this step.

Requirements:
- Use image + markdown + backend + pwa outputs to design Android UI/features.
- Naming and branding rules:
  - App name is LightMind.
  - Use \`com.lightmind.*\` namespaces and LightMind class naming by default.
- Execution mode:
  - Driver script is linear; do not start multiple unrelated tasks in parallel.
  - Avoid leaving behind background processes when you finish.
- Read-only references allowed:
  - $decompiled_ref
  - $sdk_demo_ref
- Keep full-app architecture perspective (incremental build, not isolated mock).
- Implement Android code only under:
  $android_root
- Update/consider Ralph-Wiggum automation script logic where relevant:
  auto-app-development/ralph-wiggum-example.sh
- Keep UI modern and faithful to screenshot intent.
- Save implementation notes to:
  $android_notes
- Commit and push Android changes.

Final response: DONE_ANDROID $step_id $step_slug
EOF
    run_codex_resume_from_file "$session_id" "$android_prompt" "$android_json" "$image_path"
    git_push_best_effort || true
    assert_nonempty_file "$android_notes" "android notes"
    assert_dir_has_files "$android_root" "android"
    mark_phase_done "$step_key" "android"
  fi

  android_sim_notes="$step_dir/05_android_sim_test.md"
  android_sim_prompt="$step_dir/05_android_sim_test_prompt.txt"
  android_sim_json="$step_dir/05_android_sim_test_response.jsonl"
  if phase_done_with_artifacts "$step_key" "android_sim_test" "$android_sim_notes"; then
    log "Step $step_id $step_slug: android simulator test already done, skipping"
  else
    if [ "$skip_sim_tests" -eq 1 ]; then
      log "Step $step_id $step_slug: android simulator test skipped (--skip-sim-tests)"
      cat >"$android_sim_notes" <<EOF
# Android Simulator Test (Skipped)

This phase was skipped on $(date -u '+%Y-%m-%dT%H:%M:%SZ') because the driver was run with --skip-sim-tests.

Notes:
- No Android emulator boot/build/install was attempted.
- To run simulator validation later:
  - Remove the corresponding line from: $state_file
  - Re-run without --skip-sim-tests
EOF
      git add "$android_sim_notes" || true
      if ! git diff --cached --quiet; then
        git commit -m "Skip step $step_id Android simulator validation"
      fi
      git_push_best_effort || true
      mark_phase_done "$step_key" "android_sim_test"
    else
      log "Step $step_id $step_slug: android simulator test"
      cat > "$android_sim_prompt" <<EOF
Current step context:
$step_context

Run Android simulator validation for this step.

Requirements:
- Start/attach emulator available on this machine.
- Do not let emulator work hang indefinitely:
  - All waits must be bounded (use \`timeout\` and/or explicit max-attempt loops).
  - If the emulator cannot boot within 12 minutes, write notes and stop this phase cleanly.
  - If build/install/run cannot complete within 15 minutes, write notes and stop this phase cleanly.
  - Prefer non-interactive CLI commands and avoid opening Android Studio.
- Execution mode:
  - Driver script is linear; do not run phases in parallel.
  - It's OK to start a single emulator process in the background for this phase only; avoid starting multiple emulators.
- Suggested non-sticky command pattern (adapt to whatever build system exists under $android_root):
  - Detect existing device: \`adb devices\`
  - If no emulator is running:
    - List AVDs: \`emulator -list-avds\`
    - Start one (headless if possible): \`emulator @<name> -no-audio -no-boot-anim -gpu swiftshader_indirect &\`
    - Wait for boot with a hard timeout:
      - \`timeout 600 adb wait-for-device\`
      - \`timeout 600 bash -lc 'until adb shell getprop sys.boot_completed | grep -m1 1; do sleep 2; done'\`
  - Install with a timeout (example): \`timeout 180 adb install -r <apk>\`
- Build/install/run Android app from:
  $android_root
- Perform smoke validation relevant to this step.
- Record commands, emulator name, and result in:
  $android_sim_notes
- Fix breakages if found.
- Commit and push test/fix changes.

Final response: DONE_ANDROID_SIM $step_id $step_slug
EOF
      run_codex_resume_from_file "$session_id" "$android_sim_prompt" "$android_sim_json" "$image_path"
      git_push_best_effort || true
      assert_nonempty_file "$android_sim_notes" "android simulator notes"
      mark_phase_done "$step_key" "android_sim_test"
    fi
  fi

  ios_notes="$step_dir/06_ios_notes.md"
  ios_prompt="$step_dir/06_ios_prompt.txt"
  ios_json="$step_dir/06_ios_response.jsonl"
  if phase_done_with_artifacts "$step_key" "ios" "$ios_notes"; then
    log "Step $step_id $step_slug: ios already done, skipping"
  else
    log "Step $step_id $step_slug: ios implementation"
    cat > "$ios_prompt" <<EOF
Current step context:
$step_context

Implement iOS increment for this step.

Requirements:
- Use image + markdown + backend + pwa + android context.
- Naming and branding rules:
  - App name is LightMind.
  - Use \`LightMind\` module/target naming in iOS sources by default.
- Execution mode:
  - Driver script is linear; do not start multiple unrelated tasks in parallel.
  - Avoid leaving behind background processes when you finish.
- Read-only references allowed:
  - $decompiled_ref
  - $sdk_demo_ref
- Keep full-app perspective and feature parity.
- Keep interface modern and faithful.
- Implement iOS code only under:
  $ios_root
- Save iOS implementation notes to:
  $ios_notes
- Commit and push iOS changes.

Final response: DONE_IOS $step_id $step_slug
EOF
    run_codex_resume_from_file "$session_id" "$ios_prompt" "$ios_json" "$image_path"
    git_push_best_effort || true
    assert_nonempty_file "$ios_notes" "ios notes"
    assert_dir_has_files "$ios_root" "ios"
    mark_phase_done "$step_key" "ios"
  fi

  if [ "$skip_mac_sync" -eq 0 ]; then
    ios_mac_notes="$step_dir/07_ios_mac_sync_notes.md"
    ios_mac_prompt="$step_dir/07_ios_mac_sync_prompt.txt"
    ios_mac_json="$step_dir/07_ios_mac_sync_response.jsonl"
    if phase_done_with_artifacts "$step_key" "ios_mac_sync" "$ios_mac_notes"; then
      log "Step $step_id $step_slug: ios mac sync already done, skipping"
    else
      log "Step $step_id $step_slug: ios mac sync/build handoff"
      cat > "$ios_mac_prompt" <<EOF
Current step context:
$step_context

Perform iOS mac handoff workflow for this step.

Mac connection details:
- host: $mac_host
- user: $mac_user
- remote repo path: $mac_remote_dir

Requirements:
- Ensure local repo changes are committed and pushed first.
- Connect to Mac and sync repo (git pull).
- Do not let the mac sync/build workflow hang indefinitely:
  - Use explicit timeouts (Linux: \`timeout\`; macOS: prefer \`gtimeout\` if available, otherwise implement time-bounded loops).
  - Prefer \`xcodebuild\` simulator builds (no GUI) and bail out cleanly if a step exceeds 20 minutes.
- Prefer non-interactive remote commands:
  - Use \`ssh -o BatchMode=yes\` when possible.
  - If SSH prompts for a password and no automation is available, stop and record the blocker in notes (do not hang).
- Execution mode:
  - Driver script is linear; do not start multiple unrelated tasks in parallel.
  - Avoid leaving behind background processes when you finish.
- Ensure auto-apps workspace is present on Mac and includes:
  - $backend_root
  - $pwa_root
  - $android_root
  - $ios_root
- Sync local ignored settings/secrets/tokens to Mac as needed for build.
  Preferred via ssh/scp/rsync; use environment variable MAC_PASSWORD when password auth is required.
- Install any missing build dependencies directly on Mac.
- Run a minimal iOS build sanity check on Mac when possible.
- Record exact commands and outcomes to:
  $ios_mac_notes
- Commit and push any repository changes from this step.

Important:
- Do not leak secret values into tracked files.
- Do not modify /home/lachlan/ProjectsLFS/AiMemo, $decompiled_ref, or $sdk_demo_ref.

Final response: DONE_IOS_MAC_SYNC $step_id $step_slug
EOF
      run_codex_resume_from_file "$session_id" "$ios_mac_prompt" "$ios_mac_json" "$image_path"
      git_push_best_effort || true
      assert_nonempty_file "$ios_mac_notes" "ios mac sync notes"
      mark_phase_done "$step_key" "ios_mac_sync"
    fi
  fi

  review_notes="$step_dir/08_review_notes.md"
  review_prompt="$step_dir/08_review_prompt.txt"
  review_json="$step_dir/08_review_response.jsonl"
  if phase_done_with_artifacts "$step_key" "review" "$review_notes"; then
    log "Step $step_id $step_slug: review already done, skipping"
  else
    log "Step $step_id $step_slug: systematic review"
    cat > "$review_prompt" <<EOF
Current step context:
$step_context

Run a systematic integration review for this single step.

Review scope:
- backend, pwa, android, ios coherence
- step acceptance criteria from:
  $plan_file
- regressions introduced by this step
- run focused validations where feasible

Output:
- Write review findings and resolutions to:
  $review_notes
- Fix critical issues found.
- Commit and push review/fix changes.

Final response: DONE_REVIEW $step_id $step_slug
EOF
    run_codex_resume_from_file "$session_id" "$review_prompt" "$review_json" "$image_path"
    git_push_best_effort || true
    assert_nonempty_file "$review_notes" "review notes"
    mark_phase_done "$step_key" "review"
  fi

  summary_prompt="$step_dir/09_summary_prompt.txt"
  summary_json="$step_dir/09_summary_response.jsonl"
  if phase_done_with_artifacts "$step_key" "summary" "$summary_file"; then
    log "Step $step_id $step_slug: summary already done, skipping"
  else
    log "Step $step_id $step_slug: summary"
    cat > "$summary_prompt" <<EOF
Current step context:
$step_context

Write a step summary markdown directly to:
$summary_file

Summary must include:
- what changed in backend/pwa/android/ios
- notable test results
- mac sync/build notes status
- commit references (recent hashes/messages)
- unresolved risks and next-step recommendations

Then commit and push the summary doc.

Final response: DONE_SUMMARY $step_id $step_slug
EOF
    run_codex_resume_from_file "$session_id" "$summary_prompt" "$summary_json" "$image_path"
    git_push_best_effort || true
    assert_nonempty_file "$summary_file" "step summary"
    mark_phase_done "$step_key" "summary"
  fi

  processed=$((processed + 1))
  log "Step $step_id $step_slug completed"
done

log "All requested steps completed. Processed: $processed"
log "Artifacts:"
log "  Ordered pairs: $ordered_pairs"
log "  Master plan: $master_plan"
log "  Plans dir: $plan_dir"
log "  Summaries dir: $summary_dir"
log "  State file: $state_file"
log "  Auto apps root: $auto_apps_root"
