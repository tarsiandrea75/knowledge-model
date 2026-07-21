#!/usr/bin/env python3
"""Execute one adaptively routed Codex call for an RKM task."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


EXIT_SUCCESS = 0
EXIT_SELECTION_FAILED = 20
EXIT_PROMPT_INVALID = 21
EXIT_PROFILE_UNAVAILABLE = 22
EXIT_QUOTA_EXHAUSTED = 23
EXIT_AUTHENTICATION_FAILED = 24
EXIT_CONFIGURATION_FAILED = 25
EXIT_EXECUTION_FAILED = 26
EXIT_CODEX_NOT_FOUND = 27

ROLE_KEYS = {
    "creator": "creator",
    "reviewer": "reviewer",
}

DEFAULT_SANDBOX = {
    "creator": "workspace-write",
    "reviewer": "read-only",
}

TARGET_TIER_TASK_TYPE = {
    1: "mechanical",
    2: "documentation",
    3: "code",
    4: "strategic",
}

STOP_CLASSIFICATIONS = {
    "quota_exhausted",
    "authentication_failed",
    "configuration_failed",
    "profile_unavailable",
    "codex_not_found",
}

QUOTA_PATTERNS = (
    "usage limit",
    "purchase more credits",
    "insufficient_quota",
    "quota exceeded",
    "try again at",
)

AUTHENTICATION_PATTERNS = (
    "authentication failed",
    "not logged in",
    "login required",
    "unauthorized",
    "invalid api key",
    "invalid_api_key",
)

CONFIGURATION_PATTERNS = (
    "unknown configuration",
    "unrecognized configuration",
    "strict config",
    "invalid config",
    "failed to parse config",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_write_text(path: Path, content: str) -> None:
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


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    atomic_write_text(
        path,
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
    )


def normalized_path(raw_path: str) -> str:
    cleaned = raw_path.strip().replace("\\", "/")
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned


def parse_paths(raw_paths: Sequence[str] | None) -> list[str]:
    parsed: list[str] = []
    for raw_value in raw_paths or ():
        for token in shlex.split(raw_value.replace(",", " ")):
            path = normalized_path(token)
            if path and path not in parsed:
                parsed.append(path)
    return parsed


def git_value(repository: Path, arguments: Sequence[str]) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if completed.returncode != 0:
        return "UNKNOWN"
    value = completed.stdout.strip()
    return value or "UNKNOWN"


def repository_facts(repository: Path) -> dict[str, str]:
    return {
        "root": str(repository),
        "branch": git_value(repository, ("branch", "--show-current")),
        "head": git_value(repository, ("rev-parse", "HEAD")),
        "upstream": git_value(
            repository,
            ("rev-parse", "@{upstream}"),
        ),
        "localMain": git_value(repository, ("rev-parse", "main")),
        "originMain": git_value(
            repository,
            ("rev-parse", "origin/main"),
        ),
    }


def selector_command(
    selector_path: Path,
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
        str(selector_path),
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


def run_selector(
    selector_path: Path,
    paths: Sequence[str],
    *,
    task_type: str,
    changed_file_count: int | None,
    external_research: bool,
    previous_outcome: str,
    high_consequence: bool,
) -> dict[str, Any]:
    command = selector_command(
        selector_path,
        paths,
        task_type=task_type,
        changed_file_count=changed_file_count,
        external_research=external_research,
        previous_outcome=previous_outcome,
        high_consequence=high_consequence,
    )
    completed = subprocess.run(
        command,
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

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "execution-profile selector returned invalid JSON"
        ) from exc

    if not isinstance(payload, dict):
        raise RuntimeError(
            "execution-profile selector returned a non-object result"
        )
    return payload


def reasoning_for_tier(
    selector_path: Path,
    *,
    tier: int,
    role: str,
) -> str:
    task_type = TARGET_TIER_TASK_TYPE.get(tier)
    if task_type is None:
        raise ValueError(
            f"no automatic reasoning mapping exists for Tier {tier}"
        )

    selection = run_selector(
        selector_path,
        (),
        task_type=task_type,
        changed_file_count=1,
        external_research=False,
        previous_outcome="none",
        high_consequence=False,
    )
    agent = selection[ROLE_KEYS[role]]
    reasoning = agent.get("reasoning_effort")
    if not isinstance(reasoning, str) or not reasoning:
        raise ValueError(
            f"selector did not provide reasoning for Tier {tier} {role}"
        )
    return reasoning


def read_prompt(
    *,
    prompt_file: Path | None,
    prompt_text: str | None,
) -> str:
    if prompt_file is not None:
        if not prompt_file.is_file():
            raise ValueError(f"prompt file does not exist: {prompt_file}")
        prompt = prompt_file.read_text(encoding="utf-8")
    elif prompt_text is not None:
        prompt = prompt_text
    else:
        raise ValueError("one prompt source is required")

    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    return prompt


def profile_file(codex_home: Path, profile_name: str) -> Path:
    return codex_home / f"{profile_name}.config.toml"


def build_codex_command(
    *,
    codex_command: str,
    repository: Path,
    profile_name: str,
    reasoning_effort: str,
    sandbox: str,
    approval_policy: str,
    last_message_file: Path,
    output_schema: Path | None,
    json_events: bool,
    search: bool,
    ephemeral: bool,
    strict_config: bool,
) -> list[str]:
    command = [
        codex_command,
        "exec",
        "--profile",
        profile_name,
        "--config",
        (
            "model_reasoning_effort="
            + json.dumps(reasoning_effort)
        ),
        "--sandbox",
        sandbox,
        "--ask-for-approval",
        approval_policy,
        "--cd",
        str(repository),
        "--output-last-message",
        str(last_message_file),
    ]

    if strict_config:
        command.append("--strict-config")
    if ephemeral:
        command.append("--ephemeral")
    if search:
        command.append("--search")
    if json_events:
        command.append("--json")
    if output_schema is not None:
        command.extend(("--output-schema", str(output_schema)))

    command.append("-")
    return command


def classify_failure(
    *,
    return_code: int,
    stdout: str,
    stderr: str,
    last_message_file: Path,
    output_schema: Path | None,
) -> str:
    combined = f"{stdout}\n{stderr}".lower()

    for pattern in QUOTA_PATTERNS:
        if pattern in combined:
            return "quota_exhausted"

    for pattern in AUTHENTICATION_PATTERNS:
        if pattern in combined:
            return "authentication_failed"

    for pattern in CONFIGURATION_PATTERNS:
        if pattern in combined:
            return "configuration_failed"

    if return_code != 0:
        return "execution_failed"

    if not last_message_file.is_file():
        return "invalid_output"

    last_message = last_message_file.read_text(
        encoding="utf-8"
    )
    if not last_message.strip():
        return "invalid_output"

    if output_schema is not None:
        try:
            json.loads(last_message)
        except json.JSONDecodeError:
            return "invalid_output"

    return "success"


def run_attempt(
    *,
    attempt_number: int,
    output_directory: Path,
    codex_command: str,
    codex_home: Path,
    repository: Path,
    profile_name: str,
    reasoning_effort: str,
    sandbox: str,
    approval_policy: str,
    prompt: str,
    output_schema: Path | None,
    json_events: bool,
    search: bool,
    ephemeral: bool,
    strict_config: bool,
    environment: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    stdout_file = output_directory / (
        f"attempt-{attempt_number}.stdout.log"
    )
    stderr_file = output_directory / (
        f"attempt-{attempt_number}.stderr.log"
    )
    last_message_file = output_directory / (
        f"attempt-{attempt_number}.last-message.txt"
    )

    command = build_codex_command(
        codex_command=codex_command,
        repository=repository,
        profile_name=profile_name,
        reasoning_effort=reasoning_effort,
        sandbox=sandbox,
        approval_policy=approval_policy,
        last_message_file=last_message_file,
        output_schema=output_schema,
        json_events=json_events,
        search=search,
        ephemeral=ephemeral,
        strict_config=strict_config,
    )

    process_environment = dict(os.environ)
    if environment is not None:
        process_environment.update(environment)
    process_environment["CODEX_HOME"] = str(codex_home)

    started_at = utc_now()
    started_monotonic = time.monotonic()
    completed = subprocess.run(
        command,
        check=False,
        cwd=repository,
        env=process_environment,
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    duration_seconds = round(
        time.monotonic() - started_monotonic,
        3,
    )
    finished_at = utc_now()

    atomic_write_text(stdout_file, completed.stdout)
    atomic_write_text(stderr_file, completed.stderr)

    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)

    classification = classify_failure(
        return_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        last_message_file=last_message_file,
        output_schema=output_schema,
    )

    return {
        "attempt": attempt_number,
        "profile": profile_name,
        "reasoningEffort": reasoning_effort,
        "sandbox": sandbox,
        "approvalPolicy": approval_policy,
        "command": command,
        "startedAt": started_at,
        "finishedAt": finished_at,
        "durationSeconds": duration_seconds,
        "returnCode": completed.returncode,
        "classification": classification,
        "stdoutFile": str(stdout_file),
        "stderrFile": str(stderr_file),
        "lastMessageFile": str(last_message_file),
    }


def result_exit_code(status: str) -> int:
    return {
        "SUCCESS": EXIT_SUCCESS,
        "DRY_RUN": EXIT_SUCCESS,
        "DETERMINISTIC_ONLY": EXIT_SUCCESS,
        "NO_CHANGE_REQUIRED": EXIT_SUCCESS,
        "REVIEW_NOT_REQUIRED": EXIT_SUCCESS,
        "PROFILE_UNAVAILABLE": EXIT_PROFILE_UNAVAILABLE,
        "QUOTA_EXHAUSTED": EXIT_QUOTA_EXHAUSTED,
        "AUTHENTICATION_FAILED": EXIT_AUTHENTICATION_FAILED,
        "CONFIGURATION_FAILED": EXIT_CONFIGURATION_FAILED,
        "CODEX_NOT_FOUND": EXIT_CODEX_NOT_FOUND,
        "EXECUTION_FAILED": EXIT_EXECUTION_FAILED,
        "INVALID_OUTPUT": EXIT_EXECUTION_FAILED,
    }.get(status, EXIT_EXECUTION_FAILED)


def status_for_classification(classification: str) -> str:
    return {
        "success": "SUCCESS",
        "quota_exhausted": "QUOTA_EXHAUSTED",
        "authentication_failed": "AUTHENTICATION_FAILED",
        "configuration_failed": "CONFIGURATION_FAILED",
        "profile_unavailable": "PROFILE_UNAVAILABLE",
        "codex_not_found": "CODEX_NOT_FOUND",
        "invalid_output": "INVALID_OUTPUT",
        "execution_failed": "EXECUTION_FAILED",
    }.get(classification, "EXECUTION_FAILED")


def selected_agent(
    selection: Mapping[str, Any],
    role: str,
) -> Mapping[str, Any]:
    agent = selection.get(ROLE_KEYS[role])
    if not isinstance(agent, dict):
        raise RuntimeError(
            f"selector result lacks the {role} object"
        )
    return agent


def should_skip(
    selection: Mapping[str, Any],
    *,
    role: str,
    candidate_state: str,
) -> str | None:
    agent = selected_agent(selection, role)

    if role == "creator":
        if selection.get("deterministic_only") is True:
            return "DETERMINISTIC_ONLY"
        if agent.get("required") is False:
            return "DETERMINISTIC_ONLY"
        return None

    if (
        candidate_state == "no-change"
        and agent.get("skip_on_no_change_required") is True
    ):
        return "NO_CHANGE_REQUIRED"

    if agent.get("required_on_change") is False:
        return "REVIEW_NOT_REQUIRED"

    return None


def make_base_metadata(
    *,
    repository: Path,
    output_directory: Path,
    prompt: str,
    paths: Sequence[str],
    role: str,
    candidate_state: str,
    selection: Mapping[str, Any],
    codex_home: Path,
) -> dict[str, Any]:
    return {
        "version": 1,
        "startedAt": utc_now(),
        "finishedAt": None,
        "status": "RUNNING",
        "role": role,
        "candidateState": candidate_state,
        "paths": list(paths),
        "promptSha256": sha256_text(prompt),
        "promptCharacters": len(prompt),
        "repository": repository_facts(repository),
        "outputDirectory": str(output_directory),
        "codexHome": str(codex_home),
        "selection": selection,
        "attempts": [],
        "escalation": {
            "performed": False,
            "reason": None,
        },
    }


def finalize(
    metadata: dict[str, Any],
    *,
    status: str,
    metadata_file: Path,
) -> int:
    metadata["status"] = status
    metadata["finishedAt"] = utc_now()
    atomic_write_json(metadata_file, metadata)
    print(
        f"RKM_CODEX_EXEC_STATUS={status}",
        file=sys.stderr,
    )
    print(
        f"RKM_CODEX_EXEC_METADATA={metadata_file}",
        file=sys.stderr,
    )
    return result_exit_code(status)


def execute_workflow(args: argparse.Namespace) -> int:
    repository = args.repository.expanduser().resolve()
    selector_path = args.selector.expanduser().resolve()
    codex_home = args.codex_home.expanduser().resolve()
    paths = parse_paths(args.paths)

    prompt = read_prompt(
        prompt_file=args.prompt_file,
        prompt_text=args.prompt,
    )

    output_directory = (
        args.output_dir.expanduser().resolve()
        if args.output_dir is not None
        else (
            repository
            / ".rkm"
            / "codex-exec"
            / (
                datetime.now(timezone.utc).strftime(
                    "%Y%m%dT%H%M%SZ"
                )
                + f"-{os.getpid()}"
            )
        )
    )
    output_directory.mkdir(parents=True, exist_ok=True)

    metadata_file = (
        args.metadata_file.expanduser().resolve()
        if args.metadata_file is not None
        else output_directory / "metadata.json"
    )

    selection = run_selector(
        selector_path,
        paths,
        task_type=args.task_type,
        changed_file_count=args.changed_file_count,
        external_research=args.external_research,
        previous_outcome=args.previous_outcome,
        high_consequence=args.high_consequence,
    )

    metadata = make_base_metadata(
        repository=repository,
        output_directory=output_directory,
        prompt=prompt,
        paths=paths,
        role=args.role,
        candidate_state=args.candidate_state,
        selection=selection,
        codex_home=codex_home,
    )

    skip_status = should_skip(
        selection,
        role=args.role,
        candidate_state=args.candidate_state,
    )
    if skip_status is not None:
        return finalize(
            metadata,
            status=skip_status,
            metadata_file=metadata_file,
        )

    agent = selected_agent(selection, args.role)
    profile_name = agent.get("profile")
    reasoning_effort = agent.get("reasoning_effort")
    if not isinstance(profile_name, str) or not profile_name:
        raise RuntimeError(
            f"selector did not provide a {args.role} profile"
        )
    if not isinstance(reasoning_effort, str) or not reasoning_effort:
        raise RuntimeError(
            f"selector did not provide {args.role} reasoning"
        )

    sandbox = args.sandbox or DEFAULT_SANDBOX[args.role]
    initial_profile_file = profile_file(
        codex_home,
        profile_name,
    )

    metadata["plan"] = {
        "profile": profile_name,
        "profileFile": str(initial_profile_file),
        "profileAvailable": initial_profile_file.is_file(),
        "reasoningEffort": reasoning_effort,
        "sandbox": sandbox,
        "approvalPolicy": args.approval_policy,
        "automaticEscalationEnabled": not args.no_escalation,
    }

    if args.dry_run:
        command = build_codex_command(
            codex_command=args.codex_command,
            repository=repository,
            profile_name=profile_name,
            reasoning_effort=reasoning_effort,
            sandbox=sandbox,
            approval_policy=args.approval_policy,
            last_message_file=(
                output_directory / "attempt-1.last-message.txt"
            ),
            output_schema=args.output_schema,
            json_events=args.json_events,
            search=args.search,
            ephemeral=not args.persist_session,
            strict_config=args.strict_config,
        )
        metadata["plan"]["command"] = command
        return finalize(
            metadata,
            status="DRY_RUN",
            metadata_file=metadata_file,
        )

    if not initial_profile_file.is_file():
        metadata["failure"] = {
            "classification": "profile_unavailable",
            "detail": str(initial_profile_file),
        }
        return finalize(
            metadata,
            status="PROFILE_UNAVAILABLE",
            metadata_file=metadata_file,
        )

    resolved_codex_command = shutil.which(args.codex_command)
    if resolved_codex_command is None:
        candidate = Path(args.codex_command).expanduser()
        if candidate.is_file() and os.access(candidate, os.X_OK):
            resolved_codex_command = str(candidate.resolve())

    if resolved_codex_command is None:
        metadata["failure"] = {
            "classification": "codex_not_found",
            "detail": args.codex_command,
        }
        return finalize(
            metadata,
            status="CODEX_NOT_FOUND",
            metadata_file=metadata_file,
        )

    first_attempt = run_attempt(
        attempt_number=1,
        output_directory=output_directory,
        codex_command=resolved_codex_command,
        codex_home=codex_home,
        repository=repository,
        profile_name=profile_name,
        reasoning_effort=reasoning_effort,
        sandbox=sandbox,
        approval_policy=args.approval_policy,
        prompt=prompt,
        output_schema=args.output_schema,
        json_events=args.json_events,
        search=args.search,
        ephemeral=not args.persist_session,
        strict_config=args.strict_config,
    )
    metadata["attempts"].append(first_attempt)

    first_classification = first_attempt["classification"]
    if first_classification == "success":
        return finalize(
            metadata,
            status="SUCCESS",
            metadata_file=metadata_file,
        )

    if first_classification in STOP_CLASSIFICATIONS:
        return finalize(
            metadata,
            status=status_for_classification(
                first_classification
            ),
            metadata_file=metadata_file,
        )

    escalation = selection.get("escalation")
    can_escalate = (
        not args.no_escalation
        and isinstance(escalation, dict)
        and escalation.get("available") is True
        and escalation.get("automatic") is True
        and escalation.get(
            "requires_explicit_authorization"
        ) is False
        and escalation.get("max_escalations") == 1
    )

    if not can_escalate:
        return finalize(
            metadata,
            status=status_for_classification(
                first_classification
            ),
            metadata_file=metadata_file,
        )

    target_tier = escalation.get("target_tier")
    target_profile = escalation.get("profile")
    if not isinstance(target_tier, int):
        raise RuntimeError(
            "selector escalation lacks an integer target tier"
        )
    if not isinstance(target_profile, str) or not target_profile:
        raise RuntimeError(
            "selector escalation lacks a profile"
        )

    target_reasoning = reasoning_for_tier(
        selector_path,
        tier=target_tier,
        role=args.role,
    )
    target_profile_file = profile_file(
        codex_home,
        target_profile,
    )

    metadata["escalation"] = {
        "performed": False,
        "reason": first_classification,
        "targetTier": target_tier,
        "targetProfile": target_profile,
        "targetReasoningEffort": target_reasoning,
        "targetProfileFile": str(target_profile_file),
    }

    if not target_profile_file.is_file():
        metadata["failure"] = {
            "classification": "profile_unavailable",
            "detail": str(target_profile_file),
        }
        return finalize(
            metadata,
            status="PROFILE_UNAVAILABLE",
            metadata_file=metadata_file,
        )

    metadata["escalation"]["performed"] = True
    second_attempt = run_attempt(
        attempt_number=2,
        output_directory=output_directory,
        codex_command=resolved_codex_command,
        codex_home=codex_home,
        repository=repository,
        profile_name=target_profile,
        reasoning_effort=target_reasoning,
        sandbox=sandbox,
        approval_policy=args.approval_policy,
        prompt=prompt,
        output_schema=args.output_schema,
        json_events=args.json_events,
        search=args.search,
        ephemeral=not args.persist_session,
        strict_config=args.strict_config,
    )
    metadata["attempts"].append(second_attempt)

    return finalize(
        metadata,
        status=status_for_classification(
            second_attempt["classification"]
        ),
        metadata_file=metadata_file,
    )


def write_fake_codex(path: Path) -> None:
    content = """#!/usr/bin/env python3
