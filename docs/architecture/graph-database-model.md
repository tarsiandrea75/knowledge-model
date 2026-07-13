# Graph Database Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how graph databases are represented in the RAG Knowledge Model.

Graph databases are storage entities that store, query and traverse graph-structured knowledge used by RAG retrievers, workflows, agents, evaluation processes and applications.

The Graph Database Model answers the question:

> **How should RKM describe graph storage systems whose graph model, query behavior, reasoning support, vector integration and operational constraints affect RAG retrieval and grounding?**

---

# Core Principle

A graph database is not only a persistence layer behind a knowledge graph.

A graph database is a first-class knowledge entity when its graph model, query language, traversal behavior, schema support, reasoning support, deployment model, scalability profile or integration surface materially affects RAG behavior.

```text
Retriever USES Graph Database
Framework SUPPORTS Graph Database
Provider PROVIDES Graph Database
Graph Database SUPPORTS Retriever
Benchmark EVALUATES Graph Database
Technique USES Graph Database
```

Representing graph databases explicitly allows RKM to separate graph storage capability from knowledge graph content, retriever behavior, provider availability and evidence-supported claims about graph retrieval.

---

# Graph Database

A Graph Database is an entity specialized for storing, querying and traversing graph-structured data.

Graph database entities may represent:

* native graph databases
* RDF triplestores
* multi-model databases with graph support
* relational databases with graph extensions
* search engines with graph support
* managed graph database services
* embedded graph databases
* in-memory graph stores

A graph database should be modeled when its capabilities are reusable across RAG systems or when its behavior affects retrieval quality, grounding, explainability, latency, cost, governance or reproducibility.

Preferred:

```text
Managed graph database that supports labeled property graphs, Cypher queries, path traversal, schema constraints and hybrid graph-vector retrieval for entity-centric RAG.
```

Avoid:

```text
Graph storage.
```

The avoided statement does not identify the storage boundary, graph model, query capability or RAG role.

---

# Entity Boundary

Every graph database should have a clear boundary.

The boundary identifies:

* which graph models the system stores
* which query languages or graph APIs it exposes
* which traversal, analytics, reasoning or vector integration behaviors are available
* which deployment models and providers make it available
* which consistency, scalability and operational characteristics apply
* which retrievers, frameworks, providers, datasets, benchmarks or workflows depend on it

A graph database should remain distinct from:

* a Dataset or knowledge graph stored inside the database
* a Retriever that turns graph queries into a RAG-facing retrieval capability
* a Framework that integrates with the database
* a Provider that hosts, sells or maintains the database
* a Workflow that uses graph-derived context
* a Benchmark that evaluates graph retrieval behavior

These entities may be connected through canonical relationships when the relationship has reusable semantic value.

---

# Graph Models

Graph model describes the representation supported by the database.

Common graph models include:

* property graph
* labeled property graph
* RDF
* knowledge graph
* document graph
* temporal graph
* hypergraph

Graph model knowledge should be represented when it affects interoperability, query language choice, ontology support, schema design, reasoning behavior or graph export.

A database that supports more than one graph model should describe each supported model only when that support is relevant to RAG usage or entity selection.

---

# Query Languages and Workloads

Query languages and workloads describe how graph knowledge can be retrieved, filtered, traversed and analyzed.

Important graph query knowledge includes:

* Cypher support
* Gremlin support
* SPARQL support
* SQL graph support
* native graph APIs
* traversal depth and path constraints
* subgraph search
* graph analytics
* entity resolution
* recommendation workloads

Query behavior should be structured when it affects retrieval quality, explainability, latency, reproducibility or workflow design.

Claims about query performance should identify the graph size, schema, query pattern, traversal depth, deployment profile, database version and evaluation date when those details affect interpretation.

---

# Schema and Reasoning Support

Schema support describes how the graph database constrains or validates graph structure.

Reasoning support describes whether the database can infer additional relationships, classifications or facts from stored graph knowledge.

Important schema and reasoning details include:

