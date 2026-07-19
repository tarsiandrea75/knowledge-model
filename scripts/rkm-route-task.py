#!/usr/bin/env python3
"""Map intended RKM file changes to required readings and checks."""

from __future__ import annotations

import argparse
import shlex
import sys
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Sequence


BASE_READINGS = (
    "AGENTS.md",
    "docs/maintenance/automation-guardrails.md",
    "docs/maintenance/rule-coverage-report.md",
    "docs/maintenance/governance-backlog.md",
)

RISK_HIGH = (
    "Schema, registry, validator, exporter, Makefile, release-process, "
    "graph-contract, and migration paths are high-risk and require explicit prompts."
)
RISK_DATA = (
    "Data-only additions are lower risk only when using existing entity types and "
    "existing validation paths."
)
RISK_DATA_MANIFEST = (
    "Adding data records may require updating data/manifest.json, even when the "
    "primary intended change is data-only."
)
RISK_DATA_GRAPH_EXPORT = (
    "Adding data records may require regenerating or updating "
    "examples/data-graph-export/*.nodes.json and "
    "examples/data-graph-export/*.edges.json."
)
RISK_ARCHITECTURE = (
    "Architecture docs require checking nearby existing docs to avoid duplicate authority."
)
RISK_ROUTING = (
    "Rule routing changes must keep root rules, local AGENTS files, task guides, "
    "and routing validation aligned."
)


@dataclass(frozen=True)
class RouteResult:
    readings: Sequence[str] = ()
    guides: Sequence[str] = ()
    notes: Sequence[str] = ()
    checks: Sequence[str] = ()


def normalize_path(path: str) -> str:
    normalized = str(PurePosixPath(path.replace("\\", "/")))
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_under(path: str, prefix: str) -> bool:
    return path == prefix.rstrip("/") or path.startswith(prefix.rstrip("/") + "/")


def is_local_agents_file(path: str) -> bool:
    return path == "AGENTS.md" or path.endswith("/AGENTS.md")


def is_graph_export_path(path: str) -> bool:
    graph_scripts = {
        "scripts/export-fixtures-graph.py",
        "scripts/export-data-graph.py",
        "scripts/validate-graph-exports.py",
    }
    graph_contracts = {
        "schema/graph-node.schema.json",
        "schema/graph-edge.schema.json",
        "docs/maintenance/graph-export-contract.md",
    }
    return (
        path in graph_scripts
        or path in graph_contracts
        or is_under(path, "examples/graph-export")
        or is_under(path, "examples/data-graph-export")
    )


def is_release_path(path: str) -> bool:
    return (
        is_under(path, "docs/releases")
        or path == "CHANGELOG.md"
        or path == "scripts/rkm-release-check.py"
        or path == "docs/maintenance/task-guides/preparing-release.md"
    )


def is_high_risk_path(path: str) -> bool:
    return (
        is_under(path, "schema")
        or is_under(path, "registries")
        or is_under(path, "scripts")
        or path == "Makefile"
        or is_release_path(path)
        or is_graph_export_path(path)
        or "migration" in path
    )


def add_unique(items: list[str], values: Sequence[str]) -> None:
    for value in values:
        if value not in items:
            items.append(value)


