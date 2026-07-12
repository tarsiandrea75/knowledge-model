#!/usr/bin/env python3
"""Append and report local JSONL ledger entries for RKM automation runs."""

from __future__ import annotations

import argparse
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
PATH_FRAGMENT = re.compile(
    r"(?P<path>(?:docs|schema|scripts|data|examples|tests|\.rkm)/[A-Za-z0-9._/@+-][A-Za-z0-9._/@+\- ]*)"
)
RECOVERY_MARKERS = (
    "recovery",
    "rkm-recover-revise",
    "Recover docs/",
    "Recover schema/",
    "Recover scripts/",
)
FAILURE_MARKERS = (
    "ERROR:",
    "REVISE",
    "STOP",
    "usage limit",
    "Argument list too long",
    "failed",
)


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


def extract_paths_from_line(line: str) -> list[str]:
    stripped = line.strip()
    paths: list[str] = []

    for pattern in (CREATE_MODE_LINE, STATUS_PATH_LINE):
        match = pattern.match(stripped)
        if match:
            paths.append(clean_path(match.group("path")))

    if stripped.startswith(("Commit completed:", "Recover ")):
        for match in PATH_FRAGMENT.finditer(stripped):
            paths.append(clean_path(match.group("path")))

    return [path for path in paths if "/" in path]


def extract_files(text: str) -> list[str]:
    files: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        for path in extract_paths_from_line(line):
            if path not in seen:
                seen.add(path)
                files.append(path)
    return files


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


def failure_hints(text: str) -> list[str]:
    hints: list[str] = []
    for line in text.splitlines():
        if re.search(r"\bReturn\s+ACCEPT,\s+REVISE,\s+or\s+STOP\b", line, re.IGNORECASE):
            continue
        lower_line = line.lower()
        for marker in FAILURE_MARKERS:
            found = marker in line if marker not in ("usage limit", "failed") else marker in lower_line
            if found and marker not in hints:
                hints.append(marker)
    return hints


def has_recovery(text: str) -> bool:
    lower_text = text.lower()
    return any(
        marker in text if marker.startswith("Recover ") else marker.lower() in lower_text
        for marker in RECOVERY_MARKERS
    )


def build_entry(log_path: Path, text: str, label: str | None) -> dict[str, Any]:
    token_events = extract_token_events(text)
    verdicts = extract_verdicts(text)
    commits = extract_commits(text)
    files = extract_files(text)
    hints = failure_hints(text)
    final_verdict = verdicts[-1] if verdicts else None

    return {
        "timestampUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "label": label,
        "logPath": repository_relative(log_path),
        "automationKinds": extract_automation_kinds(text, label),
        "tokenEvents": token_events,
        "totalTokens": sum(event["tokens"] for event in token_events),
        "verdicts": verdicts,
        "finalVerdict": final_verdict,
        "commits": commits,
        "files": files,
        "acceptedFileCount": len(files) if final_verdict == "ACCEPT" else 0,
        "hasRecovery": has_recovery(text),
        "hasFailure": bool(hints),
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
        "most recent entries:",
    ]

    for entry in entries[-10:][::-1]:
        lines.append(
            "- "
            f"label={entry.get('label') or 'n/a'}; "
            f"acceptedFileCount={entry.get('acceptedFileCount', 0)}; "
            f"totalTokens={entry.get('totalTokens', 0)}; "
            f"finalVerdict={entry.get('finalVerdict') or 'n/a'}; "
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


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


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
        assert_equal(first_entry["automationKinds"], ["rkm-cycle"], "automation prefix extraction")

        second_log.write_text(
            "\n".join(
                [
                    "[rkm-autocycle] recovery pass",
                    "tokens used: 200",
                    "usage limit reached",
                    "tokens used",
                    "  300",
                    "rkm-recover-revise finished",
                    "Recover docs/architecture/recovered-model.md",
                    "verdict: REVISE",
                    "STOP",
                    "[main def5678] Recover docs architecture model",
                    "Commit completed: Add docs/architecture/recovered-model.md.",
                ]
            ),
            encoding="utf-8",
        )
        second_entry = append_entry(second_log, ledger, "manual-label")

        assert_equal([event["tokens"] for event in second_entry["tokenEvents"]], [200, 300], "multiple token blocks")
        assert_equal(second_entry["verdicts"], ["REVISE", "STOP"], "final verdict extraction")
        assert_equal(second_entry["finalVerdict"], "STOP", "final verdict")
        assert_equal(second_entry["hasRecovery"], True, "recovery detection")
        assert_equal(second_entry["hasFailure"], True, "failure detection")
        assert_equal(second_entry["commits"][0]["hash"], "def5678", "recovered commit extraction")
        assert_equal(second_entry["files"], ["docs/architecture/recovered-model.md"], "recovered file extraction")
        assert_equal(second_entry["automationKinds"], ["manual-label", "rkm-autocycle"], "label and prefix extraction")

        entries = read_ledger(ledger)
        assert_equal(len(entries), 2, "append behavior")
        report = report_text(entries)
        for expected in (
            "total runs: 2",
            "total token events: 3",
            "total tokens: 1734",
            "runs with recovery: 1",
            "runs with failure hints: 1",
        ):
            if expected not in report:
                raise AssertionError(f"report behavior: missing {expected!r}")

    print("Self-test passed: token, verdict, commit, file, append, recovery, and report behavior verified.")
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

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
