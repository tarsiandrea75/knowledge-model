# RAG Knowledge Model (RKM)

RAG Knowledge Model (RKM) is a structured, extensible knowledge model for the Retrieval-Augmented Generation ecosystem.

RKM is designed to be human-readable, machine-readable, and validation-oriented. It models RAG entities, relationships, claims, evidence, references, metadata, registries, and schemas as connected knowledge artifacts rather than as a simple list of techniques.

The long-term goal is to provide a domain model, ontology, and knowledge graph foundation that can support documentation, onboarding, validation, graph export, downstream loaders, and future RAG ecosystem analysis.

RKM is not production-ready and is not a complete catalog of the RAG ecosystem.

## Current Status

The tagged release checkpoint is `v0.1.0-alpha`.

This alpha package is intended for internal evaluation, onboarding, and consumer feedback. It contains a strong foundation, but it should not be treated as a stable public API, production dependency, or comprehensive RAG knowledge base.

The current experimental branch extends that historical checkpoint with a populated seed-data graph export, first-class VectorDatabase data and decision views, and additional governance and automation work. These post-alpha capabilities are not part of the tagged `v0.1.0-alpha` release.

Autonomous Product Director v2 is specification-complete and runtime-unimplemented. Its constitution and machine-oriented loop contract are present, but the required v2 runtime, public facade, validator components, conformance suite, and launcher are not implemented. The existing bounded RKM Codex Director is a separate implemented workflow.

## What RKM Currently Includes

- Schema foundation using JSON Schema Draft 2020-12.
- Validated fixtures under `examples/fixtures/`.
- Validated seed dataset under `data/`.
- Validated component seed data under `data/components/`.
- Validated retriever and reranker seed data under `data/retrievers/` and `data/rerankers/`.
- First-class VectorDatabase architecture, registry, schema, and populated data support.
- 17 manifest-declared VectorDatabase records under `data/vector-databases/`.
- Validated relationship sets under `data/relationships/`.
- Validated relationship support sets under `data/relationship-support/`.
- Minimal fixture-derived graph export under `examples/graph-export/`.
- Post-alpha seed-data graph export under `examples/data-graph-export/`, including 17 VectorDatabase nodes alongside Technique, Component, Retriever, Reranker, and Schema nodes, provenance edges, and declared domain relationship edges.
- Source-linked entity views and deterministic, descriptive same-type comparisons through `scripts/rkm-decision-query.py`.
- Graph export node and edge schema validation.
- Validation pipeline through `make validate`.
- Consumer, release, maturity, roadmap, and assistant handoff documentation.

All 17 VectorDatabase records currently have artifact status `Draft`. Neo4j alone has review state `Approved`; the other 16 remain `Not Reviewed`. Consumers must inspect lifecycle fields, claims, evidence, references, qualifiers, limitations, and guidance before using a record in a decision. Record presence, matching comparison values, or Neo4j's scoped approval does not imply product recommendation, release approval, or semantic approval of the full dataset.

## Quick Start

For the shortest operational path, start with [QUICKSTART.md](QUICKSTART.md).

Run the full validation suite:

```bash
make validate
```

Regenerate the minimal fixture-derived graph export:

```bash
make graph-export
```

Regenerate the post-alpha seed-data graph export:

```bash
make data-graph-export
```

Inspect a source-linked VectorDatabase entity view or compare two records:

```bash
python3 scripts/rkm-decision-query.py --entity neo4j --detail full
python3 scripts/rkm-decision-query.py --compare neo4j qdrant
```

Comparison output is non-ranking and evidence-traceable. Missing values mean only that a field is not recorded, not that a capability is unsupported.

## Repository Map

- `schema/`: specialized entity schemas and top-level schema contracts.
- `schema/definitions/`: reusable schema definitions for shared concepts such as identity, metadata, descriptions, relationships, claims, evidence, and references.
- `registries/`: controlled entity type and relationship type registries.
- `docs/architecture/`: domain, entity, relationship, evidence, metadata, ontology, naming, versioning, and specialized model documentation.
- `docs/maintenance/`: consumer guidance, maturity reporting, roadmap notes, graph export contract, repository map, and assistant handoff documentation.
- `examples/fixtures/`: small validated examples that demonstrate valid schema shape and validation behavior.
- `examples/graph-export/`: minimal graph nodes and edges derived from fixtures.
- `examples/data-graph-export/`: graph nodes and edges derived from the validated seed dataset.
- `data/`: small validated seed dataset and declared relationship sets for early consumer testing and inspection.
- `scripts/`: validation, graph export, cockpit, automation, recovery, and maintenance scripts.

