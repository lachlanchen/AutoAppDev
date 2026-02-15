# Debug Notes: 040 pwa_i18n_language_pack

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js
OK: node --check pwa/app.js

timeout 10s node --check pwa/i18n.js
OK: node --check pwa/i18n.js

timeout 10s node --check pwa/service-worker.js
OK: node --check pwa/service-worker.js
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s rg -n 'id=\"ui-lang\"|AutoAppDevI18n|data-i18n' pwa/index.html pwa/app.js pwa/i18n.js | head -n 80
```

Result (first 80 lines):
```text
pwa/app.js:82:  const i18n = window.AutoAppDevI18n && typeof window.AutoAppDevI18n === "object" ? window.AutoAppDevI18n : null;
pwa/app.js:89:  const i18n = window.AutoAppDevI18n && typeof window.AutoAppDevI18n === "object" ? window.AutoAppDevI18n : null;
pwa/app.js:100:  const i18n = window.AutoAppDevI18n && typeof window.AutoAppDevI18n === "object" ? window.AutoAppDevI18n : null;
pwa/app.js:113:  document.querySelectorAll("[data-i18n]").forEach((el) => {
pwa/app.js:114:    const key = el.getAttribute("data-i18n");
pwa/app.js:118:  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
pwa/app.js:119:    const key = el.getAttribute("data-i18n-placeholder");
pwa/app.js:123:  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
pwa/app.js:124:    const key = el.getAttribute("data-i18n-title");
pwa/app.js:128:  document.querySelectorAll("[data-i18n-aria-label]").forEach((el) => {
pwa/app.js:129:    const key = el.getAttribute("data-i18n-aria-label");
pwa/i18n.js:1217:  window.AutoAppDevI18n = { PACK, SUPPORTED, RTL_LANGS, normalize };
pwa/index.html:28:          <div class="brand-name" data-i18n="ui.brand.name">AutoAppDev Studio</div>
pwa/index.html:29:          <div class="brand-sub" data-i18n="ui.brand.sub">Scratch-like pipeline controller</div>
pwa/index.html:35:          <label data-i18n="ui.label.agent">Agent</label>
pwa/index.html:44:          <label data-i18n="ui.label.model">Model</label>
pwa/index.html:52:          <label data-i18n="ui.label.language">Language</label>
pwa/index.html:53:          <select id="ui-lang">
pwa/index.html:66:        <button class="btn btn--primary" id="btn-start" data-i18n="ui.btn.start">Start</button>
pwa/index.html:67:        <button class="btn" id="btn-pause" data-i18n="ui.btn.pause">Pause</button>
pwa/index.html:68:        <button class="btn" id="btn-resume" data-i18n="ui.btn.resume">Resume</button>
pwa/index.html:69:        <button class="btn btn--danger" id="btn-stop" data-i18n="ui.btn.stop">Stop</button>
pwa/index.html:79:          <div class="panel-title" data-i18n="ui.panel.blocks.title">Blocks</div>
pwa/index.html:80:          <div class="panel-hint" data-i18n="ui.panel.blocks.hint">Drag to canvas</div>
pwa/index.html:83:          <div class="block block--plan" draggable="true" data-block="plan" data-i18n="ui.block.plan">Plan</div>
pwa/index.html:84:          <div class="block block--work" draggable="true" data-block="work" data-i18n="ui.block.work">Work</div>
pwa/index.html:85:          <div class="block block--debug" draggable="true" data-block="debug" data-i18n="ui.block.debug">Debug</div>
pwa/index.html:86:          <div class="block block--fix" draggable="true" data-block="fix" data-i18n="ui.block.fix">Fix</div>
pwa/index.html:87:          <div class="block block--summary" draggable="true" data-block="summary" data-i18n="ui.block.summary">
pwa/index.html:90:          <div class="block block--summary" draggable="true" data-block="update_readme" data-i18n="ui.block.update_readme">
pwa/index.html:93:          <div class="block block--release" draggable="true" data-block="commit_push" data-i18n="ui.block.commit_push">
pwa/index.html:101:          <div class="panel-title" data-i18n="ui.panel.program.title">Program</div>
pwa/index.html:103:            <button class="btn btn--ghost" id="btn-clear" data-i18n="ui.btn.clear">Clear</button>
pwa/index.html:104:            <button class="btn btn--ghost" id="btn-export" data-i18n="ui.btn.export_json">Export JSON</button>
pwa/index.html:105:            <button class="btn btn--ghost" id="btn-send-plan" data-i18n="ui.btn.send_plan">Send Plan</button>
pwa/index.html:106:            <button class="btn btn--ghost" id="btn-save-script" data-i18n="ui.btn.save_script">Save Script</button>
pwa/index.html:107:            <button class="btn btn--ghost" id="btn-load-script" data-i18n="ui.btn.load_script">Load Script</button>
pwa/index.html:110:        <div class="canvas" id="canvas" aria-label="Program canvas" data-i18n-aria-label="ui.canvas.aria">
pwa/index.html:112:            <span data-i18n="ui.canvas.empty">Drop blocks here to build a pipeline.</span>
pwa/index.html:120:          <button class="tab is-active" data-tab="status" data-i18n="ui.tab.status">Status</button>
pwa/index.html:121:          <button class="tab" data-tab="chat" data-i18n="ui.tab.inbox">Inbox</button>
pwa/index.html:122:          <button class="tab" data-tab="logs" data-i18n="ui.tab.logs">Logs</button>
pwa/index.html:123:          <button class="tab" data-tab="actions" data-i18n="ui.tab.actions">Actions</button>
pwa/index.html:124:          <button class="tab" data-tab="script" data-i18n="ui.tab.script">Script</button>
pwa/index.html:129:            <div class="k" data-i18n="ui.status.backend">Backend</div>
pwa/index.html:133:            <div class="k" data-i18n="ui.status.db">DB</div>
pwa/index.html:137:            <div class="k" data-i18n="ui.status.pipeline">Pipeline</div>
pwa/index.html:141:            <div class="k" data-i18n="ui.status.pid">PID</div>
pwa/index.html:149:          <div class="panel-title" data-i18n="ui.panel.workspace.title">Workspace</div>
pwa/index.html:150:          <div class="panel-hint" data-i18n="ui.panel.workspace.hint">Materials + shared context (persisted per workspace)</div>
pwa/index.html:153:            <input class="input" id="ws-slug" placeholder="my_workspace" data-i18n-placeholder="ui.ws.slug_ph" />
pwa/index.html:154:            <button class="btn btn--ghost" id="ws-load" data-i18n="ui.btn.load">Load</button>
pwa/index.html:155:            <button class="btn btn--ghost" id="ws-save" data-i18n="ui.btn.save">Save</button>
pwa/index.html:160:              <label data-i18n="ui.ws.default_language">Default language</label>
pwa/index.html:174:              <label data-i18n="ui.ws.shared_context_path_optional">Shared context path (optional)</label>
pwa/index.html:179:                data-i18n-placeholder="ui.ws.shared_context_path_ph"
pwa/index.html:185:            <label data-i18n="ui.ws.materials_paths">Materials paths (one per line)</label>
pwa/index.html:191:              data-i18n-placeholder="ui.ws.materials_paths_ph"
pwa/index.html:196:            <label data-i18n="ui.ws.shared_context_text">Shared context text</label>
pwa/index.html:202:              data-i18n-placeholder="ui.ws.shared_context_text_ph"
pwa/index.html:220:              data-i18n-placeholder="ui.chat.input_ph"
pwa/index.html:222:            <button class="btn btn--primary" id="chat-send" data-i18n="ui.btn.send">Send</button>
pwa/index.html:238:              data-i18n-aria-label="ui.logs.follow_aria"
pwa/index.html:239:              data-i18n-title="ui.logs.follow_title"
pwa/index.html:243:            <button class="btn btn--ghost" id="log-refresh" data-i18n="ui.btn.refresh">Refresh</button>
pwa/index.html:250:            <button class="btn btn--ghost" id="actions-refresh" data-i18n="ui.btn.refresh">Refresh</button>
pwa/index.html:251:            <button class="btn btn--ghost" id="actions-new" data-i18n="ui.btn.new">New</button>
pwa/index.html:252:            <button class="btn btn--ghost" id="actions-save" data-i18n="ui.btn.save">Save</button>
pwa/index.html:253:            <button class="btn btn--ghost btn--danger" id="actions-delete" data-i18n="ui.btn.delete">Delete</button>
pwa/index.html:260:            data-i18n-aria-label="ui.actions.list_aria"
pwa/index.html:267:              <label data-i18n="ui.actions.id">ID</label>
pwa/index.html:273:                data-i18n-placeholder="ui.actions.id_ph"
pwa/index.html:278:              <label data-i18n="ui.actions.enabled">Enabled</label>
pwa/index.html:285:              <label data-i18n="ui.actions.title">Title</label>
pwa/index.html:290:                data-i18n-placeholder="ui.actions.action_title_ph"
pwa/index.html:294:              <label data-i18n="ui.actions.kind">Kind</label>
pwa/index.html:304:              <label data-i18n="ui.actions.prompt">Prompt</label>
pwa/index.html:310:                data-i18n-placeholder="ui.actions.prompt_ph"
pwa/index.html:315:                <label data-i18n="ui.actions.agent_optional">Agent (optional)</label>
pwa/index.html:319:                <label data-i18n="ui.actions.model_optional">Model (optional)</label>
```

```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev
timeout 10s node - <<'NODE'
const vm = require('vm');
const fs = require('fs');
const ctx = { window: {} };
vm.runInNewContext(fs.readFileSync('pwa/i18n.js', 'utf8'), ctx, { filename: 'pwa/i18n.js' });
const i18n = ctx.window.AutoAppDevI18n;
console.log('SUPPORTED=' + i18n.SUPPORTED.join(','));
console.log('PACK_LANGS=' + Object.keys(i18n.PACK).join(','));
console.log('RTL=' + Array.from(i18n.RTL_LANGS).join(','));
const key = 'ui.btn.start';
for (const lang of i18n.SUPPORTED) {
  const v = (i18n.PACK[lang] || {})[key];
  console.log(lang + ':' + key + '=' + String(v || ''));
}
NODE
```

Result:
```text
SUPPORTED=zh-Hans,zh-Hant,en,ja,ko,vi,ar,fr,es
PACK_LANGS=en,zh-Hans,zh-Hant,ja,ko,vi,ar,fr,es
RTL=ar
zh-Hans:ui.btn.start=开始
zh-Hant:ui.btn.start=開始
en:ui.btn.start=Start
ja:ui.btn.start=開始
ko:ui.btn.start=시작
vi:ui.btn.start=Bắt đầu
ar:ui.btn.start=ابدأ
fr:ui.btn.start=Démarrer
es:ui.btn.start=Iniciar
```

## Manual Smoke (Not Run Here)
- Switch `Language` selector and verify tabs/buttons/labels update without reload.
- Switch to Arabic and verify `document.documentElement.dir === "rtl"`, then switch back and verify it returns to `ltr`.

## Issues Found
- None during these checks.

