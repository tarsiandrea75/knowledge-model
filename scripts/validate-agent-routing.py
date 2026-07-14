#!/usr/bin/env python3
"""Validate distributed agent rule routing."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

LOCAL_RULE_FILES = (
    "data/AGENTS.md",
    "schema/AGENTS.md",
    "registries/AGENTS.md",
    "scripts/AGENTS.md",
    "docs/architecture/AGENTS.md",
    "examples/AGENTS.md",
)

TASK_GUIDES = (
    "docs/maintenance/task-guides/README.md",
    "docs/maintenance/task-guides/unattended-autopilot.md",
    "docs/maintenance/task-guides/recovering-failed-new-file.md",
    "docs/maintenance/task-guides/writing-architecture-doc.md",
    "docs/maintenance/task-guides/adding-data-records.md",
    "docs/maintenance/task-guides/adding-new-entity-type.md",
    "docs/maintenance/task-guides/adding-relationship-set.md",
    "docs/maintenance/task-guides/adding-relationship-support.md",
    "docs/maintenance/task-guides/adding-schema-contract.md",
    "docs/maintenance/task-guides/refactoring-schema-definition.md",
    "docs/maintenance/task-guides/updating-graph-export.md",
    "docs/maintenance/task-guides/updating-validation-scripts.md",
    "docs/maintenance/task-guides/preparing-release.md",
    "docs/maintenance/task-guides/rule-routing-validation.md",
)

REQUIRED_GUIDE_HEADINGS = (
    "# ",
    "## Purpose",
    "## When to Use",
    "## Required Readings",
    "## Required Checks",
    "## Common Failure Modes",
    "## Done Criteria",
)

ROOT_REQUIRED_REFERENCES = LOCAL_RULE_FILES + (
    "docs/maintenance/automation-guardrails.md",
    "docs/maintenance/task-guides/README.md",
)

LOCAL_RULE_GUIDES = {
    "data/AGENTS.md": (
        "docs/maintenance/task-guides/adding-data-records.md",
        "docs/maintenance/task-guides/adding-new-entity-type.md",
        "docs/maintenance/task-guides/adding-relationship-set.md",
        "docs/maintenance/task-guides/adding-relationship-support.md",
    ),
    "schema/AGENTS.md": (
        "docs/maintenance/task-guides/adding-schema-contract.md",
        "docs/maintenance/task-guides/refactoring-schema-definition.md",
    ),
    "scripts/AGENTS.md": (
        "docs/maintenance/task-guides/updating-validation-scripts.md",
        "docs/maintenance/task-guides/updating-graph-export.md",
    ),
    "docs/architecture/AGENTS.md": (
        "docs/maintenance/task-guides/writing-architecture-doc.md",
    ),
    "examples/AGENTS.md": (
        "docs/maintenance/task-guides/updating-graph-export.md",
    ),
}

MAX_ROOT_AGENT_LINES = 280
DATA_PATH = re.compile(r"\bdata/[A-Za-z0-9_./-]+")
INVENTED_ID = re.compile(
    r"\b(?:TECHNIQUE|COMPONENT|RELATIONSHIP|RETRIEVER|RERANKER)-0001\b"
)


def display(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def read_text(root: Path, relative_path: str, errors: list[str]) -> str:
    path = root / relative_path
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{relative_path}: could not read file: {exc}")
        return ""


def validate_required_files(root: Path, errors: list[str]) -> None:
    for relative_path in LOCAL_RULE_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"{relative_path}: required local rule file is missing")

    for relative_path in TASK_GUIDES:
        if not (root / relative_path).is_file():
            errors.append(f"{relative_path}: required task guide is missing")


def validate_task_guide_headings(root: Path, errors: list[str]) -> None:
    for relative_path in TASK_GUIDES:
        if relative_path.endswith("/README.md"):
            continue

        path = root / relative_path
        if not path.is_file():
            continue

        text = read_text(root, relative_path, errors)
        lines = text.splitlines()

        for heading in REQUIRED_GUIDE_HEADINGS:
            if heading == "# ":
                if not any(line.startswith("# ") for line in lines):
                    errors.append(f"{relative_path}: missing top-level Markdown heading")
            elif heading not in lines:
                errors.append(f"{relative_path}: missing required heading {heading}")


def validate_root_agents(root: Path, errors: list[str]) -> None:
    relative_path = "AGENTS.md"
    path = root / relative_path
    if not path.is_file():
        errors.append("AGENTS.md: root rule file is missing")
        return

    text = read_text(root, relative_path, errors)
    line_count = len(text.splitlines())
    if line_count > MAX_ROOT_AGENT_LINES:
        errors.append(
            "AGENTS.md: root rule file exceeds 280 lines; long-form guidance "
            "belongs in local AGENTS.md files or task guides"
        )

    for required_reference in ROOT_REQUIRED_REFERENCES:
        if required_reference not in text:
            errors.append(f"AGENTS.md: missing required routing reference to {required_reference}")


def validate_local_rule_references(root: Path, errors: list[str]) -> None:
    for relative_path, guide_paths in LOCAL_RULE_GUIDES.items():
        path = root / relative_path
        if not path.is_file():
            continue

        text = read_text(root, relative_path, errors)
        if not any(guide_path in text for guide_path in guide_paths):
            joined_guides = ", ".join(guide_paths)
            errors.append(
                f"{relative_path}: must reference at least one relevant task guide: "
                f"{joined_guides}"
            )


def validate_architecture_examples(root: Path, errors: list[str]) -> None:
    architecture_dir = root / "docs" / "architecture"
    if not architecture_dir.is_dir():
        return

    for path in sorted(architecture_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if DATA_PATH.search(text) and INVENTED_ID.search(text):
            errors.append(
                f"{display(root, path)}: concrete data paths must not be mixed "
                "with invented example IDs such as TECHNIQUE-0001"
            )


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    validate_required_files(root, errors)
    validate_task_guide_headings(root, errors)
    validate_root_agents(root, errors)
    validate_local_rule_references(root, errors)
    validate_architecture_examples(root, errors)
    return errors


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def guide(title: str) -> str:
    return "\n".join(
        (
            f"# {title}",
            "",
            "## Purpose",
            "",
            "Define a focused routing rule.",
            "",
            "## When to Use",
            "",
            "Use this guide for matching work.",
            "",
            "## Required Readings",
            "",
            "- `AGENTS.md`.",
            "",
            "## Required Checks",
            "",
            "- Run the relevant validation command.",
            "",
            "## Common Failure Modes",
            "",
            "- Missing the local rule file.",
            "",
            "## Done Criteria",
            "",
            "- Validation passed.",
            "",
        )
    )


def populate_valid_fixture(root: Path) -> None:
    for relative_path in LOCAL_RULE_FILES:
        guide_path = LOCAL_RULE_GUIDES.get(relative_path, TASK_GUIDES[:1])[0]
        write(
            root / relative_path,
            "\n".join(
                (
                    "# Local Rules",
                    "",
                    "## Required Task Guides",
                    "",
                    f"- `{guide_path}`",
                    "",
                )
            ),
        )

    write(
        root / "AGENTS.md",
        "\n".join(
            (
                "# Root Rules",
                "",
                "Routing references:",
                *(f"- `{reference}`" for reference in ROOT_REQUIRED_REFERENCES),
                "",
            )
        ),
    )

    for relative_path in TASK_GUIDES:
        title = Path(relative_path).stem.replace("-", " ").title()
        content = "# RKM Task Guides\n\n" if relative_path.endswith("/README.md") else guide(title)
        write(root / relative_path, content)

    write(root / "docs" / "architecture" / "model.md", "# Model\n\nAbstract example only.\n")


def expect_failure(name: str, root: Path, expected_fragment: str) -> None:
    errors = validate(root)
    if not any(expected_fragment in error for error in errors):
        details = "\n".join(errors) if errors else "validation unexpectedly passed"
        raise AssertionError(f"{name}: expected {expected_fragment!r}; got:\n{details}")


def run_self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-agent-routing-") as temp_dir:
        base = Path(temp_dir)

        valid = base / "valid"
        populate_valid_fixture(valid)
        errors = validate(valid)
        if errors:
            raise AssertionError("valid minimal repository fixture failed:\n" + "\n".join(errors))

        missing_local = base / "missing-local"
        shutil.copytree(valid, missing_local)
        (missing_local / "data" / "AGENTS.md").unlink()
        expect_failure(
            "missing local rule file failure",
            missing_local,
            "data/AGENTS.md: required local rule file is missing",
        )

        missing_heading = base / "missing-heading"
        shutil.copytree(valid, missing_heading)
        write(
            missing_heading / "docs/maintenance/task-guides/adding-data-records.md",
            "# Adding Data Records\n\n## Purpose\n\nBroken guide.\n",
        )
        expect_failure(
            "missing task guide heading failure",
            missing_heading,
            "missing required heading ## When to Use",
        )

        oversized_root = base / "oversized-root"
        shutil.copytree(valid, oversized_root)
        root_lines = ["# Root Rules", *ROOT_REQUIRED_REFERENCES, *(f"Line {index}" for index in range(300))]
        write(oversized_root / "AGENTS.md", "\n".join(root_lines) + "\n")
        expect_failure(
            "oversized root AGENTS failure",
            oversized_root,
            "root rule file exceeds 280 lines",
        )

        bad_example = base / "bad-example"
        shutil.copytree(valid, bad_example)
        write(
            bad_example / "docs/architecture/model.md",
            "# Model\n\n`data/techniques/example.json` contains `TECHNIQUE-0001`.\n",
        )
        expect_failure(
            "bad concrete-path plus invented-ID example failure",
            bad_example,
            "concrete data paths must not be mixed",
        )

    print("Agent routing validation self-test passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run validator self-tests against temporary fixtures",
    )
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0

    errors = validate(REPOSITORY_ROOT)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Agent routing validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
