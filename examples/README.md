# RKM Examples

This directory contains small examples for teams that want to consume RAG Knowledge Model content outside this repository.

The examples are intentionally compact. They show the shape of RKM artifacts without requiring a populated dataset or application-specific loader.

## Contents

- `fixtures/`: minimal JSON fixtures for entity, relationship, claim, evidence, and reference consumption.
- `graph-export/`: reproducible nodes and edges generated from the minimal fixtures.
- `data-graph-export/`: reproducible nodes and edges generated from the validated seed dataset under `data/`.

## Validation

Run the repository validation from the project root:

```bash
make validate
```

The repository validator checks schema contracts, registries, documentation relationships, graph export freshness, whitespace, file hygiene, and project naming rules.

Fixture consumers can also validate individual fixture objects against the schemas they reference. The minimal RAG technique fixture is shaped for `schema/rag-technique.schema.json`. The minimal relationship fixture is shaped for `schema/definitions/relationship.schema.json`. The claim, evidence, and reference bundle contains inner objects shaped for `schema/definitions/claim.schema.json`, `schema/definitions/evidence.schema.json`, and `schema/definitions/reference.schema.json`.

## Stability

Stable for consumers:

- stable identifiers such as `TECHNIQUE-9001`, `RELATIONSHIP-9001`, `CLAIM-9001`, `EVIDENCE-9001`, and `REFERENCE-9001`
- uppercase snake case relationship predicates
- JSON Schema Draft 2020-12 schema contracts
- the separation between entities, relationships, claims, evidence, references, and metadata

Still evolving:

- fixture package layout
- graph export coverage beyond the minimal fixture package and current seed data
- content coverage across the RAG ecosystem
- additional consumer tooling for validating example packages as a group
