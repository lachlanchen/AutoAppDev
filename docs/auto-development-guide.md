# Auto Development Guide / 自动开发指南

This guide constrains `scripts/app-auto-development.sh` (and the future auto-development pipeline) to iteratively build LightMind backend/PWA/Android/iOS in a long-running, resumable, operable way.

本指南用于约束 `scripts/app-auto-development.sh`（以及后续的 auto-development pipeline）在长期、可恢复、可运营的方式下，持续迭代开发 LightMind 的 backend/PWA/Android/iOS。

## 0) Iteration Principle: Global-to-Local / 迭代原则：从整体到局部

English:
- Global first: each iteration must keep the whole system runnable/buildable before refining details.
- Small steps: each step should be small (5-30 minutes), and must state how it contributes to the overall app.
- Prompts must be redundant and self-contained: each `codex exec` prompt must repeat enough context (goal, constraints, paths, acceptance) because it only owns a tiny step but must remember the whole.
- Prompts must explicitly describe the pipeline stage (plan/implement/debug/verify/release) and dependencies to previous/next steps.

中文：
- 全局优先：每一轮迭代先保证“整体能跑通/编译通”，再逐步细化局部功能与 UI。
- 小步推进：每一步尽量足够小（可在 5-30 分钟内完成），但必须明确“这一步在为整体的哪一块铺路”。
- prompt 需冗余且自洽：每一步 prompt 都应包含足够详细甚至重复的信息（上下文、目标、限制、输出路径、验收标准），因为每次 `codex exec` 只负责一个很小的子任务，但需要记住整体目标。
- prompt 需显式说明 pipeline：让每个小步知道自己处于 pipeline 的哪个阶段（规划/实现/调试/校验/提交），以及与前后步骤的依赖关系。

## 1) Minimum Quality Bar (Fix Obvious Errors First) / 最低质量门槛（先修复明显错误）

English:
- Prioritize blockers to running/building (crash, stuck route, unclickable UI, build failures, broken APIs).
- Every step must produce a minimally verifiable result (e.g., endpoint 200, screen renders, buttons clickable, build passes).

中文：
- 优先修复“阻塞运行/编译”的问题（崩溃、路由卡死、不可点击、构建失败、接口不通等），达到至少能跑通/编译通的程度。
- 每步都要有最小可验证的结果（例如：接口 200、页面能打开、按钮可点击、构建通过）。

## 2) Themes / 主题（Theme）

English:
- Two themes: light and dark (black/white).
- Default: light.
- Keep semantic tokens consistent across PWA/Android/iOS (e.g., `surface/text/accent`).

中文：
- 两种主题：黑/白（Light/Dark）。
- 默认主题：Light。
- 主题切换应在 PWA/Android/iOS 上保持一致（同一套语义 token，例如 `surface/text/accent`）。

## 3) Languages (i18n) / 多语言（i18n）

Must support and keep consistent / 必须支持并保持一致：
- 简体中文
- 繁体中文
- English
- 日本語
- 한국어
- Tiếng Việt
- العربية
- Español
- Français
- Deutsch
- Русский

English requirements:
- Unified key naming and fallback strategy (fallback to English or Simplified Chinese).
- Arabic must support RTL (layout and icon direction).
- PWA should support runtime UI language switching and persist the choice (e.g., `localStorage["autoappdev_ui_lang"]`).

中文要求：
- 统一 key 命名与回退策略（缺失时回退到英文或简中）。
- 阿拉伯语需考虑 RTL（布局与图标方向）。
- PWA 需支持运行时切换 UI 语言并持久化（例如 `localStorage["autoappdev_ui_lang"]`）。

## 4) Every Step Must Consider the Whole Architecture / 每一步必须考虑整体结构

English:
- No one-off hardcoding only for the current screenshot. Consider navigation, state, data model, API versioning, errors, and future extensibility.
- New modules/classes/files must use LightMind naming by default (avoid introducing new HeyCyan identifiers unless compatibility requires it).

