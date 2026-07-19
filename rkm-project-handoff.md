# RAG Knowledge Model: Complete Project Hand-off

## Document purpose

This document transfers the current RAG Knowledge Model project state to another LLM, maintainer, or paired engineering agent. It is intentionally comprehensive. It explains the product scope, the repository's conceptual and operational architecture, what has been built, how it was built, how to trace each implemented capability through the repository, what remains specified but unimplemented, what remains merely proposed, and how to continue from the exact repository state recorded below.

This is a state-transfer document, not a replacement for repository rules or live inspection. The receiving agent must use it to orient itself, then verify every dynamic fact with the commands in the start protocol.

## Snapshot identity

This hand-off was prepared on 2026-07-19 UTC from the repository root.

| Fact | Snapshot value |
| --- | --- |
| Repository | RAG Knowledge Model, abbreviated RKM |
| Current branch | `experiment/codex-director` |
| Current commit before this hand-off file | `913e04fb41dc645e1eae3942b26a222bf54f50cd` |
| Commit subject | `Correct Memgraph artifact license` |
| Current upstream | `origin/experiment/codex-director` |
| Upstream alignment before this hand-off file | ahead 0, behind 0 |
| Local `main` | `e3e02681e287879e13819493b057e64a99b5c270` |
| Local `origin/main` | `e3e02681e287879e13819493b057e64a99b5c270` |
| Current branch relationship to `main` | `main` and `origin/main` are ancestors of current `HEAD` |
| Commits on current branch after `main` | 78 |
| Autonomous Product Director branch | `experiment/autonomous-product-director` at `53c9d5b8e97730a1ee9cc5e0391893a08cc75775` |
| Current branch commits after that branch tip | 75 |
| Tagged internal alpha | `v0.1.0-alpha` at `18801f31f96d0ae8cdf0d8e3babd32b5bdc3cf98` |
| Commits from the tag to `main` | 62 |
| Worktree before creating this file | clean |
| Recovery state before creating this file | `NO_RECOVERY_NEEDED` |
| Live cockpit recommendation before this task | `RUN`, normally `make autopilot N=5` |

The final validation and Git status produced during creation of this document are recorded in the final section. Because this file is intentionally created without a commit, a receiving agent must not assume the worktree is clean until it runs `git status --short`.

## Fifteen-minute receiving-agent protocol

Start in the repository root and do this before selecting or implementing work:

1. Read [AGENTS.md](AGENTS.md) completely.
2. Read this document completely.
3. Read [README.md](README.md), [QUICKSTART.md](QUICKSTART.md), and [Makefile](Makefile).
4. Run `git status --short --branch`.
5. Run `git branch -vv`.
6. Run `git log --oneline --decorate -n 20`.
7. Run `make cockpit-summary N=5`.
8. Run `make validate` before treating the checkout as healthy.
9. If a change is requested, run `make route-task PATHS="<space-separated intended paths>"` before editing.
10. Read every local `AGENTS.md` and task guide named by the router.

Use these commands to confirm the exact protected-ref relationship when branch safety matters:

```bash
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git merge-base --is-ancestor main HEAD
git merge-base --is-ancestor origin/main HEAD
```

A zero exit code from both ancestry checks is required by the autonomous product experiment contracts. Equality is not the same fact as ancestry; preserve that distinction.

## Authority and precedence

When sources appear to disagree, use this order:

1. The current human request defines the task and authorization boundary.
2. [AGENTS.md](AGENTS.md) defines repository-wide rules.
3. The nearest local `AGENTS.md` defines area-specific rules.
4. The relevant task guide defines the operational procedure for that change type.
5. Schemas, registries, manifests, source data, and executable validation define machine-enforced contracts.
6. Canonical entity JSON defines the present lifecycle and knowledge state of that entity.
7. Current source code defines implemented behavior.
8. Current generated artifacts define committed consumer views only when validation proves them fresh.
9. Architecture and maintenance documentation explain intent and rationale.
10. Historical review artifacts remain authoritative only for their pinned commits and digests.
11. This hand-off explains the snapshot but does not override any source above it.

For dynamic operational state, `make cockpit-summary N=5`, `make recovery-plan`, `make budget-report`, `git status --short`, and `make validate` outrank static prose.

## Executive project summary

RKM is a structured, human-readable and machine-readable model of the Retrieval-Augmented Generation ecosystem. It is simultaneously:

- a domain model;
- an ontology foundation;
- a family of JSON Schema Draft 2020-12 contracts;
- a registry-governed vocabulary;
- a populated but still limited knowledge dataset;
- a claim, evidence, reference, and relationship traceability system;
- a deterministic graph-export source;
- a decision-support surface;
- a validation-first repository operating system for disciplined model evolution.

RKM is not a simple product catalog. It models identities, descriptions, domain knowledge, relationships, claims, evidence, references, metadata, lifecycle, provenance, and consumer projections as distinct but connected concepts.

RKM is not production-ready, not a stable public API, not a complete RAG ecosystem catalog, and not yet a packaged downstream knowledge service. The strongest parts are repository discipline, validation, schemas, modeling breadth, and automation. The weakest parts are externally reviewed data breadth, loader demonstrations, compatibility policy, synchronized consumer documentation, and broad release packaging.

The repository's static maturity report rates the system at roughly 3.5 out of 5. That report predates the current vector-database expansion, so its reasoning remains useful but several inventory statements are no longer current.

## Product boundaries

### In scope

RKM is designed to support:

- stable identification of RAG-relevant entities;
- explicit domain relationships with controlled predicates;
- evidence-backed and limitation-aware claims;
- reusable embedded definitions and specialized first-class schemas;
- validated seed knowledge records;
- deterministic graph projections;
- machine-readable decision views;
- internal evaluation and consumer onboarding;
- future loaders for graph, document, search, vector, RDF, API, and evaluation-oriented systems;
- disciplined AI-assisted maintenance.

### Out of scope at the current maturity level

The current repository does not provide:

- a comprehensive catalog;
- live product telemetry;
- universal product rankings;
- benchmark-normalized recommendations across unlike evaluations;
- production database loaders;
- a stable graph-export compatibility guarantee;
- a public hosted API;
- autonomous promotion to `main`;
- an implemented Autonomous Product Director v2 runtime.

### Epistemic boundary

The project distinguishes external empirical evidence, official documentation, repository facts, modeled relationships, maintainer analysis, interpretations, inferences, hypotheses, and observed test results. These categories must not be collapsed.

A modeled relationship is not performance evidence. A passing schema validator is not factual review. Matching comparison fields do not prove semantic equivalence. Missing data means not recorded unless the record explicitly says unsupported. `Approved` review state applies only to the exact artifact and scope that received review.

## Version and branch strata

The repository contains four materially different historical strata.

| Stratum | Commit | Meaning |
| --- | --- | --- |
| Internal alpha tag | `18801f3` | First intentionally tagged internal evaluation package with schemas, fixtures, initial seed data, fixture graph export, validation, release notes, and release check. |
| Current `main` | `e3e0268` | Post-alpha foundation including data graph export, semantic relationship validation, relationship support, broader seed techniques and components, governance routing, bounded Director tooling, and initial decision-query entity and pipeline views. |
| Autonomous Product Director branch tip | `53c9d5b` | Product Director constitution plus the complete v2 machine-oriented loop contract. This is specification work, not a runtime implementation. |
| Current branch | `913e04f` | Current `main` plus Product Director specifications plus 17 VectorDatabase records, comparison mode, vector modeling refinements, independent Neo4j acceptance provenance, graph-export expansion, and recent artifact-license corrections. |

Never describe branch-only vector-database or Product Director work as part of the tagged alpha. Never describe a specification as executable merely because it is detailed.

