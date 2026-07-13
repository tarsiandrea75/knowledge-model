#!/usr/bin/env python3
"""Export validated RKM seed data as deterministic graph nodes and edges."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPOSITORY_ROOT / "data" / "manifest.json"
GRAPH_EXPORT_DIR = REPOSITORY_ROOT / "examples" / "data-graph-export"
NODES_OUTPUT = GRAPH_EXPORT_DIR / "rag-techniques.nodes.json"
EDGES_OUTPUT = GRAPH_EXPORT_DIR / "rag-techniques.edges.json"
RELATIONSHIP_SET_SCHEMA = "schema/relationship-set.schema.json"
RELATIONSHIP_SUPPORT_SET_SCHEMA = "schema/relationship-support-set.schema.json"


class DataGraphExportError(Exception):
    """Raised when data graph export generation or checking fails."""


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
        raise DataGraphExportError(f"{display_path(path)}: file does not exist") from exc
    except json.JSONDecodeError as exc:
        raise DataGraphExportError(f"{display_path(path)}: invalid JSON: {exc}") from exc


def require_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DataGraphExportError(f"{context} must be a JSON object")
    return value


def require_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise DataGraphExportError(f"{context} must be a JSON array")
    return value


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise DataGraphExportError(f"{context} must be a non-empty string")
    return value


def optional_list(value: Any, context: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise DataGraphExportError(f"{context} must be a JSON array when present")
    return value


def sorted_strings(values: set[str]) -> list[str]:
    return sorted(values)


def compact_object(value: dict[str, Any]) -> dict[str, Any]:
    return {key: value[key] for key in sorted(value) if value[key] is not None}


def node(
    node_id: str,
    node_type: str,
    label: str,
    source_data_file: str,
    properties: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": node_type,
        "label": label,
        "sourceDataFile": source_data_file,
        "properties": compact_object(properties),
    }


def edge(
    edge_id: str,
    predicate: str,
    source_id: str,
    target_id: str,
    source_data_file: str,
    properties: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "predicate": predicate,
        "sourceId": source_id,
        "targetId": target_id,
        "sourceDataFile": source_data_file,
        "properties": compact_object(properties),
    }


def schema_node_id(schema_path: str) -> str:
    stem = Path(schema_path).name.removesuffix(".schema.json")
    stable_part = stem.upper().replace("-", "_")
    return f"SCHEMA-{stable_part}"


def derived_edge_id(source_id: str, predicate: str, target_id: str) -> str:
    return f"EDGE-{source_id}-{predicate}-{target_id}"


def load_manifest() -> list[dict[str, str]]:
    manifest = require_object(load_json(MANIFEST_PATH), display_path(MANIFEST_PATH))
    entries = require_list(manifest.get("data"), "data/manifest.json data")
    loaded_entries: list[dict[str, str]] = []

    for index, item in enumerate(entries):
        entry = require_object(item, f"data/manifest.json data[{index}]")
        data_file = require_string(entry.get("file"), f"data/manifest.json data[{index}].file")
        schema_file = require_string(entry.get("schema"), f"data/manifest.json data[{index}].schema")
        loaded_entries.append({"file": data_file, "schema": schema_file})

    return sorted(loaded_entries, key=lambda item: (item["file"], item["schema"]))


def record_label(record: dict[str, Any], context: str) -> str:
    identity = require_object(record.get("identity"), f"{context} identity")
    name = identity.get("name")
    if isinstance(name, dict):
        for key in ("display", "official"):
            value = name.get(key)
            if isinstance(value, str) and value:
                return value

    for key in ("label", "title", "name"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value

    return require_string(identity.get("id"), f"{context} identity.id")


def record_node(record: dict[str, Any], source_data_file: str, schema_file: str) -> dict[str, Any]:
    context = source_data_file
    identity = require_object(record.get("identity"), f"{context} identity")
    description = require_object(record.get("description"), f"{context} description")
    metadata = require_object(record.get("metadata"), f"{context} metadata")
    technique = require_object(record.get("technique"), f"{context} technique")
    record_id = require_string(identity.get("id"), f"{context} identity.id")

    return node(
        record_id,
        require_string(identity.get("entityType"), f"{context} identity.entityType"),
        record_label(record, context),
        source_data_file,
        {
            "keywords": identity.get("keywords"),
            "language": identity.get("language"),
            "metadataStatus": metadata.get("status"),
            "ragStage": technique.get("ragStage"),
            "reviewState": metadata.get("reviewState"),
            "schema": schema_file,
            "slug": identity.get("slug"),
            "status": identity.get("status"),
            "summary": description.get("summary"),
            "techniqueFamily": technique.get("techniqueFamily"),
            "version": identity.get("version"),
            "visibility": identity.get("visibility"),
        },
    )


def schema_node(schema_file: str) -> dict[str, Any]:
    schema_path = REPOSITORY_ROOT / schema_file
    schema = require_object(load_json(schema_path), schema_file)
    return node(
        schema_node_id(schema_file),
        "Schema",
        schema_file,
        display_path(MANIFEST_PATH),
        {
            "declaredInManifest": display_path(MANIFEST_PATH),
            "schemaId": schema.get("$id"),
            "schemaPath": schema_file,
            "title": schema.get("title"),
        },
    )


def validation_edge(record: dict[str, Any], source_data_file: str, schema_file: str) -> dict[str, Any]:
    identity = require_object(record.get("identity"), f"{source_data_file} identity")
    record_id = require_string(identity.get("id"), f"{source_data_file} identity.id")
    target_id = schema_node_id(schema_file)
    predicate = "VALIDATED_BY_SCHEMA"
    return edge(
        derived_edge_id(record_id, predicate, target_id),
        predicate,
        record_id,
        target_id,
        source_data_file,
        {
            "declaredInManifest": display_path(MANIFEST_PATH),
            "edgeKind": "Export Provenance",
            "schema": schema_file,
        },
    )


def declared_relationship_edges(
    relationship_set: dict[str, Any],
    relationship_set_file: str,
    node_ids: set[str],
    support_by_relationship: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    relationships = require_list(relationship_set.get("relationships"), f"{relationship_set_file} relationships")
    edges: list[dict[str, Any]] = []

    for index, item in enumerate(relationships):
        context = f"{relationship_set_file} relationships[{index}]"
        relationship = require_object(item, context)
        edge_id = require_string(relationship.get("id"), f"{context}.id")
        predicate = require_string(relationship.get("predicate"), f"{context}.predicate")
        source_id = require_string(relationship.get("sourceId"), f"{context}.sourceId")
        target_id = require_string(relationship.get("targetId"), f"{context}.targetId")
        source_data_file = require_string(relationship.get("sourceDataFile"), f"{context}.sourceDataFile")
        target_data_file = require_string(relationship.get("targetDataFile"), f"{context}.targetDataFile")
        relationship_kind = require_string(relationship.get("relationshipKind"), f"{context}.relationshipKind")
        description = require_string(relationship.get("description"), f"{context}.description")
        properties = require_object(relationship.get("properties"), f"{context}.properties")

        if source_id not in node_ids:
            raise DataGraphExportError(
                f"{context}.sourceId references missing data graph node {source_id!r}"
            )
        if target_id not in node_ids:
            raise DataGraphExportError(
                f"{context}.targetId references missing data graph node {target_id!r}"
            )

        edge_properties = dict(properties)
        edge_properties.update(
            {
                "claimIds": support_by_relationship.get(edge_id, {}).get("claimIds"),
                "declaredInRelationshipSet": relationship_set_file,
                "declaredInRelationshipSupportSets": support_by_relationship.get(edge_id, {}).get(
                    "declaredInRelationshipSupportSets"
                ),
                "description": description,
                "evidenceIds": support_by_relationship.get(edge_id, {}).get("evidenceIds"),
                "referenceIds": support_by_relationship.get(edge_id, {}).get("referenceIds"),
                "relationshipKind": relationship_kind,
                "supportSourceTypes": support_by_relationship.get(edge_id, {}).get("supportSourceTypes"),
                "supportStatus": support_by_relationship.get(edge_id, {}).get("supportStatus"),
                "targetDataFile": target_data_file,
            }
        )
        edges.append(
            edge(
                edge_id,
                predicate,
                source_id,
                target_id,
                source_data_file,
                edge_properties,
            )
        )

    return edges


def relationship_support_index(
    support_sets: list[tuple[str, dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    references_by_id: dict[str, dict[str, Any]] = {}
    claims_by_id: dict[str, dict[str, Any]] = {}
    evidence_by_id: dict[str, dict[str, Any]] = {}
    support_files_by_relationship: dict[str, set[str]] = {}
    claim_ids_by_relationship: dict[str, set[str]] = {}
    evidence_ids_by_relationship: dict[str, set[str]] = {}
    reference_ids_by_relationship: dict[str, set[str]] = {}
    source_types_by_relationship: dict[str, set[str]] = {}
    status_by_relationship: dict[str, set[str]] = {}

    for support_file, support_set in support_sets:
        for item in require_list(support_set.get("references"), f"{support_file} references"):
            reference = require_object(item, f"{support_file} references item")
            reference_id = require_string(reference.get("id"), f"{support_file} reference.id")
            references_by_id[reference_id] = reference

        for item in require_list(support_set.get("claims"), f"{support_file} claims"):
            claim = require_object(item, f"{support_file} claims item")
            claim_id = require_string(claim.get("id"), f"{support_file} claim.id")
            claims_by_id[claim_id] = claim

        for item in require_list(support_set.get("evidence"), f"{support_file} evidence"):
            evidence = require_object(item, f"{support_file} evidence item")
            evidence_id = require_string(evidence.get("id"), f"{support_file} evidence.id")
            evidence_by_id[evidence_id] = evidence

    for support_file, support_set in support_sets:
        for item in require_list(support_set.get("claims"), f"{support_file} claims"):
            claim = require_object(item, f"{support_file} claims item")
            claim_id = require_string(claim.get("id"), f"{support_file} claim.id")
            subject = require_object(claim.get("subject"), f"{support_file} claim.subject")
            if subject.get("type") != "Relationship":
                continue

            relationship_id = require_string(subject.get("id"), f"{support_file} claim.subject.id")
            support_files_by_relationship.setdefault(relationship_id, set()).add(support_file)
            claim_ids_by_relationship.setdefault(relationship_id, set()).add(claim_id)
            status = claim.get("status")
            if isinstance(status, str) and status:
                status_by_relationship.setdefault(relationship_id, set()).add(status)

            for reference_id in optional_string_list(claim.get("referenceIds"), f"{support_file} claim.referenceIds"):
                reference_ids_by_relationship.setdefault(relationship_id, set()).add(reference_id)
                source_type = references_by_id.get(reference_id, {}).get("sourceType")
                if isinstance(source_type, str) and source_type:
                    source_types_by_relationship.setdefault(relationship_id, set()).add(source_type)

            for evidence_id in optional_string_list(claim.get("evidenceIds"), f"{support_file} claim.evidenceIds"):
                evidence_ids_by_relationship.setdefault(relationship_id, set()).add(evidence_id)

        for item in require_list(support_set.get("evidence"), f"{support_file} evidence"):
            evidence = require_object(item, f"{support_file} evidence item")
            evidence_id = require_string(evidence.get("id"), f"{support_file} evidence.id")
            relationships = optional_string_list(evidence.get("relationshipIds"), f"{support_file} evidence.relationshipIds")
            claim_ids = optional_string_list(evidence.get("claimIds"), f"{support_file} evidence.claimIds")
            reference_ids = optional_string_list(evidence.get("referenceIds"), f"{support_file} evidence.referenceIds")
            status = evidence.get("status")

            for relationship_id in relationships:
                support_files_by_relationship.setdefault(relationship_id, set()).add(support_file)
                evidence_ids_by_relationship.setdefault(relationship_id, set()).add(evidence_id)
                if isinstance(status, str) and status:
                    status_by_relationship.setdefault(relationship_id, set()).add(status)

                for claim_id in claim_ids:
                    claim_ids_by_relationship.setdefault(relationship_id, set()).add(claim_id)

                for reference_id in reference_ids:
                    reference_ids_by_relationship.setdefault(relationship_id, set()).add(reference_id)
                    source_type = references_by_id.get(reference_id, {}).get("sourceType")
                    if isinstance(source_type, str) and source_type:
                        source_types_by_relationship.setdefault(relationship_id, set()).add(source_type)

    support_by_relationship: dict[str, dict[str, Any]] = {}
    for relationship_id in sorted(support_files_by_relationship):
        support_by_relationship[relationship_id] = {
            "claimIds": sorted_strings(claim_ids_by_relationship.get(relationship_id, set())),
            "declaredInRelationshipSupportSets": sorted_strings(
                support_files_by_relationship.get(relationship_id, set())
            ),
            "evidenceIds": sorted_strings(evidence_ids_by_relationship.get(relationship_id, set())),
            "referenceIds": sorted_strings(reference_ids_by_relationship.get(relationship_id, set())),
            "supportSourceTypes": sorted_strings(source_types_by_relationship.get(relationship_id, set())),
            "supportStatus": sorted_strings(status_by_relationship.get(relationship_id, set())),
        }

    return support_by_relationship


def optional_string_list(value: Any, context: str) -> list[str]:
    values = optional_list(value, context)
    result: list[str] = []
    for index, item in enumerate(values):
        if not isinstance(item, str) or not item:
            raise DataGraphExportError(f"{context}[{index}] must be a non-empty string")
        result.append(item)
    return result


def build_graph() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    manifest_entries = load_manifest()
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    emitted_schema_nodes: dict[str, dict[str, Any]] = {}
    emitted_node_ids: set[str] = set()
    emitted_edge_ids: set[str] = set()

    relationship_set_entries: list[dict[str, str]] = []
    relationship_support_entries: list[dict[str, str]] = []

    for entry in manifest_entries:
        data_file = entry["file"]
        schema_file = entry["schema"]
        if schema_file == RELATIONSHIP_SET_SCHEMA:
            relationship_set_entries.append(entry)
            continue
        if schema_file == RELATIONSHIP_SUPPORT_SET_SCHEMA:
            relationship_support_entries.append(entry)
            continue

        record = require_object(load_json(REPOSITORY_ROOT / data_file), data_file)
        record_graph_node = record_node(record, data_file, schema_file)

        if record_graph_node["id"] in emitted_node_ids:
            raise DataGraphExportError(f"{data_file}: duplicate graph node id {record_graph_node['id']}")
        emitted_node_ids.add(record_graph_node["id"])
        nodes.append(record_graph_node)

        schema_id = schema_node_id(schema_file)
        if schema_id not in emitted_schema_nodes:
            emitted_schema_nodes[schema_id] = schema_node(schema_file)

        candidate = validation_edge(record, data_file, schema_file)
        if candidate["id"] in emitted_edge_ids:
            raise DataGraphExportError(f"{data_file}: duplicate graph edge id {candidate['id']}")
        emitted_edge_ids.add(candidate["id"])
        edges.append(candidate)

    support_sets = [
        (
            entry["file"],
            require_object(load_json(REPOSITORY_ROOT / entry["file"]), entry["file"]),
        )
        for entry in relationship_support_entries
    ]
    support_by_relationship = relationship_support_index(support_sets)
    emitted_relationship_edge_ids: set[str] = set()

    for entry in relationship_set_entries:
        data_file = entry["file"]
        relationship_set = require_object(load_json(REPOSITORY_ROOT / data_file), data_file)
        for candidate in declared_relationship_edges(
            relationship_set,
            data_file,
            emitted_node_ids,
            support_by_relationship,
        ):
            if candidate["id"] in emitted_edge_ids:
                raise DataGraphExportError(f"{data_file}: duplicate graph edge id {candidate['id']}")
            emitted_edge_ids.add(candidate["id"])
            emitted_relationship_edge_ids.add(candidate["id"])
            edges.append(candidate)

    for relationship_id in sorted(support_by_relationship):
        if relationship_id not in emitted_relationship_edge_ids:
            raise DataGraphExportError(
                f"relationship support references relationship {relationship_id!r}, "
                "but that relationship was not exported as a data graph edge"
            )

    nodes.extend(emitted_schema_nodes.values())
    return sorted(nodes, key=lambda item: item["id"]), sorted(edges, key=lambda item: item["id"])


def render_json(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def write_export() -> tuple[int, int]:
    nodes, edges = build_graph()
    GRAPH_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    NODES_OUTPUT.write_text(render_json(nodes), encoding="utf-8")
    EDGES_OUTPUT.write_text(render_json(edges), encoding="utf-8")
    return len(nodes), len(edges)


def compare_file(path: Path, expected: str) -> list[str]:
    try:
        actual = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise DataGraphExportError(f"{display_path(path)}: export file is missing") from exc

    if actual == expected:
        return []

    return list(
        difflib.unified_diff(
            actual.splitlines(),
            expected.splitlines(),
            fromfile=f"{display_path(path)} committed",
            tofile=f"{display_path(path)} generated",
            lineterm="",
        )
    )


def check_export() -> tuple[int, int]:
    nodes, edges = build_graph()
    diffs = []
    diffs.extend(compare_file(NODES_OUTPUT, render_json(nodes)))
    diffs.extend(compare_file(EDGES_OUTPUT, render_json(edges)))
    if diffs:
        raise DataGraphExportError(
            "Data graph export files are not up to date. Run `make data-graph-export`.\n"
            + "\n".join(diffs)
        )
    return len(nodes), len(edges)


def run_self_test() -> None:
    sample_node = node(
        "TECHNIQUE-0001",
        "Technique",
        "Sample Technique",
        "data/rag-techniques/sample-technique.json",
        {"status": "Draft", "empty": None},
    )
    if list(sample_node) != ["id", "type", "label", "sourceDataFile", "properties"]:
        raise DataGraphExportError("self-test failed: node field order changed")
    if sample_node["properties"] != {"status": "Draft"}:
        raise DataGraphExportError("self-test failed: node properties were not compacted")

    if schema_node_id("schema/rag-technique.schema.json") != "SCHEMA-RAG_TECHNIQUE":
        raise DataGraphExportError("self-test failed: schema node ID changed")

    edge_id = derived_edge_id("TECHNIQUE-0001", "VALIDATED_BY_SCHEMA", "SCHEMA-RAG_TECHNIQUE")
    if edge_id != "EDGE-TECHNIQUE-0001-VALIDATED_BY_SCHEMA-SCHEMA-RAG_TECHNIQUE":
        raise DataGraphExportError("self-test failed: derived edge ID changed")

    rendered = render_json([sample_node])
    if not rendered.endswith("\n") or "Sample Technique" not in rendered:
        raise DataGraphExportError("self-test failed: deterministic JSON rendering changed")

    relationship_set = {
        "relationships": [
            {
                "id": "RELATIONSHIP-0001",
                "predicate": "CAN_PRECEDE_IN_PIPELINE",
                "sourceId": "TECHNIQUE-0001",
                "targetId": "TECHNIQUE-0002",
                "sourceDataFile": "data/rag-techniques/sample-technique.json",
                "targetDataFile": "data/rag-techniques/next-technique.json",
                "relationshipKind": "Domain Relationship",
                "description": "Sample relationship for exporter self-test.",
                "properties": {
                    "edgeKind": "Domain Relationship"
                }
            }
        ]
    }
    declared_edges = declared_relationship_edges(
        relationship_set,
        "data/relationships/sample-relationships.json",
        {"TECHNIQUE-0001", "TECHNIQUE-0002"},
        {
            "RELATIONSHIP-0001": {
                "claimIds": ["CLAIM-0001"],
                "declaredInRelationshipSupportSets": [
                    "data/relationship-support/sample-relationship-support.json"
                ],
                "evidenceIds": ["EVIDENCE-0001"],
                "referenceIds": ["REFERENCE-0001"],
                "supportSourceTypes": ["Maintainer Analysis"],
                "supportStatus": ["Draft"],
            }
        },
    )
    if declared_edges[0]["properties"].get("declaredInRelationshipSet") != "data/relationships/sample-relationships.json":
        raise DataGraphExportError("self-test failed: declared relationship provenance was not preserved")
    if declared_edges[0]["properties"].get("claimIds") != ["CLAIM-0001"]:
        raise DataGraphExportError("self-test failed: declared relationship support metadata was not preserved")

    try:
        declared_relationship_edges(
            relationship_set,
            "data/relationships/sample-relationships.json",
            {"TECHNIQUE-0001"},
            {},
        )
    except DataGraphExportError as exc:
        if "references missing data graph node" not in str(exc):
            raise
    else:
        raise DataGraphExportError("self-test failed: missing relationship target node was not rejected")

    support_index = relationship_support_index(
        [
            (
                "data/relationship-support/sample-relationship-support.json",
                {
                    "references": [
                        {
                            "id": "REFERENCE-0001",
                            "sourceType": "Maintainer Analysis",
                        }
                    ],
                    "claims": [
                        {
                            "id": "CLAIM-0001",
                            "subject": {
                                "type": "Relationship",
                                "id": "RELATIONSHIP-0001",
                            },
                            "evidenceIds": ["EVIDENCE-0001"],
                            "referenceIds": ["REFERENCE-0001"],
                            "status": "Draft",
                        }
                    ],
                    "evidence": [
                        {
                            "id": "EVIDENCE-0001",
                            "relationshipIds": ["RELATIONSHIP-0001"],
                            "claimIds": ["CLAIM-0001"],
                            "referenceIds": ["REFERENCE-0001"],
                            "status": "Draft",
                        }
                    ],
                },
            )
        ]
    )
    if support_index["RELATIONSHIP-0001"]["supportSourceTypes"] != ["Maintainer Analysis"]:
        raise DataGraphExportError("self-test failed: relationship support source types were not indexed")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if committed export files differ")
    mode.add_argument("--self-test", action="store_true", help="run lightweight internal tests")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.self_test:
            run_self_test()
            print("export-data-graph self-test passed.")
            return 0
        if args.check:
            node_count, edge_count = check_export()
            print(f"Data graph export check passed for {node_count} node(s) and {edge_count} edge(s).")
            return 0

        node_count, edge_count = write_export()
        print(f"Wrote data graph export with {node_count} node(s) and {edge_count} edge(s).")
        return 0
    except DataGraphExportError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
