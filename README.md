# AutoAppDev

Reusable scripts + guides for building apps step-by-step from screenshots/markdown with Codex as a non-interactive tool.

## Contents
- `docs/auto-development-guide.md`: Bilingual (EN/ZH) philosophy and requirements for a long-running, resumable auto-development agent.
- `docs/ORDERING_RATIONALE.md`: Example rationale for sequencing screenshot-driven steps.
- `docs/controller-mvp-scope.md`: Controller MVP scope (screens + minimal APIs).
- `docs/env.md`: Environment variables (.env) conventions.
- `scripts/app-auto-development.sh`: The linear pipeline driver (plan -> backend -> PWA -> Android -> iOS -> review -> summary), with resume/state support.
- `scripts/generate_screenshot_docs.sh`: Screenshot -> markdown description generator (Codex-driven).
- `scripts/setup_backend_env.sh`: Backend conda env bootstrap for local runs.
- `examples/ralph-wiggum-example.sh`: Example Codex CLI automation helper.
