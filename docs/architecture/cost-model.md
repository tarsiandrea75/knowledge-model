# Cost Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how cost knowledge is represented in the RAG Knowledge Model.

Cost knowledge explains the economic constraints, measurement boundaries and evidence that affect the selection, operation, evaluation and comparison of RAG entities.

The Cost Model answers the question:

> **What cost is being measured, under which workload and deployment context, and how should that cost be connected to claims, evidence and relationships?**

---

# Core Principle

Cost is first-class knowledge when it changes how a RAG entity, workflow, provider, model, retriever, database or evaluation result should be interpreted.

Cost is not only a price string.

A cost statement should identify the cost driver, workload, unit, deployment context, time boundary and supporting evidence.

```text
Workflow DEPENDS_ON Provider
Provider PROVIDES Language Model
Retriever REQUIRES Vector Database
Evaluation Metric MEASURES Cost Attribute
Benchmark EVALUATES Workflow
Evidence SUPPORTS Claim
Evidence REFERENCES Source
```

Representing cost explicitly allows RKM to compare tradeoffs, preserve evaluation context and avoid treating cost-sensitive claims as universally true.

---

# Cost Boundary

Every cost statement should define a clear boundary.

The boundary identifies:

* the entity, workflow or deployment being measured
* the cost driver being observed
* the workload or usage pattern
* the unit of measurement
* the provider, region or hosting model when relevant
* the time period or pricing date
* the evidence that supports the statement

Preferred:

```text
Generation cost for a workflow using a managed language model endpoint, measured as input and output tokens per grounded answer under a documented benchmark workload.
```

Avoid:

```text
This workflow is cheap.
```

The avoided statement does not identify the measured entity, workload, unit, deployment context or evidence boundary.

---

# Cost Driver

A cost driver is a factor that materially affects the cost of using, evaluating or operating a RAG entity.

Common cost drivers include:

* input tokens
* output tokens
* embedding tokens
* reranking candidates
* retrieval depth
* indexed document volume
* stored vector count
* graph node and edge volume
* query volume
* request concurrency
* model invocation count
* tool invocation count
* storage capacity
* compute time
* network transfer
* human review time

Cost drivers should be structured when they are reused across claims, evaluation metrics, workflows, deployment choices or tradeoff analysis.

---

# Cost Unit

A cost unit defines how cost is measured or normalized.

Useful cost units include:

* cost per query
* cost per generated answer
* cost per document ingested
* cost per embedded token
* cost per indexed chunk
* cost per reranked candidate
* cost per workflow run
* cost per evaluation task
* cost per stored vector
* cost per tenant
* cost per time period

Cost units should be explicit because the same system may appear inexpensive under one unit and expensive under another.

For example, a retriever may have low query cost but high indexing cost when a corpus changes frequently.

---

# Workload Context

Cost claims are meaningful only within a workload context.

Important workload details include:

* corpus size
* document update frequency
* query volume
* query length
* answer length
* retrieval depth
* reranking depth
* context window usage
* number of model calls
* number of tool calls
* evaluation dataset size
* concurrency profile

Claims about cost should not generalize beyond the workload, provider, deployment context, model version, pricing date or measurement protocol supported by evidence.

---

# Cost and Evaluation

Cost can be an evaluation target or an evaluation constraint.

As an evaluation target, a cost attribute may be measured directly through an Evaluation Metric.

As an evaluation constraint, cost may bound which models, retrievers, indexes, rerankers or workflows are acceptable for a use case.

Examples include:

```text
Evaluation Metric MEASURES Cost Attribute
Benchmark EVALUATES Workflow
Benchmark EVALUATES Retriever
Benchmark USES Dataset
Evidence SUPPORTS Claim
```

Evaluation records should distinguish cost from quality metrics such as recall, faithfulness or answer correctness. A workflow may improve answer quality while increasing generation, retrieval or reranking cost.

---

# Cost and Tradeoffs

Cost is often part of a tradeoff rather than an isolated fact.

Common RAG cost tradeoffs include:

* larger context windows may reduce retrieval complexity while increasing generation cost
* deeper retrieval may improve recall while increasing retrieval latency and reranking cost
* reranking may improve relevance while increasing model invocation cost
* frequent reindexing may improve freshness while increasing embedding and storage cost
* managed services may reduce operational burden while increasing provider dependency
* local models may reduce external provider spend while increasing infrastructure and maintenance cost

Cost tradeoffs should be represented with claims and evidence when they guide entity selection, architecture decisions or operational policy.

---

# Relationship Use

Cost knowledge should use canonical relationships when the association has reusable graph meaning.

Useful cost relationship patterns include:

```text
Workflow DEPENDS_ON Provider
Workflow DEPENDS_ON Language Model
Retriever REQUIRES Vector Database
Retriever OPTIONALLY_USES Reranker
Vector Database DEPENDS_ON Embedding Model
Provider PROVIDES Embedding Model
Provider PROVIDES Language Model
Benchmark EVALUATES Workflow
Evaluation Metric MEASURES Cost Attribute
Evidence SUPPORTS Claim
Evidence REFERENCES Source
```

Relationships should connect cost-sensitive knowledge to the entities that cause, measure or support it. Plain prose may explain a local cost observation, but reusable dependencies and evidence should be represented structurally.

---

# Evidence and Claims

Cost claims require evidence when they describe price, measured spend, comparative efficiency, production suitability or operational savings.

Useful evidence includes:

* provider pricing documentation
* benchmark measurement records
* evaluation run outputs
* usage logs
* deployment configuration
* workload descriptions
* invoices or cost reports
* papers that report measured cost

Examples of evidence-scoped cost claims include:

* a workflow has lower cost per answer than another workflow under a named benchmark
* a model reduces output token cost for a documented answer style
* a retriever lowers reranking cost by reducing candidate count without lowering recall under a specific metric
* a vector database deployment has predictable storage cost for a documented corpus size
* a local embedding model avoids provider token charges under a specific ingestion workload

Claims should identify whether the evidence supports current pricing, historical pricing, measured operational cost or estimated cost.

---

# Integration With Other Models

The Cost Model depends on existing RKM concepts instead of introducing a separate cost entity type.

Cost details may appear in:

* evaluation metrics that measure cost
* claims that compare cost or efficiency
* evidence that records measured or cited cost
* deployment context that affects pricing and operational responsibility
* tradeoffs that compare cost against quality, latency, reliability or governance
* workflow and component descriptions that expose cost-driving behavior

When cost knowledge becomes reusable across entities, it should be connected through stable identifiers, canonical relationships, evidence and references rather than left as unstructured prose.
