import re
from dataclasses import dataclass
from typing import Any

from .pipeline_parser import ParseError, parse_aaps_v1


_AAPS_LINE_RE = re.compile(r"^\s*#\s*AAPS:\s*(.*)$")


@dataclass
class ShellImportError(Exception):
    code: str
    line: int
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {"ok": False, "error": self.code, "line": int(self.line), "detail": str(self.detail)}


def extract_aaps_from_shell(shell_text: str) -> tuple[str, list[int]]:
    """Extract embedded AAPS v1 lines from structured shell comments.

    Only lines matching: ^\\s*#\\s*AAPS:\\s*(.*)$
    The captured remainder is treated as a single AAPS line.

    Returns (aaps_text, shell_line_map) where shell_line_map[i] is the 1-based shell
    line number corresponding to AAPS line (i+1).
    """

    if shell_text.startswith("\ufeff"):
        shell_text = shell_text.lstrip("\ufeff")

    aaps_lines: list[str] = []
    shell_line_map: list[int] = []
    for lineno, raw in enumerate(shell_text.splitlines(), start=1):
        m = _AAPS_LINE_RE.match(raw)
        if not m:
            continue
        aaps_lines.append(m.group(1))
        shell_line_map.append(lineno)

    if not shell_line_map:
        raise ShellImportError("missing_annotations", 1, 'expected at least one "# AAPS:" annotation line')

    return "\n".join(aaps_lines), shell_line_map


def import_shell_annotated_to_ir(shell_text: str) -> dict[str, Any]:
    """Best-effort import from an annotated shell script into canonical IR.

    Deterministic: never executes code; ignores all non-annotation shell lines.
    On parse failure, the error line is mapped back to the original shell line.
    """

    aaps_text, shell_line_map = extract_aaps_from_shell(shell_text)
    warnings: list[str] = []

    try:
        ir = parse_aaps_v1(aaps_text)
    except ParseError as e:
        aaps_line = int(getattr(e, "line", 1) or 1)
        shell_line = shell_line_map[0]
        if 1 <= aaps_line <= len(shell_line_map):
            shell_line = shell_line_map[aaps_line - 1]
        raise ShellImportError(str(e.code), shell_line, str(e.detail)) from e

    return {"aaps_text": aaps_text, "ir": ir, "warnings": warnings}