## What was done, in chronological phases

### Phase 1: conceptual foundation

The project established a layered entity model, ubiquitous terminology, identity, metadata, description, relationship, claim, evidence, reference, ontology, naming, and versioning rules. The architectural decision record [ADR-0001](docs/architecture/ADR-0001-adopt-knowledge-entity-model.md) captures the adoption of the knowledge-entity approach.

The key modeling decision was to avoid string-only or prose-only knowledge. Durable IDs, explicit types, structured domain sections, controlled relationships, and evidence links became foundational.

### Phase 2: schema and registry foundation

The repository introduced reusable definitions under `schema/definitions/`, specialized entity contracts under `schema/`, and controlled entity and relationship registries under `registries/`. Schema validation was expanded beyond JSON syntax to include prerequisites, semantic contracts, and duplicate-contract safeguards.

### Phase 3: fixtures, seed data, and the alpha package

Minimal fixtures demonstrated a technique, relationship, claim, evidence object, and reference. A deterministic fixture graph export made those fixtures loadable as nodes and edges. The initial seed data established a real-data path distinct from pedagogical fixtures. The `v0.1.0-alpha` tag and release-check workflow created an internal evaluation checkpoint.

### Phase 4: post-alpha data graph and semantic relationships

The project added a data-derived graph export, formal graph node and edge schemas, explicit relationship sets, semantic endpoint checks, relationship support sets, Component data, Retriever data, Reranker data, and chunking technique records. Generated data graph artifacts became validation-checked contracts.

### Phase 5: governance and operations

The repository distributed agent rules into root and local `AGENTS.md` files, added task guides, routing validation, a task router, rule coverage reporting, governance backlog tracking, budget controls, cockpit output, recovery planning, safe push, autopilot, bounded cycles, commit automation, and per-cycle timeouts.

### Phase 6: bounded Codex Director experiment

The project added a branch-locked launcher, a detailed Director operating contract, a write-capable Worker configuration, and a read-only Reviewer configuration. The Director selects one bounded task, delegates implementation, independently inspects the diff, requests independent review, validates accepted work, commits, and publishes only through `make safe-push`.

This bounded Director is implemented. Its task is already selected and scoped before implementation. It is not the same system as the later Autonomous Product Director.

### Phase 7: evidence-backed decision query

The decision-query CLI began with source-linked entity briefs for Hybrid Retrieval and Reranking, then added pipeline composition. Compact and full text views expose different presentation density while JSON always preserves the complete decision model.

### Phase 8: Autonomous Product Director specification

The repository defined a higher supervisory layer that begins from a product mission rather than a preselected task. The constitution defines product values, observation, diagnosis, alternatives, selection, acceptance, delegation, independent review, external verification, branch boundaries, escalation, and stop behavior.

The v2 loop contract then specified an atomic runtime protocol with immutable numbered artifacts, an explicit state machine, exact Git observation, exact agent process supervision, budget charging, recovery, finalization, modular validators, a thin public facade, and a comprehensive conformance suite.

This phase produced normative documents only. The corresponding launcher, state facade, validator modules, runtime artifact implementation, and tests do not exist yet.

### Phase 9: VectorDatabase decision surface and dataset expansion

The current branch added VectorDatabase support to the decision-query projection, then added 17 records in repeated validated increments. Each record was added, declared in `data/manifest.json`, and projected into the data graph export. Comparison mode was then added for two to eight entities of the same canonical entity type.

### Phase 10: vector-database semantic hardening

Independent comparison review exposed misleading equivalence risks around modalities, filtering, hybrid retrieval, score fusion, scaling, sharding, replication, disk behavior, consistency, transactions, security, operations, tenancy, evidence granularity, mutable sources, and licensing scope.

The project responded by refining vector-database architecture semantics, adding embedded structured capabilities, modeling capability origins and availability scope, distinguishing graph-plus-vector composition from lexical-vector fusion, and separating product licensing from the license of the RKM JSON artifact.

### Phase 11: Neo4j deep correction and independent approval

Neo4j received substantially deeper treatment than the other 16 records. Claims, evidence, references, capability boundaries, deployment and edition scope, encryption, recovery, consistency, sharding, observability, tenancy, hybrid patterns, licensing, and immutable provenance were corrected through multiple commits.

An independent acceptance run returned `ACCEPT`. Commit `a617864` advanced the record to version `1.5.1` and `metadata.reviewState: Approved` without changing the accepted substantive content. The durable provenance chain is indexed in [neo4j-1.5.1-independent-acceptance.md](docs/reviews/vector-databases/neo4j-1.5.1-independent-acceptance.md).

### Phase 12: protected integration and historical review clarification

The dataset expansion history was merged into `experiment/codex-director` at `b41b206`. Historical reviewer artifacts were explicitly labeled as commit-bound snapshots so their earlier `Not Reviewed`, `Changes Requested`, and `REVISION REQUIRED` statements would not be mistaken for Neo4j's current state. Recent commits corrected the RKM artifact license on Neptune Analytics and Memgraph.

## Core mental model

### Entity layers

The conceptual hierarchy is:

```text
Entity
  -> Knowledge Entity
       -> Specialized Entity
```

An Entity owns durable identity and lifecycle. A Knowledge Entity adds descriptions, relationships, claims, evidence, references, and domain knowledge. A Specialized Entity adds a typed domain section such as `technique`, `retriever`, `reranker`, or `vectorDatabase`.

### Canonical record envelope

A typical first-class data record has:

```text
identity
metadata
description
relationships, when embedded relationships are appropriate
claims
evidence
references
externalLinks
specialized domain section
```

Identity is not metadata. Metadata is not domain knowledge. Evidence is not a raw URL. A reference identifies a source; evidence explains how that source bears on a claim; a claim is the explicit proposition.

### Stable identity

Use stable uppercase identifiers as join keys. Slugs and human names aid lookup and display but are not the durable cross-file contract. Preserve `identity.id` when revising an entity.

### Relationships

Relationships are directional, typed, and explicit. Predicates are uppercase snake case. For populated data, domain graph edges are emitted only from declared relationship-set files. The exporter must not infer edges from names, descriptions, stages, roles, capabilities, or likely architecture.

### Evidence chain

The intended trace is:

```text
subject or relationship
  -> claim
       -> evidence
            -> reference
```

Claims may cite references directly as well. Evidence records a role such as support, qualification, contradiction, definition, or evaluation. Strength and confidence must be calibrated and bounded by source scope.

### Metadata and product licensing

`metadata.license` describes the RKM artifact. A vendor product's licensing belongs in structured domain knowledge, currently `vectorDatabase.productLicensing` for VectorDatabase records. Do not replace the artifact license with a vendor's commercial terms.

### Embedded definition versus first-class entity

Reusable definitions can describe embedded concepts without making those concepts independent entities. The current `schema/definitions/capability.schema.json` is explicitly an embedded capability fragment. It has no first-class identity and lifecycle envelope. A first-class Capability would require a separate, intentionally authorized model package.

## Repository map and how to read it

