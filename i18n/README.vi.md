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

Các script và hướng dẫn có thể tái sử dụng để xây dựng ứng dụng từng bước từ ảnh chụp màn hình/markdown, dùng Codex như một công cụ không tương tác.

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## Trạng Thái Self-Dev (Tự Động Cập Nhật)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

Mục này được cập nhật bởi `scripts/auto-autoappdev-development.sh`.
Không chỉnh sửa nội dung giữa các marker.

<!-- AUTOAPPDEV:STATUS:END -->

## 🚀 Tổng Quan
AutoAppDev là một dự án điều phối cho các pipeline phát triển ứng dụng chạy dài hạn và có thể tiếp tục lại. Dự án kết hợp:

1. API backend Tornado với lưu trữ dựa trên PostgreSQL (kèm hành vi fallback JSON cục bộ trong mã lưu trữ).
2. Giao diện điều khiển PWA tĩnh kiểu Scratch.
3. Script và tài liệu cho việc biên soạn pipeline, sinh mã tất định, vòng lặp tự phát triển, và tự động hóa README.

### Nhìn nhanh

| Khu vực | Chi tiết |
| --- | --- |
| Runtime cốt lõi | Backend Tornado + frontend PWA tĩnh |
| Lưu trữ | Ưu tiên PostgreSQL với hành vi tương thích trong `backend/storage.py` |
| Mô hình pipeline | IR chuẩn (`autoappdev_ir` v1) và định dạng script AAPS |
| Luồng điều khiển | Vòng đời Start / Pause / Resume / Stop |
| Chế độ dev | Vòng lặp self-dev có thể tiếp tục + luồng script/codegen tất định |
| README/i18n | Pipeline README tự động với khung `i18n/` |

## 🧭 Triết Lý
AutoAppDev xem agent như công cụ và giữ sự ổn định công việc bằng một vòng lặp nghiêm ngặt, có thể tiếp tục lại:
1. Plan
2. Implement
3. Debug/verify (có timeout)
4. Fix
5. Summarize + log
6. Commit + push

Ứng dụng controller hướng tới việc hiện thực hóa cùng các khái niệm dưới dạng block/action kiểu Scratch (bao gồm action dùng chung `update_readme`) để mỗi workspace luôn cập nhật và có thể tái tạo.

## ✨ Tính Năng
- Điều khiển vòng đời pipeline có thể tiếp tục: start, pause, resume, stop.
- API thư viện script cho AAPS pipeline scripts (`.aaps`) và IR chuẩn (`autoappdev_ir` v1).
- Pipeline parser/import tất định:
  - Parse script AAPS đã format.
  - Import shell có chú thích qua comment `# AAPS:`.
  - Tùy chọn fallback parse có hỗ trợ Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- Action registry với action built-in + action tùy chỉnh/chỉnh sửa (luồng clone/edit cho built-in chỉ đọc).
- Block PWA kiểu Scratch và action palette nạp lúc chạy (`GET /api/actions`).
- Kênh nhắn tin runtime:
  - Inbox (`/api/inbox`) cho hướng dẫn operator -> pipeline.
  - Outbox (`/api/outbox`) bao gồm nạp hàng đợi file từ `runtime/outbox`.
