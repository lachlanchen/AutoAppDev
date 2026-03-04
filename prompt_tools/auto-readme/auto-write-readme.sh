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
  [![Label](https://img.shields.io/badge/...)](<target-link>)
- Never output partial badge fragments, shorthand badge text, or broken badge syntax.
- When architecture/ownership/workflow is important, include at least one GitHub-compatible Mermaid diagram (fenced block starting with three backticks + mermaid) such as flowchart LR or graph TD.
- Prefer Mermaid over raw HTML embeds/iframes for diagrams.
- Include a dedicated `Repository Topology` section with at least one Mermaid diagram that maps major folders and relationships.
- If present, the topology must explicitly show:
  - '.agents/skills/' (or equivalent skills directory),
  - 'orchestral/' and 'orchestral/prompt_tools/',
  - git submodules from '.gitmodules' (including nested submodules when discoverable).
- Add a separate `Submodules` table/list summarizing purpose and mount path for each submodule.
- At the top of README body, include exactly this banner markdown line:
  [![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)
- Include a support section using this exact block verbatim (do not change heading text, table separator style, badge/button markdown, links, punctuation, or bullet wording):
  ## ❤️ Support

  If this project is useful to you, these links directly support ongoing maintenance and hardware iteration.

  | Donate | PayPal | Stripe |
  | --- | --- | --- |
  | [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

  ### What your support makes possible

  - **Keep tools open**: hosting, inference, data storage, and community ops.
  - **Ship faster**: focused open-source time on WordsCardEink and related learning tools.
  - **Prototype devices**: e-ink hardware iterations and display layout research.
  - **Access for all**: subsidized deployments for students, creators, and community groups.
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
