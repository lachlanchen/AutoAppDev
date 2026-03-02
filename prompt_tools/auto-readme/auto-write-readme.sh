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
model="${AUTO_README_MODEL:-gpt-5.3-codex}"
reasoning_effort="${AUTO_README_REASONING_EFFORT:-medium}"

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
- Read the existing README first (if present) and use it as the primary source of truth before restructuring.
- Only increment from existing README content: do not remove existing substantive sections/content unless they are exact duplicates or clearly invalid.
- Include: title, badges/placeholders if relevant, overview, features, project structure, prerequisites, installation, usage, configuration, examples, development notes, troubleshooting, roadmap, contribution, license.
- If you add badges, use fully valid Markdown badge links only in this form:
  `[![Label](https://img.shields.io/badge/...)](<target-link>)`
- Never output partial badge fragments, shorthand badge text, or broken badge syntax.
- When architecture/ownership/workflow is important, include at least one GitHub-compatible Mermaid diagram (` ```mermaid `) such as `flowchart LR` or `graph TD`.
- Prefer Mermaid over raw HTML embeds/iframes for diagrams.
- Prefer repository-accurate commands and paths.
- If information is unknown, state assumptions clearly.
- Do not over-simplify: preserve substantive technical details, links, commands, and important sections from the existing README.
- Preserve donation/sponsor/support information if present.

Important:
- This step writes only the README file above.
- Keep language in English for this draft.
PROMPT

cat "$prompt_file" | codex exec \
  --model "$model" \
  -c "reasoning_effort=\"$reasoning_effort\"" \
  --dangerously-bypass-approvals-and-sandbox \
  -C "$repo_path" \
  --skip-git-repo-check \
  -

if [[ ! -s "$readme_path" ]]; then
  echo "Failed: README file was not created: $readme_path"
  exit 1
fi

echo "README draft written: $readme_path"
