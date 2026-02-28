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

سكريبتات وإرشادات قابلة لإعادة الاستخدام لبناء التطبيقات خطوة بخطوة انطلاقًا من لقطات الشاشة/Markdown باستخدام Codex كأداة غير تفاعلية.

<!-- AUTOAPPDEV:STATUS:BEGIN -->
## حالة التطوير الذاتي (تحديث تلقائي)

- آخر تحديث: 2026-02-16T00:27:20Z
- Phase commit: `Selfdev: 52 pwa_action_palette_dynamic_and_editable_blocks summary`
- التقدم: 51 / 55 مهمة مكتملة
- Codex session: `019c6056-f33a-7f31-b08f-0ca40c365351`
- الفلسفة: Plan -> Work -> Verify -> Summary -> Commit/Push (خطية وقابلة للاستئناف)

يتم تحديث هذا القسم بواسطة `scripts/auto-autoappdev-development.sh`.
لا تُعدّل المحتوى بين العلامات.

<!-- AUTOAPPDEV:STATUS:END -->

## 🚀 نظرة عامة
AutoAppDev مشروع تحكّم لخطوط تطوير التطبيقات طويلة التشغيل والقابلة للاستئناف. ويجمع بين:

1. واجهة API خلفية مبنية على Tornado مع استمرارية بيانات مدعومة بـ PostgreSQL (مع سلوك احتياطي محلي عبر JSON داخل كود التخزين).
2. واجهة تحكّم PWA ثابتة شبيهة بـ Scratch.
3. سكريبتات ووثائق لتأليف خطوط العمل، وتوليد الكود الحتمي، وحلقات التطوير الذاتي، وأتمتة README.

### لمحة سريعة

| المجال | التفاصيل |
| --- | --- |
| بيئة التشغيل الأساسية | Tornado backend + static PWA frontend |
| الاستمرارية | PostgreSQL أولًا مع سلوك توافق في `backend/storage.py` |
| نموذج خط العمل | Canonical IR (`autoappdev_ir` v1) وصيغة سكريبتات AAPS |
| تدفّق التحكّم | دورة الحياة Start / Pause / Resume / Stop |
| وضع التطوير | حلقة تطوير ذاتي قابلة للاستئناف + مسارات script/codegen حتمية |
| README/i18n | مسار README مؤتمت مع هيكل `i18n/` |

## 🧭 الفلسفة
يتعامل AutoAppDev مع الوكلاء كأدوات ويحافظ على استقرار العمل عبر حلقة صارمة قابلة للاستئناف:
1. Plan
2. Implement
3. Debug/verify (with timeouts)
4. Fix
5. Summarize + log
6. Commit + push

يهدف تطبيق التحكّم إلى تجسيد المفاهيم نفسها في صورة blocks/actions شبيهة بـ Scratch (بما في ذلك الإجراء المشترك `update_readme`) بحيث تبقى كل مساحة عمل محدّثة وقابلة لإعادة الإنتاج.

## ✨ الميزات
- تحكّم قابل للاستئناف في دورة حياة خط العمل: start, pause, resume, stop.
- واجهات API لمكتبة السكريبتات لسكريبتات خط العمل AAPS (`.aaps`) وCanonical IR (`autoappdev_ir` v1).
- مسار parser/import حتمي:
  - Parse formatted AAPS scripts.
  - Import annotated shell via `# AAPS:` comments.
  - Optional Codex-assisted parse fallback (`AUTOAPPDEV_ENABLE_LLM_PARSE=1`).
- سجل إجراءات (Action registry) يتضمن إجراءات مدمجة + إجراءات قابلة للتعديل/مخصّصة (مع تدفّق clone/edit للإجراءات readonly).
- كتل PWA شبيهة بـ Scratch ولوحة إجراءات محمّلة وقت التشغيل (`GET /api/actions`).
- قنوات مراسلة وقت التشغيل:
  - Inbox (`/api/inbox`) لإرشادات المشغّل -> خط العمل.
  - Outbox (`/api/outbox`) بما في ذلك ingestion لطابور الملفات من `runtime/outbox`.
- بث تدريجي للسجلات من سجلات backend وخط العمل (`/api/logs`, `/api/logs/tail`).
- توليد runner حتمي من Canonical IR (`scripts/pipeline_codegen/generate_runner_from_ir.py`).
- مشغّل تطوير ذاتي للتطوير التكراري للمستودع (`scripts/auto-autoappdev-development.sh`).
- مسار أتمتة README مع هيكل توليد متعدد اللغات تحت `i18n/`.

