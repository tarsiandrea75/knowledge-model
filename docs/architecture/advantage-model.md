# Advantage Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how advantages are represented in the RAG Knowledge Model.

Advantages describe beneficial properties, improvements or suitability reasons for RAG entities in defined contexts.

The Advantage Model answers the question:

> **Why is a RAG entity useful in a specific context, and how should that benefit be represented without turning it into unsupported marketing language?**

---

# Core Principle

An advantage is first-class knowledge when it affects selection, comparison, evaluation, operation or governance.

It is not only a positive note.

An advantage explains a beneficial property of an entity and should be linked to claims, evidence, affected quality attributes, use cases, limitations and tradeoffs when those links have reusable semantic meaning.

```text
Technique HAS_ADVANTAGE Advantage
Framework HAS_ADVANTAGE Advantage
Retriever HAS_ADVANTAGE Advantage
Workflow HAS_ADVANTAGE Advantage
Advantage SUPPORTS Use Case
Evidence SUPPORTS Claim
```

Advantages make RKM useful for comparison because they preserve the conditions under which an entity is expected to help.

---

# Advantage

An Advantage is a beneficial property or outcome associated with an entity in a defined context.

Advantages may apply to:

* techniques
* frameworks
* components
* retrievers
* rerankers
* models
* databases
* datasets
* benchmarks
* evaluation metrics
* agents
* workflows
* tools
* providers
* use cases

An advantage should identify the affected entity, the beneficial behavior and the context in which the benefit matters.

Preferred:

```text
Hybrid retrieval can improve recall when user queries combine semantic intent with exact identifiers or keywords.
```

Avoid:

```text
Hybrid retrieval is better.
```

The avoided statement is too broad to support evidence, comparison or scoped applicability.

---

# Advantage Boundary

Every advantage should have a clear boundary.

The boundary identifies:

* the entity or entity class receiving the advantage
* the behavior or quality being improved
* the baseline or comparison context when known
* the condition under which the advantage applies
* the affected quality attributes
* the use cases or workflows where the advantage matters
* the evidence or observation supporting the advantage

Boundaries prevent broad product, model or technique descriptions from being modeled as universal benefits.

For example, reranking may improve precision in a workflow that retrieves a broad candidate set, while providing little benefit when the initial retriever already returns a small, highly precise set.

---

# Advantage Type

Advantage type describes the primary nature of the benefit.

Canonical advantage types include:

```text
Retrieval Quality Advantage
Ranking Quality Advantage
Grounding Advantage
Citation Advantage
Latency Advantage
Cost Advantage
Scalability Advantage
Freshness Advantage
Explainability Advantage
Interoperability Advantage
Observability Advantage
Governance Advantage
Operational Advantage
Other
```

The advantage type should describe the dominant benefit, not every secondary consequence.

---

# Scope and Conditions

Advantages should preserve scope.

Important scope dimensions include:

* corpus type
* query style
* language
* modality
* document freshness
* source trust level
* benchmark or dataset
* model version
* provider behavior
* latency budget
* cost budget
* governance requirement
* deployment environment

Scope is required when an advantage would otherwise sound universal.

Preferred:

```text
Small chunks can improve retrieval granularity when source passages are short and answerable from narrow context.
```

Avoid:

```text
Small chunks improve retrieval.
```

The avoided statement drops the condition that makes the advantage meaningful.

---

# Baseline

An advantage is often comparative.

When a benefit is comparative, the baseline should be explicit.

Possible baselines include:

* another technique
* an earlier workflow version
* a simpler component configuration
* a default provider capability
* a benchmark reference system
* a manual process
* an unstated baseline recorded as unknown

Baseline clarity prevents RKM from treating relative claims as absolute facts.

Preferred:

```text
Reranking can improve top-ranked result precision compared with using initial retriever scores alone.
```

Avoid:

```text
Reranking improves precision.
```

The avoided statement does not state what the improvement is measured against.

---

# Evidence and Confidence

Advantages should be evidence-backed when they affect selection, evaluation, trust or operational use.

Evidence may include:

* benchmark results
* evaluation reports
* papers
* official documentation
* implementation documentation
* source code
* observed production behavior
* reproducible experiments

Claims about advantages should include confidence when the evidence is limited, context-specific or indirect.

An advantage supported only by anecdotal or implementation-specific evidence should not be generalized across all RAG systems.

---

# Relationship Use

Advantages should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Technique HAS_ADVANTAGE Advantage
Framework HAS_ADVANTAGE Advantage
Retriever HAS_ADVANTAGE Advantage
Reranker HAS_ADVANTAGE Advantage
Embedding Model HAS_ADVANTAGE Advantage
Language Model HAS_ADVANTAGE Advantage
Vector Database HAS_ADVANTAGE Advantage
Graph Database HAS_ADVANTAGE Advantage
Workflow HAS_ADVANTAGE Advantage
Agent HAS_ADVANTAGE Advantage
Use Case HAS_ADVANTAGE Advantage
Evaluation Metric MEASURES Advantage
Benchmark EVALUATES Technique
Evidence SUPPORTS Claim
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may explain local benefits, but reusable advantages should be represented structurally so they can support graph export and comparison.

---

# Advantages vs Limitations

An Advantage states a beneficial property.

A Limitation states a constraint or boundary.

Example:

```text
Advantage: Hybrid retrieval can improve recall when queries contain both semantic intent and exact keywords.
Limitation: Hybrid retrieval can add ranking complexity when dense and sparse scores are difficult to normalize.
```

Both statements may be true for the same entity.

RKM should preserve both instead of collapsing them into a general positive or negative judgment.

---

# Advantages vs Tradeoffs

An Advantage states a benefit.

A Tradeoff states an exchange between properties.

Example:

```text
Advantage: Increasing retrieved context can improve answer completeness when relevant evidence is distributed across passages.
Tradeoff: Increasing retrieved context can improve completeness but may increase latency, cost and context noise.
```

An advantage may be one side of a tradeoff, but the tradeoff should remain explicit when improving one property can worsen another.

---

# Modeling Guidance

Represent an advantage structurally when:

* it affects entity selection or comparison
* it is reused across multiple entities
* it supports a use case
* it depends on evidence or confidence
* it affects a quality attribute
* it is part of a known tradeoff
* it constrains evaluation design

Keep an advantage in prose when it is only local explanatory context and has no reusable semantic role.

Do not represent advantages as universal claims unless the evidence supports that scope.
