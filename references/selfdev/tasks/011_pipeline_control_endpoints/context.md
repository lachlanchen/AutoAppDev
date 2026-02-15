# AutoAppDev Self-Development Task Context

- task_seq: 11
- task_slug: pipeline_control_endpoints
- area: backend
- title: Start/stop/pause/resume endpoints
- acceptance: Implement `POST /api/pipeline/start|stop|pause|resume`; state transitions are enforced (e.g. cannot pause if stopped) and return 400 with reason on invalid transitions

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
