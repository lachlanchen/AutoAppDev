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

مجموعة سكربتات قابلة لإعادة الاستخدام مع أدلة لبناء التطبيقات خطوة بخطوة من لقطات الشاشة/الـ markdown باستخدام Codex كأداة غير تفاعلية.

> 🎯 **المهمة:** جعل خطوط تطوير التطبيقات حتمية، قابلة للاستئناف، ومعتمدة على المخرجات.
>
> 🧩 **مبدأ التصميم:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ إشارات المشروع

| الإشارة | الاتجاه الحالي |
| --- | --- |
| نموذج التشغيل | Tornado backend + static PWA controller |
| تنفيذ الـ Pipeline | حتمي وقابل للاستئناف (`start/pause/resume/stop`) |
| استراتيجية التخزين | PostgreSQL-first مع سلوك توافق احتياطي |
| تدفق التوثيق | README رئيسي كمرجع + نسخ `i18n/` مؤتمتة |

### 🔗 تنقل سريع

| تحتاج | اذهب إلى |
| --- | --- |
| أول تشغيل محلي | [⚡ البدء السريع](#-البدء-السريع) |
| البيئة والمتغيرات المطلوبة | [⚙️ الإعداد](#-الإعداد) |
| واجهات API | [📡 لمحة API](#-لمحة-api) |
| أدلة التشغيل/التصحيح | [🧭 أدلة التشغيل](#-أدلة-التشغيل) |
| قواعد توليد README/i18n | [🌐 سير عمل README و i18n](#-سير-عمل-readme-و-i18n) |
| مصفوفة حل المشكلات | [🔧 استكشاف الأخطاء وإصلاحها](#-استكشاف-الأخطاء-وإصلاحها) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## حالة التطوير الذاتي (تحديث تلقائي)

- Updated: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- Progress: 51 / 55 tasks done
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- Philosophy: Plan -> Work -> Verify -> Summary -> Commit/Push (linear, resumable)

يتم تحديث هذا القسم بواسطة `scripts/auto-autoappdev-development.sh`.
لا تعدل المحتوى بين العلامتين.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ جدول المحتويات
- [🚀 نظرة عامة](#-نظرة-عامة)
- [🧭 لمحة عن المستودع](#-لمحة-عن-المستودع)
- [🧭 الفلسفة](#-الفلسفة)
- [✨ الميزات](#-الميزات)
- [📌 لمحة سريعة](#-لمحة-سريعة)
- [🏗️ المعمارية](#-المعمارية)
- [📚 المحتويات](#-المحتويات)
- [🗂️ بنية المشروع](#-بنية-المشروع)
- [✅ المتطلبات المسبقة](#-المتطلبات-المسبقة)
- [🧩 التوافق والافتراضات](#-التوافق-والافتراضات)
- [🛠️ التثبيت](#-التثبيت)
- [⚡ البدء السريع](#-البدء-السريع)
- [⚙️ الإعداد](#-الإعداد)
- [▶️ الاستخدام](#-الاستخدام)
- [🧭 أدلة التشغيل](#-أدلة-التشغيل)
- [📡 لمحة API](#-لمحة-api)
- [🧪 أمثلة](#-أمثلة)
- [🧱 ملاحظات التطوير](#-ملاحظات-التطوير)
- [🔐 ملاحظات الأمان](#-ملاحظات-الأمان)
- [🔧 استكشاف الأخطاء وإصلاحها](#-استكشاف-الأخطاء-وإصلاحها)
- [🌐 سير عمل README و i18n](#-سير-عمل-readme-و-i18n)
- [📘 سياق توليد Readme](#-سياق-توليد-readme)
- [❓ الأسئلة الشائعة](#-الأسئلة-الشائعة)
- [🗺️ خارطة الطريق](#-خارطة-الطريق)
- [🤝 المساهمة](#-المساهمة)
- [❤️ Support](#-support)
- [📄 الترخيص](#-الترخيص)

## 🧭 لمحة عن المستودع

| المحور | الإعداد الحالي |
| --- | --- |
| الحلقة الأساسية | Plan → Work → Debug → Fix → Summary → Commit/Push |
| نموذج التشغيل | Tornado backend + static PWA controller |
| آلة الحالات | `start` / `pause` / `resume` / `stop` |
| التخزين | PostgreSQL-first مع توافق JSON احتياطي |
| التوثيق | `README.md` رئيسي مع مخرجات متعددة اللغات في `i18n/` |

## 🚀 نظرة عامة
AutoAppDev هو مشروع تحكم لخطوط تطوير تطبيقات طويلة التشغيل وقابلة للاستئناف. يجمع بين:

1. واجهة Tornado backend API مع تخزين مدعوم بـ PostgreSQL (إضافةً إلى سلوك احتياطي JSON محلي في كود التخزين).
2. واجهة تحكم static PWA شبيهة بـ Scratch.
3. سكربتات ووثائق لتأليف الـ pipeline، توليد الكود الحتمي، حلقات التطوير الذاتي، وأتمتة README.

المشروع محسّن لتنفيذ الوكلاء بشكل متوقع مع تسلسل صارم وسجل عمل قائم على المخرجات.

### 🎨 لماذا يوجد هذا المستودع

| المحور | ما يعنيه عمليًا |
| --- | --- |
| الحتمية | سير عمل canonical pipeline IR + parser/import/codegen مصمم للتكرار |
| قابلية الاستئناف | آلة حالات lifecycle صريحة (`start/pause/resume/stop`) للتشغيل طويل المدى |
| قابلية التشغيل | سجلات تشغيل، وقنوات inbox/outbox، وحلقات تحقق تعتمد السكربتات |
| التوثيق أولًا | العقود/المواصفات/الأمثلة موجودة في `docs/` مع تدفق README متعدد اللغات مؤتمت |

## 🧭 الفلسفة
يتعامل AutoAppDev مع الوكلاء كأدوات ويحافظ على استقرار العمل عبر حلقة صارمة وقابلة للاستئناف:

1. التخطيط
2. التنفيذ
3. التصحيح/التحقق (مع مهلات زمنية)
4. الإصلاح
5. التلخيص + التسجيل
6. Commit + push

يهدف تطبيق المتحكم إلى تجسيد نفس المفاهيم ككتل/إجراءات شبيهة بـ Scratch (بما في ذلك إجراء `update_readme` المشترك) حتى تبقى كل مساحة عمل محدثة وقابلة لإعادة الإنتاج.

### 🔁 هدف حالات دورة الحياة

| انتقال الحالة | الهدف التشغيلي |
| --- | --- |
| `start` | بدء pipeline من حالة stopped/ready |
| `pause` | إيقاف التنفيذ الطويل بأمان دون فقدان السياق |
| `resume` | المتابعة من حالة/مخرجات التشغيل المحفوظة |
| `stop` | إنهاء التنفيذ والرجوع إلى حالة غير تشغيلية |

## ✨ الميزات
- تحكم قابل للاستئناف في دورة حياة الـ pipeline: start و pause و resume و stop.
- واجهات مكتبة سكربتات AAPS (`.aaps`) و canonical IR (`autoappdev_ir` v1).
- خط parser/import حتمي:
  - تحليل سكربتات AAPS المنسقة.
  - استيراد shell موضح عبر تعليقات `# AAPS:`.
  - خيار parse احتياطي بمساعدة Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- سجل إجراءات مع إجراءات مدمجة + إجراءات قابلة للتحرير/مخصصة (تدفق clone/edit للإجراءات المدمجة للقراءة فقط).
- كتل PWA شبيهة بـ Scratch ولوحة إجراءات محملة أثناء التشغيل (`GET /api/actions`).
- قنوات رسائل التشغيل:
  - Inbox (`/api/inbox`) لتوجيهات المشغل -> pipeline.
  - Outbox (`/api/outbox`) تتضمن إدخال طابور ملفات من `runtime/outbox`.
- بث تدريجي للسجلات من backend وسجلات pipeline (`/api/logs`, `/api/logs/tail`).
- توليد runner حتمي من canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- مشغل تطوير ذاتي لتطور المستودع بشكل تكراري (`scripts/auto-autoappdev-development.sh`).
- خط أتمتة README مع هيكل توليد متعدد اللغات تحت `i18n/`.

## 📌 لمحة سريعة

| المجال | التفاصيل |
| --- | --- |
| وقت التشغيل الأساسي | Tornado backend + static PWA frontend |
| التخزين | PostgreSQL-first مع سلوك توافق في `backend/storage.py` |
| نموذج pipeline | Canonical IR (`autoappdev_ir` v1) وتنسيق سكربتات AAPS |
| تدفق التحكم | Start / Pause / Resume / Stop lifecycle |
| نمط التطوير | حلقة تطوير ذاتي قابلة للاستئناف + سير سكربت/codegen حتمي |
| README/i18n | خط README مؤتمت مع هيكل `i18n/` |

## 🏗️ المعمارية

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
- إتاحة APIs للمتحكم خاصة بالسكربتات، الإجراءات، الخطة، دورة حياة الـ pipeline، السجلات، inbox/outbox، وإعداد مساحة العمل.
- التحقق من أصول سكربتات pipeline وتخزينها.
- تنسيق حالة تنفيذ الـ pipeline وانتقالات الحالة.
- توفير سلوك احتياطي حتمي عندما لا يتوفر مجمع اتصال قاعدة البيانات.

### مسؤوليات الواجهة الأمامية
- عرض واجهة الكتل الشبيهة بـ Scratch وتدفق تحرير الـ pipeline.
- تحميل لوحة الإجراءات ديناميكيًا من سجل الواجهة الخلفية.
- إدارة عناصر التحكم في دورة الحياة ومراقبة الحالة/السجلات/الرسائل.

## 📚 المحتويات
خريطة مرجعية لأكثر الوثائق والسكربتات والأمثلة استخدامًا:

- `docs/auto-development-guide.md`: فلسفة ومتطلبات ثنائية اللغة (EN/ZH) لوكيل تطوير تلقائي طويل التشغيل وقابل للاستئناف.
- `docs/ORDERING_RATIONALE.md`: مثال مبررات لتسلسل خطوات تعتمد على لقطات الشاشة.
- `docs/controller-mvp-scope.md`: نطاق MVP للمتحكم (الشاشات + أقل APIs).
- `docs/end-to-end-demo-checklist.md`: قائمة تحقق عرض توضيحي يدوي حتمي من طرف إلى طرف (backend + PWA happy path).
- `docs/env.md`: اتفاقيات متغيرات البيئة (`.env`).
- `docs/api-contracts.md`: عقود الطلب/الاستجابة لواجهات المتحكم.
- `docs/pipeline-formatted-script-spec.md`: تنسيق سكربت pipeline القياسي (AAPS) ومخطط canonical IR ‏(TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: مولد حتمي لإنتاج bash pipeline runners قابلة للتشغيل من canonical IR.
- `docs/common-actions.md`: عقود/مواصفات الإجراءات الشائعة (يتضمن `update_readme`).
- `docs/workspace-layout.md`: مجلدات مساحة العمل القياسية + العقود (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: تشغيل تطبيق AutoAppDev ‏(backend + PWA) عبر tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: تشغيل مشغل التطوير الذاتي لـ AutoAppDev عبر tmux.
- `scripts/app-auto-development.sh`: مشغل pipeline خطي (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) مع دعم الاستئناف/الحالة.
- `scripts/generate_screenshot_docs.sh`: مولد وصف markdown من لقطات الشاشة (مدعوم Codex).
- `scripts/setup_autoappdev_env.sh`: سكربت تهيئة conda الأساسي للتشغيل المحلي.
- `scripts/setup_backend_env.sh`: سكربت مساعد بيئة backend.
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
- `tmux` لجلسات backend+PWA أو التطوير الذاتي بأمر واحد.
- PostgreSQL يمكن الوصول إليه عبر `DATABASE_URL`.
- اختياري: CLI `codex` للتدفقات المدعومة بـ Codex (self-dev، parse-llm الاحتياطي، auto-readme pipeline).

مصفوفة متطلبات سريعة:

| المكون | مطلوب | الغرض |
| --- | --- | --- |
| `bash` | نعم | تنفيذ السكربتات |
| Python `3.11+` | نعم | أدوات backend + codegen |
| Conda | نعم (التدفق الموصى به) | سكربتات تهيئة البيئة |
| PostgreSQL | نعم (الوضع المفضل) | التخزين الأساسي عبر `DATABASE_URL` |
| `tmux` | موصى به | إدارة جلسات backend/PWA و self-dev |
| `codex` CLI | اختياري | parse بمساعدة LLM وأتمتة README/self-dev |

## 🧩 التوافق والافتراضات

| الموضوع | التوقع الحالي |
| --- | --- |
| نظام التشغيل المحلي | Linux/macOS هما الهدف الأساسي (`bash` scripts) |
| نسخة Python | `3.11` (تدار بواسطة `scripts/setup_autoappdev_env.sh`) |
| وضع التخزين | PostgreSQL هو المفضل ويُعامل كخيار مرجعي |
| سلوك احتياطي | `backend/storage.py` يتضمن توافق JSON لسيناريوهات التراجع |
| نموذج الشبكة | تطوير localhost بمنافذ منفصلة (backend + static PWA) |
| أدوات الوكيل | `codex` CLI اختياري إلا عند استخدام parse بمساعدة LLM أو أتمتة self-dev |

الافتراضات المستخدمة في هذا README:
- تشغّل الأوامر من جذر المستودع ما لم يُذكر خلاف ذلك.
- يتم إعداد `.env` قبل تشغيل خدمات backend.
- `conda` و `tmux` متاحان لتدفقات التشغيل الموصى بها بأمر واحد.

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
- قاعدة API للواجهة الخلفية: `http://127.0.0.1:8788`
- فحص الصحة: `http://127.0.0.1:8788/api/health`

تحقق سريع بأمر واحد:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

خريطة نقاط نهاية سريعة:

| السطح | URL |
| --- | --- |
| واجهة PWA | `http://127.0.0.1:5173/` |
| Backend API | `http://127.0.0.1:8788` |
| Health endpoint | `http://127.0.0.1:8788/api/health` |

## ⚙️ الإعداد
الملف الأساسي: `.env` (راجع `docs/env.md` و `.env.example`).

### متغيرات مهمة

| المتغير | الغرض |
| --- | --- |
| `SECRET_KEY` | مطلوب حسب الاتفاق |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | إعدادات ربط backend |
| `DATABASE_URL` | PostgreSQL DSN (المفضل) |
| `AUTOAPPDEV_RUNTIME_DIR` | تجاوز مجلد التشغيل (الافتراضي `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | هدف تشغيل pipeline الافتراضي |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | تفعيل `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | إعدادات Codex الافتراضية للإجراءات/النقاط |
| `AI_API_BASE_URL`, `AI_API_KEY` | محجوز لتكاملات مستقبلية |

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

| الوضع | الأمر | الملاحظات |
| --- | --- | --- |
| تشغيل backend + PWA (موصى به) | `./scripts/run_autoappdev_tmux.sh --restart` | Backend `http://127.0.0.1:8788`, PWA `http://127.0.0.1:5173/` |
| تشغيل backend فقط | `conda run -n autoappdev python -m backend.app` | يستخدم إعدادات الربط + DB من `.env` |
| تشغيل خادم PWA ثابت فقط | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | مفيد لفحوصات الواجهة الأمامية فقط |
| تشغيل مشغل self-dev في tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | حلقة تطوير ذاتي قابلة للاستئناف |

### خيارات السكربت الشائعة
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### تحليل وتخزين السكربتات
- تحليل AAPS عبر API: `POST /api/scripts/parse`
- استيراد shell موضح: `POST /api/scripts/import-shell`
- تحليل LLM اختياري: `POST /api/scripts/parse-llm` (يتطلب `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### APIs التحكم بالـ pipeline
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### APIs أخرى كثيرة الاستخدام
- الصحة/الإصدار/الإعداد: `/api/health`, `/api/version`, `/api/config`
- الخطة/السكربتات: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- الإجراءات: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- المراسلة: `/api/chat`, `/api/inbox`, `/api/outbox`
- السجلات: `/api/logs`, `/api/logs/tail`

راجع `docs/api-contracts.md` لأشكال الطلب/الاستجابة.

## 🧭 أدلة التشغيل

### دليل: تشغيل الحزمة المحلية كاملة
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

نقاط تحقق:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- افتح `http://127.0.0.1:5173/` وتأكد أن الواجهة تحمل `/api/config`.
- اختياريًا: افتح `/api/version` وتحقق من رجوع بيانات backend المتوقعة.

### دليل: تصحيح backend فقط
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### دليل: اختبار دخاني codegen حتمي
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

مجموعات API الأساسية باختصار:

| الفئة | النقاط |
| --- | --- |
| الصحة + معلومات التشغيل | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| نموذج الخطة | `GET /api/plan`, `POST /api/plan` |
| السكربتات | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| سجل الإجراءات | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| تشغيل الـ pipeline | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| المراسلة + السجلات | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET /api/logs/tail` |
| إعدادات مساحة العمل | `GET/POST /api/workspaces/<name>/config` |

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

### Pipeline عرض حتمي
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
ثم استخدم عناصر Start/Pause/Resume/Stop في PWA وافحص `/api/logs`.

### الاستيراد من shell موضح
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
- الواجهة الخلفية مبنية على Tornado ومصممة لسهولة التطوير المحلي (بما في ذلك CORS متساهل لمنافذ localhost المنفصلة).
- التخزين PostgreSQL-first مع سلوك توافق في `backend/storage.py`.
- مفاتيح كتل PWA وقيم `STEP.block` في السكربت متعمدة التوافق (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- الإجراءات المدمجة للقراءة فقط؛ انسخ clone قبل التحرير.
- إجراء `update_readme` مقيّد أمنيًا لأهداف README داخل مساحة العمل تحت `auto-apps/<workspace>/README.md`.
- توجد إشارات تاريخية لمسارات/أسماء في بعض الوثائق والسكربتات (`HeyCyan`, `LightMind`) موروثة من تطور المشروع. المسار المرجعي الحالي هو جذر هذا المستودع.
- مجلد `i18n/` في الجذر موجود. من المتوقع وجود ملفات README اللغوية هناك في التشغيل متعدد اللغات.

### نموذج العمل وملفات الحالة
- وقت التشغيل الافتراضي هو `./runtime` ما لم يتم تجاوزه عبر `AUTOAPPDEV_RUNTIME_DIR`.
- حالة/سجل أتمتة self-dev يتم تتبعها تحت `references/selfdev/`.
- مخرجات خط README يتم تسجيلها تحت `.auto-readme-work/<timestamp>/`.

### وضع الاختبارات (حاليًا)
- المستودع يتضمن فحوصات smoke وسكربتات عرض حتمية.
- لا توجد حاليًا مجموعة اختبارات آلية/تعريف CI كامل على مستوى الجذر.
- الافتراض: التحقق يعتمد أساسًا على السكربتات حاليًا (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, قائمة تحقق end-to-end).

## 🔐 ملاحظات الأمان
- إجراء `update_readme` مقيّد عمدًا بأهداف README الخاصة بمساحة العمل (`auto-apps/<workspace>/README.md`) مع حماية من path traversal.
- تحقق سجل الإجراءات يفرض حقول مواصفات إجراء مُطبّعة وقيمًا محدودة لمستويات reasoning المدعومة.
- سكربتات المستودع تفترض تنفيذًا محليًا موثوقًا؛ راجع محتوى السكربتات قبل التشغيل في بيئات مشتركة أو قريبة من الإنتاج.
- قد يحتوي `.env` على قيم حساسة (`DATABASE_URL`, API keys). أبقِ `.env` خارج الالتزام واستخدم إدارة أسرار خاصة بكل بيئة خارج التطوير المحلي.

## 🔧 استكشاف الأخطاء وإصلاحها

| العرض | ما الذي يجب فحصه |
| --- | --- |
| `tmux not found` | ثبّت `tmux` أو شغّل backend/PWA يدويًا. |
| فشل backend عند الإقلاع بسبب نقص env | أعد التحقق من `.env` مقارنة بـ `.env.example` و `docs/env.md`. |
| أخطاء قاعدة البيانات (اتصال/مصادقة/مخطط) | تحقق من `DATABASE_URL`; أعد تشغيل `conda run -n autoappdev python -m backend.apply_schema`; فحص اتصال اختياري: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA تعمل لكن لا تستدعي API | تأكد أن backend يستمع على host/port المتوقعين؛ أعد توليد `pwa/config.local.js` عبر إعادة تشغيل `./scripts/run_autoappdev_tmux.sh`. |
| Pipeline Start يرجع انتقال حالة غير صالح | تحقق من حالة pipeline الحالية أولًا؛ ابدأ من `stopped`. |
| لا تحديثات سجلات في الواجهة | تأكد من كتابة `runtime/logs/pipeline.log`; استخدم `/api/logs` و `/api/logs/tail` مباشرةً لعزل مشكلة UI عن backend. |
| نقطة LLM parse معطلة | اضبط `AUTOAPPDEV_ENABLE_LLM_PARSE=1` ثم أعد تشغيل backend. |
| فشل `conda run -n autoappdev ...` | أعد تشغيل `./scripts/setup_autoappdev_env.sh`; وتأكد من وجود بيئة conda `autoappdev` (`conda env list`). |
| هدف API خاطئ في الواجهة الأمامية | تأكد من وجود `pwa/config.local.js` وأنه يشير إلى host/port النشطين للواجهة الخلفية. |

للمسار اليدوي الحتمي للتحقق، استخدم `docs/end-to-end-demo-checklist.md`.

## 🌐 سير عمل README و i18n
- ملف README الجذري هو المصدر المرجعي المستخدم بواسطة خط أتمتة README.
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
- يجب أن يبقى سطر تنقل اللغات كسطر واحد أعلى كل نسخة README (بدون تكرار شريط اللغات).
- نقطة دخول خط README: `prompt_tools/auto-readme-pipeline.sh`.

### قيود توليد i18n (صارمة)
- يجب دائمًا معالجة التوليد متعدد اللغات عند تحديث محتوى README المرجعي.
- أنشئ/حدّث ملفات اللغات واحدًا تلو الآخر (تسلسليًا)، وليس على دفعات غامضة.
- احتفظ بسطر تنقل لغات واحد بالضبط أعلى كل نسخة.
- لا تكرر أشرطة اللغات داخل الملف نفسه.
- حافظ على مقاطع الأوامر والروابط ومسارات API وقصد الشارات عبر الترجمات.

ترتيب توليد مقترح واحدًا تلو الآخر:
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

جدول تغطية اللغات:

| اللغة | الملف |
| --- | --- |

ملاحظة مساحة العمل المرصودة:
- قد يظهر `i18n/README.zh-Hant.md.tmp` كأثر ترجمة مؤقت؛ أبقِ الملفات النهائية المرجعية بصيغة `README.<lang>.md`.

## 📘 سياق توليد Readme

- Pipeline run timestamp: `20260301_095119`
- Trigger: `./README.md` first complete draft generation (canonical-base incremental update)
- Input user prompt: `Use current README as canonical base. No reduction: only increment and improve. Preserve existing content, links, badges, commands, and details. Always process multilingual generation (do not skip): ensure i18n exists and generate/update language files one-by-one with a single language-options line at the top and no duplicates.`
- Goal: generate a complete, beautiful README draft with required sections and support information
- Source snapshot used:
  - `./.auto-readme-work/20260301_095119/pipeline-context.md`
  - `./.auto-readme-work/20260301_095119/repo-structure-analysis.md`
- This file was generated from repository contents and preserved as a canonical draft entry point.

## ❓ الأسئلة الشائعة

### هل PostgreSQL إلزامي؟
مفضل ومتوقع للتشغيل الطبيعي. طبقة التخزين تحتوي على سلوك توافق احتياطي، لكن الاستخدام الأقرب للإنتاج يجب أن يفترض توفر PostgreSQL عبر `DATABASE_URL`.

### لماذا يوجد `AUTOAPPDEV_PORT` و `PORT` معًا؟
`AUTOAPPDEV_PORT` خاص بالمشروع. أما `PORT` فهو اسم بديل ملائم لبيئات النشر. اجعلهما متطابقين ما لم تكن تتعمد تجاوز السلوك في مسار التشغيل.

### من أين أبدأ إذا أردت فقط فحص APIs؟
شغّل backend فقط (`conda run -n autoappdev python -m backend.app`) واستخدم `/api/health`, `/api/version`, `/api/config` ثم نقاط السكربت/الإجراء المذكورة في `docs/api-contracts.md`.

### هل يتم توليد READMEs متعددة اللغات تلقائيًا؟
نعم. يتضمن المستودع `prompt_tools/auto-readme-pipeline.sh`، ويتم الحفاظ على نسخ اللغات تحت `i18n/` مع سطر تنقل لغات واحد أعلى كل نسخة.

## 🗺️ خارطة الطريق
- إكمال مهام self-dev المتبقية بعد الحالة الحالية `51 / 55`.
- توسيع أدوات مساحة العمل/المواد/السياق مع عقود مسارات آمنة أقوى.
- مواصلة تحسين تجربة لوحة الإجراءات وتدفقات الإجراءات القابلة للتحرير.
- تعميق دعم README/UI متعدد اللغات عبر `i18n/` وتبديل اللغة أثناء التشغيل.
- تقوية فحوصات smoke/integration وتغطية CI (حاليًا توجد فحوصات smoke معتمدة على السكربتات؛ لا يوجد تعريف CI كامل موثق في الجذر).
- الاستمرار في تقوية حتمية parser/import/codegen حول AAPS v1 و canonical IR.

## 🤝 المساهمة
المساهمات مرحب بها عبر issues وطلبات السحب.

سير عمل مقترح:
1. Fork وأنشئ فرع ميزة.
2. حافظ على تغييرات مركزة وقابلة لإعادة الإنتاج.
3. فضّل السكربتات/الاختبارات الحتمية متى أمكن.
4. حدّث الوثائق عندما تتغير السلوكيات/العقود (`docs/*`, عقود API, الأمثلة).
5. افتح PR يتضمن السياق، خطوات التحقق، وأي افتراضات تشغيل.

الـ remotes الحالية للمستودع تتضمن:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- قد توجد remotes إضافية في النسخ المحلية لمستودعات ذات صلة (مثال موجود في مساحة العمل هذه: `novel`).

---

## 📄 الترخيص
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

لم يتم اكتشاف ملف `LICENSE` في جذر هذا المستودع ضمن هذه اللقطة.

ملاحظة افتراضية:
- إلى أن تتم إضافة ملف ترخيص، تعامل مع شروط الاستخدام/إعادة التوزيع على أنها غير محددة وتأكد من الأمر مع maintainer.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
