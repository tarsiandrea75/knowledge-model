# Updating Validation Scripts

## Purpose

Change validation behavior while preserving strict, actionable repository checks.

## When to Use

Use this guide when editing scripts or Make targets that validate schemas, registries, data, relationships, support sets, graph exports, documentation, or release readiness.

## Required Readings

- `AGENTS.md`
- `scripts/AGENTS.md`
- Existing validator tests or self-test patterns.
- Any schema, registry, or docs contract affected by the validation change.

## Required Checks

- Add or update self-test coverage.
- Do not weaken validation unless the prompt explicitly asks for it and the documentation explains why.
- Keep validation failures actionable, with file paths and contract names where possible.
- Preserve existing validation coverage unless the change intentionally replaces it with equivalent or stricter coverage.
- Run `make validate`.

## Common Failure Modes

- Treating a validator error as noise and suppressing it.
- Removing a check without updating docs or tests.
- Adding a check that reports vague failures.
- Changing validation behavior without considering release checks and automation.

## Done Criteria

- Self-tests cover the changed behavior.
- Failure messages remain actionable.
- Validation is not silently weakened.
- `make validate` passes or unrelated pre-existing failures are reported.
