const els = {
  themeBtn: document.getElementById("btn-theme"),
  agentSelect: document.getElementById("agent-select"),
  modelSelect: document.getElementById("model-select"),
  uiLang: document.getElementById("ui-lang"),
  start: document.getElementById("btn-start"),
  pause: document.getElementById("btn-pause"),
  resume: document.getElementById("btn-resume"),
  stop: document.getElementById("btn-stop"),
  ctrlMsg: document.getElementById("ctrl-msg"),
  backendHealth: document.getElementById("backend-health"),
  dbHealth: document.getElementById("db-health"),
  pipelineStatus: document.getElementById("pipeline-status"),
  pipelinePid: document.getElementById("pipeline-pid"),
  toolbox: document.getElementById("toolbox"),
  canvas: document.getElementById("canvas"),
  canvasEmpty: document.getElementById("canvas-empty"),
  exportBtn: document.getElementById("btn-export"),
  sendPlanBtn: document.getElementById("btn-send-plan"),
  saveScriptBtn: document.getElementById("btn-save-script"),
  loadScriptBtn: document.getElementById("btn-load-script"),
  clearBtn: document.getElementById("btn-clear"),
  export: document.getElementById("export"),
  tabs: document.querySelectorAll(".tab"),
  tabStatus: document.getElementById("tab-status"),
  tabChat: document.getElementById("tab-chat"),
  tabLogs: document.getElementById("tab-logs"),
  tabActions: document.getElementById("tab-actions"),
  tabScript: document.getElementById("tab-script"),
  chatlog: document.getElementById("chatlog"),
  chatInput: document.getElementById("chat-input"),
  chatSend: document.getElementById("chat-send"),
  logSelect: document.getElementById("log-select"),
  logFollow: document.getElementById("log-follow"),
  logRefresh: document.getElementById("log-refresh"),
  logview: document.getElementById("logview"),
  scriptText: document.getElementById("script-text"),
  scriptFile: document.getElementById("script-file"),
  scriptParse: document.getElementById("script-parse"),
  scriptImportShell: document.getElementById("script-import-shell"),
  scriptFromBlocks: document.getElementById("script-from-blocks"),
  scriptDownloadAaps: document.getElementById("script-download-aaps"),
  scriptDownloadRunner: document.getElementById("script-download-runner"),
  scriptMsg: document.getElementById("script-msg"),

  actionsRefresh: document.getElementById("actions-refresh"),
  actionsNew: document.getElementById("actions-new"),
  actionsSave: document.getElementById("actions-save"),
  actionsDelete: document.getElementById("actions-delete"),
  actionsList: document.getElementById("actions-list"),
  actionId: document.getElementById("action-id"),
  actionEnabled: document.getElementById("action-enabled"),
  actionTitle: document.getElementById("action-title"),
  actionKind: document.getElementById("action-kind"),
  actionSectionPrompt: document.getElementById("action-section-prompt"),
  actionSectionCommand: document.getElementById("action-section-command"),
  actionPrompt: document.getElementById("action-prompt"),
  actionAgent: document.getElementById("action-agent"),
  actionModel: document.getElementById("action-model"),
  actionReasoning: document.getElementById("action-reasoning"),
  actionTimeout: document.getElementById("action-timeout"),
  actionCmd: document.getElementById("action-cmd"),
  actionShell: document.getElementById("action-shell"),
  actionCwd: document.getElementById("action-cwd"),
  actionTimeoutCmd: document.getElementById("action-timeout-cmd"),
  actionsMsg: document.getElementById("actions-msg"),

  wsSlug: document.getElementById("ws-slug"),
  wsLoad: document.getElementById("ws-load"),
  wsSave: document.getElementById("ws-save"),
  wsMaterials: document.getElementById("ws-materials"),
  wsLanguage: document.getElementById("ws-language"),
  wsContextText: document.getElementById("ws-context-text"),
  wsContextPath: document.getElementById("ws-context-path"),
  wsMsg: document.getElementById("ws-msg"),
};

const UI_LANG_STORAGE_KEY = "autoappdev_ui_lang";
let uiLang = "en";

function normalizeUiLang(raw) {
  const i18n = window.AutoAppDevI18n && typeof window.AutoAppDevI18n === "object" ? window.AutoAppDevI18n : null;
  if (i18n && typeof i18n.normalize === "function") return i18n.normalize(raw);
  const s = String(raw || "").trim();
  return s || "en";
}

function isRtlUiLang(lang) {
  const i18n = window.AutoAppDevI18n && typeof window.AutoAppDevI18n === "object" ? window.AutoAppDevI18n : null;
  const l = normalizeUiLang(lang);
  const rtl = i18n && i18n.RTL_LANGS;
  if (rtl && typeof rtl.has === "function") return rtl.has(l);
  if (Array.isArray(rtl)) return rtl.includes(l);
  return l === "ar";
}

function t(key) {
  const k = String(key || "");
  if (!k) return "";
  const i18n = window.AutoAppDevI18n && typeof window.AutoAppDevI18n === "object" ? window.AutoAppDevI18n : null;
  const pack = (i18n && i18n.PACK && typeof i18n.PACK === "object" ? i18n.PACK : {}) || {};
  const cur = (pack && uiLang && pack[uiLang] && typeof pack[uiLang] === "object" ? pack[uiLang] : {}) || {};
  const en = (pack && pack.en && typeof pack.en === "object" ? pack.en : {}) || {};
  const v = (k in cur ? cur[k] : undefined) ?? (k in en ? en[k] : undefined);
  if (typeof v === "string") return v;
  return k;
}

function applyUiLang() {
  document.documentElement.lang = uiLang;
  document.documentElement.dir = isRtlUiLang(uiLang) ? "rtl" : "ltr";

  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (!key) return;
    el.textContent = t(key);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (!key) return;
    el.setAttribute("placeholder", t(key));
  });
  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
    const key = el.getAttribute("data-i18n-title");
    if (!key) return;
    el.setAttribute("title", t(key));
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((el) => {
    const key = el.getAttribute("data-i18n-aria-label");
    if (!key) return;
    el.setAttribute("aria-label", t(key));
  });
}

function setUiLang(next, { persist } = {}) {
  const lang = normalizeUiLang(next);
  uiLang = lang;
  if (els.uiLang && els.uiLang.value !== lang) els.uiLang.value = lang;
  if (persist !== false) {
    try {
      localStorage.setItem(UI_LANG_STORAGE_KEY, lang);
    } catch {
      // ignore
    }
  }
  applyUiLang();
  updateThemeButtonLabel();
  updateLogFollowButtonLabel();
  renderProgram();
  renderActionsList();
}

function loadUiLangFromStorage() {
  try {
    return normalizeUiLang(localStorage.getItem(UI_LANG_STORAGE_KEY));
  } catch {
    return "en";
  }
}

const BLOCK_META = {
  plan: { title: "Plan", label_key: "ui.block.plan", cls: "block--plan" },
  work: { title: "Work", label_key: "ui.block.work", cls: "block--work" },
  debug: { title: "Debug", label_key: "ui.block.debug", cls: "block--debug" },
  fix: { title: "Fix", label_key: "ui.block.fix", cls: "block--fix" },
  summary: { title: "Summary", label_key: "ui.block.summary", cls: "block--summary" },
  update_readme: { title: "Update README", label_key: "ui.block.update_readme", cls: "block--summary" },
  commit_push: { title: "Commit+Push", label_key: "ui.block.commit_push", cls: "block--release" },
  metatasks_generator: { title: "Meta Tasks", label_key: "ui.block.metatasks_generator", cls: "block--loop" },
  for_n_round: { title: "For N_ROUND", label_key: "ui.block.for_n_round", cls: "block--loop" },
  for_each_task: { title: "For each task", label_key: "ui.block.for_each_task", cls: "block--loop" },
  if_else: { title: "If/Else", label_key: "ui.block.if_else", cls: "block--loop" },
  while_loop: { title: "While", label_key: "ui.block.while_loop", cls: "block--loop" },
  wait_input: { title: "Wait Input", label_key: "ui.block.wait_input", cls: "block--input" },
};

let program = [];

const CONTAINER_BLOCK_TYPES = new Set(["metatasks_generator", "for_n_round", "for_each_task", "if_else"]);
const ACTION_BINDABLE_BLOCK_TYPES = new Set(["plan", "work", "debug", "fix", "summary", "commit_push"]);

function isContainerBlockType(type) {
  return CONTAINER_BLOCK_TYPES.has(String(type || ""));
}

function isActionBindableBlockType(type) {
  return ACTION_BINDABLE_BLOCK_TYPES.has(String(type || ""));
}

function defaultMetaRoundProgram() {
  const nRound = 2;
  return [
    {
      type: "metatasks_generator",
      n_round: nRound,
      task_list_path: "references/meta_round/tasks_v0.json",
      children: [
        { type: "for_n_round", n_round: nRound, body: [{ type: "plan" }, { type: "plan" }] },
        {
          type: "for_each_task",
          body: [
            { type: "plan" },
            { type: "work" },
            { type: "debug" },
            { type: "if_else", condition: "on_debug_failure", if_body: [{ type: "fix" }], else_body: [] },
            { type: "summary" },
            { type: "commit_push" },
          ],
        },
      ],
    },
  ];
}

function makeBlockFromType(type) {
  const tpe = String(type || "");
  if (tpe === "metatasks_generator") {
    // Default nested two-loop template.
    return defaultMetaRoundProgram()[0];
  }
  if (tpe === "for_n_round") {
    const nRound = 2;
    return { type: "for_n_round", n_round: nRound, body: [{ type: "plan" }, { type: "plan" }] };
  }
  if (tpe === "for_each_task") {
    return {
      type: "for_each_task",
      body: [
        { type: "plan" },
        { type: "work" },
        { type: "debug" },
        { type: "if_else", condition: "on_debug_failure", if_body: [{ type: "fix" }], else_body: [] },
        { type: "summary" },
        { type: "commit_push" },
      ],
    };
  }
  if (tpe === "if_else") {
    return { type: "if_else", condition: "on_debug_failure", if_body: [{ type: "fix" }], else_body: [] };
  }
  return { type: tpe };
}

function flattenLeafBlocks(blocks) {
  const out = [];
  const visit = (b) => {
    const obj = b && typeof b === "object" ? b : {};
    const tpe = String(obj.type || "");
    if (!tpe) return;
    if (!isContainerBlockType(tpe)) {
      out.push(obj);
      return;
    }
    if (tpe === "metatasks_generator") {
      const children = Array.isArray(obj.children) ? obj.children : [];
      children.forEach(visit);
      return;
    }
    if (tpe === "for_n_round" || tpe === "for_each_task") {
      const body = Array.isArray(obj.body) ? obj.body : [];
      body.forEach(visit);
      return;
    }
    if (tpe === "if_else") {
      const ifBody = Array.isArray(obj.if_body) ? obj.if_body : [];
      const elseBody = Array.isArray(obj.else_body) ? obj.else_body : [];
      ifBody.forEach(visit);
      elseBody.forEach(visit);
      return;
    }
  };
  (Array.isArray(blocks) ? blocks : []).forEach(visit);
  return out;
}

