#!/usr/bin/env python3
"""Produce a read-only recovery plan for the local RKM repository."""

from __future__ import annotations

import argparse
import contextlib
import io
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
LEDGER_PATH = REPOSITORY_ROOT / ".rkm" / "run-ledger.jsonl"
LOG_PATHS = (
    Path("/tmp/rkm-cycle-output.txt"),
    Path("/tmp/rkm-recover-revise-output.txt"),
    Path("/tmp/rkm-recover-revise-review.txt"),
)
VERDICTS = ("ACCEPT", "REVISE", "STOP")
SUMMARY_HEADING = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(verdict|reasons?|required\s+fix(?:es)?)\s*:", re.IGNORECASE)
VERDICT_LINE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?verdict(?:\*\*)?\s*:\s*`?(ACCEPT|REVISE|STOP)`?\s*$",
    re.IGNORECASE,
)
STANDALONE_VERDICT = re.compile(r"^\s*(?:`|\*\*|`?\*\*)?(ACCEPT|REVISE|STOP)(?:`|\*\*)?\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class PlanInputs:
    status_lines: list[str]
    latest_ledger_final_status: str | None
    latest_ledger_label: str | None
    latest_ledger_timestamp_utc: str | None
    latest_verdicts: list[str]
    latest_touched_file: str | None
    reviewer_summary: str
    recovery_attempted: bool
    recovery_still_revise: bool
    log_sources: list[str]


@dataclass(frozen=True)
class RecoveryPlan:
    status: str
    is_clean: bool
    dirty_files: list[str]
    changed_project_files: list[str]
    ide_files: list[str]
    latest_ledger_final_status: str | None
    latest_ledger_label: str | None
    latest_ledger_timestamp_utc: str | None
    latest_verdicts: list[str]
    latest_touched_file: str | None
    latest_ledger_is_historical: bool
    reviewer_summary: str
    recovery_attempted: bool
    recovery_still_revise: bool
    recommended_command: str | None
    reason: str
    log_sources: list[str]


def run_command(args: list[str], repo_root: Path = REPOSITORY_ROOT) -> tuple[int, str, str]:
    completed = subprocess.run(
        args,
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def status_path(status_line: str) -> str:
    if len(status_line) >= 3 and status_line[2] == " ":
        path = status_line[3:].strip()
    else:
        parts = status_line.split(maxsplit=1)
        path = parts[1].strip() if len(parts) == 2 else ""
    if " -> " in path:
        path = path.rsplit(" -> ", 1)[1].strip()
    return path.rstrip("/")


def is_ide_path(path: str) -> bool:
    name = Path(path).name.lower()
    return path == ".idea" or path.startswith(".idea/") or name in {".classpath", ".project", ".settings"}


def is_project_path(path: str) -> bool:
    if not path or is_ide_path(path):
        return False
    if path.startswith(".git/") or path.startswith(".rkm/"):
        return False
    return True


def dirty_files(status_lines: list[str]) -> list[str]:
    return [path for path in (status_path(line) for line in status_lines) if path]


def changed_project_files(status_lines: list[str]) -> list[str]:
    return [path for path in dirty_files(status_lines) if is_project_path(path)]


def ide_files(status_lines: list[str]) -> list[str]:
    return [path for path in dirty_files(status_lines) if is_ide_path(path)]


def extract_verdicts(text: str) -> list[str]:
    verdicts: list[str] = []
    for line in text.splitlines():
        labeled = VERDICT_LINE.match(line)
        if labeled:
            verdicts.append(labeled.group(1).upper())
            continue
        standalone = STANDALONE_VERDICT.match(line)
        if standalone:
            verdicts.append(standalone.group(1).upper())
    return verdicts


def read_text_if_present(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def read_ledger_entries(path: Path = LEDGER_PATH) -> list[dict[str, Any]]:
    text = read_text_if_present(path)
    if text is None:
        return []
    entries: list[dict[str, Any]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            entry = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict):
            entries.append(entry)
    return entries


def latest_relevant_ledger(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    for entry in reversed(entries):
        final_status = entry.get("finalStatus")
        final_verdict = entry.get("finalVerdict")
        label = entry.get("label")
        if isinstance(final_status, str) and final_status:
            return entry
        if isinstance(final_verdict, str) and final_verdict:
            return entry
        if isinstance(label, str) and "recovery" in label.lower():
            return entry
    return entries[-1] if entries else None


def entry_string(entry: dict[str, Any], key: str) -> str | None:
    value = entry.get(key)
    return value if isinstance(value, str) and value else None


def entry_verdicts(entry: dict[str, Any] | None) -> list[str]:
    if entry is None:
        return []
    value = entry.get("verdicts")
    if isinstance(value, list):
        verdicts = [item.upper() for item in value if isinstance(item, str) and item.upper() in VERDICTS]
        if verdicts:
            return verdicts
    final_verdict = entry_string(entry, "finalVerdict")
    return [final_verdict.upper()] if final_verdict and final_verdict.upper() in VERDICTS else []


def entry_touched_file(entry: dict[str, Any] | None) -> str | None:
    if entry is None:
        return None
    files = entry.get("files")
    if isinstance(files, list):
        for item in reversed(files):
            if isinstance(item, str) and item:
                return item
    return None


def read_log_sources() -> dict[str, str]:
    logs: dict[str, str] = {}
    for path in LOG_PATHS:
        text = read_text_if_present(path)
        if text is not None:
            logs[path.as_posix()] = text
    return logs


def reviewer_summary_from_texts(texts: list[str], limit: int = 30) -> str:
    selected: list[str] = []
    for text in texts:
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if SUMMARY_HEADING.search(line):
                start = max(0, index - 1)
                end = min(len(lines), index + 5)
                for candidate in lines[start:end]:
                    stripped = candidate.rstrip()
                    if stripped and stripped not in selected:
                        selected.append(stripped)
                        if len(selected) >= limit:
                            return "\n".join(selected)
    return "\n".join(selected[:limit])


def recovery_attempted_from(entry: dict[str, Any] | None, logs: dict[str, str]) -> bool:
    if entry is not None:
        label = entry_string(entry, "label")
        if label and "recovery" in label.lower():
            return True
        if bool(entry.get("hasRecovery")):
            return True
    return any("rkm-recover-revise" in source or "recover-revise" in text for source, text in logs.items())


def recovery_still_revise_from(entry: dict[str, Any] | None, logs: dict[str, str]) -> bool:
    review_text = logs.get("/tmp/rkm-recover-revise-review.txt")
    if review_text is not None:
        verdicts = extract_verdicts(review_text)
        if verdicts:
            return verdicts[-1] == "REVISE"
    if entry is not None:
        label = entry_string(entry, "label")
        verdicts = entry_verdicts(entry)
        if label and "recovery" in label.lower() and verdicts:
            return verdicts[-1] == "REVISE"
    return False


def collect_inputs(repo_root: Path = REPOSITORY_ROOT) -> PlanInputs:
    code, stdout, _stderr = run_command(["git", "status", "--short"], repo_root)
    status_lines = stdout.splitlines() if code == 0 else []
    entries = read_ledger_entries(repo_root / ".rkm" / "run-ledger.jsonl")
    latest = latest_relevant_ledger(entries)
    logs = read_log_sources()
    log_verdicts: list[str] = []
    for text in logs.values():
        log_verdicts.extend(extract_verdicts(text))
    ledger_verdicts = entry_verdicts(latest)
    latest_verdicts = log_verdicts if log_verdicts else ledger_verdicts

    return PlanInputs(
        status_lines=status_lines,
        latest_ledger_final_status=entry_string(latest, "finalStatus") if latest else None,
        latest_ledger_label=entry_string(latest, "label") if latest else None,
        latest_ledger_timestamp_utc=entry_string(latest, "timestampUtc") if latest else None,
        latest_verdicts=latest_verdicts,
        latest_touched_file=entry_touched_file(latest),
        reviewer_summary=reviewer_summary_from_texts(list(logs.values())),
        recovery_attempted=recovery_attempted_from(latest, logs),
        recovery_still_revise=recovery_still_revise_from(latest, logs),
        log_sources=list(logs.keys()),
    )


def manual_fix_command(path: str) -> str:
    return f'make codex-commit PROMPT_FILE=path/to/manual-fix-prompt.md FILE="{path}" MESSAGE="Fix reviewer findings for {path}"'


def decide(inputs: PlanInputs) -> RecoveryPlan:
    dirty = dirty_files(inputs.status_lines)
    project_files = changed_project_files(inputs.status_lines)
    ide = ide_files(inputs.status_lines)
    is_clean = not dirty
    latest_verdict = inputs.latest_verdicts[-1] if inputs.latest_verdicts else None
    single_project_file = project_files[0] if len(project_files) == 1 else None
    ledger_matches_dirty_file = (
        single_project_file is not None
        and (inputs.latest_touched_file is None or inputs.latest_touched_file == single_project_file)
    )
    latest_ledger_is_historical = (
        is_clean
        and inputs.latest_ledger_final_status in {"REVISE_PENDING", "FAILED", "STOPPED"}
    )

    status = "MANUAL_REVIEW"
    command: str | None = None
    reason = "manual review required because the repository state is unclear"

    if is_clean:
        status = "NO_RECOVERY_NEEDED"
        reason = "git worktree is clean; any REVISE ledger state is historical"
    elif ide:
        status = "BLOCKED_IDE_FILES"
        command = "rm -rf .idea && make validate"
        reason = "IDE files are present in the git worktree"
    elif latest_verdict == "STOP":
        status = "MANUAL_REVIEW"
        reason = "latest reviewer verdict is STOP"
    elif len(project_files) > 1:
        status = "MANUAL_REVIEW"
        reason = "multiple changed project files are present"
    elif len(project_files) == 1 and inputs.recovery_still_revise and ledger_matches_dirty_file:
        status = "RECOVERY_FAILED_NEEDS_MANUAL_FIX"
        command = manual_fix_command(project_files[0])
        reason = "recovery was already attempted and the latest recovery review still says REVISE"
    elif len(project_files) == 1 and inputs.latest_ledger_final_status == "REVISE_PENDING" and ledger_matches_dirty_file:
        status = "RECOVERY_AVAILABLE"
        command = "make recover-revise"
        reason = "one changed project file has a latest relevant REVISE_PENDING ledger status"
    elif len(project_files) == 1:
        status = "MANUAL_REVIEW"
        reason = "one changed project file exists, but the ledger state is missing or unclear"
    else:
        status = "MANUAL_REVIEW"
        reason = "dirty worktree has no recoverable project file"

    return RecoveryPlan(
        status=status,
        is_clean=is_clean,
        dirty_files=dirty,
        changed_project_files=project_files,
        ide_files=ide,
        latest_ledger_final_status=inputs.latest_ledger_final_status,
        latest_ledger_label=inputs.latest_ledger_label,
        latest_ledger_timestamp_utc=inputs.latest_ledger_timestamp_utc,
        latest_verdicts=inputs.latest_verdicts,
        latest_touched_file=inputs.latest_touched_file,
        latest_ledger_is_historical=latest_ledger_is_historical,
        reviewer_summary=inputs.reviewer_summary,
        recovery_attempted=inputs.recovery_attempted,
        recovery_still_revise=inputs.recovery_still_revise,
        recommended_command=command,
        reason=reason,
        log_sources=inputs.log_sources,
    )


def plan_to_json(plan: RecoveryPlan) -> dict[str, Any]:
    return {
        "status": plan.status,
        "isClean": plan.is_clean,
        "dirtyFiles": plan.dirty_files,
        "changedProjectFiles": plan.changed_project_files,
        "ideFiles": plan.ide_files,
        "latestLedgerFinalStatus": plan.latest_ledger_final_status,
        "latestLedgerLabel": plan.latest_ledger_label,
        "latestLedgerTimestampUtc": plan.latest_ledger_timestamp_utc,
        "latestVerdicts": plan.latest_verdicts,
        "latestTouchedFile": plan.latest_touched_file,
        "latestLedgerIsHistorical": plan.latest_ledger_is_historical,
        "reviewerSummary": plan.reviewer_summary,
        "recoveryAttempted": plan.recovery_attempted,
        "recoveryStillRevise": plan.recovery_still_revise,
        "recommendedCommand": plan.recommended_command,
        "reason": plan.reason,
        "logSources": plan.log_sources,
    }


def print_human(plan: RecoveryPlan, verbose: bool = False) -> None:
    print(f"status: {plan.status}")
    print(f"reason: {plan.reason}")
    print(f"is clean: {str(plan.is_clean).lower()}")
    print(f"dirty files: {', '.join(plan.dirty_files) if plan.dirty_files else '(none)'}")
    print(f"changed project files: {', '.join(plan.changed_project_files) if plan.changed_project_files else '(none)'}")
    print(f"IDE files: {', '.join(plan.ide_files) if plan.ide_files else '(none)'}")
    historical_marker = " (historical)" if plan.latest_ledger_is_historical else ""
    print(f"latest ledger finalStatus: {plan.latest_ledger_final_status or '(unknown)'}{historical_marker}")
    print(f"latest ledger label: {plan.latest_ledger_label or '(unknown)'}")
    print(f"latest ledger timestampUtc: {plan.latest_ledger_timestamp_utc or '(unknown)'}")
    print(f"latest ledger is historical: {str(plan.latest_ledger_is_historical).lower()}")
    print(f"latest verdicts: {', '.join(plan.latest_verdicts) if plan.latest_verdicts else '(none)'}")
    print(f"latest touched file: {plan.latest_touched_file or '(unknown)'}")
    print(f"recovery attempted: {str(plan.recovery_attempted).lower()}")
    print(f"recovery still REVISE: {str(plan.recovery_still_revise).lower()}")
    print(f"recommended command: {plan.recommended_command or '(none)'}")
    print(f"log sources: {', '.join(plan.log_sources) if plan.log_sources else '(none)'}")
    if plan.reviewer_summary and (verbose or not plan.latest_ledger_is_historical):
        print("reviewer summary:")
        print(plan.reviewer_summary)


def render_human(plan: RecoveryPlan, verbose: bool = False) -> str:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        print_human(plan, verbose)
    return output.getvalue()


def assert_plan(name: str, inputs: PlanInputs, expected: str) -> list[str]:
    actual = decide(inputs).status
    if actual == expected:
        return []
    return [f"{name}: expected {expected}, got {actual}"]


def test_inputs(
    status_lines: list[str] | None = None,
    latest_ledger_final_status: str | None = None,
    latest_verdicts: list[str] | None = None,
    reviewer_summary: str = "",
    recovery_attempted: bool = False,
    recovery_still_revise: bool = False,
) -> PlanInputs:
    return PlanInputs(
        status_lines=status_lines or [],
        latest_ledger_final_status=latest_ledger_final_status,
        latest_ledger_label=None,
        latest_ledger_timestamp_utc=None,
        latest_verdicts=latest_verdicts or [],
        latest_touched_file=None,
        reviewer_summary=reviewer_summary,
        recovery_attempted=recovery_attempted,
        recovery_still_revise=recovery_still_revise,
        log_sources=[],
    )


def run_self_test() -> int:
    failures: list[str] = []
    failures.extend(assert_plan("clean repo", test_inputs(), "NO_RECOVERY_NEEDED"))
    clean_revise_plan = decide(
        test_inputs(
            latest_ledger_final_status="REVISE_PENDING",
            latest_verdicts=["REVISE"],
            reviewer_summary="reviewer summary detail",
        )
    )
    clean_revise_output = render_human(clean_revise_plan)
    clean_revise_verbose_output = render_human(clean_revise_plan, verbose=True)
    clean_revise_json = plan_to_json(clean_revise_plan)
    if clean_revise_plan.status != "NO_RECOVERY_NEEDED":
        failures.append(f"clean REVISE_PENDING ledger: expected NO_RECOVERY_NEEDED, got {clean_revise_plan.status}")
    if clean_revise_plan.reason != "git worktree is clean; any REVISE ledger state is historical":
        failures.append("clean REVISE_PENDING ledger: reason does not clarify historical ledger state")
    if clean_revise_plan.latest_ledger_is_historical is not True:
        failures.append("clean REVISE_PENDING ledger: expected latest_ledger_is_historical true")
    if clean_revise_plan.recommended_command is not None:
        failures.append("clean REVISE_PENDING ledger: expected no recommended command")
    if clean_revise_json.get("latestLedgerIsHistorical") is not True:
        failures.append("clean REVISE_PENDING ledger: JSON latestLedgerIsHistorical missing or false")
    if "reviewer summary:" in clean_revise_output or "reviewer summary detail" in clean_revise_output:
        failures.append("clean REVISE_PENDING ledger: default human output should not show reviewer summary")
    if "latest ledger finalStatus: REVISE_PENDING (historical)" not in clean_revise_output:
        failures.append("clean REVISE_PENDING ledger: default human output should mark finalStatus historical")
    if "reviewer summary detail" not in clean_revise_verbose_output:
        failures.append("clean REVISE_PENDING ledger: verbose human output should show reviewer summary")
    failures.extend(
        assert_plan(
            "one dirty file with REVISE_PENDING",
            test_inputs([" M docs/architecture/paper-model.md"], "REVISE_PENDING"),
            "RECOVERY_AVAILABLE",
        )
    )
    dirty_revise_plan = decide(
        test_inputs(
            [" M docs/architecture/paper-model.md"],
            "REVISE_PENDING",
            ["REVISE"],
            reviewer_summary="dirty reviewer summary detail",
        )
    )
    dirty_revise_output = render_human(dirty_revise_plan)
    if dirty_revise_plan.status != "RECOVERY_AVAILABLE":
        failures.append(f"dirty REVISE_PENDING ledger: expected RECOVERY_AVAILABLE, got {dirty_revise_plan.status}")
    if dirty_revise_plan.latest_ledger_is_historical is not False:
        failures.append("dirty REVISE_PENDING ledger: expected latest_ledger_is_historical false")
    if "dirty reviewer summary detail" not in dirty_revise_output:
        failures.append("dirty REVISE_PENDING ledger: default human output should show reviewer summary")
    failures.extend(
        assert_plan(
            "recovery review still REVISE",
            test_inputs(
                [" M docs/architecture/paper-model.md"],
                "REVISE_PENDING",
                ["REVISE"],
                recovery_attempted=True,
                recovery_still_revise=True,
            ),
            "RECOVERY_FAILED_NEEDS_MANUAL_FIX",
        )
    )
    failures.extend(
        assert_plan(
            "IDE files",
            test_inputs(["?? .idea/workspace.xml"], "REVISE_PENDING"),
            "BLOCKED_IDE_FILES",
        )
    )
    failures.extend(
        assert_plan(
            "multiple changed files",
            test_inputs([" M docs/architecture/paper-model.md", " M schema/ontology.schema.json"], "REVISE_PENDING"),
            "MANUAL_REVIEW",
        )
    )
    failures.extend(
        assert_plan(
            "STOP verdict",
            test_inputs([" M docs/architecture/paper-model.md"], "STOPPED", ["STOP"]),
            "MANUAL_REVIEW",
        )
    )

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    print("Self-test passed: recovery decision states behave as expected.")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Produce a read-only RKM recovery plan.")
    parser.add_argument("--json", action="store_true", help="print stable JSON output")
    parser.add_argument("--verbose", action="store_true", help="include historical reviewer detail in human output")
    parser.add_argument("--self-test", action="store_true", help="run pure decision self-tests")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.self_test:
        return run_self_test()

    plan = decide(collect_inputs())
    if args.json:
        print(json.dumps(plan_to_json(plan), indent=2, sort_keys=True))
    else:
        print_human(plan, args.verbose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
