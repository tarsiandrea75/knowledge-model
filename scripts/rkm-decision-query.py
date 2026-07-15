#!/usr/bin/env python3
"""Render a source-linked decision brief from a canonical RKM entity record."""

from __future__ import annotations

import argparse
import copy
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


def render_text(brief: dict[str, Any]) -> str:
    """Render a human-readable decision brief without adding new conclusions."""
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


def render_json(brief: dict[str, Any]) -> str:
    return json.dumps(brief, ensure_ascii=False, indent=2) + "\n"


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
            }
        ],
        "claims": [
            {
                "id": "CLAIM-1",
                "statement": "Fixture finding.",
                "claimType": "Factual",
                "subject": {"id": entity_id, "type": "Entity"},
                "qualifiers": [{"name": "dataset", "value": "Fixture data"}],
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
                "limitations": ["Fixture limitation."],
            }
        ],
        "technique": {
            "operationalCharacteristics": {"latencyImpact": "Variable"},
            "evaluationGuidance": ["Evaluate the fixture."],
        },
    }


def _expect_error(record: dict[str, Any], expected: str, source: Path) -> None:
    try:
        build_decision_brief(record, source)
    except DecisionQueryError as exc:
        if expected not in str(exc):
            raise AssertionError(f"Expected error containing {expected!r}; got {exc!r}") from exc
    else:
        raise AssertionError(f"Expected DecisionQueryError containing {expected!r}")


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
        text_output = render_text(brief)
        assert "Evidence-backed findings" in text_output and "Fixture limitation" in text_output
        assert json.loads(render_json(brief))["entity"]["slug"] == "example"

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
        assert "No embedded claims" in render_text(empty_brief)
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entity", help="Exact entity ID, slug, display name, or official name.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument("--self-test", action="store_true", help="Run built-in offline self-tests.")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            run_self_test()
            print("rkm-decision-query self-test passed.")
            return 0
        if not args.entity:
            parser.error("--entity is required unless --self-test is used")
        source, record = resolve_entity(args.entity, discover_entities())
        brief = build_decision_brief(record, source)
        output = render_json(brief) if args.format == "json" else render_text(brief)
        sys.stdout.write(output)
        return 0
    except DecisionQueryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
