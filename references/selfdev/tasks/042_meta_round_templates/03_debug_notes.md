# Debug Notes: 042 meta_round_templates

## Commands + Results
```bash
cd /home/lachlan/ProjectsLFS/HeyCyan/AutoAppDev

timeout 10s rg -n "Meta-round Templates \\(Convention v0\\)|docs/meta-round-templates\\.md" docs/pipeline-formatted-script-spec.md
timeout 10s rg -n "plan -> work -> debug -> fix -> translate -> summary -> log -> commit" docs/meta-round-templates.md
timeout 10s rg -n "/api/outbox|runtime/outbox" docs/meta-round-templates.md
timeout 10s rg -n "meta_round_v0" docs/meta-round-templates.md docs/pipeline-formatted-script-spec.md
```

Result (excerpt):
```text
docs/pipeline-formatted-script-spec.md:198:## 5) Meta-round Templates (Convention v0)
docs/pipeline-formatted-script-spec.md:208:- `docs/meta-round-templates.md` defines a standard `meta_round_v0` convention, including how to represent:
docs/meta-round-templates.md:6:  `plan -> work -> debug -> fix -> translate -> summary -> log -> commit`.
docs/meta-round-templates.md:108:  - `curl -sS -X POST http://127.0.0.1:8788/api/outbox -H 'content-type: application/json' -d '{"role":"pipeline","content":"..."}'`
docs/meta-round-templates.md:110:  - `printf '...\\n' > runtime/outbox/.tmp && mv runtime/outbox/.tmp runtime/outbox/$(date +%s%3N)_pipeline.md`
docs/meta-round-templates.md:113:Meta-round configuration is stored under `TASK.meta.meta_round_v0` (engine convention).
```

## Issues Found
- None (docs-only change; references and required template strings present).

