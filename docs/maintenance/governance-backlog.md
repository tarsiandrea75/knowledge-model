# Governance Backlog

## Purpose

This file captures deferred governance, validation, modeling, evidence, release, and tooling ideas for RAG Knowledge Model.

Postponed ideas should be recorded here before they are deferred so useful repository improvements are not lost in chat history or operational handoff notes.

This backlog complements, but does not replace, `docs/maintenance/rule-coverage-report.md`. The coverage report tracks current enforcement levels, while this file tracks actionable deferred work and implementation candidates.

## Entry Format

Each backlog entry uses this compact format:

- `ID`
- `Title`
- `Status`
- `Priority`
- `Area`
- `Reason`
- `Suggested implementation`
- `Related files`
- `Depends on`

## Status Values

- `Proposed`
- `Planned`
- `In Progress`
- `Implemented`
- `Superseded`
- `Deferred`

## Priority Values

- `High`
- `Medium`
- `Low`

## Maintenance Rules

- Every deferred governance, validation, modeling, release, or evidence idea should be recorded in this backlog before being postponed.
- When an item is implemented, update its status and link the implementation path or command.
- When a backlog item changes rule coverage, update `docs/maintenance/rule-coverage-report.md`.
- Prefer small implementation commits that close or advance one backlog item at a time.
- Do not inflate maturity claims because an item is listed here.

## Suggested Next Items

- `GB-003` Relationship predicate reuse checker.
- `GB-006` Recovery state validator or autopilot blocker.
- `GB-038` `v0.2.0` planning document.

## Backlog Entries

### GB-001 Schema Duplicate Contract Validator

- `ID`: `GB-001`
- `Title`: Schema duplicate contract validator.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Validation
- `Reason`: Prevent duplicate contracts such as adding `schema/definitions/benchmark.schema.json` while `schema/benchmark.schema.json` exists.
- `Suggested implementation`: Already implemented by `scripts/validate-schema-duplicate-contracts.py`, `make schema-duplicate-contracts-validate`, and `make validate`.
- `Related files`: `scripts/validate-schema-duplicate-contracts.py`; `Makefile`; `schema/`; `schema/definitions/`
- `Depends on`: Implemented in commit `bdf23f8 Add schema duplicate contract validation`.

### GB-002 New Entity Type Package Validator

- `ID`: `GB-002`
- `Title`: New entity type package validator.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Validation
- `Reason`: Adding a new entity type requires coordinated schema, registry, data, manifest, graph export, documentation, and validation support.
- `Suggested implementation`: Implemented by `scripts/validate-entity-type-packages.py`, exposed through `make entity-type-package-validate`, and included in `make validate`.
- `Related files`: `data/AGENTS.md`; `schema/`; `registries/`; `data/manifest.json`; `examples/data-graph-export/`; `docs/maintenance/task-guides/adding-new-entity-type.md`; `scripts/validate-entity-type-packages.py`
- `Depends on`: Implemented in the local GB-002 checkpoint; no canonical-data or schema migration dependency.

### GB-003 Relationship Predicate Reuse Checker

- `ID`: `GB-003`
- `Title`: Relationship predicate reuse checker.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Validation
- `Reason`: New predicates should not duplicate existing relationship semantics.
- `Suggested implementation`: Implemented by `scripts/review-relationship-predicate-reuse.py` and exposed through `make relationship-predicate-review`. The advisory review reports lexical semantic candidates and requires explicit human justification before adding a new predicate. See `docs/maintenance/task-packets/GB-003-relationship-predicate-reuse.md`.
- `Related files`: `registries/relationship-type-registry.json`; `registries/AGENTS.md`; `docs/maintenance/task-guides/adding-relationship-set.md`
- `Depends on`: Implemented in the GB-003 task packet; no canonical-data migration dependency.

### GB-004 Hard Dependency Predicate Justification Check

- `ID`: `GB-004`
- `Title`: Hard dependency predicate justification check.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Validation
- `Reason`: Hard dependency predicates such as `REQUIRES` need explicit justification because they can overstate architectural necessity.
- `Suggested implementation`: Add validation or reviewer tooling that requires justification metadata for hard dependency predicates.
- `Related files`: `registries/relationship-type-registry.json`; `data/relationships/`; `docs/maintenance/task-guides/adding-relationship-set.md`
- `Depends on`: Repository maintainer prioritization.

