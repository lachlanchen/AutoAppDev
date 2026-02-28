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

سكربتات قابلة لإعادة الاستخدام + أدلة لبناء التطبيقات خطوة بخطوة من لقطات الشاشة/الـ markdown مع Codex كأداة غير تفاعلية.

> 🎯 **المهمة:** جعل خطوط تطوير التطبيقات حتمية، قابلة للاستئناف، ومعتمدة على المخرجات.
>
> 🧩 **مبدأ التصميم:** Plan -> Work -> Verify -> Summary -> Commit/Push.

### 🔗 تنقل سريع

| الحاجة | اذهب إلى |
| --- | --- |
| أول تشغيل محلي | [⚡ البدء السريع](#-quick-start) |
| البيئة والمتغيرات المطلوبة | [⚙️ الإعدادات](#-configuration) |
| واجهات API | [📡 لمحة API](#-api-snapshot) |
| كتيبات التشغيل/تصحيح الأخطاء | [🧭 كتيبات التشغيل](#-operational-runbooks) |
| قواعد توليد README/i18n | [🌐 سير عمل README و i18n](#-readme--i18n-workflow) |
| مصفوفة استكشاف الأخطاء | [🔧 استكشاف الأخطاء وإصلاحها](#-troubleshooting) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## حالة التطوير الذاتي (تحديث تلقائي)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

يتم تحديث هذا القسم بواسطة `scripts/auto-autoappdev-development.sh`.
لا تقم بتعديل المحتوى بين العلامات.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ جدول المحتويات
- [🚀 نظرة عامة](#-overview)
- [🧭 الفلسفة](#-philosophy)
- [✨ الميزات](#-features)
- [📌 لمحة سريعة](#-at-a-glance)
- [🏗️ البنية المعمارية](#-architecture)
- [📚 المحتويات](#-contents)
- [🗂️ بنية المشروع](#-project-structure)
- [✅ المتطلبات المسبقة](#-prerequisites)
- [🧩 التوافق والافتراضات](#-compatibility--assumptions)
- [🛠️ التثبيت](#-installation)
- [⚡ البدء السريع](#-quick-start)
- [⚙️ الإعدادات](#-configuration)
- [▶️ الاستخدام](#-usage)
- [🧭 كتيبات التشغيل](#-operational-runbooks)
- [📡 لمحة API](#-api-snapshot)
- [🧪 أمثلة](#-examples)
- [🧱 ملاحظات التطوير](#-development-notes)
- [🔐 ملاحظات الأمان](#-safety-notes)
- [🔧 استكشاف الأخطاء وإصلاحها](#-troubleshooting)
- [🌐 سير عمل README و i18n](#-readme--i18n-workflow)
- [❓ الأسئلة الشائعة](#-faq)
- [🗺️ خارطة الطريق](#-roadmap)
- [🤝 المساهمة](#-contributing)
- [🙌 الدعم](#-support)
- [📄 الترخيص](#-license)
- [❤️ الرعاية والتبرع](#-sponsor--donate)

## 🚀 نظرة عامة
AutoAppDev هو مشروع متحكم لخطوط تطوير تطبيقات طويلة التشغيل وقابلة للاستئناف. يجمع بين:

1. واجهة API خلفية مبنية على Tornado مع تخزين مدعوم بـ PostgreSQL (مع سلوك JSON محلي احتياطي في كود التخزين).
2. واجهة متحكم PWA ثابتة على نمط Scratch.
3. سكربتات ووثائق لكتابة خطوط المعالجة، وتوليد الشيفرة الحتمي، وحلقات التطوير الذاتي، وأتمتة README.

المشروع مُحسَّن لتنفيذ الوكلاء بشكل متوقع مع تسلسل صارم وتاريخ سير عمل موجّه بالمخرجات.

### 🎨 لماذا يوجد هذا المستودع

| المحور | ما يعنيه عمليًا |
| --- | --- |
| الحتمية | سير parser/import/codegen + IR قياسي مصمم لقابلية إعادة التشغيل |
| قابلية الاستئناف | آلة حالات دورة حياة صريحة (`start/pause/resume/stop`) للتشغيلات الطويلة |
| قابلية التشغيل | سجلات وقت التشغيل، وقنوات inbox/outbox، وحلقات تحقق مدفوعة بالسكربتات |
| التوثيق أولًا | العقود/المواصفات/الأمثلة موجودة في `docs/` مع تدفق README متعدد اللغات آلي |

## 🧭 الفلسفة
يتعامل AutoAppDev مع الوكلاء كأدوات ويحافظ على استقرار العمل عبر حلقة صارمة وقابلة للاستئناف:

1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

يهدف تطبيق المتحكم إلى تجسيد نفس المفاهيم ككتل/إجراءات على نمط Scratch (بما في ذلك إجراء `update_readme` مشترك) حتى يبقى كل workspace محدثًا وقابلاً لإعادة الإنتاج.

### 🔁 نية حالات دورة الحياة

| انتقال الحالة | نية التشغيل |
| --- | --- |
| `start` | بدء خط معالجة من حالة التوقف/الجاهزية |
| `pause` | إيقاف التنفيذ طويل التشغيل بأمان دون فقدان السياق |
| `resume` | المتابعة من حالة/مخرجات وقت تشغيل محفوظة |
| `stop` | إنهاء التنفيذ والعودة إلى حالة غير قيد التشغيل |

## ✨ الميزات
- تحكم قابل للاستئناف في دورة حياة خط المعالجة: start و pause و resume و stop.
- واجهات API لمكتبة سكربتات AAPS (`.aaps`) و IR القياسي (`autoappdev_ir` v1).
- سير parser/import حتمي:
  - تحليل سكربتات AAPS المنسقة.
  - استيراد shell المشروح عبر تعليقات `# AAPS:`.
  - احتياطي تحليل بمساعدة Codex اختياري (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- سجل إجراءات يتضمن إجراءات مدمجة + إجراءات قابلة للتعديل/مخصصة (تدفق clone/edit للإجراءات المدمجة للقراءة فقط).
- كتل PWA على نمط Scratch ولوحة إجراءات محمّلة وقت التشغيل (`GET /api/actions`).
- قنوات مراسلة وقت التشغيل:
  - Inbox (`/api/inbox`) لإرشادات المشغّل -> خط المعالجة.
  - Outbox (`/api/outbox`) بما في ذلك ingest لطابور الملفات من `runtime/outbox`.
- بث سجلات تدريجي من backend وسجلات خط المعالجة (`/api/logs`, `/api/logs/tail`).
- توليد حتمي لكود runner من IR القياسي (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- مشغل تطوير ذاتي لتطور المستودع بشكل تكراري (`scripts/auto-autoappdev-development.sh`).
- خط أتمتة README مع هيكل توليد متعدد اللغات تحت `i18n/`.

## 📌 لمحة سريعة

| المنطقة | التفاصيل |
| --- | --- |
| وقت التشغيل الأساسي | Backend Tornado + Frontend PWA ثابت |
| الاستمرارية | PostgreSQL أولًا مع سلوك توافق في `backend/storage.py` |
| نموذج خط المعالجة | IR قياسي (`autoappdev_ir` v1) وصيغة سكربت AAPS |
| تدفق التحكم | دورة حياة Start / Pause / Resume / Stop |
| وضع التطوير | حلقة تطوير ذاتي قابلة للاستئناف + سير سكربت/codegen حتمي |
| README/i18n | خط README آلي مع هيكل `i18n/` |

## 🏗️ البنية المعمارية

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

### مسؤوليات الواجهة الخلفية
- توفير واجهات API للمتحكم الخاصة بالسكربتات، والإجراءات، والخطة، ودورة حياة خط المعالجة، والسجلات، و inbox/outbox، وإعدادات workspace.
- التحقق من أصول سكربت خط المعالجة وحفظها.
- تنسيق حالة تنفيذ خط المعالجة وانتقالات الحالة.
- توفير سلوك احتياطي حتمي عندما لا يتوفر تجمع اتصالات قاعدة البيانات.

### مسؤوليات الواجهة الأمامية
- عرض واجهة كتل على نمط Scratch وتدفق تحرير خط المعالجة.
- تحميل لوحة الإجراءات ديناميكيًا من سجل backend.
- تشغيل عناصر تحكم دورة الحياة ومراقبة الحالة/السجلات/الرسائل.

## 📚 المحتويات
خريطة مرجعية لأكثر الوثائق والسكربتات والأمثلة استخدامًا:

- `docs/auto-development-guide.md`: فلسفة ومتطلبات ثنائية اللغة (EN/ZH) لوكيل تطوير تلقائي طويل التشغيل وقابل للاستئناف.
- `docs/ORDERING_RATIONALE.md`: مثال تبرير لتسلسل خطوات مدفوعة بلقطات الشاشة.
- `docs/controller-mvp-scope.md`: نطاق MVP للمتحكم (الشاشات + أقل واجهات API).
- `docs/end-to-end-demo-checklist.md`: قائمة تحقق تجريبية يدوية من طرف إلى طرف بشكل حتمي (backend + المسار السعيد للـ PWA).
- `docs/env.md`: أعراف متغيرات البيئة (`.env`).
- `docs/api-contracts.md`: عقود الطلب/الاستجابة لواجهة API الخاصة بالمتحكم.
- `docs/pipeline-formatted-script-spec.md`: صيغة سكربت خط المعالجة القياسية (AAPS) ومخطط IR القياسي (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: مولد حتمي لمشغلات خطوط معالجة bash قابلة للتنفيذ من IR القياسي.
- `docs/common-actions.md`: عقود/مواصفات الإجراءات الشائعة (يتضمن `update_readme`).
- `docs/workspace-layout.md`: مجلدات workspace القياسية + العقود (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: تشغيل تطبيق AutoAppDev (backend + PWA) داخل tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: تشغيل مشغل التطوير الذاتي لـ AutoAppDev داخل tmux.
- `scripts/app-auto-development.sh`: مشغل خط معالجة خطي (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) مع دعم الاستئناف/الحالة.
- `scripts/generate_screenshot_docs.sh`: مولد وصف markdown من لقطات الشاشة (مدفوع بـ Codex).
- `scripts/setup_autoappdev_env.sh`: سكربت bootstrap الرئيسي لبيئة conda للتشغيل المحلي.
- `scripts/setup_backend_env.sh`: سكربت مساعد لبيئة backend.
- `examples/ralph-wiggum-example.sh`: مساعد أتمتة Codex CLI كمثال.

## 🗂️ بنية المشروع
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

## ✅ المتطلبات المسبقة
- نظام تشغيل يدعم `bash`.
- Python `3.11+`.
- Conda (`conda`) لسكربتات الإعداد المتوفرة.
- `tmux` لجلسات backend+PWA أو self-dev بأمر واحد.
- PostgreSQL يمكن الوصول إليه عبر `DATABASE_URL`.
- اختياري: CLI `codex` لمسارات مدعومة بـ Codex (self-dev، احتياطي parse-llm، خط auto-readme).

مصفوفة متطلبات سريعة:

| المكوّن | مطلوب | الغرض |
| --- | --- | --- |
| `bash` | نعم | تنفيذ السكربتات |
| Python `3.11+` | نعم | Backend + أدوات codegen |
| Conda | نعم (المسار الموصى به) | سكربتات bootstrap للبيئة |
| PostgreSQL | نعم (الوضع المفضل) | الاستمرارية الأساسية عبر `DATABASE_URL` |
| `tmux` | موصى به | جلسات backend/PWA و self-dev مُدارة |
| CLI `codex` | اختياري | تحليل بمساعدة LLM وأتمتة README/self-dev |

## 🧩 التوافق والافتراضات

| الموضوع | التوقع الحالي |
| --- | --- |
| نظام التشغيل المحلي | Shells على Linux/macOS هي الهدف الأساسي (سكربتات `bash`) |
| Python runtime | `3.11` (تُدار بواسطة `scripts/setup_autoappdev_env.sh`) |
| وضع الاستمرارية | PostgreSQL هو المفضل ويُعامل كمرجع أساسي |
| سلوك احتياطي | `backend/storage.py` يتضمن احتياطي توافق JSON لسيناريوهات التدهور |
| نموذج الشبكة | تطوير localhost بمنافذ منفصلة (backend + PWA ثابت) |
| أدوات الوكيل | CLI `codex` اختياري ما لم تستخدم تحليلًا بمساعدة LLM أو أتمتة التطوير الذاتي |

الافتراضات المستخدمة في هذا README:
- تشغّل الأوامر من جذر المستودع ما لم يذكر القسم خلاف ذلك.
- يتم إعداد `.env` قبل تشغيل خدمات backend.
- `conda` و `tmux` متاحان لمسارات التشغيل الموصى بها بأمر واحد.

## 🛠️ التثبيت
### 1) استنساخ المستودع والدخول إليه
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) إعداد البيئة
```bash
cp .env.example .env
```
حرّر `.env` واضبط على الأقل:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` و `AUTOAPPDEV_PORT` (أو `PORT`)

### 3) إنشاء/تحديث بيئة backend
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) تطبيق مخطط قاعدة البيانات
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) اختياري: اختبار دخاني لقاعدة البيانات
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ البدء السريع
```bash
# from repo root
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

ثم افتح:
- PWA: `http://127.0.0.1:5173/`
- قاعدة Backend API: `http://127.0.0.1:8788`
- فحص الصحة: `http://127.0.0.1:8788/api/health`

فحص سريع بأمر واحد:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

خريطة endpoints سريعة:

| الواجهة | URL |
| --- | --- |
| واجهة PWA | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ الإعدادات
الملف الأساسي: `.env` (انظر `docs/env.md` و `.env.example`).

### متغيرات مهمة

| المتغير | الغرض |
| --- | --- |
| `SECRET_KEY` | مطلوب بحسب العرف |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | إعدادات ربط backend |
| `DATABASE_URL` | PostgreSQL DSN (المفضل) |
| `AUTOAPPDEV_RUNTIME_DIR` | تجاوز مسار runtime (الافتراضي `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | هدف تشغيل خط المعالجة الافتراضي |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | تمكين `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | إعدادات Codex الافتراضية للإجراءات/النقاط النهائية |
| `AI_API_BASE_URL`, `AI_API_KEY` | محجوزان لتكاملات مستقبلية |

تحقق من `.env` بسرعة:
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

## ▶️ الاستخدام

| الوضع | الأمر | ملاحظات |
| --- | --- | --- |
| تشغيل backend + PWA (موصى به) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| تشغيل backend فقط | `conda run -n autoappdev python -m backend.app` | يستخدم إعدادات الربط + قاعدة البيانات من `.env` |
| تشغيل خادم PWA الثابت فقط | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | مفيد لفحوصات الواجهة الأمامية فقط |
| تشغيل مشغل self-dev داخل tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | حلقة تطوير ذاتي قابلة للاستئناف |

### خيارات سكربت شائعة
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### تحليل وحفظ السكربتات
- تحليل AAPS عبر API: `POST /api/scripts/parse`
- استيراد shell مشروح: `POST /api/scripts/import-shell`
- تحليل LLM اختياري: `POST /api/scripts/parse-llm` (يتطلب `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### واجهات API للتحكم بخط المعالجة
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### واجهات API أخرى كثيرة الاستخدام
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- Actions: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- Messaging: `/api/chat`, `/api/inbox`, `/api/outbox`
- Logs: `/api/logs`, `/api/logs/tail`

انظر `docs/api-contracts.md` لأشكال الطلب/الاستجابة.

## 🧭 كتيبات التشغيل

### Runbook: تشغيل المكدس المحلي الكامل
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

نقاط تحقق:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- افتح `http://127.0.0.1:5173/` وتأكد أن الواجهة يمكنها تحميل `/api/config`.
- اختياري: افتح `/api/version` وتحقق من رجوع metadata المتوقعة للواجهة الخلفية.

### Runbook: تصحيح backend فقط
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### Runbook: اختبار دخاني لـ codegen الحتمي
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

## 📡 لمحة API

مجموعات API الأساسية بنظرة سريعة:

| الفئة | نقاط النهاية |
| --- | --- |
| معلومات الصحة + وقت التشغيل | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| نموذج الخطة | `GET /api/plan`, `POST /api/plan` |
| السكربتات | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| سجل الإجراءات | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| وقت تشغيل خط المعالجة | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| المراسلة + السجلات | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET /api/outbox`, `GET /api/logs`, `GET /api/logs/tail` |
| إعدادات workspace | `GET/POST /api/workspaces/<name>/config` |

## 🧪 أمثلة
### مثال AAPS
```text
AUTOAPPDEV_PIPELINE 1

TASK  {"id":"t1","title":"Happy path demo"}
STEP  {"id":"s1","title":"Plan","block":"plan"}
ACTION {"id":"a1","kind":"note","params":{"text":"Read context and outline steps."}}
```

أمثلة كاملة:
- `examples/pipeline_formatted_script_v1.aaps`
- `examples/pipeline_ir_v1.json`
- `examples/pipeline_shell_annotated_v0.sh`
- `examples/pipeline_ir_codegen_demo_v0.json`

### توليد runner حتمي
```bash
python3 scripts/pipeline_codegen/generate_runner_from_ir.py \
  --in examples/pipeline_ir_codegen_demo_v0.json \
  --out /tmp/autoappdev_runner.sh

bash -n /tmp/autoappdev_runner.sh
scripts/pipeline_codegen/smoke_codegen.sh
```

### خط معالجة عرض حتمي
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
ثم استخدم عناصر التحكم Start/Pause/Resume/Stop في PWA وافحص `/api/logs`.

### استيراد من shell مشروح
```bash
curl -sS -X POST http://127.0.0.1:8788/api/scripts/import-shell \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "shell_text": "#!/usr/bin/env bash\n# AAPS: AUTOAPPDEV_PIPELINE 1\n# AAPS:\n# AAPS: TASK {\"id\":\"t1\",\"title\":\"Demo\"}\n# AAPS: STEP {\"id\":\"s1\",\"title\":\"Plan\",\"block\":\"plan\"}\n# AAPS: ACTION {\"id\":\"a1\",\"kind\":\"noop\"}\n"
}
JSON
```

## 🧱 ملاحظات التطوير
- الواجهة الخلفية مبنية على Tornado ومصممة لسهولة التطوير المحلي (بما في ذلك CORS مرن لمنافذ localhost المنفصلة).
- التخزين PostgreSQL أولًا مع سلوك توافق في `backend/storage.py`.
- مفاتيح كتل PWA وقيم `STEP.block` في السكربت متعمدة الاتساق (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- الإجراءات المدمجة للقراءة فقط؛ انسخها (clone) قبل التعديل.
- إجراء `update_readme` مقيّد بأمان المسار إلى أهداف README الخاصة بالـ workspace تحت `auto-apps/<workspace>/README.md`.
- توجد إشارات تاريخية لمسارات/أسماء في بعض الوثائق/السكربتات (`HeyCyan`, `LightMind`) موروثة من تطور المشروع. المسار المرجعي الحالي للمستودع هو جذر هذا المستودع.
- مجلد `i18n/` في الجذر موجود. من المتوقع وجود ملفات README اللغوية هناك أثناء التشغيلات متعددة اللغات.

### نموذج العمل وملفات الحالة
- افتراضي runtime هو `./runtime` ما لم يُتجاوز بواسطة `AUTOAPPDEV_RUNTIME_DIR`.
- حالة/سجل أتمتة التطوير الذاتي يتم تتبعها تحت `references/selfdev/`.
- مخرجات خط README تُسجَّل تحت `.auto-readme-work/<timestamp>/`.

### وضع الاختبارات (الحالي)
- يتضمن المستودع فحوصات دخانية وسكربتات عرض حتمية.
- لا توجد حاليًا مجموعة اختبارات آلية كاملة على مستوى الجذر/manifest CI معرّفة في metadata الجذر.
- الافتراض: التحقق يعتمد أساسًا على السكربتات في الوقت الحالي (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, قائمة تحقق من طرف إلى طرف).

## 🔐 ملاحظات الأمان
- إجراء `update_readme` مقيّد عمدًا بأهداف README الخاصة بالـ workspace (`auto-apps/<workspace>/README.md`) مع حماية من path traversal.
- التحقق من سجل الإجراءات يفرض حقول مواصفات إجراء مُطبّعة وقيمًا محدودة لمستويات reasoning المدعومة.
- سكربتات المستودع تفترض تنفيذًا محليًا موثوقًا؛ راجع محتوى السكربتات قبل تشغيلها في بيئات مشتركة أو قريبة من الإنتاج.
- قد يحتوي `.env` على قيم حساسة (`DATABASE_URL`, API keys). أبقِ `.env` خارج الالتزام واستخدم إدارة أسرار خاصة بكل بيئة خارج التطوير المحلي.

## 🔧 استكشاف الأخطاء وإصلاحها

| العرض | ما الذي يجب التحقق منه |
| --- | --- |
| `tmux not found` | ثبّت `tmux` أو شغّل backend/PWA يدويًا. |
| فشل backend عند الإقلاع بسبب متغيرات بيئة ناقصة | أعد التحقق من `.env` مقابل `.env.example` و `docs/env.md`. |
| أخطاء قاعدة البيانات (اتصال/مصادقة/مخطط) | تحقّق من `DATABASE_URL`; أعد تشغيل `conda run -n autoappdev python -m backend.apply_schema`; فحص اتصال اختياري: `conda run -n autoappdev python -m backend.db_smoketest`. |
| يتم تحميل PWA لكنه لا يستطيع استدعاء API | تأكد أن backend يستمع على host/port المتوقعين؛ أعد توليد `pwa/config.local.js` بإعادة تشغيل `./scripts/run_autoappdev_tmux.sh`. |
| يعيد Pipeline Start انتقالًا غير صالح | تحقق من حالة الخط الحالية أولًا؛ ابدأ من حالة `stopped`. |
| لا توجد تحديثات سجلات في الواجهة | تأكد من كتابة `runtime/logs/pipeline.log`; استخدم `/api/logs` و `/api/logs/tail` مباشرةً لعزل مشكلات الواجهة مقابل backend. |
| endpoint تحليل LLM يرجع disabled | اضبط `AUTOAPPDEV_ENABLE_LLM_PARSE=1` وأعد تشغيل backend. |
| فشل `conda run -n autoappdev ...` | أعد تشغيل `./scripts/setup_autoappdev_env.sh`; تأكد أن بيئة conda `autoappdev` موجودة (`conda env list`). |
| هدف API خاطئ في الواجهة الأمامية | تأكد من وجود `pwa/config.local.js` وأنه يشير إلى host/port الخلفية النشطة. |

للمسار اليدوي الحتمي للتحقق، استخدم `docs/end-to-end-demo-checklist.md`.

## 🌐 سير عمل README و i18n
- README في الجذر هو المصدر المرجعي الذي يستخدمه خط أتمتة README.
- النسخ متعددة اللغات متوقعة تحت `i18n/`.
- حالة مجلد i18n: ✅ موجود في هذا المستودع.
- مجموعة اللغات الحالية في هذا المستودع:
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
- يجب أن يبقى شريط التنقل اللغوي كسطر واحد أعلى كل نسخة README (بدون تكرار أشرطة اللغات).
- نقطة دخول خط README: `prompt_tools/auto-readme-pipeline.sh`.

### قيود توليد i18n (صارمة)
- عالج دائمًا التوليد متعدد اللغات عند تحديث محتوى README المرجعي.
- أنشئ/حدّث ملفات اللغات واحدًا تلو الآخر (تسلسليًا)، وليس على دفعات غامضة.
- احتفظ بسطر تنقل خيارات اللغة واحدًا فقط أعلى كل نسخة.
- لا تكرر أشرطة اللغات داخل الملف نفسه.
- حافظ على مقاطع الأوامر المرجعية، والروابط، ومسارات API، ومعنى الشارات عبر الترجمات.

الترتيب المقترح للتوليد واحدًا تلو الآخر:
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

جدول تغطية اللغات:

| اللغة | الملف |
| --- | --- |

## ❓ الأسئلة الشائعة

### هل PostgreSQL إلزامي؟
هو المفضل والمتوقع للتشغيل العادي. تحتوي طبقة التخزين على سلوك توافق احتياطي، لكن الاستخدام الشبيه بالإنتاج يجب أن يفترض توفر PostgreSQL عبر `DATABASE_URL`.

### لماذا كلا المتغيرين `AUTOAPPDEV_PORT` و `PORT`؟
`AUTOAPPDEV_PORT` خاص بالمشروع. أما `PORT` فهو اسم بديل مناسب للنشر. أبقِهما متوافقين ما لم تكن تتعمد تجاوز السلوك في مسار الإطلاق.

### من أين أبدأ إذا أردت فقط فحص واجهات API؟
شغّل backend فقط (`conda run -n autoappdev python -m backend.app`) ثم استخدم `/api/health` و `/api/version` و `/api/config`، ثم نقاط نهاية السكربتات/الإجراءات المذكورة في `docs/api-contracts.md`.

### هل يتم توليد ملفات README متعددة اللغات تلقائيًا؟
نعم. يتضمن المستودع `prompt_tools/auto-readme-pipeline.sh`، ويتم الحفاظ على النسخ اللغوية تحت `i18n/` مع سطر تنقل لغوي واحد أعلى كل نسخة.

## 🗺️ خارطة الطريق
- إكمال مهام التطوير الذاتي المتبقية بعد الحالة الحالية `51 / 55`.
- توسيع أدوات workspace/materials/context وتعزيز عقود المسارات الآمنة.
- مواصلة تحسين UX لوحة الإجراءات وتدفقات الإجراءات القابلة للتعديل.
- تعميق دعم README/واجهة المستخدم متعدد اللغات عبر `i18n/` وتبديل اللغة وقت التشغيل.
- تعزيز الفحوصات الدخانية/التكامل وتغطية CI (توجد حاليًا فحوصات دخانية مدفوعة بالسكربتات؛ لا يوجد manifest CI كامل موثق في الجذر).
- الاستمرار في تقوية حتمية parser/import/codegen حول AAPS v1 و IR القياسي.

## 🤝 المساهمة
المساهمات مرحب بها عبر issues وطلبات السحب.

سير عمل مقترح:
1. Fork وأنشئ فرع ميزة.
2. أبقِ التغييرات مركزة وقابلة لإعادة الإنتاج.
3. فضّل السكربتات/الاختبارات الحتمية حيثما أمكن.
4. حدّث الوثائق عند تغيّر السلوك/العقود (`docs/*`, عقود API, الأمثلة).
5. افتح PR مع السياق، وخطوات التحقق، وأي افتراضات لوقت التشغيل.

تشمل remotes الحالية للمستودع:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- قد توجد remotes إضافية في النسخ المحلية للمستودعات ذات الصلة (مثال موجود في workspace هذا: `novel`).

## 🙌 الدعم
- GitHub issues وطلبات السحب لتقارير الأخطاء ومقترحات الميزات.
- روابط الرعاية/التبرع مدرجة أدناه.

![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-2ea043)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-1f6feb)
![Maintained](https://img.shields.io/badge/Maintained-Yes-0e9f6e)

## 📄 الترخيص
لم يتم اكتشاف ملف `LICENSE` في جذر هذه اللقطة من المستودع.

ملاحظة افتراضية:
- حتى يتم إضافة ملف ترخيص، اعتبر شروط الاستخدام/إعادة التوزيع غير محددة وتحقق منها مع مسؤول الصيانة.

## ❤️ الرعاية والتبرع
- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400

إذا كان هذا المشروع يساعد سير عملك، فإن الرعاية تدعم مباشرة مهام التطوير الذاتي المستمرة، وجودة الوثائق، وتقوية الأدوات.
