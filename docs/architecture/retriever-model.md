# Retriever Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how retrievers are represented in the RAG Knowledge Model.

Retrievers are entities that select candidate documents, chunks, passages, graph nodes, records or external resources for downstream Retrieval-Augmented Generation stages.

The Retriever Model answers the question:

> **How should RKM describe retrieval capabilities that determine which candidate knowledge becomes available to a RAG workflow?**

---

# Core Principle

A retriever is not only a database query, vector search call or framework helper.

A retriever is a reusable RAG-facing capability with a defined retrieval approach, target artifact type, query processing behavior, index dependency, ranking behavior, filtering behavior, output structure, operational profile and evaluation context.

```text
Retriever USES Embedding Model
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Retriever OPTIONALLY_USES Reranker
Framework PROVIDES Retriever
Benchmark EVALUATES Retriever
```

Representing retrievers explicitly allows RKM to distinguish retrieval behavior from storage systems, embedding models, rerankers, frameworks and provider offerings.

---

# Retriever

A Retriever is an entity that selects candidate artifacts from a corpus, index, database, graph, service or external resource.

Retriever entities may return:

* documents
* chunks
* passages
* graph nodes
* triples
* table rows
* images
* code snippets
* search results
* external resources

A retriever should be modeled when its retrieval behavior is reusable across RAG systems or when it affects answer quality, citation support, latency, cost, governance, reproducibility or evaluation results.

Preferred:

```text
Hybrid retriever that combines dense vector similarity and sparse lexical search, applies metadata filters and returns ranked chunks for context assembly.
```

Avoid:

```text
Search component.
```

The avoided statement does not identify the retrieval approach, target artifacts, index dependency, ranking behavior or downstream RAG role.

---

# Retriever Boundary

Every retriever should have a clear boundary.

The boundary identifies:

* which query inputs the retriever accepts
* which corpus, index, store, graph or external service it queries
* which candidate artifact types it returns
* which ranking and filtering behaviors are part of the retriever
* which embedding models, vector databases, graph databases or external search APIs it depends on
* whether reranking is external to the retriever or intentionally modeled as part of a combined retrieval capability
* which downstream workflow step consumes the retriever output

A retriever should remain distinct from:

* an Embedding Model that creates query or document vectors
* a Vector Database that stores and searches vector representations
* a Graph Database that stores graph-structured knowledge
* a Reranker that reorders candidates after initial retrieval
* a Framework that exposes retriever abstractions or integrations
* a Provider that hosts, maintains or sells retrieval services

These entities may be connected through canonical relationships when the relationship has reusable semantic value.

---

# Retriever Type

Retriever type describes the primary retrieval capability represented by the entity.

Canonical retriever types include:

```text
Dense Vector Retriever
Sparse Retriever
Hybrid Retriever
Keyword Retriever
Graph Retriever
Multi Vector Retriever
Parent Document Retriever
Self Query Retriever
Metadata Filtered Retriever
Router Retriever
Ensemble Retriever
Web Retriever
Database Retriever
Other
```

The type should describe the dominant retrieval pattern. More specific behavior should be represented through retrieval approach, index requirements, query processing, ranking, filtering, outputs, relationships, claims and evidence.

---

# Retrieval Approach

Retrieval approach describes how candidates are selected from the underlying corpus, index or service.

Common approaches include:

* similarity search
* maximum marginal relevance
* lexical search
* Boolean search
* hybrid search
* graph traversal
* metadata filtering
* SQL query execution
* full text search
* federated search
* learned retrieval
* heuristic retrieval

The approach should be explicit when it affects recall, precision, citation support, latency, cost, portability or benchmark interpretation.

---

# Retrieval Targets

Retrieval targets describe the artifacts returned by the retriever.

Target artifacts matter because different targets support different downstream behavior. Chunk-level retrieval may support grounded answer generation, document-level retrieval may support source discovery, graph-node retrieval may support neighborhood expansion and table-row retrieval may support structured lookup.

Retrieval target knowledge should be structured when it affects context assembly, citation quality, evaluation metrics, workflow design or graph export.

---

# Query Processing

Query processing describes how an input query is transformed or constrained before candidate selection.

Important query processing behavior includes:

* query embedding
* query expansion
* query rewriting
* structured filter extraction
* natural language filtering
* routing to specialized indexes or retrievers
* dependency on an embedding model or language model

Query processing may also be represented as a Technique, Prompt Technique, Component or Workflow step when it has reusable semantic meaning outside one retriever.

Claims about retriever quality should identify whether query processing is part of the evaluated configuration.

---

