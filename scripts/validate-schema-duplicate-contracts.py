#!/usr/bin/env python3
"""Validate duplicate first-class and reusable schema contract names."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ValidationError:
    path: Path
    message: str

    def format(self, repo_root: Path) -> str:
        return f"{display_path(self.path, repo_root)}: {self.message}"


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def load_json(path: Path) -> tuple[object | None, ValidationError | None]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle), None
    except json.JSONDecodeError as exc:
        return None, ValidationError(
            path,
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
        )


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def first_class_schema_files(repo_root: Path) -> dict[str, Path]:
    schema_root = repo_root / "schema"
    return {
        path.name.removesuffix(".schema.json"): path
        for path in sorted(schema_root.glob("*.schema.json"))
    }


def definition_schema_files(repo_root: Path) -> dict[str, Path]:
    definitions_root = repo_root / "schema" / "definitions"
    return {
        path.name.removesuffix(".schema.json"): path
        for path in sorted(definitions_root.glob("*.schema.json"))
    }


def walk_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_strings(child)


def normalize_reference(value: str) -> str:
    path_part = value.split("#", 1)[0]
    path_part = path_part.replace("\\", "/")
    while path_part.startswith("./"):
        path_part = path_part[2:]
    return path_part


def references_matching_definition(document: object, definition_name: str) -> bool:
    expected_suffix = f"definitions/{definition_name}.schema.json"
    for value in walk_strings(document):
        reference = normalize_reference(value)
        if reference == expected_suffix:
            return True
        if reference.endswith(f"/{expected_suffix}"):
            return True
    return False


def validate_repository(repo_root: Path) -> list[ValidationError]:
    errors: list[ValidationError] = []
    first_class_schemas = first_class_schema_files(repo_root)
    definition_schemas = definition_schema_files(repo_root)

    for name, definition_path in definition_schemas.items():
        first_class_path = first_class_schemas.get(name)
        if first_class_path is None:
            continue

        document, error = load_json(first_class_path)
        if error is not None:
            errors.append(error)
            continue

        if references_matching_definition(document, name):
            continue

        errors.append(
            ValidationError(
                first_class_path,
                (
                    "same-name reusable definition exists at "
                    f"{display_path(definition_path, repo_root)}, but this first-class schema "
                    "does not visibly compose from it. The same commit must either compose "
                    "the first-class schema from the reusable definition or rename/remove "
                    "the duplicate definition."
                ),
            )
        )

    return errors


def print_errors(errors: Iterable[ValidationError], repo_root: Path) -> None:
    for error in errors:
        print(error.format(repo_root), file=sys.stderr)


def assert_self_test(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)


def self_test() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir)

        write_json(
            repo_root / "schema" / "definitions" / "metadata.schema.json",
            {"type": "object"},
        )
        assert_self_test(
            "definition without same-name first-class schema is valid",
            not validate_repository(repo_root),
        )

        write_json(
            repo_root / "schema" / "benchmark.schema.json",
            {
                "allOf": [
                    {"$ref": "definitions/benchmark.schema.json"},
                    {"type": "object"},
                ]
            },
        )
        write_json(
            repo_root / "schema" / "definitions" / "benchmark.schema.json",
            {"type": "object"},
        )
        assert_self_test(
            "first-class schema referencing same-name definition is valid",
            not validate_repository(repo_root),
        )

        write_json(repo_root / "schema" / "dataset.schema.json", {"type": "object"})
        write_json(
            repo_root / "schema" / "definitions" / "dataset.schema.json",
            {"type": "object"},
        )
        duplicate_errors = validate_repository(repo_root)
        formatted_duplicate_errors = "\n".join(
            error.format(repo_root) for error in duplicate_errors
        )
        assert_self_test(
            "same-name schema and definition without reference is invalid",
            "schema/dataset.schema.json" in formatted_duplicate_errors
            and "schema/definitions/dataset.schema.json" in formatted_duplicate_errors,
        )
        assert_self_test(
            "duplicate error explains required remediation",
            "compose the first-class schema from the reusable definition"
            in formatted_duplicate_errors
            and "rename/remove the duplicate definition" in formatted_duplicate_errors,
        )

    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir)
        schema_root = repo_root / "schema"
        definitions_root = schema_root / "definitions"
        definitions_root.mkdir(parents=True)
        (schema_root / "broken.schema.json").write_text("{\n", encoding="utf-8")
        write_json(definitions_root / "broken.schema.json", {"type": "object"})
        invalid_json_errors = validate_repository(repo_root)
        formatted_invalid_json_errors = "\n".join(
            error.format(repo_root) for error in invalid_json_errors
        )
        assert_self_test(
            "invalid JSON is reported",
            "schema/broken.schema.json" in formatted_invalid_json_errors
            and "invalid JSON at line" in formatted_invalid_json_errors,
        )

    print("Schema duplicate contract self-test passed.")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate duplicate RKM first-class and reusable schema contracts."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run validator self-tests using temporary directories.",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        self_test()
        return 0

    errors = validate_repository(REPOSITORY_ROOT)
    if errors:
        print_errors(errors, REPOSITORY_ROOT)
        print(
            f"Schema duplicate contract validation failed with {len(errors)} error(s).",
            file=sys.stderr,
        )
        return 1

    print("Schema duplicate contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
