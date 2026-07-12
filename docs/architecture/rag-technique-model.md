# RAG Technique Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how RAG techniques are represented in the RAG Knowledge Model.

RAG techniques are reusable methods, strategies or algorithmic approaches that materially affect how retrieval-augmented generation systems ingest knowledge, retrieve context, assemble prompts, generate answers, evaluate outputs or coordinate workflows.

The RAG Technique Model answers the question:

> **How should RKM describe reusable RAG methods so they can be compared, related, evidenced and exported as structured knowledge?**

---

# Core Principle

A RAG technique is a first-class knowledge entity when the method has reusable semantic meaning across implementations.

It is not only a product feature, code path, prompt string, benchmark result or informal label.

A technique describes the method boundary, affected RAG stages, required inputs, produced artifacts, implementation dependencies, operational impact, claims, evidence and relationships to other entities.

```text
Technique REQUIRES Component
Technique USES Embedding Model
Technique OPTIONALLY_USES Reranker
Technique SUPPORTS Workflow
Framework IMPLEMENTS Technique
Paper INTRODUCES Technique
Benchmark EVALUATES Technique
Evaluation Metric MEASURES Technique
Technique HAS_ADVANTAGE Advantage
Technique HAS_LIMITATION Limitation
Technique HAS_TRADEOFF Tradeoff
Technique HAS_USE_CASE Use Case
```

Representing techniques explicitly makes RKM useful as a domain model rather than a loose catalog of RAG names.

---

# RAG Technique

A RAG Technique represents a reusable RAG method or strategy.

A technique may describe:

* baseline retrieval-augmented generation
* query transformation
* hybrid retrieval
* reranking
* context compression
* graph-based retrieval augmentation
* corrective or self-reflective retrieval
* iterative or multi-step retrieval
* chunking or indexing strategy
* evaluation method
* prompting method when modeled at the broader RAG-method level
* agentic orchestration pattern for retrieval and generation

The technique should be modeled when the method can be named, compared, implemented, evaluated or supported by evidence independently of one project.

Preferred:

```text
Hybrid retrieval technique that combines sparse and dense candidate retrieval before score fusion or reranking.
```

Avoid:

```text
Better search.
```

The avoided statement does not identify the method, affected stage, dependencies, outputs or evaluation basis.

---

# Technique Boundary

Every technique should have a clear boundary.

The boundary identifies:

* which RAG stages the technique affects
* what inputs the technique requires
* what artifacts the technique produces
* which components, models, retrievers, stores, prompts or workflows may implement it
* which assumptions must hold for the technique to work
* which operational characteristics are changed by the technique
* which claims require evidence

The boundary prevents a technique from absorbing unrelated system behavior.

For example, Graph RAG may describe graph construction, graph retrieval, graph traversal and answer synthesis patterns, but an RKM entity should state which parts are in scope for the specific technique being modeled.

---

# Technique Family

Technique family classifies the dominant method.

Canonical technique families include:

```text
Naive RAG
Query Transformation
Hybrid Retrieval
Reranking
Context Compression
Graph RAG
Agentic RAG
Corrective RAG
Self Reflective RAG
Iterative Retrieval
Multi Step Retrieval
Chunking
Indexing
Evaluation
Prompting
Other
```

The family should describe the primary method, not every implementation detail.

More specific knowledge should be represented through relationships, inputs, outputs, claims, evidence, advantages, limitations and tradeoffs.

---

# RAG Stage

RAG stage identifies where the technique affects the pipeline.

Common stages include:

* ingestion
* chunking
* embedding
* indexing
* query understanding
* retrieval
* reranking
* context assembly
* generation
* evaluation
* orchestration
* monitoring

A technique may affect multiple stages.

For example, corrective RAG may involve retrieval evaluation, fallback retrieval, answer generation and self-checking. Those stages should be represented explicitly rather than inferred from the technique name.

---

# Inputs and Outputs

Technique inputs and outputs should be modeled structurally when they carry reusable meaning.

Common inputs include:

* user query
* conversation history
* source document
* chunk
* embedding vector
* metadata filter
* graph node or edge
* retrieval candidate
* prompt template
* evaluation rubric
* reference answer

Common outputs include:

* rewritten query
* expanded query set
* indexed record
* ranked candidate list
* compressed context
* graph neighborhood
* retrieval plan
* grounded prompt
* generated answer
* citation set
* evaluation score

Inputs and outputs should be explicit when another component, workflow, prompt technique, retriever, reranker or evaluator consumes the result.

---

