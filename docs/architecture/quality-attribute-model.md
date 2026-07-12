# Quality Attribute Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how quality attributes are represented in the RAG Knowledge Model.

Quality attributes describe measurable or assessable properties of RAG entities, systems and workflows. They explain what a model, component, technique, benchmark, provider or workflow is expected to improve, preserve, trade off or constrain.

The Quality Attribute Model answers the question:

> **Which quality dimension is being discussed, how is it assessed and how does it relate to claims, evidence and evaluation?**

---

# Core Principle

A quality attribute is structured knowledge when it carries reusable assessment meaning.

It is not only an adjective in prose.

```text
Evaluation Metric MEASURES Quality Attribute
Benchmark EVALUATES Component
Evidence SUPPORTS Claim
Component DEPENDS_ON Provider
Technique REQUIRES Component
```

RKM may describe quality attributes before representing them as first-class identity-backed entities. A quality attribute becomes a candidate entity only when it needs stable identity, relationships, evidence, lifecycle metadata or independent governance across the repository.

---

# Quality Attribute

A Quality Attribute is a named assessment dimension for RAG behavior.

Common quality attributes include:

* retrieval quality
* ranking quality
* answer correctness
* faithfulness
* citation faithfulness
* context relevance
* latency
* throughput
* cost
* freshness
* scalability
* reliability
* reproducibility
* observability
* privacy
* security
* safety
* maintainability

Quality attributes should be specific enough to support evaluation and comparison.

Preferred:

```text
Citation faithfulness measures whether cited sources support the generated answer spans they are attached to.
```

Avoid:

```text
Better quality.
```

The avoided statement does not identify the quality dimension, assessment target or evaluation meaning.

---

# Attribute Scope

Every quality attribute statement should identify its scope.

The scope explains what the attribute applies to:

* an entity, such as a retriever, reranker, language model, framework or provider
* a component boundary, such as a context assembler or evaluator
* a workflow stage, such as retrieval, reranking, generation or evaluation
* an artifact, such as a retrieved chunk, assembled context, citation or answer
* an end-to-end RAG system behavior

The same attribute may have different meaning at different scopes.

For example, latency for a retriever may refer to candidate retrieval time, while latency for an end-to-end workflow may include query rewriting, retrieval, reranking, prompt assembly, generation and post-processing.

---

# Assessment Method

A quality attribute should identify how it can be assessed when that information is known.

Assessment methods may include:

* evaluation metrics
* benchmarks
* datasets
* protocol-defined experiments
* human review
* operational observations
* policy checks
* reproducibility procedures
* qualitative analysis supported by references

When a quality attribute is measured by an Evaluation Metric, the metric should define what it consumes, what it produces and which target behavior it measures.

When a quality attribute is asserted through a Claim, the claim should be linked to Evidence and References rather than left as unsupported prose.

---

# Tradeoffs

Quality attributes often interact through tradeoffs.

Common RAG tradeoffs include:

* retrieval quality versus latency
* context completeness versus token cost
* reranking quality versus throughput
* freshness versus reproducibility
* privacy versus observability
* robustness versus implementation complexity
* citation precision versus answer fluency
* provider capability versus portability

Tradeoffs should be represented explicitly when they affect selection, comparison or evaluation.

A tradeoff statement should identify:

* the improved attribute
* the degraded or constrained attribute
* the entity or workflow where the tradeoff occurs
* the conditions under which the tradeoff is expected
* the claim, evidence or reference supporting the statement

---

# Claims and Evidence

Quality attribute statements often appear as claims.

Examples include:

* a reranker improves ranking quality
* a chunking strategy improves context relevance
* a provider reduces latency
* a workflow improves citation faithfulness
* an evaluation metric measures answer correctness

These statements should be modeled as claims when they assert something about an entity.

Evidence should identify the benchmark, dataset, experiment, observation, paper, documentation or other source that supports, contradicts or qualifies the claim.

References should identify the source material where the evidence is described.

This separation keeps the quality attribute, the asserted claim and the supporting source distinct.

---

# Relationship Use

Quality attributes should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Evaluation Metric MEASURES Quality Attribute
Benchmark EVALUATES Component
Benchmark USES Dataset
Component DEPENDS_ON Provider
Technique REQUIRES Component
Framework IMPLEMENTS Technique
Evidence SUPPORTS Claim
```

Relationship targets should use stable identifiers whenever the target is represented as an RKM entity.

Until quality attributes have identity support, they should be represented as structured fields, controlled values, claim content or documented concepts rather than as specialized entity documents.

---

# Quality Attribute vs Evaluation Metric

A quality attribute is the dimension being assessed.

An evaluation metric is the method or scoring function used to assess that dimension.

Example:

```text
Quality attribute: citation faithfulness
Evaluation metric: percentage of generated citation spans supported by retrieved source passages
```

Multiple metrics may measure the same quality attribute. A single metric may also combine several attributes, which should be documented when it affects interpretation.

---

# Quality Attribute vs Metadata

Metadata describes the RKM document and its lifecycle.

Quality attributes describe the modeled RAG entity or behavior.

For example, `metadata.status` indicates whether an RKM document is draft, reviewed or published. Reliability describes whether the modeled system, provider, workflow or component behaves consistently under expected conditions.

Quality attributes should not be stored as metadata merely because they are descriptive.

---

# Modeling Boundary

In the current RKM architecture, quality attributes are cross-cutting assessment dimensions rather than identity-backed entity types.

They may appear in:

* specialized schema detail objects
* component responsibilities and quality attribute fields
* evaluation metric definitions
* benchmark task descriptions
* claims
* evidence interpretation
* architecture documentation

A future quality attribute registry or specialized schema should be added only after shared identity support and entity registry support exist for that entity type.
