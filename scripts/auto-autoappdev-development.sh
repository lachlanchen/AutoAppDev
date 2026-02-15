#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: auto-autoappdev-development.sh [options]

Self-development driver for AutoAppDev. This script uses Codex non-interactively
to iteratively implement the AutoAppDev controller app (Tornado backend + PWA),
one small task at a time, with a consistent session and strict guardrails.

Options:
  --model <name>            Codex model (default: gpt-5.3-codex)
  --reasoning <effort>      Reasoning effort: none|minimal|low|medium|high|xhigh (default: medium)
  --sandbox <mode>          Codex sandbox: danger-full-access (default), etc.
  --approval <mode>         Codex approval: never (default), etc.
  --new-session             Start a fresh Codex session (ignore saved session id)
  --start-at <n>            Start at task sequence n (1-based)
  --max-tasks <n>           Run at most n tasks
  --stop-file <path>        If this file exists, stop after finishing current task
  --verbose                 Print extra logs
  -h, --help                Show help

Notes:
- This script is intentionally redundant in prompts. Each codex call owns only one
  tiny phase, but must be aware of the overall architecture.
- It is designed to be used together with the controller app:
  - backend: AutoAppDev/backend (Tornado)
  - pwa:     AutoAppDev/pwa (Scratch-like UI, light theme default)
USAGE
}

model="gpt-5.3-codex"
reasoning="medium"
sandbox="danger-full-access"
approval="never"
new_session=0
start_at=1
max_tasks=0
stop_file=""
verbose=0

while [ $# -gt 0 ]; do
  case "$1" in
    --model) model="${2:-}"; shift ;;
    --reasoning) reasoning="${2:-}"; shift ;;
    --sandbox) sandbox="${2:-}"; shift ;;
    --approval) approval="${2:-}"; shift ;;
    --new-session) new_session=1 ;;
    --start-at) start_at="${2:-}"; shift ;;
    --max-tasks) max_tasks="${2:-}"; shift ;;
    --stop-file) stop_file="${2:-}"; shift ;;
    --verbose) verbose=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
  shift
done

case "$reasoning" in
  extra_high|xhigh) reasoning="xhigh" ;;
  none|minimal|low|medium|high|xhigh) : ;;
  *)
    echo "Invalid --reasoning: $reasoning (expected none|minimal|low|medium|high|xhigh)." >&2
    exit 1
    ;;
esac

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SELFDEV_DIR="$ROOT_DIR/references/selfdev"
LOG_DIR="$SELFDEV_DIR/logs"
PROMPT_DIR="$SELFDEV_DIR/prompts"
TASKS_FILE="$SELFDEV_DIR/tasks.tsv"
STATE_FILE="$SELFDEV_DIR/state.tsv"
SESSION_FILE="$SELFDEV_DIR/.codex_session_id"

mkdir -p "$LOG_DIR" "$PROMPT_DIR"

# Avoid hanging on any interactive git prompt.
export GIT_TERMINAL_PROMPT=0

log() {
  local msg="$1"
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$msg" >&2
}

vlog() {
  if [ "$verbose" -eq 1 ]; then
    log "$1"
  fi
}

git_push_best_effort() {
  local tries=0
  local max=6
  local backoff=2
  while true; do
    if git push; then
      return 0
    fi
    tries=$((tries + 1))
    if [ "$tries" -ge "$max" ]; then
      return 1
    fi
    sleep "$backoff"
    backoff=$((backoff * 2))
  done
}

has_pending_changes() {
  if ! git diff --quiet; then
    return 0
  fi
  if ! git diff --cached --quiet; then
    return 0
  fi
  if [ -n "$(git ls-files --others --exclude-standard)" ]; then
    return 0
  fi
  return 1
}