# Implementation Relationships

RKM separates a technique from the entities that implement or support it.

A technique describes the reusable method. A framework, component, retriever, reranker, language model, embedding model, vector database, graph database, prompt technique, agent or workflow may provide an implementation path.

Common relationship patterns include:

```text
Framework IMPLEMENTS Technique
Component IMPLEMENTS Technique
Retriever IMPLEMENTS Technique
Reranker IMPLEMENTS Technique
Prompt Technique SUPPORTS Technique
Agent SUPPORTS Technique
Workflow USES Technique
Technique REQUIRES Component
Technique DEPENDS_ON Dataset
Technique USES Embedding Model
Technique USES Language Model
Technique USES Vector Database
Technique USES Graph Database
Technique OPTIONALLY_USES Reranker
Provider SUPPORTS Framework
Provider PROVIDES Language Model
```

Implementation relationships should not imply evidence of quality unless a claim and supporting evidence are also present.

---

# Claims and Evidence

Claims about techniques must be scoped to the evidence that supports them.

Common technique claims include:

* improves retrieval recall
* improves answer faithfulness
* reduces hallucination risk
* improves citation quality
* reduces context length
* increases latency
* increases operational complexity
* depends on high-quality metadata
* performs better on multi-hop questions

Claims should identify the task, dataset, benchmark, metric, configuration and evaluation date when available.

Evidence may come from papers, benchmarks, documentation, experiments, implementations or structured observations.

```text
Paper INTRODUCES Technique
Paper DESCRIBES Technique
Benchmark EVALUATES Technique
Evaluation Metric MEASURES Technique
Evidence SUPPORTS Claim
```

Unsupported marketing statements should not be treated as established technique knowledge.

---

# Advantages, Limitations and Tradeoffs

Technique knowledge should distinguish advantages, limitations and tradeoffs.

An advantage describes a beneficial property under a stated context.

A limitation describes a constraint, weakness or failure mode.

A tradeoff describes an exchange between desirable and undesirable properties.

Examples:

```text
Technique HAS_ADVANTAGE Advantage
Technique HAS_LIMITATION Limitation
Technique HAS_TRADEOFF Tradeoff
Technique SOLVES Problem
Technique MITIGATES Problem
```

These entities should be linked to claims and evidence when they are used to justify architectural choices.

---

# Evaluation

Techniques should be evaluated in the context where they are used.

Relevant evaluation dimensions include:

* retrieval recall
* retrieval precision
* ranking quality
* context relevance
* answer faithfulness
* citation support
* answer correctness
* robustness to noisy context
* latency
* token cost
* indexing cost
* reproducibility

Evaluation results should not be generalized beyond the supported corpus, task, dataset, benchmark, metric, configuration or implementation.

For example, a query transformation technique that improves recall on one benchmark may increase latency or reduce precision in another context.

---

# Operational Characteristics

Operational characteristics describe how a technique affects practical RAG system behavior.

Important characteristics include:

* latency impact
* cost impact
* implementation complexity
* scalability impact
* quality impact
* observability requirements
* failure modes
* dependency sensitivity
* maintenance burden

Operational characteristics should be represented when they affect adoption, comparison, deployment or governance decisions.

---

# Relationship Use

Technique entities should use canonical relationship predicates when relationships have reusable semantic value.

Use relationships for durable graph knowledge, not for prose-only notes.

Preferred:

```text
Technique SPECIALIZES Technique
Technique COMPLEMENTS Technique
Technique ALTERNATIVE_TO Technique
Technique REQUIRES Component
Framework IMPLEMENTS Technique
Benchmark EVALUATES Technique
Technique HAS_USE_CASE Use Case
```

Avoid:

```text
Technique is kind of related to another technique.
```

The avoided statement does not provide a canonical predicate, direction or graph-exportable meaning.

---

# Modeling Guidance

Create a RAG Technique entity when:

* the method has a stable name or clear reusable boundary
* multiple implementations can realize the method
* evidence or claims can be attached to the method
* the method affects RAG behavior or quality
* the method can be compared with alternatives
* graph relationships add value beyond prose

Do not create a RAG Technique entity when:

* the concept is only a specific product feature
* the content is only a parameter value
* the idea is only a one-off implementation detail
* the statement is only an unevidenced quality claim
* an existing entity type such as Component, Prompt Technique, Retriever, Reranker, Dataset, Benchmark or Evaluation Metric is the more precise model

When in doubt, model the reusable method as a Technique and connect implementation-specific knowledge through relationships.
