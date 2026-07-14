# Adding a New Entity Type

## Purpose

Introduce data support for a new entity type as a complete package rather than isolated files.

## When to Use

Use this guide when data for an entity type does not already have full validation, manifest, export, and documentation support.

## Required Readings

- `AGENTS.md`
- `data/AGENTS.md`
- `schema/AGENTS.md` when schemas change.
- `scripts/AGENTS.md` when validation or export code changes.
- `docs/maintenance/task-guides/adding-schema-contract.md` when schema support is required.
- `docs/maintenance/task-guides/updating-graph-export.md` when export behavior changes.

## Required Checks

- Add data records.
- Update `data/manifest.json`.
- Ensure validation compatibility for the new type.
- Add graph export support when the type should appear in exports.
- Add schema provenance nodes when graph export contracts require them.
- Update docs that explain the new type.
- Add or update self-test coverage for validation and export behavior.
- Run `make validate`.

## Common Failure Modes

- Adding records before shared identity support exists.
- Adding a specialized schema with an unsupported `identity.entityType` value.
- Adding data without export support for a graph-visible type.
- Forgetting schema provenance nodes in graph export output.
- Treating validation script changes as low-risk.

## Done Criteria

- Data records, manifest entries, validation compatibility, graph export support, schema provenance nodes, docs, and self-tests are coherent.
- The entity type is represented structurally and consistently across affected contracts.
- `make validate` passes or unrelated pre-existing failures are reported.