- Stream log tăng dần từ backend và pipeline logs (`/api/logs`, `/api/logs/tail`).
- Sinh mã runner tất định từ IR chuẩn (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- Driver self-dev cho tiến hóa repository lặp (`scripts/auto-autoappdev-development.sh`).
- Pipeline tự động hóa README với khung sinh đa ngôn ngữ trong `i18n/`.

## 📚 Nội Dung
- `docs/auto-development-guide.md`: Triết lý và yêu cầu song ngữ (EN/ZH) cho một agent tự phát triển chạy dài hạn, có thể tiếp tục.
- `docs/ORDERING_RATIONALE.md`: Ví dụ lập luận cho việc sắp xếp các bước theo ảnh chụp màn hình.
- `docs/controller-mvp-scope.md`: Phạm vi MVP của controller (màn hình + API tối thiểu).
- `docs/end-to-end-demo-checklist.md`: Checklist demo end-to-end thủ công, tất định (happy path backend + PWA).
- `docs/env.md`: Quy ước biến môi trường (.env).
- `docs/api-contracts.md`: Hợp đồng request/response API cho controller.
- `docs/pipeline-formatted-script-spec.md`: Định dạng script pipeline chuẩn (AAPS) và schema IR chuẩn (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: Bộ sinh tất định để tạo bash pipeline runner có thể chạy từ IR chuẩn.
- `docs/common-actions.md`: Hợp đồng/spec các action dùng chung (bao gồm `update_readme`).
- `docs/workspace-layout.md`: Thư mục workspace chuẩn + hợp đồng (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: Khởi động ứng dụng AutoAppDev (backend + PWA) trong tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: Khởi động driver self-dev của AutoAppDev trong tmux.
- `scripts/app-auto-development.sh`: Driver pipeline tuyến tính (plan -> backend -> PWA -> Android -> iOS -> review -> summary), có hỗ trợ resume/state.
- `scripts/generate_screenshot_docs.sh`: Bộ sinh mô tả markdown từ screenshot (do Codex điều khiển).
- `scripts/setup_backend_env.sh`: Bootstrap môi trường conda backend cho chạy local.
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
├── prompt_tools/
├── examples/
├── references/
├── i18n/
└── .auto-readme-work/
```

## ✅ Điều Kiện Tiên Quyết
- OS có `bash`.
- Python `3.11+`.
- Conda (`conda`) cho các script setup đi kèm.
- `tmux` cho phiên backend+PWA hoặc self-dev bằng một lệnh.
- PostgreSQL có thể truy cập qua `DATABASE_URL`.
- Tùy chọn: `codex` CLI cho các luồng dùng Codex (self-dev, parse-llm fallback, pipeline auto-readme).

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
Chỉnh `.env` và đặt ít nhất:
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

## ⚙️ Cấu Hình
Tệp chính: `.env` (xem `docs/env.md` và `.env.example`).

### Biến quan trọng

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Bắt buộc theo quy ước |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | Thiết lập bind backend |
| `DATABASE_URL` | PostgreSQL DSN (khuyến nghị) |
| `AUTOAPPDEV_RUNTIME_DIR` | Ghi đè thư mục runtime (mặc định `./runtime`) |
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

## ▶️ Cách Dùng
### Khởi động backend + PWA cùng lúc (khuyến nghị)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
Mặc định:
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### Chỉ khởi động backend
```bash
conda run -n autoappdev python -m backend.app
```

### Chỉ khởi động static server cho PWA
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### Chạy self-dev driver trong tmux
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### Parse và lưu script
- Parse AAPS qua API: `POST /api/scripts/parse`
- Import shell có chú thích: `POST /api/scripts/import-shell`
- Parse bằng LLM (tùy chọn): `POST /api/scripts/parse-llm` (cần `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### API điều khiển pipeline
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

Xem `docs/api-contracts.md` để biết cấu trúc request/response.

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

### Sinh runner tất định
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
Sau đó dùng các điều khiển Start/Pause/Resume/Stop trên PWA và kiểm tra `/api/logs`.

## 🧱 Ghi Chú Phát Triển
- Backend dựa trên Tornado và được thiết kế cho tính tiện dụng khi dev local (bao gồm CORS linh hoạt cho localhost khác cổng).
- Lưu trữ ưu tiên PostgreSQL với hành vi tương thích trong `backend/storage.py`.
- Khóa block của PWA và giá trị `STEP.block` trong script được cố ý đồng bộ (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- Action built-in là chỉ đọc; hãy clone trước khi chỉnh sửa.
- Action `update_readme` bị ràng buộc an toàn đường dẫn vào các mục tiêu README workspace dưới `auto-apps/<workspace>/README.md`.
- Có các tham chiếu đường dẫn/tên cũ trong một số tài liệu/script (`HeyCyan`, `LightMind`) do quá trình tiến hóa dự án. Đường dẫn chuẩn hiện tại là thư mục gốc của repository này.
- Thư mục gốc `i18n/` đã tồn tại. README theo ngôn ngữ được kỳ vọng đặt ở đó trong các lần chạy đa ngôn ngữ.

## 🩺 Khắc Phục Sự Cố
- `tmux not found`:
  - Cài `tmux` hoặc chạy backend/PWA thủ công.
- Backend lỗi khởi động do thiếu env:
  - Kiểm tra lại `.env` so với `.env.example` và `docs/env.md`.
- Lỗi cơ sở dữ liệu (connection/auth/schema):
  - Xác minh `DATABASE_URL`.
  - Chạy lại `conda run -n autoappdev python -m backend.apply_schema`.
  - Kiểm tra kết nối (tùy chọn): `conda run -n autoappdev python -m backend.db_smoketest`.
- PWA tải được nhưng không gọi được API:
  - Đảm bảo backend đang lắng nghe đúng host/port dự kiến.
  - Tạo lại `pwa/config.local.js` bằng cách chạy lại `./scripts/run_autoappdev_tmux.sh`.
- Pipeline Start trả về invalid transition:
  - Kiểm tra trạng thái pipeline hiện tại trước; hãy start từ trạng thái `stopped`.
- Không có cập nhật log trong UI:
  - Xác nhận `runtime/logs/pipeline.log` đang được ghi.
  - Dùng trực tiếp `/api/logs` và `/api/logs/tail` để tách lỗi UI hay backend.
- Endpoint LLM parse báo disabled:
  - Đặt `AUTOAPPDEV_ENABLE_LLM_PARSE=1` và khởi động lại backend.

Để xác minh thủ công theo hướng tất định, dùng `docs/end-to-end-demo-checklist.md`.

## 🗺️ Lộ Trình
- Hoàn tất các task self-dev còn lại vượt trạng thái hiện tại `51 / 55`.
- Mở rộng công cụ workspace/materials/context và các hợp đồng safe-path chặt chẽ hơn.
- Tiếp tục cải thiện UX action palette và luồng chỉnh sửa action.
- Tăng cường hỗ trợ README/UI đa ngôn ngữ trên `i18n/` và chuyển ngôn ngữ khi runtime.
- Củng cố kiểm tra smoke/integration và độ phủ CI (hiện tại đã có smoke check dựa trên script; chưa có manifest CI đầy đủ được mô tả ở root).

## 🤝 Đóng Góp
Hoan nghênh đóng góp qua issue và pull request.

Quy trình gợi ý:
1. Fork và tạo nhánh tính năng.
2. Giữ thay đổi tập trung và có thể tái tạo.
3. Ưu tiên script/test tất định khi có thể.
4. Cập nhật tài liệu khi hành vi/hợp đồng thay đổi (`docs/*`, API contracts, examples).
5. Mở PR với ngữ cảnh, các bước xác thực, và mọi giả định về runtime.

Remote của repository hiện gồm:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- Có thể có thêm remote khác trong bản clone cục bộ cho các repo liên quan.

## 📄 Giấy Phép
Không phát hiện tệp `LICENSE` ở root trong snapshot repository này.

Ghi chú giả định:
- Cho đến khi có tệp license, hãy xem điều khoản sử dụng/phân phối lại là chưa được chỉ định và cần xác nhận với maintainer.

## ❤️ Sponsor & Donate

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
