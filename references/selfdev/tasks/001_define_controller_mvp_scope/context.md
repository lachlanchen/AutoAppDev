# AutoAppDev Self-Development Task Context

- task_seq: 1
- task_slug: define_controller_mvp_scope
- area: docs
- title: Define MVP controller scope
- acceptance: Add a short section to docs listing required screens (blocks, chat, controls, logs, settings) and the minimal backend APIs; doc is readable in <5 minutes

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
