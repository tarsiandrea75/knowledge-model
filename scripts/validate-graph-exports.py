#!/usr/bin/env python3
"""Validate RKM graph export files against node and edge schemas."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError as JsonSchemaError


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NODE_SCHEMA_PATH = REPOSITORY_ROOT / "schema" / "graph-node.schema.json"
EDGE_SCHEMA_PATH = REPOSITORY_ROOT / "schema" / "graph-edge.schema.json"


@dataclass(frozen=True)
class GraphExport:
    name: str
    nodes_path: Path
    edges_path: Path
    source_fixture_compatibility: bool = False


GRAPH_EXPORTS = (
    GraphExport(
        name="fixture graph export",
        nodes_path=REPOSITORY_ROOT / "examples" / "graph-export" / "minimal-graph.nodes.json",
        edges_path=REPOSITORY_ROOT / "examples" / "graph-export" / "minimal-graph.edges.json",
        source_fixture_compatibility=True,
    ),
    GraphExport(
        name="data graph export",
        nodes_path=REPOSITORY_ROOT / "examples" / "data-graph-export" / "rag-techniques.nodes.json",
        edges_path=REPOSITORY_ROOT / "examples" / "data-graph-export" / "rag-techniques.edges.json",
    ),
)


class GraphExportValidationError(Exception):
    """Raised when graph export validation fails."""


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
        raise GraphExportValidationError(f"{display_path(path)}: file does not exist") from exc
    except json.JSONDecodeError as exc:
        raise GraphExportValidationError(f"{display_path(path)}: invalid JSON: {exc}") from exc


def require_array(value: Any, path: Path) -> list[Any]:
    if not isinstance(value, list):
        raise GraphExportValidationError(f"{display_path(path)}: graph export file must be a JSON array")
    return value


def load_validator(schema_path: Path) -> Draft202012Validator:
    schema = load_json(schema_path)
    if not isinstance(schema, dict):
        raise GraphExportValidationError(f"{display_path(schema_path)}: schema root must be a JSON object")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise GraphExportValidationError(f"{display_path(schema_path)}: invalid schema: {exc.message}") from exc
    return Draft202012Validator(schema)


def validation_instance(item: Any, source_fixture_compatibility: bool) -> Any:
    if (
        source_fixture_compatibility
        and isinstance(item, dict)
        and "sourceDataFile" not in item
        and isinstance(item.get("sourceFixture"), str)
        and item["sourceFixture"]
    ):
        normalized = dict(item)
        normalized["sourceDataFile"] = item["sourceFixture"]
        return normalized
    return item


def schema_error_location(path: Path, index: int, error: JsonSchemaError) -> str:
    location = f"{display_path(path)}[{index}]"
    if error.absolute_path:
        suffix = "/".join(str(part) for part in error.absolute_path)
        location = f"{location}/{suffix}"
    return location


def validate_items(
    items: list[Any],
    path: Path,
    validator: Draft202012Validator,
    item_name: str,
    source_fixture_compatibility: bool,
) -> None:
    for index, item in enumerate(items):
        instance = validation_instance(item, source_fixture_compatibility)
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        if errors:
            error = errors[0]
            location = schema_error_location(path, index, error)
            raise GraphExportValidationError(
                f"{location}: invalid graph {item_name}: {error.message}"
            )


def require_object_item(item: Any, path: Path, index: int, item_name: str) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise GraphExportValidationError(f"{display_path(path)}[{index}]: graph {item_name} must be a JSON object")
    return item


def object_string_field(item: dict[str, Any], field: str, path: Path, index: int, item_name: str) -> str:
    value = item.get(field)
    if not isinstance(value, str) or not value:
        raise GraphExportValidationError(
            f"{display_path(path)}[{index}].{field}: graph {item_name} field must be a non-empty string"
        )
    return value


def unique_ids(items: list[Any], path: Path, item_name: str) -> set[str]:
    seen: set[str] = set()
    for index, item in enumerate(items):
        item_object = require_object_item(item, path, index, item_name)
        item_id = object_string_field(item_object, "id", path, index, item_name)
        if item_id in seen:
            raise GraphExportValidationError(
                f"{display_path(path)}[{index}].id: duplicate graph {item_name} id {item_id!r}"
            )
        seen.add(item_id)
    return seen


def validate_edge_endpoints(edges: list[Any], edges_path: Path, node_ids: set[str]) -> None:
    for index, item in enumerate(edges):
        edge = require_object_item(item, edges_path, index, "edge")
        edge_id = object_string_field(edge, "id", edges_path, index, "edge")
        source_id = object_string_field(edge, "sourceId", edges_path, index, "edge")
        target_id = object_string_field(edge, "targetId", edges_path, index, "edge")
        if source_id not in node_ids:
            raise GraphExportValidationError(
                f"{display_path(edges_path)}[{index}].sourceId: edge {edge_id!r} references missing node {source_id!r}"
            )
        if target_id not in node_ids:
            raise GraphExportValidationError(
                f"{display_path(edges_path)}[{index}].targetId: edge {edge_id!r} references missing node {target_id!r}"
            )


def validate_graph_export(
    export: GraphExport,
    node_validator: Draft202012Validator,
    edge_validator: Draft202012Validator,
) -> tuple[int, int]:
    nodes = require_array(load_json(export.nodes_path), export.nodes_path)
    edges = require_array(load_json(export.edges_path), export.edges_path)

    validate_items(nodes, export.nodes_path, node_validator, "node", export.source_fixture_compatibility)
    validate_items(edges, export.edges_path, edge_validator, "edge", export.source_fixture_compatibility)

    node_ids = unique_ids(nodes, export.nodes_path, "node")
    unique_ids(edges, export.edges_path, "edge")
    validate_edge_endpoints(edges, export.edges_path, node_ids)
    return len(nodes), len(edges)


def validate_all_exports(exports: Sequence[GraphExport] = GRAPH_EXPORTS) -> tuple[int, int, int]:
    node_validator = load_validator(NODE_SCHEMA_PATH)
    edge_validator = load_validator(EDGE_SCHEMA_PATH)
    export_count = 0
    node_count = 0
    edge_count = 0

    for export in exports:
        nodes, edges = validate_graph_export(export, node_validator, edge_validator)
        export_count += 1
        node_count += nodes
        edge_count += edges

    return export_count, node_count, edge_count


def run_self_test() -> None:
    node = {
        "id": "NODE-1",
        "type": "Technique",
        "label": "Node",
        "sourceFixture": "examples/fixtures/minimal-rag-technique.json",
        "properties": {},
    }
    normalized = validation_instance(node, source_fixture_compatibility=True)
    if normalized.get("sourceDataFile") != "examples/fixtures/minimal-rag-technique.json":
        raise GraphExportValidationError("self-test failed: fixture source compatibility did not normalize")

    duplicate_nodes = [
        {"id": "NODE-1"},
        {"id": "NODE-1"},
    ]
    try:
        unique_ids(duplicate_nodes, Path("nodes.json"), "node")
    except GraphExportValidationError as exc:
        if "duplicate graph node id" not in str(exc):
            raise
    else:
        raise GraphExportValidationError("self-test failed: duplicate node ID was accepted")

    edge = {"id": "EDGE-1", "sourceId": "NODE-1", "targetId": "MISSING"}
    try:
        validate_edge_endpoints([edge], Path("edges.json"), {"NODE-1"})
    except GraphExportValidationError as exc:
        if "references missing node" not in str(exc):
            raise
    else:
        raise GraphExportValidationError("self-test failed: missing edge endpoint was accepted")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run lightweight internal tests")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.self_test:
            run_self_test()
            print("validate-graph-exports self-test passed.")
            return 0

        export_count, node_count, edge_count = validate_all_exports()
    except GraphExportValidationError as exc:
        print(str(exc), file=sys.stderr)
        print("Graph export schema validation failed.", file=sys.stderr)
        return 1

    print(
        f"Validated {export_count} graph export(s), {node_count} node(s), and {edge_count} edge(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
