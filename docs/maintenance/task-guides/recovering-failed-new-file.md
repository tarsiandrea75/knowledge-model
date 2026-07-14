# Recovering Failed Newly Added Files

## Purpose

Discard a newly added file that failed validation, review, or recovery and should not remain in the repository.

## When to Use

Use this guide when the failing file did not exist in `HEAD` and the correct action is to abandon that addition.

## Required Readings

- `AGENTS.md`
- `docs/maintenance/automation-guardrails.md`

## Required Checks

Inspect the worktree before deleting:

```bash
git status --short
```

Discard the failed newly added file from both the index and filesystem:

```bash
git restore --staged schema/definitions/benchmark.schema.json 2>/dev/null || true
rm -f schema/definitions/benchmark.schema.json
```

Then run:

```bash
git status --short
make validate
make cockpit-summary N=5
```

## Why Not `git restore -- path`

`git restore -- path` is safe for tracked files when restoring content from `HEAD`. For failed newly added files, there may be no valid `HEAD` version to restore. Using restore in that case can preserve or reintroduce invalid content instead of abandoning the failed addition.

## Common Failure Modes

- Removing only the staged entry while leaving the invalid file on disk.
- Removing only the file on disk while leaving a staged addition.
- Running autopilot again before inspecting the failed state.
- Applying the example path without replacing it for the actual failed file when the failed file is different.

## Done Criteria

- The failed newly added file is absent from the index and filesystem.
- `git status --short` reflects the intended state.
- `make validate` and `make cockpit-summary N=5` were run after recovery.
