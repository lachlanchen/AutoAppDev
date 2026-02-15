# Summary: 002 standardize_env_conventions

## What Changed
- Updated `.env.example` to include required env conventions (`SECRET_KEY`, `PORT`) and to document optional `PG*` variables.
- Added `docs/env.md` as the canonical `.env` conventions doc (copy instructions + single validation command).
- Linked `docs/env.md` from `README.md` and added a short pointer in `backend/README.md`.

## Why
This standardizes how local/dev and future deploy environments configure AutoAppDev (Postgres + ports + secret key) and gives a single place to validate env setup.

## How To Verify
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Read the conventions
sed -n '1,120p' docs/env.md

# Confirm standardized keys exist in .env.example
rg -n "^SECRET_KEY=|^AUTOAPPDEV_PORT=|^PORT=|^DATABASE_URL=" .env.example

# Confirm README links
rg -n "docs/env\\.md" README.md

# Optional: create a real .env and run the single validation command (from docs/env.md)
cp .env.example .env
# Edit .env for your local Postgres credentials, then run the validation command block.
```
