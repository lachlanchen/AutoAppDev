#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat <<USAGE
Usage: $0 <repo_path> <prompt> [--commit-and-push]

Example:
  $0 /path/to/repo "Write a complete and beautiful README" --commit-and-push
USAGE
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_path="$1"
user_prompt="$2"
commit_and_push="${3:-}"

if [[ ! -d "$repo_path" ]]; then
  echo "Repo path does not exist: $repo_path"
  exit 1
fi

if [[ ! -d "$repo_path/.git" ]]; then
  echo "Repo is not a git repository: $repo_path"
  exit 1
fi

auto_dir="$script_dir/auto-readme"
structure_tool="$auto_dir/auto-file-structure.sh"
write_tool="$auto_dir/auto-write-readme.sh"
beautify_tool="$auto_dir/auto-beautify.sh"
translate_tool="$auto_dir/auto-translate-readme.sh"

for f in "$structure_tool" "$write_tool" "$beautify_tool" "$translate_tool"; do
  if [[ ! -x "$f" ]]; then
    echo "Required executable missing: $f"
    exit 1
  fi
done

run_ts="$(date +%Y%m%d_%H%M%S)"
work_dir="$repo_path/.auto-readme-work/$run_ts"
mkdir -p "$work_dir"

readme_path="$repo_path/README.md"
structure_output_file="$work_dir/repo-structure-analysis.md"
pipeline_context_file="$work_dir/pipeline-context.md"
translation_plan_file="$work_dir/translation-plan.txt"
translated_files_file="$work_dir/translated-files.txt"

cat > "$pipeline_context_file" <<CTX
# Auto README Pipeline Context

- Run timestamp: $run_ts
- Repository path: $repo_path
- User prompt: $user_prompt
- Goal: Generate a complete, beautiful, multilingual README set.

## Step Overview
1. Analyze repository structure.
2. Create first complete README draft.
3. Beautify README with better visuals (emoji/table/badges).
4. Generate multilingual README variants.
5. Optionally commit and push changes.

## Redundant Context Notes
- Every codex step should re-read repository files and this context file.
- Each step must remain self-contained and not depend on prior session memory.
CTX

default_plan=$'en|English|README.en.md\nzh-TW|Chinese Traditional|README.zh-TW.md\nzh-CN|Chinese Simplified|README.zh-CN.md\nja|Japanese|README.ja.md\nko|Korean|README.ko.md\nvi|Vietnamese|README.vi.md\nar|Arabic|README.ar.md\nfr|French|README.fr.md\nes|Spanish|README.es.md\nde|Deutsch|README.de.md\nru|Russian|README.ru.md'

i18n_mode=0
if compgen -G "$repo_path/i18n/README.*.md" > /dev/null; then
  i18n_mode=1
fi

if [[ "$i18n_mode" -eq 1 ]]; then
  : > "$translation_plan_file"
  while IFS= read -r p; do
    f="$(basename "$p")"
    suffix="${f#README.}"
    suffix="${suffix%.md}"
    case "$suffix" in
      zh-Hant|zh-TW) code="zh-Hant"; label="Chinese Traditional" ;;
      zh-Hans|zh-CN) code="zh-Hans"; label="Chinese Simplified" ;;
      ja) code="ja"; label="Japanese" ;;
      ko) code="ko"; label="Korean" ;;
      vi) code="vi"; label="Vietnamese" ;;
      ar) code="ar"; label="Arabic" ;;
      fr) code="fr"; label="French" ;;
      es) code="es"; label="Spanish" ;;
      de) code="de"; label="Deutsch" ;;
      ru) code="ru"; label="Russian" ;;
      en) code="en"; label="English" ;;
      *) code="$suffix"; label="$suffix" ;;
    esac
    # In i18n mode, skip English variant to avoid duplicate root/i18n English files.
    if [[ "$code" == "en" ]]; then
      continue
    fi
    printf '%s|%s|i18n/%s\n' "$code" "$label" "$f" >> "$translation_plan_file"
  done < <(find "$repo_path/i18n" -maxdepth 1 -type f -name 'README.*.md' | sort)
else
  printf '%s\n' "$default_plan" > "$translation_plan_file"
fi

# Build language nav line/block from plan (single canonical top nav).
declare -a nav_items
nav_items=("[English](README.md)")
if [[ "$i18n_mode" -eq 1 ]]; then
  nav_items=("[English](../README.md)")
fi
while IFS='|' read -r lang_code lang_label output_name; do
  [[ -n "${output_name:-}" ]] || continue
  href="$output_name"
  if [[ "$i18n_mode" -eq 1 ]]; then
    href="$(basename "$output_name")"
  fi
  case "$lang_code" in
    zh-Hant|zh-TW) text="中文（繁體）" ;;
    zh-Hans|zh-CN) text="中文 (简体)" ;;
    ja) text="日本語" ;;
    ko) text="한국어" ;;
    vi) text="Tiếng Việt" ;;
    ar) text="العربية" ;;
    fr) text="Français" ;;
    es) text="Español" ;;
    de) text="Deutsch" ;;
    ru) text="Русский" ;;
    en) text="English" ;;
    *) text="$lang_label" ;;
  esac
  nav_items+=("[$text]($href)")