update_readme_autogen() {
  local msg="$1"
  python3 - "$ROOT_DIR/README.md" "$TASKS_FILE" "$STATE_FILE" "$SESSION_FILE" "$msg" <<'PY'
import datetime
import pathlib
import sys

readme_path = pathlib.Path(sys.argv[1])
tasks_path = pathlib.Path(sys.argv[2])
state_path = pathlib.Path(sys.argv[3])
session_path = pathlib.Path(sys.argv[4])
commit_msg = sys.argv[5]

now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

total = 0
if tasks_path.exists():
  for line in tasks_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    if line.count("\t") >= 4:
      total += 1

done = 0
if state_path.exists():
  for line in state_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    parts = line.split("\t")
    if len(parts) >= 2 and parts[1] == "done":
      done += 1

sid = ""
if session_path.exists():
  sid = session_path.read_text(encoding="utf-8", errors="ignore").strip()

begin = "<!-- AUTOAPPDEV:STATUS:BEGIN -->"
end = "<!-- AUTOAPPDEV:STATUS:END -->"
block = f"""{begin}
## Self-Dev Status (Auto-Updated)

- Updated: {now}
- Phase commit: `{commit_msg}`
- Progress: {done} / {total} tasks done
- Codex session: `{sid}`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

This section is updated by `scripts/auto-autoappdev-development.sh`.
Do not edit content between the markers.

{end}
"""

if readme_path.exists():
  text = readme_path.read_text(encoding="utf-8", errors="ignore")
else:
  text = "# AutoAppDev\n"

if begin in text and end in text:
  pre, rest = text.split(begin, 1)
  _, post = rest.split(end, 1)
  new_text = pre.rstrip() + "\n\n" + block + "\n" + post.lstrip()
else:
  new_text = text.rstrip() + "\n\n" + block + "\n"

readme_path.write_text(new_text, encoding="utf-8")
PY
}

git_commit_push_if_needed() {
  local msg="$1"

  if ! has_pending_changes; then
    return 0
  fi

  update_readme_autogen "$msg" || true

  git add -A
  if git diff --cached --quiet; then
    return 0
  fi

  git commit -m "$msg" || true
  git_push_best_effort || true
}

