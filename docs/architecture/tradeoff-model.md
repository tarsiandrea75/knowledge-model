# Tradeoff Model

## RAG Knowledge Model (RKM)

Version: 1.0.0

---

# Purpose

This document defines how tradeoffs are represented in the RAG Knowledge Model.

Tradeoffs describe decision tensions where improving, emphasizing or selecting one RAG property may degrade, constrain or complicate another property.

The Tradeoff Model answers the question:

> **What is gained, what is constrained, and under which conditions does that exchange matter?**

---

# Core Principle

A tradeoff is first-class knowledge when it affects selection, comparison, evaluation, operation or governance.

It is not only a balanced opinion or a list of pros and cons.

A tradeoff explains a structured tension between properties and should be linked to claims, evidence, advantages, limitations, affected quality attributes and use cases when those links have reusable semantic meaning.

```text
Technique HAS_TRADEOFF Tradeoff
Retriever HAS_TRADEOFF Tradeoff
Workflow HAS_TRADEOFF Tradeoff
Use Case HAS_TRADEOFF Tradeoff
Evaluation Metric MEASURES Tradeoff
Evidence SUPPORTS Claim
```

Tradeoffs make RKM useful for design comparison because they preserve the conditions under which one improvement may create another cost, risk or constraint.

---

# Tradeoff

A Tradeoff is a decision tension where one side of a design, model, technique, workflow or operational choice is beneficial while another side is degraded, constrained or made more complex.

Tradeoffs may apply to:

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

A tradeoff should identify the affected entity, the positive side, the negative side and the context in which the exchange matters.

Preferred:

```text
Increasing top-k retrieval can improve recall when relevant evidence is distributed across passages, but may increase latency and context noise.
```

Avoid:

```text
Top-k has pros and cons.
```

The avoided statement does not identify the decision variable, the properties being exchanged or the conditions under which the tradeoff applies.

---

# Tradeoff Boundary

Every tradeoff should have a clear boundary.

The boundary identifies:

* the affected entity or entity class
* the decision variable or design choice
* the positive side of the exchange
* the negative side of the exchange
* the conditions under which the exchange applies
* the affected quality attributes
* the use cases or workflows where the tradeoff matters
* the evidence or observation supporting the tradeoff

Boundaries prevent general design advice from being modeled as universal RKM knowledge.

For example, larger chunks may improve answer completeness in workflows that retrieve few passages, while reducing retrieval precision in workflows that need narrow evidence spans.

---

# Tradeoff Type

Tradeoff type describes the primary nature of the decision tension.

Canonical tradeoff types include:

```text
Retrieval Quality Tradeoff
Ranking Quality Tradeoff
Grounding Tradeoff
Citation Tradeoff
Latency Tradeoff
Cost Tradeoff
Scalability Tradeoff
Freshness Tradeoff
Context Window Tradeoff
Complexity Tradeoff
Observability Tradeoff
Governance Tradeoff
Operational Tradeoff
Other
```

The tradeoff type should describe the dominant tension, not every secondary effect.

---

# Positive and Negative Sides

A tradeoff should preserve both sides of the decision.

The positive side describes the property that may improve, increase or become easier to satisfy.

The negative side describes the property that may degrade, increase in cost, become constrained or require additional complexity.

Examples:

```text
Positive side: Higher top-k retrieval can increase recall.
Negative side: Higher top-k retrieval can increase reranking cost and context noise.
```

```text
Positive side: Smaller chunks can improve retrieval granularity.
Negative side: Smaller chunks can reduce answer completeness when neighboring context is not retrieved.
```

Both sides should be scoped to the same decision context so RKM consumers can compare alternatives without treating one side as universally dominant.

---

# Decision Variables

A decision variable is a parameter, design choice or operational control that influences the tradeoff.

Common decision variables include:

* chunk size
* overlap size
* top-k retrieval count
* reranking depth
* embedding model choice
* sparse and dense score weighting
* context window budget
* citation strictness
* freshness interval
* cache duration
* human review threshold
* evaluation dataset scope

