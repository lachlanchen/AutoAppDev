# Debug/Verify Notes: 002 standardize_env_conventions

## What I Verified
Doc-level smoke verification (no services started) to confirm:
- `.env.example` includes the standardized required conventions (`SECRET_KEY`, `PORT`) and documents `PG*` as an alternative convention.
- `docs/env.md` exists, includes copy instructions from `.env.example`, and includes exactly one validation command.
- `README.md` links to `docs/env.md`.
- `.gitignore` ignores `.env` (so the suggested `cp .env.example .env` workflow is safe from accidental commits).

## Commands Run + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

ls -la docs/env.md .env.example README.md backend/README.md
wc -l docs/env.md .env.example README.md backend/README.md

# Required mentions in docs/env.md
rg -n "cp \\.env\\.example \\.env" docs/env.md
rg -n "\\bSECRET_KEY\\b" docs/env.md
rg -n "\\bPORT\\b" docs/env.md
rg -n "\\bDATABASE_URL\\b" docs/env.md
rg -n "\\bPGHOST\\b|\\bPGPORT\\b|\\bPGUSER\\b|\\bPGPASSWORD\\b|\\bPGDATABASE\\b" docs/env.md

# Validation command presence
rg -n "Validate Your \\.env|bash -lc|OK: env looks set|Missing env:" docs/env.md

# .env.example keys present
rg -n "^SECRET_KEY=|^AUTOAPPDEV_HOST=|^AUTOAPPDEV_PORT=|^PORT=|^DATABASE_URL=" .env.example

# Doc links
rg -n "docs/env\\.md" README.md
rg -n "docs/env\\.md" backend/README.md

# .env safety
sed -n '1,60p' .gitignore
# OK: .env and .env.* are ignored; .env.example is explicitly un-ignored.
```

## Issues Found
- None.

## Notes
- I did not execute the validation command because it requires a real `.env` file in the repo root; the command is present and copy/pasteable as required by acceptance.
