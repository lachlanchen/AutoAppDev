# Plan: 040 pwa_i18n_language_pack

## Goal
Add runtime multilingual UI support to the PWA with a built-in language pack:
- `zh-Hans`, `zh-Hant`, `en`, `ja`, `ko`, `vi`, `ar` (RTL), `fr`, `es`
- Runtime switching (no reload required)
- Fallback strategy for missing keys (fallback to English)
- Default theme remains light (no change to existing theme defaults)

Acceptance:
- User can switch UI language at runtime via a UI control
- Arabic switches layout direction to RTL (`dir="rtl"`)
- Core UI labels/buttons/sections update to the selected language

## Current State (References)
- PWA is static/vanilla JS (no bundler):
  - `pwa/index.html` (UI markup; many hard-coded English strings)
  - `pwa/app.js` (DOM bindings + UI logic; generates dynamic labels like theme/log follow)
  - `pwa/styles.css` (layout and visual styling)
- PWA already has persistent local preferences:
  - Theme stored in `localStorage["autoappdev_theme"]` (`pwa/app.js:setTheme`)
- Supported language list is already established across tasks/docs:
  - `backend/workspace_config.py:ALLOWED_LANGUAGES` includes the same set (except this task is PWA-only)
  - `docs/auto-development-guide.md` notes i18n + RTL requirement for Arabic

## Design (Minimal, No Framework)
### Language Pack
Add a small built-in dictionary keyed by stable string IDs (English-first):
- Keys like `ui.tabs.status`, `ui.btn.start`, `ui.blocks.plan`, etc.
- Fallback: `t(key)` returns:
  1) selected language value
  2) English value
  3) the key itself (debug-friendly)

### DOM Binding Strategy
Use `data-i18n-*` attributes in `pwa/index.html` so translation coverage is explicit and robust:
- `data-i18n="key"` updates `textContent`
- `data-i18n-placeholder="key"` updates `placeholder`
- `data-i18n-title="key"` updates `title`
- (optional) `data-i18n-aria-label="key"` updates `aria-label`

This avoids brittle `querySelector(...nth-child...)` logic and keeps translations declarative.

### RTL Handling
For Arabic (`ar`):
- Set `document.documentElement.dir = "rtl"` and `lang = "ar"`
- For other languages:
  - `dir="ltr"`
  - `lang` set to selected code

Add minimal RTL CSS adjustments only if needed for readability (e.g. flip KV rows, align hint text).

### Persistence
Store the selected UI language in localStorage:
- Key: `localStorage["autoappdev_ui_lang"]`
- Boot behavior:
  - Default to `en` if not set
  - Apply language early (before most UI work) to avoid visible “flash” in English

## Implementation Steps (Next Phase: WORK)
### 1) Add Language Selector UI
Edit `pwa/index.html` topbar `.controls`:
- Add a new `<div class="select">` containing:
  - `<label data-i18n="ui.label.language">Language</label>`
  - `<select id="ui-lang">` with options using endonyms (stable, not translated):
    - `zh-Hans` -> `中文(简体)`
    - `zh-Hant` -> `中文(繁體)`
    - `en` -> `English`
    - `ja` -> `日本語`
    - `ko` -> `한국어`
    - `vi` -> `Tiếng Việt`
    - `ar` -> `العربية`
    - `fr` -> `Français`
    - `es` -> `Español`

### 2) Annotate Translatable UI Strings
Edit `pwa/index.html` and add `data-i18n*` attributes for core static strings:
- Brand:
  - `.brand-name`, `.brand-sub`
- Topbar controls:
  - Labels `Agent`, `Model`
  - Buttons `Start`, `Pause`, `Resume`, `Stop`
  - Theme button text is dynamic (handled in JS via `t()`)
- Panels:
  - “Blocks”, “Drag to canvas”, “Program”
  - Canvas empty text (“Drop blocks here…”)
