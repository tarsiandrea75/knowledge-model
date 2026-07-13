# Consumer Guide

## Purpose

This guide explains how another team can inspect, validate, and export the first small RAG Knowledge Model fixture package and the first small populated dataset.

For the shortest operational path, start with `QUICKSTART.md`. For package scope, validation expectations, limitations, and next milestones, read `docs/releases/v0.1.0-alpha.md`.

`v0.1.0-alpha` is the first internal consumable RKM package. It is intended for internal evaluation, onboarding, and consumer feedback. It is not production-ready and should not be presented as a stable public API or complete RAG catalog.

RKM is a structured knowledge model for the Retrieval-Augmented Generation ecosystem. Consumers should treat entities, relationships, claims, evidence, references, and metadata as separate but connected concepts.

## Fixture Package

The minimal fixture package lives under `examples/fixtures/`. Fixtures are minimal examples for learning the schema shape and testing validation mechanics. They are not the populated knowledge dataset.

It contains:

- `minimal-rag-technique.json`: a RAG technique entity for Hybrid Retrieval.
- `minimal-relationship.json`: a relationship showing that the technique `DEPENDS_ON` a retriever component.
- `minimal-claim-with-evidence.json`: a compact package containing one claim, one evidence object, and one reference object.

Together these files demonstrate the smallest useful consumption path:

```text
TECHNIQUE-9001 DEPENDS_ON COMPONENT-9001
CLAIM-9001 supported by EVIDENCE-9001
EVIDENCE-9001 derived from REFERENCE-9001
```

`COMPONENT-9001` is intentionally referenced but not expanded into a full component entity in this package. This keeps the first fixture small while showing that RKM relationships can point to stable identifiers outside the current fixture set.

## Populated Data

The first populated RKM dataset lives under `data/`. It is separate from fixtures and is intended for consumer testing, validation, and release packaging.

Current seed data includes three RAG technique records:

- `data/rag-techniques/hybrid-retrieval.json`
- `data/rag-techniques/query-rewriting.json`
- `data/rag-techniques/reranking.json`

These records are intentionally small and conservative. They are not a complete RAG technique catalog and should not be presented as comprehensive coverage of the RAG ecosystem.

Data validation is driven by `data/manifest.json`, which maps each data file to its validating schema. Direct data validation is available through:

```bash
make data-validate
```

## Graph Exports

RKM currently has two deterministic graph export paths.

The fixture package can be exported to a minimal graph representation under `examples/graph-export/`. The fixture graph export is intentionally minimal and pedagogical. It proves the first export contract path and validation wiring, but it is not the populated seed dataset.

The fixture graph export is derived from the committed fixtures. It contains:

- `minimal-graph.nodes.json`: a deterministic array of graph nodes.
- `minimal-graph.edges.json`: a deterministic array of graph edges.

Generate the fixture graph export from the project root:

```bash
make graph-export
```

Check that the committed export still matches the fixtures:

```bash
python3 scripts/export-fixtures-graph.py --check
```

The validated seed dataset can be exported to a separate graph representation under `examples/data-graph-export/`. The data graph export is derived from the files declared in `data/manifest.json`. It currently emits data record nodes, a schema node, and provenance edges that state which schema validates each record. It does not invent RAG domain relationships that are not present in the seed data.

Generate the data graph export from the project root:

```bash
make data-graph-export
```

Check that the committed data graph export still matches the seed dataset:

```bash
python3 scripts/export-data-graph.py --check
```

The repository validator runs both consistency checks, so stale graph export files fail `make validate`.

Both graph export paths are also validated against formal graph node and edge schemas. The schema-level validator checks the exported object shape, duplicate node IDs, duplicate edge IDs, and edge endpoints that must resolve to nodes in the same export:

```bash
make graph-export-validate
```

Consumers can rely on the current node and edge shape as an alpha/internal contract for evaluation and importer experiments. This contract is not a stable public API. Field names, coverage, package metadata, and loader-specific mappings may still change before RKM offers a public compatibility guarantee.

