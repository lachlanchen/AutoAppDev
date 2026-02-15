#!/usr/bin/env python3
"""
Deterministically generate a runnable bash pipeline runner from autoappdev_ir v1.

Usage:
  python3 scripts/pipeline_codegen/generate_runner_from_ir.py --in examples/pipeline_ir_v1.json --out /tmp/runner.sh
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PLACEHOLDER = "__PIPELINE_BODY__"


def _die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(2)


def _bash_sq(s: str) -> str:
    # Single-quote strategy: close/open around embedded single quotes.
    # Example: abc'def -> 'abc'"'"'def'
    return "'" + s.replace("'", "'\"'\"'") + "'"


def _comment_safe(s: str) -> str:
    return " ".join(s.replace("\r", " ").replace("\n", " ").split())


def _as_dict(x: Any, ctx: str) -> dict[str, Any]:
    if not isinstance(x, dict):
        _die(f"expected object for {ctx}")
    return x


def _as_list(x: Any, ctx: str) -> list[Any]:
    if not isinstance(x, list):
        _die(f"expected array for {ctx}")
    return x


def _req_str(obj: dict[str, Any], key: str, ctx: str) -> str:
    v = obj.get(key)
    if not isinstance(v, str) or not v:
        _die(f"missing/invalid {ctx}.{key} (expected non-empty string)")
    return v


def _opt_str(obj: dict[str, Any], key: str, ctx: str) -> str | None:
    v = obj.get(key)
    if v is None:
        return None
    if not isinstance(v, str) or not v:
        _die(f"invalid {ctx}.{key} (expected non-empty string)")
    return v


def _req_obj(obj: dict[str, Any], key: str, ctx: str) -> dict[str, Any]:
    v = obj.get(key)
    if v is None:
        _die(f"missing {ctx}.{key} (expected object)")
    if not isinstance(v, dict):
        _die(f"invalid {ctx}.{key} (expected object)")
    return v


def _opt_obj(obj: dict[str, Any], key: str, ctx: str) -> dict[str, Any] | None:
    v = obj.get(key)
    if v is None:
        return None
    if not isinstance(v, dict):
        _die(f"invalid {ctx}.{key} (expected object)")
    return v


def _opt_meta_obj(obj: dict[str, Any], ctx: str) -> dict[str, Any]:
    v = obj.get("meta")
    if v is None:
        return {}
    if not isinstance(v, dict):
        _die(f"invalid {ctx}.meta (expected object)")
    return v


def _emit_steps(
    *,
    lines: list[str],
    steps_any: list[Any],
    ctx_steps: str,
    t_id_for_errors: str,
    base_indent: str,
) -> None:
    for s_i, s_any in enumerate(steps_any):
        s = _as_dict(s_any, f"{ctx_steps}[{s_i}]")
        s_id = _req_str(s, "id", f"{ctx_steps}[{s_i}]")
        s_title = _req_str(s, "title", f"{ctx_steps}[{s_i}]")
        s_block = _req_str(s, "block", f"{ctx_steps}[{s_i}]")

        lines.append(f"{base_indent}# STEP {s_id} ({s_block}): {_comment_safe(s_title)}")
        lines.append(f"{base_indent}export AUTOAPPDEV_CTX_STEP_ID={_bash_sq(s_id)}")
        lines.append(f"{base_indent}export AUTOAPPDEV_CTX_STEP_TITLE={_bash_sq(s_title)}")
        lines.append(f"{base_indent}export AUTOAPPDEV_CTX_STEP_BLOCK={_bash_sq(s_block)}")
        lines.append(f"{base_indent}log {_bash_sq(f'STEP {s_id} ({s_block}): {s_title}')}")

        s_meta = _opt_meta_obj(s, f"{ctx_steps}[{s_i}]")
        s_cond_any = s_meta.get("conditional")
        if s_cond_any is None:
            s_cond = ""
        elif isinstance(s_cond_any, str):
            s_cond = s_cond_any
        else:
            _die(f"invalid {ctx_steps}[{s_i}].meta.conditional (expected string)")

        if s_cond:
            lines.append(f"{base_indent}if step_should_run {_bash_sq(s_cond)}; then")

        actions = _as_list(s.get("actions"), f"{ctx_steps}[{s_i}].actions")

        in_debug = s_block == "debug"
        if in_debug:
            lines.append(f"{base_indent}{'  ' if s_cond else ''}step_failed=0")

        for a_i, a_any in enumerate(actions):
            a = _as_dict(a_any, f"{ctx_steps}[{s_i}].actions[{a_i}]")
            a_id = _req_str(a, "id", f"{ctx_steps}[{s_i}].actions[{a_i}]")
            a_kind = _req_str(a, "kind", f"{ctx_steps}[{s_i}].actions[{a_i}]")

            pfx = base_indent + ("  " if s_cond else "")
            lines.append(f"{pfx}# ACTION {a_id}: kind={_comment_safe(a_kind)}")
            lines.append(f"{pfx}export AUTOAPPDEV_CTX_ACTION_ID={_bash_sq(a_id)}")
            lines.append(f"{pfx}export AUTOAPPDEV_CTX_ACTION_KIND={_bash_sq(a_kind)}")

            params = a.get("params") or {}
            if not isinstance(params, dict):
                _die(f"invalid params for action {t_id_for_errors}/{s_id}/{a_id} (expected object)")

            if a_kind == "note":
                text = params.get("text")
                if not isinstance(text, str):
                    _die(f"missing/invalid params.text for note action {t_id_for_errors}/{s_id}/{a_id}")
                lines.append(f"{pfx}action_note {_bash_sq(text)}")
            elif a_kind == "run":
                cmd = params.get("cmd")
                if not isinstance(cmd, str):
                    _die(f"missing/invalid params.cmd for run action {t_id_for_errors}/{s_id}/{a_id}")
                if in_debug:
                    lines.append(f"{pfx}if ! action_run {_bash_sq(cmd)}; then step_failed=1; fi")
                else:
                    lines.append(f"{pfx}action_run {_bash_sq(cmd)}")
            elif a_kind == "codex_exec":
                prompt = params.get("prompt")
                if not isinstance(prompt, str):
                    _die(f"missing/invalid params.prompt for codex_exec action {t_id_for_errors}/{s_id}/{a_id}")

                model = _opt_str(params, "model", f"action {t_id_for_errors}/{s_id}/{a_id} params")
                reasoning = _opt_str(params, "reasoning", f"action {t_id_for_errors}/{s_id}/{a_id} params")

                parts = [f"action_codex_exec {_bash_sq(prompt)}"]
                if model is not None:
                    parts.append(_bash_sq(model))
                if reasoning is not None:
                    if model is None:
                        # Keep positional args stable: model then reasoning.
                        parts.append(_bash_sq(""))
                    parts.append(_bash_sq(reasoning))

                if in_debug:
                    lines.append(f"{pfx}if ! {' '.join(parts)}; then step_failed=1; fi")
                else:
                    lines.append(f"{pfx}{' '.join(parts)}")
            else:
                _die(f"unsupported action kind {a_kind!r} for action {t_id_for_errors}/{s_id}/{a_id}")

        if in_debug:
            lines.append(f"{base_indent}{'  ' if s_cond else ''}AUTOAPPDEV_TASK_LAST_DEBUG_FAILED=\"$step_failed\"")

        if s_cond:
            lines.append(f"{base_indent}else")
            lines.append(
                f"{base_indent}  log {_bash_sq(f'SKIP STEP {s_id} ({s_block}): conditional={s_cond}')}"
            )
            lines.append(f"{base_indent}fi")


def _generate_body(ir: dict[str, Any]) -> str:
    kind = ir.get("kind")
    ver = ir.get("version")
    if kind != "autoappdev_ir" or ver != 1:
        _die('expected top-level {"kind":"autoappdev_ir","version":1,...}')

    tasks_any = _as_list(ir.get("tasks"), "ir.tasks")
    tasks: list[dict[str, Any]] = []

    controller_i: int | None = None
    controller_cfg: dict[str, Any] | None = None
    template_i: int | None = None

    for t_i, t_any in enumerate(tasks_any):
        t = _as_dict(t_any, f"tasks[{t_i}]")
        tasks.append(t)

        t_meta = _opt_meta_obj(t, f"tasks[{t_i}]")

        mr = t_meta.get("meta_round_v0")
        if mr is not None:
            if not isinstance(mr, dict):
                _die(f"invalid tasks[{t_i}].meta.meta_round_v0 (expected object)")
            if controller_i is not None:
                _die("multiple tasks define meta.meta_round_v0 (expected exactly one controller task)")
            controller_i = t_i
            controller_cfg = mr

        tt_present = "task_template_v0" in t_meta
        tt = t_meta.get("task_template_v0")
        if tt_present and tt is not None and tt is not False:
            if not isinstance(tt, (bool, dict)):
                _die(f"invalid tasks[{t_i}].meta.task_template_v0 (expected boolean or object)")
            if template_i is not None:
                _die("multiple tasks define meta.task_template_v0 (expected exactly one template task)")
            template_i = t_i

    lines: list[str] = []
    lines.append("# Generated pipeline body (autoappdev_ir v1)")

    in_meta_round = controller_i is not None or template_i is not None
    if in_meta_round:
        if controller_i is None or controller_cfg is None or template_i is None:
            _die("meta_round_v0 runner generation requires 1 controller task (meta.meta_round_v0) and 1 template task (meta.task_template_v0)")
        if controller_i == template_i:
            _die("meta_round_v0 runner generation requires distinct controller and template tasks")
        if len(tasks) != 2:
            _die("meta_round_v0 runner generation currently requires exactly 2 tasks: controller + template")

        task_list_path = controller_cfg.get("task_list_path")
        if not isinstance(task_list_path, str) or not task_list_path:
            _die("meta_round_v0 missing/invalid task_list_path (expected non-empty string)")

        controller = tasks[controller_i]
        template = tasks[template_i]

        c_id = _req_str(controller, "id", f"tasks[{controller_i}]")
        c_title = _req_str(controller, "title", f"tasks[{controller_i}]")
        c_meta = _opt_meta_obj(controller, f"tasks[{controller_i}]")
        c_acc_any = c_meta.get("acceptance")
        if c_acc_any is None:
            c_acc = ""
        elif isinstance(c_acc_any, str):
            c_acc = c_acc_any
        else:
            _die(f"invalid tasks[{controller_i}].meta.acceptance (expected string)")

        lines.append("")
        lines.append(f"# TASK {c_id}: {_comment_safe(c_title)}")
        lines.append(f"export AUTOAPPDEV_CTX_TASK_ID={_bash_sq(c_id)}")
        lines.append(f"export AUTOAPPDEV_CTX_TASK_TITLE={_bash_sq(c_title)}")
        lines.append(f"export AUTOAPPDEV_CTX_TASK_ACCEPTANCE={_bash_sq(c_acc)}")
        lines.append(f"log {_bash_sq(f'TASK {c_id}: {c_title}')}")
        lines.append("AUTOAPPDEV_TASK_LAST_DEBUG_FAILED=0")

        c_steps_any = _as_list(controller.get("steps"), f"tasks[{controller_i}].steps")
        _emit_steps(
            lines=lines,
            steps_any=c_steps_any,
            ctx_steps=f"tasks[{controller_i}].steps",
            t_id_for_errors=c_id,
            base_indent="",
        )

        t_steps_any = _as_list(template.get("steps"), f"tasks[{template_i}].steps")

        lines.append("")
        lines.append("# Template task function (task_template_v0)")
        lines.append("run_task_template_v0() {")
        lines.append('  local task_id="${1:-}"')
        lines.append('  local task_title="${2:-}"')
        lines.append('  local task_acceptance="${3:-}"')
        lines.append('  if [ -z "$task_id" ] || [ -z "$task_title" ]; then')
        lines.append('    echo "[runner] meta_round: invalid template task args" >&2')
        lines.append("    exit 2")
        lines.append("  fi")
        lines.append('  export AUTOAPPDEV_CTX_TASK_ID="$task_id"')
        lines.append('  export AUTOAPPDEV_CTX_TASK_TITLE="$task_title"')
        lines.append('  export AUTOAPPDEV_CTX_TASK_ACCEPTANCE="$task_acceptance"')
        lines.append('  log "TASK $task_id: $task_title"')
        lines.append("  AUTOAPPDEV_TASK_LAST_DEBUG_FAILED=0")

        _emit_steps(
            lines=lines,
            steps_any=t_steps_any,
            ctx_steps=f"tasks[{template_i}].steps",
            t_id_for_errors=_req_str(template, "id", f"tasks[{template_i}]"),
            base_indent="  ",
        )

        lines.append("}")
        lines.append("")
        lines.append(f"meta_round_run_template_tasks {_bash_sq(task_list_path)}")
    else:
        for t_i, t in enumerate(tasks):
            t_id = _req_str(t, "id", f"tasks[{t_i}]")
            t_title = _req_str(t, "title", f"tasks[{t_i}]")
            t_meta = _opt_meta_obj(t, f"tasks[{t_i}]")
            t_acceptance_any = t_meta.get("acceptance")
            if t_acceptance_any is None:
                t_acceptance = ""
            elif isinstance(t_acceptance_any, str):
                t_acceptance = t_acceptance_any
            else:
                _die(f"invalid tasks[{t_i}].meta.acceptance (expected string)")

            lines.append("")
            lines.append(f"# TASK {t_id}: {_comment_safe(t_title)}")
            lines.append(f"export AUTOAPPDEV_CTX_TASK_ID={_bash_sq(t_id)}")
            lines.append(f"export AUTOAPPDEV_CTX_TASK_TITLE={_bash_sq(t_title)}")
            lines.append(f"export AUTOAPPDEV_CTX_TASK_ACCEPTANCE={_bash_sq(t_acceptance)}")
            lines.append(f"log {_bash_sq(f'TASK {t_id}: {t_title}')}")
            lines.append("AUTOAPPDEV_TASK_LAST_DEBUG_FAILED=0")

            t_steps_any = _as_list(t.get("steps"), f"tasks[{t_i}].steps")
            _emit_steps(
                lines=lines,
                steps_any=t_steps_any,
                ctx_steps=f"tasks[{t_i}].steps",
                t_id_for_errors=t_id,
                base_indent="",
            )

    # Indent for inclusion inside the template's main() block.
    indented = []
    for ln in lines:
        indented.append(("  " + ln) if ln else "")
    return "\n".join(indented) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True, help="Input autoappdev_ir v1 JSON path")
    ap.add_argument("--out", dest="out_path", default="", help="Output runner .sh path (default: stdout)")
    ap.add_argument(
        "--template",
        dest="template_path",
        default=str(Path(__file__).resolve().parent / "templates" / "runner_v0.sh.tpl"),
        help="Runner template path",
    )
    args = ap.parse_args(argv)

    in_path = Path(args.in_path)
    template_path = Path(args.template_path)

    try:
        ir = json.loads(in_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _die(f"input not found: {in_path}")
    except json.JSONDecodeError as e:
        _die(f"invalid JSON in {in_path}: {e}")

    body = _generate_body(_as_dict(ir, "ir"))

    try:
        template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        _die(f"template not found: {template_path}")

    if PLACEHOLDER not in template:
        _die(f"template missing placeholder {PLACEHOLDER!r}: {template_path}")

    out = template.replace(PLACEHOLDER, body.rstrip("\n"))
    if not out.endswith("\n"):
        out += "\n"

    if args.out_path:
        Path(args.out_path).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
