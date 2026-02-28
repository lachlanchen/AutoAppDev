[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


<p align="center">
  <img src="https://raw.githubusercontent.com/lachlanchen/lachlanchen/main/figs/banner.png" alt="LazyingArt banner" />
</p>

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

Bộ script và hướng dẫn có thể tái sử dụng để xây dựng ứng dụng từng bước từ ảnh chụp màn hình/markdown, dùng Codex như một công cụ không tương tác.

> 🎯 **Sứ mệnh:** Biến pipeline phát triển ứng dụng thành quy trình tất định, có thể tiếp tục, và dựa trên hiện vật.
>
> 🧩 **Nguyên tắc thiết kế:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🔗 Điều hướng nhanh

| Nhu cầu | Đi tới |
| --- | --- |
| Chạy cục bộ lần đầu | [⚡ Quick Start](#-quick-start) |
| Môi trường và biến bắt buộc | [⚙️ Configuration](#️-configuration) |
| Bề mặt API | [📡 API Snapshot](#-api-snapshot) |
| Playbook vận hành/gỡ lỗi | [🧭 Operational Runbooks](#-operational-runbooks) |
| Quy tắc sinh README/i18n | [🌐 README & i18n Workflow](#-readme--i18n-workflow) |
| Ma trận xử lý sự cố | [🔧 Troubleshooting](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Trạng thái Self-Dev (tự động cập nhật)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Phần này được cập nhật bởi `scripts/auto-autoappdev-development.sh`.
Không chỉnh sửa nội dung giữa các marker.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Mục lục
- [🚀 Tổng quan](#-tổng-quan)
- [🧭 Triết lý](#-triết-lý)
- [✨ Tính năng](#-tính-năng)
- [📌 Nhìn nhanh](#-nhìn-nhanh)
- [🏗️ Kiến trúc](#️-kiến-trúc)
- [📚 Nội dung](#-nội-dung)
- [🗂️ Cấu trúc dự án](#️-cấu-trúc-dự-án)
- [✅ Điều kiện tiên quyết](#-điều-kiện-tiên-quyết)
- [🧩 Tương thích & giả định](#-tương-thích--giả-định)
- [🛠️ Cài đặt](#️-cài-đặt)
- [⚡ Khởi động nhanh](#-khởi-động-nhanh)
- [⚙️ Cấu hình](#️-cấu-hình)
- [▶️ Sử dụng](#️-sử-dụng)
- [🧭 Runbook vận hành](#-runbook-vận-hành)
- [📡 Ảnh chụp API](#-ảnh-chụp-api)
- [🧪 Ví dụ](#-ví-dụ)
- [🧱 Ghi chú phát triển](#-ghi-chú-phát-triển)
- [🔐 Ghi chú an toàn](#-ghi-chú-an-toàn)
- [🔧 Xử lý sự cố](#-xử-lý-sự-cố)
- [🌐 Quy trình README & i18n](#-quy-trình-readme--i18n)
- [❓ Câu hỏi thường gặp](#-câu-hỏi-thường-gặp)
- [🗺️ Lộ trình](#️-lộ-trình)
- [🤝 Đóng góp](#-đóng-góp)
- [🙌 Hỗ trợ](#-hỗ-trợ)
- [📄 Giấy phép](#-giấy-phép)
- [❤️ Tài trợ & quyên góp](#️-tài-trợ--quyên-góp)

## 🚀 Tổng quan
AutoAppDev là dự án điều phối cho các pipeline phát triển ứng dụng chạy dài hạn, có thể tiếp tục. Dự án kết hợp:

1. API backend Tornado với cơ chế lưu trữ dựa trên PostgreSQL (kèm fallback JSON cục bộ trong mã storage).
2. Giao diện điều khiển PWA tĩnh kiểu Scratch.
3. Script và tài liệu cho viết pipeline, sinh mã tất định, vòng lặp self-dev, và tự động hóa README.

Dự án được tối ưu cho việc thực thi agent có thể dự đoán, với tuần tự nghiêm ngặt và lịch sử quy trình theo định hướng hiện vật.

### 🎨 Vì sao repo này tồn tại

| Chủ đề | Ý nghĩa trong thực tế |
| --- | --- |
| Tính tất định | Pipeline IR chuẩn + luồng parser/import/codegen được thiết kế để lặp lại ổn định |
| Khả năng tiếp tục | State machine vòng đời rõ ràng (`start/pause/resume/stop`) cho các lần chạy dài |
| Tính vận hành | Log runtime, kênh inbox/outbox, và vòng lặp xác minh theo script |
| Tài liệu trước tiên | Contract/spec/example nằm trong `docs/`, kèm luồng README đa ngôn ngữ tự động |

## 🧭 Triết lý
AutoAppDev xem agent là công cụ và giữ công việc ổn định bằng một vòng lặp nghiêm ngặt, có thể tiếp tục:

1. Plan
2. Implement
3. Debug/verify (với timeout)
4. Fix
5. Summarize + log
6. Commit + push

Ứng dụng controller hướng tới việc hiện thực cùng những khái niệm này dưới dạng block/action kiểu Scratch (bao gồm action chung `update_readme`) để mỗi workspace luôn cập nhật và tái tạo được.

### 🔁 Mục tiêu trạng thái vòng đời

| Chuyển trạng thái | Mục tiêu vận hành |
| --- | --- |
| `start` | Bắt đầu pipeline từ trạng thái dừng/sẵn sàng |
| `pause` | Tạm dừng thực thi dài hạn an toàn mà không mất ngữ cảnh |
| `resume` | Tiếp tục từ trạng thái runtime/hiện vật đã lưu |
| `stop` | Kết thúc thực thi và quay về trạng thái không chạy |

## ✨ Tính năng
- Điều khiển vòng đời pipeline có thể tiếp tục: start, pause, resume, stop.
- API thư viện script cho AAPS pipeline scripts (`.aaps`) và IR chuẩn (`autoappdev_ir` v1).
- Pipeline parser/import tất định:
  - Parse script AAPS đã được định dạng.
  - Import shell có chú thích qua comment `# AAPS:`.
  - Fallback parse có hỗ trợ Codex (tùy chọn) (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Action registry với action built-in + action tùy chỉnh/chỉnh sửa (luồng clone/edit cho built-in chỉ đọc).
- Block PWA kiểu Scratch và action palette nạp lúc chạy (`GET /api/actions`).
- Kênh nhắn tin runtime:
  - Inbox (`/api/inbox`) cho hướng dẫn operator -> pipeline.
  - Outbox (`/api/outbox`) gồm cả ingest hàng đợi tệp từ `runtime/outbox`.
- Stream log tăng dần từ backend và pipeline (`/api/logs`, `/api/logs/tail`).
- Sinh mã runner tất định từ IR chuẩn (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev cho tiến hóa repository theo vòng lặp (`scripts/auto-autoappdev-development.sh`).
- Pipeline tự động README với khung sinh đa ngôn ngữ trong `i18n/`.

## 📌 Nhìn nhanh

| Khu vực | Chi tiết |
| --- | --- |
| Runtime cốt lõi | Backend Tornado + frontend PWA tĩnh |
| Lưu trữ | Ưu tiên PostgreSQL với hành vi tương thích trong `backend/storage.py` |
| Mô hình pipeline | IR chuẩn (`autoappdev_ir` v1) và định dạng script AAPS |
| Luồng điều khiển | Vòng đời Start / Pause / Resume / Stop |
| Chế độ dev | Vòng lặp self-dev có thể tiếp tục + luồng script/codegen tất định |
| README/i18n | Pipeline README tự động với khung `i18n/` |

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
- Cung cấp API điều khiển cho scripts, actions, plan, vòng đời pipeline, logs, inbox/outbox, cấu hình workspace.
- Xác thực và lưu trữ các tài sản script pipeline.
- Điều phối trạng thái thực thi pipeline và chuyển trạng thái status.
- Cung cấp fallback tất định khi DB pool không khả dụng.

### Trách nhiệm frontend
- Render UI block kiểu Scratch và luồng chỉnh sửa pipeline.
- Nạp action palette động từ registry backend.
- Điều khiển vòng đời và theo dõi trạng thái/log/tin nhắn.

## 📚 Nội dung
Bản đồ tham chiếu cho các tài liệu, script và ví dụ được dùng thường xuyên nhất:

- `docs/auto-development-guide.md`: Triết lý và yêu cầu song ngữ (EN/ZH) cho một agent auto-development chạy dài hạn, có thể tiếp tục.
- `docs/ORDERING_RATIONALE.md`: Ví dụ lập luận cho việc sắp xếp các bước theo ảnh chụp màn hình.
- `docs/controller-mvp-scope.md`: Phạm vi MVP của controller (màn hình + API tối thiểu).
- `docs/end-to-end-demo-checklist.md`: Checklist demo end-to-end thủ công tất định (happy path backend + PWA).
- `docs/env.md`: Quy ước biến môi trường (`.env`).
- `docs/api-contracts.md`: Contract request/response API cho controller.
- `docs/pipeline-formatted-script-spec.md`: Định dạng script pipeline chuẩn (AAPS) và schema IR chuẩn (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Trình sinh tất định để tạo bash pipeline runner có thể chạy từ IR chuẩn.
- `docs/common-actions.md`: Contract/spec action dùng chung (bao gồm `update_readme`).
- `docs/workspace-layout.md`: Thư mục workspace chuẩn + contract (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Khởi động ứng dụng AutoAppDev (backend + PWA) trong tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Khởi động driver self-dev AutoAppDev trong tmux.
- `scripts/app-auto-development.sh`: Driver pipeline tuyến tính (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) có hỗ trợ resume/state.
- `scripts/generate_screenshot_docs.sh`: Trình sinh mô tả markdown từ screenshot (do Codex điều khiển).
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
- Hệ điều hành có `bash`.
- Python `3.11+`.
- Conda (`conda`) cho các script setup đi kèm.
- `tmux` cho các phiên backend+PWA hoặc self-dev chạy bằng một lệnh.
- PostgreSQL có thể truy cập qua `DATABASE_URL`.
- Tùy chọn: `codex` CLI cho các luồng dùng Codex (self-dev, parse-llm fallback, pipeline auto-readme).

Ma trận yêu cầu nhanh:

| Thành phần | Bắt buộc | Mục đích |
| --- | --- | --- |
| `bash` | Có | Thực thi script |
| Python `3.11+` | Có | Backend + công cụ codegen |
| Conda | Có (luồng khuyến nghị) | Script bootstrap môi trường |
| PostgreSQL | Có (chế độ ưu tiên) | Lưu trữ chính qua `DATABASE_URL` |
| `tmux` | Khuyến nghị | Quản lý phiên backend/PWA và self-dev |
| `codex` CLI | Tùy chọn | Parse có hỗ trợ LLM và tự động README/self-dev |

## 🧩 Tương thích & giả định

| Chủ đề | Kỳ vọng hiện tại |
| --- | --- |
| Hệ điều hành cục bộ | Shell Linux/macOS là mục tiêu chính (script `bash`) |
| Python runtime | `3.11` (được quản lý bởi `scripts/setup_autoappdev_env.sh`) |
| Chế độ lưu trữ | PostgreSQL được ưu tiên và xem là chuẩn chính |
| Hành vi fallback | `backend/storage.py` có fallback tương thích JSON cho tình huống suy giảm |
| Mô hình mạng | Phát triển localhost tách cổng (backend + static PWA) |
| Công cụ agent | `codex` CLI là tùy chọn trừ khi dùng parse hỗ trợ LLM hoặc tự động self-dev |

Các giả định dùng trong README này:
- Bạn chạy lệnh từ root repository trừ khi một phần có ghi khác.
- `.env` đã cấu hình trước khi khởi động dịch vụ backend.
- Có sẵn `conda` và `tmux` cho các luồng một-lệnh được khuyến nghị.

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
Sửa `.env` và đặt tối thiểu:
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

### 5) Tùy chọn: smoke test database
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Khởi động nhanh
```bash
# from repo root
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

Bản đồ endpoint nhanh:

| Bề mặt | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Cấu hình
Tệp chính: `.env` (xem `docs/env.md` và `.env.example`).

### Biến quan trọng

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Bắt buộc theo quy ước |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Thiết lập bind backend |
| `DATABASE_URL` | PostgreSQL DSN (ưu tiên) |
| `AUTOAPPDEV_RUNTIME_DIR` | Ghi đè runtime dir (mặc định `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Mục tiêu chạy pipeline mặc định |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Bật `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Mặc định Codex cho actions/endpoints |
| `AI_API_BASE_URL`, `AI_API_KEY` | Dành riêng cho tích hợp tương lai |

Xác minh nhanh `.env`:
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
| Khởi động backend + PWA (khuyến nghị) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Chỉ khởi động backend | `conda run -n autoappdev python -m backend.app` | Dùng cấu hình bind + DB trong `.env` |
| Chỉ khởi động static server cho PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Hữu ích cho kiểm tra frontend |
| Chạy self-dev driver trong tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Vòng lặp self-development có thể tiếp tục |

### Tùy chọn script thường dùng
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parse và lưu script
- Parse AAPS qua API: `POST /api/scripts/parse`
- Import shell có chú thích: `POST /api/scripts/import-shell`
- Parse LLM (tùy chọn): `POST /api/scripts/parse-llm` (cần `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### API điều khiển pipeline
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### API thường dùng khác
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

Xem `docs/api-contracts.md` để biết cấu trúc request/response.

## 🧭 Runbook vận hành

### Runbook: dựng toàn bộ stack local
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Các mốc xác minh:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Mở `http://127.0.0.1:5173/` và xác nhận UI có thể tải `/api/config`.
- Tùy chọn: mở `/api/version` và xác minh metadata backend mong đợi được trả về.

### Runbook: gỡ lỗi chỉ backend
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: smoke codegen tất định
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

## 📡 Ảnh chụp API

Các nhóm API cốt lõi trong một bảng:

| Danh mục | Endpoint |
| --- | --- |
| Health + runtime info | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Plan model | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Pipeline runtime | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
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

### Sinh runner tất định
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Demo pipeline tất định
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
Sau đó dùng các điều khiển Start/Pause/Resume/Stop trong PWA và kiểm tra `/api/logs`.

### Import từ shell có chú thích
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
- Backend dùng Tornado và được thiết kế ưu tiên trải nghiệm dev local (bao gồm CORS thoáng cho localhost tách cổng).
- Lưu trữ ưu tiên PostgreSQL với hành vi tương thích trong `backend/storage.py`.
- Khóa block PWA và giá trị `STEP.block` của script được chủ ý đồng bộ (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Action built-in ở chế độ chỉ đọc; hãy clone trước khi chỉnh sửa.
- Action `update_readme` bị giới hạn an toàn đường dẫn cho mục tiêu README workspace dưới `auto-apps/<workspace>/README.md`.
- Có tham chiếu lịch sử về đường dẫn/tên trong một số docs/scripts (`HeyCyan`, `LightMind`) kế thừa từ quá trình tiến hóa dự án. Đường dẫn chuẩn hiện tại là root repo này.
- Thư mục `i18n/` ở root đã tồn tại. Tệp README ngôn ngữ được kỳ vọng đặt tại đây trong các lần chạy đa ngôn ngữ.

### Mô hình làm việc và tệp trạng thái
- Runtime mặc định là `./runtime` trừ khi ghi đè bằng `AUTOAPPDEV_RUNTIME_DIR`.
- Trạng thái/lịch sử tự động self-dev được theo dõi dưới `references/selfdev/`.
- Hiện vật pipeline README được ghi lại dưới `.auto-readme-work/<timestamp>/`.

### Tư thế kiểm thử (hiện tại)
- Repository có các smoke check và script demo tất định.
- Chưa có bộ kiểm thử tự động cấp root/manifest CI đầy đủ trong metadata root.
- Giả định: xác minh hiện chủ yếu theo script (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, checklist end-to-end).

## 🔐 Ghi chú an toàn
- Action `update_readme` được giới hạn có chủ đích vào các mục tiêu README workspace (`auto-apps/<workspace>/README.md`) với cơ chế chống path traversal.
- Xác thực action registry ép chuẩn các trường spec action và giới hạn giá trị cho các mức reasoning được hỗ trợ.
- Script trong repo giả định môi trường thực thi local đáng tin cậy; hãy đọc nội dung script trước khi chạy trong môi trường dùng chung hoặc gần production.
- `.env` có thể chứa giá trị nhạy cảm (`DATABASE_URL`, API keys). Giữ `.env` ngoài commit và dùng cơ chế quản lý bí mật theo môi trường ngoài local dev.

## 🔧 Xử lý sự cố

| Triệu chứng | Cần kiểm tra |
| --- | --- |
| `tmux not found` | Cài `tmux` hoặc chạy backend/PWA thủ công. |
| Backend lỗi khi khởi động do thiếu env | Kiểm tra lại `.env` theo `.env.example` và `docs/env.md`. |
| Lỗi database (kết nối/xác thực/schema) | Xác minh `DATABASE_URL`; chạy lại `conda run -n autoappdev python -m backend.apply_schema`; tùy chọn kiểm tra kết nối: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA tải được nhưng không gọi được API | Đảm bảo backend lắng nghe đúng host/port; tạo lại `pwa/config.local.js` bằng cách chạy lại `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start trả về invalid transition | Kiểm tra pipeline status hiện tại trước; hãy start từ trạng thái `stopped`. |
| UI không cập nhật log | Xác nhận `runtime/logs/pipeline.log` đang được ghi; dùng trực tiếp `/api/logs` và `/api/logs/tail` để tách lỗi UI hay backend. |
| Endpoint parse LLM báo disabled | Đặt `AUTOAPPDEV_ENABLE_LLM_PARSE=1` rồi khởi động lại backend. |
| `conda run -n autoappdev ...` lỗi | Chạy lại `./scripts/setup_autoappdev_env.sh`; xác nhận env conda `autoappdev` tồn tại (`conda env list`). |
| Frontend trỏ sai API | Xác nhận `pwa/config.local.js` tồn tại và trỏ đúng host/port backend đang chạy. |

Để xác minh thủ công tất định, dùng `docs/end-to-end-demo-checklist.md`.

## 🌐 Quy trình README & i18n
- README gốc ở root là nguồn chuẩn do pipeline tự động README sử dụng.
- Các biến thể đa ngôn ngữ được đặt trong `i18n/`.
- Trạng thái thư mục i18n: ✅ có trong repository này.
- Bộ ngôn ngữ hiện có trong repository:
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
- Thanh điều hướng ngôn ngữ phải giữ một dòng duy nhất ở đầu mỗi biến thể README (không lặp thanh ngôn ngữ).
- Entrypoint pipeline README: `prompt_tools/auto-readme-pipeline.sh`.

### Ràng buộc sinh i18n (nghiêm ngặt)
- Luôn xử lý sinh đa ngôn ngữ khi cập nhật nội dung README chuẩn.
- Sinh/cập nhật từng tệp ngôn ngữ theo từng bước (tuần tự), không chạy hàng loạt mơ hồ.
- Giữ đúng một dòng điều hướng tùy chọn ngôn ngữ ở đầu mỗi biến thể.
- Không nhân bản thanh ngôn ngữ trong cùng một tệp.
- Bảo toàn các đoạn lệnh chuẩn, liên kết, đường dẫn API, và ý nghĩa badge qua các bản dịch.

Thứ tự sinh từng tệp được đề xuất:
2. `i18n/README.ar.md`
3. `i18n/README.de.md`
4. `i18n/README.es.md`
5. `i18n/README.fr.md`
6. `i18n/README.ja.md`
7. `i18n/README.ko.md`
8. `i18n/README.ru.md`
9. `i18n/README.vi.md`
10. `i18n/README.zh-Hans.md`
11. `i18n/README.zh-Hant.md`

Bảng phạm vi ngôn ngữ:

| Ngôn ngữ | Tệp |
| --- | --- |

## ❓ Câu hỏi thường gặp

### PostgreSQL có bắt buộc không?
Được ưu tiên và kỳ vọng cho vận hành bình thường. Lớp storage có hành vi fallback tương thích, nhưng cách dùng giống production nên giả định PostgreSQL khả dụng qua `DATABASE_URL`.

### Vì sao có cả `AUTOAPPDEV_PORT` và `PORT`?
`AUTOAPPDEV_PORT` dành riêng cho dự án. `PORT` tồn tại như alias thân thiện triển khai. Hãy giữ chúng đồng bộ trừ khi bạn chủ ý ghi đè hành vi trong luồng khởi chạy.

### Tôi nên bắt đầu từ đâu nếu chỉ muốn xem API?
Chạy backend-only (`conda run -n autoappdev python -m backend.app`) và dùng `/api/health`, `/api/version`, `/api/config`, sau đó đến các endpoint script/action được liệt kê trong `docs/api-contracts.md`.

### README đa ngôn ngữ có được sinh tự động không?
Có. Repository có `prompt_tools/auto-readme-pipeline.sh`, và các biến thể ngôn ngữ được duy trì trong `i18n/` với một dòng điều hướng ngôn ngữ ở đầu mỗi tệp.

## 🗺️ Lộ trình
- Hoàn thành các tác vụ self-dev còn lại sau mốc hiện tại `51 / 55`.
- Mở rộng tooling cho workspace/materials/context và tăng cường contract đường dẫn an toàn.
- Tiếp tục cải thiện UX action palette và luồng action có thể chỉnh sửa.
- Mở rộng hỗ trợ README/UI đa ngôn ngữ trong `i18n/` và chuyển ngôn ngữ runtime.
- Tăng cường smoke/integration checks và độ phủ CI (hiện có smoke check theo script; chưa có manifest CI đầy đủ ở root).
- Tiếp tục gia cố tính tất định của parser/import/codegen quanh AAPS v1 và IR chuẩn.

## 🤝 Đóng góp
Hoan nghênh đóng góp qua issue và pull request.

Quy trình đề xuất:
1. Fork và tạo nhánh tính năng.
2. Giữ thay đổi tập trung và có thể tái tạo.
3. Ưu tiên script/test tất định khi có thể.
4. Cập nhật tài liệu khi hành vi/contract thay đổi (`docs/*`, API contracts, examples).
5. Mở PR kèm ngữ cảnh, bước xác minh, và các giả định runtime.

Remote của repository hiện bao gồm:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Có thể có remote bổ sung trong bản clone local cho các repository liên quan (ví dụ thấy trong workspace này: `novel`).

## 🙌 Hỗ trợ
- GitHub issues và pull requests cho báo lỗi và đề xuất tính năng.
- Các liên kết tài trợ/quyên góp được liệt kê bên dưới.

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 Giấy phép
Không phát hiện tệp `LICENSE` ở root trong snapshot repository này.

Lưu ý giả định:
- Cho đến khi có tệp license, hãy xem điều khoản sử dụng/phân phối lại là chưa xác định và xác nhận với maintainer.

## ❤️ Tài trợ & quyên góp
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400

Nếu dự án này hữu ích cho quy trình của bạn, tài trợ sẽ hỗ trợ trực tiếp cho các tác vụ self-dev tiếp theo, chất lượng tài liệu, và gia cố công cụ.
