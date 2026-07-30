#!/usr/bin/env python3
"""Build a deterministic, non-promoting projection of reviewed RAG evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT / "examples/fixtures/rkm-external-rag-evidence-bundle-v1.json"
REVIEW_PATH = ROOT / "examples/fixtures/rkm-external-rag-source-review-v1.json"
SCHEMA_PATH = ROOT / "schema/rkm-canonical-rag-evidence-projection-v1.schema.json"


class ProjectionError(ValueError):
    """Raised when reviewed evidence cannot be projected safely."""


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProjectionError(f"unable to read JSON file: {path}") from exc
    if not isinstance(value, dict):
        raise ProjectionError(f"JSON root must be an object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise ProjectionError(f"unable to hash file: {path}") from exc
    return digest.hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ProjectionError(message)


def _provenance(bundle: dict[str, Any], review: dict[str, Any], bundle_sha: str, review_sha: str) -> dict[str, Any]:
    reviewer = review["reviewer"]
    return {
        "bundleId": bundle["bundleId"],
        "bundleSha256": bundle_sha,
        "reviewId": review["reviewId"],
        "reviewSha256": review_sha,
        "reviewedAt": reviewer["reviewedAt"],
        "reviewer": reviewer["name"],
        "scope": reviewer["scope"],
    }


def _entity(
    entity_id: str,
    entity_type: str,
    slug: str,
    name: str,
    provenance: dict[str, Any],
    attributes: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": entity_id,
        "entityType": entity_type,
        "slug": slug,
        "name": name,
        "status": "Reviewed",
        "provenance": provenance,
        "attributes": attributes,
    }


def _relationship(
    relationship_id: str,
    relationship_type: str,
    source_id: str,
    source_type: str,
    target_id: str,
    target_type: str,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": relationship_id,
        "type": relationship_type,
        "sourceId": source_id,
        "sourceType": source_type,
        "targetId": target_id,
        "targetType": target_type,
        "status": "Reviewed",
        "provenance": provenance,
    }


def _validate_inputs(
    bundle: dict[str, Any],
    review: dict[str, Any],
    bundle_sha: str,
    review_sha: str,
    bundle_path: Path,
    review_path: Path,
) -> None:
    _require(bundle.get("contractVersion") == "rkm-external-rag-evidence-bundle-v1", "unsupported evidence bundle contract")
    _require(review.get("contractVersion") == "rkm-external-rag-source-review-v1", "unsupported source review contract")
    _require(
        bundle.get("lifecycle") == {"status": "Draft", "reviewState": "Not Reviewed", "productionPromotionAllowed": False},
        "source bundle must remain Draft, Not Reviewed and non-promotable",
    )
    _require(
        review.get("lifecycle") == {"status": "Reviewed", "reviewState": "Human Reviewed", "productionPromotionAllowed": False},
        "source review must be Human Reviewed and non-promotable",
    )
    reviewer = review.get("reviewer", {})
    _require(reviewer.get("scope") == "INTERNAL_EVALUATION_ONLY", "source review scope must be internal evaluation only")
    subject = review.get("subjectBundle", {})
    _require(subject.get("bundleId") == bundle.get("bundleId"), "source review bundle id does not match evidence bundle")
    _require(subject.get("version") == "1.0.0", "source review bundle version is unsupported")
    _require(subject.get("sha256") == bundle_sha, "source review bundle hash does not match the local bundle")
    _require(bundle_sha == _sha256(bundle_path), "source bundle hash computation is inconsistent")
    _require(review_sha == _sha256(review_path), "source review hash computation is inconsistent")
    source_ids = {source["id"] for source in bundle.get("sources", [])}
    decisions = review.get("sourceDecisions", [])
    decision_ids = {decision.get("sourceId") for decision in decisions}
    _require(source_ids == decision_ids, "source review decisions must cover exactly the bundle sources")
    _require(all(decision.get("decision") == "APPROVED" for decision in decisions), "all projected sources must be approved")


def build(bundle_path: Path = BUNDLE_PATH, review_path: Path = REVIEW_PATH) -> dict[str, Any]:
    bundle = _load(bundle_path)
    review = _load(review_path)
    bundle_sha = _sha256(bundle_path)
    review_sha = _sha256(review_path)
    _validate_inputs(bundle, review, bundle_sha, review_sha, bundle_path, review_path)
    provenance = _provenance(bundle, review, bundle_sha, review_sha)

    entities: list[dict[str, Any]] = [
        _entity("ARTIFACT-1001", "Artifact", "external-evidence-bundle", "External RAG evidence bundle", provenance, {
            "bundleId": bundle["bundleId"], "version": "1.0.0", "sha256": bundle_sha,
        }),
        _entity("DATASET-1001", "Dataset", "space-exploration-corpus", "Space exploration corpus", provenance, bundle["corpus"]),
        _entity("DATASET-1002", "Dataset", "space-exploration-golden-dataset", "Space exploration golden dataset", provenance, bundle["dataset"]),
        _entity("ARTIFACT-1002", "Artifact", "offline-rag-e2e-walkthrough", "Offline RAG generated artifact", provenance, bundle["generatedArtifact"]),
        _entity("ARTIFACT-1003", "Artifact", "offline-rag-e2e-walkthrough-decision", "Offline RAG decision record", provenance, bundle["decisionRecord"]),
        _entity("BENCHMARK-1001", "Benchmark", "offline-rag-e2e-walkthrough", "Offline RAG evaluation walkthrough", provenance, bundle["recommendationSummary"]),
    ]
    decisions_by_source = {decision["sourceId"]: decision for decision in review["sourceDecisions"]}
    for offset, source in enumerate(sorted(bundle["sources"], key=lambda item: item["id"]), start=1):
        source_id = source["id"]
        entities.append(_entity(
            f"REFERENCE-{1000 + offset}", "Reference", source_id, source["title"], provenance, source,
        ))
        entities.append(_entity(
            f"EVIDENCE-{1000 + offset}", "Evidence", f"{source_id}-review", f"Human review of {source["title"]}", provenance,
            {"sourceId": source_id, **decisions_by_source[source_id]},
        ))

    relationships = [
        _relationship("RELATIONSHIP-1001", "REFERENCES", "ARTIFACT-1001", "Artifact", "DATASET-1001", "Dataset", provenance),
        _relationship("RELATIONSHIP-1002", "REFERENCES", "ARTIFACT-1001", "Artifact", "DATASET-1002", "Dataset", provenance),
        _relationship("RELATIONSHIP-1003", "REFERENCES", "ARTIFACT-1001", "Artifact", "ARTIFACT-1002", "Artifact", provenance),
        _relationship("RELATIONSHIP-1004", "REFERENCES", "ARTIFACT-1001", "Artifact", "ARTIFACT-1003", "Artifact", provenance),
        _relationship("RELATIONSHIP-1005", "EVALUATES", "BENCHMARK-1001", "Benchmark", "ARTIFACT-1002", "Artifact", provenance),
    ]
    for offset in range(1, 6):
        relationships.append(_relationship(
            f"RELATIONSHIP-{1005 + offset}", "VALIDATES", f"EVIDENCE-{1000 + offset}", "Evidence", "ARTIFACT-1002", "Artifact", provenance,
        ))

    return {
        "contractVersion": "rkm-canonical-rag-evidence-projection-v1",
        "projectionId": f"{bundle["bundleId"]}-canonical-projection",
        "lifecycle": {
            "status": "Reviewed",
            "reviewState": "Human Reviewed",
            "scope": "INTERNAL_EVALUATION_ONLY",
            "productionPromotionAllowed": False,
        },
        "sourceBundle": {"id": bundle["bundleId"], "version": "1.0.0", "sha256": bundle_sha},
        "sourceReview": {"id": review["reviewId"], "version": review["contractVersion"], "sha256": review_sha},
        "entities": entities,
        "relationships": relationships,
        "limitations": [
            "The projection is derived from reviewed metadata and does not assert new factual claims.",
            "The projection is limited to internal evaluation and cannot authorize production promotion.",
            "Source rights and redistribution decisions remain outside this technical projection.",
        ],
    }


def _validate_projection(projection: dict[str, Any]) -> None:
    schema = _load(SCHEMA_PATH)
    errors = sorted(Draft202012Validator(schema).iter_errors(projection), key=lambda error: list(error.path))
    if errors:
        location = "/".join(str(part) for part in errors[0].path) or "root"
        raise ProjectionError(f"projection schema validation failed at {location}: {errors[0].message}")


def _write(path: Path, projection: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(projection, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError as exc:
        raise ProjectionError(f"unable to write projection: {path}") from exc


def _self_test() -> None:
    first = build()
    second = build()
    _validate_projection(first)
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert first["lifecycle"]["productionPromotionAllowed"] is False
    assert len(first["entities"]) == 16
    assert len(first["relationships"]) == 10
    with tempfile.TemporaryDirectory(prefix="rkm-projection-") as directory:
        output = Path(directory) / "projection.json"
        _write(output, first)
        assert json.loads(output.read_text(encoding="utf-8")) == first
    print("canonical RAG evidence projection self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=BUNDLE_PATH)
    parser.add_argument("--review", type=Path, default=REVIEW_PATH)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            _self_test()
            return 0
        if args.output is None:
            parser.error("--output is required unless --self-test is used")
        projection = build(args.bundle.resolve(), args.review.resolve())
        _validate_projection(projection)
        _write(args.output.resolve(), projection)
        print(json.dumps({"status": "built", "output": str(args.output.resolve()), "entityCount": len(projection["entities"]), "relationshipCount": len(projection["relationships"])}, indent=2, sort_keys=True))
        return 0
    except ProjectionError as exc:
        print(f"canonical RAG evidence projection rejected: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