import os
from pathlib import Path
import sys

arguments = sys.argv[1:]
prompt = sys.stdin.read()
mode = os.environ.get("RKM_FAKE_CODEX_MODE", "success")
capture = os.environ.get("RKM_FAKE_CODEX_CAPTURE")

if capture:
    Path(capture).write_text(
        "\\n".join(arguments) + "\\nPROMPT\\n" + prompt,
        encoding="utf-8",
    )

last_message = None
for index, value in enumerate(arguments):
    if value in {"-o", "--output-last-message"}:
        last_message = Path(arguments[index + 1])
        break

profile = None
for index, value in enumerate(arguments):
    if value in {"-p", "--profile"}:
        profile = arguments[index + 1]
        break

if mode == "quota":
    print(
        "ERROR: You've hit your usage limit. Purchase more credits.",
        file=sys.stderr,
    )
    raise SystemExit(1)

if mode == "authentication":
    print("ERROR: login required", file=sys.stderr)
    raise SystemExit(1)

if mode == "escalate" and profile == "rkm-bounded":
    print("temporary execution failure", file=sys.stderr)
    raise SystemExit(1)

if last_message is not None:
    last_message.parent.mkdir(parents=True, exist_ok=True)
    last_message.write_text("FAKE SUCCESS\\n", encoding="utf-8")

