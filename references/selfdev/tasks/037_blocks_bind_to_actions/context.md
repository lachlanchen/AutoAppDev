# AutoAppDev Self-Development Task Context

- task_seq: 37
- task_slug: blocks_bind_to_actions
- area: pwa
- title: Bind blocks to action definitions
- acceptance: Blocks can reference an action definition (by id/slug) and export includes that reference; defaults remain backwards compatible for simple blocks

	Overall goal:
	- Build AutoAppDev controller (Scratch-like PWA + Tornado backend + Postgres).
	- Default theme: light.
	- Provide chat/inbox + pipeline control + logs + block-based task builder.
	- Provide a configurable action/skill toolchain:
	  - Actions can be prompt-based (agent+model+prompt), command/script/bin-based, or hybrid.
	  - Actions must be editable in the UI and reusable across pipelines.
	- Provide workspace/materials/shared-context support:
	  - Each pipeline/workspace can reference materials folder(s) and shared context visible to all tasks.
	  - Follow a standard workspace contract and enforce safe paths (no arbitrary path writes).
	- Provide multilingual support in AutoAppDev itself and in actions:
	  - UI language switching.
	  - Actions can be language-aware; default languages: zh-Hans, zh-Hant, en, ja, ko, vi, ar, fr, es.
	  - Include translation/localization action before summary/log steps by default in pipeline templates.
	- Build the pipeline script visualization + writer module (script <-> IR <-> blocks):
	  - standard formatted script (TASKS -> STEPS -> ACTIONS)
	  - import/parse existing pipeline shell scripts into IR
	  - export/generate standardized scripts and runnable drivers
	- Standardize workspace contract: materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps + resumable tasks.

	This driver script:
	- /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev/scripts/auto-autoappdev-development.sh

	Runtime directories (design targets):
	- runtime/inbox/ (user messages for pipeline)
	- runtime/outbox/ (pipeline messages back to UI; design target)
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
