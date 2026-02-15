#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: generate_screenshot_docs.sh [options]

Automates screenshot documentation with non-interactive Codex calls:
1) Initializes one Codex session (saved to a session file)
2) Loops all images and has Codex write per-image markdown files directly
3) Calls Codex again (same session) to write a detailed app structure doc directly
4) Calls Codex again (same session) to write grouping TSV directly
5) Copies each image + markdown into grouped folders

Options:
  --input-dir <path>       Source image folder (default: com_glasssutdio_wear)
  --output-dir <path>      Output root (default: app_screenshot_description_markdown)
  --model <name>           Codex model (default: gpt-5.3-codex)
  --reasoning <level>      Reasoning effort: low|medium|high|xhigh (default: medium)
  --session-file <path>    Session ID file (default: <output-dir>/.codex_session_id)
  --new-session            Force a brand-new Codex session
  --clean-output           Clear prior generated output before starting
  --skip-git-check         Pass --skip-git-repo-check to codex exec
  --verbose                Print detailed progress logs
  -h, --help               Show this help
USAGE
}

input_dir="com_glasssutdio_wear"
output_dir="app_screenshot_description_markdown"
model="gpt-5.3-codex"
reasoning="medium"
session_file=""
new_session=0
clean_output=0
skip_git_check=0
verbose=0
max_summary_lines=45

while [ $# -gt 0 ]; do
  case "$1" in
    --input-dir)
      input_dir="${2:-}"
      shift
      ;;
    --output-dir)
      output_dir="${2:-}"
      shift
      ;;
    --model)
      model="${2:-}"
      shift
      ;;
    --reasoning)
      reasoning="${2:-}"
      shift
      ;;
    --session-file)
      session_file="${2:-}"
      shift
      ;;
    --new-session)
      new_session=1
      ;;
    --clean-output)
      clean_output=1
      ;;
    --skip-git-check)
      skip_git_check=1
      ;;
    --verbose)
      verbose=1
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

if [ -z "$input_dir" ] || [ -z "$output_dir" ] || [ -z "$model" ] || [ -z "$reasoning" ]; then
  echo "Required option value is empty." >&2
  exit 1
fi

case "$reasoning" in
  low|medium|high|xhigh) ;;
  *)
    echo "Invalid --reasoning '$reasoning'. Use: low|medium|high|xhigh." >&2
    exit 1
    ;;
esac

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found in PATH." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required." >&2
  exit 1
fi

if [ ! -d "$input_dir" ]; then
  echo "Input directory not found: $input_dir" >&2
  exit 1
fi

if [ -z "$session_file" ]; then
  session_file="$output_dir/.codex_session_id"
fi

if [ "$new_session" -eq 1 ] && [ "$clean_output" -eq 0 ]; then
  # Default behavior for a fresh run: avoid mixing old partial artifacts.
  clean_output=1
fi

if [ "$clean_output" -eq 1 ]; then
  rm -rf "$output_dir/screens" "$output_dir/groups" "$output_dir/logs"
  rm -f "$output_dir/APP_STRUCTURE_DETAILED.md" \
    "$output_dir/GROUP_INDEX.md" \
    "$output_dir/RUN_METADATA.md" \
    "$output_dir/screen_manifest.tsv" \
    "$output_dir/group_mapping.tsv" \
    "$output_dir/group_mapping.raw.tsv"
fi

mkdir -p "$output_dir" "$output_dir/screens" "$output_dir/groups" "$output_dir/logs"
codex_stderr_log="$output_dir/logs/codex_stderr.log"

log() {
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  printf '[%s] %s\n' "$ts" "$*"
}

vlog() {
  if [ "$verbose" -eq 1 ]; then
    log "$*"
  fi
}

extract_session_id_from_jsonl() {
  local json_file="$1"
  python3 - "$json_file" <<'PY'
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
}

assert_nonempty_file() {
  local target_file="$1"
  local label="$2"
  if [ ! -s "$target_file" ]; then
    echo "Codex did not produce a non-empty $label file: $target_file" >&2
    exit 1
  fi
}

normalize_group_mapping() {
  local raw_file="$1"
  local out_file="$2"
  python3 - "$raw_file" "$out_file" <<'PY'
import re
import sys

raw_path = sys.argv[1]
out_path = sys.argv[2]

rows = []
seen = set()

def clean_group_slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_-]+", "_", value)
    value = value.strip("_")
    return value or "uncategorized"

