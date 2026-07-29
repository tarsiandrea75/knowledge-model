#!/usr/bin/env python3
"""Validate the complete repository package for every populated entity type."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any


GRAPH_NODES_PATH = Path("examples/data-graph-export/rag-techniques.nodes.json")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def kebab_case(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", value).lower()


def repository_path(root: Path, value: str) -> Path:
    return root / value


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    registry_path = root / "registries/entity-type-registry.json"
    manifest_path = root / "data/manifest.json"
    identity_schema_path = root / "schema/definitions/identity.schema.json"
    graph_nodes_path = root / GRAPH_NODES_PATH

    registry = load_json(registry_path)
    manifest = load_json(manifest_path)
    identity_schema = load_json(identity_schema_path)
    graph_nodes = load_json(graph_nodes_path)

    if not isinstance(registry, dict):
        return ["registries/entity-type-registry.json: registry is missing or invalid"]
    if not isinstance(manifest, dict):
        return ["data/manifest.json: manifest is missing or invalid"]
    if not isinstance(identity_schema, dict):
        return ["schema/definitions/identity.schema.json: identity schema is missing or invalid"]
    if not isinstance(graph_nodes, list):
        return [f"{GRAPH_NODES_PATH.as_posix()}: graph node export is missing or invalid"]

    registry_entries = {
        entry.get("type"): entry
        for entry in registry.get("entityTypes", [])
        if isinstance(entry, dict) and isinstance(entry.get("type"), str)
    }
    supported_types = set(identity_schema.get("properties", {}).get("entityType", {}).get("enum", []))
    manifest_entries = manifest.get("data", [])
    populated: dict[str, list[tuple[str, str, str]]] = {}

    for index, entry in enumerate(manifest_entries):
        if not isinstance(entry, dict):
            errors.append(f"data/manifest.json data[{index}]: entry must be an object")
            continue
        data_file = entry.get("file")
        schema_file = entry.get("schema")
        if not isinstance(data_file, str) or not isinstance(schema_file, str):
            errors.append(f"data/manifest.json data[{index}]: file and schema are required strings")
            continue
        path = repository_path(root, data_file)
        record = load_json(path)
        identity = record.get("identity") if isinstance(record, dict) else None
        if identity is None:
            continue
        entity_type = identity.get("entityType") if isinstance(identity, dict) else None
        record_id = identity.get("id") if isinstance(identity, dict) else None
        if not isinstance(entity_type, str) or not isinstance(record_id, str):
            errors.append(f"{data_file}: identity.entityType and identity.id are required")
            continue
        populated.setdefault(entity_type, []).append((data_file, schema_file, record_id))

    nodes_by_type: dict[str, set[str]] = {}
    for node in graph_nodes:
        if isinstance(node, dict) and isinstance(node.get("type"), str) and isinstance(node.get("id"), str):
            nodes_by_type.setdefault(node["type"], set()).add(node["id"])

    for entity_type, records in sorted(populated.items()):
        prefix = f"entity type {entity_type}"
        registry_entry = registry_entries.get(entity_type)
        if registry_entry is None:
            errors.append(f"{prefix}: missing registries/entity-type-registry.json entry")
            continue

        directory = registry_entry.get("directory")
        schema_file = registry_entry.get("schema")
        if not isinstance(directory, str) or not directory:
            errors.append(f"{prefix}: registry directory is missing")
        else:
            storage_directories = {str(Path(data_file).parent) for data_file, _, _ in records}
            if any(not path.startswith("data/") for path in storage_directories):
                errors.append(f"{prefix}: populated records must be stored below data/")
            if len(storage_directories) > 1:
                errors.append(
                    f"{prefix}: populated records span multiple storage directories: "
                    f"{', '.join(sorted(storage_directories))}"
                )

        if not isinstance(schema_file, str) or not schema_file:
            errors.append(f"{prefix}: registry schema is missing")
        else:
            if not (root / schema_file).is_file():
                errors.append(f"{prefix}: declared schema is missing: {schema_file}")
            for data_file, declared_schema, _ in records:
                if declared_schema != schema_file:
                    errors.append(
                        f"{prefix}: manifest schema mismatch for {data_file}: "
                        f"expected {schema_file}, found {declared_schema}"
                    )

        if entity_type not in supported_types:
            errors.append(f"{prefix}: identity schema does not support entityType {entity_type}")

        schema_stem = Path(schema_file).name.removesuffix(".schema.json") if isinstance(schema_file, str) else kebab_case(entity_type)
        documentation = root / "docs/architecture" / f"{schema_stem}-model.md"
        if not documentation.is_file():
            errors.append(f"{prefix}: architecture documentation is missing: {documentation.relative_to(root)}")

        graph_ids = nodes_by_type.get(entity_type, set())
        for _, _, record_id in records:
            if record_id not in graph_ids:
                errors.append(f"{prefix}: graph export is missing node for {record_id}")

    return errors


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-entity-package-") as temporary:
        root = Path(temporary)
        registry = {"entityTypes": [{"type": "Widget", "directory": "widgets/", "schema": "schema/widget.schema.json"}]}
        identity_schema = {"properties": {"entityType": {"enum": ["Widget"]}}}
        manifest = {"data": [{"file": "data/widgets/example.json", "schema": "schema/widget.schema.json"}]}
        record = {"identity": {"entityType": "Widget", "id": "WIDGET-0001"}}
        nodes = [{"type": "Widget", "id": "WIDGET-0001"}]
        _write_json(root / "registries/entity-type-registry.json", registry)
        _write_json(root / "schema/definitions/identity.schema.json", identity_schema)
        _write_json(root / "data/manifest.json", manifest)
        _write_json(root / "data/widgets/example.json", record)
        _write_json(root / "schema/widget.schema.json", {})
        _write_json(root / GRAPH_NODES_PATH, nodes)
        (root / "docs/architecture").mkdir(parents=True)
        (root / "docs/architecture/widget-model.md").write_text("# Widget\n", encoding="utf-8")

        assert validate(root) == []

        registry["entityTypes"] = []
        _write_json(root / "registries/entity-type-registry.json", registry)
        assert any("missing registries/entity-type-registry.json entry" in error for error in validate(root))
        registry["entityTypes"] = [{"type": "Widget", "directory": "widgets/", "schema": "schema/other.schema.json"}]
        _write_json(root / "registries/entity-type-registry.json", registry)
        assert any("manifest schema mismatch" in error for error in validate(root))
        registry["entityTypes"][0]["schema"] = "schema/widget.schema.json"
        _write_json(root / "registries/entity-type-registry.json", registry)
        (root / "docs/architecture/widget-model.md").unlink()
        assert any("architecture documentation is missing" in error for error in validate(root))
        (root / "docs/architecture/widget-model.md").write_text("# Widget\n", encoding="utf-8")
        _write_json(root / GRAPH_NODES_PATH, [])
        assert any("graph export is missing node" in error for error in validate(root))

    print("entity type package validator self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run deterministic validator self-tests")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0

    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("Entity type package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("entity type package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
