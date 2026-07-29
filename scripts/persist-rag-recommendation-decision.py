#!/usr/bin/env python3
"""Create a review-ready, non-production RKM decision record from an adapter envelope."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

CONTRACT = "rkm-rag-recommendation-decision-v1"
ADAPTER_CONTRACT = "rkm-recommendation-artifact-adapter-v1"
SOURCE_CONTRACT = "rag-recommendation-report-v1"
PROFILES = ("economical", "balanced", "maximumQuality")


class DecisionError(ValueError):
    """Raised when the source envelope cannot be persisted safely."""


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DecisionError(f"{field} must be a non-empty string")
    return value


def _hash(value: Any, field: str) -> str:
    value = _text(value, field)
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise DecisionError(f"{field} must be a lowercase SHA-256 hash")
    return value


def _load(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise DecisionError(f"unable to read adapter envelope: {path}") from exc
    if not isinstance(value, dict):
        raise DecisionError("adapter envelope must be an object")
    return value


def persist(envelope: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    if envelope.get("adapterContractVersion") != ADAPTER_CONTRACT:
        raise DecisionError("unsupported adapter contract")
    source = envelope.get("sourceArtifact")
    policy = envelope.get("policyDecision")
    if not isinstance(source, dict) or not isinstance(policy, dict):
        raise DecisionError("adapter envelope must contain sourceArtifact and policyDecision")
    if policy.get("policyVersion") != source.get("policyVersion"):
        raise DecisionError("source and policy decision versions must match")
    profiles = policy.get("profiles")
    if not isinstance(profiles, dict) or any(name not in profiles for name in PROFILES):
        raise DecisionError("adapter envelope must contain all recommendation profiles")
    for name in PROFILES:
        recommendation = profiles[name]
        if not isinstance(recommendation, dict):
            raise DecisionError(f"profile {name} must be an object")
        if recommendation.get("available") is False and recommendation.get("pipelineId") != "":
            raise DecisionError(f"unavailable profile {name} must not identify a pipeline")
    required_metadata = ("artifactSha256", "corpusId", "corpusVersion", "corpusSha256", "datasetId", "datasetVersion", "datasetSha256", "indexProfiles", "pipelineCount")
    if any(field not in metadata for field in required_metadata):
        raise DecisionError("decision metadata is incomplete")
    index_profiles = metadata["indexProfiles"]
    if not isinstance(index_profiles, list) or not index_profiles:
        raise DecisionError("indexProfiles must be a non-empty list")
    normalized_indexes = []
    for profile in index_profiles:
        if not isinstance(profile, dict):
            raise DecisionError("index profile metadata must be an object")
        normalized_indexes.append({"id": _text(profile.get("id"), "index profile id"), "configurationSha256": _hash(profile.get("configurationSha256"), "index profile configuration sha256")})
    pipeline_count = metadata["pipelineCount"]
    if isinstance(pipeline_count, bool) or not isinstance(pipeline_count, int) or pipeline_count < 1:
        raise DecisionError("pipelineCount must be a positive integer")
    experiment_id = _text(source.get("experimentId"), "experimentId")
    decision_id = f"{experiment_id}-decision"
    return {
        "contractVersion": CONTRACT,
        "decisionId": decision_id,
        "decisionType": "RAG_STRATEGY_RECOMMENDATION",
        "lifecycle": {"status": "Draft", "reviewState": "Not Reviewed", "productionPromotionAllowed": False},
        "sourceArtifact": {
            "adapterContractVersion": ADAPTER_CONTRACT,
            "sourceContractVersion": SOURCE_CONTRACT,
            "experimentId": experiment_id,
            "policyVersion": _text(source.get("policyVersion"), "policyVersion"),
            "artifactSha256": _hash(metadata["artifactSha256"], "artifactSha256"),
        },
        "evaluationContext": {
            "corpus": {"id": _text(metadata["corpusId"], "corpusId"), "version": _text(metadata["corpusVersion"], "corpusVersion"), "sha256": _hash(metadata["corpusSha256"], "corpusSha256")},
            "dataset": {"id": _text(metadata["datasetId"], "datasetId"), "version": _text(metadata["datasetVersion"], "datasetVersion"), "sha256": _hash(metadata["datasetSha256"], "datasetSha256")},
            "indexProfiles": normalized_indexes,
            "pipelineCount": pipeline_count,
        },
        "profiles": {name: profiles[name] for name in PROFILES},
    }


def _self_test() -> None:
    digest = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    recommendation = {"profile": "BALANCED", "available": True, "pipelineId": "naive", "indexProfileId": "offline-fixture-index-v1", "qualityScore": 1.0, "latencyP95Ms": 10, "estimatedCost": 0.001, "costCurrency": "LOCAL", "reason": "self-test"}
    envelope = {"adapterContractVersion": ADAPTER_CONTRACT, "sourceArtifact": {"experimentId": "offline-rag-e2e-walkthrough", "policyVersion": "quality-cost-profiles-v1"}, "policyDecision": {"policyVersion": "quality-cost-profiles-v1", "profiles": {"economical": {**recommendation, "profile": "ECONOMICAL"}, "balanced": recommendation, "maximumQuality": {**recommendation, "profile": "MAXIMUM_QUALITY"}}}}
    metadata = {"artifactSha256": digest, "corpusId": "space-corpus", "corpusVersion": "1.0.0", "corpusSha256": digest, "datasetId": "space-golden", "datasetVersion": "1.0.0", "datasetSha256": digest, "indexProfiles": [{"id": "offline-fixture-index-v1", "configurationSha256": digest}], "pipelineCount": 3}
    decision = persist(envelope, metadata)
    assert decision["lifecycle"]["productionPromotionAllowed"] is False
    assert decision["sourceArtifact"]["experimentId"] == "offline-rag-e2e-walkthrough"
    assert decision["profiles"]["balanced"]["pipelineId"] == "naive"
    unavailable = {**recommendation, "available": False, "pipelineId": "", "reason": "INDEX_PROFILE_REVIEW_REQUIRED"}
    unavailable_envelope = {
        **envelope,
        "sourceArtifact": {**envelope["sourceArtifact"], "experimentId": "cross-index-review"},
        "policyDecision": {
            **envelope["policyDecision"],
            "profiles": {
                "economical": {**unavailable, "profile": "ECONOMICAL"},
                "balanced": {**unavailable, "profile": "BALANCED"},
                "maximumQuality": {**unavailable, "profile": "MAXIMUM_QUALITY"},
            },
        },
    }
    unavailable_decision = persist(unavailable_envelope, metadata)
    assert unavailable_decision["profiles"]["balanced"]["available"] is False
    assert unavailable_decision["profiles"]["balanced"]["pipelineId"] == ""
    assert unavailable_decision["lifecycle"]["productionPromotionAllowed"] is False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("envelope", nargs="?", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            _self_test()
            print("RKM recommendation decision self-test passed")
            return 0
        if args.envelope is None or args.metadata is None:
            parser.error("envelope and --metadata are required unless --self-test is used")
        decision = persist(_load(args.envelope), _load(args.metadata))
        print(json.dumps(decision, indent=2, sort_keys=True))
        return 0
    except DecisionError as exc:
        print(f"recommendation decision rejected: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
