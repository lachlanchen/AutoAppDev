const els = {
  themeBtn: document.getElementById("btn-theme"),
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
  clearBtn: document.getElementById("btn-clear"),
  export: document.getElementById("export"),
  tabs: document.querySelectorAll(".tab"),
  tabStatus: document.getElementById("tab-status"),
  tabChat: document.getElementById("tab-chat"),
  tabLogs: document.getElementById("tab-logs"),
  chatlog: document.getElementById("chatlog"),
  chatInput: document.getElementById("chat-input"),
  chatSend: document.getElementById("chat-send"),
  logSelect: document.getElementById("log-select"),
  logFollow: document.getElementById("log-follow"),
  logRefresh: document.getElementById("log-refresh"),
  logview: document.getElementById("logview"),
};

const BLOCK_META = {
  plan: { label: "Plan", cls: "block--plan" },
  work: { label: "Work", cls: "block--work" },
  debug: { label: "Debug", cls: "block--debug" },
  fix: { label: "Fix", cls: "block--fix" },
  summary: { label: "Summary", cls: "block--summary" },
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

function setTheme(next) {
  document.body.dataset.theme = next;
  els.themeBtn.textContent = next === "dark" ? "Dark" : "Light";
  localStorage.setItem("autoappdev_theme", next);
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
    const meta = BLOCK_META[b.type] || { label: b.type, cls: "block--work" };
    const row = document.createElement("div");
    row.className = `prog-block ${meta.cls}`;
    row.innerHTML = `<div class="prog-label">${meta.label}</div>`;
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

function programToPlan(prog) {
  const steps = (Array.isArray(prog) ? prog : []).map((b, idx) => ({
    id: idx + 1,
    block: String((b && b.type) || ""),
  }));
  return { kind: "autoappdev_plan", version: 1, steps };
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
    program.push({ type });
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
    if (key === "logs") refreshLogs();
    if (key === "chat") loadChat();
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

  els.exportBtn.addEventListener("click", () => {
    els.export.hidden = false;
    els.export.textContent = JSON.stringify({ program }, null, 2);
  });

  if (els.sendPlanBtn) {
    els.sendPlanBtn.addEventListener("click", sendPlan);
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

  refreshHealth();
  refreshStatus();
  loadChat();
  refreshLogs({ reset: true });

  window.setInterval(refreshHealth, 2000);
  window.setInterval(refreshStatus, 2000);
  window.setInterval(() => {
    // keep logs reasonably fresh while running
    if (!els.tabLogs.hidden) refreshLogs();
    if (!els.tabChat.hidden) loadChat();
  }, 2500);
}

boot();
