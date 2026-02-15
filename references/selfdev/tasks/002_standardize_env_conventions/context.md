# AutoAppDev Self-Development Task Context

- task_seq: 2
- task_slug: standardize_env_conventions
- area: docs
- title: Standardize .env conventions
- acceptance: Docs specify required env vars (DATABASE_URL or PG* vars, PORT, SECRET_KEY) and how to copy from .env.example; includes one command to validate env

Overall goal:
- Build AutoAppDev controller (Scratch-like PWA + Tornado backend + Postgres).
- Default theme: light.
- Provide chat/inbox, pipeline control, logs, and block-based task builder.

This driver script:
- /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev/scripts/auto-autoappdev-development.sh

Runtime directories (design targets):
- runtime/inbox/ (user messages for pipeline)
- runtime/logs/ (backend + pipeline logs)
- references/selfdev/ (tasks, prompts, summaries, state)

Important:
- Each phase below is ONE `codex exec` call and must remain linear.
- Do NOT run git commands (`git add/commit/push`). The driver script commits+pushes after each phase.