## Validation

`make validate` is the primary repository health check.

It checks:

- schema validity
- schema prerequisites
- schema contracts
- registries
- fixture instances
- data instances
- relationship-set semantics against registered predicates and declared data records
- relationship support semantics for declared references, claims, evidence, and relationship IDs
- fixture and data graph export consistency
- graph export node and edge schema validation
- unit tests
- documentation relationship usage
- repository hygiene

The validator is intentionally broad because RKM treats schemas, documentation, fixtures, data, registries, and graph export artifacts as connected parts of one model.

## Release and Alpha Package

Read the `v0.1.0-alpha` release notes in [docs/releases/v0.1.0-alpha.md](docs/releases/v0.1.0-alpha.md).

Release history is tracked in [CHANGELOG.md](CHANGELOG.md), and release documentation is indexed in [docs/releases/README.md](docs/releases/README.md).

The `v0.1.0-alpha` tag exists and preserves the first internal alpha checkpoint. Its release notes and changelog remain historical: statements that the documentation update did not itself create a tag describe that earlier operation and must not be read as current Git-state claims. Post-alpha VectorDatabase capabilities and the Autonomous Product Director v2 specifications do not retroactively expand the tagged release.

## Consumer Documentation

Start with [docs/maintenance/consumer-guide.md](docs/maintenance/consumer-guide.md) to understand the current consumption contract, validation path, fixture package, seed dataset, graph export, stability expectations, and evolving areas.

Spanish-speaking stakeholders can use [docs/maintenance/consumability-roadmap.es-AR.md](docs/maintenance/consumability-roadmap.es-AR.md) for a Spanish explanation of consumability goals and next steps.

## Maturity and Limitations

The current maturity assessment is documented in [docs/maintenance/maturity-report.md](docs/maintenance/maturity-report.md).

RKM has a strong foundation: architecture documents, JSON Schemas, reusable definitions, registries, fixtures, seed data, graph export validation, decision views, and automation are in place.

RKM is not yet level 4 maturity. The main gaps are dataset breadth and review depth, deliberate release packaging, and clearer downstream loader guidance for graph databases, search indexes, vector stores, JSON document stores, and other consumers.

Current limitations include:

- The populated dataset remains small and unevenly reviewed despite the 17-record VectorDatabase expansion.
- The fixture graph export is intentionally pedagogical, and the broader seed-data export remains early post-alpha work.
- Compatibility expectations are suitable for internal alpha evaluation, not stable public adoption.
- Loader-specific guidance is still limited.
- Autonomous Product Director v2 has no conforming runtime implementation.
- The project is not a complete RAG ecosystem catalog.

## Maintainer and Assistant Handoff

Future maintainers and assistants should start with the canonical [docs/maintenance/live-handoff.md](docs/maintenance/live-handoff.md), then use [rkm-project-handoff.md](rkm-project-handoff.md) for the comprehensive baseline and inspect live repository contracts before making changes.

Useful commands:

```bash
make cockpit-summary N=5
make validate
```

The handoff documentation explains the current repository state, operating constraints, validation expectations, and next recommended maintenance steps.

## Design Principles

RKM preserves these core design principles:

- Prefer structured information over prose-only descriptions.
- Use stable identifiers as durable references.
- Represent entities, relationships, claims, evidence, references, and metadata as first-class concepts.
- Keep metadata separate from domain knowledge.
- Use registries for controlled vocabularies.
- Preserve vendor neutrality across frameworks, providers, tools, and ecosystems.
- Keep repository content readable for humans and useful for automated processing.
- Link important claims to evidence and references whenever support is available.

## Long-Term Vision

RKM is intended to become a structured reference dataset and graph foundation for the RAG ecosystem.

The model is designed so future versions can support exports and loaders for systems such as graph databases, RDF or OWL tooling, JSON document stores, REST APIs, GraphQL APIs, vector databases, semantic search indexes, and RAG evaluation workflows without changing the core modeling assumptions.
