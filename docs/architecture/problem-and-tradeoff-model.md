# Problem and Tradeoff Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how problems, advantages, limitations, tradeoffs, use cases, anti patterns and common mistakes are represented in the RAG Knowledge Model.

The Problem and Tradeoff Model answers the question:

> **Why would someone choose, avoid, constrain or evaluate a RAG entity in a specific context?**

---

# Core Principle

Problems and tradeoffs are first-class knowledge because they explain motivation, suitability and risk.

They are not only descriptive notes.

They connect techniques, components, models, workflows, tools, datasets and evaluation methods to the reasons they matter.

```text
Technique SOLVES Problem
Technique HAS_ADVANTAGE Advantage
Technique HAS_LIMITATION Limitation
Technique HAS_TRADEOFF Tradeoff
Technique HAS_USE_CASE Use Case
Pattern HAS_ANTI_PATTERN Anti Pattern
Pattern HAS_COMMON_MISTAKE Common Mistake
```

These relationships help RKM consumers compare alternatives, select designs and understand evidence-backed claims.

---

# Problem

A Problem is a recurring challenge, failure mode, requirement gap or quality issue in RAG systems.

Examples include:

* low retrieval recall
* poor citation faithfulness
* stale indexed content
* ambiguous user queries
* high answer latency
* expensive reranking
* weak context compression
* insufficient observability

Problems should be scoped clearly enough that a relationship to a technique, component or workflow is meaningful.

Preferred:

```text
Low retrieval recall for semantically diverse user queries.
```

Avoid:

```text
Bad retrieval.
```

The avoided statement is too broad to support comparison, evidence or remediation guidance.

---

# Advantage

An Advantage is a beneficial property of an entity in a defined context.

Advantages may describe improvements in:

* retrieval quality
* grounding
* explainability
* latency
* cost
* scalability
* maintainability
* interoperability
* safety
* evaluation coverage

Advantages should include the condition under which the benefit applies whenever that condition is known.

Example:

```text
Hybrid retrieval can improve recall when user queries contain both semantic intent and exact keywords.
```

An advantage should not be treated as universal unless evidence supports that scope.

---

# Limitation

A Limitation is a known constraint, weakness or boundary of usefulness.

Limitations may come from:

* model behavior
* data quality
* index freshness
* infrastructure constraints
* algorithmic assumptions
* evaluation blind spots
* operational complexity
* provider availability

Example:

```text
Dense retrieval may miss exact identifiers that are rare or out of distribution for the embedding model.
```

Limitations should be represented explicitly when they affect adoption, architecture choice, evaluation design or operational risk.

---

# Tradeoff

A Tradeoff is a decision relationship where improving one property may worsen, constrain or complicate another property.

Common RAG tradeoffs include:

* recall versus latency
* precision versus context diversity
* chunk size versus retrieval granularity
* reranking quality versus cost
* citation coverage versus answer brevity
* agent flexibility versus predictability
* graph structure richness versus ingestion complexity

Tradeoffs should identify both sides of the decision.

Preferred:

```text
Increasing top-k retrieval can improve recall but may increase context assembly cost and noise.
```

Avoid:

```text
Top-k has pros and cons.
```

The avoided statement does not identify the properties being exchanged.

---

# Use Case

A Use Case is a recurring application context in which an entity is suitable, commonly applied or intentionally evaluated.

Examples include:

* customer support question answering
* enterprise document search
* compliance research
* codebase assistance
* literature review
* medical policy lookup
* legal document analysis
* internal knowledge assistant

Use cases should describe the task context, not only the industry label.

Preferred:

```text
Answering employee questions from versioned internal policy documents.
```

Avoid:

```text
Enterprise.
```

The avoided statement is a market category, not a use case.

---

# Anti Pattern

An Anti Pattern is a recurring design or implementation practice that tends to produce poor outcomes in RAG systems.

Examples include:

