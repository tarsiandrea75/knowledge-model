#!/usr/bin/env python3
"""Consume a RAG Lab recommendation artifact at the RKM boundary.

This adapter deliberately does not mutate RKM data. It validates the lab-owned
``rag-recommendation-report-v1`` artifact and emits a stable RKM ingestion
envelope. A later persistence/export task can map that envelope to RKM
Evaluation, Artifact and Policy Decision entities with its own review.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


SOURCE_CONTRACT = "rag-recommendation-report-v1"
SOURCE_ARTIFACT_TYPE = "RAG_RECOMMENDATION_REPORT"
ADAPTER_CONTRACT = "rkm-recommendation-artifact-adapter-v1"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PROFILES = ("economical", "balanced", "maximumQuality")
PROFILE_NAMES = {
    "economical": "ECONOMICAL",
    "balanced": "BALANCED",
    "maximumQuality": "MAXIMUM_QUALITY",
}
ROOT_FIELDS = {
    "contractVersion",
    "artifactType",
    "experimentId",
    "policyVersion",
    "qualityFloor",
    *PROFILES,
}
RECOMMENDATION_FIELDS = {
    "profile",
    "available",
    "pipelineId",
    "indexProfileId",
    "qualityScore",
    "latencyP95Ms",
    "estimatedCost",
    "costCurrency",
    "reason",
}
REQUIRED_RECOMMENDATION_FIELDS = RECOMMENDATION_FIELDS - {"indexProfileId"}


class ArtifactError(ValueError):
    """Actionable contract error without echoing artifact contents."""


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ArtifactError(f"{field} must be a non-empty string")
    return value


def _number(value: Any, field: str, minimum: float, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ArtifactError(f"{field} must be numeric")
    number = float(value)
    if not math.isfinite(number) or number < minimum or (maximum is not None and number > maximum):
        bound = f" between {minimum} and {maximum}" if maximum is not None else f" >= {minimum}"
        raise ArtifactError(f"{field} must be{bound}")
    return number


def _recommendation(value: Any, field: str, expected_profile: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ArtifactError(f"{field} must be an object")
    unknown = set(value) - RECOMMENDATION_FIELDS
    missing = REQUIRED_RECOMMENDATION_FIELDS - set(value)
    if unknown:
        raise ArtifactError(f"{field} contains unknown fields: {', '.join(sorted(unknown))}")
    if missing:
        raise ArtifactError(f"{field} is missing fields: {', '.join(sorted(missing))}")
    if value["profile"] != expected_profile:
        raise ArtifactError(f"{field}.profile must be {expected_profile}")
    if not isinstance(value["available"], bool):
        raise ArtifactError(f"{field}.available must be boolean")
    pipeline_id = value["pipelineId"]
    if not isinstance(pipeline_id, str) or (value["available"] and not pipeline_id.strip()):
        raise ArtifactError(f"{field}.pipelineId must be non-empty when available")
    if not value["available"] and pipeline_id:
        raise ArtifactError(f"{field}.pipelineId must be empty when unavailable")
    index_profile_id = value.get("indexProfileId")
    if index_profile_id is not None and (not isinstance(index_profile_id, str) or not index_profile_id.strip()):
        raise ArtifactError(f"{field}.indexProfileId must be a non-empty string when present")
    latency = _number(value["latencyP95Ms"], f"{field}.latencyP95Ms", 0)
    cost = _number(value["estimatedCost"], f"{field}.estimatedCost", 0)
    quality = _number(value["qualityScore"], f"{field}.qualityScore", 0, 1)
    currency = _text(value["costCurrency"], f"{field}.costCurrency")
    reason = _text(value["reason"], f"{field}.reason")
    if latency != int(latency):
        raise ArtifactError(f"{field}.latencyP95Ms must be an integer")
    result = {
        "profile": value["profile"],
        "available": value["available"],
        "pipelineId": pipeline_id,
        "qualityScore": quality,
        "latencyP95Ms": int(latency),
        "estimatedCost": cost,
        "costCurrency": currency,
        "reason": reason,
    }
    if index_profile_id is not None:
        result["indexProfileId"] = index_profile_id
    return result


def adapt(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise ArtifactError("artifact root must be an object")
    unknown = set(document) - ROOT_FIELDS
    missing = ROOT_FIELDS - set(document)
    if unknown:
        raise ArtifactError(f"artifact contains unknown fields: {', '.join(sorted(unknown))}")
    if missing:
        raise ArtifactError(f"artifact is missing fields: {', '.join(sorted(missing))}")
    if document["contractVersion"] != SOURCE_CONTRACT:
        raise ArtifactError(f"unsupported source contract: {document['contractVersion']!r}")
    if document["artifactType"] != SOURCE_ARTIFACT_TYPE:
        raise ArtifactError(f"unsupported artifact type: {document['artifactType']!r}")
    experiment_id = _text(document["experimentId"], "experimentId")
    policy_version = _text(document["policyVersion"], "policyVersion")
    quality_floor = _number(document["qualityFloor"], "qualityFloor", 0, 1)
    profiles = {
        profile: _recommendation(document[profile], profile, PROFILE_NAMES[profile])
        for profile in PROFILES
    }
    return {
        "adapterContractVersion": ADAPTER_CONTRACT,
        "sourceArtifact": {
            "contractVersion": SOURCE_CONTRACT,
            "artifactType": SOURCE_ARTIFACT_TYPE,
            "experimentId": experiment_id,
            "policyVersion": policy_version,
            "qualityFloor": quality_floor,
        },
        "policyDecision": {
            "decisionId": f"{experiment_id}:recommendation",
            "decisionType": "RAG_STRATEGY_RECOMMENDATION",
            "policyVersion": policy_version,
            "profiles": profiles,
        },
    }


def _load(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactError(f"unable to read JSON artifact: {path}") from exc


def _self_test() -> None:
    valid = {
        "contractVersion": SOURCE_CONTRACT,
        "artifactType": SOURCE_ARTIFACT_TYPE,
        "experimentId": "demo-001",
        "policyVersion": "quality-cost-profiles-v1",
        "qualityFloor": 0.8,
    }
    for profile in PROFILES:
        valid[profile] = {
            "profile": PROFILE_NAMES[profile],
            "available": True,
            "pipelineId": "naive",
            "qualityScore": 1.0,
            "latencyP95Ms": 0,
            "estimatedCost": 0.0,
            "costCurrency": "LOCAL",
            "reason": "self-test",
        }
    valid["balanced"]["indexProfileId"] = "offline-lexical-v1"
    envelope = adapt(valid)
    assert envelope["adapterContractVersion"] == ADAPTER_CONTRACT
    assert envelope["policyDecision"]["profiles"]["balanced"]["pipelineId"] == "naive"
    assert envelope["policyDecision"]["profiles"]["balanced"]["indexProfileId"] == "offline-lexical-v1"
    unavailable = dict(valid)
    unavailable["balanced"] = {
        **valid["balanced"],
        "available": False,
        "pipelineId": "",
        "indexProfileId": "index-profile-a",
        "reason": "INDEX_PROFILE_REVIEW_REQUIRED; explicit index-aware policy is required.",
    }
    unavailable_envelope = adapt(unavailable)
    balanced = unavailable_envelope["policyDecision"]["profiles"]["balanced"]
    assert balanced["available"] is False
    assert balanced["pipelineId"] == ""
    assert "INDEX_PROFILE_REVIEW_REQUIRED" in balanced["reason"]
    fixture = REPOSITORY_ROOT / "examples" / "fixtures" / "rag-recommendation-report-v1-index-review.json"
    fixture_envelope = adapt(_load(fixture))
    fixture_profiles = fixture_envelope["policyDecision"]["profiles"].values()
    assert all(not profile["available"] for profile in fixture_profiles)
    assert all("INDEX_PROFILE_REVIEW_REQUIRED" in profile["reason"] for profile in fixture_profiles)
    generated_fixture = REPOSITORY_ROOT / "examples" / "fixtures" / "rag-recommendation-report-v1-generated.json"
    generated_envelope = adapt(_load(generated_fixture))
    assert generated_envelope["sourceArtifact"]["experimentId"] == "offline-rag-e2e-walkthrough"
    assert generated_envelope["policyDecision"]["profiles"]["balanced"]["pipelineId"] == "naive"
    assert generated_envelope["policyDecision"]["profiles"]["balanced"]["indexProfileId"] == "offline-fixture-index-v1"
    invalid = dict(valid)
    invalid["unexpected"] = True
    try:
        adapt(invalid)
    except ArtifactError:
        pass
    else:
        raise AssertionError("unknown artifact field was accepted")
    invalid_unavailable = dict(valid)
    invalid_unavailable["balanced"] = {
        **valid["balanced"],
        "available": False,
        "pipelineId": "naive",
        "reason": "invalid unavailable recommendation self-test",
    }
    try:
        adapt(invalid_unavailable)
    except ArtifactError:
        pass
    else:
        raise AssertionError("unavailable recommendation retained a pipeline")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", nargs="?", type=Path, help="RAG Lab recommendation JSON artifact")
    parser.add_argument("--self-test", action="store_true", help="run the adapter self-test")
    args = parser.parse_args()
    try:
        if args.self_test:
            _self_test()
            print("recommendation artifact adapter self-test passed")
            return 0
        if args.artifact is None:
            parser.error("artifact is required unless --self-test is used")
        print(json.dumps(adapt(_load(args.artifact)), indent=2, sort_keys=True))
        return 0
    except ArtifactError as exc:
        print(f"recommendation artifact rejected: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
