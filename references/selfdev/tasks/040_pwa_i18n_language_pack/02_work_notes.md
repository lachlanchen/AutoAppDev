# Work Notes: 040 pwa_i18n_language_pack

## Implementation Notes
- Added a built-in language pack and normalizer in `pwa/i18n.js` (exposes `window.AutoAppDevI18n`) covering:
  - `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `vi`, `ar` (RTL), `fr`, `es`
- Updated `pwa/index.html`:
  - Load `i18n.js` before `app.js` (both `defer`).
  - Added topbar UI language selector: `select#ui-lang`.
  - Annotated core UI strings with `data-i18n*` attributes (`data-i18n`, `data-i18n-placeholder`, `data-i18n-title`, `data-i18n-aria-label`) to support declarative translation.
- Updated `pwa/app.js`:
  - Added `autoappdev_ui_lang` localStorage key and runtime language switching (`setUiLang` + `applyUiLang`).
  - Sets `document.documentElement.lang` and `dir` (`rtl` for Arabic).
  - Added `t(key)` translation helper with fallback to English and then key (debug-friendly).
  - Updated dynamic labels to use i18n:
    - Theme button label via `ui.theme.light`/`ui.theme.dark`
    - Logs follow button label via `ui.btn.pause`/`ui.btn.follow`
    - Program “Bind” button + related prompts/alerts
    - Actions list empty state + enabled/disabled meta
  - Kept exports stable:
    - `BLOCK_META` now stores canonical `title` and UI-only `label_key`.
    - IR/AAPS/runner exports use canonical titles (English) via `canonicalBlockTitle(...)`, regardless of selected UI language.
  - Health + pipeline badges now display translated labels while keeping raw state in `title` for debugging.
- Updated `pwa/styles.css` with minimal RTL tweaks:
  - Reverse key/value row order in status list (`.kv`) under `html[dir="rtl"]`.
  - Mirror chat message accent borders (`.msg--user` / `.msg--system`) under RTL.
- Updated `pwa/service-worker.js`:
  - Added `./i18n.js` to `PRECACHE_URLS`.
  - Bumped cache name to ensure the new shell asset is cached.
- Updated `docs/auto-development-guide.md` with a short note about persisting UI language choice.

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

ls -la pwa
sed -n '1,220p' pwa/app.js
sed -n '220,520p' pwa/app.js
sed -n '520,920p' pwa/app.js
sed -n '1,260p' pwa/styles.css

rg -n "\\.kv" -n pwa/styles.css | head -n 20
nl -ba pwa/styles.css | sed -n '330,430p'

nl -ba pwa/index.html | sed -n '90,220p'
nl -ba pwa/index.html | sed -n '220,400p'

nl -ba pwa/app.js | sed -n '1,120p'
rg -n "meta\\.label" pwa/app.js
rg -n "BLOCK_META\\[" pwa/app.js
rg -n "function formatProgramBlockLabel" pwa/app.js
nl -ba pwa/app.js | sed -n '260,340p'
nl -ba pwa/app.js | sed -n '430,540p'
nl -ba pwa/app.js | sed -n '1160,1200p'
rg -n "function setLogFollow" pwa/app.js
nl -ba pwa/app.js | sed -n '1420,1485p'
rg -n "function renderActionsList" pwa/app.js
nl -ba pwa/app.js | sed -n '780,860p'
rg -n "Script title\\?|Load script id\\?|Runner title\\?|Workspace slug for auto-apps" pwa/app.js
rg -n "window\\.prompt\\(" pwa/app.js | head -n 50
nl -ba pwa/app.js | sed -n '1060,1120p'
nl -ba pwa/app.js | sed -n '1188,1245p'
nl -ba pwa/app.js | sed -n '1245,1345p'
nl -ba pwa/app.js | sed -n '1335,1395p'

tail -n 40 pwa/styles.css
cat pwa/service-worker.js
nl -ba docs/auto-development-guide.md | sed -n '35,90p'

timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/i18n.js
```

