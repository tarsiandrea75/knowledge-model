#!/usr/bin/env python3
"""Find existing relationship predicates with overlapping documented semantics."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any


STOPWORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "is", "of", "on",
    "or", "that", "the", "to", "with", "while", "this", "which", "entity", "source",
    "target", "type", "indicates", "states", "represents",
}


def words(value: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9]+", value.lower())
        if token not in STOPWORDS and len(token) > 2
    }


def semantic_tokens(entry: dict[str, Any]) -> set[str]:
    direction = entry.get("canonicalDirection") or {}
    text = " ".join(
        str(entry.get(key, ""))
        for key in ("type", "label", "description", "category")
    )
    text += " " + " ".join(str(direction.get(key, "")) for key in ("sourceRole", "targetRole", "description"))
    return words(text)


def similarity(left: dict[str, Any], right: dict[str, Any]) -> float:
    left_tokens = semantic_tokens(left)
    right_tokens = semantic_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def review_candidate(candidate: dict[str, Any], entries: list[dict[str, Any]], threshold: float) -> list[tuple[str, float]]:
    matches = []
    for entry in entries:
        if entry.get("type") == candidate.get("type"):
            continue
        score = similarity(candidate, entry)
        if score >= threshold:
            matches.append((str(entry.get("type")), score))
    return sorted(matches, key=lambda item: (-item[1], item[0]))


def load_entries(path: Path) -> list[dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("relationshipTypes") if isinstance(document, dict) else None
    if not isinstance(entries, list):
        raise ValueError(f"{path}: relationshipTypes must be an array")
    return [entry for entry in entries if isinstance(entry, dict) and isinstance(entry.get("type"), str)]


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-predicate-reuse-") as directory:
        path = Path(directory) / "registry.json"
        path.write_text(json.dumps({"relationshipTypes": [
            {"type": "REQUIRES", "label": "Requires", "description": "Declares a hard dependency on a required capability.", "category": "Dependency"},
            {"type": "DEPENDS_ON", "label": "Depends on", "description": "Declares a hard dependency on a required capability.", "category": "Dependency"},
            {"type": "CONTRADICTS", "label": "Contradicts", "description": "States that two claims cannot both be true.", "category": "Evidence"},
        ]}), encoding="utf-8")
        entries = load_entries(path)
        candidate = {"type": "NEEDS", "label": "Needs", "description": "Declares a hard dependency on a required capability.", "category": "Dependency"}
        matches = review_candidate(candidate, entries, 0.25)
        assert [name for name, _ in matches] == ["DEPENDS_ON", "REQUIRES"], matches
        assert not review_candidate({"type": "SUPPORTS", "label": "Supports", "description": "Provides evidence for a claim.", "category": "Evidence"}, entries, 0.60)
    print("relationship predicate reuse self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--registry", type=Path, default=Path("registries/relationship-type-registry.json"))
    parser.add_argument("--candidate-type")
    parser.add_argument("--candidate-label")
    parser.add_argument("--candidate-description")
    parser.add_argument("--candidate-category")
    parser.add_argument("--threshold", type=float, default=0.25)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not 0.0 < args.threshold <= 1.0:
        parser.error("--threshold must be greater than 0 and at most 1")
    if not all((args.candidate_type, args.candidate_label, args.candidate_description, args.candidate_category)):
        parser.error("candidate type, label, description and category are required")
    entries = load_entries(args.registry)
    candidate = {
        "type": args.candidate_type,
        "label": args.candidate_label,
        "description": args.candidate_description,
        "category": args.candidate_category,
    }
    matches = review_candidate(candidate, entries, args.threshold)
    if not matches:
        print(f"No existing predicate exceeded similarity threshold {args.threshold:.2f}.")
        return 0
    print(f"Review candidates for {args.candidate_type}:")
    for name, score in matches:
        print(f"- {name}: lexical semantic overlap {score:.2f}; document explicit reuse justification before adding a new predicate.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
