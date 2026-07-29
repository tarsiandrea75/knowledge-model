#!/usr/bin/env python3
"""Validate JSON fenced examples in selected Markdown files."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path


def markdown_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() == ".md" else []
    return sorted(candidate for candidate in path.rglob("*.md") if candidate.is_file())


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip().lower() != "```json":
            index += 1
            continue
        start = index + 1
        index += 1
        block: list[str] = []
        while index < len(lines) and lines[index].strip() != "```":
            block.append(lines[index])
            index += 1
        if index == len(lines):
            errors.append(f"{path}:{start}: unterminated JSON fence")
            break
        try:
            json.loads("\n".join(block))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{start + exc.lineno - 1}: invalid JSON example: {exc.msg}")
        index += 1
    return errors


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    for markdown in markdown_files(path):
        errors.extend(validate_file(markdown))
    return errors


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-markdown-json-") as directory:
        root = Path(directory)
        (root / "valid.md").write_text("```json\n{\"valid\": true}\n```\n", encoding="utf-8")
        (root / "invalid.md").write_text("```json\n{invalid}\n```\n", encoding="utf-8")
        errors = validate(root)
        assert len(errors) == 1 and "invalid.md" in errors[0], errors
    print("Markdown JSON validator self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="docs", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    errors = validate(args.path)
    if errors:
        print("Markdown JSON validation errors:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Markdown JSON validation passed: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