function countLeafBlocks(blocks) {
  return flattenLeafBlocks(blocks).length;
}

const LOG_WINDOW_LIMIT = 400;
const LOG_RESET_LIMIT = 2000;
const logSince = { pipeline: 0, backend: 0 };
const logInitialized = { pipeline: false, backend: false };
let logFollow = true;

let actionsIndex = [];
let selectedActionId = null;
let selectedAction = null;
let actionsMode = "view"; // "view" | "new"
let actionsLoadedOnce = false;

let workspaceSlug = "";
let workspaceConfig = null;

const BUILTIN_ACTION_ID_TO_STEP_TYPE = {
  // backend/builtin_actions.py (keep within JS safe integer range)
  9000000001: "plan",
  9000000002: "work",
  9000000003: "debug",
  9000000004: "fix",
  9000000005: "summary",
  9000000006: "commit_push",
};

function defaultStepTypeForActionId(actionId) {
  const id = Number(actionId);
  if (!Number.isFinite(id)) return "work";
  const mapped = BUILTIN_ACTION_ID_TO_STEP_TYPE[id];
  return typeof mapped === "string" && mapped ? mapped : "work";
}

function updateThemeButtonLabel() {
  if (!els.themeBtn) return;
  const cur = String(document.body.dataset.theme || "light");
  els.themeBtn.textContent = cur === "dark" ? t("ui.theme.dark") : t("ui.theme.light");
}

function setTheme(next) {
  document.body.dataset.theme = next;
  updateThemeButtonLabel();
  localStorage.setItem("autoappdev_theme", next);
}

function parseWorkspaceSlug(raw) {
  const ws = String(raw || "").trim();
  if (!ws) return { ok: false, error: "workspace is required" };
  if (ws === "." || ws === "..") return { ok: false, error: "workspace must not be '.' or '..'" };
  if (ws.includes("/") || ws.includes("\\")) return { ok: false, error: "workspace must be a single path segment" };
  if (ws.length > 100) return { ok: false, error: "workspace is too long" };
  if (/[\x00-\x1f]/.test(ws)) return { ok: false, error: "workspace contains control characters" };
  return { ok: true, workspace: ws };
}

function normalizeActionRef(ref) {
  if (!ref || typeof ref !== "object") return null;
  if ("id" in ref) {
    const raw = ref.id;
    const n =
      typeof raw === "number" && Number.isFinite(raw)
        ? raw
        : typeof raw === "string" && /^[0-9]+$/.test(raw.trim())
          ? Number(raw.trim())
          : NaN;
    const id = Number.isFinite(n) ? Math.trunc(n) : NaN;
    if (!Number.isFinite(id) || id <= 0) return null;
    return { id };
  }
  if ("slug" in ref) {
    const s = typeof ref.slug === "string" ? ref.slug.trim() : "";
    if (!s) return null;
    if (s.length > 200) return null;
    if (/[\x00-\x1f]/.test(s)) return null;
    return { slug: s };
  }
  return null;
}

function actionRefValue(ref) {
  const r = normalizeActionRef(ref);
  if (!r) return "";
  if (typeof r.id === "number") return String(r.id);
  return String(r.slug || "");
}

function lookupActionTitleById(id) {
  const n = Number(id);
  if (!Number.isFinite(n)) return "";
  const items = Array.isArray(actionsIndex) ? actionsIndex : [];
  const it = items.find((a) => a && typeof a === "object" && a.id === n);
  const title = it && typeof it.title === "string" ? it.title.trim() : "";
  return title || "";
}

function updateReadmeTargetPath(workspace) {
  const ws = String(workspace || "").trim();
  return ws ? `auto-apps/${ws}/README.md` : "auto-apps/<workspace>/README.md";
}

function defaultUpdateReadmeBlockMarkdown({ workspace } = {}) {
  const ws = String(workspace || "").trim();
  const lines = [];
  lines.push("## Workspace Status (Auto-Updated)");
  lines.push("");
  lines.push("- Updated: <utc-iso-timestamp>");
  if (ws) lines.push(`- Workspace: ${ws}`);
  lines.push("");
  lines.push("This section is updated by AutoAppDev.");
  lines.push("Do not edit content between the markers.");
  lines.push("");
  lines.push("## Philosophy");
  lines.push("AutoAppDev treats agents as tools and keeps work stable via a strict, resumable loop:");
  lines.push("1. Plan");
  lines.push("2. Implement");
  lines.push("3. Debug/verify (with timeouts)");
  lines.push("4. Fix");
  lines.push("5. Summarize + log");
  lines.push("6. Commit + push (if used by the workflow)");
  return lines.join("\n") + "\n";
}

function canonicalBlockTitle(type, idx) {
  const tpe = String(type || "");
  const meta = BLOCK_META[tpe] || null;
  const title = meta && typeof meta.title === "string" ? meta.title.trim() : "";
  return title || tpe || `Step ${idx + 1}`;
}

function uiBlockTitle(type, idx) {
  const tpe = String(type || "");
  const meta = BLOCK_META[tpe] || null;
  const key = meta && typeof meta.label_key === "string" ? meta.label_key : "";
  const fallback = canonicalBlockTitle(tpe, idx);
  if (!key) return fallback;
  const v = t(key);
  return v === key ? fallback : v;
}

function formatProgramBlockLabel(block, idx) {
  const b = block && typeof block === "object" ? block : {};
  const type = String(b.type || "");
  if (type === "update_readme") {
    const ws = String(b.workspace || "").trim();
    const base = uiBlockTitle(type, idx);
    return `${base} (${updateReadmeTargetPath(ws)})`;
  }
  if (type === "metatasks_generator") {
    const base = uiBlockTitle(type, idx);
    const n = Number.parseInt(String(b.n_round || ""), 10);
    const nRound = Number.isFinite(n) && n > 0 ? Math.trunc(n) : null;
    const taskListPath = String(b.task_list_path || "").trim();
    const parts = [];
    if (nRound) parts.push(`N_ROUND=${nRound}`);
    if (taskListPath) parts.push(taskListPath);
    return parts.length ? `${base} (${parts.join(", ")})` : base;
  }
  if (type === "for_n_round") {
    const base = uiBlockTitle(type, idx);
    const n = Number.parseInt(String(b.n_round || ""), 10);
    const nRound = Number.isFinite(n) && n > 0 ? Math.trunc(n) : null;
    return nRound ? `${base} (N_ROUND=${nRound})` : base;
  }
  if (type === "if_else") {
    const base = uiBlockTitle(type, idx);
    const cond = String(b.condition || "").trim();
    return cond ? `${base} (${cond})` : base;
  }
  const base = uiBlockTitle(type, idx);
  const ref = normalizeActionRef(b.action_ref);
  if (!ref) return base;
  if (typeof ref.id === "number") {
    const title = lookupActionTitleById(ref.id);
    return title ? `${base} -> #${ref.id} ${title}` : `${base} -> #${ref.id}`;
  }
  return `${base} -> slug: ${String(ref.slug)}`;
}

function clampInt(n, min, max) {
  if (!Number.isFinite(n)) return min;
  const v = Math.trunc(n);
  if (v < min) return min;
  if (v > max) return max;
  return v;
}

function normalizeTaskListPath(raw) {
  const s = String(raw || "").trim();
  if (!s) return { ok: false, error: "task list path is required" };
  if (s.length > 400) return { ok: false, error: "task list path is too long" };
  if (/[\x00-\x1f]/.test(s)) return { ok: false, error: "task list path contains control characters" };
  return { ok: true, path: s };
}

function ensureForNRoundBody(loop, nRound) {
  const obj = loop && typeof loop === "object" ? loop : null;
  if (!obj) return;
  if (!Array.isArray(obj.body)) obj.body = [];
  const body = obj.body;
  if (body.length > nRound) body.splice(nRound);
  while (body.length < nRound) body.push({ type: "plan" });
}

function ensureMetaRoundChildren(meta) {
  const obj = meta && typeof meta === "object" ? meta : null;
  if (!obj) return { roundLoop: null, eachLoop: null };
  if (!Array.isArray(obj.children)) obj.children = [];
  const children = obj.children;

  let roundLoop = children.find((c) => c && typeof c === "object" && String(c.type || "") === "for_n_round") || null;
  if (!roundLoop) {
    roundLoop = { type: "for_n_round", n_round: 2, body: [{ type: "plan" }, { type: "plan" }] };
    children.unshift(roundLoop);
  }

  let eachLoop = children.find((c) => c && typeof c === "object" && String(c.type || "") === "for_each_task") || null;
  if (!eachLoop) {
    eachLoop = makeBlockFromType("for_each_task");
    children.push(eachLoop);
  }

  return { roundLoop, eachLoop };
}

function editUpdateReadmeBlock(block) {
  const obj = block && typeof block === "object" ? block : null;
  if (!obj) return;
  const curWs = String(obj.workspace || "").trim() || String(workspaceSlug || "my_workspace");
  const raw = window.prompt(t("ui.prompt.workspace_slug_for_readme"), curWs);
  if (raw === null) return;
  const parsed = parseWorkspaceSlug(raw);
  if (!parsed.ok) {
    window.alert(`${t("ui.alert.invalid_workspace")}: ${parsed.error}`);
    return;
  }
  obj.workspace = parsed.workspace;
  persistProgram();
  renderProgram();
}

function editMetaTasksGeneratorBlock(block) {
  const obj = block && typeof block === "object" ? block : null;
  if (!obj) return;

  const curN = Number.parseInt(String(obj.n_round || ""), 10);
  const defaultN = Number.isFinite(curN) && curN > 0 ? Math.trunc(curN) : 2;
  const rawN = window.prompt(t("ui.prompt.n_round"), String(defaultN));
  if (rawN === null) return;
  const parsedN = Number.parseInt(String(rawN || "").trim(), 10);
  if (!Number.isFinite(parsedN)) {
    window.alert("Invalid N_ROUND");
    return;
  }
  const nRound = clampInt(parsedN, 1, 10);

  const defaultPath = String(obj.task_list_path || "").trim() || "references/meta_round/tasks_v0.json";
  const rawPath = window.prompt(t("ui.prompt.task_list_path"), defaultPath);
  if (rawPath === null) return;
  const parsedPath = normalizeTaskListPath(rawPath);
  if (!parsedPath.ok) {
    window.alert(`Invalid task list path: ${parsedPath.error}`);
    return;
  }

  obj.n_round = nRound;
  obj.task_list_path = parsedPath.path;

  const { roundLoop } = ensureMetaRoundChildren(obj);
  if (roundLoop && typeof roundLoop === "object") {
    roundLoop.n_round = nRound;
    ensureForNRoundBody(roundLoop, nRound);
  }

  persistProgram();
  renderProgram();
}

