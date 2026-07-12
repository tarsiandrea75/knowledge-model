#!/usr/bin/env python3
"""Execute the next safe RKM operational action."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = 3

READY_TO_PUSH = "READY_TO_PUSH"
READY_TO_AUTOCYCLE = "READY_TO_AUTOCYCLE"
DIRTY_WORKTREE = "DIRTY_WORKTREE"
OVER_BUDGET = "OVER_BUDGET"
NEEDS_BUDGET_PROFILE = "NEEDS_BUDGET_PROFILE"
BLOCKED = "BLOCKED"
NEEDS_MANUAL_REVIEW = "NEEDS_MANUAL_REVIEW"

KNOWN_STATUSES = {
    READY_TO_PUSH,
    READY_TO_AUTOCYCLE,
    DIRTY_WORKTREE,
    OVER_BUDGET,
    NEEDS_BUDGET_PROFILE,
    BLOCKED,
    NEEDS_MANUAL_REVIEW,
}

STOP_EXIT_ZERO = {OVER_BUDGET, NEEDS_BUDGET_PROFILE}
STOP_EXIT_TWO = {BLOCKED, NEEDS_MANUAL_REVIEW}


@dataclass(frozen=True)
class CommandSpec:
    label: str
    args: Sequence[str]


@dataclass(frozen=True)
class Plan:
    status: str
    action: str
    commands: Sequence[CommandSpec]
    exit_code: int


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def command_text(command: CommandSpec) -> str:
    return " ".join(command.args)


def make_safe_push() -> CommandSpec:
    return CommandSpec("safe-push", ("make", "safe-push"))


def make_recover_revise() -> CommandSpec:
    return CommandSpec("recover-revise", ("make", "recover-revise"))


def make_autocycle(target: int, token_budget: int, budget_safety_factor: float) -> CommandSpec:
    return CommandSpec(
        "autocycle",
        (
            "make",
            "autocycle",
            f"N={target}",
            f"TOKEN_BUDGET={token_budget}",
            f"BUDGET_SAFETY_FACTOR={budget_safety_factor:g}",
        ),
    )


def require_positive_int(document: dict[str, Any], key: str) -> int | None:
    value = document.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None
    return value


def require_positive_number(document: dict[str, Any], key: str) -> float | None:
    value = document.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        return None
    return float(value)


def summary(document: dict[str, Any]) -> str:
    lines = [
        f"status: {document.get('status', 'UNKNOWN')}",
        f"next action: {document.get('nextAction', '(unavailable)')}",
        f"recommended command: {document.get('command', '(unavailable)')}",
    ]
    return "\n".join(lines)


def decide(document: dict[str, Any], *, allow_recovery: bool) -> Plan:
    status = document.get("status")
    if not isinstance(status, str) or status not in KNOWN_STATUSES:
        return Plan(str(status or "UNKNOWN"), "unknown status; stopping for manual review.", (), 2)

    command = document.get("command")

    if status == READY_TO_PUSH:
        if command != "make safe-push":
            return Plan(status, "recommended command is not whitelisted; stopping.", (), 2)
        return Plan(status, "run safe-push.", (make_safe_push(),), 0)

    if status == READY_TO_AUTOCYCLE:
        target = require_positive_int(document, "recommendedTarget")
        token_budget = require_positive_int(document, "recommendedTokenBudget")
        budget_safety_factor = require_positive_number(document, "budgetSafetyFactor")
        if target is None or token_budget is None or budget_safety_factor is None:
            return Plan(status, "missing autocycle recommendation fields; stopping.", (), 2)
        return Plan(
            status,
            "run autocycle, then safe-push if autocycle succeeds.",
            (make_autocycle(target, token_budget, budget_safety_factor), make_safe_push()),
            0,
        )

    if status == DIRTY_WORKTREE and command == "make recover-revise":
        if not allow_recovery:
            return Plan(status, "recovery is available but requires --allow-recovery.", (), 0)
        return Plan(
            status,
            "run recover-revise, then safe-push if recovery succeeds.",
            (make_recover_revise(), make_safe_push()),
            0,
        )

    if status in STOP_EXIT_ZERO:
        return Plan(status, "stopping without changes.", (), 0)

    if status in STOP_EXIT_TWO:
        return Plan(status, "manual review required; stopping.", (), 2)

    return Plan(status, "status is not automatically actionable; stopping.", (), 2)


def run_next_action(target: int) -> tuple[int, str, str]:
    completed = subprocess.run(
        ["python3", "scripts/rkm-next-action.py", "--target", str(target), "--json"],
        cwd=REPOSITORY_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.returncode, completed.stdout, completed.stderr


def parse_next_action(stdout: str) -> dict[str, Any]:
    document = json.loads(stdout)
    if not isinstance(document, dict):
        raise ValueError("next-action JSON output was not an object")
    return document


def run_commands(commands: Sequence[CommandSpec], *, dry_run: bool) -> int:
    if not commands:
        print("commands: none")
        return 0

    for command in commands:
        print(f"{'would run' if dry_run else 'running'}: {command_text(command)}")
        if dry_run:
            continue
        completed = subprocess.run(command.args, cwd=REPOSITORY_ROOT, check=False)
        if completed.returncode != 0:
            print(f"final outcome: {command.label} failed with exit {completed.returncode}")
            return completed.returncode
    return 0


def run_autopilot(target: int, *, dry_run: bool, allow_recovery: bool) -> int:
    code, stdout, stderr = run_next_action(target)
    if code != 0:
        print("next-action failed.")
        if stdout:
            print(stdout.rstrip())
        if stderr:
            print(stderr.rstrip(), file=sys.stderr)
        return code

    try:
        document = parse_next_action(stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"next-action output was not usable JSON: {exc}")
        if stdout:
            print(stdout.rstrip())
        if stderr:
            print(stderr.rstrip(), file=sys.stderr)
        return 2

    plan = decide(document, allow_recovery=allow_recovery)
    print(f"detected status: {plan.status}")
    print(f"action selected: {plan.action}")

    if not plan.commands:
        print(summary(document))

    command_result = run_commands(plan.commands, dry_run=dry_run)
    if command_result != 0:
        return command_result

    if dry_run and plan.commands:
        print("final outcome: dry run complete; no changes made.")
        return 0

    if plan.commands:
        print("final outcome: completed.")
    else:
        print("final outcome: stopped without changes.")
    return plan.exit_code


def assert_plan(
    name: str,
    document: dict[str, Any],
    allow_recovery: bool,
    expected_commands: Sequence[str],
    expected_exit_code: int,
) -> None:
    plan = decide(document, allow_recovery=allow_recovery)
    actual_commands = tuple(command_text(command) for command in plan.commands)
    if actual_commands != expected_commands:
        raise AssertionError(f"{name}: expected commands {expected_commands!r}, got {actual_commands!r}")
    if plan.exit_code != expected_exit_code:
        raise AssertionError(f"{name}: expected exit {expected_exit_code}, got {plan.exit_code}")


def run_self_test() -> int:
    assert_plan(
        "READY_TO_PUSH",
        {"status": READY_TO_PUSH, "command": "make safe-push"},
        False,
        ("make safe-push",),
        0,
    )
    assert_plan(
        "READY_TO_AUTOCYCLE",
        {
            "status": READY_TO_AUTOCYCLE,
            "recommendedTarget": 3,
            "recommendedTokenBudget": 100,
            "budgetSafetyFactor": 1.25,
        },
        False,
        ("make autocycle N=3 TOKEN_BUDGET=100 BUDGET_SAFETY_FACTOR=1.25", "make safe-push"),
        0,
    )
    assert_plan(
        "OVER_BUDGET",
        {"status": OVER_BUDGET, "command": "make budget-report"},
        False,
        (),
        0,
    )
    assert_plan(
        "DIRTY_WORKTREE recovery without flag",
        {"status": DIRTY_WORKTREE, "command": "make recover-revise"},
        False,
        (),
        0,
    )
    assert_plan(
        "DIRTY_WORKTREE recovery with flag",
        {"status": DIRTY_WORKTREE, "command": "make recover-revise"},
        True,
        ("make recover-revise", "make safe-push"),
        0,
    )
    assert_plan(
        "BLOCKED",
        {"status": BLOCKED, "command": "git status --short && make validate"},
        False,
        (),
        2,
    )
    print("rkm-autopilot self-test passed")
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Execute the next safe RKM operational action.")
    parser.add_argument("--target", type=positive_int, default=DEFAULT_TARGET, metavar="N")
    parser.add_argument("--dry-run", action="store_true", help="print what would be done without modifying files")
    parser.add_argument(
        "--allow-recovery",
        action="store_true",
        help="allow make recover-revise for a single-file REVISE_PENDING dirty worktree",
    )
    parser.add_argument("--self-test", action="store_true", help="run pure decision-mapping self-tests")
    return parser


def run_cli(argv: list[str]) -> int:
    parser = make_parser()
    args = parser.parse_args(argv[1:])
    if args.self_test:
        return run_self_test()
    return run_autopilot(args.target, dry_run=args.dry_run, allow_recovery=args.allow_recovery)


if __name__ == "__main__":
    raise SystemExit(run_cli(sys.argv))
