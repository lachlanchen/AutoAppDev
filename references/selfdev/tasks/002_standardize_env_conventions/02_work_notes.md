# Work Notes: 002 standardize_env_conventions

## Summary of Changes
- Updated `.env.example` to standardize required conventions (`SECRET_KEY`, `PORT`) and document optional `PG*` variables.
- Added `docs/env.md` as the single source of truth for `.env` usage, including copy instructions and a single validation command.
- Updated `README.md` Contents to link to `docs/env.md`.
- Updated `backend/README.md` with a short pointer to `docs/env.md`.

## Files Changed
- Updated: `.env.example`
- Added: `docs/env.md`
- Updated: `README.md`
- Updated: `backend/README.md`

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

# Acceptance-oriented doc checks
test -s docs/env.md
rg -n "\\bDATABASE_URL\\b" docs/env.md
rg -n "\\bPGHOST\\b|\\bPGPORT\\b|\\bPGUSER\\b|\\bPGPASSWORD\\b|\\bPGDATABASE\\b" docs/env.md
rg -n "\\bPORT\\b" docs/env.md
rg -n "\\bSECRET_KEY\\b" docs/env.md
rg -n "cp \\.env\\.example \\.env" docs/env.md

# .env.example contains standardized keys
rg -n "^SECRET_KEY=" .env.example
rg -n "^PORT=" .env.example
rg -n "^AUTOAPPDEV_PORT=" .env.example
rg -n "^DATABASE_URL=" .env.example

# README links to env doc
rg -n "docs/env\\.md" README.md
```

## Notes
- `PG*` vars are documented as a supported convention, but the backend currently reads `DATABASE_URL` (see `backend/app.py`).
- The validation command in `docs/env.md` is a single copy/paste command that loads `.env` and checks `SECRET_KEY`, `DATABASE_URL`, and `AUTOAPPDEV_PORT`/`PORT`.
