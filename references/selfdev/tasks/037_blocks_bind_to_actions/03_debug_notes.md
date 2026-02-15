# Debug Notes: 037 blocks_bind_to_actions

## Commands Run
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s node --check pwa/app.js

# Quick non-browser evaluation smoke to ensure new helpers don't crash at load time.
timeout 10s node - <<'NODE'
const fs = require('fs');
const vm = require('vm');

const src = fs.readFileSync('pwa/app.js', 'utf8');

function makeDomStub() {
  const makeEl = () => ({
    value: '',
    textContent: '',
    hidden: false,
    disabled: false,
    className: '',
    dataset: {},
    options: [],
    style: {},
    setAttribute() {},
    appendChild() {},
    remove() {},
    querySelectorAll() { return []; },
    addEventListener() {},
    scrollTop: 0,
    scrollHeight: 0,
    insertAdjacentText() {},
    classList: { toggle() {}, add() {}, remove() {} },
  });
  const els = new Map();
  return {
    body: { dataset: {}, appendChild() {}, classList: { toggle() {} } },
    getElementById(id) {
      if (!els.has(id)) els.set(id, makeEl());
      return els.get(id);
    },
    querySelectorAll() { return []; },
    createElement() { return makeEl(); },
  };
}

const sandbox = {
  window: {
    __AUTOAPPDEV_CONFIG__: { API_BASE_URL: 'http://127.0.0.1:8788' },
    AutoAppDevApi: { requestJson: async () => ({}) },
    prompt: () => null,
    alert: () => {},
    confirm: () => false,
    setInterval() {},
    setTimeout(fn) { fn(); return 0; },
    clearTimeout() {},
    URL: { createObjectURL() { return 'blob:'; }, revokeObjectURL() {} },
  },
  document: makeDomStub(),
  localStorage: { getItem() { return null; }, setItem() {} },
  navigator: {},
  console,
};

vm.runInNewContext(src, sandbox, { filename: 'pwa/app.js' });
console.log('ok: evaluated');
NODE

timeout 10s rg -n \"action_ref\" pwa/app.js docs/pipeline-formatted-script-spec.md
```

## Results
- `timeout 10s node --check pwa/app.js`
  - Exit code: `0`
- `timeout 10s node - ...`
  - Output: `ok: evaluated`
  - Exit code: `0`
- `timeout 10s rg -n "action_ref" ...`
  - Exit code: `0`

## Issues Found
- None in these smoke checks.

