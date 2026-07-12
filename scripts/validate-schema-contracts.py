#!/usr/bin/env python3
"""Validate recurring semantic contracts in RKM JSON Schemas."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


JsonPath = list[str | int]
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = REPOSITORY_ROOT / "schema"
DEFINITIONS_ROOT = SCHEMA_ROOT / "definitions"

BAD_ENTITY_TYPE_REFS = {
    "entity-type.schema.json",
    "./entity-type.schema.json",
    "../entity-type.schema.json",
}

ANNOTATION_KEYS = {
    "$comment",
    "description",
    "examples",
    "title",
}

FIRST_CLASS_ENTITY_PHRASES = (
    "complete first-class entity schema",
    "first-class entity schema",
    "complete entity schema",
    "knowledge entity schema",
)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    level: str
    file_path: Path
    json_path: str
    message: str

    def format(self, repo_root: Path) -> str:
        try:
            display_path = self.file_path.relative_to(repo_root)
        except ValueError:
            display_path = self.file_path
        return (
            f"{self.level} {self.rule_id}: {display_path}: "
            f"{self.json_path}: {self.message}"
        )


def repository_schema_files(repo_root: Path) -> list[Path]:
    files = list((repo_root / "schema").glob("*.schema.json"))
    files.extend((repo_root / "schema" / "definitions").glob("*.schema.json"))
    return sorted(files)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def path_part(part: str | int) -> str:
    if isinstance(part, int):
        return str(part)
    return part.replace("~", "~0").replace("/", "~1")


def json_path(parts: Iterable[str | int]) -> str:
    items = list(parts)
    if not items:
        return "$"
    return "$/" + "/".join(path_part(part) for part in items)


def walk_json(value: object, path: JsonPath | None = None) -> Iterable[tuple[object, JsonPath]]:
    if path is None:
        path = []
    yield value, path
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_json(child, path + [key])
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_json(child, path + [index])


def is_entity_type_property(path: JsonPath) -> bool:
    return bool(path) and path[-1] == "entityType"


def check_sc001(document: object, file_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for node, path in walk_json(document):
        if not isinstance(node, dict):
            continue
        if not is_entity_type_property(path):
            continue
        reference = node.get("$ref")
        if reference in BAD_ENTITY_TYPE_REFS:
            findings.append(
                Finding(
                    "SC001",
                    "ERROR",
                    file_path,
                    json_path(path + ["$ref"]),
                    (
                        "entityType $ref points to the entity type schema object or "
                        "registry shape, not a string entity-type vocabulary value. "
                        "Use an existing shared string entity-type definition such as "
                        "relationship.schema.json#/$defs/entityType when appropriate."
                    ),
                )
            )
    return findings


def simple_type_branch(value: object, type_name: str) -> bool:
    if not isinstance(value, dict):
        return False
    if value.get("type") != type_name:
        return False
    return all(key == "type" or key in ANNOTATION_KEYS for key in value)


def check_sc002(document: object, file_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for node, path in walk_json(document):
        if not isinstance(node, dict):
            continue
        one_of = node.get("oneOf")
        if not isinstance(one_of, list):
            continue
        has_number = any(simple_type_branch(branch, "number") for branch in one_of)
        has_integer = any(simple_type_branch(branch, "integer") for branch in one_of)
        if has_number and has_integer:
            findings.append(
                Finding(
                    "SC002",
                    "ERROR",
                    file_path,
                    json_path(path + ["oneOf"]),
                    (
                        "oneOf contains simple number and integer branches. Integer "
                        "values also satisfy number, causing oneOf ambiguity."
                    ),
                )
            )
    return findings


def is_exact_four_digit_rkm_identifier_pattern(pattern: str) -> bool:
    return pattern.endswith("-[0-9]{4}$") or pattern.endswith("-[0-9]{4}\\b")


def check_sc003(document: object, file_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    for node, path in walk_json(document):
        if not isinstance(node, dict):
            continue
        pattern = node.get("pattern")
        if isinstance(pattern, str) and is_exact_four_digit_rkm_identifier_pattern(pattern):
            findings.append(
                Finding(
                    "SC003",
                    "ERROR",
                    file_path,
                    json_path(path + ["pattern"]),
                    (
                        "RKM-style identifier pattern ends with exactly four digits. "
                        "Use {4,} when the identifier convention requires four or more digits."
                    ),
                )
            )
    return findings


def contains_knowledge_entity_reference(value: object) -> bool:
    for node, _path in walk_json(value):
        if isinstance(node, dict):
            reference = node.get("$ref")
            if isinstance(reference, str) and "knowledge-entity.schema.json" in reference:
                return True
    return False


def claims_complete_entity_schema(document: object) -> bool:
    if not isinstance(document, dict):
        return False
    text_parts = []
    for key in ("title", "description"):
        value = document.get(key)
        if isinstance(value, str):
            text_parts.append(value.lower())
    text = "\n".join(text_parts)
    return any(phrase in text for phrase in FIRST_CLASS_ENTITY_PHRASES)


def check_sc004(document: object, file_path: Path) -> list[Finding]:
    if file_path.parent.name != "definitions":
        return []
    if not claims_complete_entity_schema(document):
        return []
    if contains_knowledge_entity_reference(document):
        return []
    return [
        Finding(
            "SC004",
            "WARNING",
            file_path,
            "$",
            (
                "definition schema title or description appears to claim complete "
                "first-class entity semantics without composing the shared "
                "knowledge-entity envelope. This warning is conservative and does not fail validation."
            ),
        )
    ]


def validate_document(document: object, file_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(check_sc001(document, file_path))
    findings.extend(check_sc002(document, file_path))
    findings.extend(check_sc003(document, file_path))
    findings.extend(check_sc004(document, file_path))
    return findings


def validate_repository(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for file_path in repository_schema_files(repo_root):
        document = load_json(file_path)
        findings.extend(validate_document(document, file_path))
    return findings


def hard_findings(findings: Iterable[Finding]) -> list[Finding]:
    return [finding for finding in findings if finding.level == "ERROR"]


def print_findings(findings: Iterable[Finding], repo_root: Path) -> None:
    for finding in findings:
        print(finding.format(repo_root))


def assert_self_test(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)


def self_test() -> None:
    fake_schema = REPOSITORY_ROOT / "schema" / "fake.schema.json"
    fake_definition = REPOSITORY_ROOT / "schema" / "definitions" / "fake.schema.json"

    sc001_bad = {
        "properties": {
            "entityReference": {
                "properties": {
                    "entityType": {"$ref": "../entity-type.schema.json"}
                }
            }
        }
    }
    assert_self_test(
        "SC001 catches bad entityType ref",
        bool(hard_findings(validate_document(sc001_bad, fake_schema))),
    )

    sc001_good = {
        "properties": {
            "entityReference": {
                "properties": {
                    "entityType": {"$ref": "relationship.schema.json#/$defs/entityType"}
                }
            }
        }
    }
    assert_self_test(
        "SC001 allows shared string entity-type definition",
        not hard_findings(validate_document(sc001_good, fake_schema)),
    )

    sc002_bad = {"oneOf": [{"type": "number"}, {"type": "integer"}]}
    assert_self_test(
        "SC002 catches number and integer oneOf overlap",
        bool(hard_findings(validate_document(sc002_bad, fake_schema))),
    )

    sc002_good = {
        "properties": {
            "typeArray": {"type": ["number", "integer"]},
            "oneOf": {
                "oneOf": [
                    {"type": "number"},
                    {"type": "string"},
                    {"type": "boolean"},
                ]
            },
        }
    }
    assert_self_test(
        "SC002 allows type array and oneOf without integer branch",
        not hard_findings(validate_document(sc002_good, fake_schema)),
    )

    sc003_bad = {"properties": {"id": {"pattern": "^rkm-[a-z]+-[0-9]{4}$"}}}
    assert_self_test(
        "SC003 catches exact four-digit RKM identifier pattern",
        bool(hard_findings(validate_document(sc003_bad, fake_schema))),
    )

    sc003_good = {
        "properties": {
            "version": {"pattern": "^[0-9]{4}$"},
            "id": {"pattern": "^rkm-[a-z]+-[0-9]{4,}$"},
        }
    }
    assert_self_test(
        "SC003 ignores unrelated and four-or-more regexes",
        not hard_findings(validate_document(sc003_good, fake_schema)),
    )

    sc004_warning = {
        "title": "RKM Example First-Class Entity Schema",
        "description": "A complete entity schema for an example.",
    }
    sc004_findings = validate_document(sc004_warning, fake_definition)
    assert_self_test(
        "SC004 warning is emitted",
        any(finding.rule_id == "SC004" and finding.level == "WARNING" for finding in sc004_findings),
    )
    assert_self_test(
        "SC004 warning does not fail",
        not hard_findings(sc004_findings),
    )

    print("Schema contract self-test passed.")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate semantic contracts in RKM JSON Schema files."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run in-memory validator checks.",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    findings = validate_repository(REPOSITORY_ROOT)
    print_findings(findings, REPOSITORY_ROOT)
    errors = hard_findings(findings)
    if errors:
        print(f"Schema contract validation failed with {len(errors)} error(s).")
        return 1
    print("Schema contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
