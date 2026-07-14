# Automation Guardrails

## Purpose

This document codifies operational rules for RKM automation, recovery, schema-contract changes, and unattended runs. These rules exist because recent unattended autopilot and failed recovery runs showed that validation alone is not enough to protect the repository from dirty worktrees, invalid newly added files, duplicate schema contracts, misleading documentation examples, or budget spent on repeated recovery attempts.

These guardrails apply to post-alpha work on `main`. The `v0.1.0-alpha` tag already exists and must not be modified by routine automation.

## Distributed Rule Routing

Automation and recovery work must route through root `AGENTS.md`, then the local `AGENTS.md` file for the affected area, then the relevant task guide under `docs/maintenance/task-guides/`.

Use the task guides for operational detail instead of expanding this file with every task-specific checklist. In particular, unattended runs use `docs/maintenance/task-guides/unattended-autopilot.md`, failed-new-file recovery uses `docs/maintenance/task-guides/recovering-failed-new-file.md`, schema work uses the schema task guides, and exporter or validator changes use the graph export or validation script guides.

Distributed rule routing is validated automatically by `make validate` and can be checked directly with `make agent-routing-validate`. Duplicate schema contracts are also checked automatically through `make schema-duplicate-contracts-validate` and the standard validation pipeline.

Use `docs/maintenance/rule-coverage-report.md` to see which governance rules are documented, partially validated, or validated. The report is the enforcement-level map; this document remains the operational guardrail source and does not duplicate that table.

## Clean Worktree Invariant

Passing validation is necessary but not sufficient.

Before `make safe-push`, autopilot, or handoff, `git status --short` must be clean. If the worktree is dirty, stop automation and inspect the dirty state before running more automation or handing work to another assistant.

A dirty worktree after validation still blocks push and handoff.

## Runtime Logs and Scratch Files

Runtime logs, away-run logs, scratch files, and automation transcripts must not be written inside the repository.

Use `/tmp/rkm-runs` for local runtime output:

```bash
mkdir -p /tmp/rkm-runs
```

Do not create `.rkm-runs/` inside the repository. If `.rkm-runs/` exists inside the repository, remove it and optionally add `.rkm-runs/` to `.git/info/exclude` for local protection.

Repository-local runtime logs make the worktree dirty and can confuse recovery tooling, review state, and handoff readiness.

## Failed Newly Added Files

If a newly added file fails review or recovery and should be discarded, remove it from both the index and the filesystem:

```bash
git restore --staged path/to/file 2>/dev/null || true
rm -f path/to/file
```

Do not use `git restore -- path/to/file` for a failed newly added file unless it is known to be tracked in `HEAD`.

Restoring a failed newly added file can preserve or reintroduce invalid content. For a failed addition that should be abandoned, the correct recovery action is to unstage it and delete it.

## Recovery Failure Stop Rule

If recovery status is `RECOVERY_FAILED_NEEDS_MANUAL_FIX`, do not run autopilot again.

First run:

```bash
git status --short
make recovery-plan
```

Then choose one recovery path:

- Manually fix the dirty file.
- Run `make recover-revise` when the recovery plan says the failed work is still directionally correct.
- Discard the failed newly added file with the failed-new-file discard commands.

Running autopilot again before this inspection can spend budget on the same failed state and make recovery harder to reason about.

## Autopilot Scope

Autopilot may expand low-risk content such as architecture documents, glossary-like documentation, and data records that follow an established pattern.

Autopilot must not freely evolve structural contracts.

Schema, registry, validator, exporter, Makefile, release-process, graph-contract, and migration changes require explicit `codex-commit` prompts. These changes alter repository contracts or operational behavior and need an intentional prompt, scope, and review path.

## Unattended Autopilot Rule

For unattended runs, prefer repeated `make autopilot N=1` rounds.

Each round should validate, safe-push, and emit a cockpit summary. Larger targets may be used only when a maintainer is present to inspect recovery states.

`N=1` limits accepted work count, not wall-clock duration. Until `GB-042` is implemented, unattended runs should be treated as bounded by iteration count but not by time. After any interrupted or suspended run, operators should inspect `/tmp/rkm-runs`, `/tmp/rkm-cycle-output.txt`, and `git status --short` before continuing.

The recommended unattended pattern is:

```bash
mkdir -p /tmp/rkm-runs
set -o pipefail
for i in 1 2 3 4 5 6 7 8 9 10
do
  LOG="/tmp/rkm-runs/autopilot-away-round-${i}.log"
  echo "===== AUTOPILOT ROUND $i =====" | tee -a "$LOG"
  date | tee -a "$LOG"
  make autopilot N=1 2>&1 | tee -a "$LOG" || break
  make safe-push 2>&1 | tee -a "$LOG" || break
  make validate 2>&1 | tee -a "$LOG" || break
  make cockpit-summary N=5 2>&1 | tee -a "$LOG" || break
  echo "===== END ROUND $i =====" | tee -a "$LOG"
done
```

## Schema Duplication and Atomic Refactor Rule

Do not add `schema/definitions/<name>.schema.json` when `schema/<name>.schema.json` already exists unless the same commit refactors the first-class schema to compose from the reusable definition.

`make schema-duplicate-contracts-validate` enforces the same-name composition requirement by checking that the first-class schema visibly references the reusable definition.

Reusable definition extraction must be atomic:

- Add the reusable definition.
- Update the first-class schema.
- Update validation, self-tests, examples, and docs.
- Explain the contract relationship.

Do not allow two independently evolving schema contracts for the same concept.

## Relationship Predicate Reuse Rule

Before adding a relationship predicate, inspect `registries/relationship-type-registry.json`.

Reuse an existing predicate when its semantics fit. Add a new predicate only with explicit justification and documentation.

Avoid mandatory predicates such as `REQUIRES` unless the model truly means a hard dependency.

## New Entity Type Data Package Rule

Adding data for a new entity type requires the complete package:

- Data records.
- Manifest entries.
- Semantic validation compatibility.
- Graph export support.
- Schema provenance nodes.
- Graph export validation.
- Documentation.
- Self-test coverage when applicable.

Do not add isolated data files without export and validation support.

## JSON Example Validity Rule

Architecture docs must use either fully real seed examples or clearly abstract examples.

JSON examples with concrete repository paths must use real seed IDs and matching source or target files. Abstract examples must not use concrete repository paths.

Examples must not mix invented IDs with real repository paths.

## Budget Guard Interpretation

A budget-stop after accepted commits is not a failure if the repository is clean and accepted commits were pushed.

A budget-stop with a dirty worktree requires manual inspection.

Partial progress is acceptable only when validation passes and the worktree is clean after the accepted commits are pushed.

## Handoff Checklist

Before handoff, run:

```bash
git status --short
make validate
make safe-push
make cockpit-summary N=5
git log --oneline --decorate -n 12
```

If any command reports a dirty state, validation failure, push failure, or recovery requirement, stop and inspect before handing off.
