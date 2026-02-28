[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)




[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# AutoAppDev

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Backend](https://img.shields.io/badge/Backend-Tornado-222222)
![Frontend](https://img.shields.io/badge/Frontend-PWA-0A7EA4)
![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Self--Dev-51%2F55%20tasks%20done-2E8B57)
![i18n](https://img.shields.io/badge/i18n-11%20languages-1f6feb)
![Pipeline](https://img.shields.io/badge/Pipeline-Resumable-ff6b35)
![Docs](https://img.shields.io/badge/Docs-Workflow%20First-0e9f6e)
![Automation](https://img.shields.io/badge/Automation-README%20Pipeline-f97316)
![API](https://img.shields.io/badge/API-JSON%20HTTP-0ea5e9)
![State Machine](https://img.shields.io/badge/Lifecycle-start%2Fpause%2Fresume%2Fstop-f59e0b)
![Control Flow](https://img.shields.io/badge/Control%20Flow-Plan%20%E2%86%92%20Work%20%E2%86%92%20Verify%20%E2%86%92%20Summary-0f766e)

Reusable scripts + guides for building apps step-by-step from screenshots/markdown with Codex as a non-interactive tool.

> 🎯 **Sứ mệnh:** Làm cho quy trình phát triển ứng dụng trở nên có tính xác định rõ ràng, có thể tiếp tục, và hướng theo artifact.
>
> 🧩 **Nguyên tắc thiết kế:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Tín hiệu dự án

| Signal | Hướng phát triển hiện tại |
| --- | --- |
| Mô hình runtime | Backend Tornado + controller PWA tĩnh |
| Thực thi pipeline | Tất định và có thể tiếp tục (`start/pause/resume/stop`) |
| Chiến lược lưu trữ | PostgreSQL-first với hành vi fallback tương thích |
| Luồng tài liệu | README gốc canonical + các biến thể `i18n/` tự động |

### 🔗 Điều hướng nhanh

| Nhu cầu | Truy cập |
| --- | --- |
| Chạy local lần đầu | [⚡ Khởi Động Nhanh](#-khởi-động-nhanh) |
| Biến môi trường và biến cần thiết | [⚙️ Cấu Hình](#️-cấu-hình) |
| Bề mặt API | [📡 Ảnh Chụp Nhanh API](#-ảnh-chụp-nhanh-api) |
| Runbook vận hành/debug | [🧭 Runbook Vận Hành](#-runbook-vận-hành) |
| Quy tắc README/i18n | [🌐 Quy Trình README & i18n](#-quy-trình-readme--i18n) |
| Bảng xử lý sự cố | [🔧 Xử Lý Sự Cố](#-xử-lý-sự-cố) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Trạng thái tự phát triển (tự động cập nhật)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Tiến độ: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Triết lý: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Phần này được cập nhật bởi `scripts/auto-autoappdev-development.sh`.
Không chỉnh sửa nội dung giữa marker.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Mục lục
- [🚀 Tổng quan](#-tổng-quan)
- [🧭 Triết lý](#-triết-lý)
- [✨ Tính năng](#-tính-năng)
- [📌 Tóm tắt nhanh](#-tóm-tắt-nhanh)
- [🏗️ Kiến trúc](#-kiến-trúc)
- [📚 Nội dung](#-nội-dung)
- [🗂️ Cấu trúc dự án](#-cấu-trúc-dự-án)
- [✅ Điều kiện tiên quyết](#-điều-kiện-tiên-quyết)
- [🧩 Tương thích & giả định](#-tương-thích--giả-định)
- [🛠️ Cài đặt](#-cài-đặt)
- [⚡ Khởi động nhanh](#-khởi-động-nhanh)
- [⚙️ Cấu hình](#️-cấu-hình)
- [▶️ Sử dụng](#-sử-dụng)
- [🧭 Runbook vận hành](#-runbook-vận-hành)
- [📡 Ảnh chụp nhanh API](#-ảnh-chụp-nhanh-api)
- [🧪 Ví dụ](#-ví-dụ)
- [🧱 Ghi chú phát triển](#-ghi-chú-phát-triển)
- [🔐 Lưu ý an toàn](#-lưu-ý-an-toàn)
- [🔧 Xử lý sự cố](#-xử-lý-sự-cố)
- [🌐 Quy trình README & i18n](#-quy-trình-readme--i18n)
- [📘 Ngữ cảnh tạo README](#️-ngữ-cảnh-tạo-readme)
- [❓ FAQ](#-faq)
- [🗺️ Lộ trình](#-lộ-trình)
- [🤝 Đóng góp](#-đóng-góp)
- [❤️ Support](#-support)
- [📄 Giấy phép](#-giấy-phép)

## 🚀 Tổng quan
AutoAppDev là một dự án điều khiển pipeline phát triển ứng dụng chạy dài, có thể tạm dừng và tiếp tục lại. Nó kết hợp:

1. Backend API bằng Tornado với PostgreSQL làm persistence (kèm cơ chế fallback JSON cục bộ trong mã lưu trữ).
2. Giao diện controller PWA tĩnh theo phong cách Scratch.
3. Các script và tài liệu cho việc soạn pipeline, sinh mã deterministic, vòng lặp tự phát triển, và tự động hóa README.

Dự án này được tối ưu cho việc chạy agent theo trình tự chặt chẽ với lịch sử workflow dựa trên artifact.

### 🎨 Vì sao dự án này tồn tại

| Chủ đề | Ý nghĩa thực tế |
| --- | --- |
| Determinism | IR pipeline canonical + các workflow parser/import/codegen được thiết kế để tái lập tốt |
| Resumability | Mạy trạng thái vòng đời rõ ràng (`start/pause/resume/stop`) cho các lần chạy dài |
| Operability | Nhật ký runtime, inbox/outbox, và vòng lặp verify chạy bằng script |
| Documentation-first | Hợp đồng/specs/examples nằm trong `docs/`, cùng luồng README đa ngôn ngữ tự động |

## 🧭 Triết lý
AutoAppDev xem các agent như công cụ và giữ công việc ổn định nhờ vòng lặp nghiêm ngặt, có thể tiếp tục:

1. Plan
2. Implement
3. Debug/verify (có timeout)
4. Fix
5. Summarize + log
6. Commit + push

Ứng dụng controller hướng tới việc hiện thực các khái niệm tương tự kiểu Scratch block/action (bao gồm action mặc định `update_readme`) để mỗi workspace luôn luôn mới và có thể tái tạo.

### 🔁 Ý định trạng thái vòng đời

| Chuyển trạng thái | Mục đích vận hành |
| --- | --- |
| `start` | Bắt đầu pipeline từ trạng thái stopped/ready |
| `pause` | Tạm dừng thực thi dài hạn an toàn mà không mất ngữ cảnh |
| `resume` | Tiếp tục từ trạng thái/runtime artifact đã lưu |
| `stop` | Kết thúc thực thi và quay về trạng thái không chạy |

## ✨ Tính năng
- Điều khiển vòng đời pipeline có thể tiếp tục: start, pause, resume, stop.
- Thư viện API cho script pipeline AAPS (`.aaps`) và canonical IR (`autoappdev_ir` v1).
- Pipeline parser/import deterministic:
  - Parse script AAPS đã định dạng.
  - Import shell có chú thích qua comment `# AAPS:`.
  - Parse dự phòng bằng Codex (tùy chọn) (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Registry action với action tích hợp sẵn + action có thể chỉnh sửa (clone/edit cho built-in readonly).
- Scratch-like PWA blocks và action palette nạp động lúc runtime (`GET /api/actions`).
- Kênh messaging runtime:
  - Inbox (`/api/inbox`) cho định hướng từ operator -> pipeline.
  - Outbox (`/api/outbox`) gồm ingest file từ `runtime/outbox`.
- Stream log tăng dần từ backend và pipeline logs (`/api/logs`, `/api/logs/tail`).
- Sinh code runner deterministic từ canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev driver cho tiến hóa repo lặp lại (`scripts/auto-autoappdev-development.sh`).
- Pipeline tự động hóa README với scaffold đa ngôn ngữ trong `i18n/`.

## 📌 Tóm tắt nhanh

| Khu vực | Chi tiết |
| --- | --- |
| Runtime lõi | Tornado backend + frontend PWA tĩnh |
| Lưu trữ | PostgreSQL ưu tiên với hành vi tương thích trong `backend/storage.py` |
| Mô hình pipeline | Canonical IR (`autoappdev_ir` v1) và định dạng script AAPS |
| Luồng điều khiển | Vòng đời Start / Pause / Resume / Stop |
| Chế độ phát triển | Vòng lặp self-dev có thể tiếp tục + workflow script/codegen deterministic |
| README/i18n | Pipeline README tự động với scaffold `i18n/` |

## 🏗️ Kiến trúc

```text
Operator / Developer
        |
        v
   PWA (static files, pwa/)
        |
        | HTTP JSON API
        v
Tornado backend (backend/app.py)
        |
        +--> Postgres (DATABASE_URL)
        +--> runtime/ (logs, outbox, llm_parse artifacts)
        +--> scripts/ (pipeline runner + codegen helpers)
```

### Trách nhiệm backend
- Expose controller APIs cho scripts, actions, plan, pipeline lifecycle, logs, inbox/outbox, workspace config.
- Validate và lưu trữ pipeline script assets.
- Điều phối trạng thái chạy và chuyển trạng thái pipeline.
- Cung cấp hành vi fallback deterministic khi DB pool không khả dụng.

### Trách nhiệm frontend
- Render giao diện Scratch-like block và flow chỉnh sửa pipeline.
- Nạp action palette động từ backend registry.
- Điều khiển lifecycle controls và theo dõi status/logs/messages.

## 📚 Nội dung
Bản đồ tham chiếu cho các tài liệu, script và ví dụ được dùng nhiều nhất:

- `docs/auto-development-guide.md`: Triết lý và yêu cầu song ngữ (EN/ZH) cho agent tự phát triển chạy dài, có thể tiếp tục.
- `docs/ORDERING_RATIONALE.md`: Ví dụ lập luận sắp thứ tự theo screenshot.
- `docs/controller-mvp-scope.md`: Phạm vi MVP của controller (màn hình + APIs tối thiểu).
- `docs/end-to-end-demo-checklist.md`: Checklist demo end-to-end thủ công deterministic (happy path backend + PWA).
- `docs/env.md`: Quy ước biến môi trường (`.env`).
- `docs/api-contracts.md`: Hợp đồng request/response API cho controller.
- `docs/pipeline-formatted-script-spec.md`: Định dạng pipeline script chuẩn (AAPS) và canonical IR schema (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Generator deterministic cho runner bash có thể chạy được từ canonical IR.
- `docs/common-actions.md`: Hợp đồng/spec của các action phổ biến (bao gồm `update_readme`).
- `docs/workspace-layout.md`: Cấu trúc thư mục workspace chuẩn + hợp đồng (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Khởi động AutoAppDev (backend + PWA) trong tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Khởi động self-dev driver AutoAppDev trong tmux.
- `scripts/app-auto-development.sh`: Driver pipeline tuyến tính (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) với resume/state support.
- `scripts/generate_screenshot_docs.sh`: Generator mô tả screenshot -> markdown (Codex-driven).
- `scripts/setup_autoappdev_env.sh`: Script bootstrap môi trường conda chính cho chạy local.
- `scripts/setup_backend_env.sh`: Script hỗ trợ môi trường backend.
- `examples/ralph-wiggum-example.sh`: Ví dụ helper tự động hóa Codex CLI.

## 🗂️ Cấu trúc dự án
```text
AutoAppDev/
├── README.md
├── .env.example
├── .github/
│   └── FUNDING.yml
├── backend/
│   ├── app.py
│   ├── storage.py
│   ├── schema.sql
│   ├── apply_schema.py
│   ├── db_smoketest.py
│   ├── action_registry.py
│   ├── builtin_actions.py
│   ├── update_readme_action.py
│   ├── pipeline_parser.py
│   ├── pipeline_shell_import.py
│   ├── llm_assisted_parse.py
│   ├── workspace_config.py
│   ├── requirements.txt
│   └── README.md
├── pwa/
│   ├── index.html
│   ├── app.js
│   ├── i18n.js
│   ├── api-client.js
│   ├── styles.css
│   ├── service-worker.js
│   ├── manifest.json
│   └── README.md
├── docs/
├── scripts/
│   └── pipeline_codegen/
├── prompt_tools/
├── examples/
├── references/
├── i18n/
└── .auto-readme-work/
```

## ✅ Điều kiện tiên quyết
- OS có `bash`.
- Python `3.11+`.
- Conda (`conda`) cho các script setup có sẵn.
- `tmux` để khởi động backend+PWA hoặc self-dev bằng một lệnh.
- PostgreSQL truy cập được bởi `DATABASE_URL`.
- Tùy chọn: `codex` CLI cho luồng Codex (self-dev, parse-llm fallback, auto-readme pipeline).

Ma trận yêu cầu nhanh:

| Thành phần | Bắt buộc | Mục đích |
| --- | --- | --- |
| `bash` | Có | Thực thi script |
| Python `3.11+` | Có | Backend + tooling codegen |
| Conda | Có (luồng đề xuất) | Script bootstrap môi trường |
| PostgreSQL | Có (chế độ ưu tiên) | Lưu trữ chính qua `DATABASE_URL` |
| `tmux` | Khuyến nghị | Quản lý phiên backend/PWA và self-dev |
| `codex` CLI | Tùy chọn | Parse hỗ trợ LLM và tự động hóa README/self-dev |

## 🧩 Tương thích & giả định

| Chủ đề | Kỳ vọng hiện tại |
| --- | --- |
| OS local | Shell Linux/macOS là mục tiêu chính (`bash` scripts) |
| Python runtime | `3.11` (quản lý bởi `scripts/setup_autoappdev_env.sh`) |
| Chế độ lưu trữ | PostgreSQL là mặc định và được xem là canonical |
| Hành vi fallback | `backend/storage.py` có fallback JSON tương thích khi suy giảm |
| Mô hình mạng | Phát triển localhost split-port (backend + PWA tĩnh) |
| Công cụ agent | CLI `codex` là tùy chọn trừ khi dùng parse LLM hoặc tự động hóa self-dev |

Các giả định được dùng trong README này:
- Bạn chạy lệnh từ root repository trừ khi phần mô tả ghi khác.
- `.env` được cấu hình trước khi khởi động backend services.
- `conda` và `tmux` sẵn có cho các workflow một lệnh được đề xuất.

## 🛠️ Cài đặt
### 1) Clone và vào repo
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Cấu hình môi trường
```bash
cp .env.example .env
```
Chỉnh sửa `.env` và đặt tối thiểu:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` và `AUTOAPPDEV_PORT` (hoặc `PORT`)

### 3) Tạo/cập nhật môi trường backend
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) Áp dụng schema cơ sở dữ liệu
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) Tuỳ chọn: smoke test cơ sở dữ liệu
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Khởi động nhanh
```bash
# từ repo root
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Sau đó mở:
- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

Smoke-check bằng một lệnh:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Quick endpoint map:

| Surface | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Cấu hình
Primary file: `.env` (xem `docs/env.md` và `.env.example`).

### Biến quan trọng

| Biến | Mục đích |
| --- | --- |
| `SECRET_KEY` | Theo quy ước |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Thiết lập bind backend |
| `DATABASE_URL` | PostgreSQL DSN (ưu tiên) |
| `AUTOAPPDEV_RUNTIME_DIR` | Ghi đè runtime dir (mặc định `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Mục tiêu chạy pipeline mặc định |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Bật `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Mặc định Codex cho actions/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Dành cho tích hợp tương lai |

Kiểm tra nhanh `.env`:
```bash
bash -lc 'set -euo pipefail; test -f .env; set -a; source .env; set +a; \
python3 - <<"PY"\
import os, sys\
req = ["SECRET_KEY", "DATABASE_URL"]\
missing = [k for k in req if not os.getenv(k)]\
port_ok = bool(os.getenv("AUTOAPPDEV_PORT") or os.getenv("PORT"))\
if not port_ok: missing.append("AUTOAPPDEV_PORT or PORT")\
if missing:\
  print("Missing env:", ", ".join(missing))\
  sys.exit(1)\
print("OK: env looks set")\
PY'
```

## ▶️ Sử dụng

| Chế độ | Lệnh | Ghi chú |
| --- | --- | --- |
| Khởi động backend + PWA (đề xuất) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Chỉ chạy backend | `conda run -n autoappdev python -m backend.app` | Dùng `.env` bind + DB settings |
| Chỉ chạy PWA static server | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Hữu ích cho kiểm tra frontend riêng |
| Chạy self-dev driver trong tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Vòng lặp self-development có thể tiếp tục |

### Tùy chọn script thường dùng
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parse và lưu script
- Parse AAPS qua API: `POST /api/scripts/parse`
- Import annotated shell: `POST /api/scripts/import-shell`
- Parse LLM tùy chọn: `POST /api/scripts/parse-llm` (yêu cầu `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### Pipeline control APIs
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Các API hay dùng khác
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Xem `docs/api-contracts.md` để xem cấu trúc request/response.

## 🧭 Runbook vận hành

### Runbook: khởi chạy toàn bộ local stack
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Các mốc kiểm tra:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Mở `http://127.0.0.1:5173/` và xác nhận UI nạp được `/api/config`.
- Tùy chọn: mở `/api/version` và xác minh backend metadata mong đợi.

### Runbook: debug chỉ backend
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: deterministic codegen smoke
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
scripts/pipeline_codegen/smoke_placeholders.sh
scripts/pipeline_codegen/smoke_conditional_steps.sh
scripts/pipeline_codegen/smoke_meta_round_v0.sh
```

## 📡 Ảnh chụp nhanh API

Tổng quan nhóm API:

| Danh mục | Endpoints |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Mô hình plan | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| Workspace settings | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Ví dụ
### Ví dụ AAPS
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

Ví dụ đầy đủ:
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### Sinh runner deterministic
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Demo pipeline deterministic
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Sau đó dùng các nút Start/Pause/Resume/Stop trên PWA và kiểm tra `/api/logs`.

### Import từ annotated shell
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 Ghi chú phát triển
- Backend dùng Tornado và được thiết kế cho local dev ergonomics (kể cả CORS permissive cho localhost split port).
- Storage theo hướng PostgreSQL-first với hành vi tương thích trong `backend/storage.py`.
- Các khóa block của PWA và `STEP.block` trong script được cố tình đồng bộ (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Built-in actions là readonly; clone trước khi chỉnh sửa.
- `update_readme` action có ràng buộc path-safety cho các workspace README trong `auto-apps/<workspace>/README.md`.
- Có một số reference/path lịch sử (`HeyCyan`, `LightMind`) trong docs/scripts do evolution, đường dẫn canonical hiện tại là repository root.
- Thư mục gốc `i18n/` đã tồn tại. README theo ngôn ngữ được tạo dưới `i18n/` khi chạy đa ngôn ngữ.

### Working model and state files
- Runtime mặc định `./runtime` trừ khi `AUTOAPPDEV_RUNTIME_DIR` ghi đè.
- State/historic của self-dev tự động lưu ở `references/selfdev/`.
- Artifact của pipeline README lưu trong `.auto-readme-work/<timestamp>/`.

### Posture kiểm thử (hiện tại)
- Repository có smoke checks và deterministic demo scripts.
- Top-level automated test suite/CI manifest chưa được định nghĩa trong root metadata.
- Giả định: validation hiện tại chủ yếu script-driven (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, end-to-end checklist).

## 🔐 Lưu ý an toàn
- `update_readme` action được giới hạn có chủ đích cho workspace README target (`auto-apps/<workspace>/README.md`) với path traversal protections.
- Action registry validation chuẩn hóa các trường spec và giới hạn giá trị cho các mức reasoning được hỗ trợ.
- Scripts repo giả định chạy local tin cậy; kiểm tra nội dung script trước khi chạy trong môi trường chia sẻ hoặc gần production.
- `.env` có thể chứa giá trị nhạy cảm (`DATABASE_URL`, API keys). Đừng commit `.env` và dùng quản lý secret theo môi trường.

## 🔧 Xử lý sự cố

| Triệu chứng | Cần kiểm tra |
| --- | --- |
| `tmux not found` | Cài `tmux` hoặc chạy backend/PWA thủ công. |
| Backend fail lúc khởi động do thiếu env | Kiểm tra lại `.env` với `.env.example` và `docs/env.md`. |
| Lỗi database (kết nối/xác thực/schema) | Xác minh `DATABASE_URL`; chạy lại `conda run -n autoappdev python -m backend.apply_schema`; kiểm tra kết nối tùy chọn: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA load được nhưng không gọi API | Kiểm tra backend đang listen đúng host/port; tái tạo `pwa/config.local.js` bằng `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start trả về invalid transition | Kiểm tra trạng thái pipeline trước; bắt đầu từ `stopped`. |
| Không có log updates trong UI | Xác nhận `runtime/logs/pipeline.log` đang ghi; gọi trực tiếp `/api/logs` và `/api/logs/tail` để tách UI và backend. |
| LLM parse endpoint trả về disabled | Set `AUTOAPPDEV_ENABLE_LLM_PARSE=1` rồi restart backend. |
| `conda run -n autoappdev ...` bị lỗi | Chạy lại `./scripts/setup_autoappdev_env.sh`; xác nhận env conda `autoappdev` tồn tại (`conda env list`). |
| Sai API target ở frontend | Kiểm tra `pwa/config.local.js` có tồn tại và trỏ đúng backend host/port đang chạy. |

Để xác minh thủ công theo hướng deterministic, dùng `docs/end-to-end-demo-checklist.md`.

## 🌐 Quy trình README & i18n
- Root README là nguồn canonical dùng bởi pipeline tự động hóa README.
- Các biến thể đa ngôn ngữ nằm trong `i18n/`.
- Trạng thái thư mục i18n: ✅ có trong repository này.
- Bộ ngôn ngữ hiện tại:
  - `i18n/README.ar.md`
  - `i18n/README.de.md`
  - `i18n/README.es.md`
  - `i18n/README.fr.md`
  - `i18n/README.ja.md`
  - `i18n/README.ko.md`
  - `i18n/README.ru.md`
  - `i18n/README.vi.md`
  - `i18n/README.zh-Hans.md`
  - `i18n/README.zh-Hant.md`
- Thanh ngôn ngữ nên chỉ xuất hiện một dòng duy nhất ở đầu mỗi README variant (không trùng lặp).
- README pipeline entrypoint: `prompt_tools/auto-readme-pipeline.sh`.

### Ràng buộc sinh i18n (nghiêm ngặt)
- Luôn xử lý sinh đa ngôn ngữ khi cập nhật README canonical.
- Sinh/cập nhật files ngôn ngữ theo từng file một (sequential), không gom batch mơ hồ.
- Giữ đúng một dòng điều hướng ngôn ngữ ở đầu mỗi bản dịch.
- Không duplicate language bars trong cùng file.
- Giữ nguyên snippets lệnh, link, API paths, và ý định badge qua các bản dịch.

Thứ tự gợi ý sinh lần lượt:
1. `i18n/README.ar.md`
2. `i18n/README.de.md`
3. `i18n/README.es.md`
4. `i18n/README.fr.md`
5. `i18n/README.ja.md`
6. `i18n/README.ko.md`
7. `i18n/README.ru.md`
8. `i18n/README.vi.md`
9. `i18n/README.zh-Hans.md`
10. `i18n/README.zh-Hant.md`

Bảng ngôn ngữ:

| Ngôn ngữ | File |
| --- | --- |

## 📘 Ngữ cảnh tạo README

- Pipeline run timestamp: `20260301_064935`
- Trigger: `./README.md` first complete draft generation
- Input user prompt: `probe prompt`
- Goal: generate a complete, beautiful README draft with required sections and support information
- Source snapshot used:
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- File này được sinh từ nội dung repository và giữ vai trò canonical draft entry point.

## ❓ FAQ

### PostgreSQL có bắt buộc không?
Ưu tiên và kỳ vọng cho vận hành bình thường. Lớp storage có fallback compatibility behavior, nhưng môi trường dạng production-like nên giả định PostgreSQL có sẵn qua `DATABASE_URL`.

### Vì sao có cả `AUTOAPPDEV_PORT` và `PORT`?
`AUTOAPPDEV_PORT` là biến riêng của dự án. `PORT` tồn tại như alias phù hợp deployment. Giữ hai biến này đồng bộ trừ khi bạn chủ động override hành vi cho luồng launch.

### Nếu chỉ muốn inspect APIs thì bắt đầu từ đâu?
Chạy backend-only (`conda run -n autoappdev python -m backend.app`) rồi dùng `/api/health`, `/api/version`, `/api/config`, sau đó tới endpoints script/action trong `docs/api-contracts.md`.

### README đa ngôn ngữ có tự động sinh không?
Có. Repo có `prompt_tools/auto-readme-pipeline.sh`, và các bản ngôn ngữ được duy trì trong `i18n/` với một dòng điều hướng ngôn ngữ ở đầu mỗi variant.

## 🗺️ Lộ trình
- Hoàn tất các self-dev task còn lại ngoài mốc hiện tại `51 / 55`.
- Mở rộng workspace/materials/context tooling và tăng cường safe-path contracts.
- Tiếp tục cải thiện UX action palette và flow chỉnh sửa action.
- Mở rộng hỗ trợ README/UI đa ngôn ngữ trong `i18n/` và switching ngôn ngữ runtime.
- Nâng cấp smoke/integration checks và coverage CI (hiện có script-driven smoke checks; chưa có CI manifest đầy đủ ở root).
- Củng cố deterministic parser/import/codegen quanh AAPS v1 và canonical IR.

## 🤝 Đóng góp
Đóng góp được chào đón qua issues và pull requests.

Quy trình gợi ý:
1. Fork và tạo feature branch.
2. Giữ thay đổi tập trung và tái lập được.
3. Ưu tiên scripts/tests deterministic khi có thể.
4. Cập nhật docs khi thay đổi behavior/contracts (`docs/*`, API contracts, examples).
5. Mở PR cùng context, bước xác minh và giả định runtime.

Repository remotes hiện có:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Remote bổ sung có thể xuất hiện trong local clones cho repo liên quan (ví dụ trong workspace này: `novel`).

---

## 📄 Giấy phép
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

No root `LICENSE` file was detected in this repository snapshot.

Assumption note:
- Until a license file is added, treat usage/redistribution terms as unspecified and confirm with the maintainer.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
