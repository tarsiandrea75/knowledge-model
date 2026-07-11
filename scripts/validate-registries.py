#!/usr/bin/env python3
"""Validate canonical RKM registry files using only the standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELATIONSHIP_TYPE_REGISTRY = (
    REPOSITORY_ROOT / "registries" / "relationship-type-registry.json"
)
UPPERCASE_SNAKE_CASE = re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*$")


def display(path: Path) -> str:
    return str(path.relative_to(REPOSITORY_ROOT))


def load_json(path: Path, errors: list[str]) -> object | None:
    if not path.exists():
        errors.append(f"{display(path)}: file does not exist")
        return None
    if not path.is_file():
        errors.append(f"{display(path)}: path is not a file")
        return None

    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        errors.append(f"{display(path)}: invalid JSON: {exc}")
    except OSError as exc:
        errors.append(f"{display(path)}: could not read file: {exc}")

    return None


def validate_relationship_type_registry(errors: list[str]) -> None:
    path = RELATIONSHIP_TYPE_REGISTRY
    document = load_json(path, errors)
    if document is None:
        return

    name = display(path)
    if not isinstance(document, dict):
        errors.append(f"{name}: registry root must be a JSON object")
        return

    if "metadata" not in document:
        errors.append(f"{name}: metadata is required")
    elif not isinstance(document["metadata"], dict):
        errors.append(f"{name}: metadata must be a JSON object")

    relationship_types = document.get("relationshipTypes")
    if not isinstance(relationship_types, list):
        errors.append(f"{name}: relationshipTypes must be a non-empty array")
        return
    if not relationship_types:
        errors.append(f"{name}: relationshipTypes must be a non-empty array")
        return

    seen_types: dict[str, int] = {}
    for index, relationship_type in enumerate(relationship_types):
        prefix = f"{name}: relationshipTypes[{index}]"
        if not isinstance(relationship_type, dict):
            errors.append(f"{prefix}: relationship type entry must be a JSON object")
            continue

        type_value = relationship_type.get("type")
        if not isinstance(type_value, str):
            errors.append(f"{prefix}.type: type is required and must be a string")
            continue

        if not UPPERCASE_SNAKE_CASE.fullmatch(type_value):
            errors.append(
                f"{prefix}.type: {type_value!r} must be uppercase snake case"
            )

        previous_index = seen_types.get(type_value)
        if previous_index is not None:
            errors.append(
                f"{prefix}.type: duplicate type value {type_value!r}; "
                f"first seen at relationshipTypes[{previous_index}]"
            )
        else:
            seen_types[type_value] = index


def main() -> int:
    errors: list[str] = []
    validate_relationship_type_registry(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Registry validation passed: "
        f"{display(RELATIONSHIP_TYPE_REGISTRY)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
