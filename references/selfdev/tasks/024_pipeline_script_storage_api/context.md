# AutoAppDev Self-Development Task Context

- task_seq: 24
- task_slug: pipeline_script_storage_api
- area: backend
- title: Store scripts + IR in Postgres
- acceptance: Backend adds DB tables and minimal CRUD endpoints to persist pipeline scripts and parsed IR; PWA can save and reload by id

	Overall goal:
	- Build AutoAppDev controller (Scratch-like PWA + Tornado backend + Postgres).
	- Default theme: light.
	- Provide chat/inbox, pipeline control, logs, and block-based task builder.
	- Build the pipeline script visualization + writer module (script <-> IR <-> blocks):
	  - standard formatted script (TASKS -> STEPS -> ACTIONS)
	  - import/parse existing pipeline shell scripts into IR
	  - export/generate standardized scripts and runnable drivers
	- Standardize workspace contract: materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps + resumable tasks.

	This driver script:
	- /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev/scripts/auto-autoappdev-development.sh

	Runtime directories (design targets):
	- runtime/inbox/ (user messages for pipeline)
	- runtime/logs/ (backend + pipeline logs)
	- references/selfdev/ (tasks, prompts, summaries, state)
	- auto-apps/ (generated apps/workspaces managed by AutoAppDev)
	- materials/ (input materials for a pipeline/workspace; repo or user-provided)
	- interactions/ (user messages, decisions, approvals captured during runs)
	- outputs/ (exported artifacts, reports, built packages; not necessarily committed)
	- tools/ (reusable scripts/tools/skills invoked by pipelines)

	Important:
	- Each phase below is ONE `codex exec` call and must remain linear.
	- Do NOT run git commands (`git add/commit/push`). The driver script commits+pushes after each phase.