## 📚 المحتويات
- `docs/auto-development-guide.md`: فلسفة ومتطلبات ثنائية اللغة (EN/ZH) لوكيل تطوير تلقائي طويل التشغيل وقابل للاستئناف.
- `docs/ORDERING_RATIONALE.md`: مثال على مبررات ترتيب الخطوات المعتمدة على لقطات الشاشة.
- `docs/controller-mvp-scope.md`: نطاق Controller MVP (الشاشات + الحد الأدنى من APIs).
- `docs/end-to-end-demo-checklist.md`: قائمة تحقق عرض توضيحي يدوي end-to-end حتمي (backend + PWA happy path).
- `docs/env.md`: اصطلاحات متغيرات البيئة (.env).
- `docs/api-contracts.md`: عقود الطلب/الاستجابة لواجهة API الخاصة بالمتحكّم.
- `docs/pipeline-formatted-script-spec.md`: صيغة سكريبتات خط العمل القياسية (AAPS) ومخطط Canonical IR (TASK -> STEP -> ACTION).
- `docs/pipeline-runner-codegen.md`: مولّد حتمي لإنتاج pipeline runners قابلة للتنفيذ بـ bash من Canonical IR.
- `docs/common-actions.md`: عقود/مواصفات الإجراءات المشتركة (يتضمن `update_readme`).
- `docs/workspace-layout.md`: مجلدات مساحة العمل القياسية + العقود (materials/interactions/outputs/docs/references/scripts/tools/logs/auto-apps).
- `scripts/run_autoappdev_tmux.sh`: تشغيل تطبيق AutoAppDev (backend + PWA) داخل tmux.
- `scripts/run_autoappdev_selfdev_tmux.sh`: تشغيل مشغّل AutoAppDev للتطوير الذاتي داخل tmux.
- `scripts/app-auto-development.sh`: مشغّل خط العمل الخطي (plan -> backend -> PWA -> Android -> iOS -> review -> summary) مع دعم الاستئناف/الحالة.
- `scripts/generate_screenshot_docs.sh`: مولّد وصف markdown من لقطات الشاشة (مدفوع بـ Codex).
- `scripts/setup_backend_env.sh`: تهيئة بيئة conda للـ backend للتشغيل المحلي.
- `examples/ralph-wiggum-example.sh`: مساعد أتمتة Codex CLI كمثال.

## 🗂️ هيكل المشروع
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

## ✅ المتطلبات المسبقة
- نظام تشغيل يدعم `bash`.
- Python `3.11+`.
- Conda (`conda`) لسكريبتات الإعداد المتوفرة.
- `tmux` لجلسات backend+PWA أو التطوير الذاتي بأمر واحد.
- PostgreSQL يمكن الوصول إليه عبر `DATABASE_URL`.
- اختياري: واجهة `codex` CLI لمسارات العمل المعتمدة على Codex (التطوير الذاتي، parse-llm fallback، auto-readme pipeline).

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
حرّر ملف `.env` واضبط على الأقل:
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

## ⚙️ الإعداد
الملف الأساسي: `.env` (راجع `docs/env.md` و`.env.example`).

### المتغيرات المهمة

| المتغير | الغرض |
| --- | --- |
| `SECRET_KEY` | مطلوب حسب الاصطلاح |
| `AUTOAPPDEV_HOST`, `AUTOAPPDEV_PORT`, `PORT` | إعدادات ربط backend |
| `DATABASE_URL` | PostgreSQL DSN (مفضّل) |
| `AUTOAPPDEV_RUNTIME_DIR` | تجاوز مسار runtime (الافتراضي `./runtime`) |
| `AUTOAPPDEV_PIPELINE_CWD`, `AUTOAPPDEV_PIPELINE_SCRIPT` | هدف تشغيل خط العمل الافتراضي |
| `AUTOAPPDEV_ENABLE_LLM_PARSE=1` | تفعيل `/api/scripts/parse-llm` |
| `AUTOAPPDEV_CODEX_MODEL`, `AUTOAPPDEV_CODEX_REASONING`, `AUTOAPPDEV_CODEX_SKIP_GIT_CHECK` | إعدادات Codex الافتراضية للإجراءات/النهايات |
| `AI_API_BASE_URL`, `AI_API_KEY` | محجوز للتكاملات المستقبلية |

تحقّق سريعًا من `.env`:
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
### تشغيل backend + PWA معًا (موصى به)
```bash
./scripts/run_autoappdev_tmux.sh --restart
```
القيم الافتراضية:
- Backend: `http://127.0.0.1:8788`
- PWA: `http://127.0.0.1:5173/`

### تشغيل backend فقط
```bash
conda run -n autoappdev python -m backend.app
```

### تشغيل خادم PWA ثابت فقط
```bash
cd pwa
python3 -m http.server 5173 --bind 127.0.0.1
```

### تشغيل مشغّل التطوير الذاتي داخل tmux
```bash
./scripts/run_autoappdev_selfdev_tmux.sh --restart
```

### تحليل السكريبتات وتخزينها
- تحليل AAPS عبر API: `POST /api/scripts/parse`
- استيراد shell مُعلّق (annotated): `POST /api/scripts/import-shell`
- تحليل LLM اختياري: `POST /api/scripts/parse-llm` (يتطلب `AUTOAPPDEV_ENABLE_LLM_PARSE=1`)

### واجهات API للتحكم بخط العمل
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

راجع `docs/api-contracts.md` لصيغ الطلب/الاستجابة.

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

