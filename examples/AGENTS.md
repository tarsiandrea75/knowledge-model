# Examples Agent Rules

These rules apply to all work under `examples/**`.

## Scope

Examples include validation fixtures, generated graph exports, and consumer-facing sample artifacts. They must remain synchronized with schemas, exporters, and source data.

## Rules

- Generated examples must remain consistent with the exporters that produce them.
- Graph export node and edge files must validate against graph export schemas.
- Graph export edges must reference endpoints that exist in the same export.
- Concrete IDs and endpoints must match actual records when examples point to repository data.
- Fixture examples must stay pedagogical and minimal; data graph exports must stay derived from validated seed data.
- Do not hand-edit generated export output unless the task is explicitly updating the generated artifact and validation confirms consistency.

## Required Task Guide

Use this guide before editing graph export examples:

- `docs/maintenance/task-guides/updating-graph-export.md`

## Required Checks

Run `make validate`. For graph export work, regenerate the relevant export before validation.
