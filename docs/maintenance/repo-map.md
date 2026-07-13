# Repository Map

## Purpose

This document explains the main areas of the RAG Knowledge Model repository and how they work together. It is intended for maintainers, future AI assistants, technical leads, and contributors who need to understand the project shape before changing it.

RKM is both a knowledge model and an operational repository. The architecture documents define the meaning of the model, the schemas make that meaning machine-checkable, the registries constrain shared vocabularies, and the scripts enforce discipline through validation and automation.

## Top-Level Entry Points

`README.md` introduces the project, mission, design principles, long-term vision, and intended uses. It is the public entry point for people encountering RKM for the first time.

`AGENTS.md` defines repository-specific operating instructions for AI assistants. It is authoritative for workflow constraints, review behavior, naming rules, modeling rules, and validation expectations during assisted development.

`Makefile` is the operational command surface. Maintainers and assistants should prefer Make targets over calling scripts directly for normal work.

## Architecture Documentation

`docs/architecture` contains the conceptual foundation for the model. These files define the ubiquitous language, domain model, entity model, relationship model, evidence model, metadata model, ontology, naming conventions, and versioning rules.

Architecture documents are the semantic authority for the repository. A schema may be syntactically valid but still wrong if it conflicts with these documents. When extending RKM, start from the architecture and then update schemas or registries to match.

## Maintenance Documentation

`docs/maintenance` contains operational and handoff material for people and assistants maintaining the repository.

Key files include:

- `assistant-handoff.md`, the start-here guide for future assistants and maintainers.
- `repo-map.md`, this repository structure and command map.
- `maturity-report.md`, the current maturity assessment and risk register.
- `consumability-roadmap.es-AR.md`, a Spanish roadmap for explaining the project to colleagues, leads, and managers.

Maintenance documents should describe how to work with the repository without changing the model semantics themselves.

## Schemas

`schema` contains JSON Schema Draft 2020-12 files for RKM entities and registries.

Specialized entity schemas such as `rag-technique.schema.json`, `framework.schema.json`, `paper.schema.json`, `dataset.schema.json`, and related files describe concrete entity shapes. These schemas compose shared definitions where possible and must use supported `identity.entityType` values.

`schema/definitions` contains reusable schema definitions for shared concepts such as identity, metadata, relationships, claims, evidence, references, entity references, descriptions, costs, risks, retrieval, evaluation, graph export, and other structured concepts.

Shared definitions should be used when a concept is reusable across multiple entity types. A concept that becomes independently addressable, linkable, or graph-relevant may need to become a first-class entity or relationship instead of remaining embedded data.

## Registries

The registry schemas live under `schema`:

- `entity-type-registry.schema.json`
- `relationship-type-registry.schema.json`

These registries constrain controlled vocabularies for entity types and relationship predicates. They are part of the contract that keeps schemas, documentation, and graph-oriented use cases aligned.

Relationship predicates should use uppercase snake case. Architecture documents should use canonical relationship predicates from the relationship model unless they are explicitly marked as candidates, rejected examples, deprecated examples, or noncanonical discussion.

## Scripts

`scripts` contains repository automation and validation tooling.

The validation scripts check schema correctness, registry consistency, schema prerequisites, schema contracts, documentation relationship usage, and broader repository rules. The automation scripts run bounded work cycles, cockpit summaries, recovery planning, budget reporting, and commit workflows.

Scripts are implementation details behind the Make targets. Call them directly only when debugging the command itself or when a Make target is not available for the required operation.

## Git Hooks

`.githooks` contains repository Git hooks. The Makefile includes `make install-hooks` to configure Git to use this directory as the hook path.

Hooks are a local safety layer. They do not replace `make validate`, cockpit checks, or the repository review rules.

## How The Pieces Fit Together

RKM uses a layered model:

1. Architecture documents define the meaning of the domain.
2. Schemas turn the model into machine-checkable contracts.
3. Definitions provide reusable structured building blocks.
4. Registries constrain shared vocabularies.
5. Validation scripts enforce syntax, consistency, and semantic guardrails.
6. Automation scripts make repeated repository work safer and more reproducible.
7. Maintenance documents explain the system to assistants and human maintainers.

This means a change should be evaluated at multiple levels. A new schema should validate mechanically, fit the architecture, use registered entity and relationship types, avoid duplicating existing concepts, and remain understandable to future consumers.

## Operational Command Map

Use these commands from the repository root.

`make validate`

Runs the standard validation entry point, implemented by `bash scripts/validate-rkm.sh`. This is the required readiness check before considering changes complete.

`make cockpit-summary N=5`

Shows a compact operational dashboard for the current target. It summarizes live state such as budget, recovery posture, recent activity, and the recommended next action.

`make autopilot N=5`

Runs production automation through the Python autopilot for a bounded target. This is the normal automated work command.

`make autopilot N=24 FORCE=true`

Runs a larger or stress-oriented autopilot target. `FORCE=true` can cross target or budget guard boundaries but must not bypass validation or repository safety.

`make autocycle N=5`

Runs repeated shell-based cycles through `scripts/rkm-autocycle.sh`. This is useful for automation flow that predates or complements autopilot.

`make safe-push`

Runs validation, requires a clean working tree, shows recent commits, and then pushes. It is the preferred push path for normal repository operation.

`make recovery-plan`

Inspects the current repository and recent logs to recommend a safe recovery path without modifying files.

`make autopilot-recover`

Runs autopilot with recovery enabled. Use it when cockpit or validation indicates an interrupted or dirty automation state that can be recovered automatically.

`make codex-commit PROMPT_FILE=prompt.md FILE=path/to/file MESSAGE="Commit message"`

Creates a validated single-file commit through the repository commit automation.

`make codex-commit PROMPT_FILE=prompt.md FILES="path/a path/b" MESSAGE="Commit message"`

Creates a validated coherent multi-file commit through the repository commit automation.

`make budget-report`

Reports the local budget profile and current budget accounting. Budget state changes over time, so this command is a live operational check rather than static documentation.

## Current Consumability Gap

The repository has a strong architecture and validation system, but it is not yet easy for external consumers to use directly. The highest-value next work is to add examples, fixtures, graph exports, release documentation, and consumer-facing guides that show how to read, validate, load, and query RKM content.
