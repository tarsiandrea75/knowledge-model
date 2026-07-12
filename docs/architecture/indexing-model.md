# Indexing Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how indexing knowledge is represented in the RAG Knowledge Model.

Indexing describes how source artifacts, chunks, embeddings, metadata and graph structures are transformed into queryable retrieval structures.

The Indexing Model answers the question:

> **How should RKM describe the preparation, storage and update behavior that makes knowledge retrievable in a RAG system?**

---

# Core Principle

Indexing is first-class knowledge when it affects retrieval quality, latency, freshness, cost, governance, reproducibility or evidence interpretation.

It is not only a background storage operation.

Indexing connects chunking, embedding, metadata propagation, storage systems, retrieval behavior and operational maintenance.

```text
Component IMPLEMENTS Chunking Strategy
Component USES Embedding Model
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Workflow DEPENDS_ON Component
Benchmark EVALUATES Retriever
```

Representing indexing explicitly allows RKM to explain why the same retriever, model or storage system may behave differently across corpora, update policies and index configurations.

---

# Indexing Scope

An indexing scope defines what is prepared for retrieval and where the indexed representation is maintained.

The scope should identify:

* source artifacts included in the index
* chunking strategy or parsing behavior used before indexing
* embedding model or feature extraction method used during indexing
* metadata fields propagated into the index
* vector database, graph database or other store that holds the indexed representation
* refresh, deletion and reindexing behavior
* retrieval workflows that depend on the indexed representation

Preferred:

```text
Documentation indexing workflow that chunks Markdown sections, creates dense embeddings, preserves source URLs and heading metadata, and writes vectors to a managed vector database.
```

Avoid:

```text
Index the docs.
```

The avoided statement does not identify indexed artifacts, transformation behavior, metadata, storage target or refresh semantics.

---

# Indexed Artifact

An indexed artifact is a retrieval-ready representation derived from one or more source artifacts.

Common indexed artifacts include:

* parsed document
* chunk
* passage
* embedding vector
* sparse vector
* graph node
* graph edge
* metadata record
* citation candidate
* index record

Indexed artifacts should preserve stable references to their source artifacts when they support citation, access control, freshness checks, deletion, evaluation or provenance.

The indexed artifact is distinct from the source artifact. A source document may produce many chunks, embeddings or graph records, and those derived artifacts may have different lifecycle and governance requirements.

---

# Index Configuration

Index configuration describes the choices that shape retrieval behavior.

Important configuration includes:

* index type
* distance or similarity metric
* vector dimensionality
* sparse scoring method
* graph traversal structure
* metadata filter schema
* namespace or collection layout
* shard or partition policy
* deduplication behavior
* update strategy
* deletion strategy
* compaction or optimization behavior

Configuration should be structured when it affects reproducibility, benchmark interpretation, latency, cost, access control or answer grounding.

For example, a retrieval quality claim should not omit the embedding model, chunking strategy, index type, similarity metric and retrieval depth when those values materially affect the result.

---

# Metadata Propagation

Metadata propagation describes which source metadata is copied, transformed or derived during indexing.

Important propagated metadata includes:

* source identifier
* document version
* section or page location
* author or owner
* timestamp
* access-control attributes
* tenant or namespace
* content type
* language
* citation fields
* deletion marker

Metadata propagation is a modeling concern because retrievers often depend on indexed metadata for filtering, authorization, freshness and citation assembly.

Access-control metadata should not be described only in prose when it determines which indexed artifacts are eligible for retrieval.

---

# Freshness and Reindexing

Index freshness describes how closely indexed artifacts reflect their source artifacts.

Freshness knowledge should identify:

* update trigger
* indexing cadence
* incremental or full reindexing behavior
* stale artifact handling
* deletion propagation
* failure recovery
* version compatibility
* evidence collection for update behavior

Freshness claims require evidence when they describe production behavior, service guarantees, benchmark conditions or suitability for time-sensitive use cases.

An index built from a static benchmark corpus should not be treated as equivalent to an operational index that receives continuous document updates and deletions.

---

# Relationship Use

Indexing knowledge should use canonical relationships when the association has reusable graph meaning.

Useful indexing relationship patterns include:

```text
Component IMPLEMENTS Chunking Strategy
Component USES Embedding Model
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Vector Database DEPENDS_ON Embedding Model
Workflow DEPENDS_ON Component
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Retriever
Evidence SUPPORTS Claim
```

These relationships should be used to connect indexing behavior to retrieval dependencies, storage systems, evaluation context and evidence-backed claims.

Plain prose may explain local implementation details, but reusable dependencies and evaluation-relevant choices should be represented structurally.

---

# Evidence and Claims

Indexing claims require evidence when they describe retrieval quality, freshness, latency, scalability, cost, governance or operational reliability.

Examples of evidence-scoped indexing claims include:

* a chunking strategy improves retrieval recall for a named corpus and metric
* a metadata filter prevents unauthorized chunks from entering retrieval results
* an incremental indexing workflow propagates deletions within a documented time window
* a vector index configuration reduces query latency for a measured workload
* a graph indexing approach improves multi-hop retrieval on a specific benchmark

Claims should not generalize beyond the corpus, source version, chunking strategy, embedding model, index configuration, storage system, retrieval depth, workload or observation date supported by evidence.

---

# Integration With Other Models

The Indexing Model connects to the Chunking Model when source artifacts are segmented into retrieval units.

It connects to the Embedding Model Model when indexed artifacts include embedding vectors.

It connects to the Storage Model when vector databases or graph databases hold indexed representations.

It connects to the Retrieval Model when retrievers query indexed structures.

It connects to the Workflow Model when indexing is represented as an ordered or conditional process.

It connects to the Evidence Model when indexing behavior supports claims about retrieval quality, freshness, governance or operational performance.
