# Retrieval Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how retrieval knowledge is represented in the RAG Knowledge Model.

Retrieval knowledge explains how candidate documents, chunks, passages, graph nodes, records or external resources are selected, scored, filtered and ordered before they are used by downstream RAG stages.

The Retrieval Model answers the question:

> **How should RKM describe the retrieval and reranking capabilities that determine which knowledge is available to a RAG system?**

---

# Core Principle

Retrieval is not only a search call or vector database query.

Retrieval is a structured capability with inputs, targets, indexes, ranking behavior, filters, operational constraints, evaluation context and evidence.

```text
Retriever USES Embedding Model
Retriever REQUIRES Vector Database
Retriever OPTIONALLY_USES Reranker
Reranker USES Language Model
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Reranker
```

Representing retrieval explicitly allows RKM to compare approaches, identify dependencies, preserve evaluation context and explain downstream answer quality.

---

# Retriever

A Retriever is an entity that selects candidate artifacts from a corpus, index, database, graph, service or external resource.

A retriever may return:

* documents
* chunks
* passages
* graph nodes
* triples
* table rows
* code snippets
* search results
* external resources

Retriever entities should describe the retrieval approach, retrieval targets, input modalities, index requirements, query processing, ranking behavior, filtering behavior, outputs, capabilities, evaluation context and operational characteristics.

Preferred:

```text
Dense vector retriever that encodes text queries with an embedding model and returns ranked chunks from a vector database.
```

Avoid:

```text
Search layer.
```

The avoided statement does not identify the retrieval approach, target artifacts, index dependency or ranking behavior.

---

# Reranker

A Reranker is an entity that reorders, filters or scores candidate artifacts after an initial retrieval step.

Rerankers may be implemented through:

* cross encoders
* bi-encoder scoring
* sparse relevance scoring
* learning-to-rank methods
* LLM-based judging
* rank fusion
* rule-based scoring
* domain-specific scorers

Reranker entities should identify the scoring approach, candidate input shape, output ranking structure, model profile, deployment profile, evaluation context, latency impact, cost impact and quality impact.

A reranker should not be treated as the same entity as the retriever that supplies its candidates unless the boundary is intentionally modeled as a combined retrieval capability.

---

# Retrieval Target

A retrieval target is the artifact returned by a retrieval or reranking process.

Retrieval targets matter because different targets support different downstream reasoning and citation behavior.

Examples include:

* chunk-level retrieval for grounded question answering
* document-level retrieval for broad source discovery
* node retrieval for graph neighborhood expansion
* table-row retrieval for structured data lookup
* code-snippet retrieval for developer assistance
* citation-candidate retrieval for answer attribution

Retrieval target knowledge should be structured when it affects evaluation, context assembly, citation quality or workflow behavior.

---

# Query Processing

Query processing describes how the input query is interpreted before candidate selection.

Common query processing behaviors include:

* query rewriting
* query expansion
* decomposition
* intent classification
* metadata filter extraction
* natural language to structured query translation
* routing to specialized retrievers

Query processing may be modeled as a Prompt Technique, Technique, Component, Workflow step or Retriever capability depending on its reusable semantic role.

When query processing materially changes retrieval behavior, claims about the retriever should identify whether the claim applies before or after query processing.

---

# Index and Store Dependencies

Retrievers often depend on indexes or stores that shape their behavior.

Important dependencies include:

* vector databases
* graph databases
* full-text indexes
* sparse indexes
* relational databases
* document stores
* web search services
* metadata catalogs

Dependencies should be represented with canonical relationships when they have reusable meaning.

```text
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Retriever DEPENDS_ON Embedding Model
Framework PROVIDES Retriever
Provider PROVIDES Retriever
```

The retriever is distinct from the store or index it queries. A vector database may provide storage and similarity search, but the retriever entity describes the retrieval capability and its RAG-facing behavior.

---

# Ranking and Filtering

