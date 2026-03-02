#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "Usage: $0 <repo_path> <user_prompt> <pipeline_context_file> <readme_path>"
  exit 1
fi

repo_path="$1"
user_prompt="$2"
pipeline_context_file="$3"
readme_path="$4"
model="${AUTO_README_MODEL:-gpt-5.3-codex}"
reasoning_effort="${AUTO_README_REASONING_EFFORT:-medium}"

if [[ ! -d "$repo_path" ]]; then
  echo "Repo path does not exist: $repo_path"
  exit 1
fi

if [[ ! -s "$readme_path" ]]; then
  echo "Missing README file: $readme_path"
  exit 1
fi

prompt_file="$(mktemp)"
trap 'rm -f "$prompt_file"' EXIT

cat > "$prompt_file" <<PROMPT
You are beautifying an existing README without losing technical correctness.

Inputs:
- Repo path: $repo_path
- User goal prompt: $user_prompt
- Pipeline context file: $pipeline_context_file
- README to update: $readme_path

Required action:
- Rewrite and improve $readme_path in-place.

Beautification requirements:
- Keep the existing README structure and depth unless a change clearly improves clarity.
- Only increment and polish from the current README; do not delete substantive existing sections/content unless exact duplicates or clearly invalid.
- Keep content repository-accurate.
- Make layout more attractive with tasteful emojis, tables, and visual sectioning.
- Add color cues using Markdown-compatible badge styles (e.g., shields.io) where useful.
- Badge safety:
  - Only use full Shields URLs (e.g., `https://img.shields.io/badge/...`).
  - Ensure each badge uses valid Markdown image-link syntax:
    `[![Label](https://img.shields.io/badge/...)](<target-link>)`
  - Never emit incomplete badge fragments such as `[Principle-...` or `[![...?...)]` without a full URL.
- Encourage diagrams using GitHub-compatible Mermaid blocks (` ```mermaid `), especially for architecture/runtime ownership/flow sections.
- Do not use raw HTML iframe/embed code for diagrams; prefer Mermaid fenced code blocks.
- Keep readability high; avoid decorative noise.
- Preserve meaningful technical detail; do not collapse rich README content into a short summary.
- Preserve donation/sponsor/support sections and important links if they already exist.

Important:
- Update only the README file above.
PROMPT

cat "$prompt_file" | codex exec \
  --model "$model" \
  -c "reasoning_effort=\"$reasoning_effort\"" \
  --dangerously-bypass-approvals-and-sandbox \
  -C "$repo_path" \
  --skip-git-repo-check \
  -

echo "README beautified: $readme_path"
