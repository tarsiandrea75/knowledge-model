#!/usr/bin/env python3
"""Export minimal RKM fixtures as deterministic graph nodes and edges."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPOSITORY_ROOT / "examples" / "fixtures"
GRAPH_EXPORT_DIR = REPOSITORY_ROOT / "examples" / "graph-export"

TECHNIQUE_FIXTURE = FIXTURE_DIR / "minimal-rag-technique.json"
RELATIONSHIP_FIXTURE = FIXTURE_DIR / "minimal-relationship.json"
CLAIM_FIXTURE = FIXTURE_DIR / "minimal-claim-with-evidence.json"
NODES_OUTPUT = GRAPH_EXPORT_DIR / "minimal-graph.nodes.json"
EDGES_OUTPUT = GRAPH_EXPORT_DIR / "minimal-graph.edges.json"


class GraphExportError(Exception):
    """Raised when graph export generation or checking fails."""


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
        raise GraphExportError(f"{display_path(path)}: file does not exist") from exc
    except json.JSONDecodeError as exc:
        raise GraphExportError(f"{display_path(path)}: invalid JSON: {exc}") from exc


def require_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GraphExportError(f"{context} must be a JSON object")
    return value


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise GraphExportError(f"{context} must be a non-empty string")
    return value


def optional_list(value: Any, context: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise GraphExportError(f"{context} must be a JSON array")
    return value


def source_fixture(path: Path) -> str:
    return display_path(path)


def compact_object(value: dict[str, Any]) -> dict[str, Any]:
    return {key: value[key] for key in sorted(value) if value[key] is not None}


def node(
    node_id: str,
    node_type: str,
    label: str,
    fixture_path: Path,
    properties: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": node_type,
        "label": label,
        "sourceFixture": source_fixture(fixture_path),
        "properties": compact_object(properties),
    }


def edge(
    edge_id: str,
    predicate: str,
    source_id: str,
    target_id: str,
    fixture_path: Path,
    properties: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": edge_id,
        "predicate": predicate,
        "sourceId": source_id,
        "targetId": target_id,
        "sourceFixture": source_fixture(fixture_path),
        "properties": compact_object(properties),
    }


def derived_edge_id(source_id: str, predicate: str, target_id: str) -> str:
    return f"EDGE-{source_id}-{predicate}-{target_id}"


def technique_node(technique: dict[str, Any]) -> dict[str, Any]:
    identity = require_object(technique.get("identity"), "technique.identity")
    description = require_object(technique.get("description"), "technique.description")
    details = require_object(technique.get("technique"), "technique.technique")
    name = require_object(identity.get("name"), "technique.identity.name")

    return node(
        require_string(identity.get("id"), "technique.identity.id"),
        require_string(identity.get("entityType"), "technique.identity.entityType"),
        require_string(name.get("display"), "technique.identity.name.display"),
        TECHNIQUE_FIXTURE,
        {
            "slug": identity.get("slug"),
            "status": identity.get("status"),
            "summary": description.get("summary"),
            "techniqueFamily": details.get("techniqueFamily"),
            "ragStage": details.get("ragStage"),
        },
    )


def component_endpoint_node(relationship: dict[str, Any]) -> dict[str, Any]:
    target_id = require_string(relationship.get("targetId"), "relationship.targetId")
    target_type = require_string(relationship.get("targetType"), "relationship.targetType")
    target_slug = require_string(relationship.get("targetSlug"), "relationship.targetSlug")
    return node(
        target_id,
        target_type,
        target_slug,
        RELATIONSHIP_FIXTURE,
        {
            "slug": target_slug,
            "status": "Referenced Endpoint",
            "introducedByRelationship": relationship.get("id"),
        },
    )


def claim_node(claim: dict[str, Any]) -> dict[str, Any]:
    subject = require_object(claim.get("subject"), "claim.subject")
    claim_object = require_object(claim.get("object"), "claim.object")
    return node(
        require_string(claim.get("id"), "claim.id"),
        "Claim",
        require_string(claim.get("statement"), "claim.statement"),
        CLAIM_FIXTURE,
        {
            "claimType": claim.get("claimType"),
            "confidence": claim.get("confidence"),
            "status": claim.get("status"),
            "subjectId": subject.get("id"),
            "subjectType": subject.get("type"),
            "predicate": claim.get("predicate"),
            "objectId": claim_object.get("id"),
            "objectValue": claim_object.get("value"),
        },
    )


def evidence_node(evidence: dict[str, Any]) -> dict[str, Any]:
    return node(
        require_string(evidence.get("id"), "evidence.id"),
        "Evidence",
        require_string(evidence.get("summary"), "evidence.summary"),
        CLAIM_FIXTURE,
        {
            "role": evidence.get("role"),
            "strength": evidence.get("strength"),
            "confidence": evidence.get("confidence"),
            "status": evidence.get("status"),
            "sourceFragments": evidence.get("sourceFragments"),
        },
    )


def reference_node(reference: dict[str, Any]) -> dict[str, Any]:
    return node(
        require_string(reference.get("id"), "reference.id"),
        "Reference",
        require_string(reference.get("title"), "reference.title"),
        CLAIM_FIXTURE,
        {
            "sourceType": reference.get("sourceType"),
            "sourcePriority": reference.get("sourcePriority"),
            "publisher": reference.get("publisher"),
            "accessedAt": reference.get("accessedAt"),
            "url": reference.get("url"),
            "citation": reference.get("citation"),
            "abstract": reference.get("abstract"),
        },
    )


def relationship_edge(relationship: dict[str, Any]) -> dict[str, Any]:
    return edge(
        require_string(relationship.get("id"), "relationship.id"),
        require_string(relationship.get("type"), "relationship.type"),
        require_string(relationship.get("sourceId"), "relationship.sourceId"),
        require_string(relationship.get("targetId"), "relationship.targetId"),
        RELATIONSHIP_FIXTURE,
        {
            "confidence": relationship.get("confidence"),
            "certainty": relationship.get("certainty"),
            "status": relationship.get("status"),
            "sourceType": relationship.get("sourceType"),
            "targetType": relationship.get("targetType"),
            "rationale": relationship.get("rationale"),
        },
    )


def claim_subject_edge(claim: dict[str, Any]) -> dict[str, Any]:
    subject = require_object(claim.get("subject"), "claim.subject")
    source_id = require_string(subject.get("id"), "claim.subject.id")
    target_id = require_string(claim.get("id"), "claim.id")
    predicate = require_string(claim.get("predicate"), "claim.predicate")
    claim_object = require_object(claim.get("object"), "claim.object")
    return edge(
        derived_edge_id(source_id, predicate, target_id),
        predicate,
        source_id,
        target_id,
        CLAIM_FIXTURE,
        {
            "claimType": claim.get("claimType"),
            "confidence": claim.get("confidence"),
            "objectValue": claim_object.get("value"),
            "statement": claim.get("statement"),
        },
    )


def evidence_support_edges(claim: dict[str, Any]) -> list[dict[str, Any]]:
    claim_id = require_string(claim.get("id"), "claim.id")
    edges = []
    for evidence_id in optional_list(claim.get("evidenceIds"), "claim.evidenceIds"):
        evidence_id = require_string(evidence_id, "claim.evidenceIds item")
        edges.append(
            edge(
                derived_edge_id(evidence_id, "SUPPORTS", claim_id),
                "SUPPORTS",
                evidence_id,
                claim_id,
                CLAIM_FIXTURE,
                {"linkSource": "claim.evidenceIds"},
            )
        )
    return edges


def evidence_reference_edges(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    evidence_id = require_string(evidence.get("id"), "evidence.id")
    edges = []
    for reference_id in optional_list(evidence.get("referenceIds"), "evidence.referenceIds"):
        reference_id = require_string(reference_id, "evidence.referenceIds item")
        edges.append(
            edge(
                derived_edge_id(evidence_id, "REFERENCES", reference_id),
                "REFERENCES",
                evidence_id,
                reference_id,
                CLAIM_FIXTURE,
                {"linkSource": "evidence.referenceIds"},
            )
        )
    return edges


def claim_reference_edges(claim: dict[str, Any]) -> list[dict[str, Any]]:
    claim_id = require_string(claim.get("id"), "claim.id")
    edges = []
    for reference_id in optional_list(claim.get("referenceIds"), "claim.referenceIds"):
        reference_id = require_string(reference_id, "claim.referenceIds item")
        edges.append(
            edge(
                derived_edge_id(claim_id, "CITES", reference_id),
                "CITES",
                claim_id,
                reference_id,
                CLAIM_FIXTURE,
                {"linkSource": "claim.referenceIds"},
            )
        )
    return edges


def build_graph() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    technique = require_object(load_json(TECHNIQUE_FIXTURE), display_path(TECHNIQUE_FIXTURE))
    relationship = require_object(load_json(RELATIONSHIP_FIXTURE), display_path(RELATIONSHIP_FIXTURE))
    claim_package = require_object(load_json(CLAIM_FIXTURE), display_path(CLAIM_FIXTURE))
    claim = require_object(claim_package.get("claim"), "claim package claim")
    evidence = require_object(claim_package.get("evidence"), "claim package evidence")
    reference = require_object(claim_package.get("reference"), "claim package reference")

    nodes = [
        technique_node(technique),
        component_endpoint_node(relationship),
        claim_node(claim),
        evidence_node(evidence),
        reference_node(reference),
    ]
    edges = [
        relationship_edge(relationship),
        claim_subject_edge(claim),
        *evidence_support_edges(claim),
        *evidence_reference_edges(evidence),
        *claim_reference_edges(claim),
    ]

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
        raise GraphExportError(f"{display_path(path)}: export file is missing") from exc

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
        raise GraphExportError(
            "Graph export files are not up to date. Run `make graph-export`.\n"
            + "\n".join(diffs)
        )
    return len(nodes), len(edges)


def run_self_test() -> None:
    sample_node = node(
        "TECHNIQUE-0001",
        "Technique",
        "Sample Technique",
        TECHNIQUE_FIXTURE,
        {"status": "Draft", "empty": None},
    )
    if list(sample_node) != ["id", "type", "label", "sourceFixture", "properties"]:
        raise GraphExportError("self-test failed: node field order changed")
    if sample_node["properties"] != {"status": "Draft"}:
        raise GraphExportError("self-test failed: node properties were not compacted")

    edge_id = derived_edge_id("TECHNIQUE-0001", "DEPENDS_ON", "COMPONENT-0001")
    if edge_id != "EDGE-TECHNIQUE-0001-DEPENDS_ON-COMPONENT-0001":
        raise GraphExportError("self-test failed: derived edge ID changed")

    rendered = render_json([sample_node])
    if not rendered.endswith("\n") or "Sample Technique" not in rendered:
        raise GraphExportError("self-test failed: deterministic JSON rendering changed")


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
            print("export-fixtures-graph self-test passed.")
            return 0
        if args.check:
            node_count, edge_count = check_export()
            print(f"Graph export check passed for {node_count} node(s) and {edge_count} edge(s).")
            return 0

        node_count, edge_count = write_export()
        print(f"Wrote graph export with {node_count} node(s) and {edge_count} edge(s).")
        return 0
    except GraphExportError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
