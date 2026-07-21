#!/usr/bin/env python3
"""Build a compact deterministic evidence bundle for one RKM task."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


DATA_MANIFEST = Path("data/manifest.json")
DATA_GRAPH_NODES = Path(
    "examples/data-graph-export/rag-techniques.nodes.json"
)
DATA_GRAPH_EDGES = Path(
    "examples/data-graph-export/rag-techniques.edges.json"
)

VALIDATION_PASS_MARKER = "RKM validation passed."
VALIDATION_FAILURE_MARKERS = (
    "make: ***",
    "ERROR:",
    "Traceback (most recent call last)",
)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        temporary_path.write_text(
            content,
            encoding="utf-8",
            newline="\n",
        )
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_path(raw_path: str) -> str:
    cleaned = raw_path.strip().replace("\\", "/")
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned


def parse_paths(raw_paths: Sequence[str] | None) -> list[str]:
    paths: list[str] = []
    for raw_value in raw_paths or ():
        for token in shlex.split(raw_value.replace(",", " ")):
            path = normalized_path(token)
            if path and path not in paths:
                paths.append(path)
    return sorted(paths)


def ensure_inside_repository(
    repository: Path,
    relative_path: str,
) -> Path:
    candidate = (repository / relative_path).resolve()
    try:
        candidate.relative_to(repository)
    except ValueError as exc:
        raise ValueError(
            f"path escapes repository: {relative_path}"
        ) from exc
    return candidate


def run_git(
    repository: Path,
    arguments: Sequence[str],
    *,
    allow_failure: bool = False,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
    )
    if completed.returncode != 0 and not allow_failure:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"git {' '.join(arguments)} failed: {detail}"
        )
    return completed


def git_text(
    repository: Path,
    arguments: Sequence[str],
    *,
    default: str = "UNKNOWN",
) -> str:
    completed = run_git(
        repository,
        arguments,
        allow_failure=True,
    )
    if completed.returncode != 0:
        return default
    value = completed.stdout.strip()
    return value or default


def repository_facts(repository: Path) -> dict[str, Any]:
    status = git_text(
        repository,
        ("status", "--short", "--untracked-files=all"),
        default="",
    )
    status_lines = [
        line
        for line in status.splitlines()
        if line.strip()
    ]
    return {
        "branch": git_text(
            repository,
            ("branch", "--show-current"),
        ),
        "head": git_text(
            repository,
            ("rev-parse", "HEAD"),
        ),
        "upstream": git_text(
            repository,
            ("rev-parse", "@{upstream}"),
        ),
        "localMain": git_text(
            repository,
            ("rev-parse", "main"),
        ),
        "originMain": git_text(
            repository,
            ("rev-parse", "origin/main"),
        ),
        "statusLines": status_lines,
        "clean": not status_lines,
    }


def path_git_status(
    repository: Path,
    relative_path: str,
) -> list[str]:
    value = git_text(
        repository,
        (
            "status",
            "--short",
            "--untracked-files=all",
            "--",
            relative_path,
        ),
        default="",
    )
    return [
        line
        for line in value.splitlines()
        if line.strip()
    ]


def path_is_tracked(
    repository: Path,
    relative_path: str,
) -> bool:
    completed = run_git(
        repository,
        ("ls-files", "--error-unmatch", "--", relative_path),
        allow_failure=True,
    )
    return completed.returncode == 0


def line_count(path: Path) -> int:
    content = path.read_bytes()
    if not content:
        return 0
    return content.count(b"\n") + (
        0 if content.endswith(b"\n") else 1
    )


def scope_file_fact(
    repository: Path,
    relative_path: str,
) -> dict[str, Any]:
    absolute_path = ensure_inside_repository(
        repository,
        relative_path,
    )
    fact: dict[str, Any] = {
        "path": relative_path,
        "exists": absolute_path.exists(),
        "tracked": path_is_tracked(
            repository,
            relative_path,
        ),
        "gitStatus": path_git_status(
            repository,
            relative_path,
        ),
    }

    if not absolute_path.exists():
        fact["kind"] = "missing"
        return fact

    if absolute_path.is_dir():
        files = sorted(
            str(path.relative_to(repository)).replace("\\", "/")
            for path in absolute_path.rglob("*")
            if path.is_file()
        )
        fact.update(
            {
                "kind": "directory",
                "fileCount": len(files),
                "files": files,
            }
        )
        return fact

    fact.update(
        {
            "kind": "file",
            "sha256": sha256_file(absolute_path),
            "sizeBytes": absolute_path.stat().st_size,
            "lineCount": line_count(absolute_path),
        }
    )
    return fact


def selector_command(
    selector: Path,
    paths: Sequence[str],
    *,
    task_type: str,
    changed_file_count: int | None,
    external_research: bool,
    previous_outcome: str,
    high_consequence: bool,
) -> list[str]:
    command = [
        sys.executable,
        "-B",
        str(selector),
        "--task-type",
        task_type,
        "--previous-outcome",
        previous_outcome,
        "--format",
        "json",
    ]

    for path in paths:
        command.extend(("--paths", path))

    if changed_file_count is not None:
        command.extend(
            ("--changed-file-count", str(changed_file_count))
        )
    if external_research:
        command.append("--external-research")
    if high_consequence:
        command.append("--high-consequence")
    return command


def routing_facts(
    selector: Path,
    paths: Sequence[str],
    *,
    task_type: str,
    changed_file_count: int | None,
    external_research: bool,
    previous_outcome: str,
    high_consequence: bool,
) -> dict[str, Any]:
    completed = subprocess.run(
        selector_command(
            selector,
            paths,
            task_type=task_type,
            changed_file_count=changed_file_count,
            external_research=external_research,
            previous_outcome=previous_outcome,
            high_consequence=high_consequence,
        ),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"execution-profile selector failed: {detail}"
        )

    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise RuntimeError(
            "execution-profile selector returned a non-object"
        )
    return value


def manifest_facts(repository: Path) -> dict[str, Any]:
    path = repository / DATA_MANIFEST
    if not path.is_file():
        return {
            "path": str(DATA_MANIFEST),
            "exists": False,
        }

    value = load_json(path)
    if not isinstance(value, dict):
        raise ValueError("data manifest must be a JSON object")

    entries = value.get("data")
    if not isinstance(entries, list):
        raise ValueError("data manifest data must be an array")

    declared_files: list[str] = []
    schema_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    duplicate_counter: Counter[str] = Counter()

    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(
                "data manifest entry must be an object"
            )
        file_value = entry.get("file")
        schema_value = entry.get("schema")
        if not isinstance(file_value, str):
            raise ValueError(
                "data manifest entry file must be a string"
            )
        if not isinstance(schema_value, str):
            raise ValueError(
                "data manifest entry schema must be a string"
            )

        declared_files.append(file_value)
        duplicate_counter[file_value] += 1
        schema_counts[schema_value] += 1

        parts = Path(file_value).parts
        category = (
            parts[1]
            if len(parts) > 2 and parts[0] == "data"
            else "other"
        )
        category_counts[category] += 1

    duplicates = sorted(
        file_value
        for file_value, count in duplicate_counter.items()
        if count > 1
    )

    return {
        "path": str(DATA_MANIFEST),
        "exists": True,
        "sha256": sha256_file(path),
        "declaredFileCount": len(declared_files),
        "categoryCounts": dict(
            sorted(category_counts.items())
        ),
        "schemaCounts": dict(
            sorted(schema_counts.items())
        ),
        "duplicateFiles": duplicates,
        "declaredFiles": sorted(declared_files),
    }


def nested_string(
    value: Mapping[str, Any],
    keys: Sequence[str],
) -> str | None:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current if isinstance(current, str) else None


def first_string(
    candidates: Sequence[str | None],
) -> str | None:
    for value in candidates:
        if isinstance(value, str) and value:
            return value
    return None


def lifecycle_fact(
    repository: Path,
    relative_path: str,
) -> dict[str, Any] | None:
    if not relative_path.startswith("data/"):
        return None
    if not relative_path.endswith(".json"):
        return None

    path = ensure_inside_repository(
        repository,
        relative_path,
    )
    if not path.is_file():
        return None

    try:
        value = load_json(path)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {
            "path": relative_path,
            "jsonReadable": False,
        }

    if not isinstance(value, dict):
        return {
            "path": relative_path,
            "jsonReadable": True,
            "recordObject": False,
        }

    identity = value.get("identity")
    metadata = value.get("metadata")
    identity_object = (
        identity if isinstance(identity, dict) else {}
    )
    metadata_object = (
        metadata if isinstance(metadata, dict) else {}
    )

    status = first_string(
        (
            value.get("status")
            if isinstance(value.get("status"), str)
            else None,
            metadata_object.get("status")
            if isinstance(metadata_object.get("status"), str)
            else None,
            identity_object.get("status")
            if isinstance(identity_object.get("status"), str)
            else None,
            nested_string(
                metadata_object,
                ("lifecycle", "status"),
            ),
        )
    )
    review_state = first_string(
        (
            metadata_object.get("reviewState")
            if isinstance(
                metadata_object.get("reviewState"),
                str,
            )
            else None,
            value.get("reviewState")
            if isinstance(value.get("reviewState"), str)
            else None,
            nested_string(
                metadata_object,
                ("review", "state"),
            ),
        )
    )
    review_date = first_string(
        (
            metadata_object.get("reviewDate")
            if isinstance(
                metadata_object.get("reviewDate"),
                str,
            )
            else None,
            value.get("reviewDate")
            if isinstance(value.get("reviewDate"), str)
            else None,
            nested_string(
                metadata_object,
                ("review", "date"),
            ),
        )
    )

    fact: dict[str, Any] = {
        "path": relative_path,
        "jsonReadable": True,
        "recordObject": True,
        "id": first_string(
            (
                identity_object.get("id")
                if isinstance(identity_object.get("id"), str)
                else None,
                value.get("id")
                if isinstance(value.get("id"), str)
                else None,
            )
        ),
        "slug": first_string(
            (
                identity_object.get("slug")
                if isinstance(identity_object.get("slug"), str)
                else None,
                value.get("slug")
                if isinstance(value.get("slug"), str)
                else None,
            )
        ),
        "entityType": first_string(
            (
                identity_object.get("entityType")
                if isinstance(
                    identity_object.get("entityType"),
                    str,
                )
                else None,
                value.get("entityType")
                if isinstance(value.get("entityType"), str)
                else None,
            )
        ),
        "version": first_string(
            (
                identity_object.get("version")
                if isinstance(
                    identity_object.get("version"),
                    str,
                )
                else None,
                value.get("version")
                if isinstance(value.get("version"), str)
                else None,
            )
        ),
        "status": status,
        "reviewState": review_state,
        "reviewDate": review_date,
    }
    return fact


def graph_array(value: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        items = value
    elif isinstance(value, dict):
        items = value.get(key)
    else:
        items = None

    if not isinstance(items, list):
        raise ValueError(
            f"graph export {key} must be an array"
        )
    if not all(isinstance(item, dict) for item in items):
        raise ValueError(
            f"graph export {key} items must be objects"
        )
    return items


def graph_file_fact(
    repository: Path,
    relative_path: Path,
    key: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    path = repository / relative_path
    if not path.is_file():
        return (
            {
                "path": str(relative_path),
                "exists": False,
            },
            [],
        )

    value = load_json(path)
    items = graph_array(value, key)
    return (
        {
            "path": str(relative_path),
            "exists": True,
            "sha256": sha256_file(path),
            "count": len(items),
        },
        items,
    )


def graph_facts(
    repository: Path,
    scope_paths: Sequence[str],
) -> dict[str, Any]:
    nodes_fact, nodes = graph_file_fact(
        repository,
        DATA_GRAPH_NODES,
        "nodes",
    )
    edges_fact, edges = graph_file_fact(
        repository,
        DATA_GRAPH_EDGES,
        "edges",
    )

    node_type_counts = Counter(
        node.get("type")
        for node in nodes
        if isinstance(node.get("type"), str)
    )
    predicate_counts = Counter(
        edge.get("predicate")
        for edge in edges
        if isinstance(edge.get("predicate"), str)
    )

    scoped_nodes = [
        node
        for node in nodes
        if node.get("sourceDataFile") in scope_paths
    ]
    scoped_node_ids = {
        node.get("id")
        for node in scoped_nodes
        if isinstance(node.get("id"), str)
    }
    scoped_edges = [
        edge
        for edge in edges
        if (
            edge.get("sourceDataFile") in scope_paths
            or edge.get("sourceId") in scoped_node_ids
            or edge.get("targetId") in scoped_node_ids
        )
    ]

    return {
        "authority": {
            "sourceRecordsAuthoritative": True,
            "exportsDerived": True,
        },
        "nodes": nodes_fact,
        "edges": edges_fact,
        "nodeTypeCounts": dict(
            sorted(node_type_counts.items())
        ),
        "predicateCounts": dict(
            sorted(predicate_counts.items())
        ),
        "scope": {
            "nodeIds": sorted(
                node.get("id")
                for node in scoped_nodes
                if isinstance(node.get("id"), str)
            ),
            "edgeIds": sorted(
                edge.get("id")
                for edge in scoped_edges
                if isinstance(edge.get("id"), str)
            ),
        },
    }


def validation_facts(
    status: str,
    log_path: Path | None,
) -> dict[str, Any]:
    fact: dict[str, Any] = {
        "reportedStatus": status,
        "logProvided": log_path is not None,
    }

    if log_path is None:
        if status != "not-run":
            raise ValueError(
                "validation pass or fail requires --validation-log"
            )
        return fact

    path = log_path.expanduser().resolve()
    if not path.is_file():
        raise ValueError(
            f"validation log does not exist: {path}"
        )

    content = path.read_text(
        encoding="utf-8",
        errors="replace",
    )
    pass_marker = VALIDATION_PASS_MARKER in content
    failure_markers = sorted(
        marker
        for marker in VALIDATION_FAILURE_MARKERS
        if marker in content
    )

    observed_status = (
        "pass"
        if pass_marker and not failure_markers
        else "fail"
    )

    if status != observed_status:
        raise ValueError(
            "reported validation status conflicts with log markers"
        )

    fact.update(
        {
            "logName": path.name,
            "logSha256": sha256_file(path),
            "logSizeBytes": path.stat().st_size,
            "passMarkerObserved": pass_marker,
            "failureMarkersObserved": failure_markers,
            "observedStatus": observed_status,
            "statusConsistent": True,
        }
    )
    return fact


def wrapper_metadata_fact(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(
            f"wrapper metadata does not exist: {resolved}"
        )

    value = load_json(resolved)
    if not isinstance(value, dict):
        raise ValueError(
            "wrapper metadata must be a JSON object"
        )

    selection = value.get("selection")
    selection_object = (
        selection if isinstance(selection, dict) else {}
    )
    attempts = value.get("attempts")
    attempt_list = attempts if isinstance(attempts, list) else []

    safe_attempts: list[dict[str, Any]] = []
    for attempt in attempt_list:
        if not isinstance(attempt, dict):
            continue
        safe_attempts.append(
            {
                "attempt": attempt.get("attempt"),
                "profile": attempt.get("profile"),
                "reasoningEffort": attempt.get(
                    "reasoningEffort"
                ),
                "classification": attempt.get(
                    "classification"
                ),
                "returnCode": attempt.get("returnCode"),
                "durationSeconds": attempt.get(
                    "durationSeconds"
                ),
            }
        )

    role = value.get("role")
    agent = (
        selection_object.get(role)
        if isinstance(role, str)
        else None
    )
    agent_object = agent if isinstance(agent, dict) else {}

    return {
        "metadataName": resolved.name,
        "metadataSha256": sha256_file(resolved),
        "status": value.get("status"),
        "role": role,
        "candidateState": value.get("candidateState"),
        "promptSha256": value.get("promptSha256"),
        "tier": selection_object.get("tier"),
        "tierName": selection_object.get("tier_name"),
        "selectedProfile": agent_object.get("profile"),
        "selectedReasoningEffort": agent_object.get(
            "reasoning_effort"
        ),
        "attempts": safe_attempts,
        "escalation": value.get("escalation"),
    }


def build_bundle(
    *,
    repository: Path,
    selector: Path,
    paths: Sequence[str],
    task_type: str,
    changed_file_count: int | None,
    external_research: bool,
    previous_outcome: str,
    high_consequence: bool,
    validation_status: str,
    validation_log: Path | None,
    wrapper_metadata: Sequence[Path],
) -> dict[str, Any]:
    repository = repository.expanduser().resolve()
    selector = selector.expanduser().resolve()

    scope_facts = [
        scope_file_fact(repository, path)
        for path in paths
    ]
    lifecycle_facts = [
        fact
        for path in paths
        if (
            fact := lifecycle_fact(repository, path)
        ) is not None
    ]
    manifest = manifest_facts(repository)
    declared_files = manifest.get("declaredFiles", [])
    declared_file_set = (
        set(declared_files)
        if isinstance(declared_files, list)
        else set()
    )

    for fact in scope_facts:
        fact["declaredInManifest"] = (
            fact["path"] in declared_file_set
        )

    bundle: dict[str, Any] = {
        "version": 1,
        "repository": repository_facts(repository),
        "scope": {
            "paths": list(paths),
            "files": scope_facts,
        },
        "routing": routing_facts(
            selector,
            paths,
            task_type=task_type,
            changed_file_count=changed_file_count,
            external_research=external_research,
            previous_outcome=previous_outcome,
            high_consequence=high_consequence,
        ),
        "validation": validation_facts(
            validation_status,
            validation_log,
        ),
        "manifest": manifest,
        "lifecycle": lifecycle_facts,
        "graph": graph_facts(repository, paths),
        "codexExecutions": [
            wrapper_metadata_fact(path)
            for path in wrapper_metadata
        ],
        "privacy": {
            "fileContentsIncluded": False,
            "promptContentsIncluded": False,
            "stdoutContentsIncluded": False,
            "stderrContentsIncluded": False,
            "environmentIncluded": False,
            "credentialsIncluded": False,
        },
    }

    bundle["bundleSha256"] = sha256_bytes(
        canonical_json_bytes(bundle)
    )
    return bundle


def render_markdown(bundle: Mapping[str, Any]) -> str:
    repository = bundle["repository"]
    scope = bundle["scope"]
    routing = bundle["routing"]
    validation = bundle["validation"]
    manifest = bundle["manifest"]
    graph = bundle["graph"]

    lines = [
        "# RKM Compact Evidence Bundle",
        "",
        "## Repository",
        "",
        f"- Branch: `{repository['branch']}`",
        f"- HEAD: `{repository['head']}`",
        f"- Upstream: `{repository['upstream']}`",
        f"- Local main: `{repository['localMain']}`",
        f"- Origin main: `{repository['originMain']}`",
        f"- Worktree clean: `{str(repository['clean']).lower()}`",
        "",
        "## Scope",
        "",
    ]

    files = scope["files"]
    if files:
        for fact in files:
            digest = fact.get("sha256", "not-applicable")
            lines.append(
                f"- `{fact['path']}`: "
                f"exists={str(fact['exists']).lower()}, "
                f"tracked={str(fact['tracked']).lower()}, "
                f"sha256=`{digest}`, "
                "manifest="
                f"{str(fact['declaredInManifest']).lower()}"
            )
    else:
        lines.append("- No explicit paths.")

    creator = routing.get("creator", {})
    reviewer = routing.get("reviewer", {})
    lines.extend(
        (
            "",
            "## Routing",
            "",
            f"- Tier: `{routing.get('tier')}` "
            f"(`{routing.get('tier_name')}`)",
            f"- Creator profile: `{creator.get('profile')}`",
            (
                "- Creator reasoning: "
                f"`{creator.get('reasoning_effort')}`"
            ),
            f"- Reviewer profile: `{reviewer.get('profile')}`",
            (
                "- Reviewer reasoning: "
                f"`{reviewer.get('reasoning_effort')}`"
            ),
            "",
            "## Validation",
            "",
            (
                "- Reported status: "
                f"`{validation.get('reportedStatus')}`"
            ),
            (
                "- Validation log digest: "
                f"`{validation.get('logSha256', 'not-provided')}`"
            ),
            "",
            "## Manifest And Lifecycle",
            "",
            (
                "- Manifest declared files: "
                f"`{manifest.get('declaredFileCount', 'unknown')}`"
            ),
        )
    )

    lifecycle = bundle["lifecycle"]
    if lifecycle:
        for fact in lifecycle:
            lines.append(
                f"- `{fact['path']}`: "
                f"id=`{fact.get('id')}`, "
                f"type=`{fact.get('entityType')}`, "
                f"status=`{fact.get('status')}`, "
                f"review=`{fact.get('reviewState')}`"
            )
    else:
        lines.append("- No lifecycle-bearing scoped data records.")

    nodes = graph["nodes"]
    edges = graph["edges"]
    lines.extend(
        (
            "",
            "## Graph Export",
            "",
            f"- Nodes: `{nodes.get('count', 'unavailable')}`",
            f"- Edges: `{edges.get('count', 'unavailable')}`",
            (
                "- Scoped node IDs: "
                f"`{', '.join(graph['scope']['nodeIds']) or 'none'}`"
            ),
            (
                "- Scoped edge IDs: "
                f"`{', '.join(graph['scope']['edgeIds']) or 'none'}`"
            ),
            "",
            "## Integrity",
            "",
            f"- Bundle SHA-256: `{bundle['bundleSha256']}`",
            "- Raw file, prompt, stdout, stderr, environment, and credential contents are excluded.",
        )
    )
    return "\n".join(lines) + "\n"


def write_bundle(
    output_directory: Path,
    bundle: Mapping[str, Any],
) -> tuple[Path, Path]:
    output_directory = output_directory.expanduser().resolve()
    output_directory.mkdir(parents=True, exist_ok=True)

    json_path = output_directory / "evidence-bundle.json"
    markdown_path = output_directory / "evidence-bundle.md"

    atomic_write(
        json_path,
        json.dumps(
            bundle,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    atomic_write(markdown_path, render_markdown(bundle))
    return json_path, markdown_path


def write_fake_selector(path: Path) -> None:
    content = """#!/usr/bin/env python3
