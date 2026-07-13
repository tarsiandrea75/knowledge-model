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
RELATIONSHIP_SET_SCHEMA_PATH = SCHEMA_ROOT / "relationship-set.schema.json"
RELATIONSHIP_TYPE_REGISTRY_PATH = REPOSITORY_ROOT / "registries" / "relationship-type-registry.json"


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


def is_relationship_set_schema(schema_path: Path) -> bool:
    return schema_path.resolve() == RELATIONSHIP_SET_SCHEMA_PATH.resolve()


def relative_repository_file(path: Path) -> str:
    return display_path(path.resolve())


def load_registered_predicates(registry_path: Path = RELATIONSHIP_TYPE_REGISTRY_PATH) -> set[str]:
    registry = require_object(load_json(registry_path), display_path(registry_path))
    relationship_types = require_list(
        registry.get("relationshipTypes"),
        f"{display_path(registry_path)}.relationshipTypes",
    )

    predicates: set[str] = set()
    for index, relationship_type in enumerate(relationship_types, start=1):
        entry = require_object(
            relationship_type,
            f"{display_path(registry_path)}.relationshipTypes[{index}]",
        )
        predicate = entry.get("type")
        if not isinstance(predicate, str) or not predicate:
            raise DataValidationError(
                f"{display_path(registry_path)}.relationshipTypes[{index}].type must be a non-empty string"
            )
        predicates.add(predicate)
    return predicates


def build_entity_file_index(data_records: list[tuple[Path, Any]]) -> dict[str, str]:
    entity_files: dict[str, str] = {}
    for data_path, data in data_records:
        record = require_object(data, display_path(data_path))
        identity = require_object(record.get("identity"), f"{display_path(data_path)}.identity")
        entity_id = identity.get("id")
        if not isinstance(entity_id, str) or not entity_id:
            raise DataValidationError(f"{display_path(data_path)}.identity.id must be a non-empty string")

        data_file = relative_repository_file(data_path)
        previous_file = entity_files.get(entity_id)
        if previous_file is not None:
            raise DataValidationError(
                f"{display_path(data_path)}: duplicate entity id {entity_id}; already declared in {previous_file}"
            )
        entity_files[entity_id] = data_file
    return entity_files


def validate_relationship_semantics(
    relationship_sets: list[tuple[Path, Any]],
    registered_predicates: set[str],
    entity_files: dict[str, str],
) -> int:
    relationship_ids: dict[str, str] = {}
    semantic_triples: dict[tuple[str, str, str], str] = {}
    validation_count = 0

    for relationship_set_path, relationship_set in relationship_sets:
        relationship_set_object = require_object(relationship_set, display_path(relationship_set_path))
        relationships = require_list(
            relationship_set_object.get("relationships"),
            f"{display_path(relationship_set_path)}.relationships",
        )

        for index, raw_relationship in enumerate(relationships, start=1):
            context = f"{display_path(relationship_set_path)}.relationships[{index}]"
            relationship = require_object(raw_relationship, context)

            relationship_id = relationship.get("id")
            predicate = relationship.get("predicate")
            source_id = relationship.get("sourceId")
            target_id = relationship.get("targetId")
            source_data_file = relationship.get("sourceDataFile")
            target_data_file = relationship.get("targetDataFile")

            if not isinstance(relationship_id, str) or not relationship_id:
                raise DataValidationError(f"{context}.id must be a non-empty string")
            if not isinstance(predicate, str) or not predicate:
                raise DataValidationError(f"{context}.predicate must be a non-empty string")
            if not isinstance(source_id, str) or not source_id:
                raise DataValidationError(f"{context}.sourceId must be a non-empty string")
            if not isinstance(target_id, str) or not target_id:
                raise DataValidationError(f"{context}.targetId must be a non-empty string")
            if not isinstance(source_data_file, str) or not source_data_file:
                raise DataValidationError(f"{context}.sourceDataFile must be a non-empty string")
            if not isinstance(target_data_file, str) or not target_data_file:
                raise DataValidationError(f"{context}.targetDataFile must be a non-empty string")

            previous_relationship_file = relationship_ids.get(relationship_id)
            if previous_relationship_file is not None:
                raise DataValidationError(
                    f"{context}: duplicate relationship id {relationship_id}; "
                    f"already declared in {previous_relationship_file}"
                )
            relationship_ids[relationship_id] = display_path(relationship_set_path)

            if predicate not in registered_predicates:
                raise DataValidationError(
                    f"{context}.predicate {predicate} is not registered in "
                    f"{display_path(RELATIONSHIP_TYPE_REGISTRY_PATH)}"
                )

            actual_source_file = entity_files.get(source_id)
            if actual_source_file is None:
                raise DataValidationError(
                    f"{context}.sourceId {source_id} does not match any data entity record in "
                    f"{display_path(DATA_MANIFEST_PATH)}"
                )

            actual_target_file = entity_files.get(target_id)
            if actual_target_file is None:
                raise DataValidationError(
                    f"{context}.targetId {target_id} does not match any data entity record in "
                    f"{display_path(DATA_MANIFEST_PATH)}"
                )

            if source_data_file != actual_source_file:
                raise DataValidationError(
                    f"{context}.sourceDataFile points to {source_data_file}, but sourceId {source_id} "
                    f"is declared in {actual_source_file}"
                )

            if target_data_file != actual_target_file:
                raise DataValidationError(
                    f"{context}.targetDataFile points to {target_data_file}, but targetId {target_id} "
                    f"is declared in {actual_target_file}"
                )

            semantic_triple = (source_id, predicate, target_id)
            previous_triple_file = semantic_triples.get(semantic_triple)
            if previous_triple_file is not None:
                raise DataValidationError(
                    f"{context}: duplicate semantic relationship triple "
                    f"{source_id} {predicate} {target_id}; already declared in {previous_triple_file}"
                )
            semantic_triples[semantic_triple] = display_path(relationship_set_path)
            validation_count += 1

    return validation_count


