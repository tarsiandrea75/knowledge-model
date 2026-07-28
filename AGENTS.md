# RAG Knowledge Model Agent Instructions

RAG Knowledge Model (RKM) is a structured, extensible, machine-readable and human-readable knowledge model of the Retrieval-Augmented Generation ecosystem. It is a domain model, ontology, and knowledge graph foundation for describing RAG entities, relationships, claims, evidence, references, and structured knowledge.

## Repository Constitution

These invariants apply to all repository work:

- Use the canonical project names: RAG Knowledge Model and RKM.
- Do not use deprecated names such as RAG Knowledge Base, RAG-KB, or ragkb.
- Use English for repository content unless a file intentionally targets another language.
- Use Markdown for documentation and JSON Schema Draft 2020-12 for schemas.
- Use lowercase kebab-case for file names and uppercase snake case for relationship types.
- Treat entities, relationships, evidence, claims, references, and metadata as first-class concepts.
- Prefer structured knowledge, stable identifiers, reusable definitions, registries, and explicit relationships over prose-only modeling.
- Preserve the existing domain model, entity model, relationship model, evidence model, metadata model, ontology, naming conventions, and versioning rules.
- Keep content directly usable. Do not add incomplete sections, filler content, unfinished-work markers, or invalid examples.
- Do not commit changes unless the user explicitly requests a commit.

## Mandatory Execution Protocol

Unless the user explicitly instructs otherwise:

1. Create or modify exactly one project file per run.
2. Do not create batches of files.
3. Do not create IDE configuration files.
4. Do not create temporary review files.
5. Do not modify existing files unless the requested task requires it.
6. After creating or modifying the single allowed file, run `bash scripts/validate-rkm.sh`.
7. If validation fails, fix failures only in the file you touched when possible.
8. If validation fails because of pre-existing issues in other files, report those failures without modifying additional files.
9. Report which file was created or modified.
10. Report the validation command that was run and its result.
11. Report the final `git status --short` output.
12. Do not commit changes.
13. Stop immediately after completing the single requested file and validation report.
14. If the next natural step would require additional files, describe it instead of creating it.

## Distributed Agent Rule Routing

Root `AGENTS.md` is the repository constitution and routing layer. It must stay concise and must not become the full operational manual. Detailed rules belong in the local `AGENTS.md` file closest to the affected area or in a task guide under `docs/maintenance/task-guides/`.

Distributed rule routing is validated by `make agent-routing-validate` and by the standard `make validate` pipeline. The task guide index is `docs/maintenance/task-guides/README.md`.

Governance rule enforcement levels are tracked in `docs/maintenance/rule-coverage-report.md`.

| Work type | Required routing |
| --- | --- |
| Tasks touching `data/**` | Read `data/AGENTS.md` and the relevant data task guide. |
| Tasks touching `schema/**` | Read `schema/AGENTS.md` and either `docs/maintenance/task-guides/adding-schema-contract.md` or `docs/maintenance/task-guides/refactoring-schema-definition.md`. |
| Tasks touching `registries/**` | Read `registries/AGENTS.md`. |
| Tasks touching `scripts/**` | Read `scripts/AGENTS.md` and the relevant validation or graph export task guide. |
| Tasks touching `docs/architecture/**` | Read `docs/architecture/AGENTS.md` and `docs/maintenance/task-guides/writing-architecture-doc.md`. |
| Tasks touching `examples/**` | Read `examples/AGENTS.md` and `docs/maintenance/task-guides/updating-graph-export.md` when graph exports are involved. |
| Unattended automation | Read `docs/maintenance/automation-guardrails.md` and `docs/maintenance/task-guides/unattended-autopilot.md`. |
| Recovery from failed newly added files | Read `docs/maintenance/task-guides/recovering-failed-new-file.md`. |

## Reviewer Protocol

When the user asks Codex to review the current RKM git diff, Codex acts only as a reviewer.

Reviewer rules:

1. Do not create, modify, delete, format, or normalize files.
2. Review only the current git diff.
3. Do not review unrelated repository content unless it appears in the current git diff.
4. Do not commit changes.
5. Return exactly one verdict: `ACCEPT`, `REVISE`, or `STOP`.

Use `ACCEPT` when the current git diff is coherent with RKM architecture, follows repository rules, passes required validation or has only non-blocking issues, and is ready to commit.

Use `REVISE` when the current git diff is directionally correct but needs specific fixes before commit.

Use `STOP` when the current git diff should not be repaired as-is, such as changes outside scope, unrelated file batches, destructive changes, generated clutter, severe architectural drift, or validation failures that indicate restart is safer.

Reviewer output must include:

- verdict
- touched files in the current git diff
- reasons for the verdict
- required fixes when the verdict is `REVISE` or `STOP`
- whether commit is recommended
- final `git status --short` output

## Hard Rules

- `git status --short` must be clean before push, autopilot, or handoff.
- Runtime logs, away-run logs, scratch files, and automation transcripts must be written outside the repository. Prefer `/tmp/rkm-runs`.
- Do not create `.rkm-runs/` inside the repository.
- Do not add `schema/definitions/<name>.schema.json` when `schema/<name>.schema.json` already exists unless the same commit performs an atomic refactor and explains the contract relationship.
- Schema, registry, validator, exporter, Makefile, release-process, graph-contract, and migration changes require explicit `codex-commit` prompts.
- Architecture examples must be fully real or clearly abstract. Do not mix placeholder IDs with concrete repository paths.
- Unattended autopilot should use repeated `make autopilot N=1` rounds with validation, safe push, and cockpit summary after each round.

## Validation Standard

`make validate` is the standard validation entry point for normal repository work unless the current task explicitly requires a narrower command. Validation failures must be fixed before work is reported as ready, except when the failure is clearly pre-existing and unrelated to the touched files.

## Hosted fast-gate verification

After an authorized push, the root agent must verify the GitHub Actions
workflow for the exact current commit autonomously.

Use only this user-managed, read-only launcher:

```bash
"$HOME/bin/with-fast-gate-token" gh run list \
  --repo tarsiandrea75/knowledge-model \
  --workflow "Fast gate" \
  --commit "$(git rev-parse HEAD)" \
  --limit 1 \
  --json databaseId,workflowName,headSha,status,conclusion,url
```

Accept the hosted gate only when the returned run has:

- `headSha` exactly equal to `git rev-parse HEAD`;
- `workflowName` equal to `Fast gate`;
- `status` equal to `completed`;
- `conclusion` equal to `success`.

If the run is pending, query it again. Do not ask the user to inspect GitHub
manually when this launcher is available.

Do not access credential material directly. Never print, inspect, disclose,
modify, or copy the launcher, its token file, `GH_TOKEN`, or related secrets.
Invoke the launcher only through its documented command.