### GB-005 Task Router CLI

- `ID`: `GB-005`
- `Title`: Task router CLI that maps paths to required rule files and task guides.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Tooling
- `Reason`: Contributors need a quick way to identify the rule files and task guides required by a change.
- `Suggested implementation`: Implemented by `scripts/rkm-route-task.py` and exposed through `make route-task PATHS="schema/foo.schema.json data/rag-techniques/hybrid-retrieval.json"`.
- `Related files`: `AGENTS.md`; `docs/maintenance/task-guides/README.md`; `scripts/`; `Makefile`
- `Depends on`: Implemented on `main` after `v0.1.0-alpha`.

### GB-006 Recovery State Validator Or Autopilot Blocker

- `ID`: `GB-006`
- `Title`: Recovery state validator or autopilot blocker.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Automation
- `Reason`: Autopilot should stop when recovery state requires manual repair.
- `Suggested implementation`: Implemented by `scripts/rkm-autopilot.py`; failed recovery states produce a zero-command manual-fix plan and block post-failure publication. See `docs/maintenance/task-packets/GB-006-recovery-state-autopilot-blocker.md`.
- `Related files`: `docs/maintenance/automation-guardrails.md`; `docs/maintenance/task-guides/recovering-failed-new-file.md`; `scripts/`; `Makefile`
- `Depends on`: Implemented in the GB-006 task packet; no external dependency.

### GB-007 Runtime Artifact Detector

- `ID`: `GB-007`
- `Title`: Runtime artifact detector for repository-local logs, scratch files, transcripts, and temporary run directories.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Validation
- `Reason`: Generated runtime artifacts inside the repository can pollute status, recovery, and handoff decisions.
- `Suggested implementation`: Implemented by `scripts/validate-runtime-artifacts.py`, exposed through `make runtime-artifacts-validate`, and included in `make validate`.
- `Related files`: `AGENTS.md`; `docs/maintenance/automation-guardrails.md`; `scripts/validate-runtime-artifacts.py`; `scripts/validate-rkm.sh`; `Makefile`; `docs/maintenance/rule-coverage-report.md`
- `Depends on`: Implemented in the local GB-007 checkpoint; no schema or canonical-data dependency.

### GB-008 Rule Coverage Consistency Validator

- `ID`: `GB-008`
- `Title`: Rule coverage consistency validator.
- `Status`: `Implemented`
- `Priority`: `Medium`
- `Area`: Governance
- `Reason`: The coverage report should stay aligned with implemented validators and documented rules.
- `Suggested implementation`: Implemented by `scripts/validate-rule-coverage.py`, exposed through `make rule-coverage-validate`, and included in `make validate`. See `docs/maintenance/task-packets/GB-008-rule-coverage-consistency.md`.
- `Related files`: `docs/maintenance/rule-coverage-report.md`; `scripts/`; `Makefile`
- `Depends on`: Implemented in the GB-008 task packet; no schema or canonical-data dependency.

### GB-009 Markdown JSON Example Validator

- `ID`: `GB-009`
- `Title`: Markdown JSON example validator.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Validation
- `Reason`: Documentation examples should remain parseable and avoid misleading concrete repository paths with invalid identifiers.
- `Suggested implementation`: Extend documentation validation to parse JSON code fences and apply repository-specific example checks.
- `Related files`: `docs/`; `scripts/`; `Makefile`
- `Depends on`: Repository maintainer prioritization.

### GB-010 Stronger Graph Export Provenance Consistency Validator

- `ID`: `GB-010`
- `Title`: Stronger graph export provenance consistency validator.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Validation
- `Reason`: Graph export provenance should remain consistent with source data, fixture paths, and relationship support metadata.
- `Suggested implementation`: Add deeper provenance checks to graph export validation for source file references, support links, and export origin fields.
- `Related files`: `examples/graph-export/`; `examples/data-graph-export/`; `scripts/validate-graph-exports.py`; `docs/maintenance/graph-export-contract.md`
- `Depends on`: Repository maintainer prioritization.

