#!/usr/bin/env python3
"""Validate canonical RAG evidence projection integrity and idempotence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PROJECTION = ROOT / "examples/fixtures/rkm-canonical-rag-evidence-projection-v1.json"
SCHEMA = ROOT / "schema/rkm-canonical-rag-evidence-projection-v1.schema.json"
BUNDLE = ROOT / "examples/fixtures/rkm-external-rag-evidence-bundle-v1.json"
REVIEW = ROOT / "examples/fixtures/rkm-external-rag-source-review-v1.json"
BUILDER = ROOT / "scripts/build-canonical-rag-evidence-projection.py"


class IntegrityError(ValueError):
    """Raised when a projection fails an integrity check."""


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(f"unable to read JSON file: {path}") from exc
    if not isinstance(value, dict):
        raise IntegrityError(f"JSON root must be an object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise IntegrityError(f"unable to hash file: {path}") from exc
    return digest.hexdigest()


def _builder_module() -> Any:
    spec = importlib.util.spec_from_file_location("canonical_projection_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise IntegrityError("unable to load canonical projection builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _schema_validate(projection: dict[str, Any]) -> None:
    schema = _load(SCHEMA)
    errors = sorted(Draft202012Validator(schema).iter_errors(projection), key=lambda error: list(error.path))
    if errors:
        location = "/".join(str(part) for part in errors[0].path) or "root"
        raise IntegrityError(f"projection schema validation failed at {location}: {errors[0].message}")


def _check_identity_integrity(projection: dict[str, Any]) -> None:
    entities = projection["entities"]
    relationships = projection["relationships"]
    entity_ids = [entity["id"] for entity in entities]
    relationship_ids = [relationship["id"] for relationship in relationships]
    if len(entity_ids) != len(set(entity_ids)):
        raise IntegrityError("duplicate projected entity identity")
    if len(relationship_ids) != len(set(relationship_ids)):
        raise IntegrityError("duplicate projected relationship identity")
    known_ids = set(entity_ids)
    relation_keys: set[tuple[str, str, str]] = set()
    for relationship in relationships:
        key = (relationship["type"], relationship["sourceId"], relationship["targetId"])
        if key in relation_keys:
            raise IntegrityError(f"duplicate projected relationship tuple: {key}")
        relation_keys.add(key)
        if relationship["sourceId"] not in known_ids or relationship["targetId"] not in known_ids:
            raise IntegrityError(f"relationship endpoint is missing: {relationship["id"]}")
    envelope_provenance = None
    for entity in entities:
        if envelope_provenance is None:
            envelope_provenance = entity["provenance"]
        elif entity["provenance"] != envelope_provenance:
            raise IntegrityError(f"entity provenance diverges: {entity["id"]}")
    for relationship in relationships:
        if relationship["provenance"] != envelope_provenance:
            raise IntegrityError(f"relationship provenance diverges: {relationship["id"]}")
    if envelope_provenance is None:
        raise IntegrityError("projection contains no provenance-bearing entities")
    if envelope_provenance["bundleSha256"] != projection["sourceBundle"]["sha256"]:
        raise IntegrityError("entity provenance bundle hash differs from envelope binding")
    if envelope_provenance["reviewSha256"] != projection["sourceReview"]["sha256"]:
        raise IntegrityError("entity provenance review hash differs from envelope binding")


def validate(projection_path: Path = PROJECTION) -> dict[str, Any]:
    projection = _load(projection_path)
    _schema_validate(projection)
    if projection["lifecycle"]["productionPromotionAllowed"] is not False:
        raise IntegrityError("projection must remain non-promotable")
    if _sha256(BUNDLE) != projection["sourceBundle"]["sha256"]:
        raise IntegrityError("source bundle hash mismatch")
    if _sha256(REVIEW) != projection["sourceReview"]["sha256"]:
        raise IntegrityError("source review hash mismatch")
    _check_identity_integrity(projection)
    builder = _builder_module()
    expected = builder.build(BUNDLE, REVIEW)
    if expected != projection:
        raise IntegrityError("projection differs from a fresh deterministic build")
    return {
        "status": "verified",
        "projectionId": projection["projectionId"],
        "entityCount": len(projection["entities"]),
        "relationshipCount": len(projection["relationships"]),
        "productionPromotionAllowed": False,
    }


def _self_test() -> None:
    original = _load(PROJECTION)
    assert validate(PROJECTION)["status"] == "verified"
    tampered = json.loads(json.dumps(original))
    tampered["sourceBundle"]["sha256"] = "0" * 64
    with tempfile.TemporaryDirectory(prefix="rkm-projection-integrity-") as directory:
        path = Path(directory) / "tampered.json"
        path.write_text(json.dumps(tampered), encoding="utf-8")
        try:
            validate(path)
        except IntegrityError:
            pass
        else:
            raise AssertionError("tampered projection must be rejected")
    print("canonical RAG evidence projection integrity self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projection", type=Path, default=PROJECTION)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            _self_test()
            return 0
        print(json.dumps(validate(args.projection.resolve()), indent=2, sort_keys=True))
        return 0
    except IntegrityError as exc:
        print(f"canonical RAG evidence projection rejected: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
