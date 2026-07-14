# Scripts Agent Rules

These rules apply to all work under `scripts/**`.

## Scope

Scripts implement validation, export, release, recovery, automation, and repository maintenance behavior. Treat validators, exporters, release scripts, and automation scripts as high-risk.

## Rules

- Script changes require explicit prompts when they affect validators, exporters, release processes, automation, migrations, or graph contracts.
- Add or update self-test coverage for changed behavior.
- Do not silently weaken validation. Any intentional relaxation must be explicit, documented, and justified.
- Validation failures must remain actionable, with messages that identify the failing file or contract.
- Exporter changes must preserve graph export schema validation and endpoint integrity checks.
- Prefer Make targets as the public operational interface unless the task is debugging a script directly.
- Do not write runtime logs, transcripts, or scratch output inside the repository.

## Required Task Guides

Use the relevant guide before editing:

- `docs/maintenance/task-guides/updating-validation-scripts.md`
- `docs/maintenance/task-guides/updating-graph-export.md`

## Required Checks

Run `make validate`. For exporter changes, regenerate graph exports and validate generated node and edge files against the graph export schemas.
