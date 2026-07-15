#!/usr/bin/env python3
"""Render source-linked entity and pipeline decision views from canonical RKM data."""

from __future__ import annotations

import argparse
import contextlib
import copy
import io
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class DecisionQueryError(Exception):
    """Raised when discovery, lookup, or embedded knowledge is invalid."""


def _load_json(path: Path, description: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise DecisionQueryError(f"Could not read {description} at {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise DecisionQueryError(
            f"Malformed JSON in {description} at {path}: line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc


def _require_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DecisionQueryError(f"Malformed {context}: expected a JSON object.")
    return value


def _require_list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        raise DecisionQueryError(f"Malformed {context}: expected a JSON array.")
    return value


def _require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DecisionQueryError(f"Malformed {context}: expected a non-empty string.")
    return value


def _string_list(value: Any, context: str) -> list[str]:
    items = _require_list(value, context)
    result: list[str] = []
    for index, item in enumerate(items):
        result.append(_require_string(item, f"{context}[{index}]"))
    return result


def _require_item_strings(item: dict[str, Any], fields: Iterable[str], context: str) -> None:
    for field in fields:
        _require_string(item.get(field), f"{context}.{field}")


def _safe_manifest_path(root: Path, relative_path: str, index: int) -> Path:
    path = (root / relative_path).resolve()
    data_root = (root / "data").resolve()
    if path != data_root and data_root not in path.parents:
        raise DecisionQueryError(
            f"Malformed manifest entry {index}: file must resolve below data/: {relative_path}"
        )
    return path


def _validate_identity(record: dict[str, Any], source: Path) -> dict[str, Any]:
    identity = _require_object(record.get("identity"), f"entity identity in {source}")
    _require_string(identity.get("id"), f"identity.id in {source}")
    _require_string(identity.get("slug"), f"identity.slug in {source}")
    name = _require_object(identity.get("name"), f"identity.name in {source}")
    official = name.get("official")
    display = name.get("display")
    if not any(isinstance(value, str) and value.strip() for value in (official, display)):
        raise DecisionQueryError(
            f"Malformed identity.name in {source}: an official or display name is required."
        )
    for field, value in (("official", official), ("display", display)):
        if value is not None:
            _require_string(value, f"identity.name.{field} in {source}")
    if identity.get("status") is not None:
        _require_string(identity["status"], f"identity.status in {source}")
    return identity


def discover_entities(root: Path = REPOSITORY_ROOT) -> list[tuple[Path, dict[str, Any]]]:
    """Load manifest documents and return only records with an identity object."""
    manifest_path = root / "data" / "manifest.json"
    manifest = _require_object(_load_json(manifest_path, "data manifest"), "data manifest")
    entries = _require_list(manifest.get("data"), "data manifest field 'data'")
    entities: list[tuple[Path, dict[str, Any]]] = []
    for index, raw_entry in enumerate(entries):
        entry = _require_object(raw_entry, f"manifest entry {index}")
        relative_path = _require_string(entry.get("file"), f"manifest entry {index} field 'file'")
        path = _safe_manifest_path(root, relative_path, index)
        document = _require_object(
            _load_json(path, f"manifest document for entry {index}"),
            f"manifest document {relative_path}",
        )
        if "identity" not in document:
            continue
        _validate_identity(document, path)
        entities.append((path, document))
    return entities


def resolve_entity(
    query: str, entities: Sequence[tuple[Path, dict[str, Any]]]
) -> tuple[Path, dict[str, Any]]:
    """Resolve an exact ID/slug or case-insensitive exact official/display name."""
    requested = _require_string(query, "entity lookup value")
    folded = requested.casefold()
    matches: list[tuple[Path, dict[str, Any]]] = []
    for path, record in entities:
        identity = _validate_identity(record, path)
        name = _require_object(identity["name"], f"identity.name in {path}")
        exact_match = requested in (identity["id"], identity["slug"])
        name_match = any(
            isinstance(value, str) and value.casefold() == folded
            for value in (name.get("display"), name.get("official"))
        )
        if exact_match or name_match:
            matches.append((path, record))

    if not matches:
        raise DecisionQueryError(
            f"No canonical RKM entity matches {requested!r}. "
            "Use an exact stable ID, exact slug, or exact display/official name."
        )
    if len(matches) > 1:
        details = ", ".join(
            f"{record['identity']['id']} ({path.relative_to(path.parents[2])})"
            for path, record in matches
        )
        raise DecisionQueryError(
            f"Entity lookup {requested!r} is ambiguous; matched {len(matches)} records: {details}"
        )
    return matches[0]


def _embedded_items(record: dict[str, Any], field: str, source: Path) -> list[dict[str, Any]]:
    raw_items = record.get(field, [])
    items = _require_list(raw_items, f"{field} in {source}")
    result: list[dict[str, Any]] = []
    for index, raw_item in enumerate(items):
        item = _require_object(raw_item, f"{field}[{index}] in {source}")
        _require_string(item.get("id"), f"{field}[{index}].id in {source}")
        result.append(item)
    return result


def _index_by_id(items: Sequence[dict[str, Any]], label: str, source: Path) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for item in items:
        stable_id = item["id"]
        if stable_id in index:
            raise DecisionQueryError(f"Duplicate {label} ID {stable_id!r} in {source}.")
        index[stable_id] = item
    return index


def _validate_qualifiers(claim: dict[str, Any], source: Path) -> None:
    qualifiers = _require_list(
        claim.get("qualifiers", []), f"Claim {claim['id']} qualifiers in {source}"
    )
    for index, raw_qualifier in enumerate(qualifiers):
        qualifier = _require_object(
            raw_qualifier, f"Claim {claim['id']} qualifier {index} in {source}"
        )
        _require_string(
            qualifier.get("name"), f"Claim {claim['id']} qualifier {index} name in {source}"
        )
        if "value" not in qualifier:
            raise DecisionQueryError(
                f"Malformed Claim {claim['id']} qualifier {index} in {source}: missing value."
            )


def validate_embedded_knowledge(
    record: dict[str, Any], source: Path
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """Validate embedded IDs, link resolution, and Claim/Evidence reciprocity."""
    identity = _validate_identity(record, source)
    references = _index_by_id(_embedded_items(record, "references", source), "Reference", source)
    claims = _index_by_id(_embedded_items(record, "claims", source), "Claim", source)
    evidence = _index_by_id(_embedded_items(record, "evidence", source), "Evidence", source)

    for claim_id, claim in claims.items():
        _require_item_strings(
            claim,
            ("statement", "claimType", "confidence", "status"),
            f"Claim {claim_id} in {source}",
        )
        if claim.get("rationale") is not None:
            _require_string(claim["rationale"], f"Claim {claim_id} rationale in {source}")
        subject = _require_object(claim.get("subject"), f"Claim {claim_id} subject in {source}")
        if subject.get("id") != identity["id"]:
            raise DecisionQueryError(
                f"Claim {claim_id} subject ID {subject.get('id')!r} does not match "
                f"selected entity ID {identity['id']!r} in {source}."
            )
        if subject.get("type") != "Entity":
            raise DecisionQueryError(
                f"Claim {claim_id} subject type must be 'Entity' in {source}; "
                f"found {subject.get('type')!r}."
            )
        _validate_qualifiers(claim, source)
        evidence_ids = _string_list(
            claim.get("evidenceIds", []), f"Claim {claim_id} evidenceIds in {source}"
        )
        reference_ids = _string_list(
            claim.get("referenceIds", []), f"Claim {claim_id} referenceIds in {source}"
        )
        for evidence_id in evidence_ids:
            if evidence_id not in evidence:
                raise DecisionQueryError(
                    f"Claim {claim_id} references unresolved Evidence ID {evidence_id!r} in {source}."
                )
            linked_claims = _string_list(
                evidence[evidence_id].get("claimIds", []),
                f"Evidence {evidence_id} claimIds in {source}",
            )
            if claim_id not in linked_claims:
                raise DecisionQueryError(
                    f"Non-reciprocal Claim/Evidence link in {source}: Claim {claim_id} links "
                    f"Evidence {evidence_id}, but the Evidence does not link the Claim."
                )
        for reference_id in reference_ids:
            if reference_id not in references:
                raise DecisionQueryError(
                    f"Claim {claim_id} references unresolved Reference ID {reference_id!r} in {source}."
                )

    for evidence_id, item in evidence.items():
        _require_item_strings(
            item,
            ("role", "strength", "confidence", "summary", "interpretation"),
            f"Evidence {evidence_id} in {source}",
        )
        if item.get("status") is not None:
            _require_string(item["status"], f"Evidence {evidence_id} status in {source}")
        claim_ids = _string_list(item.get("claimIds", []), f"Evidence {evidence_id} claimIds in {source}")
        reference_ids = _string_list(
            item.get("referenceIds", []), f"Evidence {evidence_id} referenceIds in {source}"
        )
        fragments = _require_list(
            item.get("sourceFragments", []), f"Evidence {evidence_id} sourceFragments in {source}"
        )
        limitations = _require_list(
            item.get("limitations", []), f"Evidence {evidence_id} limitations in {source}"
        )
        for index, limitation in enumerate(limitations):
            _require_string(limitation, f"Evidence {evidence_id} limitation {index} in {source}")
        for claim_id in claim_ids:
            if claim_id not in claims:
                raise DecisionQueryError(
                    f"Evidence {evidence_id} references unresolved Claim ID {claim_id!r} in {source}."
                )
            linked_evidence = _string_list(
                claims[claim_id].get("evidenceIds", []),
                f"Claim {claim_id} evidenceIds in {source}",
            )
            if evidence_id not in linked_evidence:
                raise DecisionQueryError(
                    f"Non-reciprocal Evidence/Claim link in {source}: Evidence {evidence_id} links "
                    f"Claim {claim_id}, but the Claim does not link the Evidence."
                )
        for reference_id in reference_ids:
            if reference_id not in references:
                raise DecisionQueryError(
                    f"Evidence {evidence_id} references unresolved Reference ID {reference_id!r} in {source}."
                )
        for index, raw_fragment in enumerate(fragments):
            fragment = _require_object(
                raw_fragment, f"Evidence {evidence_id} source fragment {index} in {source}"
            )
            reference_id = _require_string(
                fragment.get("referenceId"),
                f"Evidence {evidence_id} source fragment {index} referenceId in {source}",
            )
            if reference_id not in references:
                raise DecisionQueryError(
                    f"Evidence {evidence_id} source fragment {index} references unresolved "
                    f"Reference ID {reference_id!r} in {source}."
                )

    return references, claims, evidence


def _copy_fields(item: dict[str, Any], fields: Iterable[str]) -> dict[str, Any]:
    return {field: copy.deepcopy(item[field]) for field in fields if field in item}


def _resolve_reference(reference: dict[str, Any]) -> dict[str, Any]:
    result = _copy_fields(
        reference,
        ("id", "title", "sourceType", "sourcePriority", "arxivId", "doi"),
    )
    authors = reference.get("authors", [])
    if isinstance(authors, list):
        result["authors"] = [
            author.get("name") if isinstance(author, dict) else author for author in authors
        ]
    publication_date = reference.get("publishedAt", reference.get("publicationDate"))
    if publication_date is not None:
        result["publicationDate"] = copy.deepcopy(publication_date)
    url = reference.get("canonicalUrl", reference.get("url"))
    if url is not None:
        result["url"] = copy.deepcopy(url)
    return result


def _resolve_evidence(item: dict[str, Any]) -> dict[str, Any]:
    return _copy_fields(
        item,
        (
            "id",
            "role",
            "strength",
            "confidence",
            "status",
            "summary",
            "interpretation",
            "sourceFragments",
            "limitations",
            "claimIds",
            "referenceIds",
        ),
    )


def _entity_characteristics(record: dict[str, Any]) -> tuple[dict[str, Any], list[Any], list[Any]]:
    operational: dict[str, Any] = {}
    evaluation: list[Any] = []
    considerations: list[Any] = []
    for value in record.values():
        if not isinstance(value, dict):
            continue
        if "operationalCharacteristics" in value:
            operational = copy.deepcopy(
                _require_object(value["operationalCharacteristics"], "operational characteristics")
            )
        if "evaluationGuidance" in value:
            evaluation = copy.deepcopy(_require_list(value["evaluationGuidance"], "evaluation guidance"))
            for index, item in enumerate(evaluation):
                _require_string(item, f"evaluation guidance item {index}")
        if "implementationConsiderations" in value:
            considerations = copy.deepcopy(
                _require_list(value["implementationConsiderations"], "implementation considerations")
            )
            for index, item in enumerate(considerations):
                _require_string(item, f"implementation consideration {index}")
    return operational, evaluation, considerations


def build_decision_brief(record: dict[str, Any], source: Path) -> dict[str, Any]:
    """Construct the single decision model consumed by both renderers."""
    identity = _validate_identity(record, source)
    references, claims, evidence = validate_embedded_knowledge(record, source)
    metadata = _require_object(record.get("metadata", {}), f"metadata in {source}")
    description = _require_object(record.get("description", {}), f"description in {source}")
    operational, evaluation, considerations = _entity_characteristics(record)

    resolved_references = [_resolve_reference(item) for item in references.values()]
    resolved_evidence = [_resolve_evidence(item) for item in evidence.values()]
    resolved_claims: list[dict[str, Any]] = []
    residual_limitations: list[str] = []
    for evidence_item in evidence.values():
        for limitation in evidence_item.get("limitations", []):
            if limitation not in residual_limitations:
                residual_limitations.append(limitation)
    for claim in claims.values():
        claim_evidence = [evidence[item_id] for item_id in claim.get("evidenceIds", [])]
        claim_reference_ids = list(claim.get("referenceIds", []))
        for evidence_item in claim_evidence:
            for reference_id in evidence_item.get("referenceIds", []):
                if reference_id not in claim_reference_ids:
                    claim_reference_ids.append(reference_id)
        resolved = _copy_fields(
            claim,
            ("id", "statement", "claimType", "confidence", "status", "qualifiers", "rationale"),
        )
        resolved["evidence"] = [_resolve_evidence(item) for item in claim_evidence]
        resolved["references"] = [_resolve_reference(references[item_id]) for item_id in claim_reference_ids]
        resolved_claims.append(resolved)

    raw_warnings = record.get("warnings", [])
    warnings = copy.deepcopy(_require_list(raw_warnings, f"warnings in {source}"))
    for index, warning in enumerate(warnings):
        _require_string(warning, f"warning {index} in {source}")
    name = identity["name"].get("display") or identity["name"].get("official")
    return {
        "entity": {
            "id": identity["id"],
            "name": name,
            "officialName": identity["name"].get("official"),
            "slug": identity["slug"],
            "entityType": identity.get("entityType"),
            "status": identity.get("status", metadata.get("status")),
            "reviewState": metadata.get("reviewState"),
        },
        "summary": description.get("summary", description.get("description", "")),
        "operationalCharacteristics": operational,
        "implementationConsiderations": considerations,
        "evaluationGuidance": evaluation,
        "claims": resolved_claims,
        "evidence": resolved_evidence,
        "references": resolved_references,
        "warnings": warnings,
        "residualLimitations": residual_limitations,
    }


def _manifest_documents_by_schema(
    root: Path, schema: str, description: str
) -> list[tuple[Path, dict[str, Any]]]:
    manifest_path = root / "data" / "manifest.json"
    manifest = _require_object(_load_json(manifest_path, "data manifest"), "data manifest")
    entries = _require_list(manifest.get("data"), "data manifest field 'data'")
    documents: list[tuple[Path, dict[str, Any]]] = []
    for index, raw_entry in enumerate(entries):
        entry = _require_object(raw_entry, f"manifest entry {index}")
        entry_schema = _require_string(
            entry.get("schema"), f"manifest entry {index} field 'schema'"
        )
        if entry_schema != schema:
            continue
        relative_path = _require_string(entry.get("file"), f"manifest entry {index} field 'file'")
        path = _safe_manifest_path(root, relative_path, index)
        document = _require_object(
            _load_json(path, f"{description} for manifest entry {index}"),
            f"{description} {relative_path}",
        )
        documents.append((path, document))
    return documents


def discover_relationships(
    entities: Sequence[tuple[Path, dict[str, Any]]], root: Path = REPOSITORY_ROOT
) -> list[dict[str, Any]]:
    """Discover and locally validate every canonical relationship instance."""
    entity_sources: dict[str, Path] = {}
    for source, record in entities:
        identity = _validate_identity(record, source)
        entity_id = identity["id"]
        if entity_id in entity_sources:
            raise DecisionQueryError(
                f"Duplicate canonical entity ID {entity_id!r} prevents relationship resolution."
            )
        entity_sources[entity_id] = source

    relationships: list[dict[str, Any]] = []
    seen_ids: dict[str, Path] = {}
    for source, document in _manifest_documents_by_schema(
        root, "schema/relationship-set.schema.json", "relationship set"
    ):
        collection = _require_list(document.get("relationships"), f"relationships in {source}")
        for index, raw_relationship in enumerate(collection):
            context = f"relationship {index} in {source}"
            relationship = _require_object(raw_relationship, context)
            _require_item_strings(
                relationship,
                ("id", "predicate", "sourceId", "targetId", "description"),
                context,
            )
            _require_object(relationship.get("properties"), f"{context}.properties")
            relationship_id = relationship["id"]
            if relationship_id in seen_ids:
                raise DecisionQueryError(
                    f"Duplicate Relationship ID {relationship_id!r} in {source}; "
                    f"first encountered in {seen_ids[relationship_id]}."
                )
            seen_ids[relationship_id] = source
            for endpoint in ("sourceId", "targetId"):
                endpoint_id = relationship[endpoint]
                if endpoint_id not in entity_sources:
                    raise DecisionQueryError(
                        f"Relationship {relationship_id} has unresolved {endpoint} "
                        f"{endpoint_id!r} in {source}."
                    )
            relationships.append(copy.deepcopy(relationship))
    return relationships


def _index_support_items(
    documents: Sequence[tuple[Path, dict[str, Any]]], field: str, label: str
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    sources: dict[str, Path] = {}
    for source, document in documents:
        items = _require_list(document.get(field), f"{field} in {source}")
        for index, raw_item in enumerate(items):
            item = _require_object(raw_item, f"{field}[{index}] in {source}")
            stable_id = _require_string(item.get("id"), f"{field}[{index}].id in {source}")
            if stable_id in result:
                raise DecisionQueryError(
                    f"Duplicate relationship-support {label} ID {stable_id!r} in {source}; "
                    f"first encountered in {sources[stable_id]}."
                )
            result[stable_id] = item
            sources[stable_id] = source
    return result


def discover_relationship_support(
    relationships: Sequence[dict[str, Any]], root: Path = REPOSITORY_ROOT
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    """Discover relationship support and validate all canonical cross-links."""
    relationship_ids = {relationship["id"] for relationship in relationships}
    documents = _manifest_documents_by_schema(
        root, "schema/relationship-support-set.schema.json", "relationship support set"
    )
    references = _index_support_items(documents, "references", "Reference")
    claims = _index_support_items(documents, "claims", "Claim")
    evidence = _index_support_items(documents, "evidence", "Evidence")

    for reference_id, reference in references.items():
        _require_item_strings(
            reference,
            ("title", "sourceType", "sourcePriority"),
            f"relationship-support Reference {reference_id}",
        )

    for claim_id, claim in claims.items():
        _require_item_strings(
            claim,
            ("statement", "claimType", "confidence", "status"),
            f"relationship-support Claim {claim_id}",
        )
        subject = _require_object(
            claim.get("subject"), f"relationship-support Claim {claim_id} subject"
        )
        if subject.get("type") != "Relationship":
            raise DecisionQueryError(
                f"Relationship-support Claim {claim_id} subject type must be 'Relationship'; "
                f"found {subject.get('type')!r}."
            )
        subject_id = _require_string(
            subject.get("id"), f"relationship-support Claim {claim_id} subject.id"
        )
        if subject_id not in relationship_ids:
            raise DecisionQueryError(
                f"Relationship-support Claim {claim_id} references unresolved Relationship ID "
                f"{subject_id!r}."
            )
        evidence_ids = _string_list(
            claim.get("evidenceIds", []), f"relationship-support Claim {claim_id} evidenceIds"
        )
        reference_ids = _string_list(
            claim.get("referenceIds", []), f"relationship-support Claim {claim_id} referenceIds"
        )
        for evidence_id in evidence_ids:
            if evidence_id not in evidence:
                raise DecisionQueryError(
                    f"Relationship-support Claim {claim_id} references unresolved Evidence ID "
                    f"{evidence_id!r}."
                )
            linked_claims = _string_list(
                evidence[evidence_id].get("claimIds", []),
                f"relationship-support Evidence {evidence_id} claimIds",
            )
            if claim_id not in linked_claims:
                raise DecisionQueryError(
                    "Non-reciprocal relationship-support Claim/Evidence link: "
                    f"Claim {claim_id} links Evidence {evidence_id}, but the Evidence does not "
                    "link the Claim."
                )
        for reference_id in reference_ids:
            if reference_id not in references:
                raise DecisionQueryError(
                    f"Relationship-support Claim {claim_id} references unresolved Reference ID "
                    f"{reference_id!r}."
                )

    for evidence_id, item in evidence.items():
        _require_item_strings(
            item,
            ("role", "strength", "confidence", "status", "summary", "interpretation"),
            f"relationship-support Evidence {evidence_id}",
        )
        claim_ids = _string_list(
            item.get("claimIds", []), f"relationship-support Evidence {evidence_id} claimIds"
        )
        reference_ids = _string_list(
            item.get("referenceIds", []),
            f"relationship-support Evidence {evidence_id} referenceIds",
        )
        linked_relationship_ids = _string_list(
            item.get("relationshipIds", []),
            f"relationship-support Evidence {evidence_id} relationshipIds",
        )
        _string_list(
            item.get("limitations", []),
            f"relationship-support Evidence {evidence_id} limitations",
        )
        for claim_id in claim_ids:
            if claim_id not in claims:
                raise DecisionQueryError(
                    f"Relationship-support Evidence {evidence_id} references unresolved Claim ID "
                    f"{claim_id!r}."
                )
            linked_evidence = _string_list(
                claims[claim_id].get("evidenceIds", []),
                f"relationship-support Claim {claim_id} evidenceIds",
            )
            if evidence_id not in linked_evidence:
                raise DecisionQueryError(
                    "Non-reciprocal relationship-support Evidence/Claim link: "
                    f"Evidence {evidence_id} links Claim {claim_id}, but the Claim does not "
                    "link the Evidence."
                )
        for reference_id in reference_ids:
            if reference_id not in references:
                raise DecisionQueryError(
                    f"Relationship-support Evidence {evidence_id} references unresolved Reference ID "
                    f"{reference_id!r}."
                )
        for relationship_id in linked_relationship_ids:
            if relationship_id not in relationship_ids:
                raise DecisionQueryError(
                    f"Relationship-support Evidence {evidence_id} references unresolved "
                    f"Relationship ID {relationship_id!r}."
                )

    return references, claims, evidence


def _support_for_relationship(
    relationship_id: str,
    references: dict[str, dict[str, Any]],
    claims: dict[str, dict[str, Any]],
    evidence: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    selected_claim_ids = [
        claim_id
        for claim_id, claim in claims.items()
        if claim.get("subject", {}).get("id") == relationship_id
    ]
    selected_evidence_ids = [
        evidence_id
        for evidence_id, item in evidence.items()
        if relationship_id in item.get("relationshipIds", [])
    ]
    for claim_id in selected_claim_ids:
        for evidence_id in claims[claim_id].get("evidenceIds", []):
            if evidence_id not in selected_evidence_ids:
                selected_evidence_ids.append(evidence_id)
    for evidence_id in selected_evidence_ids:
        for claim_id in evidence[evidence_id].get("claimIds", []):
            if claim_id not in selected_claim_ids:
                selected_claim_ids.append(claim_id)

    selected_reference_ids: list[str] = []
    for claim_id in selected_claim_ids:
        for reference_id in claims[claim_id].get("referenceIds", []):
            if reference_id not in selected_reference_ids:
                selected_reference_ids.append(reference_id)
    for evidence_id in selected_evidence_ids:
        for reference_id in evidence[evidence_id].get("referenceIds", []):
            if reference_id not in selected_reference_ids:
                selected_reference_ids.append(reference_id)
    return (
        [copy.deepcopy(claims[item_id]) for item_id in selected_claim_ids],
        [copy.deepcopy(evidence[item_id]) for item_id in selected_evidence_ids],
        [copy.deepcopy(references[item_id]) for item_id in selected_reference_ids],
    )


def classify_relationship_support(
    claims: Sequence[dict[str, Any]],
    evidence: Sequence[dict[str, Any]],
    references: Sequence[dict[str, Any]],
) -> str:
    """Classify display support without creating a persisted epistemic fact."""
    if not claims and not evidence:
        return "No canonical support objects"
    if evidence and references and all(item.get("strength") == "Weak" for item in evidence) and all(
        item.get("sourceType") == "Maintainer Analysis"
        or item.get("sourcePriority") == "Tertiary"
        for item in references
    ):
        return "Maintainer rationale only"
    return "Canonical support objects present"


def build_pipeline_model(
    requested_entities: Sequence[tuple[Path, dict[str, Any]]],
    entities: Sequence[tuple[Path, dict[str, Any]]],
    root: Path = REPOSITORY_ROOT,
) -> dict[str, Any]:
    """Build a composition model while preserving each complete stage brief."""
    if len(requested_entities) != 2:
        raise DecisionQueryError("A pipeline requires exactly two resolved entities.")
    stages = [build_decision_brief(record, source) for source, record in requested_entities]
    stage_ids = [stage["entity"]["id"] for stage in stages]
    if stage_ids[0] == stage_ids[1]:
        raise DecisionQueryError("A pipeline cannot contain the same entity twice.")

    relationships = discover_relationships(entities, root)
    selected = [
        relationship
        for relationship in relationships
        if {relationship["sourceId"], relationship["targetId"]} == set(stage_ids)
    ]
    if not selected:
        raise DecisionQueryError(
            f"No direct canonical relationship connects {stage_ids[0]} and {stage_ids[1]}; "
            "this pilot does not compute transitive paths."
        )
    references, claims, evidence = discover_relationship_support(relationships, root)
    resolved_relationships: list[dict[str, Any]] = []
    for relationship in selected:
        linked_claims, linked_evidence, linked_references = _support_for_relationship(
            relationship["id"], references, claims, evidence
        )
        resolved = copy.deepcopy(relationship)
        resolved["supportClassification"] = classify_relationship_support(
            linked_claims, linked_evidence, linked_references
        )
        resolved["claims"] = linked_claims
        resolved["evidence"] = linked_evidence
        resolved["references"] = linked_references
        resolved_relationships.append(resolved)

    first = stages[0]["entity"]
    second = stages[1]["entity"]
    warnings: list[str] = []
    for stage in stages:
        warnings.extend(item for item in stage.get("warnings", []) if item not in warnings)
    if any(
        stage["entity"].get("status") == "Draft"
        or stage["entity"].get("reviewState") == "Not Reviewed"
        for stage in stages
    ):
        warnings.append(
            "At least one stage is Draft or Not Reviewed; this composition view requires human review."
        )
    cautions = [
        "Technique findings remain attributed to their own entity.",
        "Relationship support does not prove combined-pipeline superiority.",
        "Measurements from different datasets, metrics, models, and papers are not directly comparable.",
        f"Later {second['name']} gains must not be credited to {first['name']}.",
        f"{first['name']} candidate-generation gains must not be credited to {second['name']}.",
        "A modeled workflow edge describes an optional composition and does not make either stage mandatory.",
    ]
    evaluation_checklist: list[dict[str, str]] = []
    seen_guidance: set[str] = set()
    for stage in stages:
        for guidance in stage.get("evaluationGuidance", []):
            if guidance in seen_guidance:
                continue
            seen_guidance.add(guidance)
            evaluation_checklist.append(
                {
                    "stageId": stage["entity"]["id"],
                    "stageName": stage["entity"]["name"],
                    "guidance": guidance,
                }
            )
    return {
        "pipeline": {
            "requestedOrder": stage_ids,
            "stages": stages,
            "relationships": resolved_relationships,
            "warnings": warnings,
            "attributionCautions": cautions,
            "evaluationChecklist": evaluation_checklist,
        }
    }


def _label(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", value).replace("_", " ").title()


def _display_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if value is None:
        return "Not recorded"
    return str(value)


def _reference_line(reference: dict[str, Any]) -> str:
    details = [f"[{reference.get('id', 'unknown')}] {reference.get('title', 'Untitled source')}"]
    authors = reference.get("authors", [])
    if authors:
        details.append(", ".join(str(author) for author in authors))
    if reference.get("publicationDate"):
        details.append(str(reference["publicationDate"]))
    if reference.get("sourceType") or reference.get("sourcePriority"):
        details.append(
            "/".join(
                str(value)
                for value in (reference.get("sourcePriority"), reference.get("sourceType"))
                if value
            )
        )
    if reference.get("url"):
        details.append(str(reference["url"]))
    if reference.get("arxivId"):
        details.append(f"arXiv:{reference['arxivId']}")
    if reference.get("doi"):
        details.append(f"DOI:{reference['doi']}")
    return " | ".join(details)


def render_compact_text(brief: dict[str, Any]) -> str:
    """Render a concise, traceable view of the complete decision brief."""
    entity = brief["entity"]
    lines = [
        f"RKM Decision Brief: {entity['name']}",
        "=" * (20 + len(str(entity["name"]))),
        "",
        "Entity identity and lifecycle state",
        f"- ID: {entity['id']} | Slug: {entity['slug']} | "
        f"Type: {_display_value(entity.get('entityType'))}",
        f"- Status: {_display_value(entity.get('status'))} | "
        f"Review state: {_display_value(entity.get('reviewState'))}",
    ]
    if entity.get("status") == "Draft" or entity.get("reviewState") == "Not Reviewed":
        lines.append("- Review notice: Draft or Not Reviewed content has not received human review.")

    lines.extend(("", "Summary", str(brief.get("summary") or "No summary is recorded.")))

    lines.extend(("", "Operational characteristics"))
    operational = brief.get("operationalCharacteristics", {})
    if operational:
        lines.extend(f"- {_label(key)}: {_display_value(value)}" for key, value in operational.items())
    else:
        lines.append("No operational characteristics are recorded.")

    considerations = brief.get("implementationConsiderations", [])
    if considerations:
        lines.extend(("", "Implementation considerations"))
        lines.extend(f"- {_display_value(item)}" for item in considerations)

    lines.extend(("", "Evidence-backed findings"))
    claims = brief.get("claims", [])
    if not claims:
        lines.append("No source-backed findings are recorded for this entity.")
    for number, claim in enumerate(claims, start=1):
        lines.extend(
            (
                "",
                f"{number}. {claim['statement']}",
                f"   Claim: {claim['id']} | Type: {_display_value(claim.get('claimType'))} | "
                f"Confidence: {_display_value(claim.get('confidence'))}",
            )
        )
        qualifiers = claim.get("qualifiers", [])
        if qualifiers:
            context = "; ".join(
                f"{qualifier['name']}: {_display_value(qualifier['value'])}"
                for qualifier in qualifiers
            )
            lines.append(f"   Context: {context}")
        else:
            lines.append("   Context: No contextual qualifiers are recorded.")
        if not claim.get("evidence"):
            lines.append("   Evidence: No embedded evidence is linked to this claim.")
        for item in claim.get("evidence", []):
            lines.extend(
                (
                    f"   Evidence: {item['id']} | Role: {_display_value(item.get('role'))} | "
                    f"Strength: {_display_value(item.get('strength'))}",
                    f"   Source-backed summary: {_display_value(item.get('summary'))}",
                )
            )
            limitations = item.get("limitations", [])
            if limitations:
                lines.append(f"   Main limitation: {limitations[0]}")
                if len(limitations) > 1:
                    lines.append(f"   Last recorded limitation: {limitations[-1]}")
                hidden_count = max(0, len(limitations) - 2)
                if hidden_count:
                    lines.append(
                        f"   Additional recorded limitations not shown: {hidden_count}; "
                        "use --detail full."
                    )
            else:
                lines.append("   Main limitation: No limitation is recorded.")
        reference_ids = [reference["id"] for reference in claim.get("references", [])]
        if reference_ids:
            lines.append(f"   Sources: {', '.join(reference_ids)}")
        else:
            lines.append("   Sources: No embedded references are linked to this claim.")

    lines.extend(("", "Sources"))
    if brief.get("references"):
        lines.extend(f"- {_reference_line(reference)}" for reference in brief["references"])
    else:
        lines.append("No embedded references are recorded for this entity.")

    lines.extend(("", "Evaluation guidance"))
    if brief.get("evaluationGuidance"):
        lines.extend(f"- {_display_value(item)}" for item in brief["evaluationGuidance"])
    else:
        lines.append("No evaluation guidance is recorded for this entity.")

    if brief.get("warnings"):
        lines.extend(("", "Warnings"))
        lines.extend(f"- {_display_value(item)}" for item in brief["warnings"])
    return "\n".join(lines) + "\n"


def render_full_text(brief: dict[str, Any]) -> str:
    """Render the complete human-readable decision brief."""
    entity = brief["entity"]
    lines = [
        f"RKM Decision Brief: {entity['name']}",
        "=" * (20 + len(str(entity["name"]))),
        "",
        "Entity identity and lifecycle state",
        f"- ID: {entity['id']}",
        f"- Slug: {entity['slug']}",
        f"- Type: {_display_value(entity.get('entityType'))}",
        f"- Status: {_display_value(entity.get('status'))}",
        f"- Review state: {_display_value(entity.get('reviewState'))}",
        "",
        "Summary",
        str(brief.get("summary") or "No summary is recorded."),
        "",
        "Operational characteristics",
    ]
    operational = brief.get("operationalCharacteristics", {})
    if operational:
        lines.extend(f"- {_label(key)}: {_display_value(value)}" for key, value in operational.items())
    else:
        lines.append("No operational characteristics are recorded.")

    considerations = brief.get("implementationConsiderations", [])
    if considerations:
        lines.extend(("", "Implementation considerations"))
        lines.extend(f"- {_display_value(item)}" for item in considerations)

    lines.extend(("", "Evidence-backed findings"))
    claims = brief.get("claims", [])
    if not claims and not brief.get("evidence") and not brief.get("references"):
        lines.append(
            "Embedded knowledge notice: this entity has no embedded claims, evidence, or references."
        )
    if not claims:
        lines.append(
            "No embedded claims are recorded for this entity; no source-backed finding can be rendered."
        )
    for number, claim in enumerate(claims, start=1):
        lines.extend(
            (
                "",
                f"{number}. {claim['statement']}",
                f"   Claim: {claim['id']} | Type: {_display_value(claim.get('claimType'))} | "
                f"Confidence: {_display_value(claim.get('confidence'))} | "
                f"Status: {_display_value(claim.get('status'))}",
                "   Contextual qualifiers:",
            )
        )
        qualifiers = claim.get("qualifiers", [])
        if qualifiers:
            lines.extend(
                f"   - {qualifier['name']}: {_display_value(qualifier['value'])}"
                for qualifier in qualifiers
            )
        else:
            lines.append("   - No contextual qualifiers are recorded.")
        if claim.get("rationale"):
            lines.append(f"   Rationale: {claim['rationale']}")
        lines.append("   Supporting evidence and source interpretation:")
        if not claim.get("evidence"):
            lines.append("   - No embedded evidence is linked to this claim.")
        for item in claim.get("evidence", []):
            lines.extend(
                (
                    f"   - {item['id']} | Role: {_display_value(item.get('role'))} | "
                    f"Strength: {_display_value(item.get('strength'))} | "
                    f"Confidence: {_display_value(item.get('confidence'))}",
                    f"     Source-backed summary: {_display_value(item.get('summary'))}",
                    f"     Recorded interpretation: {_display_value(item.get('interpretation'))}",
                    "     Limitations:",
                )
            )
            limitations = item.get("limitations", [])
            if limitations:
                lines.extend(f"     - {limitation}" for limitation in limitations)
            else:
                lines.append("     - No limitations are recorded.")
            fragments = item.get("sourceFragments", [])
            if fragments:
                lines.append("     Source fragments:")
                for fragment in fragments:
                    location = fragment.get("locator") or fragment.get("section") or "unspecified location"
                    lines.append(f"     - {fragment['referenceId']}: {location}")
        lines.append("   Sources:")
        if claim.get("references"):
            lines.extend(f"   - {_reference_line(reference)}" for reference in claim["references"])
        else:
            lines.append("   - No embedded references are linked to this claim.")

    lines.extend(("", "Sources"))
    if brief.get("references"):
        lines.extend(f"- {_reference_line(reference)}" for reference in brief["references"])
    else:
        lines.append("No embedded references are recorded for this entity.")

    lines.extend(("", "Evaluation guidance"))
    if brief.get("evaluationGuidance"):
        lines.extend(f"- {_display_value(item)}" for item in brief["evaluationGuidance"])
    else:
        lines.append("No evaluation guidance is recorded for this entity.")

    if brief.get("warnings"):
        lines.extend(("", "Warnings"))
        lines.extend(f"- {_display_value(item)}" for item in brief["warnings"])
    return "\n".join(lines) + "\n"


def render_text(brief: dict[str, Any], detail: str = "compact") -> str:
    """Render the requested text detail without changing the decision model."""
    if detail == "compact":
        return render_compact_text(brief)
    if detail == "full":
        return render_full_text(brief)
    raise ValueError(f"Unsupported text detail mode: {detail}")


def render_json(brief: dict[str, Any]) -> str:
    return json.dumps(brief, ensure_ascii=False, indent=2) + "\n"


def render_output(brief: dict[str, Any], output_format: str, detail: str) -> str:
    """Render JSON unchanged or select the requested text presentation."""
    if output_format == "json":
        return render_json(brief)
    return render_text(brief, detail)


def _pipeline_relationship_reference_lines(reference: dict[str, Any]) -> list[str]:
    lines = [f"- [{reference['id']}] {reference['title']}"]
    for field, value in reference.items():
        if field in {"id", "title"}:
            continue
        lines.append(f"  {_label(field)}: {_display_value(value)}")
    return lines


def render_pipeline_compact_text(model: dict[str, Any]) -> str:
    """Render a bounded composition view with strict stage attribution."""
    pipeline = model["pipeline"]
    stages = pipeline["stages"]
    first, second = stages
    names_by_id = {stage["entity"]["id"]: stage["entity"]["name"] for stage in stages}
    lines = [
        f"RKM Pipeline Composition: {first['entity']['name']} -> {second['entity']['name']}",
        "="
        * (
            29
            + len(str(first["entity"]["name"]))
            + len(str(second["entity"]["name"]))
        ),
        "",
        "Pipeline identity and lifecycle",
    ]
    for position, stage in enumerate(stages, start=1):
        entity = stage["entity"]
        lines.append(
            f"- Stage {position}: {entity['id']} | {entity['name']} | "
            f"Status: {_display_value(entity.get('status'))} | "
            f"Review state: {_display_value(entity.get('reviewState'))}"
        )
    if any(
        stage["entity"].get("status") == "Draft"
        or stage["entity"].get("reviewState") == "Not Reviewed"
        for stage in stages
    ):
        lines.append(
            "- Review notice: Draft or Not Reviewed stages and relationships require human review."
        )

    lines.extend(
        (
            "",
            "Modeled stage order",
            first["entity"]["name"],
            f"  {first.get('summary') or 'No canonical stage summary is recorded.'}",
            "      |",
            "      v",
            second["entity"]["name"],
            f"  {second.get('summary') or 'No canonical stage summary is recorded.'}",
            "- The requested order controls this presentation; stored relationship direction is "
            "shown separately.",
        )
    )

    lines.extend(("", "Direct workflow relationships"))
    for relationship in pipeline["relationships"]:
        properties = relationship["properties"]
        lines.extend(
            (
                f"- {relationship['id']} | {relationship['predicate']}",
                f"  Stored endpoints: {relationship['sourceId']} "
                f"({names_by_id[relationship['sourceId']]}) -> {relationship['targetId']} "
                f"({names_by_id[relationship['targetId']]})",
                f"  Description: {relationship['description']}",
                f"  Status: {_display_value(properties.get('status'))} | "
                f"Confidence: {_display_value(properties.get('confidence'))} | "
                f"Scope: {_display_value(properties.get('scope'))}",
                f"  Support classification: {relationship['supportClassification']}",
            )
        )

    lines.extend(
        (
            "",
            "Relationship support and epistemic status",
            "- Support classifications describe canonical support objects; they are not persisted "
            "facts or combined-pipeline performance ratings.",
        )
    )
    for relationship in pipeline["relationships"]:
        lines.append(
            f"- {relationship['id']}: {relationship['supportClassification']}"
        )
        if not relationship["claims"] and not relationship["evidence"]:
            lines.append("  No linked relationship Claim or Evidence objects were found.")
        for claim in relationship["claims"]:
            lines.extend(
                (
                    f"  Claim {claim['id']}: {claim['statement']}",
                    f"  Claim type: {_display_value(claim.get('claimType'))} | "
                    f"Confidence: {_display_value(claim.get('confidence'))} | "
                    f"Status: {_display_value(claim.get('status'))}",
                )
            )
        for item in relationship["evidence"]:
            limitations = item.get("limitations", [])
            first_limitation = (
                limitations[0] if limitations else "No limitation is recorded."
            )
            lines.extend(
                (
                    f"  Evidence {item['id']} | Role: {_display_value(item.get('role'))} | "
                    f"Strength: {_display_value(item.get('strength'))} | "
                    f"Confidence: {_display_value(item.get('confidence'))} | "
                    f"Status: {_display_value(item.get('status'))}",
                    f"  Summary: {_display_value(item.get('summary'))}",
                    f"  First limitation: {first_limitation}",
                    f"  Linked references: "
                    f"{', '.join(item.get('referenceIds', [])) or 'None'}",
                )
            )
    lines.append(
        "- Relationship support models possible workflow composition only; it does not empirically "
        "validate the combined pipeline."
    )

    lines.extend(("", "Stage responsibilities"))
    for stage in stages:
        lines.append(
            f"- [{stage['entity']['name']}] "
            f"{stage.get('summary') or 'No canonical stage summary is recorded.'}"
        )

    lines.extend(("", "Stage-specific evidence-backed findings"))
    for stage in stages:
        entity = stage["entity"]
        lines.append(f"[{entity['name']}]")
        if not stage.get("claims"):
            lines.append("- No source-backed findings are recorded for this stage.")
        for claim in stage.get("claims", []):
            limitations = [
                limitation
                for item in claim.get("evidence", [])
                for limitation in item.get("limitations", [])
            ]
            reference_ids = [reference["id"] for reference in claim.get("references", [])]
            lines.extend(
                (
                    f"- {claim['statement']}",
                    f"  Claim: {claim['id']} | Principal limitation: "
                    f"{limitations[0] if limitations else 'No limitation is recorded.'}",
                    f"  References: {', '.join(reference_ids) or 'None'}",
                )
            )
        lines.extend(
            (
                "  Inspect full stage evidence:",
                f"  python3 scripts/rkm-decision-query.py --entity {entity['slug']} --detail full",
            )
        )

    lines.extend(("", "Attribution cautions"))
    lines.extend(f"- {caution}" for caution in pipeline["attributionCautions"])

    lines.extend(("", "Combined evaluation checklist"))
    if pipeline["evaluationChecklist"]:
        lines.extend(
            f"- [{item['stageName']}] {item['guidance']}"
            for item in pipeline["evaluationChecklist"]
        )
    else:
        lines.append("No canonical evaluation guidance is recorded for either stage.")

    lines.extend(("", "Sources", "Relationship-support sources"))
    support_references: dict[str, dict[str, Any]] = {}
    for relationship in pipeline["relationships"]:
        for reference in relationship["references"]:
            support_references.setdefault(reference["id"], reference)
    if support_references:
        for reference in support_references.values():
            lines.extend(_pipeline_relationship_reference_lines(reference))
    else:
        lines.append("No relationship-support references are linked.")
    for stage in stages:
        lines.append(f"{stage['entity']['name']} technique sources")
        if stage.get("references"):
            lines.extend(f"- {_reference_line(reference)}" for reference in stage["references"])
        else:
            lines.append("- No embedded references are recorded for this stage.")

    if pipeline.get("warnings"):
        lines.extend(("", "Warnings"))
        lines.extend(f"- {_display_value(warning)}" for warning in pipeline["warnings"])
    return "\n".join(lines) + "\n"


def render_pipeline_full_text(model: dict[str, Any]) -> str:
    """Append complete canonical support and complete existing stage briefs."""
    pipeline = model["pipeline"]
    lines = [
        render_pipeline_compact_text(model).rstrip("\n"),
        "",
        "Complete relationship support objects",
    ]
    for relationship in pipeline["relationships"]:
        canonical = {
            key: copy.deepcopy(value)
            for key, value in relationship.items()
            if key
            not in {
                "supportClassification",
                "claims",
                "evidence",
                "references",
            }
        }
        lines.extend(
            (
                "",
                f"Relationship {relationship['id']} canonical object:",
                json.dumps(canonical, ensure_ascii=False, indent=2),
                f"Relationship {relationship['id']} complete Claim objects:",
                json.dumps(relationship["claims"], ensure_ascii=False, indent=2),
                f"Relationship {relationship['id']} complete Evidence objects:",
                json.dumps(relationship["evidence"], ensure_ascii=False, indent=2),
            )
        )
    lines.extend(
        (
            "",
            "Complete relationship Reference metadata is rendered once in Sources above.",
        )
    )
    lines.extend(("", "Complete stage decision briefs"))
    for stage in pipeline["stages"]:
        lines.extend(
            (
                "",
                f"Stage: {stage['entity']['name']}",
                render_full_text(stage).rstrip("\n"),
            )
        )
    return "\n".join(lines) + "\n"


def render_pipeline_output(model: dict[str, Any], output_format: str, detail: str) -> str:
    """Render complete pipeline JSON independently of text detail."""
    if output_format == "json":
        return render_json(model)
    if detail == "compact":
        return render_pipeline_compact_text(model)
    if detail == "full":
        return render_pipeline_full_text(model)
    raise ValueError(f"Unsupported text detail mode: {detail}")


def _fixture_record(entity_id: str = "ENTITY-1", slug: str = "example", name: str = "Example") -> dict[str, Any]:
    return {
        "identity": {
            "id": entity_id,
            "slug": slug,
            "name": {"official": name, "display": name},
            "entityType": "Technique",
            "status": "Draft",
        },
        "metadata": {"reviewState": "Reviewed"},
        "description": {"summary": "Fixture summary."},
        "references": [
            {
                "id": "REFERENCE-1",
                "title": "Fixture source",
                "authors": [{"name": "Fixture Author"}],
                "sourceType": "Paper",
                "sourcePriority": "Primary",
                "publishedAt": "2026-01-01",
                "canonicalUrl": "https://example.invalid/source",
            },
            {
                "id": "REFERENCE-2",
                "title": "Unlinked fixture source",
                "authors": [{"name": "Second Author"}],
                "sourceType": "Documentation",
                "sourcePriority": "Secondary",
                "publishedAt": "2026-02-01",
                "canonicalUrl": "https://example.invalid/unlinked",
            },
        ],
        "claims": [
            {
                "id": "CLAIM-1",
                "statement": "Fixture finding.",
                "claimType": "Factual",
                "subject": {"id": entity_id, "type": "Entity"},
                "qualifiers": [
                    {"name": "dataset", "value": "Fixture data"},
                    {"name": "metric", "value": "Fixture metric"},
                ],
                "confidence": "High",
                "status": "Draft",
                "evidenceIds": ["EVIDENCE-1"],
                "referenceIds": ["REFERENCE-1"],
                "rationale": "Fixture rationale.",
            }
        ],
        "evidence": [
            {
                "id": "EVIDENCE-1",
                "role": "Benchmarks",
                "strength": "Strong",
                "confidence": "High",
                "summary": "Fixture evidence.",
                "interpretation": "Fixture interpretation.",
                "claimIds": ["CLAIM-1"],
                "referenceIds": ["REFERENCE-1"],
                "sourceFragments": [{"referenceId": "REFERENCE-1", "locator": "Section 1"}],
                "limitations": [
                    "Fixture limitation.",
                    "Hidden fixture limitation.",
                    "Last fixture limitation.",
                ],
            }
        ],
        "technique": {
            "operationalCharacteristics": {"latencyImpact": "Variable"},
            "evaluationGuidance": ["Evaluate the fixture."],
        },
    }


def _fixture_relationship(
    relationship_id: str, source_id: str, target_id: str, predicate: str
) -> dict[str, Any]:
    return {
        "id": relationship_id,
        "predicate": predicate,
        "sourceId": source_id,
        "targetId": target_id,
        "description": f"{source_id} can compose with {target_id}.",
        "properties": {
            "status": "Draft",
            "confidence": "Conservative",
            "scope": "Fixture",
        },
    }


def _fixture_support(
    relationship_id: str, claim_id: str, evidence_id: str, reference_id: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    reference = {
        "id": reference_id,
        "title": "Fixture relationship rationale",
        "sourceType": "Maintainer Analysis",
        "sourcePriority": "Tertiary",
        "publisher": "Fixture maintainers",
        "notes": ["Not external empirical evidence."],
    }
    claim = {
        "id": claim_id,
        "statement": f"{relationship_id} is a possible fixture workflow edge.",
        "claimType": "Interpretive",
        "subject": {"type": "Relationship", "id": relationship_id},
        "confidence": "Low",
        "status": "Draft",
        "evidenceIds": [evidence_id],
        "referenceIds": [reference_id],
    }
    evidence = {
        "id": evidence_id,
        "role": "Motivates",
        "strength": "Weak",
        "confidence": "Low",
        "status": "Draft",
        "summary": f"Maintainer rationale for {relationship_id}.",
        "interpretation": "Possible composition only.",
        "claimIds": [claim_id],
        "referenceIds": [reference_id],
        "relationshipIds": [relationship_id],
        "limitations": [
            f"{relationship_id} is not a universal architecture rule.",
            f"{relationship_id} has no combined benchmark result.",
        ],
    }
    return reference, claim, evidence


def _write_pipeline_fixture(root: Path) -> None:
    data = root / "data"
    data.mkdir(exist_ok=True)
    second = _fixture_record("ENTITY-2", "second", "Second Example")
    second["references"][0]["id"] = "REFERENCE-SECOND"
    second["claims"][0]["id"] = "CLAIM-SECOND"
    second["claims"][0]["statement"] = "Second-stage fixture finding."
    second["claims"][0]["evidenceIds"] = ["EVIDENCE-SECOND"]
    second["claims"][0]["referenceIds"] = ["REFERENCE-SECOND"]
    second["evidence"][0]["id"] = "EVIDENCE-SECOND"
    second["evidence"][0]["claimIds"] = ["CLAIM-SECOND"]
    second["evidence"][0]["referenceIds"] = ["REFERENCE-SECOND"]
    second["evidence"][0]["sourceFragments"][0]["referenceId"] = "REFERENCE-SECOND"
    records = (
        ("example.json", _fixture_record()),
        ("second.json", second),
        ("third.json", _fixture_record("ENTITY-3", "third", "Third Example")),
    )
    for name, record in records:
        (data / name).write_text(json.dumps(record), encoding="utf-8")
    relationships = [
        _fixture_relationship("RELATIONSHIP-A", "ENTITY-1", "ENTITY-2", "CAN_FEED"),
        _fixture_relationship("RELATIONSHIP-B", "ENTITY-2", "ENTITY-1", "CAN_REFINE"),
    ]
    (data / "relationships.json").write_text(
        json.dumps({"relationships": relationships}), encoding="utf-8"
    )
    support_objects = [
        _fixture_support(
            "RELATIONSHIP-A", "RELATIONSHIP-CLAIM-A", "RELATIONSHIP-EVIDENCE-A", "RELATIONSHIP-REFERENCE"
        ),
        _fixture_support(
            "RELATIONSHIP-B", "RELATIONSHIP-CLAIM-B", "RELATIONSHIP-EVIDENCE-B", "RELATIONSHIP-REFERENCE"
        ),
    ]
    references = [support_objects[0][0]]
    claims = [item[1] for item in support_objects]
    evidence = [item[2] for item in support_objects]
    (data / "support.json").write_text(
        json.dumps({"references": references, "claims": claims, "evidence": evidence}),
        encoding="utf-8",
    )
    manifest = {
        "data": [
            *[
                {"file": f"data/{name}", "schema": "schema/example.json"}
                for name, _record in records
            ],
            {
                "file": "data/relationships.json",
                "schema": "schema/relationship-set.schema.json",
            },
            {
                "file": "data/support.json",
                "schema": "schema/relationship-support-set.schema.json",
            },
        ]
    }
    (data / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def _expect_error(record: dict[str, Any], expected: str, source: Path) -> None:
    try:
        build_decision_brief(record, source)
    except DecisionQueryError as exc:
        if expected not in str(exc):
            raise AssertionError(f"Expected error containing {expected!r}; got {exc!r}") from exc
    else:
        raise AssertionError(f"Expected DecisionQueryError containing {expected!r}")


def _expect_pipeline_error(root: Path, expected: str) -> None:
    try:
        entities = discover_entities(root)
        relationships = discover_relationships(entities, root)
        discover_relationship_support(relationships, root)
    except DecisionQueryError as exc:
        if expected not in str(exc):
            raise AssertionError(f"Expected error containing {expected!r}; got {exc!r}") from exc
    else:
        raise AssertionError(f"Expected DecisionQueryError containing {expected!r}")


def _expect_argument_error(arguments: Sequence[str], validate_mode: bool = False) -> None:
    parser = _create_argument_parser()
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            args = parser.parse_args(arguments)
            if validate_mode:
                _validate_mode_arguments(parser, args)
    except SystemExit as exc:
        if exc.code == 0:
            raise AssertionError(f"Expected argument failure for {arguments!r}")
    else:
        raise AssertionError(f"Expected argument failure for {arguments!r}")


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        data = root / "data"
        data.mkdir()
        record = _fixture_record()
        second = _fixture_record("ENTITY-2", "second", "Second Example")
        (data / "example.json").write_text(json.dumps(record), encoding="utf-8")
        (data / "second.json").write_text(json.dumps(second), encoding="utf-8")
        (data / "relationships.json").write_text(
            json.dumps({"relationshipSet": {"id": "SET-1"}}), encoding="utf-8"
        )
        manifest = {
            "data": [
                {"file": "data/example.json", "schema": "schema/example.json"},
                {"file": "data/second.json", "schema": "schema/example.json"},
                {"file": "data/relationships.json", "schema": "schema/relationships.json"},
            ]
        }
        (data / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        entities = discover_entities(root)
        assert len(entities) == 2
        assert resolve_entity("ENTITY-1", entities)[1]["identity"]["id"] == "ENTITY-1"
        assert resolve_entity("example", entities)[1]["identity"]["id"] == "ENTITY-1"
        assert resolve_entity("eXaMpLe", entities)[1]["identity"]["id"] == "ENTITY-1"
        source = data / "example.json"
        record["identity"]["name"]["official"] = "Example Official"
        assert resolve_entity("example official", [(source, record)])[1][
            "identity"
        ]["id"] == "ENTITY-1"

        brief = build_decision_brief(record, source)
        assert brief["entity"]["id"] == "ENTITY-1"
        assert brief["claims"][0]["evidence"][0]["id"] == "EVIDENCE-1"
        assert brief["claims"][0]["references"][0]["id"] == "REFERENCE-1"
        default_args = _parse_arguments(["--entity", "example"])
        compact_args = _parse_arguments(["--entity", "example", "--detail", "compact"])
        full_args = _parse_arguments(["--entity", "example", "--detail", "full"])
        assert default_args.detail == "compact"
        assert compact_args.detail == "compact" and full_args.detail == "full"

        compact_output = render_text(brief)
        explicit_compact_output = render_text(brief, "compact")
        full_output = render_text(brief, "full")
        assert compact_output == explicit_compact_output
        assert "Evidence-backed findings" in compact_output
        for claim in brief["claims"]:
            assert claim["id"] in compact_output
            assert claim["statement"] in compact_output
            for qualifier in claim.get("qualifiers", []):
                assert qualifier["name"] in compact_output
                assert _display_value(qualifier["value"]) in compact_output
            for evidence_item in claim.get("evidence", []):
                assert evidence_item["id"] in compact_output
                assert evidence_item["role"] in compact_output
                assert evidence_item["strength"] in compact_output
                assert evidence_item["limitations"][0] in compact_output
                assert evidence_item["limitations"][-1] in compact_output
                assert (
                    "Additional recorded limitations not shown: 1; use --detail full."
                    in compact_output
                )
            for reference in claim.get("references", []):
                assert reference["id"] in compact_output
        for reference in brief["references"]:
            assert reference["id"] in compact_output
            assert compact_output.count(_reference_line(reference)) == 1
        for source_detail in (
            "Fixture source",
            "Fixture Author",
            "2026-01-01",
            "Primary/Paper",
            "https://example.invalid/source",
        ):
            assert compact_output.count(source_detail) == 1
        assert compact_output.index("Fixture source") > compact_output.index("\nSources\n")
        assert "Fixture limitation." in full_output
        assert "Hidden fixture limitation." in full_output
        assert "Last fixture limitation." in full_output
        assert "Section 1" in full_output
        assert "Fixture interpretation." in full_output

        compact_json = render_output(brief, "json", "compact")
        full_json = render_output(brief, "json", "full")
        assert compact_json == full_json == render_json(brief)
        assert json.loads(compact_json) == json.loads(full_json) == brief
        assert json.loads(render_output(brief, "json", compact_args.detail))["entity"]["slug"] == "example"
        assert json.loads(render_output(brief, "json", full_args.detail))["entity"]["slug"] == "example"

        broken = copy.deepcopy(record)
        broken["claims"][0]["evidenceIds"] = ["EVIDENCE-MISSING"]
        _expect_error(broken, "unresolved Evidence ID", source)
        broken = copy.deepcopy(record)
        broken["claims"][0]["referenceIds"] = ["REFERENCE-MISSING"]
        _expect_error(broken, "unresolved Reference ID", source)
        broken = copy.deepcopy(record)
        broken["claims"][0]["evidenceIds"] = []
        broken["evidence"][0]["claimIds"] = ["CLAIM-MISSING"]
        _expect_error(broken, "unresolved Claim ID", source)
        broken = copy.deepcopy(record)
        broken["evidence"][0]["sourceFragments"][0]["referenceId"] = "REFERENCE-MISSING"
        _expect_error(broken, "source fragment 0 references unresolved", source)
        broken = copy.deepcopy(record)
        broken["evidence"][0]["claimIds"] = []
        _expect_error(broken, "Non-reciprocal Claim/Evidence link", source)
        broken = copy.deepcopy(record)
        broken["claims"][0]["evidenceIds"] = []
        _expect_error(broken, "Non-reciprocal Evidence/Claim link", source)

        for field, label in (("references", "Reference"), ("claims", "Claim"), ("evidence", "Evidence")):
            broken = copy.deepcopy(record)
            broken[field].append(copy.deepcopy(broken[field][0]))
            _expect_error(broken, f"Duplicate {label} ID", source)

        empty = _fixture_record("ENTITY-3", "empty", "Empty Entity")
        empty["references"] = []
        empty["claims"] = []
        empty["evidence"] = []
        empty_brief = build_decision_brief(empty, source)
        assert "No source-backed findings are recorded" in render_text(empty_brief, "compact")
        assert "No embedded claims" in render_text(empty_brief, "full")
        assert empty_brief["claims"] == [] and empty_brief["references"] == []

        try:
            resolve_entity("unknown", entities)
        except DecisionQueryError as exc:
            assert "No canonical RKM entity matches" in str(exc)
        else:
            raise AssertionError("Unknown entity lookup unexpectedly succeeded")

        ambiguous = _fixture_record("ENTITY-4", "fourth", "Example")
        try:
            resolve_entity("Example", entities + [(data / "fourth.json", ambiguous)])
        except DecisionQueryError as exc:
            assert "ambiguous" in str(exc)
        else:
            raise AssertionError("Ambiguous entity lookup unexpectedly succeeded")

    _expect_argument_error(["--entity", "example", "--pipeline", "example", "second"])
    _expect_argument_error(["--pipeline", "example"])
    _expect_argument_error(["--pipeline", "example", "second", "third"])
    _expect_argument_error([], validate_mode=True)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        _write_pipeline_fixture(root)
        entities = discover_entities(root)
        assert len(entities) == 3
        first = resolve_entity("example", entities)
        second = resolve_entity("ENTITY-2", entities)
        third = resolve_entity("third", entities)
        try:
            resolve_entity("unknown-pipeline-stage", entities)
        except DecisionQueryError as exc:
            assert "No canonical RKM entity matches" in str(exc)
        else:
            raise AssertionError("Unknown pipeline entity unexpectedly resolved")

        relationships = discover_relationships(entities, root)
        assert [item["id"] for item in relationships] == [
            "RELATIONSHIP-A",
            "RELATIONSHIP-B",
        ]
        assert relationships[0]["sourceId"] == "ENTITY-1"
        assert relationships[1]["sourceId"] == "ENTITY-2"
        references, support_claims, support_evidence = discover_relationship_support(
            relationships, root
        )
        assert support_claims["RELATIONSHIP-CLAIM-A"]["subject"]["id"] == "RELATIONSHIP-A"
        assert "RELATIONSHIP-B" in support_evidence["RELATIONSHIP-EVIDENCE-B"][
            "relationshipIds"
        ]
        assert list(references) == ["RELATIONSHIP-REFERENCE"]

        entity_json_before = [render_json(build_decision_brief(record, source)) for source, record in (first, second)]
        model = build_pipeline_model((first, second), entities, root)
        entity_json_after = [
            render_json(build_decision_brief(record, source)) for source, record in (first, second)
        ]
        assert entity_json_before == entity_json_after
        pipeline = model["pipeline"]
        assert pipeline["requestedOrder"] == ["ENTITY-1", "ENTITY-2"]
        assert [item["id"] for item in pipeline["relationships"]] == [
            "RELATIONSHIP-A",
            "RELATIONSHIP-B",
        ]
        assert all(
            item["supportClassification"] == "Maintainer rationale only"
            for item in pipeline["relationships"]
        )
        assert classify_relationship_support([], [], []) == "No canonical support objects"
        assert (
            classify_relationship_support(
                [{"id": "CLAIM-X"}],
                [{"id": "EVIDENCE-X", "strength": "Moderate"}],
                [{"id": "REFERENCE-X", "sourceType": "Paper", "sourcePriority": "Primary"}],
            )
            == "Canonical support objects present"
        )

        compact = render_pipeline_compact_text(model)
        full = render_pipeline_full_text(model)
        assert compact == render_pipeline_output(model, "text", "compact")
        for visible in (
            "RKM Pipeline Composition",
            "ENTITY-1",
            "ENTITY-2",
            "RELATIONSHIP-A",
            "RELATIONSHIP-B",
            "RELATIONSHIP-CLAIM-A",
            "RELATIONSHIP-CLAIM-B",
            "RELATIONSHIP-EVIDENCE-A",
            "RELATIONSHIP-EVIDENCE-B",
            "RELATIONSHIP-REFERENCE",
            "Maintainer rationale only",
            "not a universal architecture rule",
            "Attribution cautions",
            "Combined evaluation checklist",
            "[Example] Evaluate the fixture.",
        ):
            assert visible in compact
        assert "RELATIONSHIP-A has no combined benchmark result." not in compact
        assert "RELATIONSHIP-A has no combined benchmark result." in full
        assert "RELATIONSHIP-B has no combined benchmark result." in full
        findings_start = compact.index("Stage-specific evidence-backed findings")
        first_group = compact.index("\n[Example]\n", findings_start)
        second_group = compact.index("\n[Second Example]\n", findings_start)
        assert first_group < compact.index("CLAIM-1", first_group) < second_group
        assert second_group < compact.index("CLAIM-SECOND", second_group)
        assert "does not prove combined-pipeline superiority" in compact
        assert "not directly comparable" in compact
        assert "does not make either stage mandatory" in compact
        assert "complete Claim objects" in full
        assert "complete Evidence objects" in full
        assert "Complete relationship Reference metadata" in full
        compact_json = render_pipeline_output(model, "json", "compact")
        full_json = render_pipeline_output(model, "json", "full")
        assert compact_json == full_json
        assert json.loads(compact_json) == model
        for relationship in pipeline["relationships"]:
            assert relationship["claims"] and relationship["evidence"] and relationship["references"]
        try:
            build_pipeline_model((first, first), entities, root)
        except DecisionQueryError as exc:
            assert "same entity twice" in str(exc)
        else:
            raise AssertionError("Duplicate pipeline entity unexpectedly succeeded")
        try:
            build_pipeline_model((first, third), entities, root)
        except DecisionQueryError as exc:
            assert "No direct canonical relationship" in str(exc)
        else:
            raise AssertionError("Unrelated pipeline pair unexpectedly succeeded")

        support_path = root / "data" / "support.json"
        original_support = _load_json(support_path, "fixture support")
        broken_cases: list[tuple[dict[str, Any], str]] = []
        broken = copy.deepcopy(original_support)
        broken["claims"][0]["evidenceIds"] = ["EVIDENCE-MISSING"]
        broken_cases.append((broken, "unresolved Evidence ID"))
        broken = copy.deepcopy(original_support)
        broken["claims"][0]["evidenceIds"] = []
        broken["evidence"][0]["claimIds"] = ["CLAIM-MISSING"]
        broken_cases.append((broken, "unresolved Claim ID"))
        broken = copy.deepcopy(original_support)
        broken["claims"][0]["referenceIds"] = ["REFERENCE-MISSING"]
        broken_cases.append((broken, "unresolved Reference ID"))
        broken = copy.deepcopy(original_support)
        broken["claims"][0]["subject"]["id"] = "RELATIONSHIP-MISSING"
        broken_cases.append((broken, "unresolved Relationship ID"))
        broken = copy.deepcopy(original_support)
        broken["evidence"][0]["claimIds"] = []
        broken_cases.append((broken, "Non-reciprocal relationship-support Claim/Evidence"))
        broken = copy.deepcopy(original_support)
        broken["claims"][0]["evidenceIds"] = []
        broken_cases.append((broken, "Non-reciprocal relationship-support Evidence/Claim"))
        for field, label in (
            ("references", "Reference"),
            ("claims", "Claim"),
            ("evidence", "Evidence"),
        ):
            broken = copy.deepcopy(original_support)
            broken[field].append(copy.deepcopy(broken[field][0]))
            broken_cases.append((broken, f"Duplicate relationship-support {label} ID"))
        for broken, expected in broken_cases:
            support_path.write_text(json.dumps(broken), encoding="utf-8")
            _expect_pipeline_error(root, expected)
        support_path.write_text(json.dumps(original_support), encoding="utf-8")

        relationship_path = root / "data" / "relationships.json"
        original_relationships = _load_json(relationship_path, "fixture relationships")
        broken_relationships = copy.deepcopy(original_relationships)
        del broken_relationships["relationships"][0]["predicate"]
        relationship_path.write_text(json.dumps(broken_relationships), encoding="utf-8")
        try:
            discover_relationships(entities, root)
        except DecisionQueryError as exc:
            assert ".predicate" in str(exc)
        else:
            raise AssertionError("Malformed relationship unexpectedly succeeded")
        broken_relationships = copy.deepcopy(original_relationships)
        broken_relationships["relationships"].append(
            copy.deepcopy(broken_relationships["relationships"][0])
        )
        relationship_path.write_text(json.dumps(broken_relationships), encoding="utf-8")
        try:
            discover_relationships(entities, root)
        except DecisionQueryError as exc:
            assert "Duplicate Relationship ID" in str(exc)
        else:
            raise AssertionError("Duplicate Relationship ID unexpectedly succeeded")
        broken_relationships = copy.deepcopy(original_relationships)
        broken_relationships["relationships"][0]["sourceId"] = "ENTITY-MISSING"
        relationship_path.write_text(json.dumps(broken_relationships), encoding="utf-8")
        try:
            discover_relationships(entities, root)
        except DecisionQueryError as exc:
            assert "unresolved sourceId" in str(exc)
        else:
            raise AssertionError("Unresolved endpoint unexpectedly succeeded")


def _create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--entity", help="Exact entity ID, slug, display name, or official name."
    )
    modes.add_argument(
        "--pipeline",
        nargs=2,
        metavar=("ENTITY_A", "ENTITY_B"),
        help="Two exact entity lookups in the intended pipeline stage order.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--detail",
        choices=("compact", "full"),
        default="compact",
        help="Text detail level (default: compact; JSON is always complete).",
    )
    parser.add_argument("--self-test", action="store_true", help="Run built-in offline self-tests.")
    return parser


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    return _create_argument_parser().parse_args(argv)


def _validate_mode_arguments(
    parser: argparse.ArgumentParser, args: argparse.Namespace
) -> None:
    if not args.self_test and not args.entity and not args.pipeline:
        parser.error("exactly one of --entity or --pipeline is required unless --self-test is used")


def main(argv: Sequence[str] | None = None) -> int:
    parser = _create_argument_parser()
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            run_self_test()
            print("rkm-decision-query self-test passed.")
            return 0
        _validate_mode_arguments(parser, args)
        entities = discover_entities()
        if args.entity:
            source, record = resolve_entity(args.entity, entities)
            brief = build_decision_brief(record, source)
            output = render_output(brief, args.format, args.detail)
        else:
            requested = [resolve_entity(query, entities) for query in args.pipeline]
            model = build_pipeline_model(requested, entities)
            output = render_pipeline_output(model, args.format, args.detail)
        sys.stdout.write(output)
        return 0
    except DecisionQueryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
