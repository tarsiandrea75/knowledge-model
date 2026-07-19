# RKM Data

The `data/` directory contains populated RKM seed knowledge. It is distinct from `examples/fixtures/`, which contains minimal pedagogical examples used to demonstrate schema shape and validation mechanics.

Seed data is intended for validation, consumer testing, graph export, and decision-query workflows. It is not a complete catalog of the RAG ecosystem, and record presence does not imply semantic approval.

## Manifest and Validation

Every populated data file is declared in `data/manifest.json`. Each manifest entry maps a repository-relative data path to the schema that validates it.

The standard validation pipeline checks:

- JSON Schema conformance;
- identifier uniqueness;
- manifest coverage;
- relationship endpoints;
- relationship-support links;
- graph-export consistency;
- entity-specific semantic rules.

Run direct data validation from the repository root:

```bash
make data-validate
```

Run full repository validation:

```bash
make validate
```

## Current Manifest-Declared Scope

The current manifest declares 36 populated data files:

- 6 RAG technique records under `data/rag-techniques/`;
- 4 Component records under `data/components/`;
- 2 Retriever records under `data/retrievers/`;
- 1 Reranker record under `data/rerankers/`;
- 17 VectorDatabase records under `data/vector-databases/`;
- 3 relationship sets under `data/relationships/`;
- 3 relationship-support sets under `data/relationship-support/`.

Directory-level README files provide local guidance for the established technique, component, retriever, reranker, relationship, and relationship-support record sets.

## VectorDatabase Records

`data/vector-databases/` contains first-class records that validate against `schema/vector-database.schema.json`.

The current set covers:

- Amazon Neptune Analytics;
- Azure AI Search;
- Chroma;
- Elasticsearch;
- LanceDB;
- Memgraph;
- Milvus;
- MongoDB;
- Neo4j;
- OpenSearch;
- pgvector;
- Pinecone;
- Qdrant;
- Redis;
- Vertex AI Vector Search;
- Vespa;
- Weaviate.

These records model deployment forms, supported retrieval methods, structured capabilities, capability origins, availability scopes, operational characteristics, limitations, evidence, and references.

All 17 records retain `Draft` status. Neo4j is the sole record whose `metadata.reviewState` is `Approved`; the other sixteen remain `Not Reviewed`. Consumers must inspect each record's lifecycle fields, claims, evidence, references, qualifiers, limitations, and guidance before using it for decisions.

Use the decision-query CLI for source-linked entity views and same-type comparisons:

```bash
python3 scripts/rkm-decision-query.py --entity neo4j --detail full
python3 scripts/rkm-decision-query.py --compare neo4j qdrant
```

The CLI is descriptive. It does not convert `Draft` or `Not Reviewed` records into recommendations or approved guidance.

## Relationships and Support

`data/relationships/` contains declared relationship instances between populated data records. These sets are validated through the manifest and exported as domain graph edges.

`data/relationship-support/` contains support objects for relationship instances. These objects connect relationship IDs to references, claims, and evidence so consumers can inspect why a relationship appears in the seed dataset.

Domain relationships and their support are declared explicitly. They are not inferred from names, descriptions, stages, component roles, capabilities, or other record fields.

## Data Graph Export

The populated dataset has a deterministic derived graph representation under `examples/data-graph-export/`.

The current export includes Technique, Component, Retriever, Reranker, VectorDatabase, and Schema nodes; schema-validation provenance edges; and declared domain relationship edges. Generated graph artifacts are derived outputs and must remain consistent with the manifest-declared source data.

Regenerate the data graph export:

```bash
make data-graph-export
```

Validate the committed graph export:

```bash
make graph-export-validate
```

## Changing Data

Follow `data/AGENTS.md` and the applicable task guide before changing any populated record.

For an existing entity type, use:

```text
docs/maintenance/task-guides/adding-data-records.md
```

A data-record change may require coordinated updates to:

- `data/manifest.json`;
- declared relationships;
- relationship-support records;
- `examples/data-graph-export/*.nodes.json`;
- `examples/data-graph-export/*.edges.json`.

Do not treat data files as loose examples, infer domain edges from prose, reuse stable IDs, or report readiness without running the routed validation commands.
