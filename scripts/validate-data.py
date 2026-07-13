#!/usr/bin/env python3
"""
Validate RKM populated data instances against schemas declared by the data manifest.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver
from jsonschema.exceptions import RefResolutionError, SchemaError, ValidationError as JsonSchemaError


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DATA_MANIFEST_PATH = REPOSITORY_ROOT / "data" / "manifest.json"
SCHEMA_ROOT = REPOSITORY_ROOT / "schema"


class DataValidationError(Exception):
    """Raised when data validation cannot complete successfully."""


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPOSITORY_ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise DataValidationError(f"{display_path(path)}: file does not exist") from exc
    except json.JSONDecodeError as exc:
        raise DataValidationError(f"{display_path(path)}: invalid JSON: {exc}") from exc


def repository_path(value: object, field_name: str) -> Path:
    if not isinstance(value, str) or not value:
        raise DataValidationError(f"{field_name} must be a non-empty string")

    path = (REPOSITORY_ROOT / value).resolve()
    try:
        path.relative_to(REPOSITORY_ROOT)
    except ValueError as exc:
        raise DataValidationError(f"{field_name} must resolve inside the repository: {value}") from exc
    return path


def require_object(value: object, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DataValidationError(f"{context} must be a JSON object")
    return value


def require_list(value: object, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise DataValidationError(f"{context} must be a JSON array")
    return value


def load_schema_store() -> dict[str, Any]:
    store: dict[str, Any] = {}
    if not SCHEMA_ROOT.exists():
        raise DataValidationError(f"{display_path(SCHEMA_ROOT)}: schema directory is missing")

    for schema_path in sorted(SCHEMA_ROOT.rglob("*.schema.json")):
        schema = require_object(load_json(schema_path), display_path(schema_path))
        store[schema_path.resolve().as_uri()] = schema

        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            store[schema_id] = schema

    return store


def validate_instance(
    instance: Any,
    schema: dict[str, Any],
    data_path: Path,
    schema_path: Path,
    schema_store: dict[str, Any],
) -> None:
    resolver = RefResolver(
        base_uri=schema_path.as_uri(),
        referrer=schema,
        store=schema_store,
    )
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, resolver=resolver)
        validator.validate(instance)
    except SchemaError as exc:
        raise DataValidationError(f"{display_path(schema_path)}: invalid schema: {exc.message}") from exc
    except RefResolutionError as exc:
        raise DataValidationError(
            f"{display_path(schema_path)}: failed to resolve schema reference: {exc}"
        ) from exc
    except JsonSchemaError as exc:
        location = display_path(data_path)
        error_path = "/".join(str(part) for part in exc.absolute_path)
        if error_path:
            location = f"{location}/{error_path}"
        raise DataValidationError(
            f"{location}: failed validation against {display_path(schema_path)}: {exc.message}"
        ) from exc


def validate_manifest(manifest_path: Path = DATA_MANIFEST_PATH) -> tuple[int, int]:
    if not manifest_path.exists():
        raise DataValidationError(f"{display_path(manifest_path)}: data manifest is missing")

    manifest = require_object(load_json(manifest_path), display_path(manifest_path))
    data_entries = require_list(manifest.get("data"), f"{display_path(manifest_path)}.data")
    schema_store = load_schema_store()

    data_count = 0
    validation_count = 0
    for index, raw_entry in enumerate(data_entries, start=1):
        entry = require_object(raw_entry, f"data manifest entry {index}")
        data_path = repository_path(entry.get("file"), f"data manifest entry {index}.file")
        if not data_path.exists():
            raise DataValidationError(f"{display_path(data_path)}: data file is missing")

        schema_path = repository_path(entry.get("schema"), f"data manifest entry {index}.schema")
        if not schema_path.exists():
            raise DataValidationError(f"{display_path(schema_path)}: schema file is missing")

        data = load_json(data_path)
        schema = require_object(load_json(schema_path), display_path(schema_path))
        validate_instance(data, schema, data_path, schema_path, schema_store)
        data_count += 1
        validation_count += 1

    return data_count, validation_count


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        manifest = root / "manifest.json"
        manifest.write_text('{"data": []}\n', encoding="utf-8")

        loaded = require_object(load_json(manifest), "manifest")
        entries = require_list(loaded.get("data"), "manifest.data")
        if entries != []:
            raise DataValidationError("self-test failed: data manifest array was not parsed")

        path = repository_path("data/manifest.json", "self-test.path")
        if path != DATA_MANIFEST_PATH.resolve():
            raise DataValidationError("self-test failed: repository path resolution returned the wrong path")


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        try:
            run_self_test()
        except DataValidationError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print("validate-data self-test passed.")
        return 0

    if len(sys.argv) != 1:
        print("Usage: validate-data.py [--self-test]", file=sys.stderr)
        return 2

    try:
        data_count, validation_count = validate_manifest()
    except DataValidationError as exc:
        print(str(exc), file=sys.stderr)
        print("Data validation failed.", file=sys.stderr)
        return 1

    print(f"Validated {data_count} data file(s) with {validation_count} schema validation(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