function editForNRoundBlock(block, { parent } = {}) {
  const obj = block && typeof block === "object" ? block : null;
  if (!obj) return;

  const curN = Number.parseInt(String(obj.n_round || ""), 10);
  const defaultN = Number.isFinite(curN) && curN > 0 ? Math.trunc(curN) : 2;
  const rawN = window.prompt(t("ui.prompt.n_round"), String(defaultN));
  if (rawN === null) return;
  const parsedN = Number.parseInt(String(rawN || "").trim(), 10);
  if (!Number.isFinite(parsedN)) {
    window.alert("Invalid N_ROUND");
    return;
  }
  const nRound = clampInt(parsedN, 1, 10);
  obj.n_round = nRound;
  ensureForNRoundBody(obj, nRound);

  if (parent && typeof parent === "object" && String(parent.type || "") === "metatasks_generator") {
    parent.n_round = nRound;
  }

  persistProgram();
  renderProgram();
}

function editIfElseBlock(block) {
  const obj = block && typeof block === "object" ? block : null;
  if (!obj) return;
  const cur = String(obj.condition || "").trim() || "on_debug_failure";
  const raw = window.prompt(t("ui.prompt.if_condition"), cur);
  if (raw === null) return;
  const cond = String(raw || "").trim() || "on_debug_failure";
  if (cond !== "on_debug_failure") {
    window.alert("v0 supports only condition: on_debug_failure");
    return;
  }
  obj.condition = cond;
  persistProgram();
  renderProgram();
}

function renderProgram() {
  els.canvas.querySelectorAll(".program").forEach((n) => n.remove());
  if (!program.length) {
    els.canvasEmpty.hidden = false;
    els.export.hidden = true;
    return;
  }
  els.canvasEmpty.hidden = true;

  const wrap = document.createElement("div");
  wrap.className = "program";
  const INDENT_PX = 18;

  const renderBlocks = (list, depth, parentType, parentObj) => {
    const blocks = Array.isArray(list) ? list : [];
    blocks.forEach((b, idx) => {
      const obj = b && typeof b === "object" ? b : {};
      const type = String(obj.type || "");
      const meta = BLOCK_META[type] || { title: type, cls: "block--work" };
      const row = document.createElement("div");
      row.className = `prog-block ${meta.cls}`;
      if (depth > 0) {
        const dx = depth * INDENT_PX;
        row.style.marginLeft = `${dx}px`;
        row.style.width = `calc(100% - ${dx}px)`;
      }
      const label = document.createElement("div");
      label.className = "prog-label";
      const prefix = parentType === "for_n_round" ? `Round ${idx + 1}: ` : "";
      label.textContent = prefix + formatProgramBlockLabel(obj, idx);
      row.appendChild(label);

      if (type === "update_readme" || type === "metatasks_generator" || type === "for_n_round" || type === "if_else") {
        const edit = document.createElement("button");
        edit.className = "prog-bind";
        edit.type = "button";
        edit.textContent = t("ui.btn.edit");
        edit.addEventListener("click", () => {
          if (type === "update_readme") editUpdateReadmeBlock(obj);
          else if (type === "metatasks_generator") editMetaTasksGeneratorBlock(obj);
          else if (type === "for_n_round") editForNRoundBlock(obj, { parent: parentObj });
          else if (type === "if_else") editIfElseBlock(obj);
        });
        row.appendChild(edit);
      }

      if (isActionBindableBlockType(type)) {
        const bind = document.createElement("button");
        bind.className = "prog-bind";
        bind.type = "button";
        bind.textContent = t("ui.btn.bind");
        bind.addEventListener("click", () => {
          const cur = obj && typeof obj === "object" ? obj : {};
          const curRef = normalizeActionRef(cur.action_ref);
          const raw = window.prompt(t("ui.prompt.action_ref"), actionRefValue(curRef));
          if (raw === null) return;
          const s = String(raw || "").trim();
          if (!s) {
            if (cur && typeof cur === "object") delete cur.action_ref;
            persistProgram();
            renderProgram();
            return;
          }
          if (/^[0-9]+$/.test(s)) {
            const id = Number(s);
            if (Number.isFinite(id) && id > 0) {
              cur.action_ref = { id: Math.trunc(id) };
            } else {
              window.alert(t("ui.alert.invalid_id"));
              return;
            }
          } else {
            if (s.length > 200 || /[\x00-\x1f]/.test(s)) {
              window.alert(t("ui.alert.invalid_slug"));
              return;
            }
            cur.action_ref = { slug: s };
          }
          persistProgram();
          renderProgram();
        });
        row.appendChild(bind);
      }

      const rm = document.createElement("button");
      rm.className = "prog-remove";
      rm.type = "button";
      rm.textContent = "×";
      rm.addEventListener("click", () => {
        blocks.splice(idx, 1);
        persistProgram();
        renderProgram();
      });
      row.appendChild(rm);
      wrap.appendChild(row);

      if (type === "metatasks_generator") {
        renderBlocks(obj.children, depth + 1, type, obj);
      } else if (type === "for_n_round" || type === "for_each_task") {
        renderBlocks(obj.body, depth + 1, type, obj);
      } else if (type === "if_else") {
        renderBlocks(obj.if_body, depth + 1, type, obj);
        if (Array.isArray(obj.else_body) && obj.else_body.length) renderBlocks(obj.else_body, depth + 1, type, obj);
      }
    });
  };

  renderBlocks(program, 0, "", null);
  els.canvas.appendChild(wrap);
}

function persistProgram() {
  localStorage.setItem("autoappdev_program", JSON.stringify(program));
}

function loadProgram() {
  try {
    const raw = localStorage.getItem("autoappdev_program");
    if (!raw) {
      program = defaultMetaRoundProgram();
      try {
        persistProgram();
      } catch {}
      return;
    }
    const p = JSON.parse(raw);
    if (Array.isArray(p)) program = p;
  } catch {}
}

async function api(path, opts = {}) {
  if (!window.AutoAppDevApi || typeof window.AutoAppDevApi.requestJson !== "function") {
    throw new Error("api_client_not_loaded");
  }
  return await window.AutoAppDevApi.requestJson(path, opts);
}

function canSelectValue(selectEl, value) {
  if (!selectEl || !value) return false;
  const opt = Array.from(selectEl.options || []).find((o) => o.value === value);
  return Boolean(opt && !opt.disabled);
}

async function loadSettings() {
  if (!els.agentSelect || !els.modelSelect) return;
  try {
    const data = await api("/api/config");
    const cfg = data.config || {};
    const agent = typeof cfg.agent === "string" ? cfg.agent : "";
    const model = typeof cfg.model === "string" ? cfg.model : "";
    if (canSelectValue(els.agentSelect, agent)) els.agentSelect.value = agent;
    if (canSelectValue(els.modelSelect, model)) els.modelSelect.value = model;
  } catch (e) {
    console.warn("load settings failed", e);
  }
}

async function saveSettings() {
  if (!els.agentSelect || !els.modelSelect) return;
  const agent = String(els.agentSelect.value || "");
  const model = String(els.modelSelect.value || "");
  try {
    await api("/api/config", { method: "POST", body: JSON.stringify({ agent, model }) });
  } catch (e) {
    console.warn("save settings failed", e);
  }
}

function programToPlan(prog) {
  const steps = flattenLeafBlocks(Array.isArray(prog) ? prog : []).map((b, idx) => ({
    id: idx + 1,
    block: (() => {
      const type = b && typeof b === "object" ? String(b.type || "") : "";
      return type === "update_readme" ? "summary" : type;
    })(),
  }));
  return { kind: "autoappdev_plan", version: 1, steps };
}

function programToIr(prog, title = "Program") {
  const blocks = Array.isArray(prog) ? prog : [];
  const titleStr = String(title || "Program");
  const wsMeta = workspaceTaskMeta();

  const leafBlockToIrStep = (block, idx, { id, title, meta } = {}) => {
    const b = block && typeof block === "object" ? block : {};
    const type = String(b.type || "");
    const stepTitle = String(title || "").trim() || canonicalBlockTitle(type, idx);
    let stepBlock = type;
    let actions = [{ id: "a1", kind: "noop", params: {} }];
    if (type === "update_readme") {
      stepBlock = "summary";
      const ws = String((b && b.workspace) || "").trim();
      actions = [
        {
          id: "a1",
          kind: "update_readme",
          params: {
            workspace: ws,
            block_markdown: defaultUpdateReadmeBlockMarkdown({ workspace: ws }),
          },
        },
      ];
    } else {
      const ref = normalizeActionRef(b && b.action_ref);
      if (ref) actions[0].meta = { action_ref: ref };
    }
    const out = {
      id: String(id || `s${idx + 1}`),
      title: stepTitle,
      block: stepBlock,
      actions,
    };
    if (meta && typeof meta === "object" && Object.keys(meta).length) out.meta = meta;
    return out;
  };

  const programToMetaRoundIr = (root) => {
    const r = root && typeof root === "object" ? root : {};
    const children = Array.isArray(r.children) ? r.children : [];
    const roundLoop = children.find((c) => c && typeof c === "object" && String(c.type || "") === "for_n_round") || null;
    const eachLoop = children.find((c) => c && typeof c === "object" && String(c.type || "") === "for_each_task") || null;

    const roundBodyRaw = roundLoop && Array.isArray(roundLoop.body) ? roundLoop.body : [];
    const roundLeaf = flattenLeafBlocks(roundBodyRaw);
    const nCfg = Number.parseInt(String((roundLoop && roundLoop.n_round) || r.n_round || ""), 10);
    const nRound = roundLeaf.length || (Number.isFinite(nCfg) && nCfg > 0 ? Math.trunc(nCfg) : 2);

    const taskListPath = String(r.task_list_path || "").trim() || "references/meta_round/tasks_v0.json";

    const controllerSteps = [];
    for (let i = 0; i < nRound; i++) {
      const leaf = roundLeaf[i] || { type: "plan" };
      const leafType = leaf && typeof leaf === "object" ? String(leaf.type || "") : "";
      controllerSteps.push(
        leafBlockToIrStep(leaf, i, {
          id: `r${i + 1}`,
          title: `Round ${i + 1}: ${canonicalBlockTitle(leafType, i)}`,
          meta: { round: i + 1 },
        })
      );
    }

    const templateSteps = [];
    const eachBody = eachLoop && Array.isArray(eachLoop.body) ? eachLoop.body : [];
    eachBody.forEach((node) => {
      const obj = node && typeof node === "object" ? node : {};
      const tpe = String(obj.type || "");
      if (tpe === "if_else") {
        const cond = String(obj.condition || "on_debug_failure").trim() || "on_debug_failure";
        const ifBody = Array.isArray(obj.if_body) ? obj.if_body : [];
        const ifLeaf = flattenLeafBlocks(ifBody);
        const fixLeaf =
          ifLeaf.find((b) => b && typeof b === "object" && String(b.type || "") === "fix") || ifLeaf[0] || { type: "fix" };
        templateSteps.push(
          leafBlockToIrStep(fixLeaf, templateSteps.length, {
            id: `s${templateSteps.length + 1}`,
            title: "Fix (if needed)",
            meta: { conditional: cond },
          })
        );
        return;
      }
      if (isContainerBlockType(tpe)) {
        // v0: lossy flattening for nested containers inside the template body.
        const leaves = flattenLeafBlocks([obj]);
        leaves.forEach((leaf) => {
          templateSteps.push(
            leafBlockToIrStep(leaf, templateSteps.length, { id: `s${templateSteps.length + 1}` })
          );
        });
        return;
      }
      templateSteps.push(leafBlockToIrStep(obj, templateSteps.length, { id: `s${templateSteps.length + 1}` }));
    });

    const controllerMeta = Object.assign({}, wsMeta || {}, {
      meta_round_v0: { n_round: nRound, task_list_path: taskListPath },
    });
    const controllerTask = {
      id: "meta",
      title: `Meta-round controller: ${titleStr}`,
      steps: controllerSteps,
      meta: controllerMeta,
    };

    const templateMeta = Object.assign({}, wsMeta || {}, { task_template_v0: true });
    const templateTask = { id: "template", title: `Task template: ${titleStr}`, steps: templateSteps, meta: templateMeta };

    return { kind: "autoappdev_ir", version: 1, tasks: [controllerTask, templateTask] };
  };

  if (blocks.length === 1 && blocks[0] && typeof blocks[0] === "object" && String(blocks[0].type || "") === "metatasks_generator") {
    return programToMetaRoundIr(blocks[0]);
  }

  const leaf = flattenLeafBlocks(blocks);
  const steps = leaf.map((b, idx) => leafBlockToIrStep(b, idx, { id: `s${idx + 1}` }));
  const task = { id: "t1", title: titleStr, steps };
  if (wsMeta) task.meta = wsMeta;
  return { kind: "autoappdev_ir", version: 1, tasks: [task] };
}

