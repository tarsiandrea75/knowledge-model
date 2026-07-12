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


def print_dashboard(next_action: dict[str, Any], budget: dict[str, Any], recovery: dict[str, Any], target: int, no_color: bool) -> None:
    global COLOR
    COLOR = color_enabled(no_color)
    use_unicode = unicode_enabled()
    icons = {
        "repo": "◆" if use_unicode else "*",
        "recovery": "↻" if use_unicode else "~",
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

    lines = [
        frame,
        style(title, "bold", COLOR),
        frame,
        row(icons["repo"], "repo status", repo_status, repo_status == "clean", "green"),
        row(icons["recovery"], "recovery status", recovery.get("status")),
        row(icons["budget"], "budget status", budget.get("status") or next_action.get("budgetStatus")),
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
    print("\n".join(lines))


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

    clean = {"isClean": True, "status": "NO_RECOVERY_NEEDED"}
    check("recover", {"status": "READY_TO_AUTOCYCLE"}, {}, {"status": "RECOVERY_AVAILABLE"}, Decision("RECOVER", "make autopilot-recover"))
    check("manual", {"status": "READY_TO_AUTOCYCLE"}, {}, {"status": "MANUAL_REVIEW"}, Decision("STOP", "make recovery-plan"))
    check("dirty", {"repoStatus": "dirty", "status": "READY_TO_AUTOCYCLE"}, {}, clean, Decision("STOP", "make recovery-plan"))
    check("run", {"status": "READY_TO_AUTOCYCLE"}, {}, clean, Decision("RUN", "make autopilot"))
    check("reduced", {"status": "OVER_BUDGET"}, {"recommendedMaxTarget": 2}, clean, Decision("RUN_REDUCED_TARGET", "make autopilot N=2"))
    check("budget-blocked", {"status": "OVER_BUDGET"}, {"recommendedMaxTarget": 0}, clean, Decision("BUDGET_BLOCKED", "make budget-report"))
    check("push", {"status": "READY_TO_PUSH"}, {}, clean, Decision("PUSH", "make safe-push"))
    check("review", {"status": "WAIT", "command": "make recovery-plan"}, {}, clean, Decision("REVIEW", "make recovery-plan"))
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
