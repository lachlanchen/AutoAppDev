# AutoAppDev Self-Development Task Context

- task_seq: 9
- task_slug: inbox_messages_table_and_api
- area: backend
- title: Chat/inbox persistence API
- acceptance: Create DB table for inbox messages; implement `GET /api/inbox` (latest N) and `POST /api/inbox` (create) with basic validation

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