def route_one(path: str) -> RouteResult:
    readings: list[str] = []
    guides: list[str] = []
    notes: list[str] = []
    checks: list[str] = []

    if is_under(path, "data"):
        add_unique(readings, ("data/AGENTS.md",))
        add_unique(guides, ("docs/maintenance/task-guides/adding-data-records.md",))
        add_unique(notes, (RISK_DATA, RISK_DATA_MANIFEST, RISK_DATA_GRAPH_EXPORT))
        add_unique(checks, ("make data-validate", "make data-graph-export", "make graph-export-validate"))

    if is_under(path, "data/relationships"):
        add_unique(readings, ("data/AGENTS.md",))
        add_unique(guides, ("docs/maintenance/task-guides/adding-relationship-set.md",))
        add_unique(checks, ("make data-validate",))

    if is_under(path, "data/relationship-support"):
        add_unique(readings, ("data/AGENTS.md",))
        add_unique(guides, ("docs/maintenance/task-guides/adding-relationship-support.md",))
        add_unique(checks, ("make data-validate",))

    if is_under(path, "schema"):
        add_unique(readings, ("schema/AGENTS.md",))
        add_unique(guides, ("docs/maintenance/task-guides/adding-schema-contract.md",))
        add_unique(checks, ("make schema-duplicate-contracts-validate",))

    if is_under(path, "schema/definitions"):
        add_unique(readings, ("schema/AGENTS.md",))
        add_unique(guides, ("docs/maintenance/task-guides/refactoring-schema-definition.md",))
        add_unique(checks, ("make schema-duplicate-contracts-validate",))

    if is_under(path, "registries"):
        add_unique(readings, ("registries/AGENTS.md",))

    if is_under(path, "scripts"):
        add_unique(readings, ("scripts/AGENTS.md",))
        add_unique(guides, ("docs/maintenance/task-guides/updating-validation-scripts.md",))

    if is_graph_export_path(path):
        add_unique(guides, ("docs/maintenance/task-guides/updating-graph-export.md",))
        add_unique(checks, ("make graph-export-validate",))

    if is_under(path, "docs/architecture"):
        add_unique(readings, ("docs/architecture/AGENTS.md",))
        add_unique(guides, ("docs/maintenance/task-guides/writing-architecture-doc.md",))
        add_unique(notes, (RISK_ARCHITECTURE,))

    if is_under(path, "examples"):
        add_unique(readings, ("examples/AGENTS.md",))

    if is_release_path(path):
        add_unique(guides, ("docs/maintenance/task-guides/preparing-release.md",))

    if is_under(path, "docs/maintenance/task-guides") or is_local_agents_file(path):
        add_unique(guides, ("docs/maintenance/task-guides/rule-routing-validation.md",))
        add_unique(notes, (RISK_ROUTING,))
        add_unique(checks, ("make agent-routing-validate",))

    if is_high_risk_path(path):
        add_unique(notes, (RISK_HIGH,))

    return RouteResult(tuple(readings), tuple(guides), tuple(notes), tuple(checks))


def route_paths(paths: list[str]) -> RouteResult:
    readings = list(BASE_READINGS)
    guides: list[str] = []
    notes: list[str] = []
    checks = ["make validate"]

    for path in paths:
        result = route_one(path)
        add_unique(readings, result.readings)
        add_unique(guides, result.guides)
        add_unique(notes, result.notes)
        add_unique(checks, result.checks)

    if not guides:
        guides.append("No additional task guides selected by the input paths.")
    if not notes:
        notes.append("Review path ownership and nearby conventions before editing.")

    return RouteResult(tuple(readings), tuple(guides), tuple(notes), tuple(checks))


def bullet_list(items: Sequence[str]) -> str:
    return "\n".join(f"- `{item}`" if item.startswith(("AGENTS", "data/", "docs/", "schema/", "registries/", "scripts/", "examples/", "Makefile", "make ")) else f"- {item}" for item in items)


def build_report(paths: list[str]) -> str:
    normalized_paths = [normalize_path(path) for path in paths]
    result = route_paths(normalized_paths)
    return "\n".join(
        (
            "# RKM Task Routing",
            "",
            "## Input Paths",
            "",
            bullet_list(tuple(normalized_paths)),
            "",
            "## Required Readings",
            "",
            bullet_list(result.readings),
            "",
            "## Suggested Task Guides",
            "",
            bullet_list(result.guides),
            "",
            "## Risk Notes",
            "",
            bullet_list(result.notes),
            "",
            "## Required Checks",
            "",
            bullet_list(result.checks),
            "",
        )
    )