with open(raw_path, "r", encoding="utf-8") as handle:
    for line in handle:
        s = line.strip()
        if not s or s.startswith("```"):
            continue
        s = re.sub(r"^[-*]\s*", "", s)
        parts = None
        if s.count("\t") >= 2:
            parts = [p.strip() for p in s.split("\t")]
        elif "|" in s and s.count("|") >= 2:
            parts = [p.strip() for p in s.strip("|").split("|")]
        if not parts or len(parts) < 3:
            continue
        screen_slug = parts[0].strip()
        group_slug = clean_group_slug(parts[1])
        group_title = parts[2].strip() or "Uncategorized"
        if not screen_slug or screen_slug.lower() in {"screen_slug", "slug"}:
            continue
        if screen_slug in seen:
            continue
        seen.add(screen_slug)
        rows.append((screen_slug, group_slug, group_title))

with open(out_path, "w", encoding="utf-8") as handle:
    for screen_slug, group_slug, group_title in rows:
        handle.write(f"{screen_slug}\t{group_slug}\t{group_title}\n")
PY
}

sanitize_slug() {
  local input="$1"
  local slug
  slug="$(printf '%s' "$input" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/_/g; s/^_+//; s/_+$//')"
  if [ -z "$slug" ]; then
    slug="screen"
  fi
  printf '%s\n' "$slug"
}

markdown_title_slug() {
  local md_file="$1"
  local fallback_slug="$2"
  local title
  title="$(sed -n '1s/^# Screen:[[:space:]]*//p' "$md_file" | head -n 1 | tr -d '\r')"
  if [ -z "$title" ]; then
    printf '%s\n' "$fallback_slug"
    return
  fi
  sanitize_slug "$title"
}