| Area | What it is | Start here | Source-of-truth role |
| --- | --- | --- | --- |
| Root | Project entry points and global operating contract | [README.md](README.md), [QUICKSTART.md](QUICKSTART.md), [AGENTS.md](AGENTS.md), [Makefile](Makefile) | Orientation, commands, repository constitution |
| `docs/architecture/` | Conceptual and semantic model | [domain-model.md](docs/architecture/domain-model.md), [entity-model.md](docs/architecture/entity-model.md), [ontology.md](docs/architecture/ontology.md) | Normative modeling intent |
| `schema/` | First-class contracts and package contracts | [schema/AGENTS.md](schema/AGENTS.md), then the affected schema | Machine structure |
| `schema/definitions/` | Reusable embedded fragments | `identity`, `metadata`, `description`, `relationship`, `claim`, `evidence`, `reference` first | Shared machine structure |
| `registries/` | Controlled vocabularies | [registries/AGENTS.md](registries/AGENTS.md), entity and relationship registries | Allowed type and predicate vocabulary |
| `data/` | Populated knowledge | [data/AGENTS.md](data/AGENTS.md), [data/manifest.json](data/manifest.json), affected records | Canonical populated content |
| `data/relationships/` | Explicit domain edges between populated records | [relationships README](data/relationships/README.md) | Canonical declared relationship instances |
| `data/relationship-support/` | Claims, evidence, and references supporting relationship inclusion | [relationship-support README](data/relationship-support/README.md) | Canonical support trace for declared edges |
| `examples/fixtures/` | Minimal pedagogical and validation instances | [fixtures README](examples/fixtures/README.md) | Small examples, not real catalog data |
| `examples/graph-export/` | Fixture-derived graph view | [graph-export README](examples/graph-export/README.md) | Generated fixture projection |
| `examples/data-graph-export/` | Data-derived graph view | [data-graph-export README](examples/data-graph-export/README.md) | Generated data projection |
| `scripts/` | Validators, exporters, decision query, automation, recovery, release, and Director launcher | [scripts/AGENTS.md](scripts/AGENTS.md) and [Makefile](Makefile) | Executable behavior |
| `.codex/` | Bounded Director Worker and Reviewer definitions | [.codex/config.toml](.codex/config.toml) | Agent configuration |
| `.rkm/` | Local ignored budget, ledger, and autopilot state | Inspect only through Make targets or scripts | Mutable local state, not canonical repository content |
| `docs/maintenance/` | Consumer, governance, automation, hand-off, and experimental contracts | [assistant-handoff.md](docs/maintenance/assistant-handoff.md), [repo-map.md](docs/maintenance/repo-map.md) | Operational and strategic explanation |
| `docs/releases/` | Release notes and release index | [v0.1.0-alpha.md](docs/releases/v0.1.0-alpha.md) | Historical release scope |
| `docs/reviews/` | Commit-bound review and approval provenance | Read current-state notice first | Review history, not always current lifecycle |

## Architecture documentation reading order

For a general model change, read in this order:

1. [domain-model.md](docs/architecture/domain-model.md)
2. [entity-model.md](docs/architecture/entity-model.md)
3. [identity-model.md](docs/architecture/identity-model.md)
4. [metadata-model.md](docs/architecture/metadata-model.md)
5. [description-model.md](docs/architecture/description-model.md)
6. [relationship-model.md](docs/architecture/relationship-model.md)
7. [claim-model.md](docs/architecture/claim-model.md)
8. [evidence-model.md](docs/architecture/evidence-model.md)
9. [reference-model.md](docs/architecture/reference-model.md)
10. [ontology.md](docs/architecture/ontology.md)
11. [ubiquitous-language.md](docs/architecture/ubiquitous-language.md)
12. [naming-conventions.md](docs/architecture/naming-conventions.md)
13. [versioning.md](docs/architecture/versioning.md)
14. The specialized model document for the entity or concept being changed.

Specialized documents cover techniques, components, retrievers, rerankers, vector and graph databases, models, frameworks, providers, agents, datasets, benchmarks, evaluation metrics, chunking, prompts, workflows, tools, security, storage, deployment, observability, risk, policy, quality attributes, tradeoffs, limitations, and related concepts.

Do not infer that every architecture document corresponds to a populated entity type. Architecture breadth, schema breadth, registry breadth, and populated data breadth are intentionally different.

## Schema inventory

The current branch has 26 top-level schemas and 41 reusable definitions.

### Top-level schemas

First-class entity schemas:

- `agent.schema.json`
- `benchmark.schema.json`
- `chunking-strategy.schema.json`
- `component.schema.json`
- `dataset.schema.json`
- `embedding-model.schema.json`
- `evaluation-metric.schema.json`
- `framework.schema.json`
- `glossary.schema.json`
- `graph-database.schema.json`
- `language-model.schema.json`
- `paper.schema.json`
- `pattern.schema.json`
- `prompt-technique.schema.json`
- `provider.schema.json`
- `rag-technique.schema.json`
- `reranker.schema.json`
- `retriever.schema.json`
- `vector-database.schema.json`

Registry, ontology, relationship, and graph schemas:

- `entity-type-registry.schema.json`
- `relationship-type-registry.schema.json`
- `ontology.schema.json`
- `relationship-set.schema.json`
- `relationship-support-set.schema.json`
- `graph-node.schema.json`
- `graph-edge.schema.json`

### Shared definition groups

Core envelope definitions include identity, metadata, description, knowledge entity, artifact, entity reference, entity type, external link, and model.

Knowledge traceability definitions include relationship, relationship type, claim, evidence, reference, citation, advantage, limitation, tradeoff, problem, anti-pattern, risk, and quality attribute.

RAG and system definitions include retrieval, indexing, query, context assembly, RAG pipeline, memory, storage, workflow, tool, tool contract, use case, evaluation, observable signal, policy, security control, deployment context, cost, and capability.

### Schema rules that matter most

- Every schema uses JSON Schema Draft 2020-12.
- `$id` values are stable and RKM-namespaced.
- Specialized `identity.entityType` constants must already be supported by shared identity and registry contracts.
- Required fields, enums, and identifier patterns must not be silently loosened.
- A same-name reusable definition and first-class schema must compose rather than evolve independently.
- Schema work is contract evolution and requires explicit task-specific authorization.
- Schema changes normally require examples, self-tests, documentation, and downstream compatibility analysis.

## Registry inventory

The entity-type registry currently contains 19 published stable entity types:

`Technique`, `Framework`, `Paper`, `Component`, `Pattern`, `Glossary`, `Dataset`, `Benchmark`, `EmbeddingModel`, `LanguageModel`, `VectorDatabase`, `GraphDatabase`, `Retriever`, `Reranker`, `ChunkingStrategy`, `EvaluationMetric`, `PromptTechnique`, `Agent`, and `Provider`.

The relationship-type registry contains 61 published predicates across Structural, Dependency, Implementation, Provenance, Knowledge, Evaluation, Compatibility, Workflow, Quality, and Lifecycle categories.

The complete predicate set is:

`EXTENDS`, `SPECIALIZES`, `GENERALIZES`, `BELONGS_TO`, `PART_OF`, `CONTAINS`, `REQUIRES`, `DEPENDS_ON`, `USES`, `OPTIONALLY_USES`, `CONSUMES`, `PRODUCES`, `TRANSFORMS`, `IMPLEMENTS`, `SUPPORTS`, `PROVIDES`, `INTEGRATES_WITH`, `EXPOSES`, `INTRODUCES`, `DESCRIBES`, `DEFINES`, `REFERENCES`, `CITES`, `AUTHORED_BY`, `PUBLISHED_IN`, `INSPIRED_BY`, `EVALUATES`, `EVALUATED_BY`, `MEASURES`, `VALIDATES`, `BENCHMARKED_BY`, `ACHIEVES_SCORE_ON`, `COMPATIBLE_WITH`, `INCOMPATIBLE_WITH`, `ALTERNATIVE_TO`, `COMPLEMENTS`, `SUPERSEDES`, `REPLACED_BY`, `PRECEDES`, `FOLLOWS`, `EXECUTES`, `TRIGGERS`, `ROUTES_TO`, `BRANCHES_TO`, `SOLVES`, `MITIGATES`, `HAS_ADVANTAGE`, `HAS_LIMITATION`, `HAS_TRADEOFF`, `HAS_USE_CASE`, `HAS_ANTI_PATTERN`, `HAS_COMMON_MISTAKE`, `DEPLOYED_WITH`, `OBSERVED_BY`, `MONITORED_BY`, `LOGGED_BY`, `SECURED_BY`, `GOVERNED_BY`, `CAN_PRECEDE_IN_PIPELINE`, `CAN_PROVIDE_CANDIDATES_TO`, and `CAN_REFINE_RESULTS_FROM`.

