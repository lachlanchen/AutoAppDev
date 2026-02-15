# AutoAppDev

Reusable scripts + guides for building apps step-by-step from screenshots/markdown with Codex as a non-interactive tool.

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Self-Dev Status (Auto-Updated)

- Updated: 2026-02-15T14:49:13Z
- Phase commit: `Selfdev: 38 workspace_materials_and_context_api verify`
- Progress: 37 / 42 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

This section is updated by `scripts/auto-autoappdev-development.sh`.
Do not edit content between the markers.

<!-- AUTOAPPDEV:STATUS:END -->

## Philosophy
AutoAppDev treats agents as tools and keeps work stable via a strict, resumable loop:
1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

The controller app aims to embody the same concepts as Scratch-like blocks/actions (including a common `update_readme` action) so each workspace stays current and reproducible.

## Contents
- `docs/auto-development-guide.md`: Bilingual (EN/ZH) philosophy and requirements for a long-running, resumable auto-development agent.
- `docs/ORDERING_RATIONALE.md`: Example rationale for sequencing screenshot-driven steps.
- `docs/controller-mvp-scope.md`: Controller MVP scope (screens + minimal APIs).
- `docs/end-to-end-demo-checklist.md`: Deterministic manual end-to-end demo checklist (backend + PWA happy path).
- `docs/env.md`: Environment variables (.env) conventions.
- `docs/api-contracts.md`: API request/response contracts for the controller.
- `docs/pipeline-formatted-script-spec.md`: Standard pipeline script format (AAPS) and canonical IR schema (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Deterministic generator for runnable bash pipeline runners from canonical IR.
- `docs/common-actions.md`: Common action contracts/specs (includes `update_readme`).
- `docs/workspace-layout.md`: Standard workspace folders + contracts (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: Start the AutoAppDev app (backend + PWA) in tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Start the AutoAppDev self-dev driver in tmux.
- `scripts/app-auto-development.sh`: The linear pipeline driver (plan -> backend -> PWA -> Android -> iOS -> review -> summary), with resume/state support.
- `scripts/generate_screenshot_docs.sh`: Screenshot -> markdown description generator (Codex-driven).
- `scripts/setup_backend_env.sh`: Backend conda env bootstrap for local runs.
- `examples/ralph-wiggum-example.sh`: Example Codex CLI automation helper.
