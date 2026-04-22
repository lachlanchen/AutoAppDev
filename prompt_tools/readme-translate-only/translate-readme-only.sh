#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: prompt_tools/readme-translate-only/translate-readme-only.sh [options]

Translate a repository README into i18n/README.<lang>.md files one language at a
time. This is translation-only: it does not polish, restructure, or rewrite the
base README.

Options:
  --repo-root <path>      target repository root (default: current directory)
  --source <path>         source README path relative to repo root (default: README.md)
  --i18n-dir <path>       output directory relative to repo root (default: i18n)
  --languages "<list>"    space-separated language codes
  --model <name>          Codex model (default: gpt-5.4)
  --reasoning <level>     low|medium|high|xhigh (default: medium)
  --max-languages <n>     stop after n generated languages
  --branch <name>         push branch (default: current branch or main)
  --no-commit             skip git commit/push checkpoints in the target repo
  -h, --help              show help
USAGE
}

repo_root="$(pwd)"
source_rel="README.md"
i18n_dir="i18n"
languages="ar es fr ja ko vi zh-Hans zh-Hant de ru"
model="${README_TRANSLATE_MODEL:-gpt-5.4}"
reasoning="${README_TRANSLATE_REASONING:-medium}"
max_languages=0
branch=""
do_commit=1

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

repo_root="$(cd "$repo_root" && pwd)"
source_path="$repo_root/$source_rel"
i18n_path="$repo_root/$i18n_dir"
work_root="$repo_root/.readme-translate-work"
prompt_dir="$work_root/prompts"
git_common_dir="$(git -C "$repo_root" rev-parse --git-common-dir)"
case "$git_common_dir" in
  /*) ;;
  *) git_common_dir="$repo_root/$git_common_dir" ;;
esac
mkdir -p "$git_common_dir"
git_lock="$git_common_dir/readme-translate-only.lock"

case "$reasoning" in
  low|medium|high|xhigh) ;;
  *)
    echo "Invalid reasoning level: $reasoning" >&2
    exit 1
    ;;
esac

if [[ ! -s "$source_path" ]]; then
  echo "Missing source README: $source_path" >&2
  exit 1
fi

if [[ -z "$branch" ]]; then
  branch="$(git -C "$repo_root" branch --show-current 2>/dev/null || true)"
fi
if [[ -z "$branch" ]]; then
  branch="main"
fi

mkdir -p "$i18n_path" "$prompt_dir"

language_name() {
  case "$1" in
    ar) echo "Arabic" ;;
    es) echo "Spanish" ;;
    fr) echo "French" ;;
    ja) echo "Japanese" ;;
    ko) echo "Korean" ;;
    vi) echo "Vietnamese" ;;
    zh-Hans) echo "Simplified Chinese" ;;
    zh-Hant) echo "Traditional Chinese" ;;
    de) echo "German" ;;
    ru) echo "Russian" ;;
    *) echo "$1" ;;
  esac
}

language_label() {
  case "$1" in
    ar) echo "اللغات:" ;;
    es) echo "Idiomas:" ;;
    fr) echo "Langues :" ;;
    ja) echo "言語:" ;;
    ko) echo "언어:" ;;
    vi) echo "Ngôn ngữ:" ;;
    zh-Hans) echo "语言：" ;;
    zh-Hant) echo "語言：" ;;
    de) echo "Sprachen:" ;;
    ru) echo "Языки:" ;;
    *) echo "Languages:" ;;
  esac
}

i18n_nav_line() {
  local label
  label="$(language_label "$1")"
  printf '%s [English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)' "$label"
}

write_prompt() {
  local lang="$1"
  local prompt_path="$2"
  local nav_line="$3"
  local name
  name="$(language_name "$lang")"
  cat > "$prompt_path" <<PROMPT
You are creating a language-specific README translation.

This is a translate-only task.
- Do not polish or restructure the source README.
- Do not rewrite the base README.
- Do not create a shorter summary.
- Do not add new sections.

Target language:
- Code: $lang
- Name: $name

Output contract:
- Return the complete translated README as Markdown.
- Do not include commentary, summaries, wrappers, or Markdown fences around the whole file.
- The first line must be exactly:
$nav_line

Translation requirements:
1. Translate prose, headings, table descriptions, captions, alt text, and explanatory text into natural native $name.
2. Keep code blocks, shell commands, paths, filenames, environment variables, URLs, badges, and technical identifiers unchanged unless a phrase is clearly prose.
3. Preserve Markdown and HTML table structure. Do not drop rows, links, images, badges, or sections.
4. Because the output file lives under $i18n_dir/, rewrite local relative links so they still work from that folder. For example, README-root links such as docs/foo become ../docs/foo. Keep absolute http(s) URLs unchanged.
5. Preserve the source README's meaning, order, and level of detail.
6. If the English source already contains a language-navigation line, replace it with the target first line above.

English README source follows:

$(cat "$source_path")
PROMPT
}

validate_output() {
  local target="$1"
  local expected="$2"
  if [[ ! -s "$target" ]]; then
    echo "Translation output is empty: $target" >&2
    return 1
  fi
  local first_line
  first_line="$(head -n 1 "$target")"
  if [[ "$first_line" != "$expected" ]]; then
    echo "Unexpected first line in $target" >&2
    echo "Expected: $expected" >&2
    echo "Actual:   $first_line" >&2
    return 1
  fi
}

commit_language() {
  local lang="$1"
  local target_rel="$2"
  (
    flock 200
    git -C "$repo_root" add -- "$target_rel"
    if git -C "$repo_root" diff --cached --quiet -- "$target_rel"; then
      echo "No README translation changes to commit for $lang"
      exit 0
    fi
    git -C "$repo_root" commit -m "Translate README $lang"
    for attempt in 1 2 3 4 5; do
      if git -C "$repo_root" pull --rebase origin "$branch" && git -C "$repo_root" push origin "$branch"; then
        exit 0
      fi
      sleep $((attempt * 2))
    done
    echo "Failed to push README translation checkpoint for $lang after retries." >&2
    exit 1
  ) 200>"$git_lock"
}

processed=0
for lang in $languages; do
  target_rel="$i18n_dir/README.$lang.md"
  target_path="$repo_root/$target_rel"
  prompt_path="$prompt_dir/README.$lang.prompt.txt"
  output_jsonl="$work_root/README.$lang.codex.jsonl"
  nav_line="$(i18n_nav_line "$lang")"

  echo "[readme-translate] Translating $source_rel -> $target_rel with $model/$reasoning"
  write_prompt "$lang" "$prompt_path" "$nav_line"

  set +e
  codex exec \
    --json \
    --model "$model" \
    -c "model_reasoning_effort=\"$reasoning\"" \
    --sandbox read-only \
    -C "$repo_root" \
    -o "$target_path" \
    - < "$prompt_path" > "$output_jsonl"
  status=$?
  set -e

  if [[ "$status" -ne 0 ]]; then
    echo "Codex translation failed for $lang. See $output_jsonl" >&2
    exit "$status"
  fi

  validate_output "$target_path" "$nav_line"

  if [[ "$do_commit" -eq 1 ]]; then
    commit_language "$lang" "$target_rel"
  fi

  processed=$((processed + 1))
  if [[ "$max_languages" -gt 0 && "$processed" -ge "$max_languages" ]]; then
    echo "[readme-translate] Reached max language count: $max_languages"
    exit 0
  fi
done

echo "[readme-translate] Completed README translations for: $languages"