## How To Validate

Run repository validation from the project root:

```bash
make validate
```

This runs schema validity checks, fixture instance validity checks, data instance validity checks, graph export consistency checks, and the rest of the repository validation suite:

- whitespace validation
- file encoding and line ending checks
- forbidden naming checks
- incomplete content marker checks
- JSON Schema validation for repository schemas
- schema prerequisite validation
- schema contract validation
- registry validation
- fixture instance validation using `examples/fixtures/fixture-manifest.json`
- data instance validation using `data/manifest.json`
- fixture graph export consistency validation using `scripts/export-fixtures-graph.py --check`
- data graph export consistency validation using `scripts/export-data-graph.py --check`
- graph export schema validation using `scripts/validate-graph-exports.py`
- RKM unit tests
- documentation relationship validation

Fixture validation loads `examples/fixtures/fixture-manifest.json`, resolves fixture and schema paths from the repository root, and validates each fixture instance against its declared schema. The claim package fixture is an envelope, so its `claim`, `evidence`, and `reference` objects are validated against their corresponding definition schemas.

Data validation loads `data/manifest.json`, resolves data and schema paths from the repository root, and validates each populated data instance against its declared schema.

Fixture graph export generation is handled by:

```bash
make graph-export
```

Data graph export generation is handled by:

```bash
make data-graph-export
```

Graph export consistency is checked by:

```bash
make validate
```

Consumers that want direct fixture validation outside the repository scripts can use a JSON Schema Draft 2020-12 validator:

- validate `examples/fixtures/minimal-rag-technique.json` against `schema/rag-technique.schema.json`
- validate `examples/fixtures/minimal-relationship.json` against `schema/definitions/relationship.schema.json`
- validate the `claim` object in `examples/fixtures/minimal-claim-with-evidence.json` against `schema/definitions/claim.schema.json`
- validate the `evidence` object in `examples/fixtures/minimal-claim-with-evidence.json` against `schema/definitions/evidence.schema.json`
- validate the `reference` object in `examples/fixtures/minimal-claim-with-evidence.json` against `schema/definitions/reference.schema.json`

## What Is Stable

The following contracts are stable enough for early consumers:

- JSON Schema Draft 2020-12 is the schema language.
- Entity identity uses stable IDs, slugs, names, and entity types.
- Relationship predicates use uppercase snake case.
- Claims link to evidence through `evidenceIds`.
- Evidence links to references through `referenceIds`.
- Metadata is separated from domain knowledge.
- Registries define controlled entity and relationship vocabularies.
- The graph exports use stable IDs as node IDs and edge endpoints.
- The graph exports have an alpha/internal node and edge shape checked by JSON Schema and endpoint integrity validation.

## What Is Still Evolving

The following areas are still expected to change as RKM becomes more consumable:

- package-level schemas for example bundles
- graph export coverage beyond the first fixture contract and the current seed-data provenance export
- graph export compatibility policy beyond the current alpha/internal contract
- fixture coverage beyond the minimal package
- populated dataset breadth beyond the first three RAG techniques
- release packaging and version compatibility policy
- loader-specific guidance for databases, search indexes, and graph stores

Consumers should depend on the schema files and registries before depending on directory layout or package envelopes.

## Consumption Guidance

Load RKM content by stable identifier first. Slugs and names are useful for display and debugging, but IDs are the durable join keys.

Preserve relationship direction. For example, `TECHNIQUE-9001 DEPENDS_ON COMPONENT-9001` means the technique depends on the component. Inverse views should be generated by consumers only when needed for queries.

Treat claims as explicit statements, not comments. A claim should be linked to evidence and references when support is available.

Treat references as source records. Evidence explains how a source supports, contradicts, qualifies, or contextualizes a claim.

Keep metadata separate from domain interpretation. Fields such as `createdAt`, `updatedAt`, `status`, and `license` describe repository artifact management, not RAG behavior.
