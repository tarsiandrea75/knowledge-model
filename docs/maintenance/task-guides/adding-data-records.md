# Adding Data Records

## Purpose

Add records for an entity type that is already supported by RKM data validation and graph export expectations.

## When to Use

Use this guide when adding files under an existing `data/**` record set.

## Required Readings

- `AGENTS.md`
- `data/AGENTS.md`
- The schema for the entity type being populated.
- `data/manifest.json`

## Required Checks

- Validate each record against its schema.
- Update `data/manifest.json` for new records or record sets.
- Check whether relationships, relationship support, claims, evidence, or references are needed.
- Regenerate or update data graph export artifacts under `examples/data-graph-export/` when the added records affect exported nodes or edges.
- Include `data/manifest.json` and affected `examples/data-graph-export/*.nodes.json` or `examples/data-graph-export/*.edges.json` files in the explicit allowed file list for validated Codex commits when they are expected to change.
- Treat manifest and data graph export updates as expected side effects of data-record work, especially when validation or graph export validation changes node or edge counts.
- Run `make data-graph-export`.
- Run `make data-graph-export-validate`.
- Run `make validate`.

## Common Failure Modes

- Adding a data file but not adding it to the manifest.
- Adding records that change graph output but leaving stale data graph export artifacts.
- Reusing an ID or creating an ID that does not match naming rules.
- Adding prose evidence instead of structured claims, evidence, references, and support.
- Expecting graph edges to be inferred from entity text.

## Done Criteria

- Records are schema-valid and manifest-declared.
- Semantic validation accepts the records.
- Relationship, manifest, and graph export implications were handled or explicitly reported as not required.
- `make validate` passes or unrelated pre-existing failures are reported.