中文：
- 不允许“只为当前截图硬编码一次性逻辑”。需要考虑导航结构、状态管理、数据模型、API 版本化、错误处理与未来扩展。
- 新增模块/类/文件命名一律以 LightMind 为主（避免引入 HeyCyan 命名污染，除非兼容性必需）。

## 5) Debugging / 调试（PWA + Android + iOS）

English:
- PWA: local start, devtools, automated/semi-automated checks as needed (Selenium/ChromeDriver when appropriate).
- Android/iOS: each iteration must have an executable debug path (build, run, minimal smoke test).

中文：
- PWA debug。
- Android and iOS 调试（每轮迭代都应可构建、可运行、可做最小 smoke）。

## 6) Database & Secrets / 数据库与密钥

English:
- Database: PostgreSQL.
- Store secrets/keys/connection strings in `.env` (never commit real secrets).
- Read config via environment variables; provide `.env.example`.

中文：
- 数据库：PostgreSQL。
- 所有密钥、连接串、第三方配置存放在 `.env`（不要提交真实密钥）。
- 代码读取配置必须通过环境变量（并提供 `.env.example`）。

## 7) AI Backend / AI Backend

English:
- AI backend tokens must be stored in `.env`.
- Define clear degradation behavior for missing token / quota exhausted / timeout / failure so the main flow remains usable.

中文：
- AI backend 的 token 必须存放在 `.env`。
- 需要清晰的“无 token/无额度/超时/失败”降级策略，确保主流程可用。

## 8) Login & Subscription / 登录与订阅

English:
- Login: implement a basic account system and keep UX consistent across clients.
- Subscription: define a backend subscription state model + verification APIs; clients gate features gracefully.

中文：
- 登录和订阅需要在后端有明确模型与校验接口；前端根据订阅状态做能力门控（graceful）。

## 9) Codex as a Tool (Non-Interactive, Same Session) / 把 Codex 当成工具（非交互、同一 session）

English:
- Treat Codex as a non-interactive tool repeatedly invoked by scripts.
- Prefer a single long-lived session for stability; each call must do one small step and exit cleanly.
- When needed, grant full permissions (example):
  - `codex -s danger-full-access -a never exec ...`
- Each step must end with: logs/artifacts updated, `git commit`, `git push` (retry on failure and record cause).

中文：
- Codex non-interactive 整体上当成一个工具，不断调用它来完成整个任务；使用同一个 session。
- 每个小步结束必须：记录日志/产物、`git commit`、`git push`（失败要重试并写明原因）。

## 10) Pipeline Design Like Scratch (Composable Blocks) / Pipeline 设计成像 Scratch 一样的积木语言

English:
Design the pipeline as composable “blocks”; each step executes one block or a small sequence:
- Planning: read screenshots/markdown/reference code; produce step plan + acceptance.
- Implement: backend / pwa / android / ios (strict write boundaries).
- Debug: start services, run smoke checks; automation only with timeouts and clean shutdown.
- Verify: lint/build/tests/health checks/clickability checks.
- Release: commit/push (with retry), change summary, screenshot parity notes.
- Tooling: unified logs, structured outputs, failure localization, resumable state.
- Evaluation & cost: record step time, token/cost, failure rate, retries; optimize over time.

中文：
- 把 auto-development pipeline 设计成一个像 scratch 一样的编程语言：每个子模块（像 commit-push、调试、任务规划、循环、校验、工具、日志和评测）可组合、可复用、可续跑。

## Four Gaps to Close for a Long-Running Stable Agent / 长期稳定 Agent 的四件事（必须补齐）

English:
- Can do work (tools): scripted start/build/test/commit/rollback; resumable state machine; tmux/service management.
- No hallucination (RAG): retrieve real repo artifacts first (screenshots markdown, decompiled, SDK demo); validate key claims via grep and actual run results.
- Safe execution (guardrails): strict write boundaries, read-only reference paths, dangerous operation limits, timeout/exit strategies, avoid leftover background processes.
- Operable (logs/eval/cost): unified logs, observability, failure alerts, retrospectives, cost and efficiency metrics.

中文：
- 能做事（工具）
- 不瞎编（检索/RAG）
- 不乱搞（护栏+权限+审批）
- 可运营（日志+评测+成本控制）