### GB-011 Validation Weakening Detector

- `ID`: `GB-011`
- `Title`: Validation weakening detector.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Validation
- `Reason`: Validator changes should not silently narrow checks, remove cases, or lower enforcement.
- `Suggested implementation`: Add self-test coverage and review tooling that compares validator behavior before and after validation script changes.
- `Related files`: `scripts/AGENTS.md`; `docs/maintenance/task-guides/updating-validation-scripts.md`; `scripts/`; `Makefile`
- `Depends on`: Repository maintainer prioritization.

### GB-012 Policy-As-Data Registry

- `ID`: `GB-012`
- `Title`: Policy-as-data registry.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Governance
- `Reason`: Governance rules need stable structured metadata for automation, reporting, and traceability.
- `Suggested implementation`: Add a registry that records rule identifiers, source files, enforcement level, related validators, and review owner.
- `Related files`: `docs/maintenance/rule-coverage-report.md`; `registries/`; `schema/`; `scripts/`
- `Depends on`: Repository maintainer prioritization.

### GB-013 Stable Rule IDs

- `ID`: `GB-013`
- `Title`: Stable rule IDs.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Governance
- `Reason`: Stable identifiers make governance rules easier to reference from validators, reports, reviews, and backlog entries.
- `Suggested implementation`: Assign durable IDs to governance rules and use them in rule coverage, policy data, and validation output.
- `Related files`: `AGENTS.md`; `docs/maintenance/rule-coverage-report.md`; `docs/maintenance/task-guides/`; `registries/`
- `Depends on`: `GB-012`.

### GB-014 Link Rules To Validators

- `ID`: `GB-014`
- `Title`: Link rules to validators.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Governance
- `Reason`: Maintainers need to know which rule is enforced by which command or script.
- `Suggested implementation`: Add explicit rule-to-validator links in structured policy data or the rule coverage report.
- `Related files`: `docs/maintenance/rule-coverage-report.md`; `scripts/`; `Makefile`; `registries/`
- `Depends on`: `GB-012`.

### GB-015 More Granular Local Rule Files

- `ID`: `GB-015`
- `Title`: More granular local rule files.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Governance
- `Reason`: Some repository areas may need local rules closer to their files as modeling and tooling grow.
- `Suggested implementation`: Split or add local `AGENTS.md` files only where repeated work shows stable area-specific rules.
- `Related files`: `AGENTS.md`; `data/AGENTS.md`; `schema/AGENTS.md`; `scripts/AGENTS.md`; `docs/maintenance/task-guides/`
- `Depends on`: Repository maintainer prioritization.

### GB-016 Anti-Duplication Check Between Rule Sources

- `ID`: `GB-016`
- `Title`: Anti-duplication check between root `AGENTS.md`, local `AGENTS.md`, and task guides.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Governance
- `Reason`: Distributed rules should route clearly without copying full operational manuals across files.
- `Suggested implementation`: Extend agent routing validation to flag excessive repeated blocks or oversized duplicated guidance.
- `Related files`: `AGENTS.md`; `data/AGENTS.md`; `schema/AGENTS.md`; `scripts/AGENTS.md`; `docs/maintenance/task-guides/`
- `Depends on`: Repository maintainer prioritization.

### GB-017 Line Budget For Local Rule Files

- `ID`: `GB-017`
- `Title`: Line budget for local `AGENTS.md` files.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Governance
- `Reason`: Local rule files should stay concise and route detailed procedures to task guides.
- `Suggested implementation`: Add local rule file line budgets to agent routing validation with documented exceptions for justified cases.
- `Related files`: `AGENTS.md`; local `AGENTS.md` files; `scripts/validate-agent-routing.py`; `docs/maintenance/task-guides/rule-routing-validation.md`
- `Depends on`: Repository maintainer prioritization.

### GB-018 Chunking Strategy Seed Data

