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
- Consider whether graph export output must change.
- Run `make validate`.

## Common Failure Modes

- Adding a data file but not adding it to the manifest.
- Reusing an ID or creating an ID that does not match naming rules.
- Adding prose evidence instead of structured claims, evidence, references, and support.
- Expecting graph edges to be inferred from entity text.

## Done Criteria

- Records are schema-valid and manifest-declared.
- Semantic validation accepts the records.
- Relationship and graph export implications were handled or explicitly reported as not required.
- `make validate` passes or unrelated pre-existing failures are reported.
