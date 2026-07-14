# Adding a Schema Contract

## Purpose

Evolve RKM structural contracts intentionally and with downstream compatibility in mind.

## When to Use

Use this guide before adding or changing schemas under `schema/**`.

## Required Readings

- `AGENTS.md`
- `schema/AGENTS.md`
- Relevant architecture documents for the concept being modeled.
- Existing schemas and definitions that may already cover the concept.

## Required Checks

- Confirm the user gave an explicit prompt for schema work.
- Validate schema syntax and JSON Schema Draft 2020-12 usage.
- Run prerequisite validation for referenced definitions and identity support.
- Run contract validation.
- Run `make schema-duplicate-contracts-validate` when schema definitions are added or renamed.
- Consider fixtures and populated data that must be added or updated.
- Update examples, docs, and self-tests when consumers are affected.
- Run `make validate`.

## Common Failure Modes

- Creating a specialized schema before identity support exists.
- Duplicating an existing first-class schema as a definition without composing the first-class schema from that same-name definition.
- Adding a contract without fixture or data consideration.
- Loosening a schema without documenting why.

## Done Criteria

- The schema contract is intentional, validated, documented, and tested.
- Related fixtures, data, examples, and docs were updated or explicitly identified as unaffected.
- `make validate` passes or unrelated pre-existing failures are reported.
