const els = {
  themeBtn: document.getElementById("btn-theme"),
  agentSelect: document.getElementById("agent-select"),
  modelSelect: document.getElementById("model-select"),
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
};

const BLOCK_META = {
  plan: { label: "Plan", cls: "block--plan" },
  work: { label: "Work", cls: "block--work" },
  debug: { label: "Debug", cls: "block--debug" },
  fix: { label: "Fix", cls: "block--fix" },
  summary: { label: "Summary", cls: "block--summary" },
  update_readme: { label: "Update README", cls: "block--summary" },
  commit_push: { label: "Commit+Push", cls: "block--release" },
  while_loop: { label: "While", cls: "block--loop" },
  wait_input: { label: "Wait Input", cls: "block--input" },
};

let program = [];

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

function setTheme(next) {
  document.body.dataset.theme = next;
  els.themeBtn.textContent = next === "dark" ? "Dark" : "Light";
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

function formatProgramBlockLabel(block, meta) {
  const b = block && typeof block === "object" ? block : {};
  const type = String(b.type || "");
  if (type === "update_readme") {
    const ws = String(b.workspace || "").trim();
    return `${String(meta.label || "Update README")} (${updateReadmeTargetPath(ws)})`;
  }
  const base = String(meta.label || type || "Block");
  const ref = normalizeActionRef(b.action_ref);
  if (!ref) return base;
  if (typeof ref.id === "number") {
    const title = lookupActionTitleById(ref.id);
    return title ? `${base} -> #${ref.id} ${title}` : `${base} -> #${ref.id}`;
  }
  return `${base} -> slug: ${String(ref.slug)}`;
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
  program.forEach((b, idx) => {
    const type = b && typeof b === "object" ? String(b.type || "") : "";
    const meta = BLOCK_META[type] || { label: type, cls: "block--work" };
    const row = document.createElement("div");
    row.className = `prog-block ${meta.cls}`;
    const label = document.createElement("div");
    label.className = "prog-label";
    label.textContent = formatProgramBlockLabel(b, meta);
    row.appendChild(label);
    if (type !== "update_readme") {
      const bind = document.createElement("button");
      bind.className = "prog-bind";
      bind.type = "button";
      bind.textContent = "Bind";
      bind.addEventListener("click", () => {
        const cur = b && typeof b === "object" ? b : {};
        const curRef = normalizeActionRef(cur.action_ref);
        const raw = window.prompt("Action ref (id or slug). Blank to clear.", actionRefValue(curRef));
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
            window.alert("Invalid id");
            return;
          }
        } else {
          if (s.length > 200 || /[\x00-\x1f]/.test(s)) {
            window.alert("Invalid slug");
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
      program.splice(idx, 1);
      persistProgram();
      renderProgram();
    });
    row.appendChild(rm);
    wrap.appendChild(row);
  });
  els.canvas.appendChild(wrap);
}

function persistProgram() {
  localStorage.setItem("autoappdev_program", JSON.stringify(program));
}

function loadProgram() {
  try {
    const raw = localStorage.getItem("autoappdev_program");
    if (!raw) return;
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
  const steps = (Array.isArray(prog) ? prog : []).map((b, idx) => ({
    id: idx + 1,
    block: (() => {
      const type = b && typeof b === "object" ? String(b.type || "") : "";
      return type === "update_readme" ? "summary" : type;
    })(),
  }));
  return { kind: "autoappdev_plan", version: 1, steps };
}

function programToIr(prog, title = "Program") {
  const steps = (Array.isArray(prog) ? prog : []).map((b, idx) => {
    const type = b && typeof b === "object" ? String(b.type || "") : "";
    const meta = BLOCK_META[type] || { label: type || `Step ${idx + 1}` };
    let block = type;
    let actions = [{ id: "a1", kind: "noop", params: {} }];
    if (type === "update_readme") {
      block = "summary";
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
    return {
      id: `s${idx + 1}`,
      title: meta.label,
      block,
      actions,
    };
  });
  return {
    kind: "autoappdev_ir",
    version: 1,
    tasks: [{ id: "t1", title: String(title || "Program"), steps }],
  };
}

function programToAapsScript(prog, title = "Program") {
  const lines = [];
  lines.push("AUTOAPPDEV_PIPELINE 1");
  lines.push("");
  lines.push(`TASK  ${JSON.stringify({ id: "t1", title: String(title || "Program") })}`);
  lines.push("");
  (Array.isArray(prog) ? prog : []).forEach((b, idx) => {
    const type = b && typeof b === "object" ? String(b.type || "") : "";
    const meta = BLOCK_META[type] || { label: type || `Step ${idx + 1}` };
    let block = type;
    let action = { id: "a1", kind: "noop", params: {} };
    if (type === "update_readme") {
      block = "summary";
      const ws = String((b && b.workspace) || "").trim();
      action = {
        id: "a1",
        kind: "update_readme",
        params: {
          workspace: ws,
          block_markdown: defaultUpdateReadmeBlockMarkdown({ workspace: ws }),
        },
      };
    } else {
      const ref = normalizeActionRef(b && b.action_ref);
      if (ref) action.meta = { action_ref: ref };
    }
    lines.push(`STEP  ${JSON.stringify({ id: `s${idx + 1}`, title: meta.label, block })}`);
    lines.push(`ACTION ${JSON.stringify(action)}`);
    lines.push("");
  });
  return lines.join("\n").trimEnd() + "\n";
}

function irToProgram(ir) {
  if (!ir || typeof ir !== "object") return null;
  const tasks = Array.isArray(ir.tasks) ? ir.tasks : [];
  const steps = [];
  tasks.forEach((t) => {
    const s = t && Array.isArray(t.steps) ? t.steps : [];
    s.forEach((st) => {
      if (!st || typeof st !== "object") return;
      const actions = Array.isArray(st.actions) ? st.actions : [];
      const upd = actions.find((a) => a && typeof a === "object" && a.kind === "update_readme");
      const params = upd && typeof upd === "object" ? upd.params : null;
      const ws = params && typeof params === "object" ? String(params.workspace || "").trim() : "";
      if (ws) {
        steps.push({ type: "update_readme", workspace: ws });
        return;
      }
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

      if (typeof st.block === "string" && st.block.trim()) {
        const obj = { type: st.block.trim() };
        if (ref) obj.action_ref = ref;
        steps.push(obj);
      }
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
  const titleRaw = window.prompt("Script title?", "Program");
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
  const raw = window.prompt("Load script id?", "");
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
  return { ok: true, steps: nextProgram.length };
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
  if (els.actionsDelete) els.actionsDelete.disabled = !hasExisting;
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

function renderActionsList() {
  if (!els.actionsList) return;
  els.actionsList.innerHTML = "";

  const items = Array.isArray(actionsIndex) ? actionsIndex : [];
  if (!items.length) {
    const empty = document.createElement("div");
    empty.className = "canvas-empty";
    empty.textContent = "No actions yet. Click New to create one.";
    els.actionsList.appendChild(empty);
    return;
  }

  items.forEach((it) => {
    const id = it && typeof it.id === "number" ? it.id : null;
    if (id === null) return;
    const title = String((it && it.title) || "").trim() || `(untitled #${id})`;
    const kind = normalizeActionKind(it && it.kind);
    const enabled = Boolean(it && it.enabled);

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
    meta.textContent = `#${id} \u00b7 ${kind} \u00b7 ${enabled ? "enabled" : "disabled"}`;

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
    const res = await api(`/api/actions/${encodeURIComponent(String(id))}`, {
      method: "PUT",
      body: JSON.stringify({ title, enabled, spec: built.spec }),
    });
    const updated = res.action || {};
    selectedAction = updated;
    applyActionToForm(updated, { editableKind: false });
    await refreshActionsList({ keepSelection: true });
    renderActionsList();
    updateActionsButtons();
    setActionsMsg("saved");
  } catch (e) {
    setActionsMsg(formatActionApiError(e), { error: true });
  }
}

async function deleteSelectedAction() {
  if (actionsMode !== "view" || selectedActionId === null) return;
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
  const titleRaw = window.prompt("Script title?", "Program");
  if (titleRaw === null) return;
  const title = String(titleRaw).trim() || "Program";
  els.scriptText.value = programToAapsScript(program, title);
  setScriptMsg(`ok: generated script from ${program.length} block(s)`);
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
  const steps = Array.isArray(prog) ? prog : [];
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
    const meta = BLOCK_META[block] || { label: block || `Step ${idx + 1}` };
    const label = String(meta.label || block || `Step ${idx + 1}`);
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
  const titleRaw = window.prompt("Script title?", "Program");
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
  const titleRaw = window.prompt("Runner title?", "program-runner");
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
    setBadge(els.backendHealth, "badge--ok", "ok");
    const db = data.db || {};
    if (db.ok) {
      setBadge(els.dbHealth, "badge--ok", "ok", db.time ? `time: ${db.time}` : "");
    } else {
      setBadge(els.dbHealth, "badge--err", "error", db.error ? `error: ${db.error}` : "");
    }
  } catch (e) {
    setBadge(els.backendHealth, "badge--err", "down");
    setBadge(els.dbHealth, "badge--unknown", "unknown");
  }
}

async function refreshStatus() {
  try {
    const data = await api("/api/pipeline/status");
    const st = data.status || {};
    const state = st.state || (st.running ? "running" : "idle");
    els.pipelineStatus.textContent = state;
    setBadge(els.pipelineStatus, pipelineVariant(state), state);
    els.pipelinePid.textContent = st.pid ? String(st.pid) : "-";
    updateActionButtons(state);
  } catch {
    setBadge(els.pipelineStatus, "badge--unknown", "unknown");
    els.pipelinePid.textContent = "-";
    updateActionButtons("stopped");
  }
}

function bindDnD() {
  document.querySelectorAll(".toolbox .block").forEach((el) => {
    el.addEventListener("dragstart", (ev) => {
      ev.dataTransfer.setData("text/plain", el.dataset.block);
      ev.dataTransfer.effectAllowed = "copy";
    });
  });

  els.canvas.addEventListener("dragover", (ev) => {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "copy";
  });

  els.canvas.addEventListener("drop", (ev) => {
    ev.preventDefault();
    const type = ev.dataTransfer.getData("text/plain");
    if (!type) return;
    if (type === "update_readme") {
      const raw = window.prompt("Workspace slug for auto-apps/<workspace>/README.md?", "my_workspace");
      if (raw === null) return;
      const parsed = parseWorkspaceSlug(raw);
      if (!parsed.ok) {
        window.alert(`Invalid workspace: ${parsed.error}`);
        return;
      }
      program.push({ type, workspace: parsed.workspace });
    } else {
      program.push({ type });
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
    const data = await api("/api/inbox?limit=50");
    const msgs = data.messages || [];
    els.chatlog.innerHTML = "";
    msgs.forEach((m) => {
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

function setLogFollow(on) {
  logFollow = Boolean(on);
  if (els.logFollow) {
    els.logFollow.textContent = logFollow ? "Pause" : "Follow";
    els.logFollow.setAttribute("aria-pressed", logFollow ? "true" : "false");
  }
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
}

function boot() {
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

  refreshHealth();
  refreshStatus();
  loadChat();
  refreshLogs({ reset: true });
  updateActionsButtons();

  window.setInterval(refreshHealth, 2000);
  window.setInterval(refreshStatus, 2000);
  window.setInterval(() => {
    // keep logs reasonably fresh while running
    if (!els.tabLogs.hidden) refreshLogs();
    if (!els.tabChat.hidden) loadChat();
  }, 2500);
}

boot();