- `ID`: `GB-018`
- `Title`: Chunking strategy seed data.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Modeling
- `Reason`: Chunking is central to RAG behavior and should be represented in the seed dataset.
- `Suggested implementation`: The first implemented seed records are `data/rag-techniques/fixed-size-chunking.json`, `data/rag-techniques/recursive-chunking.json`, and `data/rag-techniques/semantic-chunking.json`. The first conservative relationship expansion has been added for the three chunking techniques as possible pipeline-ordering relationships before Hybrid Retrieval, with relationship support routed through the relationship-set and relationship-support task guides.
- `Related files`: `data/`; `schema/`; `registries/`; `docs/maintenance/task-guides/adding-data-records.md`
- `Depends on`: Repository maintainer prioritization.

### GB-019 Embedding Model Seed Data

- `ID`: `GB-019`
- `Title`: Embedding model seed data.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Modeling
- `Reason`: Embedding models are a core RAG dependency and need structured representation.
- `Suggested implementation`: Add seed records for representative embedding models with references and conservative relationships.
- `Related files`: `data/`; `schema/`; `registries/`
- `Depends on`: Repository maintainer prioritization.

### GB-020 Vector Database And Graph Database Seed Data

- `ID`: `GB-020`
- `Title`: Vector database and graph database seed data.
- `Status`: `Implemented`
- `Priority`: `Medium`
- `Area`: Modeling
- `Reason`: Storage systems are important RAG infrastructure and should be queryable as first-class entities or related components.
- `Suggested implementation`: Implemented through the `VectorDatabase` architecture and schema contracts, 17 manifest-declared records under `data/vector-databases/`, deterministic data graph export coverage, and source-linked decision-query and comparison views. The current dataset includes graph-plus-vector systems such as Neo4j, Amazon Neptune Analytics, and Memgraph. Implementation status records delivery of the modeled dataset and tooling; it does not imply independent semantic approval of every record. Neo4j is currently `Approved`; the other sixteen records remain `Not Reviewed`.
- `Related files`: `data/vector-databases/`; `data/manifest.json`; `docs/architecture/vector-database-model.md`; `schema/vector-database.schema.json`; `schema/definitions/capability.schema.json`; `scripts/rkm-decision-query.py`; `examples/data-graph-export/`
- `Depends on`: Implemented across the VectorDatabase model, dataset-expansion, graph-export, and decision-query commits from `01df322 Add VectorDatabase decision view` through `74ca2d0 Add entity comparison view to decision query`, with capability, licensing, and lifecycle refinements through `a617864 Approve Neo4j vector database record`.

### GB-021 Query Transformation Technique Seed Data

- `ID`: `GB-021`
- `Title`: Query transformation technique seed data.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Modeling
- `Reason`: Query transformation techniques are common in RAG pipelines and should be available in the populated dataset.
- `Suggested implementation`: Add records for representative query rewriting, decomposition, expansion, and routing techniques with evidence-backed claims.
- `Related files`: `data/techniques/`; `data/relationships/`; `data/relationship-support/`; `schema/`
- `Depends on`: Repository maintainer prioritization.

### GB-022 Evaluation Metric Seed Data

- `ID`: `GB-022`
- `Title`: Evaluation metric seed data.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Modeling
- `Reason`: Evaluation metrics are needed to describe quality, tradeoffs, and benchmark interpretation.
- `Suggested implementation`: Add metric records with definitions, source references, and relationships to benchmarks or evaluation workflows.
- `Related files`: `data/`; `schema/`; `registries/`; `docs/architecture/`
- `Depends on`: Repository maintainer prioritization.

### GB-023 Benchmark Seed Data

- `ID`: `GB-023`
- `Title`: Benchmark seed data.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Modeling
- `Reason`: Benchmarks provide shared evaluation context for RAG systems and techniques.
- `Suggested implementation`: Add representative benchmark records with scope, references, and links to metrics or datasets.
- `Related files`: `data/`; `schema/benchmark.schema.json`; `registries/`
- `Depends on`: Repository maintainer prioritization.

### GB-024 Dataset Seed Data

- `ID`: `GB-024`
- `Title`: Dataset seed data.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Modeling
- `Reason`: Datasets are needed to connect RAG techniques, evaluations, and claims to concrete evidence contexts.
- `Suggested implementation`: Add representative dataset records with references, provenance, and relationships to benchmarks or evaluation metrics.
- `Related files`: `data/`; `schema/dataset.schema.json`; `registries/`
- `Depends on`: Repository maintainer prioritization.

