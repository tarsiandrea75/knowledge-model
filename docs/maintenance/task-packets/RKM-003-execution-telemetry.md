# RKM-003: Codex Execution Telemetry and Response Format

## Status

DONE

## Objective

Define a durable, readable execution-reporting protocol for Codex work on RKM
and the RAG recommendation exchange boundary.

## Scope

- Document task and subtask start time, end time, elapsed time, validation
  results, and token-usage disclosure.
- Define semantic colors and text fallbacks for task identifiers and status.
- Record the protocol in repository guidance so future sessions discover it.

## Out of scope

- Changes to canonical RKM data, schemas, registries, graph exports, or runtime
  behavior.
- Claims of exact model-token usage when the execution platform does not expose
  that metric.
- Recording prompts, document contents, credentials, or other sensitive data.

## Acceptance criteria

- A linked operations document defines the human-readable and machine-readable
  event fields.
- `AGENTS.md` routes future sessions to the protocol.
- `TASK N` is cyan or its text fallback, success is green, failure is red, and
  intermediate or unknown status is yellow.
- Unavailable token telemetry is represented explicitly as `unavailable`.

## Required validation

Run after each changed file:

```bash
bash scripts/validate-rkm.sh
```

## Stop conditions

Stop if implementation requires unsupported platform token counters, secret
access, changes to canonical contracts, or external telemetry publication.

## Handoff

The protocol is documented in this repository and the companion RAG repository.
The repository-wide gate passes while ignoring the Git-ignored IDE directory.
The local RKM commit is ready, and no push is part of this task.
