# Assistant Handoff

## Project Identity

The project is **RAG Knowledge Model**, abbreviated **RKM**.

RKM is a structured, extensible, machine-readable and human-readable knowledge model of the Retrieval-Augmented Generation ecosystem. It is intended to support a domain model, ontology, and knowledge graph foundation for describing RAG entities, relationships, claims, evidence, references, and reusable structured knowledge.

RKM is not a plain catalog of RAG techniques. It models the ecosystem through first-class concepts such as techniques, frameworks, papers, components, benchmarks, datasets, models, retrievers, databases, workflows, tools, providers, problems, tradeoffs, claims, evidence, references, and relationships.

## Repository Discipline

Repository content is written in English.

Schemas use JSON Schema Draft 2020-12. Schema files must declare the draft explicitly, use stable `$id` values that follow RKM naming conventions, and compose shared definitions where appropriate.

Documentation and schemas must not contain unfinished-work markers, filler text, or incomplete sections.

Use the canonical project names only:

- Full name: RAG Knowledge Model
- Acronym: RKM

Do not use deprecated or alternate project names.

The workflow is validation-first. Changes should be checked with repository validation before they are considered ready. A commit should contain one coherent unit of work when possible, and each unit should preserve the domain model, entity model, relationship model, evidence model, metadata model, ontology, naming conventions, and versioning rules.

## Core Commands

Use these commands from the repository root:

```bash
make validate
make cockpit-summary N=5
make autopilot N=5
make autopilot N=24 FORCE=true
make safe-push
make recovery-plan
make autopilot-recover
make codex-commit FILE=docs/maintenance/assistant-handoff.md
make codex-commit FILES="README.md AGENTS.md"
```

`make validate` is the standard validation entry point.

`make cockpit-summary N=5` summarizes the current automation cockpit state and recommends the next operational step.

`make autopilot N=5` is the normal production run target.

`make autopilot N=24 FORCE=true` is an aggressive or stress run target that explicitly crosses normal budget or target guard boundaries.

`make safe-push` validates before pushing and should be used instead of manual pushing.

`make recovery-plan` inspects a dirty or interrupted state and reports a safe recovery path.

`make autopilot-recover` runs the automated recovery workflow.

`make codex-commit FILE=docs/maintenance/assistant-handoff.md` commits a single-file change through the repository commit automation.

`make codex-commit FILES="README.md AGENTS.md"` commits a coherent multi-file change through the repository commit automation.

## Automation Architecture

The automation system is organized around small operational scripts and make targets:

- `rkm-cycle` runs one bounded RKM work cycle.
- `rkm-autocycle` runs repeated cycles under automation control.
- `rkm-autopilot` runs production automation for a requested number of cycles.
- `rkm-next-action` determines the next recommended action from repository state.
- `rkm-recovery-plan` reports a safe recovery plan for dirty, failed, or interrupted states.
- `rkm-cockpit-summary` summarizes current state, recent activity, and recommended operation.
- `rkm-codex-commit` creates validated commits for single-file or coherent multi-file changes.
- `rkm-budget` enforces automation budget and target guardrails.
- Validation scripts enforce schema validity, contract rules, documentation quality, naming rules, and repository consistency.

The Makefile is the operational surface for maintainers and assistants. Prefer the Make targets over invoking lower-level scripts directly unless debugging the automation itself.

## Safety Model

The repository must be clean before production automation or push operations.

Validation cannot be bypassed. If validation fails, fix the cause before continuing. If the failure is unrelated to the current change, report it clearly and avoid broad edits.

`make safe-push` validates before pushing. Do not bypass it with manual push commands during normal operation.

`FORCE=true` only bypasses budget or target guard boundaries. It must not bypass validation, recovery requirements, reviewer failures, dirty worktree protections, or `safe-push`.

The working target maximum defaults to `N=5`. Larger targets require explicit force, such as `make autopilot N=24 FORCE=true`.

Budget grace exists for small near-misses, but it is not permission to ignore validation or repository safety checks.

## Known Patterns and Hardening History

The schema contract validator catches recurring semantic schema mistakes, not only syntax errors.

Recurring mistakes that have been hardened include:

- `identity.entityType` values that reference unsupported entity types.
- `oneOf` branches that confuse `number` and `integer` constraints.
- identifier patterns that accidentally allow only four digits.
- embedded definitions that should instead be represented as first-class relationships.

Cockpit summary count bugs were fixed so summary totals and recent activity counts are more reliable.

`rkm-codex-commit` now supports multi-file changes through the `FILES="README.md AGENTS.md"` interface while retaining single-file support through `FILE=docs/maintenance/assistant-handoff.md`.

## Current Recommended Operation

For normal production work, run:

```bash
make autopilot N=5
```

For an aggressive or stress run, run:

```bash
make autopilot N=24 FORCE=true
```

After every run, inspect the cockpit:

```bash
make cockpit-summary N=5
```

If the cockpit, validation, or automation reports a dirty state or recovery requirement, do not push manually. Use:

```bash
make recovery-plan
make autopilot-recover
```

Then re-run validation and the cockpit summary before continuing.

## Handoff Protocol For A New Assistant

A new assistant or maintainer should start with this sequence:

1. Read this file first.
2. Inspect `README.md`, `AGENTS.md`, and `Makefile`.
3. Run `make cockpit-summary N=5`.
4. Run `make validate`.
5. Inspect the recent git log.
6. Continue from the cockpit recommendation.

This sequence establishes project identity, repository rules, automation state, validation state, recent changes, and the next recommended operational action before new work begins.

## Open Next Improvements

Consider adding a validator rule for embedded definitions that include top-level relationships.

Consider adding a `make repo-brief` target that prints the project identity, key rules, automation state, and next recommended action.

Consider adding a `make doctor` target that checks local prerequisites, script executability, validation availability, git state, and automation readiness.

Consider summarizing registries and schema coverage in a generated or maintained operational report.

Continue expanding RKM content through:

```bash
make autopilot N=5
```
