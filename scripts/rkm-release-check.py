#!/usr/bin/env python3
"""Run the strict pre-tag readiness check for RKM v0.1.0-alpha."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "QUICKSTART.md",
    "CHANGELOG.md",
    "docs/releases/README.md",
    "docs/releases/v0.1.0-alpha.md",
    "docs/maintenance/consumer-guide.md",
    "docs/maintenance/maturity-report.md",
    "docs/maintenance/assistant-handoff.md",
    "examples/fixtures/fixture-manifest.json",
    "data/manifest.json",
    "examples/graph-export/minimal-graph.nodes.json",
    "examples/graph-export/minimal-graph.edges.json",
)

REQUIRED_DIRECTORIES = (
    "schema",
    "schema/definitions",
    "registries",
    "docs/architecture",
    "examples/fixtures",
    "examples/graph-export",
    "data",
    "scripts",
)


class ReleaseCheckError(Exception):
    """Raised when release readiness fails."""


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


def display_path(path: Path, root: Path = REPOSITORY_ROOT) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def run_command(args: list[str], root: Path = REPOSITORY_ROOT) -> CommandResult:
    completed = subprocess.run(
        args,
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def require_git_repository(root: Path = REPOSITORY_ROOT) -> None:
    result = run_command(["git", "rev-parse", "--show-toplevel"], root)
    if result.returncode != 0:
        raise ReleaseCheckError("Current directory is not inside a git repository.")

    actual_root = Path(result.stdout.strip()).resolve()
    if actual_root != root.resolve():
        raise ReleaseCheckError(
            f"Script resolved repository root as {root}, but git reports {actual_root}."
        )


def git_status_short(root: Path = REPOSITORY_ROOT) -> str:
    result = run_command(["git", "status", "--short"], root)
    if result.returncode != 0:
        raise ReleaseCheckError(
            "Could not inspect git status.\n"
            f"Command: git status --short\n{format_command_output(result)}"
        )
    return result.stdout


def require_clean_worktree(stage: str, root: Path = REPOSITORY_ROOT) -> None:
    status = git_status_short(root)
    if status.strip():
        raise ReleaseCheckError(
            f"Repository must be clean {stage}.\n"
            "Commit or discard intentional changes before running the release check.\n"
            "Current git status --short:\n"
            f"{status.rstrip()}"
        )


def check_head_alignment(root: Path = REPOSITORY_ROOT) -> list[str]:
    origin_ref = run_command(["git", "show-ref", "--verify", "--quiet", "refs/remotes/origin/main"], root)
    if origin_ref.returncode != 0:
        return ["WARN: origin/main is not available locally; skipped HEAD alignment check."]

    head = run_command(["git", "rev-parse", "HEAD"], root)
    origin_main = run_command(["git", "rev-parse", "refs/remotes/origin/main"], root)
    if head.returncode != 0 or origin_main.returncode != 0:
        raise ReleaseCheckError(
            "Could not resolve HEAD and origin/main for alignment check.\n"
            f"HEAD result:\n{format_command_output(head)}\n"
            f"origin/main result:\n{format_command_output(origin_main)}"
        )

    head_sha = head.stdout.strip()
    origin_main_sha = origin_main.stdout.strip()
    if head_sha != origin_main_sha:
        raise ReleaseCheckError(
            "HEAD is not aligned with origin/main.\n"
            f"HEAD:        {head_sha}\n"
            f"origin/main: {origin_main_sha}\n"
            "Update local refs and ensure the intended commit is at origin/main before tagging."
        )

    return []


def validate_required_paths(
    root: Path = REPOSITORY_ROOT,
    required_files: Sequence[str] = REQUIRED_FILES,
    required_directories: Sequence[str] = REQUIRED_DIRECTORIES,
) -> None:
    missing_files = [path for path in required_files if not (root / path).is_file()]
    missing_directories = [path for path in required_directories if not (root / path).is_dir()]

    if not missing_files and not missing_directories:
        return

    messages: list[str] = []
    if missing_files:
        messages.append("Missing required file(s):")
        messages.extend(f"- {path}" for path in missing_files)
    if missing_directories:
        messages.append("Missing required directory/directories:")
        messages.extend(f"- {path}" for path in missing_directories)
    raise ReleaseCheckError("\n".join(messages))


def format_command_output(result: CommandResult) -> str:
    parts = [f"Exit code: {result.returncode}"]
    if result.stdout.strip():
        parts.append(f"stdout:\n{result.stdout.rstrip()}")
    if result.stderr.strip():
        parts.append(f"stderr:\n{result.stderr.rstrip()}")
    return "\n".join(parts)


def run_required_command(args: list[str], description: str, root: Path = REPOSITORY_ROOT) -> None:
    print(f"==> {description}")
    result = run_command(args, root)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        raise ReleaseCheckError(
            f"Command failed: {' '.join(args)}\n{format_command_output(result)}"
        )


def run_release_check(root: Path = REPOSITORY_ROOT) -> None:
    print("==> Resolving repository root")
    print(f"Repository root: {root}")

    print("==> Checking git repository")
    require_git_repository(root)

    print("==> Checking clean repository state")
    require_clean_worktree("before release readiness validation", root)

    print("==> Checking HEAD alignment with origin/main")
    for warning in check_head_alignment(root):
        print(warning, file=sys.stderr)

    print("==> Checking required release files and directories")
    validate_required_paths(root)

    run_required_command(["make", "validate"], "Running make validate", root)
    run_required_command(["make", "graph-export"], "Running make graph-export", root)
    run_required_command(["make", "validate"], "Running make validate after graph export", root)

    print("==> Checking graph export did not dirty the worktree")
    require_clean_worktree("after graph export and validation", root)

    print("SUCCESS: RKM v0.1.0-alpha release readiness passed. Maintainers may intentionally create the git tag.")


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for relative_path in REQUIRED_FILES:
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x\n", encoding="utf-8")
        for relative_path in REQUIRED_DIRECTORIES:
            (root / relative_path).mkdir(parents=True, exist_ok=True)

        validate_required_paths(root)

        (root / "README.md").unlink()
        try:
            validate_required_paths(root)
        except ReleaseCheckError as exc:
            if "README.md" not in str(exc):
                raise ReleaseCheckError("self-test failed: missing file was not reported") from exc
        else:
            raise ReleaseCheckError("self-test failed: missing file did not fail validation")

        rel = display_path(root / "docs" / "releases" / "README.md", root)
        if rel != "docs/releases/README.md":
            raise ReleaseCheckError("self-test failed: display_path did not produce a relative path")

        formatted = format_command_output(CommandResult(7, "out\n", "err\n"))
        if "Exit code: 7" not in formatted or "stdout:" not in formatted or "stderr:" not in formatted:
            raise ReleaseCheckError("self-test failed: command output formatting is incomplete")


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        try:
            run_self_test()
        except ReleaseCheckError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print("rkm-release-check self-test passed.")
        return 0

    if len(argv) != 1:
        print("Usage: python3 scripts/rkm-release-check.py [--self-test]", file=sys.stderr)
        return 2

    try:
        run_release_check()
    except ReleaseCheckError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("Release readiness failed.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