* retrieving too few candidates before reranking
* using stale indexes for time-sensitive answers
* mixing untrusted retrieved text directly into system instructions
* evaluating only generated answer fluency
* treating citation presence as citation faithfulness
* chunking documents without preserving source boundaries

Anti patterns should explain the harmful structure or behavior, not merely state that a design is poor.

---

# Common Mistake

A Common Mistake is a frequent modeling, implementation, evaluation or operational error.

Common mistakes are usually narrower than anti patterns and may be correctable with guidance.

Examples include:

* comparing retrieval methods without a fixed corpus
* changing chunk size and embedding model in the same experiment
* storing display names as relationship targets instead of stable identifiers
* reporting benchmark scores without dataset version
* using only one query style during retrieval evaluation

Common mistakes should be stated in a way that helps authors avoid ambiguous or unreproducible knowledge.

---

# Relationship Use

Problems, advantages, limitations, tradeoffs and use cases should be connected through canonical relationships when they have reusable semantic value.

Common relationship patterns include:

```text
Technique SOLVES Problem
Technique MITIGATES Problem
Technique HAS_ADVANTAGE Advantage
Technique HAS_LIMITATION Limitation
Technique HAS_TRADEOFF Tradeoff
Technique HAS_USE_CASE Use Case
Workflow HAS_LIMITATION Limitation
Evaluation Metric MEASURES Problem
Benchmark EVALUATES Technique
Pattern HAS_ANTI_PATTERN Anti Pattern
Framework HAS_COMMON_MISTAKE Common Mistake
```

Relationship targets may initially be represented as structured claim objects or named concepts when the target concept is not yet promoted to a specialized entity type.

Stable identifiers should be used whenever the target concept is modeled as an entity.

---

# Claims and Evidence

Claims are required when a problem, advantage, limitation, tradeoff or use case expresses an assertion that needs review, confidence or evidence.

Examples:

```text
Reranking improves precision when the initial retriever returns many weakly relevant candidates.
```

```text
Smaller chunks can improve retrieval granularity but may reduce available context for answer synthesis.
```

Evidence may come from:

* papers
* benchmark results
* dataset documentation
* framework documentation
* implementation examples
* experiment reports
* production traces
* maintainer analysis

Evidence should be linked to the claim it supports, not only to the entity document.

---

# Context and Qualifiers

Problems and tradeoffs are often context-dependent.

Important qualifiers include:

* corpus type
* query type
* model version
* embedding model
* retriever type
* reranker type
* latency budget
* cost budget
* domain sensitivity
* evaluation dataset
* deployment environment

Qualifiers should be represented structurally when they affect whether a claim is true.

Example:

```text
Hybrid retrieval is especially relevant when exact lexical matches and semantic similarity are both needed.
```

---

# Boundaries

Use this model for decision-relevant knowledge.

Do not create separate problem or tradeoff records for generic prose that does not support comparison, evaluation, graph export or implementation guidance.

A limitation should not duplicate an advantage with negative wording.

A tradeoff should not duplicate two unrelated claims.

A use case should not duplicate an entity category.

---

# Graph Export

Graph export should preserve:

* source entity identity
* relationship predicate
* target concept or entity
* claim statement
* evidence links
* confidence
* qualifiers
* status
* version information

This enables queries such as:

* Which techniques solve low retrieval recall?
* Which approaches trade latency for retrieval quality?
* Which use cases require citation faithfulness?
* Which components have known limitations for time-sensitive data?
* Which anti patterns are associated with agentic RAG workflows?

---

# Schema Implications

Future schemas may introduce specialized entity types for Problem, Advantage, Limitation, Tradeoff, Use Case, Anti Pattern and Common Mistake.

Before specialized schemas are introduced, the shared identity model must support the corresponding `identity.entityType` values.

Until then, these concepts should be represented through structured claims, canonical relationships, evidence and carefully scoped named concepts within existing knowledge entities.