Before proposing a new predicate, inspect the registry and reuse an existing semantic fit. Hard-dependency predicates require especially strong justification.

## Current populated data snapshot

### Manifest structure

[data/manifest.json](data/manifest.json) contains one flat `data` array. Each item maps a repository-relative JSON file to its validating schema. Entity records, relationship sets, and relationship support sets are all declared through this array.

The manifest currently declares 36 files:

- 30 entity records;
- 3 relationship sets;
- 3 relationship support sets.

### Entity records by type

| Type | Count | Records |
| --- | ---: | --- |
| Technique | 6 | Hybrid Retrieval, Query Rewriting, Reranking, Fixed-Size Chunking, Recursive Chunking, Semantic Chunking |
| Component | 4 | Keyword Retriever, Semantic Retriever, Rank Fusion, Cross-Encoder Reranker |
| Retriever | 2 | Lexical Retriever, Embedding Retriever |
| Reranker | 1 | Cross-Encoder Reranker |
| VectorDatabase | 17 | Listed below |

Every current entity record has artifact status `Draft`. Twenty-nine have review state `Not Reviewed`. Neo4j alone has review state `Approved`.

Across the 30 entity records at this snapshot, there are 115 embedded claims, 110 embedded evidence objects, and 242 embedded references. These counts measure recorded content, not quality.

### VectorDatabase records

| ID | Slug | Current review state | Claim, evidence, reference counts |
| --- | --- | --- | --- |
| `VECTOR-DATABASE-10001` | `pgvector` | Not Reviewed | 5, 5, 4 |
| `VECTOR-DATABASE-10002` | `qdrant` | Not Reviewed | 5, 5, 9 |
| `VECTOR-DATABASE-10003` | `weaviate` | Not Reviewed | 5, 5, 9 |
| `VECTOR-DATABASE-10004` | `milvus` | Not Reviewed | 5, 5, 9 |
| `VECTOR-DATABASE-10005` | `pinecone` | Not Reviewed | 5, 5, 10 |
| `VECTOR-DATABASE-10006` | `chroma` | Not Reviewed | 5, 5, 10 |
| `VECTOR-DATABASE-10007` | `elasticsearch` | Not Reviewed | 5, 5, 10 |
| `VECTOR-DATABASE-10008` | `opensearch` | Not Reviewed | 5, 5, 11 |
| `VECTOR-DATABASE-10009` | `redis` | Not Reviewed | 5, 5, 11 |
| `VECTOR-DATABASE-10010` | `mongodb` | Not Reviewed | 5, 5, 14 |
| `VECTOR-DATABASE-10011` | `neo4j` | Approved | 18, 13, 30 |
| `VECTOR-DATABASE-10012` | `lancedb` | Not Reviewed | 5, 5, 15 |
| `VECTOR-DATABASE-10013` | `vespa` | Not Reviewed | 5, 5, 15 |
| `VECTOR-DATABASE-10014` | `azure-ai-search` | Not Reviewed | 5, 5, 17 |
| `VECTOR-DATABASE-10015` | `vertex-ai-vector-search` | Not Reviewed | 5, 5, 20 |
| `VECTOR-DATABASE-10016` | `amazon-neptune-analytics` | Not Reviewed | 5, 5, 20 |
| `VECTOR-DATABASE-10017` | `memgraph` | Not Reviewed | 5, 5, 20 |

The repeated five-claim and five-evidence shape on 16 records is a review risk, not proof of balanced coverage. The historical independent reviewer pack explicitly questioned whether those counts reflect an authoring template. Neo4j's later depth must not be projected onto the other records.

### Relationship data

The three relationship sets contain 13 explicit domain relationships:

- 6 technique-to-technique relationships;
- 4 technique-to-component `OPTIONALLY_USES` relationships;
- 3 Retriever or Reranker to Component `SPECIALIZES` relationships.

Predicate distribution is:

- `CAN_PRECEDE_IN_PIPELINE`: 4;
- `CAN_PROVIDE_CANDIDATES_TO`: 1;
- `CAN_REFINE_RESULTS_FROM`: 1;
- `OPTIONALLY_USES`: 4;
- `SPECIALIZES`: 3.

The three support sets contain 13 claims, 13 evidence objects, and 4 references. Their sources are conservative `Maintainer Analysis`, not independent empirical evidence.

### What populated data does not yet cover

The registries and schemas are much broader than the populated dataset. There are no populated first-class records yet for Framework, Paper, Dataset, Benchmark, EmbeddingModel, LanguageModel, GraphDatabase, ChunkingStrategy as its own entity type, EvaluationMetric, PromptTechnique, Agent, Provider, Pattern, or Glossary. Some of those concepts appear as embedded knowledge or architecture documents, which is not the same as populated first-class data.

## Graph exports

### Fixture graph export

The fixture export contains 5 nodes and 5 edges.

Nodes:

- one Technique;
- one minimal Component endpoint;
- one Claim;
- one Evidence;
- one Reference.

Edges:

- `DEPENDS_ON`;
- `HAS_ADVANTAGE`;
- `SUPPORTS`;
- `REFERENCES`;
- `CITES`.

Generate it with `make graph-export`. Check freshness with `python3 scripts/export-fixtures-graph.py --check`.

### Data graph export

The current data export contains 35 nodes and 43 edges.

Node distribution:

- 6 Technique;
- 4 Component;
- 2 Retriever;
- 1 Reranker;
- 17 VectorDatabase;
- 5 Schema.

Edge distribution:

- 30 `VALIDATED_BY_SCHEMA` provenance edges;
- 13 declared domain edges with the predicate distribution described above.

Generate it with `make data-graph-export`. Check freshness with `python3 scripts/export-data-graph.py --check`.

The filenames `rag-techniques.nodes.json` and `rag-techniques.edges.json` are now narrower than their content. Do not rename them casually because filenames are consumer-visible and exporter-controlled.

### Export authority and limitations

Source records, relationship sets, support sets, schemas, and the manifest remain authoritative. Exports are deterministic derived views. Relationship-support claims, evidence, and references are currently represented as edge metadata links, not full nodes in the data export. Package metadata, stable compatibility policy, and loader mappings are still evolving.

## Implemented functionality and how to trace it

### Full validation pipeline

Public command: `make validate`

Primary implementation: [scripts/validate-rkm.sh](scripts/validate-rkm.sh)

The pipeline performs, in order:

1. Git whitespace validation.
2. UTF-8, line-ending, final-newline, and invisible-character validation for changed files.
3. Forbidden project-name validation.
4. Incomplete-content marker validation.
5. IDE-file detection.
6. Temporary-review-file detection.
7. JSON Schema validation.
8. Schema prerequisite validation.
9. Schema contract validation.
10. Duplicate schema contract validation.
11. Registry validation.
12. Fixture instance validation.
13. Data instance and semantic validation.
14. Fixture graph export freshness validation.
15. Data graph export freshness validation.
16. Graph schema and endpoint validation.
17. RKM unit tests.
18. Documentation relationship validation.
19. Distributed agent routing validation.

The shell script prints Git status on exit. A pass means the wired contracts are coherent; it does not imply that every fact is independently reviewed.

### Decision-query CLI

Public implementation: [scripts/rkm-decision-query.py](scripts/rkm-decision-query.py)

