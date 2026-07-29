# Codex Execution Telemetry and Response Format

## Purpose

This document defines the durable reporting format for Codex work on RKM and
the RAG recommendation exchange boundary. It makes task progress, subtask
timing, validation evidence, and token-usage disclosure easy to scan without
recording prompts, document contents, credentials, or other sensitive data.

The protocol is observational. It does not change canonical RKM data, schemas,
registries, graph exports, runtime behavior, sandbox boundaries, or Git
permissions.

## Human-readable report

Every bounded task should use this structure at meaningful milestones:

```text
╭─ 🔷 TASK OPS-002 ─────────────────────────────────────
│ ▶ Start: 2026-07-29T14:10:00Z
│ ⏹ End:   2026-07-29T14:22:34Z
│ ⏱ Elapsed: 00:12:34
│ ▸ Subtasks: 3 completed
│ ◉ Validation: PASS
│ ◌ Token usage: unavailable (platform metric not exposed)
╰─ 🟢 Status: DONE ──────────────────────────────────────
```

Subtasks should use the same fields in compact form:

```text
  🔷 SUBTASK 2.1 | schema validation | 00:01:18 | 🟢 SUCCESS
```

Use UTC timestamps in ISO 8601 format. Report elapsed time as `HH:MM:SS` and
retain millisecond precision in machine-readable events when available.

## Status color contract

The presentation layer uses these semantic colors:

| Semantic value | Terminal color | Text fallback |
| --- | --- | --- |
| `TASK N` and task identifiers | cyan (`36`) | `🔷 TASK N` |
| success: `DONE`, `COMPLETED`, `SUCCESS`, `PASS` | green (`32`) | `🟢` |
| failure: `FAILED`, `ERROR`, `STOPPED` | red (`31`) | `🔴` |
| all other or unresolved states, including `ACTIVE`, `RUNNING`, `PENDING`, `BLOCKED` | yellow (`33`) | `🟡` |

ANSI escape sequences may be used in terminal output only when the output
destination supports them. Markdown, CI summaries, and plain logs must use the
text fallback so that the meaning remains visible without color rendering.

## Token-usage disclosure

Never invent token counts. Report the actual platform metric when it is exposed;
otherwise use:

```text
Token usage: unavailable (platform metric not exposed)
```

If a platform exposes counts, report `input`, `output`, and `total` tokens and
identify the source. Estimates must be labelled `estimated` and must not be
presented as measured usage. Tool output size and elapsed time are not model
token counts.

## Machine-readable event

For durable event logs, use one JSON object per line and keep the event outside
the repository unless it is an intentional reviewed artifact:

```json
{"event":"task_end","taskId":"OPS-002","startedAt":"2026-07-29T14:10:00Z","finishedAt":"2026-07-29T14:22:34Z","elapsedMs":754000,"status":"DONE","validation":"PASS","tokenUsage":{"status":"unavailable","source":"platform"}}
```

Required fields are `event`, `taskId`, `startedAt`, `status`, and
`tokenUsage.status`. Completed events should also include `finishedAt`,
`elapsedMs`, and `validation`. Subtask events add `subtaskId`.

## Persistence and privacy

The response format is part of repository operating guidance and applies to
future Codex sessions that read `AGENTS.md`. Runtime telemetry belongs in
machine-local or `/tmp` output unless a task explicitly requires a reviewed
repository artifact. Do not persist credentials, tokens, prompts, document
contents, provider responses, or unrestricted environment data.
