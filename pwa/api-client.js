/* Small API client wrapper for the AutoAppDev PWA (no bundler/modules). */

(function () {
  const cfg = window.__AUTOAPPDEV_CONFIG__ || {};
  const API_BASE_URL = cfg.API_BASE_URL || "http://127.0.0.1:8788";

  async function requestJson(path, opts = {}) {
    const { timeout_ms, headers, ...rest } = opts || {};
    const timeoutMs = Number.isFinite(timeout_ms) ? Number(timeout_ms) : 4000;

    const ctrl = new AbortController();
    const timer = window.setTimeout(() => ctrl.abort(), timeoutMs);

    try {
      const res = await fetch(`${API_BASE_URL}${path}`, {
        headers: { "Content-Type": "application/json", ...(headers || {}) },
        signal: ctrl.signal,
        ...rest,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        const msg = data.error || data.detail || `HTTP ${res.status}`;
        const err = new Error(msg);
        err.status = res.status;
        err.data = data;
        throw err;
      }
      return data;
    } catch (e) {
      if (e && e.name === "AbortError") {
        const err = new Error("timeout");
        err.code = "timeout";
        throw err;
      }
      throw e;
    } finally {
      window.clearTimeout(timer);
    }
  }

  window.AutoAppDevApi = {
    API_BASE_URL,
    requestJson,
  };
})();

