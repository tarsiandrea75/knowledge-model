# Storage Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how storage systems are represented in the RAG Knowledge Model.

Storage systems preserve, index, query and expose the data structures that retrieval, generation, evaluation and governance workflows depend on.

The Storage Model answers the question:

> **How should RKM describe vector and graph storage systems that shape RAG retrieval behavior, operational constraints and evidence interpretation?**

---

# Core Principle

A storage system is not only an implementation detail behind a retriever.

A storage system is a first-class knowledge entity when its data model, index behavior, query capabilities, deployment model, consistency guarantees, scalability limits or operational constraints affect RAG system behavior.

```text
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Framework SUPPORTS Vector Database
Provider PROVIDES Graph Database
Vector Database DEPENDS_ON Embedding Model
Benchmark EVALUATES Vector Database
```

Representing storage explicitly allows RKM to compare retrieval infrastructure, identify dependencies, preserve evaluation context and explain tradeoffs that cannot be captured by a retriever entity alone.

---

# Storage Boundary

Every storage entity should define a clear boundary.

The boundary identifies:

* which data structures the system stores
* which query or retrieval operations it exposes
* which indexing approaches it supports
* which deployment models are available
* which consistency, scalability and operational characteristics apply
* which retrievers, frameworks, providers or models depend on it

Preferred:

```text
Managed vector database that stores dense text embeddings, supports HNSW indexing and metadata filtering, and is used by retrievers for chunk-level semantic search.
```

Avoid:

```text
Database for RAG.
```

The avoided statement does not identify the stored representation, index behavior, retrieval role or operational boundary.

---

# Vector Database

A Vector Database is a storage entity specialized for storing, indexing, filtering and retrieving vector representations.

Vector databases may support:

* dense vector search
* approximate nearest neighbor indexes
* exact vector search
* hybrid sparse and dense retrieval
* metadata filtering
* namespace or collection partitioning
* multimodal embeddings
* managed or self-hosted deployment

Important vector database knowledge includes supported index types, distance metrics, filtering behavior, supported modalities, scalability profile, consistency profile, integration surface, operational model and RAG usage.

Vector database entities should remain distinct from the embedding models that create vectors and from the retrievers that turn vector search into a RAG-facing retrieval capability.

---

# Graph Database

A Graph Database is a storage entity specialized for storing, querying and traversing graph-structured knowledge.

Graph databases may support:

* property graphs
* RDF graphs
* knowledge graphs
* graph traversal
* path finding
* subgraph search
* graph analytics
* entity resolution
* hybrid graph and vector retrieval

Important graph database knowledge includes graph model, query languages, supported workloads, schema support, reasoning support, vector integration, scalability profile, consistency profile, operational model and RAG usage.

Graph database entities should remain distinct from the knowledge graph content they store, the retrievers that query them and the workflows that assemble graph-derived context.

---

# Indexing and Query Behavior

Indexing and query behavior should be represented when it materially affects retrieval quality, latency, cost, reproducibility or operational risk.

For vector databases, important indexing details include:

* HNSW or graph-based approximate nearest neighbor indexes
* inverted file indexes
* product quantization
* scalar quantization
* flat indexes
* disk-based indexes
* hybrid sparse and dense indexes

For graph databases, important query details include:

* traversal depth
* path constraints
* graph query language
* schema enforcement
* reasoning support
* graph analytics support
* vector search integration

Claims about storage performance or retrieval quality should identify the index configuration, corpus, query workload, deployment profile and evaluation date when that context affects the claim.

---

# Metadata, Filtering and Access Control

Storage systems often determine which candidate artifacts are eligible for retrieval.

Metadata and filtering knowledge should be structured when it affects:

* tenant isolation
* access control
* document freshness
* jurisdiction or region constraints
* source type filtering
* time-window filtering
* user or role permissions
* retrieval reproducibility

Filtering behavior should not be collapsed into prose when it explains why a retriever returns different candidates under different workflow conditions.

---

# Deployment and Operations

Storage deployment affects cost, latency, governance and reliability.

Common deployment models include:

* self-hosted
* managed cloud
* serverless
* embedded
* local
* hybrid
* edge

Operational knowledge should describe the characteristics that matter for RAG design, including scalability, durability, consistency, backup support, monitoring, isolation, indexing latency, query latency and failure modes.

When a managed service and an open source deployment have materially different behavior, RKM should preserve that distinction through provider, deployment and evidence context instead of treating them as interchangeable.

---

# Relationship Use

Storage systems should be connected to other entities through canonical relationships when those relationships have reusable semantic value.

Useful storage relationship patterns include:

```text
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Framework SUPPORTS Vector Database
Framework SUPPORTS Graph Database
Provider PROVIDES Vector Database
Provider PROVIDES Graph Database
Vector Database DEPENDS_ON Embedding Model
Graph Database SUPPORTS Retriever
Benchmark EVALUATES Vector Database
Benchmark EVALUATES Graph Database
Component IMPLEMENTS Vector Database
```

Storage relationships should express graph-ready knowledge about dependency, compatibility, implementation, evaluation and provider availability.

---

# Evidence and Claims

Storage claims require evidence when they describe behavior such as performance, scalability, reliability, retrieval quality, compliance support or production suitability.

Examples of evidence-scoped storage claims include:

* a vector database improves recall under a named benchmark and embedding model
* a graph database supports a specific query language or graph model
* metadata filtering changes retrieval precision for a documented workload
* a managed deployment provides a documented availability or regional capability
* a hybrid graph and vector configuration improves citation support in a specific workflow

Claims should not generalize beyond the storage version, deployment model, corpus, workload, index configuration, query pattern or benchmark supported by evidence.

---

# Integration With Other Models

The Storage Model works with the Retrieval Model, Model Model, Provider Model, Evaluation Model and Evidence Model.

Retrieval entities describe the RAG-facing selection capability.

Model entities describe embedding, reranking and language capabilities that produce or consume stored representations.

Provider entities describe who makes storage capabilities available and under which access or governance conditions.

Evaluation entities describe how storage-dependent behavior is measured.

Evidence entities preserve the source context behind storage claims.
