# Consumer Guide

## Purpose

This guide explains how another team can inspect, validate, and export the first small RAG Knowledge Model fixture package.

RKM is a structured knowledge model for the Retrieval-Augmented Generation ecosystem. Consumers should treat entities, relationships, claims, evidence, references, and metadata as separate but connected concepts.

## Fixture Package

The minimal consumer package lives under `examples/fixtures/`.

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

## Minimal Graph Export

The same fixture package can be exported to a minimal graph representation under `examples/graph-export/`. The current graph export is intentionally minimal and fixture-derived. It proves the first export contract path and validation wiring, but it is not a complete or production-grade graph product.

The graph export is derived from the committed fixtures. It contains:

- `minimal-graph.nodes.json`: a deterministic array of graph nodes.
- `minimal-graph.edges.json`: a deterministic array of graph edges.

Generate the export from the project root:

```bash
make graph-export
```

Check that the committed export still matches the fixtures:

```bash
python3 scripts/export-fixtures-graph.py --check
```

The repository validator runs this consistency check, so stale graph export files fail `make validate`.

## How To Validate

Run repository validation from the project root:

```bash
make validate
```

This runs schema validity checks, fixture instance validity checks, graph export consistency checks, and the rest of the repository validation suite:

- whitespace validation
- file encoding and line ending checks
- forbidden naming checks
- incomplete content marker checks
- JSON Schema validation for repository schemas
- schema prerequisite validation
- schema contract validation
- registry validation
- fixture instance validation using `examples/fixtures/fixture-manifest.json`
- graph export consistency validation using `scripts/export-fixtures-graph.py --check`
- RKM unit tests
- documentation relationship validation

Fixture validation loads `examples/fixtures/fixture-manifest.json`, resolves fixture and schema paths from the repository root, and validates each fixture instance against its declared schema. The claim package fixture is an envelope, so its `claim`, `evidence`, and `reference` objects are validated against their corresponding definition schemas.

Graph export generation is handled by:

```bash
make graph-export
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
- The minimal graph export uses stable IDs as node IDs and edge endpoints.

## What Is Still Evolving

The following areas are still expected to change as RKM becomes more consumable:

- package-level schemas for example bundles
- graph export coverage beyond the first minimal contract
- fixture coverage beyond the minimal package
- release packaging and version compatibility policy
- loader-specific guidance for databases, search indexes, and graph stores

Consumers should depend on the schema files and registries before depending on directory layout or package envelopes.

## Consumption Guidance

Load RKM content by stable identifier first. Slugs and names are useful for display and debugging, but IDs are the durable join keys.

Preserve relationship direction. For example, `TECHNIQUE-9001 DEPENDS_ON COMPONENT-9001` means the technique depends on the component. Inverse views should be generated by consumers only when needed for queries.

Treat claims as explicit statements, not comments. A claim should be linked to evidence and references when support is available.

Treat references as source records. Evidence explains how a source supports, contradicts, qualifies, or contextualizes a claim.

Keep metadata separate from domain interpretation. Fields such as `createdAt`, `updatedAt`, `status`, and `license` describe repository artifact management, not RAG behavior.