- Tabs:
  - Status / Inbox / Logs / Actions / Script
- Toolbox block labels:
  - Plan / Work / Debug / Fix / Summary / Update README / Commit+Push
- Actions tab labels + buttons
- Script tab labels + placeholder
- Workspace section labels + placeholders (added in task 039)

Keep this minimal and incremental:
- Focus on user-facing navigation + primary actions first
- It’s acceptable for a few deeper hint paragraphs to remain English in v0 if needed, but ensure the tab/button/label surface is translated.

### 3) Add Language Pack File
Add `pwa/i18n.js` (new file):
- Expose `window.AutoAppDevI18n` with:
  - `PACK` object containing translations for all supported languages
  - `SUPPORTED` list
  - `RTL_LANGS` set (`["ar"]`)
  - `normalize(lang)` helper (falls back to `en`)

Update `pwa/index.html` to load it before `pwa/app.js`:
```html
<script src="i18n.js" defer></script>
<script src="app.js" defer></script>
```

### 4) Wire i18n Into the App
Edit `pwa/app.js`:
- Add `els.uiLang = document.getElementById("ui-lang")`
- Add i18n helpers:
  - `getUiLang()` reads from localStorage (default `en`)
  - `setUiLang(lang)` persists + calls `applyUiLang(lang)`
  - `t(key)` reads from `window.AutoAppDevI18n.PACK` with fallback
  - `applyUiLang(lang)`:
    - sets `document.documentElement.lang` and `.dir`
    - updates all `[data-i18n]` nodes + placeholder/title bindings
    - updates dynamic labels that are set in JS:
      - theme button text in `setTheme()`
      - log follow button text in `setLogFollow()`
      - per-block “Bind” button label in `renderProgram()` (task 037)
      - any other “created/saved/deleted” one-word status strings if practical

Important: keep exports stable.
- Do not change the canonical AAPS/IR generation titles just because the UI language changed.
- If block labels need translation, store:
  - `BLOCK_META[type].title` (canonical English used for script `STEP.title`)
  - `BLOCK_META[type].label_key` (used only for UI display via `t()`)

### 5) Minimal RTL CSS Adjustments (Only If Needed)
Edit `pwa/styles.css`:
- Add small rules scoped to `html[dir="rtl"]` for readability:
  - Optional: flip KV label/value row alignment (`.kv { flex-direction: row-reverse; }`)
  - Optional: set `.panel-actions` / `.controls` alignment if it looks wrong

Keep changes minimal; rely on `dir="rtl"` for baseline behavior first.

### 6) (Optional) Small Doc Note
If helpful, add a short note to `README.md` or `docs/auto-development-guide.md` describing:
- how to change UI language (localStorage key)
- supported languages
Only do this if the plan implementation adds a visible language selector (it will).

## Commands To Run (Verification in DEBUG/VERIFY Phase)
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

# Ensure language selector + pack are present
timeout 10s rg -n 'id=\"ui-lang\"|AutoAppDevI18n|data-i18n' pwa/index.html pwa/app.js pwa/i18n.js
```

Manual smoke (interactive):
1. Open PWA.
2. Switch language via the `Language` selector:
   - Verify tabs/buttons/labels update without reload.
3. Switch to Arabic:
   - Verify `document.documentElement.dir` becomes `rtl` and layout reads right-to-left.
4. Switch back to English and confirm direction returns to LTR.

## Acceptance Checklist
- [ ] `ui-lang` selector exists and persists choice in `localStorage["autoappdev_ui_lang"]`.
- [ ] Language pack includes all required languages: zh-Hans/zh-Hant/en/ja/ko/vi/ar/fr/es.
- [ ] Arabic sets `dir="rtl"` and `lang="ar"`.
- [ ] Core navigation + primary actions are translated (tabs, top buttons, toolbox blocks, main panel titles).
- [ ] Default theme remains light (no change to existing theme default behavior).

