# Refactoring a Schema Definition

## Purpose

Extract or update reusable schema definitions without creating duplicated, independently evolving contracts.

## When to Use

Use this guide when moving shared schema structure into `schema/definitions/**` or changing a reusable definition used by first-class schemas.

## Required Readings

- `AGENTS.md`
- `schema/AGENTS.md`
- The first-class schema being refactored.
- All schemas, fixtures, data records, tests, and docs that consume the definition.

## Required Checks

- Perform reusable definition extraction atomically.
- Do not add `schema/definitions/<name>.schema.json` when `schema/<name>.schema.json` already exists unless the same commit refactors the first-class schema to compose from it.
- Same-name reusable definitions require the first-class `schema/<name>.schema.json` contract to visibly compose from `schema/definitions/<name>.schema.json`.
- Update the first-class schema in the same commit.
- Update examples, tests, validation expectations, and docs in the same commit.
- Confirm no duplicated contract remains independently authoritative.
- Run `make schema-duplicate-contracts-validate` for same-name first-class schema and reusable definition pairs.
- Run `make validate`.

## Common Failure Modes

- Leaving both a first-class schema and a definition to evolve separately.
- Passing duplicate contract validation while still changing semantics, compatibility, or migration behavior without reviewer-visible justification.
- Updating a definition without checking every schema that composes it.
- Forgetting examples or fixtures that rely on the old structure.
- Treating a reusable embedded object as a first-class entity without modeling identity and relationships.

## Done Criteria

- The reusable definition and all consumers are updated together.
- The contract relationship is clear in docs or commit context.
- Duplicate schema contract validation passes, and reviewers can still assess semantic equivalence and migration safety.
- Validation passes or unrelated pre-existing failures are reported.