function programToAapsScript(prog, title = "Program") {
  const ir = programToIr(prog, title);
  return irToAapsText(ir);
}

function irToAapsText(ir) {
  const tasks = ir && typeof ir === "object" && Array.isArray(ir.tasks) ? ir.tasks : [];
  const lines = [];
  lines.push("AUTOAPPDEV_PIPELINE 1");
  lines.push("");
  tasks.forEach((t, tIdx) => {
    const taskNo = tIdx + 1;
    const taskObj = t && typeof t === "object" ? t : {};
    const meta = taskObj.meta && typeof taskObj.meta === "object" && !Array.isArray(taskObj.meta) ? taskObj.meta : null;
    const outTask = { id: String(taskObj.id || `t${taskNo}`), title: String(taskObj.title || `Task ${taskNo}`) };
    if (meta && Object.keys(meta).length) outTask.meta = meta;
    lines.push(`# ${taskNo} Task`);
    lines.push(`TASK  ${JSON.stringify(outTask)}`);
    lines.push("");

    const steps = Array.isArray(taskObj.steps) ? taskObj.steps : [];
    steps.forEach((st, sIdx) => {
      const stepNo = sIdx + 1;
      const stepObj = st && typeof st === "object" ? st : {};
      const stepMeta = stepObj.meta && typeof stepObj.meta === "object" && !Array.isArray(stepObj.meta) ? stepObj.meta : null;
      const outStep = {
        id: String(stepObj.id || `s${stepNo}`),
        title: String(stepObj.title || `Step ${stepNo}`),
        block: String(stepObj.block || "plan"),
      };
      if (stepMeta && Object.keys(stepMeta).length) outStep.meta = stepMeta;
      lines.push(`# ${taskNo}.${stepNo} Step`);
      lines.push(`  STEP  ${JSON.stringify(outStep)}`);

      const actions = Array.isArray(stepObj.actions) ? stepObj.actions : [];
      actions.forEach((a, aIdx) => {
        const actionNo = aIdx + 1;
        const act = a && typeof a === "object" ? a : {};
        const params = act.params && typeof act.params === "object" && !Array.isArray(act.params) ? act.params : null;
        const aMeta = act.meta && typeof act.meta === "object" && !Array.isArray(act.meta) ? act.meta : null;
        const outAction = { id: String(act.id || `a${actionNo}`), kind: String(act.kind || "noop") };
        if (params) outAction.params = params;
        if (aMeta && Object.keys(aMeta).length) outAction.meta = aMeta;
        lines.push(`# ${taskNo}.${stepNo}.${actionNo} Action`);
        lines.push(`    ACTION ${JSON.stringify(outAction)}`);
      });
      lines.push("");
    });
  });
  return lines.join("\n").trimEnd() + "\n";
}

function irToProgram(ir) {
  if (!ir || typeof ir !== "object") return null;
  const tasks = Array.isArray(ir.tasks) ? ir.tasks : [];

  const isObj = (o) => Boolean(o && typeof o === "object" && !Array.isArray(o));
  const isMetaRoundTask = (t) => {
    if (!t || typeof t !== "object") return false;
    const meta = isObj(t.meta) ? t.meta : null;
    return Boolean(meta && isObj(meta.meta_round_v0));
  };
  const isTemplateTask = (t) => {
    if (!t || typeof t !== "object") return false;
    const meta = isObj(t.meta) ? t.meta : null;
    return Boolean(meta && meta.task_template_v0 === true);
  };

  const controller = tasks.find(isMetaRoundTask) || null;
  const template = tasks.find(isTemplateTask) || null;

  const irStepToLeafBlock = (st) => {
    if (!st || typeof st !== "object") return null;
    const actions = Array.isArray(st.actions) ? st.actions : [];
    const upd = actions.find((a) => a && typeof a === "object" && a.kind === "update_readme");
    const params = upd && typeof upd === "object" ? upd.params : null;
    const ws = params && typeof params === "object" ? String(params.workspace || "").trim() : "";
    if (ws) return { type: "update_readme", workspace: ws };

    let ref = null;
    actions.forEach((a) => {
      if (ref) return;
      if (!a || typeof a !== "object") return;
      const meta = a.meta && typeof a.meta === "object" ? a.meta : null;
      if (!meta) return;
      const ar = meta.action_ref;
      const norm = normalizeActionRef(ar);
      if (norm) ref = norm;
    });

    if (typeof st.block !== "string" || !st.block.trim()) return null;
    const obj = { type: st.block.trim() };
    if (ref) obj.action_ref = ref;
    return obj;
  };

  if (controller && template) {
    const meta = controller.meta && typeof controller.meta === "object" ? controller.meta : {};
    const mr = meta && typeof meta.meta_round_v0 === "object" ? meta.meta_round_v0 : {};
    const nCfg = Number.parseInt(String(mr.n_round || ""), 10);
    const nRound = Number.isFinite(nCfg) && nCfg > 0 ? Math.trunc(nCfg) : 2;
    const taskListPath = String(mr.task_list_path || "").trim() || "references/meta_round/tasks_v0.json";

    const controllerSteps = Array.isArray(controller.steps) ? controller.steps : [];
    const roundBody = controllerSteps.map(irStepToLeafBlock).filter(Boolean);
    const forNRound = { type: "for_n_round", n_round: nRound, body: roundBody };

    const templateSteps = Array.isArray(template.steps) ? template.steps : [];
    const eachBody = [];
    templateSteps.forEach((st) => {
      const step = st && typeof st === "object" ? st : {};
      const stMeta = step.meta && typeof step.meta === "object" ? step.meta : null;
      const cond = stMeta && typeof stMeta.conditional === "string" ? stMeta.conditional : "";
      if (cond === "on_debug_failure" && String(step.block || "") === "fix") {
        const fixLeaf = irStepToLeafBlock(step) || { type: "fix" };
        eachBody.push({ type: "if_else", condition: cond, if_body: [fixLeaf], else_body: [] });
        return;
      }
      const leaf = irStepToLeafBlock(step);
      if (leaf) eachBody.push(leaf);
    });
    const forEach = { type: "for_each_task", body: eachBody };

    return [{ type: "metatasks_generator", n_round: nRound, task_list_path: taskListPath, children: [forNRound, forEach] }];
  }

  const steps = [];
  tasks.forEach((t) => {
    const s = t && Array.isArray(t.steps) ? t.steps : [];
    s.forEach((st) => {
      const leaf = irStepToLeafBlock(st);
      if (leaf) steps.push(leaf);
    });
  });
  return steps;
}

async function saveScript() {
  if (!program.length) {
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ ok: false, error: "empty_program" }, null, 2);
    return;
  }
  const titleRaw = window.prompt(t("ui.prompt.script_title"), "Program");
  if (titleRaw === null) return;
  const title = String(titleRaw).trim() || "Program";
  const script_text = programToAapsScript(program, title);
  const ir = programToIr(program, title);
  try {
    const res = await api("/api/scripts", {
      method: "POST",
      body: JSON.stringify({ title, script_text, script_version: 1, script_format: "aaps", ir }),
    });
    els.export.hidden = false;
    els.export.textContent = JSON.stringify(res, null, 2);
  } catch (e) {
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ ok: false, error: e.message || String(e) }, null, 2);
  }
}

async function loadScript() {
  const raw = window.prompt(t("ui.prompt.load_script_id"), "");
  if (raw === null) return;
  const id = String(raw).trim();
  if (!id) return;
  try {
    const res = await api(`/api/scripts/${encodeURIComponent(id)}`);
    els.export.hidden = false;
    els.export.textContent = JSON.stringify(res, null, 2);
    const script = res.script || {};
    const nextProgram = irToProgram(script.ir);
    if (Array.isArray(nextProgram) && nextProgram.length) {
      program = nextProgram;
      persistProgram();
      renderProgram();
    }
  } catch (e) {
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ ok: false, error: e.message || String(e) }, null, 2);
  }
}

function setScriptMsg(text, { error } = {}) {
  if (!els.scriptMsg) return;
  const msg = String(text || "");
  els.scriptMsg.textContent = msg;
  els.scriptMsg.classList.toggle("is-error", Boolean(error) && Boolean(msg));
}

