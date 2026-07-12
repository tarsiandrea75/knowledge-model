#!/usr/bin/env python3
"""Extract the final explicit RKM reviewer verdict from a text file."""

from __future__ import annotations

import re
import sys
from pathlib import Path


VERDICTS = ("ACCEPT", "REVISE", "STOP")

STANDALONE_VERDICT = re.compile(
    r"^(?:`(?P<code>ACCEPT|REVISE|STOP)`|(?P<plain>ACCEPT|REVISE|STOP)|\*\*`(?P<bold_code>ACCEPT|REVISE|STOP)`\*\*|\*\*(?P<bold>ACCEPT|REVISE|STOP)\*\*)$"
)
LABELED_VERDICT = re.compile(
    r"^(?:verdict:|Verdict:|\*\*Verdict:\*\*)\s*(?:`(?P<code>ACCEPT|REVISE|STOP)`|\*\*(?P<bold>ACCEPT|REVISE|STOP)\*\*|(?P<plain>ACCEPT|REVISE|STOP))$"
)


def explicit_verdict(line: str) -> str | None:
    normalized = line.strip()

    outer_bold = normalized.startswith("**") and normalized.endswith("**")
    if outer_bold:
        normalized = normalized[2:-2].strip()

    standalone = STANDALONE_VERDICT.fullmatch(normalized)
    if standalone:
        for group_name in ("code", "plain", "bold_code", "bold"):
            verdict = standalone.group(group_name)
            if verdict:
                return verdict

    labeled = LABELED_VERDICT.fullmatch(normalized)
    if labeled:
        for group_name in ("code", "bold", "plain"):
            verdict = labeled.group(group_name)
            if verdict:
                return verdict

    return None


def verdict_from_text(text: str) -> str | None:
    verdict = None
    for line in text.splitlines():
        line_verdict = explicit_verdict(line)
        if line_verdict is not None:
            verdict = line_verdict
    return verdict


def run_self_test() -> int:
    passing_cases = {
        "ACCEPT": "ACCEPT",
        "`REVISE`": "REVISE",
        "**STOP**": "STOP",
        "**`ACCEPT`**": "ACCEPT",
        "verdict: REVISE": "REVISE",
        "Verdict: `STOP`": "STOP",
        "**Verdict: ACCEPT**": "ACCEPT",
        "**Verdict:** ACCEPT": "ACCEPT",
        "**Verdict:** `STOP`": "STOP",
        "Verdict: **REVISE**": "REVISE",
        "Verdict: ACCEPT\nnotes\nverdict: STOP": "STOP",
        "Return ACCEPT, REVISE, or STOP\n\n**Verdict:** `REVISE`": "REVISE",
    }
    failing_cases = (
        "",
        "Return ACCEPT, REVISE, or STOP",
        "The verdict should be ACCEPT.",
        "Verdict may be ACCEPT",
        "- Verdict: ACCEPT",
        "verdict: accept",
        "Verdict: ACCEPT because validation passed",
    )

    failures = []
    for text, expected in passing_cases.items():
        actual = verdict_from_text(text)
        if actual != expected:
            failures.append(f"expected {expected!r}, got {actual!r} for {text!r}")

    for text in failing_cases:
        actual = verdict_from_text(text)
        if actual is not None:
            failures.append(f"expected no verdict, got {actual!r} for {text!r}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("Self-test passed.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return run_self_test()

    if len(argv) != 2:
        print(
            "ERROR: missing path. Usage: python3 scripts/rkm-review-verdict.py PATH",
            file=sys.stderr,
        )
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file does not exist: {path}", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"ERROR: path is not a file: {path}", file=sys.stderr)
        return 2

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: could not read file: {path}: {exc}", file=sys.stderr)
        return 2

    verdict = verdict_from_text(text)
    if verdict is None:
        print(f"ERROR: no explicit reviewer verdict found in {path}", file=sys.stderr)
        return 1

    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