### GB-025 LLM, Embedding, And Reranker Provider Modeling

- `ID`: `GB-025`
- `Title`: LLM, embedding, and reranker provider modeling.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Modeling
- `Reason`: Provider relationships affect availability, capabilities, and model provenance.
- `Suggested implementation`: Define provider records and relationships to model offerings after confirming whether providers are entities, organizations, or both.
- `Related files`: `data/`; `schema/`; `registries/`; `docs/architecture/`
- `Depends on`: Repository maintainer prioritization.

### GB-026 Agentic RAG Workflow Modeling

- `ID`: `GB-026`
- `Title`: Agentic RAG workflow modeling.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Modeling
- `Reason`: Agentic retrieval workflows need explicit structure for planning, tool use, retrieval loops, and evidence use.
- `Suggested implementation`: Add workflow model guidance, seed records, and relationships after clarifying the workflow entity contract.
- `Related files`: `data/`; `schema/`; `docs/architecture/`; `registries/`
- `Depends on`: Repository maintainer prioritization.

### GB-027 External References Pass

- `ID`: `GB-027`
- `Title`: External references pass.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Evidence
- `Reason`: Claims and seed records need stronger external grounding before downstream consumers rely on them.
- `Suggested implementation`: Review high-value records and add primary references, stable identifiers, and conservative citation metadata.
- `Related files`: `data/`; `data/relationship-support/`; `schema/reference.schema.json`; `docs/maintenance/task-guides/adding-data-records.md`
- `Depends on`: Repository maintainer prioritization.

### GB-028 Evidence Strength Calibration

- `ID`: `GB-028`
- `Title`: Evidence strength calibration.
- `Status`: `Implemented`
- `Priority`: `Medium`
- `Area`: Evidence
- `Reason`: Evidence strength should be applied consistently across claims and relationships.
- `Suggested implementation`: Implemented in `docs/architecture/evidence-model.md` under `Evidence Strength Calibration`, which calibrates strength against the exact claim, requires the lowest justified strength, lists factors that lower strength, rejects source-authority or reputation inflation, prefers narrowing overbroad claims, and keeps evidence strength distinct from maintainer confidence. This is review guidance rather than schema or validator enforcement.
- `Related files`: `docs/architecture/evidence-model.md`; `schema/evidence.schema.json`; `schema/claim.schema.json`; `data/relationship-support/`
- `Depends on`: Implemented in commit `d26e165 Update docs/architecture/evidence-model.md`.

### GB-029 Primary Versus Secondary Source Policy

- `ID`: `GB-029`
- `Title`: Primary versus secondary source policy.
- `Status`: `Implemented`
- `Priority`: `Medium`
- `Area`: Evidence
- `Reason`: Source priority affects source preference and review expectations, while source type separately identifies what the source is, including maintainer analysis.
- `Suggested implementation`: Implemented in `docs/architecture/reference-model.md` under `Source Priority`, which defines Primary, Secondary, and Tertiary source roles and preference guidance, and in `schema/definitions/reference.schema.json`, which represents that distinction with the `sourcePriority` enum while separately representing `Maintainer Analysis` in the `sourceType` enum. This is documented and structured schema support rather than validator enforcement.
- `Related files`: `docs/architecture/reference-model.md`; `schema/definitions/reference.schema.json`
- `Depends on`: Implemented in commits `940baa7 Add docs/architecture/reference-model.md` and `5ed036d Add initial RKM architecture and JSON schemas`.

### GB-030 Claim Review Workflow

- `ID`: `GB-030`
- `Title`: Claim review workflow.
- `Status`: `Implemented`
- `Priority`: `Medium`
- `Area`: Evidence
- `Reason`: Claims need a repeatable review path for wording, support, scope, and source quality.
- `Suggested implementation`: Implemented in `docs/architecture/claim-model.md` under `Claim Review Path`, which documents checks for claim wording and scope, subject identity, claim type, qualifiers, evidence linkage and strength, confidence, relationship-facing wording, `Draft` to `Review` to `Published` transitions, reviewer questions, and corrective narrowing or splitting.
- `Related files`: `docs/architecture/claim-model.md`; `schema/claim.schema.json`; `data/relationship-support/`
- `Depends on`: Implemented in commit `af7f991 Update docs/architecture/claim-model.md`.