Help command:

```bash
python3 scripts/rkm-decision-query.py --help
```

Modes:

- `--entity ENTITY`: one exact entity lookup by ID, slug, display name, or official name.
- `--pipeline ENTITY_A ENTITY_B`: exactly two resolved entities in requested stage order.
- `--compare ENTITY_1 ENTITY_2 [additional entities]`: two through eight distinct entities of the same canonical entity type.

Output controls:

- `--format text` is the default.
- `--format json` returns the complete model.
- `--detail compact` is the default text presentation.
- `--detail full` includes all recorded qualifiers, evidence details, limitations, and source metadata.
- JSON output is complete and identical regardless of text-detail choice.

The entity view returns entity identity and lifecycle, summary, operational characteristics, implementation considerations, evaluation guidance, claims, evidence, references, warnings, and residual limitations.

The pipeline view returns requested order, stage briefs, direct canonical relationships, cautions, and an evaluation checklist. It does not claim universal ordering or comparable performance.

The comparison view flattens lifecycle, operational-characteristic, and evidence-coverage profiles. Rows are marked `Same`, `Different`, or `Incomplete`. Lists are compared order-independently for display. The comparison is deterministic and non-ranking. It does not select a winner.

Useful examples:

```bash
python3 scripts/rkm-decision-query.py --entity hybrid-retrieval
python3 scripts/rkm-decision-query.py --entity neo4j --detail full
python3 scripts/rkm-decision-query.py --pipeline hybrid-retrieval reranking
python3 scripts/rkm-decision-query.py --compare pgvector neo4j
python3 scripts/rkm-decision-query.py --compare neo4j amazon-neptune-analytics memgraph --format json
```

The built-in self-test is invoked by `scripts/rkm-unit-tests.sh` and therefore by `make validate`.

### Task routing

Public command:

```bash
make route-task PATHS="data/example.json schema/example.schema.json"
```

Implementation: [scripts/rkm-route-task.py](scripts/rkm-route-task.py)

The router maps intended paths to root rules, local rules, task guides, risk notes, expected side effects, and required checks. It is a pre-edit aid, not authorization. Data routes identify likely manifest and generated graph side effects.

### Fixture and data graph exporters

Implementations:

- [scripts/export-fixtures-graph.py](scripts/export-fixtures-graph.py)
- [scripts/export-data-graph.py](scripts/export-data-graph.py)

Both support deterministic generation, freshness checking, and self-tests. The data exporter reads the manifest, projects supported entity types, adds schema provenance, reads only declared relationship sets for domain edges, and enriches matching edges with declared relationship-support metadata.

### Graph export validator

Implementation: [scripts/validate-graph-exports.py](scripts/validate-graph-exports.py)

It validates node and edge objects against formal schemas, requires JSON arrays, rejects duplicate node IDs and edge IDs, and rejects missing source or target endpoints. A compatibility bridge maps the fixture export's older `sourceFixture` field to the formal `sourceDataFile` contract during validation.

### Data validator

Implementation: [scripts/validate-data.py](scripts/validate-data.py)

It validates every manifest entry against its declared schema. For relationship sets it additionally validates registered predicates, endpoint existence, source and target file correctness, relationship ID uniqueness, and semantic-triple uniqueness. For support sets it validates global support identifiers and every relationship, claim, evidence, and reference link.

### Schema validators

Implementations:

- `validate-schemas.py`: schema validity.
- `validate-schema-prerequisites.py`: prerequisites such as supported identity types.
- `validate-schema-contracts.py`: recurring semantic schema requirements.
- `validate-schema-duplicate-contracts.py`: same-name first-class and reusable definition composition.

Each has focused self-tests where applicable.

### Registry validator

Implementation: [scripts/validate-registries.py](scripts/validate-registries.py)

It validates registry shape and cross-contract expectations. Registry semantic reuse remains partly a reviewer responsibility.

### Documentation and rule-routing validators

Implementations:

- [scripts/validate-doc-relationships.py](scripts/validate-doc-relationships.py)
- [scripts/validate-agent-routing.py](scripts/validate-agent-routing.py)

They enforce canonical relationship usage in documentation and the distributed rule-routing structure, including required local rule files, task guides, root routing references, and line budgets.

### Release check

Public command: `make release-check`

Implementation: [scripts/rkm-release-check.py](scripts/rkm-release-check.py)

This is the strict pre-tag path for the already existing internal alpha contract. It requires a clean worktree, checks available alignment with `origin/main`, validates, regenerates the fixture graph export, validates again, and fails if generation dirties the worktree. Do not retag or rewrite `v0.1.0-alpha`.

### Cockpit, budget, recovery, and autopilot

Public entry points are in [Makefile](Makefile). Core scripts are:

| Script | Responsibility |
| --- | --- |
| `rkm-budget.py` | Local token-budget profile, reserve, usage, and target checks |
| `rkm-run-ledger.py` | Local automation run ledger reporting |
| `rkm-next-action.py` | Read-only recommended action from repository and budget state |
| `rkm-recovery-plan.py` | Read-only recovery diagnosis |
| `rkm-cockpit-summary.py` | Compact live decision dashboard |
| `rkm-autopilot.py` | Production orchestration wrapper for bounded automated work |
| `rkm-autocycle.sh` | Repeated bounded cycles with timeout and budget inputs |
| `rkm-cycle.sh` | One lower-level bounded work cycle |
| `rkm-discover.sh` | Bounded discovery workflow |
| `rkm-recover-revise.sh` | Recovery path for a directionally correct revision |
| `rkm-review-verdict.py` | Review verdict parsing and normalization |
| `rkm-codex-commit.sh` | Validated single-file or explicit multi-file commit workflow |
| `rkm-fix-eof.sh` | Focused final-newline repair |

The `.rkm/` directory is ignored locally through `.git/info/exclude`; it contains mutable operational state and is not portable canonical knowledge. Never copy local budget or ledger values into product facts.

### Safe push and commit behavior

`make safe-push` runs validation, requires a clean worktree, prints recent commits, and pushes. Normal operation should not use a direct push in place of this target.

`make codex-commit` requires a prompt file, an explicit file or file list, and a message. Protected categories require an explicit task-specific commit prompt. The current user request did not authorize a commit.

### Bounded Codex Director

Implemented launcher: [scripts/rkm-director.sh](scripts/rkm-director.sh)

Operating contract: [rkm-director-prompt.md](docs/maintenance/rkm-director-prompt.md)

Agent definitions:

- [.codex/agents/rkm-worker.toml](.codex/agents/rkm-worker.toml)
- [.codex/agents/rkm-reviewer.toml](.codex/agents/rkm-reviewer.toml)
- [.codex/config.toml](.codex/config.toml)

The launcher:

- requires branch `experiment/codex-director`;
- requires upstream `origin/experiment/codex-director`;
- fetches and checks remote state;
- requires a clean starting worktree;
- records local and remote protected refs;
- uses `/tmp/rkm-runs` for logs, status, prompts, and final reports;
- enforces a hard timeout, default 7200 seconds;
- emits heartbeat progress;
- prevents concurrent runs with a lock directory;
- invokes Codex with the Director contract;
- supports one optional instruction file;
- verifies protected refs and final repository state;
- has a launcher self-test.

The Director coordinates one Worker and one Reviewer sequentially. It may allow one bounded revision, validates accepted work, commits only accepted scope, and uses `make safe-push`. It never promotes to `main`.

## Specified but not implemented: Autonomous Product Director v2

### Purpose

