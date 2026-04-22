# README Translate Only Prompt Tool

This prompt tool translates a repository's existing `README.md` into
language-specific files under `i18n/`.

It is intentionally narrower than the older `auto-readme` pipeline:

- it does not polish the English README
- it does not rewrite the base README
- it does not add new sections
- it only writes `i18n/README.<lang>.md`
- it can run one language at a time in `tmux`

Default target languages:

- `ar`
- `es`
- `fr`
- `ja`
- `ko`
- `vi`
- `zh-Hans`
- `zh-Hant`
- `de`
- `ru`

Default model settings:

- model: `gpt-5.4`
- reasoning: `medium`

Example:

```bash
prompt_tools/readme-translate-only/start-readme-translate-only-tmux.sh \
  --repo-root /path/to/repo \
  --model gpt-5.4 \
  --reasoning medium \
  --no-attach
```

For a direct foreground run:

```bash
prompt_tools/readme-translate-only/translate-readme-only.sh \
  --repo-root /path/to/repo \
  --languages "zh-Hans zh-Hant ja" \
  --model gpt-5.4 \
  --reasoning medium
```