### GB-031 Citation Freshness And Staleness Policy

- `ID`: `GB-031`
- `Title`: Citation freshness and staleness policy.
- `Status`: `Implemented`
- `Priority`: `Medium`
- `Area`: Evidence
- `Reason`: RAG tooling changes quickly, so evidence may need recency expectations or review cadence.
- `Suggested implementation`: Implemented in `docs/architecture/reference-model.md` under `Reference Freshness and Staleness`, which evaluates freshness relative to the supported claim, evidence role, or relationship and applies source-sensitive expectations for mutable versus stable sources based on factors such as source type, source priority, update behavior, release cadence, version or access date, and downstream risk. It directs re-review when a source changes, a new major version is released, or downstream use depends on the claim, and recommends narrowing date-sensitive claims with evidence notes. `schema/definitions/reference.schema.json` supplies optional `updatedAt`, `accessedAt`, `version`, `canonicalUrl`, repository context, and `notes` metadata. This is documented review guidance plus optional metadata support, not automated staleness detection, reporting, or validator enforcement.
- `Related files`: `docs/architecture/reference-model.md`; `schema/definitions/reference.schema.json`
- `Depends on`: Implemented in commits `9d92683 Update docs/architecture/reference-model.md` and `5ed036d Add initial RKM architecture and JSON schemas`.

### GB-032 Task-Specific Command Generator

- `ID`: `GB-032`
- `Title`: Task-specific command generator.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Tooling
- `Reason`: Contributors need the right validation commands for each change type without memorizing the full Makefile.
- `Suggested implementation`: Generate recommended commands from changed paths, task type, and rule routing metadata.
- `Related files`: `Makefile`; `scripts/`; `docs/maintenance/task-guides/README.md`
- `Depends on`: `GB-005`.

### GB-033 Backlog Query Tooling

- `ID`: `GB-033`
- `Title`: Backlog query tooling.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Tooling
- `Reason`: Maintainers should be able to list open, high-priority, area-specific backlog entries quickly.
- `Suggested implementation`: Add a lightweight script that parses this backlog and emits filtered summaries by status, priority, and area.
- `Related files`: `docs/maintenance/governance-backlog.md`; `scripts/`; `Makefile`
- `Depends on`: Repository maintainer prioritization.

### GB-034 Cockpit Integration For Backlog Priorities

- `ID`: `GB-034`
- `Title`: Cockpit integration for backlog priorities.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Tooling
- `Reason`: Cockpit summaries should surface the most relevant planned governance work during operational handoff.
- `Suggested implementation`: Extend cockpit summary output to include selected open high-priority backlog entries.
- `Related files`: `docs/maintenance/governance-backlog.md`; `scripts/`; `Makefile`
- `Depends on`: `GB-033`.

### GB-035 Autopilot Mode Profiles

- `ID`: `GB-035`
- `Title`: Autopilot mode profiles.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Automation
- `Reason`: Different automation runs need clearer modes for content work, validation work, recovery, and release preparation.
- `Suggested implementation`: Define named autopilot profiles with explicit allowed change types, commands, and guardrails.
- `Related files`: `docs/maintenance/automation-guardrails.md`; `scripts/`; `Makefile`
- `Depends on`: Repository maintainer prioritization.

### GB-036 Autopilot Risk Tiers

- `ID`: `GB-036`
- `Title`: Autopilot risk tiers.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Automation
- `Reason`: Automation should distinguish low-risk content additions from structural contract changes.
- `Suggested implementation`: Add risk tier metadata for task types and enforce extra approvals or stops for higher-risk areas.
- `Related files`: `docs/maintenance/automation-guardrails.md`; `AGENTS.md`; `scripts/`; `Makefile`
- `Depends on`: Repository maintainer prioritization.

### GB-037 Rule Routing Summary Targets

