#!/usr/bin/env python3
"""Append and report local JSONL ledger entries for RKM automation runs."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_PATH = REPOSITORY_ROOT / ".rkm" / "run-ledger.jsonl"
VERDICTS = ("ACCEPT", "REVISE", "STOP")

TOKEN_MARKER = re.compile(r"tokens\s+used", re.IGNORECASE)
INTEGER = re.compile(r"\b\d[\d,]*\b")
STANDALONE_VERDICT = re.compile(
    r"^(?:`(?P<code>ACCEPT|REVISE|STOP)`|(?P<plain>ACCEPT|REVISE|STOP)|"
    r"\*\*`(?P<bold_code>ACCEPT|REVISE|STOP)`\*\*|"
    r"\*\*(?P<bold>ACCEPT|REVISE|STOP)\*\*)$"
)
LABELED_VERDICT = re.compile(
    r"^(?:verdict:|Verdict:|\*\*Verdict:\*\*)\s*`?(?P<verdict>ACCEPT|REVISE|STOP)`?$"
)
COMMIT_LINE = re.compile(r"^\[[^\]\s]+\s+(?P<hash>[0-9a-f]{6,40})\]\s+(?P<message>.+)$")
CREATE_MODE_LINE = re.compile(r"^create mode \d{6}\s+(?P<path>\S.+)$")
STATUS_PATH_LINE = re.compile(r"^\s*(?:A|M|D|R|C|\?\?)\s+(?P<path>\S.+)$")
AUTOMATION_PREFIX = re.compile(r"\[(?P<label>rkm-[a-z0-9-]+)\]")
REPO_PATH_TOKEN = re.compile(
    r"(?<![\w./-])(?P<path>"
    r"docs/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+\.md|"
    r"scripts/[A-Za-z0-9._-]+\.(?:sh|py)|"
    r"schema/(?:definitions/)?[A-Za-z0-9._-]+\.schema\.json|"
    r"registries/[A-Za-z0-9._-]+\.json|"
    r"Makefile|"
    r"AGENTS\.md|"
    r"README\.md"
    r")(?![\w./-])"
)
RECOVERY_MARKERS = (
    "Codex recovery output",
    "entering single-file REVISE recovery",
    "accepted after recovery",
)
RECOVERY_SCRIPT_EXECUTION = re.compile(r"\bbash\s+scripts/rkm-recover-revise\.sh\b")
RECOVERY_PATH_PATTERN = re.compile(
    r"(?:^\[[^\]\s]+\s+[0-9a-f]{6,40}\]\s+Recover\b|\bRecover\s+(?:"
    r"docs/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+\.md|"
    r"schema/(?:definitions/)?[A-Za-z0-9._-]+\.schema\.json|"
    r"))"
)
ERROR_MARKER = re.compile(r"\bERROR:")
USAGE_LIMIT_MARKER = re.compile(r"\busage limit\b", re.IGNORECASE)
ARGUMENT_LIST_TOO_LONG_MARKER = re.compile(r"\bArgument list too long\b", re.IGNORECASE)
EXIT_NONZERO_MARKER = re.compile(r"\bexit nonzero\b", re.IGNORECASE)
RECOVERY_FAILED_MARKER = re.compile(
    r"(?:\bERROR:\s+REVISE recovery failed\b|\bCodex recovery failed\.)",
    re.IGNORECASE,
)
MAKE_FATAL_MARKER = re.compile(r"(?:^|\s)make(?:\[\d+\])?: \*\*\* .*", re.IGNORECASE)
TRACEBACK_MARKER = re.compile(r"\bTraceback \(most recent call last\):")
COMPLETION_ACCEPTED_FILE_COUNT = re.compile(
    r"\b(?:Cycle|Autocycle) completed:\s+(?P<count>\d+)\s+accepted file\(s\) committed\.",
    re.IGNORECASE,
)
ITERATION_ACCEPTED = re.compile(
    r"\bIteration\s+\d+\s+of\s+\d+\s+accepted\s+(?:by rkm-cycle\.sh|after recovery)\b",
    re.IGNORECASE,
)
COMMIT_COMPLETED_LINE = re.compile(r"\bCommit completed:\s+.+")


def repository_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_path(value: str | None, default: Path) -> Path:
    if value is None:
        return default
    path = Path(value)
    if path.is_absolute():
        return path
    return (REPOSITORY_ROOT / path).resolve()


def read_log(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_token_events(text: str) -> list[dict[str, int]]:
    events: list[dict[str, int]] = []
    for match in TOKEN_MARKER.finditer(text):
        nearby = text[match.end() : match.end() + 160]
        integer = INTEGER.search(nearby)
        if integer is None:
            continue
        raw_value = integer.group(0).replace(",", "")
        events.append(
            {
                "line": line_number_at(text, match.start()),
                "tokens": int(raw_value),
            }
        )
    return events


def explicit_verdict(line: str) -> str | None:
    normalized = line.strip()

    standalone = STANDALONE_VERDICT.fullmatch(normalized)
    if standalone:
        for group_name in ("code", "plain", "bold_code", "bold"):
            verdict = standalone.group(group_name)
            if verdict:
                return verdict

    labeled = LABELED_VERDICT.fullmatch(normalized)
    if labeled:
        return labeled.group("verdict")

    return None


def extract_verdicts(text: str) -> list[str]:
    verdicts: list[str] = []
    for line in text.splitlines():
        verdict = explicit_verdict(line)
        if verdict is not None:
            verdicts.append(verdict)
    return verdicts


def extract_commits(text: str) -> list[dict[str, str]]:
    commits: list[dict[str, str]] = []
    for line in text.splitlines():
        match = COMMIT_LINE.match(line.strip())
        if match:
            commits.append(
                {
                    "hash": match.group("hash"),
                    "message": match.group("message").strip(),
                }
            )
    return commits


def clean_path(value: str) -> str:
    path = value.strip().strip("`'\"")
    path = path.rstrip(".,;:)")
    if " -> " in path:
        path = path.rsplit(" -> ", 1)[1].strip()
    return path


def repo_paths(value: str) -> list[str]:
    return [clean_path(match.group("path")) for match in REPO_PATH_TOKEN.finditer(value)]


def extract_paths_from_line(line: str) -> list[str]:
    stripped = line.strip()
    paths: list[str] = []

    for pattern in (CREATE_MODE_LINE, STATUS_PATH_LINE):
        match = pattern.match(stripped)
        if match:
            paths.extend(repo_paths(match.group("path")))

    if stripped.startswith(("Commit completed:", "Recover ")):
        paths.extend(repo_paths(stripped))

    return paths


def extract_files(text: str) -> list[str]:
    files: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        for path in extract_paths_from_line(line):
            if path not in seen:
                seen.add(path)
                files.append(path)
    return files


def accepted_file_count(text: str, label: str | None, final_verdict: str | None, files: list[str]) -> int:
    if final_verdict != "ACCEPT":
        return 0

    explicit_counts = [int(match.group("count")) for match in COMPLETION_ACCEPTED_FILE_COUNT.finditer(text)]
    if explicit_counts:
        return explicit_counts[-1]

    iteration_acceptances = ITERATION_ACCEPTED.findall(text)
    if iteration_acceptances:
        return len(iteration_acceptances)

    if label in {"autocycle-cycle", "autocycle-recovery-review"}:
        return 1

    return len(files)


def extract_automation_kinds(text: str, label: str | None) -> list[str]:
    kinds: list[str] = []
    seen: set[str] = set()
    if label:
        seen.add(label)
        kinds.append(label)
    for match in AUTOMATION_PREFIX.finditer(text):
        kind = match.group("label")
        if kind not in seen:
            seen.add(kind)
            kinds.append(kind)
    return kinds


def append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def failure_hint_events(text: str) -> list[dict[str, int | str]]:
    events: list[dict[str, int | str]] = []
    verdicts = extract_verdicts(text)
    final_verdict = verdicts[-1] if verdicts else None
    accept_final = final_verdict == "ACCEPT"

    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.search(r"\bReturn\s+ACCEPT,\s+REVISE,\s+or\s+STOP\b", line, re.IGNORECASE):
            continue
        if not accept_final and ERROR_MARKER.search(line):
            events.append({"hint": "ERROR:", "line": line_number})
        if USAGE_LIMIT_MARKER.search(line):
            events.append({"hint": "usage limit", "line": line_number})
        if ARGUMENT_LIST_TOO_LONG_MARKER.search(line):
            events.append({"hint": "Argument list too long", "line": line_number})
        if EXIT_NONZERO_MARKER.search(line):
            events.append({"hint": "exit nonzero", "line": line_number})
        if RECOVERY_FAILED_MARKER.search(line):
            events.append({"hint": "recovery failed", "line": line_number})
        if MAKE_FATAL_MARKER.search(line):
            events.append({"hint": "make fatal error", "line": line_number})
        if TRACEBACK_MARKER.search(line):
            events.append({"hint": "uncaught traceback", "line": line_number})

    if final_verdict == "STOP":
        events.append({"hint": "STOP", "line": len(text.splitlines()) + 1})
    return events


def failure_hints_from_events(events: list[dict[str, int | str]]) -> list[str]:
    hints: list[str] = []
    for event in events:
        hint = event.get("hint")
        if isinstance(hint, str):
            append_unique(hints, hint)
    return hints


def failure_hints(text: str) -> list[str]:
    return failure_hints_from_events(failure_hint_events(text))


def success_anchor_lines(text: str) -> list[int]:
    lines: list[int] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if COMMIT_LINE.match(stripped):
            lines.append(line_number)
        elif COMMIT_COMPLETED_LINE.search(stripped):
            lines.append(line_number)
        elif COMPLETION_ACCEPTED_FILE_COUNT.search(stripped):
            lines.append(line_number)
        elif ITERATION_ACCEPTED.search(stripped):
            lines.append(line_number)
    return lines


def has_recovery(text: str, label: str | None) -> bool:
    if label and "recovery" in label.lower():
        return True
    return (
        any(marker in text for marker in RECOVERY_MARKERS)
        or bool(RECOVERY_SCRIPT_EXECUTION.search(text))
        or any(RECOVERY_PATH_PATTERN.search(line.strip()) for line in text.splitlines())
    )


def final_status(final_verdict: str | None, has_failure: bool, recovered: bool) -> str:
    if final_verdict == "ACCEPT" and recovered and not has_failure:
        return "RECOVERED"
    if final_verdict == "ACCEPT" and not has_failure:
        return "ACCEPTED"
    if final_verdict == "REVISE":
        return "REVISE_PENDING"
    if final_verdict == "STOP":
        return "STOPPED"
    if has_failure:
        return "FAILED"
    return "UNKNOWN"


def has_unresolved_failure(
    hint_events: list[dict[str, int | str]], final_verdict: str | None, accepted_count: int, anchors: list[int]
) -> bool:
    if not hint_events:
        return False
    severe_hints = {
        "usage limit",
        "Argument list too long",
        "STOP",
        "recovery failed",
        "make fatal error",
    }
    transient_hints = {"recovery failed", "make fatal error"}
    last_anchor = max(anchors) if anchors else None
    accept_with_success = final_verdict == "ACCEPT" and accepted_count > 0 and last_anchor is not None

    for event in hint_events:
        hint = event.get("hint")
        if not isinstance(hint, str):
            continue
        if final_verdict == "ACCEPT" and accepted_count > 0 and hint not in severe_hints:
            continue
        if accept_with_success and hint in transient_hints:
            line = event.get("line")
            if isinstance(line, int) and line < last_anchor:
                continue
        return True
    return False


def entry_final_status(entry: dict[str, Any]) -> str:
    stored = entry.get("finalStatus")
    if isinstance(stored, str) and stored:
        return stored
    final_verdict = entry.get("finalVerdict")
    if not isinstance(final_verdict, str):
        final_verdict = None
    return final_status(final_verdict, bool(entry.get("hasFailure")), bool(entry.get("hasRecovery")))


def build_entry(log_path: Path, text: str, label: str | None) -> dict[str, Any]:
    token_events = extract_token_events(text)
    verdicts = extract_verdicts(text)
    commits = extract_commits(text)
    files = extract_files(text)
    hint_events = failure_hint_events(text)
    hints = failure_hints_from_events(hint_events)
    final_verdict = verdicts[-1] if verdicts else None
    recovered = has_recovery(text, label)
    accepted_count = accepted_file_count(text, label, final_verdict, files)
    has_failure = has_unresolved_failure(hint_events, final_verdict, accepted_count, success_anchor_lines(text))

    return {
        "timestampUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "label": label,
        "logPath": repository_relative(log_path),
        "automationKinds": extract_automation_kinds(text, label),
        "tokenEvents": token_events,
        "totalTokens": sum(event["tokens"] for event in token_events),
        "verdicts": verdicts,
        "finalVerdict": final_verdict,
        "hadRevise": "REVISE" in verdicts,
        "hadStop": "STOP" in verdicts,
        "hadUsageLimit": "usage limit" in hints,
        "hadArgumentListTooLong": "Argument list too long" in hints,
        "hadTraceback": "uncaught traceback" in hints,
        "finalStatus": final_status(final_verdict, has_failure, recovered),
        "commits": commits,
        "files": files,
        "acceptedFileCount": accepted_count,
        "hasRecovery": recovered,
        "hasFailure": has_failure,
        "failureHints": hints,
    }


def append_entry(log_path: Path, ledger_path: Path, label: str | None) -> dict[str, Any]:
    text = read_log(log_path)
    entry = build_entry(log_path, text, label)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")
    return entry


def read_ledger(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                document = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL entry: {exc}") from exc
            if isinstance(document, dict):
                entries.append(document)
    return entries


def report_text(entries: list[dict[str, Any]]) -> str:
    total_runs = len(entries)
    total_token_events = sum(len(entry.get("tokenEvents", [])) for entry in entries)
    total_tokens = sum(int(entry.get("totalTokens", 0) or 0) for entry in entries)
    accepted_files = sum(int(entry.get("acceptedFileCount", 0) or 0) for entry in entries)
    runs_with_recovery = sum(1 for entry in entries if entry.get("hasRecovery"))
    runs_with_failure = sum(1 for entry in entries if entry.get("hasFailure"))
    recovered_runs = sum(1 for entry in entries if entry_final_status(entry) == "RECOVERED")
    revise_pending_runs = sum(1 for entry in entries if entry_final_status(entry) == "REVISE_PENDING")
    stopped_runs = sum(1 for entry in entries if entry_final_status(entry) == "STOPPED")

    lines = [
        "RKM run ledger report",
        f"total runs: {total_runs}",
        f"total token events: {total_token_events}",
        f"total tokens: {total_tokens}",
        f"average tokens per run: {total_tokens / total_runs:.2f}" if total_runs else "average tokens per run: n/a",
        (
            f"average tokens per accepted file: {total_tokens / accepted_files:.2f}"
            if accepted_files
            else "average tokens per accepted file: n/a"
        ),
        f"runs with recovery: {runs_with_recovery}",
        f"runs with failure hints: {runs_with_failure}",
        f"recovered runs: {recovered_runs}",
        f"revise pending runs: {revise_pending_runs}",
        f"stopped runs: {stopped_runs}",
        "most recent entries:",
    ]

    for entry in entries[-10:][::-1]:
        lines.append(
            "- "
            f"label={entry.get('label') or 'n/a'}; "
            f"acceptedFileCount={entry.get('acceptedFileCount', 0)}; "
            f"totalTokens={entry.get('totalTokens', 0)}; "
            f"finalVerdict={entry.get('finalVerdict') or 'n/a'}; "
            f"finalStatus={entry_final_status(entry)}; "
            f"hasRecovery={bool(entry.get('hasRecovery'))}"
        )
    if not entries:
        lines.append("- n/a")

    return "\n".join(lines)


def print_report(ledger_path: Path) -> int:
    if not ledger_path.exists():
        print(f"Ledger is empty: {repository_relative(ledger_path)} does not exist.")
        return 0
    try:
        entries = read_ledger(ledger_path)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(report_text(entries))
    return 0


def positive_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def non_negative_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a non-negative integer") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be a non-negative integer")
    return parsed


def parse_timestamp_utc(value: str) -> datetime:
    normalized = value
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"invalid UTC timestamp: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def entry_timestamp_utc(entry: dict[str, Any]) -> datetime | None:
    timestamp = entry.get("timestampUtc")
    if not isinstance(timestamp, str) or not timestamp:
        return None
    try:
        return parse_timestamp_utc(timestamp)
    except ValueError:
        return None


def estimate_values(
    entries: list[dict[str, Any]], target: int, safety_factor: float, since: str | None
) -> dict[str, float | int]:
    historical_accepted_files = 0
    historical_tokens = 0
    costs_per_file: list[float] = []

    for entry in entries:
        accepted_count = int(entry.get("acceptedFileCount", 0) or 0)
        total_tokens = int(entry.get("totalTokens", 0) or 0)
        if entry_final_status(entry) not in {"ACCEPTED", "RECOVERED"} or accepted_count <= 0:
            continue
        historical_accepted_files += accepted_count
        historical_tokens += total_tokens
        costs_per_file.append(total_tokens / accepted_count)

    if historical_accepted_files == 0:
        return {
            "historicalAcceptedFiles": 0,
            "historicalTokens": 0,
            "averageTokensPerAcceptedFile": 0.0,
            "maxTokensPerAcceptedFile": 0.0,
            "targetAcceptedFiles": target,
            "safetyFactor": safety_factor,
            "estimatedTokens": 0.0,
            "tokensUsedSince": 0,
        }

    tokens_used_since = 0
    if since is not None:
        since_timestamp = parse_timestamp_utc(since)
        for entry in entries:
            entry_timestamp = entry_timestamp_utc(entry)
            if entry_timestamp is not None and entry_timestamp >= since_timestamp:
                tokens_used_since += int(entry.get("totalTokens", 0) or 0)

    average_tokens_per_accepted_file = historical_tokens / historical_accepted_files
    estimated_tokens = average_tokens_per_accepted_file * target * safety_factor

    return {
        "historicalAcceptedFiles": historical_accepted_files,
        "historicalTokens": historical_tokens,
        "averageTokensPerAcceptedFile": average_tokens_per_accepted_file,
        "maxTokensPerAcceptedFile": max(costs_per_file),
        "targetAcceptedFiles": target,
        "safetyFactor": safety_factor,
        "estimatedTokens": estimated_tokens,
        "tokensUsedSince": tokens_used_since,
    }


def estimate_text(values: dict[str, float | int], budget: int | None) -> str:
    lines = [
        "RKM run ledger budget estimate",
        f"historicalAcceptedFiles: {values['historicalAcceptedFiles']}",
        f"historicalTokens: {values['historicalTokens']}",
        f"averageTokensPerAcceptedFile: {values['averageTokensPerAcceptedFile']:.2f}",
        f"maxTokensPerAcceptedFile: {values['maxTokensPerAcceptedFile']:.2f}",
        f"targetAcceptedFiles: {values['targetAcceptedFiles']}",
        f"safetyFactor: {values['safetyFactor']:.2f}",
        f"estimatedTokens: {values['estimatedTokens']:.2f}",
    ]
    if budget is not None:
        remaining_budget = budget - int(values["tokensUsedSince"])
        over_budget = float(values["estimatedTokens"]) > remaining_budget
        lines.extend(
            [
                f"budget: {budget}",
                f"tokensUsedSince: {values['tokensUsedSince']}",
                f"remainingBudget: {remaining_budget}",
                f"overBudget: {str(over_budget).lower()}",
            ]
        )
    return "\n".join(lines)


def print_estimate(
    ledger_path: Path, target: int, budget: int | None, since: str | None, safety_factor: float
) -> int:
    if not ledger_path.exists():
        print(f"Estimation unavailable: no usable historical accepted entries in {repository_relative(ledger_path)}.")
        return 2 if budget is not None else 0
    try:
        entries = read_ledger(ledger_path)
        values = estimate_values(entries, target, safety_factor, since)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if int(values["historicalAcceptedFiles"]) == 0:
        print(f"Estimation unavailable: no usable historical accepted entries in {repository_relative(ledger_path)}.")
        return 2 if budget is not None else 0

    print(estimate_text(values, budget))
    if budget is None:
        return 0

    remaining_budget = budget - int(values["tokensUsedSince"])
    return 3 if float(values["estimatedTokens"]) > remaining_budget else 0


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def quiet_call(function: Any, *args: Any) -> int:
    with contextlib.redirect_stdout(io.StringIO()):
        return int(function(*args))


def run_self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="rkm-run-ledger-") as temporary:
        root = Path(temporary)
        ledger = root / ".rkm" / "run-ledger.jsonl"
        first_log = root / "first.log"
        second_log = root / "second.log"

        first_log.write_text(
            "\n".join(
                [
                    "[rkm-cycle] start",
                    "Return ACCEPT, REVISE, or STOP",
                    "A prose sentence about docs architecture naming is not a repository path.",
                    "Checking scripts/rkm-recover-revise.sh",
                    "tokens used",
                    "  1,234 total",
                    "verdict: `ACCEPT`",
                    "[main abc1234] Add docs architecture example",
                    "A docs/architecture/example-model.md",
                    "create mode 100644 docs/architecture/example-model.md",
                    "Commit completed: Add docs/architecture/example-model.md.",
                ]
            ),
            encoding="utf-8",
        )
        first_entry = append_entry(first_log, ledger, None)

        assert_equal([event["tokens"] for event in first_entry["tokenEvents"]], [1234], "token extraction")
        assert_equal(first_entry["verdicts"], ["ACCEPT"], "verdict extraction")
        assert_equal(first_entry["commits"], [{"hash": "abc1234", "message": "Add docs architecture example"}], "commit extraction")
        assert_equal(first_entry["files"], ["docs/architecture/example-model.md"], "file extraction")
        assert_equal(first_entry["acceptedFileCount"], 1, "accepted file count")
        assert_equal(first_entry["hasRecovery"], False, "plain accept recovery detection")
        assert_equal(first_entry["hasFailure"], False, "plain accept failure detection")
        assert_equal(first_entry["hadRevise"], False, "plain accept revise detection")
        assert_equal(first_entry["finalStatus"], "ACCEPTED", "plain accept final status")
        assert_equal(first_entry["automationKinds"], ["rkm-cycle"], "automation prefix extraction")

        second_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] start",
                    "tokens used: 200",
                    "validation failed before the requested fix was accepted",
                    "tokens used",
                    "  300",
                    "entering single-file REVISE recovery",
                    "Recover docs/architecture/recovered-model.md",
                    "verdict: REVISE",
                    "accepted after recovery",
                    "verdict: ACCEPT",
                    "[main def5678] Recover docs architecture model",
                    "Commit completed: Add docs/architecture/recovered-model.md.",
                ]
            ),
            encoding="utf-8",
        )
        second_entry = append_entry(second_log, ledger, "manual-label")

        assert_equal([event["tokens"] for event in second_entry["tokenEvents"]], [200, 300], "multiple token blocks")
        assert_equal(second_entry["verdicts"], ["REVISE", "ACCEPT"], "transient revise verdict extraction")
        assert_equal(second_entry["finalVerdict"], "ACCEPT", "recovered final verdict")
        assert_equal(second_entry["hadRevise"], True, "transient revise detection")
        assert_equal(second_entry["hadStop"], False, "stop detection")
        assert_equal(second_entry["hasRecovery"], True, "recovery detection")
        assert_equal(second_entry["hasFailure"], False, "transient revise failure detection")
        assert_equal(second_entry["finalStatus"], "RECOVERED", "recovered final status")
        assert_equal(second_entry["commits"][0]["hash"], "def5678", "recovered commit extraction")
        assert_equal(second_entry["files"], ["docs/architecture/recovered-model.md"], "recovered file extraction")
        assert_equal(second_entry["automationKinds"], ["manual-label", "rkm-autocycle"], "label and prefix extraction")

        third_log = root / "third.log"
        third_log.write_text(
            "\n".join(
                [
                    "[rkm-cycle] start",
                    "Argument list too long",
                    "Traceback (most recent call last):",
                    "verdict: STOP",
                ]
            ),
            encoding="utf-8",
        )
        third_entry = append_entry(third_log, ledger, None)
        assert_equal(third_entry["hadArgumentListTooLong"], True, "argument list too long detection")
        assert_equal(third_entry["hadTraceback"], True, "stop traceback detection")
        assert_equal(third_entry["hasFailure"], True, "argument list too long failure detection")
        assert_equal(third_entry["finalStatus"], "STOPPED", "stop final status")

        fourth_log = root / "fourth.log"
        fourth_log.write_text(
            "\n".join(
                [
                    "[rkm-cycle] start",
                    "ERROR: validation failed before Codex fixed the file",
                    "verdict: ACCEPT",
                    "Cycle completed: 1 accepted file(s) committed.",
                ]
            ),
            encoding="utf-8",
        )
        fourth_entry = append_entry(fourth_log, ledger, None)
        assert_equal(fourth_entry["hasFailure"], False, "accepted generic error failure detection")
        assert_equal(fourth_entry["finalStatus"], "ACCEPTED", "accepted generic error final status")
        assert_equal(fourth_entry["acceptedFileCount"], 1, "cycle completion accepted file count")

        fifth_log = root / "fifth.log"
        fifth_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] start",
                    (
                        "Commit completed: Add docs/architecture/autocycle-model.md "
                        "with schema/definitions/identity.schema.json support."
                    ),
                    "Autocycle completed: 1 accepted file(s) committed.",
                    "verdict: ACCEPT",
                ]
            ),
            encoding="utf-8",
        )
        fifth_entry = append_entry(fifth_log, ledger, "autocycle-cycle")
        assert_equal(
            fifth_entry["files"],
            ["docs/architecture/autocycle-model.md", "schema/definitions/identity.schema.json"],
            "autocycle referenced file extraction",
        )
        assert_equal(fifth_entry["acceptedFileCount"], 1, "autocycle explicit accepted file count")

        sixth_log = root / "sixth.log"
        sixth_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] start",
                    "ERROR: usage limit reached",
                    "verdict: ACCEPT",
                    "Autocycle completed: 1 accepted file(s) committed.",
                ]
            ),
            encoding="utf-8",
        )
        sixth_entry = append_entry(sixth_log, ledger, None)
        assert_equal(sixth_entry["hadUsageLimit"], True, "usage limit detection")
        assert_equal(sixth_entry["hasFailure"], True, "usage limit failure detection")
        assert_equal(sixth_entry["finalStatus"], "FAILED", "usage limit final status")

        seventh_log = root / "seventh.log"
        seventh_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] start",
                    "Traceback (most recent call last):",
                    "historical traceback captured in reviewer output",
                    "verdict: ACCEPT",
                    "Autocycle completed: 1 accepted file(s) committed.",
                ]
            ),
            encoding="utf-8",
        )
        seventh_entry = append_entry(seventh_log, ledger, None)
        assert_equal(seventh_entry["hadTraceback"], True, "accepted traceback detection")
        assert_equal(seventh_entry["hasFailure"], False, "accepted traceback failure detection")
        assert_equal(seventh_entry["finalStatus"], "ACCEPTED", "accepted traceback final status")
        assert_equal(seventh_entry["acceptedFileCount"], 1, "accepted traceback file count")

        eighth_log = root / "eighth.log"
        eighth_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] start",
                    "Argument list too long",
                    "verdict: ACCEPT",
                    "Autocycle completed: 1 accepted file(s) committed.",
                ]
            ),
            encoding="utf-8",
        )
        eighth_entry = append_entry(eighth_log, ledger, None)
        assert_equal(eighth_entry["hadArgumentListTooLong"], True, "accepted argument list too long detection")
        assert_equal(eighth_entry["hasFailure"], True, "accepted argument list too long failure detection")
        assert_equal(eighth_entry["finalStatus"], "FAILED", "accepted argument list too long final status")

        ninth_log = root / "ninth.log"
        ninth_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] start",
                    "Recovery state validator that blocks autopilot when recovery failed.",
                    "Traceback (most recent call last):",
                    "FileNotFoundError: [Errno 2] No such file or directory: '/tmp/rkm-missing'",
                    "make[2]: *** [Makefile:25: validate] Error 1",
                    "verdict: ACCEPT",
                    "[main 123abcd] Add accepted RKM file",
                    "Commit completed: Add docs/architecture/accepted-model.md.",
                    "Cycle completed: 1 accepted file(s) committed.",
                ]
            ),
            encoding="utf-8",
        )
        ninth_entry = append_entry(ninth_log, ledger, None)
        assert_equal("recovery failed" in ninth_entry["failureHints"], False, "prose recovery failed hint suppression")
        assert_equal(ninth_entry["hadTraceback"], True, "accepted cycle traceback remains diagnostic")
        assert_equal("make fatal error" in ninth_entry["failureHints"], True, "resolved make fatal hint remains diagnostic")
        assert_equal(ninth_entry["hasFailure"], False, "accepted cycle resolved make fatal failure detection")
        assert_equal(ninth_entry["finalStatus"], "ACCEPTED", "accepted cycle resolved make fatal final status")
        assert_equal(ninth_entry["acceptedFileCount"], 1, "accepted cycle resolved make fatal file count")

        tenth_log = root / "tenth.log"
        tenth_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] start",
                    "verdict: ACCEPT",
                    "Autocycle completed: 1 accepted file(s) committed.",
                    "make: *** [Makefile:25: validate] Error 1",
                ]
            ),
            encoding="utf-8",
        )
        tenth_entry = append_entry(tenth_log, ledger, None)
        assert_equal("make fatal error" in tenth_entry["failureHints"], True, "post-success make fatal hint detection")
        assert_equal(tenth_entry["hasFailure"], True, "post-success make fatal failure detection")
        assert_equal(tenth_entry["finalStatus"], "FAILED", "post-success make fatal final status")
        assert_equal(tenth_entry["acceptedFileCount"], 1, "post-success make fatal accepted file count")

        entries = read_ledger(ledger)
        assert_equal(len(entries), 10, "append behavior")
        report = report_text(entries)
        for expected in (
            "total runs: 10",
            "total token events: 3",
            "total tokens: 1734",
            "runs with recovery: 1",
            "runs with failure hints: 4",
            "recovered runs: 1",
            "stopped runs: 1",
        ):
            if expected not in report:
                raise AssertionError(f"report behavior: missing {expected!r}")

        estimate = estimate_values(entries, 3, 1.25, None)
        assert_equal(estimate["historicalAcceptedFiles"], 6, "estimate historical accepted files")
        assert_equal(estimate["historicalTokens"], 1734, "estimate historical tokens")
        assert_equal(
            f"{estimate['averageTokensPerAcceptedFile']:.2f}",
            "289.00",
            "estimate average tokens per accepted file",
        )
        assert_equal(f"{estimate['maxTokensPerAcceptedFile']:.2f}", "1234.00", "estimate max tokens per accepted file")
        assert_equal(estimate["targetAcceptedFiles"], 3, "estimate target accepted files")
        assert_equal(estimate["safetyFactor"], 1.25, "estimate safety factor")
        assert_equal(f"{estimate['estimatedTokens']:.2f}", "1083.75", "estimate tokens")

        assert_equal(quiet_call(print_estimate, ledger, 3, 2000, None, 1.25), 0, "estimate budget within")
        assert_equal(quiet_call(print_estimate, ledger, 3, 1000, None, 1.25), 3, "estimate budget over")

        since_ledger = root / ".rkm" / "since-ledger.jsonl"
        since_entries = [
            {
                "timestampUtc": "2026-01-01T00:00:00Z",
                "finalStatus": "ACCEPTED",
                "totalTokens": 100,
                "acceptedFileCount": 1,
            },
            {
                "timestampUtc": "2026-01-02T00:00:00Z",
                "finalStatus": "ACCEPTED",
                "totalTokens": 200,
                "acceptedFileCount": 1,
            },
        ]
        since_ledger.parent.mkdir(parents=True, exist_ok=True)
        since_ledger.write_text(
            "".join(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n" for entry in since_entries),
            encoding="utf-8",
        )
        assert_equal(
            quiet_call(print_estimate, since_ledger, 1, 500, "2026-01-02T00:00:00Z", 1.0),
            0,
            "estimate since within budget",
        )
        since_estimate = estimate_values(read_ledger(since_ledger), 1, 1.0, "2026-01-02T00:00:00Z")
        assert_equal(since_estimate["tokensUsedSince"], 200, "estimate since tokens used")

        empty_ledger = root / ".rkm" / "empty-ledger.jsonl"
        empty_ledger.write_text(
            json.dumps(
                {"timestampUtc": "2026-01-01T00:00:00Z", "finalStatus": "STOPPED", "totalTokens": 900, "acceptedFileCount": 0},
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
        )
        assert_equal(quiet_call(print_estimate, empty_ledger, 1, None, None, 1.25), 0, "estimate no history without budget")
        assert_equal(quiet_call(print_estimate, empty_ledger, 1, 1000, None, 1.25), 2, "estimate no history with budget")

    print("Self-test passed: parser precision, status, append, recovery, and report behavior verified.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run internal tests without persistent files")
    subparsers = parser.add_subparsers(dest="command")

    append_parser = subparsers.add_parser("append", help="append one ledger entry from a log")
    append_parser.add_argument("--log", required=True, help="path to the automation log")
    append_parser.add_argument("--ledger", help="path to the JSONL ledger")
    append_parser.add_argument("--label", help="optional run label")

    report_parser = subparsers.add_parser("report", help="print a concise ledger report")
    report_parser.add_argument("--ledger", help="path to the JSONL ledger")

    estimate_parser = subparsers.add_parser("estimate", help="estimate token cost for accepted files")
    estimate_parser.add_argument("--target", required=True, type=positive_integer, help="target accepted file count")
    estimate_parser.add_argument("--budget", type=non_negative_integer, help="available token budget")
    estimate_parser.add_argument("--ledger", help="path to the JSONL ledger")
    estimate_parser.add_argument("--since", help="UTC timestamp for budget usage accounting")
    estimate_parser.add_argument("--safety-factor", type=float, default=1.25, help="multiplier applied to the estimate")

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])

    if args.self_test:
        return run_self_test()

    if args.command == "append":
        log_path = resolve_path(args.log, REPOSITORY_ROOT)
        ledger_path = resolve_path(args.ledger, DEFAULT_LEDGER_PATH)
        if not log_path.exists() or not log_path.is_file():
            print(f"ERROR: log file does not exist: {log_path}", file=sys.stderr)
            return 2
        entry = append_entry(log_path, ledger_path, args.label)
        print(json.dumps(entry, indent=2, sort_keys=True))
        return 0

    if args.command == "report":
        return print_report(resolve_path(args.ledger, DEFAULT_LEDGER_PATH))

    if args.command == "estimate":
        if args.safety_factor <= 0:
            print("ERROR: --safety-factor must be positive", file=sys.stderr)
            return 2
        return print_estimate(
            resolve_path(args.ledger, DEFAULT_LEDGER_PATH),
            args.target,
            args.budget,
            args.since,
            args.safety_factor,
        )

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