# Index and Store Requirements

Retrievers often depend on indexes, stores or external services that shape their behavior.

Common requirements include:

* vector indexes
* inverted indexes
* full text indexes
* graph indexes
* keyword indexes
* metadata indexes
* relational tables
* external search APIs

These requirements should be represented structurally when they affect reproducibility, portability, operational risk or entity selection.

```text
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Retriever DEPENDS_ON Embedding Model
Provider PROVIDES Retriever
```

The retriever is distinct from the store or index it queries. A database may provide search primitives, but the retriever entity describes the RAG-facing retrieval capability and its behavior in a workflow.

---

# Ranking and Filtering

Ranking describes how candidates are ordered before optional downstream reranking.

Filtering describes which candidates are eligible to be returned.

Important ranking and filtering knowledge includes:

* primary score type
* top-k behavior
* score thresholds
* diversity-aware selection
* rank fusion
* metadata filters
* date range filters
* source filters
* access-control filters
* language filters
* tenant filters
* graph constraints

Ranking and filtering details should be preserved when they affect evaluation results, answer quality, citation behavior, latency, cost or governance.

---

# Outputs

Retriever output describes what the downstream RAG system receives.

Common outputs include:

* ranked candidates
* unranked candidates
* scored documents
* scored chunks
* graph nodes
* graph paths
* query results
* context candidates

Output structure should identify whether scores, metadata or other attributes are included when downstream context assembly, reranking, citation or evaluation depends on them.

---

# Evaluation

Retriever evaluation should identify the evaluated target, corpus, query set, configuration, dataset, benchmark, metric, protocol and result.

Common retriever metrics include:

* recall at k
* precision at k
* mean reciprocal rank
* mean average precision
* normalized discounted cumulative gain
* hit rate
* latency
* cost
* context relevance
* answer correctness

Example:

```text
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Retriever
Evidence SUPPORTS Claim
```

Claims about retriever quality should not be generalized beyond the corpus, dataset, query set, retrieval depth, filtering rules, embedding model, index configuration, metric, benchmark or evaluation date supported by evidence.

---

# Operational Characteristics

Retrievers often determine the practical behavior of RAG systems.

Operational characteristics may include:

* latency sensitivity
* cost sensitivity
* index freshness sensitivity
* scale sensitivity
* recall sensitivity
* precision sensitivity
* throughput limits
* failure modes
* access-control behavior
* observability requirements

Operational knowledge should be represented when it affects system design, framework compatibility, deployment choice, production suitability or use-case fit.

---

# Relationship Use

Retrievers should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Retriever USES Embedding Model
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Retriever OPTIONALLY_USES Reranker
Retriever IMPLEMENTS Technique
Retriever SUPPORTS Workflow
Framework PROVIDES Retriever
Framework SUPPORTS Retriever
Provider PROVIDES Retriever
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Retriever
Paper INTRODUCES Retriever
Retriever HAS_LIMITATION Limitation
Retriever HAS_TRADEOFF Tradeoff
```

Relationships should express graph-ready knowledge rather than restating prose. When a relationship depends on a specific configuration or benchmark result, the relationship should be supported by claims, evidence and references.

---

# Schema Alignment

Retriever entity documents are validated by `schema/retriever.schema.json`.

The schema requires:

* `identity`
* `metadata`
* `description`
* `retriever`

The `identity.entityType` value must be `Retriever`.

The specialized `retriever` object captures domain-specific structure such as retriever type, retrieval approach, retrieval targets, input modalities, index requirements, query processing, ranking, filtering, outputs, RAG stages, capabilities, evaluation, operational characteristics, limitations and usage guidance.

Shared concepts such as relationships, claims, evidence, references and external links remain outside the specialized object so they can be reused consistently across RKM entities and graph exports.

---

# Integration With Other Models

The Retriever Model works with the Retrieval Model, Reranker Model, Embedding Model Model, Vector Database Model, Graph Database Model, Framework Model, Provider Model, Benchmark Model, Evidence Model and Relationship Model.

The Retrieval Model defines the broader retrieval knowledge boundary for candidate selection, scoring, filtering and ordering.

The Reranker Model defines post-retrieval candidate reordering and scoring behavior.

The Embedding Model Model defines models that produce query or document vectors used by dense and hybrid retrievers.

The Vector Database Model and Graph Database Model define storage systems and query capabilities that retrievers may depend on.

The Framework Model and Provider Model describe software abstractions and organizations that expose or supply retriever capabilities.

The Benchmark Model, Evidence Model and Relationship Model preserve the evaluation, evidence and graph structure behind retriever claims.