function applyIrToCanvas(ir) {
  const nextProgram = irToProgram(ir);
  if (!Array.isArray(nextProgram)) return { ok: false, error: "invalid_ir" };
  program = nextProgram;
  persistProgram();
  renderProgram();
  return { ok: true, steps: countLeafBlocks(nextProgram) };
}

function formatScriptApiError(e) {
  const data = e && e.data && typeof e.data === "object" ? e.data : {};
  const line = typeof data.line === "number" ? data.line : null;
  const code = typeof data.error === "string" ? data.error : "";
  const detail = typeof data.detail === "string" ? data.detail : "";
  const msg = detail || code || (e && e.message) || String(e);
  return line ? `line ${line}: ${msg}` : msg;
}

function setActionsMsg(text, { error } = {}) {
  if (!els.actionsMsg) return;
  const msg = String(text || "");
  els.actionsMsg.textContent = msg;
  els.actionsMsg.classList.toggle("is-error", Boolean(error) && Boolean(msg));
}

function formatActionApiError(e) {
  const data = e && e.data && typeof e.data === "object" ? e.data : {};
  const code = typeof data.error === "string" ? data.error : "";
  const detail = typeof data.detail === "string" ? data.detail : "";
  return detail || code || (e && e.message) || String(e);
}

function setWsMsg(text, { error } = {}) {
  if (!els.wsMsg) return;
  const msg = String(text || "");
  els.wsMsg.textContent = msg;
  els.wsMsg.classList.toggle("is-error", Boolean(error) && Boolean(msg));
}

function loadWorkspaceSlugFromStorage() {
  try {
    return String(localStorage.getItem("autoappdev_workspace") || "").trim();
  } catch {
    return "";
  }
}

function saveWorkspaceSlugToStorage(slug) {
  try {
    localStorage.setItem("autoappdev_workspace", String(slug || "").trim());
  } catch {
    // ignore
  }
}

function parseMaterialsPaths(raw) {
  const txt = String(raw || "");
  const parts = txt
    .split(/[\n,]+/g)
    .map((s) => String(s || "").trim())
    .filter(Boolean);
  const uniq = [];
  parts.forEach((p) => {
    if (!uniq.includes(p)) uniq.push(p);
  });
  return uniq.length ? uniq : ["materials"];
}

function fillWorkspaceForm(cfg) {
  const c = cfg && typeof cfg === "object" ? cfg : {};
  const mats = Array.isArray(c.materials_paths) ? c.materials_paths.map((s) => String(s || "").trim()).filter(Boolean) : [];
  if (els.wsMaterials) els.wsMaterials.value = mats.length ? mats.join("\n") : "materials";
  if (els.wsLanguage) {
    const lang = typeof c.default_language === "string" ? c.default_language : "en";
    els.wsLanguage.value = lang;
  }
  if (els.wsContextText) els.wsContextText.value = typeof c.shared_context_text === "string" ? c.shared_context_text : "";
  if (els.wsContextPath) els.wsContextPath.value = typeof c.shared_context_path === "string" ? c.shared_context_path : "";
}

function buildWorkspacePayloadFromForm() {
  const materials_paths = parseMaterialsPaths(els.wsMaterials ? els.wsMaterials.value : "");
  const default_language = String((els.wsLanguage && els.wsLanguage.value) || "en").trim() || "en";
  const shared_context_text = String((els.wsContextText && els.wsContextText.value) || "");
  const shared_context_path = String((els.wsContextPath && els.wsContextPath.value) || "").trim();
  return { materials_paths, default_language, shared_context_text, shared_context_path };
}

function workspaceTaskMeta() {
  const ws = String(workspaceSlug || "").trim();
  if (!ws) return null;
  const cfg = workspaceConfig && typeof workspaceConfig === "object" ? workspaceConfig : null;
  return { workspace: ws, workspace_config: cfg || {} };
}

async function loadWorkspaceConfig(slugRaw) {
  const parsed = parseWorkspaceSlug(slugRaw);
  if (!parsed.ok) {
    setWsMsg(`Invalid workspace: ${parsed.error}`, { error: true });
    return;
  }
  const ws = parsed.workspace;
  if (els.wsSlug) els.wsSlug.value = ws;
  setWsMsg("loading...");
  try {
    const res = await api(`/api/workspaces/${encodeURIComponent(ws)}/config`);
    const cfg = res && typeof res.config === "object" && res.config ? res.config : {};
    workspaceSlug = ws;
    workspaceConfig = cfg;
    fillWorkspaceForm(cfg);
    saveWorkspaceSlugToStorage(ws);
    setWsMsg(res && res.exists ? "loaded" : "loaded defaults (not saved yet)");
  } catch (e) {
    setWsMsg(formatActionApiError(e), { error: true });
  }
}

async function saveWorkspaceConfig() {
  if (!els.wsSlug) return;
  const parsed = parseWorkspaceSlug(els.wsSlug.value);
  if (!parsed.ok) {
    setWsMsg(`Invalid workspace: ${parsed.error}`, { error: true });
    return;
  }
  const ws = parsed.workspace;
  const payload = buildWorkspacePayloadFromForm();
  setWsMsg("saving...");
  try {
    const res = await api(`/api/workspaces/${encodeURIComponent(ws)}/config`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    const cfg = res && typeof res.config === "object" && res.config ? res.config : payload;
    workspaceSlug = ws;
    workspaceConfig = cfg;
    fillWorkspaceForm(cfg);
    saveWorkspaceSlugToStorage(ws);
    setWsMsg("saved");
  } catch (e) {
    setWsMsg(formatActionApiError(e), { error: true });
  }
}

function normalizeActionKind(raw) {
  const k = String(raw || "").trim().toLowerCase();
  return k === "command" ? "command" : "prompt";
}

function setActionKindUi(kind, { editable } = {}) {
  const k = normalizeActionKind(kind);
  if (els.actionKind) {
    els.actionKind.value = k;
    els.actionKind.disabled = !Boolean(editable);
  }
  if (els.actionSectionPrompt) els.actionSectionPrompt.hidden = k !== "prompt";
  if (els.actionSectionCommand) els.actionSectionCommand.hidden = k !== "command";
}

function updateActionsButtons() {
  const hasExisting = actionsMode === "view" && selectedActionId !== null;
  const ro = Boolean(selectedAction && typeof selectedAction === "object" && selectedAction.readonly);
  if (els.actionsDelete) els.actionsDelete.disabled = !hasExisting || ro;
}

function clearActionForm() {
  if (els.actionId) els.actionId.value = "";
  if (els.actionTitle) els.actionTitle.value = "";
  if (els.actionEnabled) els.actionEnabled.value = "true";
  if (els.actionKind) els.actionKind.value = "prompt";

  if (els.actionPrompt) els.actionPrompt.value = "";
  if (els.actionAgent) els.actionAgent.value = "";
  if (els.actionModel) els.actionModel.value = "";
  if (els.actionReasoning) els.actionReasoning.value = "medium";
  if (els.actionTimeout) els.actionTimeout.value = "";

  if (els.actionCmd) els.actionCmd.value = "";
  if (els.actionShell) els.actionShell.value = "bash";
  if (els.actionCwd) els.actionCwd.value = ".";
  if (els.actionTimeoutCmd) els.actionTimeoutCmd.value = "";
}

function renderActionPalette() {
  if (!els.toolbox) return;

  // Remove any previous dynamic palette section.
  els.toolbox.querySelectorAll('[data-palette="actions"]').forEach((n) => n.remove());

  const items = Array.isArray(actionsIndex) ? actionsIndex : [];
  if (!items.length) return;

  const wrap = document.createElement("div");
  wrap.dataset.palette = "actions";

  const divider = document.createElement("div");
  divider.className = "divider";
  wrap.appendChild(divider);

  items.forEach((it) => {
    const id = it && typeof it.id === "number" ? it.id : null;
    if (id === null) return;
    const title = String((it && it.title) || "").trim() || `Action #${id}`;
    const enabled = Boolean(it && it.enabled);
    const readonly = Boolean(it && it.readonly);
    const stepType = defaultStepTypeForActionId(id);
    const cls = (BLOCK_META[stepType] && BLOCK_META[stepType].cls) || "block--work";

    const el = document.createElement("div");
    el.className = `block ${cls}`;
    el.draggable = true;
    el.dataset.paletteKind = "action";
    el.dataset.actionId = String(id);
    el.dataset.defaultStep = stepType;
    el.title = `#${id}${readonly ? " (readonly)" : ""}${enabled ? "" : " (disabled)"}`;
    el.textContent = `${title}${readonly ? " \u00b7 readonly" : ""}${enabled ? "" : " \u00b7 disabled"}`;
    wrap.appendChild(el);
  });

  els.toolbox.appendChild(wrap);
}

function renderActionsList() {
  if (!els.actionsList) return;
  els.actionsList.innerHTML = "";

  const items = Array.isArray(actionsIndex) ? actionsIndex : [];
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "canvas-empty";
    empty.textContent = t("ui.actions.empty");
    els.actionsList.appendChild(empty);
    return;
  }

  items.forEach((it) => {
    const id = it && typeof it.id === "number" ? it.id : null;
    if (id === null) return;
    const title = String((it && it.title) || "").trim() || `(untitled #${id})`;
    const kind = normalizeActionKind(it && it.kind);
    const enabled = Boolean(it && it.enabled);
    const ro = Boolean(it && it.readonly);

    const row = document.createElement("button");
    row.type = "button";
    row.className = "actionrow";
    if (id === selectedActionId) row.classList.add("is-selected");
    row.dataset.actionId = String(id);
    row.addEventListener("click", () => loadActionDefinition(id));

    const t = document.createElement("div");
    t.className = "actionrow-title";
    t.textContent = title;
    const meta = document.createElement("div");
    meta.className = "actionrow-meta";
    const enabledLabel = enabled ? t("ui.actions.state_enabled") : t("ui.actions.state_disabled");
    meta.textContent = `#${id} \u00b7 ${kind} \u00b7 ${enabledLabel}${ro ? " \u00b7 readonly" : ""}`;

    row.appendChild(t);
    row.appendChild(meta);
    els.actionsList.appendChild(row);
  });
}

async function refreshActionsList({ keepSelection } = {}) {
  if (!els.actionsList) return;
  try {
    const data = await api("/api/actions?limit=200");
    actionsIndex = Array.isArray(data.actions) ? data.actions : [];
    if (keepSelection && selectedActionId !== null) {
      const still = actionsIndex.some((a) => a && typeof a === "object" && a.id === selectedActionId);
      if (!still) {
        selectedActionId = null;
        selectedAction = null;
      }
    }
    renderActionPalette();
    renderActionsList();
    updateActionsButtons();
  } catch (e) {
    setActionsMsg(formatActionApiError(e), { error: true });
  }
}

