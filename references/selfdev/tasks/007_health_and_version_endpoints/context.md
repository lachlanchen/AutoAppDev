# AutoAppDev Self-Development Task Context

- task_seq: 7
- task_slug: health_and_version_endpoints
- area: backend
- title: Health + version endpoints
- acceptance: `GET /api/health` returns ok with DB connectivity status; `GET /api/version` returns app name + git-less build/version string

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
