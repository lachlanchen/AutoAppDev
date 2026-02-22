#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 5 ]]; then
  echo "Usage: $0 <repo_path> <user_prompt> <pipeline_context_file> <structure_output_file> <readme_path>"
  exit 1
fi

repo_path="$1"
user_prompt="$2"
pipeline_context_file="$3"
structure_output_file="$4"
readme_path="$5"

if [[ ! -d "$repo_path" ]]; then
  echo "Repo path does not exist: $repo_path"
  exit 1
fi

if [[ ! -s "$structure_output_file" ]]; then
  echo "Missing structure output file: $structure_output_file"
  exit 1
fi

prompt_file="$(mktemp)"
trap 'rm -f "$prompt_file"' EXIT

cat > "$prompt_file" <<PROMPT
You are generating the first complete README draft for a repository.

Inputs:
- Repo path: $repo_path
- User goal prompt: $user_prompt
- Pipeline context file: $pipeline_context_file
- Repository structure analysis: $structure_output_file

Required actions:
1. Read repository files and the structure analysis.
2. Write a complete, high-quality README to this exact path: $readme_path
3. Make it "complete and beautiful" with strong structure and practical details.

README requirements:
- Markdown only.
- Include: title, badges/placeholders if relevant, overview, features, project structure, prerequisites, installation, usage, configuration, examples, development notes, troubleshooting, roadmap, contribution, license.
- Prefer repository-accurate commands and paths.
- If information is unknown, state assumptions clearly.

Important:
- This step writes only the README file above.
- Keep language in English for this draft.
PROMPT

cat "$prompt_file" | codex exec \
  --dangerously-bypass-approvals-and-sandbox \
  -C "$repo_path" \
  --skip-git-repo-check \
  -

if [[ ! -s "$readme_path" ]]; then
  echo "Failed: README file was not created: $readme_path"
  exit 1
fi

echo "README draft written: $readme_path"
