#!/usr/bin/env python3
"""Validate architecture documentation relationship predicate mentions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELATIONSHIP_TYPE_REGISTRY = (
    REPOSITORY_ROOT / "registries" / "relationship-type-registry.json"
)
ENTITY_TYPE_REGISTRY = REPOSITORY_ROOT / "registries" / "entity-type-registry.json"
ARCHITECTURE_DOCS = REPOSITORY_ROOT / "docs" / "architecture"

UPPERCASE_SNAKE_CASE = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\b")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
FENCE_START = re.compile(r"^```([A-Za-z0-9_-]*)\s*$")
FENCE_END = re.compile(r"^```\s*$")
IGNORED_MARKERS = (
    "noncanonical",
    "candidate",
    "future candidate",
    "deprecated",
    "rejected",
    "derived inverse",
    "avoid storing both",
)
ELLIPSIS = "." * 3
INVALID_RELATIONSHIP_TRIPLES = (
    ("Dataset", "EVALUATES", None, f"Benchmark EVALUATES {ELLIPSIS}"),
    ("Workflow", "EXECUTES", "Agent", "Agent EXECUTES Workflow"),
    ("Framework", "SUPPORTS", "Component", "Framework PROVIDES Component"),
    ("Framework", "SUPPORTS", "Workflow", "Framework IMPLEMENTS Workflow"),
    ("Framework", "USES", "Tool", "Framework PROVIDES Tool"),
    ("Provider", "PROVIDES", "Framework", "Provider SUPPORTS Framework"),
)
SELF_TEST_VALID_TRIPLES = (
    ("Benchmark", "EVALUATES", "Reranker"),
    ("Agent", "EXECUTES", "Workflow"),
    ("Framework", "PROVIDES", "Component"),
    ("Framework", "IMPLEMENTS", "Workflow"),
    ("Framework", "PROVIDES", "Tool"),
    ("Provider", "SUPPORTS", "Framework"),
)
SELF_TEST_INVALID_TRIPLES = (
    ("Dataset", "EVALUATES", "Reranker"),
    ("Workflow", "EXECUTES", "Agent"),
    ("Framework", "SUPPORTS", "Component"),
    ("Framework", "SUPPORTS", "Workflow"),
    ("Framework", "USES", "Tool"),
    ("Provider", "PROVIDES", "Framework"),
)
SELF_TEST_UNKNOWN_PREDICATE = "Paper COMPARES Technique"
SELF_TEST_CANONICAL_SINGLE_WORD = "Paper CITES Reference"
SELF_TEST_ACRONYM_PROSE = "RAG uses JSON and HTTP APIs"
SELF_TEST_ALLOWED_NONCANONICAL = (
    "Future candidate noncanonical example: Paper COMPARES Technique"
)


def display(path: Path) -> str:
    return str(path.relative_to(REPOSITORY_ROOT))


def is_uppercase_snake_case(value: str) -> bool:
    return UPPERCASE_SNAKE_CASE.fullmatch(value) is not None


def line_is_ignored(line: str) -> bool:
    normalized = line.lower()
    return any(marker in normalized for marker in IGNORED_MARKERS)


def load_canonical_predicates(errors: list[str]) -> set[str]:
    try:
        with RELATIONSHIP_TYPE_REGISTRY.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{display(RELATIONSHIP_TYPE_REGISTRY)}: could not load registry: {exc}")
        return set()

    relationship_types = document.get("relationshipTypes")
    if not isinstance(relationship_types, list):
        errors.append(
            f"{display(RELATIONSHIP_TYPE_REGISTRY)}: relationshipTypes must be an array"
        )
        return set()

    predicates: set[str] = set()
    for index, relationship_type in enumerate(relationship_types):
        if not isinstance(relationship_type, dict):
            errors.append(
                f"{display(RELATIONSHIP_TYPE_REGISTRY)}: "
                f"relationshipTypes[{index}] must be an object"
            )
            continue

        predicate = relationship_type.get("type")
        if not isinstance(predicate, str):
            errors.append(
                f"{display(RELATIONSHIP_TYPE_REGISTRY)}: "
                f"relationshipTypes[{index}].type must be a string"
            )
            continue

        predicates.add(predicate)

    return predicates


def load_registered_entity_types(errors: list[str]) -> set[str]:
    entity_types = load_relationship_endpoint_entity_types(errors)

    try:
        with ENTITY_TYPE_REGISTRY.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
    except FileNotFoundError:
        return entity_types
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{display(ENTITY_TYPE_REGISTRY)}: could not load registry: {exc}")
        return entity_types

    registry_entity_types = document.get("entityTypes")
    if not isinstance(registry_entity_types, list):
        errors.append(f"{display(ENTITY_TYPE_REGISTRY)}: entityTypes must be an array")
        return entity_types

    for index, entity_type in enumerate(registry_entity_types):
        if not isinstance(entity_type, dict):
            errors.append(
                f"{display(ENTITY_TYPE_REGISTRY)}: "
                f"entityTypes[{index}] must be an object"
            )
            continue

        type_name = entity_type.get("type")
        if not isinstance(type_name, str):
            errors.append(
                f"{display(ENTITY_TYPE_REGISTRY)}: "
                f"entityTypes[{index}].type must be a string"
            )
            continue

        entity_types.add(type_name)

    return entity_types


def load_relationship_endpoint_entity_types(errors: list[str]) -> set[str]:
    try:
        with RELATIONSHIP_TYPE_REGISTRY.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{display(RELATIONSHIP_TYPE_REGISTRY)}: could not load registry: {exc}")
        return set()

    relationship_types = document.get("relationshipTypes")
    if not isinstance(relationship_types, list):
        errors.append(
            f"{display(RELATIONSHIP_TYPE_REGISTRY)}: relationshipTypes must be an array"
        )
        return set()

    entity_types: set[str] = set()
    for relationship_index, relationship_type in enumerate(relationship_types):
        if not isinstance(relationship_type, dict):
            continue

        for endpoint_name in ("allowedSources", "allowedTargets"):
            endpoints = relationship_type.get(endpoint_name, [])
            if not isinstance(endpoints, list):
                errors.append(
                    f"{display(RELATIONSHIP_TYPE_REGISTRY)}: "
                    f"relationshipTypes[{relationship_index}].{endpoint_name} "
                    "must be an array"
                )
                continue

            for endpoint_index, endpoint in enumerate(endpoints):
                if not isinstance(endpoint, dict):
                    errors.append(
                        f"{display(RELATIONSHIP_TYPE_REGISTRY)}: "
                        f"relationshipTypes[{relationship_index}]."
                        f"{endpoint_name}[{endpoint_index}] must be an object"
                    )
                    continue

                entity_type = endpoint.get("entityType")
                if isinstance(entity_type, str):
                    entity_types.add(entity_type)

    return entity_types


def relationship_position_triples(
    line: str,
    entity_types: set[str],
) -> list[tuple[str, str, str]]:
    if not entity_types:
        return []

    entity_type_pattern = "|".join(
        re.escape(entity_type)
        for entity_type in sorted(entity_types, key=len, reverse=True)
    )
    pattern = re.compile(
        rf"(?<![A-Za-z0-9])"
        rf"(?P<subject>{entity_type_pattern})"
        rf"\s+"
        rf"(?P<predicate>[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*)"
        rf"\s+"
        rf"(?P<object>{entity_type_pattern})"
        rf"\b"
    )

    return [
        (match.group("subject"), match.group("predicate"), match.group("object"))
        for match in pattern.finditer(line)
    ]


def relationship_predicate_in_example(
    line: str,
    canonical_predicates: set[str] | None = None,
) -> str | None:
    candidates = []
    for match in UPPERCASE_SNAKE_CASE.finditer(line):
        before = line[: match.start()].strip()
        after = line[match.end() :].strip()
        if before and after:
            candidates.append(match)

    if not candidates:
        return None

    for match in candidates:
        if "_" in match.group(0):
            return match.group(0)

    for match in candidates:
        before = line[: match.start()]
        after = line[match.end() :]
        if re.search(r"[─-]{2,}\s*$", before) and re.search(r"^\s*[─-]{2,}", after):
            return match.group(0)

    if canonical_predicates is not None:
        for match in candidates:
            if match.group(0) in canonical_predicates:
                return match.group(0)

    return None


def clean_relationship_endpoint(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"^[*+-]\s+", "", cleaned)
    cleaned = cleaned.strip("`| ")
    cleaned = re.sub(r"^[\s|:;,.<>\-─—–→←►◄]+", "", cleaned)
    cleaned = re.sub(r"[\s|:;,.<>\-─—–→←►◄]+$", "", cleaned)
    return cleaned.strip()


def relationship_triple_in_example(
    line: str,
    canonical_predicates: set[str] | None = None,
    entity_types: set[str] | None = None,
) -> tuple[str, str, str] | None:
    predicate = relationship_predicate_in_example(line, canonical_predicates)
    if predicate is None and entity_types is not None:
        triples = relationship_position_triples(line, entity_types)
        if triples:
            return triples[0]

    if predicate is None:
        return None

    match = re.search(rf"\b{re.escape(predicate)}\b", line)
    if match is None:
        return None

    subject = clean_relationship_endpoint(line[: match.start()])
    object_ = clean_relationship_endpoint(line[match.end() :])
    if not subject or not object_:
        return None

    return subject, predicate, object_


def invalid_relationship_guidance(
    subject: str,
    predicate: str,
    object_: str,
) -> str | None:
    for invalid_subject, invalid_predicate, invalid_object, guidance in (
        INVALID_RELATIONSHIP_TRIPLES
    ):
        if subject != invalid_subject or predicate != invalid_predicate:
            continue
        if invalid_object is None or object_ == invalid_object:
            return guidance

    return None


def validate_relationship_triple(
    path: Path,
    line_number: int,
    line: str,
    canonical_predicates: set[str],
    errors: list[str],
) -> None:
    triple = relationship_triple_in_example(line, canonical_predicates)
    if triple is None:
        return

    subject, predicate, object_ = triple
    guidance = invalid_relationship_guidance(subject, predicate, object_)
    if guidance is None:
        return

    errors.append(
        f"{display(path)}:{line_number}: invalid relationship triple "
        f"{subject} {predicate} {object_}; prefer {guidance}"
    )


def validate_relationship_position_line(
    path: Path,
    line_number: int,
    line: str,
    canonical_predicates: set[str],
    entity_types: set[str],
    errors: list[str],
) -> None:
    if line_is_ignored(line):
        return

    position_triples = relationship_position_triples(line, entity_types)
    if position_triples:
        for subject, predicate, object_ in position_triples:
            if predicate not in canonical_predicates:
                errors.append(
                    f"{display(path)}:{line_number}: "
                    f"unknown relationship predicate {predicate}"
                )
                continue

            guidance = invalid_relationship_guidance(subject, predicate, object_)
            if guidance is not None:
                errors.append(
                    f"{display(path)}:{line_number}: invalid relationship triple "
                    f"{subject} {predicate} {object_}; prefer {guidance}"
                )
        return

    predicate = relationship_predicate_in_example(line, canonical_predicates)
    if predicate is None:
        return

    if predicate in canonical_predicates:
        validate_relationship_triple(path, line_number, line, canonical_predicates, errors)
    else:
        errors.append(
            f"{display(path)}:{line_number}: unknown relationship predicate {predicate}"
        )


def validate_fenced_line(
    path: Path,
    line_number: int,
    line: str,
    canonical_predicates: set[str],
    entity_types: set[str],
    errors: list[str],
) -> None:
    validate_relationship_position_line(
        path,
        line_number,
        line,
        canonical_predicates,
        entity_types,
        errors,
    )


def validate_inline_code(
    path: Path,
    line_number: int,
    line: str,
    canonical_predicates: set[str],
    entity_types: set[str],
    errors: list[str],
) -> None:
    if line_is_ignored(line):
        return

    for match in INLINE_CODE.finditer(line):
        validate_relationship_position_line(
            path,
            line_number,
            match.group(1),
            canonical_predicates,
            entity_types,
            errors,
        )


def validate_markdown_file(
    path: Path,
    canonical_predicates: set[str],
    entity_types: set[str],
    errors: list[str],
) -> None:
    in_fence = False
    inspect_fence = False
    ignore_fence = False
    recent_nonblank_lines: list[str] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"{display(path)}: could not read file: {exc}")
        return

    for line_number, line in enumerate(lines, start=1):
        if not in_fence:
            fence = FENCE_START.match(line)
            if fence:
                in_fence = True
                language = fence.group(1).lower()
                inspect_fence = language in {"", "text"}
                ignore_fence = any(line_is_ignored(recent) for recent in recent_nonblank_lines)
                continue

            validate_inline_code(
                path,
                line_number,
                line,
                canonical_predicates,
                entity_types,
                errors,
            )
            validate_relationship_position_line(
                path,
                line_number,
                INLINE_CODE.sub(" ", line),
                canonical_predicates,
                entity_types,
                errors,
            )
            if line.strip():
                recent_nonblank_lines.append(line)
                recent_nonblank_lines = recent_nonblank_lines[-4:]
            continue

        if FENCE_END.match(line):
            in_fence = False
            inspect_fence = False
            ignore_fence = False
            continue

        if inspect_fence and not ignore_fence:
            validate_fenced_line(
                path,
                line_number,
                line,
                canonical_predicates,
                entity_types,
                errors,
            )


def run_self_test() -> int:
    errors: list[str] = []
    self_test_path = ARCHITECTURE_DOCS / "self-test.md"
    canonical_predicates = {
        predicate
        for _, predicate, _ in SELF_TEST_VALID_TRIPLES + SELF_TEST_INVALID_TRIPLES
    }
    canonical_predicates.add("CITES")
    entity_types = {
        entity_type
        for subject, _, object_ in SELF_TEST_VALID_TRIPLES + SELF_TEST_INVALID_TRIPLES
        for entity_type in (subject, object_)
    }
    entity_types.update({"Paper", "Technique", "Reference"})

    for line_number, expected_triple in enumerate(SELF_TEST_VALID_TRIPLES, start=1):
        line = " ".join(expected_triple)
        parsed = relationship_triple_in_example(
            line,
            canonical_predicates,
            entity_types,
        )
        if parsed != expected_triple:
            errors.append(
                f"self-test valid case {line!r}: parsed {parsed!r}, "
                f"expected {expected_triple!r}"
            )
            continue

        case_errors: list[str] = []
        validate_fenced_line(
            self_test_path,
            line_number,
            line,
            canonical_predicates,
            entity_types,
            case_errors,
        )
        if case_errors:
            errors.append(
                f"self-test valid case {line!r}: expected no errors, got "
                f"{case_errors!r}"
            )

    first_invalid_line_number = len(SELF_TEST_VALID_TRIPLES) + 1
    for offset, expected_triple in enumerate(SELF_TEST_INVALID_TRIPLES):
        line_number = first_invalid_line_number + offset
        line = " ".join(expected_triple)
        parsed = relationship_triple_in_example(
            line,
            canonical_predicates,
            entity_types,
        )
        if parsed != expected_triple:
            errors.append(
                f"self-test invalid case {line!r}: parsed {parsed!r}, "
                f"expected {expected_triple!r}"
            )
            continue

        case_errors: list[str] = []
        validate_fenced_line(
            self_test_path,
            line_number,
            line,
            canonical_predicates,
            entity_types,
            case_errors,
        )
        if len(case_errors) != 1:
            errors.append(
                f"self-test invalid case {line!r}: expected one error, got "
                f"{case_errors!r}"
            )
            continue

        expected_message = f"invalid relationship triple {line}; prefer "
        if expected_message not in case_errors[0]:
            errors.append(
                f"self-test invalid case {line!r}: error did not include "
                f"{expected_message!r}: {case_errors[0]!r}"
            )

    unknown_cases = (
        ("prose", validate_relationship_position_line, SELF_TEST_UNKNOWN_PREDICATE),
        ("inline", validate_inline_code, f"`{SELF_TEST_UNKNOWN_PREDICATE}`"),
        ("fenced", validate_fenced_line, SELF_TEST_UNKNOWN_PREDICATE),
    )
    for offset, (case_name, validator, line) in enumerate(unknown_cases, start=1):
        case_errors = []
        validator(
            self_test_path,
            100 + offset,
            line,
            canonical_predicates,
            entity_types,
            case_errors,
        )
        if len(case_errors) != 1:
            errors.append(
                f"self-test {case_name} unknown predicate case {line!r}: "
                f"expected one error, got {case_errors!r}"
            )
            continue
        if "unknown relationship predicate COMPARES" not in case_errors[0]:
            errors.append(
                f"self-test {case_name} unknown predicate case {line!r}: "
                f"unexpected error {case_errors[0]!r}"
            )

    valid_position_cases = (
        ("canonical single-word predicate", SELF_TEST_CANONICAL_SINGLE_WORD),
        ("ordinary acronym prose", SELF_TEST_ACRONYM_PROSE),
        ("allowed noncanonical example", SELF_TEST_ALLOWED_NONCANONICAL),
    )
    for offset, (case_name, line) in enumerate(valid_position_cases, start=1):
        case_errors = []
        validate_relationship_position_line(
            self_test_path,
            200 + offset,
            line,
            canonical_predicates,
            entity_types,
            case_errors,
        )
        if case_errors:
            errors.append(
                f"self-test valid {case_name} case {line!r}: "
                f"expected no errors, got {case_errors!r}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Documentation relationship self-test passed: "
        f"{len(SELF_TEST_VALID_TRIPLES)} valid cases, "
        f"{len(SELF_TEST_INVALID_TRIPLES)} invalid cases, "
        f"{len(unknown_cases)} unknown predicate cases, "
        f"{len(valid_position_cases)} relationship-position cases"
    )
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate architecture documentation relationship predicate mentions."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run synthetic parser and semantic guardrail checks without reading docs",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.self_test:
        return run_self_test()

    errors: list[str] = []
    canonical_predicates = load_canonical_predicates(errors)
    entity_types = load_registered_entity_types(errors)

    if canonical_predicates and entity_types:
        for path in sorted(ARCHITECTURE_DOCS.glob("*.md")):
            validate_markdown_file(path, canonical_predicates, entity_types, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Documentation relationship validation passed: "
        f"{display(ARCHITECTURE_DOCS)}/*.md"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