function applyActionToForm(action, { editableKind } = {}) {
  const a = action && typeof action === "object" ? action : {};
  const id = typeof a.id === "number" ? a.id : null;
  const title = String(a.title || "");
  const enabled = Boolean(a.enabled);
  const kind = normalizeActionKind(a.kind);
  const spec = a && typeof a.spec === "object" && a.spec ? a.spec : {};

  if (els.actionId) els.actionId.value = id === null ? "" : String(id);
  if (els.actionTitle) els.actionTitle.value = title;
  if (els.actionEnabled) els.actionEnabled.value = enabled ? "true" : "false";
  setActionKindUi(kind, { editable: Boolean(editableKind) });

  if (kind === "prompt") {
    if (els.actionPrompt) els.actionPrompt.value = String(spec.prompt || "");
    if (els.actionAgent) els.actionAgent.value = typeof spec.agent === "string" ? spec.agent : "";
    if (els.actionModel) els.actionModel.value = typeof spec.model === "string" ? spec.model : "";
    if (els.actionReasoning) els.actionReasoning.value = typeof spec.reasoning === "string" ? spec.reasoning : "medium";
    if (els.actionTimeout) {
      els.actionTimeout.value =
        typeof spec.timeout_s === "number" && Number.isFinite(spec.timeout_s) ? String(spec.timeout_s) : "";
    }
  } else {
    if (els.actionCmd) els.actionCmd.value = String(spec.cmd || "");
    if (els.actionShell) els.actionShell.value = "bash";
    if (els.actionCwd) els.actionCwd.value = typeof spec.cwd === "string" ? spec.cwd : ".";
    if (els.actionTimeoutCmd) {
      els.actionTimeoutCmd.value =
        typeof spec.timeout_s === "number" && Number.isFinite(spec.timeout_s) ? String(spec.timeout_s) : "";
    }
  }
}

async function loadActionDefinition(id) {
  const aid = Number(id);
  if (!Number.isFinite(aid)) return;
  setActionsMsg("");
  try {
    const res = await api(`/api/actions/${encodeURIComponent(String(aid))}`);
    const action = res.action || {};
    actionsMode = "view";
    selectedActionId = aid;
    selectedAction = action;
    applyActionToForm(action, { editableKind: false });
    renderActionsList();
    updateActionsButtons();
  } catch (e) {
    setActionsMsg(formatActionApiError(e), { error: true });
  }
}

function enterNewActionMode() {
  actionsMode = "new";
  selectedActionId = null;
  selectedAction = null;
  clearActionForm();
  setActionKindUi("prompt", { editable: true });
  setActionsMsg("");
  renderActionsList();
  updateActionsButtons();
}

function buildActionSpecFromForm(kind, { forCreate } = {}) {
  const k = normalizeActionKind(kind);
  if (k === "prompt") {
    const prompt = String((els.actionPrompt && els.actionPrompt.value) || "").trim();
    if (!prompt) return { ok: false, error: "prompt is required" };
    const reasoning = String((els.actionReasoning && els.actionReasoning.value) || "medium").trim() || "medium";

    const spec = { prompt, reasoning };

    const agent = String((els.actionAgent && els.actionAgent.value) || "").trim();
    if (agent) spec.agent = agent;
    else if (!forCreate) spec.agent = null;

    const model = String((els.actionModel && els.actionModel.value) || "").trim();
    if (model) spec.model = model;
    else if (!forCreate) spec.model = null;

    const tRaw = String((els.actionTimeout && els.actionTimeout.value) || "").trim();
    if (tRaw) {
      const n = Number(tRaw);
      if (!Number.isFinite(n)) return { ok: false, error: "timeout must be a number" };
      spec.timeout_s = n;
    } else if (!forCreate) {
      spec.timeout_s = null;
    }
    return { ok: true, spec };
  }

  const cmd = String((els.actionCmd && els.actionCmd.value) || "").trim();
  if (!cmd) return { ok: false, error: "cmd is required" };
  const spec = { cmd, shell: "bash" };

  const cwd = String((els.actionCwd && els.actionCwd.value) || "").trim();
  if (cwd) spec.cwd = cwd;
  else if (!forCreate) spec.cwd = null;

  const tRaw = String((els.actionTimeoutCmd && els.actionTimeoutCmd.value) || "").trim();
  if (tRaw) {
    const n = Number(tRaw);
    if (!Number.isFinite(n)) return { ok: false, error: "timeout must be a number" };
    spec.timeout_s = n;
  } else if (!forCreate) {
    spec.timeout_s = null;
  }
  return { ok: true, spec };
}

async function saveActionFromForm() {
  if (!els.actionTitle || !els.actionKind || !els.actionEnabled) return;
  setActionsMsg("");

  const title = String(els.actionTitle.value || "").trim();
  if (!title) {
    setActionsMsg("title is required", { error: true });
    return;
  }

  const kind = normalizeActionKind(els.actionKind.value);
  const enabled = String(els.actionEnabled.value || "true") !== "false";

  const creating = actionsMode === "new" || selectedActionId === null;
  const built = buildActionSpecFromForm(kind, { forCreate: creating });
  if (!built.ok) {
    setActionsMsg(built.error, { error: true });
    return;
  }

  try {
    if (creating) {
      const res = await api("/api/actions", {
        method: "POST",
        body: JSON.stringify({ title, kind, enabled, spec: built.spec }),
      });
      const created = res.action || {};
      const id = typeof created.id === "number" ? created.id : null;
      actionsMode = "view";
      if (id !== null) selectedActionId = id;
      selectedAction = created;
      applyActionToForm(created, { editableKind: false });
      await refreshActionsList({ keepSelection: true });
      renderActionsList();
      updateActionsButtons();
      setActionsMsg("created");
      return;
    }

    const id = Number(selectedActionId);
    const isReadonly = Boolean(selectedAction && typeof selectedAction === "object" && selectedAction.readonly);

    const doUpdate = async (targetId) => {
      const res = await api(`/api/actions/${encodeURIComponent(String(targetId))}`, {
        method: "PUT",
        body: JSON.stringify({ title, enabled, spec: built.spec }),
      });
      const updated = res.action || {};
      selectedAction = updated;
      applyActionToForm(updated, { editableKind: false });
      await refreshActionsList({ keepSelection: true });
      renderActionsList();
      updateActionsButtons();
      return updated;
    };

    if (isReadonly) {
      const cloneRes = await api(`/api/actions/${encodeURIComponent(String(id))}/clone`, { method: "POST", body: "{}" });
      const created = cloneRes.action || {};
      const cloneId = typeof created.id === "number" ? created.id : null;
      if (cloneId === null) throw new Error("clone_failed");
      actionsMode = "view";
      selectedActionId = cloneId;
      selectedAction = created;
      const updated = await doUpdate(cloneId);
      selectedActionId = typeof updated.id === "number" ? updated.id : cloneId;
      setActionsMsg("cloned and saved");
      return;
    }

    try {
      const updated = await doUpdate(id);
      selectedActionId = typeof updated.id === "number" ? updated.id : id;
      setActionsMsg("saved");
      return;
    } catch (e) {
      const code = e && e.data && typeof e.data === "object" ? e.data.error : "";
      if (code === "readonly") {
        const cloneRes = await api(`/api/actions/${encodeURIComponent(String(id))}/clone`, { method: "POST", body: "{}" });
        const created = cloneRes.action || {};
        const cloneId = typeof created.id === "number" ? created.id : null;
        if (cloneId === null) throw new Error("clone_failed");
        actionsMode = "view";
        selectedActionId = cloneId;
        selectedAction = created;
        const updated = await doUpdate(cloneId);
        selectedActionId = typeof updated.id === "number" ? updated.id : cloneId;
        setActionsMsg("cloned and saved");
        return;
      }
      throw e;
    }
  } catch (e) {
    setActionsMsg(formatActionApiError(e), { error: true });
  }
}

async function deleteSelectedAction() {
  if (actionsMode !== "view" || selectedActionId === null) return;
  if (selectedAction && typeof selectedAction === "object" && selectedAction.readonly) {
    setActionsMsg("readonly", { error: true });
    return;
  }
  const id = Number(selectedActionId);
  if (!Number.isFinite(id)) return;
  const ok = window.confirm(`Delete action #${id}?`);
  if (!ok) return;
  setActionsMsg("");
  try {
    await api(`/api/actions/${encodeURIComponent(String(id))}`, { method: "DELETE" });
    selectedActionId = null;
    selectedAction = null;
    actionsMode = "view";
    clearActionForm();
    setActionKindUi("prompt", { editable: true });
    await refreshActionsList({ keepSelection: false });
    setActionsMsg("deleted");
  } catch (e) {
    setActionsMsg(formatActionApiError(e), { error: true });
  }
}

async function parseAapsToBlocks() {
  if (!els.scriptText) return;
  const script_text = String(els.scriptText.value || "");
  if (!script_text.trim()) {
    setScriptMsg("empty script", { error: true });
    return;
  }
  setScriptMsg("parsing...");
  try {
    const res = await api("/api/scripts/parse", { method: "POST", body: JSON.stringify({ script_text }) });
    const applied = applyIrToCanvas(res.ir || {});
    if (!applied.ok) {
      setScriptMsg("invalid IR returned from backend", { error: true });
      return;
    }
    setScriptMsg(`ok: parsed ${applied.steps} step(s) into blocks`);
  } catch (e) {
    setScriptMsg(formatScriptApiError(e), { error: true });
  }
}

async function importShellToBlocks() {
  if (!els.scriptText) return;
  const shell_text = String(els.scriptText.value || "");
  if (!shell_text.trim()) {
    setScriptMsg("empty shell text", { error: true });
    return;
  }
  setScriptMsg("importing...");
  try {
    const res = await api("/api/scripts/import-shell", { method: "POST", body: JSON.stringify({ shell_text }) });
    const extracted = typeof res.script_text === "string" ? res.script_text : "";
    if (extracted) els.scriptText.value = extracted;

    const applied = applyIrToCanvas(res.ir || {});
    if (!applied.ok) {
      setScriptMsg("invalid IR returned from backend", { error: true });
      return;
    }
    const warnings = Array.isArray(res.warnings) ? res.warnings : [];
    if (warnings.length) {
      setScriptMsg(`ok: imported ${applied.steps} step(s) (warnings: ${warnings.length})`);
    } else {
      setScriptMsg(`ok: imported ${applied.steps} step(s) into blocks`);
    }
  } catch (e) {
    setScriptMsg(formatScriptApiError(e), { error: true });
  }
}

