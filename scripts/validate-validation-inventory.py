#!/usr/bin/env python3
"""Detect removal of critical validator scripts or pipeline hooks."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNIT_TESTS = ROOT / "scripts" / "rkm-unit-tests.sh"
VALIDATE = ROOT / "scripts" / "validate-rkm.sh"

CRITICAL_VALIDATORS = (
    ("scripts/validate-data.py", "scripts/validate-data.py --self-test", "scripts/validate-data.py"),
    ("scripts/validate-schema-contracts.py", "scripts/validate-schema-contracts.py --self-test", "scripts/validate-schema-contracts.py"),
    ("scripts/validate-graph-exports.py", "scripts/validate-graph-exports.py --self-test", "scripts/validate-graph-exports.py"),
    ("scripts/validate-rule-coverage.py", "scripts/validate-rule-coverage.py --self-test", "scripts/validate-rule-coverage.py"),
)


class InventoryError(Exception):
    """Raised when a critical validation hook is missing."""


def validate_inventory() -> None:
    unit_text = UNIT_TESTS.read_text(encoding="utf-8")
    validate_text = VALIDATE.read_text(encoding="utf-8")
    for script, self_test_marker, pipeline_marker in CRITICAL_VALIDATORS:
        script_path = ROOT / script
        if not script_path.is_file():
            raise InventoryError(f"critical validator is missing: {script}")
        if self_test_marker not in unit_text:
            raise InventoryError(f"critical validator self-test is not wired: {self_test_marker}")
        if pipeline_marker not in validate_text:
            raise InventoryError(f"critical validator is not wired into the main pipeline: {pipeline_marker}")


def run_self_test() -> None:
    validate_inventory()
    if any(not item[0].endswith(".py") for item in CRITICAL_VALIDATORS):
        raise InventoryError("self-test failed: inventory contains a non-Python validator")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run the inventory self-test")
    args = parser.parse_args()
    try:
        run_self_test() if args.self_test else validate_inventory()
    except InventoryError as exc:
        print(f"ERROR: {exc}")
        return 1
    print("validation inventory passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