import json

print(json.dumps({
    "version": 1,
    "tier": 3,
    "tier_name": "engineering",
    "creator": {
        "profile": "rkm-engineering",
        "reasoning_effort": "medium"
    },
    "reviewer": {
        "profile": "rkm-engineering",
        "reasoning_effort": "high"
    },
    "escalation": {
        "available": True,
        "automatic": True,
        "target_tier": 4
    }
}))
"""
    path.write_text(content, encoding="utf-8", newline="\n")
    path.chmod(0o755)


def run_self_test() -> None:
    with tempfile.TemporaryDirectory(
        prefix="rkm-evidence-bundle-"
    ) as temporary_directory:
        root = Path(temporary_directory)
        repository = root / "repository"
        repository.mkdir()

        subprocess.run(
            ["git", "init", "-q", str(repository)],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "config",
                "user.email",
                "self-test@example.invalid",
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "config",
                "user.name",
                "RKM Self Test",
            ],
            check=True,
        )

        record_path = (
            repository / "data/vector-databases/sample.json"
        )
        record_path.parent.mkdir(parents=True)
        record_path.write_text(
            json.dumps(
                {
                    "identity": {
                        "id": "VECTOR-DATABASE-TEST",
                        "slug": "sample",
                        "entityType": "VectorDatabase",
                        "version": "1.0.0",
                    },
                    "metadata": {
                        "status": "Draft",
                        "reviewState": "Not Reviewed",
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        manifest_path = repository / DATA_MANIFEST
        manifest_path.write_text(
            json.dumps(
                {
                    "data": [
                        {
                            "file": (
                                "data/vector-databases/sample.json"
                            ),
                            "schema": (
                                "schema/vector-database.schema.json"
                            ),
                        }
                    ]
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        nodes_path = repository / DATA_GRAPH_NODES
        nodes_path.parent.mkdir(parents=True)
        nodes_path.write_text(
            json.dumps(
                [
                    {
                        "id": "VECTOR-DATABASE-TEST",
                        "type": "VectorDatabase",
                        "sourceDataFile": (
                            "data/vector-databases/sample.json"
                        ),
                    }
                ],
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        edges_path = repository / DATA_GRAPH_EDGES
        edges_path.write_text(
            json.dumps(
                [
                    {
                        "id": "EDGE-TEST",
                        "predicate": "VALIDATED_BY_SCHEMA",
                        "sourceId": "VECTOR-DATABASE-TEST",
                        "targetId": "SCHEMA-TEST",
                        "sourceDataFile": (
                            "data/vector-databases/sample.json"
                        ),
                    }
                ],
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        subprocess.run(
            ["git", "-C", str(repository), "add", "."],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "commit",
                "-q",
                "-m",
                "Create evidence fixture",
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "branch",
                "main",
            ],
            check=True,
        )

        selector = root / "fake-selector.py"
        write_fake_selector(selector)

        validation_log = root / "validation.log"
        validation_log.write_text(
            "RKM validation passed. Total elapsed: 1s\n",
            encoding="utf-8",
            newline="\n",
        )

        metadata_path = root / "metadata.json"
        metadata_path.write_text(
            json.dumps(
                {
                    "status": "SUCCESS",
                    "role": "creator",
                    "candidateState": "changed",
                    "promptSha256": "abc123",
                    "selection": {
                        "tier": 3,
                        "tier_name": "engineering",
                        "creator": {
                            "profile": "rkm-engineering",
                            "reasoning_effort": "medium",
                        },
                    },
                    "attempts": [
                        {
                            "attempt": 1,
                            "profile": "rkm-engineering",
                            "reasoningEffort": "medium",
                            "classification": "success",
                            "returnCode": 0,
                            "durationSeconds": 0.1,
                        }
                    ],
                    "escalation": {
                        "performed": False,
                        "reason": None,
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        arguments = {
            "repository": repository,
            "selector": selector,
            "paths": [
                "data/vector-databases/sample.json"
            ],
            "task_type": "auto",
            "changed_file_count": None,
            "external_research": False,
            "previous_outcome": "none",
            "high_consequence": False,
            "validation_status": "pass",
            "validation_log": validation_log,
            "wrapper_metadata": [metadata_path],
        }

        first = build_bundle(**arguments)
        second = build_bundle(**arguments)

        assert canonical_json_bytes(first) == canonical_json_bytes(
            second
        )
        assert first["manifest"]["declaredFileCount"] == 1
        assert first["lifecycle"][0]["status"] == "Draft"
        assert (
            first["lifecycle"][0]["reviewState"]
            == "Not Reviewed"
        )
        assert first["graph"]["nodes"]["count"] == 1
        assert first["graph"]["edges"]["count"] == 1
        assert first["routing"]["tier"] == 3
        assert first["validation"]["observedStatus"] == "pass"
        assert first["codexExecutions"][0]["status"] == "SUCCESS"
        assert first["privacy"]["promptContentsIncluded"] is False

        output_directory = root / "output"
        json_path, markdown_path = write_bundle(
            output_directory,
            first,
        )
        assert json_path.is_file()
        assert markdown_path.is_file()
        assert (
            load_json(json_path)["bundleSha256"]
            == first["bundleSha256"]
        )
        assert "RKM Compact Evidence Bundle" in (
            markdown_path.read_text(encoding="utf-8")
        )

    print("RKM evidence bundle self-test passed.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Default: current directory.",
    )
    parser.add_argument(
        "--selector",
        type=Path,
        default=(
            Path(__file__).resolve().parent
            / "rkm-select-execution-profile.py"
        ),
        help="Execution-profile selector path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory receiving the JSON and Markdown bundle.",
    )
    parser.add_argument(
        "--paths",
        action="append",
        help="Authorized repository paths. May be repeated.",
    )
    parser.add_argument(
        "--task-type",
        choices=(
            "auto",
            "deterministic-check",
            "mechanical",
            "documentation",
            "data-record",
            "governance",
            "code",
            "validation",
            "recovery",
            "automation",
            "research",
            "architecture",
            "schema",
            "ontology",
            "release",
            "integration",
            "strategic",
        ),
        default="auto",
    )
    parser.add_argument("--changed-file-count", type=int)
    parser.add_argument(
        "--external-research",
        action="store_true",
    )
    parser.add_argument(
        "--previous-outcome",
        choices=(
            "none",
            "invalid",
            "validation-failure",
            "revise",
            "stop",
        ),
        default="none",
    )
    parser.add_argument(
        "--high-consequence",
        action="store_true",
    )
    parser.add_argument(
        "--validation-status",
        choices=("not-run", "pass", "fail"),
        default="not-run",
    )
    parser.add_argument(
        "--validation-log",
        type=Path,
    )
    parser.add_argument(
        "--wrapper-metadata",
        action="append",
        type=Path,
        help="Optional rkm-codex-exec metadata JSON. May be repeated.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
    )
    return parser


def validate_arguments(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> None:
    if args.self_test:
        return
    if args.output_dir is None:
        parser.error("--output-dir is required")
    if (
        args.changed_file_count is not None
        and args.changed_file_count < 0
    ):
        parser.error("--changed-file-count must be non-negative")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_arguments(parser, args)

    if args.self_test:
        run_self_test()
        return 0

    try:
        paths = parse_paths(args.paths)
        bundle = build_bundle(
            repository=args.repository,
            selector=args.selector,
            paths=paths,
            task_type=args.task_type,
            changed_file_count=args.changed_file_count,
            external_research=args.external_research,
            previous_outcome=args.previous_outcome,
            high_consequence=args.high_consequence,
            validation_status=args.validation_status,
            validation_log=args.validation_log,
            wrapper_metadata=args.wrapper_metadata or (),
        )
        json_path, markdown_path = write_bundle(
            args.output_dir,
            bundle,
        )
    except (
        FileNotFoundError,
        json.JSONDecodeError,
        RuntimeError,
        ValueError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"EVIDENCE_BUNDLE_JSON={json_path}")
    print(f"EVIDENCE_BUNDLE_MARKDOWN={markdown_path}")
    print(f"EVIDENCE_BUNDLE_SHA256={bundle['bundleSha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
