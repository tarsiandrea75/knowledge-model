# Preparing a Release

## Purpose

Prepare release artifacts and checks without modifying existing tags or weakening validation.

## When to Use

Use this guide before release packaging, release documentation, version updates, or tag preparation.

## Required Readings

- `AGENTS.md`
- `docs/maintenance/automation-guardrails.md`
- Existing release documentation.
- `CHANGELOG.md`
- Versioned schemas, examples, and docs affected by the release.

## Required Checks

- Start from a clean worktree.
- Run full validation.
- Run the release check when the release process requires it.
- Confirm changelog and release docs match the intended version and scope.
- Confirm version consistency across docs, schemas, and examples.
- Do not modify existing git tags.
- Do not retag `v0.1.0-alpha`.

## Common Failure Modes

- Updating release notes but not the changelog.
- Changing version references inconsistently.
- Treating post-alpha work on `main` as part of an already tagged alpha.
- Modifying or recreating an existing tag.

## Done Criteria

- Worktree is clean before release commands and before handoff.
- Full validation and release checks pass.
- Changelog, release docs, and version references agree.
- Existing tags remain unchanged.
