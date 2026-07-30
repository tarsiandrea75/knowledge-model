#!/usr/bin/env python3
"""Validate the RKM policy-as-data registry and its executable references."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries/governance-policy-registry.json"
SCHEMA = ROOT / "schema/governance-policy-registry-v1.schema.json"
MAKEFILE = ROOT / "Makefile"


class PolicyRegistryError(ValueError):
    """Raised when a policy registry is invalid or stale."""


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyRegistryError(f"unable to read JSON file: {path}") from exc
    if not isinstance(value, dict):
        raise PolicyRegistryError(f"JSON root must be an object: {path}")
    return value


def _make_targets(path: Path) -> set[str]:
    return set(re.findall(r"^([A-Za-z0-9_-]+):", path.read_text(encoding="utf-8"), re.MULTILINE))


def _validate_schema(registry: dict[str, Any]) -> None:
    schema = _load(SCHEMA)
    errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda error: list(error.path))
    if errors:
        location = "/".join(str(part) for part in errors[0].path) or "root"
        raise PolicyRegistryError(f"policy registry schema validation failed at {location}: {errors[0].message}")


def _resolve_repo_path(value: str, label: str) -> Path:
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise PolicyRegistryError(f"{label} escapes the repository: {value}") from exc
    if not candidate.is_file():
        raise PolicyRegistryError(f"{label} does not exist: {value}")
    return candidate


def _validate_command(command: str, targets: set[str]) -> None:
    parts = command.split()
    if not parts:
        raise PolicyRegistryError("empty policy command")
    if parts[0] == "make":
        if len(parts) < 2 or parts[1] not in targets:
            raise PolicyRegistryError(f"policy command references missing Make target: {command}")
        return
    if parts[0] in {"python3", "bash"} and len(parts) >= 2:
        _resolve_repo_path(parts[1], f"policy command script in {command}")
        return
    raise PolicyRegistryError(f"unsupported policy command: {command}")


def validate(registry_path: Path = REGISTRY) -> dict[str, Any]:
    registry = _load(registry_path)
    _validate_schema(registry)
    targets = _make_targets(MAKEFILE)
    rule_ids: set[str] = set()
    for policy in registry["policies"]:
        rule_id = policy["ruleId"]
        if rule_id in rule_ids:
            raise PolicyRegistryError(f"duplicate stable rule id: {rule_id}")
        rule_ids.add(rule_id)
        for source_file in policy["sourceFiles"]:
            _resolve_repo_path(source_file, f"source file for {rule_id}")
        for validator in policy["validators"]:
            _resolve_repo_path(validator, f"validator for {rule_id}")
        for command in policy["commands"]:
            _validate_command(command, targets)
        if policy["enforcementLevel"] == "Validated" and not policy["validators"]:
            raise PolicyRegistryError(f"validated policy has no validator: {rule_id}")
    return {
        "status": "verified",
        "registryId": registry["registryId"],
        "registryVersion": registry["registryVersion"],
        "policyCount": len(registry["policies"]),
        "validatedPolicyCount": sum(policy["enforcementLevel"] == "Validated" for policy in registry["policies"]),
    }


def _self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-policy-registry-") as directory:
        root = Path(directory)
        (root / "docs").mkdir()
        (root / "scripts").mkdir()
        (root / "docs/source.md").write_text("source\n", encoding="utf-8")
        (root / "scripts/check.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "Makefile").write_text("check: \n\ttrue\n", encoding="utf-8")
        registry = {
            "contractVersion": "rkm-governance-policy-registry-v1",
            "registryId": "rkm-core-governance-policies",
            "registryVersion": "1.0.0",
            "status": "Published",
            "policies": [{
                "ruleId": "RKM-GOV-999",
                "title": "A temporary policy for validator testing",
                "area": "Validation",
                "priority": "Low",
                "enforcementLevel": "Validated",
                "status": "Implemented",
                "sourceFiles": ["docs/source.md"],
                "validators": ["scripts/check.py"],
                "commands": ["make check"],
                "reviewOwner": "Test Owner"
            }]
        }
        registry_path = root / "registry.json"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        original_root = globals()["ROOT"]
        original_schema = globals()["SCHEMA"]
        original_makefile = globals()["MAKEFILE"]
        globals()["ROOT"] = root
        globals()["SCHEMA"] = original_root / "schema/governance-policy-registry-v1.schema.json"
        globals()["MAKEFILE"] = root / "Makefile"
        try:
            result = validate(registry_path)
            assert result["policyCount"] == 1
            invalid = dict(registry)
            invalid["policies"] = [dict(registry["policies"][0], commands=["make missing"])]
            invalid_path = root / "invalid.json"
            invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
            try:
                validate(invalid_path)
            except PolicyRegistryError:
                pass
            else:
                raise AssertionError("missing Make target must be rejected")
        finally:
            globals()["ROOT"] = original_root
            globals()["SCHEMA"] = original_schema
            globals()["MAKEFILE"] = original_makefile
    print("governance policy registry validator self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            _self_test()
            return 0
        print(json.dumps(validate(), indent=2, sort_keys=True))
        return 0
    except PolicyRegistryError as exc:
        print(f"governance policy registry rejected: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
