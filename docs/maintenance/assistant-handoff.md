# Assistant Handoff

## Purpose

This document is the starting point for future AI assistants and maintainers working on **RAG Knowledge Model**, abbreviated **RKM**.

RKM is a structured, extensible, machine-readable and human-readable knowledge model of the Retrieval-Augmented Generation ecosystem. It is intended to support a domain model, ontology, and knowledge graph foundation for describing RAG entities, relationships, claims, evidence, references, and reusable structured knowledge.

RKM is not a plain catalog of RAG techniques. It models the ecosystem through first-class concepts such as techniques, frameworks, papers, components, benchmarks, datasets, models, retrievers, databases, workflows, tools, providers, problems, tradeoffs, claims, evidence, references, and relationships.

The project has moved beyond the question of whether this can be built. The current operating question is how to make the model consumable by other people and systems without overclaiming product maturity.

## Start Here Protocol

A new assistant or maintainer should start with this sequence from the repository root:

1. Read this file.
2. Read `README.md`, `AGENTS.md`, `Makefile`, `QUICKSTART.md`, and `docs/releases/v0.1.0-alpha.md`.
3. Run `make cockpit-summary N=5`.
4. Run `make validate`.
5. Inspect the recent git log with `git log --oneline -n 10`.
6. Continue from the cockpit recommendation and the current user request.

`make cockpit-summary N=5` and `make validate` are authoritative for current operational state because the automation budget, run ledger, recovery state, and working target guardrails change over time. Static documentation explains the system, but cockpit and validation report the live state.

Maintenance documents provide strategic context, not operational truth. Use them to understand direction and rationale, but treat `make cockpit-summary` and `make validate` as the current source of truth for readiness, validation, and next operational action.

## Related Maintenance Documents

Use these documents together:

- `docs/maintenance/repo-map.md` explains the repository structure, how the main areas fit together, and the operational command map.
- `docs/maintenance/maturity-report.md` explains the current maturity level, risks, and recommended next milestones.
- `docs/maintenance/consumability-roadmap.es-AR.md` explains the project in Spanish for human colleagues, technical leads, and managers, with emphasis on making RKM consumable by others.

For product or managerial conversations, read `docs/maintenance/consumability-roadmap.es-AR.md` before explaining the next phase. Use it to describe why RKM should focus on consumability now: the foundation is strong and graph export paths now exist for both fixtures and seed data, but external users still need broader real data, richer examples, expanded export guidance, consumer documentation, and a release package. The Spanish roadmap is meant for human stakeholders, not automation.

When discussing consumability, onboarding, release scope, or alpha packaging, inspect `QUICKSTART.md` and `docs/releases/v0.1.0-alpha.md` before answering. `v0.1.0-alpha` has already been tagged. Do not confuse that already tagged alpha with post-alpha changes on `main`, such as the data graph export and graph export schema validation.

## Repository Discipline

