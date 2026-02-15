# Summary: 040 pwa_i18n_language_pack

## What Changed
- Added built-in PWA language pack + runtime switching:
  - New `pwa/i18n.js` exposes `window.AutoAppDevI18n` with `SUPPORTED`, `PACK`, RTL detection, and language normalization.
- Updated PWA UI to be translatable:
  - `pwa/index.html` now loads `i18n.js` before `app.js`, adds a `Language` selector (`select#ui-lang`), and marks core strings with `data-i18n*` attributes.
  - `pwa/app.js` wires `autoappdev_ui_lang` persistence, translates static and dynamic labels, and toggles `document.documentElement.dir` to `rtl` for Arabic.
  - Export stability preserved: canonical block titles remain English for IR/AAPS/runner output; UI labels are translated via `label_key`.
- Minimal RTL styling tweaks in `pwa/styles.css` for status KV rows + chat message accents.
- Updated `pwa/service-worker.js` shell cache to include `i18n.js` (cache name bumped).
- Doc note added in `docs/auto-development-guide.md` about persisting UI language selection.

## Why
Task 040 acceptance requires runtime UI language switching with a built-in pack for:
`zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `vi`, `ar` (RTL), `fr`, `es`, while keeping the default theme light and keeping exported pipeline scripts stable.

## How To Verify
Minimal checks:
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node --check pwa/app.js
timeout 10s node --check pwa/i18n.js
timeout 10s node --check pwa/service-worker.js
timeout 10s rg -n 'id=\"ui-lang\"|AutoAppDevI18n|data-i18n' pwa/index.html pwa/app.js pwa/i18n.js
```

Manual smoke:
1. Open the PWA and switch `Language` (topbar) between a few languages; confirm labels update without reload.
2. Switch to Arabic and confirm layout direction becomes RTL; switch back to English and confirm it returns to LTR.