The Autonomous Product Director begins from a product-level mission. It observes the product, diagnoses consumer-relevant gaps, proposes two or three materially different experiments, selects one, writes acceptance criteria before implementation, scopes paths, delegates to Worker and Reviewer, responds to revision or stop evidence, validates, commits, publishes its experimental branch, verifies from an isolated consumer workspace, and returns a recommendation to a human product owner.

The constitution is [rkm-autonomous-product-director.md](docs/maintenance/rkm-autonomous-product-director.md). The exact runtime contract is [rkm-autonomous-loop-contract.md](docs/maintenance/rkm-autonomous-loop-contract.md).

### Current implementation status

The two documents exist and are detailed. No `scripts/rkm-autonomous-state.py` exists. No launcher for the autonomous product loop exists. No specialized v2 validator modules exist. No runtime artifact writer exists. No conformance suite is wired into `scripts/rkm-unit-tests.sh`. No Make target exposes the facade. Therefore the feature is specification-complete at the contract level and implementation-absent at the runtime level.

The existing bounded Director, Worker, and Reviewer must not be relabeled as the Autonomous Product Director. The v2 contract explicitly preserves the existing bounded Director and current agent configurations.

### Contract version and branch

Every structured JSON artifact must use `contractVersion: rkm-autonomous-loop/v2`. V1 is an incompatible experimental predecessor and must be rejected rather than inferred or migrated silently.

The first real autonomous experiment is defined for `experiment/autonomous-product-director`, tracking `origin/experiment/autonomous-product-director`. The current checkout is on a different branch. Do not launch a first real mission from the current branch.

### Runtime location and bootstrap

Each session belongs under:

```text
/tmp/rkm-runs/autonomous-product-director-<UTC timestamp>-<process identifier>
```

Initialization is one fail-closed atomic transaction. A private adjacent staging directory must contain mutually consistent candidate `RUN_STATE.json` and `GIT_OBSERVATION-01.json`. Only after joint validation may the complete directory be atomically renamed to its final session path. Either artifact alone is not a valid initialized session. Staging debris is not a session.

### State machine

Normal non-terminal states are:

```text
INITIALIZING
OBSERVING
DIAGNOSING
GENERATING_OPTIONS
SELECTING_EXPERIMENT
DEFINING_ACCEPTANCE
IMPLEMENTING
INSPECTING_WORK
REVIEWING
VALIDATING
COMMITTING
PUBLISHING
VERIFYING_EXTERNALLY
FINALIZING
```

Corrective states are `REVISING` and `REPLANNING`. Terminal states are `COMPLETED`, `ESCALATED`, `STOPPED`, `FAILED`, and `INTERRUPTED`. Every orderly terminal outcome must pass through `FINALIZING`.

### Runtime artifacts

The normal successful path requires:

- `RUN_STATE.json`;
- `OBSERVATION.json`;
- `OPTIONS.json`;
- numbered `DIRECTOR_DECISION` files;
- numbered `GIT_OBSERVATION` files;
- numbered `WORKER_ASSIGNMENT` files;
- numbered `AGENT_SUPERVISION` files;
- numbered `WORKER_RESULT` files;
- numbered `WORK_INSPECTION` files;
- numbered `REVIEW_VERDICT` files;
- numbered `VALIDATION_RESULT` files;
- numbered `EXTERNAL_VERIFICATION` files;
- `FINAL_REPORT.md`;
- numbered `RECOVERY_RECORD` files when recovery occurs.

Repeatable families begin at `-01`, use contiguous two-digit numbering, never overwrite history, and are immutable once published. `RUN_STATE.json` alone is atomically replaced on legal transitions.

### Hard behavioral requirements

The implementation must preserve:

- exact decision digests and atomic initial decision plus Worker registration;
- append-only identifiers and transition history;
- at most one active agent;
- authoritative Git facts from one Git observer;
- authoritative process facts from a distinct agent supervisor;
- exact Worker and Reviewer process invocation;
- exact stdout and stderr bytes, base64 encoding, lengths, and digests;
- bounded revision, replan, and commit budgets with exact-once charges;
- scope union of at most six product files for the first mission unless explicitly authorized otherwise;
- no autonomous changes to protected categories without task-specific authorization;
- no promotion to `main`;
- isolated external verification after publication;
- fail-closed behavior when a component is missing, malformed, rejecting, or inconsistent.

### Required modular implementation

The contract requires separate in-process responsibility owners for:

1. authoritative Git observation;
2. JSON loading, duplicate-key rejection, canonicalization, and shared artifact validation;
3. bootstrap validation;
4. decision, scope, budget, and digest validation;
5. state transition validation;
6. agent-supervision validation;
7. Worker and Reviewer lifecycle validation;
8. finalization and publication validation;
9. substantive final-report validation.

The thin public facade must be `scripts/rkm-autonomous-state.py` and expose:

```text
initialize
validate-artifact
validate-session
transition
summarize
self-test
```

Exit codes are 0 for full pass, 2 when at least one component rejects and none errors, and 3 for missing, malformed, or erroring required components.

### Implementation order

Because root rules permit exactly one project file per run unless the user explicitly changes the protocol, implement the v2 runtime incrementally:

1. Obtain explicit human authorization for the protected validator, script, test-runner, launcher, and Makefile scope.
2. Resolve which branch will be the authoritative implementation baseline.
3. Implement leaf components one file at a time with focused self-tests.
4. Implement boundary integration only after its dependencies exist.
5. Implement the thin facade after every required component exists.
6. Add public-facade end-to-end tests using disposable Git repositories below `/tmp`.
7. Wire the conformance suite into `scripts/rkm-unit-tests.sh` only with explicit authorization.
8. Add a Make target only with explicit authorization.
9. Add or adapt a launcher only after facade and tests pass.
10. Run the first real mission only from the contractually correct clean, aligned branch.

An intermediate module must not default to `PASS`, fake absent dependencies, duplicate another component's rules, or claim end-to-end conformance.

## Review artifacts and how to interpret them

### Historical reviewer pack

[independent-reviewer-pack.md](docs/reviews/vector-databases/independent-reviewer-pack.md) is bound to comparison baseline `74ca2d0`. Its lifecycle statements describe that historical snapshot. It is valuable for its review rubric and finding inventory, not for current Neo4j lifecycle.

### Historical graph-plus-vector adjudication

[graph-plus-vector-review-adjudication.md](docs/reviews/vector-databases/graph-plus-vector-review-adjudication.md) is bound to an earlier baseline and records `REVISION REQUIRED` for Neo4j, Amazon Neptune Analytics, and Memgraph at that time. Its decisions guided later semantic work. It must not be rewritten to pretend it approved later content.

### Current Neo4j acceptance

[neo4j-1.5.1-independent-acceptance.md](docs/reviews/vector-databases/neo4j-1.5.1-independent-acceptance.md) binds current Neo4j version `1.5.1` to:

- canonical SHA-256 `6ea8eb9ac34d995c3759a71ce7cf43e7c8ee6445947720bbb71354b3bb473e55`;
- Git blob `c98ac1e352e216b712ccd2f3cdd84d9f9b986d82`;
- approval commit `a617864fff7f56b25f3a37ab259d727275648de4`;
- integration commit `b41b206887fee1ace942b9bf939a4df7e0365b24`;
- independent acceptance verdict `ACCEPT`.

The canonical JSON remains the present lifecycle authority. Neo4j is artifact status `Draft`, review state `Approved`. This approval does not cover the other 16 VectorDatabase records.

## Known documentation drift on the current branch

The current branch added substantial data and code after many maintenance documents were last synchronized. Treat these as known inconsistencies, not as reasons to ignore canonical data:

