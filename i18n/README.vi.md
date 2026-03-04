[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# AutoAppDev 🚀

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
![GitHub stars](https://img.shields.io/github/stars/lachlanchen/AutoAppDev?style=flat&logo=github&logoColor=white&color=%231DA1F2)
![GitHub forks](https://img.shields.io/github/forks/lachlanchen/AutoAppDev?style=flat&logo=github&logoColor=white&color=%2300A4A6)
![GitHub issues](https://img.shields.io/github/issues/lachlanchen/AutoAppDev?style=flat&logo=github&logoColor=white&color=%23ef4444)

---

Các script và hướng dẫn có thể tái sử dụng để xây dựng ứng dụng theo từng bước từ ảnh chụp màn hình/markdown với Codex như một công cụ không tương tác.

> 🎯 **Sứ mệnh:** Làm cho pipeline phát triển ứng dụng trở nên xác định, tiếp tục được, và hướng theo artifact.
>
> 🧩 **Nguyên tắc thiết kế:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ Tín hiệu dự án

| Tín hiệu           | Hướng đi hiện tại                                       |
| ------------------ | ------------------------------------------------------- |
| Mô hình chạy       | Backend Tornado + bộ điều khiển PWA tĩnh                |
| Thực thi pipeline  | Xác định và có thể tiếp tục (`start/pause/resume/stop`) |
| Chiến lược lưu trữ | PostgreSQL-first với hành vi dự phòng tương thích       |
| Luồng tài liệu     | README gốc canonical + các biến thể `i18n/` tự động     |

### 🔗 Điều hướng nhanh

| Nhu cầu                              | Truy cập                                               |
| ------------------------------------ | ------------------------------------------------------ |
| Chạy local lần đầu                   | [⚡ Khởi động nhanh](#-khởi-động-nhanh)                |
| Cấu hình môi trường và biến bắt buộc | [⚙️ Cấu hình](#️-cấu-hình)                              |
| Bề mặt API                           | [📡 Ảnh chụp nhanh API](#-ảnh-chụp-nhanh-api)          |
| Runbook vận hành/gỡ lỗi              | [🧭 Runbook vận hành](#-runbook-vận-hành)              |
| Quy tắc README/i18n                  | [🌐 Quy trình README & i18n](#-quy-trình-readme--i18n) |
| Bảng xử lý sự cố                     | [🔧 Xử lý sự cố](#-xử-lý-sự-cố)                        |

<!-- AUTOAPPDEV:STATUS:BEGIN -->

## Trạng thái tự phát triển (cập nhật tự động)

- Cập nhật: 2026-02-16T00:27:20Z
- Cam kết giai đoạn: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Tiến độ: 51 / 55 tác vụ đã hoàn thành
- Phiên làm việc Codex: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Triết lý: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Phần này được cập nhật bởi `scripts/auto-autoappdev-development.sh`.
Không chỉnh sửa nội dung giữa các marker.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Mục lục

- [🚀 Tổng quan](#-tổng-quan)
- [🧭 Tổng quan repository](#-tổng-quan-repository)
- [🧭 Triết lý](#-triết-lý)
- [✨ Tính năng](#-tính-năng)
- [📌 Tổng quan nhanh](#-tổng-quan-nhanh)
- [🏗️ Kiến trúc](#-kiến-trúc)
- [📚 Nội dung](#-nội-dung)
- [🗂️ Cấu trúc dự án](#-cấu-trúc-dự-án)
- [✅ Yêu cầu tiên quyết](#-yêu-cầu-tiên-quyết)
- [🧩 Tương thích & giả định](#-tương-thích--giả-định)
- [🛠️ Cài đặt](#-cài-đặt)
- [⚡ Khởi động nhanh](#-khởi-động-nhanh)
- [⚙️ Cấu hình](#️-cấu-hình)
- [▶️ Cách dùng](#-cách-dùng)
- [🧭 Runbook vận hành](#-runbook-vận-hành)
- [📡 Ảnh chụp nhanh API](#-ảnh-chụp-nhanh-api)
- [🧪 Ví dụ](#-ví-dụ)
- [🧱 Ghi chú phát triển](#-ghi-chú-phát-triển)
- [🔐 Lưu ý an toàn](#-lưu-ý-an-toàn)
- [🔧 Xử lý sự cố](#-xử-lý-sự-cố)
- [🌐 Quy trình README & i18n](#-quy-trình-readme--i18n)
- [📘 Bối cảnh tạo README](#-bối-cảnh-tạo-readme)
- [❓ FAQ](#-faq)
- [🗺️ Lộ trình](#-lộ-trình)
- [🤝 Đóng góp](#-đóng-góp)
- [❤️ Support](#-support)
- [📄 Giấy phép](#-giấy-phép)

## 🧭 Tổng quan repository

| Trọng tâm        | Thiết lập hiện tại                                         |
| ---------------- | ---------------------------------------------------------- |
| Vòng lặp cốt lõi | Plan → Work → Debug → Fix → Summary → Commit/Push          |
| Mô hình runtime  | Backend Tornado + bộ điều khiển PWA tĩnh                   |
| State machine    | `start` / `pause` / `resume` / `stop`                      |
| Lưu trữ          | PostgreSQL-first với cơ chế tương thích fallback JSON      |
| Tài liệu         | `README.md` canonical và các bản đa ngôn ngữ trong `i18n/` |

## 🚀 Tổng quan

AutoAppDev là một dự án điều khiển pipeline phát triển ứng dụng chạy dài, có thể tiếp tục. Nó kết hợp:

1. Một API backend Tornado với persistence PostgreSQL (cùng hành vi dự phòng JSON cục bộ trong mã lưu trữ).
2. Giao diện bộ điều khiển PWA tĩnh kiểu Scratch.
3. Các script và tài liệu cho việc biên soạn pipeline, sinh mã có tính xác định, vòng lặp tự phát triển và tự động hóa README.

Dự án được tối ưu cho việc chạy agent theo thứ tự nghiêm ngặt với lịch sử workflow dựa trên artifact.

### 🎨 Lý do dự án này tồn tại

| Chủ đề            | Ý nghĩa thực tế                                                                      |
| ----------------- | ------------------------------------------------------------------------------------ |
| Tính xác định     | Pipeline IR chuẩn + quy trình parser/import/codegen được thiết kế để có tính lặp lại |
| Khả năng tiếp tục | State machine vòng đời rõ ràng (`start/pause/resume/stop`) cho các lần chạy dài      |
| Khả năng vận hành | Nhật ký runtime, kênh inbox/outbox, và vòng lặp xác minh do script điều khiển        |
| Ưu tiên tài liệu  | Hợp đồng/specs/examples nằm trong `docs/`, cùng luồng README đa ngôn ngữ tự động     |

## 🧭 Triết lý

AutoAppDev coi agent như công cụ và giữ cho công việc ổn định qua vòng lặp nghiêm ngặt có thể tiếp tục:

1. Plan
2. Implement
3. Debug/verify (có timeout)
4. Fix
5. Summarize + log
6. Commit + push

Ứng dụng controller nhằm hiện thực cùng khái niệm như block/action theo kiểu Scratch (kể cả `update_readme` action chuẩn) để mỗi workspace luôn ở trạng thái cập nhật và tái lập được.

### 🔁 Ý định của state machine vòng đời

| Chuyển trạng thái | Mục đích vận hành                                       |
| ----------------- | ------------------------------------------------------- |
| `start`           | Bắt đầu một pipeline từ trạng thái stopped/ready        |
| `pause`           | Tạm dừng thực thi dài hạn an toàn mà không mất ngữ cảnh |
| `resume`          | Tiếp tục từ runtime state/artifact đã lưu               |
| `stop`            | Kết thúc thực thi và quay về trạng thái không chạy      |

## ✨ Tính năng

- Điều khiển vòng đời pipeline có thể tiếp tục: start, pause, resume, stop.
- API thư viện script cho pipeline AAPS (`.aaps`) và canonical IR (`autoappdev_ir` v1).
- Quy trình parser/import deterministic:
  - Parse script AAPS đã định dạng.
  - Import shell có annotation qua comment `# AAPS:`.
  - Parse dự phòng có hỗ trợ Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`) (tùy chọn).
- Registry action có action tích hợp sẵn + action có thể chỉnh sửa/biên tập (clone/edit flow cho built-ins readonly).
- PWA blocks kiểu Scratch và action palette tải động tại runtime (`GET /api/actions`).
- Kênh nhắn tin runtime:
  - Inbox (`/api/inbox`) cho hướng dẫn từ operator -> pipeline.
  - Outbox (`/api/outbox`) gồm ingest file queue từ `runtime/outbox`.
- Luồng log gia tăng từ backend và pipeline logs (`/api/logs`, `/api/logs/tail`).
- Sinh runner code deterministic từ canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Self-dev driver cho quá trình tiến hóa repo lặp đi lặp lại (`scripts/auto-autoappdev-development.sh`).
- Tự động hóa README qua pipeline với scaffold đa ngôn ngữ trong `i18n/`.

## 📌 Tổng quan nhanh

| Khu vực              | Chi tiết                                                                  |
| -------------------- | ------------------------------------------------------------------------- |
| Runtime lõi          | Backend Tornado + frontend PWA tĩnh                                       |
| Lưu trữ              | PostgreSQL ưu tiên với hành vi fallback trong `backend/storage.py`        |
| Mô hình pipeline     | Canonical IR (`autoappdev_ir` v1) và định dạng script AAPS                |
| Dòng chảy điều khiển | Vòng đời Start / Pause / Resume / Stop                                    |
| Chế độ phát triển    | Vòng lặp self-dev có thể tiếp tục + workflow script/codegen deterministic |
| README/i18n          | Pipeline README tự động với scaffold `i18n/`                              |

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

- Mở các API controller cho scripts, actions, plan, vòng đời pipeline, logs, inbox/outbox, cấu hình workspace.
- Kiểm tra và lưu trữ pipeline script assets.
- Điều phối trạng thái chạy và chuyển đổi trạng thái pipeline.
- Cung cấp hành vi fallback deterministic khi pool DB không sẵn sàng.

### Trách nhiệm frontend

- Render UI block kiểu Scratch và luồng chỉnh sửa pipeline.
- Tải action palette động từ registry backend.
- Điều khiển lifecycle controls và theo dõi status/logs/messages.

## 📚 Nội dung

Bản đồ tài liệu tham chiếu cho các tài liệu, script và ví dụ được dùng phổ biến:

- `docs/auto-development-guide.md`: Triết lý và yêu cầu song ngữ (EN/ZH) cho agent tự phát triển chạy dài, có thể tiếp tục.
- `docs/ORDERING_RATIONALE.md`: Lý giải ví dụ cho thứ tự bước dẫn xuất từ screenshot.
- `docs/controller-mvp-scope.md`: Phạm vi MVP controller (màn hình + các API tối thiểu).
- `docs/end-to-end-demo-checklist.md`: Checklist demo end-to-end thủ công deterministic (đường đi backend + PWA).
- `docs/env.md`: Quy ước biến môi trường (`.env`).
- `docs/api-contracts.md`: Hợp đồng request/response API cho controller.
- `docs/pipeline-formatted-script-spec.md`: Định dạng script pipeline chuẩn (AAPS) và schema IR chuẩn (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Bộ sinh mã deterministic cho runner bash chạy được từ canonical IR.
- `docs/common-actions.md`: Các hợp đồng/spec action phổ biến (bao gồm `update_readme`).
- `docs/workspace-layout.md`: Cấu trúc thư mục workspace chuẩn + hợp đồng (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Khởi động AutoAppDev (backend + PWA) trong tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Khởi động self-dev driver AutoAppDev trong tmux.
- `scripts/app-auto-development.sh`: Driver pipeline tuyến tính (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) với hỗ trợ resume/state.
- `scripts/generate_screenshot_docs.sh`: Trình sinh mô tả markdown từ screenshot (Codex-driven).
- `scripts/setup_autoappdev_env.sh`: Script bootstrap môi trường conda chính cho chạy local.
- `scripts/setup_backend_env.sh`: Script trợ giúp môi trường backend.
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

## ✅ Yêu cầu tiên quyết

- Hệ điều hành có `bash`.
- Python `3.11+`.
- Conda (`conda`) cho các script setup đi kèm.
- `tmux` để khởi động backend+PWA hoặc self-dev bằng một lệnh.
- PostgreSQL có thể truy cập thông qua `DATABASE_URL`.
- Tùy chọn: `codex` CLI cho luồng Codex (self-dev, parse-llm fallback, auto-readme pipeline).

Ma trận yêu cầu nhanh:

| Thành phần     | Bắt buộc            | Mục đích                                 |
| -------------- | ------------------- | ---------------------------------------- |
| `bash`         | Có                  | Thực thi script                          |
| Python `3.11+` | Có                  | Backend + công cụ codegen                |
| Conda          | Có (khuyến nghị)    | Bootstrap môi trường                     |
| PostgreSQL     | Có (chế độ ưu tiên) | Persistence chính qua `DATABASE_URL`     |
| `tmux`         | Khuyến nghị         | Quản lý session backend/PWA và self-dev  |
| `codex` CLI    | Tùy chọn            | Parse LLM và tự động hóa README/self-dev |

## 🧩 Tương thích & giả định

| Chủ đề             | Mong đợi hiện tại                                                             |
| ------------------ | ----------------------------------------------------------------------------- |
| Hệ điều hành local | Shell Linux/macOS là mục tiêu chính (`bash` scripts)                          |
| Runtime Python     | `3.11` (được quản lý bởi `scripts/setup_autoappdev_env.sh`)                   |
| Chế độ persistence | PostgreSQL được ưu tiên và được xem là canonical                              |
| Hành vi fallback   | `backend/storage.py` có JSON compatibility fallback cho các kịch bản degraded |
| Mô hình mạng       | Phát triển localhost split-port (backend + PWA tĩnh)                          |
| Công cụ agent      | `codex` CLI là tùy chọn trừ khi dùng parse LLM hoặc tự động hóa self-dev      |

Giả định trong README này:

- Bạn chạy lệnh từ root repo trừ khi section chỉ định khác.
- `.env` được cấu hình trước khi khởi động dịch vụ backend.
- `conda` và `tmux` khả dụng cho luồng gợi ý một lệnh.

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

Chỉnh sửa `.env` và thiết lập ít nhất:

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

### 5) Kiểm thử cơ sở dữ liệu (tùy chọn)

```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Khởi động nhanh

```bash
# từ root repo
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Sau đó mở:

- PWA: `http://127.0.0.1:5173/`
- Backend API base: `http://127.0.0.1:8788`
- Health check: `http://127.0.0.1:8788/api/health`

Kiểm tra nhanh bằng một lệnh:

```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Bản đồ endpoint nhanh:

| Mặt phẳng       | URL                                |
| --------------- | ---------------------------------- |
| UI PWA          | `http://127.0.0.1:5173/`           |
| Backend API     | `http://127.0.0.1:8788`            |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Cấu hình

Tệp chính: `.env` (xem `docs/env.md` và `.env.example`).

### Biến quan trọng

| Biến                                                                                      | Mục đích                                   |
| ----------------------------------------------------------------------------------------- | ------------------------------------------ |
| `SECRET_KEY`                                                                              | Yêu cầu theo quy ước                       |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT`                                              | Cài đặt bind backend                       |
| `DATABASE_URL`                                                                            | PostgreSQL DSN (ưu tiên)                   |
| `AUTOAPPDEV_RUNTIME_DIR`                                                                  | Ghi đè runtime dir (mặc định `./runtime`)  |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT`                                   | Pipeline chạy mặc định                     |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1`                                                           | Bật `/api/scripts/parse-llm`               |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Giá trị mặc định Codex cho action/endpoint |
| `AI_API_BASE_URL`, `AI_API_KEY`                                                           | Dành cho tích hợp tương lai                |

Xác thực nhanh `.env`:

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

## ▶️ Cách dùng

| Chế độ                                | Lệnh                                                     | Ghi chú                                                       |
| ------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| Khởi động backend + PWA (khuyến nghị) | `./scripts/run_autoappdev_tmux.sh --restart`             | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Khởi động riêng backend               | `conda run -n autoappdev python -m backend.app`          | Dùng bind và DB settings từ `.env`                            |
| Chỉ chạy máy chủ PWA tĩnh             | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Hữu ích cho kiểm tra frontend-only                            |
| Chạy self-dev driver trong tmux       | `./scripts/run_autoappdev_selfdev_tmux.sh --restart`     | Vòng lặp tự phát triển có thể tiếp tục                        |

### Tùy chọn script thường dùng

- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parse và lưu trữ scripts

- Parse AAPS qua API: `POST /api/scripts/parse`
- Import shell có annotation: `POST /api/scripts/import-shell`
- Parse LLM tùy chọn: `POST /api/scripts/parse-llm` (yêu cầu `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### Pipeline control APIs

- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### Các API thường dùng khác

- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Xem `docs/api-contracts.md` để xem shapes của request/response.

## 🧭 Runbook vận hành

### Runbook: bật full local stack

```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Validation checkpoints:

- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Mở `http://127.0.0.1:5173/` và xác nhận UI có tải được `/api/config`.
- Tùy chọn: mở `/api/version` và xác minh metadata backend mong đợi được trả về.

### Runbook: debug backend-only

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

Các nhóm API quan trọng:

| Nhóm                  | Endpoints                                                                                                                                                       |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config`                                                                                    |
| Plan model            | `GET /api/plan`, `POST /api/plan`                                                                                                                               |
| Scripts               | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm`         |
| Action registry       | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme`                                  |
| Pipeline runtime      | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs      | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail`                                            |
| Workspace settings    | `GET/POST /api/workspaces/<name>/config`                                                                                                                        |

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

Sau đó dùng điều khiển Start/Pause/Resume/Stop trên PWA và kiểm tra `/api/logs`.

### Import từ shell có annotation

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

- Backend dựa trên Tornado và thiết kế cho ergonomics local dev (bao gồm CORS tương đối rộng cho split-port localhost).
- Lưu trữ là PostgreSQL-first với hành vi fallback trong `backend/storage.py`.
- Khóa block ở PWA và giá trị `STEP.block` của script được căn chỉnh có chủ đích (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Action tích hợp sẵn là readonly; cần clone trước khi chỉnh sửa.
- Action `update_readme` có ràng buộc path-safety cho các target README workspace dưới `auto-apps/<workspace>/README.md`.
- Có một số tham chiếu tên/path lịch sử trong docs/scripts (`HeyCyan`, `LightMind`) do tiến hóa dự án. Đường dẫn canonical hiện tại là root repository này.
- Thư mục `i18n/` ở root đã tồn tại. Tệp README theo từng ngôn ngữ dự kiến nằm trong `i18n/` trong các lần chạy đa ngôn ngữ.

### Mô hình hoạt động và state files

- Runtime mặc định là `./runtime` trừ khi ghi đè bởi `AUTOAPPDEV_RUNTIME_DIR`.
- State/historic của tự động hóa self-dev được theo dõi tại `references/selfdev/`.
- README pipeline artifacts được ghi lại trong `.auto-readme-work/<timestamp>/`.

### Tư thế kiểm chứng hiện tại

- Repository có smoke checks và deterministic demo scripts.
- Chưa có test suite/CI manifest đầy đủ ở cấp root metadata.
- Giả định: validation chủ yếu do script điều khiển hiện tại (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, end-to-end checklist).

## 🔐 Lưu ý an toàn

- Action `update_readme` có ràng buộc intentional đến các target README workspace (`auto-apps/<workspace>/README.md`) với bảo vệ chống path traversal.
- Validation trong action registry áp đặt chuẩn hóa trường spec action và giá trị giới hạn cho các mức reasoning được hỗ trợ.
- Script repository giả định chạy trên môi trường local tin cậy; hãy xem trước nội dung script trước khi chạy trong môi trường chia sẻ hoặc gần production.
- `.env` có thể chứa giá trị nhạy cảm (`DATABASE_URL`, API keys). Giữ `.env` không commit và dùng quản lý secret phù hợp theo môi trường.

## 🔧 Xử lý sự cố

| Triệu chứng                                          | Nên kiểm tra                                                                                                                                                             |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tmux not found`                                     | Cài `tmux` hoặc chạy backend/PWA thủ công.                                                                                                                               |
| Backend khởi động thất bại do thiếu env              | Kiểm tra lại `.env` theo `.env.example` và `docs/env.md`.                                                                                                                |
| Lỗi DB (kết nối/xác thực/schema)                     | Kiểm tra `DATABASE_URL`; chạy lại `conda run -n autoappdev python -m backend.apply_schema`; kiểm tra tùy chọn: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA tải được nhưng không gọi API                     | Đảm bảo backend đang nghe đúng host/port; tái tạo `pwa/config.local.js` bằng cách chạy lại `./scripts/run_autoappdev_tmux.sh`.                                           |
| Pipeline Start trả về chuyển trạng thái không hợp lệ | Kiểm tra trạng thái pipeline hiện tại; bắt đầu từ `stopped`.                                                                                                             |
| Không có cập nhật log trên UI                        | Xác nhận `runtime/logs/pipeline.log` đang được ghi; dùng trực tiếp `/api/logs` và `/api/logs/tail` để tách ranh giới UI vs backend.                                      |
| Endpoint parse LLM báo disabled                      | Đặt `AUTOAPPDEV_ENABLE_LLM_PARSE=1` rồi khởi động lại backend.                                                                                                           |
| `conda run -n autoappdev ...` lỗi                    | Chạy lại `./scripts/setup_autoappdev_env.sh`; xác nhận env conda `autoappdev` tồn tại (`conda env list`).                                                                |
| Sai API target ở frontend                            | Xác nhận `pwa/config.local.js` tồn tại và trỏ đúng backend host/port đang hoạt động.                                                                                     |

Để có đường kiểm chứng thủ công deterministic, dùng `docs/end-to-end-demo-checklist.md`.

## 🌐 Quy trình README & i18n

- README gốc là nguồn chuẩn dùng bởi pipeline tự động README.
- Variants đa ngôn ngữ dự kiến nằm trong `i18n/`.
- Trạng thái i18n: ✅ có trong repository này.
- Bộ ngôn ngữ hiện tại trong repo này:
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
- Thanh ngôn ngữ phải là một dòng duy nhất ở đầu mỗi bản README (không lặp lại).
- Điểm vào pipeline README: `prompt_tools/auto-readme-pipeline.sh`.

### Ràng buộc tạo i18n (nghiêm ngặt)

- Luôn chạy quy trình đa ngôn ngữ khi cập nhật nội dung README canonical.
- Tạo/cập nhật từng ngôn ngữ tuần tự (một file một lần), không chạy hàng loạt mơ hồ.
- Giữ đúng một dòng language-options duy nhất ở đầu mỗi bản dịch.
- Không trùng lặp language bars trong cùng một file.
- Bảo toàn snippets, links, API paths và ý nghĩa badge giữa các bản dịch.

Thứ tự gợi ý sinh một-một:

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

| Language | File                |
| -------- | ------------------- |
| Arabic   | `i18n/README.ar.md` |

Ghi chú quan sát trong workspace:

- `i18n/README.zh-Hant.md.tmp` có thể xuất hiện như artifact dịch tạm thời; file canonical cuối cùng nên giữ dạng `README.<lang>.md`.

## 📘 Bối cảnh tạo README

- Pipeline run timestamp: `20260301_095119`
- Trigger: `./README.md` first complete draft generation (canonical-base incremental update)
- Input user prompt: `Use current README as canonical base. No reduction: only increment and improve. Preserve existing content, links, badges, commands, and details. Always process multilingual generation (do not skip): ensure i18n exists and generate/update language files one-by-one with a single language-options line at the top and no duplicates.`
- Mục tiêu: tạo bản README hoàn chỉnh, đẹp, có đủ section yêu cầu và thông tin support
- Snapshot nguồn sử dụng:
  - `./.auto-readme-work/20260301_095119/pipeline-context.md`
  - `./.auto-readme-work/20260301_095119/repo-structure-analysis.md`
- File này được tạo từ nội dung repository và được giữ lại như điểm vào cho bản nháp canonical.

## ❓ FAQ

### PostgreSQL có bắt buộc không?

Ưu tiên và mong đợi cho vận hành bình thường. Lớp lưu trữ có hành vi fallback compatibility, nhưng dùng production-like nên giả định PostgreSQL khả dụng qua `DATABASE_URL`.

### Tại sao có cả `AUTOAPPDEV_PORT` lẫn `PORT`?

`AUTOAPPDEV_PORT` là project-specific. `PORT` tồn tại như alias thân thiện khi deploy. Giữ hai biến đồng nhất trừ khi bạn cố tình override behavior theo đường chạy launch.

### Nên bắt đầu từ đâu nếu chỉ muốn kiểm tra APIs?

Chạy backend-only (`conda run -n autoappdev python -m backend.app`) rồi dùng `/api/health`, `/api/version`, `/api/config`, sau đó tới các endpoint script/action trong `docs/api-contracts.md`.

### READMEs đa ngôn ngữ có tạo tự động không?

Có. Repo có `prompt_tools/auto-readme-pipeline.sh`, và các bản dịch ngôn ngữ được duy trì trong `i18n/` với đúng một dòng navigation ngôn ngữ ở đầu mỗi bản.

## 🗺️ Lộ trình

- Hoàn thành các self-dev task còn lại ngoài `51 / 55` hiện tại.
- Mở rộng tooling workspace/materials/context và hợp đồng an toàn đường dẫn mạnh hơn.
- Tiếp tục cải thiện action palette UX và quy trình chỉnh sửa action có thể biên tập.
- Mở rộng hỗ trợ README/UI đa ngôn ngữ trên `i18n/` và runtime language switching.
- Củng cố smoke/integration checks và CI coverage (hiện có smoke checks bằng script; chưa có CI manifest đầy đủ tại root).
- Tiếp tục tăng cường tính xác định của parser/import/codegen quanh AAPS v1 và canonical IR.

## 🤝 Đóng góp

Đóng góp hoan nghênh qua issues và pull requests.

Quy trình gợi ý:

1. Fork và tạo feature branch.
2. Giữ thay đổi tập trung và tái lập được.
3. Ưu tiên scripts/tests deterministic khi có thể.
4. Cập nhật docs khi hành vi/hợp đồng thay đổi (`docs/*`, API contracts, examples).
5. Mở PR với context, bước xác thực, và giả định runtime.

Remote của repository hiện tại bao gồm:

- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Có thể có remote bổ sung trong các clone local cho repo liên quan (ví dụ trong workspace: `novel`).

---

## 📄 Giấy phép

![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

Không có file `LICENSE` gốc được phát hiện trong snapshot repository này.

Ghi chú giả định:

- Cho đến khi file license được thêm vào, hãy xem điều khoản sử dụng/phân phối là chưa xác định và xác thực với maintainer.

## ❤️ Support

| Donate                                                                                                                                                                                                                                                                                                                                                     | PayPal                                                                                                                                                                                                                                                                                                                                                          | Stripe                                                                                                                                                                                                                                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
