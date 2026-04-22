# README Translate-Only Prompt Tool

Date: 2026-04-22

This note documents the `prompt_tools/readme-translate-only/` tool.

## Purpose

The tool exists for repositories that already have a good English `README.md`
and only need localized README variants.

It is deliberately different from `prompt_tools/auto-readme/`:

- `auto-readme` may analyze, polish, restructure, and then translate
- `readme-translate-only` only translates the current README
- `readme-translate-only` treats the base `README.md` as read-only input

## Output Contract

For each target language, the tool writes:

- `i18n/README.ar.md`
- `i18n/README.es.md`
- `i18n/README.fr.md`
- `i18n/README.ja.md`
- `i18n/README.ko.md`
- `i18n/README.vi.md`
- `i18n/README.zh-Hans.md`
- `i18n/README.zh-Hant.md`
- `i18n/README.de.md`
- `i18n/README.ru.md`

The English root README is not changed.

Each translated README starts with a language-navigation line. The label is in
the target language, for example:

- `Idiomas:` for Spanish
- `Langues :` for French
- `言語:` for Japanese
- `語言：` for Traditional Chinese
- `Языки:` for Russian

## Default Runtime

The default Codex configuration is:

- model: `gpt-5.4`
- reasoning: `medium`

The tmux wrapper processes languages sequentially so one language can be
reviewed, committed, and pushed before the next language starts.

## Example: Video2Book

From the AutoAppDev repo:

```bash
prompt_tools/readme-translate-only/start-readme-translate-only-tmux.sh \
  --repo-root /home/lachlan/ProjectsLFS/LazyEarn/Video2Book \
  --session video2book-readme-i18n \
  --model gpt-5.4 \
  --reasoning medium \
  --no-attach
```

That creates or refreshes:

- `/home/lachlan/ProjectsLFS/LazyEarn/Video2Book/i18n/README.<lang>.md`

The generated files can then be used by the target repo's README or website
without forcing the English README to be rewritten.
