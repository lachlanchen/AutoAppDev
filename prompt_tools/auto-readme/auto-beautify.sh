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
- Keep readability high; avoid decorative noise.
- Preserve meaningful technical detail; do not collapse rich README content into a short summary.
- Preserve donation/sponsor/support sections and important links if they already exist.

Important:
- Update only the README file above.
PROMPT

cat "$prompt_file" | codex exec \
  --dangerously-bypass-approvals-and-sandbox \
  -C "$repo_path" \
  --skip-git-repo-check \
  -

echo "README beautified: $readme_path"