- `ID`: `GB-037`
- `Title`: Rule routing summary targets.
- `Status`: `Proposed`
- `Priority`: `Medium`
- `Area`: Tooling
- `Reason`: Maintainers need concise summaries of applicable rules during handoff, review, and automation planning.
- `Suggested implementation`: Add Make targets that summarize routing requirements for changed paths and recent commits.
- `Related files`: `AGENTS.md`; `docs/maintenance/task-guides/README.md`; `scripts/validate-agent-routing.py`; `Makefile`
- `Depends on`: `GB-005`.

### GB-038 `v0.2.0` Planning Document

- `ID`: `GB-038`
- `Title`: `v0.2.0` planning document.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Release
- `Reason`: Post-alpha work on `main` needs a clear release planning surface without changing the existing alpha tag.
- `Suggested implementation`: Add a planning document that defines candidate scope, readiness gates, excluded work, and validation expectations for `v0.2.0`.
- `Related files`: `docs/releases/`; `CHANGELOG.md`; `docs/maintenance/maturity-report.md`
- `Depends on`: Repository maintainer prioritization.

### GB-039 Release Readiness Matrix

- `ID`: `GB-039`
- `Title`: Release readiness matrix.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Release
- `Reason`: Release readiness should be evaluated across validation, content, documentation, compatibility, and consumer usability.
- `Suggested implementation`: Add a matrix that maps release criteria to commands, documents, owners, and current status.
- `Related files`: `docs/releases/`; `docs/maintenance/maturity-report.md`; `docs/maintenance/task-guides/preparing-release.md`
- `Depends on`: Repository maintainer prioritization.

### GB-040 Granular Maturity Scorecard

- `ID`: `GB-040`
- `Title`: Granular maturity scorecard.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Maturity
- `Reason`: RKM maturity needs more precise signals than a single overall score.
- `Suggested implementation`: Implemented in `docs/maintenance/maturity-report.md` with diagnostic scores for conceptual model, schema, validation discipline, data, evidence, graph export, release, automation, and consumer documentation.
- `Related files`: `docs/maintenance/maturity-report.md`; `docs/maintenance/rule-coverage-report.md`
- `Depends on`: Implemented in commit `a2c302f Add granular RKM maturity scorecard`.

### GB-041 Changelog Discipline Validator

- `ID`: `GB-041`
- `Title`: Changelog discipline validator.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Release
- `Reason`: Release and governance changes should be recorded consistently under `CHANGELOG.md` `Unreleased`.
- `Suggested implementation`: Add validation or release-check support that detects relevant changed files and requires an appropriate changelog entry.
- `Related files`: `CHANGELOG.md`; `docs/maintenance/task-guides/preparing-release.md`; `scripts/`; `Makefile`
- `Depends on`: Repository maintainer prioritization.

### GB-042 Autopilot Per-Cycle Timeout

- `ID`: `GB-042`
- `Title`: Autopilot per-cycle timeout.
- `Status`: `Implemented`
- `Priority`: `High`
- `Area`: Automation
- `Reason`: `make autopilot N=1` can still run for many hours when the underlying cycle remains active.
- `Implementation`: `Makefile` passes `PER_CYCLE_TIMEOUT_SECONDS` into `RKM_PER_CYCLE_TIMEOUT_SECONDS`, and `scripts/rkm-autocycle.sh` enforces that positive-integer timeout with GNU `timeout` around each underlying `rkm-cycle.sh` attempt. `scripts/rkm-autopilot.py` treats timeout exit 124 as an inspect-only stop and does not run automatic `safe-push` after that failure.
- `Command examples`: `make autopilot N=1 PER_CYCLE_TIMEOUT_SECONDS=1800`; `make autocycle N=1 PER_CYCLE_TIMEOUT_SECONDS=1800`
- `Related files`: `scripts/rkm-autopilot.py`; `scripts/rkm-autocycle.sh`; `scripts/rkm-cycle.sh`; `docs/maintenance/task-guides/unattended-autopilot.md`; `docs/maintenance/automation-guardrails.md`
- `Depends on`: Implemented.

### GB-043 Data Route Side-Effect Guidance

