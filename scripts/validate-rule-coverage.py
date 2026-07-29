#!/usr/bin/env python3
"""Validate consistency between the governance coverage report and repository checks."""

from __future__ import annotations

import argparse
import re
import tempfile
from pathlib import Path


ROW_PATTERN = re.compile(r"^\|(?P<rule>[^|]+)\|(?P<location>[^|]+)\|(?P<level>[^|]+)\|(?P<check>[^|]+)\|(?P<notes>[^|]+)\|")
REQUIRED_LEVELS = {"Validated", "Partially Validated"}


def backtick_values(value: str) -> list[str]:
    return re.findall(r"`([^`]+)`", value)


def make_targets(makefile: Path) -> set[str]:
    return {
        match.group(1)
        for match in re.finditer(r"^(?P<target>[A-Za-z0-9_-]+):", makefile.read_text(encoding="utf-8"), re.MULTILINE)
    }


def validate(root: Path) -> list[str]:
    report_path = root / "docs/maintenance/rule-coverage-report.md"
    makefile = root / "Makefile"
    errors: list[str] = []
    targets = make_targets(makefile)
    for line_number, line in enumerate(report_path.read_text(encoding="utf-8").splitlines(), 1):
        match = ROW_PATTERN.match(line)
        if not match:
            continue
        level = match.group("level").strip()
        if level not in REQUIRED_LEVELS:
            continue
        check = match.group("check").strip()
        if check == "None":
            errors.append(f"{report_path}:{line_number}: {level} rule has no automated check")
            continue
        for reference in backtick_values(check):
            if reference.startswith("scripts/"):
                script = reference.split()[0]
                if not (root / script).is_file():
                    errors.append(f"{report_path}:{line_number}: missing check script {script}")
            if reference.startswith("make "):
                target = reference.removeprefix("make ").split()[0]
                if target not in targets:
                    errors.append(f"{report_path}:{line_number}: missing Make target {target}")
    return errors


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-rule-coverage-") as directory:
        root = Path(directory)
        (root / "docs/maintenance").mkdir(parents=True)
        (root / "scripts").mkdir()
        (root / "scripts/check.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "Makefile").write_text("check: \n\ttrue\n", encoding="utf-8")
        report = """| Rule | Location | Coverage Level | Automated Check | Notes |
| good | `AGENTS.md` | Validated | `scripts/check.py`; `make check` | ok |
| bad | `AGENTS.md` | Validated | `scripts/missing.py`; `make missing` | bad |
"""
        (root / "docs/maintenance/rule-coverage-report.md").write_text(report, encoding="utf-8")
        errors = validate(root)
        assert len(errors) == 2, errors
    print("rule coverage validator self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("Rule coverage consistency errors:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("rule coverage validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
