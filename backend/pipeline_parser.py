import json
from dataclasses import dataclass
from typing import Any


ALLOWED_BLOCKS = {"plan", "work", "debug", "fix", "summary", "commit_push"}


@dataclass
class ParseError(Exception):
    code: str
    line: int
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {"ok": False, "error": self.code, "line": int(self.line), "detail": str(self.detail)}


def _is_comment_or_blank(line: str) -> bool:
    s = line.strip()
    return (not s) or s.startswith("#")


def _require_str(obj: dict[str, Any], key: str, *, line: int) -> str:
    v = obj.get(key)
    if not isinstance(v, str) or not v.strip():
        raise ParseError("missing_or_invalid_field", line, f"{key} must be a non-empty string")
    return v


def _require_obj(obj: dict[str, Any], key: str, *, line: int, required: bool = False) -> dict[str, Any] | None:
    if key not in obj:
        if required:
            raise ParseError("missing_or_invalid_field", line, f"{key} must be an object")
        return None
    v = obj.get(key)
    if v is None:
        return None
    if not isinstance(v, dict):
        raise ParseError("missing_or_invalid_field", line, f"{key} must be an object")
    return v


def parse_aaps_v1(text: str) -> dict[str, Any]:
    """Parse AutoAppDev formatted pipeline script (AAPS v1) into canonical IR.

    Deterministic, no I/O, no execution.
    Raises ParseError for invalid input.
    """

    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")

    lines = text.splitlines()
    header_line = None
    header_lineno = 0
    for idx, raw in enumerate(lines, start=1):
        if _is_comment_or_blank(raw):
            continue
        header_line = raw.strip()
        header_lineno = idx
        break

    if header_line is None:
        raise ParseError("missing_header", 1, "expected header: AUTOAPPDEV_PIPELINE 1")
    if header_line != "AUTOAPPDEV_PIPELINE 1":
        raise ParseError("invalid_header", header_lineno, "expected header: AUTOAPPDEV_PIPELINE 1")

    ir: dict[str, Any] = {"kind": "autoappdev_ir", "version": 1, "tasks": []}
    tasks: list[dict[str, Any]] = ir["tasks"]

    cur_task: dict[str, Any] | None = None
    cur_step: dict[str, Any] | None = None

    seen_task_ids: set[str] = set()
    seen_step_ids: dict[str, set[str]] = {}
    seen_action_ids: dict[tuple[str, str], set[str]] = {}

    for lineno, raw in enumerate(lines, start=1):
        if lineno <= header_lineno:
            continue
        if _is_comment_or_blank(raw):
            continue
        stripped = raw.lstrip()
        # Split keyword + JSON part.
        parts = stripped.split(None, 1)
        if len(parts) != 2:
            raise ParseError("invalid_statement", lineno, "expected: KEYWORD <json-object>")
        kw = parts[0].strip()
        json_part = parts[1].strip()
        if kw not in ("TASK", "STEP", "ACTION"):
            raise ParseError("unknown_keyword", lineno, f"unknown keyword: {kw}")
        try:
            obj = json.loads(json_part)
        except Exception as e:
            raise ParseError("invalid_json", lineno, f"failed to parse JSON object: {type(e).__name__}: {e}") from e
        if not isinstance(obj, dict):
            raise ParseError("invalid_json_object", lineno, "statement JSON must be an object")

        if kw == "TASK":
            task_id = _require_str(obj, "id", line=lineno)
            title = _require_str(obj, "title", line=lineno)
            if task_id in seen_task_ids:
                raise ParseError("duplicate_id", lineno, f"duplicate task id: {task_id}")
            seen_task_ids.add(task_id)
            task_meta = _require_obj(obj, "meta", line=lineno, required=False)
            task: dict[str, Any] = {"id": task_id, "title": title, "steps": []}
            if task_meta is not None:
                task["meta"] = task_meta
            tasks.append(task)
            cur_task = task
            cur_step = None
            seen_step_ids[task_id] = set()
            continue

        if kw == "STEP":
            if not cur_task:
                raise ParseError("step_before_task", lineno, "STEP must appear after a TASK")
            step_id = _require_str(obj, "id", line=lineno)
            title = _require_str(obj, "title", line=lineno)
            block = _require_str(obj, "block", line=lineno)
            if block not in ALLOWED_BLOCKS:
                raise ParseError("invalid_block", lineno, f"unknown STEP.block: {block}")
            task_id = str(cur_task["id"])
            if step_id in seen_step_ids[task_id]:
                raise ParseError("duplicate_id", lineno, f"duplicate step id in task {task_id}: {step_id}")
            seen_step_ids[task_id].add(step_id)
            step_meta = _require_obj(obj, "meta", line=lineno, required=False)
            step: dict[str, Any] = {"id": step_id, "title": title, "block": block, "actions": []}
            if step_meta is not None:
                step["meta"] = step_meta
            cur_task["steps"].append(step)
            cur_step = step
            seen_action_ids[(task_id, step_id)] = set()
            continue

        if kw == "ACTION":
            if not cur_step or not cur_task:
                raise ParseError("action_before_step", lineno, "ACTION must appear after a STEP")
            action_id = _require_str(obj, "id", line=lineno)
            kind = _require_str(obj, "kind", line=lineno)
            params = _require_obj(obj, "params", line=lineno, required=False)
            meta = _require_obj(obj, "meta", line=lineno, required=False)
            task_id = str(cur_task["id"])
            step_id = str(cur_step["id"])
            key = (task_id, step_id)
            if action_id in seen_action_ids[key]:
                raise ParseError("duplicate_id", lineno, f"duplicate action id in step {step_id}: {action_id}")
            seen_action_ids[key].add(action_id)
            action: dict[str, Any] = {"id": action_id, "kind": kind}
            if params is not None:
                action["params"] = params
            if meta is not None:
                action["meta"] = meta
            cur_step["actions"].append(action)
            continue

    if not tasks:
        raise ParseError("missing_task", header_lineno, "expected at least one TASK")

    return ir

