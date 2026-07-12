#!/usr/bin/env python3
"""Execute the next safe RKM operational action."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = 3
DEFAULT_STATE_PATH = Path(".rkm/autopilot-state.json")

READY_TO_PUSH = "READY_TO_PUSH"
READY_TO_AUTOCYCLE = "READY_TO_AUTOCYCLE"
DIRTY_WORKTREE = "DIRTY_WORKTREE"
OVER_BUDGET = "OVER_BUDGET"
NEEDS_BUDGET_PROFILE = "NEEDS_BUDGET_PROFILE"
BLOCKED = "BLOCKED"
NEEDS_MANUAL_REVIEW = "NEEDS_MANUAL_REVIEW"

RECOVERY_AVAILABLE = "RECOVERY_AVAILABLE"
RECOVERY_FAILED_NEEDS_MANUAL_FIX = "RECOVERY_FAILED_NEEDS_MANUAL_FIX"
BLOCKED_IDE_FILES = "BLOCKED_IDE_FILES"
MANUAL_REVIEW = "MANUAL_REVIEW"
NO_RECOVERY_NEEDED = "NO_RECOVERY_NEEDED"

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
REQUIRED_STATE_KEYS = {
    "timestampUtc",
    "target",
    "dryRun",
    "allowRecovery",
    "detectedStatus",
    "nextAction",
    "recommendedCommand",
    "actionSelected",
    "commandsPlanned",
    "commandsRun",
    "commandsSkipped",
    "exitCode",
    "finalOutcome",
    "nextActionJson",
    "recoveryPlanJson",
}


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


@dataclass(frozen=True)
class CommandRunResult:
    exit_code: int
    commands_run: Sequence[str]
    commands_skipped: Sequence[str]


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


def resolve_state_path(state_path: str | Path) -> Path:
    path = Path(state_path)
    if path.is_absolute():
        return path
    return REPOSITORY_ROOT / path


def new_state(
    *,
    target: int,
    dry_run: bool,
    allow_recovery: bool,
    detected_status: str,
    next_action: Any,
    recommended_command: Any,
    action_selected: str,
    commands_planned: Sequence[str],
    next_action_json: dict[str, Any] | None,
    recovery_plan_json: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "timestampUtc": "",
        "target": target,
        "dryRun": dry_run,
        "allowRecovery": allow_recovery,
        "detectedStatus": detected_status,
        "nextAction": next_action,
        "recommendedCommand": recommended_command,
        "actionSelected": action_selected,
        "commandsPlanned": list(commands_planned),
        "commandsRun": [],
        "commandsSkipped": [],
        "exitCode": None,
        "finalOutcome": "",
        "nextActionJson": next_action_json,
        "recoveryPlanJson": recovery_plan_json,
    }


def write_state(state: dict[str, Any], state_path: str | Path) -> None:
    from datetime import datetime, timezone

    resolved = resolve_state_path(state_path)
    state = dict(state)
    state["timestampUtc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(state, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_state_or_report(state: dict[str, Any], state_path: str | Path) -> bool:
    try:
        write_state(state, state_path)
    except OSError as exc:
        print(f"failed to write autopilot state: {resolve_state_path(state_path)}: {exc}", file=sys.stderr)
        return False
    return True


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


def run_recovery_plan() -> tuple[int, str, str]:
    completed = subprocess.run(
        ["python3", "scripts/rkm-recovery-plan.py", "--json"],
        cwd=REPOSITORY_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.returncode, completed.stdout, completed.stderr


def parse_recovery_plan(stdout: str) -> dict[str, Any]:
    document = json.loads(stdout)
    if not isinstance(document, dict):
        raise ValueError("recovery-plan JSON output was not an object")
    return document


def recovery_plan_summary(document: dict[str, Any]) -> str:
    lines = [
        f"recovery plan status: {document.get('status', 'UNKNOWN')}",
        f"reason: {document.get('reason', '(unavailable)')}",
        f"latest touched file: {document.get('latestTouchedFile', '(unavailable)')}",
    ]
    reviewer_summary = document.get("reviewerSummary")
    if isinstance(reviewer_summary, str) and reviewer_summary:
        lines.extend(("reviewer summary:", reviewer_summary))
    lines.append(f"recommended command: {document.get('recommendedCommand', '(unavailable)')}")
    return "\n".join(lines)


def blocked_recovery_summary(document: dict[str, Any]) -> str:
    lines = [
        f"recovery plan status: {document.get('status', 'UNKNOWN')}",
        f"reason: {document.get('reason', '(unavailable)')}",
        f"recommended cleanup command: {document.get('recommendedCommand', '(unavailable)')}",
    ]
    return "\n".join(lines)


def manual_review_recovery_summary(document: dict[str, Any]) -> str:
    lines = [
        f"recovery plan status: {document.get('status', 'UNKNOWN')}",
        f"reason: {document.get('reason', '(unavailable)')}",
    ]
    recommended_command = document.get("recommendedCommand")
    if recommended_command:
        lines.append(f"recommended command: {recommended_command}")
    return "\n".join(lines)


def decide_recovery(document: dict[str, Any]) -> Plan | None:
    status = document.get("status")
    if status == NO_RECOVERY_NEEDED:
        return None
    if status == RECOVERY_AVAILABLE:
        return Plan(
            status,
            "run recover-revise, then safe-push if recovery succeeds.",
            (make_recover_revise(), make_safe_push()),
            0,
        )
    if status == RECOVERY_FAILED_NEEDS_MANUAL_FIX:
        return Plan(status, "recovery already failed; stopping for manual targeted fix.", (), 0)
    if status == BLOCKED_IDE_FILES:
        return Plan(status, "IDE files block recovery; stopping for cleanup.", (), 2)
    if status == MANUAL_REVIEW:
        return Plan(status, "manual review required by recovery plan; stopping.", (), 2)
    return Plan(str(status or "UNKNOWN"), "unknown recovery-plan status; stopping.", (), 2)


def run_commands(commands: Sequence[CommandSpec], *, dry_run: bool) -> CommandRunResult:
    commands_run: list[str] = []
    if not commands:
        print("commands: none")
        return CommandRunResult(0, (), ())

    for index, command in enumerate(commands):
        text = command_text(command)
        print(f"{'would run' if dry_run else 'running'}: {command_text(command)}")
        if dry_run:
            continue
        commands_run.append(text)
        completed = subprocess.run(command.args, cwd=REPOSITORY_ROOT, check=False)
        if completed.returncode != 0:
            print(f"final outcome: {command.label} failed with exit {completed.returncode}")
            commands_skipped = tuple(command_text(skipped) for skipped in commands[index + 1 :])
            return CommandRunResult(completed.returncode, tuple(commands_run), commands_skipped)
    commands_skipped = tuple(command_text(command) for command in commands) if dry_run else ()
    return CommandRunResult(0, tuple(commands_run), commands_skipped)


def run_autopilot(target: int, *, dry_run: bool, allow_recovery: bool, state_path: str | Path) -> int:
    code, stdout, stderr = run_next_action(target)
    if code != 0:
        print("next-action failed.")
        if stdout:
            print(stdout.rstrip())
        if stderr:
            print(stderr.rstrip(), file=sys.stderr)
        state = new_state(
            target=target,
            dry_run=dry_run,
            allow_recovery=allow_recovery,
            detected_status="NEXT_ACTION_FAILED",
            next_action=None,
            recommended_command=None,
            action_selected="next-action failed.",
            commands_planned=(),
            next_action_json=None,
        )
        state["exitCode"] = code
        state["finalOutcome"] = f"next-action failed with exit {code}"
        if not dry_run and not write_state_or_report(state, state_path):
            return 1
        return code

    try:
        document = parse_next_action(stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"next-action output was not usable JSON: {exc}")
        if stdout:
            print(stdout.rstrip())
        if stderr:
            print(stderr.rstrip(), file=sys.stderr)
        state = new_state(
            target=target,
            dry_run=dry_run,
            allow_recovery=allow_recovery,
            detected_status="UNUSABLE_NEXT_ACTION_JSON",
            next_action=None,
            recommended_command=None,
            action_selected="next-action output was not usable JSON.",
            commands_planned=(),
            next_action_json=None,
        )
        state["exitCode"] = 2
        state["finalOutcome"] = "next-action output was not usable JSON"
        if not dry_run and not write_state_or_report(state, state_path):
            return 1
        return 2

    recovery_document: dict[str, Any] | None = None
    if allow_recovery:
        recovery_code, recovery_stdout, recovery_stderr = run_recovery_plan()
        if recovery_code != 0:
            print(f"recovery-plan failed with exit {recovery_code}.")
            if recovery_stdout:
                print(recovery_stdout.rstrip())
            if recovery_stderr:
                print(recovery_stderr.rstrip(), file=sys.stderr)
            state = new_state(
                target=target,
                dry_run=dry_run,
                allow_recovery=allow_recovery,
                detected_status="RECOVERY_PLAN_FAILED",
                next_action=document.get("nextAction"),
                recommended_command=document.get("command"),
                action_selected="recovery-plan failed.",
                commands_planned=(),
                next_action_json=document,
                recovery_plan_json=None,
            )
            state["exitCode"] = recovery_code
            state["finalOutcome"] = f"recovery-plan failed with exit {recovery_code}"
            if not dry_run and not write_state_or_report(state, state_path):
                return 1
            return recovery_code

        try:
            recovery_document = parse_recovery_plan(recovery_stdout)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"recovery-plan output was not usable JSON: {exc}")
            if recovery_stdout:
                print(recovery_stdout.rstrip())
            if recovery_stderr:
                print(recovery_stderr.rstrip(), file=sys.stderr)
            state = new_state(
                target=target,
                dry_run=dry_run,
                allow_recovery=allow_recovery,
                detected_status="UNUSABLE_RECOVERY_PLAN_JSON",
                next_action=document.get("nextAction"),
                recommended_command=document.get("command"),
                action_selected="recovery-plan output was not usable JSON.",
                commands_planned=(),
                next_action_json=document,
                recovery_plan_json=None,
            )
            state["exitCode"] = 2
            state["finalOutcome"] = "recovery-plan output was not usable JSON"
            if not dry_run and not write_state_or_report(state, state_path):
                return 1
            return 2

    recovery_plan = decide_recovery(recovery_document) if recovery_document is not None else None
    plan = recovery_plan if recovery_plan is not None else decide(document, allow_recovery=allow_recovery)
    planned_commands = tuple(command_text(command) for command in plan.commands)
    recommended_command = (
        recovery_document.get("recommendedCommand")
        if recovery_plan is not None and recovery_document is not None
        else document.get("command")
    )
    state = new_state(
        target=target,
        dry_run=dry_run,
        allow_recovery=allow_recovery,
        detected_status=plan.status,
        next_action=document.get("nextAction"),
        recommended_command=recommended_command,
        action_selected=plan.action,
        commands_planned=planned_commands,
        next_action_json=document,
        recovery_plan_json=recovery_document,
    )
    print(f"detected status: {plan.status}")
    print(f"action selected: {plan.action}")

    if not plan.commands:
        if recovery_plan is not None and recovery_document is not None:
            if plan.status == RECOVERY_FAILED_NEEDS_MANUAL_FIX:
                print(recovery_plan_summary(recovery_document))
            elif plan.status == BLOCKED_IDE_FILES:
                print(blocked_recovery_summary(recovery_document))
            elif plan.status == MANUAL_REVIEW:
                print(manual_review_recovery_summary(recovery_document))
            else:
                print(recovery_plan_summary(recovery_document))
        else:
            print(summary(document))

    command_result = run_commands(plan.commands, dry_run=dry_run)
    state["commandsRun"] = list(command_result.commands_run)
    state["commandsSkipped"] = list(command_result.commands_skipped)
    if command_result.exit_code != 0:
        state["exitCode"] = command_result.exit_code
        state["finalOutcome"] = f"command failed with exit {command_result.exit_code}"
        if not dry_run and not write_state_or_report(state, state_path):
            return 1
        return command_result.exit_code

    if dry_run and plan.commands:
        print("final outcome: dry run complete; no changes made.")
        state["exitCode"] = 0
        state["finalOutcome"] = "dry run complete; no changes made."
        return 0

    if plan.commands:
        print("final outcome: completed.")
        state["finalOutcome"] = "completed."
    else:
        print("final outcome: stopped without changes.")
        state["finalOutcome"] = "stopped without changes."
    state["exitCode"] = plan.exit_code
    if not dry_run and not write_state_or_report(state, state_path):
        return 1
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


def assert_recovery_plan(
    name: str,
    document: dict[str, Any],
    expected_commands: Sequence[str],
    expected_exit_code: int,
) -> Plan | None:
    plan = decide_recovery(document)
    actual_commands = tuple(command_text(command) for command in plan.commands) if plan is not None else ()
    if actual_commands != expected_commands:
        raise AssertionError(f"{name}: expected commands {expected_commands!r}, got {actual_commands!r}")
    actual_exit_code = plan.exit_code if plan is not None else 0
    if actual_exit_code != expected_exit_code:
        raise AssertionError(f"{name}: expected exit {expected_exit_code}, got {actual_exit_code}")
    return plan


def read_state(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise AssertionError(f"{path}: state JSON was not an object")
    return document


def display_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "(unavailable)"
    return str(value)


def print_command_list(label: str, commands: Any) -> None:
    print(f"{label}:")
    if not isinstance(commands, list) or not commands:
        print("  none")
        return
    for command in commands:
        print(f"  - {display_value(command)}")


def read_status_state(state_path: str | Path) -> tuple[dict[str, Any] | None, int]:
    resolved = resolve_state_path(state_path)
    try:
        state = json.loads(resolved.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(
            f"autopilot state not found: {resolved}\n"
            "Run `make autopilot-dry-run` to generate a fresh state preview.",
            file=sys.stderr,
        )
        return None, 2
    except json.JSONDecodeError as exc:
        print(f"autopilot state is invalid JSON: {resolved}: {exc}", file=sys.stderr)
        return None, 2
    except OSError as exc:
        print(f"failed to read autopilot state: {resolved}: {exc}", file=sys.stderr)
        return None, 2

    if not isinstance(state, dict):
        print(f"autopilot state is invalid: {resolved}: expected a JSON object", file=sys.stderr)
        return None, 2

    return state, 0


def print_budget_status(next_action_json: Any, requested_target: Any) -> None:
    if not isinstance(next_action_json, dict):
        return

    budget_keys = (
        "dailyBudgetTokens",
        "tokensUsedInCurrentWindow",
        "reserveTokens",
        "recoveryRiskReserveTokens",
        "usableRemainingTokensAfterRisk",
        "recommendedTarget",
        "requiredBudgetForTarget",
    )
    if not any(key in next_action_json for key in budget_keys):
        return

    print("budget:")
    for key in budget_keys:
        if key in next_action_json:
            print(f"  {key}: {display_value(next_action_json.get(key))}")

    usable = next_action_json.get("usableRemainingTokensAfterRisk")
    required = next_action_json.get("requiredBudgetForTarget")
    recommended_target = next_action_json.get("recommendedTarget")
    if usable is not None or required is not None or recommended_target is not None:
        print(
            "  explanation: "
            f"usable remaining tokens after reserves are {display_value(usable)}; "
            f"requested target {display_value(requested_target)} requires {display_value(required)} tokens; "
            f"recommended safe target is {display_value(recommended_target)}."
        )


def print_historical_ledger_status(next_action_json: Any) -> None:
    if isinstance(next_action_json, dict) and next_action_json.get("lastLedgerIsHistorical") is True:
        print("last ledger status: historical; no dirty file is pending.")


def print_status(state: dict[str, Any]) -> None:
    print("autopilot status")
    print(f"last autopilot timestamp: {display_value(state.get('timestampUtc'))}")
    print(f"detected status: {display_value(state.get('detectedStatus'))}")
    print(f"final outcome: {display_value(state.get('finalOutcome'))}")
    print(f"target: {display_value(state.get('target'))}")
    print(f"dryRun: {display_value(state.get('dryRun'))}")
    print(f"allowRecovery: {display_value(state.get('allowRecovery'))}")
    print(f"recommended command: {display_value(state.get('recommendedCommand'))}")
    print_command_list("commands planned", state.get("commandsPlanned"))
    print_command_list("commands run", state.get("commandsRun"))
    print_command_list("commands skipped", state.get("commandsSkipped"))
    print(f"exit code: {display_value(state.get('exitCode'))}")
    next_action_json = state.get("nextActionJson")
    print_budget_status(next_action_json, state.get("target"))
    print_historical_ledger_status(next_action_json)


def run_status(state_path: str | Path) -> int:
    state, exit_code = read_status_state(state_path)
    if state is None:
        return exit_code
    print_status(state)
    return 0


def assert_required_state_keys(name: str, state: dict[str, Any]) -> None:
    missing = REQUIRED_STATE_KEYS.difference(state)
    if missing:
        raise AssertionError(f"{name}: state JSON missing keys {sorted(missing)!r}")


def assert_autopilot_state(
    name: str,
    document: dict[str, Any],
    *,
    dry_run: bool,
    command_result: CommandRunResult | None,
) -> dict[str, Any] | None:
    original_run_next_action = run_next_action
    original_run_commands = run_commands
    with tempfile.TemporaryDirectory(prefix="rkm-autopilot-test-") as directory:
        state_path = Path(directory) / "autopilot-state.json"

        def fake_next_action(target: int) -> tuple[int, str, str]:
            return 0, json.dumps(document), ""

        def fake_run_commands(commands: Sequence[CommandSpec], *, dry_run: bool) -> CommandRunResult:
            if command_result is None:
                return original_run_commands(commands, dry_run=dry_run)
            return command_result

        globals()["run_next_action"] = fake_next_action
        globals()["run_commands"] = fake_run_commands
        try:
            run_autopilot(3, dry_run=dry_run, allow_recovery=False, state_path=state_path)
        finally:
            globals()["run_next_action"] = original_run_next_action
            globals()["run_commands"] = original_run_commands

        if dry_run:
            if state_path.exists():
                raise AssertionError(f"{name}: dry-run wrote state")
            return None

        state = read_state(state_path)
        assert_required_state_keys(name, state)
        return state


def assert_status_result(
    name: str,
    state_content: str | None,
    expected_exit_code: int,
    expected_stdout: Sequence[str],
    expected_stderr: Sequence[str] = (),
    unexpected_stdout: Sequence[str] = (),
) -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-autopilot-status-test-") as directory:
        state_path = Path(directory) / "autopilot-state.json"
        if state_content is not None:
            state_path.write_text(state_content, encoding="utf-8")

        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            actual_exit_code = run_status(state_path)

        if actual_exit_code != expected_exit_code:
            raise AssertionError(f"{name}: expected exit {expected_exit_code}, got {actual_exit_code}")

        actual_stdout = stdout.getvalue()
        for expected in expected_stdout:
            if expected not in actual_stdout:
                raise AssertionError(f"{name}: expected stdout to contain {expected!r}, got {actual_stdout!r}")

        for unexpected in unexpected_stdout:
            if unexpected in actual_stdout:
                raise AssertionError(f"{name}: expected stdout not to contain {unexpected!r}, got {actual_stdout!r}")

        actual_stderr = stderr.getvalue()
        for expected in expected_stderr:
            if expected not in actual_stderr:
                raise AssertionError(f"{name}: expected stderr to contain {expected!r}, got {actual_stderr!r}")


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
    recovery_available_plan = assert_recovery_plan(
        "allow-recovery RECOVERY_AVAILABLE",
        {"status": RECOVERY_AVAILABLE, "recommendedCommand": "make recover-revise"},
        ("make recover-revise", "make safe-push"),
        0,
    )
    if recovery_available_plan is None:
        raise AssertionError("allow-recovery RECOVERY_AVAILABLE: expected recovery plan")
    dry_run_output = io.StringIO()
    with contextlib.redirect_stdout(dry_run_output):
        dry_run_result = run_commands(recovery_available_plan.commands, dry_run=True)
    if dry_run_result.commands_run:
        raise AssertionError("allow-recovery RECOVERY_AVAILABLE dry-run: expected no commands run")
    if tuple(dry_run_result.commands_skipped) != ("make recover-revise", "make safe-push"):
        raise AssertionError("allow-recovery RECOVERY_AVAILABLE dry-run: expected both commands skipped")
    assert_recovery_plan(
        "allow-recovery RECOVERY_FAILED_NEEDS_MANUAL_FIX",
        {"status": RECOVERY_FAILED_NEEDS_MANUAL_FIX, "recommendedCommand": "make manual-fix"},
        (),
        0,
    )
    assert_recovery_plan(
        "allow-recovery BLOCKED_IDE_FILES",
        {"status": BLOCKED_IDE_FILES, "recommendedCommand": "rm -rf .idea && make validate"},
        (),
        2,
    )
    assert_recovery_plan(
        "allow-recovery MANUAL_REVIEW",
        {"status": MANUAL_REVIEW, "recommendedCommand": "git status --short && make validate"},
        (),
        2,
    )
    no_recovery_plan = decide_recovery({"status": NO_RECOVERY_NEEDED})
    if no_recovery_plan is not None:
        raise AssertionError("allow-recovery NO_RECOVERY_NEEDED: expected normal next-action fallback")
    fallback_plan = decide({"status": READY_TO_PUSH, "command": "make safe-push"}, allow_recovery=True)
    if tuple(command_text(command) for command in fallback_plan.commands) != ("make safe-push",):
        raise AssertionError("allow-recovery NO_RECOVERY_NEEDED: normal next-action fallback failed")
    assert_autopilot_state(
        "dry-run does not write state",
        {"status": READY_TO_PUSH, "command": "make safe-push"},
        dry_run=True,
        command_result=None,
    )
    over_budget_state = assert_autopilot_state(
        "OVER_BUDGET writes state",
        {"status": OVER_BUDGET, "command": "make budget-report"},
        dry_run=False,
        command_result=CommandRunResult(0, (), ()),
    )
    if over_budget_state is None or over_budget_state["detectedStatus"] != OVER_BUDGET:
        raise AssertionError("OVER_BUDGET writes state: wrong detected status")

    ready_to_push_state = assert_autopilot_state(
        "READY_TO_PUSH writes planned command",
        {"status": READY_TO_PUSH, "command": "make safe-push"},
        dry_run=False,
        command_result=CommandRunResult(0, ("make safe-push",), ()),
    )
    if ready_to_push_state is None or ready_to_push_state["commandsPlanned"] != ["make safe-push"]:
        raise AssertionError("READY_TO_PUSH writes planned command: planned command missing")

    failed_state = assert_autopilot_state(
        "failed command records exit code",
        {"status": READY_TO_PUSH, "command": "make safe-push"},
        dry_run=False,
        command_result=CommandRunResult(7, ("make safe-push",), ()),
    )
    if failed_state is None or failed_state["exitCode"] != 7:
        raise AssertionError("failed command records exit code: wrong exit code")

    if failed_state["commandsRun"] != ["make safe-push"]:
        raise AssertionError("failed command records exit code: failed command was not recorded")

    assert_status_result(
        "status missing state",
        None,
        2,
        (),
        ("autopilot state not found", "make autopilot-dry-run"),
    )
    assert_status_result(
        "status invalid state",
        "{",
        2,
        (),
        ("autopilot state is invalid JSON",),
    )
    assert_status_result(
        "status valid over-budget state",
        json.dumps(
            {
                "timestampUtc": "2026-07-12T00:00:00Z",
                "target": 3,
                "dryRun": False,
                "allowRecovery": False,
                "detectedStatus": OVER_BUDGET,
                "nextAction": "reduce target",
                "recommendedCommand": "make budget-report",
                "actionSelected": "stopping without changes.",
                "commandsPlanned": [],
                "commandsRun": [],
                "commandsSkipped": [],
                "exitCode": 0,
                "finalOutcome": "stopped without changes.",
                "nextActionJson": {
                    "status": OVER_BUDGET,
                    "dailyBudgetTokens": 1000,
                    "tokensUsedInCurrentWindow": 950,
                    "reserveTokens": 100,
                    "recoveryRiskReserveTokens": 50,
                    "usableRemainingTokensAfterRisk": -100,
                    "recommendedTarget": 1,
                    "requiredBudgetForTarget": 300,
                    "lastLedgerIsHistorical": True,
                },
            }
        ),
        0,
        (
            "detected status: OVER_BUDGET",
            "dailyBudgetTokens: 1000",
            "usableRemainingTokensAfterRisk: -100",
            "requested target 3 requires 300 tokens",
            "recommended safe target is 1",
            "last ledger status: historical; no dirty file is pending.",
        ),
    )
    assert_status_result(
        "status budget explanation uses requested target",
        json.dumps(
            {
                "timestampUtc": "2026-07-12T00:00:00Z",
                "target": 3,
                "dryRun": False,
                "allowRecovery": False,
                "detectedStatus": OVER_BUDGET,
                "nextAction": "reduce target",
                "recommendedCommand": "make budget-report",
                "actionSelected": "stopping without changes.",
                "commandsPlanned": [],
                "commandsRun": [],
                "commandsSkipped": [],
                "exitCode": 0,
                "finalOutcome": "stopped without changes.",
                "nextActionJson": {
                    "status": OVER_BUDGET,
                    "usableRemainingTokensAfterRisk": 100000,
                    "recommendedTarget": 0,
                    "requiredBudgetForTarget": 223117,
                },
            }
        ),
        0,
        (
            "requested target 3 requires 223117 tokens",
            "recommended safe target is 0",
        ),
        unexpected_stdout=("target 0 requires 223117 tokens",),
    )
    assert_status_result(
        "status valid ready-to-autocycle state",
        json.dumps(
            {
                "timestampUtc": "2026-07-12T00:00:00Z",
                "target": 3,
                "dryRun": True,
                "allowRecovery": False,
                "detectedStatus": READY_TO_AUTOCYCLE,
                "nextAction": "run autocycle",
                "recommendedCommand": "make autocycle N=3 TOKEN_BUDGET=500 BUDGET_SAFETY_FACTOR=1.25",
                "actionSelected": "run autocycle, then safe-push if autocycle succeeds.",
                "commandsPlanned": [
                    "make autocycle N=3 TOKEN_BUDGET=500 BUDGET_SAFETY_FACTOR=1.25",
                    "make safe-push",
                ],
                "commandsRun": [],
                "commandsSkipped": [],
                "exitCode": 0,
                "finalOutcome": "dry run complete; no changes made.",
                "nextActionJson": {"status": READY_TO_AUTOCYCLE},
            }
        ),
        0,
        (
            "detected status: READY_TO_AUTOCYCLE",
            "commands planned:",
            "make autocycle N=3 TOKEN_BUDGET=500 BUDGET_SAFETY_FACTOR=1.25",
            "make safe-push",
        ),
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
    parser.add_argument("--state-path", default=DEFAULT_STATE_PATH, metavar="PATH", help="autopilot state output path")
    parser.add_argument("--self-test", action="store_true", help="run pure decision-mapping self-tests")
    return parser


def make_status_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print the latest RKM autopilot status.")
    parser.add_argument("--state-path", default=DEFAULT_STATE_PATH, metavar="PATH", help="autopilot state input path")
    return parser


def run_cli(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "status":
        parser = make_status_parser()
        args = parser.parse_args(argv[2:])
        return run_status(args.state_path)

    parser = make_parser()
    args = parser.parse_args(argv[1:])
    if args.self_test:
        return run_self_test()
    return run_autopilot(args.target, dry_run=args.dry_run, allow_recovery=args.allow_recovery, state_path=args.state_path)


if __name__ == "__main__":
    raise SystemExit(run_cli(sys.argv))
