# AutoAppDev Self-Development Task Context

- task_seq: 13
- task_slug: log_capture_and_storage
- area: backend
- title: Capture logs for viewing
- acceptance: Backend captures subprocess stdout/stderr into a rolling buffer and optionally persists last N lines in DB; `GET /api/logs?since=<id>` returns incremental lines

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
