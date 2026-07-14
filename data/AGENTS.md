# Data Agent Rules

These rules apply to all work under `data/**`.

## Scope

`data/**` contains populated RKM knowledge records, manifests, relationship sets, and relationship support sets. Treat it as validated seed knowledge, not as loose example content.

## Rules

- Every record must validate against its declared schema.
- New records or new record sets must update `data/manifest.json`.
- Data changes must remain compatible with semantic validation, including identifier uniqueness, data file references, relationship endpoints, and support links.
- New entity types must include graph export consideration before they are considered complete.
- When relationship evidence is modeled, relationship support must be represented through valid support records rather than inferred from prose.
- Do not infer domain graph edges from record names, descriptions, stages, component roles, or other fields. Declare relationships explicitly.
- Preserve stable IDs and keep entity names separate from identity.

## Required Task Guides

Use the relevant guide before editing:

- `docs/maintenance/task-guides/adding-data-records.md`
- `docs/maintenance/task-guides/adding-new-entity-type.md`
- `docs/maintenance/task-guides/adding-relationship-set.md`
- `docs/maintenance/task-guides/adding-relationship-support.md`

## Required Checks

Run `make validate` after data changes. If graph export output is expected to change, regenerate and validate the export through the documented Make targets before reporting readiness.
