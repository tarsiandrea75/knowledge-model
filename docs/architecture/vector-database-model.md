# Vector Database Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how vector databases are represented in the RAG Knowledge Model.

Vector databases are storage entities that store, index, filter and retrieve vector representations used by RAG retrievers, workflows, benchmarks and applications.

The Vector Database Model answers the question:

> **How should RKM describe vector storage systems whose indexing, query behavior, deployment model and operational constraints affect RAG retrieval quality?**

---

# Core Principle

A vector database is not only a backing store behind a retriever.

A vector database is a first-class knowledge entity when its index support, distance metrics, metadata filtering, deployment model, consistency behavior, scalability profile or integration surface materially affects RAG behavior.

```text
Retriever REQUIRES Vector Database
Framework SUPPORTS Vector Database
Provider PROVIDES Vector Database
Vector Database DEPENDS_ON Embedding Model
Benchmark EVALUATES Vector Database
Technique USES Vector Database
```

Representing vector databases explicitly allows RKM to separate storage capability from embedding model behavior, retriever behavior, provider availability and evidence-supported performance claims.

---

# Vector Database

A Vector Database is an entity specialized for storing vector representations and making them searchable through similarity, filtering or hybrid retrieval operations.

Vector database entities may represent:

* dedicated vector databases
* search engines with vector support
* relational databases with vector extensions
* NoSQL databases with vector support
* graph databases with vector support
* in-memory vector stores
* embedded vector stores
* managed vector search services

A vector database should be modeled when its capabilities are reusable across RAG systems or when its behavior affects retrieval quality, latency, cost, governance or reproducibility.

Preferred:

```text
Managed vector database that supports HNSW indexing, cosine similarity, metadata filtering and hybrid sparse-dense search for chunk-level retrieval.
```

Avoid:

```text
Vector search tool.
```

The avoided statement does not identify the storage boundary, index behavior, query capability or RAG role.

---

# Entity Boundary

Every vector database should have a clear boundary.

The boundary identifies:

* which vector representations the system stores
* which index types and distance metrics it supports
* which filtering, partitioning and hybrid search behaviors are available
* which deployment models and providers make it available
* which consistency, scalability and operational characteristics apply
* which retrievers, frameworks, embedding models, providers or benchmarks depend on it

A vector database should remain distinct from:

* an Embedding Model that creates vectors
* a Retriever that turns vector search into a RAG-facing retrieval capability
* a Provider that hosts, sells or maintains the database
* a Dataset or corpus stored inside the database
* a Benchmark that evaluates retrieval behavior using the database

These entities may be connected through canonical relationships when the relationship has reusable semantic value.

---

# Index Support

Index support describes the retrieval structures or search approaches available in the database.

Important index knowledge includes:

* flat exact search
* HNSW indexes
* inverted file indexes
* product quantization
* scalar quantization
* disk-based approximate nearest neighbor indexes
* graph-based approximate nearest neighbor indexes
* hybrid sparse and dense indexes

Index details should be represented when they affect retrieval quality, latency, cost, memory use, update behavior or reproducibility.

Claims about index performance should identify the corpus, vector dimensionality, distance metric, hardware, deployment model, query workload, index configuration and evaluation date when those details affect interpretation.

---

# Distance Metrics and Vector Compatibility

Distance metrics describe how stored vectors are compared at query time.

Common vector comparison methods include:

* cosine similarity
* dot product
* Euclidean distance
* Manhattan distance
* Hamming distance
* Jaccard similarity

Vector compatibility matters because embedding models may expect specific normalization behavior, dimensionality, distance metrics or sparse-dense representation shapes.

Compatibility should be modeled through structured fields and canonical relationships instead of prose-only claims when it affects entity selection or graph export.

---

# Filtering and Hybrid Search

Filtering defines which stored objects are eligible for retrieval.

Hybrid search combines vector retrieval with other retrieval signals such as sparse lexical search, full-text search, metadata constraints, graph constraints or rule-based filters.

Filtering and hybrid search knowledge should be structured when it affects:

* tenant isolation
* access control
* document freshness
* source selection
* jurisdiction or region constraints
* metadata predicates
* sparse-dense score fusion
* retrieval reproducibility

Filtering behavior should not be collapsed into general feature prose when it explains why one RAG workflow returns different context from another.

---

# Deployment and Operations

Vector database deployment affects cost, latency, governance and reliability.

Common deployment models include:

* self-hosted
* managed cloud
* serverless
* embedded
* local
* hybrid
* edge

Operational knowledge should describe the characteristics that matter for RAG design, including scalability, durability, consistency, backup support, monitoring, indexing latency, query latency, update behavior, multi-tenancy and failure modes.

When a managed service and self-hosted deployment have materially different behavior, RKM should preserve that distinction through provider, deployment, claims, evidence and relationships.

---

# Relationship Use

Vector databases should be connected to other entities through canonical relationships when those relationships have reusable semantic value.

Useful vector database relationship patterns include:

```text
Retriever REQUIRES Vector Database
Framework SUPPORTS Vector Database
Provider PROVIDES Vector Database
Vector Database DEPENDS_ON Embedding Model
Vector Database SUPPORTS Retriever
Benchmark EVALUATES Vector Database
Technique USES Vector Database
Component IMPLEMENTS Vector Database
Vector Database HAS_LIMITATION Limitation
```

Relationships should express graph-ready knowledge about dependency, compatibility, support, implementation, evaluation and operational constraints.

---

# Evidence and Claims

Vector database claims require evidence when they describe behavior such as retrieval quality, latency, scalability, reliability, cost, consistency, filtering correctness, compliance support or production suitability.

Examples of evidence-scoped vector database claims include:

* a database supports a specific index type or distance metric
* a metadata filter changes retrieval precision for a documented workload
* a hybrid search configuration improves recall under a named benchmark
* a managed deployment provides documented region availability
* an index configuration reduces latency for a specified vector dimensionality and corpus size

Claims should not generalize beyond the database version, deployment model, index configuration, embedding model, corpus, query workload, metric, benchmark or evaluation date supported by evidence.

---

# Schema Alignment

Vector database entity documents are validated by `schema/vector-database.schema.json`.

The schema requires:

* `identity`
* `metadata`
* `description`
* `vectorDatabase`

The `identity.entityType` value must be `VectorDatabase`.

The specialized `vectorDatabase` object captures domain-specific structure such as database type, deployment models, supported index types, distance metrics, supported modalities, metadata filtering, hybrid search, scalability, consistency, integration, operations, RAG usage, limitations and usage guidance.

Shared concepts such as relationships, claims, evidence, references and external links remain outside the specialized object so they can be reused consistently across RKM entities and graph exports.

---

# Integration With Other Models

The Vector Database Model works with the Storage Model, Retrieval Model, Embedding Model Model, Provider Model, Benchmark Model, Evidence Model and Relationship Model.

The Storage Model defines the broader storage boundary for vector and graph storage systems.

The Retrieval Model defines the RAG-facing retrieval capability that queries a vector database.

The Embedding Model Model defines the models that produce vectors stored by the database.

The Provider Model identifies organizations or platforms that provide, host or support vector database capabilities.

The Benchmark Model and Evidence Model preserve the evaluation context behind claims about retrieval quality, performance and operational suitability.
