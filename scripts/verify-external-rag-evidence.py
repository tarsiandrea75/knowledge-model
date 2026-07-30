#!/usr/bin/env python3
"""Verify the integrity and non-promoting boundary of an external RAG bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "examples/fixtures/rkm-external-rag-evidence-bundle-v1.json"
SCHEMA = ROOT / "schema/rkm-external-rag-evidence-bundle-v1.schema.json"


class VerificationError(ValueError):
    """Raised when an evidence bundle cannot be verified safely."""


def _load(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise VerificationError(f"unable to read JSON file: {path}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"JSON root must be an object: {path}")
    return value


def _safe_path(root: Path, relative: Any, label: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise VerificationError(f"{label} must be a relative path")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise VerificationError(f"{label} escapes its authorized root: {relative}") from exc
    return candidate


def _sha256(path: Path, label: str) -> str:
    if not path.is_file():
        raise VerificationError(f"{label} does not exist as a regular file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _expect_hash(root: Path, reference: dict[str, Any], label: str) -> None:
    path = _safe_path(root, reference.get("path"), f"{label} path")
    actual = _sha256(path, label)
    expected = reference.get("sha256")
    if actual != expected:
        raise VerificationError(f"{label} hash mismatch: expected {expected}, got {actual}")


def _commit_is_reachable(rag_root: Path, commit: str) -> None:
    try:
        commit_exists = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=rag_root,
            capture_output=True,
            check=False,
            text=True,
        ).returncode == 0
        reachable = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            cwd=rag_root,
            capture_output=True,
            check=False,
        ).returncode == 0
    except OSError as exc:
        raise VerificationError(f"unable to inspect RAG repository Git history: {rag_root}") from exc
    if not commit_exists:
        raise VerificationError(f"declared RAG source commit is absent: {commit}")
    if not reachable:
        raise VerificationError(f"declared RAG source commit is not reachable from RAG HEAD: {commit}")


def _check_source_readiness(sources: list[dict[str, Any]], as_of: date, max_age_days: int) -> dict[str, Any]:
    if max_age_days < 0:
        raise VerificationError("max source age must not be negative")
    ages: list[int] = []
    human_review_required: list[str] = []
    for source in sources:
        source_id = source.get("id", "<unknown>")
        parsed_url = urlparse(source.get("canonicalUrl", ""))
        if parsed_url.scheme != "https" or not parsed_url.netloc:
            raise VerificationError(f"source {source_id} must use a canonical HTTPS URL")
        if not source.get("rights") or not source.get("attribution"):
            raise VerificationError(f"source {source_id} is missing rights or attribution metadata")
        try:
            retrieval_date = date.fromisoformat(source["retrievalDate"])
        except (KeyError, TypeError, ValueError) as exc:
            raise VerificationError(f"source {source_id} has an invalid retrieval date") from exc
        age_days = (as_of - retrieval_date).days
        if age_days < 0:
            raise VerificationError(f"source {source_id} is dated in the future: {retrieval_date}")
        if age_days > max_age_days:
            raise VerificationError(
                f"source {source_id} is stale: {retrieval_date} is {age_days} days before {as_of}"
            )
        ages.append(age_days)
        human_review_required.append(f"{source_id}: verify rights and attribution before human review")
    return {
        "asOfDate": as_of.isoformat(),
        "maxAgeDays": max_age_days,
        "oldestAgeDays": max(ages, default=0),
        "humanReviewRequired": human_review_required,
    }


def _validate_schema(bundle: dict[str, Any]) -> None:
    schema = _load(SCHEMA)
    errors = sorted(Draft202012Validator(schema).iter_errors(bundle), key=lambda error: list(error.path))
    if errors:
        location = "/".join(str(part) for part in errors[0].path) or "root"
        raise VerificationError(f"bundle schema validation failed at {location}: {errors[0].message}")


def verify(bundle_path: Path, rag_root: Path, as_of: date | None = None, max_age_days: int = 365) -> dict[str, Any]:
    bundle = _load(bundle_path)
    _validate_schema(bundle)
    lifecycle = bundle["lifecycle"]
    if lifecycle != {"status": "Draft", "reviewState": "Not Reviewed", "productionPromotionAllowed": False}:
        raise VerificationError("bundle lifecycle is not the required fail-closed Draft/Not Reviewed state")

    source_repository = bundle["sourceRepository"]
    if source_repository["repository"] != "BuildingRAGAgentsWithLLMs":
        raise VerificationError("source repository is not the authorized RAG Lab repository")
    _commit_is_reachable(rag_root, source_repository["commit"])
    _expect_hash(rag_root, bundle["corpus"], "corpus")
    _expect_hash(rag_root, bundle["dataset"], "dataset")
    _expect_hash(ROOT, bundle["generatedArtifact"], "generated artifact")
    _expect_hash(ROOT, bundle["decisionRecord"], "decision record")
    source_readiness = _check_source_readiness(bundle["sources"], as_of or date.today(), max_age_days)

    return {
        "bundleId": bundle["bundleId"],
        "status": "verified",
        "sourceCommit": source_repository["commit"],
        "productionPromotionAllowed": False,
        "sourceCount": len(bundle["sources"]),
        "sourceReadiness": source_readiness,
    }


def _self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="rkm-evidence-review-") as directory:
        root = Path(directory)
        sample = root / "sample.json"
        sample.write_text("{}\n", encoding="utf-8")
        expected = hashlib.sha256(b"{}\n").hexdigest()
        _expect_hash(root, {"path": "sample.json", "sha256": expected}, "self-test sample")
        try:
            _safe_path(root, "../outside.json", "self-test traversal")
        except VerificationError:
            pass
        else:
            raise AssertionError("path traversal must be rejected")
        fresh_source = {
            "id": "fresh-source",
            "canonicalUrl": "https://example.org/source",
            "rights": "Review required",
            "attribution": "Example",
            "retrievalDate": "2026-07-27",
        }
        readiness = _check_source_readiness([fresh_source], date(2026, 7, 30), 30)
        assert readiness["oldestAgeDays"] == 3
        for invalid_source in (
            {**fresh_source, "retrievalDate": "2025-01-01"},
            {**fresh_source, "retrievalDate": "2026-08-01"},
            {**fresh_source, "canonicalUrl": "http://example.org/source"},
        ):
            try:
                _check_source_readiness([invalid_source], date(2026, 7, 30), 30)
            except VerificationError:
                pass
            else:
                raise AssertionError("invalid source readiness must be rejected")
    _validate_schema(_load(BUNDLE))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=BUNDLE)
    parser.add_argument("--rag-root", type=Path)
    parser.add_argument("--as-of-date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--max-age-days", type=int, default=365)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            _self_test()
            print("external RAG evidence verifier self-test passed")
            return 0
        if args.rag_root is None:
            parser.error("--rag-root is required unless --self-test is used")
        result = verify(args.bundle.resolve(), args.rag_root.resolve(), args.as_of_date, args.max_age_days)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except VerificationError as exc:
        print(f"external RAG evidence verification rejected: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