function fillScriptFromBlocks() {
  if (!els.scriptText) return;
  if (!program.length) {
    setScriptMsg("no blocks on canvas", { error: true });
    return;
  }
  const titleRaw = window.prompt(t("ui.prompt.script_title"), "Program");
  if (titleRaw === null) return;
  const title = String(titleRaw).trim() || "Program";
  els.scriptText.value = programToAapsScript(program, title);
  setScriptMsg(`ok: generated script from ${countLeafBlocks(program)} step(s)`);
}

function sanitizeFileBase(name) {
  const raw = String(name || "").trim().toLowerCase();
  const cleaned = raw
    .replace(/[^a-z0-9_-]+/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 60);
  return cleaned || "program";
}

function downloadTextFile({ filename, content, mime }) {
  const fn = String(filename || "download.txt");
  const body = String(content || "");
  const type = String(mime || "text/plain") + ";charset=utf-8";
  const blob = new Blob([body], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = fn;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 0);
}

function aapsToShellAnnotations(aapsText) {
  const lines = String(aapsText || "").replace(/\r\n?/g, "\n").split("\n");
  return lines.map((l) => (l ? `# AAPS: ${l}` : "# AAPS:")).join("\n");
}

function generateRunnerScript(prog, { title, aapsText } = {}) {
  const steps = flattenLeafBlocks(Array.isArray(prog) ? prog : []);
  const safeTitle = String(title || "Program").replace(/\"/g, '\\"');
  const embedded = aapsToShellAnnotations(String(aapsText || ""));
  const out = [];
  out.push("#!/usr/bin/env bash");
  out.push("set -euo pipefail");
  out.push("");
  out.push('ROOT_DIR="$(pwd)"');
  out.push('RUNTIME_DIR="${AUTOAPPDEV_RUNTIME_DIR:-$ROOT_DIR/runtime}"');
  out.push('PAUSE_FLAG="$RUNTIME_DIR/PAUSE"');
  out.push("");
  out.push("cleanup() {");
  out.push('  echo "[autoappdev] received stop signal, exiting"');
  out.push("  exit 0");
  out.push("}");
  out.push("trap cleanup INT TERM");
  out.push("");
  out.push("pause_if_needed() {");
  out.push('  if [ -f "$PAUSE_FLAG" ]; then');
  out.push('    echo "[autoappdev] paused (remove $PAUSE_FLAG to resume)"');
  out.push('    while [ -f "$PAUSE_FLAG" ]; do');
  out.push("      sleep 0.5");
  out.push("    done");
  out.push('    echo "[autoappdev] resumed"');
  out.push("  fi");
  out.push("}");
  out.push("");
  out.push('mkdir -p "$RUNTIME_DIR"');
  out.push("");
  out.push('echo "[autoappdev] runner starting"');
  out.push(`echo "[autoappdev] title: ${safeTitle}"`);
  out.push('echo "[autoappdev] time: $(date -Iseconds)"');
  out.push('echo "[autoappdev] runtime_dir: $RUNTIME_DIR"');
  out.push(`echo "[autoappdev] steps: ${steps.length}"`);
  out.push("");

  if (embedded.trim()) {
    out.push("# Embedded AAPS v1 (importable via /api/scripts/import-shell):");
    out.push(embedded);
    out.push("# End embedded AAPS");
    out.push("");
  }

  steps.forEach((b, idx) => {
    const block = String((b && b.type) || "").trim();
    const label = canonicalBlockTitle(block, idx);
    out.push(`echo \"[autoappdev] step ${idx + 1}/${steps.length}: ${label} (${block || "unknown"})\"`);
    out.push("pause_if_needed");
    if (block === "commit_push") {
      out.push('echo "[autoappdev] note: commit/push is not performed by this generated runner"');
      out.push("sleep 1");
    } else {
      out.push("sleep 1");
    }
    out.push("");
  });

  out.push('echo "[autoappdev] done"');
  out.push("");
  return out.join("\n");
}

function exportAapsFile() {
  if (!els.scriptText) return;
  if (!program.length) {
    setScriptMsg("no blocks on canvas", { error: true });
    return;
  }
  const titleRaw = window.prompt(t("ui.prompt.script_title"), "Program");
  if (titleRaw === null) return;
  const title = String(titleRaw).trim() || "Program";
  const aaps = programToAapsScript(program, title);
  els.scriptText.value = aaps;
  const base = sanitizeFileBase(title);
  downloadTextFile({ filename: `${base}.aaps`, content: aaps, mime: "text/plain" });
  setScriptMsg(`ok: downloaded ${base}.aaps`);
}

function exportRunnerFile() {
  if (!program.length) {
    setScriptMsg("no blocks on canvas", { error: true });
    return;
  }
  const titleRaw = window.prompt(t("ui.prompt.runner_title"), "program-runner");
  if (titleRaw === null) return;
  const title = String(titleRaw).trim() || "program-runner";
  const aaps = programToAapsScript(program, title);
  if (els.scriptText) els.scriptText.value = aaps;
  const runner = generateRunnerScript(program, { title, aapsText: aaps });
  const base = sanitizeFileBase(title);
  downloadTextFile({ filename: `${base}.sh`, content: runner, mime: "text/x-shellscript" });
  setScriptMsg(`ok: downloaded ${base}.sh (run with: bash ${base}.sh)`);
}

async function sendPlan() {
  if (!program.length) {
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ ok: false, error: "empty_program" }, null, 2);
    return;
  }
  const payload = programToPlan(program);
  try {
    const ack = await api("/api/plan", { method: "POST", body: JSON.stringify(payload) });
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ ack, plan: payload }, null, 2);
  } catch (e) {
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ ok: false, error: e.message || String(e) }, null, 2);
  }
}

function setBadge(el, variant, text, title) {
  if (!el) return;
  el.classList.remove("badge--ok", "badge--warn", "badge--err", "badge--unknown", "badge--idle");
  el.classList.add("badge", variant);
  if (typeof text === "string") el.textContent = text;
  if (title !== undefined) el.title = title || "";
}

function pipelineVariant(state) {
  switch (String(state || "").toLowerCase()) {
    case "running":
      return "badge--ok";
    case "paused":
      return "badge--warn";
    case "failed":
      return "badge--err";
    case "completed":
    case "stopped":
    case "idle":
      return "badge--idle";
    default:
      return "badge--unknown";
  }
}

function normalizePipelineState(state) {
  const st = String(state || "").toLowerCase();
  if (st === "running") return "running";
  if (st === "paused") return "paused";
  return "stopped";
}

function updateActionButtons(state) {
  const st = normalizePipelineState(state);
  const isRunning = st === "running";
  const isPaused = st === "paused";
  els.start.disabled = isRunning || isPaused;
  els.pause.disabled = !isRunning;
  els.resume.disabled = !isPaused;
  els.stop.disabled = !(isRunning || isPaused);
}

function setCtrlMsg(text, { error } = {}) {
  if (!els.ctrlMsg) return;
  const msg = String(text || "");
  els.ctrlMsg.textContent = msg;
  els.ctrlMsg.classList.toggle("is-error", Boolean(error) && Boolean(msg));
}

async function doPipelineAction(action, fn) {
  setCtrlMsg("");
  try {
    await fn();
  } catch (e) {
    const status = e && typeof e.status === "number" ? e.status : null;
    if (status === 400) {
      const detail = e && e.data && e.data.detail ? String(e.data.detail) : "";
      setCtrlMsg(detail || e.message || `failed: ${action}`, { error: true });
    } else {
      setCtrlMsg((e && e.message) || `failed: ${action}`, { error: true });
    }
  } finally {
    await refreshStatus();
  }
}

async function refreshHealth() {
  try {
    const data = await api("/api/health");
    setBadge(els.backendHealth, "badge--ok", t("ui.health.ok"));
    const db = data.db || {};
    if (db.ok) {
      setBadge(els.dbHealth, "badge--ok", t("ui.health.ok"), db.time ? `time: ${db.time}` : "");
    } else {
      setBadge(els.dbHealth, "badge--err", t("ui.health.error"), db.error ? `error: ${db.error}` : "");
    }
  } catch (e) {
    setBadge(els.backendHealth, "badge--err", t("ui.health.down"));
    setBadge(els.dbHealth, "badge--unknown", t("ui.health.unknown"));
  }
}

async function refreshStatus() {
  try {
    const data = await api("/api/pipeline/status");
    const st = data.status || {};
    const state = st.state || (st.running ? "running" : "idle");
    const raw = String(state || "").toLowerCase();
    const key = `ui.pipeline.${raw}`;
    const label = t(key);
    setBadge(els.pipelineStatus, pipelineVariant(raw), label === key ? raw : label, raw);
    els.pipelinePid.textContent = st.pid ? String(st.pid) : "-";
    updateActionButtons(state);
  } catch {
    setBadge(els.pipelineStatus, "badge--unknown", t("ui.pipeline.unknown"));
    els.pipelinePid.textContent = "-";
    updateActionButtons("stopped");
  }
}

function bindDnD() {
  // Use event delegation so dynamically injected palette blocks (actions) work without re-binding.
  if (els.toolbox) {
    els.toolbox.addEventListener("dragstart", (ev) => {
      const t = ev && ev.target && ev.target.closest ? ev.target.closest(".block") : null;
      if (!t || !els.toolbox.contains(t)) return;
      const actionId = t.dataset.actionId;
      const blockType = t.dataset.block;
      if (actionId) {
        ev.dataTransfer.setData("text/plain", `action:${actionId}`);
      } else if (blockType) {
        ev.dataTransfer.setData("text/plain", `block:${blockType}`);
      } else {
        return;
      }
      ev.dataTransfer.effectAllowed = "copy";
    });
  }

  els.canvas.addEventListener("dragover", (ev) => {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "copy";
  });

  els.canvas.addEventListener("drop", (ev) => {
    ev.preventDefault();
    const payload = ev.dataTransfer.getData("text/plain");
    if (!payload) return;
    const m = /^([a-z_]+):(.*)$/.exec(String(payload || ""));
    const kind = m ? m[1] : "block";
    const value = m ? m[2] : String(payload || "");

    if (kind === "action") {
      const id = Number(String(value || "").trim());
      if (!Number.isFinite(id)) return;
      const stepType = defaultStepTypeForActionId(id);
      program.push({ type: stepType, action_ref: { id: Math.trunc(id) } });
      persistProgram();
      renderProgram();
      return;
    }

    const type = String(value || "").trim();
    if (!type) return;
    if (type === "update_readme") {
      const raw = window.prompt(
        t("ui.prompt.workspace_slug_for_readme"),
        String(workspaceSlug || "my_workspace")
      );
      if (raw === null) return;
      const parsed = parseWorkspaceSlug(raw);
      if (!parsed.ok) {
        window.alert(`${t("ui.alert.invalid_workspace")}: ${parsed.error}`);
        return;
      }
      program.push({ type, workspace: parsed.workspace });
    } else {
      program.push(makeBlockFromType(type));
    }
    persistProgram();
    renderProgram();
  });
}

