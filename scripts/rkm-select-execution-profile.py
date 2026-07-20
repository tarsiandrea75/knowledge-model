#!/usr/bin/env python3
"""Select an RKM Codex execution profile from deterministic task signals."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from dataclasses import asdict, dataclass
from pathlib import PurePosixPath
from typing import Iterable, Sequence


TIER_NAMES = {
    0: "deterministic",
    1: "mechanical",
    2: "bounded-semantic",
    3: "engineering",
    4: "strategic",
    5: "exceptional-multi-agent",
}

DEFAULT_PROFILES = {
    1: "rkm-mechanical",
    2: "rkm-bounded",
    3: "rkm-engineering",
    4: "rkm-strategic",
    5: "rkm-exceptional",
}

PROFILE_ENV_VARS = {
    1: "RKM_CODEX_PROFILE_MECHANICAL",
    2: "RKM_CODEX_PROFILE_BOUNDED",
    3: "RKM_CODEX_PROFILE_ENGINEERING",
    4: "RKM_CODEX_PROFILE_STRATEGIC",
    5: "RKM_CODEX_PROFILE_EXCEPTIONAL",
}

CREATOR_REASONING = {
    0: None,
    1: "low",
    2: "low",
    3: "medium",
    4: "high",
    5: "high",
}

REVIEWER_REASONING = {
    0: None,
    1: None,
    2: "medium",
    3: "high",
    4: "high",
    5: "high",
}

TASK_TYPE_TIERS = {
    "deterministic-check": 0,
    "mechanical": 1,
    "documentation": 2,
    "data-record": 3,
    "governance": 3,
    "code": 3,
    "validation": 3,
    "recovery": 3,
    "automation": 3,
    "research": 3,
    "architecture": 4,
    "schema": 4,
    "ontology": 4,
    "release": 4,
    "integration": 4,
    "strategic": 4,
}

PREVIOUS_OUTCOMES = (
    "none",
    "invalid",
    "validation-failure",
    "revise",
    "stop",
)

GOVERNANCE_PATHS = {
    "AGENTS.md",
    "docs/maintenance/automation-guardrails.md",
    "docs/maintenance/governance-backlog.md",
    "docs/maintenance/live-handoff.md",
    "docs/maintenance/rule-coverage-report.md",
}

BOUNDED_DOCUMENTATION_PATHS = {
    "README.md",
    "QUICKSTART.md",
    "data/README.md",
    "docs/maintenance/assistant-handoff.md",
    "docs/maintenance/consumer-guide.md",
    "docs/maintenance/graph-export-contract.md",
    "docs/maintenance/maturity-report.md",
    "examples/data-graph-export/README.md",
}

HIGH_RISK_SCRIPT_NAMES = {
    "rkm-autopilot.py",
    "rkm-budget.py",
    "rkm-codex-commit.sh",
    "rkm-cycle.sh",
    "rkm-director.sh",
    "rkm-discover.sh",
    "rkm-recover-revise.sh",
    "validate-rkm.sh",
}


@dataclass(frozen=True)
class AgentSelection:
    required: bool
    required_on_change: bool
    profile: str | None
    reasoning_effort: str | None
    max_calls: int
    skip_on_no_change_required: bool


@dataclass(frozen=True)
class EscalationSelection:
    available: bool
    automatic: bool
    target_tier: int | None
    target_tier_name: str | None
    profile: str | None
    max_escalations: int
    requires_explicit_authorization: bool


@dataclass(frozen=True)
class Selection:
    version: int
    paths: Sequence[str]
    requested_task_type: str
    resolved_task_type: str
    tier: int
    tier_name: str
    deterministic_only: bool
    evidence_bundle_required: bool
    creator: AgentSelection
    reviewer: AgentSelection
    escalation: EscalationSelection
    signals: dict[str, object]
    reasons: Sequence[str]


def normalized_path(raw_path: str) -> str:
    cleaned = raw_path.strip().replace("\\", "/")
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    if not cleaned:
        return ""
    return str(PurePosixPath(cleaned))


def parse_paths(raw_paths: Sequence[str] | None) -> Sequence[str]:
    if not raw_paths:
        return ()

    parsed: list[str] = []
    for raw_value in raw_paths:
        for token in shlex.split(raw_value.replace(",", " ")):
            path = normalized_path(token)
            if path and path not in parsed:
                parsed.append(path)
    return tuple(parsed)


def is_under(path: str, prefix: str) -> bool:
    return path == prefix.rstrip("/") or path.startswith(prefix)


def path_basename(path: str) -> str:
    return PurePosixPath(path).name


def configured_profile(tier: int) -> str | None:
    if tier == 0:
        return None
    env_name = PROFILE_ENV_VARS[tier]
    return os.environ.get(env_name, DEFAULT_PROFILES[tier])


def infer_path_tier(path: str) -> tuple[int, str, list[str]]:
    reasons: list[str] = []

    if path in GOVERNANCE_PATHS:
        reasons.append(f"{path} is a governance or operational-authority path.")
        return 3, "governance", reasons

    if path in BOUNDED_DOCUMENTATION_PATHS:
        reasons.append(f"{path} is an established bounded consumer-documentation path.")
        return 2, "documentation", reasons

    if is_under(path, "schema/"):
        reasons.append(f"{path} is under schema/ and may change a structural contract.")
        return 4, "schema", reasons

    if is_under(path, "docs/architecture/"):
        reasons.append(f"{path} is under docs/architecture/ and may change architecture semantics.")
        return 4, "architecture", reasons

    if path in {
        "docs/maintenance/rkm-autonomous-loop-contract.md",
        "docs/maintenance/rkm-autonomous-product-director.md",
        "docs/maintenance/rkm-director-prompt.md",
    }:
        reasons.append(f"{path} defines strategic or cross-cutting autonomous behavior.")
        return 4, "strategic", reasons

    if is_under(path, "docs/releases/") or path == "CHANGELOG.md":
        reasons.append(f"{path} affects release scope or release evidence.")
        return 4, "release", reasons

    if is_under(path, "data/") and path.endswith(".json"):
        reasons.append(f"{path} is canonical populated data requiring semantic accuracy.")
        return 3, "data-record", reasons

    if is_under(path, "registries/"):
        reasons.append(f"{path} changes a registry contract or allowed semantic value.")
        return 4, "ontology", reasons

    if is_under(path, "scripts/") or path == "Makefile":
        if path_basename(path) in HIGH_RISK_SCRIPT_NAMES or path == "Makefile":
            reasons.append(f"{path} affects validation, recovery, automation, budget, or execution.")
        else:
            reasons.append(f"{path} is executable repository tooling.")
        return 3, "code", reasons

    if is_under(path, ".codex/"):
        reasons.append(f"{path} changes Codex execution or agent configuration.")
        return 3, "automation", reasons

    if (
        is_under(path, "examples/data-graph-export/")
        and path.endswith((".nodes.json", ".edges.json"))
    ):
        reasons.append(f"{path} is a deterministic generated graph artifact.")
        return 0, "deterministic-check", reasons

    if path.endswith(".md"):
        reasons.append(f"{path} is documentation without a stronger path-specific signal.")
        return 2, "documentation", reasons

    reasons.append(f"{path} has no lower-risk path rule; engineering is the safe default.")
    return 3, "code", reasons


def choose_base_tier(
    paths: Sequence[str],
    requested_task_type: str,
) -> tuple[int, str, list[str]]:
    if requested_task_type != "auto":
        tier = TASK_TYPE_TIERS[requested_task_type]
        return (
            tier,
            requested_task_type,
            [f"Explicit task type {requested_task_type} selects Tier {tier}."],
        )

    if not paths:
        return (
            3,
            "code",
            ["No paths or explicit task type were provided; engineering is the safe default."],
        )

    candidates = [infer_path_tier(path) for path in paths]
    tier = max(candidate[0] for candidate in candidates)
    selected_types = [
        candidate[1]
        for candidate in candidates
        if candidate[0] == tier
    ]
    resolved_type = sorted(selected_types)[0]
    reasons = [
        reason
        for candidate in candidates
        for reason in candidate[2]
    ]
    return tier, resolved_type, reasons


def apply_risk_signals(
    tier: int,
    reasons: list[str],
    *,
    changed_file_count: int,
    external_research: bool,
    previous_outcome: str,
    high_consequence: bool,
) -> int:
    selected = tier

    if changed_file_count > 3:
        selected = max(selected, 4)
        reasons.append(
            f"{changed_file_count} authorized files require at least strategic coordination."
        )
    elif changed_file_count > 1:
        selected = max(selected, 3)
        reasons.append(
            f"{changed_file_count} authorized files require at least engineering coordination."
        )

    if external_research:
        selected = max(selected, 3)
        reasons.append("External factual research requires at least the engineering tier.")

    if previous_outcome in {"invalid", "validation-failure", "revise"}:
        old = selected
        selected = min(4, selected + 1)
        reasons.append(
            f"Previous outcome {previous_outcome} escalates Tier {old} to Tier {selected}."
        )
    elif previous_outcome == "stop":
        selected = max(selected, 4)
        reasons.append("A previous STOP requires strategic replanning or recovery.")

    if high_consequence:
        selected = max(selected, 4)
        reasons.append("High false-acceptance consequence requires the strategic tier.")

    return selected


def build_creator(tier: int) -> AgentSelection:
    if tier == 0:
        return AgentSelection(
            required=False,
            required_on_change=False,
            profile=None,
            reasoning_effort=None,
            max_calls=0,
            skip_on_no_change_required=True,
        )

    return AgentSelection(
        required=True,
        required_on_change=True,
        profile=configured_profile(tier),
        reasoning_effort=CREATOR_REASONING[tier],
        max_calls=1,
        skip_on_no_change_required=False,
    )


def build_reviewer(tier: int) -> AgentSelection:
    if tier <= 1:
        return AgentSelection(
            required=False,
            required_on_change=False,
            profile=None,
            reasoning_effort=None,
            max_calls=0,
            skip_on_no_change_required=True,
        )

    return AgentSelection(
        required=False,
        required_on_change=True,
        profile=configured_profile(tier),
        reasoning_effort=REVIEWER_REASONING[tier],
        max_calls=1,
        skip_on_no_change_required=True,
    )


def build_escalation(tier: int) -> EscalationSelection:
    if tier >= 5:
        return EscalationSelection(
            available=False,
            automatic=False,
            target_tier=None,
            target_tier_name=None,
            profile=None,
            max_escalations=0,
            requires_explicit_authorization=True,
        )

    target_tier = tier + 1
    return EscalationSelection(
        available=True,
        automatic=tier < 4,
        target_tier=target_tier,
        target_tier_name=TIER_NAMES[target_tier],
        profile=configured_profile(target_tier),
        max_escalations=1,
        requires_explicit_authorization=target_tier == 5,
    )


def select_profile(
    paths: Iterable[str] = (),
    *,
    task_type: str = "auto",
    changed_file_count: int | None = None,
    external_research: bool = False,
    previous_outcome: str = "none",
    high_consequence: bool = False,
) -> Selection:
    normalized_paths = tuple(
        path
        for raw_path in paths
        if (path := normalized_path(raw_path))
    )

    base_tier, resolved_type, reasons = choose_base_tier(
        normalized_paths,
        task_type,
    )

    effective_file_count = (
        changed_file_count
        if changed_file_count is not None
        else len(normalized_paths)
    )
    if effective_file_count < 0:
        raise ValueError("changed_file_count must be non-negative")

    tier = apply_risk_signals(
        base_tier,
        reasons,
        changed_file_count=effective_file_count,
        external_research=external_research,
        previous_outcome=previous_outcome,
        high_consequence=high_consequence,
    )

    deterministic_only = tier == 0
    evidence_bundle_required = tier >= 2

    return Selection(
        version=1,
        paths=normalized_paths,
        requested_task_type=task_type,
        resolved_task_type=resolved_type,
        tier=tier,
        tier_name=TIER_NAMES[tier],
        deterministic_only=deterministic_only,
        evidence_bundle_required=evidence_bundle_required,
        creator=build_creator(tier),
        reviewer=build_reviewer(tier),
        escalation=build_escalation(tier),
        signals={
            "changedFileCount": effective_file_count,
            "externalResearch": external_research,
            "previousOutcome": previous_outcome,
            "highConsequence": high_consequence,
        },
        reasons=tuple(reasons),
    )


def selection_as_json(selection: Selection) -> str:
    payload = asdict(selection)
    return json.dumps(payload, indent=2, sort_keys=True)


def selection_as_text(selection: Selection) -> str:
    creator = selection.creator
    reviewer = selection.reviewer
    escalation = selection.escalation

    lines = [
        "# RKM Codex Execution Profile",
        "",
        "## Selection",
        "",
        f"- Tier: `{selection.tier}` (`{selection.tier_name}`)",
        f"- Task type: `{selection.resolved_task_type}`",
        f"- Deterministic only: `{str(selection.deterministic_only).lower()}`",
        (
            "- Evidence bundle required: "
            f"`{str(selection.evidence_bundle_required).lower()}`"
        ),
        "",
        "## Creator",
        "",
        f"- Required: `{str(creator.required).lower()}`",
        f"- Profile: `{creator.profile or 'none'}`",
        f"- Reasoning effort: `{creator.reasoning_effort or 'none'}`",
        f"- Maximum calls: `{creator.max_calls}`",
        "",
        "## Reviewer",
        "",
        (
            "- Required on changed candidate: "
            f"`{str(reviewer.required_on_change).lower()}`"
        ),
        f"- Profile: `{reviewer.profile or 'none'}`",
        f"- Reasoning effort: `{reviewer.reasoning_effort or 'none'}`",
        (
            "- Skip on `NO_CHANGE_REQUIRED`: "
            f"`{str(reviewer.skip_on_no_change_required).lower()}`"
        ),
        "",
        "## Escalation",
        "",
        f"- Available: `{str(escalation.available).lower()}`",
        f"- Automatic: `{str(escalation.automatic).lower()}`",
        f"- Target tier: `{escalation.target_tier_name or 'none'}`",
        f"- Profile: `{escalation.profile or 'none'}`",
        f"- Maximum escalations: `{escalation.max_escalations}`",
        (
            "- Explicit authorization required: "
            f"`{str(escalation.requires_explicit_authorization).lower()}`"
        ),
        "",
        "## Reasons",
        "",
    ]

    lines.extend(f"- {reason}" for reason in selection.reasons)
    return "\n".join(lines) + "\n"


def assert_selection(
    selection: Selection,
    *,
    tier: int,
    creator_profile: str | None,
    reviewer_required_on_change: bool,
) -> None:
    assert selection.tier == tier, selection
    assert selection.creator.profile == creator_profile, selection
    assert (
        selection.reviewer.required_on_change
        == reviewer_required_on_change
    ), selection


def run_self_test() -> None:
    assert_selection(
        select_profile(task_type="deterministic-check"),
        tier=0,
        creator_profile=None,
        reviewer_required_on_change=False,
    )

    assert_selection(
        select_profile(("QUICKSTART.md",)),
        tier=2,
        creator_profile=configured_profile(2),
        reviewer_required_on_change=True,
    )

    assert_selection(
        select_profile(("docs/maintenance/governance-backlog.md",)),
        tier=3,
        creator_profile=configured_profile(3),
        reviewer_required_on_change=True,
    )

    assert_selection(
        select_profile(("scripts/rkm-cycle.sh",)),
        tier=3,
        creator_profile=configured_profile(3),
        reviewer_required_on_change=True,
    )

    assert_selection(
        select_profile(("schema/vector-database.schema.json",)),
        tier=4,
        creator_profile=configured_profile(4),
        reviewer_required_on_change=True,
    )

    assert_selection(
        select_profile(("README.md", "QUICKSTART.md")),
        tier=3,
        creator_profile=configured_profile(3),
        reviewer_required_on_change=True,
    )

    assert_selection(
        select_profile(
            ("README.md",),
            external_research=True,
        ),
        tier=3,
        creator_profile=configured_profile(3),
        reviewer_required_on_change=True,
    )

    assert_selection(
        select_profile(
            ("QUICKSTART.md",),
            previous_outcome="stop",
        ),
        tier=4,
        creator_profile=configured_profile(4),
        reviewer_required_on_change=True,
    )

    assert_selection(
        select_profile(
            ("examples/data-graph-export/rag-techniques.nodes.json",),
        ),
        tier=0,
        creator_profile=None,
        reviewer_required_on_change=False,
    )

    assert_selection(
        select_profile(
            ("README.md",),
            high_consequence=True,
        ),
        tier=4,
        creator_profile=configured_profile(4),
        reviewer_required_on_change=True,
    )

    overridden = os.environ.copy()
    try:
        os.environ["RKM_CODEX_PROFILE_BOUNDED"] = "custom-bounded"
        selection = select_profile(("QUICKSTART.md",))
        assert selection.creator.profile == "custom-bounded"
        assert selection.reviewer.profile == "custom-bounded"
    finally:
        os.environ.clear()
        os.environ.update(overridden)

    first = selection_as_json(select_profile(("README.md",)))
    second = selection_as_json(select_profile(("README.md",)))
    assert first == second

    print("RKM execution profile selector self-test passed.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paths",
        action="append",
        help=(
            "Authorized repository paths. May be repeated or contain "
            "shell-style whitespace-separated paths."
        ),
    )
    parser.add_argument(
        "--task-type",
        choices=("auto", *TASK_TYPE_TIERS.keys()),
        default="auto",
        help="Explicit task classification. Default: infer from paths.",
    )
    parser.add_argument(
        "--changed-file-count",
        type=int,
        help="Authorized file count when it differs from the supplied path count.",
    )
    parser.add_argument(
        "--external-research",
        action="store_true",
        help="Raise the minimum tier for externally researched factual work.",
    )
    parser.add_argument(
        "--previous-outcome",
        choices=PREVIOUS_OUTCOMES,
        default="none",
        help="Escalate after an invalid result, validation failure, REVISE, or STOP.",
    )
    parser.add_argument(
        "--high-consequence",
        action="store_true",
        help="Require the strategic tier because false acceptance is costly.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Default: text.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run deterministic built-in tests and exit.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        run_self_test()
        return 0

    paths = parse_paths(args.paths)
    try:
        selection = select_profile(
            paths,
            task_type=args.task_type,
            changed_file_count=args.changed_file_count,
            external_research=args.external_research,
            previous_outcome=args.previous_outcome,
            high_consequence=args.high_consequence,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "json":
        print(selection_as_json(selection))
    else:
        print(selection_as_text(selection), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
