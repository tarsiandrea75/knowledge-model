#!/usr/bin/env python3
"""Validate architecture documentation relationship predicate mentions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELATIONSHIP_TYPE_REGISTRY = (
    REPOSITORY_ROOT / "registries" / "relationship-type-registry.json"
)
ARCHITECTURE_DOCS = REPOSITORY_ROOT / "docs" / "architecture"

UPPERCASE_SNAKE_CASE = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\b")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE_START = re.compile(r"^```([A-Za-z0-9_-]*)\s*$")
FENCE_END = re.compile(r"^```\s*$")
IGNORED_MARKERS = (
    "noncanonical",
    "candidate",
    "future candidate",
    "deprecated",
    "rejected",
    "derived inverse",
    "avoid storing both",
)


def display(path: Path) -> str:
    return str(path.relative_to(REPOSITORY_ROOT))


def is_uppercase_snake_case(value: str) -> bool:
    return UPPERCASE_SNAKE_CASE.fullmatch(value) is not None


def line_is_ignored(line: str) -> bool:
    normalized = line.lower()
    return any(marker in normalized for marker in IGNORED_MARKERS)


def load_canonical_predicates(errors: list[str]) -> set[str]:
    try:
        with RELATIONSHIP_TYPE_REGISTRY.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{display(RELATIONSHIP_TYPE_REGISTRY)}: could not load registry: {exc}")
        return set()

    relationship_types = document.get("relationshipTypes")
    if not isinstance(relationship_types, list):
        errors.append(
            f"{display(RELATIONSHIP_TYPE_REGISTRY)}: relationshipTypes must be an array"
        )
        return set()

    predicates: set[str] = set()
    for index, relationship_type in enumerate(relationship_types):
        if not isinstance(relationship_type, dict):
            errors.append(
                f"{display(RELATIONSHIP_TYPE_REGISTRY)}: "
                f"relationshipTypes[{index}] must be an object"
            )
            continue

        predicate = relationship_type.get("type")
        if not isinstance(predicate, str):
            errors.append(
                f"{display(RELATIONSHIP_TYPE_REGISTRY)}: "
                f"relationshipTypes[{index}].type must be a string"
            )
            continue

        predicates.add(predicate)

    return predicates


def relationship_predicate_in_example(line: str) -> str | None:
    candidates = []
    for match in UPPERCASE_SNAKE_CASE.finditer(line):
        before = line[: match.start()].strip()
        after = line[match.end() :].strip()
        if before and after:
            candidates.append(match)

    if not candidates:
        return None

    for match in candidates:
        if "_" in match.group(0):
            return match.group(0)

    for match in candidates:
        before = line[: match.start()]
        after = line[match.end() :]
        if re.search(r"[─-]{2,}\s*$", before) and re.search(r"^\s*[─-]{2,}", after):
            return match.group(0)

    return None


def validate_fenced_line(
    path: Path,
    line_number: int,
    line: str,
    canonical_predicates: set[str],
    errors: list[str],
) -> None:
    if line_is_ignored(line):
        return

    predicate = relationship_predicate_in_example(line)
    if predicate is None or predicate in canonical_predicates:
        return

    errors.append(
        f"{display(path)}:{line_number}: unknown relationship predicate {predicate}"
    )


def validate_inline_code(
    path: Path,
    line_number: int,
    line: str,
    canonical_predicates: set[str],
    errors: list[str],
) -> None:
    if line_is_ignored(line):
        return

    for match in INLINE_CODE.finditer(line):
        predicate = match.group(1).strip()
        if not is_uppercase_snake_case(predicate):
            continue
        if predicate in canonical_predicates:
            continue
        errors.append(
            f"{display(path)}:{line_number}: unknown relationship predicate {predicate}"
        )


def validate_markdown_file(
    path: Path,
    canonical_predicates: set[str],
    errors: list[str],
) -> None:
    in_fence = False
    inspect_fence = False
    ignore_fence = False
    recent_nonblank_lines: list[str] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"{display(path)}: could not read file: {exc}")
        return

    for line_number, line in enumerate(lines, start=1):
        if not in_fence:
            fence = FENCE_START.match(line)
            if fence:
                in_fence = True
                language = fence.group(1).lower()
                inspect_fence = language in {"", "text"}
                ignore_fence = any(line_is_ignored(recent) for recent in recent_nonblank_lines)
                continue

            validate_inline_code(
                path,
                line_number,
                line,
                canonical_predicates,
                errors,
            )
            if line.strip():
                recent_nonblank_lines.append(line)
                recent_nonblank_lines = recent_nonblank_lines[-4:]
            continue

        if FENCE_END.match(line):
            in_fence = False
            inspect_fence = False
            ignore_fence = False
            continue

        if inspect_fence and not ignore_fence:
            validate_fenced_line(
                path,
                line_number,
                line,
                canonical_predicates,
                errors,
            )


def main() -> int:
    errors: list[str] = []
    canonical_predicates = load_canonical_predicates(errors)

    if canonical_predicates:
        for path in sorted(ARCHITECTURE_DOCS.glob("*.md")):
            validate_markdown_file(path, canonical_predicates, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Documentation relationship validation passed: "
        f"{display(ARCHITECTURE_DOCS)}/*.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