run_codex_new_session_from_file() {
  local prompt_file="$1"
  local json_file="$2"
  local cmd=(codex exec --json --full-auto -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  if [ "$skip_git_check" -eq 1 ]; then
    cmd+=(--skip-git-repo-check)
  fi
  cmd+=(-)
  "${cmd[@]}" < "$prompt_file" > "$json_file" 2>>"$codex_stderr_log"
}

run_codex_resume_from_file() {
  local current_session_id="$1"
  local prompt_file="$2"
  local json_file="$3"
  local image_file="${4:-}"
  local cmd=(codex exec resume "$current_session_id" --json --full-auto -m "$model" -c "model_reasoning_effort=\"$reasoning\"")
  if [ "$skip_git_check" -eq 1 ]; then
    cmd+=(--skip-git-repo-check)
  fi
  if [ -n "$image_file" ]; then
    cmd+=(--image "$image_file")
  fi
  cmd+=(-)
  "${cmd[@]}" < "$prompt_file" > "$json_file" 2>>"$codex_stderr_log"
}

mapfile -d '' images < <(find "$input_dir" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.webp' \) -print0 | sort -z)

if [ "${#images[@]}" -eq 0 ]; then
  echo "No images found in $input_dir" >&2
  exit 1
fi

log "Found ${#images[@]} images in $input_dir"
log "Model: $model, reasoning: $reasoning"

session_id=""
if [ "$new_session" -eq 0 ] && [ -f "$session_file" ]; then
  session_id="$(tr -d ' \t\r\n' < "$session_file")"
fi

if [ -z "$session_id" ]; then
  vlog "Initializing new Codex session"
  init_prompt_file="$output_dir/logs/00_init_prompt.txt"
  init_json_file="$output_dir/logs/00_init_response.jsonl"
  cat > "$init_prompt_file" <<'EOF'
You are helping build structured documentation for a mobile app from screenshots.
You will receive one screenshot at a time. For each screenshot:
- infer the screen purpose
- identify key UI components and visible data
- infer likely user actions and navigation context
- keep claims grounded in the screenshot

Important output rule for later image prompts:
- respond in markdown only
- no code fences unless explicitly requested
EOF
  run_codex_new_session_from_file "$init_prompt_file" "$init_json_file"
  session_id="$(extract_session_id_from_jsonl "$init_json_file")"
  if [ -z "$session_id" ]; then
    echo "Failed to capture session ID from initialization response." >&2
    exit 1
  fi
  printf '%s\n' "$session_id" > "$session_file"
else
  vlog "Reusing existing session ID from $session_file"
fi

log "Using session ID: $session_id"

manifest_file="$output_dir/screen_manifest.tsv"
: > "$manifest_file"

declare -A slug_counts
screen_counter=0

for image in "${images[@]}"; do
  screen_counter=$((screen_counter + 1))
  image_base="$(basename "$image")"
  rel_path="${image#$input_dir/}"
  rel_stem="${rel_path%.*}"
  base_slug="$(sanitize_slug "$rel_stem")"
  slug_idx="${slug_counts[$base_slug]:-0}"
  if [ "$slug_idx" -eq 0 ]; then
    screen_slug="$base_slug"
  else
    screen_slug="${base_slug}_$slug_idx"
  fi
  slug_counts["$base_slug"]=$((slug_idx + 1))

  screen_dir="$output_dir/screens/$screen_slug"
  mkdir -p "$screen_dir"

  copied_image_path="$screen_dir/$image_base"
  screen_md_path="$screen_dir/${screen_slug}.md"
  screen_md_tmp_path="$screen_dir/${screen_slug}.md.tmp"
  screen_json_path="$output_dir/logs/screen_${screen_slug}.jsonl"
  prompt_file="$output_dir/logs/prompt_${screen_slug}.txt"

  cp -f "$image" "$copied_image_path"

  cat > "$prompt_file" <<EOF
Task: Analyze the attached mobile app screenshot and write the markdown directly to this file path:
$screen_md_tmp_path

Do not output the markdown in chat. Write the file in the workspace.

Required markdown structure inside the file:
# Screen: <short descriptive title>
## What this screen is for
## Key UI elements
## User actions and navigation
## Data shown
## App flow inference
## Notes and confidence

Quality requirements:
- Be specific and meaningful.
- Mention visible labels/buttons/text where readable.
- If text is unclear, explicitly say it is unreadable.
- Keep each section concise but information-dense.
- Keep claims grounded in the screenshot.

Metadata:
- Screenshot identifier: $screen_slug
- Original filename: $image_base
- Image path: $copied_image_path

Execution requirements:
- Ensure parent directory exists.
- Write UTF-8 markdown directly to the target file.
- Final response must be exactly: WROTE $screen_md_tmp_path
EOF

  log "[$screen_counter/${#images[@]}] Describing $image_base -> $screen_slug"
  run_codex_resume_from_file "$session_id" "$prompt_file" "$screen_json_path" "$copied_image_path"
  assert_nonempty_file "$screen_md_tmp_path" "screen markdown"
  mv -f "$screen_md_tmp_path" "$screen_md_path"

  printf '%s\t%s\t%s\n' "$screen_slug" "$copied_image_path" "$screen_md_path" >> "$manifest_file"
done

summary_context_file="$output_dir/logs/01_screen_summaries_for_structure.md"
: > "$summary_context_file"
while IFS=$'\t' read -r screen_slug copied_image_path screen_md_path; do
  {
    echo "## $screen_slug"
    echo "Image: $(basename "$copied_image_path")"
    sed -n "1,${max_summary_lines}p" "$screen_md_path"
    echo
  } >> "$summary_context_file"
done < "$manifest_file"

log "Generating detailed app structure document (same session)"
structure_prompt_file="$output_dir/logs/02_structure_prompt.txt"
structure_json_file="$output_dir/logs/02_structure_response.jsonl"
structure_md_file="$output_dir/APP_STRUCTURE_DETAILED.md"
structure_md_tmp_file="$output_dir/APP_STRUCTURE_DETAILED.md.tmp"

cat > "$structure_prompt_file" <<'EOF'
Using the screenshot analyses below, write a detailed markdown document describing the app structure.

Requirements:
- Markdown only
- Include:
  - # App Structure Overview
  - ## Core modules
  - ## Primary navigation model
  - ## Typical user journeys
  - ## Settings and system pages
  - ## AI-related features
  - ## BLE / device-control touchpoints (if evident)
  - ## Uncertain areas and assumptions
- Be explicit about confidence and assumptions.
- Infer likely architecture from screen flow, not backend code.

Screenshot analyses:

EOF
cat "$summary_context_file" >> "$structure_prompt_file"
cat >> "$structure_prompt_file" <<EOF

Write the final markdown directly to this path (do not print it in chat):
$structure_md_tmp_file

Execution requirements:
- Ensure parent directory exists.
- Write UTF-8 markdown to the target file.
- Final response must be exactly: WROTE $structure_md_tmp_file
EOF

run_codex_resume_from_file "$session_id" "$structure_prompt_file" "$structure_json_file"
assert_nonempty_file "$structure_md_tmp_file" "app structure markdown"
mv -f "$structure_md_tmp_file" "$structure_md_file"

log "Generating grouping map (same session)"
group_prompt_file="$output_dir/logs/03_group_prompt.txt"
group_json_file="$output_dir/logs/03_group_response.jsonl"
group_map_file="$output_dir/group_mapping.tsv"
group_map_raw_file="$output_dir/group_mapping.raw.tsv"
group_map_raw_tmp_file="$output_dir/group_mapping.raw.tsv.tmp"

cat > "$group_prompt_file" <<'EOF'
From the screenshot analyses below, assign each screen slug to a high-level app-structure group.

Output format rules:
- Output plain TSV only
- One row per screen
- Exactly 3 columns:
  1) screen_slug
  2) group_slug (lowercase snake_case)
  3) group_title (human-readable)
- No markdown, no code fences, no explanations

Examples:
home_main	home	Home
settings_device	recording_settings	Recording Settings

Screenshot analyses:

EOF
cat "$summary_context_file" >> "$group_prompt_file"
cat >> "$group_prompt_file" <<EOF