done < "$translation_plan_file"

language_nav_line="**Languages:** "
for i in "${!nav_items[@]}"; do
  if [[ "$i" -gt 0 ]]; then
    language_nav_line+=" · "
  fi
  language_nav_line+="${nav_items[$i]}"
done
language_nav_block_file="$work_dir/language-nav-block.html"

printf '%s\n' "$language_nav_line" > "$language_nav_block_file"

echo "[1/5] Analyze repository structure"
"$structure_tool" "$repo_path" "$user_prompt" "$pipeline_context_file" "$structure_output_file"

echo "[2/5] Write first complete README"
"$write_tool" "$repo_path" "$user_prompt" "$pipeline_context_file" "$structure_output_file" "$readme_path"

echo "[3/5] Beautify README"
"$beautify_tool" "$repo_path" "$user_prompt" "$pipeline_context_file" "$readme_path"

echo "[4/5] Generate multilingual READMEs"
: > "$translated_files_file"
while IFS='|' read -r lang_code lang_label output_name; do
  [[ -n "${output_name:-}" ]] || continue
  output_path="$repo_path/$output_name"
  step_note="Translating README into $lang_label ($lang_code) as part of multilingual batch generation."
  "$translate_tool" \
    "$repo_path" \
    "$user_prompt" \
    "$pipeline_context_file" \
    "$readme_path" \
    "$lang_label" \
    "$lang_code" \
    "$output_path" \
    "$language_nav_line" \
    "$step_note"
  printf '%s\n' "$output_name" >> "$translated_files_file"
done < "$translation_plan_file"

echo "[5/6] Insert language link bar into all README variants"
(
  cd "$repo_path"
  nav_block="$(cat "$language_nav_block_file")"
  files=(README.md)
  while IFS= read -r rel; do
    [[ -n "${rel:-}" ]] || continue
    files+=("$rel")
  done < "$translated_files_file"
  for f in "${files[@]}"; do
    if [[ ! -f "$f" ]]; then
      continue
    fi
    tmp_file="$(mktemp)"
    awk '
      BEGIN {
        in_block = 0
        state = "prefix"
      }
      state == "prefix" {
        if ($0 ~ /^\*\*Languages:\*\*/) { next }
        if ($0 ~ /README(\.[a-zA-Z-]+)?\.md/ && $0 ~ /(English|中文|日本語|한국어|Tiếng Việt|العربية|Français|Español|Deutsch|Русский)/) { next }
        if ($0 == "") { next }
        if ($0 ~ /^<p([[:space:]][^>]*)?>$/) {
          in_block = 1
          block = $0 "\n"
          has_lang = ($0 ~ /Languages|README(\.[a-zA-Z-]+)?\.md/)
          next
        }
        state = "body"
        print
        next
      }
      in_block == 1 {
        block = block $0 "\n"
        if ($0 ~ /Languages|README(\.[a-zA-Z-]+)?\.md/) {
          has_lang = 1
        }
        if ($0 ~ /^<\/p>$/) {
          in_block = 0
          if (has_lang) {
            block = ""
            has_lang = 0
            next
          }
          printf "%s", block
          block = ""
          state = "body"
          next
        }
        next
      }
      { print }
    ' "$f" > "$tmp_file"
    {
      printf '%s\n\n' "$nav_block"
      cat "$tmp_file"
    } > "$f"
    rm -f "$tmp_file"
  done
)

echo "[6/7] Normalize i18n/root README layout"
if [[ "$i18n_mode" -eq 1 ]]; then
  while IFS= read -r p; do
    b="$(basename "$p")"
    # Keep canonical root README.md; move/merge language variants to i18n.
    if [[ "$b" == "README.md" ]]; then
      continue
    fi
    dest="$repo_path/i18n/$b"
    if [[ -f "$dest" ]]; then
      rm -f "$p"
    else
      mkdir -p "$repo_path/i18n"
      mv "$p" "$dest"
      if ! grep -Fxq "i18n/$b" "$translated_files_file"; then
        printf 'i18n/%s\n' "$b" >> "$translated_files_file"
      fi
    fi
  done < <(find "$repo_path" -maxdepth 1 -type f -name 'README.*.md' | sort)
fi

echo "[7/7] Optional commit and push"
if [[ "$commit_and_push" == "--commit-and-push" ]]; then
  (
    cd "$repo_path"
    if [[ "$i18n_mode" -eq 1 ]]; then
      git add README.md i18n/README.*.md
      # Stage removals of any root README.<lang>.md files after normalization.
      git add -A README.*.md
    else
      git add README.md
      while IFS= read -r rel; do
        [[ -n "${rel:-}" ]] || continue
        if [[ -f "$rel" ]]; then
          git add "$rel"
        fi
      done < "$translated_files_file"
    fi
    if git diff --cached --quiet; then
      echo "No README changes to commit."
    else
      git commit -m "Add autogenerated multilingual README pipeline output"
      git push
    fi
  )
else
  echo "Skipping commit/push. Pass --commit-and-push to enable."
fi

echo "Pipeline completed. Work dir: $work_dir"
