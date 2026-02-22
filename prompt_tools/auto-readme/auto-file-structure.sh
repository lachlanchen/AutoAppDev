#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "Usage: $0 <repo_path> <user_prompt> <pipeline_context_file> <structure_output_file>"
  exit 1
fi

repo_path="$1"
user_prompt="$2"
pipeline_context_file="$3"
structure_output_file="$4"

if [[ ! -d "$repo_path" ]]; then
  echo "Repo path does not exist: $repo_path"
  exit 1
fi

mkdir -p "$(dirname "$structure_output_file")"

prompt_file="$(mktemp)"
trap 'rm -f "$prompt_file"' EXIT

cat > "$prompt_file" <<PROMPT
You are analyzing a repository to support README generation.

Primary goal:
- Produce a concise but complete repository structure analysis in Markdown.

Inputs:
- Repo path: $repo_path
- User goal prompt: $user_prompt
- Pipeline context file: $pipeline_context_file

Required actions:
1. Inspect the repository tree and key files (README, package/config files, docs, source entrypoints, scripts).
2. Infer project purpose, setup steps, usage flow, and notable implementation details.
3. Write the final analysis to this exact file path: $structure_output_file

Output format requirements for $structure_output_file:
- Markdown only.
- Sections: Project Summary, Repository Map, Key Components, Setup Signals, Usage Signals, Gaps/Unknowns.
- Include a compact tree-like list of major directories/files.
- Keep it factual and based on repository contents.

Important:
- Do not modify repository files in this step.
- Use shell commands to inspect and then write only the output file above.
PROMPT

cat "$prompt_file" | codex exec \
  --dangerously-bypass-approvals-and-sandbox \
  -C "$repo_path" \
  --skip-git-repo-check \
  -

if [[ ! -s "$structure_output_file" ]]; then
  echo "Failed: structure output file was not created: $structure_output_file"
  exit 1
fi

echo "Structure analysis written: $structure_output_file"