def validate_manifest(manifest_path: Path = DATA_MANIFEST_PATH) -> tuple[int, int, int]:
    if not manifest_path.exists():
        raise DataValidationError(f"{display_path(manifest_path)}: data manifest is missing")

    manifest = require_object(load_json(manifest_path), display_path(manifest_path))
    data_entries = require_list(manifest.get("data"), f"{display_path(manifest_path)}.data")
    schema_store = load_schema_store()

    data_count = 0
    validation_count = 0
    entity_records: list[tuple[Path, Any]] = []
    relationship_sets: list[tuple[Path, Any]] = []
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

        if is_relationship_set_schema(schema_path):
            relationship_sets.append((data_path, data))
        else:
            entity_records.append((data_path, data))

    semantic_validation_count = 0
    if relationship_sets:
        registered_predicates = load_registered_predicates()
        entity_files = build_entity_file_index(entity_records)
        semantic_validation_count = validate_relationship_semantics(
            relationship_sets,
            registered_predicates,
            entity_files,
        )

    return data_count, validation_count, semantic_validation_count


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

        relationship_schema = repository_path(
            "schema/relationship-set.schema.json",
            "self-test.relationshipSchema",
        )
        if relationship_schema != (SCHEMA_ROOT / "relationship-set.schema.json").resolve():
            raise DataValidationError("self-test failed: relationship-set schema path resolution returned the wrong path")

        predicates = load_registered_predicates()
        if "CAN_PRECEDE_IN_PIPELINE" not in predicates:
            raise DataValidationError("self-test failed: registered predicate lookup did not find CAN_PRECEDE_IN_PIPELINE")

        source_record = {
            "identity": {
                "id": "TECHNIQUE-TEST-1",
            },
        }
        target_record = {
            "identity": {
                "id": "TECHNIQUE-TEST-2",
            },
        }
        entity_files = build_entity_file_index(
            [
                (REPOSITORY_ROOT / "data/rag-techniques/source-test.json", source_record),
                (REPOSITORY_ROOT / "data/rag-techniques/target-test.json", target_record),
            ]
        )
        if entity_files["TECHNIQUE-TEST-1"] != "data/rag-techniques/source-test.json":
            raise DataValidationError("self-test failed: entity id to data file mapping returned the wrong path")

        valid_relationship_set = {
            "relationships": [
                {
                    "id": "RELATIONSHIP-TEST-1",
                    "predicate": "CAN_PRECEDE_IN_PIPELINE",
                    "sourceId": "TECHNIQUE-TEST-1",
                    "targetId": "TECHNIQUE-TEST-2",
                    "sourceDataFile": "data/rag-techniques/source-test.json",
                    "targetDataFile": "data/rag-techniques/target-test.json",
                }
            ]
        }
        validate_relationship_semantics(
            [(REPOSITORY_ROOT / "data/relationships/test-relationships.json", valid_relationship_set)],
            predicates,
            entity_files,
        )

        unknown_predicate_set = {
            "relationships": [
                {
                    "id": "RELATIONSHIP-TEST-2",
                    "predicate": "UNREGISTERED_TEST_PREDICATE",
                    "sourceId": "TECHNIQUE-TEST-1",
                    "targetId": "TECHNIQUE-TEST-2",
                    "sourceDataFile": "data/rag-techniques/source-test.json",
                    "targetDataFile": "data/rag-techniques/target-test.json",
                }
            ]
        }
        try:
            validate_relationship_semantics(
                [(REPOSITORY_ROOT / "data/relationships/test-relationships.json", unknown_predicate_set)],
                predicates,
                entity_files,
            )
        except DataValidationError as exc:
            if "is not registered" not in str(exc):
                raise
        else:
            raise DataValidationError("self-test failed: unknown predicate was not rejected")

        source_mismatch_set = {
            "relationships": [
                {
                    "id": "RELATIONSHIP-TEST-3",
                    "predicate": "CAN_PRECEDE_IN_PIPELINE",
                    "sourceId": "TECHNIQUE-TEST-1",
                    "targetId": "TECHNIQUE-TEST-2",
                    "sourceDataFile": "data/rag-techniques/wrong-source-test.json",
                    "targetDataFile": "data/rag-techniques/target-test.json",
                }
            ]
        }
        try:
            validate_relationship_semantics(
                [(REPOSITORY_ROOT / "data/relationships/test-relationships.json", source_mismatch_set)],
                predicates,
                entity_files,
            )
        except DataValidationError as exc:
            if "sourceDataFile points to" not in str(exc):
                raise
        else:
            raise DataValidationError("self-test failed: sourceDataFile mismatch was not rejected")

        duplicate_relationship_id_set = {
            "relationships": [
                {
                    "id": "RELATIONSHIP-TEST-4",
                    "predicate": "CAN_PRECEDE_IN_PIPELINE",
                    "sourceId": "TECHNIQUE-TEST-1",
                    "targetId": "TECHNIQUE-TEST-2",
                    "sourceDataFile": "data/rag-techniques/source-test.json",
                    "targetDataFile": "data/rag-techniques/target-test.json",
                },
                {
                    "id": "RELATIONSHIP-TEST-4",
                    "predicate": "CAN_PROVIDE_CANDIDATES_TO",
                    "sourceId": "TECHNIQUE-TEST-2",
                    "targetId": "TECHNIQUE-TEST-1",
                    "sourceDataFile": "data/rag-techniques/target-test.json",
                    "targetDataFile": "data/rag-techniques/source-test.json",
                },
            ]
        }
        try:
            validate_relationship_semantics(
                [(REPOSITORY_ROOT / "data/relationships/test-relationships.json", duplicate_relationship_id_set)],
                predicates,
                entity_files,
            )
        except DataValidationError as exc:
            if "duplicate relationship id" not in str(exc):
                raise
        else:
            raise DataValidationError("self-test failed: duplicate relationship id was not rejected")

        duplicate_triple_set = {
            "relationships": [
                {
                    "id": "RELATIONSHIP-TEST-5",
                    "predicate": "CAN_PRECEDE_IN_PIPELINE",
                    "sourceId": "TECHNIQUE-TEST-1",
                    "targetId": "TECHNIQUE-TEST-2",
                    "sourceDataFile": "data/rag-techniques/source-test.json",
                    "targetDataFile": "data/rag-techniques/target-test.json",
                },
                {
                    "id": "RELATIONSHIP-TEST-6",
                    "predicate": "CAN_PRECEDE_IN_PIPELINE",
                    "sourceId": "TECHNIQUE-TEST-1",
                    "targetId": "TECHNIQUE-TEST-2",
                    "sourceDataFile": "data/rag-techniques/source-test.json",
                    "targetDataFile": "data/rag-techniques/target-test.json",
                },
            ]
        }
        try:
            validate_relationship_semantics(
                [(REPOSITORY_ROOT / "data/relationships/test-relationships.json", duplicate_triple_set)],
                predicates,
                entity_files,
            )
        except DataValidationError as exc:
            if "duplicate semantic relationship triple" not in str(exc):
                raise
        else:
            raise DataValidationError("self-test failed: duplicate semantic triple was not rejected")


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
        data_count, validation_count, semantic_validation_count = validate_manifest()
    except DataValidationError as exc:
        print(str(exc), file=sys.stderr)
        print("Data validation failed.", file=sys.stderr)
        return 1

    print(
        f"Validated {data_count} data file(s) with {validation_count} schema validation(s) "
        f"and {semantic_validation_count} relationship semantic validation(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
