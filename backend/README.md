# AutoAppDev Backend (Tornado)

Runs a local controller API for the AutoAppDev PWA.

## Run

```bash
cd AutoAppDev
./scripts/setup_autoappdev_env.sh

# Start backend only
conda run -n autoappdev python -m backend.app
```

Default: `http://127.0.0.1:8788`

## Env
Create `.env` from `.env.example` and follow `docs/env.md`.