Decision variables should be represented structurally when they affect reproducibility, evaluation or comparison.

Preferred:

```text
Increasing reranking depth may improve top-ranked precision, but can increase latency and provider cost.
```

Avoid:

```text
Reranking is expensive.
```

The avoided statement omits the variable that creates the exchange.

---

# Scope and Conditions

Tradeoffs should preserve scope.

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

Scope is required when a tradeoff would otherwise sound universal.

Preferred:

```text
Strict citation verification can improve groundedness in regulated policy lookup, but may increase answer abstention when source documents are incomplete.
```

Avoid:

```text
Citation verification improves quality but reduces answers.
```

The avoided statement drops the use case and source condition that make the tradeoff meaningful.

---

# Relationship Use

Tradeoffs should be connected through canonical relationships when those relationships have reusable semantic value.

Common relationship patterns include:

```text
Technique HAS_TRADEOFF Tradeoff
Framework HAS_TRADEOFF Tradeoff
Retriever HAS_TRADEOFF Tradeoff
Reranker HAS_TRADEOFF Tradeoff
Embedding Model HAS_TRADEOFF Tradeoff
Language Model HAS_TRADEOFF Tradeoff
Vector Database HAS_TRADEOFF Tradeoff
Graph Database HAS_TRADEOFF Tradeoff
Workflow HAS_TRADEOFF Tradeoff
Agent HAS_TRADEOFF Tradeoff
Use Case HAS_TRADEOFF Tradeoff
Evaluation Metric MEASURES Tradeoff
Evidence SUPPORTS Claim
```

Relationship targets should use stable identifiers whenever the target concept is represented as an RKM entity.

Plain prose may explain local design considerations, but reusable tradeoffs should be represented structurally so they can support graph export, comparison and evidence-backed selection.

---

# Tradeoffs vs Advantages

An Advantage states a beneficial property.

A Tradeoff states an exchange between properties.

Example:

```text
Advantage: Hybrid retrieval can improve recall when queries combine semantic intent with exact keywords.
Tradeoff: Hybrid retrieval can improve recall but may increase ranking complexity when dense and sparse scores must be normalized.
```

An advantage may describe one side of a tradeoff, but the tradeoff should remain explicit when a design choice creates a cost, constraint or risk.

---

# Tradeoffs vs Limitations

A Limitation states a boundary or weakness.

A Tradeoff states a decision tension that includes both a benefit and a cost.

Example:

```text
Limitation: Dense retrieval may miss rare exact identifiers.
Tradeoff: Adding sparse retrieval can improve exact identifier recall but may increase index complexity and tuning effort.
```

The limitation explains where an entity may be weak.

The tradeoff explains the exchange involved in addressing or accepting that weakness.

---

# Claims and Evidence

Tradeoffs often need claims because they express contextual assertions about competing properties.

Examples of tradeoff claims include:

* increasing top-k retrieval improves recall in a specific benchmark but increases latency
* smaller chunks improve retrieval granularity for narrow answers but reduce completeness for multi-section answers
* stricter citation verification improves groundedness but increases abstention
* more frequent indexing improves freshness but increases operational cost
* broader evaluation datasets improve coverage but reduce diagnostic specificity

Evidence should identify the source, evaluation context, decision variable, observed positive side and observed negative side.

Evidence may come from:

* papers
* benchmarks
* datasets
* framework documentation
* provider documentation
* experiment reports
* production traces
* maintainer analysis

Evidence should support the scoped tradeoff claim, not only one side of the tradeoff.

---

# Modeling Guidance

Represent a tradeoff structurally when:

* it affects entity selection or comparison
* it explains why one design is suitable in one context but unsuitable in another
* it is reused across multiple entities
* it affects a quality attribute
* it links an advantage to a limitation
* it constrains evaluation design
* it depends on evidence or confidence

Keep a tradeoff in prose when it is only local explanatory context and has no reusable semantic role.

Do not model vague balanced statements as tradeoffs. A valid tradeoff must identify what changes, what improves, what is constrained and the conditions under which the exchange applies.
