#!/usr/bin/env python3
"""Print a compact read-only RKM automation cockpit summary."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = 3
STOP_RECOVERY_STATUSES = {
    "RECOVERY_FAILED_NEEDS_MANUAL_FIX",
    "MANUAL_REVIEW",
    "BLOCKED_IDE_FILES",
    "STOP",
    "STOPPED",
    "BLOCKED",
}


@dataclass(frozen=True)
class Decision:
    decision: str
    command: str


@dataclass(frozen=True)
class RecentRunSummary:
    available: bool
    accepted: int = 0
    recovered: int = 0
    revise_pending: int = 0
    partial: bool = False
    budget_stop: bool = False
    push_pending: bool = False


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        args,
        cwd=REPOSITORY_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        return {"_error": completed.stderr.strip() or completed.stdout.strip(), "_exitCode": completed.returncode}
    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {"_error": f"invalid JSON: {exc}", "_exitCode": completed.returncode}
    return parsed if isinstance(parsed, dict) else {"_error": "JSON output was not an object"}


def read_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def read_jsonl_file(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for line in lines:
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            entries.append(parsed)
    return entries


def repo_is_dirty(next_action: dict[str, Any], recovery: dict[str, Any]) -> bool:
    if next_action.get("repoStatus") == "dirty":
        return True
    if recovery.get("isClean") is False:
        return True
    dirty_files = next_action.get("dirtyFiles") or recovery.get("dirtyFiles")
    return isinstance(dirty_files, list) and len(dirty_files) > 0


def recommended_max_target(budget: dict[str, Any], next_action: dict[str, Any]) -> int:
    for source in (budget, next_action):
        value = source.get("recommendedMaxTarget")
        if isinstance(value, bool):
            continue
        try:
            return max(int(value), 0)
        except (TypeError, ValueError):
            continue
    return 0


def int_value(value: Any, fallback: int = 0) -> int:
    if isinstance(value, bool):
        return fallback
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def decide(next_action: dict[str, Any], budget: dict[str, Any], recovery: dict[str, Any]) -> Decision:
    recovery_status = str(recovery.get("status") or "").upper()
    next_status = str(next_action.get("status") or "").upper()
    max_target = recommended_max_target(budget, next_action)

    if recovery_status == "RECOVERY_AVAILABLE":
        return Decision("RECOVER", "make autopilot-recover")
    if recovery_status in STOP_RECOVERY_STATUSES or "MANUAL" in recovery_status or "BLOCKED" in recovery_status:
        return Decision("STOP", "make recovery-plan")
    if repo_is_dirty(next_action, recovery):
        return Decision("STOP", "make recovery-plan")
    if next_status == "READY_TO_AUTOCYCLE":
        return Decision("RUN", "make autopilot")
    if next_status == "OVER_BUDGET" and max_target > 0:
        return Decision("RUN_REDUCED_TARGET", f"make autopilot N={max_target}")
    if next_status == "OVER_BUDGET":
        return Decision("BUDGET_BLOCKED", "make budget-report")
    if next_status == "READY_TO_PUSH":
        return Decision("PUSH", "make safe-push")

    fallback = next_action.get("command") or budget.get("suggestedCommand") or recovery.get("recommendedCommand")
    return Decision("REVIEW", fallback if isinstance(fallback, str) and fallback else "make cockpit")


def color_enabled(no_color: bool) -> bool:
    return not no_color and "NO_COLOR" not in os.environ and sys.stdout.isatty()


def unicode_enabled() -> bool:
    encoding = (sys.stdout.encoding or "").lower()
    return "utf" in encoding


def style(text: str, color: str, enabled: bool) -> str:
    colors = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "cyan": "36",
        "bold": "1",
    }
    if not enabled:
        return text
    return f"\033[{colors[color]}m{text}\033[0m"


def decision_color(decision: str) -> str:
    if decision in {"RUN", "RUN_REDUCED_TARGET", "PUSH"}:
        return "green"
    if decision in {"RECOVER", "REVIEW"}:
        return "yellow"
    return "red"


def safe_text(value: Any, fallback: str = "unknown") -> str:
    if value is None:
        return fallback
    text = str(value)
    return text if text else fallback


def row(icon: str, label: str, value: Any, color: bool = False, color_name: str = "cyan") -> str:
    text = safe_text(value)
    if color:
        text = style(text, color_name, COLOR)
    return f"{icon} {label:<27} -> {text}"


def meaningful_ledger_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [entry for entry in entries if entry.get("label") != "autocycle-recovery-review"]


def recent_entries_for_state(entries: list[dict[str, Any]], state: dict[str, Any]) -> list[dict[str, Any]]:
    meaningful = meaningful_ledger_entries(entries)
    target = int_value(state.get("target"), 0)
    if target <= 0:
        return meaningful[-20:]

    selected_reversed: list[dict[str, Any]] = []
    accepted = 0
    recovered_files: set[str] = set()
    pending_files: set[str] = set()

    for entry in reversed(meaningful):
        selected_reversed.append(entry)
        status = str(entry.get("finalStatus") or "").upper()
        files = tuple(str(file) for file in entry.get("files") or [] if file)
        label = str(entry.get("label") or "")
        if status == "RECOVERED" and label == "autocycle-recovery":
            recovered_files.update(files)
        elif status == "ACCEPTED":
            accepted += max(int_value(entry.get("acceptedFileCount"), 1), 1)
        elif status == "REVISE_PENDING":
            pending_files.update(files)
        unresolved_pending = pending_files - recovered_files
        if accepted + len(recovered_files) + len(unresolved_pending) >= target:
            break

    return list(reversed(selected_reversed))


def summarize_recent_run(
    state: dict[str, Any],
    ledger_entries: list[dict[str, Any]],
    next_action: dict[str, Any],
) -> RecentRunSummary:
    if not state and not ledger_entries:
        return RecentRunSummary(False)

    recent_entries = recent_entries_for_state(ledger_entries, state)
    accepted = 0
    recovered_files: set[str] = set()
    pending_files: set[str] = set()

    for entry in recent_entries:
        status = str(entry.get("finalStatus") or "").upper()
        label = str(entry.get("label") or "")
        files = tuple(str(file) for file in entry.get("files") or [] if file)
        if status == "ACCEPTED":
            accepted += max(int_value(entry.get("acceptedFileCount"), 1), 1)
        elif status == "RECOVERED" and label == "autocycle-recovery":
            recovered_files.update(files)
        elif status == "REVISE_PENDING":
            pending_files.update(files)

    unresolved_pending = pending_files - recovered_files
    final_outcome = str(state.get("finalOutcome") or "").lower()
    commands_skipped = state.get("commandsSkipped") if isinstance(state.get("commandsSkipped"), list) else []
    skipped_push = any("safe-push" in str(command) for command in commands_skipped)
    exit_failed = int_value(state.get("exitCode"), 0) != 0
    target = int_value(state.get("target"), 0)
    completed = accepted + len(recovered_files)
    partial = (target > 0 and completed < target) or (exit_failed and skipped_push)
    budget_stop = (
        "budget" in final_outcome
        or "token" in final_outcome
        or (exit_failed and skipped_push)
        or str(next_action.get("status") or "").upper() == "OVER_BUDGET"
    )

    return RecentRunSummary(
        True,
        accepted=accepted,
        recovered=len(recovered_files),
        revise_pending=len(unresolved_pending),
        partial=partial,
        budget_stop=budget_stop,
        push_pending=str(next_action.get("status") or "").upper() == "READY_TO_PUSH",
    )


def recent_run_text(summary: RecentRunSummary) -> str | None:
    if not summary.available:
        return None
    state = "partial" if summary.partial else "complete"
    if summary.budget_stop:
        state = f"{state}/budget-stop"
    parts = [state, f"accepted {summary.accepted}", f"recovered {summary.recovered}"]
    if summary.revise_pending:
        parts.append(f"revise pending {summary.revise_pending}")
    if summary.push_pending:
        parts.append("push pending")
    return "; ".join(parts)


def budget_text(next_action: dict[str, Any], budget: dict[str, Any], target: int) -> str:
    next_status = str(next_action.get("status") or "").upper()
    max_target = recommended_max_target(budget, next_action)
    if next_status == "OVER_BUDGET" and max_target > 0:
        return f"target {target} blocked; max safe target {max_target}"
    if next_status == "OVER_BUDGET":
        return f"target {target} blocked"
    if next_status == "READY_TO_AUTOCYCLE":
        return f"target {target} allowed"
    if next_status == "READY_TO_PUSH":
        if max_target > 0:
            return f"info; max safe target {max_target}"
        return "info"
    return safe_text(budget.get("status") or next_action.get("budgetStatus"))


def render_dashboard(
    next_action: dict[str, Any],
    budget: dict[str, Any],
    recovery: dict[str, Any],
    target: int,
    no_color: bool,
    state: dict[str, Any] | None = None,
    ledger_entries: list[dict[str, Any]] | None = None,
) -> str:
    global COLOR
    COLOR = color_enabled(no_color)
    use_unicode = unicode_enabled()
    icons = {
        "repo": "◆" if use_unicode else "*",
        "recovery": "↻" if use_unicode else "~",
        "recent": "↯" if use_unicode else "~",
        "push": "⇡" if use_unicode else "^",
        "budget": "$",
        "target": "→" if use_unicode else ">",
        "next": "▶" if use_unicode else ">",
        "cmd": "›" if use_unicode else ">",
        "decision": "✓" if use_unicode else "!",
    }
    decision = decide(next_action, budget, recovery)
    repo_status = "dirty" if repo_is_dirty(next_action, recovery) else "clean"
    title = " RKM COCKPIT "
    frame = "═" * len(title) if use_unicode else "=" * len(title)
    recent = summarize_recent_run(state or {}, ledger_entries or [], next_action)

    lines = [
        frame,
        style(title, "bold", COLOR),
        frame,
        row(icons["repo"], "repo status", repo_status, repo_status == "clean", "green"),
        row(icons["recovery"], "recovery status", recovery.get("status")),
    ]
    recent_text = recent_run_text(recent)
    if recent_text:
        lines.append(f"{icons['recent']} last run -> {recent_text}")
    if str(next_action.get("status") or "").upper() == "READY_TO_PUSH":
        lines.append(f"{icons['push']} push pending -> make safe-push")
    lines.extend(
        [
        row(icons["budget"], "budget", budget_text(next_action, budget, target)),
        row(icons["target"], "recommended max target", recommended_max_target(budget, next_action)),
        row(icons["next"], f"next-action status T={target}", next_action.get("status")),
        row(icons["cmd"], "current recommended command", next_action.get("command") or recovery.get("recommendedCommand")),
        row(
            icons["decision"],
            "decision",
            decision.decision,
            True,
            decision_color(decision.decision),
        ),
        row(icons["cmd"], "run", decision.command, True, decision_color(decision.decision)),
        ]
    )
    return "\n".join(lines)


def print_dashboard(next_action: dict[str, Any], budget: dict[str, Any], recovery: dict[str, Any], target: int, no_color: bool) -> None:
    state = read_json_file(REPOSITORY_ROOT / ".rkm" / "autopilot-state.json")
    ledger_entries = read_jsonl_file(REPOSITORY_ROOT / ".rkm" / "run-ledger.jsonl")
    print(render_dashboard(next_action, budget, recovery, target, no_color, state, ledger_entries))


def collect(target: int) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    next_action = run_json(["python3", "scripts/rkm-next-action.py", "--target", str(target), "--json"])
    budget = run_json(["python3", "scripts/rkm-budget.py", "report", "--json"])
    recovery = run_json(["python3", "scripts/rkm-recovery-plan.py", "--json"])
    return next_action, budget, recovery


def run_self_test() -> int:
    def check(name: str, next_action: dict[str, Any], budget: dict[str, Any], recovery: dict[str, Any], expected: Decision) -> None:
        actual = decide(next_action, budget, recovery)
        if actual != expected:
            raise AssertionError(f"{name}: expected {expected}, got {actual}")

    def assert_contains(name: str, text: str, expected: str) -> None:
        if expected not in text:
            raise AssertionError(f"{name}: expected to find {expected!r} in:\n{text}")

    clean = {"isClean": True, "status": "NO_RECOVERY_NEEDED"}
    check("recover", {"status": "READY_TO_AUTOCYCLE"}, {}, {"status": "RECOVERY_AVAILABLE"}, Decision("RECOVER", "make autopilot-recover"))
    check("manual", {"status": "READY_TO_AUTOCYCLE"}, {}, {"status": "MANUAL_REVIEW"}, Decision("STOP", "make recovery-plan"))
    check("dirty", {"repoStatus": "dirty", "status": "READY_TO_AUTOCYCLE"}, {}, clean, Decision("STOP", "make recovery-plan"))
    check("run", {"status": "READY_TO_AUTOCYCLE"}, {}, clean, Decision("RUN", "make autopilot"))
    check("reduced", {"status": "OVER_BUDGET"}, {"recommendedMaxTarget": 2}, clean, Decision("RUN_REDUCED_TARGET", "make autopilot N=2"))
    check("budget-blocked", {"status": "OVER_BUDGET"}, {"recommendedMaxTarget": 0}, clean, Decision("BUDGET_BLOCKED", "make budget-report"))
    check("push", {"status": "READY_TO_PUSH"}, {}, clean, Decision("PUSH", "make safe-push"))
    check("review", {"status": "WAIT", "command": "make recovery-plan"}, {}, clean, Decision("REVIEW", "make recovery-plan"))

    recovered_ledger = [
        {"label": "autocycle-cycle", "finalStatus": "ACCEPTED", "acceptedFileCount": 1, "files": ["a.md"]},
        {"label": "autocycle-cycle", "finalStatus": "REVISE_PENDING", "acceptedFileCount": 0, "files": ["b.md"]},
        {"label": "autocycle-recovery", "finalStatus": "RECOVERED", "acceptedFileCount": 1, "files": ["b.md"]},
        {"label": "autocycle-recovery-review", "finalStatus": "RECOVERED", "acceptedFileCount": 1, "files": ["b.md"]},
    ]
    push_dashboard = render_dashboard(
        {"status": "READY_TO_PUSH", "command": "make safe-push"},
        {"recommendedMaxTarget": 1},
        clean,
        3,
        True,
        {"target": 3, "exitCode": 2, "commandsSkipped": ["make safe-push"]},
        recovered_ledger,
    )
    assert_contains("push pending row", push_dashboard, "push pending -> make safe-push")
    assert_contains("recovered count", push_dashboard, "recovered 1")

    over_budget_dashboard = render_dashboard(
        {"status": "OVER_BUDGET", "recommendedMaxTarget": 1},
        {},
        clean,
        3,
        True,
    )
    assert_contains("over budget row", over_budget_dashboard, "target 3 blocked; max safe target 1")

    allowed_dashboard = render_dashboard(
        {"status": "READY_TO_AUTOCYCLE"},
        {},
        clean,
        3,
        True,
    )
    assert_contains("allowed budget row", allowed_dashboard, "target 3 allowed")

    missing_root = REPOSITORY_ROOT / ".missing-rkm-self-test"
    if read_json_file(missing_root / "autopilot-state.json") != {}:
        raise AssertionError("missing state file should return an empty object")
    if read_jsonl_file(missing_root / "run-ledger.jsonl") != []:
        raise AssertionError("missing ledger file should return an empty list")
    render_dashboard({"status": "READY_TO_AUTOCYCLE"}, {}, clean, 3, True, {}, [])

    print("self-test: PASS")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=positive_int, default=DEFAULT_TARGET, help=f"next-action target (default: {DEFAULT_TARGET})")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI color output")
    parser.add_argument("--self-test", action="store_true", help="run decision-rule tests without shelling out")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = parse_args()
    if args.self_test:
        return run_self_test()

    next_action, budget, recovery = collect(args.target)
    print_dashboard(next_action, budget, recovery, args.target, args.no_color)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
