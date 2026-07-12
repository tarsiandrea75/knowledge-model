#!/usr/bin/env python3
"""Validate prerequisites for specialized RKM entity schemas."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path


SHARED_INFRASTRUCTURE_STEMS = {
    "claim",
    "description",
    "entity-type",
    "evidence",
    "identity",
    "knowledge-entity",
    "metadata",
    "reference",
    "relationship",
    "relationship-type",
}

REGISTRY_SCHEMA_STEMS = {
    "entity-type-registry",
    "ontology",
    "relationship-type-registry",
}

RELATIONSHIP_PROPERTY_NAMES = {
    "relationship",
    "relationships",
    "relatedEntities",
    "relatedEntity",
}


class ValidationError:
    def __init__(self, path: Path, entity_type: str, missing: str, guidance: str) -> None:
        self.path = path
        self.entity_type = entity_type
        self.missing = missing
        self.guidance = guidance

    def format(self, repo_root: Path) -> str:
        try:
            display_path = self.path.relative_to(repo_root)
        except ValueError:
            display_path = self.path
        return (
            f"{display_path}: entity type {self.entity_type!r} is missing prerequisite "
            f"{self.missing}. {self.guidance}"
        )


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def repository_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def canonical_entity_types(repo_root: Path) -> set[str]:
    identity_schema = load_json(repo_root / "schema" / "definitions" / "identity.schema.json")
    if not isinstance(identity_schema, dict):
        return set()
    entity_type = (
        identity_schema.get("properties", {})
        .get("entityType", {})
        .get("enum", [])
    )
    return set(entity_type) if isinstance(entity_type, list) else set()


def registered_entity_types(repo_root: Path) -> set[str]:
    registry = load_json(repo_root / "registries" / "entity-type-registry.json")
    if not isinstance(registry, dict):
        return set()
    values = set()
    for item in registry.get("entityTypes", []):
        if isinstance(item, dict) and isinstance(item.get("type"), str):
            values.add(item["type"])
    return values


def relationship_registry_entity_types(repo_root: Path) -> set[str] | None:
    registry_path = repo_root / "registries" / "relationship-type-registry.json"
    if not registry_path.exists():
        return None
    registry = load_json(registry_path)
    if not isinstance(registry, dict):
        return None

    values = set()
    has_vocabulary = False
    for relationship_type in registry.get("relationshipTypes", []):
        if not isinstance(relationship_type, dict):
            continue
        for key in ("allowedSources", "allowedTargets"):
            constraints = relationship_type.get(key)
            if not isinstance(constraints, list):
                continue
            has_vocabulary = True
            for constraint in constraints:
                if isinstance(constraint, dict) and isinstance(constraint.get("entityType"), str):
                    values.add(constraint["entityType"])
    return values if has_vocabulary else None


def iter_schema_files(repo_root: Path) -> list[Path]:
    return sorted((repo_root / "schema").glob("**/*.schema.json"))


def path_to_entity_type_candidate(path: Path) -> str:
    stem = path.name.removesuffix(".schema.json")
    return "".join(part.capitalize() for part in stem.split("-") if part)


def title_to_entity_type_candidates(schema: dict[str, object]) -> set[str]:
    title = schema.get("title")
    if not isinstance(title, str):
        return set()

    cleaned = title
    cleaned = re.sub(r"\bRKM\b", "", cleaned)
    cleaned = re.sub(r"\bSchema\b", "", cleaned)
    cleaned = re.sub(r"\bDefinition\b", "", cleaned)
    words = re.findall(r"[A-Za-z0-9]+", cleaned)
    if not words:
        return set()
    return {"".join(word[:1].upper() + word[1:] for word in words)}


def id_to_entity_type_candidates(schema: dict[str, object]) -> set[str]:
    schema_id = schema.get("$id")
    if not isinstance(schema_id, str):
        return set()
    last = schema_id.rstrip("/").split("/")[-1]
    if not last.endswith(".schema.json"):
        return set()
    return {path_to_entity_type_candidate(Path(last))}


def root_identity_schema(schema: dict[str, object]) -> object | None:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return None
    return properties.get("identity")


def find_entity_type_consts(node: object, *, within_identity: bool = False) -> set[str]:
    values = set()
    if isinstance(node, dict):
        if within_identity:
            entity_type = node.get("entityType")
            if isinstance(entity_type, dict) and isinstance(entity_type.get("const"), str):
                values.add(entity_type["const"])
            if node.get("const") and isinstance(node.get("const"), str):
                values.add(node["const"])
        for key, value in node.items():
            values.update(find_entity_type_consts(value, within_identity=within_identity or key == "identity"))
    elif isinstance(node, list):
        for item in node:
            values.update(find_entity_type_consts(item, within_identity=within_identity))
    return values


def explicit_root_entity_type(schema: dict[str, object]) -> str | None:
    identity_schema = root_identity_schema(schema)
    if identity_schema is None:
        return None
    values = sorted(find_entity_type_consts(identity_schema, within_identity=True))
    return values[0] if values else None


def is_shared_infrastructure(path: Path) -> bool:
    stem = path.name.removesuffix(".schema.json")
    return (
        path.parent.name == "definitions"
        and stem in SHARED_INFRASTRUCTURE_STEMS
    ) or stem in REGISTRY_SCHEMA_STEMS


def infer_specialized_entity_type(
    path: Path,
    schema: dict[str, object],
    known_entity_types: set[str],
) -> str | None:
    explicit = explicit_root_entity_type(schema)
    if explicit:
        return explicit

    if is_shared_infrastructure(path):
        return None

    candidates = {path_to_entity_type_candidate(path)}
    candidates.update(title_to_entity_type_candidates(schema))
    candidates.update(id_to_entity_type_candidates(schema))
    matches = sorted(candidate for candidate in candidates if candidate in known_entity_types)
    if matches:
        return matches[0]
    return None


def schema_has_relationship_bearing_structure(schema: dict[str, object]) -> bool:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return False
    for name, value in properties.items():
        if name in RELATIONSHIP_PROPERTY_NAMES:
            return True
        if not isinstance(value, dict):
            continue
        ref = value.get("$ref")
        if isinstance(ref, str) and "relationship.schema.json" in ref:
            return True
        items = value.get("items")
        if isinstance(items, dict):
            item_ref = items.get("$ref")
            if isinstance(item_ref, str) and "relationship.schema.json" in item_ref:
                return True
    return False


def validate_repo(repo_root: Path) -> list[ValidationError]:
    identity_types = canonical_entity_types(repo_root)
    registry_types = registered_entity_types(repo_root)
    known_types = identity_types | registry_types
    relationship_types = relationship_registry_entity_types(repo_root)
    errors = []

    for schema_path in iter_schema_files(repo_root):
        loaded = load_json(schema_path)
        if not isinstance(loaded, dict):
            continue
        entity_type = infer_specialized_entity_type(schema_path, loaded, known_types)
        if not entity_type:
            continue
        if entity_type not in identity_types:
            errors.append(
                ValidationError(
                    schema_path,
                    entity_type,
                    "schema/definitions/identity.schema.json entityType enum",
                    "Add the shared identity entity type before introducing the specialized schema.",
                )
            )
        if entity_type not in registry_types:
            errors.append(
                ValidationError(
                    schema_path,
                    entity_type,
                    "registries/entity-type-registry.json entityTypes",
                    "Register the entity type before introducing the specialized schema.",
                )
            )
        relationship_supported = (
            relationship_types is None
            or entity_type in relationship_types
            or "Artifact" in relationship_types
        )
        if schema_has_relationship_bearing_structure(loaded) and not relationship_supported:
            errors.append(
                ValidationError(
                    schema_path,
                    entity_type,
                    "relationship registry entity-type vocabulary",
                    "Add relationship registry support for this entity type or remove root relationship-bearing structures.",
                )
            )
    return errors


def print_validation_result(repo_root: Path, errors: list[ValidationError]) -> int:
    if errors:
        print("Schema prerequisite validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error.format(repo_root)}", file=sys.stderr)
        return 1
    print("Schema prerequisite validation passed.")
    return 0


def minimal_identity_schema(entity_types: list[str]) -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://rkm.org/schema/definitions/identity.schema.json",
        "type": "object",
        "properties": {
            "entityType": {
                "type": "string",
                "enum": entity_types,
            }
        },
    }


def minimal_entity_type_registry(entity_types: list[str]) -> dict[str, object]:
    return {
        "entityTypes": [
            {
                "type": entity_type,
            }
            for entity_type in entity_types
        ]
    }


def widget_schema() -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://rkm.org/schema/definitions/widget.schema.json",
        "title": "RKM Widget Schema",
        "type": "object",
        "properties": {
            "identity": {
                "allOf": [
                    {"$ref": "identity.schema.json"},
                    {
                        "type": "object",
                        "properties": {
                            "entityType": {
                                "const": "Widget",
                            }
                        },
                    },
                ]
            }
        },
    }


def shared_infrastructure_schema() -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://rkm.org/schema/definitions/metadata.schema.json",
        "title": "RKM Metadata Definition",
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
            }
        },
    }


def prepare_synthetic_repo(
    root: Path,
    *,
    identity_types: list[str],
    registry_types: list[str],
    include_widget_schema: bool = True,
    include_shared_schema: bool = False,
) -> None:
    write_json(root / "schema" / "definitions" / "identity.schema.json", minimal_identity_schema(identity_types))
    write_json(root / "registries" / "entity-type-registry.json", minimal_entity_type_registry(registry_types))
    if include_widget_schema:
        write_json(root / "schema" / "definitions" / "widget.schema.json", widget_schema())
    if include_shared_schema:
        write_json(root / "schema" / "definitions" / "metadata.schema.json", shared_infrastructure_schema())


def assert_error_contains(errors: list[ValidationError], missing: str) -> None:
    if not any(missing in error.missing for error in errors):
        formatted = [error.missing for error in errors]
        raise AssertionError(f"Expected missing prerequisite containing {missing!r}; got {formatted!r}")


def run_self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="rkm-schema-prereq-") as tmp:
        root = Path(tmp) / "missing-both"
        prepare_synthetic_repo(root, identity_types=[], registry_types=[])
        errors = validate_repo(root)
        assert_error_contains(errors, "identity.schema.json")
        assert_error_contains(errors, "entity-type-registry.json")

    with tempfile.TemporaryDirectory(prefix="rkm-schema-prereq-") as tmp:
        root = Path(tmp) / "missing-registry"
        prepare_synthetic_repo(root, identity_types=["Widget"], registry_types=[])
        errors = validate_repo(root)
        if any("identity.schema.json" in error.missing for error in errors):
            raise AssertionError("Widget present in identity should not fail the identity prerequisite")
        assert_error_contains(errors, "entity-type-registry.json")

    with tempfile.TemporaryDirectory(prefix="rkm-schema-prereq-") as tmp:
        root = Path(tmp) / "passing"
        prepare_synthetic_repo(root, identity_types=["Widget"], registry_types=["Widget"])
        errors = validate_repo(root)
        if errors:
            raise AssertionError(f"Expected no errors when Widget prerequisites are aligned; got {errors!r}")

    with tempfile.TemporaryDirectory(prefix="rkm-schema-prereq-") as tmp:
        root = Path(tmp) / "shared-infra"
        prepare_synthetic_repo(
            root,
            identity_types=["Widget"],
            registry_types=["Widget"],
            include_widget_schema=False,
            include_shared_schema=True,
        )
        errors = validate_repo(root)
        if errors:
            raise AssertionError(f"Expected shared infrastructure schema to be ignored; got {errors!r}")

    print("Schema prerequisite self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run synthetic self-tests")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    repo_root = repository_root_from_script()
    errors = validate_repo(repo_root)
    return print_validation_result(repo_root, errors)


if __name__ == "__main__":
    raise SystemExit(main())