* schema-optional or schema-enforced operation
* uniqueness and existence constraints
* type and cardinality constraints
* ontology-driven validation
* RDF Schema or OWL support
* rule-based inference
* materialized inference
* query-time inference

Schema and reasoning support should be represented when it affects grounding, explainability, validation, graph export, governance or compatibility with ontology-driven RAG workflows.

---

# Vector Integration

Some graph databases support vector search, embeddings or hybrid graph-vector retrieval.

Vector integration should describe whether the graph database can:

* store embeddings on nodes or edges
* index vectors
* combine vector search with graph traversal
* filter vector results with graph constraints
* rerank graph candidates with vector similarity
* expose hybrid graph-vector retrieval through an API

Graph-vector integration should not collapse the graph database into a vector database.

When vector functionality is central enough to affect selection, RKM may represent both the graph database and a related Vector Database capability, connected through canonical relationships such as `SUPPORTS`, `USES`, `DEPENDS_ON` or `INTEGRATES_WITH`.

---

# Deployment and Operations

Graph database deployment affects cost, latency, governance and reliability.

Common deployment models include:

* self-hosted
* managed cloud
* serverless
* embedded
* local
* hybrid
* edge

Operational knowledge should describe the characteristics that matter for RAG design, including scalability, durability, consistency, backup support, monitoring, query latency, indexing latency, transaction behavior, multi-tenancy, access control and failure modes.

When a managed service and self-hosted deployment have materially different behavior, RKM should preserve that distinction through provider, deployment, claims, evidence and relationships.

---

# Relationship Use

Graph databases should be connected to other entities through canonical relationships when those relationships have reusable semantic value.

Useful graph database relationship patterns include:

```text
Retriever USES Graph Database
Retriever REQUIRES Graph Database
Framework SUPPORTS Graph Database
Provider PROVIDES Graph Database
Graph Database SUPPORTS Retriever
Benchmark EVALUATES Graph Database
Technique USES Graph Database
Component IMPLEMENTS Graph Database
Graph Database INTEGRATES_WITH Vector Database
Graph Database HAS_LIMITATION Limitation
```

Relationships should express graph-ready knowledge about dependency, compatibility, support, implementation, evaluation, integration and operational constraints.

---

# Evidence and Claims

Graph database claims require evidence when they describe behavior such as query support, traversal performance, reasoning correctness, scalability, reliability, cost, vector integration, compliance support or production suitability.

Examples of evidence-scoped graph database claims include:

* a database supports a specific graph model or query language
* a traversal pattern improves answer grounding in a documented workflow
* a graph-vector configuration improves recall under a named benchmark
* a schema constraint prevents invalid entity relationships in a documented corpus
* a managed deployment provides documented regional availability

Claims should not generalize beyond the database version, deployment model, graph model, schema, corpus, query workload, benchmark or evaluation date supported by evidence.

---

# Schema Alignment

Graph database entity documents are validated by `schema/graph-database.schema.json`.

The schema requires:

* `identity`
* `metadata`
* `description`
* `graphDatabase`

The `identity.entityType` value must be `GraphDatabase`.

The specialized `graphDatabase` object captures domain-specific structure such as database type, graph models, deployment models, query languages, supported workloads, schema support, reasoning support, vector integration, scalability, consistency, operations, RAG usage, limitations and usage guidance.

Shared concepts such as relationships, claims, evidence, references and external links remain outside the specialized object so they can be reused consistently across RKM entities and graph exports.

---

# Integration With Other Models

The Graph Database Model works with the Storage Model, Retrieval Model, Provider Model, Benchmark Model, Evidence Model and Relationship Model.

The Storage Model defines the broader storage boundary for vector and graph storage systems.

The Retrieval Model defines the RAG-facing retrieval capability that queries or traverses a graph database.

The Provider Model identifies organizations or platforms that provide, host or support graph database capabilities.

The Benchmark Model and Evidence Model preserve the evaluation context behind claims about graph retrieval quality, query behavior, performance and operational suitability.