Repository content is written in English unless a specific file intentionally targets another language.

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
make autocycle N=5
make safe-push
make recovery-plan
make autopilot-recover
make budget-report
make codex-commit PROMPT_FILE=prompt.md FILE=docs/maintenance/assistant-handoff.md MESSAGE="Update assistant handoff"
make codex-commit PROMPT_FILE=prompt.md FILES="README.md AGENTS.md" MESSAGE="Update repository guidance"
```

`make validate` is the standard validation entry point.

`make validate` checks schema validity, fixture instance validity, data instance validity, relationship-set semantics, fixture graph export consistency, data graph export consistency, graph export schema validity, and graph endpoint integrity. New assistants should know that data validation and both graph exports are wired into validation, so malformed populated data, invalid declared relationship predicates, relationship endpoints that do not resolve to declared data records, stale export files, malformed graph node or edge files, duplicate graph IDs, or missing graph edge endpoints are validation failures rather than optional cleanup.

`make release-check` is a stricter pre-tag gate for `v0.1.0-alpha`. It requires a clean repository, checks local `origin/main` alignment when available, runs validation, regenerates the graph export, validates again, and fails if the worktree becomes dirty. It is not part of normal validation because ordinary development and `codex-commit` runs intentionally operate with temporary dirty worktrees.

Fixtures and populated data serve different purposes. `examples/fixtures/` contains minimal pedagogical examples and validation fixtures. `data/` contains the first small populated knowledge dataset for consumer testing and release packaging. Do not describe fixtures as the real dataset, and do not describe the seed dataset as a complete RAG catalog.

Relationship instances for populated data are declared in `data/relationships/` and validated through `data/manifest.json`. Relationship-set validation checks that predicates are registered in `registries/relationship-type-registry.json`, source and target IDs exist in declared data entity records, source and target data file fields point to the files that actually contain those IDs, and duplicate relationship IDs or duplicate semantic triples are rejected. The data graph exporter may emit domain graph edges only from declared, validated relationship-set files. Future assistants must not infer domain graph edges from record names, descriptions, stages, or other fields unless those relationships are first represented in validated data.

There are now two graph export paths:

- `make graph-export` generates `examples/graph-export/` from the fixture package.
- `make data-graph-export` generates `examples/data-graph-export/` from validated seed data declared in `data/manifest.json`.

Keep these paths distinct. The fixture graph export is pedagogical and minimal. The data graph export is post-alpha work on `main` and is derived from the real seed dataset plus declared relationship sets.

Graph exports have formal node and edge schemas:

- `schema/graph-node.schema.json`
- `schema/graph-edge.schema.json`

Use `make graph-export-validate` or `python3 scripts/validate-graph-exports.py` to validate both fixture and data graph export files against those schemas. This validation also checks duplicate node IDs, duplicate edge IDs, and edge endpoints that must exist among nodes in the same export. The current fixture artifact still uses `sourceFixture`; the graph export validator maps that fixture provenance field into the formal `sourceDataFile` contract for schema validation.

`make cockpit-summary N=5` summarizes the current automation cockpit state and recommends the next operational step.

`make autopilot N=5` is the normal production run target.

`make autopilot N=24 FORCE=true` is an aggressive or stress run target that explicitly crosses normal budget or target guard boundaries.

`make autocycle N=5` runs repeated bounded cycles through the shell automation layer.

`make safe-push` validates before pushing and should be used instead of manual pushing.

`make recovery-plan` inspects a dirty or interrupted state and reports a safe recovery path.

`make autopilot-recover` runs the automated recovery workflow.

`make budget-report` reports current budget state from the local budget profile.

`make codex-commit` creates validated commits through repository automation. It supports both `FILE` for one file and `FILES` for a coherent multi-file change.

## Automation Architecture

The automation system is organized around small operational scripts and Make targets:

- `rkm-cycle` runs one bounded RKM work cycle.
- `rkm-autocycle` runs repeated cycles under automation control.
- `rkm-autopilot` runs production automation for a requested number of cycles.
- `rkm-next-action` determines the next recommended action from repository state.
- `rkm-recovery-plan` reports a safe recovery plan for dirty, failed, or interrupted states.
- `rkm-cockpit-summary` summarizes current state, recent activity, and recommended operation.
- `rkm-codex-commit` creates validated commits for single-file or coherent multi-file changes.
- `rkm-budget` enforces automation budget and target guardrails.
- Validation scripts enforce schema validity, contract rules, documentation relationship rules, registry consistency, naming expectations, and repository consistency.

The Makefile is the operational surface for maintainers and assistants. Prefer the Make targets over invoking lower-level scripts directly unless debugging the automation itself.

## Safety Model

The repository must be clean before production automation or push operations.

Validation cannot be bypassed. If validation fails, fix the cause before continuing. If the failure is unrelated to the current change, report it clearly and avoid broad edits.

`make safe-push` validates before pushing. Do not bypass it with manual push commands during normal operation.

`FORCE=true` only bypasses budget or target guard boundaries. It must not bypass validation, recovery requirements, reviewer failures, dirty worktree protections, or `safe-push`.

The working target maximum defaults to `N=5`. Larger targets require explicit force, such as `make autopilot N=24 FORCE=true`.

Budget grace exists for small near misses, but it is not permission to ignore validation or repository safety checks.

## Current Maturity

RKM is a strong foundation and production-oriented repository system, but it is not yet a finished consumable product.

Current maturity is approximately:

- Overall maturity: 3.5 / 5
- Conceptual and model maturity: 3.3 / 5
- Tooling and automation maturity: 3.7 / 5
- Consumability maturity: 3.3 / 5
- Populated knowledge base maturity: 2.2 / 5
- Release readiness: 3.0 / 5

The architecture, schema base, validation system, registries, and automation are materially beyond an exploratory prototype. The project also has a first minimal graph export generated from fixtures and checked during validation, a first small seed dataset checked during validation, relationship-set semantics checked against the registry and declared data records, and a post-alpha data graph export generated from that seed dataset with declared domain relationship edges. The project still needs broader populated data, richer examples, release packaging, expanded graph export coverage, and consumer-facing documentation before outside users can adopt it easily.

## Known Patterns and Hardening History

The schema contract validator catches recurring semantic schema mistakes, not only syntax errors.

Fixture validation, data validation, graph export consistency checks, and graph export schema validation are part of the normal validation path. Treat the committed fixture graph export as a generated contract artifact derived from fixtures, not as a complete production-grade export. Treat the committed data graph export as a generated contract artifact derived from `data/manifest.json`, including relationship sets in `data/relationships/`, not as a complete production-grade export. Treat `data/` as populated sample knowledge content, not as a complete ecosystem catalog.

Recurring mistakes that have been hardened include:

- `identity.entityType` values that reference unsupported entity types.
- `oneOf` branches that confuse `number` and `integer` constraints.
- Identifier patterns that accidentally allow only four digits.
- Embedded definitions that start behaving like first-class entities without explicit modeling decisions.

Cockpit summary count bugs were fixed so summary totals and recent activity counts are more reliable.

`rkm-codex-commit` supports multi-file changes through the `FILES="README.md AGENTS.md"` interface while retaining single-file support through `FILE=docs/maintenance/assistant-handoff.md`.

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

## Near-Term Direction

The next natural work should improve consumability:

- Broaden the first small seed dataset with representative populated content.
- Add richer examples and fixtures that demonstrate valid entities, relationships, claims, evidence, references, and graph export behavior.
- Add release documentation, release packaging, and consumer-oriented guides.
- Expand the current minimal graph exports so the model can be consumed more broadly outside the repository.
- Keep schema expansion disciplined so embedded reusable concepts do not drift into implicit entity models.
- Continue using validation and cockpit output as the source of truth for readiness.
