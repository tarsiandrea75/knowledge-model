#!/usr/bin/env python3
"""Print the next safe operational action for the local RKM repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = 3
DEFAULT_ESTIMATED_BUDGET = 0


@dataclass(frozen=True)
class CommandResult:
    code: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class RepoSnapshot:
    status_lines: list[str]
    branch: str | None
    head: str | None
    upstream: str | None
    ahead: int | None
    behind: int | None
    budget_profile_exists: bool
    ledger_exists: bool
    latest_ledger_final_status: str | None
    latest_ledger_entries: list[dict[str, Any]]
    budget_check: CommandResult | None
    budget_report: CommandResult | None
    target: int


@dataclass(frozen=True)
class Decision:
    status: str
    budget_status: str
    next_action: str
    command: str


def run_command(args: list[str], repo_root: Path = REPOSITORY_ROOT) -> CommandResult:
    completed = subprocess.run(
        args,
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return CommandResult(completed.returncode, completed.stdout.strip(), completed.stderr.strip())


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def git_status_lines(repo_root: Path = REPOSITORY_ROOT) -> list[str]:
    result = run_command(["git", "status", "--short"], repo_root)
    if result.code != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def git_text(args: list[str], repo_root: Path = REPOSITORY_ROOT) -> str | None:
    result = run_command(args, repo_root)
    if result.code != 0 or not result.stdout:
        return None
    return result.stdout.strip()


def upstream_counts(repo_root: Path = REPOSITORY_ROOT) -> tuple[str | None, int | None, int | None]:
    upstream = git_text(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], repo_root)
    if upstream is None:
        return None, None, None

    revision_range = "HEAD" + "." * 3 + "@{upstream}"
    counts = git_text(["git", "rev-list", "--left-right", "--count", revision_range], repo_root)
    if counts is None:
        return upstream, None, None

    parts = counts.split()
    if len(parts) != 2:
        return upstream, None, None
    try:
        return upstream, int(parts[0]), int(parts[1])
    except ValueError:
        return upstream, None, None


def read_ledger_entries(ledger_path: Path, limit: int = 5) -> list[dict[str, Any]]:
    if not ledger_path.exists():
        return []

    entries: list[dict[str, Any]] = []
    with ledger_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                document = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if isinstance(document, dict):
                entries.append(document)
    return entries[-limit:]


def collect_snapshot(target: int, repo_root: Path = REPOSITORY_ROOT) -> RepoSnapshot:
    branch = git_text(["git", "branch", "--show-current"], repo_root)
    head = git_text(["git", "rev-parse", "--short", "HEAD"], repo_root)
    upstream, ahead, behind = upstream_counts(repo_root)
    budget_profile = repo_root / ".rkm" / "budget-profile.json"
    ledger = repo_root / ".rkm" / "run-ledger.jsonl"
    latest_ledger_entries = read_ledger_entries(ledger)
    latest_final_status = latest_ledger_entries[-1].get("finalStatus") if latest_ledger_entries else None
    if not isinstance(latest_final_status, str):
        latest_final_status = None

    budget_check = None
    budget_report = None
    if budget_profile.exists():
        budget_check = run_command(["python3", "scripts/rkm-budget.py", "check", "--target", str(target)], repo_root)
        budget_report = run_command(["python3", "scripts/rkm-budget.py", "report"], repo_root)

    return RepoSnapshot(
        status_lines=git_status_lines(repo_root),
        branch=branch,
        head=head,
        upstream=upstream,
        ahead=ahead,
        behind=behind,
        budget_profile_exists=budget_profile.exists(),
        ledger_exists=ledger.exists(),
        latest_ledger_final_status=latest_final_status,
        latest_ledger_entries=latest_ledger_entries,
        budget_check=budget_check,
        budget_report=budget_report,
        target=target,
    )


def status_path(status_line: str) -> str:
    if len(status_line) >= 3 and status_line[2] == " ":
        path = status_line[3:].strip()
    else:
        parts = status_line.split(maxsplit=1)
        path = parts[1].strip() if len(parts) == 2 else ""
    if " -> " in path:
        path = path.rsplit(" -> ", 1)[1]
    return path.rstrip("/")


def is_ide_status_line(status_line: str) -> bool:
    path = status_path(status_line)
    return path == ".idea" or path.startswith(".idea/") or path.endswith("/.idea")


def changed_project_files(status_lines: list[str]) -> list[str]:
    paths: list[str] = []
    for line in status_lines:
        path = status_path(line)
        if not path or is_ide_status_line(line):
            continue
        if path.startswith(".rkm/"):
            continue
        paths.append(path)
    return paths


def ide_files(status_lines: list[str]) -> list[str]:
    return [status_path(line) for line in status_lines if is_ide_status_line(line)]


def repo_has_dirty_files(snapshot: RepoSnapshot) -> bool:
    return bool(snapshot.status_lines)


def parse_budget_status(result: CommandResult | None) -> str:
    if result is None:
        return "unavailable"
    text = "\n".join(part for part in (result.stdout, result.stderr) if part)
    match = re.search(r"^status:\s*(.+)$", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    if result.code == 0:
        return "available"
    return f"unavailable (exit {result.code})"


def parse_suggested_command(*results: CommandResult | None) -> str | None:
    for result in results:
        if result is None:
            continue
        text = "\n".join(part for part in (result.stdout, result.stderr) if part)
        for line in text.splitlines():
            prefix = "suggested command:"
            if line.lower().startswith(prefix):
                command = line[len(prefix) :].strip()
                if command.startswith("make autocycle"):
                    return command
    return None


def parse_estimated_budget(result: CommandResult | None) -> int:
    if result is None:
        return DEFAULT_ESTIMATED_BUDGET
    text = "\n".join(part for part in (result.stdout, result.stderr) if part)
    match = re.search(r"^estimated cost for target:\s*([0-9]+)(?:\.[0-9]+)?$", text, flags=re.MULTILINE)
    if match:
        return int(match.group(1)) + 1
    return DEFAULT_ESTIMATED_BUDGET


def with_safe_push(command: str) -> str:
    if "safe-push" in command:
        return command
    return f"{command} && make safe-push"


def fallback_autocycle_command(snapshot: RepoSnapshot) -> str:
    estimated_budget = parse_estimated_budget(snapshot.budget_check)
    return (
        f"make autocycle N={snapshot.target} TOKEN_BUDGET={estimated_budget} "
        "BUDGET_SAFETY_FACTOR=1.25 && make safe-push"
    )


def autocycle_option(command: str, name: str) -> str | None:
    match = re.search(rf"(?:^|\s){re.escape(name)}=([^\s&]+)", command)
    if not match:
        return None
    return match.group(1)


def parse_int_option(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_float_option(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def decide_next_action(snapshot: RepoSnapshot) -> Decision:
    budget_status = parse_budget_status(snapshot.budget_check)

    if any(is_ide_status_line(line) for line in snapshot.status_lines):
        return Decision(
            status="BLOCKED",
            budget_status=budget_status,
            next_action="remove or ignore IDE files before validation.",
            command="rm -rf .idea && make validate",
        )

    if (
        snapshot.ahead is not None
        and snapshot.ahead > 0
        and (snapshot.behind is None or snapshot.behind == 0)
        and not repo_has_dirty_files(snapshot)
    ):
        return Decision(
            status="READY_TO_PUSH",
            budget_status=budget_status,
            next_action="push local commits with the repository safe-push workflow.",
            command="make safe-push",
        )

    if repo_has_dirty_files(snapshot):
        project_files = changed_project_files(snapshot.status_lines)
        if len(project_files) == 1 and snapshot.latest_ledger_final_status == "REVISE_PENDING":
            return Decision(
                status="DIRTY_WORKTREE",
                budget_status=budget_status,
                next_action="recover the pending revise for the single changed project file.",
                command="make recover-revise",
            )
        if snapshot.latest_ledger_final_status == "REVISE_PENDING":
            return Decision(
                status="DIRTY_WORKTREE",
                budget_status=budget_status,
                next_action="manually review the dirty worktree before choosing a recovery path.",
                command="git status --short && make validate",
            )
        return Decision(
            status="DIRTY_WORKTREE",
            budget_status=budget_status,
            next_action="inspect the worktree and validate before proceeding.",
            command="git status --short && make validate",
        )

    if not snapshot.budget_profile_exists:
        return Decision(
            status="NEEDS_BUDGET_PROFILE",
            budget_status="missing profile",
            next_action="create a local token budget profile.",
            command="make budget-init DAILY_BUDGET=300000",
        )

    if snapshot.budget_check is not None and (
        snapshot.budget_check.code == 3 or parse_budget_status(snapshot.budget_check) == "over budget"
    ):
        return Decision(
            status="OVER_BUDGET",
            budget_status="over budget",
            next_action="review budget usage before running more automation.",
            command="make budget-report",
        )

    if snapshot.budget_check is not None and (
        snapshot.budget_check.code == 0 or parse_budget_status(snapshot.budget_check) == "within budget"
    ):
        suggested = parse_suggested_command(snapshot.budget_check, snapshot.budget_report)
        command = with_safe_push(suggested) if suggested else fallback_autocycle_command(snapshot)
        return Decision(
            status="READY_TO_AUTOCYCLE",
            budget_status="within budget",
            next_action="run the budgeted autocycle and safe-push if it succeeds.",
            command=command,
        )

    return Decision(
        status="NEEDS_MANUAL_REVIEW",
        budget_status=budget_status,
        next_action="collect repository and budget context manually.",
        command="make status && make budget-report",
    )


def upstream_text(snapshot: RepoSnapshot) -> str:
    if snapshot.upstream is None:
        return "not configured"
    if snapshot.ahead is None or snapshot.behind is None:
        return f"{snapshot.upstream} (ahead/behind unavailable)"
    return f"{snapshot.upstream} (ahead {snapshot.ahead}, behind {snapshot.behind})"


def latest_ledger_text(snapshot: RepoSnapshot) -> str:
    if not snapshot.ledger_exists:
        return "missing"
    if snapshot.latest_ledger_final_status is None:
        return "available, no finalStatus found"
    if last_ledger_is_historical(snapshot):
        return "REVISE_PENDING (historical; no dirty file to recover)"
    return snapshot.latest_ledger_final_status


def last_ledger_is_historical(snapshot: RepoSnapshot) -> bool:
    return snapshot.latest_ledger_final_status == "REVISE_PENDING" and not repo_has_dirty_files(snapshot)


def format_human(snapshot: RepoSnapshot, decision: Decision) -> str:
    repo_state = "clean" if not snapshot.status_lines else f"dirty ({len(snapshot.status_lines)} status entrie(s))"
    branch = snapshot.branch or "unknown"
    head = snapshot.head or "unknown"
    return "\n".join(
        [
            f"repo status: {decision.status} ({repo_state})",
            f"branch/head: {branch} @ {head}",
            f"upstream status: {upstream_text(snapshot)}",
            f"budget status: {decision.budget_status}",
            f"last ledger final status: {latest_ledger_text(snapshot)}",
            f"next action: {decision.next_action}",
            f"command: {decision.command}",
        ]
    )


def format_json(snapshot: RepoSnapshot, decision: Decision) -> str:
    recommended_target = parse_int_option(autocycle_option(decision.command, "N"))
    recommended_token_budget = parse_int_option(autocycle_option(decision.command, "TOKEN_BUDGET"))
    budget_safety_factor = parse_float_option(autocycle_option(decision.command, "BUDGET_SAFETY_FACTOR"))
    document = {
        "status": decision.status,
        "repoStatus": "clean" if not repo_has_dirty_files(snapshot) else "dirty",
        "repoStatusLines": list(snapshot.status_lines),
        "branch": snapshot.branch,
        "head": snapshot.head,
        "upstream": snapshot.upstream,
        "ahead": snapshot.ahead,
        "behind": snapshot.behind,
        "isClean": not repo_has_dirty_files(snapshot),
        "dirtyFiles": changed_project_files(snapshot.status_lines),
        "ideFiles": ide_files(snapshot.status_lines),
        "budgetProfileExists": snapshot.budget_profile_exists,
        "ledgerExists": snapshot.ledger_exists,
        "lastLedgerFinalStatus": snapshot.latest_ledger_final_status,
        "lastLedgerIsHistorical": last_ledger_is_historical(snapshot),
        "recommendedTarget": recommended_target,
        "recommendedTokenBudget": recommended_token_budget,
        "budgetSafetyFactor": budget_safety_factor,
        "budgetStatus": decision.budget_status,
        "nextAction": decision.next_action,
        "command": decision.command,
    }
    return json.dumps(document, indent=2, sort_keys=True)


def assert_decision(
    name: str,
    snapshot: RepoSnapshot,
    expected_status: str,
    expected_command: str,
    expected_next_action: str | None = None,
) -> None:
    decision = decide_next_action(snapshot)
    if decision.status != expected_status:
        raise AssertionError(f"{name}: expected status {expected_status}, got {decision.status}")
    if decision.command != expected_command:
        raise AssertionError(f"{name}: expected command {expected_command!r}, got {decision.command!r}")
    if expected_next_action is not None and decision.next_action != expected_next_action:
        raise AssertionError(
            f"{name}: expected next action {expected_next_action!r}, got {decision.next_action!r}"
        )


def assert_human_contains(name: str, snapshot: RepoSnapshot, expected_text: str) -> None:
    decision = decide_next_action(snapshot)
    output = format_human(snapshot, decision)
    if expected_text not in output:
        raise AssertionError(f"{name}: expected output to contain {expected_text!r}, got {output!r}")


def assert_json_output(
    name: str,
    snapshot: RepoSnapshot,
    expected_status: str,
    expected_values: dict[str, Any] | None = None,
) -> None:
    decision = decide_next_action(snapshot)
    output = format_json(snapshot, decision)
    try:
        document = json.loads(output)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{name}: JSON output is invalid: {exc}") from exc

    required_keys = {
        "status",
        "repoStatus",
        "branch",
        "head",
        "upstream",
        "ahead",
        "behind",
        "isClean",
        "dirtyFiles",
        "ideFiles",
        "budgetStatus",
        "lastLedgerFinalStatus",
        "lastLedgerIsHistorical",
        "recommendedTarget",
        "recommendedTokenBudget",
        "budgetSafetyFactor",
        "nextAction",
        "command",
    }
    missing_keys = sorted(required_keys.difference(document))
    if missing_keys:
        raise AssertionError(f"{name}: JSON output is missing keys: {missing_keys}")
    if document["status"] != expected_status:
        raise AssertionError(f"{name}: expected JSON status {expected_status}, got {document['status']}")
    for key, expected_value in (expected_values or {}).items():
        if document.get(key) != expected_value:
            raise AssertionError(f"{name}: expected JSON {key}={expected_value!r}, got {document.get(key)!r}")


def test_snapshot(
    *,
    status_lines: list[str] | None = None,
    ahead: int | None = 0,
    behind: int | None = 0,
    budget_profile_exists: bool = True,
    ledger_exists: bool = True,
    latest_ledger_final_status: str | None = "ACCEPTED",
    budget_check: CommandResult | None = CommandResult(0, "status: within budget\nsuggested command: make autocycle N=3 TOKEN_BUDGET=100 BUDGET_SAFETY_FACTOR=1.25", ""),
    budget_report: CommandResult | None = CommandResult(0, "suggested command: make autocycle N=3 TOKEN_BUDGET=100 BUDGET_SAFETY_FACTOR=1.25", ""),
    target: int = DEFAULT_TARGET,
) -> RepoSnapshot:
    return RepoSnapshot(
        status_lines=status_lines or [],
        branch="main",
        head="abc1234",
        upstream="origin/main",
        ahead=ahead,
        behind=behind,
        budget_profile_exists=budget_profile_exists,
        ledger_exists=ledger_exists,
        latest_ledger_final_status=latest_ledger_final_status,
        latest_ledger_entries=(),
        budget_check=budget_check,
        budget_report=budget_report,
        target=target,
    )


def run_self_test() -> int:
    assert_decision(
        "IDE files blocked",
        test_snapshot(status_lines=["?? .idea/"]),
        "BLOCKED",
        "rm -rf .idea && make validate",
    )
    assert_decision(
        "clean repo ahead of upstream",
        test_snapshot(ahead=2, behind=0),
        "READY_TO_PUSH",
        "make safe-push",
    )
    assert_json_output(
        "READY_TO_PUSH JSON output",
        test_snapshot(ahead=2, behind=0),
        "READY_TO_PUSH",
        {
            "repoStatus": "clean",
            "isClean": True,
            "dirtyFiles": [],
            "ideFiles": [],
            "recommendedTarget": None,
            "recommendedTokenBudget": None,
            "budgetSafetyFactor": None,
        },
    )
    assert_decision(
        "dirty repo with REVISE_PENDING and one changed file",
        test_snapshot(status_lines=[" M docs/architecture/paper-model.md"], latest_ledger_final_status="REVISE_PENDING"),
        "DIRTY_WORKTREE",
        "make recover-revise",
        "recover the pending revise for the single changed project file.",
    )
    assert_json_output(
        "DIRTY_WORKTREE with one REVISE_PENDING file JSON output",
        test_snapshot(status_lines=[" M docs/architecture/paper-model.md"], latest_ledger_final_status="REVISE_PENDING"),
        "DIRTY_WORKTREE",
        {
            "repoStatus": "dirty",
            "isClean": False,
            "dirtyFiles": ["docs/architecture/paper-model.md"],
            "lastLedgerFinalStatus": "REVISE_PENDING",
            "lastLedgerIsHistorical": False,
            "recommendedTarget": None,
            "recommendedTokenBudget": None,
            "budgetSafetyFactor": None,
        },
    )
    assert_human_contains(
        "clean repo with historical REVISE_PENDING",
        test_snapshot(latest_ledger_final_status="REVISE_PENDING"),
        "last ledger final status: REVISE_PENDING (historical; no dirty file to recover)",
    )
    assert_decision(
        "dirty repo with REVISE_PENDING and multiple changed files",
        test_snapshot(
            status_lines=[
                " M docs/architecture/paper-model.md",
                " M docs/architecture/framework-model.md",
            ],
            latest_ledger_final_status="REVISE_PENDING",
        ),
        "DIRTY_WORKTREE",
        "git status --short && make validate",
        "manually review the dirty worktree before choosing a recovery path.",
    )
    assert_decision(
        "missing budget profile",
        test_snapshot(budget_profile_exists=False, budget_check=None, budget_report=None),
        "NEEDS_BUDGET_PROFILE",
        "make budget-init DAILY_BUDGET=300000",
    )
    assert_decision(
        "over budget",
        test_snapshot(budget_check=CommandResult(3, "status: over budget", "")),
        "OVER_BUDGET",
        "make budget-report",
    )
    assert_json_output(
        "OVER_BUDGET clean repo JSON output",
        test_snapshot(budget_check=CommandResult(3, "status: over budget", "")),
        "OVER_BUDGET",
        {
            "repoStatus": "clean",
            "isClean": True,
            "budgetStatus": "over budget",
            "recommendedTarget": None,
            "recommendedTokenBudget": None,
            "budgetSafetyFactor": None,
        },
    )
    assert_decision(
        "ready to autocycle",
        test_snapshot(),
        "READY_TO_AUTOCYCLE",
        "make autocycle N=3 TOKEN_BUDGET=100 BUDGET_SAFETY_FACTOR=1.25 && make safe-push",
    )
    assert_json_output(
        "READY_TO_AUTOCYCLE JSON output",
        test_snapshot(),
        "READY_TO_AUTOCYCLE",
        {
            "repoStatus": "clean",
            "isClean": True,
            "recommendedTarget": 3,
            "recommendedTokenBudget": 100,
            "budgetSafetyFactor": 1.25,
        },
    )
    print("rkm-next-action self-test passed")
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print the next safe operational action for RKM.")
    parser.add_argument("--target", type=positive_int, default=DEFAULT_TARGET, metavar="N")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON output")
    parser.add_argument("--self-test", action="store_true", help="run pure decision-function self-tests")
    return parser


def run_cli(argv: list[str]) -> int:
    parser = make_parser()
    args = parser.parse_args(argv[1:])
    if args.self_test:
        return run_self_test()

    snapshot = collect_snapshot(args.target)
    decision = decide_next_action(snapshot)
    print(format_json(snapshot, decision) if args.json else format_human(snapshot, decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(sys.argv))
