# RKM Task Guides

## Purpose

Task guides provide operational instructions for common RKM change types. They keep root `AGENTS.md` concise while preserving detailed, task-specific rules where future agents can find them.

## When to Use

Use these guides after reading root `AGENTS.md` and any local `AGENTS.md` file that governs the files being changed.

For intended file changes, `make route-task PATHS="schema/foo.schema.json data/rag-techniques/hybrid-retrieval.json"` is the operational entry point for choosing required readings, suggested task guides, risk notes, and required checks.

For data work, `make route-task` also highlights expected side effects such as `data/manifest.json` and `examples/data-graph-export/` node and edge artifact updates.

## Routing Table

| Task type | Guide |
| --- | --- |
| Unattended automation | `unattended-autopilot.md` |
| Recovery from a failed newly added file | `recovering-failed-new-file.md` |
| Architecture documentation | `writing-architecture-doc.md` |
| Records for an existing data entity type | `adding-data-records.md` |
| Data for a new entity type | `adding-new-entity-type.md` |
| Relationship set data | `adding-relationship-set.md` |
| Relationship support data | `adding-relationship-support.md` |
| New or changed schema contract | `adding-schema-contract.md` |
| Reusable schema definition extraction | `refactoring-schema-definition.md` |
| Graph export behavior or generated export files | `updating-graph-export.md` |
| Validation script behavior | `updating-validation-scripts.md` |
| Release preparation | `preparing-release.md` |
| Distributed agent rule routing validation | `rule-routing-validation.md` |

## Required Readings

- Root `AGENTS.md` for repository invariants and routing.
- The nearest local `AGENTS.md` file for area-specific rules.
- The task guide that matches the requested work.
- `docs/maintenance/automation-guardrails.md` for automation, recovery, schema-contract, or unattended work.

## Maintenance References

- `docs/maintenance/rule-coverage-report.md` is a maintenance reference, not a task guide. Task guides may point to it when deciding whether a documented rule needs automation.
- `docs/maintenance/governance-backlog.md` is a maintenance reference for deferred governance, validation, modeling, evidence, release, and tooling work. Task guides can create or reference backlog entries when a recommended improvement is postponed.

## Required Checks

Run the validation command required by the current task. For normal repository work, use `make validate`.

## Common Failure Modes

- Reading root rules but missing local area rules.
- Editing generated examples without regenerating their source export.
- Adding schema contracts without updating examples, tests, docs, or validation.
- Adding data records without updating `data/manifest.json`.
- Adding data records without refreshing affected data graph export artifacts.
- Treating a task guide as a replacement for the local `AGENTS.md` file.

## Done Criteria

- The appropriate local rule file and task guide were read.
- The change follows repository invariants and area rules.
- Required checks passed or unrelated pre-existing failures were reported.
- `git status --short` was inspected before handoff.
