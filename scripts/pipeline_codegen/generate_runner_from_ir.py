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


def _generate_body(ir: dict[str, Any]) -> str:
    kind = ir.get("kind")
    ver = ir.get("version")
    if kind != "autoappdev_ir" or ver != 1:
        _die('expected top-level {"kind":"autoappdev_ir","version":1,...}')

    tasks = _as_list(ir.get("tasks"), "ir.tasks")

    lines: list[str] = []
    lines.append("# Generated pipeline body (autoappdev_ir v1)")

    for t_i, t_any in enumerate(tasks):
        t = _as_dict(t_any, f"tasks[{t_i}]")
        t_id = _req_str(t, "id", f"tasks[{t_i}]")
        t_title = _req_str(t, "title", f"tasks[{t_i}]")

        lines.append("")
        lines.append(f"# TASK {t_id}: {_comment_safe(t_title)}")
        lines.append(f"log {_bash_sq(f'TASK {t_id}: {t_title}')}")

        steps = _as_list(t.get("steps"), f"tasks[{t_i}].steps")
        for s_i, s_any in enumerate(steps):
            s = _as_dict(s_any, f"tasks[{t_i}].steps[{s_i}]")
            s_id = _req_str(s, "id", f"tasks[{t_i}].steps[{s_i}]")
            s_title = _req_str(s, "title", f"tasks[{t_i}].steps[{s_i}]")
            s_block = _req_str(s, "block", f"tasks[{t_i}].steps[{s_i}]")

            lines.append(f"# STEP {s_id} ({s_block}): {_comment_safe(s_title)}")
            lines.append(f"log {_bash_sq(f'STEP {s_id} ({s_block}): {s_title}')}")

            actions = _as_list(s.get("actions"), f"tasks[{t_i}].steps[{s_i}].actions")
            for a_i, a_any in enumerate(actions):
                a = _as_dict(a_any, f"tasks[{t_i}].steps[{s_i}].actions[{a_i}]")
                a_id = _req_str(a, "id", f"tasks[{t_i}].steps[{s_i}].actions[{a_i}]")
                a_kind = _req_str(a, "kind", f"tasks[{t_i}].steps[{s_i}].actions[{a_i}]")

                lines.append(f"# ACTION {a_id}: kind={_comment_safe(a_kind)}")

                params = a.get("params") or {}
                if not isinstance(params, dict):
                    _die(f"invalid params for action {t_id}/{s_id}/{a_id} (expected object)")

                if a_kind == "note":
                    text = params.get("text")
                    if not isinstance(text, str):
                        _die(f"missing/invalid params.text for note action {t_id}/{s_id}/{a_id}")
                    lines.append(f"action_note {_bash_sq(text)}")
                elif a_kind == "run":
                    cmd = params.get("cmd")
                    if not isinstance(cmd, str):
                        _die(f"missing/invalid params.cmd for run action {t_id}/{s_id}/{a_id}")
                    lines.append(f"action_run {_bash_sq(cmd)}")
                elif a_kind == "codex_exec":
                    prompt = params.get("prompt")
                    if not isinstance(prompt, str):
                        _die(f"missing/invalid params.prompt for codex_exec action {t_id}/{s_id}/{a_id}")

                    model = _opt_str(params, "model", f"action {t_id}/{s_id}/{a_id} params")
                    reasoning = _opt_str(params, "reasoning", f"action {t_id}/{s_id}/{a_id} params")

                    parts = [f"action_codex_exec {_bash_sq(prompt)}"]
                    if model is not None:
                        parts.append(_bash_sq(model))
                    if reasoning is not None:
                        if model is None:
                            # Keep positional args stable: model then reasoning.
                            parts.append(_bash_sq(""))
                        parts.append(_bash_sq(reasoning))
                    lines.append(" ".join(parts))
                else:
                    _die(f"unsupported action kind {a_kind!r} for action {t_id}/{s_id}/{a_id}")

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

