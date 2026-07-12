# Query Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how query knowledge is represented in the RAG Knowledge Model.

Query knowledge explains how user questions, system-generated requests, transformed queries and retrieval constraints shape Retrieval-Augmented Generation behavior.

The Query Model answers the question:

> **How should RKM describe the query artifacts and transformations that determine what a RAG system retrieves, evaluates and uses for generation?**

---

# Core Principle

A query is an artifact with context, intent, constraints and lifecycle.

It is not only a text string submitted to a retriever.

```text
Prompt Technique TRANSFORMS Query
Retriever CONSUMES Query
Retriever PRODUCES Retrieval Result
Evaluation Metric MEASURES Query Transformation Quality
Evidence SUPPORTS Claim
```

Representing query knowledge explicitly allows RKM to compare retrieval behavior, preserve evaluation context and explain why a system selected particular evidence.

---

# Query

A Query is an artifact that expresses an information need, command, evaluation prompt or intermediate request used by a RAG workflow.

Queries may originate from:

* a user question
* a conversation turn
* a workflow step
* an agent planning action
* a prompt technique
* an evaluation task
* a benchmark example
* a monitoring or diagnostic process

A query should be modeled structurally when it affects retrieval, routing, context assembly, evaluation, cost, latency, safety or reproducibility.

Preferred:

```text
Standalone retrieval query derived from a conversational user question and constrained to product documentation published after a specific release date.
```

Avoid:

```text
Search text.
```

The avoided statement does not identify origin, intent, constraints or downstream use.

---

# Query Boundary

Every query representation should define a clear boundary.

The boundary identifies:

* the source of the query
* the query text or structured request
* the intended retrieval or reasoning task
* the context used to construct the query
* the constraints carried with the query
* the artifact or decision expected as output
* the workflow stage that consumes the query

Boundaries matter because a user question, rewritten query, database query and evaluation prompt may all contain natural language while serving different RAG roles.

---

# Query Intent

Query intent describes the information need or action requested by the query.

Common query intents include:

* factual lookup
* explanatory answer
* comparison
* summarization
* troubleshooting
* citation request
* source discovery
* entity lookup
* relationship lookup
* multi-hop reasoning
* evaluation judgment
* tool or retriever selection

Intent should be explicit when it affects retrieval strategy, prompt technique selection, evaluation metric choice or answer format.

---

# Query Context

Query context is the information available when the query is created or interpreted.

Common context includes:

* conversation history
* user profile or role
* task instructions
* selected corpus
* document metadata
* access policy
* locale or language
* time range
* previous retrieval results
* evaluation rubric
* benchmark task definition

Context should be separated from the query text when downstream behavior depends on knowing whether information came from the user, the system, retrieved evidence or evaluation setup.

---

# Query Constraints

Query constraints restrict the acceptable retrieval targets, sources, formats or decisions.

Important constraints include:

* corpus boundary
* metadata filter
* date or version range
* language
* modality
* access-control rule
* freshness requirement
* source type
* retrieval depth
* ranking objective
* citation requirement
* abstention policy

Constraints should be represented structurally when they affect reproducibility, compliance, evaluation results or graph export.

---

# Query Transformation

Query transformation changes a query before another stage consumes it.

Common transformations include:

* query rewriting
* query expansion
* query decomposition
* hypothetical document generation
* translation
* normalization
* metadata filter extraction
* natural language to structured query translation
* routing query generation

A transformation should identify the input query, output query, transformation method, responsible entity and evidence for quality claims.

Examples:

```text
Prompt Technique TRANSFORMS Query
Technique SUPPORTS Query Transformation
Component PRODUCES Query
Retriever CONSUMES Query
```

Query transformation quality should not be inferred only from downstream answer quality. Evaluation should preserve the transformed query, retrieval target, dataset, metric and protocol when available.

---

# Structured Query

A Structured Query is a query artifact with machine-readable fields.

Structured queries may include:

* query text
* intent label
* target entity type
* filters
* sort order
* retrieval depth
* scoring preferences
* required output shape
* citation requirements
* safety or policy constraints

Structured query fields should be stable enough for validation, comparison and export. Free-form text may still be retained for readability and traceability.

---

# Retrieval Role

Queries connect upstream intent to downstream retrieval behavior.

Important retrieval knowledge includes:

* which retriever consumes the query
* which index or store is required
* which targets can be returned
* which ranking and filtering rules apply
* whether reranking changes the result set
* whether query context is visible to retrieval
* whether constraints are enforced before or after retrieval

Relationships should be used when the dependency has reusable semantic meaning.

```text
Retriever CONSUMES Query
Retriever USES Embedding Model
Retriever REQUIRES Vector Database
Reranker CONSUMES Retrieval Result
Reranker PRODUCES Ranked Result
```

---

# Evaluation Role

Queries are central to evaluating retrieval, generation and grounding behavior.

Evaluation records should distinguish:

* original user query
* rewritten query
* expanded query
* decomposed subquery
* structured query
* generated retrieval plan
* reference query supplied by a benchmark

Benchmarks and metrics should make clear which query artifact is being evaluated.

```text
Benchmark EVALUATES Retriever
Evaluation Metric MEASURES Query Transformation Quality
Dataset PROVIDES Query
Evidence SUPPORTS Claim
```

Claims about query transformation or retrieval quality should identify the dataset, query set, transformation method, retriever, retrieval depth, metric and evaluation date when available.

---

# Relationship Guidance

Use canonical relationships to connect query knowledge to other RKM concepts.

Recommended relationships include:

```text
Prompt Technique TRANSFORMS Query
Component PRODUCES Query
Retriever CONSUMES Query
Retriever PRODUCES Retrieval Result
Evaluation Metric MEASURES Query Transformation Quality
Benchmark EVALUATES Retriever
Evidence SUPPORTS Claim
Paper DESCRIBES Query Transformation Method
```

Use relationship objects when a query-related statement has evidence, confidence, lifecycle metadata or reusable graph meaning.

---

# Modeling Guidance

Model query knowledge when it explains system behavior.

Do not create a separate entity for every transient query unless the query is reused, evaluated, cited, benchmarked or needed to explain a claim.

Prefer structured representation when the query has semantic parts that downstream systems need to inspect.

Examples of structured query knowledge include:

* original question and rewritten retrieval query
* decomposition into subqueries
* metadata filters extracted from natural language
* routing decision produced from query intent
* evaluation query linked to reference answer and relevance judgments
* query constraints that affect source eligibility

Query artifacts should link back to claims, evidence and references when they support assertions about retrieval quality, grounding, faithfulness or workflow behavior.