- `ID`: `GB-043`
- `Title`: Data route side-effect guidance.
- `Status`: `Implemented`
- `Priority`: `Medium`
- `Area`: Automation
- `Reason`: Data-only commits can legitimately update `data/manifest.json` and generated data graph export artifacts.
- `Suggested implementation`: Implemented through task router output and data-record task-guide guidance.
- `Related files`: `scripts/rkm-route-task.py`; `docs/maintenance/task-guides/adding-data-records.md`; `data/manifest.json`; `examples/data-graph-export/`
- `Depends on`: `GB-005 Task router CLI`.
### GB-044 Adaptive Codex Model Routing And Token Budgeting

- `ID`: `GB-044`
- `Title`: Adaptive Codex model routing and token budgeting.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Automation
- `Reason`: Current Codex execution paths largely inherit the user-level `gpt-5.6-sol` model with `high` reasoning effort, while the configured Worker and Reviewer agents also default to `high`. This applies expensive reasoning to bounded documentation, mechanical inspection, and semantic architecture work alike. Deterministic repository checks already cover many factual invariants, but RKM has no execution-profile selector that separates zero-model checks, low-cost bounded work, standard engineering tasks, and high-risk strategic reasoning.
- `Suggested implementation`: Define a deterministic-first execution policy; add a path- and task-aware selector for Creator, Reviewer, and escalation profiles; create configurable named Codex profiles; generate compact evidence bundles before semantic review; skip model calls when shell, Python, Git, Make, or schema validation can decide the result; require stronger profiles for architecture, schema, ontology, cross-cutting automation, and integration work; log selected model, reasoning effort, context budget, result, and escalation reason; and add self-tests plus integration coverage for cycle, discovery, recovery, commit, Director, and autopilot paths. Initial candidate bindings are GPT-5.4 Mini for strictly mechanical model-assisted work, GPT-5.6 Luna for low-risk bounded semantic work, GPT-5.6 Terra for standard engineering and semantic review, and GPT-5.6 Sol for architecture, strategy, conflicts, and high-risk decisions. Exact model bindings must remain configurable and be checked against current Codex availability rather than treated as permanent contracts.
- `Related files`: `scripts/rkm-select-execution-profile.py`; `scripts/rkm-codex-exec.py`; `scripts/rkm-route-task.py`; `scripts/rkm-cycle.sh`; `scripts/rkm-discover.sh`; `scripts/rkm-recover-revise.sh`; `scripts/rkm-codex-commit.sh`; `scripts/rkm-director.sh`; `scripts/rkm-budget.py`; `.codex/config.toml`; `.codex/agents/`; `docs/maintenance/codex-execution-policy.md`; `docs/maintenance/automation-guardrails.md`; `Makefile`
- `Depends on`: `GB-005 Task Router CLI`; `GB-035 Autopilot Mode Profiles`; `GB-036 Autopilot Risk Tiers`; existing token-budget and run-ledger tooling.

### GB-045 External RAG Evidence And Recommendation Persistence

- `ID`: `GB-045`
- `Title`: External RAG evidence and recommendation persistence.
- `Status`: `Proposed`
- `Priority`: `High`
- `Area`: Evidence
- `Reason`: The RAG-to-RKM consumer walkthrough proves structural envelope
  interoperability, but the current fixture is compatibility evidence rather
  than a live externally sourced evaluation and the adapter does not persist
  recommendations into canonical RKM Evaluation, Artifact, or Policy Decision
  records.
- `Suggested implementation`: Add a separately reviewed ingestion path for
  immutable lab artifacts, preserve source and corpus hashes, record external
  references and review state, validate compatibility before persistence, and
  demonstrate at least one downstream loader using a real provider-free or
  externally sourced report.
- `Related files`: `docs/maintenance/rag-recommendation-consumer-walkthrough.md`;
  `docs/maintenance/task-packets/RKM-001-downstream-consumer-walkthrough.md`;
  `scripts/import-rag-recommendation-artifact.py`;
  `schema/rag-recommendation-artifact-adapter-v1.schema.json`;
  `data/`; `schema/`; `docs/maintenance/maturity-report.md`
- `Depends on`: `RKM-001`; explicit provenance, lifecycle, compatibility, and
  review decisions; no automatic production promotion.
