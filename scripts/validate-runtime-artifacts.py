#!/usr/bin/env python3
"""Reject repository-local runtime logs, scratch files, and run artifacts."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path


FORBIDDEN_DIRECTORY_NAMES = {
    ".rkm-runs",
    "rkm-runs",
    "runtime-logs",
    "scratch",
    "transcripts",
}
FORBIDDEN_FILE_SUFFIXES = (
    ".log",
    ".out",
    ".trace",
    ".transcript",
    ".tmp",
    ".temp",
    ".scratch",
)
FORBIDDEN_FILE_PREFIXES = (
    "rkm-autopilot-",
    "rkm-cycle-output",
    "rkm-discovery-",
    "codex-run-",
)


def _is_forbidden(path: Path, root: Path) -> str | None:
    relative = path.relative_to(root)
    parts = relative.parts
    if ".git" in parts:
        return None

    if any(part in FORBIDDEN_DIRECTORY_NAMES for part in parts[:-1]):
        return "runtime directory"

    name = path.name
    if name.startswith(FORBIDDEN_FILE_PREFIXES):
        return "generated runtime artifact"
    if name.endswith(FORBIDDEN_FILE_SUFFIXES):
        return "runtime file suffix"
    return None


def find_violations(root: Path) -> list[tuple[str, str]]:
    violations: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        reason = _is_forbidden(path, root)
        if reason is not None:
            violations.append((path.relative_to(root).as_posix(), reason))
    return violations


def _self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-runtime-artifacts-") as temporary:
        root = Path(temporary)
        (root / "docs").mkdir()
        (root / ".git").mkdir()
        (root / "runtime-logs" / "nested").mkdir(parents=True)
        (root / "docs" / "README.md").write_text("valid\n", encoding="utf-8")
        (root / ".git" / "ignored.log").write_text("ignored\n", encoding="utf-8")
        (root / "runtime-logs" / "nested" / "session.log").write_text("bad\n", encoding="utf-8")
        (root / "rkm-discovery-report-1.zip").write_text("bad\n", encoding="utf-8")
        (root / "notes.tmp").write_text("bad\n", encoding="utf-8")

        violations = find_violations(root)
        paths = {path for path, _ in violations}
        expected = {
            "runtime-logs/nested/session.log",
            "rkm-discovery-report-1.zip",
            "notes.tmp",
        }
        assert paths == expected, (paths, expected)
        assert ".git/ignored.log" not in paths
        assert "docs/README.md" not in paths

    print("runtime artifact validator self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run deterministic validator self-tests")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0

    root = Path(__file__).resolve().parents[1]
    violations = find_violations(root)
    if violations:
        print("Repository-local runtime artifacts detected:")
        for path, reason in violations:
            print(f"- {path}: {reason}")
        print("Move runtime output to /tmp/rkm-runs and remove the repository-local artifact.")
        return 1

    print("runtime artifact validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