- [README.md](README.md) does not list VectorDatabase seed data in its current-content bullets.
- [QUICKSTART.md](QUICKSTART.md) does not document `--compare` or VectorDatabase examples.
- [data/README.md](data/README.md) does not list the 17 vector-database files.
- [examples/data-graph-export/README.md](examples/data-graph-export/README.md) says the current export emits Technique, Component, Retriever, Reranker, and schema nodes, omitting 17 VectorDatabase nodes.
- [graph-export-contract.md](docs/maintenance/graph-export-contract.md) has the same older node-coverage description.
- [assistant-handoff.md](docs/maintenance/assistant-handoff.md) predates VectorDatabase graph nodes and the current branch distinction.
- [maturity-report.md](docs/maintenance/maturity-report.md) describes 13 entity records rather than the current 30 and omits VectorDatabase coverage.
- [governance-backlog.md](docs/maintenance/governance-backlog.md) still marks GB-020, Vector Database and Graph Database Seed Data, as `Proposed` even though VectorDatabase seed data now exists. GraphDatabase seed data remains absent, so the combined item needs deliberate reclassification or splitting.
- The release notes correctly describe the tagged alpha, not current branch scope. They should not be “updated” to include later branch work under the old tag.

Documentation synchronization is a valid next task, but the one-file-per-run rule means each file must be handled in its own run unless the user explicitly authorizes a coherent multi-file update.

## Current backlog

### Implemented backlog entries

- GB-001: schema duplicate contract validator.
- GB-005: task router CLI.
- GB-018: chunking strategy seed data.
- GB-028: evidence strength calibration.
- GB-029: primary versus secondary source policy.
- GB-030: claim review workflow.
- GB-031: citation freshness and staleness policy.
- GB-040: granular maturity scorecard.
- GB-042: autopilot per-cycle timeout.
- GB-043: data route side-effect guidance.

### Proposed high-priority entries

- GB-002: new entity type package validator.
- GB-003: relationship predicate reuse checker.
- GB-004: hard dependency predicate justification check.
- GB-006: recovery-state validator or autopilot blocker.
- GB-007: runtime artifact detector.
- GB-012: policy-as-data registry.
- GB-013: stable rule IDs.
- GB-014: link rules to validators.
- GB-021: query transformation technique seed data.
- GB-022: evaluation metric seed data.
- GB-027: external references pass.
- GB-038: v0.2.0 planning document.
- GB-039: release readiness matrix.
- GB-041: changelog discipline validator.

### Proposed medium-priority entries

- GB-008: rule coverage consistency validator.
- GB-009: Markdown JSON example validator.
- GB-010: stronger graph-export provenance consistency validator.
- GB-011: validation weakening detector.
- GB-015: more granular local rule files.
- GB-016: anti-duplication checks among rule sources.
- GB-017: local rule-file line budgets.
- GB-019: embedding model seed data.
- GB-020: vector and graph database seed data, now partially stale as explained above.
- GB-023: benchmark seed data.
- GB-024: dataset seed data.
- GB-025: model and reranker provider modeling.
- GB-026: agentic RAG workflow modeling.
- GB-032: task-specific command generator.
- GB-033: backlog query tooling.
- GB-034: cockpit integration for backlog priorities.
- GB-035: autopilot mode profiles.
- GB-036: autopilot risk tiers.
- GB-037: rule routing summary targets.

Backlog status is maintained prose, not automatically derived from Git. Verify whether an item has already been partially or fully implemented before selecting it.

## Recommended continuation from this exact point

There are three distinct next-direction tracks. A human product owner should select one rather than letting an agent blend them.

### Track A: integrate and stabilize the current experiment

Use this when the goal is to make the current `experiment/codex-director` branch reviewable for eventual promotion.

1. Commit this hand-off only if the user explicitly authorizes it.
2. Re-run `make validate` from a clean post-commit state.
3. Review the 78-commit branch diff against `main` by product increment, not as one undifferentiated 20,000-line change.
4. Confirm that autonomous-loop specification and vector-database dataset expansion are intentionally meant to land together. They are conceptually separate.
5. Synchronize branch-level consumer documentation one file per run.
6. Reconcile governance backlog statuses, especially GB-020.
7. Decide whether the broad branch should be split, merged as a whole, or retained as an experiment.
8. Only a human should authorize promotion to `main`.

This is the safest immediate path because it resolves what already exists before adding another subsystem.

### Track B: continue vector-database product work

Use this when the goal is evidence-first architecture decision support.

1. Treat the 16 `Not Reviewed` records as draft inputs.
2. Choose one record or one tightly bounded semantic family, not a bulk rewrite.
3. Read the historical review rubric and current vector-database architecture model.
4. Pin mutable sources by version, commit, date, or digest as appropriate.
5. Separate product-core, extension, package, cloud-platform, host-infrastructure, and application-composition capabilities.
6. Separate product licensing from artifact licensing.
7. Split compound claims into independently reviewable propositions.
8. Record limitations and contrary scope.
9. Regenerate affected graph artifacts only when the task authorizes all required files.
10. Obtain independent read-only review before advancing lifecycle state.

Neptune Analytics and Memgraph are natural next review candidates because the historical graph-plus-vector adjudication already identifies their blocking issues. Their recent artifact-license corrections did not constitute substantive re-review.

### Track C: implement Autonomous Product Director v2

Use this only after explicit authorization for protected implementation work.

1. Decide the branch baseline. The contract names `experiment/autonomous-product-director`, but that branch is 75 commits behind the current branch and does not contain the later dataset integration.
2. Do not implement on `experiment/codex-director` while claiming contract conformance.
3. Define an explicit allowed file for the first run.
4. Begin with a leaf component whose contract can be tested in isolation.
5. Preserve the required modular boundaries.
6. Keep the public facade absent until dependencies are real.
7. Add test and Make integration only through separately authorized protected changes.
8. Perform the first real mission only after complete conformance and branch-safety validation.

The branch-baseline decision is genuine product ownership. An agent should not silently merge or rebase the autonomous branch to manufacture a baseline.

## Task playbooks

### Add or revise one existing-type data record

Required reading:

- root [AGENTS.md](AGENTS.md);
- [data/AGENTS.md](data/AGENTS.md);
- [adding-data-records.md](docs/maintenance/task-guides/adding-data-records.md);
- the entity schema;
- neighboring records;
- relevant architecture model;
- evidence and reference models when knowledge claims change.

Normal dependency chain:

```text
record
  -> data/manifest.json
  -> data graph nodes and provenance edges
  -> validation
```

Under the default one-file protocol, complete only the authorized single-file increment and describe additional required files as later runs unless the user explicitly authorizes the coherent package.

### Add a new populated entity type

Read [adding-new-entity-type.md](docs/maintenance/task-guides/adding-new-entity-type.md). A complete package needs record data, manifest entries, semantic validation compatibility, exporter support, schema provenance, generated artifacts, documentation, and self-tests. Existing validation checks parts of this package but does not yet enforce package completeness as one rule.

### Add a relationship set

Read [adding-relationship-set.md](docs/maintenance/task-guides/adding-relationship-set.md). Reuse a registered predicate, preserve direction, use existing endpoint IDs and exact endpoint file paths, avoid duplicate triples, and do not infer relationships from prose.

### Add relationship support

Read [adding-relationship-support.md](docs/maintenance/task-guides/adding-relationship-support.md). Every relationship, claim, evidence, and reference ID must resolve. State clearly whether support is official, empirical, secondary, or maintainer analysis.

### Change a schema contract

Read [schema/AGENTS.md](schema/AGENTS.md), [adding-schema-contract.md](docs/maintenance/task-guides/adding-schema-contract.md), and [automation-guardrails.md](docs/maintenance/automation-guardrails.md). Obtain explicit authorization. Inspect identity support, registry support, definitions, examples, validators, self-tests, data, exports, docs, versioning, and migration implications.

### Extract a reusable definition

