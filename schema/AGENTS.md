# Schema Agent Rules

These rules apply to all work under `schema/**`.

## Scope

Schemas define structural contracts for RKM data, fixtures, registries, and graph exports. Treat schema work as contract evolution.

## Rules

- Schema changes are structural contract changes and require explicit `codex-commit` prompts.
- Use JSON Schema Draft 2020-12 and stable `$id` values that follow RKM naming conventions.
- Compose shared definitions where appropriate instead of duplicating contract fragments.
- Do not add `schema/definitions/<name>.schema.json` when `schema/<name>.schema.json` already exists unless the same commit performs an atomic refactor and explains the contract relationship.
- Reusable definition extraction must update the first-class schema, examples, tests, validation expectations, and docs in the same commit.
- Specialized schemas must only use `identity.entityType` `const` values already supported by `schema/definitions/identity.schema.json`.
- Add shared identity support before introducing specialized schemas for new entity types.
- Do not silently loosen required fields, enum values, identifier patterns, or graph export contracts.

## Required Task Guides

Use the relevant guide before editing:

- `docs/maintenance/task-guides/adding-schema-contract.md`
- `docs/maintenance/task-guides/refactoring-schema-definition.md`

## Required Checks

Run `make validate`. Schema contract changes also require self-tests, examples, and documentation updates when the contract affects consumers.
