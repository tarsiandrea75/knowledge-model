# RAG Knowledge Model (RKM)

RAG Knowledge Model (RKM) is a structured, extensible knowledge model for the Retrieval-Augmented Generation ecosystem.

RKM is designed to be human-readable, machine-readable, and validation-oriented. It models RAG entities, relationships, claims, evidence, references, metadata, registries, and schemas as connected knowledge artifacts rather than as a simple list of techniques.

The long-term goal is to provide a domain model, ontology, and knowledge graph foundation that can support documentation, onboarding, validation, graph export, downstream loaders, and future RAG ecosystem analysis.

RKM is not production-ready and is not a complete catalog of the RAG ecosystem.

## Current Status

The current package is `v0.1.0-alpha`.

This alpha package is intended for internal evaluation, onboarding, and consumer feedback. It contains a strong foundation, but it should not be treated as a stable public API, production dependency, or comprehensive RAG knowledge base.

The package currently includes schemas, fixtures, seed data, validated relationship sets, a minimal fixture graph export, validation commands, and documentation for consumers, maintainers, and future assistants. Post-alpha work on `main` also includes a seed-data graph export under `examples/data-graph-export/`.

## What RKM Currently Includes

- Schema foundation using JSON Schema Draft 2020-12.
- Validated fixtures under `examples/fixtures/`.
- Validated seed dataset under `data/`.
- Validated relationship sets under `data/relationships/`.
- Minimal fixture-derived graph export under `examples/graph-export/`.
- Post-alpha seed-data graph export under `examples/data-graph-export/`, including provenance edges and declared domain relationship edges.
- Graph export node and edge schema validation.
- Validation pipeline through `make validate`.
- Consumer, release, maturity, roadmap, and assistant handoff documentation.

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
- fixture and data graph export consistency
- graph export node and edge schema validation
- unit tests
- documentation relationship usage
- repository hygiene

The validator is intentionally broad because RKM treats schemas, documentation, fixtures, data, registries, and graph export artifacts as connected parts of one model.

## Release and Alpha Package

Read the `v0.1.0-alpha` release notes in [docs/releases/v0.1.0-alpha.md](docs/releases/v0.1.0-alpha.md).

Release history is tracked in [CHANGELOG.md](CHANGELOG.md), and release documentation is indexed in [docs/releases/README.md](docs/releases/README.md).

The `v0.1.0-alpha` documentation package does not imply that a git tag exists. Maintainers should create a tag only when they intentionally decide to publish a tagged release.

## Consumer Documentation

Start with [docs/maintenance/consumer-guide.md](docs/maintenance/consumer-guide.md) to understand the current consumption contract, validation path, fixture package, seed dataset, graph export, stability expectations, and evolving areas.

Spanish-speaking stakeholders can use [docs/maintenance/consumability-roadmap.es-AR.md](docs/maintenance/consumability-roadmap.es-AR.md) for a Spanish explanation of consumability goals and next steps.

## Maturity and Limitations

The current maturity assessment is documented in [docs/maintenance/maturity-report.md](docs/maintenance/maturity-report.md).

RKM has a strong foundation: architecture documents, JSON Schemas, reusable definitions, registries, fixtures, seed data, graph export validation, and automation are in place.

RKM is not yet level 4 maturity. The main gaps are dataset breadth, graph export expansion beyond the minimal fixture-derived path, deliberate release packaging, and clearer downstream loader guidance for graph databases, search indexes, vector stores, JSON document stores, and other consumers.

Current limitations include:

- The populated dataset is small.
- The graph exports are intentionally minimal. The fixture export is pedagogical, and the seed-data export is early post-alpha work.
- Compatibility expectations are suitable for internal alpha evaluation, not stable public adoption.
- Loader-specific guidance is still limited.
- The project is not a complete RAG ecosystem catalog.

## Maintainer and Assistant Handoff

Future maintainers and assistants should start with [docs/maintenance/assistant-handoff.md](docs/maintenance/assistant-handoff.md), then run the cockpit and validation commands before making changes.

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
