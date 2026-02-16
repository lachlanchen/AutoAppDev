from __future__ import annotations

from typing import Any


# Built-in actions are virtual (not persisted) and live in a reserved ID range.
# Keep IDs within JS safe integer range for the PWA.
BUILTIN_ID_BASE = 9_000_000_000


def _prompt_preamble() -> str:
    # Keep this short and stable; the goal is to nudge multilingual output without
    # requiring new schema/config wiring.
    return (
        "Language:\n"
        "- Write in the same language as the task/context.\n"
        "- If a language is explicitly required, follow it.\n"
        "- Default to English if unclear.\n"
    )


def _prompt_placeholders_note() -> str:
    return (
        "Context placeholders (if present):\n"
        "- {{task.title}}, {{task.acceptance}}, {{runtime_dir}}\n"
    )


_BUILTINS_FULL: list[dict[str, Any]] = [
    {
        "id": BUILTIN_ID_BASE + 1,
        "title": "Plan (builtin, multilingual)",
        "kind": "prompt",
        "enabled": True,
        "readonly": True,
        "created_at": None,
        "updated_at": None,
        "spec": {
            "reasoning": "medium",
            "prompt": (
                _prompt_preamble()
                + _prompt_placeholders_note()
                + "\n"
                + "You are implementing one small, incremental task in a larger system.\n"
                + "Write a step-specific plan and explicit acceptance checks.\n"
                + "\n"
                + "Output:\n"
                + "- Plan steps (small, incremental)\n"
                + "- Commands to run (use timeouts for anything that could hang)\n"
                + "- Acceptance checklist\n"
            ),
        },
    },
    {
        "id": BUILTIN_ID_BASE + 2,
        "title": "Work (builtin, multilingual)",
        "kind": "prompt",
        "enabled": True,
        "readonly": True,
        "created_at": None,
        "updated_at": None,
        "spec": {
            "reasoning": "medium",
            "prompt": (
                _prompt_preamble()
                + _prompt_placeholders_note()
                + "\n"
                + "Implement the smallest set of changes needed to satisfy acceptance.\n"
                + "Keep the architecture consistent with the repo.\n"
                + "Avoid unrelated refactors.\n"
            ),
        },
    },
    {
        "id": BUILTIN_ID_BASE + 3,
        "title": "Debug/Verify (builtin, multilingual)",
        "kind": "prompt",
        "enabled": True,
        "readonly": True,
        "created_at": None,
        "updated_at": None,
        "spec": {
            "reasoning": "low",
            "prompt": (
                _prompt_preamble()
                + _prompt_placeholders_note()
                + "\n"
                + "Run the smallest possible verification (build/run/smoke).\n"
                + "- Use timeouts for anything that could hang.\n"
                + "- Record exact commands and results.\n"
                + "- If issues are found, implement minimal fixes and re-run verification.\n"
            ),
        },
    },
    {
        "id": BUILTIN_ID_BASE + 4,
        "title": "Fix (builtin, multilingual)",
        "kind": "prompt",
        "enabled": True,
        "readonly": True,
        "created_at": None,
        "updated_at": None,
        "spec": {
            "reasoning": "medium",
            "prompt": (
                _prompt_preamble()
                + _prompt_placeholders_note()
                + "\n"
                + "Implement minimal fixes required to make verification pass.\n"
                + "Do not broaden scope.\n"
            ),
        },
    },
    {
        "id": BUILTIN_ID_BASE + 5,
        "title": "Summary (builtin, multilingual)",
        "kind": "prompt",
        "enabled": True,
        "readonly": True,
        "created_at": None,
        "updated_at": None,
        "spec": {
            "reasoning": "low",
            "prompt": (
                _prompt_preamble()
                + _prompt_placeholders_note()
                + "\n"
                + "Write a concise summary:\n"
                + "- What changed\n"
                + "- Why\n"
                + "- How to verify\n"
                + "\n"
                + "If target languages are specified elsewhere, add a short 'Translations' section.\n"
            ),
        },
    },
    {
        "id": BUILTIN_ID_BASE + 6,
        "title": "Release Note (builtin, multilingual)",
        "kind": "prompt",
        "enabled": True,
        "readonly": True,
        "created_at": None,
        "updated_at": None,
        "spec": {
            "reasoning": "low",
            "prompt": (
                _prompt_preamble()
                + "\n"
                + "Write a short release/log note for the operator UI.\n"
                + "- Mention any manual follow-ups.\n"
                + "- If git commit/push is policy-driven, state that it is handled externally.\n"
            ),
        },
    },
]

_BUILTINS_BY_ID: dict[int, dict[str, Any]] = {int(a["id"]): a for a in _BUILTINS_FULL}


def is_builtin_action_id(action_id: int) -> bool:
    try:
        aid = int(action_id)
    except Exception:
        return False
    return aid in _BUILTINS_BY_ID


def get_builtin_action(action_id: int) -> dict[str, Any] | None:
    """Return full builtin action (includes spec)."""
    try:
        aid = int(action_id)
    except Exception:
        return None
    it = _BUILTINS_BY_ID.get(aid)
    if not it:
        return None
    # Shallow copy for safety.
    return dict(it)


def list_builtin_action_summaries() -> list[dict[str, Any]]:
    """Return list items for GET /api/actions (no spec)."""
    out: list[dict[str, Any]] = []
    for it in _BUILTINS_FULL:
        obj = dict(it)
        obj.pop("spec", None)
        out.append(obj)
    return out

