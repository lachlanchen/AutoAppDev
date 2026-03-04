#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 9 ]]; then
  echo "Usage: $0 <repo_path> <user_prompt> <pipeline_context_file> <source_readme_path> <language_label> <language_code> <output_path> <language_nav_line> <step_note>"
  exit 1
fi

repo_path="$1"
user_prompt="$2"
pipeline_context_file="$3"
source_readme_path="$4"
language_label="$5"
language_code="$6"
output_path="$7"
language_nav_line="$8"
step_note="$9"
model="${AUTO_README_MODEL:-gpt-5.3-codex}"
reasoning_effort="${AUTO_README_REASONING_EFFORT:-medium}"

if [[ ! -d "$repo_path" ]]; then
  echo "Repo path does not exist: $repo_path"
  exit 1
fi

if [[ ! -s "$source_readme_path" ]]; then
  echo "Missing source README file: $source_readme_path"
  exit 1
fi

mkdir -p "$(dirname "$output_path")"

prompt_file="$(mktemp)"
trap 'rm -f "$prompt_file"' EXIT

cat > "$prompt_file" <<PROMPT
You are creating a language-specific README translation.

Overall task context:
- Build multilingual README variants from the beautified English README.
- Each language version should read naturally for native speakers.

Current step context:
- Step note: $step_note
- Target language: $language_label ($language_code)

Inputs:
- Repo path: $repo_path
- User goal prompt: $user_prompt
- Pipeline context file: $pipeline_context_file
- Source README (English): $source_readme_path

Required action:
- Create or overwrite this file: $output_path

Strict requirements:
1. Translate/adapt the README into the target language with fluent, native-style phrasing.
2. Keep commands, paths, filenames, code blocks, and technical identifiers unchanged unless translation is required for prose only.
3. Preserve Mermaid diagram blocks as valid Mermaid syntax; prefer keeping Mermaid blocks semantically equivalent and avoid introducing syntax-breaking edits.
4. At the very top, place exactly this language navigation line:
$language_nav_line
5. Keep the canonical banner markdown unchanged if present:
   [![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)
6. Keep Markdown structure consistent and readable.
7. Keep support/donation links unchanged if present:
   - https://chat.lazying.art/donate
   - https://paypal.me/RongzhouChen
   - https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400

Important:
- Write only the target output file for this step.
PROMPT

cat "$prompt_file" | codex exec \
  --model "$model" \
  -c "reasoning_effort=\"$reasoning_effort\"" \
  --dangerously-bypass-approvals-and-sandbox \
  -C "$repo_path" \
  --skip-git-repo-check \
  -

if [[ ! -s "$output_path" ]]; then
  echo "Failed: translated README not created: $output_path"
  exit 1
fi

echo "Translated README written: $output_path"
