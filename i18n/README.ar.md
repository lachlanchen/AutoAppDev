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

سكريبتات وأدلة قابلة لإعادة الاستخدام لبناء التطبيقات خطوة بخطوة من لقطات الشاشة/ملفات Markdown باستخدام Codex كأداة غير تفاعلية.

> 🎯 **المهمة:** جعل خطوط أنابيب تطوير التطبيقات حتمية وقابلة للاستئناف ومبنية على الأدلة.
>
> 🧩 **مبدأ التصميم:** Plan -> Work -> Verify -> Summary -> Commit/Push.

---

### 🎛️ إشارات المشروع

| الإشارة | الاتجاه الحالي |
| --- | --- |
| نموذج التشغيل | خلفية Tornado + وحدة تحكم PWA ثابتة |
| تنفيذ الخط الانتاجي | حتمي وقابل للاستئناف (`start/pause/resume/stop`) |
| استراتيجية الاستمرارية | PostgreSQL-أساسًا مع سلوك رجوع متوافق |
| تدفق التوثيق | README أساسي مرجعي + نسخ متعددة اللغات تلقائية داخل `i18n/` |

### 🔗 التنقل السريع

| الحاجة | انتقل إلى |
| --- | --- |
| التشغيل المحلي الأول | [⚡ البدء السريع](#-البدء-السريع) |
| البيئة والمتغيرات المطلوبة | [⚙️ الإعدادات](#-الإعدادات) |
| واجهة API | [📡 لقطة API](#-لقطة-api) |
| تشغيل وتشخيص runtime | [🧭 أدلة التشغيل](#-أدلة-التشغيل) |
| قواعد توليد README/i18n | [🌐 سير عمل README و i18n](#-سير-عمل-readme--i18n) |
| مصفوفة استكشاف الأخطاء | [🔧 استكشاف الأخطاء](#-استكشاف-الأخطاء) |

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## حالة التطوير الذاتي (محدث تلقائيًا)

- آخر تحديث: 2026-02-16T00:27:20Z
- مرحلة الالتزام: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- التقدم: 51 / 55 مهمة مكتملة
- جلسة Codex: `019c6056-f33a-7f31-b08f-0ca40c365351`
- الفلسفة: Plan -> Work -> Verify -> Summary -> Commit/Push (تسلسل خطي قابل للاستئناف)

يتم تحديث هذا القسم بواسطة `scripts/auto-autoappdev-development.sh`.
لا تعدّل المحتوى بين العلامات.

<!-- AUTOAPPDEV:STATUS:END -->

## 🗂️ جدول المحتويات
- [🚀 النظرة العامة](#-النظرة-العامة)
- [🧭 الفلسفة](#-الفلسفة)
- [✨ الميزات](#-الميزات)
- [📌 لمحة سريعة](#-لمحة-سريعة)
- [🏗️ البنية المعمارية](#-البنية-المعمارية)
- [📚 المحتوى](#-المحتوى)
- [🗂️ هيكلة المشروع](#-هيكلة-المشروع)
- [✅ المتطلبات المسبقة](#-المتطلبات-المسبقة)
- [🧩 التوافق والافتراضات](#-التوافق-والافتراضات)
- [🛠️ التثبيت](#-التثبيت)
- [⚡ البدء السريع](#-البدء-السريع)
- [⚙️ الإعدادات](#-الإعدادات)
- [▶️ الاستخدام](#-الاستخدام)
- [🧭 أدلة التشغيل](#-أدلة-التشغيل)
- [📡 لقطة API](#-لقطة-api)
- [🧪 الأمثلة](#-الأمثلة)
- [🧱 ملاحظات التطوير](#-ملاحظات-التطوير)
- [🔐 ملاحظات الأمان](#-ملاحظات-الأمان)
- [🔧 استكشاف الأخطاء](#-استكشاف-الأخطاء)
- [🌐 سير عمل README & i18n](#-سير-عمل-readme--i18n)
- [📘 سياق توليد Readme](#-سياق-توليد-readme)
- [❓ الأسئلة الشائعة](#-الأسئلة-الشائعة)
- [🗺️ خارطة الطريق](#-خريطة-الطريق)
- [🤝 المساهمة](#-المساهمة)
- [❤️ Support](#-support)
- [📄 License](#-license)

## 🧭 لقطة المشروع

| التركيز | الإعداد الحالي |
| --- | --- |
| الحلقة الأساسية | Plan → Work → Debug → Fix → Summary → Commit/Push |
| نموذج التشغيل | خلفية Tornado + وحدة تحكم PWA ثابتة |
| آلة الحالة | `start` / `pause` / `resume` / `stop` |
| التخزين | PostgreSQL-أساسًا مع توافق JSON كإرجاع احتياطي |
| التوثيق | `README.md` الأساسي + مخرجات `i18n/` متعددة اللغات |

## 🚀 نظرة عامة
AutoAppDev هو مشروع تحكم لمسارات تطوير التطبيقات طويلة الأجل والقابلة للاستئناف. يجمع بين:

1. واجهة خلفية Tornado مع تخزين مبني على PostgreSQL (مع سلوك احتياطي JSON محلي في كود التخزين).
2. واجهة تحكم ثابتة بنمط Scratch لواجهة PWA.
3. سكربتات وملفات توثيق لكتابة مسارات التشغيل، وإنشاء الكود الحتمي، وحلقات التطوير الذاتي، وأتمتة README.

المشروع مُحسَّن للتنفيذ المتوقع للوكلاء بتسلسل صارم وتاريخ سير عمل موجّه نحو الأدلة.

### 🎨 لماذا وُجد هذا المستودع

| الموضوع | ما يعنيه عمليًا |
| --- | --- |
| الحتمية | IR موحد + تدفقات parser/import/codegen مصممة للتكرار |
| قابلية الاستئناف | آلة حالة دورة حياة صريحة (`start/pause/resume/stop`) للتشغيلات الطويلة |
| القابلية للتشغيل | سجلات تشغيل، قنوات inbox/outbox، وحلقات تحقق موجهة بالسكربتات |
| التوثيق أولًا | العقود/المواصفات/الأمثلة موجودة في `docs/`، مع تدفق README متعدد اللغات تلقائي |

## 🧭 الفلسفة
يتعامل AutoAppDev مع الوكلاء كأدوات ويحافظ على استقرار العمل عبر حلقة صارمة وقابلة للاستئناف:

1. Plan
2. Implement
3. Debug/verify (مع قيود زمنية)
4. Fix
5. Summarize + log
6. Commit + push

تسعى تطبيقات التحكم إلى تجسيد نفس مفاهيم كتل/إجراءات نمط Scratch (بما في ذلك إجراء مشترك `update_readme`) حتى يبقى كل workspace حديثًا وقابلاً لإعادة الإنتاج.

### 🔁 قصد حالة دورة الحياة

| انتقال الحالة | القصد التشغيلي |
| --- | --- |
| `start` | بدء خط الأنابيب من حالة متوقف/جاهز |
| `pause` | إيقاف تنفيذ طويل بأمان دون فقدان السياق |
| `resume` | المتابعة من حالة التشغيل/الآثار المحفوظة |
| `stop` | إنهاء التنفيذ والعودة لحالة غير تشغيلية |

## ✨ الميزات
- تحكم قابل للاستئناف في دورة حياة الخطّ: start و pause و resume و stop.
- واجهات API لمكتبة السكربتات لمسارات AAPS (`.aaps`) و IR موحد (`autoappdev_ir` v1).
- مسار parser/import حتمي:
  - تحليل سكربتات AAPS المنسّقة.
  - استيراد shell المشروح عبر تعليقات `# AAPS:`.
  - بديل اختياري لتحليل معتمد على LLM عبر Codex (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- سجل إجراءات مع إجراءات مدمجة + إجراءات قابلة للتعديل/مخصصة (تدفق clone/edit للإجراءات الجاهزة للقراءة فقط).
- كتل PWA شبيهة بـ Scratch ولوحة إجراءات يتم تحميلها أثناء التشغيل (`GET /api/actions`).
- قنوات رسائل تشغيل:
  - Inbox (`/api/inbox`) لإرشاد المشغّل -> الخطّ.
  - Outbox (`/api/outbox`) تشمل استقبال طوابير الملفات من `runtime/outbox`.
- تدفق تسجيل متدرج من الخلفية وسجلات الخطّ (`/api/logs`، `/api/logs/tail`).
- توليد تشغيل حتمي من IR موحد (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- محرك تطوير ذاتي للتطور التكراري للمستودع (`scripts/auto-autoappdev-development.sh`).
- أتمتة README مع بنية توليد متعددة اللغات تحت `i18n/`.

## 📌 لمحة سريعة

| المجال | التفاصيل |
| --- | --- |
| وقت التشغيل الأساسي | خلفية Tornado + واجهة PWA ثابتة |
| التخزين | PostgreSQL-أساسًا مع سلوك توافق في `backend/storage.py` |
| نموذج الخط | IR موحد (`autoappdev_ir` v1) وتنسيق سكربت AAPS |
| تدفق التحكم | دورة حياة Start / Pause / Resume / Stop |
| وضع التطوير | حلقة self-dev قابلة للاستئناف + تدفقات script/codegen حتمية |
| README/i18n | خطّ README أوتوماتيكي مع بنية `i18n/` |

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

### مسؤوليات الخلفية
- إتاحة واجهات API للتحكم في السكربتات والإجراءات والخطة ودورة حياة pipeline والسجلات و inbox/outbox وإعدادات workspace.
- التحقق من أصول سكربتات الخطّ وحفظها.
- تنسيق حالة تنفيذ pipeline وتحولات الحالة.
- توفير سلوك احتياطي حتمي عند عدم توفر تجمع DB.

### مسؤوليات الواجهة الأمامية
- عرض واجهة كتل مشابهة لـ Scratch وسير تحرير الخط.
- تحميل لوحة الإجراءات ديناميكيًا من سجل الإجراءات الخلفي.
- تشغيل عناصر التحكم في دورة الحياة ومراقبة الحالة والسجلات/الرسائل.

## 📚 المحتوى
خريطة مرجعية لأكثر المستندات والسكربتات والأمثلة استخدامًا:

- `docs/auto-development-guide.md`: فلسفة ومتطلبات ثنائية اللغة (EN/ZH) لوكيل تطوير ذاتي طويل ومتاح للاستئناف.
- `docs/ORDERING_RATIONALE.md`: مثال على مبررات ترتيب الخطوات المستندة إلى لقطات الشاشة.
- `docs/controller-mvp-scope.md`: نطاق MVP للمتتحكم (الشاشات + واجهات API الأساسية).
- `docs/end-to-end-demo-checklist.md`: قائمة تحقق ديمو end-to-end حتمية (backend + مسار النجاح في PWA).
- `docs/env.md`: اتفاقيات متغيرات البيئة (`.env`).
- `docs/api-contracts.md`: عقود طلب/استجابة API الخاصة بالتحكم.
- `docs/pipeline-formatted-script-spec.md`: تنسيق سكربت pipeline قياسي (AAPS) ومخطط IR موحد (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: مولد حتمي للـ bash runner القابل للتنفيذ من IR موحد.
- `docs/common-actions.md`: عقود/مواصفات الإجراءات الشائعة (تتضمن `update_readme`).
- `docs/workspace-layout.md`: ملفات workspace القياسية + العقود (`materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps`).
- `scripts/run_autoappdev_tmux.sh`: تشغيل تطبيق AutoAppDev (back-end + PWA) داخل tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: تشغيل محرك self-dev الخاص بـ AutoAppDev داخل tmux.
- `scripts/app-auto-development.sh`: مشغّل خط مستقيم (`plan -> backend -> PWA -> Android -> iOS -> review -> summary`) مع دعم استئناف/حالة.
- `scripts/generate_screenshot_docs.sh`: مولّد وصف markdown من لقطة الشاشة (بدعم Codex).
- `scripts/setup_autoappdev_env.sh`: سكربت التمهيد الرئيسي لبيئة conda للتشغيل المحلي.
- `scripts/setup_backend_env.sh`: سكربت مساعد لتهيئة backend.
- `examples/ralph-wiggum-example.sh`: مثال لمساعد تلقائي لأتمتة Codex CLI.

## 🗂️ هيكلة المشروع
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
- نظام تشغيل يحتوي على `bash`.
- Python `3.11+`.
- conda (`conda`) لسكريبتات الإعداد المرفقة.
- `tmux` للجلسات ذات الأمر الواحد للباك إند + PWA أو جلسات self-dev.
- PostgreSQL يمكن الوصول إليه عبر `DATABASE_URL`.
- اختياريًا: `codex` CLI لمسارات Codex (self-dev، تحليل LLM بديل، أتمتة auto-readme).

مصفوفة المتطلبات السريعة:

| المكوّن | مطلوب | الغرض |
| --- | --- | --- |
| `bash` | نعم | تنفيذ السكربتات |
| Python `3.11+` | نعم | الخلفية + أدوات codegen |
| Conda | نعم (موصى به) | سكربتات تمهيد البيئة |
| PostgreSQL | نعم (الوضع المفضل) | التخزين الأساسي عبر `DATABASE_URL` |
| `tmux` | مفضل | جلسات backend/PWA و self-dev المُدارة |
| `codex` CLI | اختياري | تحليل مدعوم بواسطة LLM وتلقائية README/self-dev |

## 🧩 التوافق والافتراضات

| الموضوع | التوقع الحالي |
| --- | --- |
| نظام التشغيل المحلي | Linux/macOS عبر أدوات `bash` هو الهدف الأساسي |
| وقت تشغيل Python | `3.11` (مدار عبر `scripts/setup_autoappdev_env.sh`) |
| وضع التخزين | PostgreSQL مفضل ويُعتبر المرجع الأساسي |
| سلوك الرجوع | `backend/storage.py` يحتوي على احتياطي JSON للتوافق في السيناريوهات المتدهورة |
| نموذج الشبكة | تطوير محلي منفصل المنافذ (backend + PWA ثابت) |
| أدوات الوكيل | `codex` CLI اختياري إلا عند استخدام parse-llm أو أتمتة self-dev |

الافتراضات المستخدمة في هذا الـ README:
- تُشغّل الأوامر من جذر المستودع ما لم تُذكر خلاف ذلك في قسم معيّن.
- يُفترض إعداد `.env` قبل بدء تشغيل خدمات الباك إند.
- `conda` و`tmux` متاحان لمسارات العمل الموصى بها.

## 🛠️ التثبيت
### 1) استنساخ المستودع والدخول إليه
```bash
git clone git@github.com:lachlanchen/AutoAppDev.git
cd AutoAppDev
```

### 2) تهيئة البيئة
```bash
cp .env.example .env
```
عدّل `.env` وحدد على الأقل:
- `SECRET_KEY`
- `DATABASE_URL`
- `AUTOAPPDEV_HOST` و`AUTOAPPDEV_PORT` (أو `PORT`)

### 3) إنشاء/تحديث بيئة الخادم الخلفي
```bash
./scripts/setup_autoappdev_env.sh
```

### 4) تطبيق مخطط قاعدة البيانات
```bash
conda run -n autoappdev python -m backend.apply_schema
```

### 5) اختبار smoke اختياري لقاعدة البيانات
```bash
conda run -n autoappdev python -m backend.db_smoketest
```

## ⚡ البدء السريع
```bash
# من جذر المستودع
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

ثم افتح:
- PWA: `http://127.0.0.1:5173/`
- Base API للباك إند: `http://127.0.0.1:8788`
- فحص الصحة: `http://127.0.0.1:8788/api/health`

التحقق السريع باستخدام أمر واحد:
```bash
curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool
```

خريطة الواجهات السريعة:

| السطح | الرابط |
| --- | --- |
| واجهة PWA | `http://127.0.0.1:5173/` |
| API الباك إند | `http://127.0.0.1:8788` |
| نقطة الصحة | `http://127.0.0.1:8788/api/health` |

## ⚙️ الإعدادات
الملف الأساسي: `.env` (راجع `docs/env.md` و`.env.example`).

### المتغيرات المهمة

| المتغير | الغرض |
| --- | --- |
| `SECRET_KEY` | مطلوب كاتفاقية |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | إعدادات ربط الباك إند |
| `DATABASE_URL` | DSN الخاص بـ PostgreSQL (مفضل) |
| `AUTOAPPDEV_RUNTIME_DIR` | تجاوز مجلد التشغيل (افتراضي `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | هدف تشغيل الخطّ الافتراضي |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | تفعيل `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | افتراضيات Codex للنقاط ونقاط النهاية |
| `AI_API_BASE_URL`, `AI_API_KEY` | محجوز للتكاملات المستقبلية |

تحقق سريع من `.env`:
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
| تشغيل backend + PWA (موصى به) | `./scripts/run_autoappdev_tmux.sh --restart` | الباك إند `http://127.0.0.1:8788`، PWA `http://127.0.0.1:5173/` |
| تشغيل الباك إند فقط | `conda run -n autoappdev python -m backend.app` | يستخدم إعدادات الربط في `.env` و إعدادات DB |
| تشغيل خادم PWA ثابت فقط | `cd pwa && python3 -m http.server 5173 --bind 127.0.0.1` | مفيد لفحص الواجهة الأمامية فقط |
| تشغيل self-dev في tmux | `./scripts/run_autoappdev_selfdev_tmux.sh --restart` | حلقة self-development قابلة للاستئناف |

### خيارات السكربت الشائعة
- `./scripts/run_autoappdev_tmux.sh --help`
- `./scripts/run_autoappdev_tmux.sh --backend-port 8790 --pwa-port 5174`
- `./scripts/run_autoappdev_tmux.sh --detached`
- `./scripts/run_autoappdev_selfdev_tmux.sh --help`
- `./scripts/run_autoappdev_selfdev_tmux.sh --start-at 14 --reasoning xhigh`

### تحليل وتخزين السكربتات
- تحليل AAPS عبر API: `POST /api/scripts/parse`
- استيراد shell موثّق: `POST /api/scripts/import-shell`
- تحليل LLM اختياري: `POST /api/scripts/parse-llm` (يتطلب `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### واجهات التحكم في الخطّ
- `GET /api/pipeline`
- `GET /api/pipeline/status`
- `POST /api/pipeline/start`
- `POST /api/pipeline/pause`
- `POST /api/pipeline/resume`
- `POST /api/pipeline/stop`

### واجهات API شائعة الاستخدام الأخرى
- Health/version/config: `/api/health`, `/api/version`, `/api/config`
- Plan/scripts: `/api/plan`, `/api/scripts`, `/api/scripts/<id>`
- الإجراءات: `/api/actions`, `/api/actions/<id>`, `/api/actions/<id>/clone`, `/api/actions/update-readme`
- المراسلة: `/api/chat`, `/api/inbox`, `/api/outbox`
- السجلات: `/api/logs`, `/api/logs/tail`

راجع `docs/api-contracts.md` لفحصات شكل الطلبات/الاستجابات.

## 🧭 أدلة التشغيل

### دليل تشغيل كامل للدكد المحلي
```bash
cp .env.example .env
./scripts/setup_autoappdev_env.sh
conda run -n autoappdev python -m backend.apply_schema
./scripts/run_autoappdev_tmux.sh --restart
```

نقاط تحقق التحقق:
- `curl -sS http://127.0.0.1:8788/api/health | python3 -m json.tool`
- افتح `http://127.0.0.1:5173/` وتحقق من تحميل الواجهة لـ `/api/config`.
- اختياريًا: افتح `/api/version` وتحقق من إرجاع بيانات تعريف backend المتوقعة.

### دليل استكشاف أخطاء backend
```bash
conda run -n autoappdev python -m backend.app
curl -sS http://127.0.0.1:8788/api/version
curl -sS http://127.0.0.1:8788/api/pipeline/status | python3 -m json.tool
```

### دليل codegen حتمي للتحقق السريع
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

## 📡 لقطة API

المجموعات الأساسية للـ API من النظرة السريعة:

| الفئة | نقاط النهاية |
| --- | --- |
| الصحة + معلومات التشغيل | `GET /api/health`, `GET /api/version`, `GET /api/config`, `POST /api/config` |
| نموذج الخطة | `GET /api/plan`, `POST /api/plan` |
| السكربتات | `GET/POST /api/scripts`, `GET/PUT/DELETE /api/scripts/<id>`, `POST /api/scripts/parse`, `POST /api/scripts/import-shell`, `POST /api/scripts/parse-llm` |
| سجل الإجراءات | `GET/POST /api/actions`, `GET/PUT/DELETE /api/actions/<id>`, `POST /api/actions/<id>/clone`, `POST /api/actions/update-readme` |
| تشغيل الخط | `GET /api/pipeline`, `GET /api/pipeline/status`, `POST /api/pipeline/start`, `POST /api/pipeline/pause`, `POST /api/pipeline/resume`, `POST /api/pipeline/stop` |
| الرسائل + السجلات | `GET/POST /api/chat`, `GET/POST /api/inbox`, `GET/POST /api/outbox`, `GET/POST /api/logs`, `GET/POST /api/logs/tail` |
| إعدادات المساحة | `GET/POST /api/workspaces/<name>/config` |

## 🧪 الأمثلة
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

### خطّ ديمو حتمي
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
ثم استخدم تحكمات PWA Start/Pause/Resume/Stop وفحص `/api/logs`.

### الاستيراد من shell موثق
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
- الباك إند مبني على Tornado ومصمم لراحة التطوير المحلي (بما في ذلك CORS متساهل لمنفذ localhost المنفصل).
- التخزين PostgreSQL-أساسًا مع سلوك توافق في `backend/storage.py`.
- مفاتيح الواجهة الأمامية وقيم `STEP.block` في السكربتات مصممة للتطابق عمدا (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- الإجراءات المدمجة للقراءة فقط؛ قم بـ clone قبل التعديل.
- إجراء `update_readme` مقيد أمنيًا لمسارات README في workspace ضمن `auto-apps/<workspace>/README.md`.
- توجد مراجع تاريخية/أسماء في بعض الوثائق والسكربتات (`HeyCyan`, `LightMind`) موروثة من تطور المشروع. المسار الكنسي في المستودع الحالي هو جذر هذا المستودع.
- دليل `i18n/` الجذري موجود. تتوقع ملفات README متعددة اللغات في هذا المجلد خلال عمليات التوليد.

### نموذج العمل وملفات الحالة
- التشغيل الافتراضي في `./runtime` ما لم تُستبدل عبر `AUTOAPPDEV_RUNTIME_DIR`.
- تتبع حالة تاريخ self-dev في `references/selfdev/`.
- تُسجل مخرجات سير عمل README في `.auto-readme-work/<timestamp>/`.

### وضع الاختبار (الحالي)
- المستودع يشتمل على smoke checks وسكربتات demo Deterministic.
- لا يوجد حتى الآن تعريف كامل لاختبارات أتمتة/CI في تعريفات الميتا للمستودع.
- الافتراض: التحقق يعتمد أساسًا على سكربتات تشغيل محددة (`scripts/pipeline_codegen/smoke_*.sh`, `backend.db_smoketest`, checklist end-to-end).

## 🔐 ملاحظات الأمان
- إجراء `update_readme` مقيد بشكل متعمد لمسارات workspace README (`auto-apps/<workspace>/README.md`) مع حماية traversal.
- تحقق سجل الإجراءات يفرض حقول spec الموحدة والقيم الحدودية لمستويات reasoning المدعومة.
- سكربتات المستودع تفترض تشغيلًا موثوقًا محليًا؛ راجع محتويات السكربت قبل التشغيل في بيئات مشتركة أو قريبة من الإنتاج.
- قد يحتوي `.env` على قيم حساسة (`DATABASE_URL`, مفاتيح API). لا تقم بإضافة `.env` إلى git واستخدم إدارة أسرار مناسبة لكل بيئة.

## 🔧 استكشاف الأخطاء

| العرض | ما يجب فحصه |
| --- | --- |
| `tmux not found` | ثبّت `tmux` أو شغّل الباك إند وPWA يدويًا. |
| فشل الباك إند عند البدء بسبب env مفقود | أعد فحص `.env` مقابل `.env.example` و`docs/env.md`. |
| أخطاء قاعدة البيانات (اتصال/مصادقة/مخطط) | تحقق من `DATABASE_URL`; أعد تشغيل `conda run -n autoappdev python -m backend.apply_schema`; تحقق اختياري: `conda run -n autoappdev python -m backend.db_smoketest`. |
| PWA يحمّل لكن لا يستطيع استدعاء API | تأكد من backend يستمع على المضيف/المنفذ المتوقع؛ أعد إنشاء `pwa/config.local.js` عبر إعادة تشغيل `./scripts/run_autoappdev_tmux.sh`. |
| Start الخاص بالخطّ يرجع انتقالًا غير صالح | افحص حالة pipeline الحالية أولًا؛ ابدأ من حالة `stopped`. |
| لا توجد تحديثات سجل في الواجهة | تأكد من كتابة `runtime/logs/pipeline.log`; استخدم `/api/logs` و`/api/logs/tail` مباشرة لعزل مشاكل الواجهة vs الخلفية. |
| نقطة نهاية LLM parse معطلة | فعل `AUTOAPPDEV_ENABLE_LLM_PARSE=1` وأعد تشغيل الباك إند. |
| فشل `conda run -n autoappdev ...` | أعد تشغيل `./scripts/setup_autoappdev_env.sh`; تأكد من وجود بيئة conda باسم `autoappdev` (`conda env list`). |
| هدف API خاطئ في الواجهة الأمامية | تأكد من وجود `pwa/config.local.js` ويشير إلى backend host/port الفعّال. |

للتحقق اليدوي الحتمي، استخدم `docs/end-to-end-demo-checklist.md`.

## 🌐 سير عمل README & i18n
- README الجذري هو المصدر المرجعي المستخدم في خط أتمتة README.
- النسخ متعددة اللغات متوقعة داخل `i18n/`.
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
- رابط التنقل اللغوي يجب أن يبقى كسطر واحد في أعلى كل نسخة من README (بدون تكرار أشرطة اللغات).
- مدخل خط أنابيب README: `prompt_tools/auto-readme-pipeline.sh`.

### قيود توليد i18n (صارم)
- يجب دائمًا معالجة التوليد متعدد اللغات عند تحديث محتوى README الأساسي.
- توليد/تحديث الملفات اللغوية واحدًا تلو الآخر (تسلسليًا)، لا بالتجميع غير الواضح.
- احتفظ بسطر تنقل لغات واحد فقط في أعلى كل نسخة.
- لا تكرر أشرطة اللغات داخل نفس الملف.
- حافظ على أوامر أوامر shell و روابط API ومسارات الملفات وبنية الملصقات عبر الترجمات.

ترتيب التوليد المقترح:
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

## 📘 سياق توليد Readme

- طابع زمني لتشغيل الخط: `20260301_064935`
- المحفز: `./README.md` أول توليد مسودة كاملة
- طلب المستخدم المدخل: `probe prompt`
- الهدف: توليد مسودة README كاملة وجذابة مع الأقسام المطلوبة ومعلومات الدعم
- لقطة المصدر المستخدمة:
  - `./.auto-readme-work/20260301_064935/pipeline-context.md`
  - `./.auto-readme-work/20260301_064935/repo-structure-analysis.md`
- تم توليد هذا الملف من محتويات المستودع كمُدخل مرجعي لبداية المسودة الاساسية.

## ❓ الأسئلة الشائعة

### هل PostgreSQL إلزامي؟
مفضل ومُتوقع للاستخدام العادي. طبقة التخزين تحتوي سلوك fallback للتوافق، لكن الاستخدام شبه الإنتاجي ينبغي أن يفترض توفر PostgreSQL عبر `DATABASE_URL`.

### لماذا كلٌ من `AUTOAPPDEV_PORT` و`PORT`؟
`AUTOAPPDEV_PORT` خاص بالمشروع. `PORT` موجود كاسم مستعار مناسب للنشر. أبقهما متطابقين إلا إذا أردت تغيير السلوك متعمدًا في مسار الإطلاق.

### من أين أبدأ إذا أردت فقط فحص APIs؟
شغّل backend فقط (`conda run -n autoappdev python -m backend.app`) واستخدم `/api/health`, `/api/version`, `/api/config`, ثم نقاط endpoint الخاصة بالسكربت/الإجراءات المذكورة في `docs/api-contracts.md`.

### هل README متعددة اللغات تُولد تلقائيًا؟
نعم. يشمل المستودع `prompt_tools/auto-readme-pipeline.sh`، وتُدار نسخ اللغات في `i18n/` مع سطر لغة واحد في أعلى كل نسخة.

## 🗺️ خارطة الطريق
- استكمال المهام المتبقية من حالة self-dev الحالية (`51 / 55`).
- توسيع أدوات workspace/materials/context وعقود المسار الآمنة.
- متابعة تحسين تجربة لوحة الإجراءات وقابلية تعديل سير العمل.
- تعميق دعم README/i18n وواجهة تبديل اللغة أثناء التشغيل.
- تعزيز فحوص smoke/integration وتقوية تغطية CI (يوجد حالياً فحوص smoke مدفوعة؛ لا توجد وثيقة CI شاملة مثبتة في الجذر).
- مواصلة تدعيم حتمية parser/import/codegen حول AAPS v1 وcanonical IR.

## 🤝 المساهمة
المساهمات مرحب بها عبر issues و pull requests.

سير العمل المقترح:
1. انشئ fork وأنشئ فرع ميزة.
2. أبقِ التغييرات مركزة وقابلة لإعادة الإنتاج.
3. فضل استخدام السكربتات/الاختبارات الحتمية كلما أمكن.
4. حدّث التوثيق عندما تتغير السلوكيات/العقود (`docs/*`, عقود API، أمثلة).
5. افتح PR مع سياق وخطوات تحقق وأية افتراضات تشغيلية.

تحتوي remotes الحالية على:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- قد تكون remotes إضافية موجودة في نسخ محلية مرتبطة لمستودعات ذات صلة (مثال موجود في هذه البيئة: `novel`).

---

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## 📄 License
![License](https://img.shields.io/badge/License-Not%20Detected-C53030?logo=law&logoColor=white)

لم يتم اكتشاف ملف `LICENSE` في لقطة هذا المستودع.

ملاحظة افتراض:
- حتى تتم إضافة ملف ترخيص، عُدّ شروط الاستخدام وإعادة التوزيع غير محددة وتأكد منها مع maintainer.
