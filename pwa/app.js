const els = {
  themeBtn: document.getElementById("btn-theme"),
  start: document.getElementById("btn-start"),
  pause: document.getElementById("btn-pause"),
  resume: document.getElementById("btn-resume"),
  stop: document.getElementById("btn-stop"),
  backendHealth: document.getElementById("backend-health"),
  dbHealth: document.getElementById("db-health"),
  pipelineStatus: document.getElementById("pipeline-status"),
  pipelinePid: document.getElementById("pipeline-pid"),
  toolbox: document.getElementById("toolbox"),
  canvas: document.getElementById("canvas"),
  canvasEmpty: document.getElementById("canvas-empty"),
  exportBtn: document.getElementById("btn-export"),
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
  } catch {
    setBadge(els.pipelineStatus, "badge--unknown", "unknown");
    els.pipelinePid.textContent = "-";
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
  };

  els.tabs.forEach((t) => {
    t.addEventListener("click", () => setTab(t.dataset.tab));
  });
}

async function loadChat() {
  try {
    const data = await api("/api/chat?limit=50");
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
    await api("/api/chat", { method: "POST", body: JSON.stringify({ content }) });
  } catch (e) {
    console.warn(e);
  }
  await loadChat();
}

async function refreshLogs() {
  const name = els.logSelect.value || "pipeline";
  try {
    const data = await api(`/api/logs/tail?name=${encodeURIComponent(name)}&lines=400`);
    els.logview.textContent = (data.lines || []).join("\n");
  } catch (e) {
    els.logview.textContent = String(e.message || e);
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

  els.logRefresh.addEventListener("click", refreshLogs);

  els.start.addEventListener("click", async () => {
    // Minimal integration: just start the default pipeline script.
    try {
      await api("/api/pipeline/start", { method: "POST", body: JSON.stringify({}) });
    } catch (e) {
      alert(`Start failed: ${e.message || e}`);
    }
    await refreshStatus();
  });

  els.pause.addEventListener("click", async () => {
    await api("/api/pipeline/pause", { method: "POST", body: "{}" }).catch(() => {});
    await refreshStatus();
  });
  els.resume.addEventListener("click", async () => {
    await api("/api/pipeline/resume", { method: "POST", body: "{}" }).catch(() => {});
    await refreshStatus();
  });
  els.stop.addEventListener("click", async () => {
    await api("/api/pipeline/stop", { method: "POST", body: "{}" }).catch(() => {});
    await refreshStatus();
  });
}

function boot() {
  loadProgram();
  renderProgram();
  bindDnD();
  bindTabs();
  bindControls();

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
  refreshLogs();

  window.setInterval(refreshHealth, 2000);
  window.setInterval(refreshStatus, 2000);
  window.setInterval(() => {
    // keep logs reasonably fresh while running
    if (!els.tabLogs.hidden) refreshLogs();
    if (!els.tabChat.hidden) loadChat();
  }, 2500);
}

boot();
