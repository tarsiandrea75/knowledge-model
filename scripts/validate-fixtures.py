#!/usr/bin/env python3
"""
Validate RKM fixture instances against the schemas declared by the fixture manifest.
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
FIXTURE_MANIFEST_PATH = REPOSITORY_ROOT / "examples" / "fixtures" / "fixture-manifest.json"
SCHEMA_ROOT = REPOSITORY_ROOT / "schema"


class FixtureValidationError(Exception):
    """Raised when fixture validation cannot complete successfully."""


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
        raise FixtureValidationError(f"{display_path(path)}: file does not exist") from exc
    except json.JSONDecodeError as exc:
        raise FixtureValidationError(f"{display_path(path)}: invalid JSON: {exc}") from exc


def repository_path(value: object, field_name: str) -> Path:
    if not isinstance(value, str) or not value:
        raise FixtureValidationError(f"{field_name} must be a non-empty string")

    path = (REPOSITORY_ROOT / value).resolve()
    try:
        path.relative_to(REPOSITORY_ROOT)
    except ValueError as exc:
        raise FixtureValidationError(f"{field_name} must resolve inside the repository: {value}") from exc
    return path


def require_object(value: object, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FixtureValidationError(f"{context} must be a JSON object")
    return value


def require_list(value: object, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise FixtureValidationError(f"{context} must be a JSON array")
    return value


def resolve_json_pointer(document: Any, pointer: str, fixture_path: Path) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise FixtureValidationError(
            f"{display_path(fixture_path)}: instancePointer must be empty or start with /: {pointer}"
        )

    current = document
    for raw_part in pointer.lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            raise FixtureValidationError(
                f"{display_path(fixture_path)}: instancePointer does not resolve: {pointer}"
            )
    return current


def load_schema_store() -> dict[str, Any]:
    store: dict[str, Any] = {}
    if not SCHEMA_ROOT.exists():
        raise FixtureValidationError(f"{display_path(SCHEMA_ROOT)}: schema directory is missing")

    for schema_path in sorted(SCHEMA_ROOT.rglob("*.schema.json")):
        schema = require_object(load_json(schema_path), display_path(schema_path))
        store[schema_path.resolve().as_uri()] = schema

        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            store[schema_id] = schema

    return store


def validation_entries(entry: dict[str, Any], entry_number: int) -> list[dict[str, Any]]:
    has_schema = "schema" in entry
    has_validations = "validations" in entry

    if has_schema and has_validations:
        raise FixtureValidationError(
            f"fixture manifest entry {entry_number}: use either schema or validations"
        )
    if has_schema:
        return [{"instancePointer": "", "schema": entry["schema"]}]
    if has_validations:
        validations = require_list(entry["validations"], f"fixture manifest entry {entry_number}.validations")
        return [require_object(item, f"fixture manifest entry {entry_number}.validations item") for item in validations]
    raise FixtureValidationError(f"fixture manifest entry {entry_number}: schema or validations is required")


def validate_instance(
    instance: Any,
    schema: dict[str, Any],
    fixture_path: Path,
    schema_path: Path,
    pointer: str,
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
        raise FixtureValidationError(f"{display_path(schema_path)}: invalid schema: {exc.message}") from exc
    except RefResolutionError as exc:
        raise FixtureValidationError(
            f"{display_path(schema_path)}: failed to resolve schema reference: {exc}"
        ) from exc
    except JsonSchemaError as exc:
        location = display_path(fixture_path)
        if pointer:
            location = f"{location}#{pointer}"
        error_path = "/".join(str(part) for part in exc.absolute_path)
        if error_path:
            location = f"{location}/{error_path}"
        raise FixtureValidationError(
            f"{location}: failed validation against {display_path(schema_path)}: {exc.message}"
        ) from exc


def validate_manifest(manifest_path: Path = FIXTURE_MANIFEST_PATH) -> tuple[int, int]:
    manifest = require_object(load_json(manifest_path), display_path(manifest_path))
    fixtures = require_list(manifest.get("fixtures"), f"{display_path(manifest_path)}.fixtures")
    schema_store = load_schema_store()

    fixture_count = 0
    validation_count = 0
    for index, raw_entry in enumerate(fixtures, start=1):
        entry = require_object(raw_entry, f"fixture manifest entry {index}")
        fixture_path = repository_path(entry.get("fixture"), f"fixture manifest entry {index}.fixture")
        if not fixture_path.exists():
            raise FixtureValidationError(f"{display_path(fixture_path)}: fixture file is missing")

        fixture = load_json(fixture_path)
        fixture_count += 1

        for raw_validation in validation_entries(entry, index):
            schema_path = repository_path(
                raw_validation.get("schema"),
                f"fixture manifest entry {index}.schema",
            )
            if not schema_path.exists():
                raise FixtureValidationError(f"{display_path(schema_path)}: schema file is missing")

            pointer = raw_validation.get("instancePointer", "")
            if not isinstance(pointer, str):
                raise FixtureValidationError(
                    f"fixture manifest entry {index}.instancePointer must be a string"
                )

            schema = require_object(load_json(schema_path), display_path(schema_path))
            instance = resolve_json_pointer(fixture, pointer, fixture_path)
            validate_instance(instance, schema, fixture_path, schema_path, pointer, schema_store)
            validation_count += 1

    return fixture_count, validation_count


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        fixture = {"claim": {"id": "CLAIM-0001"}}
        pointer_result = resolve_json_pointer(fixture, "/claim/id", root / "fixture.json")
        if pointer_result != "CLAIM-0001":
            raise FixtureValidationError("self-test failed: JSON Pointer resolution returned the wrong value")

        manifest_entry = {"fixture": "fixture.json", "schema": "schema.json"}
        entries = validation_entries(manifest_entry, 1)
        if entries != [{"instancePointer": "", "schema": "schema.json"}]:
            raise FixtureValidationError("self-test failed: schema manifest entry expansion returned the wrong value")

        nested_manifest_entry = {
            "fixture": "fixture.json",
            "validations": [{"instancePointer": "/claim", "schema": "schema.json"}],
        }
        nested_entries = validation_entries(nested_manifest_entry, 1)
        if nested_entries != [{"instancePointer": "/claim", "schema": "schema.json"}]:
            raise FixtureValidationError("self-test failed: nested manifest entry expansion returned the wrong value")


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        try:
            run_self_test()
        except FixtureValidationError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print("validate-fixtures self-test passed.")
        return 0

    if len(sys.argv) != 1:
        print("Usage: validate-fixtures.py [--self-test]", file=sys.stderr)
        return 2

    try:
        fixture_count, validation_count = validate_manifest()
    except FixtureValidationError as exc:
        print(str(exc), file=sys.stderr)
        print("Fixture validation failed.", file=sys.stderr)
        return 1

    print(
        f"Validated {fixture_count} fixture file(s) with {validation_count} schema validation(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
