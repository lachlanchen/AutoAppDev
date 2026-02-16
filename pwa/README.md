# AutoAppDev PWA (Scratch-like Controller UI)

Static PWA UI served by a simple local HTTP server during development.

- Default URL: `http://127.0.0.1:5173/`
- Backend API: `http://127.0.0.1:8788/`

Toolbox notes:
- The left Blocks palette is extended at runtime with draggable **Actions** loaded from the backend (`GET /api/actions`).
- Dropping an action creates a normal step block pre-bound via `action_ref`.

Use `scripts/run_autoappdev_tmux.sh` to start both backend + PWA together.
