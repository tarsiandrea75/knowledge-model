#!/usr/bin/env python3
"""Manage a local RKM Codex/token budget profile."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import math
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_PATH = REPOSITORY_ROOT / ".rkm" / "budget-profile.json"
DEFAULT_LEDGER_PATH = REPOSITORY_ROOT / ".rkm" / "run-ledger.jsonl"

DEFAULT_SAFETY_FACTOR = 1.25
DEFAULT_RESERVE_RATIO = 0.20
DEFAULT_WINDOW_HOURS = 24

SUCCESSFUL_STATUSES = {"ACCEPTED", "RECOVERED"}


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: str, field_name: str = "timestamp") -> datetime:
    normalized = value
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"invalid {field_name}: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def resolve_path(value: str | None, default: Path, repo_root: Path = REPOSITORY_ROOT) -> Path:
    if value is None:
        return default
    path = Path(value)
    if path.is_absolute():
        return path
    return (repo_root / path).resolve()


def repository_relative(path: Path, repo_root: Path = REPOSITORY_ROOT) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive number") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive number")
    return parsed


def ratio_float(value: str) -> float:
    parsed = positive_float(value)
    if parsed >= 1:
        raise argparse.ArgumentTypeError("must be less than 1")
    return parsed


def build_profile(
    daily_budget_tokens: int,
    safety_factor: float,
    reserve_ratio: float,
    window_hours: int,
    now: datetime | None = None,
) -> dict[str, Any]:
    timestamp = utc_text(now or utc_now())
    return {
        "createdAtUtc": timestamp,
        "windowStartedAtUtc": timestamp,
        "dailyBudgetTokens": daily_budget_tokens,
        "safetyFactor": safety_factor,
        "reserveRatio": reserve_ratio,
        "windowHours": window_hours,
    }


def write_profile(profile_path: Path, profile: dict[str, Any]) -> None:
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(json.dumps(profile, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_profile(profile_path: Path) -> dict[str, Any]:
    with profile_path.open("r", encoding="utf-8") as handle:
        profile = json.load(handle)
    if not isinstance(profile, dict):
        raise ValueError(f"profile must be a JSON object: {profile_path}")
    required = (
        "createdAtUtc",
        "windowStartedAtUtc",
        "dailyBudgetTokens",
        "safetyFactor",
        "reserveRatio",
        "windowHours",
    )
    missing = [field for field in required if field not in profile]
    if missing:
        raise ValueError(f"profile is missing required field(s): {', '.join(missing)}")
    return profile


def read_ledger(ledger_path: Path) -> list[dict[str, Any]]:
    if not ledger_path.exists():
        return []

    entries: list[dict[str, Any]] = []
    with ledger_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                document = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{ledger_path}:{line_number}: invalid JSONL entry: {exc}") from exc
            if isinstance(document, dict):
                entries.append(document)
    return entries


def int_field(entry: dict[str, Any], field_name: str) -> int:
    value = entry.get(field_name, 0)
    if isinstance(value, bool):
        return 0
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return 0
    return max(parsed, 0)


def entry_timestamp(entry: dict[str, Any]) -> datetime | None:
    value = entry.get("timestampUtc")
    if not isinstance(value, str) or not value:
        return None
    try:
        return parse_utc(value, "timestampUtc")
    except ValueError:
        return None


def successful_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in entries
        if entry.get("finalStatus") in SUCCESSFUL_STATUSES and int_field(entry, "acceptedFileCount") > 0
    ]


def compute_budget(profile: dict[str, Any], entries: list[dict[str, Any]], target: int | None = None) -> dict[str, Any]:
    window_started = parse_utc(str(profile["windowStartedAtUtc"]), "windowStartedAtUtc")
    successful = successful_entries(entries)

    historical_accepted_files = sum(int_field(entry, "acceptedFileCount") for entry in successful)
    historical_tokens = sum(int_field(entry, "totalTokens") for entry in successful)
    costs_per_file = [
        int_field(entry, "totalTokens") / int_field(entry, "acceptedFileCount")
        for entry in successful
        if int_field(entry, "acceptedFileCount") > 0
    ]

    average = historical_tokens / historical_accepted_files if historical_accepted_files else 0.0
    max_cost = max(costs_per_file) if costs_per_file else 0.0

    tokens_used_in_current_window = 0
    for entry in entries:
        timestamp = entry_timestamp(entry)
        if timestamp is not None and timestamp >= window_started:
            tokens_used_in_current_window += int_field(entry, "totalTokens")

    daily_budget = int(profile["dailyBudgetTokens"])
    safety_factor = float(profile["safetyFactor"])
    reserve_ratio = float(profile["reserveRatio"])
    reserve_tokens = daily_budget * reserve_ratio
    usable_remaining = daily_budget - tokens_used_in_current_window - reserve_tokens

    estimated_cost = None
    if target is not None and average > 0:
        estimated_cost = average * target * safety_factor

    recommended_max_target = 0
    if average > 0 and safety_factor > 0:
        recommended_max_target = max(0, math.floor(usable_remaining / (average * safety_factor)))

    return {
        "historicalAcceptedFiles": historical_accepted_files,
        "historicalTokens": historical_tokens,
        "averageTokensPerAcceptedFile": average,
        "maxTokensPerAcceptedFile": max_cost,
        "tokensUsedInCurrentWindow": tokens_used_in_current_window,
        "reserveTokens": reserve_tokens,
        "usableRemainingTokens": usable_remaining,
        "estimatedCostForTarget": estimated_cost,
        "recommendedMaxTarget": recommended_max_target,
    }


def suggested_command(target: int, estimated_cost: float, safety_factor: float) -> str:
    return (
        f"make autocycle N={target} TOKEN_BUDGET={math.ceil(estimated_cost)} "
        f"BUDGET_SAFETY_FACTOR={safety_factor:g}"
    )


def missing_profile_message(profile_path: Path, repo_root: Path = REPOSITORY_ROOT) -> str:
    return (
        f"Budget profile is missing: {repository_relative(profile_path, repo_root)}\n"
        "Create one with: python3 scripts/rkm-budget.py init --daily-budget TOKENS"
    )


def missing_history_message(ledger_path: Path, repo_root: Path = REPOSITORY_ROOT) -> str:
    return (
        f"No usable accepted-run history found in {repository_relative(ledger_path, repo_root)}.\n"
        "Run a small autocycle first, then record it in the run ledger."
    )


def command_init(args: argparse.Namespace) -> int:
    profile = build_profile(
        daily_budget_tokens=args.daily_budget,
        safety_factor=args.safety_factor,
        reserve_ratio=args.reserve_ratio,
        window_hours=args.window_hours,
    )
    write_profile(DEFAULT_PROFILE_PATH, profile)
    print(json.dumps(profile, indent=2, sort_keys=True))
    return 0


def command_report(args: argparse.Namespace) -> int:
    profile_path = resolve_path(args.profile, DEFAULT_PROFILE_PATH)
    ledger_path = resolve_path(args.ledger, DEFAULT_LEDGER_PATH)

    if not profile_path.exists():
        print(missing_profile_message(profile_path))
        return 0

    try:
        profile = load_profile(profile_path)
        entries = read_ledger(ledger_path)
        budget = compute_budget(profile, entries)
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    lines = [
        "RKM budget report",
        f"profile: {repository_relative(profile_path)}",
        f"ledger: {repository_relative(ledger_path)}",
        f"window started UTC: {profile['windowStartedAtUtc']}",
        f"daily budget tokens: {int(profile['dailyBudgetTokens'])}",
        f"safety factor: {float(profile['safetyFactor']):g}",
        f"reserve ratio: {float(profile['reserveRatio']):g}",
        f"historical accepted files: {budget['historicalAcceptedFiles']}",
        f"historical tokens: {budget['historicalTokens']}",
        f"average tokens per accepted file: {budget['averageTokensPerAcceptedFile']:.2f}",
        f"max tokens per accepted file: {budget['maxTokensPerAcceptedFile']:.2f}",
        f"tokens used in current window: {budget['tokensUsedInCurrentWindow']}",
        f"reserve tokens: {budget['reserveTokens']:.2f}",
        f"usable remaining tokens: {budget['usableRemainingTokens']:.2f}",
        f"recommended max target: {budget['recommendedMaxTarget']}",
    ]

    if budget["historicalAcceptedFiles"] <= 0:
        lines.append(missing_history_message(ledger_path))
    elif budget["recommendedMaxTarget"] > 0:
        target = int(budget["recommendedMaxTarget"])
        estimated = float(budget["averageTokensPerAcceptedFile"]) * target * float(profile["safetyFactor"])
        lines.append(f"suggested command: {suggested_command(target, estimated, float(profile['safetyFactor']))}")
    else:
        lines.append("suggested command: reset the window or increase the daily budget before running autocycle.")

    print("\n".join(lines))
    return 0


def command_check(args: argparse.Namespace) -> int:
    profile_path = resolve_path(args.profile, DEFAULT_PROFILE_PATH)
    ledger_path = resolve_path(args.ledger, DEFAULT_LEDGER_PATH)

    if not profile_path.exists():
        print(missing_profile_message(profile_path), file=sys.stderr)
        return 2

    try:
        profile = load_profile(profile_path)
        entries = read_ledger(ledger_path)
        budget = compute_budget(profile, entries, args.target)
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if budget["historicalAcceptedFiles"] <= 0 or budget["estimatedCostForTarget"] is None:
        print(missing_history_message(ledger_path), file=sys.stderr)
        return 2

    estimated = float(budget["estimatedCostForTarget"])
    remaining = float(budget["usableRemainingTokens"])
    suggestion = suggested_command(args.target, estimated, float(profile["safetyFactor"]))
    status = "within budget" if estimated <= remaining else "over budget"
    print(f"target: {args.target}")
    print(f"estimated cost for target: {estimated:.2f}")
    print(f"usable remaining tokens: {remaining:.2f}")
    print(f"recommended max target: {budget['recommendedMaxTarget']}")
    print(f"status: {status}")
    print(f"suggested command: {suggestion}")
    return 0 if estimated <= remaining else 3


def command_reset_window(args: argparse.Namespace) -> int:
    profile_path = resolve_path(args.profile, DEFAULT_PROFILE_PATH)
    if not profile_path.exists():
        print(missing_profile_message(profile_path), file=sys.stderr)
        return 2

    try:
        profile = load_profile(profile_path)
        profile["windowStartedAtUtc"] = utc_text(utc_now())
        write_profile(profile_path, profile)
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(profile, indent=2, sort_keys=True))
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a local RKM token budget profile.")
    parser.add_argument("--self-test", action="store_true", help="run isolated self-tests")

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="create the default budget profile")
    init_parser.add_argument("--daily-budget", type=positive_int, required=True, metavar="TOKENS")
    init_parser.add_argument("--safety-factor", type=positive_float, default=DEFAULT_SAFETY_FACTOR)
    init_parser.add_argument("--reserve-ratio", type=ratio_float, default=DEFAULT_RESERVE_RATIO)
    init_parser.add_argument("--window-hours", type=positive_int, default=DEFAULT_WINDOW_HOURS, metavar="HOURS")
    init_parser.set_defaults(func=command_init)

    report_parser = subparsers.add_parser("report", help="print a budget report")
    report_parser.add_argument("--profile")
    report_parser.add_argument("--ledger")
    report_parser.set_defaults(func=command_report)

    check_parser = subparsers.add_parser("check", help="check whether a target fits the usable budget")
    check_parser.add_argument("--target", type=positive_int, required=True, metavar="N")
    check_parser.add_argument("--profile")
    check_parser.add_argument("--ledger")
    check_parser.set_defaults(func=command_check)

    reset_parser = subparsers.add_parser("reset-window", help="reset the profile window start to now")
    reset_parser.add_argument("--profile")
    reset_parser.set_defaults(func=command_reset_window)

    return parser


def run_cli(argv: list[str]) -> int:
    parser = make_parser()
    args = parser.parse_args(argv[1:])
    if args.self_test:
        return run_self_test()
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    return int(args.func(args))


def capture_result(func: Any, args: argparse.Namespace) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = func(args)
    return code, stdout.getvalue(), stderr.getvalue()


def write_test_ledger(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_self_test() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="rkm-budget-test-") as temp_dir:
            root = Path(temp_dir)
            profile_path = root / ".rkm" / "budget-profile.json"
            ledger_path = root / ".rkm" / "run-ledger.jsonl"
            old_entry_time = "2026-07-10T00:00:00Z"
            current_entry_time = "2026-07-12T10:00:00Z"
            profile_time = parse_utc("2026-07-12T00:00:00Z")

            profile = build_profile(
                daily_budget_tokens=1000,
                safety_factor=2.0,
                reserve_ratio=0.25,
                window_hours=24,
                now=profile_time,
            )
            write_profile(profile_path, profile)
            loaded = load_profile(profile_path)
            assert_true(loaded["dailyBudgetTokens"] == 1000, "init/write profile behavior failed")

            write_test_ledger(
                ledger_path,
                [
                    {
                        "timestampUtc": old_entry_time,
                        "finalStatus": "ACCEPTED",
                        "acceptedFileCount": 2,
                        "totalTokens": 200,
                    },
                    {
                        "timestampUtc": current_entry_time,
                        "finalStatus": "RECOVERED",
                        "acceptedFileCount": 1,
                        "totalTokens": 100,
                    },
                    {
                        "timestampUtc": current_entry_time,
                        "finalStatus": "FAILED",
                        "acceptedFileCount": 0,
                        "totalTokens": 50,
                    },
                ],
            )

            budget = compute_budget(loaded, read_ledger(ledger_path), target=1)
            assert_true(budget["historicalAcceptedFiles"] == 3, "historical accepted file count failed")
            assert_true(budget["historicalTokens"] == 300, "historical token count failed")
            assert_true(budget["averageTokensPerAcceptedFile"] == 100, "average cost failed")
            assert_true(budget["maxTokensPerAcceptedFile"] == 100, "max cost failed")
            assert_true(budget["tokensUsedInCurrentWindow"] == 150, "current window token count failed")
            assert_true(budget["reserveTokens"] == 250, "reserve calculation failed")
            assert_true(budget["usableRemainingTokens"] == 600, "usable remaining calculation failed")
            assert_true(budget["estimatedCostForTarget"] == 200, "target estimate failed")
            assert_true(budget["recommendedMaxTarget"] == 3, "recommended max target failed")

            report_args = argparse.Namespace(profile=str(profile_path), ledger=str(ledger_path))
            code, out, err = capture_result(command_report, report_args)
            assert_true(code == 0 and "recommended max target: 3" in out and err == "", "report behavior failed")

            check_args = argparse.Namespace(target=3, profile=str(profile_path), ledger=str(ledger_path))
            code, out, err = capture_result(command_check, check_args)
            assert_true(code == 0 and "status: within budget" in out and "make autocycle N=3" in out and err == "", "within-budget check failed")

            over_args = argparse.Namespace(target=4, profile=str(profile_path), ledger=str(ledger_path))
            code, out, err = capture_result(command_check, over_args)
            assert_true(code == 3 and "status: over budget" in out and err == "", "over-budget check failed")

            missing_profile_args = argparse.Namespace(target=1, profile=str(root / "missing.json"), ledger=str(ledger_path))
            code, out, err = capture_result(command_check, missing_profile_args)
            assert_true(code == 2 and out == "" and "init --daily-budget TOKENS" in err, "missing profile case failed")

            no_history_ledger = root / ".rkm" / "no-history.jsonl"
            write_test_ledger(
                no_history_ledger,
                [{"timestampUtc": current_entry_time, "finalStatus": "FAILED", "acceptedFileCount": 0, "totalTokens": 75}],
            )
            no_history_args = argparse.Namespace(target=1, profile=str(profile_path), ledger=str(no_history_ledger))
            code, out, err = capture_result(command_check, no_history_args)
            assert_true(code == 2 and out == "" and "small autocycle" in err, "missing history case failed")

            before_reset = load_profile(profile_path)
            reset_args = argparse.Namespace(profile=str(profile_path))
            code, out, err = capture_result(command_reset_window, reset_args)
            after_reset = load_profile(profile_path)
            assert_true(code == 0 and err == "" and "windowStartedAtUtc" in out, "reset-window output failed")
            assert_true(after_reset["createdAtUtc"] == before_reset["createdAtUtc"], "reset changed createdAtUtc")
            assert_true(after_reset["dailyBudgetTokens"] == before_reset["dailyBudgetTokens"], "reset changed dailyBudgetTokens")
            assert_true(after_reset["windowStartedAtUtc"] != before_reset["windowStartedAtUtc"], "reset did not update window")

        print("Self-test passed: init, report, check, reset-window, missing cases, and recommendation math verified.")
        return 0
    except AssertionError as exc:
        print(f"ERROR: self-test failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run_cli(sys.argv))