Write the TSV directly to this file path (do not print TSV in chat):
$group_map_raw_tmp_file

Execution requirements:
- Ensure parent directory exists.
- Write plain UTF-8 text with tab delimiters.
- No markdown/code fences/explanations in file content.
- Final response must be exactly: WROTE $group_map_raw_tmp_file
EOF

run_codex_resume_from_file "$session_id" "$group_prompt_file" "$group_json_file"
assert_nonempty_file "$group_map_raw_tmp_file" "group mapping TSV"
mv -f "$group_map_raw_tmp_file" "$group_map_raw_file"
normalize_group_mapping "$group_map_raw_file" "$group_map_file"

declare -A group_by_screen
declare -A group_title_by_slug
declare -A group_subfolder_seen
declare -A group_screen_slug_by_subfolder

if [ -s "$group_map_file" ]; then
  while IFS=$'\t' read -r mapped_screen_slug mapped_group_slug mapped_group_title; do
    [ -z "$mapped_screen_slug" ] && continue
    group_by_screen["$mapped_screen_slug"]="$mapped_group_slug"
    if [ -n "$mapped_group_slug" ] && [ -n "$mapped_group_title" ] && [ -z "${group_title_by_slug[$mapped_group_slug]:-}" ]; then
      group_title_by_slug["$mapped_group_slug"]="$mapped_group_title"
    fi
  done < "$group_map_file"
fi

group_subfolder_mapping_file="$output_dir/group_subfolder_mapping.tsv"
: > "$group_subfolder_mapping_file"

while IFS=$'\t' read -r screen_slug copied_image_path screen_md_path; do
  group_slug="${group_by_screen[$screen_slug]:-uncategorized}"
  base_subfolder_slug="$(markdown_title_slug "$screen_md_path" "$screen_slug")"
  collision_key="$group_slug|$base_subfolder_slug"
  collision_idx="${group_subfolder_seen[$collision_key]:-0}"
  if [ "$collision_idx" -eq 0 ]; then
    group_subfolder_slug="$base_subfolder_slug"
  else
    group_subfolder_slug="${base_subfolder_slug}_$collision_idx"
  fi
  group_subfolder_seen["$collision_key"]=$((collision_idx + 1))
  group_screen_slug_by_subfolder["$group_slug|$group_subfolder_slug"]="$screen_slug"

  group_dir="$output_dir/groups/$group_slug/$group_subfolder_slug"
  mkdir -p "$group_dir"
  cp -f "$copied_image_path" "$group_dir/"
  cp -f "$screen_md_path" "$group_dir/"
  printf '%s\t%s\t%s\t%s\t%s\n' "$screen_slug" "$copied_image_path" "$screen_md_path" "$group_slug" "$group_subfolder_slug" >> "$group_subfolder_mapping_file"
done < "$manifest_file"

group_index_file="$output_dir/GROUP_INDEX.md"
{
  echo "# Screenshot Groups"
  echo
  echo "- Session ID: \`$session_id\`"
  echo "- Model: \`$model\`"
  echo "- Reasoning: \`$reasoning\`"
  echo "- Total screens: ${#images[@]}"
  echo
  while IFS= read -r group_dir; do
    group_slug="$(basename "$group_dir")"
    group_title="${group_title_by_slug[$group_slug]:-$group_slug}"
    echo "## $group_title (\`$group_slug\`)"
    while IFS= read -r screen_dir; do
      group_subfolder_slug="$(basename "$screen_dir")"
      source_screen_slug="${group_screen_slug_by_subfolder[$group_slug|$group_subfolder_slug]:-$group_subfolder_slug}"
      echo "- $group_subfolder_slug (\`$source_screen_slug\`)"
    done < <(find "$group_dir" -mindepth 1 -maxdepth 1 -type d | sort)
    echo
  done < <(find "$output_dir/groups" -mindepth 1 -maxdepth 1 -type d | sort)
} > "$group_index_file"

run_metadata_file="$output_dir/RUN_METADATA.md"
{
  echo "# Run Metadata"
  echo
  echo "- Input dir: \`$input_dir\`"
  echo "- Output dir: \`$output_dir\`"
  echo "- Model: \`$model\`"
  echo "- Reasoning: \`$reasoning\`"
  echo "- Session file: \`$session_file\`"
  echo "- Session ID: \`$session_id\`"
  echo "- Screens processed: ${#images[@]}"
  echo
  echo "Artifacts:"
  echo "- \`$manifest_file\`"
  echo "- \`$structure_md_file\`"
  echo "- \`$group_index_file\`"
  echo "- \`$group_map_file\`"
  echo "- \`$group_subfolder_mapping_file\`"
} > "$run_metadata_file"

log "Done. Outputs are in: $output_dir"
log "Main files:"
log "  - $structure_md_file"
log "  - $group_index_file"
log "  - $manifest_file"
