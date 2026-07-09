#!/usr/bin/env python3
"""
Validate RKM JSON Schema files using only the Python standard library.

The script checks that every schema file is valid JSON, declares JSON Schema
Draft 2020-12, uses an RKM-compatible schema identifier, and does not contain
broken local file references.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urldefrag


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPOSITORY_ROOT / "schema"
EXPECTED_DRAFT = "https://json-schema.org/draft/2020-12/schema"
ALLOWED_ID_PREFIXES = (
    "https://rkm.org/schema/",
)


class ValidationError(Exception):
    """Raised when a schema validation check fails."""


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def require_object(path: Path, document: object) -> dict[str, object]:
    if not isinstance(document, dict):
        raise ValidationError(f"{path}: schema root must be a JSON object")
    return document


def find_schema_files() -> list[Path]:
    if not SCHEMA_ROOT.exists():
        raise ValidationError(f"{SCHEMA_ROOT}: schema directory does not exist")
    return sorted(SCHEMA_ROOT.rglob("*.schema.json"))


def walk_json(value: object) -> object:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def resolve_json_pointer(document: object, pointer: str) -> bool:
    if pointer in ("", "/"):
        return True
    if not pointer.startswith("/"):
        return False

    current = document
    for raw_part in pointer.lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False
    return True


def referenced_schema_path(schema_path: Path, reference: str) -> Path | None:
    reference_path, _fragment = urldefrag(reference)
    if reference_path == "":
        return schema_path
    if reference_path.startswith(("http://", "https://")):
        return None
    return (schema_path.parent / reference_path).resolve()


def validate_reference(
    schema_path: Path,
    schema_document: dict[str, object],
    reference: str,
    loaded_documents: dict[Path, dict[str, object]],
) -> None:
    target_path = referenced_schema_path(schema_path, reference)
    if target_path is None:
        return

    reference_path, fragment = urldefrag(reference)
    if target_path not in loaded_documents:
        display_reference = reference_path or schema_path.name
        raise ValidationError(
            f"{schema_path}: unresolved $ref target {display_reference}"
        )

    target_document = schema_document if target_path == schema_path else loaded_documents[target_path]
    if fragment and not resolve_json_pointer(target_document, fragment):
        raise ValidationError(f"{schema_path}: unresolved $ref fragment {reference}")


def validate_schema_header(path: Path, document: dict[str, object]) -> None:
    schema_value = document.get("$schema")
    if schema_value != EXPECTED_DRAFT:
        raise ValidationError(
            f"{path}: $schema must be {EXPECTED_DRAFT!r}, found {schema_value!r}"
        )

    identifier = document.get("$id")
    if not isinstance(identifier, str):
        raise ValidationError(f"{path}: $id is required and must be a string")
    if not identifier.endswith(".schema.json"):
        raise ValidationError(f"{path}: $id must end with .schema.json")
    if not identifier.startswith(ALLOWED_ID_PREFIXES):
        allowed = ", ".join(ALLOWED_ID_PREFIXES)
        raise ValidationError(f"{path}: $id must start with one of: {allowed}")


def validate_schema_references(
    path: Path,
    document: dict[str, object],
    loaded_documents: dict[Path, dict[str, object]],
) -> None:
    for node in walk_json(document):
        if isinstance(node, dict) and "$ref" in node:
            reference = node["$ref"]
            if not isinstance(reference, str):
                raise ValidationError(f"{path}: $ref must be a string")
            validate_reference(path, document, reference, loaded_documents)


def main() -> int:
    schema_files = find_schema_files()
    loaded_documents: dict[Path, dict[str, object]] = {}

    for path in schema_files:
        document = require_object(path, load_json(path))
        loaded_documents[path.resolve()] = document

    errors: list[str] = []

    for path in schema_files:
        resolved_path = path.resolve()
        document = loaded_documents[resolved_path]
        try:
            validate_schema_header(path, document)
            validate_schema_references(resolved_path, document, loaded_documents)
        except ValidationError as exc:
            errors.append(str(exc))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"Validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(f"Validated {len(schema_files)} schema file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