Ranking defines how candidates are ordered.

Filtering defines which candidates are eligible to be returned.

Important ranking and filtering knowledge includes:

* similarity metric
* sparse scoring method
* hybrid score fusion
* maximum marginal relevance
* graph traversal depth
* metadata predicates
* access-control filters
* freshness constraints
* score thresholds
* retrieval depth
* reranking depth

Ranking and filtering details should be preserved when they affect reproducibility, evaluation results, cost, latency or answer quality.

---

# Retrieval Evaluation

Retrieval evaluation should identify the evaluated target, task, dataset, metric, protocol and result.

Common retrieval evaluation metrics include:

* recall
* precision
* mean reciprocal rank
* normalized discounted cumulative gain
* hit rate
* context relevance
* citation support
* latency
* cost

Evaluation claims should distinguish initial retrieval from reranked retrieval.

Example:

```text
Benchmark EVALUATES Retriever
Benchmark EVALUATES Reranker
Evaluation Metric MEASURES Retriever
Evaluation Metric MEASURES Reranker
Evidence SUPPORTS Claim
```

Claims about retrieval quality should not be generalized beyond the corpus, dataset, query set, metric, retrieval depth, reranking configuration or evaluation date supported by evidence.

---

# Operational Characteristics

Retrieval capabilities often determine practical RAG system behavior.

Important operational characteristics include:

* latency
* throughput
* index freshness
* indexing cost
* query cost
* storage cost
* scalability
* reproducibility
* access control
* observability
* failure modes

Operational characteristics should be represented structurally when they affect architecture choices or tradeoffs.

For example, a cross-encoder reranker may improve precision while increasing latency and per-query cost.

---

# Relationship Use

Retrieval entities should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Retriever USES Embedding Model
Retriever REQUIRES Vector Database
Retriever USES Graph Database
Retriever OPTIONALLY_USES Reranker
Retriever IMPLEMENTS Technique
Retriever SUPPORTS Workflow
Reranker USES Language Model
Reranker COMPLEMENTS Retriever
Framework PROVIDES Retriever
Framework SUPPORTS Reranker
Benchmark EVALUATES Retriever
Benchmark EVALUATES Reranker
Retriever HAS_LIMITATION Limitation
Reranker HAS_TRADEOFF Tradeoff
```

Relationship targets should use stable identifiers whenever the target is represented as an RKM entity.

Plain prose may explain local retrieval behavior, but reusable dependencies, support statements, compatibility claims and evaluation results should be represented structurally.

---

# Claims and Evidence

Retrieval claims often depend on corpus composition, index configuration, embedding model, query distribution, reranking depth, filtering rules and evaluation protocol.

Claims that should cite evidence include:

* improves recall
* improves precision
* reduces hallucination
* improves citation support
* supports multilingual retrieval
* supports metadata filtering
* reduces latency
* increases cost
* scales to a corpus size
* depends on a specific index type

Evidence should record the retrieval configuration, corpus or dataset, query set, metric, evaluation date and relevant model or store versions whenever those details are available.

---

# Boundary With Related Models

Retrieval is closely related to other RKM concepts, but each has a distinct boundary.

## Retrieval vs Model

An embedding model or language model provides a scoring, encoding or reasoning capability.

A retriever or reranker uses that capability to select or order candidate artifacts for a RAG workflow.

## Retrieval vs Database

A vector database or graph database stores and queries indexed data.

A retriever describes the RAG-facing selection capability, including how queries are processed, which targets are returned and how candidates are ranked.

## Retrieval vs Component

A component is an architectural building block.

A retriever may be implemented by a component, exposed by a framework or provided as a service, but the retriever entity captures the reusable retrieval behavior.

## Retrieval vs Workflow

A workflow orders steps across a RAG process.

Retrieval and reranking may be workflow steps, but their reusable behavior should remain available as first-class Retriever and Reranker entities when it supports comparison, evaluation or graph export.
