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

Bộ script + hướng dẫn có thể tái sử dụng để xây dựng ứng dụng theo từng bước từ ảnh chụp màn hình/markdown, dùng Codex như một công cụ không tương tác.

> 🎯 **Sứ mệnh:** Biến pipeline phát triển ứng dụng thành quy trình tất định, có thể tiếp tục và dựa trên artifact.
>
> 🧩 **Nguyên tắc thiết kế:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🎛️ Tín Hiệu Dự Án

| Tín hiệu | Hướng hiện tại |
| --- | --- |
| Mô hình runtime | Backend Tornado + controller PWA tĩnh |
| Thực thi pipeline | Tất định và có thể tiếp tục (`start/pause/resume/stop`) |
| Chiến lược lưu trữ | PostgreSQL ưu tiên với hành vi fallback tương thích |
| Luồng tài liệu | README gốc canonical + biến thể `i18n/` tự động |

### 🔗 Điều Hướng Nhanh

| Nhu cầu | Đi tới |
| --- | --- |
| Chạy local lần đầu | [⚡ Khởi Động Nhanh](#-khởi-động-nhanh) |
| Biến môi trường bắt buộc | [⚙️ Cấu Hình](#-cấu-hình) |
| Bề mặt API | [📡 Ảnh Chụp Nhanh API](#-ảnh-chụp-nhanh-api) |
| Playbook vận hành/debug | [🧭 Runbook Vận Hành](#-runbook-vận-hành) |
| Quy tắc tạo README/i18n | [🌐 Quy Trình README & i18n](#-quy-trình-readme--i18n) |
| Bảng xử lý sự cố | [🔧 Xử Lý Sự Cố](#-xử-lý-sự-cố) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Trạng Thái Tự Phát Triển (Tự Động Cập Nhật)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Phần này được cập nhật bởi `scripts/auto-autoappdev-development.sh`.
Không chỉnh sửa nội dung giữa các marker.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ Mục Lục
- [🚀 Tổng Quan](#-tổng-quan)
- [🧭 Triết Lý](#-triết-lý)
- [✨ Tính Năng](#-tính-năng)
- [📌 Tóm Tắt Nhanh](#-tóm-tắt-nhanh)
- [🏗️ Kiến Trúc](#️-kiến-trúc)
- [📚 Nội Dung](#-nội-dung)
- [🗂️ Cấu Trúc Dự Án](#️-cấu-trúc-dự-án)
- [✅ Điều Kiện Tiên Quyết](#-điều-kiện-tiên-quyết)
- [🧩 Tương Thích & Giả Định](#-tương-thích--giả-định)
- [🛠️ Cài Đặt](#️-cài-đặt)
- [⚡ Khởi Động Nhanh](#-khởi-động-nhanh)
- [⚙️ Cấu Hình](#️-cấu-hình)
- [▶️ Sử Dụng](#️-sử-dụng)
- [🧭 Runbook Vận Hành](#-runbook-vận-hành)
- [📡 Ảnh Chụp Nhanh API](#-ảnh-chụp-nhanh-api)
- [🧪 Ví Dụ](#-ví-dụ)
- [🧱 Ghi Chú Phát Triển](#-ghi-chú-phát-triển)
- [🔐 Lưu Ý An Toàn](#-lưu-ý-an-toàn)
- [🔧 Xử Lý Sự Cố](#-xử-lý-sự-cố)
- [🌐 Quy Trình README & i18n](#-quy-trình-readme--i18n)
- [❓ FAQ](#-faq)
- [🗺️ Lộ Trình](#️-lộ-trình)
- [🤝 Đóng Góp](#-đóng-góp)
- [❤️ Support](#-support)
- [📄 Giấy Phép](#-giấy-phép)
- [❤️ Sponsor & Donate](#-sponsor--donate)

## 🚀 Tổng Quan
AutoAppDev là dự án controller cho các pipeline phát triển ứng dụng chạy dài hạn và có thể tiếp tục. Dự án kết hợp:

1. Backend API Tornado với lưu trữ dùng PostgreSQL (kèm hành vi fallback JSON cục bộ trong mã storage).
2. UI controller PWA tĩnh kiểu Scratch.
3. Script và tài liệu cho việc soạn pipeline, sinh mã tất định, vòng lặp tự phát triển, và tự động hóa README.

Dự án được tối ưu cho việc thực thi agent có thể dự đoán, với trình tự nghiêm ngặt và lịch sử quy trình theo hướng artifact.

### 🎨 Vì sao repo này tồn tại

| Chủ đề | Ý nghĩa trong thực tế |
| --- | --- |
| Tính tất định | Workflow canonical pipeline IR + parser/import/codegen được thiết kế để lặp lại ổn định |
| Khả năng tiếp tục | Máy trạng thái vòng đời rõ ràng (`start/pause/resume/stop`) cho các lần chạy dài |
| Khả năng vận hành | Runtime log, kênh inbox/outbox, và vòng lặp kiểm chứng bằng script |
| Tài liệu trước tiên | Hợp đồng/spec/ví dụ nằm trong `docs/`, kèm luồng README đa ngôn ngữ tự động |

## 🧭 Triết Lý
AutoAppDev coi agent là công cụ và giữ công việc ổn định bằng vòng lặp nghiêm ngặt, có thể tiếp tục:

1. Plan
2. Implement
3. Debug/verify (có timeout)
4. Fix
5. Summarize + log
6. Commit + push

Ứng dụng controller hướng tới việc hiện thực cùng các khái niệm đó dưới dạng block/action kiểu Scratch (bao gồm action chung `update_readme`), để mỗi workspace luôn cập nhật và có thể tái lập.

### 🔁 Ý nghĩa trạng thái vòng đời

| Chuyển trạng thái | Mục tiêu vận hành |
| --- | --- |
| `start` | Bắt đầu pipeline từ trạng thái dừng/sẵn sàng |
| `pause` | Dừng an toàn tiến trình chạy dài mà không mất ngữ cảnh |
| `resume` | Tiếp tục từ trạng thái/artifact runtime đã lưu |
| `stop` | Kết thúc thực thi và quay về trạng thái không chạy |

## ✨ Tính Năng
- Điều khiển vòng đời pipeline có thể tiếp tục: start, pause, resume, stop.
- API thư viện script cho script pipeline AAPS (`.aaps`) và canonical IR (`autoappdev_ir` v1).
- Pipeline parser/import tất định:
  - Parse script AAPS đã định dạng.
  - Import shell có chú thích qua comment `# AAPS:`.
  - Fallback parse có hỗ trợ Codex (tùy chọn) (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Action registry gồm action tích hợp sẵn + action tùy biến/chỉnh sửa được (clone/edit cho action readonly).
- Block PWA kiểu Scratch và action palette nạp động lúc runtime (`GET /api/actions`).
- Kênh nhắn tin runtime:
  - Inbox (`/api/inbox`) cho hướng dẫn operator -> pipeline.
  - Outbox (`/api/outbox`) bao gồm nạp hàng đợi file từ `runtime/outbox`.
- Stream log tăng dần từ backend và log pipeline (`/api/logs`, `/api/logs/tail`).
- Sinh mã runner tất định từ canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev cho tiến hóa repository theo vòng lặp (`scripts/auto-autoappdev-development.sh`).
- Pipeline tự động hóa README với khung sinh đa ngôn ngữ dưới `i18n/`.

## 📌 Tóm Tắt Nhanh

| Khu vực | Chi tiết |
| --- | --- |
| Runtime lõi | Backend Tornado + frontend PWA tĩnh |
| Lưu trữ | PostgreSQL ưu tiên với hành vi tương thích trong `backend/storage.py` |
| Mô hình pipeline | Canonical IR (`autoappdev_ir` v1) và định dạng script AAPS |
| Luồng điều khiển | Vòng đời Start / Pause / Resume / Stop |
| Chế độ phát triển | Vòng lặp self-dev có thể tiếp tục + workflow script/codegen tất định |
| README/i18n | Pipeline README tự động với khung `i18n/` |

## 🏗️ Kiến Trúc

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
- Cung cấp API controller cho script, action, plan, vòng đời pipeline, log, inbox/outbox, cấu hình workspace.
- Xác thực và lưu trữ tài sản script pipeline.
- Điều phối trạng thái thực thi pipeline và các chuyển trạng thái.
- Cung cấp hành vi fallback tất định khi DB pool không khả dụng.

### Trách nhiệm frontend
- Hiển thị UI block kiểu Scratch và luồng chỉnh sửa pipeline.
- Nạp động action palette từ registry của backend.
- Điều khiển vòng đời và theo dõi trạng thái/log/tin nhắn.

## 📚 Nội Dung
Bản đồ tham chiếu cho các tài liệu, script và ví dụ thường dùng nhất:

- `docs/auto-development-guide.md`: Triết lý và yêu cầu song ngữ (EN/ZH) cho agent tự phát triển chạy dài hạn, có thể tiếp tục.
- `docs/ORDERING_RATIONALE.md`: Ví dụ lý do sắp thứ tự bước theo ảnh chụp màn hình.
- `docs/controller-mvp-scope.md`: Phạm vi controller MVP (màn hình + API tối thiểu).
- `docs/end-to-end-demo-checklist.md`: Checklist demo end-to-end thủ công theo hướng tất định (happy path backend + PWA).
- `docs/env.md`: Quy ước biến môi trường (`.env`).
- `docs/api-contracts.md`: Hợp đồng request/response API cho controller.
- `docs/pipeline-formatted-script-spec.md`: Định dạng script pipeline chuẩn (AAPS) và schema canonical IR (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Bộ sinh tất định tạo bash runner pipeline có thể chạy từ canonical IR.
- `docs/common-actions.md`: Hợp đồng/spec action phổ biến (bao gồm `update_readme`).
- `docs/workspace-layout.md`: Thư mục workspace chuẩn + hợp đồng (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: Khởi động app AutoAppDev (backend + PWA) trong tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Khởi động driver self-dev AutoAppDev trong tmux.
- `scripts/app-auto-development.sh`: Driver pipeline tuyến tính (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) có hỗ trợ resume/state.
- `scripts/generate_screenshot_docs.sh`: Bộ sinh mô tả screenshot -> markdown (dựa trên Codex).
- `scripts/setup_autoappdev_env.sh`: Script bootstrap môi trường conda chính cho chạy local.
- `scripts/setup_backend_env.sh`: Script hỗ trợ môi trường backend.
- `examples/ralph-wiggum-example.sh`: Ví dụ helper tự động hóa Codex CLI.

## 🗂️ Cấu Trúc Dự Án
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

## ✅ Điều Kiện Tiên Quyết
- OS có `bash`.
- Python `3.11+`.
- Conda (`conda`) cho các script thiết lập được cung cấp.
- `tmux` để chạy backend+PWA hoặc self-dev bằng một lệnh.
- PostgreSQL truy cập được qua `DATABASE_URL`.
- Tùy chọn: CLI `codex` cho các luồng dùng Codex (self-dev, parse-llm fallback, pipeline auto-readme).

Bảng yêu cầu nhanh:

| Thành phần | Bắt buộc | Mục đích |
| --- | --- | --- |
| `bash` | Có | Chạy script |
| Python `3.11+` | Có | Backend + tooling codegen |
| Conda | Có (luồng khuyến nghị) | Script bootstrap môi trường |
| PostgreSQL | Có (chế độ ưu tiên) | Lưu trữ chính qua `DATABASE_URL` |
| `tmux` | Khuyến nghị | Quản lý phiên backend/PWA và self-dev |
| `codex` CLI | Tùy chọn | Parse có hỗ trợ LLM và tự động hóa README/self-dev |

## 🧩 Tương Thích & Giả Định

| Chủ đề | Kỳ vọng hiện tại |
| --- | --- |
| OS local | Shell Linux/macOS là mục tiêu chính (script `bash`) |
| Runtime Python | `3.11` (được quản lý bởi `scripts/setup_autoappdev_env.sh`) |
| Chế độ lưu trữ | PostgreSQL được ưu tiên và xem là canonical |
| Hành vi fallback | `backend/storage.py` có fallback JSON tương thích cho tình huống suy giảm |
| Mô hình mạng | Phát triển localhost tách cổng (backend + PWA tĩnh) |
| Công cụ agent | CLI `codex` là tùy chọn trừ khi dùng parse hỗ trợ LLM hoặc tự động hóa self-dev |

Các giả định dùng trong README này:
- Bạn chạy lệnh từ thư mục gốc repository trừ khi có ghi khác.
- `.env` đã được cấu hình trước khi khởi động dịch vụ backend.
- `conda` và `tmux` sẵn có cho các workflow một lệnh được khuyến nghị.

## 🛠️ Cài Đặt
### 1) Clone và vào repo
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) Cấu hình môi trường
```bash
cp .env.example .env
```
Chỉnh `.env` và đặt tối thiểu:
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

### 5) Tùy chọn: smoke test cơ sở dữ liệu
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ Khởi Động Nhanh
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

Kiểm tra nhanh bằng một lệnh:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

Bản đồ endpoint nhanh:

| Bề mặt | URL |
| --- | --- |
| PWA UI | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ Cấu Hình
Tệp chính: `.env` (xem `docs/env.md` và `.env.example`).

### Biến quan trọng

| Biến | Mục đích |
| --- | --- |
| `SECRET_KEY` | Bắt buộc theo quy ước |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Thiết lập bind backend |
| `DATABASE_URL` | PostgreSQL DSN (ưu tiên) |
| `AUTOAPPDEV_RUNTIME_DIR` | Ghi đè thư mục runtime (mặc định `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | Mục tiêu chạy pipeline mặc định |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | Bật `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | Mặc định Codex cho action/endpoint |
| `AI_API_BASE_URL`, `AI_API_KEY` | Dành cho tích hợp tương lai |

Xác thực `.env` nhanh:
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

## ▶️ Sử Dụng

| Chế độ | Lệnh | Ghi chú |
| --- | --- | --- |
| Khởi động backend + PWA (khuyến nghị) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| Chỉ khởi động backend | `conda run -n autoappdev python -m backend.app` | Dùng cấu hình bind + DB trong `.env` |
| Chỉ khởi động static server PWA | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | Hữu ích khi kiểm tra frontend |
| Chạy self-dev driver trong tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | Vòng lặp tự phát triển có thể tiếp tục |

### Tùy chọn script thường dùng
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### Parse và lưu script
- Parse AAPS qua API: `POST /api/scripts/parse`
- Import annotated shell: `POST /api/scripts/import-shell`
- Parse LLM tùy chọn: `POST /api/scripts/parse-llm` (cần `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### API điều khiển pipeline
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

Xem `docs/api-contracts.md` để biết cấu trúc request/response.

## 🧭 Runbook Vận Hành

### Runbook: khởi chạy toàn bộ stack local
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

Các điểm kiểm chứng:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- Mở `http://127.0.0.1:5173/` và xác nhận UI có thể nạp `/api/config`.
- Tùy chọn: mở `/api/version` và kiểm tra metadata backend trả về như kỳ vọng.

### Runbook: debug chỉ backend
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

## 📡 Ảnh Chụp Nhanh API

Nhìn nhanh các nhóm API cốt lõi:

| Danh mục | Endpoints |
| --- | --- |
| Health + thông tin runtime | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| Mô hình plan | `GET /api/plan`, `POST /api/plan` |
| Scripts | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| Action registry | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| Runtime pipeline | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| Messaging + logs | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
| Cấu hình workspace | `GET/POST /api/workspaces/<name>/config` |

## 🧪 Ví Dụ
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

### Sinh deterministic runner
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### Pipeline demo tất định
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

## 🧱 Ghi Chú Phát Triển
- Backend dựa trên Tornado và được thiết kế tối ưu cho local dev (bao gồm CORS thoáng cho localhost tách cổng).
- Lưu trữ ưu tiên PostgreSQL với hành vi tương thích trong `backend/storage.py`.
- Khóa block của PWA và giá trị `STEP.block` trong script được cố ý căn chỉnh (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Action tích hợp sẵn là readonly; hãy clone trước khi chỉnh sửa.
- Action `update_readme` bị ràng buộc an toàn đường dẫn tới README workspace dưới `auto-apps/<workspace>/README.md`.
- Một số tài liệu/script còn tham chiếu tên/đường dẫn cũ (`HeyCyan`, `LightMind`) do lịch sử phát triển. Đường dẫn canonical hiện tại là thư mục gốc repository này.
- Thư mục gốc `i18n/` đã tồn tại. README theo ngôn ngữ được kỳ vọng đặt tại đó trong các lần chạy đa ngôn ngữ.

### Mô hình làm việc và tệp trạng thái
- Runtime mặc định là `./runtime` trừ khi ghi đè bằng `AUTOAPPDEV_RUNTIME_DIR`.
- Trạng thái/lịch sử tự động hóa self-dev được theo dõi trong `references/selfdev/`.
- Artifact pipeline README được ghi dưới `.auto-readme-work/<timestamp>/`.

### Tư thế kiểm thử (hiện tại)
- Repository có smoke check và script demo tất định.
- Hiện chưa có bộ test tự động/manifest CI đầy đủ ở cấp root metadata.
- Giả định: hiện tại xác thực chủ yếu theo script (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, checklist end-to-end).

## 🔐 Lưu Ý An Toàn
- Action `update_readme` cố ý bị giới hạn vào README workspace (`auto-apps/<workspace>/README.md`) với cơ chế chống path traversal.
- Validation của action registry cưỡng chế trường spec action được chuẩn hóa và giới hạn giá trị cho các mức reasoning được hỗ trợ.
- Script trong repository giả định môi trường local đáng tin cậy; hãy xem nội dung script trước khi chạy trong môi trường chia sẻ hoặc gần production.
- `.env` có thể chứa giá trị nhạy cảm (`DATABASE_URL`, API key). Không commit `.env` và dùng quản lý bí mật theo môi trường ngoài local dev.

## 🔧 Xử Lý Sự Cố

| Triệu chứng | Cần kiểm tra |
| --- | --- |
| `tmux not found` | Cài `tmux` hoặc chạy backend/PWA thủ công. |
| Backend lỗi khi khởi động do thiếu env | Kiểm tra lại `.env` theo `.env.example` và `docs/env.md`. |
| Lỗi cơ sở dữ liệu (kết nối/xác thực/schema) | Xác minh `DATABASE_URL`; chạy lại `conda run -n autoappdev python -m backend.apply_schema`; tùy chọn kiểm tra kết nối: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA tải được nhưng không gọi được API | Đảm bảo backend đang lắng nghe đúng host/port; tạo lại `pwa/config.local.js` bằng cách chạy lại `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start trả về invalid transition | Kiểm tra trạng thái pipeline hiện tại trước; bắt đầu từ trạng thái `stopped`. |
| UI không cập nhật log | Xác nhận `runtime/logs/pipeline.log` đang được ghi; dùng trực tiếp `/api/logs` và `/api/logs/tail` để tách lỗi UI hay backend. |
| Endpoint parse LLM trả disabled | Đặt `AUTOAPPDEV_ENABLE_LLM_PARSE=1` rồi khởi động lại backend. |
| `conda run -n autoappdev ...` lỗi | Chạy lại `./scripts/setup_autoappdev_env.sh`; xác nhận env conda `autoappdev` tồn tại (`conda env list`). |
| Frontend trỏ sai API | Xác nhận `pwa/config.local.js` tồn tại và trỏ đúng host/port backend đang chạy. |

Để xác minh thủ công theo hướng tất định, dùng `docs/end-to-end-demo-checklist.md`.

## 🌐 Quy Trình README & i18n
- README gốc là nguồn canonical dùng bởi pipeline tự động hóa README.
- Biến thể đa ngôn ngữ được kỳ vọng nằm trong `i18n/`.
- Trạng thái thư mục i18n: ✅ đã có trong repository này.
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
- Thanh điều hướng ngôn ngữ phải giữ một dòng duy nhất ở đầu mỗi biến thể README (không được trùng lặp).
- Entrypoint pipeline README: `prompt_tools/auto-readme-pipeline.sh`.

### Ràng buộc sinh i18n (nghiêm ngặt)
- Luôn xử lý sinh đa ngôn ngữ khi cập nhật README canonical.
- Tạo/cập nhật từng tệp ngôn ngữ theo thứ tự (tuần tự), không chạy mơ hồ theo lô.
- Giữ đúng một dòng điều hướng ngôn ngữ ở đầu mỗi biến thể.
- Không nhân bản thanh ngôn ngữ trong cùng một tệp.
- Giữ nguyên snippet lệnh, liên kết, API path và ý nghĩa badge trong bản dịch.

Thứ tự gợi ý để sinh từng ngôn ngữ:
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

Bảng phạm vi ngôn ngữ:

| Language | File |
| --- | --- |

## ❓ FAQ

### PostgreSQL có bắt buộc không?
Được ưu tiên và là kỳ vọng cho vận hành bình thường. Tầng storage có hành vi fallback tương thích, nhưng khi dùng kiểu production nên giả định PostgreSQL sẵn có qua `DATABASE_URL`.

### Vì sao có cả `AUTOAPPDEV_PORT` và `PORT`?
`AUTOAPPDEV_PORT` là biến riêng của dự án. `PORT` tồn tại như một alias thân thiện triển khai. Hãy giữ đồng bộ hai biến trừ khi bạn cố ý ghi đè hành vi trong luồng khởi chạy.

### Nếu chỉ muốn xem API thì bắt đầu từ đâu?
Chạy backend-only (`conda run -n autoappdev python -m backend.app`) rồi dùng `/api/health`, `/api/version`, `/api/config`, sau đó đến các endpoint script/action trong `docs/api-contracts.md`.

### README đa ngôn ngữ có được tạo tự động không?
Có. Repository có `prompt_tools/auto-readme-pipeline.sh`, và các bản ngôn ngữ được duy trì dưới `i18n/` với một dòng điều hướng ngôn ngữ ở đầu mỗi biến thể.

## 🗺️ Lộ Trình
- Hoàn tất các tác vụ self-dev còn lại vượt mốc hiện tại `51 / 55`.
- Mở rộng tooling cho workspace/materials/context và siết chặt hợp đồng safe-path.
- Tiếp tục cải thiện UX action palette và luồng chỉnh sửa action.
- Mở rộng hỗ trợ README/UI đa ngôn ngữ trong `i18n/` và chuyển ngôn ngữ lúc runtime.
- Tăng cường smoke/integration check và độ bao phủ CI (hiện có smoke check dựa trên script; chưa có manifest CI đầy đủ ở root).
- Tiếp tục tăng độ cứng tính tất định của parser/import/codegen quanh AAPS v1 và canonical IR.

## 🤝 Đóng Góp
Đóng góp luôn được chào đón qua issue và pull request.

Quy trình đề xuất:
1. Fork và tạo nhánh tính năng.
2. Giữ thay đổi tập trung và có thể tái lập.
3. Ưu tiên script/test tất định khi có thể.
4. Cập nhật tài liệu khi hành vi/hợp đồng thay đổi (`docs/*`, API contracts, ví dụ).
5. Mở PR kèm ngữ cảnh, bước xác thực, và các giả định runtime.

Remote hiện có của repository:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Có thể tồn tại remote bổ sung trong bản clone local cho các repository liên quan (ví dụ phát hiện trong workspace này: `novel`).

## ❤️ Support

| Donate | PayPal | Stripe |
|---|---|---|
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=ko-fi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 Giấy Phép
Không phát hiện tệp `LICENSE` ở thư mục gốc trong snapshot repository này.

Lưu ý giả định:
- Cho tới khi thêm tệp license, hãy coi điều khoản sử dụng/phân phối lại là chưa xác định và xác nhận với maintainer.

## ❤️ Sponsor & Donate
| Channel | Link |
| --- | --- |
| GitHub Sponsors | https://github.com/sponsors/lachlanchen |
| Donate | https://chat.lazying.art/donate |
| PayPal | https://paypal.me/RongzhouChen |
| Stripe | https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400 |

Nếu dự án này giúp ích cho workflow của bạn, tài trợ trực tiếp sẽ hỗ trợ các tác vụ self-dev liên tục, chất lượng tài liệu và việc củng cố công cụ.