### خط عمل عرض توضيحي حتمي
```bash
export AUTOAPPDEV_PIPELINE_SCRIPT=scripts/pipeline_demo.sh
conda run -n autoappdev python -m backend.app
```
ثم استخدم عناصر التحكم Start/Pause/Resume/Stop في PWA وافحص `/api/logs`.

## 🧱 ملاحظات التطوير
- الـ backend مبني على Tornado ومصمّم لسهولة التطوير المحلي (بما في ذلك CORS متساهل لمنافذ localhost المنفصلة).
- التخزين PostgreSQL-first مع سلوك توافق في `backend/storage.py`.
- مفاتيح كتل PWA وقيم `STEP.block` في السكريبتات متوافقة عمدًا (`plan`, `work`, `debug`, `fix`, `summary`, `commit_push`).
- الإجراءات المدمجة readonly؛ استخدم clone قبل التعديل.
- إجراء `update_readme` مقيّد بأمان المسار ليستهدف README الخاص بمساحة العمل تحت `auto-apps/<workspace>/README.md`.
- توجد إشارات تاريخية للمسارات/الأسماء في بعض الوثائق/السكريبتات (`HeyCyan`, `LightMind`) موروثة من تطوّر المشروع. المسار المرجعي الحالي هو جذر هذا المستودع.
- مجلد الجذر `i18n/` موجود. وملفات README للغات متوقّعة داخله عند تشغيل المسارات متعددة اللغات.

## 🩺 استكشاف الأخطاء وإصلاحها
- `tmux not found`:
  - ثبّت `tmux` أو شغّل backend/PWA يدويًا.
- فشل backend عند الإقلاع بسبب متغيرات بيئة ناقصة:
  - أعد التحقق من `.env` مقابل `.env.example` و`docs/env.md`.
- أخطاء قاعدة البيانات (الاتصال/المصادقة/المخطط):
  - تحقّق من `DATABASE_URL`.
  - أعد تشغيل `conda run -n autoappdev python -m backend.apply_schema`.
  - فحص اتصال اختياري: `conda run -n autoappdev python -m backend.db_smoketest`.
- يتم تحميل PWA لكن لا يمكنه استدعاء API:
  - تأكد أن backend يعمل على المضيف/المنفذ المتوقع.
  - أعد توليد `pwa/config.local.js` عبر تشغيل `./scripts/run_autoappdev_tmux.sh` مرة أخرى.
- يرجع Pipeline Start انتقالًا غير صالح:
  - افحص حالة خط العمل الحالية أولًا؛ ابدأ من حالة `stopped`.
- لا تظهر تحديثات السجل في الواجهة:
  - أكد أن `runtime/logs/pipeline.log` تتم الكتابة إليه.
  - استخدم `/api/logs` و`/api/logs/tail` مباشرةً لعزل المشكلة بين UI وbackend.
- ترجع نهاية parse الخاصة بـ LLM أنها معطلة:
  - اضبط `AUTOAPPDEV_ENABLE_LLM_PARSE=1` وأعد تشغيل backend.

لمسار تحقق يدوي حتمي، استخدم `docs/end-to-end-demo-checklist.md`.

## 🗺️ خارطة الطريق
- إكمال مهام التطوير الذاتي المتبقية بعد الحالة الحالية `51 / 55`.
- توسيع أدوات workspace/materials/context وتعزيز عقود safe-path.
- مواصلة تحسين تجربة لوحة الإجراءات وسير عمل الإجراءات القابلة للتحرير.
- تعميق دعم README/UI متعدد اللغات عبر `i18n/` وتبديل اللغة وقت التشغيل.
- تعزيز فحوصات smoke/integration وتغطية CI (توجد حاليًا فحوصات smoke مدفوعة بالسكريبتات؛ ولا يوجد توصيف CI كامل موثّق في الجذر).

## 🤝 المساهمة
المساهمات مرحّب بها عبر Issues وPull Requests.

مسار عمل مقترح:
1. قم بعمل Fork وأنشئ فرع ميزة.
2. اجعل التغييرات مركّزة وقابلة لإعادة الإنتاج.
3. فضّل السكريبتات/الاختبارات الحتمية متى أمكن.
4. حدّث الوثائق عند تغيّر السلوك/العقود (`docs/*`, API contracts, examples).
5. افتح PR يتضمن السياق، وخطوات التحقق، وأي افتراضات تشغيل.

تتضمن الـ remotes الحالية للمستودع:
- `origin`: `git@github.com:lachlanchen/AutoAppDev.git`
- قد يوجد remote إضافي في النسخ المحلية لمستودعات ذات صلة.

## 📄 الترخيص
لم يتم اكتشاف ملف `LICENSE` في جذر هذا الالتقاط من المستودع.

ملاحظة افتراضية:
- إلى أن تتم إضافة ملف ترخيص، اعتبر شروط الاستخدام/إعادة التوزيع غير محددة وتأكد منها مع maintainer.

## ❤️ الرعاية والتبرع

- GitHub Sponsors: https://github.com/sponsors/lachlanchen
- Donate: https://chat.lazying.art/donate
- PayPal: https://paypal.me/RongzhouChen
- Stripe: https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400