function bindTabs() {
  const setTab = (key) => {
    els.tabs.forEach((t) => t.classList.toggle("is-active", t.dataset.tab === key));
    els.tabStatus.hidden = key !== "status";
    els.tabChat.hidden = key !== "chat";
    els.tabLogs.hidden = key !== "logs";
    if (els.tabActions) els.tabActions.hidden = key !== "actions";
    if (els.tabScript) els.tabScript.hidden = key !== "script";
    if (key === "logs") refreshLogs();
    if (key === "chat") loadChat();
    if (key === "actions" && !actionsLoadedOnce) {
      actionsLoadedOnce = true;
      refreshActionsList({ keepSelection: true });
    }
  };

  els.tabs.forEach((t) => {
    t.addEventListener("click", () => setTab(t.dataset.tab));
  });
}

async function loadChat() {
  try {
    const [inboxRes, outboxRes] = await Promise.all([
      api("/api/inbox?limit=80").catch(() => ({ messages: [] })),
      api("/api/outbox?limit=80").catch(() => ({ messages: [] })),
    ]);

    const inbox = Array.isArray(inboxRes && inboxRes.messages) ? inboxRes.messages : [];
    const outbox = Array.isArray(outboxRes && outboxRes.messages) ? outboxRes.messages : [];
    const merged = [];
    let idx = 0;
    inbox.forEach((m) => merged.push({ m, idx: idx++ }));
    outbox.forEach((m) => merged.push({ m, idx: idx++ }));

    const parseTs = (it) => {
      const obj = it && typeof it === "object" ? it : {};
      const raw = obj.created_at;
      if (typeof raw !== "string") return 0;
      const n = Date.parse(raw);
      return Number.isFinite(n) ? n : 0;
    };

    merged.sort((a, b) => {
      const ta = parseTs(a.m);
      const tb = parseTs(b.m);
      if (ta !== tb) return ta - tb;
      return a.idx - b.idx;
    });

    els.chatlog.innerHTML = "";
    merged.forEach(({ m }) => {
      const div = document.createElement("div");
      div.className = `msg ${m.role === "user" ? "msg--user" : "msg--system"}`;
      div.textContent = m.content || "";
      els.chatlog.appendChild(div);
    });
    els.chatlog.scrollTop = els.chatlog.scrollHeight;
  } catch {
    // ignore
  }
}

async function sendChat() {
  const content = (els.chatInput.value || "").trim();
  if (!content) return;
  els.chatInput.value = "";
  try {
    await api("/api/inbox", { method: "POST", body: JSON.stringify({ content }) });
  } catch (e) {
    console.warn(e);
  }
  await loadChat();
}

function scrollLogsToBottom() {
  const candidates = [els.tabLogs, els.logview];
  candidates.forEach((el) => {
    if (!el) return;
    try {
      el.scrollTop = el.scrollHeight;
    } catch {}
  });
}

function appendLogText(text) {
  if (!els.logview) return;
  els.logview.insertAdjacentText("beforeend", String(text || ""));
}

function updateLogFollowButtonLabel() {
  if (!els.logFollow) return;
  els.logFollow.textContent = logFollow ? t("ui.btn.pause") : t("ui.btn.follow");
  els.logFollow.setAttribute("aria-pressed", logFollow ? "true" : "false");
}

function setLogFollow(on) {
  logFollow = Boolean(on);
  updateLogFollowButtonLabel();
  if (logFollow) scrollLogsToBottom();
}

async function refreshLogs({ reset } = {}) {
  const sourceRaw = String((els.logSelect && els.logSelect.value) || "pipeline");
  const source = sourceRaw === "backend" ? "backend" : "pipeline";
  const shouldReset = Boolean(reset) || !logInitialized[source];

  try {
    if (shouldReset) {
      els.logview.textContent = "";
      logSince[source] = 0;
      const data = await api(
        `/api/logs?source=${encodeURIComponent(source)}&since=0&limit=${LOG_RESET_LIMIT}`
      );
      const items = Array.isArray(data.lines) ? data.lines : [];
      const slice = items.slice(-LOG_WINDOW_LIMIT);
      const text = slice.map((it) => String((it && it.line) || "")).join("\n");
      els.logview.textContent = text;
      if (text) appendLogText("\n");
      const next = Number.isFinite(data.next) ? Number(data.next) : 0;
      logSince[source] = next;
      logInitialized[source] = true;
      if (logFollow) scrollLogsToBottom();
      return;
    }

    const since = logSince[source] || 0;
    const data = await api(
      `/api/logs?source=${encodeURIComponent(source)}&since=${since}&limit=${LOG_WINDOW_LIMIT}`
    );
    const items = Array.isArray(data.lines) ? data.lines : [];
    if (items.length) {
      appendLogText(items.map((it) => String((it && it.line) || "")).join("\n") + "\n");
      if (logFollow) scrollLogsToBottom();
    }
    const next = Number.isFinite(data.next) ? Number(data.next) : since;
    logSince[source] = next;
  } catch (e) {
    els.logview.textContent = String((e && e.message) || e);
  }
}

function bindControls() {
  els.themeBtn.addEventListener("click", () => {
    const cur = document.body.dataset.theme || "light";
    setTheme(cur === "light" ? "dark" : "light");
  });

  if (els.uiLang) {
    els.uiLang.addEventListener("change", () => setUiLang(els.uiLang.value));
  }

  if (els.agentSelect) els.agentSelect.addEventListener("change", saveSettings);
  if (els.modelSelect) els.modelSelect.addEventListener("change", saveSettings);

  els.exportBtn.addEventListener("click", () => {
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ program }, null, 2);
  });

  if (els.sendPlanBtn) {
    els.sendPlanBtn.addEventListener("click", sendPlan);
  }
  if (els.saveScriptBtn) {
    els.saveScriptBtn.addEventListener("click", saveScript);
  }
  if (els.loadScriptBtn) {
    els.loadScriptBtn.addEventListener("click", loadScript);
  }
  if (els.scriptParse) {
    els.scriptParse.addEventListener("click", parseAapsToBlocks);
  }
  if (els.scriptImportShell) {
    els.scriptImportShell.addEventListener("click", importShellToBlocks);
  }
  if (els.scriptFromBlocks) {
    els.scriptFromBlocks.addEventListener("click", fillScriptFromBlocks);
  }
  if (els.scriptDownloadAaps) {
    els.scriptDownloadAaps.addEventListener("click", exportAapsFile);
  }
  if (els.scriptDownloadRunner) {
    els.scriptDownloadRunner.addEventListener("click", exportRunnerFile);
  }
  if (els.scriptFile) {
    els.scriptFile.addEventListener("change", async () => {
      const file = els.scriptFile.files && els.scriptFile.files[0];
      if (!file) return;
      try {
        const text = await file.text();
        if (els.scriptText) els.scriptText.value = text;
        const name = String(file.name || "").toLowerCase();
        if (name.endsWith(".sh")) {
          await importShellToBlocks();
        } else {
          await parseAapsToBlocks();
        }
      } catch (e) {
        setScriptMsg(`failed to load file: ${(e && e.message) || String(e)}`, { error: true });
      } finally {
        try {
          els.scriptFile.value = "";
        } catch {}
      }
    });
  }

  els.clearBtn.addEventListener("click", () => {
    program = [];
    persistProgram();
    renderProgram();
    els.export.hidden = true;
  });

  els.chatSend.addEventListener("click", sendChat);
  els.chatInput.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter") sendChat();
  });

  if (els.logFollow) {
    els.logFollow.addEventListener("click", () => setLogFollow(!logFollow));
  }
  if (els.logSelect) {
    els.logSelect.addEventListener("change", () => refreshLogs({ reset: true }));
  }
  els.logRefresh.addEventListener("click", () => refreshLogs({ reset: true }));

  els.start.addEventListener("click", () =>
    doPipelineAction("start", () => api("/api/pipeline/start", { method: "POST", body: JSON.stringify({}) }))
  );

  els.pause.addEventListener("click", () =>
    doPipelineAction("pause", () => api("/api/pipeline/pause", { method: "POST", body: JSON.stringify({}) }))
  );
  els.resume.addEventListener("click", () =>
    doPipelineAction("resume", () => api("/api/pipeline/resume", { method: "POST", body: JSON.stringify({}) }))
  );
  els.stop.addEventListener("click", () =>
    doPipelineAction("stop", () => api("/api/pipeline/stop", { method: "POST", body: JSON.stringify({}) }))
  );

  if (els.actionsRefresh) {
    els.actionsRefresh.addEventListener("click", () => refreshActionsList({ keepSelection: true }));
  }
  if (els.actionsNew) {
    els.actionsNew.addEventListener("click", enterNewActionMode);
  }
  if (els.actionsSave) {
    els.actionsSave.addEventListener("click", saveActionFromForm);
  }
  if (els.actionsDelete) {
    els.actionsDelete.addEventListener("click", deleteSelectedAction);
  }
  if (els.actionKind) {
    els.actionKind.addEventListener("change", () => {
      const k = normalizeActionKind(els.actionKind.value);
      setActionKindUi(k, { editable: actionsMode === "new" });
    });
  }

  if (els.wsLoad) {
    els.wsLoad.addEventListener("click", () => loadWorkspaceConfig(els.wsSlug ? els.wsSlug.value : ""));
  }
  if (els.wsSave) {
    els.wsSave.addEventListener("click", saveWorkspaceConfig);
  }
  if (els.wsSlug) {
    els.wsSlug.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") loadWorkspaceConfig(els.wsSlug.value);
    });
  }
}

function boot() {
  setUiLang(loadUiLangFromStorage(), { persist: false });

  loadProgram();
  renderProgram();
  bindDnD();
  bindTabs();
  bindControls();
  updateActionButtons("stopped");
  setLogFollow(true);

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("./service-worker.js").catch((e) => {
      console.warn("service worker registration failed", e);
    });
  }

  const savedTheme = localStorage.getItem("autoappdev_theme");
  setTheme(savedTheme === "dark" ? "dark" : "light");

  loadSettings();
  const savedWs = loadWorkspaceSlugFromStorage();
  if (els.wsSlug && savedWs) els.wsSlug.value = savedWs;
  if (savedWs) loadWorkspaceConfig(savedWs);

  refreshHealth();
  refreshStatus();
  loadChat();
  refreshLogs({ reset: true });
  updateActionsButtons();
  refreshActionsList({ keepSelection: true });

  window.setInterval(refreshHealth, 2000);
  window.setInterval(refreshStatus, 2000);
  window.setInterval(() => {
    // keep logs reasonably fresh while running
    if (!els.tabLogs.hidden) refreshLogs();
    if (!els.tabChat.hidden) loadChat();
  }, 2500);
}

boot();