def parse_paths(raw_paths: list[str] | None) -> list[str]:
    if not raw_paths:
        return []

    paths: list[str] = []
    for raw_path in raw_paths:
        paths.extend(shlex.split(raw_path))
    return [path for path in paths if path]


def assert_contains(report: str, expected: Sequence[str]) -> None:
    for value in expected:
        if value not in report:
            raise AssertionError(f"Expected route output to contain {value}")


def assert_occurs_once(report: str, value: str) -> None:
    line = f"- `{value}`"
    if report.splitlines().count(line) != 1:
        raise AssertionError(f"Expected route output to contain {value} exactly once")


def run_self_test() -> None:
    cases = (
        (
            ["data/rag-techniques/hybrid-retrieval.json"],
            (
                "data/AGENTS.md",
                "docs/maintenance/task-guides/adding-data-records.md",
                "data/manifest.json",
                "examples/data-graph-export/*.nodes.json",
                "examples/data-graph-export/*.edges.json",
                "make data-validate",
                "make data-graph-export",
                "make graph-export-validate",
            ),
        ),
        (
            ["data/relationships/technique-component-relationships.json"],
            ("docs/maintenance/task-guides/adding-relationship-set.md", "make data-validate"),
        ),
        (
            ["data/relationship-support/technique-component-support.json"],
            ("docs/maintenance/task-guides/adding-relationship-support.md", "make data-validate"),
        ),
        (
            ["schema/foo.schema.json"],
            ("schema/AGENTS.md", "docs/maintenance/task-guides/adding-schema-contract.md", "make schema-duplicate-contracts-validate"),
        ),
        (
            ["schema/definitions/foo.schema.json"],
            ("docs/maintenance/task-guides/refactoring-schema-definition.md", "make schema-duplicate-contracts-validate"),
        ),
        (
            ["scripts/validate-data.py"],
            ("scripts/AGENTS.md", "docs/maintenance/task-guides/updating-validation-scripts.md"),
        ),
        (
            ["scripts/export-data-graph.py"],
            ("docs/maintenance/task-guides/updating-graph-export.md", "make graph-export-validate"),
        ),
        (
            ["docs/architecture/model.md"],
            ("docs/architecture/AGENTS.md", "docs/maintenance/task-guides/writing-architecture-doc.md"),
        ),
        (
            ["examples/fixtures/minimal-rag-technique.json"],
            ("examples/AGENTS.md",),
        ),
        (
            ["docs/releases/v0.2.0.md"],
            ("docs/maintenance/task-guides/preparing-release.md",),
        ),
        (
            ["data/AGENTS.md"],
            ("docs/maintenance/task-guides/rule-routing-validation.md", "make agent-routing-validate"),
        ),
    )

    for paths, expected in cases:
        assert_contains(build_report(paths), expected)

    mixed_report = build_report(
        [
            "schema/foo.schema.json",
            "schema/definitions/foo.schema.json",
            "data/rag-techniques/hybrid-retrieval.json",
            "data/relationships/technique-component-relationships.json",
            "docs/maintenance/task-guides/README.md",
        ]
    )
    assert_occurs_once(mixed_report, "AGENTS.md")
    assert_occurs_once(mixed_report, "schema/AGENTS.md")
    assert_occurs_once(mixed_report, "data/AGENTS.md")
    assert_occurs_once(mixed_report, "make validate")
    assert_occurs_once(mixed_report, "make data-validate")
    assert_occurs_once(mixed_report, "make data-graph-export")
    assert_occurs_once(mixed_report, "make graph-export-validate")
    assert_occurs_once(mixed_report, "make schema-duplicate-contracts-validate")
    assert_occurs_once(mixed_report, "docs/maintenance/task-guides/rule-routing-validation.md")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", nargs="+", help="One or more intended changed paths.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in self-tests.")
    args = parser.parse_args(argv)

    if args.self_test:
        run_self_test()
        print("Task router self-test passed.")
        return 0

    paths = parse_paths(args.paths)
    if not paths:
        parser.error("--paths requires one or more paths")

    print(build_report(paths), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
