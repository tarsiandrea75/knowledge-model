#!/usr/bin/env python3
"""Query a verified canonical RAG evidence projection without promotion."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROJECTION = ROOT / "examples/fixtures/rkm-canonical-rag-evidence-projection-v1.json"


def _validator() -> Any:
    path = ROOT / "scripts/validate-canonical-rag-evidence-projection.py"
    spec = importlib.util.spec_from_file_location("canonical_projection_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load canonical projection validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def query(projection_path: Path, entity_type: str | None = None, source_id: str | None = None) -> dict[str, Any]:
    validation = _validator().validate(projection_path)
    projection = _load(projection_path)
    entities = projection["entities"]
    if entity_type:
        entities = [entity for entity in entities if entity["entityType"] == entity_type]
    if source_id:
        entities = [
            entity for entity in entities
            if entity["attributes"].get("sourceId") == source_id
            or entity["attributes"].get("id") == source_id
            or entity["slug"] == source_id
        ]
    entity_ids = {entity["id"] for entity in entities}
    relationships = [
        relationship for relationship in projection["relationships"]
        if relationship["sourceId"] in entity_ids or relationship["targetId"] in entity_ids
    ]
    return {
        "status": "verified",
        "scope": projection["lifecycle"]["scope"],
        "productionPromotionAllowed": validation["productionPromotionAllowed"],
        "entities": entities,
        "relationships": relationships,
    }


def _self_test() -> None:
    result = query(PROJECTION, entity_type="Reference", source_id="nasa-sun-facts")
    assert result["status"] == "verified"
    assert result["scope"] == "INTERNAL_EVALUATION_ONLY"
    assert result["productionPromotionAllowed"] is False
    assert len(result["entities"]) == 1
    print("canonical RAG evidence projection query self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projection", type=Path, default=PROJECTION)
    parser.add_argument("--entity-type")
    parser.add_argument("--source-id")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0
    print(json.dumps(query(args.projection.resolve(), args.entity_type, args.source_id), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