print("fake codex success")
"""

    path.write_text(content, encoding="utf-8", newline="\n")
    path.chmod(0o755)


def make_test_namespace(
    *,
    repository: Path,
    selector: Path,
    codex_home: Path,
    codex_command: str,
    output_dir: Path,
    prompt_file: Path,
    no_escalation: bool = False,
) -> argparse.Namespace:
    return argparse.Namespace(
        repository=repository,
        selector=selector,
        codex_home=codex_home,
        codex_command=codex_command,
        output_dir=output_dir,
        metadata_file=None,
        role="creator",
        candidate_state="changed",
        paths=["QUICKSTART.md"],
        task_type="auto",
        changed_file_count=None,
        external_research=False,
        previous_outcome="none",
        high_consequence=False,
        prompt_file=prompt_file,
        prompt=None,
        sandbox=None,
        approval_policy="never",
        output_schema=None,
        json_events=False,
        search=False,
        persist_session=False,
        strict_config=False,
        no_escalation=no_escalation,
        dry_run=False,
    )


def run_self_test() -> None:
    repository = Path(__file__).resolve().parent.parent
    selector = (
        repository / "scripts/rkm-select-execution-profile.py"
    )
    assert selector.is_file()

    assert classify_failure(
        return_code=1,
        stdout="",
        stderr="usage limit reached",
        last_message_file=Path("/missing"),
        output_schema=None,
    ) == "quota_exhausted"

    assert classify_failure(
        return_code=1,
        stdout="",
        stderr="login required",
        last_message_file=Path("/missing"),
        output_schema=None,
    ) == "authentication_failed"

    with tempfile.TemporaryDirectory(
        prefix="rkm-codex-wrapper-"
    ) as temporary_directory:
        root = Path(temporary_directory)
        codex_home = root / "codex-home"
        codex_home.mkdir()
        for profile_name in (
            "rkm-bounded",
            "rkm-engineering",
        ):
            (
                codex_home / f"{profile_name}.config.toml"
            ).write_text(
                'model = "fake-model"\n'
                'model_reasoning_effort = "low"\n',
                encoding="utf-8",
                newline="\n",
            )

        fake_codex = root / "fake-codex.py"
        write_fake_codex(fake_codex)

        prompt_file = root / "prompt.md"
        prompt_file.write_text(
            "Perform one bounded fake task.\n",
            encoding="utf-8",
            newline="\n",
        )

        capture_file = root / "capture.txt"
        success_args = make_test_namespace(
            repository=repository,
            selector=selector,
            codex_home=codex_home,
            codex_command=str(fake_codex),
            output_dir=root / "success",
            prompt_file=prompt_file,
        )

        previous_mode = os.environ.get("RKM_FAKE_CODEX_MODE")
        previous_capture = os.environ.get("RKM_FAKE_CODEX_CAPTURE")
        try:
            os.environ["RKM_FAKE_CODEX_MODE"] = "success"
            os.environ["RKM_FAKE_CODEX_CAPTURE"] = str(
                capture_file
            )
            assert execute_workflow(success_args) == EXIT_SUCCESS

            success_metadata = json.loads(
                (
                    root / "success/metadata.json"
                ).read_text(encoding="utf-8")
            )
            assert success_metadata["status"] == "SUCCESS"
            assert len(success_metadata["attempts"]) == 1
            assert (
                success_metadata["attempts"][0]["profile"]
                == "rkm-bounded"
            )

            captured = capture_file.read_text(encoding="utf-8")
            assert captured.endswith(
                "PROMPT\nPerform one bounded fake task.\n"
            )
            assert "\n-\nPROMPT\n" in captured
            assert (
                'model_reasoning_effort="low"'
                in captured
            )

            os.environ["RKM_FAKE_CODEX_MODE"] = "quota"
            quota_args = make_test_namespace(
                repository=repository,
                selector=selector,
                codex_home=codex_home,
                codex_command=str(fake_codex),
                output_dir=root / "quota",
                prompt_file=prompt_file,
            )
            assert (
                execute_workflow(quota_args)
                == EXIT_QUOTA_EXHAUSTED
            )
            quota_metadata = json.loads(
                (
                    root / "quota/metadata.json"
                ).read_text(encoding="utf-8")
            )
            assert quota_metadata["status"] == "QUOTA_EXHAUSTED"
            assert len(quota_metadata["attempts"]) == 1

            os.environ["RKM_FAKE_CODEX_MODE"] = "escalate"
            escalation_args = make_test_namespace(
                repository=repository,
                selector=selector,
                codex_home=codex_home,
                codex_command=str(fake_codex),
                output_dir=root / "escalation",
                prompt_file=prompt_file,
            )
            assert execute_workflow(escalation_args) == EXIT_SUCCESS
            escalation_metadata = json.loads(
                (
                    root / "escalation/metadata.json"
                ).read_text(encoding="utf-8")
            )
            assert escalation_metadata["status"] == "SUCCESS"
            assert len(escalation_metadata["attempts"]) == 2
            assert (
                escalation_metadata["attempts"][1]["profile"]
                == "rkm-engineering"
            )
            assert (
                escalation_metadata["attempts"][1][
                    "reasoningEffort"
                ]
                == "medium"
            )

            missing_profile_args = make_test_namespace(
                repository=repository,
                selector=selector,
                codex_home=root / "missing-home",
                codex_command=str(fake_codex),
                output_dir=root / "missing-profile",
                prompt_file=prompt_file,
            )
            assert (
                execute_workflow(missing_profile_args)
                == EXIT_PROFILE_UNAVAILABLE
            )
        finally:
            if previous_mode is None:
                os.environ.pop("RKM_FAKE_CODEX_MODE", None)
            else:
                os.environ["RKM_FAKE_CODEX_MODE"] = previous_mode

            if previous_capture is None:
                os.environ.pop("RKM_FAKE_CODEX_CAPTURE", None)
            else:
                os.environ[
                    "RKM_FAKE_CODEX_CAPTURE"
                ] = previous_capture

    print("RKM Codex execution wrapper self-test passed.")


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
        "--codex-home",
        type=Path,
        default=Path(
            os.environ.get(
                "CODEX_HOME",
                str(Path.home() / ".codex"),
            )
        ),
        help="Codex configuration home.",
    )
    parser.add_argument(
        "--codex-command",
        default="codex",
        help="Codex executable name or path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Run artifact directory.",
    )
    parser.add_argument(
        "--metadata-file",
        type=Path,
        help="Metadata JSON path. Default: output-dir/metadata.json.",
    )
    parser.add_argument(
        "--role",
        choices=("creator", "reviewer"),
    )
    parser.add_argument(
        "--candidate-state",
        choices=("changed", "no-change"),
        default="changed",
    )
    parser.add_argument(
        "--paths",
        action="append",
        help="Authorized paths. May be repeated.",
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

    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument("--prompt-file", type=Path)
    prompt_group.add_argument("--prompt")

    parser.add_argument(
        "--sandbox",
        choices=(
            "read-only",
            "workspace-write",
            "danger-full-access",
        ),
        help="Default: workspace-write for Creator, read-only for Reviewer.",
    )
    parser.add_argument(
        "--approval-policy",
        choices=("untrusted", "on-request", "never"),
        default="never",
    )
    parser.add_argument("--output-schema", type=Path)
    parser.add_argument("--json-events", action="store_true")
    parser.add_argument("--search", action="store_true")
    parser.add_argument("--persist-session", action="store_true")
    parser.add_argument("--strict-config", action="store_true")
    parser.add_argument("--no-escalation", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser


def validate_arguments(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> None:
    if args.self_test:
        return

    if args.role is None:
        parser.error("--role is required unless --self-test is used")

    if args.prompt_file is None and args.prompt is None:
        parser.error("--prompt-file or --prompt is required")

    if args.changed_file_count is not None:
        if args.changed_file_count < 0:
            parser.error("--changed-file-count must be non-negative")

    if args.output_schema is not None:
        args.output_schema = args.output_schema.expanduser().resolve()
        if not args.output_schema.is_file():
            parser.error(
                f"output schema does not exist: {args.output_schema}"
            )

    if (
        args.role == "reviewer"
        and args.sandbox == "workspace-write"
    ):
        parser.error(
            "Reviewer sandbox must not be workspace-write"
        )

    if args.role == "reviewer" and args.search:
        parser.error(
            "Reviewer web search requires a separate governed workflow"
        )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_arguments(parser, args)

    if args.self_test:
        run_self_test()
        return EXIT_SUCCESS

    try:
        return execute_workflow(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_PROMPT_INVALID
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_SELECTION_FAILED


if __name__ == "__main__":
    sys.exit(main())