extract_session_id_from_jsonl() {
  local json_file="$1"
  python3 - "$json_file" <<'PY'
import json, sys
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

run_codex_new_session_init() {
  local prompt_file="$1"
  local json_file="$2"
  local cmd=(codex -s "$sandbox" -a "$approval" exec --json -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  cmd+=(-)
  "${cmd[@]}" < "$prompt_file" > "$json_file"
}

run_codex_resume() {
  local sid="$1"
  local prompt_file="$2"
  local json_file="$3"
  local cmd=(codex -s "$sandbox" -a "$approval" exec resume "$sid" --json --full-auto -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  cmd+=(-)
  "${cmd[@]}" < "$prompt_file" > "$json_file"
}

session_id=""
if [ "$new_session" -eq 0 ] && [ -f "$SESSION_FILE" ]; then
  session_id="$(tr -d ' \t\r\n' < "$SESSION_FILE")"
fi

if [ -z "$session_id" ]; then
  init_prompt="$PROMPT_DIR/000_init.md"
  init_json="$LOG_DIR/000_init.jsonl"
	cat >"$init_prompt" <<EOF
	Session initialization only.

	You are developing **AutoAppDev**, a long-running stable agent system.
	Repo root: $ROOT_DIR
	This driver script: $ROOT_DIR/scripts/auto-autoappdev-development.sh

	High-level product goal (AutoAppDev app):
	- Build a Scratch-like PWA to control and observe a long-running auto-development pipeline.
	- Provide start/stop/pause/resume + settings (agent SDK + LLM/vision models).
	- Provide a persistent chat/inbox for user -> pipeline guidance, plus a way for pipelines to report back
	  (outbox/messages/logs) via HTTP/DB and/or files.
	- Make **Actions** first-class and editable:
	  - Each ACTION can be defined as:
	    - prompt-based: (agent SDK like Codex) + (model) + (prompt template) + (allowed tools/skills)
	    - command-based: shell script / binary / other tool invocation
	    - hybrid: Codex runs a script/bin as part of the action with strict guardrails
	  - Users can edit actions in the UI (prompts, toolchains, skills, scripts used) and reuse them across pipelines.
	- Make **Workspace / Materials / Shared Context** first-class:
	  - Each pipeline/workspace can point at a materials folder and a shared context file(s) that all tasks can use.
	  - These paths must follow a standard workspace contract and be safe (no arbitrary path writes).
	- Make **Multilingual** support first-class:
	  - AutoAppDev UI supports multiple languages and can switch at runtime.
	  - Actions can include a language parameter and/or language-specific prompt variants.
	  - Default language pack: zh-Hans (Chinese Simplified), zh-Hant (Chinese Traditional), en, ja, ko, vi, ar, fr, es.
	  - Include a standard pipeline action for translation/localization that runs before summary/log steps by default.
	- Backend: Python Tornado. Database: PostgreSQL. Secrets in .env.
	- Frontend: PWA (static HTML/CSS/JS). Default theme: light.

	Scratch-like Blocks & Control-Flow (new hard requirement):
	- The PWA "Blocks" palette must be **dynamic** and generated from the Action library:
	  - Any action definition can be used as a draggable block on the canvas.
	  - Users can add new actions (therefore new blocks) and delete arbitrary non-default actions.
	  - Canvas blocks are always removable/reorderable.
	- Provide **built-in default actions** that are read-only:
	  - Default actions (plan/work/debug/fix/summary/update_readme/commit_push) and a default
	    **multilingual support** action must ship with the app.
	  - Built-in actions are **read-only** in the UI and via API; they cannot be modified or deleted.
	  - If the user tries to edit a built-in action, the app must **clone** it into a new user action
	    and then edit the clone (original unchanged).
	- Provide Scratch-like control-flow blocks:
	  - Metatasks generator block (heuristic, redundant prompt) that outputs a task list artifact.
	  - For-loop blocks (outer: For N_ROUND; inner: For each task in metatasks).
	  - If/Else block (mapped to STEP.meta.conditional in IR) for conditional fixes.
	- Default program shown on first load must demonstrate nested control-flow:
	  For N_ROUND:
	    metatasks generator
	    for task in metatasks:
	      plan -> work -> debug -> fix -> multilingual -> summary -> update_readme -> commit/push

		Core missing module (must be built):
		- **Pipeline Script Visualization + Writer**
		  - Define a standardized, formatted pipeline script (human-editable) that represents:
		    TASKS -> STEPS -> ACTIONS (+ action definitions, tools/skills, models, languages, materials/paths, logs, locks, acceptance).
		  - The formatted script must feel **Scratch-like** in text form:
		    - Optional numbering prefixes + indentation for readability (still deterministically parseable).
		    - Minimal placeholder syntax to pass context/outputs between actions (e.g. {{task.title}}, {{task.acceptance}}, {{runtime_dir}}).
		  - Control-flow must be expressible and executable:
		    - for-loops via meta_round_v0 (N_ROUND + task list artifact + per-task template).
		    - if/else via STEP.meta.conditional (e.g. on_debug_failure) and runner state.
		  - Support "rounds" / meta-loops:
		    For N_ROUND: generate/refine tasks from a goal + shared context, then for each task run a standard action template.
		  - Import an existing pipeline shell script (written by other agents/tools) and parse it into
		    the standardized IR, then visualize it as Scratch-like blocks.
		  - Export blocks/IR back into the standardized formatted script and generate a runnable shell
	    driver script (Codex non-interactive steps, reusable actions, skills/tools).
	  - Round-trip conversion should be a first-class feature (script <-> blocks).

	Standardization targets (workspace contract):
	- Standardize and document these concepts and paths so pipelines are portable/resumable:
	  - input materials, user interactions, outputs, docs, references, scripts, tools, logs
	  - place to store generated apps: auto-apps/
	  - task management and resume state (DB-backed where possible)
	  - action registry (prompt- and command-based actions) + safe execution constraints
	  - multilingual language packs + per-workspace language defaults

	Important clarification (do not confuse two "pipelines"):
	- This driver script's development loop (plan -> work -> debug/fix -> summary/log -> commit/push)
	  is how we build AutoAppDev itself.
	- AutoAppDev the product models a generic TASK/STEP/ACTION pipeline and can embody the same
	  philosophy, but it must remain configurable and scriptable (via the standardized script format).

	Hard guardrails (must remember for all subsequent turns):
	- Work only inside this repository ($ROOT_DIR).
	- Every step is **small** and **linear**. No parallel execution between steps.
	- Each \`codex exec\` call completes one small phase and then exits cleanly.
	- Do not leave behind background processes when a phase ends.
	- Do NOT run git commands (\`git add/commit/push\`). This driver script will commit+push after each phase.
	- If you need to communicate what changed, write it into the phase notes file; the driver will commit.

Important:
- For this initialization step: do NOT run commands; do NOT read/write files.
- Reply with exactly: READY_AUTOAPPDEV_SESSION
EOF
  log "Initializing Codex session"
  run_codex_new_session_init "$init_prompt" "$init_json"
  if ! grep -q "READY_AUTOAPPDEV_SESSION" "$init_json"; then
    echo "Init missing READY_AUTOAPPDEV_SESSION marker." >&2
    exit 1
  fi
  session_id="$(extract_session_id_from_jsonl "$init_json")"
  [ -n "$session_id" ] || { echo "Failed to get session id." >&2; exit 1; }
  printf '%s\n' "$session_id" > "$SESSION_FILE"
fi

log "Using session ID: $session_id"

if [ ! -s "$TASKS_FILE" ]; then
  repo_files="$(cd "$ROOT_DIR" && find . -maxdepth 3 -type f | sort || true)"
  order_prompt="$PROMPT_DIR/001_generate_tasks.md"
  order_json="$LOG_DIR/001_generate_tasks.jsonl"
	cat >"$order_prompt" <<EOF
	You are developing AutoAppDev (Scratch-like PWA + Tornado backend + Postgres).
	Driver script: $ROOT_DIR/scripts/auto-autoappdev-development.sh (this script).

	Current repo file list (use this; do NOT spend tool-calls on extra repo inspection):
	$repo_files

	Task (MUST complete fully in this single turn):
	1) Design a first batch of small, incremental tasks that make the controller app real and usable.
	2) Write tasks to: $TASKS_FILE (create/overwrite it).
	3) Verify the file is non-empty (e.g. \`wc -l\`, \`sed -n '1,5p'\`).
	4) Do NOT run git commands; the driver script will commit+push.

TSV format (NO header, 5 columns):
1) seq (1-based int)
2) task_slug (snake_case)
3) area (backend|pwa|scripts|docs)
4) title (short)
5) acceptance_criteria (short but testable)

	Rules:
	- Tasks must be small and ordered from global-to-local.
	- Include explicit tasks for: Postgres wiring, .env handling, light theme PWA, scratch-like blocks, chat/inbox, pipeline start/stop/pause, logs view.
	- Include explicit tasks for:
	  - Action registry/editor (prompt actions + command/script/bin actions + hybrid actions) with guardrails.
	  - Workspace/materials/shared-context configuration (standard contract; safe paths).
	  - Multilingual UI + language packs + language-aware actions (default languages listed in init prompt).
	- MUST include explicit tasks for the **pipeline script visualization + writer** module:
	  - Define standardized formatted script + IR schema (docs + code).
	  - Parse existing pipeline shell scripts into IR (best-effort; with clear limitations).
	  - Render IR as blocks and allow editing.
	  - Export IR/blocks back to formatted script and generate a runnable shell driver script.
	  - Round-trip acceptance checks (script <-> blocks) for at least one example script.
	- MUST include tasks to standardize workspace paths/contracts:
	  - materials/, interactions/, outputs/, docs/, references/, scripts/, tools/, logs/, auto-apps/
	  - resume/task-management behavior and persistence.
	- Do not modify code in this step. Only write the tasks list file.
	- Do NOT commit any files; the driver script handles git.

Final response: DONE_TASKS
EOF
  log "Generating initial task list"
  run_codex_resume "$session_id" "$order_prompt" "$order_json"
  git_commit_push_if_needed "Add initial selfdev tasks list"

  # Retry once with an even more forceful prompt if Codex didn't write the file.
  if [ ! -s "$TASKS_FILE" ]; then
    retry_prompt="$PROMPT_DIR/001b_generate_tasks_retry.md"
    retry_json="$LOG_DIR/001b_generate_tasks_retry.jsonl"
    cat >"$retry_prompt" <<EOF
You did not create the required tasks file on the previous turn.

Hard requirement: create/overwrite this file NOW and commit+push it:
- $TASKS_FILE

Do not inspect the repo further. Do not change any code.

Do:
1) Write at least 12 TSV lines (NO header, 5 tab-separated fields per line).
2) Verify it is non-empty (wc -l).
3) Do NOT run git commands; the driver script will commit+push.

Final response: DONE_TASKS_RETRY
EOF
    log "Retrying task list generation (tasks.tsv missing)"
    run_codex_resume "$session_id" "$retry_prompt" "$retry_json"
    git_commit_push_if_needed "Add initial selfdev tasks list"
  fi

  # Last-resort fallback: seed a minimal tasks.tsv so the pipeline can proceed.
  if [ ! -s "$TASKS_FILE" ]; then
    log "Codex did not create tasks.tsv; seeding a minimal tasks list locally"
    cat >"$TASKS_FILE" <<'TSV'
1	backend_task_crud	backend	Add basic task CRUD API	Pipeline can create/list/update/complete tasks via HTTP endpoints
2	pwa_task_list_ui	pwa	Add task list view in PWA	Task list renders from backend and supports marking done
3	pwa_blocks_export	pwa	Export Scratch-like blocks to JSON	Exported JSON matches the on-canvas program and is saved to backend
4	backend_program_store	backend	Store/serve program JSON	Backend persists program JSON in Postgres (or state.json fallback) and serves it back
5	pipeline_run_logs	backend	Improve pipeline run metadata	Backend records start/stop/pause/resume transitions and exposes run history
6	inbox_consumer_contract	scripts	Define inbox consumption contract	Document how pipeline reads runtime/inbox and how it acknowledges messages
7	pwa_inbox_view	pwa	Show inbox + acknowledgements	PWA displays recent inbox messages and whether consumed
8	rag_guardrails_docs	docs	Add RAG + guardrails checklist	Add a checklist for “retrieve evidence first” + timeouts + boundaries
9	eval_cost_logging	backend	Log per-step cost/usage metrics	Backend stores per-step duration and token/cost estimates (best-effort)
10	tmux_dev_quality	scripts	Make tmux dev session nicer	Add pane titles, ports printed, and health curl hints
11	light_theme_polish	pwa	Polish default light theme	Improve typography/spacing; keep light default and accessible contrast
12	readme_quickstart	docs	Add quickstart docs	README includes env setup, tmux run, and API endpoints
TSV
    git_commit_push_if_needed "Seed AutoAppDev selfdev task list"
  fi
fi

mapfile -t tasks < <(awk -F '\t' 'NF>=5 {print $0}' "$TASKS_FILE")
if [ "${#tasks[@]}" -eq 0 ]; then
  echo "No tasks found in $TASKS_FILE" >&2
  exit 1
fi

touch "$STATE_FILE"

done_task() {
  local seq="$1"
  awk -F '\t' -v s="$seq" '$1==s && $2=="done"{found=1} END{exit(found?0:1)}' "$STATE_FILE"
}

mark_done() {
  local seq="$1"
  printf '%s\tdone\t%s\n' "$seq" "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$STATE_FILE"
}

processed=0

for row in "${tasks[@]}"; do
  IFS=$'\t' read -r seq slug area title acceptance <<<"$row"
  [ -z "${seq:-}" ] && continue
  if [ "$seq" -lt "$start_at" ]; then
    continue
  fi
  if [ "$max_tasks" -gt 0 ] && [ "$processed" -ge "$max_tasks" ]; then
    break
  fi
  if done_task "$seq"; then
    vlog "Skipping already-done task $seq $slug"
    continue
  fi

  log "Task $seq $slug ($area): planning"
  step_dir="$SELFDEV_DIR/tasks/$(printf '%03d' "$seq")_$slug"
  mkdir -p "$step_dir"

  context="$step_dir/context.md"
  cat >"$context" <<EOF
# AutoAppDev Self-Development Task Context

- task_seq: $seq
- task_slug: $slug
- area: $area
- title: $title
- acceptance: $acceptance

	Overall goal:
	- Build AutoAppDev controller (Scratch-like PWA + Tornado backend + Postgres).
	- Default theme: light.
	- Provide chat/inbox + pipeline control + logs + block-based task builder.
	- Provide a configurable action/skill toolchain:
	  - Actions can be prompt-based (agent+model+prompt), command/script/bin-based, or hybrid.
	  - Actions must be editable in the UI and reusable across pipelines.
	- Provide workspace/materials/shared-context support:
	  - Each pipeline/workspace can reference materials folder(s) and shared context visible to all tasks.
	  - Follow a standard workspace contract and enforce safe paths (no arbitrary path writes).
	- Provide multilingual support in AutoAppDev itself and in actions:
	  - UI language switching.
	  - Actions can be language-aware; default languages: zh-Hans, zh-Hant, en, ja, ko, vi, ar, fr, es.
	  - Include translation/localization action before summary/log steps by default in pipeline templates.
	- Provide Scratch-like control-flow blocks + default nested program:
	  - metatasks generator + For N_ROUND + For each task + If/Else.
	  - Dynamic blocks palette generated from Action definitions (built-ins are read-only; clone-on-edit).
	- Build the pipeline script visualization + writer module (script <-> IR <-> blocks):
	  - standard formatted script (TASKS -> STEPS -> ACTIONS)
	  - import/parse existing pipeline shell scripts into IR
	  - export/generate standardized scripts and runnable drivers
	- Standardize workspace contract: materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps + resumable tasks.

	This driver script:
	- $ROOT_DIR/scripts/auto-autoappdev-development.sh

	Runtime directories (design targets):
	- runtime/inbox/ (user messages for pipeline)
	- runtime/outbox/ (pipeline messages back to UI; design target)
	- runtime/logs/ (backend + pipeline logs)
	- references/selfdev/ (tasks, prompts, summaries, state)
	- auto-apps/ (generated apps/workspaces managed by AutoAppDev)
	- materials/ (input materials for a pipeline/workspace; repo or user-provided)
	- interactions/ (user messages, decisions, approvals captured during runs)
	- outputs/ (exported artifacts, reports, built packages; not necessarily committed)
	- tools/ (reusable scripts/tools/skills invoked by pipelines)

	Important:
	- Each phase below is ONE \`codex exec\` call and must remain linear.
	- Do NOT run git commands (\`git add/commit/push\`). The driver script commits+pushes after each phase.
EOF

  # Phase 1: plan
  plan_file="$step_dir/01_plan.md"
  plan_prompt="$step_dir/01_plan_prompt.md"
  plan_json="$step_dir/01_plan.jsonl"
  cat >"$plan_prompt" <<EOF
Current task context:
$context

Phase: PLAN
Goal:
- Produce a detailed, step-specific plan to implement this task, explicitly referencing existing files and where changes will go.
- Include commands to run and acceptance checks.

Constraints:
- Work only under $ROOT_DIR.
- Keep changes minimal and incremental (small step).
- Keep default PWA theme light.
- Postgres + .env rules apply to the overall system.
- Do NOT run git add/commit/push; the driver script will commit+push.

Write plan to:
$plan_file

Do NOT implement code in this phase.

Final response: DONE_PLAN $seq $slug
EOF
  run_codex_resume "$session_id" "$plan_prompt" "$plan_json"
  git_commit_push_if_needed "Selfdev: $seq $slug plan"

  # Phase 2: work
  work_notes="$step_dir/02_work_notes.md"
  work_prompt="$step_dir/02_work_prompt.md"
  work_json="$step_dir/02_work.jsonl"
  cat >"$work_prompt" <<EOF
Current task context:
$context

Phase: WORK
Use this plan:
$plan_file

Implement the task now.
Requirements:
- Make only the changes needed for this task.
- Keep the architecture consistent with the overall system.
- Do not start background processes; keep commands linear.
- Update docs if needed.
- Do NOT run git add/commit/push; the driver script will commit+push.
- Write implementation notes + commands run to:
$work_notes

Final response: DONE_WORK $seq $slug
EOF
  run_codex_resume "$session_id" "$work_prompt" "$work_json"
  git_commit_push_if_needed "Selfdev: $seq $slug work"

  # Phase 3: debug/verify
  dbg_notes="$step_dir/03_debug_notes.md"
  dbg_prompt="$step_dir/03_debug_prompt.md"
  dbg_json="$step_dir/03_debug.jsonl"
  cat >"$dbg_prompt" <<EOF
Current task context:
$context

Phase: DEBUG/VERIFY
Goal:
- Run the smallest possible verification for this task (build/run/smoke).
- Use timeouts for anything that could hang.
- Record exact commands and results.
- Do NOT run git add/commit/push; the driver script will commit+push.

Write debug notes to:
$dbg_notes

If issues found, implement minimal fixes in this same phase.

Final response: DONE_DEBUG $seq $slug
EOF
  run_codex_resume "$session_id" "$dbg_prompt" "$dbg_json"
  git_commit_push_if_needed "Selfdev: $seq $slug verify"

  # Phase 4: summary
  sum_file="$step_dir/04_summary.md"
  sum_prompt="$step_dir/04_summary_prompt.md"
  sum_json="$step_dir/04_summary.jsonl"
  cat >"$sum_prompt" <<EOF
Current task context:
$context

Phase: SUMMARY
Write a concise summary of what changed, why, and how to verify.
Do NOT run git add/commit/push; the driver script will commit+push.
Write summary to:
$sum_file

Final response: DONE_SUMMARY $seq $slug
EOF
  run_codex_resume "$session_id" "$sum_prompt" "$sum_json"
  git_commit_push_if_needed "Selfdev: $seq $slug summary"

  mark_done "$seq"
  processed=$((processed + 1))

  if [ -n "$stop_file" ] && [ -f "$stop_file" ]; then
    log "Stop file present ($stop_file). Stopping after task $seq."
    break
  fi
done

log "Selfdev run complete."