Read [refactoring-schema-definition.md](docs/maintenance/task-guides/refactoring-schema-definition.md). The refactor must be atomic. A same-name first-class schema must visibly compose the reusable definition. Avoid creating two sources of truth.

### Change graph export behavior

Read [examples/AGENTS.md](examples/AGENTS.md), [scripts/AGENTS.md](scripts/AGENTS.md), [updating-graph-export.md](docs/maintenance/task-guides/updating-graph-export.md), and [graph-export-contract.md](docs/maintenance/graph-export-contract.md). Explicitly authorize exporter, generated artifact, schema, test, and documentation paths. Regenerate; do not manually synthesize generated output.

### Change a validator

Read [updating-validation-scripts.md](docs/maintenance/task-guides/updating-validation-scripts.md). Preserve actionable diagnostics, add focused self-tests, and prove that the change does not silently weaken validation.

### Write architecture documentation

Read [docs/architecture/AGENTS.md](docs/architecture/AGENTS.md) and [writing-architecture-doc.md](docs/maintenance/task-guides/writing-architecture-doc.md). Reuse canonical terminology. Concrete repository paths must use real IDs and real files. Abstract examples must remain fully abstract.

### Prepare a release

Read [preparing-release.md](docs/maintenance/task-guides/preparing-release.md). Do not mutate the existing alpha tag. A future version requires an intentional version plan, compatibility statement, changelog and release notes, clean validation, reproducible artifacts, and explicit human tagging authority.

### Run unattended automation

Read [automation-guardrails.md](docs/maintenance/automation-guardrails.md) and [unattended-autopilot.md](docs/maintenance/task-guides/unattended-autopilot.md). Prefer repeated `make autopilot N=1` rounds, keep logs below `/tmp/rkm-runs`, validate and safe-push after each successful round, and stop on recovery ambiguity.

### Recover a failed new file

Read [recovering-failed-new-file.md](docs/maintenance/task-guides/recovering-failed-new-file.md). A failed new file that must be discarded needs to be removed from both index and filesystem after diagnostic preservation. Never use broad destructive Git cleanup.

## Operational invariants and failure traps

- Default repository work changes exactly one project file per run.
- Do not commit unless the user explicitly requests a commit.
- Run `bash scripts/validate-rkm.sh` after the one allowed file change.
- Report the touched file, validation command and result, and final `git status --short`.
- Use canonical project names only.
- Repository content is English unless a file intentionally targets another language.
- File names are lowercase kebab case; relationship predicates are uppercase snake case.
- Do not create IDE configuration or repository-local run logs.
- Do not create `.rkm-runs/` inside the repository.
- Treat generated exports as generated contracts.
- Treat fixtures as pedagogical examples and data as populated seed knowledge.
- Treat schemas, registries, validators, exporters, Makefile, release process, graph contracts, and migrations as protected categories.
- `FORCE=true` may cross budget or target guards only; it never bypasses validation, clean-worktree, review, recovery, or safe-push rules.
- Do not restart autopilot after `RECOVERY_FAILED_NEEDS_MANUAL_FIX` without inspection and a recovery plan.
- Do not infer a missing architecture document from filename symmetry.
- Do not infer a domain edge from likely semantics.
- Do not use evidence counts as quality rankings.
- Do not update historical review conclusions to match later state.
- Do not confuse artifact `status` with `reviewState`.
- Do not confuse product licensing with the RKM artifact license.
- Do not confuse current branch work with tagged alpha scope.
- Do not confuse the bounded Director with the Autonomous Product Director.
- Do not claim Autonomous Product Director v2 is implemented.
- Do not run its first mission from the wrong branch.
- Do not promote any experimental branch to `main` autonomously.

## Command reference

### Health and inspection

```bash
git status --short
git log --oneline --decorate -n 20
make validate
make cockpit-summary N=5
make recovery-plan
make budget-report
make autopilot-status
```

### Routing and focused validation

```bash
make route-task PATHS="path/a path/b"
make data-validate
make graph-export-validate
make schema-duplicate-contracts-validate
make agent-routing-validate
```

### Generation

```bash
make graph-export
make data-graph-export
```

### Decision support

```bash
python3 scripts/rkm-decision-query.py --help
python3 scripts/rkm-decision-query.py --entity hybrid-retrieval
python3 scripts/rkm-decision-query.py --pipeline hybrid-retrieval reranking
python3 scripts/rkm-decision-query.py --compare pgvector neo4j
```

### Automation

```bash
make autopilot N=5
make autopilot N=1 PER_CYCLE_TIMEOUT_SECONDS=1800
make autopilot-dry-run N=1
make autopilot-recover N=1
make safe-push
```

### Bounded Director

```bash
bash scripts/rkm-director.sh --self-test
bash scripts/rkm-director.sh
bash scripts/rkm-director.sh --instruction-file /absolute/path/to/instruction.md
```

The Director launcher performs remote and branch checks and can cause external state changes through accepted commits and safe push. Run it only with appropriate authorization and from the exact expected branch.

## Receiving-agent decision checklist

Before changing anything, answer these questions from repository evidence:

1. What branch am I on, and what upstream does it track?
2. Is the worktree clean except for an explicitly handed-off change?
3. Is recovery required?
4. Is the requested outcome review, diagnosis, implementation, automation, or release work?
5. Which paths are actually authorized?
6. Which local rules and task guides govern them?
7. Is the task in a protected category?
8. Does the repository already implement the requested capability under another name?
9. Is the source I am reading canonical current state, generated output, static guidance, or historical evidence?
10. What machine-enforced side effects follow from the change?
11. Can the work be completed under the one-file rule?
12. What validation proves structure, and what independent review proves semantics?
13. Does the proposed change improve a consumer-observable outcome?
14. What claims remain unsupported or only internally supported?
15. What exact next action will leave the repository in a trustworthy state?

## Definition of a trustworthy hand-off after future work

A future hand-off should record:

- objective and authorization;
- starting branch and commit;
- files changed;
- exact behavior or knowledge changed;
- relevant architecture and contract decisions;
- commands run and exit results;
- independent review outcome when applicable;
- generated artifacts refreshed;
- unresolved epistemic and technical risks;
- final branch and commit;
- upstream alignment;
- final `git status --short`;
- whether a commit and push occurred;
- the precise recommended next action.

Do not call a hand-off clean when the worktree is dirty, except when the user explicitly requested an uncommitted artifact and that state is clearly disclosed.

## Bottom line

RKM is a strong, validation-oriented knowledge-model foundation with a broad schema and architecture surface, explicit evidence and relationship semantics, deterministic fixture and data graph exports, disciplined governance, operational automation, an implemented bounded Director, a useful decision-query CLI, and a current branch containing 17 VectorDatabase records plus a deeply reviewed Neo4j record.

The most important current distinction is between breadth and trust. The repository can structurally represent much more than it has populated, and it has populated more VectorDatabase content than it has independently reviewed. Neo4j is the only approved VectorDatabase record. The current comparison feature is descriptive and traceable, not a recommendation engine.

The second critical distinction is between specification and implementation. The Autonomous Product Director v2 contract is unusually complete, but no conforming runtime exists. Implementing it is a separate, protected, incremental engineering program that requires branch and authorization decisions before code is written.

The safest continuation is to stabilize and consciously integrate the current experimental branch, synchronize branch documentation, and choose explicitly between deeper vector-database review and v2 runtime implementation. Do not let automation select that strategic fork by accident.

## Creation record

This document is the only project file created during its preparation. No existing file was modified and no commit was created. The required validation command and final Git status must be read from the hand-off response that accompanied this file or recomputed immediately with:

```bash
bash scripts/validate-rkm.sh
git status --short
```
